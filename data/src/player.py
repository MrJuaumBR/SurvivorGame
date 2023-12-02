from .config import *
from .data.Tiles import *
from .data.Items import *
from .data.enemys import *

import base64
import pickle
import math

TC = TimeConverter(DB)

TranslateCharacter = {
    'Man 1':{'Walk':{'up':[(0,48,16,16),(16,48,16,16),(32,48,16,16),],'down':[(0,0,16,16),(16,0,16,16),(32,0,16,16)],'right':[(0,32,16,16),(16,32,16,16),(32,32,16,16)],'left':[(0,16,16,16),(16,16,16,16),(32,16,16,16)],},'Idle':{'up':[(0,48,16,16)],'down':[(16,0,16,16)],'right':[(16,32,16,16)],'left':[(16,16,16,16)]},
        'Dead':{

        }
    },
    "Guy 1":{"Walk":{"up":[(48,48,16,16),(64,48,16,16),(80,48,16,16)],"down":[(48,0,16,16),(64,0,16,16),(80,0,16,16)],'right':[(48,32,16,16),(64,32,16,16),(80,32,16,16)],'left':[(48,16,16,16),(64,16,16,16),(80,16,16,16)],},"Idle":{"up":[(64,48,16,16),],"down":[(64,0,16,16),],'right':[(64,32,16,16),],'left':[(64,16,16,16),]},
        "Dead":{}
    },
}

TC = TimeConverter(DB)

MouseSprites = spritesheet(f'.{TEXTURES_PATH}/mouse.png')

import pygame as pyg
import math

class _Mouse():
    """
    This class represents the mouse in the game.
    """

    pos = (0,0)
    offset_pos = (0,0)
    camera:Camera = None
    Active = False
    Set_Side = 'right'

    def __init__(self, player) -> None:
        """
        Initializes the _Mouse object.

        Parameters:
        - player: The player object associated with the mouse.
        """
        self.player = player
        self.camera = self.player.Camera
        self.getSpriteDisplay = lambda Active: MouseSprites.image_at((0,0,16,16),0) if Active else MouseSprites.image_at((16,0,16,16),0)
        self.display = pyg.cursors.Cursor((15,5), pyg.transform.scale(self.getSpriteDisplay(self.Active),(24,24)))

    def SideRefactor(self, player_pos, mouse_pos):
        direction = self.camera.convert_offset(mouse_pos) - pyg.math.Vector2(self.camera.convert_offset(player_pos))

        radius, angle = direction.as_polar()

        if angle > -130 or angle > -140:
            side = f'right'
        elif angle < -150 or angle < -135:
            side = f'left'
        else:
            side = f'up'

        return side
        

    def draw(self):
        """
        Draws the mouse on the screen.

        This method is called to draw the mouse on the screen when it is active.
        It checks if the player is not locked or dead before drawing the mouse.
        """
        if self.Active:
            if not (self.player._locked or self.player._dead):
                pme.draw_text((350,SCREEN.get_size()[1]-50),f'Mouse Mode: Pointing, {self.Set_Side}',2,'white',antialias=True)
                self.player.lastSide = self.Set_Side
            self.getSpriteDisplay = lambda Active: MouseSprites.image_at((0,0,16,16),0) if Active else MouseSprites.image_at((16,0,16,16),0)
            self.display = pyg.cursors.Cursor((15,5), pyg.transform.scale(self.getSpriteDisplay(self.Active),(24,24)))

    def update(self):
        """
        Updates the position and appearance of the mouse.

        This method is called to update the position and appearance of the mouse.
        It gets the current mouse position, refactors the side of the mouse, and updates the mouse cursor.
        If an exception occurs during the refactoring process, it prints an error message and sets the camera.
        """
        self.pos = pyg.mouse.get_pos()
        try:
            self.Set_Side = self.SideRefactor(self.player.rect.topleft,self.pos)
            self.display = pyg.cursors.Cursor((15,5), pyg.transform.scale(self.getSpriteDisplay(self.Active),(24,24)))
            pyg.mouse.set_cursor(self.display)
        except Exception as err:
            print(f'[Mouse - Player] {Fore.RED}Mouse Side Cant Refactor for now.{Fore.RESET}')
            print(f'\n\n{Fore.RED}{err}{Fore.RESET}')
            self.camera = self.player.Camera

class _Slash(pyg.sprite.Sprite):
    image = None
    files = LoadSlashAnimation()
    waitTime = 0
    style = 0
    BaseDamage = 12

    Attacking = False

    Animation_Frame = 0
    
    HitRep = 1
    def __init__(self, player) -> None:
        super().__init__()
        self.player:player = player
        self.rect:Rect = Rect(0,0,64,64)
        self.offset = pyg.math.Vector2(0,0)
        
    def input(self):
        if pyg.mouse.get_pressed(3)[0]:
            if self.waitTime <= 0:
                self.waitTime = TC.getTime(1)
                self.HitRep = 1
                self.Attacking = True
                
    def fliper(self):
        lastSide = self.player.lastSide
        imgs = self.files[self.style]
        new = []
        if lastSide == 'right':
            new = imgs
            self.offset.x = 16
            self.offset.y = 0
        elif lastSide == 'left':
            for item in imgs:
                new.append(pyg.transform.flip(item,True,False))
            self.offset.x = -16
            self.offset.y = 0
        elif lastSide == 'up':
            for item in imgs:
                new.append(pyg.transform.rotate(item,180))
            self.offset.y = -16
            self.offset.x = 0
        elif lastSide == 'down':
            for item in imgs:
                new.append(pyg.transform.rotate(item,90))
            self.offset.y = 16
            self.offset.x = 0
        return new
    def draw(self, surf:pyg.Surface):
        if self.Attacking:
            images = self.fliper()
            if self.Animation_Frame >= len(images):
                self.Animation_Frame = 0
                self.Attacking = False
                self.image = None
                self.HitRep = 1
            self.image = images[int(self.Animation_Frame)]
            self.Animation_Frame += .25
            try:
                pos = self.player.rect.topleft
                pos = [pos[0],pos[1]]
                # pos[0] += self.offset.x
                # pos[1] += self.offset.y
                self.hit(pos)
                self.player.Camera.draw_in(self.image, pos, surf)
            except Exception as err:
                print(f'{Fore.RED}[Slash - Draw] {err}{Fore.RESET}')
    
    def CalculateDamage(self):
        x = self.BaseDamage + (1+(self.player.attack*.6))
        return x

    def hit(self,pos):
        if self.Attacking:
            re_rect = Rect(0,0,48,48)
            re_rect.topleft = self.rect
            collides:list = self.player.Camera.sprites_collide(re_rect)
            if self.HitRep >= 1:
                print(f'{Fore.YELLOW}[Slash - Hit] Player Attacking{Fore.RESET}')
                print(f'\t{Fore.LIGHTYELLOW_EX}[Slash - Hit] Collides: {collides} {Fore.RESET}')
                print(f'\t{Fore.LIGHTYELLOW_EX}[Slash - Hit] Hit Repeater: {self.HitRep} {Fore.RESET}')
                if len(collides) > 0:
                    for enu in collides:
                        if enu._type != 'player':
                            if enu._type == 'enemy':  
                                dmg = self.CalculateDamage()
                                print(f'{Fore.LIGHTGREEN_EX}[Slash - Hit] Player give {dmg} to {enu._name}{Fore.RESET}')
                                enu.takeDamage(dmg)
            self.HitRep = 0
        else:
            pass
            

    def update(self):
        if not self.player._locked:
            if self.waitTime > 0:
                self.waitTime -= 1
            self.input()
            self.rect = self.player.rect.center

class player(pyg.sprite.Sprite):
    _layer = 5
    saveable = ['name','health','maxhealth','speed','LastExperience','W','Items','pos','_locked','_dead', 'Color','Level','Experience','points','attack','luck','defense','agility','inteligence']

    # GUIs
    MouseWheel = 0
    _StatusOpen = False
    _InventoryOpen = False
        # Inventory
    Inv_Scrollarea_Rect = Rect(64,75,SCREEN.get_size()[0]-128,SCREEN.get_size()[1]-295)
    Inv_Y_Shift = Inv_Scrollarea_Rect.top + (64//2)
        # Build
    _BuildOpen = False
    _BuildPage = 1
    _BuildXSHIFT = 90

    W = {}

    _type = 'player'

    # Waiters
    _Wait_time_levelUpSong = TC.getTime(1)
    C_Wait_time_levelUpSong = 0

    # Others
    _MOUSE:_Mouse = None
    Camera:Camera = None
    def __init__(self, XY=(0,0),*groups) -> None:
        super().__init__(*groups)
        self.name = ""
        self.pos = XY
        self.size = (32,32)

        # Animation
        self.curr = 'Idle'
        self.lastSide = 'right'
        self.anim_frame = 0
        self.Color = 'Man 1'
        self.animations = {'Walk':{'up':[],'left':[],'right':[],'down':[]},'Idle':{'up':[],'left':[],'right':[],'down':[]},'Dead':{'up':[],'left':[],'right':[],'down':[]}}
        self.animationsBuild()

        self.Slash = _Slash(self)

        self.rect = Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.image = self.animations[self.curr][self.lastSide][int(self.anim_frame)]

        # Inventory
        self.Items = {
            'inventory':[],
            'handbar':[]
        }
        self.Items['inventory'] = [ItemBase((0,0))]
        self.Items['handbar'] = []

        # Status
            # State
        self._locked = False
        self._dead = False

            # Health
        self.maxhealth = 100
        self.health = self.maxhealth
        self.heal_cooldown = 0

            # Movement
        self.move = pyg.math.Vector2(0,0)
        self.speed = 5

            # Level
        self.Level = 1
        self.Experience = 0
        self.LastExperience = self.Experience
            # Money
        self.money = 100
            # Warns
        self.warns = []
        self.ClearAll = 0

            # Status
        self.attack = 1 # Damage
        self.agility = 1 # Speed
        self.defense = 1 # Health
        self.inteligence = 1 # Magic Damage
        self.luck = 1 # Luck(Drops, Exp and Critical)
        self.points = 3
            # Others
        self.damage = 5
            # Mouse
        self._MOUSE = _Mouse(self)
    def animationsBuild(self):
        self.animations = {'Walk':{'up':[],'left':[],'right':[],'down':[]},'Idle':{'up':[],'left':[],'right':[],'down':[]},'Dead':{'up':[],'left':[],'right':[],'down':[]}}
        s = spritesheet("."+PLAYERS_SPRITESHEET)
        t = TranslateCharacter[self.Color]
        for state in t.keys():
            for frame in t[state].keys():
                for f in t[state][frame]:
                    img = s.image_at(f,0)
                    index = t[state][frame].index(f)
                    self.animations[state][frame].insert(index,img)
    def animate(self):
        if not self._dead:
            if self.move.x != 0:
                self.curr = 'Walk'
            elif self.move.y != 0:
                self.curr = 'Walk'
            else:
                self.curr = 'Idle'
            self.anim_frame += 0.15
            if self.anim_frame >= len(self.animations[self.curr][self.lastSide]):
                self.anim_frame = 0
            self.image = self.animations[self.curr][self.lastSide][int(self.anim_frame)]
            self.image = pyg.transform.scale(self.image, self.size)
        else:
            self.curr = "Dead"

    def checkWarn(self):
        if len(self.warns) > 0:
            if self.ClearAll <= 0:
                self.ClearAll = 0
                self.warns = []
            else:
                self.ClearAll -= 1
                
    def addWarn(self, warn:str, color:tuple or str):
        self.ClearAll = TC.getTime(3.5)
        self.warns.insert(0,[warn,color])
        if len(self.warns) > 5:
            del self.warns[-1]

    def checklevel(self):
        self.statusRefactor()
        if self.Experience >= 100*self.Level:
            self.Experience -= 100*self.Level
            self.Level += 1
            self.points += 3
            self.addWarn(f'Level up to: {self.Level}','Green')
            if self.C_Wait_time_levelUpSong <= 0:
                s= pyg.mixer.Sound(TRACKS['level-up'])
                s.set_volume(CONFIG['VOLUME']/100)
                s.play()
                C_Wait_time_levelUpSong=self._Wait_time_levelUpSong
        if self.Experience > self.LastExperience:
            self.addWarn(f'Got {self.Experience-self.LastExperience} Exp','Green')
            self.LastExperience = self.Experience

    def takeDamage(self, damage:float):
        if not self._dead:
            self.health -= damage
            self.heal_cooldown += TC.getTime(1)
            if self.health <= 0:
                self._dead = True

    def heal(self, quantity:float):
        if not self._dead:
            self.health += quantity
            if self.health >= self.maxhealth:
                self.health = self.maxhealth

    def recoverHealth(self, recover_per:float=0.05):
        if not self._dead:
            if self.heal_cooldown <= 0:
                self.health += self.maxhealth*recover_per
                self.heal_cooldown = TC.getTime(0.05)
                if self.health >= self.maxhealth:
                    self.health = self.maxhealth
                    self.heal_cooldown = TC.getTime(6)
            else:
                self.heal_cooldown -= 1
            if self.heal_cooldown < 0:
                self.heal_cooldown = 0

    def Input(self):
        if not self._locked:
            if (pme.while_key_hold(K_w) or pme.while_key_hold(K_UP)):
                self.move.y = -1
            elif (pme.while_key_hold(K_s) or pme.while_key_hold(K_DOWN)):
                self.move.y = 1
            else:
                self.move.y = 0
            if (pme.while_key_hold(K_d) or pme.while_key_hold(K_RIGHT)):
                self.move.x = 1
            elif (pme.while_key_hold(K_a) or pme.while_key_hold(K_LEFT)):
                self.move.x =-1
            else:
                self.move.x = 0
            if pme.while_key_hold(K_b):
                self._BuildOpen = not self._BuildOpen
                pyg.time.delay(100)

    def ConvertMove(self):
        if not self._MOUSE.Active:
            if self.move.x != 0:
                if self.move.x > 0:
                    self.lastSide = 'right'
                elif self.move.x < 0:
                    self.lastSide = 'left'
                else:
                    self.lastSide = self.lastSide
            else:
                if self.move.y > 0:
                    self.lastSide = 'down'
                elif self.move.y < 0:
                    self.lastSide = 'up'
                else:
                    self.lastSide = self.lastSide

    def movement(self):
        if not self._locked:
            self.ConvertMove()
            self.rect.x += self.move.x * self.speed
            self.rect.y += self.move.y * self.speed

            # self.move.x *= 0.25
            # self.move.y *= 0.25
            # if self.move.x < 0.25:
            #     self.move.x = 0
            # if self.move.y < 0.25:
            #     self.move.y = 0
        if self._dead:
            self._locked = True
        else:
            self._locked = False

    def draw_ui(self, camera):
        convert_offset = camera.convert_offset((self.rect.centerx,self.rect.bottom))
        if self.health < self.maxhealth:
            pme.draw_bar((convert_offset[0]-16,convert_offset[1]+18),(32,15),self.health,self.maxhealth,text=f'{round(self.health)}/{round(self.maxhealth)}', textfont=5)
        pme.draw_text([convert_offset[0]-16,convert_offset[1]+6],str(self.name[10:]),5,(255,255,255))        
        # self.Slash.draw()

    def statusRefactor(self):
        if not self._dead:
            if not (self.maxhealth == (100 + self.defense * 0.8)):
                self.maxhealth = 100 + self.defense * 0.8
            if not (self.damage == (5 + self.attack * 0.8)):
                self.damage = (5+self.attack*0.8)
            if not (self.speed == (5 + self.agility * 0.1)):
                self.speed = 5 + self.agility * 0.1
                if self.speed > 15:
                    self.speed = 15

    def WaitingManager(self):
        if self.C_Wait_time_levelUpSong > 0:
            self.C_Wait_time_levelUpSong -= 1

    def update(self) -> None:
        self.Input()
        self.movement()
        self.recoverHealth()
        self.animate()
        self.checklevel()
        self.checkWarn()
        self._MOUSE.update()
        self.Slash.update()
         
        return super().update()
    
    # UIs
    def DetectScroll(self,collision:Rect):
        if collision:
            MouseChange = pyg.mouse.get_rel()[1]
            if MouseChange > 0:
                MouseChange = 1
            elif MouseChange < 0:
                MouseChange = -1
            else:
                MouseChange = 0
            if not pyg.mouse.get_pressed()[0]:
                MouseChange = 0
            if collision.collidepoint(pyg.mouse.get_pos()):
                self.MouseWheelChange(MouseChange)

    def drawUis(self,BUILD_TILES:dict):
        self._MOUSE.draw()
        self.draw_status(self._StatusOpen)
        self.draw_build(self._BuildOpen,BUILD_TILES)
        self.draw_inventory(self._InventoryOpen)

    def draw_status(self, state:bool):
        if state:
            # Background
            pme.draw_rect((75,75),(pme.screen.get_size()[0]-(75*2),pme.screen.get_size()[1]-(75*2)),(216, 211, 192, 100))

            # Title
            pme.draw_text((80,80),'Status',1,'white',antialias=True)

            # Close
            if pme.draw_button((pme.screen.get_size()[0]-(75*2),80),'Close',1,'white','red',True):
                self._StatusOpen = False

            # Tips
            AtkTip = Tip('Attack: Give More Damage',pme, (0,0,0), (216, 211, 192), 4)
            DefTip = Tip('Defense: Give More Life, Resistance',pme, (0,0,0), (216, 211, 192), 4)
            AgiTip = Tip('Agility: Give More Attack Speed, Moviment Speed',pme, (0,0,0), (216, 211, 192), 4)
            LckTip = Tip('Luck: Give better rewards, More Chance to Critical',pme, (0,0,0), (216, 211, 192), 4)
            IntTip = Tip('Inteligence: Give more money, more experience',pme, (0,0,0), (216, 211, 192), 4)

            # Status
                # Attack
            pme.draw_text((85,150),f'Attack: {self.attack}',1,'white',antialias=True)
            if pme.draw_button((300,150),'+',1,'white','green',True,AtkTip):
                self.points -= 1
                self.attack += 1
                pyg.time.delay(50)
                # Defense
            pme.draw_text((85,200),f'Defense: {self.defense}',1,'white',antialias=True)
            if pme.draw_button((300,200),'+',1,'white','green',True,DefTip):
                self.points -= 1
                self.defense += 1
                pyg.time.delay(50)
                # Agility
            pme.draw_text((85,250),f'Agility: {self.agility}',1,'white',antialias=True)
            if pme.draw_button((300,250),'+',1,'white','green',True,AgiTip):
                self.points -= 1
                self.agility += 1
                pyg.time.delay(50)
                # Luck
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))-105,150),f'Luck: {self.luck}',1,'white',antialias=True)
            if pme.draw_button(((pme.screen.get_size()[0]-(75*2))-125,150),'+',1,'white','green',True,LckTip):
                self.points -= 1
                self.luck += 1
                pyg.time.delay(50)
                # Inteligence
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))-105,200),f'Inteligence: {self.inteligence}',1,'white',antialias=True)
            if pme.draw_button(((pme.screen.get_size()[0]-(75*2))-125,200),'+',1,'white','green',True,IntTip):
                self.points -= 1
                self.inteligence += 1
                pyg.time.delay(50)
                # Points
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))//2,(pme.screen.get_size()[1]-(75*2))),f'Points: {self.points}',1,'white',antialias=True)

    def MouseWheelChange(self, Change):
        self.MouseWheel = Change

    def draw_inventory(self, state:bool):
        if state:
            # Background
            pme.draw_rect((45,45),(pme.screen.get_size()[0]-(45*2),pme.screen.get_size()[1]-(45*2)),(216, 211, 192, 100))

            # Scrolling Frame
            def Draw_Scroll():
                btns = []
                pme.draw_rect(self.Inv_Scrollarea_Rect.topleft,self.Inv_Scrollarea_Rect.size,(200,170,100,50))
                pme.draw_rect(self.Inv_Scrollarea_Rect.topleft,self.Inv_Scrollarea_Rect.size,(200,200,200),2)
                BARY = self.Inv_Y_Shift
                if self.Inv_Y_Shift < self.Inv_Scrollarea_Rect.top:
                    BARY = self.Inv_Scrollarea_Rect.top
                elif self.Inv_Y_Shift+(self.Inv_Scrollarea_Rect.size[1]//len(self.Items['inventory'])) >= self.Inv_Scrollarea_Rect.bottom:
                    BARY = self.Inv_Scrollarea_Rect.bottom - (self.Inv_Scrollarea_Rect.size[1]//len(self.Items['inventory']))

                Scroll_button_rect = Rect(self.Inv_Scrollarea_Rect.right+5,BARY,10,self.Inv_Scrollarea_Rect.size[1]//len(self.Items['inventory']))
                pme.draw_rect(Scroll_button_rect.topleft,Scroll_button_rect.size,(90,90,90))
                RangePL = 0
                for x,item in enumerate(self.Items['inventory']):
                    if x <= 0:
                        id = 1
                    X,Y = (64+32,self.Inv_Y_Shift+(id*35))
                    if RangePL >= 9:
                        if id % 2 == 0:
                            X,Y = (X,Y-25)
                        else:
                            X,Y = (X,Y+25)
                        RangePL = 0
                    else:
                        RangePL += 1
                    
                    if Y < self.Inv_Scrollarea_Rect.top:
                        pass
                    elif Y > self.Inv_Scrollarea_Rect.bottom:
                        pass
                    else:
                        pme.draw_rect((X,Y), (64,64),(200,195,100,50))

                # Input
                self.DetectScroll(Scroll_button_rect)
                M_Pos = pyg.mouse.get_pos()
                if (self.Inv_Scrollarea_Rect.collidepoint(M_Pos) or Scroll_button_rect.collidepoint(M_Pos)):
                    if self.MouseWheel != 0:
                        self.Inv_Y_Shift += 5 * self.MouseWheel
                        self.MouseWheel * 0.2

            Draw_Scroll()
            # Title
            pme.draw_text((50,50),'Inventory',1,'white',antialias=True)

            # Close
            if pme.draw_button((pme.screen.get_size()[0]-(75*2),50),'Close',1,'white','red',True):
                self._InventoryOpen = False


    def draw_build(self, state:bool,BUILD_TILES:dict):
        if state:
            # Background
            pme.draw_rect((10,(pme.screen.get_size()[1]//4)*3),(pme.screen.get_size()[0]-20,pme.screen.get_size()[1]//4),(0,0,0,100))

            # Title
            pme.draw_text((15,(pme.screen.get_size()[1]//4)*3),'Build',1,'white',antialias=True)

            # Build Tiles
            for i in range(0,self._BuildPage*9):
                try:
                    if len(BUILD_TILES) >= i+1:
                        if BUILD_TILES[str(i)] and callable(BUILD_TILES[str(i)]):
                            id = (1 if i <= 0 else i)
                            X = (id * 90) + self._BuildXSHIFT
                            Y = ((pme.screen.get_size()[1]//4)*3)+130
                            if id % 2 == 0:
                                X -= (90//4)*2
                            else:
                                X += (90//3)*2
                            if X >= pme.screen.get_size()[0]-100:
                                pass
                            elif X < 10:
                                pass
                            else:
                                pme.screen.blit(pyg.transform.scale(BUILD_TILES[str(i)]((0,0)).image,(90,90)),(X,Y-130))
                                pme.draw_text((X,Y),f'{BUILD_TILES[str(i)].name}',4,'white',antialias=True)
                except:
                    raise(Exception('Tile not found'))
            
            # Bar
            BAR_WD = (pme.screen.get_size()[0]-40)//len(BUILD_TILES)
            if pme.draw_rect((self._BuildXSHIFT,((pme.screen.get_size()[1]//4)*3)+100),(BAR_WD,10),(100,100,100)).collidepoint(pyg.mouse.get_pos()):
                if pyg.mouse.get_pressed(3)[0]:
                    x = self._BuildXSHIFT + pyg.mouse.get_rel()[0]
                    if not ((x < 10) or (x > ((pme.screen.get_size()[0]-10)-BAR_WD))):
                        self._BuildXSHIFT = x

    # Save
    def SaveInventory(self):
        i = {}
        for key in self.Items.keys():
            i[key] = []
            for item in self.Items[key]:
                dic = item.__dict__
                ndic = {}
                for s in item.saveable:
                    ndic[s] = dic[s]
                i[key].append(ndic)
        return i
    def Save(self,camera) -> bytes:
        self.pos = self.rect.topleft
        self.size = self.rect.size
        s = {}
        for item in self.saveable:
            if item == 'Items':
                inv = self.SaveInventory()
                s['Items'] = inv
            else:
                s[item] = self.__dict__[item]
        if camera:
            s['sprites']:list = camera.saving()
            try:
                s['sprites'].remove(self)
            except:
                pass
        return base64.b64encode(pickle.dumps(s))
    # Load
    def LoadInventory(self,ddata:dict):
        for key in ddata['Items'].keys():
            for item in ddata['Items'][key]:
                i = ITEMS[item['_RealName']]((0,0))
                for s in i.saveable:
                    i.__dict__[s] = item[s]
                self.Items[key].append(i)
    def Load(self, data:bytes):
        s = {}
        ddata:dict = pickle.loads(base64.b64decode(data))
        for item in self.saveable:
            if item == 'Items':
                self.LoadInventory(ddata)
            else:
                self.__dict__[item] = ddata[item]
        self.rect.topleft = self.pos

        # Update Things
        self.animationsBuild()