import os
import sqlite3
from datetime import datetime
import telebot
from telebot import types

TOKEN = "7623908162:AAHrl4ntkl8b_NyHE3f3sQGHfu70zSnN1Jg"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 6538670514

print("Bot concienciando...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("♻️ Reciclar")
    btn2 = types.KeyboardButton("🔧 Diagnóstico")
    btn3 = types.KeyboardButton("📞 Contacto")
    btn4 = types.KeyboardButton("ℹ️ Más Info")
    btn5 = types.KeyboardButton("🛞 Refacciones")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    if user_id == ADMIN_ID:
        markup.add(types.KeyboardButton("⛔ Apagar bot"))

    bot.send_message(
        message.chat.id,
        f"Hola, soy Refacell_ConciencIAR.\nTu ID es: {user_id}\n¿En qué puedo ayudarte hoy?",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text.lower() == "hola")
def handle_hola(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    print(f"[{message.from_user.first_name}] ({message.from_user.id}): {message.text}")

    conn = sqlite3.connect("registro.db")
    cursor = conn.cursor()

    user_id = message.from_user.id
    nombre = message.from_user.first_name
    texto = message.text
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO conversaciones (user_id, nombre, mensaje, fecha) VALUES (?, ?, ?, ?)",
                   (user_id, nombre, texto, fecha))

    conn.commit()
    conn.close()

    if message.text == "♻️ Reciclar":
        bot.send_message(message.chat.id, "Perfecto. ¿Qué tipo de equipo deseas reciclar?")
    elif message.text == "🔧 Diagnóstico":
        bot.send_message(message.chat.id, "Describe la falla de tu equipo y uno de nuestros técnicos te ayudará.")
    elif message.text == "📞 Contacto":
        bot.send_message(message.chat.id, "Puedes escribirnos directo por WhatsApp o dejarnos tu número aquí.")
    elif message.text == "ℹ️ Más Info":
        bot.send_message(message.chat.id, "Refacell_ConciencIAR es un proyecto de reciclaje, conciencia tecnológica y reparación.")
    elif message.text == "🛞 Refacciones":
        bot.send_message(message.chat.id, "Pasanos el dato, marca, modelo(como aparece en la tapa, alfanumerico), si es 5g, nombre de la pieza, foto de tapa trasera y en un momento te conectamos con tu refaccion.")
    elif message.text == "⛔ Apagar bot" and message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Apagando bot... Hasta pronto.")
        os._exit(0)
    else:
        bot.send_message(message.chat.id, "No entendí eso. Elige una opción del menú.")

bot.polling()
