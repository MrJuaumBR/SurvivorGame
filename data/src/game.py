from .config import *
from .camera import *
from .player import player
from .data.items import *
from .data.enemys import *

def loadBuild():
    for x,item in enumerate(BUILD_ITEMS,0):
        BUILD_TILES[str(x)] = item

def game(playerId):
    run = True
    loadBuild()
    pyg.mixer.music.load(TRACKS['ingame'])
    pyg.mixer.music.play(-1)
    cam = Camera()
    Plr = player((550,550),cam)
    Plr.Load(DB.database.get_value('saves','data',id=playerId))
    def ex():
        DB.database.update_value('saves','data',playerId,Plr.Save(cam))
        DB.database.save()
        pyg.mixer.music.stop()
        return False
    def generateMap():
        for i in range(random.randint(10, 25)):
            Enemy((random.randint(0, 1000), random.randint(0, 1000)), cam)
    generateMap()
    MenuOpen = False
    def DrawWarns():
        for x,warn in enumerate(Plr.warns):
            pme.draw_text((10,65+(x*15)),f'{warn[0]}',4,warn[1],(0,0,0))
    def DrawMenu(op:bool):
        if op:
            pme.draw_rect((0,0),(150,pme.screen.get_size()[1]),(0,0,0,100))
            pme.draw_text((10,10),'Menu',1,'white')
            if pme.draw_button((10,80),'Status',2,'white','brown',True):
                Plr._StatusOpen = True
                return not op
            else:
                return op
        else:
            return op
    while run:
        DrawWarns()
        MenuOpen = DrawMenu(MenuOpen)
        if ShowFPS(0): # Exit by clicking in X on screen
            pyg.time.delay(100)
            run = ex()

        for ev in pme.events():
            if ev.type == QUIT:
                run = ex()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    MenuOpen = not MenuOpen
    
        # Update
        PLoader.LoadGameLoop(PLUGINS_HANDLER, globals(), locals())
        Plr.drawUis(BUILD_TILES)
        pme.update()
        cam.update(Plr)

        # Draw
        SCREEN.fill('black')
        cam.draw(Plr)
        # FPS
        CLOCK.tick(CONFIG['FPS'])