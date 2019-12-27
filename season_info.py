# Package imports
import pandas as pd
import requests
import datetime
from unidecode import unidecode as UnicodeFormatter
import os
import bcolors

# Local imports
import path_configuration
import url_configuration
import progress_calculator


class Season_Info(object):
    Url = None
    Path = None
    Requests = None

    def __init__(self):
        self.Url = url_configuration.Url_builder()
        self.Path = path_configuration.Path()
        self.Requests = requests

    def import_seasons(self, year_to_find=None):
        print(bcolors.PASS + 'STARTING EXTRACTOR, GETTING SEASONS...' + bcolors.END)

        url_list = self.Url.url_season(year_to_find)
        Progress = progress_calculator.ProgressBar(url_list)

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
            Latitude = []
            Longitude = []

            page = self.Requests.get(url)
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
                Latitude.append(circuit['Circuit']['Location']['lat'])
                Longitude.append(circuit['Circuit']['Location']['long'])
                Date.append(circuit['date'])

            # CONSOLE PT
            print(bcolors.WAITMSG + ' Getting Season Data:' + Season + bcolors.END)

            Circuit_Data = {'Round': Round, 'Grand Prix': GrandPrix, 'Circuit ID': CircuitID,
                            'Circuit Name': CircuitName, 'City': City, 'Country': Country, 'Latitude': Latitude,
                            'Longitude': Longitude, 'Date': Date}
            Circuit_DF = pd.DataFrame(data=Circuit_Data)
            Circuit_DF = Circuit_DF.set_index('Round')

            path = self.Path.season_path(Season)
            Circuit_DF.to_csv(path)
