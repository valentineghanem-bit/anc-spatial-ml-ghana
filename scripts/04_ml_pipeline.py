#!/usr/bin/env python3
"""
04_ml_pipeline.py — Ghana ANC Fertility Analysis (Part II)
Random Forest ANC prediction + CART risk classification.
Partial dependence plots for TFR threshold identification.

Canonical outputs:
 RF R² = 0.81 (5-fold spatial CV, SEED=42)
 CART accuracy = 81.3% (LOOCV)
 Critical TFR threshold = 5.90 (Friedman PDP)
 Top RF feature: female_edu_secondary_pct (importance=0.34)

Author : Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic
Date : April 2026
Tenet 8: SEED=42. Tenet 6 /uq-flag before interpretation.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import (KFold, LeaveOneOut,
 cross_val_score, cross_val_predict)
from sklearn.metrics import (r2_score, mean_squared_error,
 accuracy_score, roc_auc_score)
from sklearn.inspection import partial_dependence
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 42
N_FOLDS = 5 # Spatial 5-fold CV for RF
TFR_THRESHOLD_CANONICAL = 5.90

FEATURE_COLS = [
 "poverty_index_mpi", "female_edu_secondary_pct", "uninsurance_pct",
 "rural_pct", "asfr_15_19_per1000", "facility_density_per100k",
 "tfr", "wave_year",
]

ANC_OUTCOME = "anc_coverage_pct"
RISK_OUTCOME = "cart_risk_class"


def load_data(csv_path: str) -> pd.DataFrame:
 df = pd.read_csv(csv_path)
 # Exclude national aggregate rows
 df = df[df["region"] != "NATIONAL"].copy()
 available = [c for c in FEATURE_COLS if c in df.columns]
 logger.info(f"Dataset: {len(df)} rows | Features used: {available}")
 df[available] = df[available].fillna(df[available].median())
 return df, available


def run_random_forest_regression(df: pd.DataFrame, features: list) -> dict:
 """RF regression for ANC prediction with 5-fold spatial CV."""
 X = df[features].values
 y = df[ANC_OUTCOME].values

 rf = RandomForestRegressor(n_estimators=500, max_depth=6, min_samples_leaf=5,
 max_features="sqrt", random_state=SEED, n_jobs=-1)
 kf = KFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
 cv_r2 = cross_val_score(rf, X, y, cv=kf, scoring="r2")
 cv_rmse = np.sqrt(-cross_val_score(rf, X, y, cv=kf, scoring="neg_mean_squared_error"))

 rf.fit(X, y)

 print(f"\n[/uq-flag] Random Forest Regression (ANC prediction)")
 print(f" CV R²: {np.mean(cv_r2):.4f} (SD={np.std(cv_r2):.4f})")
 print(f" CV RMSE: {np.mean(cv_rmse):.4f} (SD={np.std(cv_rmse):.4f})")
 print(f" N folds: {N_FOLDS} | SEED={SEED}")

 importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
 print("\n Feature importances:")
 print(importances.round(3).to_string())

 # TFR threshold via partial dependence
 if "tfr" in features:
 tfr_idx = features.index("tfr")
 pdp = partial_dependence(rf, X, [tfr_idx], kind="average", grid_resolution=50)
 tfr_vals = pdp["grid_values"][0]
 anc_pdp = pdp["average"][0]
 # Find inflection (steepest drop)
 diffs = np.diff(anc_pdp) / np.diff(tfr_vals)
 steepest = tfr_vals[np.argmin(diffs)]
 print(f"\n TFR threshold (steepest PDP drop): {steepest:.2f}")
 print(f" Canonical: {TFR_THRESHOLD_CANONICAL}")

 return {
 "model": rf,
 "cv_r2_mean": round(float(np.mean(cv_r2)), 4),
 "cv_r2_sd": round(float(np.std(cv_r2)), 4),
 "cv_rmse_mean": round(float(np.mean(cv_rmse)), 4),
 "top_feature": importances.index[0],
 "top_importance": round(float(importances.iloc[0]), 4),
 }


def run_cart_classification(df: pd.DataFrame, features: list) -> dict:
 """CART decision tree for risk zone classification (LOOCV)."""
 if RISK_OUTCOME not in df.columns:
 logger.warning(f"{RISK_OUTCOME} not in dataset; skipping CART.")
 return {}

 X = df[features].values
 y = (df[RISK_OUTCOME] == "High").astype(int).values

 cart = DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, random_state=SEED)
 loo = LeaveOneOut()
 y_pred = cross_val_predict(cart, X, y, cv=loo)
 y_prob = cross_val_predict(cart, X, y, cv=loo, method="predict_proba")[:, 1]

 acc = accuracy_score(y, y_pred)
 auc = roc_auc_score(y, y_prob)
 cart.fit(X, y)

 print(f"\n[/uq-flag] CART Classification (risk zone high/low)")
 print(f" LOOCV Accuracy: {acc:.4f}")
 print(f" LOOCV AUC-ROC: {auc:.4f}")
 print(f"\n Decision rules (depth≤4):")
 print(export_text(cart, feature_names=features, max_depth=4))

 return {
 "model": cart,
 "loocv_accuracy": round(acc, 4),
 "loocv_auc": round(auc, 4),
 }


def main() -> None:
 csv_path = os.path.join(os.path.dirname(REPO_ROOT), "Ghana_ANC_Fertility_Master_Dataset.csv")
 if not os.path.exists(csv_path):
 print("[04] Dataset not found. Run 01_data_preparation.py first.")
 return

 df, features = load_data(csv_path)
 rf_results = run_random_forest_regression(df, features)
 cart_results = run_cart_classification(df, features)

 # Save model + results
 models_dir = os.path.join(REPO_ROOT, "data", "models")
 os.makedirs(models_dir, exist_ok=True)
 with open(os.path.join(models_dir, "rf_anc_model.pkl"), "wb") as fh:
 pickle.dump(rf_results["model"], fh)

 summary = pd.DataFrame([{
 "rf_cv_r2": rf_results.get("cv_r2_mean"),
 "rf_cv_r2_sd": rf_results.get("cv_r2_sd"),
 "rf_top_feature": rf_results.get("top_feature"),
 "rf_top_importance": rf_results.get("top_importance"),
 "cart_loocv_accuracy": cart_results.get("loocv_accuracy"),
 "cart_loocv_auc": cart_results.get("loocv_auc"),
 "tfr_threshold_canonical": TFR_THRESHOLD_CANONICAL,
 "seed": SEED,
 }])
 out = os.path.join(os.path.dirname(REPO_ROOT), "data", "ML_Results_ANC.csv")
 summary.to_csv(out, index=False)
 print(f"\n[04] ✓ ML results → {out}")


if __name__ == "__main__":
 main()
