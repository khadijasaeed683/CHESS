import pygame
import argparse
from ChessAI import ChessAI
from ChessGraph import ChessGraph,show_message_box
from constants import PIECE_IMAGES, SQUARE_SIZE, ROWS, COLS,CHESSBOARD_SIZE,BLACK,WHITE,BEIGE, BROWN,GREEN,DARK_BROWN,LIGHT_BROWN,SANDY_BROWN, CHOCOLATE,WIDTH,HEIGHT

def draw_board(screen, chess_graph, valid_moves=None):
    # Draw border
    pygame.draw.rect(screen, BLACK, (80, 80, CHESSBOARD_SIZE, CHESSBOARD_SIZE), 5)

    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, chess_graph.nodes[(row, col)].rect)

            # Draw piece image if it exists
            if chess_graph.nodes[(row, col)].image:
                piece_color = chess_graph.nodes[(row, col)].color
                piece_name = chess_graph.nodes[(row, col)].piece

                if "King" in piece_name:
                    king_position = chess_graph.nodes[(row, col)].position
                    if (piece_color == 'white' and chess_graph.is_in_check('white')) or (piece_color == 'black' and chess_graph.is_in_check('black')):
                        pygame.draw.rect(screen, (255, 0, 0), chess_graph.nodes[(row, col)].rect)  # Red background for king in check
                        screen.blit(chess_graph.nodes[(row, col)].image, (col * SQUARE_SIZE + 85, row * SQUARE_SIZE + 85))
                        continue

                screen.blit(chess_graph.nodes[(row, col)].image, (col * SQUARE_SIZE + 85, row * SQUARE_SIZE + 85))

            # Highlight valid moves
            if valid_moves and (row, col) in valid_moves:
                pygame.draw.rect(screen, GREEN, chess_graph.nodes[(row, col)].rect, 5)

    # Draw ranks and files outside the board
    font = pygame.font.SysFont(None, 32)
    for row in range(ROWS):
        rank_text = font.render(str(8 - row), True, BLACK)
        screen.blit(rank_text, (50, row * SQUARE_SIZE + 100))

    for col in range(COLS):
        file_text = font.render(chr(ord('a') + col), True, BLACK)
        screen.blit(file_text, (col * SQUARE_SIZE + 100, CHESSBOARD_SIZE + 90))
            
def draw_captured_pieces(screen, captured_white_pieces, captured_black_pieces):
    # Display captured white pieces at the bottom right
    unique_captured_white_pieces = list(set(captured_white_pieces))
    for index, piece in enumerate(unique_captured_white_pieces):
        image = PIECE_IMAGES[piece]
        scaled_image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        screen.blit(scaled_image, (CHESSBOARD_SIZE + 100 + (index % 8) * 30, HEIGHT - 180 - (index // 8) * 30))

    # Display captured black pieces at the top right
    unique_captured_black_pieces = list(set(captured_black_pieces))
    for index, piece in enumerate(unique_captured_black_pieces):
        image = PIECE_IMAGES[piece]
        scaled_image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        screen.blit(scaled_image, (CHESSBOARD_SIZE + 100 + (index % 8) * 30, 30 + (index // 8) * 30))

def end_screen(screen, winner, reason=""):
    pygame.time.delay(3000)
    """Displays the win/lose screen."""
    screen.fill((30, 30, 30))  # Dark gray background

    # Fonts
    title_font = pygame.font.SysFont("Times New Roman", 50)
    button_font = pygame.font.SysFont("Times New Roman", 35)

    # Title Text
    title_text = f"{winner} Wins!" if winner != "Draw" else "It's a Draw!"
    title_surface = title_font.render(title_text, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    screen.blit(title_surface, title_rect)

    pygame.display.update()

    # Handle Events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

CHECKMATE_EVENT = pygame.USEREVENT + 1  # Define the custom event for checkmate


def main(player1="Player 1", player2="Player 2", mode=1, game_type="normal"):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Initialize ChessGraph with the selected game type
    chess_graph = ChessGraph(screen,game_type=game_type)
    chess_graph.ai = ChessAI('black') if mode == 1 else None
    chess_graph.game_over = False

    selected_piece = None
    valid_moves = []
    ai_move_time = 0  

    undo_image, undo_button_rect = None, None
    if game_type != "professional":
        undo_image = pygame.image.load("Images/undo-icon.png")
        undo_image = pygame.transform.scale(undo_image, (90, 90))
        undo_button_rect = undo_image.get_rect()
        undo_button_rect.topleft = (WIDTH - 250, HEIGHT // 2 - 105)

    print(f"Game started with {player1} and {player2}. Mode: {'Human vs Human' if mode == 0 else 'Human vs AI'}")
    print(f"Game type: {game_type}")

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == CHECKMATE_EVENT:
                player, opponent = chess_graph.checkmate_info
                print(f"Checkmate! {player} wins. Game over!")
                show_message_box(screen,f"Checkmate! {player} wins. Game over!")
                end_screen(screen, player, reason="")
                chess_graph.game_over = True
                pygame.time.set_timer(CHECKMATE_EVENT, 0)  # Stop the timer after handling
            
            if chess_graph.game_over:
                continue  # Skip event handling if the game is over

            # Undo action (disabled for professional mode)
            if game_type != "professional":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    if mode == 1:
                        chess_graph.undo_move()  # Undo AI move first
                    chess_graph.undo_move()  # Undo human move

                elif event.type == pygame.MOUSEBUTTONDOWN and undo_button_rect.collidepoint(event.pos):
                    if mode == 1:
                        chess_graph.undo_move()  # Undo AI move first
                    chess_graph.undo_move()  # Undo human move

            # Human vs Human mode
            if mode == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = (x - 80) // SQUARE_SIZE, (y - 80) // SQUARE_SIZE
                    if 0 <= col < COLS and 0 <= row < ROWS:
                        clicked_position = (row, col)
                        piece = chess_graph.nodes[clicked_position].piece
                        piece_color = chess_graph.nodes[clicked_position].color
                        player = 'white' if piece_color == 'white' else 'black'

                        if selected_piece is None:
                            if piece and chess_graph.players[player].turn:
                                selected_piece = clicked_position
                                # Calculate valid moves but do not highlight in professional mode
                                valid_moves = chess_graph.get_valid_moves_for_piece(clicked_position)
                            else:
                                print(f"It's not {player}'s turn.")
                        elif selected_piece == clicked_position:
                            selected_piece = None
                            valid_moves = []
                        else:
                            if clicked_position in valid_moves:
                                chess_graph.move_piece(selected_piece, clicked_position)
                                selected_piece = None
                                valid_moves = []

            # Human vs AI mode
            elif mode == 1:
                if chess_graph.players['white'].turn and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = (x - 80) // SQUARE_SIZE, (y - 80) // SQUARE_SIZE
                    if 0 <= col < COLS and 0 <= row < ROWS:
                        clicked_position = (row, col)
                        piece = chess_graph.nodes[clicked_position].piece
                        piece_color = chess_graph.nodes[clicked_position].color
                        player = 'white' if piece_color == 'white' else 'black'

                        if selected_piece is None:
                            if piece and chess_graph.players[player].turn:
                                selected_piece = clicked_position
                                # Calculate valid moves but do not highlight in professional mode
                                valid_moves = chess_graph.get_valid_moves_for_piece(clicked_position)
                        elif selected_piece == clicked_position:
                            selected_piece = None
                            valid_moves = []
                        else:
                            if clicked_position in valid_moves:
                                chess_graph.move_piece(selected_piece, clicked_position)
                                selected_piece = None
                                valid_moves = []
                                ai_move_time = current_time + 1000  # AI move after 1 second

        # AI move logic for Human vs AI mode
        if mode == 1 and not chess_graph.players['white'].turn and current_time >= ai_move_time:
            best_move = chess_graph.ai.get_best_move(chess_graph)
            if best_move:
                chess_graph.move_piece(best_move[0], best_move[1], print_invalid_moves=False)
        
                
        if game_type == "rapid" or game_type == "professional":
            timer_result = chess_graph.update_timers()
            if timer_result:
                winner = timer_result["winner"].capitalize()  # 'white' or 'black'
                reason = timer_result["reason"]  # e.g., "Out of time"
                action = end_screen(screen, winner, reason)  # Show end screen

                if action == "home":
                    return  # Go back to the main menu
                elif action == "quit":
                    running = False  # Quit the game
                    
        # Draw the board and other components
        screen.fill(CHOCOLATE)
        border_thickness = 5
        pygame.draw.rect(screen, BLACK, (80 - border_thickness, 80 - border_thickness, CHESSBOARD_SIZE + 2 * border_thickness, CHESSBOARD_SIZE + 2 * border_thickness))
        pygame.draw.rect(screen, WHITE, (80, 80, CHESSBOARD_SIZE, CHESSBOARD_SIZE))

        # Draw player names above and below the chessboard
        font = pygame.font.SysFont(None, 29)
        
        player1_text = font.render("Player 1: " + player1, True, WHITE)
        screen.blit(player1_text, (WIDTH // 2 - player1_text.get_width() - 90, HEIGHT - 95))

        # Player 2 (Black) name at the top
        player2_text = font.render("Player 2: " + player2, True, WHITE)
        screen.blit(player2_text, (WIDTH // 2 - player2_text.get_width() -90 , 45))

        # Draw the board
        draw_board(screen, chess_graph, [] if game_type == "professional" else valid_moves)
        draw_captured_pieces(screen, chess_graph.captured_white_pieces, chess_graph.captured_black_pieces)

        if game_type in ["rapid", "professional"]:
            chess_graph.draw_timers(screen)

        # Draw the undo button only if not professional
        if game_type != "professional" and undo_image and undo_button_rect:
            screen.blit(undo_image, undo_button_rect)
        
        # *****************Title at the top center***************************************
        font = pygame.font.SysFont("Times New Roman", 25)
        title_text = f"CHESS - ({game_type.capitalize()}) - {'Human vs Human' if mode == 0 else 'Human vs AI'}"
        title_surface = font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 20))  # Positioning it at the top center
        screen.blit(title_surface, title_rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Game")
    parser.add_argument("--player1", type=str, default="Player 1", help="Name of Player 1")
    parser.add_argument("--player2", type=str, default="Player 2", help="Name of Player 2")
    parser.add_argument("--mode", type=int, choices=[0, 1], default=1, help="Game mode: 0 for Human vs Human, 1 for Human vs AI")
    parser.add_argument("--game_type", type=str, choices=["normal", "rapid", "classic", "professional"], default="normal", help="Game type: normal, rapid, classic, or professional")
    args = parser.parse_args()

    main(player1=args.player1, player2=args.player2, mode=args.mode, game_type=args.game_type)
