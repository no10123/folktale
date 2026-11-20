import os, random
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
os.system("clear")

# functions
def build_deck():
    deck = [
        {"suit": suit, "number": rank}
        for suit in ["clubs", "spades", "diamonds", "hearts"]
        for rank in range(2, 15 if suit in ["clubs", "spades"] else 11)
    ]
    random.shuffle(deck)
    return deck

while True:
    hp = 20
    has_flee = True
    weapon = -1
    wfresh = False
    deck = build_deck()
    hand = [deck.pop(0)]

    while True:
        hand = deck[:3] + hand
        os.system("clear")
        print(f"Total cards: {len(deck)}")
        print(f"hp: {hp}")
        print("-- cards --")
        print("\n".join(list(f"{x}. {c['number']} of {c['suit']}" for x, c in enumerate(hand))))
        print(f"-- weapon: {'none' if weapon == -1 else weapon} --")
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
            I = ""
            print("you flee'd last floor, so you must play these cards.")
            i = 'play'
        if i == 'flee':
            has_flee = False
            del deck[:3]
            deck.extend(hand)
            hand = [deck.pop(0)]
            continue
        elif i == 'play':
            has_flee = True
            del deck[:3]
            X = []
            for i in range(min(3,len(hand))):
                os.system('clear')
                os.system("clear")
                print(f"Total cards: {len(deck)}")
                print(f"hp: {hp}")
                print("-- cards --")
                print("\n".join(list(f"{x}. {c['number']} of {c['suit']}" for x, c in enumerate(hand))))
                print(f"-- weapon: {'none' if weapon == -1 else weapon} --")
                print(f"\033[s" + "would you like to play or flee [p/f]: {I}" if I != "" else "you flee'd last floor, so you must play these cards.")
                if X != []:
                    for v, i in enumerate(X):
                        left = [str(n) for n in range(len(hand)) if n not in X[:(v+1)]]
                        print(f"number for the card ({', '.join(left)}): {i}")
                while True:
                    left = [str(n) for n in range(len(hand)) if n not in X]
                    i = input(f"number for the card ({', '.join(left)}): ")
                    valid_input = False
                    for x, c in enumerate(hand):
                        if (i == str(x) or i == f"{c['number']} of {c['suit']}") and x not in X:
                            valid_input = True
                            break
                    if valid_input:
                        break
                X.append(x)
                if c["suit"] in ['clubs','spades']:
                    if wfresh or c["number"] < weapon:
                        damage = c["number"] - weapon
                        weapon = c["number"]
                        wfresh = False
                    else:
                        damage = c["number"]
                    hp -= max(0,damage)
                    print(f"You took {damage} damage")
                elif c["suit"] == 'hearts':
                    old_hp = hp
                    hp = min(20, hp + c["number"])
                    healed = hp - old_hp

                    print(f"You healed {healed} hp")
                elif c["suit"] == 'diamonds':
                    weapon = c["number"]
                    wfresh = True
                    print(f"You gained a weapon with {c['number']} strength.")
            for i in range(len(hand)):
                if i not in X:
                    hand = [hand[i]]
                    break
            else:
                hand = []
        
        if hp <= 0 or (len(deck) == 0 and len(hand) == 0):
            break
    if hp <= 0:
        print("you lost")
    else:
        print("you won")
    if "no".startswith(input("do you want to play again?\n[y/n] > ").lower()):
        break

