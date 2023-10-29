from .config import *
from .data.items import *
import base64
import pickle

TC = TimeConverter(DB)

Animation_Y_Colors = {
    'Green':0,
    'Red':32,
    'Blue':64,
    'Yellow':96,
    'Purple':128
}

class player(pyg.sprite.Sprite):
    _layer = 1
    saveable = ['name','health','maxhealth','speed','pos','_locked','_dead', 'Color','Level','Experience','points','attack','luck','defense','agility','inteligence']

    # GUIs
    _StatusOpen = False
        # Build
    _BuildOpen = False
    _BuildPage = 1
    _BuildXSHIFT = 90


    _type = 'player'
    def __init__(self, XY=(0,0),*groups) -> None:
        super().__init__(*groups)
        self.name = ""
        self.pos = XY
        self.size = (32,32)

        # Animation
        self.curr = 'Idle'
        self.lastSide = 'Right'
        self.anim_frame = 0
        self.Color = 'Green'
        self.animationsBuild()

        self.rect = Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.image = self.animations[self.curr][int(self.anim_frame)]
        if self.lastSide != 'Right':
            pyg.transform.flip(self.image,True,False)

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
    def animationsBuild(self):
        self.animations = {'Idle':[],'Walk':[],'Dead':[]}
        s = spritesheet("."+TEXTURES_PATH+'/players.png')
        self.animations['Walk'] = s.images_at([
            (1,Animation_Y_Colors[self.Color]+1,31,31),
            (33,Animation_Y_Colors[self.Color]+1,31,31)
        ],0)
        self.animations['Dead'] = s.images_at([
            (65, Animation_Y_Colors[self.Color]+1,31,31),
            (97, Animation_Y_Colors[self.Color]+1,31,31)
        ],0)
        self.animations['Idle'] = s.images_at([
            (129,Animation_Y_Colors[self.Color]+1,31,31),
            (161,Animation_Y_Colors[self.Color]+1,31,31)
        ],0)

    def animate(self):
        if not self._dead:
            if self.move.x != 0:
                self.curr = 'Walk'
                self.lastSide = 'Right' if self.move.x > 0 else 'Left'
            elif self.move.y != 0:
                self.curr = 'Walk'
                self.lastSide = 'Right' if self.move.y > 0 else 'Left'
            else:
                self.curr = 'Idle'
            self.anim_frame += 0.15
            if self.anim_frame >= len(self.animations[self.curr]):
                self.anim_frame = 0
            self.image = self.animations[self.curr][int(self.anim_frame)]
            if self.lastSide != 'Right':
                self.image = pyg.transform.flip(self.image,True,False)
                pass
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

    def movement(self):
        if not self._locked:
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

    def update(self) -> None:
        self.Input()
        self.movement()
        self.recoverHealth()
        self.animate()
        self.checklevel()
        self.checkWarn()
        return super().update()
    
    # UIs
    def drawUis(self,BUILD_TILES:dict):
        self.draw_status(self._StatusOpen)
        self.draw_build(self._BuildOpen,BUILD_TILES)

    def draw_status(self, state:bool):
        if state:
            # Background
            pme.draw_rect((75,75),(pme.screen.get_size()[0]-(75*2),pme.screen.get_size()[1]-(75*2)),(0,0,0,100))

            # Title
            pme.draw_text((80,80),'Status',1,'white',antialias=True)

            # Close
            if pme.draw_button((pme.screen.get_size()[0]-(75*2),80),'Close',1,'white','red',True):
                self._StatusOpen = False

            # Status
                # Attack
            pme.draw_text((85,150),f'Attack: {self.attack}',1,'white',antialias=True)
            if pme.draw_button((300,150),'+',1,'white','green',True):
                self.points -= 1
                self.attack += 1
                pyg.time.delay(50)
                # Defense
            pme.draw_text((85,200),f'Defense: {self.defense}',1,'white',antialias=True)
            if pme.draw_button((300,200),'+',1,'white','green',True):
                self.points -= 1
                self.defense += 1
                pyg.time.delay(50)
                # Agility
            pme.draw_text((85,250),f'Agility: {self.agility}',1,'white',antialias=True)
            if pme.draw_button((300,250),'+',1,'white','green',True):
                self.points -= 1
                self.agility += 1
                pyg.time.delay(50)
                # Luck
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))-105,150),f'Luck: {self.luck}',1,'white',antialias=True)
            if pme.draw_button(((pme.screen.get_size()[0]-(75*2))-125,150),'+',1,'white','green',True):
                self.points -= 1
                self.luck += 1
                pyg.time.delay(50)
                # Inteligence
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))-105,200),f'Inteligence: {self.inteligence}',1,'white',antialias=True)
            if pme.draw_button(((pme.screen.get_size()[0]-(75*2))-125,200),'+',1,'white','green',True):
                self.points -= 1
                self.inteligence += 1
                pyg.time.delay(50)
                # Points
            pme.draw_text(((pme.screen.get_size()[0]-(75*2))//2,(pme.screen.get_size()[1]-(75*2))),f'Points: {self.points}',1,'white',antialias=True)

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
    def Save(self,camera) -> bytes:
        self.pos = self.rect.topleft
        self.size = self.rect.size
        s = {}
        for item in self.saveable:
            s[item] = self.__dict__[item]
        s['sprites']:list = camera.saving()
        try:
            s['sprites'].remove(self)
        except:
            pass
        return base64.b64encode(pickle.dumps(s))
    
    def Load(self, data:bytes):
        s = {}
        ddata:dict = pickle.loads(base64.b64decode(data))
        for item in self.saveable:
            self.__dict__[item] = ddata[item]
        self.rect.topleft = self.pos