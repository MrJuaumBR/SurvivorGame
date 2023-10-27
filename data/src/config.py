import os
import random
import importlib
import webbrowser

global TRACKS

VERSION = 0.1

from data.plugins.pluginHandler import Loader

if not os.path.exists('./save/'):
    os.mkdir('./save/')

DATABASE_PATH = "/save/saves"
TEXTURES_PATH = "/data/assets"
ICONS_PATH    = TEXTURES_PATH + "/icons"

SOUNDS_PATH   = "/data/musics"

CONFIG_DEFAULT_VALUE = {
    "FPS":60,
    "VOLUME":100,
    "FULLSCREEN":False,
    "SHOWFPS":False
}
DF_WIDTH = 1024
DF_HEIGHT = 720
DEFAULT_SCREEN_SIZE = (DF_WIDTH, DF_HEIGHT)

from .handler.database import DB
from .handler.PyMaxEngine import *
from .handler.spritesheet import spritesheet
from .handler.timerConverter import TimeConverter

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

# Setup Game
pyg.init()

pme = PyMaxEngine()

SCREEN_FLAGS = SCALED
if CONFIG['FULLSCREEN']:
    SCREEN_FLAGS = FULLSCREEN|SCALED

SCREEN = pme.create_screen(DEFAULT_SCREEN_SIZE, flags=SCREEN_FLAGS)

CLOCK = pyg.time.Clock()

TRACKS = {'ingame':f'.{SOUNDS_PATH}/ambientguitar.wav'}

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

###                  After All, Load Plugin Handler                  ###

PLoader = Loader(pme, VERSION)