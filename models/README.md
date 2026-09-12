# Generated models

`ridge_monthly_index_forecaster.joblib` is generated locally by
`notebooks/06_monthly_forecasting.ipynb` and is excluded from Git.

The model is a Ridge regression pipeline with:

- StandardScaler fitted on the training features
- Ridge regression with alpha 100
- Seven ordered forecasting features
- Training observations through July 2026

The operational model is retrained after final test evaluation using
all available model-ready observations. Reported test metrics belong
to the frozen model trained only through July 2024, not this retrained
operational artifact.

Run the forecasting notebook from the beginning to rebuild the model.
