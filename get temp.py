import requests
import pandas as pd

test_page = requests.get('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json')
json_file = test_page.json()
print(json_file)

j_temp = json_file['Weather']
print(j_temp)

j_temp = j_temp['graph']
print(j_temp)

j_temp = j_temp['data']
print(j_temp)

j_temp = j_temp['pTrack']
print(j_temp)

# GET BY JSON
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

print(Track_Temp_Data.head())
