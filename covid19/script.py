import csv
import string

from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import datetime
import country_converter as coco

http = urllib3.PoolManager()


def get_data():
    url = 'https://www.worldometers.info/coronavirus/'

    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features='lxml')
    get_table = soup.find('table', {'id': "main_table_countries_today"})
    headers = [header.text for header in get_table.find_all('th')]
    rows = []
    for row in get_table.find_all('tr'):
        rows.append([val.text.replace('\n', '').strip() for val in row.find_all('td')])
        with open('corona.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            writer.writerows(row for row in rows if row)


def rename_column():
    df = pd.read_csv("corona.csv")
    df.rename(columns={'Country,Other': 'Country',
                       'Serious,Critical': 'Critical'}, inplace=True)

    df.to_csv("corona.csv", encoding='utf-8', index=False)


def add_column():
    df = pd.read_csv("corona.csv")
    df['date'] = ""
    df.to_csv("corona.cvs", index=False)

    df = pd.read_csv("corona.csv")
    df['date'] = datetime.datetime.today().strftime('%d-%b-%Y')
    df.to_csv('corona.csv', index=False)


def delete_column():
    f = pd.read_csv("corona.csv")
    keep_col = ['Country', 'TotalCases', 'NewCases', 'TotalDeaths',
                'NewDeaths', 'TotalRecovered', 'ActiveCases', 'Critical',
                'TotalTests', 'Continent', 'date']
    new_f = f[keep_col]
    new_f.to_csv("corona.csv", index=False)


def start():
    get_data()
    rename_column()
    add_column()
    delete_column()


start()
