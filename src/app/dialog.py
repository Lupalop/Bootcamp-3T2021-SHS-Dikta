from engine import *
from engine.entities import *
from app import utils

from engine.entities import ClickableEntity, Label
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame
from queue import Queue

RECT_NAME = pygame.Rect(0, 0, 155, 38)
RECT_BASE = pygame.Rect(0, RECT_NAME.height, 765, 90)
RECT_SPEECH = pygame.Rect(20, RECT_NAME.height, RECT_BASE.width - 140, RECT_BASE.height)
RECT_DIALOG = pygame.Rect(0, 0, RECT_BASE.width, RECT_NAME.height + RECT_BASE.height)
RECT_PORTRAIT = pygame.Rect(RECT_DIALOG.x, RECT_DIALOG.y, RECT_DIALOG.height, RECT_DIALOG.height)
RECT_NAME_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_NAME.y, RECT_NAME.width, RECT_NAME.height)
RECT_SPEECH_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_SPEECH.y, RECT_SPEECH.width, RECT_SPEECH.height)

class Dialog(ClickableEntity):
    def __init__(self, emitter, position, name, text, portrait_id = None, callback = None):
        super().__init__(
            position,
            RECT_DIALOG.size,
            pygame.Surface(RECT_DIALOG.size, pygame.SRCALPHA, 32)
        )

        self.emitter = emitter
        self.callback = callback

        rect_speech_final = RECT_SPEECH
        rect_name_final = RECT_NAME
        # Determine if we have a portrait and adjust position accordingly
        self.portrait = None
        if portrait_id:
            self.portrait = Image(utils.load_ca_image(portrait_id), RECT_PORTRAIT)
            rect_speech_final = RECT_SPEECH_WP
            rect_name_final = RECT_NAME_WP
        # Draw boxes to entity surface
        self.box_name = utils.load_ui_image("dialog-box-nametag")
        self._surface.blit(self.box_name, rect_name_final)
        self.box_base = utils.load_ui_image("dialog-box-main")
        self._surface.blit(self.box_base, RECT_BASE)
        # Initialize name tag and its position
        self.label_name = Label(name, utils.get_font(28), pygame.Color("white"))
        label_name_pos = (
            position[0] + rect_name_final.x + (rect_name_final.width / 2) - self.label_name.get_rect().width / 2,
            position[1] + rect_name_final.y + (rect_name_final.height / 2) - self.label_name.get_rect().height / 2
        )
        self.label_name.set_position(label_name_pos)
        # Initialize speech text and its position
        self.label_speech = Label(text, utils.get_font(24), pygame.Color("white"))
        label_speech_pos = (
            position[0] + rect_speech_final.x,
            position[1] + rect_speech_final.y + (rect_speech_final.height / 2) - self.label_speech.get_rect().height / 2
        )
        self.label_speech.set_position(label_speech_pos)
        # Draw portrait to entity surface
        if self.portrait:
            self.portrait.draw(self._surface)

    @classmethod
    def from_entity(cls, entity, name, text):
        entity_copy = cls(name,
                          text,
                          entity.get_position())
        return entity_copy

    def set_position(self, position):
        raise("Changing the position of a dialog is not allowed.")

    def set_rect(self, rect):
        raise("Changing the rectangle of a dialog is not allowed.")

    def set_size(self, size):
        raise("Changing the size of a dialog is not allowed.")

    def set_surface(self, texture):
        raise("Changing the surface of a dialog is not allowed.")

    # Event handlers
    def _on_click(self, button):
        self.emitter.next()
        super()._on_click(button)

    def draw(self, layer):
        super().draw(layer)
        self.label_speech.draw(layer)
        self.label_name.draw(layer)

class DialogSide(IntEnum):
    TOP = 1
    BOTTOM = 2

RECT_DISPLAY = pygame.Rect(0, 0, 1360, 765) # FIXME: this should not be hardcoded

class DialogEmitter():
    def __init__(self):
        self._queue = Queue()
        self.current = None

    def next(self):
        if self.current and self.current.callback:
            self.current.callback()
        if not self._queue.empty():
            self.current = self._queue.get()
        else:
            self.current = None

    def update(self, game, events):
        if not self.current:
            self.next()
        if self.current:
            self.current.update(game, events)
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_KP_ENTER or \
                       event.key == pygame.K_RETURN or \
                       event.key == pygame.K_SPACE:
                        self.next()

    def draw(self, layer):
        if self.current:
            self.current.draw(layer)

    def add(self, side, name, text, portrait_id = None, callback = None):
        position = (0, 0)
        dialog_center = (RECT_DISPLAY.width / 2) - (RECT_DIALOG.width / 2)
        if side == DialogSide.TOP:
            position = (dialog_center, 25)
        elif side == DialogSide.BOTTOM:
            position = (dialog_center, RECT_DISPLAY.height - 60 - RECT_DIALOG.height)
        else:
            raise("unexpected dialog side")
        dialog = Dialog(self, position, name, text, portrait_id, callback)
        self._queue.put(dialog)
        if not self.current:
            self.next()