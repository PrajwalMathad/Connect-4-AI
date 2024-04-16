import random
import numpy as np
import matplotlib.pyplot as plt


class ConnectFour:
    random_calls = 0

    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.player = 1

    def is_valid_move(self, column):
        return self.board[0][column] == 0

    def make_move(self, column):
        for row in range(5, -1, -1):
            # print("Row", row, "Column", column)
            if self.board[row][column] == 0:
                self.board[row][column] = self.player
                self.switch_player()
                # self.print_board()
                break

    def switch_player(self):
        self.player = 3 - self.player

    def is_winner(self, player):
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if np.all(self.board[row, col : col + 4] == player):
                    return True

        # Check vertical
        for row in range(3):
            for col in range(7):
                if np.all(self.board[row : row + 4, col] == player):
                    return True

        # Check diagonal
        for row in range(3):
            for col in range(4):
                if np.all(
                    self.board[row : row + 4, col : col + 4].diagonal() == player
                ):
                    return True
                if np.all(
                    np.fliplr(self.board[row : row + 4, col : col + 4]).diagonal()
                    == player
                ):
                    return True

        return False

    def is_board_full(self):
        return np.all(self.board != 0)

    def get_valid_moves(self):
        return [col for col in range(7) if self.is_valid_move(col)]

    def get_state(self):
        return self.board.copy(), self.player

    def print_board(self):
        print(self.board)

    def play_random_move(self):
        self.random_calls += 1
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        self.make_move(move)

    def is_terminal(self):
        return (
            is_winner(self.board, 1) or is_winner(self.board, 2) or self.is_board_full()
        )


def is_winner(board, player):
    # Check rows
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check columns
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonals
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + i][col + 3 - i] == player for i in range(4)):
                return True

    return False


def heuristic(board, player):
    scores = [0] * 7

    # Check for potential winning moves for both players
    for col in range(7):
        if board[5][col] != 0:
            continue

        # Simulate making a move in this column
        temp_board = np.copy(board)
        for row in range(6):
            if temp_board[row][col] == 0:
                temp_board[row][col] = player
                break

        # Evaluate the board state using the refined scoring system
        scores[col] = evaluate_board(temp_board, player)

    return scores


def evaluate_board(board, player):
    score = 0

    # Check for potential winning moves for the current player
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                score += 100  # Add a high score for potential winning moves

    # Check for potential winning moves for the opponent
    opponent = 3 - player
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == opponent for i in range(4)):
                score -= 50  # Subtract a score for opponent's potential winning moves

    # Prioritize center column
    center_column = 3
    for row in range(6):
        if board[row][center_column] == player:
            score += 10  # Add a score for occupying the center column
        elif board[row][center_column] == opponent:
            score -= 5  # Subtract a score for opponent occupying the center column

    # Balance defense and offense
    defense_score = evaluate_defense(board, opponent)
    offense_score = evaluate_offense(board, player)
    score += offense_score - defense_score

    # Add more scoring criteria as needed based on game strategy

    return score


def evaluate_defense(board, player):
    # Evaluate the defensive strength of the board for the given player
    # For example, count the number of opponent's potential winning moves
    return sum(
        1
        for row in range(6)
        for col in range(4)
        if all(board[row][col + i] == player for i in range(4))
    )


def evaluate_offense(board, player):
    # Evaluate the offensive strength of the board for the given player
    # For example, count the number of player's potential winning moves
    return sum(
        1
        for row in range(6)
        for col in range(4)
        if all(board[row][col + i] == player for i in range(4))
    )


class MonteCarloTreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, state):
        child = MonteCarloTreeNode(state, self)
        self.children.append(child)
        return child

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())

    def is_terminal(self):
        # board, _ = self.state.get_state()
        return (
            is_winner(self.state.board, 1)
            or is_winner(self.state.board, 2)
            or self.state.is_board_full()
        )


def monte_carlo_tree_search(root_state, iterations, epochs):
    root = MonteCarloTreeNode(root_state)
    win_rates = []
    avg_depths = []
    for _ in range(epochs):
        total_depth = 0
        ai_wins = 0
        for i in range(iterations):
            node = root
            state = root_state
            depth = 0
            # Selection
            while not node.is_terminal():
                if state.player == 1:
                    # print("selection for player 1")
                    if node.is_fully_expanded():
                        # Use UCB for Player 1
                        ucb_values = [
                            (child.wins / child.visits)
                            + np.sqrt(2 * np.log(node.visits) / child.visits)
                            for child in node.children
                        ]
                        selected_index = np.argmax(ucb_values)
                        node = node.children[selected_index]
                        # print("Player 1 move in selection expanded")
                        state.make_move(selected_index)
                    else:
                        valid_moves = state.get_valid_moves()
                        # print("Player 1 move in selection")
                        random_move = random.choice(valid_moves)
                        new_state = ConnectFour()  # Create a new ConnectFour object
                        new_state.board, new_state.player = (
                            state.get_state()
                        )  # Set board and player

                        # scores = heuristic(new_state.board, new_state.player)
                        # valid_moves = new_state.get_valid_moves()
                        # selected_move = max(valid_moves, key=lambda x: scores[x])
                        # new_state.make_move(selected_move)
                        new_state.make_move(random_move)  # Make the random move
                        node = node.add_child(new_state)
                        state = new_state
                else:
                    # Player 2 makes a move using heuristic
                    # print("Player 2 move in selection")
                    state.play_random_move()
                    # scores = heuristic(state.board, state.player)
                    # valid_moves = state.get_valid_moves()
                    # selected_move = max(valid_moves, key=lambda x: scores[x])
                    # state.make_move(selected_move)
                    for child in node.children:
                        if child.state == state:
                            node = child
                            break
                    else:
                        node = node.add_child(state)
                        break
                depth += 1

            # Expansion
            if not node.is_terminal() and not node.is_fully_expanded():
                valid_moves = state.get_valid_moves()
                random_move = random.choice(valid_moves)
                new_state = ConnectFour()  # Create a new ConnectFour object
                new_state.board, new_state.player = (
                    state.get_state()
                )  # Set board and player
                new_state.make_move(random_move)  # Make the random move
                # random.play_random_move()
                node = node.add_child(new_state)
                state = new_state
                depth += 1

            # Simulation
            sim_state = node.state.get_state()[0].copy(), node.state.get_state()[1]
            sim_game = ConnectFour()
            sim_game.board, sim_game.player = sim_state
            while not sim_game.is_terminal():
                if sim_game.player == 1:
                    # Player 1 selects moves using the heuristic
                    # print("Player 1 move")
                    sim_game.play_random_move()
                    # scores = heuristic(sim_game.board, sim_game.player)
                    # valid_moves = sim_game.get_valid_moves()
                    # selected_move = max(valid_moves, key=lambda x: scores[x])
                    # sim_game.make_move(selected_move)
                else:
                    # print("Player 2 move")
                    sim_game.play_random_move()
                    # scores = heuristic(sim_game.board, sim_game.player)
                    # valid_moves = sim_game.get_valid_moves()
                    # selected_move = max(valid_moves, key=lambda x: scores[x])
                    # sim_game.make_move(selected_move)
                depth += 1

            # Backpropagation
            winner = (
                1
                if is_winner(sim_game.board, 1)
                else 2 if is_winner(sim_game.board, 2) else 0
            )
            if winner == 1:
                ai_wins += 1
            while node is not None:
                node.visits += 1
                if winner == 1:
                    node.wins += 1
                elif winner == 2:
                    node.wins -= 1
                node = node.parent

            total_depth += depth
            # print(
            #     "Winner of game", i, " ", winner, "random calls", sim_game.random_calls
            # )
            # print(sim_game.board)

        average_depth = total_depth / iterations
        win_rate = (ai_wins / iterations) * 100
        win_rates.append(win_rate)
        avg_depths.append(average_depth)
        print("Average depth", average_depth)
        print("Win rate", win_rate)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), win_rates, marker="o")
    plt.title("Win Rate Over Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Win Rate (%)")
    plt.grid(True)

    # Plot average depths
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs + 1), avg_depths, marker="o", color="orange")
    plt.title("Average Depth Over Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Average Depth")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    game = ConnectFour()
    # game.print_board()
    monte_carlo_tree_search(game, 20, 10)

    # while not game.is_winner(1) and not game.is_winner(2) and not game.is_board_full():
    #     if game.player == 1:
    #         # print("AI")
    #         monte_carlo_tree_search(game, 5)
    #         # game.make_move(column)
    #         # game.print_board()
    #     else:
    #         print("Human")
    #         valid_moves = game.get_valid_moves()
    #         print("Valid moves:", valid_moves)
    #         column = int(input("Enter your move: "))
    #         game.make_move(column)
    #         game.print_board()
    #     game.switch_player()

    # if game.is_winner(1):
    #     print("Player 1 wins!")
    # elif game.is_winner(2):
    #     print("Player 2 wins!")
    # else:
    #     print("It's a draw!")
