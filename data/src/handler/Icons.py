from ..config import *

IconsSH = spritesheet(f'.{TEXTURES_PATH}/icons.png')

class _Icon(pyg.sprite.Sprite):
    Size = 32,32
    Sprite_pos = (0,0,31,31)
    Tip = None
    def __init__(self, Size:tuple[int, int] or list[int, int],hasHover:bool,TipText:str="",*groups) -> None:
        super().__init__(*groups)
        self.rect = Rect(0,0,self.Size[0],self.Size[1])
        self.image = pyg.Surface(self.Size)

        self.Size = Size
        self.LoadIcon()

        self.hasHover = hasHover
        if self.hasHover:
            if not (TipText in ['',' ',None]):
                self.Tip = Tip(TipText, pme, (55,55,55),(216, 211, 192), 2)

    def LoadIcon(self):
        if IconsSH:
            self.image = pyg.transform.scale(IconsSH.image_at(self.Sprite_pos,-1),self.Size)

    def onHover(self):
        if self.rect.collidepoint(pyg.mouse.get_pos()):
            if self.Tip:
                self.Tip.HoveRing(True)
        else:
            if self.Tip:
                self.Tip.HoveRing(False)
    def draw(self,pos):
        self.rect.center = pos
        SCREEN.blit(self.image,self.rect)
        self.onHover()

class LifeIcon(_Icon):
    Sprite_pos = (0,0,31,31)

class ExperienceIcon(_Icon):
    Sprite_pos = (64,0,31,31)

class ResistanceIcon(_Icon):
    Sprite_pos = (32,0,31,31)