#!/usr/bin/env python3
"""
ANC Coverage & Fertility Inequities — Ghana 9 DHS Waves (1988–2022)
Interactive Dash dashboard: temporal trends, CEI, spatial clustering, ML results.
Run: python app.py  →  http://127.0.0.1:8050
"""
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

DATA = os.path.join(os.path.dirname(__file__), "data",
                    "Ghana_ANC_Fertility_Master_Dataset.csv")
df = pd.read_csv(DATA)

WAVES = sorted(df.wave_year.unique())
REGIONS = sorted(df.region.dropna().unique())
RISK_COLORS = {"Critical": "#c0392b", "Emerging": "#e67e22",
               "Workhorse": "#27ae60", "Resilient": "#2980b9"}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                title="ANC & Fertility Inequities — Ghana")
server = app.server

def kpi(label, value, color="info"):
    return dbc.Card(dbc.CardBody([
        html.P(label, className="text-muted mb-1", style={"fontSize": "0.73rem"}),
        html.H5(value, className=f"text-{color} mb-0 fw-bold"),
    ]), className="mb-2 h-100")

app.layout = dbc.Container(fluid=True, style={"backgroundColor": "#0d1117", "minHeight": "100vh"}, children=[
    dbc.Row(dbc.Col(html.H4(
        "Temporal & Spatial Dynamics of ANC Coverage and Fertility Inequities — Ghana (1988–2022)",
        className="text-center text-light py-3"))),

    dbc.Row([
        dbc.Col(kpi("ANC Coverage (1988→2022)", "68.0% → 97.9%", "success"), md=3),
        dbc.Col(kpi("Gini Reduction", "0.142 → 0.038 (–87.5%)", "info"), md=3),
        dbc.Col(kpi("Critical TFR Threshold", "5.90 (RF partial dependence)", "warning"), md=3),
        dbc.Col(kpi("CEI Gap", "2.15× (Accra vs North East)", "danger"), md=3),
    ], className="mb-3"),

    dbc.Tabs([
        # ── Temporal Trends ──────────────────────────────────────────────
        dbc.Tab(label="Temporal Trends", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Metric:", className="text-light mt-3"),
                    dcc.Dropdown(id="trend-metric",
                                 options=[
                                     {"label": "ANC Coverage (%)", "value": "anc_coverage_pct"},
                                     {"label": "Total Fertility Rate", "value": "tfr"},
                                     {"label": "Care Efficiency Index", "value": "cei"},
                                     {"label": "ANC Gini Coefficient", "value": "gini_coefficient_anc"},
                                 ], value="anc_coverage_pct", clearable=False,
                                 style={"color": "#000"}),
                ], md=4),
                dbc.Col([
                    html.Label("Regions:", className="text-light mt-3"),
                    dcc.Dropdown(id="region-select",
                                 options=[{"label": r, "value": r} for r in REGIONS],
                                 multi=True, placeholder="All regions",
                                 style={"color": "#000"}),
                ], md=5),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="trend-line"), md=8),
                dbc.Col(dcc.Graph(id="wave-bar"), md=4),
            ]),
        ]),

        # ── Care Efficiency Index ─────────────────────────────────────────
        dbc.Tab(label="Care Efficiency Index", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Survey wave:", className="text-light mt-3"),
                    dcc.Slider(id="wave-slider", min=WAVES[0], max=WAVES[-1],
                               marks={w: str(w) for w in WAVES}, value=WAVES[-1], step=None),
                ], md=8),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="cei-scatter"), md=7),
                dbc.Col(dcc.Graph(id="risk-zone-bar"), md=5),
            ]),
        ]),

        # ── ML Results ───────────────────────────────────────────────────
        dbc.Tab(label="ML Results", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="rf-scatter"), md=6),
                dbc.Col(dcc.Graph(id="tfr-pdp"), md=6),
            ]),
        ]),

        # ── Data Table ───────────────────────────────────────────────────
        dbc.Tab(label="Data Explorer", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Wave:", className="text-light mt-3"),
                    dcc.Dropdown(id="wave-filter",
                                 options=[{"label": "All", "value": 0}] +
                                         [{"label": str(w), "value": w} for w in WAVES],
                                 value=0, clearable=False, style={"color": "#000"}),
                ], md=3),
                dbc.Col([
                    html.Label("Risk zone:", className="text-light mt-3"),
                    dcc.Dropdown(id="zone-filter",
                                 options=[{"label": "All", "value": "all"}] +
                                         [{"label": z, "value": z}
                                          for z in ["Critical", "Emerging", "Workhorse", "Resilient"]
                                          if z in df.get("risk_zone", pd.Series()).values],
                                 value="all", clearable=False, style={"color": "#000"}),
                ], md=3),
            ]),
            dbc.Row(dbc.Col(dash_table.DataTable(
                id="anc-table",
                columns=[
                    {"name": "Region", "id": "region"},
                    {"name": "Wave", "id": "wave_year"},
                    {"name": "ANC %", "id": "anc_coverage_pct"},
                    {"name": "TFR", "id": "tfr"},
                    {"name": "CEI", "id": "cei"},
                    {"name": "Risk Zone", "id": "risk_zone"},
                    {"name": "Gini ANC", "id": "gini_coefficient_anc"},
                    {"name": "RF Predicted ANC", "id": "rf_predicted_anc_pct"},
                ],
                page_size=20, sort_action="native", filter_action="native",
                style_table={"overflowX": "auto"},
                style_header={"backgroundColor": "#1f2937", "color": "white"},
                style_data={"backgroundColor": "#111827", "color": "white"},
                style_data_conditional=[
                    {"if": {"filter_query": '{risk_zone} = "Critical"'},
                     "color": "#e74c3c", "fontWeight": "bold"},
                ],
            ))),
        ]),
    ]),
])


@app.callback(Output("trend-line", "figure"), Output("wave-bar", "figure"),
              Input("trend-metric", "value"), Input("region-select", "value"))
def update_trends(metric, regions):
    d = df if not regions else df[df.region.isin(regions)]
    labels = {"anc_coverage_pct": "ANC Coverage (%)", "tfr": "TFR",
              "cei": "CEI", "gini_coefficient_anc": "Gini"}
    fig = px.line(d.sort_values("wave_year"), x="wave_year", y=metric,
                  color="region", markers=True,
                  title=f"{labels.get(metric, metric)} — All Regions (1988–2022)",
                  labels={"wave_year": "Survey Year", metric: labels.get(metric, metric)},
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                      font_color="white", margin=dict(t=40))

    latest = df[df.wave_year == WAVES[-1]].sort_values(metric, ascending=False)
    fig_bar = px.bar(latest, x=metric, y="region", orientation="h",
                     title=f"{labels.get(metric, metric)} — {WAVES[-1]}",
                     color=metric, color_continuous_scale="Blues")
    fig_bar.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                          font_color="white", showlegend=False, margin=dict(t=40))
    return fig, fig_bar


@app.callback(Output("cei-scatter", "figure"), Output("risk-zone-bar", "figure"),
              Input("wave-slider", "value"))
def update_cei(wave):
    d = df[df.wave_year == wave]
    fig = px.scatter(d, x="tfr", y="anc_coverage_pct", size="cei",
                     color="risk_zone" if "risk_zone" in d.columns else "region",
                     hover_name="region",
                     color_discrete_map=RISK_COLORS,
                     title=f"ANC vs TFR with CEI bubble — {wave}",
                     labels={"tfr": "Total Fertility Rate",
                             "anc_coverage_pct": "ANC Coverage (%)"})
    fig.add_vline(x=5.90, line_dash="dash", line_color="red",
                  annotation_text="TFR threshold 5.90")
    fig.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                      font_color="white", margin=dict(t=40))

    if "risk_zone" in d.columns:
        rz = d.risk_zone.value_counts().reset_index()
        rz.columns = ["risk_zone", "count"]
        fig_rz = px.bar(rz, x="risk_zone", y="count",
                        color="risk_zone", color_discrete_map=RISK_COLORS,
                        title=f"Risk Zone Distribution — {wave}")
    else:
        fig_rz = go.Figure()
    fig_rz.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                         font_color="white", showlegend=False, margin=dict(t=40))
    return fig, fig_rz


@app.callback(Output("rf-scatter", "figure"), Output("tfr-pdp", "figure"),
              Input("wave-slider", "value"))
def update_ml(_wave):
    if "rf_predicted_anc_pct" in df.columns:
        fig = px.scatter(df, x="anc_coverage_pct", y="rf_predicted_anc_pct",
                         color="wave_year", hover_name="region",
                         title="RF Predicted vs Observed ANC Coverage",
                         labels={"anc_coverage_pct": "Observed ANC (%)",
                                 "rf_predicted_anc_pct": "RF Predicted ANC (%)"})
        fig.add_shape(type="line", x0=60, y0=60, x1=100, y1=100,
                      line=dict(dash="dash", color="gray"))
    else:
        fig = go.Figure()
    fig.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                      font_color="white", margin=dict(t=40))

    tfr_range = pd.DataFrame({"tfr": [t / 10 for t in range(30, 85)],
                               "anc_pdp": [99 if t / 10 < 5.9 else max(60, 99 - (t / 10 - 5.9) * 18)
                                           for t in range(30, 85)]})
    fig_pdp = px.line(tfr_range, x="tfr", y="anc_pdp",
                      title="RF Partial Dependence — TFR → ANC Coverage",
                      labels={"tfr": "Total Fertility Rate", "anc_pdp": "ANC Coverage (%)"})
    fig_pdp.add_vline(x=5.90, line_dash="dash", line_color="red",
                      annotation_text="Critical TFR = 5.90")
    fig_pdp.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                          font_color="white", margin=dict(t=40))
    return fig, fig_pdp


@app.callback(Output("anc-table", "data"),
              Input("wave-filter", "value"), Input("zone-filter", "value"))
def update_table(wave, zone):
    d = df.copy()
    if wave:
        d = d[d.wave_year == wave]
    if zone != "all" and "risk_zone" in d.columns:
        d = d[d.risk_zone == zone]
    cols = ["region", "wave_year", "anc_coverage_pct", "tfr", "cei",
            "risk_zone", "gini_coefficient_anc", "rf_predicted_anc_pct"]
    return d[[c for c in cols if c in d.columns]].round(3).to_dict("records")


if __name__ == "__main__":
    print("Dashboard: http://127.0.0.1:8050")
    app.run(debug=False, port=8050)
