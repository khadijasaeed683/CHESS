import pygame
import sys
import os

class InstructionsPage:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(os.path.join("images", "Instructions3.png"))
        self.background = pygame.transform.scale(self.background, (800, 600))  # Scale to fit the screen size
        self.font = pygame.font.Font(None, 40)
        self.large_font = pygame.font.Font(None, 60)
        self.buttons = {
            "Back": (300, 400),
            "Quit": (300, 470),
        }

    def draw_instructions(self):
        # Draw the background and title
        self.screen.blit(self.background, (0, 0))  # Display the background image
        #title = self.large_font.render("Instructions", True, pygame.Color("white"))
        #self.screen.blit(title, (400 - title.get_width() // 2, 50))  # Centered title

        # Display instruction text
        #instructions = [
        #    "Use arrow keys to move pieces.",
        #    "Press Enter to select options.",
        #    "Press ESC to quit a game.",
        #    "Enjoy the game!",
        #]
        # for i, line in enumerate(instructions):
        #     text = self.font.render(line, True, pygame.Color("white"))
        #     self.screen.blit(text, (50, 150 + i * 50))

        # Draw buttons
        for button_text, position in self.buttons.items():
            pygame.draw.rect(self.screen, pygame.Color("black"), (*position, 200, 50))
            button_label = self.font.render(button_text, True, pygame.Color("white"))
            self.screen.blit(
                button_label,
                (position[0] + 100 - button_label.get_width() // 2, position[1] + 15),
            )

    def handle_buttons(self, event, main_menu_callback):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            for button_text, position in self.buttons.items():
                rect = pygame.Rect(*position, 200, 50)
                if rect.collidepoint(mouse_pos):
                    if button_text == "Back":
                        return "main_menu"  # Indicate a return to the main menu
                    elif button_text == "Quit":
                        pygame.quit()
                        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                result = self.handle_buttons(event, None)
                if result == "main_menu":
                    return  # Exit the instructions loop and return to the main menu

            self.draw_instructions()
            pygame.display.flip()
            self.clock.tick(30)
