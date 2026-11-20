# folktale
A simple Python remake of the card game Scoundrel.

Teaches you how to play in the terminal, but just in case:

## How to play

You start with 20 HP

You will get 4 cards each round

You can then flee or play these cards

If you flee, 4 new cards will be generated. (Note: you cannot do consecutive flees)

If you choose to play, you can play the cards in any order.

-- card types -- 

Numbers - 2 to 10 and (A-14,K-13,Q-12,J-11)

clubs and spades - enemies will deal damage to you based on their number

diamonds - weapons; you will equip one, or it will replace your old one; these will block damage equal to their number from attacks

(weapons can only be used if they haven't been used yet, or the monster is less than the last killed monster.)

hearts - will heal you for the number on it (max HP is 20).

## Features:

deck generation - a simple function that builds a whole random deck

flee - the ability to flee and not consecutively.

color-coded cards - blue for enemies (clubs + spades), red for HP (hearts), and yellow for weapons (diamonds). (uses catpuccin colors in ansi)

card selection - allowing selection of cards

win / loss detection - game detects once you have won or lost


## Credits:
me - dev
game - [https://www.youtube.com/watch?v=Gt2tYzM93h4&t=8s ](https://www.youtube.com/watch?v=7fP-QLtWQZs) 

