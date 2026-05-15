# Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)  
**Reporting standard:** STROBE  
**Date:** April 2026

> Ghanem VG. *Temporal and spatial dynamics of antenatal care coverage and fertility inequities in Ghana: a subnational ecological study using nine DHS survey waves (1988–2022).* 2026.

**Note:** This is Part II of a Ghana ANC longitudinal series.

---

## Overview

This subnational ecological study traces antenatal care (ANC) coverage and fertility trajectories across nine Ghana DHS survey waves (1988–2022), covering 34 years of subnational maternal health data. A novel Care Efficiency Index (CEI = ANC% / TFR) quantifies the efficiency of ANC delivery relative to fertility burden. Machine learning (Random Forest, Decision Tree) with spatial cross-validation predicts regional ANC coverage. LISA and Global Moran's I characterise spatial clustering dynamics over time.

---

## Key Findings

| Metric | Value |
|--------|-------|
| ANC coverage change | 68.0% (1988) → 97.9% (2022) |
| Total observations | 92 (90 region-year + 2 national aggregates) |
| Critical TFR threshold | 5.90 (RF partial dependence) |
| CEI range | 14.3 (North East) – 30.8 (Greater Accra) |
| CEI gap | 2.15× |
| RF ANC prediction R² | 0.81 (5-fold spatial CV) |
| CART accuracy (LOOCV) | 81.3% |
| ANC Gini 1988→2022 | 0.142 → 0.038 |
| Critical zones | 3 regions (North East, Savannah, Upper West) |

---

## Repository Structure

```
anc-spatial-ml-ghana/
├── scripts/
│   ├── 01_data_preparation.py
│   ├── 02_cei_calculation.py
│   ├── 03_spatial_analysis.py
│   ├── 04_ml_pipeline.py
│   ├── 05_figures.py
│   └── 06_analysis_pipeline.py
├── tests/
│   └── test_anc_analysis.py
├── data/
│   └── README_data.md
├── docs/
│   └── codebook.md
├── figures/
├── requirements.txt
└── CITATION.cff
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/valentineghanem-bit/anc-spatial-ml-ghana.git
cd anc-spatial-ml-ghana
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
python scripts/06_analysis_pipeline.py --all
```

### 4. Run tests

```bash
pytest tests/ -v
```

---

## Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Ghana DHS subnational data (9 waves) | ANC coverage (≥1 and ≥4 visits), TFR, regional estimates | 1988, 1993, 1998, 2003, 2008, 2014, 2016, 2019, 2022 | dhsprogram.com (registration) |
| Ghana administrative boundaries (GADM) | Regional polygon geometries | 2021 | gadm.org (open) |

---

## Methods Summary

| Method | Tool | Purpose |
|--------|------|---------|
| Gini coefficient | scipy | ANC coverage equity over time |
| Global Moran's I (KNN k=4) | esda / libpysal | Spatial autocorrelation of ANC and TFR |
| LISA (Rook contiguity) | esda | Local cluster detection |
| Random Forest (n=200, max_depth=6) | scikit-learn | ANC prediction (5-fold spatial CV) |
| Decision Tree (LOOCV) | scikit-learn | Interpretable ANC risk stratification |
| Partial Dependence | scikit-learn | Critical TFR threshold identification |
| Care Efficiency Index (CEI) | Custom | ANC% / TFR composite metric |
| Risk Stratification (z-score quadrant) | Custom | Regional priority classification |

---

## Reproducibility

- Random seed: 42 throughout  
- Reporting: STROBE  
- All random seeds set explicitly (`random_state=42`)  
- DHS data accessed under registration from dhsprogram.com

---

## Ethical Statement

This study used exclusively de-identified secondary data from the Ghana DHS programme. No primary data collection from human participants was conducted. DHS data were accessed under standard registration. Ethical review was therefore not required.

---

## Citation

```bibtex
@misc{ghanem2026ancspatial,
  author = {Ghanem, Valentine Golden},
  title  = {Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988--2022)},
  year   = {2026},
  url    = {https://github.com/valentineghanem-bit/anc-spatial-ml-ghana}
}
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Contact

Valentine Golden Ghanem  
Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
valentineghanem@gmail.com  
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
