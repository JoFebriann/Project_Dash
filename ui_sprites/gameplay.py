from kink import di

from project_dash.sprites import ImageSprite, TextSprite

import pygame as pg

import project_dash.config


class SpritePenguin(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 500, 250, 255, *groups)

    def update_image(self, _x: int, _y: int):
        # print(f"Updating SpritePenguin with {sin(pg.time.get_ticks()/2)*100+200}.")
        # self.set_pos(450, sin(pg.time.get_ticks()/2)*100+200)
        self.set_pos(_x, _y)


class TextSpriteScore(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 30, 436, 255, "Score: ", di["clr_white"], *groups)


class SpriteTree(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 0, 0, 255, *groups)

    def update_image(self, _x: int, _y: int):
        self.set_pos(_x, _y)


# game over
class SpriteGameOverMessage(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 228, 161, 255, *groups)


class TextSpriteGameOverScore(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 325, 259, 255, "Score: ", di["clr_white"], *groups)