# Package imports
import pandas as pd
import requests
import datetime
from unidecode import unidecode as UnicodeFormatter
import os

# Local imports
import path_configuration
import url_configuration
import progress_calculator


class Season_Info(object):
    def import_seasons(self, year_to_find=None):
        Url = url_configuration.Url_builder()
        Path = path_configuration.Path()

        try:
            url_list = Url.url_season(year_to_find)
        except:
            print('ERROR WHEN GETTING URL')

        Progress = progress_calculator.ProgressBar(url_list)

        try:
            for url in url_list:
                Progress.get_progress_bar()
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

                Circuit_Data = {'Round': Round, 'Grand Prix': GrandPrix, 'Circuit ID': CircuitID,
                                'Circuit Name': CircuitName, 'City': City,
                                'Country': Country, 'Date': Date}
                Circuit_DF = pd.DataFrame(data=Circuit_Data)
                Circuit_DF = Circuit_DF.set_index('Round')

                path = Path.season_path(Season)
                Circuit_DF.to_csv(path)

        except:
            print('ERROR WHEN GENERATE/CONVERT DATAFRAMES')
