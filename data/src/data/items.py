from ..config import *
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

class Tile(pyg.sprite.Sprite):
    _layer = 2
    _collision = True
    _action = True
    _action_delay = TC.getTime(1)
    _action_delay_counter = 0
    def __init__(self, XY,*groups) -> None:
        super().__init__(*groups)
        self.rect = Rect(XY[0],XY[1],32,32)
        self.image = pyg.Surface((32,32))
        self.image.fill((0,100,0))
        self.camera = self.groups()[0]

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
    
class Magma(Tile):
    _layer = 2
    _collision = True
    _action_delay = TC.getTime(.25)
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.rect = Rect(XY[0],XY[1],32,32)
        self.image = pyg.Surface((32,32))
        self.image.fill((200,100,0))

    def action(self, player):
        player.takeDamage(25)