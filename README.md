# Correlation Analysis of Inductance Measurements and Stig Balance Values – HLD & LLD

## Overview

This project performs statistical and correlation analysis between **Inductance measurements** and **Stig Balance values**. The objective is to identify relationships between electrical inductance properties and stig balance parameters using statistical testing, correlation techniques, and visualization methods.

Inductance is a property of electrical circuits where coils (inductors) store energy in a magnetic field when electric current passes through them. This analysis helps evaluate how inductance measurements influence or relate to stig balance values.

The project provides:

* Automated data loading from Excel files
* Data cleaning and preprocessing
* Distribution analysis using histograms and KDE plots
* Statistical summaries
* Normality testing using the Shapiro-Wilk test
* Pearson and Spearman correlation analysis
* Correlation heatmap visualizations
* Export of results into Excel and image files

---

# Features

* Load input data directly from Excel files
* Remove missing or invalid records
* Generate distribution histograms with KDE curves
* Compute descriptive statistics
* Perform Shapiro-Wilk normality tests
* Calculate Pearson and Spearman correlation coefficients
* Generate correlation heatmaps
* Save outputs as Excel and JPG files

---

# Project Structure

```bash
project-directory/
│
├── main.py
├── requirements.txt
├── README.md
├── Sigma Condenser SN Dashboard 290425.xlsx
│
├── outputs/
│   ├── distributions/
│   ├── summaries/
│   ├── shapiro_results/
│   ├── correlations/
│   └── heatmaps/
│
└── images/
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Required Libraries

The project uses the following Python libraries:

```txt
pandas
numpy
matplotlib
seaborn
scipy
openpyxl
```

---

# Usage

## 1. Prepare Input File

Place the Excel file below inside the project directory:

```txt
Sigma Condenser SN Dashboard 290425.xlsx
```

## 2. Run the Script

```bash
python main.py
```

---

# Generated Outputs

The script automatically generates:

| Output Type          | Description                                    |
| -------------------- | ---------------------------------------------- |
| Distribution Plots   | Histogram + KDE plots saved as JPG             |
| Statistical Summary  | Descriptive statistics saved as Excel          |
| Shapiro-Wilk Results | Normality test results saved as Excel          |
| Correlation Tables   | Pearson & Spearman results saved as Excel      |
| Heatmaps             | Correlation matrix visualizations saved as JPG |

---

# Factors Affecting Coil Inductance

## 1. Number of Turns

Increasing the number of turns significantly increases inductance.

* Doubling turns approximately quadruples inductance.

## 2. Coil Length

Larger coil area generally increases inductance.

## 3. Material

Higher magnetic permeability leads to higher inductance.

## 4. Coil Shape

| Coil Type              | Inductance |
| ---------------------- | ---------- |
| Toroidal (Donut Shape) | High       |
| Solenoid (Cylindrical) | Low        |

---

# High-Level Design (HLD)

## Objective

Develop a Python-based statistical analysis system that evaluates relationships between inductance measurements and stig balance values using descriptive statistics, normality testing, correlation analysis, and visualization techniques.

---

## System Components

### 1. Data Input Layer

* Reads Excel input files
* Imports measurement datasets into DataFrames

### 2. Data Processing Layer

* Cleans missing values
* Filters incomplete records
* Prepares datasets for analysis

### 3. Statistical Analysis Layer

* Generates statistical summaries
* Performs Shapiro-Wilk normality tests
* Computes Pearson and Spearman correlations

### 4. Visualization Layer

* Creates histograms
* Generates KDE curves
* Produces correlation heatmaps

### 5. Output Generation Layer

* Saves Excel reports
* Exports visualization images

---

## Workflow

```text
Excel File Input
        ↓
Data Cleaning
        ↓
Distribution Analysis
        ↓
Statistical Summary
        ↓
Shapiro-Wilk Test
        ↓
Correlation Analysis
        ↓
Heatmap Visualization
        ↓
Export Results
```

---

# Low-Level Design (LLD)

## Core Functions

---

## 1. `plot_distribution(df, group_name, bins)`

### Purpose

Generate histograms and KDE plots for dataset columns.

### Inputs

* `df` → Input DataFrame
* `group_name` → Dataset group name
* `bins` → Number of histogram bins

### Outputs

* JPG distribution plots

---

## 2. `run_shapiro_test(df, df_name, save_path)`

### Purpose

Perform Shapiro-Wilk normality tests on DataFrame columns.

### Inputs

* `df` → Input DataFrame
* `df_name` → Dataset name
* `save_path` → Output file path

### Outputs

* Excel file containing:

  * W-statistic
  * p-values
  * Normality interpretation

---

## 3. `analyze_correlations(file_path)`

### Purpose

Main execution function for end-to-end analysis.

### Inputs

* `file_path` → Excel dataset location

### Outputs

* Distribution plots
* Statistical summaries
* Correlation matrices
* Heatmaps
* Shapiro-Wilk test reports

---

# Data Structures Used

| Structure  | Purpose                       |
| ---------- | ----------------------------- |
| DataFrame  | Data storage and manipulation |
| List       | Dynamic column management     |
| Dictionary | Store correlation results     |

---

# Statistical Methods Used

## Shapiro-Wilk Test

Used to determine whether the data follows a normal distribution.

### Interpretation

| p-value | Interpretation           |
| ------- | ------------------------ |
| > 0.05  | Normally distributed     |
| ≤ 0.05  | Not normally distributed |

---

## Pearson Correlation

Used for:

* Continuous variables
* Linear relationships
* Normally distributed data

### Correlation Range

| Value | Interpretation              |
| ----- | --------------------------- |
| +1    | Strong positive correlation |
| 0     | No correlation              |
| -1    | Strong negative correlation |

---

## Spearman Correlation

Used for:

* Non-normal data
* Ordinal data
* Monotonic relationships

A non-parametric correlation technique based on ranked values.

---

# Interpretation of Results

## Distribution Curves

### Normal Distribution

Bell-shaped curve with values concentrated around the mean.

### Right Skew (Positive Skew)

Tail extends toward higher values.

### Left Skew (Negative Skew)

Tail extends toward lower values.

---

# Correlation Interpretation

| Correlation Coefficient | Interpretation                 |
| ----------------------- | ------------------------------ |
| Near 0                  | Very weak relationship         |
| Near +0.5               | Moderate positive relationship |
| Near +1                 | Strong positive relationship   |
| Near -0.5               | Moderate negative relationship |
| Near -1                 | Strong negative relationship   |

### Example

If correlation coefficients are close to zero, it suggests that inductance measurements do not strongly influence stig balance values.

---

# Statistical Summary Interpretation

## Mean

Average value; sensitive to outliers.

## Median

Middle value; robust against outliers.

## Mode

Most frequently occurring value.

## Range

Difference between maximum and minimum values.

## Standard Deviation

Measures spread of data around the mean.

## Interquartile Range (IQR)

Represents the middle 50% of the dataset.

## KDE Curve

Provides a smooth estimate of data distribution density.

---

# Error Handling

## Missing Data

Rows containing missing values are removed before analysis.

## File Validation

Ensure:

* Correct Excel file path
* Valid sheet names
* Required columns exist

---

# Future Enhancements

* Interactive dashboards using Plotly or Power BI
* Automated anomaly detection
* Machine learning-based predictive analysis
* Support for multiple Excel sheets
* Real-time monitoring integration

---

# Example Command

```bash
python main.py
```

---

# Conclusion

This project provides a complete statistical analysis framework for studying relationships between inductance measurements and stig balance values. It combines data preprocessing, statistical testing, correlation analysis, and visualization techniques to generate meaningful engineering insights and support further research or manufacturing optimization.
