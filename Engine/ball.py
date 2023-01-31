import pygame as pg

from .game_object import GameObject, GO_LIST
from .game_board import GameBoard
from .collider import Collider
from .generic_maths import Position, Rect, Velocity
from .player import Player
from .sensor import Sensor

from .color import COLORS
from .audio_handler import AUDIOHANDLER


class Ball(GameObject):
    def __init__(self, pos: Position, vel: Velocity) -> None:
        self.game_board: GameBoard
        self.ball_diameter = 10
        self.ball_radius = self.ball_diameter / 2
        self.ball_velocity = vel
        self.is_ball_stable = False
        self.sens_pos = [Position(0, 0) for _ in range(4)]
        self.sens_list = [Sensor(Position(0, 0)) for _ in range(4)]

        hit_box = Collider(
            Rect(0, 0, self.ball_diameter, self.ball_diameter),
            pos
        )
        super().__init__(hit_box, pos)

        for i in GO_LIST:
            if isinstance(i, GameBoard):
                self.game_board = i

        self.setup_sensors_positions()
        self.update_sensor_pos()

        self.ball_surf_base = pg.Surface((self.ball_diameter, self.ball_diameter))
        pg.draw.circle(
            self.ball_surf_base,
            (255, 255, 255),
            (self.ball_radius, self.ball_radius),
            self.ball_radius
        )
        self.ball_surf = self.ball_surf_base.copy()

    def setup_sensors_positions(self):
        self.sens_pos[0] = Position(self.ball_radius, -3)
        self.sens_pos[1] = Position(self.ball_diameter + 2, self.ball_radius - 1)
        self.sens_pos[2] = Position(self.ball_radius, self.ball_diameter + 2)
        self.sens_pos[3] = Position(-3, self.ball_radius - 1)

        for i in self.sens_list:
            i.delta_time = self.delta_time

    def stop_out_of_bounds(self):
        for i, sens in enumerate(self.sens_list):
            if i in {0, 2}:
                if sens.position.pos_y <= 2 or \
                 sens.position.pos_y >= (self.game_board.board_height * 32) - 2:
                    sens.disable_sensor()
                    self.ball_velocity.flip_y_velocity()
                    AUDIOHANDLER.play_bounce()

                if sens.position.pos_y < 0:
                    sens.disable_sensor()
                    self.position += Position(5, 0)

                if sens.position.pos_y > self.game_board.board_height * 32:
                    sens.disable_sensor()
                    self.position -= Position(5, 0)

                continue

            if i in {1, 3}:
                if sens.position.pos_x <= 2 or \
                 sens.position.pos_x >= (self.game_board.board_width * 32) - 2:
                    sens.disable_sensor()
                    self.ball_velocity.flip_x_velocity()
                    AUDIOHANDLER.play_bounce()

                if sens.position.pos_x < 0:
                    sens.disable_sensor()
                    self.position += Position(5, 0)

                if sens.position.pos_x > self.game_board.board_height * 32:
                    sens.disable_sensor()
                    self.position -= Position(6, 0)

                continue

    def update_sensor_pos(self):
        for i, sens in enumerate(self.sens_list):
            sens.position = self.position.copy() + self.sens_pos[i]

    def collision_check(self):
        for i, sen in enumerate(self.sens_list):
            temp = sen.check_if_colliding((type(self), type(GameBoard)))

            if isinstance(temp[1], type(None)):
                continue

            def collider_handle(tst: Collider, sen: Sensor):
                col_area = tst.collision_area()
                if (sen.position.pos_x >= col_area[0][0] and sen.position.pos_x <= col_area[0][1]) and \
                    (sen.position.pos_y >= col_area[1][0] and sen.position.pos_y <= col_area[1][1]):
                    return True

                return False

            if temp[0]:
                if isinstance(temp[1], Player):
                    if i in {0, 2}:
                        tmp_collider1 = temp[1].left_hit
                        tmp_collider2 = temp[1].right_hit
                        if collider_handle(tmp_collider1, sen):
                            self.ball_velocity.vel_x = abs(self.ball_velocity.vel_x)
                            sen.disable_sensor()
                        if collider_handle(tmp_collider2, sen):
                            self.ball_velocity.vel_x = -abs(self.ball_velocity.vel_x)
                            sen.disable_sensor()
                        AUDIOHANDLER.play_bounce()


                if i in {0, 2}:
                    temp[1].on_collision()
                    self.ball_velocity.flip_y_velocity()

                if i in {1, 3}:
                    temp[1].on_collision()
                    self.ball_velocity.flip_x_velocity()

    def on_frame(self) -> None:

        self.update_sensor_pos()
        self.stop_out_of_bounds()
        self.collision_check()

        for i in self.sens_list:
            i.delta_time = self.delta_time
            i.on_frame()

        if not self.is_ball_stable:
            self.position -= self.ball_velocity * self.delta_time

    def render(self, surf: pg.Surface):

        if self.collider.is_drawing_collider:
            self.collider.render_collider(self.ball_surf, COLORS["red"])
            for sens in self.sens_list:
                sens.render(surf)
        else:
            self.ball_surf = self.ball_surf_base.copy()

        surf.blit(
            self.ball_surf,
            self.position.get_tuple()
        )
