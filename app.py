import config
import logging
import aiogram
from aiogram import types
from ProxyAgent import Agent

logging.basicConfig(level=logging.INFO);

bot = aiogram.Bot(config.TOKEN);

eventHandler = aiogram.Dispatcher(bot);

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
    

    phone_number = contact.phone_number
    first_name = contact.first_name


    
    print(user_id)    
  
    await message.reply_contact(phone_number=phone_number, first_name=first_name)


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

if __name__ == "__main__":
    
    aiogram.executor.start_polling(eventHandler,skip_updates=True);
    