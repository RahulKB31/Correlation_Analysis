import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, mean_absolute_percentage_error
from scipy.stats import skew

# Paths to save and load models
MODEL_PATH = 'model_trained.pkl'
IMPUTER_PATH = 'inductance_imputer.pkl'
TRANSFORMER_PATH = 'transformer.pkl'

def train_and_predict_stig_balance_ap_stig(
    excel_file,
    new_inductance_values,
    test_size=0.2,
    random_state=42
):
    # Read the data from the Excel file
    df = pd.read_excel(excel_file)

    # Define the inductance columns and the STIG output columns
    inductance_cols = ['L1X', 'L1Y', 'L2X', 'L2Y', 'L3X', 'L3Y', 'L4X', 'L4Y']
    stig_cols = [col for col in df.columns if col.startswith("AP_STIG")]

    # Check if model and imputer files exist
    if os.path.exists(MODEL_PATH) and os.path.exists(IMPUTER_PATH) and os.path.exists(TRANSFORMER_PATH):
        # If models and transformers exist, load them
        model_trained = joblib.load(MODEL_PATH)
        inductance_imputer = joblib.load(IMPUTER_PATH)
        transformer = joblib.load(TRANSFORMER_PATH)
    else:
        # If models do not exist, train a new model

        # Impute missing values for inductance columns
        inductance_imputer = SimpleImputer(strategy='mean')
        df_inductance = df[inductance_cols]
        df_inductance_imputed = inductance_imputer.fit_transform(df_inductance)

        # Impute missing values for STIG columns
        stig_imputer = SimpleImputer(strategy='mean')
        df_stig = stig_imputer.fit_transform(df[stig_cols])

        # Split data into train and test
        X_train, X_test, y_train, y_test = train_test_split(
            df_inductance_imputed, df_stig, test_size=test_size, random_state=random_state
        )

        # Identify skewed columns and apply transformations
        skewed_columns = [col for col in inductance_cols if skew(df[col]) > 0.5]

        transformer = {}

        # Apply transformation for skewed data (PowerTransformer) and normal data (StandardScaler)
        for col in inductance_cols:
            if col in skewed_columns:
                transformer[col] = PowerTransformer(method='yeo-johnson')
            else:
                transformer[col] = StandardScaler()

        # Apply transformations to the training and test data
        for col in inductance_cols:
            if col in skewed_columns:
                X_train[:, inductance_cols.index(col)] = transformer[col].fit_transform(
                    X_train[:, [inductance_cols.index(col)]]).flatten()
                X_test[:, inductance_cols.index(col)] = transformer[col].transform(
                    X_test[:, [inductance_cols.index(col)]]).flatten()
            else:
                X_train[:, inductance_cols.index(col)] = transformer[col].fit_transform(
                    X_train[:, [inductance_cols.index(col)]]).flatten()
                X_test[:, inductance_cols.index(col)] = transformer[col].transform(
                    X_test[:, [inductance_cols.index(col)]]).flatten()

        # Train the XGBoost model
        xgb_base_model = XGBRegressor(
            objective="reg:squarederror",
            verbosity=1,
            n_jobs=-1
        )
        model_trained = MultiOutputRegressor(xgb_base_model)
        model_trained.fit(X_train, y_train)

        # Save the trained model, imputer, and transformer
        joblib.dump(model_trained, MODEL_PATH)
        joblib.dump(inductance_imputer, IMPUTER_PATH)
        joblib.dump(transformer, TRANSFORMER_PATH)

    # Prepare new inductance values for prediction
    new_inductance_values_filled = inductance_imputer.transform(new_inductance_values)

    # Apply appropriate transformations to new inductance values
    for col in inductance_cols:
        if col in skewed_columns:
            new_inductance_values_filled[:, inductance_cols.index(col)] = transformer[col].transform(
                new_inductance_values_filled[:, [inductance_cols.index(col)]]).flatten()
        else:
            new_inductance_values_filled[:, inductance_cols.index(col)] = transformer[col].transform(
                new_inductance_values_filled[:, [inductance_cols.index(col)]]).flatten()

    # Predict the STIG values
    preds = model_trained.predict(new_inductance_values_filled)

    # Evaluate the model accuracy on the test set
    if 'X_test' in locals():
        y_pred = model_trained.predict(X_test)

        # Calculate R² score (Goodness of fit)
        r2 = r2_score(y_test, y_pred)
        print(f"R² (Goodness of fit): {r2 * 100:.2f}%")

        # Calculate Mean Absolute Error (MAE)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Mean Absolute Error (MAE): {mae:.4f}")

        # Calculate Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error (MSE): {mse:.4f}")

        # Calculate Root Mean Squared Error (RMSE)
        rmse = np.sqrt(mse)
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

        # Calculate Mean Absolute Percentage Error (MAPE)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        print(f"Mean Absolute Percentage Error (MAPE): {mape * 100:.2f}%")

        # Calculate Explained Variance Score
        evs = explained_variance_score(y_test, y_pred)
        print(f"Explained Variance Score: {evs:.4f}")

    return preds, stig_cols


# Example usage for user input
if __name__ == "__main__":
    excel_file = 'Sigma Condenser SN Dashboard 290425.xlsx'
    inductance_cols = ['L1X', 'L1Y', 'L2X', 'L2Y', 'L3X', 'L3Y', 'L4X', 'L4Y']

    # User input for inductance values
    user_input = {}
    for col in inductance_cols:
        val = input(f"{col}: ")
        try:
            val = float(val)
        except Exception:
            val = np.nan # Default to NaN if input is invalid
        user_input[col] = val

    user_df = pd.DataFrame([user_input])

    # Get predictions
    preds, stig_cols = train_and_predict_stig_balance_ap_stig(excel_file, user_df)

    # Display the predicted STIG values
    for name, val in zip(stig_cols, preds[0]):
        print(f"{name}: {val:.10f}")
