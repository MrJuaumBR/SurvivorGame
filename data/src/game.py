from .config import *
from .camera import *
from .player import player
from .data.Tiles import *
from .data.enemys import *
from .world import *
from .handler.Icons import *

def loadBuild():
    for x,item in enumerate(BUILD_ITEMS,0):
        BUILD_TILES[str(x)] = item

def game(playerId):
    run = True
    loadBuild()
    pyg.mixer.music.load(TRACKS['ingame'])
    pyg.mixer.music.play(-1)
    DrawEmotions = False
    cam = Camera()
    Plr = player((550,550),cam)
    Plr.Load(DB.database.get_value('saves','data',id=playerId))
    W:World = World()
    W.Load(Plr.W.__dict__)

    # Create Uis Icon (Free Ram)
    LFIcon = LifeIcon((32,32),True,'Life')
    ExpIcon = ExperienceIcon((64,64),True,'Experience')

    def ex():
        DB.database.update_value('saves','data',playerId,Plr.Save(cam))
        DB.database.save()
        pyg.mixer.music.stop()
        return False
    def generateMap():
        # Enemy
        for i in range(random.randint(10, 25)):
            Enemy((random.randint(0, 2000), random.randint(0, 2000)), cam)
        
        # Friendly
        for i in range(random.randint(10,25)):
            Chicken((random.randint(0, 2000), random.randint(0, 2000)), cam)

        # Decorations
        for i in range(random.randint(100, 250)):
            random.choice([Decoration1,Decoration2,Decoration3,Decoration4,Decoration5])((random.randint(0, 2000), random.randint(0, 2000)), cam)
        
        # Trees
        for i in range(random.randint(75,175)):
            random.choice([Tree])((random.randint(0, 2000), random.randint(0, 2000)), cam)
    generateMap()
    MenuOpen = False

    # Tips
    EmoBtnTip = Tip('Emotions Menu', pme,(0,0,0),(216, 211, 192),4)
    def DrawWarns():
        for x,warn in enumerate(Plr.warns):
            pme.draw_text((10,65+(x*15)),f'{warn[0]}',4,warn[1],(0,0,0))
    def DrawMenu(op:bool,DrawEmotions:bool):
        EmotionsButtons:list[Rect,Rect,] = []
        if DrawEmotions:
            pme.draw_rect(((SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-125),(500,250),(216, 211, 192,100))
            pme.draw_text(((SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-125),'Emotions',2,'white')
            if pme.draw_button(((SCREEN.get_size()[0]//2)+190,(SCREEN.get_size()[1]//2)-125),'Close',2,'white','red'):
                DrawEmotions = False
            Pos = [(SCREEN.get_size()[0]//2)-250,(SCREEN.get_size()[1]//2)-100]
            for i,emotion in enumerate(EMOTIONS_SHEET.keys()):
                if i >= 5:
                    Pos[0] = (SCREEN.get_size()[0]//2)-250
                    Pos[1] += 36
                else:
                    Pos[0] += 36
                try:
                    XTip = Tip(f'Emotion: {emotion}', pme,(0,0,0),(216, 211, 192),4)
                    x = SCREEN.blit(pyg.transform.scale(EMOTIONS_SHEET[emotion][0],(32,32)),Pos)
                    EmotionsButtons.append([x,XTip])
                except:
                    pass
            for btn in EmotionsButtons:
                m_pos = pyg.mouse.get_pos()
                if btn[0].collidepoint(m_pos):
                    btn[1].HoveRing(True)
                else:
                    btn[1].HoveRing(False)
                    
            
                
        if op:
            pme.draw_rect((0,0),(150,pme.screen.get_size()[1]),(216, 211, 192,100))
            pme.draw_rect((0,0),(150,pme.screen.get_size()[1]),(166, 161, 142),2)
            pme.draw_text((10,10),'Menu',1,'white')
            DrawEmotions = False
            #if pme.draw_button2((10,80),'Status',2,'white','brown',True):
            if pme.draw_button2((10,80),'Status', 2,[(255,255,255),(166, 161, 142,100),(100,100,100)],True):
                Plr._StatusOpen = True
                return (not op),DrawEmotions
            elif pme.draw_button2((10,135),'Inventory',2,[(255,255,255),(166, 161, 142,100),(100,100,100)],True):
                Plr._InventoryOpen = True
                return (not op),DrawEmotions
        else:
            SY = SCREEN.get_size()[1]
            pme.draw_rect((0,SY-150),(275,150),(216, 211, 192,100))
            pme.draw_rect((0,SY-150),(275,150),(166, 161, 142),2)

            # Health
            pme.draw_bar((24,SY-120),(200,24),Plr.health,Plr.maxhealth,[pme.colors['Maroon'],(200,10,10),(0,0,0)],f'{round(Plr.health)}/{round(Plr.maxhealth)} ({round(Plr.health/Plr.maxhealth*100)}%)',2)
            LFIcon.draw((10,SY-110))
            # Name, Level, Money
            pme.draw_text((24,SY-95),Plr.name[:12],2,'white',antialias=True)
            pme.draw_text((24,SY-65),f'Level: {Plr.Level}',2,'blue',antialias=True)
            pme.draw_text((75+24,SY-65),f'Money: ${Plr.money}',2,'green',antialias=True)

            # Experience
            pme.draw_bar((24,SY-40),(200,24),Plr.Experience,Plr.Level*100,[pme.colors['Maroon'],(153, 229, 80),(0,0,0)],f'{round(Plr.Experience)}/{round(Plr.Level*100)} ({round((Plr.Experience/(Plr.Level*100)*100))}%)',2)
            ExpIcon.draw((10,SY-30))

            pme.draw_text((32,SY-145),f'{W.GetTime(["H","M"])} - {W.GetDate()}',2,'white',antialias=True)
            if SCREEN.blit(EMOTIONS_SHEET['Alert'][0],(10,SY-145)).collidepoint(pyg.mouse.get_pos()):
                EmoBtnTip.HoveRing(True)
                if pyg.mouse.get_pressed(3)[0]:
                    DrawEmotions = not DrawEmotions
                    pyg.time.delay(250)
                else:
                    DrawEmotions = DrawEmotions
            else:
                EmoBtnTip.HoveRing(False)
                DrawEmotions = DrawEmotions
        return op, DrawEmotions
    while run:
        pme.draw_rect((0,0),pme.screen.get_size(),(0,0,0,W.getAlpha()))
        # Gui
        DrawWarns()
        MenuOpen,DrawEmotions = DrawMenu(MenuOpen,DrawEmotions)
        if ShowFPS(0): # Exit by clicking in X on screen
            pyg.time.delay(100)
            run = ex()

        for ev in pme.events():
            if ev.type == MOUSEWHEEL:
                Plr.MouseWheelChange(ev.y)
            else:
                Plr.MouseWheelChange(0)
            if ev.type == QUIT:
                run = ex()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    MenuOpen = not MenuOpen
                elif ev.key in [K_LCTRL,K_RCTRL]:
                    Plr._MOUSE.Active = not Plr._MOUSE.Active
                    print(f'[Game - InGame] {Fore.CYAN}Mouse: {Plr._MOUSE.Active}{Fore.RESET}')
    
        # Update
        PLoader.LoadGameLoop(PLUGINS_HANDLER, globals(), locals())
        Plr.drawUis(BUILD_TILES)
        pme.update()
        cam.update(Plr)
        W.AutoSkipping()

        # Draw
        SCREEN.fill('black')
        cam.draw(Plr)
        # FPS
        CLOCK.tick(CONFIG['FPS'])