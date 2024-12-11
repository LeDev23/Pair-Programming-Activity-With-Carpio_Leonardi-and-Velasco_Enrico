#Carpio, Leonardi Miguel and Velasco, Enrico Miguel
#CS317 Sotware Programming Activity 1: TicTacToe
#Date: 2024-09-29
#CS3A

import tkinter as tk                     # Adds UI to the game
from tkinter import messagebox
import random
import copy
from operator import iadd

class TicTacToe:
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def __init__(self, root):
        self.board = [" "] * 9
        self.curr_player = random.choice(["X", "O"])  # Randomly assigns who goes first
        self.move_number = 0
        self.x_wins = 0
        self.o_wins = 0
        self.winning_squares = []
        self.game_over = False
        self.button = []

        # Setting up the GUI for the Game
        root.title("Tic-Tac-Toe")

        self.info_text = tk.StringVar()
        self.info_text.set(f"It is {self.curr_player}'s turn")
        self.info_label = tk.Label(root, textvariable=self.info_text)
        self.info_label.grid(row=0, column=0, columnspan=3)

        self.score_text = tk.StringVar()
        self.score_text.set(f"X: {self.x_wins} | O: {self.o_wins}")
        self.score_label = tk.Label(root, textvariable=self.score_text)
        self.score_label.grid(row=1, column=0, columnspan=3)

        self.moves = [tk.StringVar() for _ in range(9)]
        for square in range(9):
            temp_button = tk.Button(root, textvariable=self.moves[square], height=4, width=8, font=("Helvetica", 20),
                                    command=lambda s=square: self.make_move(s))
            temp_button.grid(row=(square // 3) + 2, column=(square % 3), sticky="nsew")
            self.button.append(temp_button)

        self.ai_on_var = tk.IntVar()
        self.ai_on_checkbox = tk.Checkbutton(root, text="Switch AI", variable=self.ai_on_var)
        self.ai_on_checkbox.grid(row=6, column=2)

        self.difficulty_var = tk.StringVar(value="Medium")  # This would be the default difficulty
        difficulty_menu = tk.OptionMenu(root, self.difficulty_var, "Easy", "Medium", "Hard")
        difficulty_menu.grid(row=6, column=1)

        # Add a Restart button
        restart_button = tk.Button(root, text="Restart", command=self.reset_game)
        restart_button.grid(row=6, column=0)

        # AI makes the first move if it's the AI's turn
        if self.curr_player == "O" and self.ai_on_var.get():
            self.ai_move()

    def make_move(self, move):
        if self.game_over or self.board[move] != " ":
            return

        self.move_number += 1
        self.board[move] = self.curr_player
        self.moves[move].set(self.curr_player)
        self.button[move].config(state="disabled")

        if self.curr_player == "X":
            self.curr_player = "O"
            self.info_text.set("It is O's turn")
        else:
            self.curr_player = "X"
            self.info_text.set("It is X's turn")

        winner = self.check_winner(self.board)
        if winner:
            self.end_game(winner)
        elif self.move_number == 9:
            self.end_game("Tie")

        if self.curr_player == "O" and self.ai_on_var.get() and not self.game_over:
            self.ai_move()

    def ai_move(self):
        difficulty = self.difficulty_var.get()
        random_move_prob = self.get_random_move_probability(difficulty)

        if random.random() < random_move_prob:  # Decides when to make a random move
            move = self.get_random_move()
        else:
            move = self.get_best_move("O", self.board)

        self.make_move(move)

    def get_random_move_probability(self, difficulty):
        if difficulty == "Easy":
            return 0.8  # This means that the AI has 80% chance for a random move
        elif difficulty == "Medium":
            return 0.5  # This means that the AI has 50% chance for a random move
        else:  # Hard difficulty
            return 0.2  # This means that the AI has 20% chance for a random move

    def get_random_move(self):
        available_moves = [i for i in range(9) if self.board[i] == " "]
        return random.choice(available_moves)

    def get_best_move(self, player, board):
        best_score = -1000
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, 0, False)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -1000
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, board):
        for combo in TicTacToe.winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
                self.winning_squares = combo
                return board[combo[0]]
        return None

    def end_game(self, result):
        if result == "Tie":
            self.info_text.set("It's a tie!")
        else:
            self.info_text.set(f"{result} wins!")
            if result == "X":
                self.x_wins += 1
            else:
                self.o_wins += 1
                for i in self.winning_squares:
                    self.button[i].config(disabledforeground="red")

            self.game_over = True
            for b in self.button:
                b.config(state="disabled")

        # Update the score display
        self.score_text.set(f"X: {self.x_wins} | O: {self.o_wins}")

    def reset_game(self):
        self.curr_player = random.choice(["X", "O"])  # Randomly chooses who goes first
        self.move_number = 0
        self.board = [" "] * 9
        self.info_text.set(f"It is {self.curr_player}'s turn")
        self.game_over = False
        for i in range(9):
            self.moves[i].set(" ")
            self.button[i].config(state="normal", disabledforeground="black")
        if self.curr_player == "O" and self.ai_on_var.get():
            self.ai_move()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
