# -*- coding: utf-8 -*-

from sfhelpers import Player, roll, animal_names, exchange_table
import curses
import time

t_width = 80
t_height = 25


def center_text(window, top, text, *args):
    """Helper function for centering text in window"""
    width = window.getmaxyx()[1]
    for line in text.split("\n"):
        window.addstr(top, width//2-len(line)//2, line, *args)
        top += 1


def display_animals(window, top, player):
    window.clear()
    for line in player.farm_state():
        window.addstr(top, 0, line)
        top += 1
    window.refresh()


def display_exchange_table(window, top, player):
    window.clear()
    window.addstr(top, 0, player.name)
    window.addstr(top+2, 0, exchange_table)
    window.refresh()


def display_winning_message(window, top, player):
    """ Congrats! """
    text = "GAME OVER\n{} WINS".format(player.name)
    window.clear()
    center_text(window, 1, text, curses.A_STANDOUT)
    window.refresh()


def exchange(f_window, r_window, top, player):
    """ Allows exchange of rabbits to other animals and vice versa. """
    while True:
        f_window.clear()
        display_animals(f_window, top, player)
        display_exchange_table(r_window, top, player)

        c = f_window.getch()

        if c == ord("A"):
            player.buy_animal("S")
        if c == ord("a"):
            player.sell_animal("S")

        if c == ord("S"):
            player.buy_animal("P")
        if c == ord("s"):
            player.sell_animal("P")

        if c == ord("D"):
            player.buy_animal("C")
        if c == ord("d"):
            player.sell_animal("C")

        if c == ord("F"):
            player.buy_animal("H")
        if c == ord("f"):
            player.sell_animal("H")

        if c == ord("G"):
            player.buy_animal("SD")
        if c == ord("g"):
            player.sell_animal("SD")

        if c == ord("H"):
            player.buy_animal("LD")
        if c == ord("h"):
            player.sell_animal("LD")

        if c == 10 or c == curses.KEY_ENTER:  # Press Enter to skip
            r_window.clear()
            break


def display_roll(window, top, roll):
    window.clear()
    text = "Rolled: " + ", ".join(animal_names[a] for a in roll)
    center_text(gameplay_window, 4, text, curses.A_BOLD)
    gameplay_window.refresh()


print("\x1b[8;{};{}t".format(t_height, t_width))  # Resize terminal window
time.sleep(0.1)  # Not sure why this is necessary, but bugs happen without it.

stdscr = curses.initscr()
curses.noecho()  # Comment out these two lines \
curses.cbreak()  # To make the debugger work consistently.
stdscr.keypad(1)
curses.curs_set(0)

anykey = stdscr.getch  # For clarity, use this when no input is necessary


try:
    # Title screen

    center_text(stdscr, 1, "SUPER FARMER", curses.A_STANDOUT)
    center_text(stdscr, 2, "LESZEK KICIOR 2018")
    center_text(stdscr, 5, "PRESS ANY KEY TO START")
    stdscr.refresh()
    anykey()


# Setup
    players = []
    curr_h = 0
    stdscr.clear()
    curses.curs_set(1)
    curses.echo()
    stdscr.addstr(0, 0, "Select number of players: ")

    while True:
        stdscr.refresh()
        c = stdscr.getch(0, 26)

        if c in range(49, 58):
            n = int(chr(c))
            time.sleep(0.2)

            break
    for x in range(1, int(n)+1):  # Deliberately not xrange()
        curr_h += 1
        pl_num = "Player {}".format(x)
        stdscr.addstr(curr_h, 0, pl_num+": ")
        name = stdscr.getstr(10)
        if name == "":
            name = pl_num
        players.append(Player(name))

    #  Window setup
    curses.noecho()
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    farm_window = curses.newwin(25, 24, 0, 0)           # INITIATE
    separator = curses.newwin(25, 1, 0, 25)             # THREE
    gameplay_window = curses.newwin(25, 53, 0, 27)      # WINDOWS

    separator.vline(0, 0, "|", 25)
    separator.refresh()
    fin = False

# Game loop
    """
    Gameplay loop:
        For each player:
            - Display state
            - Exchange animals
            - Roll dice
            - Update animals
            - Display state & check victory condition
    """

    while True:

        for player in players:

            #  Clear and prepare
            farm_window.clear()
            gameplay_window.clear()
            farm_window.refresh()
            gameplay_window.refresh()

            display_animals(farm_window, 0, player)
            farm_window.refresh()

            #  Display the exchange tables if exchange is possible
            if player.total_value >= 6:
                exchange(farm_window, gameplay_window, 0, player)

            center_text(gameplay_window, 0, player.name)
            center_text(gameplay_window, 2, "--Press any key to roll dice--")
            gameplay_window.refresh()
            anykey()

            #  Roll and display changes
            r = roll()
            player.update_animals(r)
            display_roll(gameplay_window, 0, r)
            display_animals(farm_window, 0, player)

            #  Check if winner
            if player.check_victory_condition():
                display_winning_message(gameplay_window, 0, player)
                anykey()
                fin = True
                break
            anykey()
        if fin:
            break


finally:  # Return terminal window to normal
    stdscr.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
