# NZ Job Market Data Analysis & ML

An end-to-end Python and data science portfolio project analyzing trends in New Zealand online job advertisements using official MBIE Jobs Online data.

## Project objective

This project will examine how online job-advertisement activity changes across industries, occupations, regions, and time. It will cover:

- Data loading and inspection
- Data cleaning and validation
- Exploratory data analysis
- Data visualization
- Feature engineering
- Machine-learning modelling
- Model evaluation and interpretation
- Conclusions and recommendations

> **Important:** MBIE Jobs Online primarily reports job-advertisement index data. Index values represent relative changes in online job advertisements and should not be interpreted as actual vacancy counts.

## Project structure

```text
├── data/
│   ├── raw/              # Original MBIE data
│   └── processed/        # Cleaned and transformed data
├── models/               # Saved machine-learning models
├── notebooks/            # Jupyter notebooks
├── reports/
│   └── figures/          # Exported charts and visualizations
├── src/                  # Reusable Python modules
├── .gitignore
├── README.md
└── requirements.txt
```

# Data sources

This project uses official Jobs Online data published by New Zealand's Ministry of Business, Innovation and Employment (MBIE).

Source page:  
https://www.mbie.govt.nz/business-and-employment/employment-and-skills/labour-market-reports-data-and-analysis/jobs-online

## Quarterly dataset

- File: `jobs-online-all-vacancies-unadjusted-quarterly-june-2026.xlsx`
- Coverage: through the June 2026 quarter
- Format: Excel
- Worksheet: `Data`
- Purpose: regional, industry, occupation and skill-level analysis

## Interpretation

Jobs Online tracks changes in online job advertisements using index values. The values are not actual vacancy counts. The series is unadjusted, so seasonal patterns may remain in the data.

## Raw-data policy

Files in `data/raw/` are preserved without modification and excluded from Git. Cleaned and transformed datasets will be generated reproducibly from the source files.
