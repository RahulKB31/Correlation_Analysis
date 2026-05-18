from statistics import correlation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from matplotlib.pyplot import title
from scipy.stats import pearsonr, spearmanr, shapiro
from setuptools.sandbox import save_path

def plot_distribution(df, group_name="Inductance", bins=30):
    num_cols = len(df.columns)
    num_rows = math.ceil(num_cols / 3)  # 3 plots per row

    fig, axes = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))
    axes = axes.flatten()

    for i, col in enumerate(df.columns):
        sns.histplot(df[col].dropna(), kde=True, bins=bins, ax=axes[i])
        axes[i].set_title(col)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(f"{group_name}_Distributions.jpg", format="jpg")
    plt.close()
    print(f"Saved distributions as '{group_name}_Distributions.jpg'")

    #     plt.subplot(n_rows, 3, idx)
    #     sns.histplot(df[col].dropna(), kde=True, bins=bins)
    #     plt.title(f"Distribution: {col}")
    # plt.tight_layout()
    # plt.savefig(f'Distribution.jpg', format='jpg')
    # #plt.show()

def run_shapiro_test(df, df_name="DataFrame", save_path=None):
    results = []
    for col in df.columns:
        data = df[col].dropna()
        if len(data) < 3:
            results.append({
                'Column':col,
                'W-Stat': None,
                'p-value': None,
                'Normality': None
            })
            continue

        stat, p = shapiro(data)
        normality = 'Normal' if p > 0.05 else 'Not Normal'
        results.append({
            'Column': col,
            'W-Stat': stat,
            'p-value': p,
            'Normality': normality
        })
    result_df = pd.DataFrame(results)
    if save_path:
        if save_path.endswith('.xlsx'):
            result_df.to_excel(save_path, index=False)
        else:
            result_df.to_csv(save_path, index=False)
    return result_df

def analyze_correlations(file_path):
    # Loading the csv data
    df = pd.read_excel(file_path)

    # Defining the columns for the 1st dataframe
    columns_for_first_df = ['L1X','L1Y','L2X','L2Y','L3X','L3Y','L4X','L4Y']

    # Creating the first dataframe
    df_first = df[columns_for_first_df]

    # Defining the columns for the 2nd dataframe
    base_columns = [
        'AP_STIGXLOWER', 'AP_STIGYLOWER',
        'AP_STIGXUPPER', 'AP_STIGYUPPER'
    ]

    # Creating an empty list to store the columns for 2nd df
    columns_for_second_df = []

    # Loop through the numbers 1 to 7 to generate the columns names
    for i in range(1, 8):
        for base in base_columns:
            columns_for_second_df.append(f'{base}_{i}_Off')
            columns_for_second_df.append(f'{base}_{i}_On')

    # Creating the 2nd df
    df_second = df[columns_for_second_df]

    # Remove rows
    stig_na_mask = df_second.isna().any(axis=1)
    df_first_clean = df_first[~stig_na_mask].reset_index(drop=True)
    df_second_clean = df_second[~stig_na_mask].reset_index(drop=True)

    # Distributions
    plot_distribution(df_first_clean, group_name="Inductance_")
    print("Saved distribution for Inductance plots to jpg")
    plot_distribution(df_second_clean, group_name="Stig Balance_")
    print("Saved distribution for Stig Balance plots to jpg")

    # Statistical Summary
    desc_first_clean = df_first_clean.describe()
    desc_first_clean.to_excel("Inductance_Summary.xlsx")
    print("Saved Inductance Summary to Excel")
    desc_second_clean = df_second_clean.describe()
    desc_second_clean.to_excel("Stig_Balance_Summary.xlsx")
    print("Saved Stig Balance Summary to Excel")

    # Shapiro-Wilk Normality Test
    run_shapiro_test(
        df_first_clean,
        "df_first_clean (Inductance Columns)",
        save_path = "Shapiro_Inducatance.xlsx"
    )
    print("Saved Shapiro Inductance Values to Excel")
    run_shapiro_test(
        df_second_clean,
        "df_second_clean (Stig Balance Columns)",
        save_path="Shapiro_Stig_Balance.xlsx"
    )
    print("Saved Shapiro Stig Balance Values to Excel")

    # Correlation ANalysis
    correlations = []
    for i in range(1,8):
        cols_stig = [f'{base}_{i}_Off' for base in base_columns] + [f'{base}_{i}_On' for base in base_columns]
        df_stig_balance = df_second_clean[cols_stig]
        df_inductance = df_first_clean

        for coil_col in df_inductance.columns:
            for aperture_col in df_stig_balance.columns:
                pearson_corr, _ = pearsonr(df_inductance[coil_col], df_stig_balance[aperture_col])
                spearman_corr, _ = spearmanr(df_inductance[coil_col], df_stig_balance[aperture_col])
                correlations.append({
                    "Coil": coil_col,
                    "Aperture": aperture_col,
                    "Pearson": pearson_corr,
                    "Spearman": spearman_corr,
                })

    correlation_df = pd.DataFrame(correlations)
    correlation_df.to_excel("Coil_Aperture_Correlation_Table.xlsx", index=False)
    print("Saved Coil Aperture Correlation Table to Excel")

    for i in range(1,8):
        cols_stig = [f'{base}_{i}_Off' for base in base_columns] + [f'{base}_{i}_On' for base in base_columns]
        df_stig_balance = df_second_clean[cols_stig]
        df_inductance = df_first_clean

        df_combined = pd.concat([df_stig_balance, df_inductance], axis=1)

        # Pearson HeatMap
        pearson_corr_matrix = df_combined.corr(method='pearson')
        plt.figure(figsize=(12, 10))
        sns.heatmap(pearson_corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink":.9})
        plt.title('Pearson Correlation Matrix Aperture {i}', fontsize=14)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(f'Pearson_Corr_Matrix_Aperture_{i}.jpg', format='jpg')
        plt.close()
        print(f"Saved Pearson Correlation correlation heatmap for aperture {i}.")

        # Spearman HeatMap
        spearman_corr_matrix = df_combined.corr(method='spearman')
        plt.figure(figsize=(12, 10))
        sns.heatmap(spearman_corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .9})
        plt.title('Spearman Correlation Matrix Aperture {i}', fontsize=14)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(f'Spearman_Corr_Matrix_Aperture_{i}.jpg', format='jpg')
        plt.close()
        print(f"Saved Spearman Correlation correlation heatmap for aperture {i}.")


    #     # # Remove rows with NA
    #     # not_na_index = df_stig_balance.dropna().index
    #     # df_stig_balance = df_stig_balance.loc[not_na_index].reset_index(drop=True)
    #     # df_inductance = df_inductance.loc[not_na_index].reset_index(drop=True)
    #
    #     # Combining the dataframes#
    #     df_combined = pd.concat([df_stig_balance, df_inductance], axis=1)
    #
    #     ## Calculating the correlation matrix]
    #     correlation_matrix = df_combined.corr()
    #
    #     # PLotting heatmaps
    #     plt.figure(figsize=(12,10))
    #     sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink":.9})
    #     plt.title(f'Correlation Matrix Aperture {i}', fontsize=14)
    #     plt.xticks(rotation=90)
    #     plt.yticks()
    #     plt.tight_layout()
    #     plt.savefig(f'Corr_Matrix_Aperture_{i}.jpg', format='jpg')
    #     plt.show()
    #
    #     # Calculating corr for each of the sets###
    #     correlations[i] = {}
    #     for col_ind, col_stig in zip(df_inductance.columns, df_stig_balance.columns):
    #         pearson_corr, _ = pearsonr(df_inductance[col_ind], df_stig_balance[col_stig])
    #         spearman_corr, _ = spearmanr(df_inductance[col_ind], df_stig_balance[col_stig])
    #         correlations[i][col_stig] = {'Pearson': pearson_corr, 'Spearman':spearman_corr}
    #
    # # Print correlations
    # print("Correlations")
    # for index, corr_values in correlations.items():
    #     print(f'Index {index}:')
    #     for col, values in corr_values.items():
    #         print(f" {col}: Pearson = {values['Pearson']:.2f}, Spearman = {values['Spearman']:.2f}")

if __name__ == '__main__':
    analyze_correlations('Sigma Condenser SN Dashboard 290425.xlsx')
    print("Process Completed!")

























