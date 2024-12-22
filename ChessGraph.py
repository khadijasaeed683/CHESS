from Player import Player
import pygame
from  constants import PIECE_IMAGES,SQUARE_SIZE,ROWS,COLS
from Stack import myStack
from Node import Node
from ChessAI import ChessAI
import time
import sys
from Queue import MyQueue

WHITE, BEIGE, BROWN, GREEN, BLACK, RED = (255, 255, 255), (240, 255, 230), (196, 164, 132), (0, 255, 0), (0, 0, 0), (255, 0, 0)
WIDTH, HEIGHT = 1000, 750  
CHECKMATE_EVENT = pygame.USEREVENT + 1  


class ChessGraph:
    def __init__(self,main_screen, game_type="normal"):
        self.nodes = {} 
        self.create_chessboard()
        self.setup_pieces()
        self.king_positions = {'white': (7, 4), 'black': (0, 4)}
        self.players = {'white': Player('white'), 'black': Player('black')} 
        self.players['white'].turn = True 
        self.move_history = myStack()
        self.main_screen = main_screen
        self.ai = ChessAI('black' if self.players['white'].turn else 'white')
        self.font = pygame.font.SysFont("Arial", 24)  
        self.last_time = pygame.time.get_ticks()
        self.game_over = False 
        self.checkmate_info = None
        self.game_type = game_type  

        # Timer settings (only for "rapid")
        if self.game_type == "rapid":
            self.players['white'].timer = 300  
            self.players['black'].timer = 300  

        self.captured_white_pieces = [] 
        self.captured_black_pieces = []
        
    def can_castle(self, player, side):
        king_start_pos = self.king_positions[player]
        if side == 'kingside':
            rook_start_pos = (king_start_pos[0], king_start_pos[1] + 3)
        elif side == 'queenside':
            rook_start_pos = (king_start_pos[0], king_start_pos[1] - 4)
        else:
            return False

        try:
            if not self.nodes[rook_start_pos].piece == f'Rook_{player}':
                return False
            if self.is_in_check(player):
                return False
            if side == 'kingside':
                positions = [(king_start_pos[0], king_start_pos[1] + i) for i in range(1, 3)]
            else:
                positions = [(king_start_pos[0], king_start_pos[1] - i) for i in range(1, 4)]

            for pos in positions:
                if pos not in self.nodes or self.nodes[pos].piece:
                    return False
                original_state = self.store_original_state(king_start_pos, self.nodes[pos], player)
                captured_piece = self.simulate_move_and_capture(king_start_pos, pos)
                self.recalculate_valid_moves()
                if self.is_in_check(player):
                    self.undo_simulated_move(original_state)
                    return False
                self.undo_simulated_move(original_state)

            return True
        except KeyError:
            return False


    def is_square_attacked(self, pos, player_color):
        opponent_color = 'black' if player_color == 'white' else 'white'
        for src_pos, node in self.nodes.items():
            if node.color == opponent_color:
                if "Pawn" in node.piece:
                    opponent_moves = self.get_valid_pawn_moves_bfs(src_pos)
                elif "Knight" in node.piece:
                    opponent_moves = self.get_valid_knight_moves_bfs(src_pos)
                elif "Rook" in node.piece:
                    opponent_moves = self.get_valid_rook_moves_bfs(src_pos)
                elif "Bishop" in node.piece:
                    opponent_moves = self.get_valid_bishop_moves_bfs(src_pos)
                elif "Queen" in node.piece:
                    opponent_moves = self.get_valid_queen_moves_bfs(src_pos)
                elif "King" in node.piece:
                    opponent_moves = self.get_valid_king_moves_bfs(src_pos)

                if pos in opponent_moves:
                    return True
        return False

    def create_chessboard(self):
        for row in range(ROWS):
            for col in range(COLS):
                position = (row, col)
                rect = pygame.Rect(col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)  # Offset for border
                self.nodes[position] = Node(position, rect)

    def setup_pieces(self):
        # Set up pawns
        for col in range(COLS):
            self.nodes[(1, col)].set_piece("Pawn_black", PIECE_IMAGES["Pawn_black"],"black")
            self.nodes[(6, col)].set_piece("Pawn_white", PIECE_IMAGES["Pawn_white"],"white")

        # Set up rooks
        self.nodes[(0, 0)].set_piece("Rook_black", PIECE_IMAGES["Rook_black"],"black")
        self.nodes[(0, 7)].set_piece("Rook_black", PIECE_IMAGES["Rook_black"],"black")
        self.nodes[(7, 0)].set_piece("Rook_white", PIECE_IMAGES["Rook_white"],"white")
        self.nodes[(7, 7)].set_piece("Rook_white", PIECE_IMAGES["Rook_white"],"white")

        # Set up knights
        self.nodes[(0, 1)].set_piece("Knight_black", PIECE_IMAGES["Knight_black"],"black")
        self.nodes[(0, 6)].set_piece("Knight_black", PIECE_IMAGES["Knight_black"],"black")
        self.nodes[(7, 1)].set_piece("Knight_white", PIECE_IMAGES["Knight_white"],"white")
        self.nodes[(7, 6)].set_piece("Knight_white", PIECE_IMAGES["Knight_white"],"white")

        # Set up bishops
        self.nodes[(0, 2)].set_piece("Bishop_black", PIECE_IMAGES["Bishop_black"],"black")
        self.nodes[(0, 5)].set_piece("Bishop_black", PIECE_IMAGES["Bishop_black"],"black")
        self.nodes[(7, 2)].set_piece("Bishop_white", PIECE_IMAGES["Bishop_white"],"white")
        self.nodes[(7, 5)].set_piece("Bishop_white", PIECE_IMAGES["Bishop_white"],"white")

        # Set up queens
        self.nodes[(0, 3)].set_piece("Queen_black", PIECE_IMAGES["Queen_black"],"black")
        self.nodes[(7, 3)].set_piece("Queen_white", PIECE_IMAGES["Queen_white"],"white")

        # Set up kings
        self.nodes[(0, 4)].set_piece("King_black", PIECE_IMAGES["King_black"],"black")
        self.nodes[(7, 4)].set_piece("King_white", PIECE_IMAGES["King_white"],"white")

    def is_in_check(self, player_color):
        """Check if the player's king is in check."""
        opponent_color = 'black' if player_color == 'white' else 'white'
        king_pos = self.king_positions[player_color]
        
        # Check if any of the opponent's moves can capture the king
        for pos, node in self.nodes.items():
            if node.color == opponent_color:
                if "Pawn" in node.piece:
                    opponent_moves = self.get_valid_pawn_moves_bfs(pos)
                elif "Knight" in node.piece:
                    opponent_moves = self.get_valid_knight_moves_bfs(pos)
                elif "Rook" in node.piece:
                    opponent_moves = self.get_valid_rook_moves_bfs(pos)
                elif "Bishop" in node.piece:
                    opponent_moves = self.get_valid_bishop_moves_bfs(pos)
                elif "Queen" in node.piece:
                    opponent_moves = self.get_valid_queen_moves_bfs(pos)
                elif "King" in node.piece:
                    opponent_moves = self.get_valid_king_moves_bfs(pos)
                
                if king_pos in opponent_moves:
                    return True
        return False
    
    def update_valid_moves(self):
        for pos, node in self.nodes.items():
            if node.piece:
                piece = node.piece
                valid_moves = []
                if "Pawn" in piece:
                    valid_moves = self.get_valid_pawn_moves_bfs(pos)
                elif "Knight" in piece:
                    valid_moves = self.get_valid_knight_moves_bfs(pos)
                elif "Rook" in piece:
                    valid_moves = self.get_valid_rook_moves_bfs(pos)
                elif "Bishop" in piece:
                    valid_moves = self.get_valid_bishop_moves_bfs(pos)
                elif "Queen" in piece:
                    valid_moves = self.get_valid_queen_moves_bfs(pos)
                elif "King" in piece:
                    valid_moves = self.get_valid_king_moves_bfs(pos)
                node.valid_moves = valid_moves  # Store the valid moves for the piece


  

    def store_original_state(self, source, dest_node, player):
        src_node = self.nodes[source]
        return (
            (source, src_node.piece, src_node.image, src_node.color),
            (dest_node.position, dest_node.piece, dest_node.image, dest_node.color),
            self.king_positions.copy(),
            player,
            self.captured_white_pieces.copy(),
            self.captured_black_pieces.copy(),
        )

    def handle_castling(self, source, destination, player, src_node):
        if "King" in src_node.piece:
            if abs(source[1] - destination[1]) == 2:
                if destination[1] == 6 and self.can_castle(player, 'kingside'):  # Kingside castling
                    self.perform_castling(source, 'kingside')
                    self.king_positions[src_node.color] = destination
                    src_node.has_moved = True
                    return True
                elif destination[1] == 2 and self.can_castle(player, 'queenside'):  # Queenside castling
                    self.perform_castling(source, 'queenside')
                    self.king_positions[src_node.color] = destination
                    src_node.has_moved = True
                    return True
            else:
                self.king_positions[src_node.color] = destination
        return False
    
    

    def simulate_move_and_capture(self, source, destination):
        src_node = self.nodes[source]
        dest_node = self.nodes[destination]
        captured_piece = None

        if dest_node.piece:
            captured_piece = dest_node.piece
            if dest_node.color == 'white':
                self.captured_white_pieces.append(dest_node.piece)
            else:
                self.captured_black_pieces.append(dest_node.piece)

        if "Pawn" in src_node.piece and abs(source[0] - destination[0]) == 1 and abs(source[1] - destination[1]) == 1:
            if not dest_node.piece:
                captured_pos = (source[0], destination[1])
                captured_node = self.nodes[captured_pos]
                captured_piece = captured_node.piece
                captured_node.remove_piece()
                if captured_node.color == 'white':
                    self.captured_white_pieces.append(captured_piece)
                else:
                    self.captured_black_pieces.append(captured_piece)

        dest_node.set_piece(src_node.piece, src_node.image, src_node.color)
        src_node.remove_piece()
        dest_node.has_moved = True
        return captured_piece

    def check_for_pawn_promotion(self, destination, player):
        dest_node = self.nodes[destination]
        if "Pawn" in dest_node.piece and (destination[0] == 0 or destination[0] == 7):
            self.promote_pawn(destination, player)

    def recalculate_valid_moves(self):
        self.update_valid_moves()

    def handle_invalid_move(self, original_state, player, captured_piece):
        src_node = self.nodes[original_state[0][0]]
        dest_node = self.nodes[original_state[1][0]]

        src_node.set_piece(original_state[0][1], original_state[0][2], original_state[0][3])
        if original_state[1][1]:
            dest_node.set_piece(original_state[1][1], original_state[1][2], original_state[1][3])
        else:
            dest_node.remove_piece()

        if captured_piece:
            if dest_node.color == 'white':
                self.captured_white_pieces.remove(captured_piece)
            else:
                self.captured_black_pieces.remove(captured_piece)

        if "King" in src_node.piece:
            self.king_positions[src_node.color] = src_node.position

        
            self.move_history.POP()

        # Toggle turn back to the player who made the invalid move
        self.players[player].turn = True
        opponent = 'black' if player == 'white' else 'white'
        self.players[opponent].turn = False
     
    
    def get_legal_moves_to_undo_check(self, player_color):
        """Check if there are any legal moves that can remove the king from check."""
        
        # Check if the player is in check
        if not self.is_in_check(player_color):
            return True  # If not in check, no special legal moves are needed

        for pos, node in self.nodes.items():
            if node.color == player_color and node.piece is not None:  
                valid_moves = []

                # Calculate valid moves for the piece at the current position
                if "Pawn" in node.piece:
                    valid_moves = self.get_valid_pawn_moves_bfs(pos)
                elif "Knight" in node.piece:
                    valid_moves = self.get_valid_knight_moves_bfs(pos)
                elif "Rook" in node.piece:
                    valid_moves = self.get_valid_rook_moves_bfs(pos)
                elif "Bishop" in node.piece:
                    valid_moves = self.get_valid_bishop_moves_bfs(pos)
                elif "Queen" in node.piece:
                    valid_moves = self.get_valid_queen_moves_bfs(pos)
                elif "King" in node.piece:
                    king_moves = self.can_king_uncheck(player_color)
                    if king_moves:  # If there are any moves that can uncheck the king, return True
                        return True
                    continue  

                # Simulate each move and check if it removes the check
                for move in valid_moves:
                    original_state = self.store_original_state(pos, self.nodes[move], player_color)
                    captured_piece = self.simulate_move_and_capture(pos, move)
                    self.recalculate_valid_moves()

                    if not self.is_in_check(player_color):
                        # Undo the simulated move and return True if a legal move is found
                        self.undo_simulated_move(original_state)
                        return True

                    # Undo the simulated move
                    self.undo_simulated_move(original_state)

        return False  # Return False if no legal moves can uncheck the king


    def can_king_uncheck(self, player_color):
        """Check if the king can move to any position to get out of check and return those moves."""
        king_position = self.king_positions[player_color]
        king_moves = self.get_valid_king_moves_bfs(king_position)
        valid_king_moves = []

        for move in king_moves:
            original_state = self.store_original_state(king_position, self.nodes[move], player_color)
            captured_piece = self.simulate_move_and_capture(king_position, move)
            self.recalculate_valid_moves()

            # Check if the new position leaves the king in check
            if not self.is_square_attacked(move, player_color):
                valid_king_moves.append((king_position, move))

            # Undo the simulated move
            self.undo_simulated_move(original_state)

        return valid_king_moves

    
    def move_piece(self, source, destination, simulated=False, print_invalid_moves=True):
        if source not in self.nodes or destination not in self.nodes:
            if not simulated:
                print(f"Invalid positions: {source} to {destination}.")
            return False

        src_node = self.nodes[source]
        dest_node = self.nodes[destination]

        if not src_node.piece:
            if not simulated:
                print(f"No piece at {source} to move.")
            return False

        player = 'white' if src_node.color == 'white' else 'black'
        opponent = 'black' if player == 'white' else 'white'

        if not self.players[player].turn:
            if not simulated:
                print(f"It's not {player}'s turn.")
            return False

        if not simulated:
            print(f"Moving piece: {src_node.piece} from {source} to {destination}")
            print(f"Player: {player}")

        original_state = self.store_original_state(source, dest_node, player)

        if not simulated:
            self.move_history.PUSH(original_state)

        if self.handle_castling(source, destination, player, src_node):
            if not simulated:
                self.players[player].toggle_turn()
                self.players[opponent].toggle_turn()
            return True

        captured_piece = self.simulate_move_and_capture(source, destination)
        self.check_for_pawn_promotion(destination, player)
        self.recalculate_valid_moves()

        if self.is_in_check(player):
            if print_invalid_moves:
                print(f"Invalid move: {player} is in check after this move!")
                self.handle_invalid_move(original_state, player, captured_piece)
            return False

        if not simulated:
            self.players[player].toggle_turn()
            self.players[opponent].toggle_turn()

        if self.is_in_check(opponent):
            print(f"Check! {opponent}'s king is in check.")
            if not self.get_legal_moves_to_undo_check(opponent):
                self.checkmate_info = (player, opponent)
                pygame.time.set_timer(CHECKMATE_EVENT, 3000)  # 5-second delay for checkmate announcement
                return False

        return True



    def clear_board(self): 
        """Remove all pieces from the board.""" 
        for position in self.nodes: 
            self.nodes[position].remove_piece()
            
    def undo_simulated_move(self, state):
        source_state, dest_state, last_king_positions, player, captured_white, captured_black = state
        src_pos, src_piece, src_image, src_color = source_state
        dest_pos, dest_piece, dest_image, dest_color = dest_state
        self.nodes[src_pos].set_piece(src_piece, src_image, src_color)
        if dest_piece:
            self.nodes[dest_pos].set_piece(dest_piece, dest_image, dest_color)
        else:
            self.nodes[dest_pos].remove_piece()
        self.king_positions = last_king_positions
        self.captured_white_pieces = captured_white
        self.captured_black_pieces = captured_black

                
    
    def perform_castling(self, king_pos, side):
        """Perform castling move."""
        king_row, king_col = king_pos

        if side == 'kingside':
            new_king_col = 6
            new_rook_col = 5
            rook_pos = (king_row, 7)
        elif side == 'queenside':
            new_king_col = 2
            new_rook_col = 3
            rook_pos = (king_row, 0)

        # Move the king
        self.nodes[(king_row, new_king_col)].set_piece(self.nodes[king_pos].piece, self.nodes[king_pos].image, self.nodes[king_pos].color)
        self.nodes[king_pos].remove_piece()
        self.nodes[(king_row, new_king_col)].has_moved = True  # Mark the king as having moved

        # Move the rook
        self.nodes[(king_row, new_rook_col)].set_piece(self.nodes[rook_pos].piece, self.nodes[rook_pos].image, self.nodes[rook_pos].color)
        self.nodes[rook_pos].remove_piece()
        self.nodes[(king_row, new_rook_col)].has_moved = True  # Mark the rook as having moved


    def promote_pawn(self, position, player_color):
        """Promotes a pawn to a queen, rook, bishop, or knight based on player's choice."""
        promotion_piece = open_promotion_window(player_color, self.main_screen)

        if promotion_piece:
            piece_image = self.get_piece_image(promotion_piece, player_color)
            self.nodes[position].set_piece(f'{promotion_piece}_{player_color}', piece_image, player_color)
            print(f"Pawn promoted to {promotion_piece} at {position} for {player_color} player")
            
            

    def get_piece_image(self, piece, color):
        """Helper function to get the image for a piece."""
        return pygame.image.load(f'{color}-{piece}.png')  # Adjust the path as needed



    def undo_move(self):    
        if self.move_history.isEmpty():
            print("No moves to undo.")
            return

        # Pop the last move from the stack
        last_state = self.move_history.POP()
        src_state, dest_state, last_king_positions, last_player, last_captured_white, last_captured_black = last_state

        # Restore the source and destination nodes
        src_pos, src_piece, src_image, src_color = src_state
        dest_pos, dest_piece, dest_image, dest_color = dest_state

        self.nodes[src_pos].set_piece(src_piece, src_image, src_color)
        if dest_piece:
            self.nodes[dest_pos].set_piece(dest_piece, dest_image, dest_color)
        else:
            self.nodes[dest_pos].remove_piece()

        # Check if the move was castling and restore the rook's position
        if "King" in src_piece and abs(src_pos[1] - dest_pos[1]) == 2:
            if dest_pos[1] == 6:  
                rook_src_pos = (src_pos[0], 7)
                rook_dest_pos = (src_pos[0], 5)
            elif dest_pos[1] == 2:  
                rook_src_pos = (src_pos[0], 0)
                rook_dest_pos = (src_pos[0], 3)

            rook_piece = self.nodes[rook_dest_pos].piece
            rook_image = self.nodes[rook_dest_pos].image
            rook_color = self.nodes[rook_dest_pos].color

            self.nodes[rook_src_pos].set_piece(rook_piece, rook_image, rook_color)
            self.nodes[rook_dest_pos].remove_piece()

            # Ensure the king and rook are marked as not having moved
            self.nodes[src_pos].has_moved = False
            self.nodes[rook_src_pos].has_moved = False

        # Restore the king positions
        self.king_positions = last_king_positions

        # Restore the captured pieces
        self.captured_white_pieces = last_captured_white
        self.captured_black_pieces = last_captured_black

        # Toggle turn back
        self.players[last_player].toggle_turn()
        self.players['white' if last_player == 'black' else 'black'].toggle_turn()

    def get_valid_knight_moves_bfs(self, position):
        moves = []
        row, col = position
        potential_moves = [
            (row - 2, col - 1), (row - 2, col + 1), (row + 2, col - 1), (row + 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2), (row + 1, col - 2), (row + 1, col + 2)
        ]

        current_piece_color = self.nodes[position].color  # Color of the Knight at the current position

        for r, c in potential_moves:
            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece_color = target_node.color

                if not target_node.piece or target_piece_color != current_piece_color:
                    moves.append((r, c))

        return moves


    def get_valid_rook_moves_bfs(self, position):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        current_piece_color = self.nodes[position].color

        queue = MyQueue()
        for direction in directions:
            queue.enqueue((position, direction))

        while not queue.is_empty():
            (row, col), (dr, dc) = queue.dequeue()
            r, c = row + dr, col + dc

            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color

                if target_piece:
                    if target_piece_color != current_piece_color:
                        moves.append((r, c))
                    continue  # Stop if a piece blocks further movement
                moves.append((r, c))
                queue.enqueue(((r, c), (dr, dc)))  # Continue in the same direction

        return moves

    def get_valid_bishop_moves_bfs(self, position):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        current_piece_color = self.nodes[position].color

        queue = MyQueue()
        for direction in directions:
            queue.enqueue((position, direction))

        while not queue.is_empty():
            (row, col), (dr, dc) = queue.dequeue()
            r, c = row + dr, col + dc

            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color

                if target_piece:
                    if target_piece_color != current_piece_color:
                        moves.append((r, c))
                    continue  # Stop if a piece blocks further movement
                moves.append((r, c))
                queue.enqueue(((r, c), (dr, dc)))  # Continue in the same direction

        return moves

    def get_valid_queen_moves_bfs(self, position):
        return self.get_valid_rook_moves_bfs(position) + self.get_valid_bishop_moves_bfs(position)

    def get_valid_king_moves_bfs(self, position):
        moves = []
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the King at the current position
        potential_moves = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
        ]

        for r, c in potential_moves:
            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color  # Color of the piece at the target square

                # Check if it's an empty square or an enemy piece
                if not target_piece or target_piece_color != current_piece_color:
                    moves.append((r, c))

        return moves


    def get_valid_pawn_moves_bfs(self, position):
        moves = []
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the Pawn at the current position
        direction = -1 if current_piece_color == "white" else 1
        start_row = 6 if current_piece_color == "white" else 1
        en_passant_row = 3 if current_piece_color == "white" else 4

        # Move forward one square
        if 0 <= row + direction < ROWS and not self.nodes[(row + direction, col)].piece:
            moves.append((row + direction, col))

            # Move forward two squares from the starting position
            if row == start_row and not self.nodes[(row + 2 * direction, col)].piece:
                moves.append((row + 2 * direction, col))

        # Capture diagonally
        for dc in [-1, 1]:
            if 0 <= col + dc < COLS and 0 <= row + direction < ROWS:
                target_piece = self.nodes[(row + direction, col + dc)].piece
                target_piece_color = self.nodes[(row + direction, col + dc)].color  # Color of the target piece
                if target_piece and target_piece_color != current_piece_color:
                    moves.append((row + direction, col + dc))  # Valid capture

        # En passant capture
        if row == en_passant_row:
            for dc in [-1, 1]:
                if 0 <= col + dc < COLS:
                    target_position = (row, col + dc)
                    target_node = self.nodes[target_position]
                    if target_node.piece and target_node.color != current_piece_color and "Pawn" in target_node.piece:
                        # Check the last move to see if it was a pawn moving two squares forward
                        last_move = self.move_history.Peek() if not self.move_history.isEmpty() else None
                        if last_move:
                            src_last_move, dest_last_move, _, _, _, _ = last_move  # Adjusting to match the stored state
                            src_pos, src_piece, src_image, src_color = src_last_move
                            dest_pos, dest_piece, dest_image, dest_color = dest_last_move
                            src_row, src_col = src_pos
                            dest_row, dest_col = dest_pos
                            if abs(src_row - dest_row) == 2 and (dest_row, dest_col) == target_position:
                                moves.append((row + direction, col + dc))  # En passant capture

        return moves
    
   

    def is_game_over(self):
        # Check for checkmate
        if self.is_in_check('white') and not self.get_legal_moves_to_undo_check('white'):
            print("Checkmate! Black wins.")
            return True
        if self.is_in_check('black') and not self.get_legal_moves_to_undo_check('black'):
            print("Checkmate! White wins.")
            return True

        # Check for stalemate (no legal moves and not in check)
        if not self.is_in_check('white') and not self.get_legal_moves_to_undo_check('white'):
            print("Stalemate! It's a draw.")
            return True
        if not self.is_in_check('black') and not self.get_legal_moves_to_undo_check('black'):
            print("Stalemate! It's a draw.")
            return True

        # Additional checks for other endgame conditions like insufficient material can be added here.
        return False
    
    def get_valid_moves_for_piece(self, position):
    
        node = self.nodes.get(position)
        if not node or not node.piece:
            return []  # No piece at the given position

        piece = node.piece
        if "Pawn" in piece:
            return self.get_valid_pawn_moves_bfs(position)
        elif "Knight" in piece:
            return self.get_valid_knight_moves_bfs(position)
        elif "Rook" in piece:
            return self.get_valid_rook_moves_bfs(position)
        elif "Bishop" in piece:
            return self.get_valid_bishop_moves_bfs(position)
        elif "Queen" in piece:
            return self.get_valid_queen_moves_bfs(position)
        elif "King" in piece:
            valid_moves = self.get_valid_king_moves_bfs(position)
            # Add castling moves
            player = "white" if node.color == "white" else "black"
            if self.can_castle(player, "kingside"):
                valid_moves.append((position[0], 6))
            if self.can_castle(player, "queenside"):
                valid_moves.append((position[0], 2))
            return valid_moves

        return []  # Default empty list if piece type is unknown


    def draw_timers(self, screen):
        """Draw the timers and time bars for each player."""
        # Timer dimensions
        
       
        if self.game_type != "rapid":
            return
        

                
        timer_width = 200  
        timer_height = 40  
        bar_length = 200   
        bar_height = 20    
        margin = 20        

        black_timer_x = WIDTH - timer_width - margin - 100
        black_timer_y = margin + 5

        pygame.draw.rect(screen, BROWN, (black_timer_x, black_timer_y+50, timer_width, timer_height))
        black_time_text = self.font.render(f"Black Time Left: {int(self.players['black'].timer)}s", True, WHITE)
        screen.blit(black_time_text, (black_timer_x + 5, black_timer_y + 50))

        black_bar_x = WIDTH - bar_length - margin - 100
        black_bar_y = black_timer_y + timer_height + 70

        pygame.draw.rect(screen, BEIGE, (black_bar_x, black_bar_y, bar_length, bar_height))  # Background
        pygame.draw.rect(screen, GREEN, (black_bar_x, black_bar_y,
                                        int((self.players['black'].timer / 300) * bar_length), bar_height))  # Remaining time

        white_timer_x = WIDTH - timer_width - margin - 100
        white_timer_y = HEIGHT - timer_height - margin - 100

        pygame.draw.rect(screen, BROWN, (white_timer_x, white_timer_y, timer_width, timer_height))
        white_time_text = self.font.render(f"White Time Left: {int(self.players['white'].timer)}s", True, WHITE)
        screen.blit(white_time_text, (white_timer_x + 5, white_timer_y + 10))

        white_bar_x = WIDTH - bar_length - margin - 100
        white_bar_y = white_timer_y - bar_height - 10

        pygame.draw.rect(screen, BEIGE, (white_bar_x, white_bar_y, bar_length, bar_height))  # Background
        pygame.draw.rect(screen, GREEN, (white_bar_x, white_bar_y,
                                        int((self.players['white'].timer / 300) * bar_length), bar_height))  # Remaining time

        
    def update_timers(self):
        """Update the timer for the current player and check for timeout."""
        if self.game_type != "rapid":
            return None  

        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000  
        self.last_time = current_time  
        
        current_player = 'white' if self.players['white'].turn else 'black'
        self.players[current_player].timer = max(0, self.players[current_player].timer - elapsed)

        # Check if time runs out
        if self.players[current_player].timer == 0:
            winner = 'black' if current_player == 'white' else 'white'
            return {"winner": winner, "reason": "Out of time"}

        return None  # Game continues
    
    
    
    
def open_promotion_window(player_color, main_screen):
    """Displays the promotion choices on the main screen."""
    window_width, window_height = 400, 200
    border_thickness = 5  # Set the thickness of the border
    promotion_surface = pygame.Surface((window_width, window_height))
    promotion_surface.fill((255, 255, 255))

    promotion_choices = ['Queen', 'Rook', 'Bishop', 'Knight']
    piece_images = {piece: PIECE_IMAGES[f"{piece}_{player_color}"] for piece in promotion_choices}

    # Resize images
    piece_images = {piece: pygame.transform.scale(img, (80, 80)) for piece, img in piece_images.items()}

    def draw_promotion_choices():
        # Fill the promotion surface with white
        promotion_surface.fill((255, 255, 255))

        # Draw the border
        pygame.draw.rect(promotion_surface, (0, 0, 0), (0, 0, window_width, window_height), border_thickness)

        # Draw the piece images
        for i, (piece, img) in enumerate(piece_images.items()):
            x = i * 100 + 20
            y = 60
            promotion_surface.blit(img, (x, y))
        
        # Blit the promotion surface onto the main screen
        main_screen.blit(promotion_surface, (main_screen.get_width() // 2 - window_width // 2, main_screen.get_height() // 2 - window_height // 2))
        pygame.display.flip()

    promotion_piece = None
    running = True
    while running:
        draw_promotion_choices()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                relative_x = mouse_x - (main_screen.get_width() // 2 - window_width // 2)
                relative_y = mouse_y - (main_screen.get_height() // 2 - window_height // 2)
                for i, piece in enumerate(promotion_choices):
                    x = i * 100 + 20
                    y = 60
                    if x <= relative_x <= x + 80 and y <= relative_y <= y + 80:
                        promotion_piece = piece
                        running = False
                        break

    return promotion_piece

    


def show_message_box( screen, message):
        """Displays a message box with the given message."""
        font = pygame.font.SysFont(None, 48)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)  # Adjust transparency level (0 - 255)

        screen.blit(overlay, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()  

    
def end_screen(screen, winner):
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



