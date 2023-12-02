import os

"""
Exception
"""

from JPyDB import pyDatabase
from colorama import Fore, Back
class CustomExc(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args

"""
Main Code
"""

class Loader():
    Accetable = ['pyplugin','py']
    def __init__(self, pme, gameVersion) -> None:
        self.Folder = './data/plugins/'
        if not os.path.exists(self.Folder+'assets/'):
            os.mkdir(self.Folder+'assets/')
        self.IGNORE = ['pluginHandler.py','basePlugin.py']

    def CheckIntegrity(self, _file:str) -> bool:
        x = _file.split('.')
        if len(x) > 1:
            if len(x) == 2:
                if x[1].lower() in self.Accetable:
                    return True
        return False
    
    def StripLines(self, text:str) -> list [str,]:
        stripped = []
        for line in text.split('\n'):
            if not (line.startswith('#') or line.startswith('"""')):
                stripped.append(line)
        return stripped

    def LoadPlugin(self,file:str) -> str:
        x = None
        x2 = None
        if not self.CheckIntegrity(file):
            return
        try:
            with open(self.Folder+file,'r') as f:
                x = f.read()
        except Exception as err:
            raise(err)
        x2 = self.StripLines(x)
        if x and x2 and len(x2) > 0:
            if not (x2[0].split(' ')[1].lower() in self.Accetable):
               raise(CustomExc(f'[Plugin Handler] {Fore.RED}{file} is not a plugin!{Fore.RESET}'))
            else:
                print(f'[Plugin Handler] {Fore.GREEN}{file} Loaded!{Fore.RESET}')
                Stringed = ""
                Stringed = self.Folder.replace('.','') #remove extra '.'
                Stringed = Stringed[1:] # Remove First Character
                Stringed = Stringed.replace('/','.')
                Stringed = Stringed + file.split(".")[0]
                return f'{Stringed}'

    def DeletePlugin(self, pluginName):
        try:
            if os.path.exists('./assets/'+self.Folder+pluginName):
                os.remove('./assets/'+self.Folder+pluginName)
                print(f'[Plugin Handler] {Fore.RED}{pluginName} Assets Deleted!{Fore.RESET}')
            else:
                print(f'[Plugin Handler] {Fore.RED}{pluginName} Assets Not Found!{Fore.RESET}')
            if os.path.exists('./'+self.Folder+pluginName+'.py'):
                os.remove('./'+self.Folder+pluginName+'.py')
                print(f'[Plugin Handler] {Fore.RED}{pluginName} Main Deleted!{Fore.RESET}')
            else:
                print(f'[Plugin Handler] {Fore.RED}{pluginName} Main Not Found!{Fore.RESET}')
        except Exception as err:
            print(f"[Plugin Handler] {Fore.RED}Error while trying to delete {pluginName}{Fore.RESET}")
            raise(err)

    def Load(self) -> list[str,]:
        loades = []
        for file in os.listdir(self.Folder):
            if file not in self.IGNORE:
                loades.append(self.LoadPlugin(file))
        return loades

    def RejectMetadata(self, plugins:dict) -> list:
        l = []
        for key in plugins.keys():
            if plugins[key]:
                if not (len(key.split('_metadata')) > 1):
                    l.append(key)
        return l

    def LoadMainGameLoop(self, Plugins:dict):
        for key in self.RejectMetadata(Plugins):
            if Plugins[key].isEnabled():
                Plugins[key].MainGameLoop()

    def LoadOptionsLoop(self, Plugins:dict):
        for key in self.RejectMetadata(Plugins):
            if Plugins[key].isEnabled():
                Plugins[key].optionsLoop()

    def LoadSaveScreenLoop(self, Plugins:dict):
        for key in self.RejectMetadata(Plugins):
            if Plugins[key].isEnabled():
                Plugins[key].LoadSaveScreenLoop()

    def LoadGameLoop(self, Plugins:dict, globalsvars:dict, localsvars:dict):
        x = globalsvars | localsvars
        for key in self.RejectMetadata(Plugins):
            if Plugins[key].isEnabled():
                Plugins[key].GameLoop(x)

if __name__ == "__main__":
    x = Loader()
    x.Load()