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

                self.drivers_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.contructors_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.pitstops_times_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.result_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])
                self.by_lap_csv(Round[i], Date_obj[i].year, Date[i], GrandPrix[i])

                if Date_obj[i].year > 2017:
                    # get data from f1
                    print(' ')

            Progress.get_progress_bar()
            i = i + 1

    def drivers_csv(self, round, year, date, gp_name):
        url = self.Url.url_driver(round, year)

        page = self.Requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['DriverTable']
        Drivers = json['Drivers']

        DriversID = []
        DriversInitials = []
        DriversName = []
        YearsOld = []

        for driver in Drivers:
            DriversID.append(driver['driverId'])
            DriversInitials.append(driver['code'])
            DriversName.append(UnicodeFormatter(driver['givenName']+' '+driver['familyName']))
            YearsOld.append(
                datetime.datetime.now().year - datetime.datetime.strptime(driver['dateOfBirth'], '%Y-%m-%d').year
            )

        Drivers_Dict = {'Driver ID': DriversID, 'Driver Initials': DriversInitials,
                        'Driver Name': DriversName, 'Years Old': YearsOld}
        Drivers_Data = pd.DataFrame(data=Drivers_Dict)

        Path = self.Path.grandprix_path(year, date, gp_name, 'Drivers')
        Drivers_Data.to_csv(Path)

    def contructors_csv(self, round, year, date, gp_name):
        url = self.Url.url_constructor(round, year)

        page = self.Requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['ConstructorTable']
        Constructors = json['Constructors']

        ConstructorID = []
        ConstructorName = []

        for constructor in Constructors:
            ConstructorID.append(constructor['constructorId'])
            ConstructorName.append(constructor['name'])

        Constructors_Dict = {"Constructor ID": ConstructorID, "Constructor Name": ConstructorName}
        Constructor_Data = pd.DataFrame(data=Constructors_Dict)

        Path = self.Path.grandprix_path(year, date, gp_name, 'Constructors')
        Constructor_Data.to_csv(Path)

    def pitstops_times_csv(self, round, year, date, gp_name):
        url = self.Url.url_pitstops_time(round, year)

        page = self.Requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['RaceTable']
        Race = json['Races'][0]

        PitStops = Race['PitStops']

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

        Path = self.Path.gp_multiplerace_path(year, date, gp_name, 'PitStop', i)
        PitStop_Data.to_csv(Path)

    def result_csv(self, round, year, date, gp_name):
        url = self.Url.url_results(round, year)

        page = self.Requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['RaceTable']
        Race = json['Races'][0]
        Results = Race['Results']

        DriverPosition = []
        DriverGridPosition = []
        DriverID = []
        ConstructorID = []
        TimeToLeader = []
        RaceStatus = []
        FastestLapRank = []
        AverageSpeed = []

        for result in Results:

            # DRIVER POSITION
            if result['positionText'] == 'R':
                DriverPosition.append(None)
            else:
                DriverPosition.append(result['positionText'])

            # GRID
            DriverGridPosition.append(result['grid'])
            # DRIVER ID
            DriverID.append(result['Driver']['driverId'])
            # CONSTRUCTOR ID
            ConstructorID.append(result['Constructor']['constructorId'])

            # TIME TO LEADER
            if result['position'] == '1':
                TimeToLeader.append("0")
            elif result['status'] != 'Finished':
                Check = result['status']
                if Check[0] == '+':
                    TimeToLeader.append(result['status'])
                else:
                    TimeToLeader.append(None)
            else:
                TimeToLeader.append(result['Time']['time'])

            # RACE STATUS
            if result['status'][0] == '+':
                RaceStatus.append('Finished')
            else:
                RaceStatus.append(result['status'])

            # CASE THE DRIVER GET OUT OF RACE WITHOUT DO ONE LAP
            if 'FastestLap' not in result:
                # RANK FASTEST LAP
                FastestLapRank.append(None)
                # AVERAGE SPEED
                AverageSpeed.append(None)
            else:
                # RANK FASTEST LAP
                FastestLapRank.append(result['FastestLap']['rank'])
                # AVERAGE SPEED
                AverageSpeed.append(result['FastestLap']['AverageSpeed']['speed'])

        Result_Dict = {'Result Positions': DriverPosition, 'Initials Positions': DriverGridPosition,
                       'DriverID': DriverID, 'ConstructorID': ConstructorID, 'Result Time to Leader': TimeToLeader,
                       'Result Status': RaceStatus, 'Result Fastest Rank': FastestLapRank,
                       'Result Average Speed': AverageSpeed}
        Result_Data = pd.DataFrame(data=Result_Dict)
        Result_Data = Result_Data.set_index('Result Positions')

        Path = self.Path.grandprix_path(year, date, gp_name, 'Result')
        Result_Data.to_csv(Path)

    def by_lap_csv(self, round, year, date, gp_name):
        # Progress Calculator
        Progress = progress_calculator.ProgressBar(True)

        # URL
        url_1, url_2 = self.Url.url_lapbylap(round, year)

        # LAP COUNTER
        Lap_Counter = 1

        # LAP VALIDATOR
        Lap_v = True

        # DRIVER LIST
        driver_list = list(pd.read_csv(self.Path.grandprix_path(year, date, gp_name, 'Drivers'))['Driver ID'].values)

        # DRIVERS DICT
        Lap_Times_Dict = {}
        Lap_Positions_Dict = {}

        # START VALUES
        Lap_Times_Dict['Driver ID'] = driver_list
        Lap_Positions_Dict['Driver ID'] = driver_list

        while Lap_v:
            # PROGRESS
            Progress.get_progress_counter(Lap_Counter)

            # DRIVERS LIST
            Lap_Times = []
            Lap_Positions = []

            page = self.Requests.get(url_1 + str(Lap_Counter) + url_2)
            json = page.json()
            json = json['MRData']

            if int(json['total']) == 0:
                Lap_v = False
            else:
                jtemp = json['RaceTable']
                jtemp = jtemp['Races'][0]
                jtemp = jtemp['Laps'][0]
                Laps = jtemp['Timings']

                for driver in driver_list:
                    Driver_Out_Checker = True
                    for lap in Laps:
                        if driver == lap['driverId']:
                            Driver_Out_Checker = False
                            Lap_Times.append(lap['time'])
                            Lap_Positions.append(lap['position'])

                    if Driver_Out_Checker:
                        Lap_Times.append(None)
                        Lap_Positions.append(None)

                Lap_Times_Dict[Lap_Counter] = Lap_Times
                Lap_Positions_Dict[Lap_Counter] = Lap_Positions

                Lap_Counter = Lap_Counter + 1

        Lap_Times_Data = pd.DataFrame(data=Lap_Times_Dict)
        Lap_Times_Data = Lap_Times_Data.set_index('Driver ID')
        Path = self.Path.grandprix_path(year, date, gp_name, 'TimesByLap')
        Lap_Times_Data.to_csv(Path)

        Lap_Positions_Data = pd.DataFrame(data=Lap_Positions_Dict)
        Lap_Positions_Data = Lap_Positions_Data.set_index('Driver ID')
        Path = self.Path.grandprix_path(year, date, gp_name, 'PositionsByLap')
        Lap_Positions_Data.to_csv(Path)
