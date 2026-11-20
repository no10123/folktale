import os, random
# color codes
BLUE   = "\033[38;2;137;180;250m"   # clubs + spades
YELLOW = "\x1b[38;2;249;226;175m"   # diamonds
RED    = "\x1b[38;2;243;139;168m"   # hearts
CLEAR  = "\033[0m"
BG     = "\033[48;2;30;30;46m"
TEXT   = "\033[38;2;205;214;244m"
def clear():
    print("\033[H\033[2J", end="", flush=True)
    print(TEXT)

clear()
print("""
welcome to a python version of Scoundrel.

how to play:
0. you start with 20 hp
1. you will get 4 cards each round
2. you can then flee or play these cards
3. if you flee 4 new cards will be generated. (Note: you cannot do consecutive flee's)
4. if you choose play you can play the cards in any order.
-- card types -- 
Numbers - 2 to 10 and (A-14,K-13,Q-12,J-11)
clubs and spades - enemies will deal damage to use based on their number
diamonds - weapons, you will equip one or it will replace your old one, these will block damage equal to it's number from attacks
(weapons can only be used if it hasn't been used yet, or the monster is less than the last killed monster.)
hearts - will heal you for the number on it (max hp is 20).
""")

# game loop, hand -> play cards or flee. 

i = input("Press enter to Play: ")
clear()

# functions
def build_deck():
    deck = [
        {"suit": suit, "number": rank, "color": {'hearts':RED,'clubs':BLUE,'spades':BLUE,'diamonds':YELLOW}[suit]}
        for suit in ["clubs", "spades", "diamonds", "hearts"]
        for rank in range(2, 15 if suit in ["clubs", "spades"] else 11)
    ]
    random.shuffle(deck)
    return deck

while True:
    hp = 20
    has_flee = True
    weapon = None
    last_killed = None
    deck = build_deck()
    hand = [deck.pop(0)]

    while True:
        hand = [deck.pop(0) for _ in range(min(3, len(deck)))] + hand
        clear()
        print(f"Total cards: {len(deck)}")
        print(f"hp: {hp}")
        print("-- cards --")
        print("\n".join(list(f"{x}.{c['color']} {c['number']} of {c['suit']}{TEXT}" for x, c in enumerate(hand))))
        print(f"-- weapon: {weapon}, last killed: {last_killed} --")
        i = " "
        if has_flee:
            while True:
                i = input("\033[s" + "would you like to play or flee [p/f]: ").lower()
                if  'play'.startswith(i):
                    I = i
                    i = 'play'
                    break
                elif 'flee'.startswith(i):
                    i = 'flee'
                    break
                else:
                    # 38 is prompt length - 1
                    print(end=f"\033[u\r\033[J")
        else:
            I = None
            print("you flee'd last floor, so you must play these cards.")
            i = 'play'
        if i == 'flee':
            has_flee = False
            deck.extend(hand)
            hand = [deck.pop(0)]
            continue
        elif i == 'play':
            has_flee = True
            X = []
            IL = []
            actions = []
            for i in range(min(3,len(hand))):
                clear()
                print(f"Total cards: {len(deck)}")
                print(f"hp: {hp}")
                print("-- cards --")
                print("\n".join(list(f"{'*' if x in X else x}.{c['color']} {c['number']} of {c['suit']}{TEXT}" for x, c in enumerate(hand))))
                print(f"-- weapon: {weapon}, last killed: {last_killed} --")
                print(f"\033[s" + f"would you like to play or flee [p/f]: {I}" if I is not None else "you flee'd last floor, so you must play these cards.")
                if X != []:
                    for v, i in enumerate(X):
                        left = [str(n) for n in range(len(hand)) if n not in X[:(v)]]
                        print(f"number for the card ({', '.join(left)}): {IL[v]}")
                        print(actions[v])
                while True:
                    left = [str(n) for n in range(len(hand)) if n not in X]
                    i = input(TEXT + f"number for the card ({', '.join(left)}): ")
                    valid_input = False
                    for x, c in enumerate(hand):
                        if (i == str(x) or i == f"{c['number']} of {c['suit']}") and x not in X:
                            valid_input = True
                            break
                    if valid_input:
                        break
                X.append(x)
                IL.append(i)
                if c["suit"] in ['clubs','spades']:
                    if (last_killed is None or c["number"] < last_killed) and not (weapon is None):
                        damage = c["number"] - weapon
                    else:
                        damage = c["number"]
                    last_killed = c["number"]
                    hp -= max(0,damage)
                    actions.append(TEXT + f"You took {damage} damage")
                    if hp <= 0:
                        break
                elif c["suit"] == 'hearts':
                    old_hp = hp
                    hp = min(20, hp + c["number"])
                    healed = hp - old_hp
                    actions.append(TEXT + f"You healed {healed} hp")
                elif c["suit"] == 'diamonds':
                    weapon = c["number"]
                    last_killed = None
                    actions.append(TEXT + f"You gained a weapon with {c['number']} strength.")
            for i in range(len(hand)):
                if i not in X:
                    hand = [hand[i]]
                    break
            else:
                hand = []
        if hp <= 0 or (len(deck) == 0 and len(hand) == 0):
            break
        print(TEXT + actions[-1])
        input(TEXT + "Press enter to go to next round: ")
    if hp <= 0:
        print(TEXT + "you lost")
    else:
        print(TEXT + "you won")
    if "no".startswith(input(TEXT + "do you want to play again?\n[y/n] > ").lower()):
        break

