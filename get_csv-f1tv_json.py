import pandas as pd
import requests
import os

class extract_as_csv(object):
    def extract_f1_json(url):
        page = requests.get(url)
        json_file = page.json()

        def db_name():
            j_temp = json_file['path']
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

        def weather(json_file):
            j_temp = json_file['Weather']
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

        def current_drivers(json_file):
            j_temp = json_file['init']
            j_temp = j_temp['data']
            j_temp = j_temp['Drivers']

            Driver_Name = []
            Driver_Initials = []
            Driver_Team = []
            Driver_Num = []

            for Driver in j_temp:
                Driver_Name.append(Driver['FirstName'] + ' ' + Driver['Name'])
                Driver_Initials.append(Driver['Initials'])
                Driver_Team.append(Driver['Team'])
                Driver_Num.append(Driver['Num'])

            print(Driver_Initials)

            return Driver_Initials

        def drivers_performance_points(json_file, Driver_Initials):
            j_temp = json_file['Scores']
            j_temp = j_temp['graph']
            j_temp = j_temp['Performance']

            for key in j_temp:
                print(key)
                for value in key:
                    print(value)

        weather(json_file)
        Driver_Initials = current_drivers(json_file)
        #drivers_performance_points(json_file, Driver_Initials)

    extract_f1_json('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json')
