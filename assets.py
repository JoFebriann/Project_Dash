from kink import di

import os
import pygame as pg

import project_dash.config


class AssetsLoader:
    def __init__(self):
        self.assets_dir = di["assets_dir"]

        # Shared assets
        #   Image
        self.img_bg = [self.load_image("BG.png", False)]
        self.img_tree = [self.load_image("Tree.png", True)]

        #   Font
        self.font_temp = self.load_font("GOTHMBOL_0.TTF", 20)
        self.font_score = self.load_font("GOTHMBOL_0.TTF", 40)

        # Intro assets
        self.img_intro = [self.load_image("IntroA.png", False),
                          self.load_image("IntroB.png", False)]

        # Main menu assets
        #   Image
        self.img_logo = [self.load_image("Logo.png", True)]
        self.img_continue = [self.load_image("ClickToContinue.png", True)]

        # Register assets
        #   Image
        self.img_register = [self.load_image("RegisterYes.png", True),
                             self.load_image("RegisterNo.png", True)]
        self.img_login = [self.load_image("LoginYes.png", True),
                          self.load_image("LoginNo.png", True)]
        self.img_username = [self.load_image("username.png", True)]
        self.img_email = [self.load_image("email.png", True)]
        self.img_text_input = [self.load_image("Text_Field.png", True), self.load_image("Text_Field_Y.png", True)]
        self.img_play = [self.load_image("Play.png", True)]

        # Gameplay assets
        #   Image
        self.img_penguin = [self.load_image("Penguin.png", True),
                            self.load_image("Penguin2.png", True)]
        #   Sound
        self.sound_point = [self.load_sound("snd_achievement.wav"), self.load_sound("snd_point2.wav")]

        # Highscore assets
        #   Image
        self.img_back = [self.load_image("Back.png", True)]
        self.img_highscore = [self.load_image("HIGHSCORE.png", True)]
        self.img_table = [self.load_image("Table.png", True)]

        # GameOver assets
        #   Image
        self.img_game_over_message = [self.load_image("GameOver.png", True)]
        # #   Sound
        # self.sound_game_over = [self.load_sound()]

    def load_image(self, _file_name: str, alpha=False):
        """loads an image, prepares it for play"""
        file_path = os.path.join(self.assets_dir, _file_name)
        try:
            surface = pg.image.load(file_path).convert_alpha()
        except pg.error:
            raise SystemExit(f'Could not load image "{file_path}" {pg.get_error()}')
        if alpha:
            return surface.convert_alpha()
        return surface.convert()

    def load_sound(self, _file_name: str):
        """because pygame can be compiled without mixer."""
        if not pg.mixer:
            return None
        file_path = os.path.join(self.assets_dir, _file_name)
        try:
            sound = pg.mixer.Sound(file_path)
            return sound
        except pg.error:
            print(f"Warning, unable to load, {file_path}")
        return None

    def load_font(self, _file_name: str, _font_size: int):
        file_path = os.path.join(self.assets_dir, _file_name)
        return pg.font.Font(file_path, _font_size)
