import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from opening_screen import OpeningScreen  # Import the OpeningScreen class

class GraphicsEngine:
    def __init__ (self, win_size=(1600,900)):
        # set window size variable
        self.WIN_SIZE = win_size
        self.fullscreen = False
        # light
        self.light = Light()
        # set color and brightness
        self.bg_brightness = 20 * .1
        self.bg_color = (0.1 * self.bg_brightness, 0.1 * self.bg_brightness, 0.15 * self.bg_brightness)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.dtime = 0

        # Initialize Pygame mixer
        pg.mixer.init()

        # Default music (replace with your default music file path)
        self.default_music = "music/bg.wav"
        self.current_music = None  # To track currently playing music

    def init_opengl(self):
        # Initialize Pygame and OpenGL context
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_caption("Graphics Engine", "Graphics Engine")
        
        # Load and set window icon
        self.icon = pg.image.load('logic/logic.png')
        pg.display.set_icon(self.icon)

        # Hide mouse cursor and grab input
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Create OpenGL context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

    def play_music(self, music_path):
        if self.current_music:
            pg.mixer.music.stop()
        self.current_music = music_path
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(-1)  # -1 plays the music indefinitely

    def play_default_music(self):
        self.play_music(self.default_music)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_F11:
                self.toggle_fullscreen()
            elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.toggle_mute()

    def toggle_fullscreen(self):
        if self.fullscreen:
            pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        else:
            pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN)
        self.fullscreen = not self.fullscreen

    def toggle_mute(self):
        if pg.mixer.music.get_volume() == 0.0:
            pg.mixer.music.set_volume(1.0)
        else:
            pg.mixer.music.set_volume(0.0)

    def render(self):
        # Clear the screen
        self.ctx.clear(color=self.bg_color)
        # Render the scene
        self.scene_renderer.render()
        # Swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        # Set initial window size
        opening_screen_size = (800, 600)
        
        # Run the opening screen
        opening_screen = OpeningScreen("logic/logic.png", "logic/logic.wav", opening_screen_size)
        opening_screen.run()

        # Initialize OpenGL after the opening screen
        self.init_opengl()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

        # Main game loop
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.dtime = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
