import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("C:/Users/User/Desktop/un-greenhouse-gas-data/UNdata_Export_co2.csv")
df2 = pd.read_csv("C:/Users/User/Desktop/un-greenhouse-gas-data/UNdata_Export_methane.csv")
df3 = pd.read_csv("C:/Users/User/Desktop/un-greenhouse-gas-data/UNdata_Export_hfc.csv")
df4 = pd.read_csv("C:/Users/User/Desktop/un-greenhouse-gas-data/UNdata_Export_greenhouse_gas.csv")

df["Gas"] = "CO2"
df2["Gas"] = "Methane"
df3["Gas"] = "HFC"
df4["Gas"] = "GHG"

df_all = pd.concat([df, df2, df3, df4], ignore_index=True)

countries = df_all["Country or Area"].unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("UN Emissions Dashboard", style={"textAlign": "center"}),
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in countries],
        value="Ukraine"   # Default country
    ),
    dcc.Graph(id="emission-graph")
])

@app.callback(
    Output("emission-graph", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(selected_country):
    df_country = df_all[df_all["Country or Area"] == selected_country]
    fig = px.line(df_country, x="Year", y="Value", color="Gas",
                  title=f"Emissions Over Time in {selected_country}")
    return fig

if __name__ == "__main__":
    app.run(debug=True)
