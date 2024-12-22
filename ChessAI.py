class ChessAI:
    def __init__(self, color, depth=2):
        self.color = color  # 'white' or 'black'
        self.depth = depth  # Depth of the Minimax search

    def get_best_move(self, chess_graph):
        best_move = None
        best_value = float('-inf') if self.color == 'white' else float('inf')

        for move in self.get_all_possible_moves(chess_graph, self.color):
            value = self.minimax(chess_graph, move, self.depth, float('-inf'), float('inf'), self.color == 'black')
            if (self.color == 'white' and value > best_value) or (self.color == 'black' and value < best_value):
                best_value = value
                best_move = move
        
        return best_move

    def get_all_possible_moves(self, chess_graph, color):
        moves = []
        for pos, node in chess_graph.nodes.items():
            if node.color == color:
                if "Pawn" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_pawn_moves_bfs(pos)])
                elif "Knight" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_knight_moves_bfs(pos)])
                elif "Rook" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_rook_moves_bfs(pos)])
                elif "Bishop" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_bishop_moves_bfs(pos)])
                elif "Queen" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_queen_moves_bfs(pos)])
                elif "King" in node.piece:
                    moves.extend([(pos, move) for move in chess_graph.get_valid_king_moves_bfs(pos)])
        return moves

    def minimax(self, chess_graph, move, depth, alpha, beta, maximizing_player):
        if depth == 0 or chess_graph.is_game_over():
            return self.evaluate_board(chess_graph)

        source, destination = move
        player = 'white' if maximizing_player else 'black'
        original_state = (
            (source, chess_graph.nodes[source].piece, chess_graph.nodes[source].image, chess_graph.nodes[source].color),
            (destination, chess_graph.nodes[destination].piece, chess_graph.nodes[destination].image, chess_graph.nodes[destination].color),
            chess_graph.king_positions.copy(),
            player,  # Add player to match undo_simulated_move attributes
            chess_graph.captured_white_pieces.copy(),  # Track captured white pieces
            chess_graph.captured_black_pieces.copy()   # Track captured black pieces
        )

        chess_graph.move_piece(source, destination, simulated=True)

        if maximizing_player:
            max_eval = float('-inf')
            for next_move in self.get_all_possible_moves(chess_graph, 'white'):
                eval = self.minimax(chess_graph, next_move, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            best_eval = max_eval
        else:
            min_eval = float('inf')
            for next_move in self.get_all_possible_moves(chess_graph, 'black'):
                eval = self.minimax(chess_graph, next_move, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            best_eval = min_eval

        chess_graph.undo_simulated_move(original_state)
        return best_eval




    def evaluate_board(self, chess_graph):
        value = 0
        piece_values = {'Pawn': 1, 'Knight': 3, 'Bishop': 3, 'Rook': 5, 'Queen': 9, 'King': 0}
        for node in chess_graph.nodes.values():
            if node.piece:
                piece_value = piece_values[node.piece.split('_')[0]]
                if node.color == 'white':
                    value += piece_value
                else:
                    value -= piece_value
        return value
