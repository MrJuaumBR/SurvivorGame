"""
Pre-Generated Structures
"""

from .Tiles import *
from pygame.locals import *
from ..config import (DB, TILESET, TEXTURES_PATH, pyg, spritesheet,pme,random,DEBUG)
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

class BaseStructure(pyg.sprite.Sprite):
    _layer=1
    _collision = False
    _type = 'structure'
    _sub_type = 'base'
    _build = False
    _name = 'Base Structure'
    def __init__(self, XY=(0,0),*groups) -> None:
        super().__init__(XY,*groups)
        
        self.size = (0,0)
        self.rect = Rect(XY[0],XY[1],self.size[0],self.size[1])

        self.Column_X = 3
        self.Column_Y = 3

        self.build_tiles = [] # Build Tiles Y -> Build Tiles X
        self.set_build_tiles()
    
    def set_build_tiles(self):
        startX = self.rect.x - (self.size[0]//self.Column_X)
        startY = self.rect.y - (self.size[1]//self.Column_Y)

        line1 = [
            SkullDeco((startX, startY),self.groups()[0]),
            SkullDeco((startX+64, startY),self.groups()[0]),
        ]