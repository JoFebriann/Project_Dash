from kink import di

from project_dash.dtos import SwitchSceneDTO
from project_dash.sprites import ButtonListener, ImageSprite

import pygame as pg

import project_dash.config


class ButtonSpriteContinue(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 322, 415, 255, *groups)

    def highlight(self, _is_highlighted: bool):
        if _is_highlighted:
            self.set_opacity(120)
        else:
            self.set_opacity(255)

    def is_clicked(self):
        return SwitchSceneDTO("register")
            

class SpriteLogo(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 208, 43, 255, *groups)