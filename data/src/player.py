from .config import *
from .data.items import *
import base64
import pickle

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

class player(pyg.sprite.Sprite):
    _layer = 5
    saveable = ['name','health','maxhealth','speed','LastExperience','W','pos','_locked','_dead', 'Color','Level','Experience','points','attack','luck','defense','agility','inteligence']

    # GUIs
    _StatusOpen = False
        # Build
    _BuildOpen = False
    _BuildPage = 1
    _BuildXSHIFT = 90

    W = {}

    _type = 'player'

    # Waiters
    _Wait_time_levelUpSong = TC.getTime(1)
    C_Wait_time_levelUpSong = 0
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

        self.rect = Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.image = self.animations[self.curr][self.lastSide][int(self.anim_frame)]

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
        return super().update()
    
    # UIs
    def drawUis(self,BUILD_TILES:dict):
        self.draw_status(self._StatusOpen)
        self.draw_build(self._BuildOpen,BUILD_TILES)

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
        if camera:
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

        # Update Things
        self.animationsBuild()