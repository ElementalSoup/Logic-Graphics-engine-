import pygame as pg
import sys

class OpeningScreen:
    def __init__(self, logo_path, audio_path, win_size):
        self.win_size = win_size
        
        # Initialize Pygame and set the display mode
        pg.init()
        self.screen = pg.display.set_caption("LOGiC")
        self.screen = pg.display.set_mode(self.win_size, flags=pg.DOUBLEBUF)

        self.logo = pg.image.load(logo_path).convert_alpha()
        self.audio_path = audio_path
        # Load and set window icon
        self.icon = pg.image.load('logic/logic.png')  # Replace with your icon path
        pg.display.set_icon(self.icon)
        
        self.fade_alpha = 255
        self.fade_speed = 5
        self.logo_pos = [self.win_size[0] // 2 - self.logo.get_width() // 2, -self.logo.get_height()]  # Start logo above the screen
        self.show_logo = True
        self.font = pg.font.Font(None, 74)
        self.start_button = pg.Rect((self.win_size[0]//2 - 100, self.win_size[1]//2 + 100, 200, 50))
        self.button_fill_color = (0, 0, 0)        # Black button fill color
        self.button_text_color = (255, 255, 255)  # White text color
        self.button_outline_color = (0, 0, 0)     # Black outline color
        self.button_alpha = 255

        # Make the mouse visible and not grabbed
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

    def play_audio(self):
        pg.mixer.music.load(self.audio_path)
        pg.mixer.music.play()

    def fade_in(self):
        if self.fade_alpha > 0:
            self.fade_alpha -= self.fade_speed
        else:
            self.fade_alpha = 0

    def animate_logo_drop(self):
        target_y = self.win_size[1] // 2 - 200
        current_y = self.logo_pos[1]
        distance = target_y - current_y
        if abs(distance) > 1:
            self.logo_pos[1] += distance * 0.075  # Adjust the factor (0.1) for desired animation speed

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen

        # Render logo with position adjustment
        self.screen.blit(self.logo, self.logo_pos)

        # Render fade effect
        overlay = pg.Surface(self.win_size)
        overlay.fill((255, 255, 255))
        overlay.set_alpha(self.fade_alpha)
        self.screen.blit(overlay, (0, 0))

        # Check if the mouse is over the button
        if self.start_button.collidepoint(pg.mouse.get_pos()):
            # Invert button colors on hover
            self.button_fill_color = (255, 255, 255)  # White button fill color
            self.button_text_color = (0, 0, 0)        # Black text color
            self.button_outline_color = (0, 0, 0)     # Black outline color
        else:
            self.button_fill_color = (0, 0, 0)        # Default black fill color
            self.button_text_color = (255, 255, 255)  # Default white text color
            self.button_outline_color = (0, 0, 0)     # Default black outline color

        # Draw the outline
        outline_rect = pg.Rect(self.start_button.left - 2, self.start_button.top - 2, self.start_button.width + 4, self.start_button.height + 4)
        pg.draw.rect(self.screen, self.button_outline_color, outline_rect)

        # Draw the filled button
        pg.draw.rect(self.screen, self.button_fill_color, self.start_button)

        start_text = self.font.render('START', True, self.button_text_color)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)

    def run(self):
        self.play_audio()
        while self.show_logo:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.show_logo = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        self.show_logo = False
            
            self.fade_in()
            self.animate_logo_drop()
            self.render()
            pg.display.flip()
            pg.time.delay(30)

        # Close the opening screen and return
        pg.quit()
