from ascii_art import STAGES
import random
from typing import Set

# Words to guess
WORDS = ["python", "git", "github", "snowman", "meltdown"]

MAX_MISTAKES = len(STAGES) - 1


def get_random_word() -> str:
    """Select and return a random secret word."""
    return random.choice(WORDS)


def display_game_state(mistakes: int, secret_word: str, guessed_letters: Set[str]) -> None:
    idx = min(mistakes, MAX_MISTAKES)
    print(STAGES[idx])
    display_word = " ".join([c if c in guessed_letters else "_" for c in secret_word])
    print("Word:", display_word)
    print(f"Mistakes: {mistakes}/{MAX_MISTAKES}")
    if guessed_letters:
        print("Guessed:", " ".join(sorted(guessed_letters)))
    print()


def is_word_guessed(secret_word: str, guessed_letters: Set[str]) -> bool:
    return all(ch in guessed_letters for ch in secret_word)


def play_game() -> None:
    print("Welcome to Snowman Meltdown!")

    # Outer loop to allow replaying multiple rounds
    while True:
        secret_word = get_random_word()
        guessed_letters: Set[str] = set()
        mistakes = 0

        # Inner loop: one round
        while True:
            display_game_state(mistakes, secret_word, guessed_letters)

            guess = input("Guess a letter (or the whole word): ").lower().strip()
            if not guess:
                print("Please type a letter or word and press Enter.")
                continue

            # Single-letter guess
            if len(guess) == 1:
                if not guess.isalpha():
                    print("Please enter a valid letter (a-z).")
                    continue
                if guess in guessed_letters:
                    print("You've already guessed that letter.")
                    continue
                guessed_letters.add(guess)
                if guess in secret_word:
                    print(f"Good guess: '{guess}' is in the word!")
                else:
                    mistakes += 1
                    print(f"Sorry, '{guess}' is not in the word.")
            else:
                # Full-word guess
                if guess == secret_word:
                    guessed_letters.update(secret_word)
                    print("Fantastic — you guessed the full word!")
                else:
                    mistakes += 1
                    print("That's not the correct word.")

            # Check win/lose conditions after processing the guess so the final
            # state is displayed once (below) instead of being shown both before
            # and after the message.
            if is_word_guessed(secret_word, guessed_letters):
                print("Congratulations! You guessed the word:", secret_word)
                break
            if mistakes >= MAX_MISTAKES:
                print("Oh no! The snowman melted. The word was:", secret_word)
                break

        # Final state display (single display after round)
        display_game_state(min(mistakes, MAX_MISTAKES), secret_word, guessed_letters)

        # Replay prompt
        while True:
            replay = input("Play again? (y/n): ").lower().strip()
            if replay in ("y", "yes"):
                break  # start a new round
            if replay in ("n", "no"):
                print("Thanks for playing Snowman Meltdown!")
                return
            print("Please answer 'y' or 'n'.")


if __name__ == "__main__":
    play_game()
