
import pygame as pg
from .generic_maths import Position
from .game_object import GameObject
from .color import COLORS

class ScoreBoard(GameObject):

    def __init__(self) -> None:
        self.board_width = 3
        self.board_height = 6
        self.position = Position(11 * 32, 2 * 32)
        self.collider = None

        super().__init__(self.collider, self.position)

        self.font: pg.font.Font

        self.score: int
        self.lives: int

        self.score_board_surf_base = pg.Surface(
            (self.board_width * 32, self.board_height * 32)
        ).convert_alpha()

        self.score_board_surf = self.score_board_surf_base.copy()

    def render(self, surf: pg.Surface):
        self.score_board_surf = self.score_board_surf_base.copy()

        next_y = 0

        score = self.font.render("Score:", False, COLORS["white"], COLORS["black"])
        self.score_board_surf.blit(
            score,
            (0, 0)
        )

        next_y += score.get_size()[1]

        score_rend = self.font.render(str(self.score), False, COLORS["white"], COLORS["black"])
        self.score_board_surf.blit(
            score_rend,
            ((self.board_width * 32) - score_rend.get_size()[0], next_y)
        )

        next_y += score_rend.get_size()[1]

        lives = self.font.render("Lives:", False, COLORS["white"], COLORS["black"])
        self.score_board_surf.blit(
            lives,
            (0, next_y)
        )

        next_y += lives.get_size()[1]

        lives_rend = self.font.render(str(self.lives), False, COLORS["white"], COLORS["black"])
        self.score_board_surf.blit(
            lives_rend,
            ((self.board_width * 32) - lives_rend.get_size()[0], next_y)
        )

        surf.blit(self.score_board_surf, self.position.get_tuple())
