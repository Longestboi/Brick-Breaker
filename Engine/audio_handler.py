import pygame as pg

class AudioHandler:
    """ Audio handling class, for ease of playing sounds. """
    def __init__(self):
        pg.mixer.init()

        self.is_sound_muted: bool = False

        # Sound effects
        self.block_break = pg.mixer.Sound("Audio/BlockBreak.wav")
        self.block_break.set_volume(.2)

        self.ball_launch = pg.mixer.Sound("Audio/BallLaunch.wav")
        self.ball_launch.set_volume(.2)

        self.ball_lost = pg.mixer.Sound("Audio/BallLost.wav")
        self.ball_lost.set_volume(.2)

        self.bounce = pg.mixer.Sound("Audio/Bounce.wav")
        self.bounce.set_volume(.2)

        self.game_over = pg.mixer.Sound("Audio/GameOver.wav")
        self.game_over.set_volume(.2)

        self.win = pg.mixer.Sound("Audio/Win.wav")
        self.win.set_volume(.2)

    def play_block_break_sound(self):
        """ For playing block break sound. """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.block_break)

    def play_ball_launch(self):
        """ For playing the ball launch sound """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.ball_launch)

    def play_ball_lost(self):
        """ For playing the ball lost sound. """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.ball_lost)

    def play_bounce(self):
        """ For playing the bounce sound. """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.bounce)

    def play_game_over(self):
        """ For playing the game over sound. """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.game_over)

    def play_win(self):
        """ For playing the win sound. """
        if self.is_sound_muted:
            return

        pg.mixer.Sound.play(self.win)

    def toggle_sound_mute(self):
        self.is_sound_muted = not self.is_sound_muted

AUDIOHANDLER = AudioHandler()
""" Global audio handler, so functions can be called from anywhere. """