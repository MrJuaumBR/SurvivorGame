"""
Config File
"""

import json
import os
import random
import importlib
import webbrowser
import sys
from .lines_counter import ForItemInDir
from .auto_installer import AUINS
import pyttsx3 # Text 2 Speech
from threading import Thread
Text2Speech = pyttsx3.Engine()

def _Speak(text):
    Text2Speech.say(text)
    Text2Speech.runAndWait()

def Speak(text:str):
    Thread(target=_Speak, args=(str(text),)).start()

import requests

global TRACKS, VERSION, BUILD_TILES

VERSION = '0.1.1b'
DEBUG = False
GAME_TITLE = "Survivor Game"
WORLD_MAX_SIZE = (2000,2000)

from data.plugins.pluginHandler import Loader

if not os.path.exists('./save/'):
    os.mkdir('./save/')

DATABASE_PATH = "/save/saves"
TEXTURES_PATH = "/data/assets"
ICONS_PATH    = TEXTURES_PATH + "/icons"
PLAYERS_SPRITESHEET = TEXTURES_PATH + "/player_spritesheet.png"
TILESET = TEXTURES_PATH + "/tileset.png"
DECO_ANIMATED = TEXTURES_PATH + "/deco_animated.png"
EMOTIONSET = TEXTURES_PATH + "/emotions.png"
PLAYERS = [
    "Man 1",
    "Guy 1",
    "Guy 2",
    "Old Man 1",
    "Guy 3",
    "Kid 1",
    "Knight 1",
    "Old Man 2",
    "Woman 1",
    "Woman 2",
    "Skull 1",
]
EMOTIONS = [
    "Alert",
    "Question",
    "Croon",
    "Heart",
    "Angry",
    "Nervous",
    "Confused",
    "Thinking",
    "Partying",
    "Drowsy"
]
EMOTIONS_POSITIONS = {
    "Alert":[(0,0,16,16),(16,0,16,16),(32,0,16,16),(48,0,16,16),(64,0,16,16),(80,0,16,16),(96,0,16,16)],
    "Question":[(0,16,16,16),(16,16,16,16),(32,16,16,16),(48,16,16,16),(64,16,16,16),(80,16,16,16),(96,16,16,16)],
    "Croon":[],
    "Heart":[],
    "Angry":[],
    "Nervous":[],
    "Confused":[],
    "Thinking":[],
    "Partying":[],
    "Drowsy":[]
}
EMOTIONS_SHEET = {
    "Alert":[],
    "Question":[],
    "Croon":[],
    "Heart":[],
    "Angry":[],
    "Nervous":[],
    "Confused":[],
    "Thinking":[],
    "Partying":[],
    "Drowsy":[]
}

SOUNDS_PATH   = "/data/musics"

CONFIG_DEFAULT_VALUE = {
    "FPS":60,
    "VOLUME":100,
    "FULLSCREEN":False,
    "SHOWFPS":False,
    'AUTOSAVE':True,
    'AUTOSAVE_TIME':4,
    'DEBUG_OUTPUT':False,
    'Text2Speech':False
}

# 0, 1, 2, 3, 4
AUTOSAVE_TIMES = [20,40,60,120,300] # Autosave Times in seconds

# 0, 1, 2
FPS_LIMIT_LIST = [30,60,120] # Frame Per Seconds Limit List

DF_WIDTH = 1024
DF_HEIGHT = 720
DEFAULT_SCREEN_SIZE = (DF_WIDTH, DF_HEIGHT)

from .handler.database import DB
from .handler.PyMaxEngine import *
from .handler.timerConverter import TimeConverter
from .handler.spritesheet import spritesheet

def LoadSlashAnimation():
    ss = spritesheet(f'.{TEXTURES_PATH}/sword_animation.png')

    StartPos = [20, 25]
    X_Addition = 120
    Y_Addition = 155
    SlashAnimations = {}
    for y in range(4):
        SlashAnimations[y] = []
        for x in range(6):
            img = pyg.transform.scale(ss.image_at((StartPos[0],StartPos[1],96,96),-1),(64,64))
            SlashAnimations[y].append(img)
            StartPos[0] += X_Addition
        StartPos[1] += Y_Addition
    return SlashAnimations

"""         Split Text         """
def split_text(text: str, max_per_line: int) -> list[str]:
    """
    Splits a given text into multiple lines based on a maximum number of characters per line.

    Args:
        text (str): The input text to be split.
        max_per_line (int): The maximum number of characters allowed per line.

    Returns:
        list[str]: A list of strings, each representing a line of the split text.
    """
    lines = []
    current_line = ""
    index_letter = 0
    if len(text) >= max_per_line:
        for letter in text:
            current_line += letter
            index_letter += 1
            if index_letter%max_per_line == 0:
                index_letter = 0
                lines.append(current_line)
                current_line = ''
    else:
        lines.append(text)
    return lines

def CreateTables():
    DB.database.create_table('saves',[('data',bytes,False)])
    DB.database.create_table('config',[('data',dict,False)])
    DB.database.create_table('plugins',[('pluginName',str),('pluginState',bool)])

    if not DB.database.get_value('config','data',0):
        # Insert Config if not exists
        DB.database.add_value('config','data',0,value=CONFIG_DEFAULT_VALUE)
    DB.save()

CreateTables() # Create Tables

def get_class(class_name) -> object:
    # Import Enemys
    return getattr(sys.modules[__name__], class_name)

# Load Data
CONFIG = dict(DB.database.get_value('config','data',0))

PLUGINS_HANDLER = {}

BUILD_TILES = {
    '0':None
}

# Setup Game
pyg.init()

pyg.mixer.init()

# Load Volume Config
pyg.mixer.music.set_volume(CONFIG['VOLUME']/100)

pme = PyMaxEngine()

SCREEN_FLAGS = SCALED
if CONFIG['FULLSCREEN']:
    SCREEN_FLAGS = FULLSCREEN|SCALED

SCREEN = pme.create_screen(DEFAULT_SCREEN_SIZE, flags=SCREEN_FLAGS)
# Get Icon

# Load Background Image
GAME_BACKGROUND = pyg.transform.scale(pme.load_image(f'.{TEXTURES_PATH}/background.jpeg'),SCREEN.get_size())

if not os.path.exists(f'.{ICONS_PATH}/png/icons.png'):
    icon = pyg.Surface((32,32))
    icon.fill((255,255,255))
    print('Icon Null')
else:
    Icons_Pos = [
        (47,70),
        (205,70),
        (371,70),
        (523,70), # Y2 = 220
    ]
    try:
        s = spritesheet(f'.{ICONS_PATH}/png/icons.png')
        rnd = random.choice(Icons_Pos)
        icon = s.image_at((rnd[0],rnd[1],128,128),-1)
        icon = pyg.transform.scale(icon, (32,32))
    except Exception as err:
        print(err)
# Load Icon
try:
    pme.set_icon(icon)
except:
    pass
# Load Emotions
try:
    for item in EMOTIONS_POSITIONS.keys():
        for pos in EMOTIONS_POSITIONS[item]:
            s = spritesheet("."+EMOTIONSET)
            EMOTIONS_SHEET[item].append(s.image_at(pos,0))
except Exception as err:
    raise(err)

CLOCK = pyg.time.Clock()

PUSH_NEWS = eval(requests.get('https://potatogameleague.jpgamesbr.repl.co/api/news.json').content)


TRACKS = {'ingame':f'.{SOUNDS_PATH}/ambientguitar.wav','level-up':f'.{SOUNDS_PATH}/levelup.mp3'}

FPS_FONT = pme.create_sysFont('arial',14,True,True) # Font Zero: 0
def ShowFPS(t=None):
    if CONFIG['SHOWFPS']:
        if int(CLOCK.get_fps()) <= CONFIG['FPS'] * 0.3:
            Color= 'red'
        elif int(CLOCK.get_fps()) <= CONFIG['FPS'] * 0.6:
            Color = 'yellow'
        elif int(CLOCK.get_fps()) <= CONFIG['FPS'] * 0.8:
            Color = 'lime'
        elif int(CLOCK.get_fps()) >= CONFIG['FPS'] * 0.9:
            Color = 'green'
        else:
            Color = 'black'
        pme.draw_text((SCREEN.get_size()[0]-50,0),str(int(CLOCK.get_fps())),FPS_FONT,Color,antialias=True)
    if pme.draw_button((SCREEN.get_size()[0]-30,0),'X',2,'white','red'):
        if t == None:
            DB.save()
            print(f'[Game - {GAME_TITLE}] {Fore.LIGHTMAGENTA_EX}Game ended!{Fore.RESET}')
            pme.quit()
        elif t == 0:
            pyg.time.delay(150)
            return True
        else:
            return False
    else:
        return False
    
global RND_COLOR
RND_COLOR = pme.colors[random.choice(list(pme.colors.keys()))]

"""          FONTS          """

pme.create_sysFont('arial', 32, True,False) # Font One: 1
pme.create_sysFont('arial', 18, True,False) # Font Two: 2
pme.create_sysFont('arial', 40, True,True) # Font Three: 3
pme.create_sysFont('arial', 12, True,False) # Font Four: 4
pme.create_sysFont('arial', 10, True,False) # Font Five: 5

"""          SIGNS          """
from math import pi

GAME_SIGNS_TEXT = ['Hello!',"I'm just a normal sign","Roberto Azevedo","Cleython Bom De guerra",f"{round(pi,8)}"]
GAME_NAMES = ['Pow Pow Game','Medieval Life','Plataformer Game','Survival2d',"JPyDB","ChosenBit","MrJuaum"]


from .camera import Camera

DebugStrf = "%d%m%y-%I_%M_%S_%p"

def EndGame():
    print(f'[Game - {GAME_TITLE}] {Fore.LIGHTMAGENTA_EX}Game ended!{Fore.RESET}')
    sys.stdout.close()

###                  After All, Load Plugin Handler                  ###

PLoader = Loader(pme, VERSION)

from .data.enemys import *
from .data.Tiles import *
from .data.Items import *