# Climate teleconnections and coastal temperature predictability

We use this repository to ask whether current-season climate indices help predict next-season temperature anomalies on the U.S. West Coast and East Coast.

The main question is: **Can current-season climate indices help predict next-season coastal temperature anomalies, and is the signal different for the West Coast and East Coast?**

We keep the modeling simple. The main tools are correlation checks, multiple linear regression, a collinearity check, out-of-sample validation, and residual diagnostics.

## Project goal

We compare broad West Coast and East Coast temperature anomalies using the same climate predictors: Niño 3.4, PDO, and AO. Rather than chasing the strongest possible forecast, we use a small model family to see whether the indices leave a clearer one-season-ahead signal on one coast than the other.

The current result is cautious. The West Coast signal is clearer than the East Coast signal, but prediction skill is limited. The later test period is also often warmer than the models predict.

## Data sources

The notebook uses four local data files:

- `data/ERA5_2mtemp_1x1.nc`: ERA5 monthly 2m temperature on a 1x1 grid
- `data/nina34.anom.data`: Niño 3.4 monthly index
- `data/ersst.v5.pdo.dat`: PDO monthly index
- `data/ao.long.csv`: AO monthly index

ERA5 is used to build regional seasonal temperature anomalies. The three climate indices are converted to seasonal means and used as current-season predictors.

## Method overview

We first turn ERA5 monthly temperature into area-weighted regional averages for two simple coastal boxes. Then we convert monthly temperature into seasonal anomalies by removing each region's usual DJF, MAM, JJA, and SON means.

For the predictors, we convert Niño 3.4, PDO, and AO into seasonal means. The modeling table pairs each predictor season with the following temperature season, so the setup stays one season ahead.

Before fitting regressions, we check predictor correlations and variance inflation factors (VIF). This keeps the coefficient interpretation honest, especially because Niño 3.4 and PDO are related.

The regression comparison uses a time-ordered 80/20 train/test split. We compare a baseline, Niño-only regression, Niño+PDO regression, and a full model with Niño 3.4, PDO, and AO. We also examine full-model residuals because positive test residuals mean the model is predicting anomalies that are too cool.

## Repository structure

```text
.
├── README.md
├── project_helpers.py
├── topic2_temperature_prediction_mvp.ipynb
├── tests/
│   └── test_project_helpers.py
└── data/
    ├── ERA5_2mtemp_1x1.nc
    ├── nina34.anom.data
    ├── ersst.v5.pdo.dat
    └── ao.long.csv
```

`project_helpers.py` keeps the repeated technical code out of the notebook. It includes climate-index parsing, seasonal means, area-weighted regional means, model metrics, model evaluation, VIF calculation, and residual metrics.

## How to run

This repo uses Git LFS because the ERA5 NetCDF file is large. After cloning, run these commands from the repo root:

```bash
git lfs install
git lfs pull
```

Then open and run:

```text
topic2_temperature_prediction_mvp.ipynb
```

The notebook expects `pandas`, `numpy`, `xarray`, `matplotlib`, and `scikit-learn`. It imports helper functions from `project_helpers.py`. It does not save figures or other output files; plots display inside the notebook.

Optional helper checks can be run with:

```bash
python3 -m unittest tests/test_project_helpers.py
```

## Analysis flow

The notebook moves through the analysis in this order:

- Question and approach
- Temperature targets
- Climate predictors
- One-season-ahead dataset
- Correlation and collinearity
- Regression comparison and out-of-sample skill
- Residual diagnostics
- Main takeaways
