from .config import *
from .camera import *
from .player import player
from .data.items import *
from .data.enemys import *

def loadBuild():
    for x,item in enumerate(BUILD_ITEMS,0):
        BUILD_TILES[str(x)] = item

def game(playerId):
    global DrawEmotions
    run = True
    loadBuild()
    pyg.mixer.music.load(TRACKS['ingame'])
    pyg.mixer.music.play(-1)
    DrawEmotions = False
    cam = Camera()
    Plr = player((550,550),cam)
    Plr.Load(DB.database.get_value('saves','data',id=playerId))
    def ex():
        DB.database.update_value('saves','data',playerId,Plr.Save(cam))
        DB.database.save()
        pyg.mixer.music.stop()
        return False
    def generateMap():
        # Enemy
        for i in range(random.randint(10, 25)):
            Enemy((random.randint(0, 2000), random.randint(0, 2000)), cam)
        
        # Decorations
        for i in range(random.randint(100, 250)):
            random.choice([Decoration1,Decoration2,Decoration3,Decoration4,Decoration5])((random.randint(0, 2000), random.randint(0, 2000)), cam)
    generateMap()
    MenuOpen = False
    def DrawWarns():
        for x,warn in enumerate(Plr.warns):
            pme.draw_text((10,65+(x*15)),f'{warn[0]}',4,warn[1],(0,0,0))
    def DrawMenu(op:bool,DrawEmotions:bool):
        if DrawEmotions:
            pme.draw_rect(((SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-125),(500,250),(0,0,0,100))
            pme.draw_text(((SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-125),'Emotions',2,'white')
            Pos = [(SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-100]
            for i,emotion in enumerate(EMOTIONS_SHEET.keys()):
                if i >= 5:
                    Pos[0] = (SCREEN.get_size()[0]//2)-250
                    Pos[1] += 36
                else:
                    Pos[0] += 36
                try:
                    SCREEN.blit(pyg.transform.scale(EMOTIONS_SHEET[emotion][0],(32,32)),Pos)
                except:
                    pass
                
        if op:
            pme.draw_rect((0,0),(150,pme.screen.get_size()[1]),(0,0,0,100))
            pme.draw_text((10,10),'Menu',1,'white')
            DrawEmotions = False
            if pme.draw_button((10,80),'Status',2,'white','brown',True):
                Plr._StatusOpen = True
                return (not op),DrawEmotions
            else:
                return op, DrawEmotions
        else:
            SY = SCREEN.get_size()[1]
            pme.draw_bar((10,SY-120),(200,20),Plr.health,Plr.maxhealth,[pme.colors['Maroon'],(200,10,10),(0,0,0)],f'{round(Plr.health)}/{round(Plr.maxhealth)} ({round(Plr.health/Plr.maxhealth*100)}%)',2)
            pme.draw_text((10,SY-95),Plr.name[:12],2,'white',antialias=True)
            pme.draw_text((10,SY-65),f'Level: {Plr.Level}',2,'white',antialias=True)
            pme.draw_bar((10,SY-40),(200,20),Plr.Experience,Plr.Level*100,[pme.colors['Maroon'],pme.colors['BlueViolet'],(0,0,0)],f'{round(Plr.Experience)}/{round(Plr.Level*100)} ({round((Plr.Experience/(Plr.Level*100)*100))}%)',2)
            if SCREEN.blit(EMOTIONS_SHEET['Alert'][0],(10,SY-145)).collidepoint(pyg.mouse.get_pos()):
                if pyg.mouse.get_pressed(3)[0]:
                    DrawEmotions = not DrawEmotions
                    pyg.time.delay(250)
                else:
                    DrawEmotions = DrawEmotions
            else:
                DrawEmotions = DrawEmotions
            return op, DrawEmotions
    while run:
        DrawWarns()
        MenuOpen,DrawEmotions = DrawMenu(MenuOpen,DrawEmotions)
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