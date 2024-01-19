from ..config import *
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

""" TILES """
class Tree(Tile):
    _layer = 1
    _collision = True
    _build = False
    name = "Tree"
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((16,64,32,32),-1),(64,64))
        self.rect = Rect(XY[0],XY[1],64,64)

class Sign1(Tile):
    _layer = 0
    _collision = False
    _build = False
    name = "Sign"
    def __init__(self, XY, *groups,Text:str="Hello! i'm a Sign.") -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(SIGNS).image_at((2,4,28,28),-1),(32,32))
        self.rect = Rect(XY[0],XY[1],self.image.get_size()[0]*3,self.image.get_size()[1]*3)

        # Create Hitbox, and set it to the center of rect
        self.hitbox:pyg.Rect = Rect(XY[0],XY[1],64,64)
        self.hitbox.center = self.rect.center

        # Defines the signs text
        self.Text = str(Text)

        # IsActive
        self.IsActive = False
        self.ActivateKey = K_KP_ENTER or K_RETURN
        self.WaitCooldown = 0 # Cooldown Default = 0

        # Unique Code
        self.UniqueCode = str(random.randint(0, 200000))+self.name + str(random.randint(0, 100))

    # def _draw(self):
    #     pme.draw_rect2((50,SCREEN.get_size()[1]-175),(SCREEN.get_size()[0]-100,150),(0,0,0,200),2)

    def draw_text(self,player):
        if self.IsActive:
            if self.hitbox.colliderect(player.rect):
                if not player.CheckByUniqueCode(self):
                    # print(f"{self.name}({self.UniqueCode}): {self.Text}")
                    player.addSigns(self.Text, (190,120,56,120), self, 2)
            else:
                self.IsActive = False
        else:
            if player.CheckByUniqueCode(self):
                # print(f"[] {self.name}({self.UniqueCode}) - Removed")
                player.TriesRemove(self)

    def collision(self, player):
        # Modded for Sign
        self.draw_text(player)
        if self.WaitCooldown > 0:
            self.WaitCooldown -= 1
        if self.WaitCooldown <= 0:
            if self.hitbox.colliderect(player.rect):
                if pme.key_pressed(self.ActivateKey):
                    # Reset Cooldown
                    self.WaitCooldown = TimeConverter(DB).getTime(.25)
                    self.IsActive = not self.IsActive
            else:
                self.IsActive = False

""" DECORATION TILES"""
class Decoration1(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration1'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,64,16,16),-1),(32,32))

class Decoration2(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
    _build = False
    name = 'Decoration2'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((96,80,16,16),-1),(32,32))

class Decoration3(Tile):
    _layer = 1
    _collision = False
    _type = 'decoration'
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
    _type = 'decoration'
    _build = False
    name = 'Decoration5'
    def __init__(self, XY, *groups) -> None:
        super().__init__(XY, *groups)
        self.image = pyg.transform.scale(spritesheet(TILES).image_at((0,96,16,16),-1),(32,32))

"""                         END                         """
BUILD_ITEMS = [
    
]