from __future__ import print_function

import os
import requests
from django.shortcuts import render
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as pyo
import datetime
import folium
import numpy as np
# Data from John hopkins University
df_country = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
df_recovered = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
df_death = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_confirmed_case = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

# clean data
df_country.columns = map(str.lower, df_country.columns)
df_recovered.columns = map(str.lower, df_recovered.columns)
df_death.columns = map(str.lower, df_death.columns)
df_confirmed_case.columns = map(str.lower, df_confirmed_case.columns)

# rename headers
df_recovered = df_recovered.rename(columns={'province/state': 'state', 'country/region': 'country'})
df_death = df_death.rename(columns={'province/state': 'state', 'country/region': 'country'})
df_confirmed_case = df_confirmed_case.rename(columns={'province/state': 'state', 'country/region': 'country'})
df_country = df_country.rename(columns={'country_region': 'country'})


def home(request):
    labels = df_country['country']
    values = df_country['active']
    data = [go.Pie(labels=labels,
                   values=values,
                   textinfo='percent+label')]
    fig = go.Figure(data=data)

    pie_chart = pyo.plot(fig, auto_open=False, output_type='div')
    date = datetime.datetime.today().strftime('%d-%b-%Y')

    # Funnel chart
    new_cases = bubble_chart(30)
    co_map = covid_map()
    monthly_cases = cases_per_month()
    daily_cases = line_graph('world')
    my_map = test1()
    return render(request, 'home/welcome.html', locals())


def covid_map():
    global_map = folium.Map(location=[1, 0], zoom_start=1, max_zoom=6, min_zoom=0.500)

    for cases in range(0, len(df_confirmed_case)):
        folium.Circle(
            location=[df_confirmed_case.iloc[cases]['lat'], df_confirmed_case.iloc[cases]['long']],
            fill=True,
            radius=(int((np.log(df_confirmed_case.iloc[cases, -1] + 1.00001))) + 0.2) * 50000,
            color='red',
            fill_color='indigo',
            tooltip="<div style='margin: 0; background-color: Green; color: orange;'>" +
                    "<h4 style='text-align:center;font-weight: bold'>" + df_confirmed_case.iloc[cases][
                        'country'] + "</h4>"
                                     "<hr style='margin:10px;color: white;'>" +
                    "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>" +
                    "<li>Confirmed: " + str(df_confirmed_case.iloc[cases, -1]) + "</li>" +
                    "<li>Deaths:   " + str(df_death.iloc[cases, -1]) + "</li>" +
                    "<li>Death Rate: " + str(
                np.round(df_death.iloc[cases, -1] / (df_confirmed_case.iloc[cases, -1] + 1.00001) * 100, 2)) + "</li>" +
                    "</ul></div>",
        ).add_to(global_map)

    global_map = global_map._repr_html_()
    return global_map


def bubble_chart(n):
    sorted_country_df = df_country.sort_values('confirmed', ascending=False)
    fig = px.scatter(sorted_country_df.head(n), x="country", y="confirmed", size="confirmed", color="country",
                     hover_name="country", size_max=60)
    fig.update_layout(
        xaxis_title="Countries",
        yaxis_title="Confirmed Cases",
        width=900,

    )
    new_cases = pyo.plot(fig, auto_open=False, output_type='div')
    return new_cases


# def funnel():
#     fig1 = px.funnel_area(names=df['Country'],
#                           values=df['TotalDeaths'],
#                           )
#     new_cases = pyo.plot(fig1, auto_open=False, output_type='div')
#     return new_cases
#

def cases_per_month():
    df = pd.read_csv('/home/ubuntu/project/covid19/covid19/covid19/static/report_2020-04-08.csv')
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
                      yaxis_title='Covid-19 Cases',
                      width=900,

                      ),

    month_cases = pyo.plot(fig, auto_open=False, output_type='div')
    return month_cases


def line_graph(country):
    labels = ['confirmed', 'deaths', 'recovered']
    colors = ['blue', 'red', 'green']
    line_size = [1, 1, 1]

    df_list = [df_confirmed_case, df_death, df_recovered]

    fig = go.Figure()

    for i, df in enumerate(df_list):
        country = 'world'
        x_data = np.array(list(df.iloc[:, 20:].columns))
        y_data = np.sum(np.asarray(df.iloc[:, 6:]), axis=0)
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                                 name=labels[i],
                                 line=dict(color=colors[i], width=line_size[i]),
                                 connectgaps=True,
                                 text="Total " + str(labels[i]) + ": " + str(y_data[-1])
                                 ))
        fig.update_layout(
            title=country + " " + "COVID-19 Cases",
            xaxis_title='Date',
            yaxis_title='No. of Confirmed Cases',
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="lightgrey",
            width=800,

        )
    fig.update_yaxes(type="linear")
    test_plot = pyo.plot(fig, auto_open=False, output_type='div')
    return test_plot


def show_table(request):
    layout = go.Layout(title='Covid-19 Cases per Day',
                       )
    fig = go.Figure(layout=layout, data=[go.Table(
        header=dict(values=list(df_country.columns),
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
