# poker.py
# Copyright (c) 2024-2025 dhpoware. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""A simple five-card draw poker implementation."""

import sys

from random import randint, shuffle
from enum import Enum
from functools import total_ordering
from collections import Counter


@total_ordering
class CardSuit(Enum):
    """A class that represents the 4 suits of a playing card."""
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4
    
    def __str__(self):
        if self.name == "CLUBS":
            return u"\u2663"
        elif self.name == "DIAMONDS":
            return u"\u2666"
        elif self.name == "HEARTS":
            return u"\u2665"
        elif self.name == "SPADES":
            return u"\u2660"
            
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            raise NotImplementedError


@total_ordering
class CardRank(Enum):
    """A class that represents the 13 ranks of a playing card."""
    DEUCE = 2
    TREY = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    def __str__(self):
        if self.name == "JACK":
            return "J"
        elif self.name == "QUEEN":
            return "Q"
        elif self.name == "KING":
            return "K"
        elif self.name == "ACE":
            return "A"
        else:
            return str(self.value)
            
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            raise NotImplementedError


class Card(tuple):
    """A class that models a playing card."""
    
    def __new__(cls, rank, suit):
        """rank is a CardRank object. suit is a CardSuit object."""
        assert isinstance(rank, CardRank)
        assert isinstance(suit, CardSuit)
        return tuple.__new__(cls, (rank, suit))
        
    def __str__(self):
        """Returns a two character string representation of the card."""
        return "{}{}".format(self[0], self[1])
        
    @property
    def rank(self):
        """Get this card's rank."""
        return self[0]
        
    @property
    def suit(self):
        """Get this card's suit."""
        return self[1]
        

class OutOfCards(Exception):
    """Exception raised when the CardDeck doesn't have enough cards."""
    pass
        

class CardDeck:
    """A class that models a standard deck of playing cards."""
    
    def __init__(self):
        """Create all the cards in the deck and shuffles them."""
        self.reset()
        
    def print(self):
        """Diagnotic method to print out all the cards in the deck."""
        for i in range(len(self.cards)):
            print(f"Card #{i+1}: {self.cards[i]}")
    
    def reset(self):
        """Returns all dealt cards back into the card deck and reshuffles them."""
        self.cards = []
        for suit in CardSuit:
            for rank in CardRank:
                self.cards.append(Card(rank, suit))
        shuffle(self.cards)
        
    def deal_card(self):
        """
        Removes a single card from the card deck and returns it.
        An OutOfCards exception is raised if the card deck doesn't have enough cards.
        """
        if len(self.cards) - 1 > 0:
            return self.cards.pop()
        else:
            raise OutOfCards
        
    def deal_cards(self, number_of_cards):
        """
        Removes the specified number of cards from the card deck and returns them.
        An OutOfCards exception is raised if the card deck doesn't have enough cards.
        """
        dealt_cards = []
        if len(self.cards) - number_of_cards > 0:
            for i in range(number_of_cards):
                dealt_cards.append(self.cards.pop())
        else:
            raise OutOfCards
        return dealt_cards
    
    
class PokerHandEvaluator:
    """A class to evaluate a five-card draw poker hand."""
    
    def __init__(self, cards):
        """Initializes the evaluator with a list of 5 card objects."""
        assert isinstance(cards, list) and all(isinstance(element, Card) for element in cards)
        self.cards = cards
        
    def is_straight_flush(self):
        """
        Determines whether this poker hand contains a straight flush.
        Returns the rank of the highest ranking card if it is a straight flush.
        Otherwise, None is returned.
        """
        return self.high_card().rank if self.is_straight() and self.is_flush() else None
    
    def is_four_of_a_kind(self):
        """
        Determines whether this poker hand contains a four of a kind.
        Returns the rank of the high card if it is a four of a kind.
        Otherwise, None is returned.
        """
        for rank, occurrences in Counter(card.rank for card in self.cards).items():
            if occurrences == 4:
                return rank
        return None
    
    def is_full_house(self):
        """
        Determines whether this poker hand contains a full house.
        A full house is three cards of one rank and two cards of another rank.
        Returns a tuple with the rank of the three matching cards and the two matching cards.
        Otherwise, None is returned.
        """
        three_matching_cards = []
        two_matching_cards = []
        for rank, occurrences in Counter(card.rank for card in self.cards).items():
            if occurrences == 3:
                three_matching_cards.append(rank)
            elif occurrences == 2:
                two_matching_cards.append(rank)
        return (three_matching_cards[0], two_matching_cards[0]) if len(three_matching_cards) == 1 and len(two_matching_cards) == 1 else None
        
    def is_flush(self):
        """
        Determines whether this poker hand contains a flush.
        Returns the rank of the high card if it is a flush.
        Otherwise, None is returned.
        """
        suits_set = {*[card.suit for card in self.cards]}
        return sorted(self.cards)[-1].rank if len(suits_set) == 1 else None
    
    def is_straight(self):
        """
        Determines whether this poker hand contains a straight.
        Returns the rank of the high card if it is a straight.
        Otherwise, None is returned.
        """
        contains_duplicates = False
        for occurrences in Counter(card.rank for card in self.cards).values():
            if occurrences > 1:
                contains_duplicates = True
                break
        if not contains_duplicates:
            sorted_hand_ranks = [card.rank for card in sorted(self.cards)]
            if sorted_hand_ranks[-1].value - sorted_hand_ranks[0].value == 4:
                return sorted_hand_ranks[-1]
            return None
        else:
            return None
    
    def is_three_of_a_kind(self):
        """
        Determines whether this poker hand contains a three of a kind.
        Returns the rank of the high card if it is a three of a kind.
        Otherwise, None is returned.
        """
        for rank, occurrences in Counter(card.rank for card in self.cards).items():
            if occurrences == 3:
                return rank
        return None
    
    def is_one_pair(self):
        """
        Determines whether this poker hand contains one pair.
        Returns the rank of the pair. Otherwise, None is returned.
        """
        total_pairs = []
        for rank, occurrences in Counter(card.rank for card in self.cards).items():
            if occurrences == 2:
                total_pairs.append(rank)
        if len(total_pairs) == 1:
            return total_pairs[0]
        else:
            return None
            
    def is_two_pairs(self):
        """
        Determines whether this poker hand contains two pair.
        Returns the ranks of the pairs as a tuple. Otherwise, None is returned.
        """
        total_pairs = []
        for rank, occurrences in Counter(card.rank for card in self.cards).items():
            if occurrences == 2:
                total_pairs.append(rank)
        if len(total_pairs) == 2:
            return (total_pairs[0], total_pairs[1])
        else:
            return None
        
    def high_card(self):
        """Returns the high card in this poker hand."""
        return sorted(self.cards, reverse=True)[0]
    
    
class PokerHand:
    """A class that models a five-card draw poker hand."""
    
    def __init__(self, card_deck):
        """Creates a poker hand by drawing 5 cards from the card deck."""
        assert isinstance(card_deck, CardDeck)
        self.__cards = card_deck.deal_cards(5)
        
    def __str__(self):
        """Diagnotic method to print out the cards in this poker hand."""
        return f"[1]:{str(self.__cards[0])} [2]:{str(self.__cards[1])} [3]:{str(self.__cards[2])} [4]:{str(self.__cards[3])} [5]:{str(self.__cards[4])}"
    
    def display(self):
        """Displays the poker hand in the terminal window."""
        print(f"Your hand is: {str(self.__cards[0])} {str(self.__cards[1])} {str(self.__cards[2])} {str(self.__cards[3])} {str(self.__cards[4])}")       
    
    def replace_cards(self, card_deck, card_indices_replace):
        """Replaces the cards identified in the card_indices_replace list with new cards from the card deck."""
        assert isinstance(card_deck, CardDeck)
        assert isinstance(card_indices_replace, list) and all(isinstance(element, int) for element in card_indices_replace)
        for index in card_indices_replace:
            self.__cards[index-1] = card_deck.deal_card()       
       
    def evaluate(self):
        """
        Evaluate the poker hand and calculate the overall rank of the hand.
        straight flush > four of a kind > full house > flush > straight > three of a kind > two pairs > one pair > high card
        """
        evaluator = PokerHandEvaluator(self.__cards)
        straight_flush_rank = evaluator.is_straight_flush()
        if straight_flush_rank:
            print(f"You have a {straight_flush_rank}-high straight flush.")
        else:
            four_of_a_kind_rank = evaluator.is_four_of_a_kind()
            if four_of_a_kind_rank:
                print(f"You have a four of a kind of {four_of_a_kind_rank}.")
            else:
                full_house_ranks = evaluator.is_full_house()
                if full_house_ranks:
                    print(f"You have a full house, {full_house_ranks[0]} over {full_house_ranks[1]}.")
                else:
                    flush_rank = evaluator.is_flush()
                    if flush_rank:
                        print(f"You have a {flush_rank}-high flush.")
                    else:
                        straight_rank = evaluator.is_straight()
                        if straight_rank:
                            print(f"You have a {straight_rank}-high straight.")
                        else:    
                            three_of_a_kind_rank = evaluator.is_three_of_a_kind()
                            if three_of_a_kind_rank:
                                print(f"You have a three of a kind of {three_of_a_kind_rank}.")
                            else:
                                two_pairs_ranks = evaluator.is_two_pairs()
                                if two_pairs_ranks:
                                    print(f"You have 2 pairs of {two_pairs_ranks[0]} and {two_pairs_ranks[1]}.")
                                else:
                                    one_pair_rank = evaluator.is_one_pair()
                                    if one_pair_rank:
                                        print(f"You have 1 pair of {one_pair_rank}.")
                                    else:
                                        print(f"You have nothing. Your high card is {evaluator.high_card()}.")
                        

def main():
    """Play poker from the command line."""
    print("Welcome to Python Five-Card Draw Poker!")
    deck = CardDeck()
    hand = PokerHand(deck)
    hand.display()
    while True:
        if input("Do you want to replace any cards (y/n)? ").lower() == "y":
            print(hand)
            cards_to_replace = input("Replace these cards (use a space as separator): ").split()
            if len(cards_to_replace) > 3:
                print("Too many cards! Only a max of 3 cards can be replaced. Please try again.")
                continue
            elif len(cards_to_replace) > 0:
                cards_indices = [int(i) for i in cards_to_replace]
                hand.replace_cards(deck, cards_indices)
                hand.display()
            else:
                break
                
        hand.evaluate()        
                
        if input("Play another hand (y/n)? ").lower() == "y":
            hand = PokerHand(deck)
            hand.display()
        else:
            break
    return 0
    
    
if __name__ == "__main__":
    sys.exit(main())