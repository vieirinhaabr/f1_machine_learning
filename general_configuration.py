# Package imports
import pandas as pd
import requests
import datetime
from unidecode import unidecode as UnicodeFormatter
import os
import json

# Local imports
import path_configuration
import url_configuration
import progress_calculator


class General_Config(object):
    Url = None
    Path = None
    Requests = None

    def __init__(self):
        self.Url = url_configuration.Url_builder()
        self.Path = path_configuration.Path()
        self.Requests = requests

    def import_status_csv(self):
        url = self.Url.url_status()

        page = self.Requests.get(url)
        json = page.json()
        json = json['MRData']
        json = json['StatusTable']
        Status = json['Status']

        counter = 0
        for element in Status:
            counter = counter + 1
        Progress = progress_calculator.ProgressBar(counter)

        StateID = []
        StateOccurrences = []
        StateDescription = []

        for state in Status:
            StateID.append(state['statusId'])
            StateOccurrences.append(state['count'])
            StateDescription.append(state['status'])

            Progress.get_progress_bar()

        Status_Dict = {"State ID": StateID, "State Occurrences": StateOccurrences,
                       "State Description": StateDescription}
        State_Data = pd.DataFrame(data=Status_Dict)
        State_Data = State_Data.set_index("State ID")

        Path = self.Path.config_path('StatusInfo')
        State_Data.to_csv(Path)
