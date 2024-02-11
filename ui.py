from math import ceil
from kink import di, inject

from project_dash.assets import AssetsLoader
from project_dash.dtos import SwitchSceneDTO
from project_dash.scenes import SceneIntro, SceneMainMenu, SceneRegister, SceneGameplay, SceneHighScore
from project_dash.services import DashService

import pygame as pg

import project_dash.config


@inject
class DashUI:
    def __init__(self, _service: DashService): 
        self.service = _service

    def run(self):
        pg.init()

        # Set mixer
        if pg.mixer and not pg.mixer.get_init():
            print("[DEBUG] Warning, no sound!")
            pg.mixer = None

        # Set the display mode
        screen_rect = pg.Rect(0, 0, di["width"], di["height"])
        screen = pg.display.set_mode((di["width"], di["height"]))
        pg.display.set_caption("Dashing through the Snow V1.0")

        # Load images, assign to sprite classes
        assets = AssetsLoader()

        # Set the clock
        clock = pg.time.Clock()

        # Set the background
        bgdtile = assets.img_bg[0]
        scroll = 0
        tiles = ceil(di["width"] / bgdtile.get_width()) + 50  # awalnya 1
        background = pg.Surface((di["width"], di["height"]))
        # for x in range(0, di["width"], bgdtile.get_width()):
        #     background.blit(bgdtile, (x, 0))
        # screen.blit(background, (0, 0))

        # Initialize game groups
        group_intro = pg.sprite.RenderUpdates()
        group_main_menu = pg.sprite.RenderUpdates()
        group_register = pg.sprite.RenderUpdates()
        group_gameplay = pg.sprite.RenderUpdates()
        group_highscore = pg.sprite.RenderUpdates()

        # Initialize scenes
        scene_intro = SceneIntro(assets, group_intro, self.service)
        scene_main_menu = SceneMainMenu(assets, group_main_menu, self.service)
        scene_register = SceneRegister(assets, group_register, self.service)
        scene_gameplay = SceneGameplay(assets, group_gameplay, self.service)
        scene_highscore = SceneHighScore(assets, group_highscore, self.service)

        # Play background music
        pg.mixer.music.load(di["bgm"])
        pg.mixer.music.play(-1)
        print(f"{di['bgm'] = }")

        # Run the main loop
        current_scene = scene_intro
        previous_group = group_intro

        current_group = previous_group

        running = True
        do_once = True
        while running:
            # For CPU optimization
            ## https://www.pygame.org/docs/ref/time.html#pygame.time.wait
            ## https://pygame-users.seul.narkive.com/72cJeMuv/pygame-why-does-pygame-get-so-high-cpu-usage
            pg.time.wait(10)

            # Scroll the background
            ## Append the image to the back of the same image
            clock.tick(30)
            i = 0
            while i < tiles:
                background.blit(bgdtile, (bgdtile.get_width() * i + scroll, 0)) 
                i += 1
            ## Frame for scrolling
            scroll -= 30  # Semakin besar, semakin cepat; awalnya 6
            ## Reset the scroll frame 
            if abs(scroll) > bgdtile.get_width(): 
                scroll = 0
            screen.blit(background, (0, 0))

            # Perform specific action(s) only once after loading a scene
            if do_once:
                current_scene.do_once()
            do_once = False

            # Grab the mouse coordinates
            mouse_coords = pg.mouse.get_pos()

            # Listen for events
            ## https://www.pygame.org/docs/ref/event.html#pygame.event.wait
            ## Continue once no event has entered the queue in the last 50 milliseconds
            event = pg.event.wait(50)
            if event.type == pg.QUIT:
                # Exit the program
                # https://stackoverflow.com/a/19882744
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_button = event.button
                current_scene.play_mouse_click(mouse_coords, mouse_button)
            elif event.type == pg.KEYDOWN:
                # current_scene.play_keyboard_click(pg.key.name(event.key))
                current_scene.play_keyboard_click(event)

            # Clear/erase the last drawn sprite_objects
            previous_group.clear(screen, background)
            current_group.clear(screen, background)

            # Update scene every tick
            ## https://stackoverflow.com/a/44035094/22699824
            dt = clock.tick(30) / 1000
            update_output = current_scene.update(dt, mouse_coords)

            if update_output is not None:
                if type(update_output) is SwitchSceneDTO:  # Switch to another scene if required
                    previous_group = current_group
                    do_once = True

                    print("BBB", update_output.scene_name)

                    if update_output.scene_name == "intro":
                        current_group = group_intro
                        current_scene = scene_intro

                    elif update_output.scene_name == "main_menu":
                        current_group = group_main_menu
                        current_scene = scene_main_menu

                    elif update_output.scene_name == "register":
                        current_group = group_register
                        current_scene = scene_register

                    elif update_output.scene_name == "gameplay":
                        current_group = group_gameplay
                        current_scene = scene_gameplay

                    elif update_output.scene_name == "highscore":
                        print("AAA")
                        current_group = group_highscore
                        current_scene = scene_highscore

                    # Reset the current scene DTO
                    update_output = None

                # elif type(update_output) is CandidateNumDTO:
                #     self.service.increase_one_vote(update_output)

            # Update sprite objects
            current_group.update(dt)

            # Draw the scene
            ## https://www.pygame.org/docs/tut/newbieguide.html
            current_group.draw(screen)
            pg.display.flip()

        pg.quit()  