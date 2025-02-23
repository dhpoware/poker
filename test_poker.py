# test_poker.py
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

from poker import PokerHandEvaluator, Card, CardRank, CardSuit

"""Test cases for the poker module."""

def test_pokerhandevaluator_is_straight_flush():
    straight_flush = [
        Card(CardRank.QUEEN, CardSuit.HEARTS),
        Card(CardRank.JACK, CardSuit.HEARTS),
        Card(CardRank.TEN, CardSuit.HEARTS),
        Card(CardRank.NINE, CardSuit.HEARTS),
        Card(CardRank.EIGHT, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(straight_flush)
    assert evaluator.is_straight_flush()
    
    not_straight_flush = [
        Card(CardRank.NINE, CardSuit.CLUBS),
        Card(CardRank.NINE, CardSuit.SPADES),
        Card(CardRank.NINE, CardSuit.DIAMONDS),
        Card(CardRank.NINE, CardSuit.HEARTS),
        Card(CardRank.JACK, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(not_straight_flush)
    assert not evaluator.is_straight_flush()

def test_pokerhandevaluator_four_of_a_kind():
    four_of_a_kind = [
        Card(CardRank.NINE, CardSuit.CLUBS),
        Card(CardRank.NINE, CardSuit.SPADES),
        Card(CardRank.NINE, CardSuit.DIAMONDS),
        Card(CardRank.NINE, CardSuit.HEARTS),
        Card(CardRank.JACK, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(four_of_a_kind)
    assert evaluator.is_four_of_a_kind()
    
    not_four_of_a_kind = [
        Card(CardRank.TREY, CardSuit.CLUBS),
        Card(CardRank.TREY, CardSuit.SPADES),
        Card(CardRank.TREY, CardSuit.DIAMONDS),
        Card(CardRank.SIX, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(not_four_of_a_kind)
    assert not evaluator.is_four_of_a_kind()

def test_pokerhandevaluator_full_house():
    full_house = [
        Card(CardRank.TREY, CardSuit.CLUBS),
        Card(CardRank.TREY, CardSuit.SPADES),
        Card(CardRank.TREY, CardSuit.DIAMONDS),
        Card(CardRank.SIX, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(full_house)
    assert evaluator.is_full_house()
    
    not_full_house = [
        Card(CardRank.KING, CardSuit.CLUBS),
        Card(CardRank.TEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.CLUBS),
        Card(CardRank.FOUR, CardSuit.CLUBS)
    ]
    evaluator = PokerHandEvaluator(not_full_house)
    assert not evaluator.is_full_house()

def test_pokerhandevaluator_flush():
    flush = [
        Card(CardRank.KING, CardSuit.CLUBS),
        Card(CardRank.TEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.CLUBS),
        Card(CardRank.FOUR, CardSuit.CLUBS)
    ]
    evaluator = PokerHandEvaluator(flush)
    assert evaluator.is_flush()
    
    not_flush = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.SPADES),
        Card(CardRank.FIVE, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(not_flush)
    assert not evaluator.is_flush()
    
def test_pokerhandevaluator_straight():
    straight = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SIX, CardSuit.SPADES),
        Card(CardRank.FIVE, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(straight)
    assert evaluator.is_straight()
    
    not_straight = [
        Card(CardRank.QUEEN, CardSuit.HEARTS),
        Card(CardRank.TEN, CardSuit.SPADES),
        Card(CardRank.TEN, CardSuit.HEARTS),
        Card(CardRank.EIGHT, CardSuit.SPADES),
        Card(CardRank.QUEEN, CardSuit.DIAMONDS)
    ]
    evaluator = PokerHandEvaluator(not_straight)
    assert not evaluator.is_straight()

def test_pokerhandevaluator_three_of_a_kind():
    three_of_a_kind = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.SPADES),
        Card(CardRank.SEVEN, CardSuit.DIAMONDS),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(three_of_a_kind)
    assert evaluator.is_three_of_a_kind()
    
    not_three_of_a_kind = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.DIAMONDS),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(not_three_of_a_kind)
    assert not evaluator.is_three_of_a_kind()

def test_pokerhandevaluator_two_pairs():
    two_pairs = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.DIAMONDS),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(two_pairs)
    assert evaluator.is_two_pairs()
    
    not_two_pairs = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.SPADES),
        Card(CardRank.SIX, CardSuit.DIAMONDS),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(not_two_pairs)
    assert not evaluator.is_two_pairs()

def test_pokerhandevaluator_one_pair():
    one_pair = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.SEVEN, CardSuit.SPADES),
        Card(CardRank.SIX, CardSuit.DIAMONDS),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS)
    ]
    evaluator = PokerHandEvaluator(one_pair)
    assert evaluator.is_one_pair()
    
    not_one_pair = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.FIVE, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS),
        Card(CardRank.DEUCE, CardSuit.SPADES)
    ]
    evaluator = PokerHandEvaluator(not_one_pair)
    assert not evaluator.is_one_pair()

def test_pokerhandevaluator_high_card():
    high_card = [
        Card(CardRank.SEVEN, CardSuit.CLUBS),
        Card(CardRank.FIVE, CardSuit.SPADES),
        Card(CardRank.FOUR, CardSuit.HEARTS),
        Card(CardRank.TREY, CardSuit.HEARTS),
        Card(CardRank.DEUCE, CardSuit.SPADES)
    ]
    evaluator = PokerHandEvaluator(high_card)
    assert evaluator.high_card()