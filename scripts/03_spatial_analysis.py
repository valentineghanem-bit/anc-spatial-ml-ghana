#!/usr/bin/env python3
"""
03_spatial_analysis.py — Ghana ANC Fertility Analysis (Part II)
Global Moran's I + Bivariate LISA (ANC × TFR co-clustering).

Tenet 5 (Spatial Autocorrelation First): Moran's I tested before any regression.
/uq-flag: z-score + p-value stated before interpretation.

Author : Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic
Date : April 2026
"""

import os
import pickle
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import geopandas as gpd
from libpysal.weights import KNN, Rook
from esda.moran import Moran, Moran_BV, Moran_Local_BV
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = 42
PERMS = 999
KNN_K = 8
ALPHA = 0.05

# Canonical values (QA-verified)
CANONICAL_MORANS_ANC = 0.43
CANONICAL_MORANS_TFR = 0.61


def compute_moran(values: np.ndarray, w, label: str) -> dict:
 """Compute Global Moran's I with /uq-flag output."""
 m = Moran(values, w, permutations=PERMS)
 print(f"\n[/uq-flag] {label} — Global Moran's I")
 print(f" I = {m.I:.4f} | EI = {m.EI:.4f} | z = {m.z_norm:.4f} | p = {m.p_norm:.4f}")
 print(f" Significant (α={ALPHA}): {m.p_norm < ALPHA}")
 return {"I": round(m.I,4), "EI": round(m.EI,4), "z": round(m.z_norm,4),
 "p": round(m.p_norm,4), "significant": m.p_norm < ALPHA}


def compute_bivariate_lisa(gdf: gpd.GeoDataFrame, anc_col: str, tfr_col: str, w) -> gpd.GeoDataFrame:
 """Bivariate LISA: ANC coverage × TFR (Rook contiguity, 999 permutations)."""
 bvlisa = Moran_BV(gdf[anc_col].values, gdf[tfr_col].values, w, permutations=PERMS)
 print(f"\n Bivariate Moran's I (ANC × TFR): {bvlisa.I:.4f} (p={bvlisa.p_sim:.4f})")

 bvlm = Moran_Local_BV(gdf[anc_col].values, gdf[tfr_col].values, w,
 transformation="r", permutations=PERMS, seed=SEED)
 gdf = gdf.copy()
 gdf["bv_lisa_I"] = bvlm.Is
 gdf["bv_lisa_p"] = bvlm.p_sim
 gdf["bv_lisa_q"] = bvlm.q
 q_map = {1:"High-High", 2:"Low-High", 3:"Low-Low", 4:"High-Low"}
 gdf["bv_lisa_quadrant"] = gdf.apply(
 lambda r: q_map.get(int(r["bv_lisa_q"]), "NS") if r["bv_lisa_p"] < ALPHA else "Not Significant",
 axis=1
 )
 clusters = gdf[gdf["bv_lisa_p"] < ALPHA].groupby("bv_lisa_quadrant").size()
 print(f" Significant LISA clusters (p<{ALPHA}): {clusters.to_dict()}")
 return gdf


def main() -> None:
 csv_path = os.path.join(os.path.dirname(REPO_ROOT), "Ghana_ANC_Fertility_Master_Dataset.csv")
 if not os.path.exists(csv_path):
  print("[03] Dataset not found. Run 01_data_preparation.py first.")
  return

  df = pd.read_csv(csv_path)
  df_2022 = df[df["wave_year"] == 2022].copy().reset_index(drop=True)

 # Region centroids (approximate Ghana legacy regions)
  centroids = {
  "Greater Accra":(5.6037,-0.187),"Ashanti":(6.747,-1.5209),"Western":(5.093,-2.336),
  "Central":(5.538,-1.198),"Eastern":(6.558,-0.425),"Volta":(7.0,-0.484),
  "Brong-Ahafo":(7.7,-1.98),"Northern":(9.5675,-0.5),
  "Upper East":(10.7,-0.824),"Upper West":(10.252,-2.323),
  }
  df_2022["latitude"] = df_2022["region"].map({k:v[0] for k,v in centroids.items()})
  df_2022["longitude"] = df_2022["region"].map({k:v[1] for k,v in centroids.items()})
  df_2022 = df_2022.dropna(subset=["latitude","longitude"])

  gdf = gpd.GeoDataFrame(df_2022, geometry=gpd.points_from_xy(df_2022.longitude, df_2022.latitude), crs="EPSG:4326")

  w_knn = KNN.from_dataframe(gdf, k=KNN_K)
  w_knn.transform = "r"
  w_rook = Rook.from_dataframe(gdf)
  w_rook.transform = "r"

  anc_col = next(c for c in gdf.columns if "anc_coverage" in c.lower())
  tfr_col = "tfr"

  mi_anc = compute_moran(gdf[anc_col].values, w_knn, "ANC Coverage (%)")
  mi_tfr = compute_moran(gdf[tfr_col].values, w_knn, "TFR")

  gdf = compute_bivariate_lisa(gdf, anc_col, tfr_col, w_rook)

  results = pd.DataFrame([{
  "wave_year": 2022,
  "morans_i_anc": mi_anc["I"], "morans_z_anc": mi_anc["z"], "morans_p_anc": mi_anc["p"],
  "morans_i_tfr": mi_tfr["I"], "morans_z_tfr": mi_tfr["z"], "morans_p_tfr": mi_tfr["p"],
  "lisa_hh_count": (gdf["bv_lisa_quadrant"]=="High-High").sum(),
  "lisa_ll_count": (gdf["bv_lisa_quadrant"]=="Low-Low").sum(),
  "weight_matrix": f"KNN k={KNN_K} row-standardised",
  "permutations": PERMS,
  }])
  out = os.path.join(os.path.dirname(REPO_ROOT), "data", "Spatial_Results_ANC_2022.csv")
  os.makedirs(os.path.dirname(out), exist_ok=True)
  results.to_csv(out, index=False)
  print(f"\n[03] ✓ Spatial results → {out}")


if __name__ == "__main__":
 main()
