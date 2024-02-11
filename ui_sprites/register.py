from kink import di

from project_dash.dtos import LoginDTO, RegisterDTO, SelectDTO, SwitchSceneDTO, WarningDTO
from project_dash.services import DashService
from project_dash.sprites import ButtonListener, ImageSprite, TextSprite

import pygame as pg

import project_dash.config


class SpriteTickboxRegister(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 54, 45, 255, *groups)
    

class SpriteTickboxLogin(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 469, 48, 255, *groups)
        

class SpriteTextRegisterUsername(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 55, 140, 255, *groups)


class SpriteTextRegisterEmail(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 53, 260, 255, *groups)


class SpriteTextLoginUsername(ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 467, 140, 255, *groups)


class ButtonSpriteTextInputRegisterUsername(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 53, 185, 255, *groups)

    def highlight(self, _is_highlighted: bool):
        pass

    def is_clicked(self):
        return SelectDTO("register-username")


class ButtonSpriteTextInputRegisterEmail(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 53, 312, 255, *groups)

    def highlight(self, _is_highlighted: bool):
        pass

    def is_clicked(self):
        return SelectDTO("register-email")


class ButtonSpriteTextInputLoginUsername(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 465, 185, 255, *groups)

    def highlight(self, _is_highlighted: bool):
        pass

    def is_clicked(self):
        return SelectDTO("login")


class ButtonSpritePlay(ButtonListener, ImageSprite):
    def __init__(self, _assets: list[pg.Surface], _warning: TextSprite, _service: DashService, *groups: pg.sprite.RenderUpdates):
        ImageSprite.__init__(self, _assets, 678, 415, 255, *groups)
        self.warning = _warning
        self.service = _service
        self.is_register = True
        self.email = ""
        self.username = ""

    def highlight(self, _is_highlighted: bool):
        if _is_highlighted:
            self.set_opacity(120)
        else:
            self.set_opacity(255)

    def is_clicked(self) -> (SwitchSceneDTO, WarningDTO):
        """
        Returns either a WarningDTO or a SwitchSceneDTO
        """
        
        if self.is_register is True:
            return self.service.service_register.register_acc(RegisterDTO(self.username, self.email))
        else:
            return self.service.service_register.login_acc(LoginDTO(self.username))


class TextSpriteRegisterUsername(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 77, 196, 255, "", di["clr_dark_blue"], *groups)


class TextSpriteRegisterEmail(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 77, 321, 255, "", di["clr_dark_blue"], *groups)


class TextSpriteLoginUsername(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 480, 196, 255, "", di["clr_dark_blue"], *groups)


class TextSpriteWarning(TextSprite):
    def __init__(self, _asset: pg.font.Font, *groups: pg.sprite.RenderUpdates):
        TextSprite.__init__(self, _asset, 0, 0, 255, "", di["clr_red"], *groups)