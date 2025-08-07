from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
from game_logic import play_ai_game, determine_winner

ADMIN_ID = 6575412146
rooms = {}
leaderboard_file = "leaderboard.json"

def update_leaderboard(user_id, result):
    try:
        with open(leaderboard_file, 'r') as f:
            board = json.load(f)
    except:
        board = {}
    if str(user_id) not in board:
        board[str(user_id)] = {"win": 0, "loss": 0, "draw": 0}
    board[str(user_id)][result] += 1
    with open(leaderboard_file, 'w') as f:
        json.dump(board, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [['Play AI 🤖', 'Create PvP Room 🔐']]
    await update.message.reply_text("Welcome to the Game Bot!", reply_markup=ReplyKeyboardMarkup(kb))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if text == 'play ai 🤖':
        kb = [['Rock', 'Paper', 'Scissors']]
        await update.message.reply_text("Choose your move:", reply_markup=ReplyKeyboardMarkup(kb))
        context.user_data['mode'] = 'ai'
        return

    if context.user_data.get('mode') == 'ai':
        result, ai_move = play_ai_game(text)
        update_leaderboard(user_id, result)
        await update.message.reply_text(f"AI chose {ai_move.capitalize()}. You {result.upper()}!")

    elif text == 'create pvp room 🔐':
        rooms[user_id] = {"player1": user_id, "player2": None, "move1": None, "move2": None}
        await update.message.reply_text(f"Room created. Share your ID: {user_id}")

    elif text.startswith("join ") and text.split()[1].isdigit():
        room_owner = int(text.split()[1])
        if room_owner in rooms and rooms[room_owner]['player2'] is None:
            rooms[room_owner]['player2'] = user_id
            await update.message.reply_text("Joined the game. Now both players can send 'Rock', 'Paper', or 'Scissors'")
        else:
            await update.message.reply_text("Room not available.")

    elif text in ['rock', 'paper', 'scissors']:
        for room_id, room in rooms.items():
            if room['player1'] == user_id or room['player2'] == user_id:
                if room['player1'] == user_id:
                    room['move1'] = text
                else:
                    room['move2'] = text
                if room['move1'] and room['move2']:
                    winner = determine_winner(room['move1'], room['move2'])
                    if winner == 'draw':
                        msg = "It's a DRAW!"
                        update_leaderboard(room['player1'], 'draw')
                        update_leaderboard(room['player2'], 'draw')
                    elif winner == 'player1':
                        msg = "Player 1 WINS!"
                        update_leaderboard(room['player1'], 'win')
                        update_leaderboard(room['player2'], 'loss')
                    else:
                        msg = "Player 2 WINS!"
                        update_leaderboard(room['player2'], 'win')
                        update_leaderboard(room['player1'], 'loss')
                    await context.bot.send_message(chat_id=room['player1'], text=msg)
                    await context.bot.send_message(chat_id=room['player2'], text=msg)
                    del rooms[room_id]
                return

    elif text == 'leaderboard':
        try:
            with open(leaderboard_file, 'r') as f:
                board = json.load(f)
            user_stats = board.get(str(user_id), {"win": 0, "loss": 0, "draw": 0})
            await update.message.reply_text(f"🏆 Your Stats:\nWins: {user_stats['win']}\nLosses: {user_stats['loss']}\nDraws: {user_stats['draw']}")
        except:
            await update.message.reply_text("No leaderboard data yet.")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Access denied.")
        return
    await update.message.reply_text("Welcome Admin.")

app = ApplicationBuilder().token("8446535268:AAGeQGM5NL2qJVtZxowiF6_cWHb4Z5xM4Xk").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

if __name__ == "__main__":
    app.run_polling()