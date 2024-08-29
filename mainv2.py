import random
from Player import *

def sorted_hand_order(l):
    numbers = "0123456789TJQKA"
    l_indexes = [numbers.index(i) for i in l]
    return [numbers[i] for i in sorted(l_indexes)][::-1]

def is_better_hand(l1, l2):
    hand1, rank1 = l1
    hand2, rank2 = l2

    if rank1>rank2:
        return 1
    elif rank1<rank2:
        return-1
    else:
        numbers = "0123456789TJQKA" #added 0, 1 as dummy cards so algos in Player don't error
        for i, j in zip(hand1, hand2):
            if numbers.index(i)>numbers.index(j):
                return 1
            elif numbers.index(i)<numbers.index(j):
                return -1
        else:
            return 0

class Poker:
    def __init__(self, num_players = 5, players = []):
        self.num_players = num_players
        self.players = players

        numbers = "23456789TJQKA" #added 0, 1 as dummy cards so algos in Player don't error
        suits = "scdh"
        self.cards = []
        for i in numbers:
            for j in suits:
                self.cards.append(i + j)

        self.player_cards = [None for i in range(num_players)]
        self.board = []
        self.pot = 6

        self.num_players_left = self.num_players + 0
        self.players_left = self.players + []


    def reset_game(self):
        numbers = "23456789TJQKA"
        suits = "scdh"
        self.cards = []
        for i in numbers:
            for j in suits:
                self.cards.append(i + j)

        self.player_cards = [None for i in range(self.num_players)]
        self.board = []
        self.pot = 1.5

        self.num_players_left = self.num_players + 0
        self.players_left = self.players + []
        print("Finished resetting game...\n")

    def deal(self):
        for i in range(self.num_players):
            c1 = self.cards.pop(random.randint(0, len(self.cards) - 1))
            c2 = self.cards.pop(random.randint(0, len(self.cards) - 1))
            self.player_cards[i] = [c1, c2]
        print("Player cards:", self.player_cards)
        print("Finished dealing...\n")

    def betting_round(self, starting_pos, money_bet=None, skip_start=False):
        if money_bet == None: money_bet = [0 for i in range(self.num_players_left)]
        current_pos = starting_pos #TODO: New
        for i in range(self.num_players_left-(1 if skip_start else 0)):
            #current_pos = (i + starting_pos) % self.num_players_left #TODO: OLD
            action, amount = self.players_left[current_pos].action(self.pot, money_bet[current_pos], max(money_bet), self.player_cards[current_pos], self.board)
            if action == "call":
                if money_bet[current_pos]==max(money_bet):
                    print(f"player {self.players_left[current_pos].name} checks")
                else:
                    print(f"player {self.players_left[current_pos].name} calls")
                self.players_left[current_pos].stack -= max(money_bet)-money_bet[current_pos]
                self.pot += max(money_bet)-money_bet[current_pos]

                money_bet[current_pos] = max(money_bet)
                print(f"Pot: {round(self.pot, 2)}, money bet: {', '.join([player.name+'-'+str(round(money, 2)) for player, money in zip(self.players_left, money_bet)])}; player stacks: {', '.join([player.name+'-'+str(round(player.stack, 2)) for player in self.players])}\n---")
            if action == "raise_to":
                print(f"player {self.players_left[current_pos].name} raises to {round(amount, 2)}")
                self.players_left[current_pos].stack -= amount-money_bet[current_pos]
                self.pot += amount-money_bet[current_pos]

                money_bet[current_pos] = amount
                print(f"Pot: {round(self.pot, 2)}, money bet: {', '.join([player.name+'-'+str(round(money, 2)) for player, money in zip(self.players_left, money_bet)])}; player stacks: {', '.join([player.name+'-'+str(round(player.stack, 2)) for player in self.players])}\n---")

                self.betting_round((current_pos+1)%self.num_players_left, money_bet, True)#TODO: OLD version: self.betting_round(current_pos+1, money_bet, True)
                break
            if action == "fold":
                print(f"player {self.players_left[current_pos].name} folds")
                del self.players_left[current_pos]
                del money_bet[current_pos]
                del self.player_cards[current_pos]
                print(f"Pot: {round(self.pot, 2)}, money bet: {', '.join([player.name+'-'+str(round(money, 2)) for player, money in zip(self.players_left, money_bet)])}; player stacks: {', '.join([player.name+'-'+str(round(player.stack, 2)) for player in self.players])}\n---")

                self.num_players_left -= 1
                #starting_pos -= 1 #TODO: OLD
                current_pos -= 1 #TODO: New


            current_pos = (current_pos+1) % self.num_players_left #NEW

        if skip_start==False:
            #print([type(player).__name__ for player in self.players_left])#TODO: fix this
            print("Finished betting round...\n")


    def return_hand_strength(self, hand, rank):
        if rank == 1:
            return(f"{hand[0]} high (rank 1)")#: {combo}")
        elif rank == 2:
            return(f"{hand[0]} high pair (rank 2)")#: {combo}")
        elif rank == 3:
            return(f"{hand[0]}, {hand[1]} two pair (rank 3)")#: {combo}")
        elif rank == 4:
            return(f"{hand[0]} high three of a kind (rank 4)")#: {combo}")
        elif rank == 5:
            return(f"{hand[0]} high straight (rank 5)")#: {combo}")
        elif rank == 6:
            return(f"{hand[0]} high flush (rank 6)")#: {combo}")
        elif rank == 7:
            return(f"{hand[0]}, {hand[1]} full house (rank 7)")#: {combo}")
        elif rank == 8:
            return(f"{hand[0]} high four of a kind (rank 8)")#: {combo}")
        elif rank == 9:
            return(f"{hand[0]} high straight-flush (rank 9)")#: {combo}")

    def game(self, sb_pos = 0):

        #INIT
        print("-"*10+"NEW ROUND"+"-"*10)
        self.reset_game()
        self.deal()

        #PRE FLOP
        self.players[sb_pos].stack -= 0.5
        self.players[(sb_pos+1)%self.num_players].stack -= 1
        print(f"{self.players[sb_pos].name} bets small blind (0.5). {self.players[(sb_pos+1)%self.num_players].name} bets big blind (1).\n---")
        self.betting_round((sb_pos+2)%self.num_players, [0.5, 1] + [0 for i in range(self.num_players - 2)], False)

        #FLOP
        if self.num_players_left > 1:
            for i in range(3):
                self.board.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
            print("FLOP:", self.board)

            self.betting_round(0)


        #TURN
        if self.num_players_left > 1:
            self.board.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
            print("TURN:", self.board)

            self.betting_round(0)

        #RIVER
        if self.num_players_left > 1:
            self.board.append(self.cards.pop(random.randint(0, len(self.cards) - 1)))
            print("RIVER:", self.board)

            self.betting_round(0)

        #EVALUATE
        best_hand = []
        winner = None

        if self.num_players_left > 1:
            print("SHOWDOWN:", self.board)
            for player, cards in zip(self.players_left, self.player_cards):
                hand = player.evaluate_current_equity(cards, self.board)
                #print("HAND", hand)
                print(f"Player {player.name}'s cards: {cards} -> {self.return_hand_strength(*hand)}")


                if best_hand == [] or is_better_hand(hand, best_hand)==1:
                    best_hand = hand
                    winner = player
            print("")
            print(f"Winner: {winner.name}, best hand: {self.return_hand_strength(*best_hand)}")
        else:
            winner = self.players_left[0]


        winner.stack += self.pot
        print(f"{winner.name} recieves a pot of {self.pot}")
        print(f"Player stacks: {', '.join([player.name+'-'+str(round(player.stack, 2)) for player in self.players])}\n\n\n")


if __name__ == "__main__":
    poker = Poker(5, [CPUv1("Andrew", 100), CPUv1("Bob", 100), Player("Chris", 100), Player("Drake", 100), Player("Ethan", 100)])

    for i in range(50):
        poker.game(i%5)
