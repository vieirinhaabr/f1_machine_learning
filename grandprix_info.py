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
                print(bcolors.PASS + 'STARTING EXTRACTOR, GETTING FROM', GrandPrix[i], 'DATE:', Date[i] + bcolors.END)
                self.drivers_csv(Round[i], Date_obj[i].year, GrandPrix[i])
                self.contructors_csv(Round[i], Date_obj[i].year, GrandPrix[i])
                self.pitstops_times_csv(Round[i], Date_obj[i].year, GrandPrix[i])
                self.result_csv(Round[i], Date_obj[i].year, GrandPrix[i])
                self.by_lap_csv(Round[i], Date_obj[i].year, GrandPrix[i])
                self.current_driver_standings(Round[i], Date_obj[i].year, GrandPrix[i])
                self.status(Round[i], Date_obj[i].year, GrandPrix[i])

                if Date_obj[i].year > 2017:
                    url = self.Url.f1_url(Date_obj[i].year, Date_obj[i].date(), GrandPrix[i])
                    self.load_data_from_f1(url, Date_obj[i].year, GrandPrix[i])

            Progress.get_progress_bar()
            i = i + 1

    def drivers_csv(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING DRIVERS BY RACE...', gp_name + bcolors.END)

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

        Path = self.Path.grandprix_path(year, gp_name, 'Drivers')
        Drivers_Data.to_csv(Path)

    def contructors_csv(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING CONSTRUCTORS BY RACE...', gp_name + bcolors.END)

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

        Path = self.Path.grandprix_path(year, gp_name, 'Constructors')
        Constructor_Data.to_csv(Path)

    def pitstops_times_csv(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING PITSTOPS BY RACE...', gp_name + bcolors.END)

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

        Path = self.Path.grandprix_path(year, gp_name, 'PitStop')
        PitStop_Data.to_csv(Path)

    def result_csv(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING RESULT BY RACE...', gp_name + bcolors.END)

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

        Initial_Ps_Dict = {'Positions': DriverGridPosition, 'DriverID': DriverID}
        Initial_Ps_Data = pd.DataFrame(data=Initial_Ps_Dict)
        Initial_Ps_Data = Initial_Ps_Data.set_index('Positions')

        Path = self.Path.grandprix_path(year, gp_name, 'InitialPositions')
        Initial_Ps_Data.to_csv(Path)

        Result_Dict = {'Positions': DriverPosition, 'DriverID': DriverID, 'ConstructorID': ConstructorID,
                       'Time to Leader': TimeToLeader, 'Status': RaceStatus,
                       'Fastest Rank': FastestLapRank, 'Average Speed': AverageSpeed}
        Result_Data = pd.DataFrame(data=Result_Dict)
        Result_Data = Result_Data.set_index('Positions')

        Path = self.Path.grandprix_path(year, gp_name, 'Result')
        Result_Data.to_csv(Path)

    def by_lap_csv(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING LAP TIMES AND POSITIONS BY RACE...', gp_name + bcolors.END)
        # Progress Calculator
        Progress = progress_calculator.ProgressBar(True)

        # URL
        url_1, url_2 = self.Url.url_lapbylap(round, year)

        # LAP COUNTER
        Lap_Counter = 1

        # LAP VALIDATOR
        Lap_v = True

        # DRIVER LIST
        driver_list = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, 'Drivers'))['Driver ID'].values)

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
        Path = self.Path.grandprix_path(year, gp_name, 'TimesByLap')
        Lap_Times_Data.to_csv(Path)

        Lap_Positions_Data = pd.DataFrame(data=Lap_Positions_Dict)
        Lap_Positions_Data = Lap_Positions_Data.set_index('Driver ID')
        Path = self.Path.grandprix_path(year, gp_name, 'PositionsByLap')
        Lap_Positions_Data.to_csv(Path)

    def current_driver_standings(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING DRIVER STANDINGS FROM ERGAST...', gp_name + bcolors.END)

        url = self.Url.url_driver_standings(round, year)

        # LOAD JSON
        page = requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['StandingsTable']
        json = json['StandingsLists'][0]
        DriverStandings = json['DriverStandings']

        # STARTING LISTS
        DriverPosition = []
        DriverPoints = []
        DriverWins = []
        DriverID = []
        ConstructorID = []

        for driver in DriverStandings:
            DriverPosition.append(driver['position'])
            DriverPoints.append(driver['points'])
            DriverWins.append(driver['wins'])
            DriverID.append(driver['Driver']['driverId'])
            ConstructorID.append(driver['Constructors'][-1]['constructorId'])

        DriverStandingsDict = {'Position': DriverPosition, 'DriverID': DriverID, 'ConstructorID': ConstructorID,
                               'Wins': DriverWins, 'Points': DriverPoints}

        DriverStandingsData = pd.DataFrame(data=DriverStandingsDict)
        DriverStandingsData = DriverStandingsData.set_index('Position')

        Path = self.Path.standings_path(year)
        DriverStandingsData.to_csv(Path)

    def status(self, round, year, gp_name):
        print(bcolors.ITALIC + 'GETTING STATUS FROM ERGAST...', gp_name + bcolors.END)

        url = self.Url.url_status(round, year)

        # LOAD JSON
        page = requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['StatusTable']
        Status = json['Status']

        # STARTING LISTS
        StatusID = []
        StatusDescription = []
        StatusOccurrences = []

        for state in Status:
            StatusID.append(state['statusId'])
            StatusDescription.append(state['status'])
            StatusOccurrences.append(state['count'])

        StatusDict = {'StatusID': StatusID, 'Status Description': StatusDescription,
                      'Status Occurrences': StatusOccurrences}

        StatusData = pd.DataFrame(data=StatusDict)
        StatusData = StatusData.set_index('StatusID')

        Path = self.Path.grandprix_path(year, gp_name, 'RaceStatus')
        StatusData.to_csv(Path)

    def load_data_from_f1(self, url, year, gp_name):
        print(bcolors.ITALIC + 'GETTING SOME DATA FROM F1...', gp_name + bcolors.END)

        page = requests.get(url)
        json = page.json()

        def for_loop_by_time(json):
            Time = []
            Something = []

            i = 0
            for value in json:
                if i == 0:
                    Time.append(value)
                    i = 1
                else:
                    Something.append(value)
                    i = 0

            return Time, Something

        def weather(json):
            json = json['Weather']
            json = json['graph']
            weather_data = json['data']

            def temperature(json):
                def temp_df(json, description):
                    Time, Temp = for_loop_by_time(json)

                    TrackTempDict = {"Time": Time, description: Temp}

                    TrackTempData = pd.DataFrame(data=TrackTempDict)
                    TrackTempData = TrackTempData.set_index('Time')

                    return TrackTempData

                def track_temp(json):
                    print(bcolors.ITALIC + 'GETTING TRACK TEMP FROM F1...', gp_name + bcolors.END)

                    json = json['pTrack']
                    TrackTempData = temp_df(json, "Track Temperature")

                    Path = self.Path.grandprix_path(year, gp_name, 'TrackTemp')
                    TrackTempData.to_csv(Path)

                def air_temp(json):
                    print(bcolors.ITALIC + 'GETTING AIR TEMP FROM F1...', gp_name + bcolors.END)

                    json = json['pAir']
                    TrackTempData = temp_df(json, "Air Temperature")

                    Path = self.Path.grandprix_path(year, gp_name, 'AirTemp')
                    TrackTempData.to_csv(Path)

                track_temp(json)
                air_temp(json)

            def is_raining(json):
                print(bcolors.ITALIC + 'GETTING WEATHER FROM F1...', gp_name + bcolors.END)

                json = json['pRaining']
                Time, Raining = for_loop_by_time(json)

                TrackTemp = {"Time": Time, "Is Raining": Raining}

                TrackTempData = pd.DataFrame(data=TrackTemp)
                TrackTempData = TrackTempData.set_index('Time')

                Path = self.Path.grandprix_path(year, gp_name, 'Raining')
                TrackTempData.to_csv(Path)

            def wind_speed(json):
                print(bcolors.ITALIC + 'GETTING WIND SPEED FROM F1...', gp_name + bcolors.END)

                json = json['pWind Speed']

                Time, Wind_Speed = for_loop_by_time(json)

                TrackTemp = {"Time": Time, "Wind Speed": Wind_Speed}

                TrackTempData = pd.DataFrame(data=TrackTemp)
                TrackTempData = TrackTempData.set_index('Time')

                Path = self.Path.grandprix_path(year, gp_name, 'Wind_Speed')
                TrackTempData.to_csv(Path)

            def wind_direction(json):
                print(bcolors.ITALIC + 'GETTING WIND DIRECTION FROM F1...', gp_name + bcolors.END)

                json = json['pWind Dir']

                Time, Wind_Direction = for_loop_by_time(json)

                TrackTemp = {"Time": Time, "Wind Direction": Wind_Direction}

                TrackTempData = pd.DataFrame(data=TrackTemp)
                TrackTempData = TrackTempData.set_index('Time')

                Path = self.Path.grandprix_path(year, gp_name, 'Wind_Direction')
                TrackTempData.to_csv(Path)

            def humidity(json):
                print(bcolors.ITALIC + 'GETTING HUMIDITY FROM F1...', gp_name + bcolors.END)

                json = json['pHumidity']

                Time, Humidity = for_loop_by_time(json)

                TrackTemp = {"Time": Time, "Humidity": Humidity}

                TrackTempData = pd.DataFrame(data=TrackTemp)
                TrackTempData = TrackTempData.set_index('Time')

                Path = self.Path.grandprix_path(year, gp_name, 'Humidity')
                TrackTempData.to_csv(Path)

            def air_pressure(json):
                print(bcolors.ITALIC + 'GETTING AIR PRESSURE FROM F1...', gp_name + bcolors.END)

                json = json['pPressure']

                Time, Air_Pressure = for_loop_by_time(json)

                TrackTemp = {"Time": Time, "Air Pressure": Air_Pressure}

                TrackTempData = pd.DataFrame(data=TrackTemp)
                TrackTempData = TrackTempData.set_index('Time')

                Path = self.Path.grandprix_path(year, gp_name, 'Air_Pressure')
                TrackTempData.to_csv(Path)

            temperature(weather_data)
            is_raining(weather_data)
            wind_speed(weather_data)
            wind_direction(weather_data)
            humidity(weather_data)
            air_pressure(weather_data)

        def track_status(json):
            print(bcolors.ITALIC + 'GETTING TRACK STATUS FROM F1...', gp_name + bcolors.END)

            json = json['Scores']
            json = json['graph']
            TrackStatusJson = json['TrackStatus']

            TrackStatus = []
            Laps = []

            i = 0
            for lap in TrackStatusJson:
                if i == 1:
                    if lap == '':
                        TrackStatus.append(None)
                    elif lap == 'Y':
                        TrackStatus.append('YellowFlag')
                    elif lap == 'S':
                        TrackStatus.append('SafetyCar')
                    elif lap == 'R':
                        TrackStatus.append('RedFlag')
                    else:
                        TrackStatus.append(lap)
                    i = i - 1
                else:
                    Laps.append(lap)
                    i = i + 1

            TrackStatusDict = {"Lap": Laps, "Status": TrackStatus}

            TrackStatusData = pd.DataFrame(data=TrackStatusDict)
            TrackStatusData = TrackStatusData.set_index('Lap')

            Path = self.Path.grandprix_path(year, gp_name, 'Track_Status')
            TrackStatusData.to_csv(Path)

        def drivers_performance_points(json):
            print(bcolors.ITALIC + 'GETTING DRIVER PERFORMANCE POINTS FROM F1...', gp_name + bcolors.END)

            json = json['Scores']
            json = json['graph']
            PF_Points = json['Performance']

            DriversID = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, "Drivers"))['Driver ID'])
            DriversInitials = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, "Drivers"))['Driver Initials'])
            Laps = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, "Track_Status"))['Lap'][1:])

            DriverPerformancePointsDict = {}
            DriverPerformancePointsDict['Lap'] = Laps

            counter = 0
            for Driver in DriversInitials:
                i = 0
                Performance_Gap = []

                for Performance in PF_Points['p'+Driver]:
                    if i == 0:
                        i = i + 1
                    else:
                        Performance_Gap.append(Performance)
                        i = i - 1

                while Performance_Gap.__len__() < Laps.__len__():
                    Performance_Gap.append(None)

                DriverPerformancePointsDict[DriversID[counter]] = Performance_Gap
                counter = counter + 1

            DriverPerformanceData = pd.DataFrame(data=DriverPerformancePointsDict)
            DriverPerformanceData = DriverPerformanceData.set_index('Lap')

            Path = self.Path.grandprix_path(year, gp_name, 'Drivers_Performance')
            DriverPerformanceData.to_csv(Path)

        def order_driver_list(json):
            json = json['init']
            json = json['data']
            Drivers_json = json['Drivers']

            Drivers_InOrder = []
            Drivers_Dict = {}
            Drivers_Ordered = []

            for Driver in Drivers_json:
                Drivers_InOrder.append(Driver['Initials'])

            DriversID = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, "Drivers"))['Driver ID'])
            DriversInitials = list(pd.read_csv(self.Path.grandprix_path(year, gp_name, "Drivers"))['Driver Initials'])

            i = 0
            for Driver in DriversInitials:
                Drivers_Dict[Driver] = DriversID[i]
                i = i + 1

            for Driver in Drivers_InOrder:
                Drivers_Ordered.append(Drivers_Dict[Driver])

            return Drivers_Ordered

        def highest_speed(json):
            print(bcolors.ITALIC + 'GETTING HIGHEST SPEED FROM F1...', gp_name + bcolors.END)

            temp = json['best']
            temp = temp['data']
            temp = temp['DR']

            Highest_Speed_Sector_1 = []
            Highest_Speed_Sector_2 = []
            Highest_Speed_Sector_3 = []

            for item in temp:
                i = 0
                for content in item['B']:
                    if i == 13:
                        Highest_Speed_Sector_1.append(content)
                    elif i == 16:
                        Highest_Speed_Sector_2.append(content)
                    elif i == 19:
                        Highest_Speed_Sector_3.append(content)
                    i = i + 1

            SpeedDict = {'Driver': order_driver_list(json), 'Speed S1': Highest_Speed_Sector_1,
                         'Speed S2': Highest_Speed_Sector_2, 'Speed S3': Highest_Speed_Sector_3}

            SpeedData = pd.DataFrame(data=SpeedDict)
            SpeedData = SpeedData.set_index('Driver')

            Path = self.Path.grandprix_path(year, gp_name, 'Highest_Speed')
            SpeedData.to_csv(Path)

        def tyre_types(json):
            print(bcolors.ITALIC + 'GETTING TYRES HISTORY FROM F1...', gp_name + bcolors.END)

            DriverList = order_driver_list(json)
            TyresHistory = []
            Tyres_Dict = {}

            temp = json['xtra']
            temp = temp['data']
            Tyres_json = temp['DR']

            temp_lenght = 0
            for TyreLine in Tyres_json:
                TyresHistory.append(TyreLine['X'][9])
                if len(TyreLine['X'][9]) > temp_lenght:
                    temp_lenght = len(TyreLine['X'][9])

            i = 0
            for Tyres in TyresHistory:
                Driver_Tyres = []

                for Tyre in Tyres:
                    Driver_Tyres.append(Tyre)

                while len(Driver_Tyres) < temp_lenght:
                    Driver_Tyres.append(None)

                Tyres_Dict[DriverList[i]] = Driver_Tyres
                i = i + 1

            Tyre_Data = pd.DataFrame(data=Tyres_Dict)

            Path = self.Path.grandprix_path(year, gp_name, 'Tyres_History')
            Tyre_Data.to_csv(Path)

        weather(json)
        track_status(json)
        drivers_performance_points(json)
        highest_speed(json)
        tyre_types(json)

    # fr changes
    def regulations_pd_generator(self):
        print(bcolors.ITALIC + 'GETTING REGULATIONS OF F1...', + bcolors.END)
        # Can Be True or False

        Aerodynamic = []
        Engine = []
        Tyres = []
        Eletronic = []
        PitStop = []
        Races = []
        Weight = []
        GearBox = []
        Suspension = []
        Years = []

        i = 1970
        while i <= 2020:
            if i == 1976 or i == 1978 or i == 1981 or i == 1982 or i == 1983 or i == 1985 or i == 1990 or i == 1991 or \
                    i == 1993 or i == 1994 or i == 1996 or i == 1998 or i == 1999 or i == 2001 or i == 2004 or i == 2005\
                    or i == 2009 or i == 2011 or i == 2012 or i == 2015 or i == 2017 or i == 2018 or i == 2019:
                Aerodynamic.append(True)
            else:
                Aerodynamic.append(False)
            if i == 1981 or i == 1982 or i == 1986 or i == 1987 or i == 1988 or i == 1989 or i == 1994 or i == 1995 or \
                    i == 2000 or i == 2006 or i == 2007 or i == 2014:
                Engine.append(True)
            else:
                Engine.append(False)
            if i == 1993 or i == 1999 or i == 2004 or i == 2005 or i == 2006 or i == 2007 or i == 2009 or i == 2010:
                Tyres.append(True)
            else:
                Tyres.append(False)
            if i == 1994 or i == 2001 or i == 2003 or i == 2004 or i == 2007 or i == 2008 or i == 2009 or i == 2011 \
                    or i == 2012 or i == 2014 or i == 2019:
                Eletronic.append(True)
            else:
                Eletronic.append(False)
            if i == 1981 or i == 1984 or i == 1992 or i == 1994 or i == 1998 or i == 2004 or i == 2009 or i == 2010 \
                    or i == 2012:
                PitStop.append(True)
            else:
                PitStop.append(False)
            if i == 1970 or i == 1971 or i == 1974 or i == 1977 or i == 1978 or i == 1981 or i == 1984 or i == 1986 or \
                    i == 1987 or i == 1989 or i == 1990 or i == 1990 or i == 1993 or i == 1994 or i == 1996 or \
                    i == 1997 or i == 1999 or i == 2002 or i == 2003 or i == 2005 or i == 2006 or i == 2010 or \
                    i == 2011 or i == 2016:
                Races.append(True)
            else:
                Races.append(False)
            if i == 1970 or i == 1972 or i == 1973 or i == 1980 or i == 1981 or i == 1982 or i == 1983 or i == 1984 or \
                    i == 1987 or i == 1988 or i == 2004 or i == 2013 or i == 2017 or i == 2019:
                Weight.append(True)
            else:
                Weight.append(False)
            if i == 1981 or i == 1983 or i == 1993 or i == 2001 or i == 2004:
                GearBox.append(True)
            else:
                GearBox.append(False)
            if i == 1973 or i == 1982:
                Suspension.append(True)
            else:
                Suspension.append(False)

            Years.append(i)

            i = i + 1

        Regulations_Dict = {'Years': Years, 'Aerodynamic': Aerodynamic, 'Engine': Engine, 'Tyres': Tyres,
                            'Eletronic': Eletronic, 'PitStop': PitStop, 'Races': Races, 'Weight': Weight,
                            'GearBox': GearBox, 'Suspension': Suspension}

        Regulations_Data = pd.DataFrame(data=Regulations_Dict)
        Regulations_Data = Regulations_Data.set_index('Years')

        Path = self.Path.config_path('Regultations')
        Regulations_Data.to_csv(Path)
