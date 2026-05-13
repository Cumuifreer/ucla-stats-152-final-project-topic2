# Topic 2 Temperature Prediction MVP

This repository is an early MVP for our Stats 152 final project.

The main idea is to study whether large-scale climate indices can help predict next-season temperature anomaly at one selected location. The current notebook is only a first data check. It loads the data, cleans obvious missing values, makes simple EDA checks, and outlines the next project steps.

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

## Data

The project currently uses these files:

- `data/ERA5_2mtemp_1x1.nc`: ERA5 monthly 2m temperature
- `data/nina34.anom.data`: Nino 3.4 monthly index
- `data/ersst.v5.pdo.dat`: PDO monthly index
- `data/ao.long.csv`: AO monthly index

## Current Notebook

Open `topic2_temperature_prediction_mvp.ipynb` to see the first data check.

The notebook currently:

- imports the needed packages
- loads the four datasets
- cleans obvious missing-value codes
- makes simple EDA checks
- combines the climate indices
- makes one simple time series plot
- outlines a more detailed next plan

It does not run regression, prediction, train/test splitting, or residual analysis yet.
