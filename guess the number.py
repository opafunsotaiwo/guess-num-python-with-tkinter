import tkinter as tk
import random
from tkinter import messagebox

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Initialize game variables
        self.no_to_guess = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 3

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.root,
            text="Guess a Number Between 1 and 100",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        # Answer label (initially hidden)
        self.answer_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            fg="green"
        )
        self.answer_label.pack(pady=5)

        # Instruction label
        instruction_label = tk.Label(
            self.root,
            text="Enter your guess:",
            font=("Arial", 12)
        )
        instruction_label.pack(pady=5)

        # Entry field for guess with validation
        vcmd = (self.root.register(self.validate_input), '%P')
        self.guess_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center",
            width=10,
            validate="key",
            validatecommand=vcmd
        )
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", self.check_guess)
        self.guess_entry.focus()

        # Attempts remaining label
        self.attempts_remaining_label = tk.Label(
            self.root,
            text=f"Attempts remaining: {self.max_attempts - self.attempts}",
            font=("Arial", 10),
            fg="purple"
        )
        self.attempts_remaining_label.pack(pady=5)

        # Submit button
        submit_button = tk.Button(
            self.root,
            text="Submit Guess",
            command=self.check_guess,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        submit_button.pack(pady=10)

        # Result label
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            fg="blue",
            wraplength=400
        )
        self.result_label.pack(pady=10)

        # Attempts counter
        self.attempts_label = tk.Label(
            self.root,
            text="Attempts: 0",
            font=("Arial", 10)
        )
        self.attempts_label.pack(pady=5)

        # New game button
        new_game_button = tk.Button(
            self.root,
            text="New Game",
            command=self.new_game,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white"
        )
        new_game_button.pack(pady=10)

    def validate_input(self, new_text):
        # Only allow digits or empty string
        if new_text == "" or new_text.isdigit():
            return True
        return False

    def check_guess(self, event=None):
        # Get the guess from the entry field
        guess_text = self.guess_entry.get()

        # Check if input is empty
        if not guess_text:
            self.result_label.config(text="Please enter a number!", fg="red")
            return

        try:
            guess = int(guess_text)
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            self.attempts_remaining_label.config(
                text=f"Attempts remaining: {max(0, self.max_attempts - self.attempts)}"
            )

            if guess < 1 or guess > 100:
                self.result_label.config(text="Please enter a number between 1 and 100", fg="red")
            elif guess < self.no_to_guess:
                self.result_label.config(text="Too low! Try again.", fg="red")
            elif guess > self.no_to_guess:
                self.result_label.config(text="Too high! Try again.", fg="red")
            else:
                self.result_label.config(text=f"Congratulations! You've won in {self.attempts} attempts!", fg="green")
                messagebox.showinfo("You Won!",
                                    f"Congratulations! You guessed the number {self.no_to_guess} in {self.attempts} attempts!")
                self.guess_entry.config(state="disabled")
                return

            # Check if maximum attempts reached
            if self.attempts >= self.max_attempts:
                # Show the correct answer only when player fails
                self.answer_label.config(text=f"The number was: {self.no_to_guess}")
                self.result_label.config(
                    text=f"Game over! You've used all {self.max_attempts} attempts. Click 'New Game' to play again.",
                    fg="red"
                )
                messagebox.showinfo("Game Over",
                                   f"Sorry, you've used all {self.max_attempts} attempts. The number was {self.no_to_guess}.")
                self.guess_entry.config(state="disabled")

            # Clear the entry field
            self.guess_entry.delete(0, tk.END)

        except ValueError:
            self.result_label.config(text="That's not a valid number!", fg="red")
            self.guess_entry.delete(0, tk.END)

    def new_game(self):
        # Reset game variables
        self.no_to_guess = random.randint(1, 100)
        self.attempts = 0

        # Reset UI elements - hide the answer again
        self.answer_label.config(text="")
        self.result_label.config(text="")
        self.attempts_label.config(text="Attempts: 0")
        self.attempts_remaining_label.config(text=f"Attempts remaining: {self.max_attempts}")
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()


# Create the main window and start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()