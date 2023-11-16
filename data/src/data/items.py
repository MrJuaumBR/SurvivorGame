from ..config import *
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

TILES = "."+TILESET

class Tile(pyg.sprite.Sprite):
    _layer = 2
    _collision = True
    _action = True
    _action_delay = TC.getTime(1)
    _action_delay_counter = 0
    _type = 'tile'
    _build = False
    name = 'BaseTile'
    def __init__(self, XY,*groups) -> None:
        super().__init__(*groups)
        self.rect = Rect(XY[0],XY[1],32,32)
        self.image = pyg.Surface((32,32))
        self.image.fill((0,100,0))
        if len(self.groups()) > 0:
            self.camera = self.groups()[0]
        else:
            self.camera = None

    def action(self,player):
        pass

    def collision(self,player):
        if self._collision:
            if self.rect.colliderect(player.rect): # Collide
                if player.move.x != 0:
                    if player.move.x > 0:
                        player.rect.right = self.rect.left
                    elif player.move.x < 0:
                        player.rect.left = self.rect.right
                elif player.move.y != 0:
                    if player.move.y > 0:
                        player.rect.bottom = self.rect.top
                    elif player.move.y < 0:
                        player.rect.top = self.rect.bottom
                    
                self._faction(player)

    def _faction(self,player):
        if self._action:
            if self._action_delay_counter <= 0:
                self.action(player)
                self._action_delay_counter = self._action_delay
            else:
                self._action_delay_counter -= 1
                if self._action_delay_counter < 0:
                    self._action_delay_counter = 0
            

    def update(self, player) -> None:
        self.collision(player)
        return super().update()

""" DECORATION TILES"""
class Decoration1(Tile):
    _layer = 1
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration1'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,64,16,16),-1),(32,32))

class Decoration2(Tile):
    _layer = 1
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration2'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,80,16,16),-1),(32,32))

class Decoration3(Tile):
    _layer = 1
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration3'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((112,80,16,16),-1),(32,32))

class Decoration4(Tile):
    _layer = 1
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration4'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((0,80,16,16),-1),(32,32))

class Decoration5(Tile):
    _layer = 6
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration5'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((0,96,16,16),-1),(32,32))

"""                         END                         """
BUILD_ITEMS = [
    
]