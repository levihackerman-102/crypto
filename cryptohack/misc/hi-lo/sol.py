from functools import total_ordering
from Crypto.Random import random
# from utils import listener
from pwn import remote
import json

FLAG = 'crypto{?????????????????????????????}'
VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
SUITS = ['Clubs', 'Hearts', 'Diamonds', 'Spades']


class RNG:
    mul = random.getrandbits(60)
    inc = random.getrandbits(60)
    mod = 2**61 - 1  # 9th mersenne prime

    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * self.mul + self.inc) % self.mod
        return self.state


@total_ordering
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return VALUES.index(self.value) > VALUES.index(other.value)


class Game:
    def __init__(self):
        self.rng = RNG(random.getrandbits(60))
        self.deck = [Card(value, suit) for suit in SUITS for value in VALUES]
        self.num_deals = self.shuffle()

    def rebase(self, n, b=52):
        if n < b:
            return [n]
        else:
            return [n % b] + self.rebase(n//b, b)

    def shuffle(self):
        self.deals = self.rebase(self.rng.next())
        return len(self.deals)

    def deal_card(self):
        index = self.deals.pop()
        if self.deals == []:
            self.num_deals = self.shuffle()

        return self.deck[index]


# class Challenge():
#     def __init__(self):
#         self.game = Game()
#         self.funds = 20
#         self.dollars = self.funds
#         self.round = 0
#         self.hidden = self.game.deal_card()

#     def play_round(self, msg=None):
#         self.round += 1
#         self.hand = self.hidden # move last round's hidden card to player's hand
#         self.hidden = self.game.deal_card() # deal new hidden card
#         self.shuffle_msg = ""
#         if self.game.num_deals: # dealer shuffled deck
#             self.shuffle_msg = f"I will reshuffle the deck after {self.game.num_deals} rounds. "
#             self.game.num_deals = None

#         if self.round == 1:
#             msg = f"Welcome to my virtual casino! You are sitting down for a game of lo-hi. {self.shuffle_msg}Your hand is the {self.hand}. Lower or higher?"
#             self.shuffle_msg = ""

#         return {
#             "round": self.round,
#             "$": self.dollars,
#             "hand": str(self.hand),
#             "msg": msg
#         }

#     def win(self):
#         self.dollars += 1
#         msg = f"Correct! Hidden card was {self.hidden}. {self.shuffle_msg}Lower or higher?"
#         return self.play_round(msg)

#     def lose(self):
#         self.dollars -= 2 # house edge
#         msg = f"Incorrect! Hidden card was {self.hidden}. {self.shuffle_msg}Lower or higher?"
#         return self.play_round(msg)

#     def challenge(self, your_input):
#         if self.round == 0:
#             return self.play_round()

#         elif self.dollars <= 0:
#             self.exit = True
#             return {"error": "You're broke!"}

#         elif self.round == 200:
#             self.exit = True
#             if self.dollars >= 130:
#                 return {"msg": f"You pulled a 21! Here's a flag: {FLAG}"}
#             elif self.dollars > self.funds:
#                 return {"msg": f"Nice, you beat the house!"}
#             else:
#                 return {"msg": f"Aww, have a free drink!"}

#         elif not 'choice' in your_input:
#             self.exit = True
#             return {"error": "You must make a choice"}

#         else:
#             if self.hidden == self.hand:
#                 return self.lose() # house edge

#             choice = your_input['choice']
#             if choice.lower().startswith('l'):
#                 if self.hidden < self.hand:
#                     return self.win()
#                 else:
#                     return self.lose()
#             elif choice.lower().startswith('h'):
#                 if self.hidden > self.hand:
#                     return self.win()
#                 else:
#                     return self.lose()
#             else:
#                 self.exit = True
#                 return {"error": "Invalid input"}


# listener.start_server(port=13383)

r = remote('socket.cryptohack.org', 13383, level='debug')

deck = [Card(value, suit) for suit in SUITS for value in VALUES]
decks = []

for de in range(len(deck)):
    decks = decks + [deck[de].__str__()]

print(decks)

def json_recv():
    line = r.recvline()
    return line.decode()

def json_send(hsh):
    request = json.dumps (hsh).encode()
    r.sendline(request)

a = []
b = []
c = []

for i in range(11):
    received = json. loads (json_recv())
    card = received["hand"]
    temp = card[0:2]
    if temp == "Ac" or temp == "Tw" or temp == "Th" or temp == "Fo" or temp == "Fi" or temp == "Si" or temp == "Se":
        to_send = {"choice": "h"}
    else:
        to_send = {"choice": "l"}
    for de in range(len(decks)):
        if card == decks [de]: 
            a = a + [de]
            break
    json_send(to_send)

a.reverse()
stateA = 0
for aa in range(len(a)):
    stateA = stateA + a[aa] * pow(52, aa)

for i in range(11):
    received = json.loads(json_recv())
    card = received["hand"]
    temp = card[0:2]
    if temp == "Ac" or temp == "Tw" or temp == "Th" or temp == "Fo" or temp == "Fi" or temp == "Si" or temp == "Se":
        to_send = {"choice": "h"}
    else:
        to_send = {"choice": "l"}
    for de in range(len(decks)):
        if card == decks [de]: 
            b = b + [de]
            break
    json_send(to_send)

b.reverse()
stateB = 0
for bb in range(len(b)):
    stateB = stateB + b[bb] * pow(52, bb)

for i in range(11):
    received = json.loads(json_recv())
    card = received["hand"]
    temp = card[0:2]
    if temp == "Ac" or temp == "Tw" or temp == "Th" or temp == "Fo" or temp == "Fi" or temp == "Si" or temp == "Se":
        to_send = {"choice": "h"}
    else:
        to_send = {"choice": "l"}
    for de in range(len(decks)):
        if card == decks [de]: 
            c = c + [de]
            break
    json_send(to_send)

c.reverse()
print(c)
stateC = 0
for cc in range(len(c)):
    stateC = stateC + c[cc] * pow(52, cc)
print(stateC)

mod = pow(2, 61) - 1
mul1 = (stateB - stateC) % mod
mul2 = pow((stateA - stateB), mod - 2, mod)
mul = (mul1 * mul2) % mod
# mul = (b - c) * ((a - b) ^ (2^ 61 - 3)) mod (2^ 61 - 1)
inc = (stateB- (stateA * mul) % mod) % mod
# self.state = (self.state self.mul + self.inc) % self.mod
next_state= (stateC * mul + inc) % mod
cardhand = c[10]
gg = Game()
answer = gg.rebase (next_state)
answer.reverse()
print("answer:", answer)
for ans in range(1,len (answer)):
    received = json. loads (json_recv())
    card = received["hand"]
    if (cardhand % 13) > (answer[ans] % 13):
        to_send = {"choice": "l"}
    else:
        to_send = {"choice": "h"}
    cardhand = answer[ans]
    json_send(to_send)

next_state= (next_state* mul + inc) % mod
for i in range (20):
    gg = Game()
    answer = gg.rebase(next_state)
    answer.reverse()
    print("answer:", answer)
    for ans in range (len (answer)):
        received = json. loads (json_recv())
        card = received["hand"]
        if (cardhand % 13) > (answer [ans] % 13):
            to_send = {"choice": "l"}
        else:
            to_send = {"choice": "h"}
        cardhand = answer[ans]
        json_send(to_send)
    next_state= (next_state* mul + inc) % mod

