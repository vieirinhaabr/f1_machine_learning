import os
import bcolors


class ProgressBar(object):
    Max = None
    Progress = 0
    Progress_Bars = ''
    Status = ''
    Left_Border = '['
    Right_Border = ']'

    def __init__(self, undefined):
        if type(undefined) == list:
            self.as_list(undefined)
        elif type(undefined) == int:
            self.as_int(undefined)
        elif type(undefined) == bool:
            self.create_progress_counter()
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

        print(bcolors.HELP + '/ ' + self.Status + ' / ' + '{0:.2f}'.format(self.Progress) + bcolors.END)

    def create_progress_counter(self):
        self.Progress_Bars = '#'
        self.Status = self.Progress_Bars
        print('Starting Counter...')

    def get_progress_counter(self, counter):
        print(bcolors.WAITMSG + self.Left_Border + self.Status + self.Right_Border, ' Getting lap:', str(counter) + bcolors.END)
        self.Status = self.Status + self.Progress_Bars
