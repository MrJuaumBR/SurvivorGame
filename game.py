from data.src.config import *
from data.src.screens import *


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
                if not plg:
                    DB.database.add_values('plugins',['pluginName','pluginState'],[pluginName,False])
                    DB.save()
                PLUGINS_HANDLER[pluginName+"_metadata"] = importlib.import_module(plugin)
                PLUGINS_HANDLER[pluginName] = PLUGINS_HANDLER[pluginName+"_metadata"].Plugin(gameData)
                PLUGINS_HANDLER[pluginName].Enabled = plg['pluginState']
                if PLUGINS_HANDLER[pluginName].Enabled:
                    if PLUGINS_HANDLER[pluginName]._HasSounds:
                        for key in PLUGINS_HANDLER[pluginName]._Musics.keys():
                            TRACKS[key] = f'{PLUGINS_HANDLER[pluginName].AssetsFolder}/{str(PLUGINS_HANDLER[pluginName].Name).replace(" ","")}/{PLUGINS_HANDLER[pluginName]._Musics[key]}'
            except Exception as err:
                print(f"Error occurred while trying to load plugins, plugin index: {x}, plugin import: {plugin}")
                raise(err)
# Game Loop
def gameLoop():
    while True:
        for ev in pme.events():
            if ev.type == QUIT:
                DB.save()
                pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_F9:
                    pass

        
        
        
        ShowFPS() # Show FPS
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR)
        if pme.draw_button((50,50),'PLAY',1,'white','green'):
            LoadSaveScreen()
        elif pme.draw_button((50,100),'OPTIONS',1,'white','blue'):
            options()
            pyg.mixer.music.set_volume(CONFIG['VOLUME']//100)
        elif pme.draw_button((50,SCREEN.get_size()[1]-75),'EXIT',1,'white','red'):
            DB.save()
            pme.quit()
        PLoader.LoadMainGameLoop(PLUGINS_HANDLER)
        pme.update()
        pme.screen.fill('white') # Fill Screen
        CLOCK.tick(CONFIG['FPS'])


if __name__ == "__main__":
    LoadPluginsMods()
    gameLoop()