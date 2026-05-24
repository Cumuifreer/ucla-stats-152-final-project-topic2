"""Small helper functions for the coastal temperature notebook."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


MISSING_VALUES = [99.99, -99.99, 999, -999, -9999]
SEASON_ORDER = ["DJF", "MAM", "JJA", "SON"]
SEASON_TO_NUMBER = {"DJF": 0, "MAM": 1, "JJA": 2, "SON": 3}
SEASON_START_MONTH = {"DJF": 12, "MAM": 3, "JJA": 6, "SON": 9}


def load_year_month_index(file_path, column_name, missing_values=MISSING_VALUES):
    """Read index files stored as one year followed by 12 monthly values."""
    rows = []

    with Path(file_path).open("r") as data_file:
        for line in data_file:
            parts = line.split()

            if len(parts) == 13 and parts[0].isdigit():
                year = int(parts[0])
                for month, value in enumerate(parts[1:], start=1):
                    rows.append(
                        {
                            "date": pd.Timestamp(year=year, month=month, day=1),
                            column_name: float(value),
                        }
                    )

    data = pd.DataFrame(rows).set_index("date").sort_index()
    return data.replace(missing_values, np.nan)


def load_monthly_csv_index(file_path, column_name, missing_values=MISSING_VALUES):
    """Read a two-column monthly index CSV with date and value columns."""
    data = pd.read_csv(
        file_path,
        names=["date", column_name],
        header=0,
        skipinitialspace=True,
    )
    data["date"] = pd.to_datetime(data["date"])
    data[column_name] = pd.to_numeric(data[column_name], errors="coerce")
    return data.set_index("date").sort_index().replace(missing_values, np.nan)


def add_season_columns(monthly_data):
    """Add season labels, with December assigned to the next DJF year."""
    data = monthly_data.copy()
    data["month"] = data.index.month
    data["season_year"] = data.index.year
    data.loc[data["month"] == 12, "season_year"] += 1

    season_by_month = {
        12: "DJF",
        1: "DJF",
        2: "DJF",
        3: "MAM",
        4: "MAM",
        5: "MAM",
        6: "JJA",
        7: "JJA",
        8: "JJA",
        9: "SON",
        10: "SON",
        11: "SON",
    }
    data["season"] = data["month"].map(season_by_month)
    return data


def season_start_date(season_year, season):
    """Return a timestamp for the first month of a seasonal average."""
    if season == "DJF":
        return pd.Timestamp(year=int(season_year) - 1, month=12, day=1)
    return pd.Timestamp(year=int(season_year), month=SEASON_START_MONTH[season], day=1)


def make_seasonal_mean(monthly_data):
    """Convert monthly data into complete 3-month seasonal means."""
    data = add_season_columns(monthly_data)
    value_columns = [
        col
        for col in data.columns
        if col not in ["month", "season_year", "season"]
    ]

    grouped = data.groupby(["season_year", "season"])
    seasonal_mean = grouped[value_columns].mean()
    seasonal_count = grouped[value_columns].count()

    complete_seasons = seasonal_count.eq(3).all(axis=1)
    seasonal_mean = seasonal_mean.loc[complete_seasons].reset_index()

    seasonal_mean["season"] = pd.Categorical(seasonal_mean["season"], SEASON_ORDER, ordered=True)
    seasonal_mean = seasonal_mean.sort_values(["season_year", "season"]).reset_index(drop=True)
    seasonal_mean["season"] = seasonal_mean["season"].astype(str)
    seasonal_mean["season_number"] = seasonal_mean["season"].map(SEASON_TO_NUMBER)
    seasonal_mean["season_id"] = seasonal_mean["season_year"] * 4 + seasonal_mean["season_number"]
    seasonal_mean["date"] = [
        season_start_date(year, season)
        for year, season in zip(seasonal_mean["season_year"], seasonal_mean["season"])
    ]
    seasonal_mean["season_label"] = (
        seasonal_mean["season_year"].astype(str) + " " + seasonal_mean["season"]
    )

    return seasonal_mean


def area_weighted_regional_mean(data_array, region_box):
    """Average a gridded DataArray over a lat-lon box using cosine latitude weights."""
    region = data_array.sel(
        lat=slice(region_box["lat_min"], region_box["lat_max"]),
        lon=slice(region_box["lon_min"], region_box["lon_max"]),
    )
    latitude_weights = np.cos(np.deg2rad(region.lat))
    return region.weighted(latitude_weights).mean(dim=["lat", "lon"])


def time_ordered_split(data, train_fraction=0.80):
    """Split rows in time order, with earlier rows used for training."""
    split_index = int(len(data) * train_fraction)
    return data.iloc[:split_index].copy(), data.iloc[split_index:].copy()


def safe_correlation(observed, predicted):
    """Calculate correlation, returning NaN for constant predictions."""
    observed = np.asarray(observed)
    predicted = np.asarray(predicted)

    if (
        len(observed) < 2
        or np.std(observed) <= 1e-12
        or np.std(predicted) <= 1e-12
    ):
        return np.nan

    return np.corrcoef(observed, predicted)[0, 1]


def calculate_metrics(observed, predicted):
    """Return the prediction metrics used in the notebook."""
    return {
        "RMSE": np.sqrt(mean_squared_error(observed, predicted)),
        "MAE": mean_absolute_error(observed, predicted),
        "R2": r2_score(observed, predicted),
        "test_correlation": safe_correlation(observed, predicted),
    }


def compute_vif(predictor_data):
    """Return simple variance inflation factors for model predictors."""
    predictors = pd.DataFrame(predictor_data).copy()
    vif_rows = []

    for predictor_name in predictors.columns:
        other_names = [name for name in predictors.columns if name != predictor_name]

        if not other_names:
            vif_value = 1.0
        else:
            model = LinearRegression()
            model.fit(predictors[other_names], predictors[predictor_name])
            fitted_values = model.predict(predictors[other_names])
            r2 = r2_score(predictors[predictor_name], fitted_values)

            if r2 >= 1 - 1e-12:
                vif_value = np.inf
            else:
                vif_value = 1 / (1 - r2)

        vif_rows.append({"predictor": predictor_name, "VIF": vif_value})

    return pd.DataFrame(vif_rows)


def evaluate_models(data, target_column, region_name, model_specs, train_fraction=0.80):
    """Fit the model list for one region and return metrics plus full-model residuals."""
    train_data, test_data = time_ordered_split(data, train_fraction=train_fraction)
    y_train = train_data[target_column].values
    y_test = test_data[target_column].values

    result_rows = []
    full_model_predictions = None

    for model_name, predictor_columns in model_specs:
        if not predictor_columns:
            predictions = np.repeat(y_train.mean(), len(test_data))
            coefficients = {}
        else:
            model = LinearRegression()
            model.fit(train_data[predictor_columns], y_train)
            predictions = model.predict(test_data[predictor_columns])
            coefficients = dict(zip(predictor_columns, model.coef_))

        result_rows.append(
            {
                "region": region_name,
                "model": model_name,
                **calculate_metrics(y_test, predictions),
                "nino34": coefficients.get("nino34", np.nan),
                "pdo": coefficients.get("pdo", np.nan),
                "ao": coefficients.get("ao", np.nan),
            }
        )

        if model_name.lower() == "full":
            full_model_predictions = test_data[
                ["target_date", "target_season", "target_season_label", target_column]
            ].copy()
            full_model_predictions = full_model_predictions.rename(
                columns={target_column: "observed"}
            )
            full_model_predictions["predicted"] = predictions
            full_model_predictions["residual"] = (
                full_model_predictions["observed"] - full_model_predictions["predicted"]
            )
            full_model_predictions["region"] = region_name

    return pd.DataFrame(result_rows), full_model_predictions


def lag_one_autocorrelation(values):
    """Calculate lag-1 autocorrelation for a residual series."""
    values = pd.Series(values).dropna()

    if len(values) < 3:
        return np.nan

    return values.autocorr(lag=1)
