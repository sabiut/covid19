import dash_table
from django_plotly_dash import DjangoDash
import pandas as pd

df = pd.read_csv('corona_old.csv')
app = DjangoDash('raw_table')
app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[
        {'name': i, 'id': i} for i in df.columns
    ],
    style_data_conditional=[{
        'if': {'column_id': 'TotalCases'},
        'backgroundColor': '#3D9970',
        'color': 'white',
    }]
)