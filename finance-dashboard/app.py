import pandas as pd
import yfinance as yf
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots
from dbops import DatabaseOps

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(id="title", style={"textAlign": "center"}),
    html.H2(id="name", style={"textAlign": "center", "margin": "10px"}),

    # Ticker input box and period selection buttons
    html.Div(
        children=[
        dcc.Input(id="ticker", value="AAPL", type="text"),
        dbc.RadioItems(
            id="radios",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "1min", "value": "1Min"},
                {"label": "5min", "value": "5Min"},
                {"label": "10min", "value": "10Min"},
                {"label": "30min", "value": "30Min"},
                {"label": "1h", "value": "1h"},
                {"label": "4h", "value": "4h"},
                {"label": "1d", "value": "1d"},
                {"label": "1wk", "value": "5d"}
            ],
            value="5Min",
            style={"display": "flex", "flexDirection": "Horizontal"})],
        style={"justifyContent": "left", "margin": "10px 15%"}),

    # Graph
    html.Div(children=dcc.Graph(id="fig"),
             style={"width": "75%", "margin": "auto", "alignItems": "center", "justifyContent": "center"}),
    dcc.Interval(id="time-count", interval=60000)
])

@app.callback(
    Output(component_id="title", component_property="children"),
    Output(component_id="fig", component_property="figure"),
    Input(component_id="ticker", component_property="value"),
    Input(component_id="radios", component_property="value"),
    Input(component_id="time-count", component_property="n_intervals")
)
def update_ticker(input_ticker: str, time_frame: str, n_intervals: int):

    # Fetch data from yfinance
    stock = yf.Ticker(input_ticker)
    name = stock.info["shortName"]
    if time_frame == "1Min":
        df = stock.history(period="7d", interval="1m")\
            .resample(time_frame)\
            .agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last','Volume':'sum'})\
            .dropna()
    else:
        df = stock.history(period="60d", interval="5m") \
            .resample(time_frame) \
            .agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last','Volume':'sum'}) \
            .dropna()

    # Create Moving Average Columns
    df["MA12"] = df["Close"].rolling(window=12).mean()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA26"] = df["Close"].rolling(window=26).mean()
    df["MA20-stddev"] = df["Close"].rolling(window=20).std(ddof=0)

    # Drop NA rows, otherwise there will be residuals from last graph shown
    df.dropna()

    fig = plotly.subplots.make_subplots(rows=2,
                                        cols=1,
                                        shared_xaxes=True,
                                        shared_yaxes=False,
                                        vertical_spacing=0.1,
                                        subplot_titles=("Price", "Volume"),
                                        row_width=[0.2, 0.7])

    # Add price plot with log y-axis
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df["Open"],
                                 high=df["High"],
                                 low=df["Low"],
                                 close=df["Close"],
                                 name="Price",
                                 showlegend=False),
                  row=1,
                  col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=df["MA12"],
                             name="MA12",
                             showlegend=True),
                  row=1,
                  col=1)

    fig.add_trace(go.Scatter(x=df.index,
                             y=df["MA20"],
                             name="MA20",
                             marker={"color": "orange"},
                             showlegend=True),
                  row=1,
                  col=1)

    # Upper Bollinger Band on MA20
    fig.add_trace(go.Scatter(x=df.index,
                             y=df["MA20"] + 2*df["MA20-stddev"],
                             line={"dash": "dot"},
                             marker={"color": "grey"},
                             showlegend=False),
                  row=1,
                  col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=df["MA20"] - 2*df["MA20-stddev"],
                             line={"dash": "dot"},
                             marker={"color": "grey"},
                             fill="tonexty",
                             showlegend=False),
                  row=1,
                  col=1)

    fig.add_trace(go.Scatter(x=df.index,
                             y=df["MA26"],
                             name="MA26",
                             showlegend=True),
                  row=1,
                  col=1)
    fig.update_yaxes(type="log", row=1, col=1)

    fig.add_trace(go.Bar(x=df.index,
                         y=df["Volume"],
                         name="Volume",
                         marker={'color': "#0068ff"},
                         showlegend=False),
                  row=2,
                  col=1)

    fig.update_xaxes(
        rangeslider_visible=False,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )

    return f"{name} ({str.upper(input_ticker)})", fig


if __name__ == "__main__":
    app.run_server(debug=True)