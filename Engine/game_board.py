
import pygame as pg
from .generic_maths import Position
from .game_object import GameObject

class GameBoard(GameObject):

    def __init__(self) -> None:
        self.board_width = 8
        self.board_height = 16
        self.position = Position(32, 32 * 2)
        self.collider = None

        super().__init__(self.collider, self.position)

        self.game_board_surf_base = pg.Surface(
            (self.board_width * 32, self.board_height * 32)
        ).convert_alpha()

        self.game_board_surf = self.game_board_surf_base.copy()

    def render(self, surf: pg.Surface):

        surf.blit(
            self.game_board_surf,
            self.position.get_tuple()
        )

        self.game_board_surf = self.game_board_surf_base.copy()
