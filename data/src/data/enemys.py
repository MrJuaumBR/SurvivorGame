from ..config import *
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

Animations = {
    "Enemies":{},
    "Friendly":{
        "Chicken":{
            'Walk':{
                'left':[(96,145,16,16),(112,145,16,16),(128,145,16,16)],
                'right':[(96,162,16,16),(112,162,16,16),(128,162,16,16)],
                'up':[(96,128,16,16),(112,128,16,16),(128,128,16,16)],
                'down':[(96,176,16,16),(112,176,16,16),(128,176,16,16)],
            },
            'Idle':{
                'left':[(112,145,16,16),],
                'right':[(112,162,16,16),],
                'up':[(112,128,16,16),],
                'down':[(112,176,16,16),],
            },
        }
    }
}

"""  ENEMIES   """
class Enemy(pyg.sprite.Sprite):
    _layer = 3
    _attack_delay = TC.getTime(1)
    _move_delay = TC.getTime(2)
    _damage = 5
    _speed = 5
    _locked = False
    _type = 'enemy'
    _name = "Enemy Base"
    health = 100
    maxhealth = 100
    def __init__(self, XY,*groups) -> None:
        super().__init__(*groups)
        self.rect = Rect(XY[0],XY[1],32,32)
        self.image = pyg.Surface((32,32))
        self.image.fill((200,0,0))
        self.camera = self.groups()[0]

        self.repeat = 0
        self.path = pyg.math.Vector2(0,0)

    def getRange(self):
        return self._damage * random.choice([0.8,0.9,1,1.1,1.2])

    def attack(self,player):
        if self.health > 0:
            if self._attack_delay <= 0 and not (player._dead):
                player.takeDamage(self.getRange())
                self._attack_delay = TC.getTime(1)

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            self.attack(player)
            self._locked = True
        else:
            self._locked = False

    def movement(self):
        if self._move_delay <= 0:
            if not self._locked:
                if self.repeat >= random.randint(2,4):
                    self.path.x = random.choice([-1.2,-1,0,1,1.2])
                    self.path.y = random.choice([-1.2,-1,0,1,1.2])
                    self._move_delay = TC.getTime(2)
                    self.repeat = 0
                else:
                    self.repeat += 1
                    self._move_delay = TC.getTime(random.choice([0.1,0.2,0.3]))
                    self.rect.x += self.path.x * self._speed
                    self.rect.y += self.path.y * self._speed

    def update(self, player):
        self.collision(player)
        self.movement()
        if self._attack_delay > 0:
            self._attack_delay -= 1
        if self._move_delay > 0:
            self._move_delay -= 1


""" FRIENDLY """
class Friendly(pyg.sprite.Sprite):
    _layer = 3
    _move_delay = TC.getTime(1)
    _damage = 5
    _speed = 5
    _locked = False
    _type = 'enemy'
    _name = "Friendly Base"
    health = 100
    maxhealth = 100
    size = (32,32)
    def __init__(self, XY,*groups) -> None:
        super().__init__(*groups)
        self.camera = self.groups()[0]

        self.repeat = 0
        self.path = pyg.math.Vector2(0,0)

        self.animations = {'Walk':{'up':[],'down':[],'left':[],'right':[]},'Idle':{'up':[],'down':[],'left':[],'right':[]}}
        self.setupAnimations()

        self.anim_frame = 0
        self.state = 'Idle'
        self.lastSide = 'left'

        self.rect = Rect(XY[0],XY[1],32,32)
        self.image = self.animations[self.state][self.lastSide][self.anim_frame] or pyg.Surface((32,32))

    def animPlay(self):
        track = self.animations[self.state][self.lastSide]
        self.anim_frame += .15
        if self.anim_frame > len(track):
            self.anim_frame = 0
        self.image = track[int(self.anim_frame)]

    def setupAnimations(self):
        try:
            myStyle = Animations['Friendly']
            myStyle = myStyle[self._name]
            for state in myStyle.keys():
                for side in myStyle[state].keys():
                    for i,anim in enumerate(myStyle[state][side]):
                        s = spritesheet('.'+PLAYERS_SPRITESHEET)
                        self.animations[state][side].insert(i,pyg.transform.scale(s.image_at(anim,-1),self.size))
        except Exception as err:
            print(err)

    def collision(self, player):
        if self.rect.colliderect(player.rect):
            self._locked = True
        else:
            self._locked = False

    def movement(self):
        if self._move_delay <= 0:
            if not self._locked:
                if self.repeat >= random.randint(2,4):
                    self.path.x = random.choice([-1.2,-1,0,1,1.2])
                    self.path.y = random.choice([-1.2,-1,0,1,1.2])
                    self._move_delay = TC.getTime(0.5)
                    self.repeat = 0
                else:
                    self.CheckSideAndState()
                    self.repeat += 1
                    self._move_delay = TC.getTime(random.choice([0.1,0.2,0.3]))
                    self.rect.x += self.path.x * self._speed
                    self.rect.y += self.path.y * self._speed
        if self.path.x != 0 or self.path.y != 0:
            self.animPlay()

    def CheckSideAndState(self):
        if not self._locked:
            if self.path.y != 0 or self.path.x != 0:
                self.state = 'Walk'
                if self.path.x > 0:
                    self.lastSide = 'right'
                elif self.path.x < 0:
                    self.lastSide = 'left'
                elif self.path.y > 0:
                    self.lastSide = 'down'
                elif self.path.y < 0:
                    self.lastSide = 'up'
            else:
                self.state = 'Idle'
        else:
            self.state = 'Idle'
        if self.health <= 0:
            self.state = 'Dead'

    def update(self, player):
        self.collision(player)
        self.movement()
        if self._move_delay > 0:
            self._move_delay -= 1

class Chicken(Friendly):
    _name = "Chicken"
    health = 25
    maxhealth = 25
    _speed = 2.5