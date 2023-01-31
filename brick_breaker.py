import pygame as pg

from Engine.game_logic import GameLogic
from Engine.game_object import GO_LIST, GameObject
from Engine.player import Player

class BrickBreaker:
    """ Main application class """

    def __init__(self) -> None:
        self.is_application_running = True
        self.height = 640
        self.width = 480
        self.resolution = (self.width, self.height)

        self.screen = pg.display.set_mode(self.resolution)
        self.background_image = pg.image.load("Images/BKG.png").convert()

        self.clock = pg.time.Clock()
        self.game_logic = GameLogic()

    def application_init(self):
        """ Initialization for application """
        pg.init()
        pg.font.init()
        pg.display.set_caption("Brick Breaker")

    def event_handler(self, program_event: pg.event):
        """ Event handler function """

        if program_event.type == pg.QUIT:
            self.is_application_running = False

        self.debug_events(program_event)

    def debug_events(self, program_event: pg.event):
        if program_event.type == pg.KEYDOWN:
            if program_event.key == pg.K_o:
                for g_o in GO_LIST:
                    if issubclass(type(g_o), GameObject):
                        if isinstance(g_o.collider, type(None)):
                            continue
                        g_o.collider.toggle_draw_collider()

            if program_event.key == pg.K_p:
                for g_o in GO_LIST:
                    if isinstance(g_o, Player):
                        print(g_o.collider.collision_area())

            if program_event.key == pg.K_q:
                self.is_application_running = False

    def render_frame(self):
        """ Do render on every frame """
        self.screen.blit(self.background_image, (0, 0))

        self.game_logic.game_board.render(self.screen)
        self.game_logic.score_board.render(self.screen)
        pg.display.flip()

    def application_start(self):
        """ Start the application function """

        if self.application_init() is False:
            self.is_application_running = False

        self.game_logic.on_app_init()

        # Main Loop
        while self.is_application_running:
            for event in pg.event.get():
                self.event_handler(event)

            self.game_logic.on_frame()

            self.render_frame()
            self.game_logic.delta_time = self.clock.tick(60) / 1000

def main():
    """ Main function """
    app = BrickBreaker()
    app.application_start()

if __name__ == "__main__":
    main()
