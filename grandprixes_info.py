import pandas as pd
import requests
import datetime
from unidecode import unidecode as UnicodeFormatter
import os
import path_configuration


class GrandPrix_Info(object):

    def att_circuits_list():

        def build_url():
            current_year = datetime.datetime.today().year
            url_list = []

            year = 1980
            while year <= current_year:
                url = "https://ergast.com/api/f1/" + str(year) + ".json"
                url_list.append(url)
                year = year + 1

            return url_list

        url_list = build_url()
        Path = path_configuration.Path()

        for url in url_list:
            Season = 0
            Round = []
            GrandPrix = []
            CircuitID = []
            CircuitName = []
            City = []
            Country = []
            Date = []

            page = requests.get(url)
            json = page.json()
            j_temp = json['MRData']
            j_temp = j_temp['RaceTable']
            circuits_list = j_temp['Races']

            for circuit in circuits_list:
                Season = circuit['season']
                Round.append(circuit['round'])
                GrandPrix.append(UnicodeFormatter(circuit['raceName'].replace(' ', '_')))
                CircuitID.append(UnicodeFormatter(circuit['Circuit']['circuitId']))
                CircuitName.append(UnicodeFormatter(circuit['Circuit']['circuitName']))
                City.append(UnicodeFormatter(circuit['Circuit']['Location']['locality']))
                Country.append(UnicodeFormatter(circuit['Circuit']['Location']['country']))
                Date.append(circuit['date'])

            Circuit_Data = {'Round': Round, 'Grand Prix': GrandPrix, 'Circuit ID': CircuitID, 'Circuit Name': CircuitName, 'City': City,
                            'Country': Country, 'Date': Date}
            Circuit_DF = pd.DataFrame(data=Circuit_Data)
            Circuit_DF = Circuit_DF.set_index('Round')

            path = Path.season_path(Season)
            Circuit_DF.to_csv(path)

    att_circuits_list()