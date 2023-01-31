import pygame as pg

from .generic_maths import Position
from .collider import Collider

GO_LIST = []

class GameObject:
    def __init__(self, hit_box: Collider, pos: Position) -> None:
        self.position = pos
        self.collider = hit_box
        self.delta_time = float()
        GO_LIST.append(self)

    def __del__(self):
        # Should probably handle exceptions here
        try:
            for i, g_o in enumerate(GO_LIST):
                if self == g_o:
                    GO_LIST.pop(i)
        except:
            print(self)

        del self

    def on_frame(self):
        pass

    def render(self, surf: pg.Surface):
        pass
