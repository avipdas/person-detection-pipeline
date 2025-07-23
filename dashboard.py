import dash
import time
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import json

def load_logs(path="anomaly_log.jsonl"):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def init_dashboard(server):
    dash_app = dash.Dash(
        __name__, server=server, url_base_pathname="/dashboard/", external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    df = load_logs()
    if df.empty:
        df = pd.DataFrame(columns=["frame", "track_id", "type", "timestamp"])

    summary = df["type"].value_counts().to_frame().reset_index()
    summary.columns = ["Anomaly Type", "Count"]

    dash_app.layout = dbc.Container([
        html.H2("Anomaly Dashboard"),
        html.Video(src=f"/static/output.mp4?v={int(time.time())}", controls=True, style={"width": "100%", "maxWidth": "640px"}), 
        html.Hr(),
        html.H4("Anomaly Log"),
        dcc.Graph(
            figure={
                "data": [
                    {"x": summary["Anomaly Type"], "y": summary["Count"], "type": "bar"}
                ],
                "layout": {"title": "Anomaly Type Frequency"}
            }
        ),
        html.Div([
            html.H5("Raw Logs:"),
            html.Pre(df.to_string(index=False))
        ])
    ])
