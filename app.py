import config
import logging
import aiogram
import ast
from aiogram import types
from ProxyAgent import Agent

logging.basicConfig(level=logging.INFO);

bot = aiogram.Bot(config.TOKEN);

eventHandler = aiogram.Dispatcher(bot);


def generate_keyboard_for_recipient():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Decrypt message', callback_data='button1')
    keyboard.add(button1)
    return keyboard



def preprocess_message(message):
        message = message.replace("Encrypted message: ", "")
        message = message.replace(", keys: ", " * ")
        message = message.split(" * ")

        return ast.literal_eval(message[0]), ast.literal_eval(message[1])

@eventHandler.callback_query_handler(lambda c: c.data == 'button1')
async def decrypt_message(callback: types.CallbackQuery):
    last_layer, keys = preprocess_message(callback.message.text)
    word, layers = Agent().decrypt_message(last_layer, keys)

    await callback.message.answer(layers)
    await callback.message.answer(word)

@eventHandler.message_handler(commands=['config'])
async def encrypt_command_handler(message: types.Message):
   
    text = message.text[8:]  # Remove the "/config  " part of the command

    string = text

    pairs = string.split(",")

    dictionary = {}

    for pair in pairs:
   
        key, value = pair.split(":")

        key = key.strip()
        value = value.strip()

        dictionary[key] = int(value)

    config.encryption_config = dictionary
    
    
    await message.reply(f"New config: {config.encryption_config}")
    
@eventHandler.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    user_id = message.contact.user_id
    config.recipient_id = user_id
    

    phone_number = contact.phone_number
    first_name = contact.first_name


    
    print(user_id)    
  
    await message.answer('User added successfully')


@eventHandler.message_handler(commands=['encrypt'])
async def encrypt_command_handler(message: types.Message):
    
    text = message.text[9:]  # Remove the "/encrypt " part of the command

    
    encrypted_text, keys , info= Agent().encrypt_message(text, config.encryption_config)
    try:
        await message.reply(info)
    except aiogram.utils.exceptions.MessageIsTooLong: 
        await message.reply("Info in console ")
        print(info)
       
    try:
        await message.reply(f"Encrypted message: {encrypted_text}, keys: {keys} ")
    except aiogram.utils.exceptions.MessageIsTooLong:
        await message.reply("Output in console ")
        print(f"Encrypted message: {encrypted_text},\n keys: {keys} ")
    await bot.send_message(config.recipient_id,f"Encrypted message: {encrypted_text}, keys: {keys} ",reply_markup=generate_keyboard_for_recipient())

if __name__ == "__main__":
    
    aiogram.executor.start_polling(eventHandler,skip_updates=True);
    