# West Coast vs East Coast Seasonal Temperature Predictability

This repository contains our Stats 152 final project notebook.

We study whether current-season climate indices can help predict next-season seasonal-mean temperature anomalies for the U.S. West Coast and East Coast.

## Project Goal

The main project question is:

Can current-season Niño 3.4, PDO, and AO help predict next-season temperature anomalies for coastal regions of the western and eastern United States?

We compare:

- West Coast vs East Coast predictability
- simple models vs the full multiple regression model
- model performance across seasons

The main model is multiple linear regression. More complex machine learning methods are kept as possible future extensions.

## Data Sources

The project uses four data files:

- `data/ERA5_2mtemp_1x1.nc`: ERA5 monthly 2m temperature on a 1x1 grid
- `data/nina34.anom.data`: Niño 3.4 monthly index
- `data/ersst.v5.pdo.dat`: PDO monthly index
- `data/ao.long.csv`: AO monthly index

ERA5 temperature is used to compute regional seasonal temperature anomalies. Niño 3.4, PDO, and AO are converted to seasonal means and used as predictors.

## Method Overview

The notebook follows this analysis flow:

1. Load and clean ERA5 temperature and the three climate indices.
2. Define simple coastal proxy regions for the West Coast and East Coast.
3. Compute area-weighted monthly temperature for each region.
4. Convert monthly temperature to seasonal means.
5. Compute seasonal temperature anomalies by removing each season's long-run average.
6. Convert climate indices to seasonal means.
7. Build a one-season-ahead prediction table.
8. Fit and compare multiple regression models for both coasts.
9. Use a time-ordered 80/20 train/test split for out-of-sample validation.
10. Check residuals and interpret model performance.

The notebook keeps EDA focused. It includes only basic data checks, region definitions, key correlations, and a few useful plots.

## Repository Structure

```text
.
├── README.md
├── topic2_temperature_prediction_mvp.ipynb
└── data/
    ├── ERA5_2mtemp_1x1.nc
    ├── nina34.anom.data
    ├── ersst.v5.pdo.dat
    └── ao.long.csv
```

## How to Clone This Repository

This project uses Git LFS because the ERA5 NetCDF file is large. Please install Git LFS before cloning or before pulling the data.

### 1. Install Git LFS

On macOS with Homebrew:

```bash
brew install git-lfs
git lfs install
```

If Git LFS is already installed, just run:

```bash
git lfs install
```

### 2. Clone the repository

Using SSH:

```bash
git clone git@github.com:Cumuifreer/ucla-stats-152-final-project-topic2.git
cd ucla-stats-152-final-project-topic2
```

If SSH is not set up, use HTTPS:

```bash
git clone https://github.com/Cumuifreer/ucla-stats-152-final-project-topic2.git
cd ucla-stats-152-final-project-topic2
```

### 3. Download the Git LFS data files

After cloning, run:

```bash
git lfs pull
```

This should download the real data files inside the `data/` folder. If a NetCDF file looks like a tiny text file instead of a large data file, Git LFS did not download correctly. Run `git lfs install` and `git lfs pull` again.

## How to Run

Open the notebook:

```text
topic2_temperature_prediction_mvp.ipynb
```

Run the cells from top to bottom.

The notebook uses:

- pandas
- numpy
- xarray
- matplotlib
- scikit-learn

It does not save output files or figure files. All plots are displayed inside the notebook.
