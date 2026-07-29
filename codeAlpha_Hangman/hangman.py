import random
import os

# List of predefined words for the Hangman game
WORDS = ["python", "programming", "developer", "computer", "algorithm"]

# Hangman ASCII art stages representing the gallows
HANGMAN_STAGES = [
    # 0 incorrect guesses
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    # 1 incorrect guess: Head
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    # 2 incorrect guesses: Torso
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    # 3 incorrect guesses: Left arm
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    # 4 incorrect guesses: Right arm
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    # 5 incorrect guesses: Left leg
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    # 6 incorrect guesses: Right leg (Game Over)
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def select_word():
    """Returns a random word from the predefined word list."""
    return random.choice(WORDS).upper()

def display_game_status(stage_index, word, guessed_letters):
    """
    Displays the current hangman figure, the hidden/revealed word,
    and the list of letters guessed so far.
    """
    print(HANGMAN_STAGES[stage_index])
    
    # Generate the masked word representation (e.g., P _ T H _ N)
    masked_word = " ".join([char if char in guessed_letters else "_" for char in word])
    print(f"  Word to guess:  {masked_word}")
    print()
    
    # Sort and display guessed letters
    if guessed_letters:
        sorted_guesses = sorted(list(guessed_letters))
        print(f"  Guessed letters: {', '.join(sorted_guesses)}")
    else:
        print("  Guessed letters: None")
    
    attempts_left = len(HANGMAN_STAGES) - 1 - stage_index
    print(f"  Incorrect guesses left: {attempts_left}")
    print("-" * 40)

def get_user_guess(guessed_letters):
    """
    Prompts the user for a single letter guess.
    Validates that input is a single alphabetic character not guessed before.
    """
    while True:
        guess = input("  Guess a letter: ").strip().upper()
        
        if len(guess) != 1:
            print("  [!] Please enter exactly one letter.")
        elif not guess.isalpha():
            print("  [!] Invalid character. Please enter an English letter (A-Z).")
        elif guess in guessed_letters:
            print(f"  [!] You have already guessed '{guess}'. Try another one.")
        else:
            return guess

def play_game():
    """Executes a single game session of Hangman."""
    word = select_word()
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect = len(HANGMAN_STAGES) - 1
    
    while incorrect_guesses < max_incorrect:
        clear_screen()
        print("=" * 40)
        print("             HANGMAN GAME             ")
        print("=" * 40)
        
        display_game_status(incorrect_guesses, word, guessed_letters)
        
        # Get next valid guess
        guess = get_user_guess(guessed_letters)
        guessed_letters.add(guess)
        
        # Check if the guess is in the word
        if guess in word:
            print(f"\n  [+] Good job! '{guess}' is in the word.")
            # Check if player won
            if all(char in guessed_letters for char in word):
                clear_screen()
                print("=" * 40)
                print("           CONGRATULATIONS!           ")
                print("=" * 40)
                display_game_status(incorrect_guesses, word, guessed_letters)
                print(f"  [🎉] WINNER! You guessed the word: {word}")
                return True
        else:
            print(f"\n  [-] Sorry, '{guess}' is not in the word.")
            incorrect_guesses += 1
            
        # Small pause so the user can read the hit/miss feedback
        input("\n  Press Enter to continue...")

    # If loop terminates without returning, player ran out of guesses
    clear_screen()
    print("=" * 40)
    print("              GAME OVER               ")
    print("=" * 40)
    display_game_status(incorrect_guesses, word, guessed_letters)
    print(f"  [💀] You lost! The correct word was: {word}")
    return False

def main():
    """Main program entry point with play-again loop."""
    clear_screen()
    print("=" * 50)
    print("        Welcome to CodeAlpha Hangman!        ")
    print("=" * 50)
    print("  Rules:")
    print("  - Guess the hidden word one letter at a time.")
    print("  - You are allowed up to 6 incorrect guesses.")
    print("  - Good luck!")
    print("=" * 50)
    input("\n  Press Enter to start playing...")
    
    while True:
        play_game()
        print("\n" + "=" * 40)
        play_again = input("  Do you want to play again? (yes/no): ").strip().lower()
        if play_again not in ('y', 'yes'):
            print("\n  Thank you for playing CodeAlpha Hangman! Goodbye.")
            break

if __name__ == "__main__":
    main()
