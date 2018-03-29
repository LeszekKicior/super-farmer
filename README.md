#Terminal Superfarmer

A command line implementation of the simple Polish kids boardgame.
Playable, but mostly serves as a proof of concept.
Turns out that there's not actually much to do once all the dice rolls are done by a machine.
*2017 Leszek Kicior*

## Requirements
None. Currently only works on **Python 2**.

## Playing the game
To try playing, simply run `python superfarmer-render.py` in terminal.

After selecting the number of players and inputting their names (if left blank, they default to "Player 1" and so on) the players will take turns rolling the two dice.
The dice feature following animals:

* Red die: 6 rabbits, 3 sheep, pig, cow, wolf
* Yellow die: 6 rabbits, 3 sheep, pig, horse, fox

After rolling the dice, the players will receive a number of animals equal to half of the number they already own + the number featured on the dice, rounded down.
Once a player has 6 or more rabbits (or 1 of any other animal), they can exchange animals before rolling, based on the following values:

* Sheep: 6 rabbits
* Pig: 12 rabbits
* Cow: 36 rabbits
* Horse: 72 rabbits
* Small dog: 6 rabbits
* Large dog: 36 rabbits

Rolling a fox will cause the player to lose all of his rabbits, while rolling a wolf will cause him to lose all animals except horses. This can be protected against by purchasing small or large dogs, which protect against a single fox or wolf, respectively.

The winner is the first player to own at least 1 of every animal (except dogs) after rolling the dice. The game ends when a player manages to do this.

##License

The boardgame version of Superfarmer belongs to *GRANNA sp. z o.o.*, and I claim no ownership.
The code itself is a tiny student project, and I can't fathom how it could be of any use to anyone, but is nonetheless freely available under an MIT license.

##Links
* [Superfarmer at BoardGameGeek](https://boardgamegeek.com/boardgame/17557/super-farmer)
* [English rules PDF](https://boardgamegeek.com/filepage/16176/super-farmer-enpdf)