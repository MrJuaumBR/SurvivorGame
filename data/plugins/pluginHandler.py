import os

"""
Exception
"""

from JPyDB import pyDatabase
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
        self.IGNORE = ['pluginHandler.py','.py']

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
               raise(CustomExc(f'{file} is not a plugin!'))
            else:
                print(f'{file} Loaded!')
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
                print(f'{pluginName} Assets Deleted!')
            else:
                print(f'{pluginName} Assets Not Found!')
            if os.path.exists('./'+self.Folder+pluginName+'.py'):
                os.remove('./'+self.Folder+pluginName+'.py')
                print(f'{pluginName} Main Deleted!')
            else:
                print(f'{pluginName} Main Not Found!')
        except Exception as err:
            print(f"Error while trying to delete {pluginName}")
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