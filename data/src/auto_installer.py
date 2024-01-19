"""
System for install some Libraries if it don't is installed

Only works if python is installed & Only in windows
"""


# Only Execute if can't install some thing from requirements.txt
from os import system

class AutoInstaller():
    ex_JPyDB = ''
    ex_PyGame = ''
    def InstallJPyDB(self):
        try:
            system(self.ex_JPyDB)
        except Exception as err:
            print(err)

    def InstallPyGame(self):
        try:
            system(self.ex_PyGame)
        except Exception as err:
            print(err)

AUINS = AutoInstaller()