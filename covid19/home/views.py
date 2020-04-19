from django.shortcuts import render
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo
import datetime

df = pd.read_csv('corona.csv', skiprows=[1, 2, 3, 4, 5, 6, 7, 8, 221])


def home(request):
    labels = df['Country']
    values = df['TotalCases']
    data = [go.Pie(labels=labels,
                   text=["Date:" + df['date'][0]],
                   values=values,
                   textinfo='percent+label')]
    fig = go.Figure(data=data)
    pie_chart = pyo.plot(fig, auto_open=False, output_type='div')
    date = datetime.datetime.today().strftime('%d-%b-%Y')

    # Funnel chart
    new_cases = funnel()
    co_map = maps()
    return render(request, 'home/welcome.html', locals())


def maps():
    fig = px.scatter_geo(df, locations="iso_alpha",
                         projection="natural earth",
                         color="TotalCases",
                         hover_name="Country",
                         text='TotalRecovered',
                         labels='TotalCases',
                         size="TotalDeaths",
                         color_continuous_scale=px.colors.diverging.Portland,
                         height=500)
    co_map = pyo.plot(fig, auto_open=False, output_type='div')
    return co_map


def funnel():
    fig1 = px.funnel_area(names=df['Country'],
                          values=df['NewCases'],
                          )
    new_cases = pyo.plot(fig1, auto_open=False, output_type='div')
    return new_cases
