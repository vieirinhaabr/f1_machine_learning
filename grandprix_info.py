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
                # METHOD CALLS

                # self.drivers_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.contructors_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                # self.pitstops_times_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                # self.result_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])

                if Date_obj[i].year > 2017:
                    # get data from f1
                    print(' ')

            Progress.get_progress_bar()
            i = i + 1

    def drivers_csv(self, round, year, date, gp_name):
        url = self.Url.url_driver(round, year)

        url = self.Requests.get(url)
        json = url.json()
        json = json['MRData']
        json = json['DriverTable']
        Drivers = json['Drivers']

        DriversID = []
        DriversNumber = []
        DriversInitials = []
        DriversName = []
        Birth = []
        DriversNationality = []

        for driver in Drivers:
            DriversID.append(driver['driverId'])
            DriversNumber.append(driver['permanentNumber'])
            DriversInitials.append(driver['code'])
            DriversName.append(UnicodeFormatter(driver['givenName']+' '+driver['familyName']))
            Birth.append(driver['dateOfBirth'])
            DriversNationality.append(UnicodeFormatter(driver['nationality']))

        Drivers_Dict = {'Driver Number': DriversNumber, 'Driver ID': DriversID, 'Driver Initials': DriversInitials,
                        'Driver Name': DriversName, 'Birth Date': Birth, 'Driver Nationality': DriversNationality}
        Drivers_Data = pd.DataFrame(data=Drivers_Dict)

        Path = self.Path.grandprix_path(date, gp_name, 'Drivers')
        Drivers_Data.to_csv(Path)

    def contructors_csv(self, round, year, date, gp_name):
        url = self.Url.url_constructor(round, year)

        url = self.Requests.get(url)
        json = url.json()
        json = json['MRData']
        json = json['ConstructorTable']
        Constructors = json['Constructors']

        ConstructorID = []
        ConstructorName = []
        ConstructorNationality = []

        for constructor in Constructors:
            ConstructorID.append(constructor['constructorId'])
            ConstructorName.append(constructor['name'])
            ConstructorNationality.append(constructor['nationality'])

        Constructors_Dict = {"Constructor ID": ConstructorID, "Constructor Name": ConstructorName,
                             "Constructor Nationality": ConstructorNationality}
        Constructor_Data = pd.DataFrame(data=Constructors_Dict)

        Path = self.Path.grandprix_path(date, gp_name, 'Constructors')
        Constructor_Data.to_csv(Path)

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

            PitStop_Dict = {'Pit Stop Lap': Corresponding_Lap, 'Driver ID': DriverID, 'Pit Stop Number': Driver_Stop_Number,
                            'Pit Stop Time': PitStop_Time}
            PitStop_Data = pd.DataFrame(data=PitStop_Dict)

            Path = self.Path.gp_multiplerace_path(date, gp_name, 'PitStop', i)
            PitStop_Data.to_csv(Path)

            i = i + 1

    def result_csv(self, round, year, date, gp_name):
        url = self.Url.url_results(round, year)

        url = self.Requests.get(url)
        json = url.json()
        json = json['MRData']
        json = json['RaceTable']
        Races = json['Races']

        i = 1
        for race in Races:
            Result = race['PitStops']

            DriverID = []
            Position = []
            Driver_Stop_Number = []
            PitStop_Time = []

            for pitstop in Result:
                DriverID.append(pitstop['driverId'])
                Position.append(pitstop['lap'])
                Driver_Stop_Number.append(pitstop['stop'])
                PitStop_Time.append(pitstop['duration'])

            PitStop_Dict = {'Pit Stop Lap': Position, 'Driver ID': DriverID,
                            'Pit Stop Number': Driver_Stop_Number,
                            'Pit Stop Time': PitStop_Time}
            PitStop_Data = pd.DataFrame(data=PitStop_Dict)

            Path = self.Path.pitstop_path(date, gp_name, 'PitStop', i)
            PitStop_Data.to_csv(Path)

            i = i + 1
