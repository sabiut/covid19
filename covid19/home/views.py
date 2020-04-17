from django.shortcuts import render

import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo
import datetime


def home(request):
    df = pd.read_csv('corona.csv', skiprows=[1, 2, 3, 4, 5, 6, 7, 8, 221])
    labels = df['Country']
    values = df['TotalCases']
    data = [go.Pie(labels=labels,
                   text=["Date:" + df['date'][0]],
                   values=values,
                   textinfo='percent+label')]
    fig = go.Figure(data=data)
    pie_chart = pyo.plot(fig, auto_open=False, output_type='div')
    date = datetime.datetime.today().strftime('%d-%b-%Y')
    return render(request, 'home/welcome.html', locals())
