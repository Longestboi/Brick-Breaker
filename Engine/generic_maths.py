import pygame as pg

class Rect:

    def __init__(self,
        top_left_x: int, top_left_y: int,
        bottom_right_x: int, bottom_right_y: int
    ) -> None:
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y

    def to_pygame(self) -> pg.Rect:
        return pg.Rect(
            self.top_left_x, self.top_left_y,
            self.bottom_right_x, self.bottom_right_y
        )

class Position:

    def __init__(self, x: int, y: int) -> None:
        self.pos_x = x
        self.pos_y = y

    def get_tuple(self) -> tuple:
        """ Return tuple of position """
        return (self.pos_x, self.pos_y)

    def copy(self):
        return Position(self.pos_x, self.pos_y)

    def __str__(self):
        return f"X: {self.pos_x}, Y: {self.pos_y}"

    def __add__(self, other):
        if isinstance(other, Position):
            self.pos_x += other.pos_x
            self.pos_y += other.pos_y
            return Position(self.pos_x, self.pos_y)

        if isinstance(other, Velocity):
            self.pos_x += other.vel_x
            self.pos_y += other.vel_y
            return self

    def __sub__(self, other):
        if isinstance(other, Position):
            self.pos_x -= other.pos_x
            self.pos_y -= other.pos_y
            return self

        if isinstance(other, Velocity):
            self.pos_x -= other.vel_x
            self.pos_y -= other.vel_y
            return self

    def __mul__(self, other):
        if isinstance(other, int):
            self.pos_x *= other
            self.pos_y *= other
            return self

        if isinstance(other, Position):
            self.pos_x *= other.pos_x
            self.pos_y *= other.pos_y
            return self

        if isinstance(other, Velocity):
            self.pos_x *= other.vel_x
            self.pos_y *= other.vel_y
            return self

class Velocity:

    def __init__(self, vel_x: int, vel_y: int):
        self.vel_x = vel_x
        self.vel_y = vel_y

    def copy(self):
        return Velocity(self.vel_x, self.vel_y)

    def flip_x_velocity(self):
        self.vel_x = - self.vel_x

    def flip_y_velocity(self):
        self.vel_y = - self.vel_y

    def __sub__(self, other):
        self.vel_x -= other.vel_x
        self.vel_y -= other.vel_y

    def __mul__(self, other):
        if isinstance(other, float):
            return Velocity(self.vel_x * other, self.vel_y * other)

    def __str__(self):
        return f"X_Vel: {self.vel_x}, Y_Vel: {self.vel_y}"
