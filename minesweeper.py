from team_a.mine_bot import get_response as get_response_a
from team_b.mine_bot import get_response as get_response_b
from banned_words import check_banned_words_in_text

def play_game():
    response_a = get_response_a("Start a conversation about your favorite memory of christmas.")
    print(response_a)
    if check_banned_words_in_text(response_a):
        print("\n\n\n")
        print("B Won!")
        return

    for i in range(30):
        response_b = get_response_b(response_a)
        print(response_b)
        if check_banned_words_in_text(response_b):
            print("\n\n\n")
            print("A Won!")
            return
        response_a = get_response_a(response_b)
        print(response_a)
        if check_banned_words_in_text(response_a):
            print("\n\n\n")
            print("B Won!")
            return

    print("\n\n\n")
    print("Tie!")

play_game()
