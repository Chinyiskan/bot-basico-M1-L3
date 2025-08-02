import discord
import random
import os
from bot_logic import gen_pass
from dotenv import load_dotenv

# Diccionario de preguntas y respuestas
python_questions = {
    "¿Qué es una variable en Python?": "Es un espacio en memoria que almacena un valor",
    "¿Cómo se crea una lista en Python?": "Usando corchetes [], por ejemplo: mi_lista = [1, 2, 3]",
    "¿Qué es un bucle for?": "Es una estructura que permite repetir un bloque de código varias veces",
    "¿Qué función se usa para imprimir en Python?": "La función print()",
    "¿Cómo se comenta una línea en Python?": "Usando el símbolo #",
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

current_question = None
current_answer = None

@client.event
async def on_ready():
    print(f'Bot iniciado como {client.user}')

@client.event
async def on_message(message):
    global current_question, current_answer
    
    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        help_text = """
        Comandos disponibles:
        $question - Obtener una pregunta sobre Python
        $answer - Ver la respuesta a la pregunta actual
        $pass <número> - Genera una contraseña con la longitud especificada
        $help - Mostrar esta ayuda
        """
        await message.channel.send(help_text)

    elif message.content.startswith('$pass'):
        try:
            length = int(message.content.split()[1])
            if length > 0:
                password = gen_pass(length)
                await message.channel.send(f"🔒 Tu contraseña generada es: `{password}`")
            else:
                await message.channel.send("❌ La longitud debe ser un número positivo")
        except (IndexError, ValueError):
            await message.channel.send("❌ Uso correcto: $pass <número>")

    elif message.content.startswith('$question'):
        current_question = random.choice(list(python_questions.keys()))
        current_answer = python_questions[current_question]
        await message.channel.send(f"📝 Pregunta: {current_question}")

    elif message.content.startswith('$answer'):
        if current_question:
            await message.channel.send(f"✅ Respuesta: {current_answer}")
        else:
            await message.channel.send("❌ Primero pide una pregunta usando $question")

#Chicos aqui utilizamos el archivo .env para guardar el token de discord
# y no tenerlo en el codigo, para que no se vea en github
# no es necesario que lo hagan, pero es una buena practica
# para guardar datos sensibles

load_dotenv('discord_token.env')
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("No se encontró el token de Discord. Asegúrate de que existe el archivo .env con DISCORD_TOKEN")

client.run(TOKEN)