from .config import *
from .game import game, player
from .player import Animation_Y_Colors

def createSave() -> bool:
    run = True
    CharName = ''
    TX_BOX = False
    color_ind = 0
    Colors = []
    for key in Animation_Y_Colors.keys():
        Colors.append(key)
    while run:
        # Draw Components
        pme.draw_text((25,50),'Character Name: ', 2, 'black')
        TX_BOX, CharName = pme.draw_textbox((30,80),1,['white',pme.colors['salmon'],pme.colors['orangered']],TX_BOX,CharName,25,[K_SPACE])

        pme.draw_text((25,125),'Character Color:', 2, 'black')
        color_ind = pme.draw_select((90,165),Colors,color_ind, 1, ((255,255,255),Colors[color_ind]))

        if pme.draw_button((25,SCREEN.get_size()[1]-100),'SAVE',2,'white','green'):
            if len(CharName) >= 5 and len(CharName) <= 25:
                plr = player()
                plr.name = CharName
                plr.Color = Colors[color_ind]
                x = plr.Save()
                DB.database.add_value('saves','data',value=x)
                DB.save()
                run = False
                return True

        # Events
        for ev in pme.events():
            if ev.type == QUIT:
                run = False
                return False

        # Draw Needed UI
        pme.draw_text((15,0),"Create Save",3,'black',antialias=True) # Title
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR) # Bar
        if ShowFPS(0): # Exit by clicking in X on screen
            run = False
            return False

        pme.update()
        pme.screen.fill('white') # Fill SCreen
        CLOCK.tick(CONFIG['FPS'])

def LoadSaveScreen():
    run = True
    saves = DB.database.get_all('saves')
    selected = {'name':"",'data':{},'id':0}
    def drawSaves(saves):
        # Draw Saves
        pos = [50,75]
        btns = []
        for id,save in enumerate(saves):
            REAL_POS = [pos[0],pos[1]]
            if id+1 % 2 == 0:
                REAL_POS[0] = pos[0] - (id * 45)
            else:
                REAL_POS[0] = pos[0] + (id * 45)
            plr = player()
            plr.Load(save['data'])
            Name = lambda plr: plr.name[:10] if len(plr.name) > 10 else plr.name
            pme.draw_rect(REAL_POS,(100,80),(50,100,200))
            pme.draw_text((REAL_POS[0]+10,REAL_POS[1]+10),Name(plr),2,'black',antialias=True)
            # Buttons
            sel = pme.draw_button((REAL_POS[0]+5,REAL_POS[1]+55),'Select',4,'white','green')
            dell = pme.draw_button((REAL_POS[0]+70,REAL_POS[1]+55),'Delete',4,'white','red',True)
            btns.append((sel, dell, {'id':id,'data':save['data']}))
            pos[0] += 70
            if pos[0] >= SCREEN.get_size()[0]-50:
                pos[0] = 50
                pos[1] += 75

        for button in btns:
            if True in button:
                if button[0]:
                    
                    plr = player()
                    plr.Load(button[2]['data'])
                    selected['name'] = plr.name
                    selected['data'] = button[2]['data']
                    selected['id'] = button[2]['id']
                elif button[1]:
                    try:
                        DB.database.delete_values('saves',id=button[2]['id'])
                        DB.save()
                    except:
                        print("error occured...")
    while run:
        for ev in pme.events():
            if ev.type == QUIT:
                run = False
                    
        drawSaves(DB.database.get_all('saves'))
        # Draw Buttons
        if pme.draw_button((25,SCREEN.get_size()[1]-75),'Create',2,'white','green'):
            if createSave():
                saves = DB.database.get_all('saves')
        if pme.draw_button((100, SCREEN.get_size()[1]-75),f'Load: {selected["name"][:12]}',2,'white','green'):
            if not (selected['name'] in [" ","",None, "None"]):
                game(selected['id'])


        # Draw Needed UI
        pme.draw_text((15,0),"Load Save",3,'black',antialias=True) # Title
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR) # Bar
        PLoader.LoadSaveScreenLoop(PLUGINS_HANDLER)
        if ShowFPS(0): # Exit by clicking in X on screen
            pyg.time.delay(100)
            run = False

        pme.update()
        pme.screen.fill('white') # Fill SCreen
        CLOCK.tick(CONFIG['FPS'])
        
def options():
    run = True

    VOL_VALUE = CONFIG['VOLUME']
    VOL_X = (VOL_VALUE/100)*(25+SCREEN.get_size()[0]-100)

    SCR_VALUE = CONFIG["FULLSCREEN"]
    SHOWFPS_VALUE = CONFIG["SHOWFPS"]
    def exitM():
        CONFIG['VOLUME'] = VOL_VALUE
        CONFIG['FULLSCREEN'] = SCR_VALUE
        CONFIG["SHOWFPS"] = SHOWFPS_VALUE

        DB.database.update_value('config','data',0,CONFIG)
        DB.save()
        pyg.time.delay(100)
        return False
    while run:
        for ev in pme.events():
            if ev.type == QUIT:
                run = exitM()

        # Draw Components
        VOL_X, VOL_VALUE = pme.draw_slider((25,80),SCREEN.get_size()[0]-100,VOL_X)
        VOL_VALUE = 100*VOL_VALUE
        pme.draw_text((20,50),f'Volume: {int(VOL_VALUE)}',2,'black')

        SCR_VALUE = pme.draw_switch((25,135),2,SCR_VALUE)
        pme.draw_text((25,110),'Fullscreen: ',2,'black')

        SHOWFPS_VALUE = pme.draw_switch((25,190),2,SHOWFPS_VALUE)
        pme.draw_text((25,170),'Show FPS: ',2,'black')

        if pme.draw_button((25,SCREEN.get_size()[1]-50),'Mods/Plugins',2,'black', 'blue'):
            ModsPlugins()

        # Draw Needed UI
        pme.draw_text((15,0),"Options",3,'black',antialias=True) # Title
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR) # Bar
        PLoader.LoadOptionsLoop(PLUGINS_HANDLER)
        if ShowFPS(0): # Exit by clicking in X on screen
            run = exitM()
            
        
        
        pme.update()
        pme.screen.fill('white') # Fill SCreen
        CLOCK.tick(CONFIG['FPS'])

def ModsPlugins():
    run = True
    def exitM():
        pyg.time.delay(100)
        return False
    Y_Shift = 90
    Scrollarea_Rect = Rect(30,55,SCREEN.get_size()[0]-100,SCREEN.get_size()[1]-75)
    def LoadPlugins():
        btns = []
        pme.draw_rect(Scrollarea_Rect.topleft,Scrollarea_Rect.size,(50,50,50))
        BARY = Y_Shift
        if Y_Shift < Scrollarea_Rect.top:
            BARY = Scrollarea_Rect.top
        elif Y_Shift+(Scrollarea_Rect.size[1]//len(PLoader.RejectMetadata(PLUGINS_HANDLER))) >= Scrollarea_Rect.bottom:
            BARY = Scrollarea_Rect.bottom - (Scrollarea_Rect.size[1]//len(PLoader.RejectMetadata(PLUGINS_HANDLER)))
        pme.draw_rect((Scrollarea_Rect.right+5,BARY),(10,Scrollarea_Rect.size[1]//len(PLoader.RejectMetadata(PLUGINS_HANDLER))),(90,90,90))
        for i,pluginName in enumerate(PLoader.RejectMetadata(PLUGINS_HANDLER)):
            plugin = PLUGINS_HANDLER[pluginName]
            plg = DB.database.findByText('plugins','pluginName',pluginName)
            plugin.Enabled = plg['pluginState']
            if i <= 0:
                id = 1
            XY = (60,Y_Shift+(id*75))
            if id % 2 == 0:
                XY = (XY[0],XY[1]-25)
            else:
                XY = (XY[0],XY[1]+25)
            if XY[1] <= 55:
                pass
            elif XY[1] >= SCREEN.get_size()[1]-75:
                pass
            else:
                pme.draw_rect((XY[0],XY[1]),(pme.screen.get_size()[0]-160,120),(50,100,200))
                pme.draw_text(XY,f"{i} - {pluginName[:32]}",1, (255,255,255),antialias=True)
                pme.draw_text((XY[0],XY[1]+50),f"{plugin.Description[:65]}",4, (255,255,255),antialias=True)
                deleteBtn = pme.draw_button((pme.screen.get_size()[0]-160,XY[1]+100),"Delete",2,'white','red',True)
                authorBtn = pme.draw_button((XY[0]+5,XY[1]+30),f"By: {plugin.Author[:32]}",2,'white')

                Enabled = lambda state: "Enabled" if state else "Disabled"
                EnabledColor = lambda state: (0,255,0) if state else (255,0,0)
                enableBtn = pme.draw_button((pme.screen.get_size()[0]-225,XY[1]+100),Enabled(plugin.Enabled),2,(255,255,255),EnabledColor(plugin.Enabled),waitMouseUp=True)

                if plugin.Icon != '':
                    SCREEN.blit(pyg.transform.scale(pyg.image.load(f'{plugin.AssetsFolder}/{plugin.Name.replace(" ", "")}/{plugin.Icon}'),(72,72)),(pme.screen.get_size()[0]-(160+72),XY[1]+30))
                btns.append((pluginName, deleteBtn,authorBtn, enableBtn))
        for data in btns:
            delete = data[1]
            if delete:
                Plg = DB.database.findByText('plugins','pluginName',data[0])
                PLoader.DeletePlugin(data[0])
                PLUGINS_HANDLER.pop(data[0])
                PLUGINS_HANDLER.pop(data[0]+"_metadata") # Delete MetaData
                DB.database.delete_values('plugins',Plg['id'])
            elif data[2]: # Redirect to author url
                webbrowser.open(PLUGINS_HANDLER[pluginName].AuthorUrl)
            elif data[3]: # Enable or disable
                PLUGINS_HANDLER[data[0]].Enabled = not PLUGINS_HANDLER[data[0]].Enabled
                Plg = DB.database.findByText('plugins','pluginName',data[0])
                DB.database.update_value('plugins','pluginState',Plg['id'],PLUGINS_HANDLER[data[0]].Enabled)
                DB.save()
                pyg.time.delay(100)
    while run:
        for ev in pme.events():
            if ev.type == QUIT:
                run = exitM()
            elif ev.type == MOUSEWHEEL:
                if Scrollarea_Rect.collidepoint(pyg.mouse.get_pos()):
                    Y_Shift += (-ev.y) * 25
                        
        
        # REsponse
        LoadPlugins()
        if pme.draw_button((25,50),'Load Plugins', 2, (255,255,255),'green'):
            print('Load Plugins')
            for pluginName in PLoader.RejectMetadata(PLUGINS_HANDLER):
                plugin = PLUGINS_HANDLER[pluginName]
                d = lambda state,plugin: f"Can be dangerous\nList of require: {plugin.required}" if state else ""
                print(f"""
                    Name: {plugin.Name}
                    Description: {plugin.Description}
                    Version: {plugin.Version}
                    Require Download: {plugin.RequireDownload}
                    {d(plugin.RequireDownload,plugin)}

                    For Game Version: {plugin.GameVersion}
                """)
            pyg.time.delay(100)

        #

        pme.draw_text((15,0),"Mods/Plugins",3,'black',antialias=True) # Title
        pme.draw_rect((0,0),(10,pme.screen.get_size()[1]),RND_COLOR) # Bar
        if ShowFPS(0): # Exit by clicking in X on screen
            run = exitM()

        pme.update()
        pme.screen.fill('white') # Fill SCreen
        CLOCK.tick(CONFIG['FPS'])