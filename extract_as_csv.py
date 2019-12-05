import pandas as pd
import requests
import lxml.html as ht
import json

"""class extract_as_csv(object):
        def get_table(page, table_class, table_type=True):
            if table_type is True:
                #race
            else:
                #classification"
            """

# get json from f1 site
page = requests.get('https://livetiming.formula1.com/static/2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/SPFeed.json')

# convert to string
page_content = str(page.content)
print(page_content)

# remove /n/d from code of page
page_content = page_content[14:]
print("\n\n", page_content)

lenght = len(page_content)

i = 0

# GET TEMPERATURE OF TRACK

for i in range(0, lenght):
    if page_content[i] == "p":
        if page_content[i + 1] == "T":
            if page_content[i + 2] == "r":
                if page_content[i + 3] == "a":
    i = i + 1
# page_json = json.loads('{"0.0" "30.7", "15.0", "35.0"}')

# {"pTrack":[0.0,30.7,15.0,30.7,75.0,30.5]}         ---BEFORE
# {"pTrack":["0.0":"30.7","15.0":"30.7","75.0":"30.5"]}           --AFTER



# print(page_json)
