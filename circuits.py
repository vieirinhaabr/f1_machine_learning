import pandas as pd
import requests
import datetime
import os


class Circuits_Info(object):

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

        #url_list = build_url()
        url_list = ["https://ergast.com/api/f1/2019.json"]

        for url in url_list:
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
                Round.append(circuit['round'])
                GrandPrix.append(circuit['raceName'].replace(' ', '_'))
                CircuitID.append(circuit['Circuit']['circuitId'])
                CircuitName.append(circuit['Circuit']['circuitName'])
                City.append(circuit['Circuit']['Location']['locality'])
                Country.append(circuit['Circuit']['Location']['country'])
                Date.append(circuit['date'])

            Circuit_Data = {'Round': Round, 'Grand Prix': GrandPrix, 'Circuit ID': CircuitID, 'Circuit Name': CircuitName, 'City': City,
                            'Country': Country, 'Date': Date}
            Circuit_DF = pd.DataFrame(data=Circuit_Data)
            Circuit_DF = Circuit_DF.set_index('Round')
            print(Circuit_DF)



    att_circuits_list()