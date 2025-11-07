"""Game logic for the Snowman Meltdown game.

This module exposes functions to run the game loop and helpers used by the
command-line entrypoint in ``snowman.py``.
"""

from ascii_art import STAGES
import random
from typing import Set, Tuple

# Words to guess
WORDS = ["python", "git", "github", "snowman", "meltdown"]

MAX_MISTAKES = len(STAGES) - 1


def get_random_word() -> str:
    """Select and return a random secret word."""
    return random.choice(WORDS)


def display_game_state(mistakes: int, secret_word: str, guessed_letters: Set[str]) -> None:
    """Print the current snowman ASCII art and the masked secret word.

    Args:
        mistakes: Current number of mistakes (index into STAGES).
        secret_word: Word the player is trying to guess.
        guessed_letters: Set of letters the player has guessed.
    """
    idx = min(mistakes, MAX_MISTAKES)
    print(STAGES[idx])
    display_word = " ".join(
        [c if c in guessed_letters else "_" for c in secret_word]
    )
    print("Word:", display_word)
    print(f"Mistakes: {mistakes}/{MAX_MISTAKES}")
    if guessed_letters:
        print("Guessed:", " ".join(sorted(guessed_letters)))
    print()


def is_word_guessed(secret_word: str, guessed_letters: Set[str]) -> bool:
    """Return True when every character of ``secret_word`` is in
    ``guessed_letters``.
    """
    return all(ch in guessed_letters for ch in secret_word)


def is_valid_letter(guess: str) -> bool:
    """Return True if ``guess`` is a single alphabetic character.

    This small helper keeps validation logic separate from I/O.
    """
    return len(guess) == 1 and guess.isalpha()


def process_single_letter_guess(
    guess: str, secret_word: str, guessed_letters: Set[str]
) -> Tuple[int, str]:
    """Process a single-letter guess.

    Returns a tuple (mistake_increment, message). The function updates
    ``guessed_letters`` in-place.
    """
    if guess in guessed_letters:
        return 0, "You've already guessed that letter."

    guessed_letters.add(guess)
    if guess in secret_word:
        return 0, f"Good guess: '{guess}' is in the word!"

    return 1, f"Sorry, '{guess}' is not in the word."


def process_full_word_guess(guess: str, secret_word: str, guessed_letters: Set[str]) -> Tuple[int, str]:
    """Process a full-word guess and return (mistake_increment, message).

    If the guess is correct the function adds all letters from the secret
    word to ``guessed_letters``.
    """
    if guess == secret_word:
        guessed_letters.update(secret_word)
        return 0, "Fantastic — you guessed the full word!"

    return 1, "That's not the correct word."


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

            if is_valid_letter(guess):
                inc, msg = process_single_letter_guess(
                    guess, secret_word, guessed_letters
                )
                mistakes += inc
                print(msg)
                # continue to end-of-round checks
            else:
                # Treat anything longer than one character as a full-word guess
                inc, msg = process_full_word_guess(
                    guess, secret_word, guessed_letters
                )
                mistakes += inc
                print(msg)

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
