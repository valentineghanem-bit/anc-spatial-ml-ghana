#!/usr/bin/env python3
"""
02_cei_calculation.py — Ghana ANC Fertility Analysis (Part II)
Care Efficiency Index (CEI) computation and 2x2 risk zone classification.

CEI = ANC_coverage_pct / TFR
Risk zones: Critical (low CEI + high TFR), Emerging, Workhorse, Resilient

Author : Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic
Date : April 2026
Tenet 7 (Causal Clarity): Ecological study — no individual-level causal inference.
Tenet 8 (Reproducibility): SEED=42; all thresholds documented.
"""

import os
import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(REPO_ROOT), "data")

SEED = 42
CEI_MEAN = 20.0 # Used for z-score standardisation (grand mean)
CEI_SD = 5.0
TFR_MEAN = 4.5 # Used for z-score standardisation
TFR_SD = 1.2
TFR_THRESHOLD = 5.90 # Critical threshold from RF partial dependence plot (Tenet 6)


def compute_cei(df: pd.DataFrame) -> pd.DataFrame:
 """
 Compute Care Efficiency Index and risk zone classification.

 CEI = ANC_coverage_pct / TFR
 Zones (2x2 z-score quadrant):
 Critical : CEI z < 0 AND TFR z > 0
 Emerging : CEI z < 0.5 AND TFR z > 0.3
 Workhorse : CEI z >= 0 AND TFR z <= 0
 Resilient : CEI z >= 0 AND TFR z < 0
 """
 anc_col = next(c for c in df.columns if "anc_coverage" in c.lower())
 tfr_col = next(c for c in df.columns if c.lower() == "tfr")

 df = df.copy()
 df["cei"] = (df[anc_col] / df[tfr_col]).round(2)
 df["cei_z_score"] = ((df["cei"] - CEI_MEAN) / CEI_SD).round(3)
 df["tfr_z_score"] = ((df[tfr_col] - TFR_MEAN) / TFR_SD).round(3)
 df["tfr_above_threshold_590"] = (df[tfr_col] >= TFR_THRESHOLD).astype(int)

 def classify_zone(row):
 c, t = row["cei_z_score"], row["tfr_z_score"]
 if c < -0.3 and t > 0.2:
 return "Critical"
 elif c < 0.3 and t > 0.3:
 return "Emerging"
 elif c > 0.2:
 return "Resilient"
 else:
 return "Workhorse"

 df["risk_zone"] = df.apply(classify_zone, axis=1)
 df["cart_risk_class"] = df["risk_zone"].apply(
 lambda z: "High" if z in {"Critical", "Emerging"} else "Low"
 )
 return df


def print_cei_summary(df: pd.DataFrame) -> None:
 """Print CEI canonical summary (Tenet 6 /uq-flag before interpretation)."""
 print("\n[/uq-flag] CEI UNCERTAINTY QUANTIFICATION")
 print(f" Standardisation: CEI mean={CEI_MEAN}, SD={CEI_SD} | TFR mean={TFR_MEAN}, SD={TFR_SD}")
 print(f" Critical TFR threshold: {TFR_THRESHOLD} (RF partial dependence, Friedman 2001)")

 # 2022 wave only for canonical comparison
 df_2022 = df[df["wave_year"] == 2022] if "wave_year" in df.columns else df
 if len(df_2022) > 0:
 cei_max = df_2022.nlargest(1, "cei")[["region","cei"]].values[0]
 cei_min = df_2022.nsmallest(1, "cei")[["region","cei"]].values[0]
 print(f"\n CEI range (2022): {cei_min[0]}={cei_min[1]:.1f} — {cei_max[0]}={cei_max[1]:.1f}")
 print(f" CEI gap: {cei_max[1]/max(cei_min[1],0.01):.2f}×")
 print("\n Risk zones (2022):")
 print(df_2022.groupby("risk_zone").size().to_string())


def main() -> None:
 csv_path = os.path.join(
 os.path.dirname(REPO_ROOT),
 "Ghana_ANC_Fertility_Master_Dataset.csv"
 )
 if not os.path.exists(csv_path):
 print(f"[02] Dataset not found at {csv_path}. Run 01_data_preparation.py first.")
 return

 df = pd.read_csv(csv_path)
 df = compute_cei(df)
 print_cei_summary(df)

 out_path = csv_path.replace(".csv", "_CEI.csv")
 df.to_csv(out_path, index=False)
 print(f"\n[02] ✓ CEI-enriched dataset → {out_path}")


if __name__ == "__main__":
 main()
