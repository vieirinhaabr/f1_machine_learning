import pandas as pd
import requests


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

        def generate_csv_name(csv_type):
            path_db = 'Database/' + csv_name + '-' + csv_type + '.csv'

            return path_db

        def track_temp():
            j_temp = json_file['Weather']
            j_temp = j_temp['graph']
            j_temp = j_temp['data']
            j_temp = j_temp['pTrack']

            Time = []
            Temp = []

            i = 0
            for value in j_temp:
                if i == 0:
                    Time.append(value)
                    i = 1
                else:
                    Temp.append(value)
                    i = 0

            Track_Temp = {"Time": Time, "Temperature": Temp}

            Track_Temp_Data = pd.DataFrame(data=Track_Temp)
            Track_Temp_Data = Track_Temp_Data.set_index('Time')

            path_db = generate_csv_name('Track_Temp')

            Track_Temp_Data.to_csv(path_db)

        track_temp()

    extract_f1_json('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json')
