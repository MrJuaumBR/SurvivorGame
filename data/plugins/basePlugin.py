"""
File: pyplugin
"""

import requests
import os
import pygame

class _Plugin():
    ITEMS = {}
    AssetsFolder = "./data/plugins/assets"

    # Security
    RequireDownload = False # Require Download
    required = ''
    Enabled = False

    # Info
    Name = "Base Plugin"
    Version = 0.1
    GameVersion = 0.1
    Description = 'A Base Plugin'
    Icon = ''
    Author = 'MrJuaumBR'
    AuthorUrl = 'https://www.youtube.com/@mrjuaumbr'

    # Sounds and musics
    _HasSounds = False
    _Musics = {'ingame':None}
    def __init__(self, gameData) -> None:
        self.gameData = gameData
        self.pme = self.gameData.PME
        self.game_show_menu = False

        self._Musics['ingame'] = None

    def _FixUrl(self, url):
        return (url.split('?'))[0]

    def isEnabled(self) -> bool:
        if self.Enabled:
            return True
        else:
            return False
        
    def _DownloadData(self, local:str, chunk_size=128):
        try:
            save_path = self.AssetsFolder
            r = requests.get(local, stream=True)
            filename = self._FixUrl(local.split('/')[-1])
            save_path = f'{save_path}/{self.Name.replace(" ", "")}/{filename}'
            if not os.path.exists(f'{save_path.replace(filename,"")}'):
                print("\n\nPlugin creating folder...")
                os.mkdir(f"{save_path.replace(filename,'')}")
            if not os.path.exists(save_path):
                print(f"Downloading: {save_path}...")
                with open(save_path, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        fd.write(chunk)
                print("Download Completed!\n\n")
            else:
                print(f"Required: {save_path}, But already exists.")
        except Exception as err:
            print("Error occurred while trying to download plugin data.")
            raise(err)
        
    def varsGet(self,defines:list or dict, varname) -> any:
        x = defines.keys()
        if varname in x:
            return defines[varname]
        else:
            return None

    def Items(self) -> list:
        Items = []
        return Items

class Plugin(_Plugin):
    def __init__(self, gameData) -> None:
        super().__init__(gameData)
        if self.RequireDownload:
            if type(self.required) == str:
                self._DownloadData(self.required)
            elif type(self.required) == list:
                for item in self.required:
                    self._DownloadData(item)
            elif type(self.required) == dict:
                for key in self.required.keys():
                    self._DownloadData(self.required[key])