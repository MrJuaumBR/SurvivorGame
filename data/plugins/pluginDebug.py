"""
File: pyplugin
"""
from .basePlugin import _Plugin as _BasePlugin
import requests
import os
import pygame

def ConvertSize(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024**2:
        return f"{size/1024:.2f}KB"
    elif size < 1024**3:
        return f"{size/(1024**2):.2f}MB"
    elif size < 1024**4:
        return f"{size/(1024**3):.2f}GB"

class _Plugin(_BasePlugin):
    ITEMS = {}
    AssetsFolder = "./data/plugins/assets"

    # Security
    RequireDownload = True # Require Download
    required = ['https://raw.githubusercontent.com/MrJuaumBR/MrJuaumBR.github.io/main/data/debugPluginIcon.jpeg','https://github.com/MrJuaumBR/Survivor2d/raw/main/data/sounds/mainmusic.wav']
    Enabled = False

    # Info
    Name = "Debug Plugin"
    Version = 0.1
    GameVersion = 0.1
    Description = 'A Base plugin, with some Debug features...'
    Icon = 'debugPluginIcon.jpeg'
    Author = 'MrJuaumBR'
    AuthorUrl = 'https://www.youtube.com/@mrjuaumbr'

    # Sounds and musics
    _HasSounds = True
    _Musics = {'ingame':None}
    def __init__(self, gameData) -> None:
        self.gameData = gameData
        self.pme = self.gameData.PME
        self.game_show_menu = False

        self._Musics['ingame'] = 'mainmusic.wav'

    # Loops
    def MainGameLoop(self):
        pass

    def CreateSaveLoop(self):
        pass

    def LoadSaveScreenLoop(self):
        self.pme.draw_text((10,10),f'Saves: {self.gameData.DB.database.ids_count("saves")},     Size: {ConvertSize(os.path.getsize(self.gameData.DB.database.filename))}',4, (0,0,0),(255,255,255))

    def optionsLoop(self):
        plugins = ''
        Rejected = self.gameData.PLoader.RejectMetadata(self.gameData.PLUGINS_HANDLER)
        for name in Rejected:
            if name != Rejected[-1]:
                plugins += f"{name}, "
            else:
                plugins += f'{name}'
        self.pme.draw_text((10,10),f"Mods: {plugins}",4, (0,0,0),(255,255,255))
        if self.pme.draw_button((10,self.pme.screen.get_size()[1]-100),'Delete Database',2,'white','red'):
            self.gameData.DB.deleteDatabase()
        if self.pme.draw_button((10,self.pme.screen.get_size()[1]-125),'Delete Saves',2,'white','red'):
            self.gameData.DB.database.delete_all('saves')

    def drawGameMenu(self, player, camera):
        if self.game_show_menu:
            self.pme.draw_rect((50,50),(self.pme.screen.get_size()[0]-100,self.pme.screen.get_size()[1]-100),(0,0,0,128))
            self.pme.draw_text((60,55),f'Debug Menu',1, (0,0,0),(255,255,255))
            self.pme.draw_text((60,95),f'Name: {player.name[:65]}',4, (0,0,0),(255,255,255))
            self.pme.draw_text((60,125),f'Origin Pos: {player.rect.center}, Offset pos: {camera.convert_offset(player.rect.topleft)}',4, (0,0,0),(255,255,255))
            self.pme.draw_text((175,155),f'Player Lvl: {player.Level}, Experience: {player.Experience}/{player.Level * 100}',4, (0,0,0),(255,255,255))
            self.pme.draw_text((60, 200),f'Attack: {player.attack}, Defense: {player.defense}, Agility: {player.agility}, Inteligence: {player.inteligence}, Luck: {player.luck}',2, (0,0,0),(255,255,255))
            self.pme.draw_text((60, 250),f'Speed: {player.speed}, Damage: {player.damage}',2, (0,0,0),(255,255,255))
            self.pme.draw_text((60,300),f'Character Color: {player.Color}',2, (0,0,0),(255,255,255))
            if self.pme.draw_button((60,155),'+ 1 Level',1,'white','green'):
                player.Experience += player.Level * 100
            if self.pme.draw_button((350,155),'+ 100 Exp',1,'white','green'):
                player.Experience += 100
            if player._dead:
                if self.pme.draw_button((60,self.pme.screen.get_size()[1]-150),'Revive',1,'white','green'):
                    player.health = player.maxhealth
                    player._dead = False
            player._locked = True
        else:
            player._locked = False

    def GameLoop(self, defined:list or dict):
        player = self.varsGet(defined, 'Plr')
        camera = self.varsGet(defined, 'cam')
        self.pme.draw_text((10,10),f'Game Version: {self.GameVersion}',4, (0,0,0),(255,255,255))
        obj = pygame.transform.scale(pygame.image.load(f'{self.AssetsFolder}/{self.Name.replace(" ", "")}/{self.Icon}'),(32,32))
        objpos = obj.get_rect()
        objpos.topleft = (10,30)
        self.pme.screen.blit(obj,objpos)

        offset = camera.convert_offset((player.rect.centerx,player.rect.top))
        self.pme.draw_text((offset[0]-10,offset[1]-10),f'Health: {player.health}/{player.maxhealth}',4, (0,0,0),(255,255,255))
        self.pme.draw_text((offset[0]-10,offset[1]-30),f'Name: {player.name[:12]}',4, (0,0,0),(255,255,255))

        if objpos.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed(3)[0]:
                self.game_show_menu = not self.game_show_menu
                pygame.time.delay(100)
        if self.game_show_menu:
            self.drawGameMenu(player, camera)

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