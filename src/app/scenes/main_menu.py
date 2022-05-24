from engine import *
from engine.entities import *
from app import utils
from app.scenes import *

import pygame

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("Main Menu")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        background = Image(
            content.load_image("bg-main-menu.png"), (0, 0))
        logo = Image(
            content.load_image("game-logo.png"), (70, 80))
        label_version = Label(
            "Version 1.0.0a1 - For testing purposes only.", utils.fonts["sm"], pygame.Color("white"), (35, 555))
        label_copyright = Label(
            "© 2022 Pacific Tech", utils.fonts["sm"], pygame.Color("white"), (35, 565))
        self.timer = Timer(1500, True, True)
        def update_time():
            # label_version.set_text(str((self.timer.get_remaining())))
            alpha = 0 + (255 * (self.timer.get_elapsed() / self.timer.interval))
            label_copyright.set_text(str(alpha))
            label_version.get_surface().set_alpha(alpha)
        self.timer.on_tick = update_time

        button_new_game = Button.from_button(utils.button_default, "New Game")
        button_new_game.set_position((510, 100))
        def on_new_game_click():
            pass
            #game.scenes.set_scene(
        button_new_game.on_left_click = on_new_game_click

        self.entities = {
            "background": background,
            "logo": logo,
            "label_copyright": label_copyright,
            "label_version": label_version,
            "button_new_game": button_new_game,
        }
