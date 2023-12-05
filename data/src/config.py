import json
import os
import random
import importlib
import webbrowser
import sys

import requests

global TRACKS, VERSION, BUILD_TILES

VERSION = 0.1
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
    'AUTOSAVE_TIME':0,
    'DEBUG_OUTPUT':False
}

AUTOSAVE_TIMES = [5,10,20,40,80,160]

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

def CreateTables():
    DB.database.create_table('saves',[('data',bytes,False)])
    DB.database.create_table('config',[('data',dict,False)])
    DB.database.create_table('plugins',[('pluginName',str),('pluginState',bool)])

    if not DB.database.get_value('config','data',0):
        # Insert Config if not exists
        DB.database.add_value('config','data',0,value=CONFIG_DEFAULT_VALUE)
    DB.save()

CreateTables() # Create Tables

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

FPS_FONT = pme.create_sysFont('arial',14,True,True)
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

pme.create_sysFont('arial', 32, True,False)
pme.create_sysFont('arial', 18, True,False)
pme.create_sysFont('arial', 40, True,True)
pme.create_sysFont('arial', 12, True,False)
pme.create_sysFont('arial', 10, True,False)

from .camera import Camera

DebugStrf = "%d%m%y-%I_%M_%S_%p"
#print(datetime.now().strftime(DebugStrf))
#print(datetime.now().strftime('%d/%m/%y, %I:%M:%S(%p)'))

def EndGame():
    print(f'[Game - {GAME_TITLE}] {Fore.LIGHTMAGENTA_EX}Game ended!{Fore.RESET}')
    sys.stdout.close()

###                  After All, Load Plugin Handler                  ###

PLoader = Loader(pme, VERSION)