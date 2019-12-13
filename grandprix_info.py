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


class GrandPrix(object):
    Url = None
    Path = None
    Requests = None

    def __init__(self):
        self.Url = url_configuration.Url_builder()
        self.Path = path_configuration.Path()
        self.Requests = requests

    def import_grand_prix(self):
        content = os.listdir(self.Path.get_season_path())
        content.sort()

        """for year in content:
            DataFrame = pd.read_csv(Path.get_season_path()+year)

            print(DataFrame)"""

        DataFrame = pd.read_csv(self.Path.get_season_path()+'2019.csv')

        Date = list(DataFrame['Date'])
        GrandPrix = list(DataFrame['Grand Prix'])
        Round = list(DataFrame['Round'])
        Date_obj = []

        # DATE OBJ
        for date in Date:
            Date_obj.append(datetime.datetime.strptime(date, '%Y-%m-%d'))

        Progress = progress_calculator.ProgressBar(Round)

        # WHILE - BY GPS OF THE YEAR
        i = 0
        while i < Round.__len__():

            # CHECK YEAR
            if Date_obj[i] < datetime.datetime.now():

                if Date_obj[i].year > 2017:
                    # get data from f1
                    print(' ')
                # METHOD CALLS

                # self.drivers_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.pitstops_times_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])

            Progress.get_progress_bar()
            i = i + 1

    def drivers_csv(self, round, year, date, gp_name):
        url = self.Url.url_driver(round, year)

        url = self.Requests.get(url)
        json = url.json()
        json = json['MRData']
        json = json['DriverTable']
        json = json['Drivers']

        DriversID = []
        DriversNumber = []
        DriversInitials = []
        DriversName = []
        Birth = []
        DriversNationality = []

        for driver in json:
            DriversID.append(driver['driverId'])
            DriversNumber.append(driver['permanentNumber'])
            DriversInitials.append(driver['code'])
            DriversName.append(UnicodeFormatter(driver['givenName']+' '+driver['familyName']))
            Birth.append(driver['dateOfBirth'])
            DriversNationality.append(UnicodeFormatter(driver['nationality']))

        Drivers = {'Driver Number': DriversNumber, 'ID': DriversID, 'Driver Initials': DriversInitials,
                   'Driver Name': DriversName, 'Birth Date': Birth, 'Nationality': DriversNationality}
        Drivers_Data = pd.DataFrame(data=Drivers)

        Path = self.Path.grandprix_path(date, gp_name, 'Drivers')
        Drivers_Data.to_csv(Path)

    def pitstops_times_csv(self, round, year, date, gp_name):
        url = self.Url.url_pitstops_time(round, year)

        url = self.Requests.get(url)
        json = url.json()
        json = json['MRData']
        json = json['RaceTable']
        # IF HAVE MORE THAN ONE RACE
        Races = json['Races']

        i = 1
        for race in Races:
            PitStops = race['PitStops']

            DriverID = []
            Corresponding_Lap = []
            Driver_Stop_Number = []
            PitStop_Time = []

            for pitstop in PitStops:
                DriverID.append(pitstop['driverId'])
                Corresponding_Lap.append(pitstop['lap'])
                Driver_Stop_Number.append(pitstop['stop'])
                PitStop_Time.append(pitstop['duration'])

            PitStop_Dict = {'ID': DriverID, 'Pit Stop Lap': Corresponding_Lap, 'Pit Stop Number': Driver_Stop_Number,
                            'Pit Stop Time': PitStop_Time}
            PitStop_Data = pd.DataFrame(data=PitStop_Dict)

            Path = self.Path.pitstop_path(date, gp_name, 'PitStop', i)
            PitStop_Data.to_csv(Path)

            i = i + 1
