from ..config import (DB, TILESET, TEXTURES_PATH, pyg, spritesheet,pme,random,DEBUG,DECO_ANIMATED)
from pygame.locals import *
from ..handler.PyMaxEngine import Tip
from ..handler.timerConverter import TimeConverter
TC = TimeConverter(DB)

TILES = "."+TILESET
SIGNS = "."+TEXTURES_PATH+"/Signs.png"

class Tile(pyg.sprite.Sprite):
    _layer = 2
    _collision = True
    _action = True
    _action_delay = TC.getTime(1)
    _action_delay_counter = 0
    _type = 'tile'
    _sub_type = 'base'
    _build = False
    name = 'BaseTile'
    def __init__(self, XY=(0,0),*groups) -> None:
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
    
    def update_things(self):
        pass

    def Load(self, data:dict):
        for key in data.keys():
            try:
                self.__dict__[key] = data[key]
            except:
                pass
        try:
            self.update_things()
        except: pass

    def others(self):
        pass

    def update(self, player) -> None:
        self.others()
        self.collision(player)
        return super().update()

""" TILES """
class Tree(Tile):
    _layer = 1
    _collision = True
    _build = False
    name = "Tree"
    _sub_type = 'tree'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((16,64,32,32),-1),(64,64))
        self.rect = Rect(XY[0],XY[1],64,32)

""" Interactive Tiles """
class Sign1(Tile):
    _layer = 0
    _collision = False
    _build = False
    name = "Sign"
    Color = (190,120,56,120)
    BorderColor = (170,100,36,255)
    _sub_type = "sign"
    def __init__(self, XY=(0,0),*groups,Text:str="Hello! i'm a Sign.") -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(SIGNS).image_at((2,4,28,28),-1),(32,32))
        self.rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)

        # Create Hitbox, and set it to the center of rect
        self.hitbox:pyg.Rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)
        self.hitbox.top = self.rect.top - self.hitbox.height//2
        self.hitbox.left = self.rect.left - self.hitbox.width//2
        # self.hitbox.center = self.rect.center

        # Defines the signs text
        self.Text = str(Text)

        # Defines The Tip
        self.Tip = Tip("Press 'E' for open.",pme,(50,50,50),(225,215,170),4)

        # IsActive
        self.IsActive = False
        self.ActivateKeys = [K_e, K_KP_ENTER]
        self.WaitCooldown = 0 # Cooldown Default = 0

        # Unique Code
        self.UniqueCode = str(random.randint(0, 200000))+self.name + str(random.randint(0, 100))

    # def _draw(self):
    #     pme.draw_rect2((50,SCREEN.get_size()[1]-175),(SCREEN.get_size()[0]-100,150),(0,0,0,200),2)

    def draw_text(self,player):
        if self.IsActive:
            if self.hitbox.colliderect(player.rect):
                if not player.CheckByUniqueCode(self):
                    if DEBUG:
                        print(f"{self.name}({self.UniqueCode}): {self.Text}")
                    player.addSigns(self.Text, self.Color, self, 3, border_color=self.BorderColor)
            else:
                self.IsActive = False
        else:
            if player.CheckByUniqueCode(self):
                if DEBUG:
                    print(f"{self.name}({self.UniqueCode}) - Removed")
                player.TriesRemove(self)

    def update_things(self):
        # Update Hitbox
        XY = self.rect.topleft
        self.hitbox:pyg.Rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)
        self.hitbox.top = self.rect.top - self.hitbox.height//2
        self.hitbox.left = self.rect.left - self.hitbox.width//2

    def collision(self, player):
        # Modded for Sign

        self.draw_text(player)
        if self.WaitCooldown > 0:
            self.WaitCooldown -= 1
        if self.WaitCooldown <= 0:
            if self.hitbox.colliderect(player.rect):
                if DEBUG:
                    print(f'{self.name}({self.UniqueCode}): \n\t - Activ. Cooldown: {self.WaitCooldown}\n\t - Active: {self.IsActive}')
                for key in self.ActivateKeys:
                    if pme.while_key_hold(key):
                        # Reset Cooldown
                        self.WaitCooldown = TimeConverter(DB).getTime(.25)
                        self.IsActive = not self.IsActive
            else:
                self.IsActive = False


class Rip(Sign1):
    _layer = 0
    _collision = True
    _build = False
    name = "Rip"
    _sub_type = "sign"
    Color = (100,100,100,120)
    BorderColor = (80,80,80)
    def __init__(self, XY=(0,0),*groups,Text:str="...") -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet("."+TILESET).image_at((32,128,16,16),-1),(32,32))
        self.rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)

        # Create Hitbox, and set it to the center of rect
        self.hitbox:pyg.Rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)
        self.hitbox.top = self.rect.top - self.hitbox.height//2
        self.hitbox.left = self.rect.left - self.hitbox.width//2
        # self.hitbox.center = self.rect.center

        # Defines the signs text
        self.Text = str(Text)

        # Defines The Tip
        self.Tip = Tip("Press 'E' for read.",pme,(50,50,50),(225,215,170),4)

        # IsActive
        self.IsActive = False
        self.ActivateKeys = [K_e, K_KP_ENTER]
        self.WaitCooldown = 0 # Cooldown Default = 0

""" DECORATION TILES"""
class Decoration1(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration1'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,64,16,16),-1),(32,32))

class CandleDeco(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = True
    name = 'Candle Decoration'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.animation = []
        self.animation_index = 0
        self.size = (16,16)

        self.setup_animation()

        self.image = self.animation[int(self.animation_index)]

        self.rect = Rect(XY[0],XY[1],self.size[0],self.size[1])

    def setup_animation(self):
        ss = spritesheet("."+DECO_ANIMATED)
        pos = [
            (1,1,32,32),
            (34,1,32,32),
            (64,1,32,32)
        ]
        for p in pos:
            self.animation.append(pyg.transform.scale(ss.image_at(p,-1),self.size))

    def animate(self):
        self.animation_index += 0.15
        if self.animation_index > len(self.animation):
            self.animation_index = 0
        self.image = self.animation[int(self.animation_index)]

    def others(self):
        self.animate()
        return super().others()

class FirebowlDeco(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = True
    name = 'FireBowl Decoration'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.animation = []
        self.animation_index = 0
        self.size = (32,32)

        self.setup_animation()

        self.image = self.animation[int(self.animation_index)]

        self.rect = Rect(XY[0],XY[1],self.size[0],self.size[1])

    def setup_animation(self):
        ss = spritesheet("."+DECO_ANIMATED)
        pos = [
            (1,34,32,32),
            (34,34,32,32),
            (64,34,32,32)
        ]
        for p in pos:
            self.animation.append(pyg.transform.scale(ss.image_at(p,-1),self.size))

    def animate(self):
        self.animation_index += 0.15
        if self.animation_index > len(self.animation):
            self.animation_index = 0
        self.image = self.animation[int(self.animation_index)]

    def others(self):
        self.animate()
        return super().others()

class SkullDeco(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Skull Decoration'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((80,177,16,16),-1),(32,32))

class Decoration2(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration2'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,80,16,16),-1),(32,32))

class Decoration3(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration3'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((112,80,16,16),-1),(32,32))

class Decoration4(Tile):
    _layer = 1
    _collision = False
    _type = 'tile'
    _build = False
    name = 'Decoration4'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((0,80,16,16),-1),(32,32))

class Decoration5(Tile):
    _layer = 6
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration5'
    def __init__(self, XY=(0,0), *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((0,96,16,16),-1),(32,32))


"""                         END                         """
BUILD_ITEMS = [
    
]