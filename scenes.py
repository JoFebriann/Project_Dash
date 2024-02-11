from kink import di

from project_dash.ui_sprites.intro import SpriteIntro
from project_dash.ui_sprites.main_menu import ButtonSpriteContinue, SpriteLogo
from project_dash.ui_sprites.gameplay import SpritePenguin, SpriteTree, TextSpriteScore, SpriteGameOverMessage, TextSpriteGameOverScore
from project_dash.ui_sprites.register import SpriteTickboxRegister, SpriteTickboxLogin, SpriteTextRegisterUsername, SpriteTextRegisterEmail, SpriteTextLoginUsername, ButtonSpriteTextInputRegisterUsername, ButtonSpriteTextInputRegisterEmail, ButtonSpriteTextInputLoginUsername, ButtonSpritePlay, TextSpriteRegisterUsername, TextSpriteRegisterEmail, TextSpriteLoginUsername, TextSpriteWarning
from project_dash.ui_sprites.highscore import ButtonSpriteBack, SpriteHighscore, SpriteTable, TextSpritePlayer1, TextSpritePlayer2, TextSpritePlayer3, TextSpritePlayer4, TextSpritePlayer5, TextSpriteScorePlayer1, TextSpriteScorePlayer2, TextSpriteScorePlayer3, TextSpriteScorePlayer4, TextSpriteScorePlayer5
from project_dash.assets import AssetsLoader
from project_dash.dtos import GameOverDTO, SelectDTO, SoundDTO, SwitchSceneDTO, WarningDTO
from project_dash.services import DashService
from project_dash.sprites import ButtonSubject

import pygame as pg

import project_dash.config


class Scene:
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService, *buttons):
        self.button_subject = ButtonSubject([*buttons])
        self.subject_output = None
        self.dash_service = _dash_service

    def do_once(self):
        self.subject_output = None

    def play_keyboard_click(self, _event: pg.event.Event):
        # TBA - play a sound
        pass

    def play_mouse_click(self, _mouse_coords: tuple[int, int], _mouse_button: int):
        self.subject_output = self.button_subject.play_mouse_click(_mouse_coords, _mouse_button)

    def update(self, _dt: float, _mouse_coords: tuple[int, int]):
        if self.subject_output is not None:
            for dto in self.subject_output:
                if type(dto) is SwitchSceneDTO:
                    return dto

        self.button_subject.highlight_on_hover(_mouse_coords)


class SceneIntro(Scene):
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService):
        self.spr_intro = SpriteIntro(_assets_loader.img_intro, _all)

        Scene.__init__(self, _assets_loader, _all, _dash_service)

    def update(self, _dt: float, _mouse_coords: tuple[int, int]):
        Scene.update(self, _dt, _mouse_coords)
        ticks = pg.time.get_ticks()
        if ticks > 5000:
            return SwitchSceneDTO("main_menu")
        if ticks % 600 in range(0, 301):
            self.spr_intro.set_image(self.spr_intro.assets[0])
        else:
            self.spr_intro.set_image(self.spr_intro.assets[1])


class SceneMainMenu(Scene):
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService):
        self.buttonspr_continue = ButtonSpriteContinue(_assets_loader.img_continue, _all)
        self.spr_logo = SpriteLogo(_assets_loader.img_logo, _all)

        Scene.__init__(self, _assets_loader, _all, _dash_service, self.buttonspr_continue)


class SceneGameplay(Scene):
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService):
        self.spr_penguin = SpritePenguin(_assets_loader.img_penguin, _all)
        self.spr_tree = SpriteTree(_assets_loader.img_tree, _all)
        self.textspr_score = TextSpriteScore(_assets_loader.font_score, _all)
        self.sound_point = [_assets_loader.sound_point[0], _assets_loader.sound_point[1]]

        self.game_over = 0
        self.spr_game_over_message = SpriteGameOverMessage(_assets_loader.img_game_over_message, _all)
        self.textspr_game_over_score = TextSpriteGameOverScore(_assets_loader.font_score, _all)

        Scene.__init__(self, _assets_loader, _all, _dash_service)

    def do_once(self):
        Scene.do_once(self)
        self.game_over = 0
        self.spr_game_over_message.set_opacity(0)
        self.textspr_game_over_score.set_opacity(0)

    def play_keyboard_click(self, _event: pg.event.Event):
        Scene.play_keyboard_click(self, _event)
        
        if _event.key == pg.K_q:
            self.subject_output = [SwitchSceneDTO("highscore")]

    def play_mouse_click(self, _mouse_coords: tuple[int, int], _mouse_button: int):
        Scene.play_mouse_click(self, _mouse_coords, _mouse_button)
        self.dash_service.service_gameplay.play_mouse_click()
        
    def update(self, _dt: float, _mouse_coords: tuple[int, int]):
        if self.game_over == 1:
                pg.time.wait(2000)
                self.subject_output = [SwitchSceneDTO("highscore")]

        scene_update_output = Scene.update(self, _dt, _mouse_coords)
        if type(scene_update_output) == SwitchSceneDTO:
            return scene_update_output
        
        service_update_output = self.dash_service.service_gameplay.update()

        if type(service_update_output) == GameOverDTO:
            self.textspr_game_over_score.set_msg(f"Score: {service_update_output.final_score}")
            self.textspr_game_over_score.align("center_x", di["width"])
            self.textspr_game_over_score.set_opacity(255)
            self.spr_game_over_message.set_opacity(255)

            if self.game_over == 0:
                self.game_over = 1

        elif type(service_update_output) == SoundDTO:
            if service_update_output.score % 5 == 0:  # kalau skor 5, 10, 15, dst
                self.sound_point[0].play()
            else:  # kalau skor 1, 2, 3, 4, 6, dst
                self.sound_point[1].play()

        if self.dash_service.service_gameplay.player_logic.is_jumping:
            self.spr_penguin.set_image(self.spr_penguin.assets[1])
        else:
            self.spr_penguin.set_image(self.spr_penguin.assets[0])

        self.spr_penguin.update_image(self.dash_service.service_gameplay.player_logic.rect.x,
                                      self.dash_service.service_gameplay.player_logic.rect.y)
        
        self.spr_tree.update_image(self.dash_service.service_gameplay.tree_logic.rect.x,
                                      self.dash_service.service_gameplay.tree_logic.rect.y)

        self.textspr_score.set_msg(f"Score: {self.dash_service.service_gameplay.player_score}")


class SceneRegister(Scene):
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService):
        self.spr_tickbox_register = SpriteTickboxRegister(_assets_loader.img_register, _all)
        self.spr_tickbox_login = SpriteTickboxLogin(_assets_loader.img_login, _all)
        self.spr_text_register_username = SpriteTextRegisterUsername(_assets_loader.img_username, _all)
        self.spr_text_register_email = SpriteTextRegisterEmail(_assets_loader.img_email, _all)
        self.spr_text_login_username = SpriteTextLoginUsername(_assets_loader.img_username, _all)
        self.buttonspr_text_input_register_username = ButtonSpriteTextInputRegisterUsername(_assets_loader.img_text_input, _all)
        self.buttonspr_text_input_register_email = ButtonSpriteTextInputRegisterEmail(_assets_loader.img_text_input, _all)
        self.buttonspr_text_input_login_username = ButtonSpriteTextInputLoginUsername(_assets_loader.img_text_input, _all)
        self.textspr_register_username = TextSpriteRegisterUsername(_assets_loader.font_temp, _all)
        self.textspr_register_email = TextSpriteRegisterEmail(_assets_loader.font_temp, _all)
        self.textspr_login_username = TextSpriteLoginUsername(_assets_loader.font_temp, _all)
        self.textspr_warning = TextSpriteWarning(_assets_loader.font_temp, _all)
        self.buttonspr_play = ButtonSpritePlay(_assets_loader.img_play, self.textspr_warning, _dash_service, _all)
        
        self.register = [self.spr_tickbox_register, self.spr_text_register_username, self.spr_text_register_email,
                         self.buttonspr_text_input_register_username, self.buttonspr_text_input_register_email,
                         self.textspr_register_username, self.textspr_register_email]
        
        self.login = [self.spr_tickbox_login, self.spr_text_login_username, self.buttonspr_text_input_login_username,
                      self.textspr_login_username]

        self.text_register_username = []
        self.text_register_email = []
        self.text_login_username = []
        
        self.selected_textspr = self.textspr_register_username
        self.selected_text = self.text_register_username

        self.editing_username = True

        Scene.__init__(self, _assets_loader, _all, _dash_service, self.buttonspr_text_input_register_email,
                       self.buttonspr_text_input_register_username, self.buttonspr_text_input_login_username,
                       self.buttonspr_play)

    def do_once(self):
        Scene.do_once(self)
        self.buttonspr_text_input_register_username.set_image(self.buttonspr_text_input_register_username.assets[1])
        self.buttonspr_text_input_register_email.set_image(self.buttonspr_text_input_register_email.assets[0])
        self.buttonspr_text_input_login_username.set_image(self.buttonspr_text_input_login_username.assets[0])

        self.spr_tickbox_register.set_image(self.spr_tickbox_register.assets[0])
        self.spr_tickbox_login.set_image(self.spr_tickbox_login.assets[1])

        for sprite in self.register:
            sprite.set_opacity(255)
        for sprite in self.login:
            sprite.set_opacity(120)

        self.text_register_username.clear()
        self.text_register_email.clear()
        self.text_login_username.clear()

        self.buttonspr_play.is_register = True

        self.editing_username = True

    def play_keyboard_click(self, _event: pg.event.Event):
        Scene.play_keyboard_click(self, _event)
        
        if _event.key == pg.K_BACKSPACE:
            if len(self.selected_text) > 0:
                self.selected_text.pop(-1)  # hapus karakter terakhir
        else:
            self.selected_text.append(_event.unicode)  # tambah karakter ke urutan terakhir

        current_text = "".join(self.selected_text)
        if self.editing_username is True:
            self.buttonspr_play.username = current_text
        elif self.editing_username is False:
            self.buttonspr_play.email = current_text
        self.selected_textspr.set_msg(current_text)

    def play_mouse_click(self, _mouse_coords: tuple[int, int], _mouse_button: int):
        Scene.play_mouse_click(self, _mouse_coords, _mouse_button)

        if self.subject_output is not None:
            for dto in self.subject_output:
                if type(dto) is SelectDTO:
                    if dto.selected_name in ("register-email", "register-username"):
                        self.buttonspr_play.is_register = True

                        if dto.selected_name == "register-email":
                            self.editing_username = False
                            self.selected_textspr = self.textspr_register_email
                            self.selected_text = self.text_register_email

                            self.buttonspr_text_input_register_username.set_image(self.buttonspr_text_input_register_username.assets[0])
                            self.buttonspr_text_input_register_email.set_image(self.buttonspr_text_input_register_email.assets[1])
                            self.buttonspr_text_input_login_username.set_image(self.buttonspr_text_input_login_username.assets[0])
                        
                        else:
                            self.editing_username = True
                            self.selected_textspr = self.textspr_register_username
                            self.selected_text = self.text_register_username

                            self.buttonspr_text_input_register_username.set_image(self.buttonspr_text_input_register_username.assets[1])
                            self.buttonspr_text_input_register_email.set_image(self.buttonspr_text_input_register_email.assets[0])
                            self.buttonspr_text_input_login_username.set_image(self.buttonspr_text_input_login_username.assets[0])

                        self.spr_tickbox_register.set_image(self.spr_tickbox_register.assets[0])
                        self.spr_tickbox_login.set_image(self.spr_tickbox_login.assets[1])
                        for sprite in self.register:
                            sprite.set_opacity(255)
                        for sprite in self.login:
                            sprite.set_opacity(120)

                    elif dto.selected_name == "login":
                        self.editing_username = True
                        self.buttonspr_play.is_register = False

                        self.selected_textspr = self.textspr_login_username
                        self.selected_text = self.text_login_username

                        self.buttonspr_text_input_register_username.set_image(self.buttonspr_text_input_register_username.assets[0])
                        self.buttonspr_text_input_register_email.set_image(self.buttonspr_text_input_register_email.assets[0])
                        self.buttonspr_text_input_login_username.set_image(self.buttonspr_text_input_login_username.assets[1])

                        self.spr_tickbox_register.set_image(self.spr_tickbox_register.assets[1])
                        self.spr_tickbox_login.set_image(self.spr_tickbox_login.assets[0])
                        for sprite in self.register:
                            sprite.set_opacity(120)
                        for sprite in self.login:
                            sprite.set_opacity(255)
                
                elif type(dto) is WarningDTO:
                    self.textspr_warning.set_msg(dto.warning)
                    self.textspr_warning.align("center", di["width"])


class SceneHighScore(Scene):
    def __init__(self, _assets_loader: AssetsLoader, _all: pg.sprite.RenderUpdates, _dash_service: DashService):
        self.buttonspr_back = ButtonSpriteBack(_assets_loader.img_back, _all)
        self.spr_highscore = SpriteHighscore(_assets_loader.img_highscore, _all)
        self.spr_table = SpriteTable(_assets_loader.img_table, _all)
        self.txtspr_player_1 = TextSpritePlayer1(_assets_loader.font_temp, _all)
        self.txtspr_player_2 = TextSpritePlayer2(_assets_loader.font_temp, _all)
        self.txtspr_player_3 = TextSpritePlayer3(_assets_loader.font_temp, _all)
        self.txtspr_player_4 = TextSpritePlayer4(_assets_loader.font_temp, _all)
        self.txtspr_player_5 = TextSpritePlayer5(_assets_loader.font_temp, _all)
        self.txtspr_score_player_1 = TextSpriteScorePlayer1(_assets_loader.font_temp, _all)
        self.txtspr_score_player_2 = TextSpriteScorePlayer2(_assets_loader.font_temp, _all)
        self.txtspr_score_player_3 = TextSpriteScorePlayer3(_assets_loader.font_temp, _all)
        self.txtspr_score_player_4 = TextSpriteScorePlayer4(_assets_loader.font_temp, _all)
        self.txtspr_score_player_5 = TextSpriteScorePlayer5(_assets_loader.font_temp, _all)

        self.txt_players = [self.txtspr_player_1, self.txtspr_player_2, self.txtspr_player_3, self.txtspr_player_4, self.txtspr_player_5]
        self.txt_score_players = [self.txtspr_score_player_1, self.txtspr_score_player_2, self.txtspr_score_player_3, self.txtspr_score_player_4, self.txtspr_score_player_5]

        Scene.__init__(self, _assets_loader, _all, _dash_service, self.buttonspr_back)

    def do_once(self):
        Scene.do_once(self)
        temp_leaderboards: list = self.dash_service.service_highscore.get_leaderboards()

        for i in range(5):
            if i < len(temp_leaderboards):
                self.txt_players[i].set_msg(temp_leaderboards[i].username)
                self.txt_score_players[i].set_msg(str(temp_leaderboards[i].score))
            else:
                self.txt_players[i].set_msg("")
                self.txt_score_players[i].set_msg("")