import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from django_plotly_dash import DjangoDash

df = pd.read_csv("corona.csv"
                 )
mgr_options = df["Country"].unique()

app = DjangoDash('simple_example')

app.layout = html.Div([
    html.H2("Sales Funnel Report"),
    html.Div(
        [
            dcc.Dropdown(
                id="Country",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='All Managers'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Country', 'value')])
def update_graph(Country):
    if Country == "Country":
        df_plot = df.copy()
    else:
        df_plot = df[df['Country'] == Country]

    pv = pd.pivot_table(
        df_plot,
        index=[''],
        columns=["Country"],
        values=['TotalCases', 'NewCases', 'TotalDeaths', 'TotalRecovered'],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[('TotalCases')], name='Declined')
    trace2 = go.Bar(x=pv.index, y=pv[('NewCases')], name='Pending')
    trace3 = go.Bar(x=pv.index, y=pv[('TotalDeaths')], name='Presented')
    trace4 = go.Bar(x=pv.index, y=pv[('TotalRecovered')], name='Won')

    return {
        'data': [trace1, trace2, trace3, trace4],
        'layout':
            go.Layout(
                title='Customer Order Status for {}'.format(Country),
                barmode='stack')
    }


