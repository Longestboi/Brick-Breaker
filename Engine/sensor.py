import pygame as pg

from .generic_maths import Position
from .game_object import GO_LIST, GameObject
from .color import COLORS

class Sensor:

    def __init__(self, pos: Position):
        self.position = pos

        self.is_sensor_enabled = True
        self.delta_time = float()
        self.timer = 0.3

        self.is_rendering_debug = True

    def check_if_colliding(self, ignore_class) -> tuple:

        if not self.is_sensor_enabled:
            return (False, None)

        for g_o in GO_LIST:

            # No need to check self
            if issubclass(type(g_o), ignore_class):
                continue

            if issubclass(type(g_o), GameObject):
                # Check if collider exists
                if isinstance(g_o.collider, type(None)):
                    continue

                tmp = g_o.collider.collision_area()
                if \
                    (self.position.pos_x >= tmp[0][0] and self.position.pos_x <= tmp[0][1]) and \
                    (self.position.pos_y >= tmp[1][0] and self.position.pos_y <= tmp[1][1]) \
                :
                    return (True, g_o)

        return (False, None)

    def move_sensor(self, pos: Position):
        self.position += pos

    def disable_sensor(self):
        self.is_sensor_enabled = False

    def on_frame(self):
        if not self.is_sensor_enabled:
            self.timer = self.timer - self.delta_time

            if self.timer <= 0:
                self.is_sensor_enabled = True
                self.timer = .3

    def render(self, surf: pg.Surface):
        if self.is_rendering_debug:
            pg.draw.rect(
                surf, COLORS['yellow'],
                pg.rect.Rect(self.position.pos_x, self.position.pos_y, 1, 1), 1
            )
