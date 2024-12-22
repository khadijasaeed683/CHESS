import pygame
class Player:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.turn = False   # Whether it's this player's turn
        self.timer = 50  # Set the timer for 5 minutes (in seconds)
        self.start_time = pygame.time.get_ticks()  # To track the start time of the player's turn

    def toggle_turn(self):
        self.turn = not self.turn

    def set_turn(self, turn):
        self.turn = turn  # Explicitly set turn (useful for starting the game)

    def __str__(self):
        return f"Player {self.name} ({self.color.capitalize()}) - {'It\'s your turn!' if self.turn else 'Wait for your turn.'}"
