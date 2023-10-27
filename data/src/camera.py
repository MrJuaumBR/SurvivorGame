from .config import *
import pygame as pyg
from pygame.locals import *

class Camera(pyg.sprite.Group):
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

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def zoom_keyboard_control(self):
        # More Zoom
        if pme.key_pressed(K_PLUS) or (pme.key_pressed(K_KP_PLUS) or pme.key_pressed(K_PAGEUP)):
            self.zoom_scale += 0.1
            if self.zoom_scale > 1.5:
                self.zoom_scale = 1.5
        elif pme.key_pressed(K_MINUS) or (pme.key_pressed(K_KP_MINUS) or pme.key_pressed(K_PAGEDOWN)):
            self.zoom_scale -= 0.1
            if self.zoom_scale < 0.8:
                self.zoom_scale = 0.8

    def update(self,player ,*args, **kwargs) -> None:
        for spr in self.sprites():
            if spr != player:
                spr.update(player,*args, **kwargs)
            else:
                spr.update()

    def draw(self,player):
        self.center_target_camera(player)
        self.zoom_keyboard_control()

        self.internal_surf.fill((100,195,100))
        # active elements
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.layer):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)
            sprite.offset_pos = offset_pos
        
        scaled_surf = pyg.transform.scale(self.internal_surf, self.internal_surf_size_vector*self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w,self.half_h))

        self.display_surface.blit(scaled_surf,scaled_rect)
        player.draw_ui(self)

    def convert_offset(self, pos):
        offset_pos = pos - self.offset + self.internal_offset
        return offset_pos

    def receive_sprites(self,*sprites):
        for spr in sprites:
            self.add(spr)