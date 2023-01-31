
import inspect
import os

import pygame as pg
from .game_board import GameBoard
from .score_board import ScoreBoard
from .generic_maths import Position, Velocity

from .game_object import GO_LIST
from .color import COLORS
from .audio_handler import AUDIOHANDLER

from .block import Block
from .player import Player
from .ball import Ball

class GameLogic:

    def __init__(self) -> None:
        self.delta_time = float()
        self.current_event = pg.event.get()
        self.game_board = GameBoard()
        self.score_board = ScoreBoard()
        self.score_board.lives = 3
        self.score_board.score = 0
        self.pop_up_timer = 5
        self.game_over = False
        self.win = False
        tmp_surf = pg.Surface(self.game_board.game_board_surf.get_size())

        self.game_board.game_board_surf.blit(tmp_surf, (0, 0))

        self.player = Player(
            Position(
                int(self.game_board.board_width / 2) * 32,
                (self.game_board.board_height - 1) * 32
            )
        )

        self.initial_ball_vel = Velocity(200, 200)
        self.initial_ball_pos = Position(0, 0)
        self.ball_launch_mode = True

        self.ball = Ball(Position(0, 0), self.initial_ball_vel.copy())

        self.reset_ball()

        self.ball.game_board = self.game_board

        self.block_grid = []

        self.init_game()

        self.pop_up_text: pg.Surface

    def init_game(self):
        self.reset_ball()

        self.pop_up_text = None

        for i, g_o in enumerate(GO_LIST):
            if isinstance(g_o, Block):
                GO_LIST.remove(g_o)
                g_o.__del__()

        self.block_grid.clear()

        for i, y_pos in enumerate(reversed(range(8))):
            tmp = []

            for x in range(8):
                test = Block(Position(x * 32, 32 + (y_pos * 16)))
                test.big_list = self.block_grid
                test.score = (i + 1) * 10
                test.score_board = self.score_board
                test.set_brick_color(COLORS[y_pos % 7], .7)
                tmp.append(test)

            self.block_grid.append(tmp)

        # Set the position of the player to the proper position
        self.player.collider.collider_position = self.player.position = Position(
            (self.game_board.board_width * 32 / 2) - self.player.player_width / 2,
            self.player.position.pos_y
        )

        self.pop_up_timer = 5
        self.score_board.lives = 3

        self.game_over = False
        self.win = False

    def on_app_init(self):
        # Import font
        self.score_board.font = pg.font.Font(
            f"{os.path.dirname(inspect.stack()[1][1])}/Images/PixelEmulator.ttf",
            18
        )

    def handle_user_input(self):
        keys = pg.key.get_pressed()

        if self.game_over or self.win:
            return

        if keys[pg.K_a]:
            sub_potential = self.player.position.pos_x - 350 * self.delta_time

            if sub_potential > 0:
                self.player.position.pos_x = sub_potential

        if keys[pg.K_d]:
            add_potential = self.player.position.pos_x + 350 * self.delta_time

            if add_potential < (self.game_board.board_width * 32) - self.player.player_width:
                self.player.position.pos_x = add_potential

        if keys[pg.K_SPACE] and self.ball_launch_mode:
            self.ball_launch_mode = not self.ball_launch_mode
            AUDIOHANDLER.play_ball_launch()

    def reset_ball(self):

        self.initial_ball_pos = self.player.position.copy() + Position(
            (self.player.player_width / 2) - self.ball.ball_radius,
            -15
        )

        self.ball_launch_mode = True
        self.ball.position = self.initial_ball_pos.copy()
        self.ball.ball_velocity = self.initial_ball_vel.copy()

    def launch_ball(self):

        if self.ball_launch_mode:
            self.ball.position = self.player.position.copy() + Position(
                (self.player.player_width / 2) - self.ball.ball_radius,
                -15
            )

    def on_game_over(self):
        # weird way of layout, but I'm not refactoring it
        if self.score_board.lives == 0:
            if not self.game_over:
                AUDIOHANDLER.play_game_over()
            self.game_over = True

        if self.game_over:
            self.pop_up_timer -= self.delta_time
            self.pop_up_text = self.score_board.font.render(
                "GAME OVER", False,
                COLORS["white"], COLORS["black"]
            )

            if self.pop_up_timer <= 0:
                self.score_board.score = 0
                self.init_game()

    def on_win(self):

        if self.win:
            self.pop_up_timer -= self.delta_time
            self.pop_up_text = self.score_board.font.render(
                "YOU WIN!!!", False,
                COLORS["white"], COLORS["black"]
            )

            self.reset_ball()

            if self.pop_up_timer <= 0:
                self.init_game()

    def on_frame(self):
        # Delta_time Updates
        for g_o in GO_LIST:
            g_o.delta_time = self.delta_time

        self.handle_user_input()

        # On_frames of all game objects
        for g_o in GO_LIST:
            g_o.on_frame()

        self.launch_ball()

        if self.ball.position.pos_y - self.player.player_height > self.player.position.pos_y:
            self.reset_ball()
            AUDIOHANDLER.play_ball_lost()
            self.score_board.lives -= 1

        self.on_game_over()

        num_block = 0
        for i in self.block_grid:
            for j in i:
                if j:
                    num_block += 1

        if num_block == 0:
            if not self.win:
                AUDIOHANDLER.play_win()
            self.win = True
            self.on_win()

        # Render on game logic
        self.render()

    def render(self):
        # Loop through game object list to render them
        for g_o in GO_LIST:
            g_o.render(self.game_board.game_board_surf)

        if not self.game_over and not self.win:
            return

        self.game_board.game_board_surf.blit(
            self.pop_up_text,
            (
                ((self.game_board.board_width * 32) / 2) - (self.pop_up_text.get_size()[0] / 2),
                ((self.game_board.board_height * 32) / 2) - (self.pop_up_text.get_size()[1] /2)
            )
        )
