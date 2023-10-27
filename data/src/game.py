from .config import *
from .camera import *
from .player import player
from .data.items import *
from .data.enemys import *

def game(playerId):
    run = True
    pyg.mixer.music.load(TRACKS['ingame'])
    pyg.mixer.music.play(-1)
    cam = Camera()
    Plr = player((550,550),cam)
    Plr.Load(DB.database.get_value('saves','data',id=playerId))
    def ex():
        DB.database.update_value('saves','data',playerId,Plr.Save())
        DB.database.save()
        pyg.mixer.music.stop()
        return False
    def generateMap():
        for i in range(random.randint(10, 25)):
            Enemy((random.randint(0, 1000), random.randint(0, 1000)), cam)
    generateMap()

    def DrawWarns():
        for x,warn in enumerate(Plr.warns):
            pme.draw_text((10,65+(x*15)),f'{warn[0]}',4,warn[1],(0,0,0))
    while run:
        DrawWarns()
        if ShowFPS(0): # Exit by clicking in X on screen
            pyg.time.delay(100)
            run = ex()

        for ev in pme.events():
            if ev.type == QUIT:
                run = ex()
    
        # Update
        PLoader.LoadGameLoop(PLUGINS_HANDLER, globals(), locals())
        pme.update()
        cam.update(Plr)

        # Draw
        SCREEN.fill('black')
        cam.draw(Plr)
        # FPS
        CLOCK.tick(CONFIG['FPS'])