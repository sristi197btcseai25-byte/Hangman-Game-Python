import random

# Function to choose a random word from a file
def choose_word_from_file(filename):
    try:
        with open(filename, 'r') as file:
            words = file.read().splitlines()
        return random.choice(words)
    except FileNotFoundError:
        return None

hangman_stages = [
    # 0 Errors: Empty Gallows
    (
        "  +---+\n"
        "  |   |\n"
        "      |\n"
        "      |\n"
        "      |\n"
        "      |\n"
        "========="
    ),
    # 1 Error: Head
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        "      |\n"
        "      |\n"
        "      |\n"
        "========="
    ),
    # 2 Errors: Head + Torso
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        "  |   |\n"
        "      |\n"
        "      |\n"
        "========="
    ),
    # 3 Errors: Left Arm
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        " /|   |\n"
        "      |\n"
        "      |\n"
        "========="
    ),
    # 4 Errors: Right Arm
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        " /|\\  |\n"
        "      |\n"
        "      |\n"
        "========="
    ),
    # 5 Errors: Left Leg
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        " /|\\  |\n"
        " /    |\n"
        "      |\n"
        "========="
    ),
    # 6 Errors: Right Leg (Game Over)
    (
        "  +---+\n"
        "  |   |\n"
        "  O   |\n"
        " /|\\  |\n"
        " / \\  |\n"
        "      |\n"
        "========="
    )
]

def print_header(title):
    print("\n" + "*" * 40)
    print(title.center(40))
    print("*" * 40 + "\n")

# Main Hangman game logic
max_attempts = 6

while True:
    print_header("WELCOME TO HANGMAN")
    
    guessed_letters = []
    guessed_words = []
    attempts = 0
    
    print("Select a Genre:")
    print("  1. Countries")
    print("  2. Eatables")
    print("  3. Animals")
    print("  4. Exit Game")
    
    try:
        choice_input = input("\n>>> Enter choice (1-4): ")
        genre = int(choice_input)
    except ValueError:
        print("!!! Invalid input. Please enter a number. !!!")
        continue

    # File Selection Logic
    if genre == 1:
        word_to_guess = choose_word_from_file('Countries.txt')  
    elif genre == 2:
        word_to_guess = choose_word_from_file('Food.txt')
    elif genre == 3:
        word_to_guess = choose_word_from_file('Animal.txt')
    elif genre == 4:
        print("Exiting... See you next time!")
        break
    else:
        print("!!! Number out of range. Try again. !!!")
        continue
    
    if word_to_guess is None:
        print("Error: The text file for that genre was not found.")
        break
    
    # Difficulty Selection
    print("\nSelect Difficulty:")
    print("  1. Easy (Vowels revealed)")
    print("  2. Hard (No help)")
    
    try:
        diff_input = input("\n>>> Enter difficulty (1-2): ")
        diff = int(diff_input)
    except ValueError:
        print("Defaulting to Easy mode.")
        diff = 1

    print("\nStarting game... The word has " + str(len(word_to_guess)) + " letters.")

    # --- GAME LOOP ---
    while True:
        # 1. Construct the word display based on difficulty
        display = ""
        if diff == 1:
            for letter in word_to_guess:
                if letter.lower() in guessed_letters or letter.lower() in 'aeiou':
                    display += letter + " "
                else:
                    display += "_ "
        elif diff == 2:
            for letter in word_to_guess:
                if letter.lower() in guessed_letters or letter.upper() in guessed_letters:
                    display += letter + " "
                else:
                    display += "_ "
        else:
            diff = 1
            continue

        # 2. Print the "Dashboard"
        print("\n" + "="*30)
        print("Attempts Left: " + str(max_attempts - attempts))
        print(hangman_stages[attempts])
        print("WORD:    " + display)
        # Use .join to make the list of letters look nice
        print("USED:    " + ", ".join(guessed_letters))
        print("="*30)
        
        # 3. Check Win Condition
        if '_' not in display:
            print("\n" + "#"*40)
            print("VICTORY! You guessed the word: " + word_to_guess)
            print("#"*40 + "\n")
            break

        # 4. Get Input
        guess = input("\n>>> Guess a letter or word (or 'exit'): ").lower().strip()

        if guess == 'exit':
            attempts = max_attempts 
            break  

        # 5. Process Logic
        if len(guess) == 1:
            if not guess.isalpha():
                 print("!!! Please enter a letter, not a number/symbol. !!!")
                 continue

            if guess in guessed_letters:
                print("--> You already guessed '" + guess + "'. Try a new one.")
                continue
            
            guessed_letters.append(guess)

            if guess not in word_to_guess.lower():
                attempts += 1
                print("--> Sorry, '" + guess + "' is NOT in the word.")
            else:
                print("--> Good job! '" + guess + "' is in the word.")
                
        elif len(guess) > 1:
            if guess in guessed_words:
                 print("--> You already guessed that word.")
                 continue
            
            guessed_words.append(guess)

            if guess == word_to_guess.lower():
                print("\n" + "#"*40)
                print("VICTORY! You guessed the word: " + word_to_guess)
                print("#"*40 + "\n")
                break
            else:
                attempts += 1
                print("--> '" + guess + "' is not the correct word.")
        else:   
            print("!!! Invalid input. !!!")
       
        # 6. Check Lose Condition
        if attempts == max_attempts:
            print(hangman_stages[attempts]) 
            print("\n" + "x"*40)
            print("GAME OVER!")
            print("The word was: " + word_to_guess)
            print("x"*40 + "\n")
            break  

    # Play Again?
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        break  

print_header("THANKS FOR PLAYING")