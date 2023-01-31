
import pygame as pg

from .game_object import GameObject
from .score_board import ScoreBoard
from .collider import Collider
from .generic_maths import Position, Rect

from .color import COLORS, overlay_color_on_surface
from .audio_handler import AUDIOHANDLER

BRICK_IMAGE = pg.image.load("Images/brick.png")

class Block(GameObject):

    def __init__(self, pos: Position) -> None:
        self.block_width = 32
        self.block_height = 16
        self.score_board: ScoreBoard
        self.big_list: list
        hit_box = Collider(Rect(0, 0, self.block_width, self.block_height), pos)
        super().__init__(hit_box, pos)

        self.score = 0

        self.block_surf_base = pg.Surface((self.block_width, self.block_height))
        # Copy block surface to buffer.
        # Without the copy block_surf_buffer is effectively a pointer.
        self.block_surf = self.block_surf_base.copy()
        self.set_brick_color(COLORS[0])

    def on_collision(self):
        self.score_board.score += self.score
        AUDIOHANDLER.play_block_break_sound()
        for i in self.big_list:
            try: 
                i.remove(self)
            except ValueError:
                pass
        super().__del__()

    def set_brick_color(self, color: tuple, intensity: int = .5):
        self.block_surf_base.blit(BRICK_IMAGE.convert(), (0, 0))
        self.block_surf_base = overlay_color_on_surface(self.block_surf_base, color, intensity)
        self.block_surf = self.block_surf_base.copy()

    def on_frame(self) -> None:

        
        pass

    def render(self, surf: pg.Surface):
        if self.collider.is_drawing_collider:
            self.collider.render_collider(self.block_surf, COLORS["red"])
        else:
            self.block_surf = self.block_surf_base.copy()

        surf.blit(
            self.block_surf,
            self.position.get_tuple()
        )
