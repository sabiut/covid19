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
    monthly_cases = cases_per_month()
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
                             line=dict(color='green', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=month, y=deaths, name='Deaths ',
                             line=dict(color='red', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title='Number of Covid-19 Cases per month',
                      xaxis_title='Month',
                      yaxis_title='Covid-19 Cases')

    month_cases = pyo.plot(fig, auto_open=False, output_type='div')
    return month_cases
