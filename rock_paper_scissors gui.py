import tkinter as tk
from tkinter import messagebox, ttk
import random


class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("500x550")
        self.root.resizable(True, True)

        # Game variables
        self.pick = ('rock', 'paper', 'scissors')
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.rounds_played = 0
        self.max_rounds = 5
        self.game_active = True

        # Create GUI
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Rock Paper Scissors",
            font=("Arial", 20, "bold"),
            fg="darkblue"
        )
        title_label.pack(pady=15)

        # Round counter
        self.round_label = tk.Label(
            self.root,
            text=f"Round: 1/{self.max_rounds}",
            font=("Arial", 12),
            fg="purple"
        )
        self.round_label.pack(pady=5)

        # Instruction
        instruction = tk.Label(
            self.root,
            text="Choose your weapon:",
            font=("Arial", 14)
        )
        instruction.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        # Choice buttons
        self.rock_btn = tk.Button(
            button_frame,
            text="Rock",
            font=("Arial", 14),
            width=8,
            height=2,
            bg="lightgray",
            command=lambda: self.play_game("rock")
        )
        self.rock_btn.grid(row=0, column=0, padx=10)

        self.paper_btn = tk.Button(
            button_frame,
            text="Paper",
            font=("Arial", 14),
            width=8,
            height=2,
            bg="lightyellow",
            command=lambda: self.play_game("paper")
        )
        self.paper_btn.grid(row=0, column=1, padx=10)

        self.scissors_btn = tk.Button(
            button_frame,
            text="Scissors",
            font=("Arial", 14),
            width=8,
            height=2,
            bg="lightblue",
            command=lambda: self.play_game("scissors")
        )
        self.scissors_btn.grid(row=0, column=2, padx=10)

        # Result display
        self.result_frame = tk.LabelFrame(self.root, text="Game Result", font=("Arial", 12))
        self.result_frame.pack(pady=15, padx=20, fill="both", expand=True)

        self.computer_choice_label = tk.Label(
            self.result_frame,
            text="Computer will choose after you",
            font=("Arial", 12),
            fg="purple"
        )
        self.computer_choice_label.pack(pady=8)

        self.result_label = tk.Label(
            self.result_frame,
            text="Make your choice!",
            font=("Arial", 14, "bold"),
            fg="darkgreen"
        )
        self.result_label.pack(pady=8)

        # Score display
        score_frame = tk.Frame(self.root)
        score_frame.pack(pady=10)

        self.score_label = tk.Label(
            score_frame,
            text="Score: You 0 - Computer 0 - Draws 0",
            font=("Arial", 12, "bold"),
            fg="darkred"
        )
        self.score_label.pack()

        # Game status
        self.status_label = tk.Label(
            self.root,
            text="Game in progress...",
            font=("Arial", 11),
            fg="gray"
        )
        self.status_label.pack(pady=5)

        # Button frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=15)

        # New game button
        self.new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 12),
            bg="lightgreen",
            command=self.reset_game,
            state="disabled"  # Disabled until game ends
        )
        self.new_game_btn.grid(row=0, column=0, padx=10)

        # Exit button
        self.exit_btn = tk.Button(
            control_frame,
            text="Exit Game",
            font=("Arial", 12),
            bg="lightcoral",
            command=self.exit_game
        )
        self.exit_btn.grid(row=0, column=1, padx=10)

    def play_game(self, player_choice):
        if not self.game_active:
            return

        # Computer makes random choice
        computer_choice = random.choice(self.pick)

        # Update computer choice display
        self.computer_choice_label.config(text=f"Computer chose: {computer_choice.title()}")

        # Determine winner
        if player_choice == computer_choice:
            result_text = "It's a Draw!"
            result_color = "blue"
            self.draws += 1
        elif (
                (player_choice == 'rock' and computer_choice == 'scissors') or
                (player_choice == 'scissors' and computer_choice == 'paper') or
                (player_choice == 'paper' and computer_choice == 'rock')
        ):
            result_text = "You Win!"
            result_color = "green"
            self.player_score += 1
        else:
            result_text = "You Lose!"
            result_color = "red"
            self.computer_score += 1

        # Update result display
        self.result_label.config(
            text=result_text,
            fg=result_color
        )

        # Update round counter
        self.rounds_played += 1
        self.round_label.config(text=f"Round: {self.rounds_played}/{self.max_rounds}")

        # Update score display
        self.update_display()

        # Check if game should end
        if self.rounds_played >= self.max_rounds:
            self.end_game()

    def update_display(self):
        self.score_label.config(
            text=f"Score: You {self.player_score} - Computer {self.computer_score} - Draws {self.draws}"
        )

    def end_game(self):
        self.game_active = False

        # Determine final winner
        if self.player_score > self.computer_score:
            winner_text = "🎉 You Win the Game! 🎉"
            winner_color = "green"
        elif self.computer_score > self.player_score:
            winner_text = "💻 Computer Wins the Game! 💻"
            winner_color = "red"
        else:
            winner_text = "🤝 It's a Tie Game! 🤝"
            winner_color = "blue"

        # Update status label
        self.status_label.config(
            text=winner_text,
            fg=winner_color,
            font=("Arial", 14, "bold")
        )

        # Enable new game button
        self.new_game_btn.config(state="normal")

        # Disable choice buttons
        self.rock_btn.config(state="disabled")
        self.paper_btn.config(state="disabled")
        self.scissors_btn.config(state="disabled")

        # Show final results message
        messagebox.showinfo(
            "Game Over",
            f"Final Score:\nYou: {self.player_score}\nComputer: {self.computer_score}\nDraws: {self.draws}\n\n{winner_text}"
        )

    def reset_game(self):
        # Reset game variables
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        self.rounds_played = 0
        self.game_active = True

        # Reset displays
        self.computer_choice_label.config(text="Computer will choose after you")
        self.result_label.config(text="Make your choice!", fg="darkgreen")
        self.round_label.config(text=f"Round: 1/{self.max_rounds}")
        self.status_label.config(text="Game in progress...", fg="gray", font=("Arial", 11))

        # Update score display
        self.update_display()

        # Enable choice buttons
        self.rock_btn.config(state="normal")
        self.paper_btn.config(state="normal")
        self.scissors_btn.config(state="normal")

        # Disable new game button during play
        self.new_game_btn.config(state="disabled")

    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()