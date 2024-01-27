"""
Camera System for the game

Functions:
Draw By layer;
Draw By Y Pos;
Zoom;
Player Follow;
...
"""

from .config import *
import pygame as pyg
from pygame.locals import *
from .data.Tiles import *
from .data.enemys import *
from .data.Items import *

# Save System
from pickle import dumps, loads
from base64 import b64encode, b64decode

class Camera(pyg.sprite.Group):
    _Player_Def = False
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)

        self.display_surface = pyg.display.get_surface()

        self.offset = pyg.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

        # Zoom
        self.zoom_scale = 1
        self.internal_surf_size = pme.screen.get_size()
        self.internal_surf = pyg.Surface(self.internal_surf_size,pyg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w,self.half_w))
        self.internal_surf_size_vector = pyg.math.Vector2(self.internal_surf_size)
        self.internal_offset = pyg.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

        self.player = None

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def zoom_keyboard_control(self):
        # More Zoom
        if (pme.key_pressed(K_PLUS) or pme.key_pressed(K_i)) or (pme.key_pressed(K_KP_PLUS) or pme.key_pressed(K_PAGEUP)):
            self.zoom_scale += 0.1
            if self.zoom_scale > 1.5:
                self.zoom_scale = 1.5
        elif (pme.key_pressed(K_MINUS) or pme.key_pressed(K_o)) or (pme.key_pressed(K_KP_MINUS) or pme.key_pressed(K_PAGEDOWN)):
            self.zoom_scale -= 0.1
            if self.zoom_scale < 0.8:
                self.zoom_scale = 0.8
        elif (pme.key_pressed(K_EQUALS) or pme.key_pressed(K_KP_EQUALS)):
            self.zoom_scale = 1

    def update(self,player ,*args, **kwargs) -> None:
        for spr in self.sprites():
            if spr != player:
                spr.update(player,*args, **kwargs)
            else:
                if not self._Player_Def:
                    spr.Camera = self
                    self._Player_Def = True
                spr.update()

    def Draw_Enemy_Info(self):
        for sprite in self.sprites():
            if sprite._type in ['enemy']:
                try:
                    sprite.draw_info(self)
                except Exception as err:
                    print(f'{Fore.RED}[Camera - Draw_Enemy_Info] Cant Draw Info: {sprite.name}\n{err}{Fore.RESET}')
                    pass

    def draw(self, player):
        # Center the camera on the player
        self.center_target_camera(player)
        
        # Control the zoom level using keyboard input
        self.zoom_keyboard_control()

        # Fill the internal surface with a green color
        self.internal_surf.fill((100, 195, 100))
        
        # Draw the decoration sprites on the internal surface
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.layer):
            if sprite._type == 'decoration':
                offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
                self.internal_surf.blit(sprite.image, offset_pos)
                sprite.offset_pos = offset_pos
        
        # Draw the tile, player, and enemy sprites on the internal surface
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite._type in ['tile', 'player', 'enemy']:
                offset_pos = tuple(sprite.rect.topleft) - self.offset + self.internal_offset
                self.internal_surf.blit(sprite.image, offset_pos)
                sprite.offset_pos = offset_pos
                
                # Draw hitbox if DEBUG mode is enabled
                if DEBUG:
                    try:
                        if sprite.hitbox:
                            offset_hitbox = sprite.hitbox.topleft - self.offset + self.internal_offset
                            hitbox = pyg.Surface(sprite.hitbox.size)
                            self.internal_surf.blit(hitbox, offset_hitbox)
                    except:
                        pass
        
        # Scale the internal surface based on the zoom scale
        scaled_surf = pyg.transform.scale(self.internal_surf, self.internal_surf_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        # Draw the player's slash effect on the scaled surface
        player.Slash.draw(scaled_surf)
        
        # Blit the scaled surface onto the display surface
        self.display_surface.blit(scaled_surf, scaled_rect)
        
        # Draw the player's UI elements
        player.draw_ui(self)
        
        # Set the current player object
        self.player = player
        
        # Draw enemy information
        self.Draw_Enemy_Info()

    def draw_in(self, surf, pos, to_surf:pyg.Surface):
        offset_pos = self.convert_offset(pos)
        to_surf.blit(surf, offset_pos)
        # self.internal_surf.blit()

    def convert_offset(self, pos):
        offset_pos = pos - self.offset + self.internal_offset
        return offset_pos

    def receive_sprites(self,*sprites):
        for spr in sprites:
            self.add(spr)

    def sprites_rect(self) -> list[pyg.Rect,]:
        spr:list[pyg.sprite.Sprite] = self.sprites()
        rects = []
        for sprite in spr:
            rects.append(sprite.rect)
        return rects
    
    def sprites_collide(self, rect:Rect) -> list[pyg.sprite.Sprite,]:
        spr:list[pyg.sprite.Sprite] = self.sprites()
        rects = []
        for sprt in spr:
            if sprt.rect.colliderect(rect):
                rects.append(sprt)
        return rects

    def EncodeNecessaireBytes(self, sprite:Tile) -> bytes:
        """
        Encode the necessary bytes for a given sprite.
        
        Args:
            sprite (Tile): The sprite object to encode.
        
        Returns:
            bytes: The encoded bytes.
        """
        spriteRealDict = sprite.__dict__
        sprite_dict = {
            'rect': sprite.rect,
        }
        try:
            try:
                if spriteRealDict['UniqueCode']:
                    sprite_dict['UniqueCode'] = sprite.UniqueCode
            except: pass
            try:
                if spriteRealDict['Text']:
                    sprite_dict['Text'] = sprite.Text
            except: pass
        except Exception as err:
            print(err, sprite)

        dic = b64encode(dumps([sprite_dict,sprite.__class__.__name__]))

        return dic

    def DeencodeNecessaireBytes(self, dic:bytes) -> [dict, str]:
        """
        Decode the given base64 encoded dictionary string into a list of dictionaries and a string.

        Parameters:
            dic (bytes): The base64 encoded dictionary string.

        Returns:
            list[dict, str]: The decoded dictionary as a list of dictionaries and a string.
        """
        dic:[dict, str] = loads(b64decode(dic))

        d:dict = dic[0]
        s:str = dic[1]

        return d,s

    def saving(self) -> list[dict,]:
        s = []
        for spr in self.sprites():
            if str(spr._type).lower() in ['tile','item','enemy','decoration']:
                s.append(self.EncodeNecessaireBytes(spr))
        return s
    
    def Load(self, sprites:list[bytes,]):
        for sprite in sprites:
            spriteData, spriteClassName = self.DeencodeNecessaireBytes(sprite)
            clss = get_class(spriteClassName)
            try:
                try:
                    if clss._sub_type == 'sign':
                        spr = clss(XY=(0,0),groups=(self),text=spriteData['Text'])
                    else:
                        spr = clss(XY=(0,0),groups=(self))
                except: 
                    spr = clss(XY=(0,0),groups=(self))
                
            except:
                spr = clss()
            spr.Load(spriteData)
            self.add(spr)