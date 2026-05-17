# Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022)

[![CI](https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**Reporting standard:** STROBE
**Date:** April 2026
**Status:** Manuscript in preparation | Part I of Ghana ANC longitudinal series

> Valentine Golden Ghanem (2026). *Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022).* GitHub repository. https://github.com/valentineghanem-bit/anc-spatial-ml-ghana

---

## 1. Abstract

This subnational ecological study traces antenatal care (ANC) coverage and fertility trajectories across nine Ghana DHS survey waves (1988–2022), covering 34 years of subnational maternal health data. A novel Care Efficiency Index (CEI = ANC% / TFR) quantifies the efficiency of ANC delivery relative to fertility burden. Machine learning (Random Forest, Decision Tree) with spatial cross-validation predicts regional ANC coverage. LISA and Global Moran's I characterise spatial clustering dynamics over time.

---

## 2. Research Question & Aims

- **Primary:** Map the spatial and temporal evolution of ANC coverage and fertility across Ghana, 1988–2022.
- **Secondary:** (a) Operationalise the Care Efficiency Index (CEI); (b) build ML models to predict regional ANC under spatial cross-validation; (c) identify critical thresholds of TFR beyond which ANC stagnates; (d) stratify regions for targeted policy investment.

---

## 3. Methods Summary

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

## 4. Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Ghana DHS subnational data (9 waves) | ANC coverage (≥1 and ≥4 visits), TFR, regional estimates | 1988, 1993, 1998, 2003, 2008, 2014, 2016, 2019, 2022 | [dhsprogram.com](https://dhsprogram.com) (registration) |
| Ghana administrative boundaries (GADM) | Regional polygon geometries | 2021 | [gadm.org](https://gadm.org) (open) |

> DHS data accessed under standard registration.

---

## 5. Key Findings

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

## 6. Repository Structure

```
anc-spatial-ml-ghana/
├── scripts/
│   ├── 01_data_preparation.py
│   ├── 02_cei_calculation.py
│   ├── 03_spatial_analysis.py
│   ├── 04_ml_pipeline.py
│   ├── 05_figures.py
│   └── 06_analysis_pipeline.py
├── app.py                          # Plotly Dash interactive application
├── analysis.R                      # R spatial diagnostics
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

## 7. Reproducibility

### 7.1 Requirements
- Python 3.12 (see `requirements.txt` for pinned versions)
- R 4.3+ (for R scripts; see `renv.lock` or `analysis.R` header for pinned packages)
- Random seed: 42 throughout (set via `random_state=42` and `np.random.seed(42)`)
- Estimated runtime: ~3–5 minutes on a standard laptop
- Tested on: Ubuntu 22.04 / macOS 14 / Windows 11 (CI: GitHub Actions)

### 7.2 Clone & install
```bash
git clone https://github.com/valentineghanem-bit/anc-spatial-ml-ghana.git
cd anc-spatial-ml-ghana
pip install -r requirements.txt
# For R scripts (optional):
Rscript -e "if (!requireNamespace('renv', quietly=TRUE)) install.packages('renv'); renv::restore()"
```

### 7.3 Run the analytical pipeline
```bash
python scripts/06_analysis_pipeline.py --all
```

### 7.4 Run the test suite
```bash
pytest tests/ -v
```

### 7.5 Launch the interactive Dash application
```bash
python app.py
# Navigate to http://127.0.0.1:8050 in your browser
```

### 7.6 Open the static HTML dashboard
Static dashboard not bundled in this repo; use the interactive Dash app (section 7.5).

---

## 8. Outputs

- **Interactive Dash app:** `app.py` — `python app.py` → http://127.0.0.1:8050
- **Figures:** `figures/*.png` — 300 DPI publication-ready
- **Documentation:** `docs/codebook.md`

---

## 8a. Downloadable artefacts (HTML)

Both the interactive dashboard and the conference poster are committed to the repository as **self-contained HTML files** — no server, no build step. They can be:

- **Viewed in browser:** open the rendered preview, or clone the repo and open locally
- **Downloaded:** right-click → *Save link as*, or use the raw URL

| Artefact | View on GitHub | Live preview | Direct download (raw HTML) |
|----------|----------------|--------------|------------------------------|
| Interactive dashboard | [`ANC_Fertility_Dashboard_Ghana.html`](https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/blob/main/dashboard/ANC_Fertility_Dashboard_Ghana.html) | [Open preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/blob/main/dashboard/ANC_Fertility_Dashboard_Ghana.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/anc-spatial-ml-ghana/main/dashboard/ANC_Fertility_Dashboard_Ghana.html) |
| Conference poster | [`ANC_Fertility_Poster_Ghana.html`](https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/blob/main/poster/ANC_Fertility_Poster_Ghana.html) | [Open preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/anc-spatial-ml-ghana/blob/main/poster/ANC_Fertility_Poster_Ghana.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/anc-spatial-ml-ghana/main/poster/ANC_Fertility_Poster_Ghana.html) |

> **Tip:** the dashboard works fully offline once downloaded. The poster is print-ready at A0 (841 × 1189 mm).


---

## 9. Reporting Standard

This study follows the **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) reporting guideline for observational ecological studies.

---

## 10. Ethical Statement

This study used exclusively de-identified secondary data from the Ghana DHS programme. No primary data collection from human participants was conducted. DHS data were accessed under standard registration. Ethical review was therefore not required.

---

## 11. Citation

**APA:**
Ghanem, V. G. (2026). *Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022)*. GitHub. https://github.com/valentineghanem-bit/anc-spatial-ml-ghana

**BibTeX:**
```bibtex
@misc{ghanem2026ancspatial,
  author = {Ghanem, Valentine Golden},
  title  = {Temporal and Spatial Dynamics of Antenatal Care Coverage and Fertility Inequities in Ghana: A Subnational Ecological Study Using Nine DHS Survey Waves (1988–2022)},
  year   = {2026},
  url    = {https://github.com/valentineghanem-bit/anc-spatial-ml-ghana}
}
```

A machine-readable citation is provided in `CITATION.cff`.

---

## 12. License

Code is released under the **MIT License** — see [LICENSE](LICENSE) for details. Outputs: CC BY 4.0.

---

## 13. Author & Contact

- **Valentine Golden Ghanem**
  Ghana COCOBOD Cocoa Clinic, Accra, Ghana
  Email: [valentineghanem@gmail.com](mailto:valentineghanem@gmail.com)
  ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

---

## 14. Acknowledgements

- **Ghana Demographic and Health Survey programme** (ICF International) for survey data access under signed Data Use Agreement.
- **Ghana Statistical Service** for the 2021 Population and Housing Census and administrative boundary data.
- **WHO Global Health Observatory** for national-level indicators.

---

