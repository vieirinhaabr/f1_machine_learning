import os


class ProgressBar(object):
    Max = None
    Progress = 0
    Progress_Bars = ''
    Status = ''

    def __init__(self, undefined):
        if type(undefined) == list:
            self.as_list(undefined)
        elif type(undefined) == int:
            self.as_int(undefined)
        else:
            print('Type error')

    def create_progress_bar(self):
        i = 0
        while i <= int(self.Max):
            self.Progress_Bars = self.Progress_Bars + '#'
            i = i + 1

    def as_list(self, list):
        gap = 100 / list.__len__()
        self.Max = gap
        self.create_progress_bar()

    def as_int(self, counter):
        gap = 100 / counter
        self.Max = gap
        self.create_progress_bar()

    def get_progress_bar(self):
        self.Progress = self.Progress + self.Max
        self.Status = self.Status + self.Progress_Bars

        return '/ ' + self.Status + ' / ' + str(self.Progress)
