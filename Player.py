import random
from mainv2 import sorted_hand_order, is_better_hand

class Player:
    def __init__(self, name, stack = 100):
        self.name = name
        self.stack = stack

    """def call(self, amount):
        pass

    def raise_to(self, amount):
        pass

    def fold(self):
        pass"""

    def evaluate_current_equity(self, cards, board):
        def high_card(combo):
            combo_numbers = [card[0] for card in combo]
            #number_indexes = [numbers.index(card[0]) for card in combo]
            #highest_card = numbers[max(number_indexes)]
            return sorted_hand_order(combo_numbers)#return highest_card

        def one_pair(combo):
            combo_numbers = [card[0] for card in combo]
            if len(set(combo_numbers)) == 4:
                for card in combo_numbers:
                    if combo_numbers.count(card) == 2:
                        return [card] + sorted_hand_order([i for i in combo_numbers if i!=card])
                        #return card
                else:
                    return -1
            else:
                return -1

        def two_pair(combo):
            pair_numbs = []
            combo_numbers = [card[0] for card in combo]
            if len(set(combo_numbers)) == 3:
                for card in combo_numbers:
                    if combo_numbers.count(card) == 2 and card not in pair_numbs:
                        pair_numbs.append(card)
                if len(pair_numbs) == 0:
                    return -1
                else:
                    return sorted_hand_order(pair_numbs) + sorted_hand_order([i for i in combo_numbers if i not in pair_numbs])
                    #return pair_numbs
            else:
                return -1

        def trips(combo):
            combo_numbers = [card[0] for card in combo]
            if len(set(combo_numbers)) == 3:
                for card in combo_numbers:
                    if combo_numbers.count(card) == 3:
                        return [card] + sorted_hand_order([i for i in combo_numbers if i!=card])
                        #return card
                else:
                    return -1
            else:
                return -1

        def straight(combo):
            #number_indexes = [numbers.index(card[0]) for card in combo]
            combo_numbers = [card[0] for card in combo]
            if ''.join(sorted_hand_order(combo_numbers)) in "AKQJT98765432A":
                #highest_card = numbers[max(number_indexes)]
                #return highest_card
                return sorted_hand_order(combo_numbers)
            else:
                return -1

        def flush(combo):
            combo_suits = [card[1] for card in combo]
            if len(set(combo_suits)) == 1:
                return high_card(combo)
            else:
                return -1

        def full_house(combo):
            trips = -1
            pair = -1
            combo_numbers = [card[0] for card in combo]
            if len(set(combo_numbers)) == 2:
                for card in combo_numbers:
                    if combo_numbers.count(card) == 3 and trips == -1:
                        trips = card
                    if combo_numbers.count(card) == 2 and pair == -1:
                        pair = card
                if -1 not in [trips, pair]:
                    return [trips, pair]
                else:
                    return -1
            else:
                return -1

        def quads(combo):
            combo_numbers = [card[0] for card in combo]
            if len(set(combo_numbers)) == 2:
                for card in combo_numbers:
                    if combo_numbers.count(card) == 4:
                        return [card] + sorted_hand_order([i for i in combo_numbers if i!=card])
                else:
                    return -1
            else:
                return -1

        def straight_flush(combo):
            if straight(combo) != -1 and flush(combo) != -1:
                combo_numbers = [card[0] for card in combo]
                return sorted_hand_order(combo_numbers)
            else:
                return -1

        #CHECKING ALL COMBOS
        import itertools

        all_combos = list(itertools.combinations(cards + board, 5))
        best_combo = []
        best_hand = []
        current_rank = 0 #represents which rank (what type of hand) the player's best hand is

        for combo in all_combos:
            if straight_flush(combo) != -1 and current_rank<=9: #rank 9
                if not (current_rank == 9 and is_better_hand([best_hand, 9], [straight_flush(combo), 9]) == 1):
                    best_combo = combo
                    best_hand = straight_flush(combo)
                    current_rank = 9
            elif quads(combo) != -1 and current_rank<=8: #rank 8
                if not (current_rank==8 and is_better_hand([best_hand, 8], [quads(combo), 8])==1):
                    best_combo = combo
                    best_hand = quads(combo)
                    current_rank = 8
            elif full_house(combo) != -1 and current_rank<=7: #rank 7
                if not (current_rank == 7 and is_better_hand([best_hand, 7], [full_house(combo), 7]) == 1):
                    best_combo = combo
                    best_hand = full_house(combo)
                    current_rank = 7
            elif flush(combo) != -1 and current_rank<=6: #rank 6
                if not (current_rank == 6 and is_better_hand([best_hand, 6], [flush(combo), 6]) == 1):
                    best_combo = combo
                    best_hand = flush(combo)
                    current_rank = 6
            elif straight(combo) != -1 and current_rank<=5: #rank 5
                if not (current_rank == 5 and is_better_hand([best_hand, 5], [straight(combo), 5]) == 1):
                    best_combo = combo
                    best_hand = straight(combo)
                    current_rank = 5
            elif trips(combo) != -1 and current_rank<=4: #rank 4
                if not (current_rank == 4 and is_better_hand([best_hand, 4], [trips(combo), 4]) == 1):
                    best_combo = combo
                    best_hand = trips(combo)
                    current_rank = 4
            elif two_pair(combo) != -1 and current_rank<=3: #rank 3
                if not (current_rank == 3 and is_better_hand([best_hand, 3], [two_pair(combo), 3]) == 1):
                    best_combo = combo
                    best_hand = two_pair(combo)
                    current_rank = 3
            elif one_pair(combo) != -1 and current_rank<=2: #rank 2
                if not (current_rank == 2 and is_better_hand([best_hand, 2], [one_pair(combo), 2]) == 1):
                    best_combo = combo
                    best_hand = one_pair(combo)
                    current_rank = 2
            elif high_card(combo) != -1 and current_rank<=1: #rank 1
                if not (current_rank == 1 and is_better_hand([best_hand, 1], [high_card(combo), 1]) == 1):
                    best_combo = combo
                    best_hand = high_card(combo)
                    current_rank = 1

        return [best_hand, current_rank]#[best_hand, current_rank, best_combo]

    def action(self, pot, player_amount_bet, highest_amount_bet, cards, board):
        action, new_amount_bet = self.calc_action(pot, player_amount_bet, highest_amount_bet, cards, board)
        if action == 0:
            #self.call(amount)
            try:
                assert self.stack >= highest_amount_bet-player_amount_bet
                return ["call", -1]
            except:
                print("Player does not have sufficient money, so they will fold")
                return ["fold", -1]
        elif action == 1:
            try:
                assert self.stack >= new_amount_bet-player_amount_bet
                return ["raise_to", new_amount_bet]
            except:
                print("Player does not have sufficient money, so they will re-raise all-in")
                return ["raise_to", self.stack]
        elif action == 2:
            return ["fold", -1]

    def calc_action(self, pot, player_amount_bet, highest_amount_bet, cards, board): #returns [action, new_amount_bet]
        action = random.randint(0, 3)
        if action == 0:
            return [0, -1]
        elif action == 1:
            if highest_amount_bet == 0:
                return [1, pot/3]
            else:
                return [1, 2 * highest_amount_bet]
        elif action == 2 or action == 3:
            if highest_amount_bet != 0 and player_amount_bet!=highest_amount_bet:
                return [2, -1]
            else:
                return [0, -1]


class HumanPlayer(Player):
    def __init__(self, name, stack):
        super().__init__(name, stack)

    def calc_action(self, pot, player_amount_bet, highest_amount_bet, cards, board):
        print("THIS IS THE NAME:", self.name)#TODO: fix this
        while True:
            try:
                action = int(input("Please choose your action (type 0 for call, 1 for raise, and 2 for fold): "))
                assert action in [0, 1, 2]
                break
            except:
                print("Error. Please make sure you choose a number from 0-2")
        if action%2==0:
            return [action, -1]
        elif action==1:
            while True:
                try:
                    new_bet_amount = int(input("Please choose how much you would like to re-raise to: "))
                    break
                except:
                    print("Error. Please make sure you enter a number that is below your total stack")
            return [action, new_bet_amount]


class CPUv1(Player):
    def __init__(self, name, stack):
        super().__init__(name, stack)

    def eval_strong_outs(self, cards, board):
        print(cards, board)
        #see number of ways it can create an rank 5+ hand
        #see number of ways it can create a rank 4 hand for pocket pairs
        #add an out for a backdoor flush draw
        numbers = "23456789TJQKA"
        suits = "scdh"
        unknown_cards = []
        for i in numbers:
            for j in suits:
                unknown_cards.append(i + j)
        for i in cards+board:
            del unknown_cards[unknown_cards.index(i)]

        cards_hand, cards_rank = self.evaluate_current_equity(cards, board)
        outs = 0

        for i in unknown_cards:
            if self.evaluate_current_equity(cards, board+[i])[1] >= 5 and cards_rank < 5 and self.evaluate_current_equity(cards, board+[i])[1] != self.evaluate_current_equity([], board+[i])[1]:
                outs += 1
            elif self.evaluate_current_equity(cards, board+[i])[1] >= 4 and cards_rank < 4 and cards[0][0] == cards[1][0] and self.evaluate_current_equity(cards, board+[i])[1] != self.evaluate_current_equity([], board+[i])[1]:
                outs += 1

        return outs

    def eval_weak_outs(self, cards, board):
        numbers = "23456789TJQKA"
        suits = "scdh"
        unknown_cards = []
        for i in numbers:
            for j in suits:
                unknown_cards.append(i + j)
        for i in cards + board:
            del unknown_cards[unknown_cards.index(i)]

        cards_hand, cards_rank = self.evaluate_current_equity(cards, board)
        outs = 0

        for i in unknown_cards:
            if self.evaluate_current_equity(cards, board + [i])[1] == 2 and self.evaluate_current_equity(cards, board)[1] == 1: #if it is a one-pair with the new card
                #print(f'one pair hand comparison: {self.evaluate_current_equity(cards, board + [i])}, {self.evaluate_current_equity(["0o", str(sorted_hand_order([c[0] for c in board])[0]) + "o"], board + [i])}')
                if is_better_hand(self.evaluate_current_equity(cards, board + [i]),
                           self.evaluate_current_equity(["0o", str(sorted_hand_order([c[0] for c in board])[0]) + "o"], board + [i]))==1 and self.evaluate_current_equity(cards, board+[i])[1] != self.evaluate_current_equity(["1o", "0o"], board+[i])[1]: #self.evaluate_current_equity(cards, board + [i])[1] > cards_rank
                    #print(i, end = ', ')
                    #print(self.evaluate_current_equity([], board + [i])[1])
                    outs += 1
            else: #future hand-current hand> future board - current board
                if self.evaluate_current_equity(cards, board + [i])[1]- cards_rank > self.evaluate_current_equity(["1o", "0o"], board+[i])[1] - self.evaluate_current_equity(["1o", "0o"], board)[1]:#if self.evaluate_current_equity(cards, board + [i])[1] > cards_rank and self.evaluate_current_equity(cards, board+[i])[1] != self.evaluate_current_equity(["1o", "0o"], board+[i])[1]:
                    #print(i, end=', ')
                    #print(self.evaluate_current_equity([], board + [i])[1])
                    #print(f'{self.evaluate_current_equity(cards, board + [i])[1]} - {cards_rank} > {self.evaluate_current_equity(["1o", "0o"], board+[i])[1]} - {self.evaluate_current_equity(["1o", "0o"], board)[1]}')

                    outs += 1




        return outs

    def calc_action(self, pot, player_amount_bet, highest_amount_bet, cards, board):
        print(cards, board)
        if len(board) != 0 and len(board) != 5:
            print("Strong outs:", self.eval_strong_outs(cards, board))
            print("Weak outs:", self.eval_weak_outs(cards, board))
        return super().calc_action(pot, player_amount_bet, highest_amount_bet, cards, board)