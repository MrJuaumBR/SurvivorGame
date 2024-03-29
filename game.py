"""
Game File

Run This for run the game
"""
from data.src.Exceptions import *
from data.src.integrity import IntegrityCheck

if not IntegrityCheck('./'):
    raise MissingFilesOrFolders

try:
    from data.src.config import *
    from data.src.screens import *
except ModuleNotFoundError:
    print('Some Modules Not Found')
    try:
        print('Installing Modules...')
        # Try to install modules
        from os import system
        system('pip install -r requirements.txt')
        # If Sucess, re-run
        print('Installed Needed Modules! Re Run the game')
    except Exception as err:
        print("Can't Install Modules...")
        raise(err)
    
DB_CHECK= lambda: f'Database Size: {DB.get_db_size()}' if os.path.exists(DB.database.filename) else ''
print(f"""
[Game - {GAME_TITLE}]
\tPyGame Version: {pyg.__version__}
\tPyMaxEngine Version: {pme.ver}
\tJPyDB Version: {DB.database.VERSION}
\tGame Version: {VERSION}
\tWelcome to the game!
\tTotal Lines: {ForItemInDir("./")}
\t{DB_CHECK()}
""")

if CONFIG['DEBUG_OUTPUT']:
    if not os.path.exists('./save/debug/'):
        os.mkdir('./save/debug/')
    DebugFilename = f'debug{datetime.now().strftime(DebugStrf)}'
    sys.stdout = open(f'./save/debug/{DebugFilename}.log', 'w+')

# Plugins Sender
class _gameData():
    # Version
    VERSION = VERSION

    # Paths
    DATABASE_PATH = DATABASE_PATH
    TEXTURES_PATH = TEXTURES_PATH
    ICONS_PATH    = ICONS_PATH
    SOUNDS_PATH   = SOUNDS_PATH
    PME = pme
    PLUGINS_HANDLER = PLUGINS_HANDLER
    PLoader = PLoader
    DB = DB
    def __init__(self) -> None:
        pass

gameData = _gameData()

# Load plugins/mods
def LoadPluginsMods():
    plugins = PLoader.Load()
    for x,plugin in enumerate(plugins):
        if plugin:
            try:
                pluginName = plugin.split('.')[-1]
                plg = DB.database.findByText('plugins', 'pluginName',pluginName)
                if not plg['id']:
                    DB.database.add_values('plugins',['pluginName','pluginState'],[pluginName,False])
                    DB.save()
                plg = DB.database.findByText('plugins', 'pluginName',pluginName)
                PLUGINS_HANDLER[pluginName+"_metadata"] = importlib.import_module(plugin)
                PLUGINS_HANDLER[pluginName] = PLUGINS_HANDLER[pluginName+"_metadata"].Plugin(gameData)
                PLUGINS_HANDLER[pluginName].Enabled = plg['pluginState']
                if PLUGINS_HANDLER[pluginName].Enabled:
                    if PLUGINS_HANDLER[pluginName]._HasSounds:
                        for key in PLUGINS_HANDLER[pluginName]._Musics.keys():
                            TRACKS[key] = f'{PLUGINS_HANDLER[pluginName].AssetsFolder}/{str(PLUGINS_HANDLER[pluginName].Name).replace(" ","")}/{PLUGINS_HANDLER[pluginName]._Musics[key]}'
            except Exception as err:
                print(f"[Plugin Loader] {Fore.RED}Error occurred while trying to load plugins, plugin index: {x}, plugin import: {plugin}{Fore.RESET}")
                raise(err)
# Game Loop
def gameLoop():
    print(f'[Game - {GAME_TITLE}]\n\t{Fore.LIGHTMAGENTA_EX}Version: {VERSION}\n\tStarting...{Fore.RESET}')
    l = 0
    while True:
        if l == 0:
            l += 1
            print(f'[Game - {GAME_TITLE}]\n\t{Fore.LIGHTMAGENTA_EX}Started!{Fore.RESET}')
            
        for ev in pme.events():
            if ev.type == QUIT:
                DB.save()
                EndGame()
                pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_F9:
                    pass

        
                
        ShowFPS() # Show FPS
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR)
        pme.draw_text((SCREEN.get_size()[0]-(304*2),32),GAME_TITLE,1,(0,0,0),antialias=True)
        pme.draw_rect2((45,45),(300, SCREEN.get_size()[1]-60),(216, 211, 192,100),3)
        if pme.draw_button((50,50),'PLAY',1,'white','green'):
            LoadSaveScreen()
        elif pme.draw_button((50,100),'OPTIONS',1,'white','blue'):
            options()
            pyg.mixer.music.set_volume(CONFIG['VOLUME']//100)
        elif pme.draw_button((50,SCREEN.get_size()[1]-75),'EXIT',1,'white','red'):
            DB.save()
            pme.quit()
        elif pme.draw_button((200,SCREEN.get_size()[1]-75),'LEGALS',2,'white','brown'):
            Legals()
        elif pme.draw_button((200,SCREEN.get_size()[1]-50),'GitHub',2,'white','black',True):
            webbrowser.open('https://github.com/MrJuaumBR/SurvivorGame')
            pyg.time.delay(100)
        elif pme.draw_button((275,SCREEN.get_size()[1]-75),'Discord',2,'white','blue',True):
            webbrowser.open('https://discord.gg/fb84sHDX7R')
            pyg.time.delay(100)
        PLoader.LoadMainGameLoop(PLUGINS_HANDLER)
        pme.update()
        pme.screen.fill((216, 211, 192)) # Fill Screen
        pme.insert_on(GAME_BACKGROUND,(0,0))
        CLOCK.tick(CONFIG['FPS'])
    EndGame()


if __name__ == "__main__":
    LoadPluginsMods()
    gameLoop()
    EndGame()