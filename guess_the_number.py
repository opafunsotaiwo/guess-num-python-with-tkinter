import random

no_to_guess = random.randint(1, 100)
while True:
    try:
        guess = int(input("Guess a number between 1 and 100: "))
        if guess < no_to_guess:
            print("Too low")
        elif guess > no_to_guess:
            print("Too high")
        else:
            print('you have won')
            break
    except ValueError:
        print("That's not a number")


