import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash

df_country = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
# clean data
df_country.columns = map(str.lower, df_country.columns)
# rename headers
df_country = df_country.rename(columns={'country_region': 'country'})

app = DjangoDash('pubble_chart')

country_options = []
for country in df_country['country']:
    country_options.append({'label': str(country), 'value': country})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='country_picker', options='country_options', value=df_country['country']=='world')
])


@app.callback(Output('graph', 'figure'),
              [Input('country_picker', 'value')])
def update_figure(selected_country):

    filtered_df = df_country[df_country['country'] == selected_country]
    df_list = [df_confirmed_case, df_death, df_recovered]

    traces = []
    for country_name in filtered_df['country']:
        df_by_country = filtered_df[filtered_df['country'] == country_name]
        traces.append(px.scatter(df_by_country, x="country", y="confirmed", size="confirmed", color="country",
                                 hover_name="country", size_max=60))
    return {'data': traces,
            'layout': px.update_layout(
                xaxis_title="Countries",
                yaxis_title="Confirmed Cases",
                width=900,
                height=700,
            )}
