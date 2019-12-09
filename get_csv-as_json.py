import pandas as pd
import requests
import os

class extract_as_csv(object):
    def extract_f1_json(url__f1_tv, url__drivers):
        page = requests.get(url__f1_tv)
        json__f1_tv = page.json()

        # ergast data
        page = requests.get(url__drivers)
        json__drivers = page.json()

        def db_name():
            j_temp = json__f1_tv['path']
            j_temp = j_temp[5:]
            csv_name = ''

            n = 0
            while j_temp[n] != '/':
                csv_name = csv_name + j_temp[n]
                n = 1 + n

            return csv_name

        csv_name = db_name()

        def create_path():
            if not os.path.exists('Database/'+csv_name):
                os.makedirs('Database/'+csv_name)

        create_path()

        def generate_csv_name(csv_type):
            path_db = 'Database/' + csv_name + '/' + csv_name + '-' + csv_type + '.csv'

            return path_db

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

        def weather(json__f1_tv):
            j_temp = json__f1_tv['Weather']
            j_temp = j_temp['graph']
            j_temp = j_temp['data']

            def temperature(j_temp):
                def temp_df(j_temp):
                    Time, Temp = for_loop_by_time(j_temp)

                    Track_Temp = {"Time": Time, "Temperature": Temp}

                    Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                    Track_Temp_Data = Track_Temp_Data.set_index('Time')

                    return Track_Temp_Data

                def track_temp(j_temp):
                    j_temp = j_temp['pTrack']

                    Track_Temp_Data = temp_df(j_temp)

                    path_db = generate_csv_name('Track_Temp')

                    Track_Temp_Data.to_csv(path_db)

                def air_temp(j_temp):
                    j_temp = j_temp['pAir']

                    Track_Temp_Data = temp_df(j_temp)

                    path_db = generate_csv_name('Air_Temp')

                    Track_Temp_Data.to_csv(path_db)

                track_temp(j_temp)
                air_temp(j_temp)

            def is_raining(j_temp):
                j_temp = j_temp['pRaining']

                Time, Raining = for_loop_by_time(j_temp)

                Track_Temp = {"Time": Time, "Raining": Raining}

                Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                Track_Temp_Data = Track_Temp_Data.set_index('Time')

                path_db = generate_csv_name('Raining')

                Track_Temp_Data.to_csv(path_db)

            def wind_speed(j_temp):
                j_temp = j_temp['pWind Speed']

                Time, Wind_Speed = for_loop_by_time(j_temp)

                Track_Temp = {"Time": Time, "Wind Speed": Wind_Speed}

                Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                Track_Temp_Data = Track_Temp_Data.set_index('Time')

                path_db = generate_csv_name('Wind_Speed')

                Track_Temp_Data.to_csv(path_db)

            def humidity(j_temp):
                j_temp = j_temp['pHumidity']

                Time, Humidity = for_loop_by_time(j_temp)

                Track_Temp = {"Time": Time, "Humidity": Humidity}

                Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                Track_Temp_Data = Track_Temp_Data.set_index('Time')

                path_db = generate_csv_name('Humidity')

                Track_Temp_Data.to_csv(path_db)

            def air_pressure(j_temp):
                j_temp = j_temp['pPressure']

                Time, Air_Pressure = for_loop_by_time(j_temp)

                Track_Temp = {"Time": Time, "Air Pressure": Air_Pressure}

                Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                Track_Temp_Data = Track_Temp_Data.set_index('Time')

                path_db = generate_csv_name('Air_Pressure')

                Track_Temp_Data.to_csv(path_db)

            def wind_direction(j_temp):
                j_temp = j_temp['pWind Dir']

                Time, Wind_Direction = for_loop_by_time(j_temp)

                Track_Temp = {"Time": Time, "Wind Direction": Wind_Direction}

                Track_Temp_Data = pd.DataFrame(data=Track_Temp)
                Track_Temp_Data = Track_Temp_Data.set_index('Time')

                path_db = generate_csv_name('Wind_Direction')

                Track_Temp_Data.to_csv(path_db)

            temperature(j_temp)
            is_raining(j_temp)
            wind_speed(j_temp)
            humidity(j_temp)
            air_pressure(j_temp)
            wind_direction(j_temp)

        def current_drivers(json__f1_tv):
            j_temp = json__f1_tv['init']
            j_temp = j_temp['data']
            j_temp = j_temp['Drivers']

            Driver_Name = []
            Driver_Initials = []
            Driver_Team = []
            Driver_Num = []
            Team_Color_Picker = []

            for Driver in j_temp:
                Driver_Name.append(Driver['FirstName'] + ' ' + Driver['Name'])
                Driver_Initials.append(Driver['Initials'])
                Driver_Team.append(Driver['Team'])
                Driver_Num.append(Driver['Num'])
                Team_Color_Picker.append(Driver['Color'])

            Current_Drivers = {"Number": Driver_Num, "Driver Name": Driver_Name, "Driver Initials": Driver_Initials, "Driver Team": Driver_Team, "Color": Team_Color_Picker}

            Current_Drivers_Data = pd.DataFrame(data=Current_Drivers)
            Current_Drivers_Data = Current_Drivers_Data.set_index('Number')

            path_db = generate_csv_name('Drivers')

            Current_Drivers_Data.to_csv(path_db)

            return Driver_Initials

        def count_laps(json__f1_tv):
            j_temp = json__f1_tv['free']
            j_temp = j_temp['data']

            Lap = []

            i = 1
            while i <= j_temp['L']:
                Lap.append(i)
                i = i + 1

            return Lap

        def track_status(json__f1_tv, Laps):
            j_temp = json__f1_tv['Scores']
            j_temp = j_temp['graph']
            j_temp = j_temp['TrackStatus']

            Track_Status = []

            i = 0
            for lap in j_temp:
                if i == 1:
                    if lap == '':
                        lap = None
                    Track_Status.append(lap)
                    i = i - 1
                else:
                    i = i + 1

            Track_Status_Dict = {"Lap": Laps, "Status": Track_Status[1:Laps.__len__()+1]}

            Track_Status_Data = pd.DataFrame(data=Track_Status_Dict)
            Track_Status_Data = Track_Status_Data.set_index('Lap')

            path_db = generate_csv_name('Track_Status')

            Track_Status_Data.to_csv(path_db)

        def drivers_performance_points(json__f1_tv, Driver_Initials, Laps):
            j_temp = json__f1_tv['Scores']
            j_temp = j_temp['graph']
            j_temp = j_temp['Performance']

            Driver_Performance = {}

            Driver_Performance['Lap'] = Laps

            for Driver in Driver_Initials:
                i = 0
                Performance_Gap = []

                for Performance in j_temp['p'+Driver]:
                    if i == 0:
                        i = i + 1
                    else:
                        Performance_Gap.append(Performance)
                        i = i - 1

                while Performance_Gap.__len__() < Laps.__len__():
                    Performance_Gap.append(None)

                Driver_Performance[Driver] = Performance_Gap

            Driver_Performance_Data = pd.DataFrame(data=Driver_Performance)
            Driver_Performance_Data = Driver_Performance_Data.set_index('Lap')

            path_db = generate_csv_name('Drivers_Performance')

            Driver_Performance_Data.to_csv(path_db)

        def drivers_positions_by_lap(json__f1_tv, Driver_Initials, Laps):
            j_temp = json__f1_tv['LapPos']
            j_temp = j_temp['graph']
            Drivers_Gap = j_temp['data']

            Driver_Positions_Dict = {}

            Driver_Positions_Dict['Lap'] = Laps

            for Driver in Driver_Initials:
                i = 0
                Driver_Positions = []

                for lap in Drivers_Gap['p'+Driver]:
                    if i == 1:
                        Driver_Positions.append(lap)
                        i = i - 1
                    else:
                        i = i + 1

                Driver_Positions_Dict[Driver] = Driver_Positions[1:Laps.__len__()+1]
                print(Driver_Positions.__len__())

            Driver_Positions_Data = pd.DataFrame(data=Driver_Positions_Dict)
            Driver_Positions_Data = Driver_Positions_Data.set_index('Lap')

            path_db = generate_csv_name('Drivers_Positions')

            Driver_Positions_Data.to_csv(path_db)

        weather(json__f1_tv)
        Driver_Initials = current_drivers(json__f1_tv)
        Laps = count_laps(json__f1_tv)
        track_status(json__f1_tv, Laps)
        drivers_performance_points(json__f1_tv, Driver_Initials, Laps)
        drivers_positions_by_lap(json__f1_tv, Driver_Initials, Laps)

    extract_f1_json('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json',
                    'http://ergast.com/api/f1/2019/drivers.json')
