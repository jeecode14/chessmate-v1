import chess
import chess.engine
import json
import os

# Set the path to your Stockfish engine executable
stockfish_path = "stockfish/stockfish-windows-x86-64-avx2.exe"

data_file = "taken_pieces_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return {}

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

def get_opponent_move():
    while True:
        move = input("Enter opponent's move (e.g., e7e5): ")
        if move in [str(m) for m in board.legal_moves]:
            return move
        else:
            print("Invalid move. Please enter a valid move.")

def main():
    global board
    # Create a new chess board
    board = chess.Board()

    # Load previous data
    taken_pieces_data = load_data()

    # Start the Stockfish engine
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        # White's first move is always e2e4
        first_move = "e2e4"
        print(f"\nWhite's move: {first_move}")
        board.push(chess.Move.from_uci(first_move))
        print(board)

        while not board.is_game_over():
            # Get the opponent's move (black)
            print("\nOpponent's turn:")
            opponent_move = get_opponent_move()
            board.push(chess.Move.from_uci(opponent_move))
            

            # Predict the best move for White
            print("\nWhite's move:")
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
            print(board)

        # Print the result of the game
        print("\nGame over:", board.result())

if __name__ == "__main__":
    main()
