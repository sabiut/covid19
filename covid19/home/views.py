import os
import requests
from django.shortcuts import render
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo
import datetime
import folium

df = pd.read_csv('corona.csv', skiprows=[1, 2, 3, 4, 5, 6, 7, 8, 221])
url = '/home/sabiut/Documents/2020/COMPX532-20A/fnal_pro/covid19'
filename = 'corona.csv'


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
    monthly_cases = cases_per_month()
    my_map = test1()
    return render(request, 'home/welcome.html', locals())


def maps():
    fig = px.scatter_geo(df, locations="iso_alpha",
                         projection="natural earth",
                         color="Country",
                         hover_name="Country",
                         text="TotalCases",
                         size="NewCases",
                         labels="TotalRecovered",
                         color_continuous_scale=px.colors.diverging.Portland,
                         height=500)
    co_map = pyo.plot(fig, auto_open=False, output_type='div')
    return co_map


def funnel():
    fig1 = px.funnel_area(names=df['Country'],
                          values=df['TotalDeaths'],
                          )
    new_cases = pyo.plot(fig1, auto_open=False, output_type='div')
    return new_cases


def cases_per_month():
    df = pd.read_csv('report_2020-04-08.csv')
    month = df['date']
    confirm_cases = df['new_confirmed_cases']
    recover = df['new_recoveries']
    deaths = df['new_deaths']
    recover = df['new_recoveries']

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=month, y=confirm_cases, name='Confirm cases',
                             line=dict(color='firebrick', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=month, y=recover, name='Recovered cases',
                             line=dict(color='green', width=4, dash="dot")))
    fig.add_trace(go.Scatter(x=month, y=deaths, name='Deaths ',
                             line=dict(color='red', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title='Number of Covid-19 Cases per month',
                      xaxis_title='Month',
                      yaxis_title='Covid-19 Cases')

    month_cases = pyo.plot(fig, auto_open=False, output_type='div')
    return month_cases


def show_table(request):
    layout = go.Layout(title='Covid-19 Cases per Day',
                       )
    fig = go.Figure(layout=layout, data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.Country, df.TotalCases, df.NewCases, df.TotalDeaths, df.NewDeaths,
                           df.TotalRecovered, df.ActiveCases, df.Critical, df.TotalTests,
                           df.iso_alpha, df.date],
                   fill_color='lavender',
                   align='left'))
    ])

    shows_table = pyo.plot(fig, auto_open=False, output_type='div')
    return render(request, 'home/table.html', locals())


def test1():
    SF_COORDINATES = (-16.378575, 167.862999)
    crimedata = pd.read_csv('stat.csv')

    m = folium.Map(location=SF_COORDINATES,
                   zoom_start=10
                   )
    test = crimedata[['X', 'Y']]
    list = test.values.tolist()
    size = len(list)

    for each in range(0, size):
        folium.Marker(list[each],

                      popup="Village:" + str(crimedata['Village_Name'][each]) +
                            "\nMale:" + str(crimedata['Male'][each]) +
                            "\nFemale:" + str(crimedata['Female'][each]) +
                            "\nTotal Pop:" + str(crimedata['Totpop'][each]) +
                            "\nHH:" + str(crimedata['HH'][each]),
                      icon=folium.Icon(color='orange')).add_to(m)

    folium.Marker(
        location=[-16.308389, 168.267770],
        radius=50,
        popup='S/E Number of Villages: 21 Male:791 Female:758 Population:1,549 HH:457',
        color='#3186cc',
        fill=True,
        fill_color='#3186cc',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    folium.Marker(
        location=[-16.239604, 167.916719],
        popup='West Number of Villages: 34 Male:1428 Female:1389 Population:2,817 HH:642',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    folium.Marker(
        location=[-16.128442, 168.160146],
        popup='North Number of Villages: 50 Male:1459 Female:1560 Population:3,019 HH:664 ',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    folium.Marker(
        location=[-16.458311, 168.235905],
        popup='Number of Villages: 19 Male:867 Female:853 Population:1,720 HH:390',
        icon=folium.Icon(icon='cloud')
    ).add_to(m)

    folium.Circle(
        radius=100,
        location=[-16.350303, 168.272950],
        popup='Utas Polling Station',
        fill=True,
        opacity=8.8,
        stroke=True,
        weitht=1.0,
        color='red',
        fill_color='red'
    ).add_to(m)

    folium.Circle(
        radius=100,
        location=[-16.333166, 168.300781],
        popup='Ulei Polling Station',
        fill=True,
        opacity=8.8,
        stroke=True,
        weitht=1.0,
        color='red',
        fill_color='red'

    ).add_to(m)

    folium.Circle(
        radius=100,
        location=[-16.357205, 168.252766],
        popup='Moru harbour',
        fill=True,
        color='yellow'

    ).add_to(m)

    folium.Circle(
        radius=100,
        location=[-16.357805, 168.233938],
        popup='Taveak harbour',
        fill=True,
        color='yellow'

    ).add_to(m)
    m = m._repr_html_()
    return m


def test(request):
    my_map = test1()
    return render(request, 'home/map.html', locals())
