import requests
import pandas as pd

test_page = requests.get('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json')
json_file = test_page.json()
print(json_file)

j_temp = json_file['path']
j_temp = j_temp[5:]
csv_name = ''

n = 0
while j_temp[n] != '/':
    csv_name = csv_name+j_temp[n]
    n = 1 + n

print('\ncsv name')
print(csv_name)
