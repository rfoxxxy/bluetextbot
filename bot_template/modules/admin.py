from aiogram import types

from bot_template import dp, utils


@dp.message_handler(commands=['ram'], state="*", is_admin=True)
async def ram_handler(message: types.Message):
    return await message.reply(f"RAM: {await utils.get_process_memory()}MB")


@dp.message_handler(commands=['uptime'], state="*", is_admin=True)
async def uptime_handler(message: types.Message):
    return await message.reply(f"Uptime: {utils.get_uptime()}")
