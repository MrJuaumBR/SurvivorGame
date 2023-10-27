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
    saveable = ['name','health','maxhealth','speed','pos','_locked','_dead', 'Color','Level','Experience']
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
        if self.Experience >= 100*self.Level:
            self.Experience -= 100*self.Level
            self.Level += 1
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

    def update(self) -> None:
        self.Input()
        self.movement()
        self.recoverHealth()
        self.animate()
        self.checklevel()
        self.checkWarn()
        return super().update()
    
    # Save
    def Save(self) -> bytes:
        self.pos = self.rect.topleft
        self.size = self.rect.size
        s = {}
        for item in self.saveable:
            s[item] = self.__dict__[item]
        return base64.b64encode(pickle.dumps(s))
    
    def Load(self, data:bytes):
        s = {}
        ddata:dict = pickle.loads(base64.b64decode(data))
        for item in self.saveable:
            self.__dict__[item] = ddata[item]
        self.rect.topleft = self.pos