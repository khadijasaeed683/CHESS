import pygame
import sys
from UI import main as backend_main  # Import backend main function
from instructions import InstructionsPage

class MainMenu:
    MAIN_MENU = 0
    GAME_MODE_MENU = 1  #human vs HUman or Human vs AI
    NAME_ENTRY_MENU = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Chess Game Menu")
        self.clock = pygame.time.Clock()
        self.HeadingFont = pygame.font.SysFont("verdana", 65, bold=True)
        self.font = pygame.font.SysFont("timesnewroman", 40)
        self.small_font = pygame.font.SysFont("timesnewroman", 30)

        try:
            self.background_image = pygame.image.load("Images/chessbg6.jpg")
            self.background_image = pygame.transform.scale(self.background_image, (800, 600))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit()

        self.options = ["Start Game", "Instructions", "Quit"]
        self.selected_option = 0
        self.game_mode_options = ["Human vs Human", "Human vs AI"]
        self.selected_game_mode = 0
        self.names = {"Player 1": "", "Player 2": ""}
        self.name_limit = 20
        self.input_focus = "Player 1"
        self.start_button_visible = False
        self.menu_state = self.MAIN_MENU
        self.game_types = ["classic", "professional", "rapid"]  # Define game types list
        self.selected_game_type_index = 0  # Default to the first game type in the list
        self.hovered_over_dropdown = False

    def draw_menu(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the title
        title = self.HeadingFont.render("Chess", True, pygame.Color("white"))
        self.screen.blit(title, (800 // 2 - title.get_width() // 2, 50))

        if self.menu_state == self.MAIN_MENU:
            # Draw main menu options
            for i, option in enumerate(self.options):
                color = pygame.Color("yellow") if i == self.selected_option else pygame.Color("white")
                text = self.font.render(option, True, color)
                self.screen.blit(text, (800 // 2 - text.get_width() // 2, 200 + i * 100))

        elif self.menu_state == self.GAME_MODE_MENU:
            # Draw game mode selection options
            for i, option in enumerate(self.game_mode_options):
                color = pygame.Color("yellow") if i == self.selected_game_mode else pygame.Color("white")
                text = self.font.render(option, True, color)
                self.screen.blit(text, (800 // 2 - text.get_width() // 2, 200 + i * 100))

        elif self.menu_state == self.NAME_ENTRY_MENU:
            # Title for name entry screen
            title = self.font.render("Enter Player Names", True, pygame.Color("white"))
            self.screen.blit(title, (800 // 2 - title.get_width() // 2, 140))

            # Player name input prompts
            player1_prompt = self.small_font.render("Player 1 Name: ", True, pygame.Color("white"))
            player2_prompt = self.small_font.render("Player 2 Name: ", True, pygame.Color("white"))
            self.screen.blit(player1_prompt, (50, 200))
            self.screen.blit(player2_prompt, (50, 300))

            # Draw text boxes for player names
            pygame.draw.rect(self.screen, pygame.Color("white"), (250, 200, 500,                        50), 2)
            pygame.draw.rect(self.screen, pygame.Color("white"), (250, 300, 500, 50), 2)

            # Display current names typed
            player1_text = self.small_font.render(self.names["Player 1"], True, pygame.Color("white"))
            player2_text = self.small_font.render(self.names["Player 2"], True, pygame.Color("white"))
            self.screen.blit(player1_text, (260, 210))
            self.screen.blit(player2_text, (260, 310))

            # Draw the "Game Type" label
            game_type_label = self.small_font.render("Game Type: ", True, pygame.Color("white"))
            self.screen.blit(game_type_label, (50, 375))  # Position the label to the left of the dropdown

            # Draw the dropdown for selecting game type
            game_type_colors = {
                "classic": pygame.Color("green"),
                "professional": pygame.Color("blue"),
                "rapid": pygame.Color("red")
            }

            # Get the color for the selected game type
            dropdown_color = game_type_colors.get(self.game_types[self.selected_game_type_index], pygame.Color("gray"))

            # Make the dropdown more interactive
            dropdown_rect = pygame.Rect(250, 375, 500, 50)

            # Highlight the dropdown when hovered over
            if self.hovered_over_dropdown:
                pygame.draw.rect(self.screen, pygame.Color("lightgray"), dropdown_rect)
            else:
                pygame.draw.rect(self.screen, dropdown_color, dropdown_rect)

            # Draw border around the dropdown
            pygame.draw.rect(self.screen, pygame.Color("white"), dropdown_rect, 2)
            
            # Render selected game type text on the left inside the dropdown
            selected_game_type_text = self.small_font.render(self.game_types[self.selected_game_type_index], True, pygame.Color("black"))
            self.screen.blit(selected_game_type_text, (dropdown_rect.x + 10, dropdown_rect.y + 10))

            # Add a small arrow on the right side of the dropdown
            arrow = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.polygon(arrow, pygame.Color("white"), [(10, 0), (0, 10), (20, 10)])
            self.screen.blit(arrow, (dropdown_rect.x + dropdown_rect.width - 55, dropdown_rect.y + 15))

            # Show the start button when both names are entered
            if self.start_button_visible:
                start_button = pygame.Rect(300, 460, 200, 50)  # Adjusted position for the start button
                pygame.draw.rect(self.screen, pygame.Color("yellow"), start_button)
                start_text = self.small_font.render("Start Game", True, pygame.Color("black"))
                self.screen.blit(start_text, (300 + 100 - start_text.get_width() // 2, 470))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.menu_state == self.MAIN_MENU:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Start Game
                        self.menu_state = self.GAME_MODE_MENU
                    elif self.selected_option == 1:  # Instructions
                        self.show_instructions()
                    elif self.selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()

            elif self.menu_state == self.GAME_MODE_MENU:
                if event.key == pygame.K_UP:
                    self.selected_game_mode = (self.selected_game_mode - 1) % len(self.game_mode_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_game_mode = (self.selected_game_mode + 1) % len(self.game_mode_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_game_mode == 0:  # Human vs Human
                        self.menu_state = self.NAME_ENTRY_MENU
                        print("game mode 0: Human vs Human")
                    elif self.selected_game_mode == 1:  # Human vs AI
                        self.menu_state = self.NAME_ENTRY_MENU
                        print("game mode 1: Human vs AI")

            elif self.menu_state == self.NAME_ENTRY_MENU:
                if event.key == pygame.K_BACKSPACE:  # Handle name deletion
                    if self.input_focus == "Player 1" and len(self.names["Player 1"]) > 0:
                        self.names["Player 1"] = self.names["Player 1"][:-1]
                    elif self.input_focus == "Player 2" and len(self.names["Player 2"]) > 0:
                        self.names["Player 2"] = self.names["Player 2"][:-1]
                elif event.key == pygame.K_RETURN:  # Switch focus or start game
                    if self.input_focus == "Player 1" and len(self.names["Player 1"]) > 0:
                        self.input_focus = "Player 2"
                    elif self.input_focus == "Player 2" and len(self.names["Player 2"]) > 0:
                        self.start_game()  # Will be handled based on selected game mode
                else:  # Handle name typing
                    if self.input_focus == "Player 1" and len(self.names["Player 1"]) < self.name_limit:
                        self.names["Player 1"] += event.unicode
                    elif self.input_focus == "Player 2" and len(self.names["Player 2"]) < self.name_limit:
                        self.names["Player 2"] += event.unicode

                    # Update start button visibility
                    if len(self.names["Player 1"]) > 0 and len(self.names["Player 2"]) > 0:
                        self.start_button_visible = True
                    else:
                        self.start_button_visible = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_state == self.NAME_ENTRY_MENU:
                # Check if the dropdown was clicked to change the game type
                dropdown_rect = pygame.Rect(250, 375, 500, 50)
                if dropdown_rect.collidepoint(event.pos):
                    # Cycle through game types
                    self.selected_game_type_index = (self.selected_game_type_index + 1) % len(self.game_types)

                # Check if the start button was clicked
                if self.start_button_visible:
                    start_button = pygame.Rect(300, 460, 200, 50)
                    if start_button.collidepoint(event.pos):
                        self.start_game()  # This will now start the correct game based on the mode selected

        elif event.type == pygame.MOUSEMOTION:
            # Handle hover effect for the dropdown
            if self.menu_state == self.NAME_ENTRY_MENU:
                dropdown_rect = pygame.Rect(250, 375, 500, 50)
                self.hovered_over_dropdown = dropdown_rect.collidepoint(event.pos)


    def start_game(self):
        if not self.names["Player 1"] or not self.names["Player 2"]:
            self.show_name_error()
        else:
            game_type = self.game_types[self.selected_game_type_index]  # Get the selected game type
            if self.selected_game_mode == 0:  # Human vs Human
                print(f"Starting Human vs Human game with {self.names['Player 1']} and {self.names['Player 2']} in {game_type} mode")
                backend_main(player1=self.names["Player 1"], player2=self.names["Player 2"], mode=0, game_type=game_type)
            elif self.selected_game_mode == 1:  # Human vs AI
                print(f"Starting Human vs AI game with {self.names['Player 1']} and {self.names['Player 2']} in {game_type} mode")
                backend_main(player1=self.names["Player 1"], player2=self.names["Player 2"], mode=1, game_type=game_type)
            pygame.quit()


    
    def show_instructions(self):
        instructions_page = InstructionsPage(self.screen)
        instructions_page.run()

    def show_name_error(self):
        error_message = self.font.render("Please enter both names!", True, pygame.Color("red"))
        self.screen.blit(error_message, (800 // 2 - error_message.get_width() // 2, 500))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Hover effect
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    dropdown_rect = pygame.Rect(250, 375, 500, 50)
                    self.hovered_over_dropdown = dropdown_rect.collidepoint(mouse_x, mouse_y)

                self.handle_input(event)

            self.draw_menu()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()