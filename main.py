from Board import Board

BOARD = Board()


def main():
    board_for_astar = BOARD.shuffle()
    if BOARD.start():
        choice = input("\nAuto solve using IDS? (yes or no):")
        if choice == "yes":
            print("\nThinking...")
            BOARD.ids(25)  # an theloume allo bathos, allazoume thn parametro

        choice = input("\nAuto solve using A*? (yes or no):")
        if choice == "yes":
            print("\nThinking...")
            BOARD.astar(board_for_astar)


main()
