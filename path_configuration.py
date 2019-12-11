import os
import datetime

class Path(object):

    Database = 'Database/'
    GrandPrix = 'GrandPrix/'
    Config = 'Config/'
    Season = 'Season/'

    def __init__(self):
        if not os.path.exists(self.Database + self.GrandPrix):
            os.makedirs(self.Database + self.GrandPrix)
        if not os.path.exists(self.Database + self.Config):
            os.makedirs(self.Database + self.Config)
        if not os.path.exists(self.Database + self.Season):
            os.makedirs(self.Database + self.Season)

    def grandprix_path(self, date, name):
        Path = self.Database + self.GrandPrix + date + '_' + name + '.csv'
        return Path

    def config_path(self, name):
        Path = self.Database + self.Config + name + '.csv'
        return Path

    def season_path(self, name):
        Path = self.Database + self.Season + name + '.csv'
        return Path
