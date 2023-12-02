from ..config import *
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

class ItemBase(pyg.sprite.Sprite):
    # Info
    Name = 'Item Base'
    Tip = 'A Base Item\nUse it to create new items.'
    RColor = (55,55,55)

    # Data
    saveable = ['pos','rect','size','_RealName']
    def __init__(self, pos:tuple or list,*groups) -> None:
        super().__init__(*groups)
        self._RealName = "ItemBase"

        self.size = (16,16)
        self.pos = pos
        self.image = pyg.Surface(self.size)
        self.image.fill((175,55,55))
        self.rect = Rect(0,0,self.size[0],self.size[1])
        self.rect.topleft = self.pos

    def draw(self):
        SCREEN.blit(self.image,self.rect)

    def update(self, *args, **kwargs) -> None:

        return super().update(*args, **kwargs)
    
ITEMS = {
    'ItemBase':ItemBase
}