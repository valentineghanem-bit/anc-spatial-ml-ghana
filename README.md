# Temporal and Spatial Dynamics of ANC Coverage and Fertility Inequities in Ghana

**Principal Investigator:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra 
**ORCID:** 0009-0002-8332-0220 
**Date:** April 2026 
**Status:** Part II of Ghana ANC longitudinal series

## Overview

> **"Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022)"**

### Key Findings

| Metric | Value |
|--------|-------|
| ANC coverage 1988→2022 | 68.0% → 97.9% |
| Observations | 92 (90 region-year + 2 national aggregates) |
| Critical TFR threshold | 5.90 (RF partial dependence) |
| CEI range | 14.3 (North East) – 30.8 (Greater Accra) |
| CEI gap | 2.15× |
| RF ANC prediction R² | 0.81 (5-fold spatial CV) |
| CART accuracy | 81.3% (LOOCV) |
| ANC Gini 1988→2022 | 0.142 → 0.038 |
| Critical zones | 3 regions (North East, Savannah, Upper West) |

## Structure

```
github_repo/
├── README.md
├── requirements.txt
├── CITATION.cff
├── LICENSE
├── .gitignore
├── scripts/
│ ├── 01_data_preparation.py # Load, validate, standardise DHS waves
│ ├── 02_cei_calculation.py # Care Efficiency Index + risk zone classification
│ ├── 03_spatial_analysis.py # Moran's I + Bivariate LISA
│ ├── 04_ml_pipeline.py # Random Forest + CART + PDPs
│ ├── 05_figures.py # All 12 publication figures + 5 supplementary
│ └── 06_analysis_pipeline.py # Master orchestration script
├── tests/
│ └── test_anc_analysis.py # Unit tests — canonical value assertions
├── data/
│ └── README_data.md # Dataset instructions
├── docs/
│ └── codebook.md # Variable codebook (40 columns)
└── figures/ # Generated figures (see ../06_figure_*.png)
```

## Installation

```bash
pip install -r requirements.txt
python scripts/06_analysis_pipeline.py --all
pytest tests/ -v
```

## Reproducibility

- Random seed: 42 throughout
- Reporting: STROBE (observational ecological study)
- Software: Python 3.11 · scikit-learn 1.5.2 · libpysal 4.11 · esda 2.7

## Citation

```
Ghanem VG. Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility
Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves
(1988–2022). 2026. ORCID: 0009-0002-8332-0220
```

## Licence

MIT — see LICENSE.
