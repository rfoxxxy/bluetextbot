from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_template import dp
from bot_template.keyboards.models import ButtonRow, InlineKeyboard, URLButton


@dp.callback_query_handler(text="test_callback")
async def test_button(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    match action:
        case "show_username":
            return await call.answer(f"SUCCESS!\n\nusername: {callback_data['user'].name}", True)
        case _:
            return await call.answer("SUCCESS!", True)


@dp.message_handler(commands=['reset_state'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    if not await state.get_state():
        return await message.reply("no state active")
    await state.reset_state(with_data=False)
    return await message.reply("success")


@dp.inline_handler(text="tests")
async def test_inline_handler(query: types.InlineQuery):
    keyboard = InlineKeyboard(ButtonRow(URLButton("google", "https://google.com")))
    return await query.answer([types.InlineQueryResultArticle(id=query.id + "1",
                                                              title="test",
                                                              reply_markup=keyboard,
                                                              description="test object",
                                                              input_message_content=types.InputTextMessageContent("test"))],
                              cache_time=0)


@dp.chosen_inline_handler()
async def test_chosen_inline_handler(chosen: types.ChosenInlineResult):
    await chosen.bot.edit_message_text(f"test successful, {chosen.from_user.full_name}!", inline_message_id=chosen.inline_message_id)
