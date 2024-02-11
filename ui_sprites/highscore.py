from kink import di

from project_dash.dtos import SwitchSceneDTO
from project_dash.sprites import ButtonListener, ImageSprite, TextSprite

import pygame as pg

import project_dash.config


class SpriteHighscore(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 227, 38, 255, *groups)

class SpriteTable(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 205, 120, 255, *groups)


class ButtonSpriteBack(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 676, 415, 255, *groups)

    def highlight(self, _is_highlighted: bool):
        if _is_highlighted:
            self.set_opacity(40)
        else:
            self.set_opacity(255)

    def is_clicked(self):
        return SwitchSceneDTO("main_menu")

# leader board text player
class TextSpritePlayer1(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 235, 189, 255, "E", di["clr_dark_blue"], *groups)

class TextSpritePlayer2(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 235, 227, 255, "F", di["clr_dark_blue"], *groups)

class TextSpritePlayer3(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 235, 265, 255, "", di["clr_dark_blue"], *groups)

class TextSpritePlayer4(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 235, 302, 255, "", di["clr_dark_blue"], *groups)
        
class TextSpritePlayer5(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 235, 340, 255, "", di["clr_dark_blue"], *groups)
        
# text leaderboard player's score
class TextSpriteScorePlayer1(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):        
        TextSprite.__init__(self, _asset, 620, 189, 255, "", di["clr_dark_blue"], *groups)
        
class TextSpriteScorePlayer2(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 620, 227, 255, "", di["clr_dark_blue"], *groups)
        
class TextSpriteScorePlayer3(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 620, 265, 255, "", di["clr_dark_blue"], *groups)
        
class TextSpriteScorePlayer4(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 620, 302, 255, "3", di["clr_dark_blue"], *groups)
        
class TextSpriteScorePlayer5(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 620, 340, 255, "R", di["clr_dark_blue"], *groups)

'''
class Highscore(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpritePlayer1(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpritePlayer2(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpritePlayer3(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpritePlayer4(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpritePlayer5(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpriteScore1(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpriteScore2(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpriteScore3(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpriteScore4(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

class SpriteScore5(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)

'''
