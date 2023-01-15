def run_example_solver():
    """Demonstrates how to play and win a simple game in which there are 2 possible numbers,
    1 lie is permitted, and we have 3 questions."""
    # First tell the server to start the game for us
    while True:
        game_id = start_game()
        i = 0
        valid_numbers = generate_list(1,1024)
        i += 2
        answer1 = ask_question(game_id, valid_numbers)
        answer2 = ask_question(game_id, valid_numbers)
        if answer1 != answer2:
            break

    while i < GUESSES:
        print("-------------------------------")
        print(f"Guesses: {i}")
        lower_range = int(input("lower_range: "))
        upper_range = int(input("upper_range: "))
        mid = math.floor((lower_range + upper_range)/2)
        print(f"Mid: {mid}")
        valid_numbers = generate_list(lower_range, upper_range)
        answer = ask_question(game_id, valid_numbers)
        print(f"Answer = {answer}")
        i += 1

    guess = int(input("Guess: "))

    # Finally, make our guess
    correct, secret_number = verify_guess(game_id, guess)
    print(
        f"Guessed {guess} and was {'' if correct else 'in'}correct - answer is {secret_number}"
    )
