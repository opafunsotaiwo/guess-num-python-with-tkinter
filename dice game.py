import random

print("Welcome to the Dice Rolling Game!")
while True:
    print("\nEnter 'y' to roll or any other key to exit: ")
    player = input().strip().lower()
    if player == 'y':
        # Roll two dice
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        # Display the results
        print(f"{die1}", f"{die2}")
    else:
        print("Thanks for playing!")
        break