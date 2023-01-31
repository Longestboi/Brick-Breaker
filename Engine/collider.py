
import pygame as pg
from .generic_maths import Rect, Position

class Collider:

    def __init__(self, hit_box: Rect, coll_pos: Position) -> None:
        self.is_drawing_collider = False
        self.hit_box: Rect = hit_box
        self.collider_position = coll_pos

    def on_collision(self):
        """ Function to handle what happens on collision """

    def collision_area(self) -> tuple:
        between = []

        # this could be optimized
        between.append(
            (
                self.collider_position.pos_x,
                self.hit_box.bottom_right_x + self.collider_position.pos_x
            )
        )

        between.append(
            (
                self.collider_position.pos_y,
                self.hit_box.bottom_right_y + self.collider_position.pos_y
            )
        )

        return tuple(between)

    def toggle_draw_collider(self):
        """ Toggle collider drawing """
        self.is_drawing_collider = not self.is_drawing_collider

    def render_collider(self, surf: pg.Surface, color: tuple):
        return pg.draw.rect(surf, color, self.hit_box.to_pygame(), 1)
