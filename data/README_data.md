# Data — Ghana ANC Fertility Analysis

## Primary Dataset

`Ghana_ANC_Fertility_Master_Dataset.csv` — located in the project root folder (parent of this repo).

**Structure:** 92 rows × 40 columns 
- Rows: 90 region-year observations (10 legacy regions × 9 DHS waves, 1988–2022) + 2 national aggregate rows 
- Columns: Region/wave identifiers, ANC outcomes, fertility measures, CEI, covariates, spatial outputs, ML outputs, provenance fields

## Data Sources

| Variable group | Source |
|----------------|--------|
| ANC coverage, TFR, ASFR | Ghana DHS 1988–2022 (ICF International) |
| Female education, uninsurance | Ghana DHS (wave-matched) |
| Poverty index (MPI) | OPHI MPI Ghana 2023 / GSS Census 2021 |
| Population denominators | GSS Census 2021 / WorldPop 2020 |
| Facility density | Ghana Health Service facility registry (DHIMS2) |

## Usage

```python
import pandas as pd
df = pd.read_csv("../Ghana_ANC_Fertility_Master_Dataset.csv")
df_region_year = df[df["region"] != "NATIONAL"] # 90 obs for ML
df_2022 = df[(df["wave_year"] == 2022) & (df["region"] != "NATIONAL")] # 10 regions
```

## Ethics

This study uses publicly available DHS survey data. No primary data were collected; no IRB approval required. DHS programme access: dhsprogram.com.
