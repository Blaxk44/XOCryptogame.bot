from random import choice
from config import PLATFORM_FEE, WIN_MULTIPLIER
from wallet_logic import deposit, withdraw, get_balance

def start_game(user1_id, user2_id, bet_amount):
    total_pot = bet_amount * 2
    winner = choice([user1_id, user2_id])  # For now random winner
    winner_amount = bet_amount * WIN_MULTIPLIER
    platform_fee = bet_amount * PLATFORM_FEE

    deposit(winner, winner_amount)
    return winner, winner_amount, platform_fee
import random

def play_ai_game(user_move):
    moves = ['rock', 'paper', 'scissors']
    ai_move = random.choice(moves)
    if ai_move == user_move:
        return 'draw', ai_move
    if (user_move == 'rock' and ai_move == 'scissors') or \
       (user_move == 'paper' and ai_move == 'rock') or \
       (user_move == 'scissors' and ai_move == 'paper'):
        return 'win', ai_move
    return 'lose', ai_move

def determine_winner(move1, move2):
    if move1 == move2:
        return 'draw'
    if (move1 == 'rock' and move2 == 'scissors') or \
       (move1 == 'paper' and move2 == 'rock') or \
       (move1 == 'scissors' and move2 == 'paper'):
        return 'player1'
    return 'player2'
