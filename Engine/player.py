
import pygame as pg

from .game_object import GameObject
from .collider import Collider
from .generic_maths import Position, Rect

from .color import COLORS

PLAYER_IMAGE = pg.image.load("Images/Player.png")

class Player(GameObject):

    def __init__(self, pos: Position) -> None:
        self.player_width = 48
        self.player_height = 16
        hit_box = Collider(
            Rect(0, 0, self.player_width, self.player_height),
            pos
        )

        super().__init__( hit_box, pos )

        self.left_hit = Collider(
            Rect(0, 0, self.player_width / 2, self.player_height),
            pos.copy()
        )
        self.right_hit = Collider(
            Rect(self.player_width / 2, 0, self.player_width / 2, self.player_height),
            pos.copy() + Position(0, self.player_height)
        )

        self.right_hit.is_drawing_collider = self.left_hit.is_drawing_collider = True

        self.player_surf_base = pg.Surface((self.player_width, self.player_height))
        self.player_surf_base.blit(PLAYER_IMAGE.convert(), (0, 0))
        self.player_surf = self.player_surf_base.copy()

    def on_collision(self):
        pass

    def on_frame(self) -> None:
        self.left_hit.collider_position = self.position.copy()
        self.right_hit.collider_position = self.position.copy() + Position(self.player_width / 2, 0)

    def render(self, surf: pg.Surface):

        if self.collider.is_drawing_collider:
            self.collider.render_collider(self.player_surf, COLORS["red"])
            self.left_hit.render_collider(self.player_surf, COLORS["orange"])
            self.right_hit.render_collider(self.player_surf, COLORS["blue"])
        else:
            self.player_surf = self.player_surf_base.copy()

        surf.blit(
            self.player_surf,
            self.position.get_tuple()
        )
