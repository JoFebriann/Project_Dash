from abc import ABC, abstractmethod
from kink import di


import pygame as pg

import project_dash.config


class _Sprite(pg.sprite.Sprite):
    def __init__(self, _x: int, _y: int, _opacity: int, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.x = _x
        self.y = _y
        self.opacity = _opacity
        self.is_highlighted = False

        self.image = None
        self.rect = None

    def set_pos(self, _x: int, _y: int):
        self.x = _x
        self.y = _y
        self.set_rect()

    def set_rect(self):
        self.rect = self.image.get_rect().move(self.x, self.y)

    def set_opacity(self, _opacity: int):
        self.opacity = _opacity
        self.set_alpha()

    def set_alpha(self):
        self.image.set_alpha(self.opacity)

    def fill_overlay(self, _color: tuple[int, int, int]):
        """
        https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen
        Fill all pixels of the surface with color, preserving transparency.
        """
        w, h = self.image.get_size()
        r, g, b, = _color
        for x in range(w):
            for y in range(h):
                a = self.image.get_at((x, y))[3]
                self.image.set_at((x, y), pg.Color(r, g, b, a))


class ImageSprite(_Sprite):
    def __init__(self, _assets: list[pg.Surface], _x: int, _y: int, _opacity: int, *groups):
        _Sprite.__init__(self, _x, _y, _opacity, *groups)
        self.assets = _assets
        self.set_image(self.assets[0])

    def set_image(self, _asset: pg.Surface):
        self.image = _asset.copy()
        self.set_rect()


class ButtonListener(ABC):
    @abstractmethod
    def is_clicked(self):
        pass

    @abstractmethod
    def highlight(self, _is_highlighted: bool):
        pass


class ButtonSubject:
    def __init__(self, _observers):
        self.observers = _observers
        # self.observers will be a list of objects that inherit both ButtonListeners and ImageSprite

    def __repr__(self):
        return f"ButtonSubject({self.observers})"

    def play_mouse_click(self, _mouse_coords: tuple[int, int], _mouse_button: int):
        subject_output = []
        for observer in self.observers:
            if observer.rect.collidepoint(_mouse_coords):
                subject_output.append(observer.is_clicked())
        return subject_output

    def highlight_on_hover(self, _mouse_coords: tuple[int, int]):
        for observer in self.observers:
            if not observer.is_highlighted:
                if observer.rect.collidepoint(_mouse_coords):
                    observer.highlight(True)
                    observer.is_highlighted = True
                    # observer.fill_overlay(di["clr_light_grey"])
            else:
                if not observer.rect.collidepoint(_mouse_coords):
                    # observer.fill_overlay(di["clr_white"])
                    observer.highlight(False)
                    observer.is_highlighted = False


class TextSprite(_Sprite):
    def __init__(self, _asset: pg.font.Font, _x: int, _y: int, _opacity: int, _msg: str, _color: tuple, *groups):
        _Sprite.__init__(self, _x, _y, _opacity, *groups)
        self.asset = _asset
        self.msg = _msg
        self.color = _color

        self.set_image()

    def set_image(self):
        self.image = self.asset.render(self.msg, True, self.color)
        self.set_rect()

    def set_msg(self, _msg: str):
        self.msg = _msg
        self.set_image()

    def align(self, _enum: str, _box_width=float("inf"), _box_height=float("inf")):
        # https://stackoverflow.com/questions/25149892/how-to-get-the-width-of-text-using-pygame
        box_width = di["width"] if (_box_width == float("inf")) else _box_width
        box_height = di["height"] if (_box_height == float("inf")) else _box_height

        text_width, text_height = self.asset.size(self.msg)

        new_x, new_y = self.x, self.y
        if _enum == "center_x" or _enum == "center":
            new_x = (box_width - text_width) // 2
        elif _enum == "center_y" or _enum == "center":
            new_y = (box_height - text_height) // 2
        else:
            raise ValueError
        self.rect = self.image.get_rect().move(new_x, new_y)
