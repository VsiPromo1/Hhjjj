# УВАГА: Цей файл містить повний код Telegram-бота Jackpot Pulse із двома валютами.

# [Уже включено вище...]

# Фарт-картка
@bot.message_handler(func=lambda m: m.text == '🃏 Фарт-картка')
def fart_card(message):
    user_id = message.from_user.id
    if not check_subscriptions(user_id):
        bot.send_message(message.chat.id, "<b>⚠️ Спершу підпишись на всі наші спонсорські канали!</b>", reply_markup=main_keyboard)
        return

    now = int(time.time())
    last_card = users_data[user_id].get('last_card', 0)
    if now - last_card < 86400:
        bot.send_message(message.chat.id, "<b>⏳ Фарт-картку можна відкривати лише раз на добу. Заходь завтра!</b>", reply_markup=main_keyboard)
        return

    users_data[user_id]['last_card'] = now
    outcomes = [
        ("💰 <b>+50 PulseCoins!</b>", 50),
        ("🎟 <b>Квиток на розіграш!</b>", 0),
        (f"🤣 <i>{random.choice(jokes)}</i>", 0),
        ("🤷‍♂️ <b>Нічого не випало цього разу. Спробуй ще!</b>", 0)
    ]
    text, coins = random.choice(outcomes)
    if "Квиток" in text:
        users_data[user_id]['tickets'] += 1
    if coins > 0:
        users_data[user_id]['pulse'] += coins
    save_data()
    bot.send_message(message.chat.id, f"<b>🃏 Твоя фарт-картка показує:</b>

{text}", reply_markup=main_keyboard)

# Кнопка Вивести
@bot.message_handler(func=lambda m: m.text == '💸 Вивести')
def request_withdraw(message):
    user_id = message.from_user.id
    if users_data.get(user_id, {}).get('lucky', 0) < 250:
        bot.send_message(message.chat.id, "❌ Мінімум для виводу — 250 LuckyTokens", reply_markup=main_keyboard)
        return
    bot.send_message(message.chat.id, "✏️ Введи реквізити для виводу (номер картки, банку або інше):")
    bot.register_next_step_handler(message, process_withdraw_request)

def process_withdraw_request(message):
    user_id = message.from_user.id
    requisites = message.text.strip()
    users_data[user_id]['lucky'] -= 250
    users_data[user_id]['withdraw_request'] = {
        'amount': 250,
        'requisites': requisites,
        'status': 'pending',
        'timestamp': int(time.time())
    }
    save_data()
    bot.send_message(message.chat.id, "✅ Заявка прийнята. Обробка протягом 48 годин.", reply_markup=main_keyboard)
    bot.send_message(ADMIN_ID, f"📤 Запит на виведення від @{message.from_user.username} ({user_id}):
💰 Сума: 250 LuckyTokens
🏦 Реквізити: {requisites}")

# Топ 5 гравців
@bot.message_handler(func=lambda m: m.text == '⭐️ Топ 5 гравців')
def top_players(message):
    top = sorted(users_data.items(), key=lambda x: x[1].get('pulse', 0), reverse=True)[:5]
    text = "<b>🏆 Топ 5 гравців за PulseCoins:</b>

"
    for i, (uid, data) in enumerate(top, 1):
        username = f"@{bot.get_chat(uid).username}" if bot.get_chat(uid).username else str(uid)
        text += f"{i}. {username} — {data['pulse']} PulseCoins
"
    bot.send_message(message.chat.id, text)

# Реферальне посилання
@bot.message_handler(func=lambda m: m.text == '👯 Запросити друга')
def invite(message):
    ref_link = f"https://t.me/JackpotPulse_bot?start={message.from_user.id}"
    bot.send_message(message.chat.id, f"<b>👥 Запроси друзів!</b>

Твоє реф-посилання:
{ref_link}", reply_markup=main_keyboard)

# Запуск бота
print("✅ Jackpot Pulse Bot запущено...")
bot.infinity_polling()
