from ..config import *
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

class Enemy(pyg.sprite.Sprite):
    _layer = 3
    _attack_delay = TC.getTime(1)
    _move_delay = TC.getTime(2)
    _damage = 5
    _speed = 5
    _locked = False
    
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