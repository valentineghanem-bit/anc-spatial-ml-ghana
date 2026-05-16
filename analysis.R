# analysis.R — ANC Coverage & Fertility Inequities, Ghana 9 DHS Waves
# Mixed-effects models + Gini decomposition + spatial autocorrelation
# Author: Valentine Golden Ghanem | ORCID: 0009-0002-8332-0220
# Usage: Rscript analysis.R
suppressPackageStartupMessages({
  library(lme4)
  library(lmerTest)
  library(spdep)
  library(ineq)      # Gini
  library(dplyr)
  library(readr)
  library(ggplot2)
})
set.seed(42)

cat("── Loading data ──────────────────────────────────────────────────────\n")
df <- read_csv("data/Ghana_ANC_Fertility_Master_Dataset.csv",
               show_col_types = FALSE)
cat(sprintf("Loaded: %d region-wave obs × %d variables\n", nrow(df), ncol(df)))
waves <- sort(unique(df$wave_year))
cat("Survey waves:", paste(waves, collapse = ", "), "\n")

# ── 1. Gini coefficient over time ─────────────────────────────────────────────
cat("\n── Gini Coefficient (ANC coverage) by wave ───────────────────────────\n")
gini_tbl <- df |>
  filter(!is.na(anc_coverage_pct)) |>
  group_by(wave_year) |>
  summarise(gini_anc = round(ineq(anc_coverage_pct, type = "Gini"), 4),
            mean_anc = round(mean(anc_coverage_pct), 1),
            mean_tfr = round(mean(tfr, na.rm = TRUE), 2),
            .groups = "drop")
print(gini_tbl)

# ── 2. Mixed-effects model: ANC ~ TFR + time + (1|region) ────────────────────
cat("\n── Linear mixed-effects model: ANC ~ TFR + wave + (1|region) ─────────\n")
m1 <- lmer(anc_coverage_pct ~ tfr + wave_year + poverty_index_mpi +
             female_edu_secondary_pct + (1 | region),
           data = df, REML = FALSE)
print(summary(m1))
cat(sprintf("  Random effect (region) variance: %.4f\n",
            as.numeric(VarCorr(m1)$region)))

# ── 3. Model with interaction: TFR × wave ────────────────────────────────────
cat("\n── Model with TFR × wave interaction ────────────────────────────────\n")
m2 <- lmer(anc_coverage_pct ~ tfr * wave_year + (1 | region),
           data = df, REML = FALSE)
cat(sprintf("  AIC m1=%.2f  AIC m2=%.2f  (interaction term)\n",
            AIC(m1), AIC(m2)))
print(anova(m1, m2))

# ── 4. CEI model: what drives Care Efficiency Index? ─────────────────────────
cat("\n── Mixed model: CEI predictors ───────────────────────────────────────\n")
if ("cei" %in% names(df)) {
  m_cei <- lmer(cei ~ tfr + poverty_index_mpi + female_edu_secondary_pct +
                  wave_year + (1 | region),
                data = df, REML = FALSE)
  print(summary(m_cei)$coefficients)
}

# ── 5. Temporal Moran's I (latest wave) ───────────────────────────────────────
cat("\n── Spatial autocorrelation — latest wave ─────────────────────────────\n")
latest <- df |> filter(wave_year == max(wave_year)) |>
  arrange(region_code)
if (nrow(latest) >= 5) {
  nb_ring <- cell2nb(nrow = 4, ncol = ceiling(nrow(latest) / 4))
  W_r <- nb2listw(nb_ring, style = "W", zero.policy = TRUE)
  mi <- moran.test(latest$anc_coverage_pct, W_r, zero.policy = TRUE)
  cat(sprintf("  ANC Moran I = %.4f (z=%.3f, p=%.4f)\n",
              mi$estimate[1], mi$statistic, mi$p.value))
}

# ── 6. North–South ANC gap ────────────────────────────────────────────────────
cat("\n── North–South ANC gap by wave ───────────────────────────────────────\n")
north <- c("Northern", "Upper East", "Upper West", "Savannah",
           "North East", "Oti", "Bono East")
df_ns <- df |>
  mutate(zone = if_else(region %in% north, "North", "South")) |>
  group_by(wave_year, zone) |>
  summarise(mean_anc = round(mean(anc_coverage_pct, na.rm=TRUE), 1),
            .groups = "drop") |>
  tidyr::pivot_wider(names_from = zone, values_from = mean_anc) |>
  mutate(gap = round(South - North, 1))
print(df_ns)
cat("\nAnalysis complete.\n")
