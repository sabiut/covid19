from django.shortcuts import render
import plotly.express as px
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

    # Funnel chart
    fig1 = px.funnel_area(names=df['Country'],
                          values=df['NewCases'],
                          )

    new_cases = pyo.plot(fig1, auto_open=False, output_type='div')
    return render(request, 'home/welcome.html', locals())


def funnel(request):
    import plotly.express as px
    import pandas as pd
    stages = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"]
    df_mtl = pd.DataFrame(dict(number=[39, 27.4, 20.6, 11, 3], stage=stages))
    df_mtl['office'] = 'Montreal'
    df_toronto = pd.DataFrame(dict(number=[52, 36, 18, 14, 5], stage=stages))
    df_toronto['office'] = 'Toronto'
    df = pd.concat([df_mtl, df_toronto], axis=0)
    plot = px.funnel(df, x='number', y='stage', color='office')
    return render(request, 'home/funnel.html', locals())
