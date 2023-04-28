from aiogram import types

from bluetextbot import dp


@dp.inline_handler(state="*")
async def inline_handler(query: types.InlineQuery):
    return await query.answer([
        types.InlineQueryResultArticle(
            id=1,
            input_message_content=types.InputTextMessageContent(
                "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"
            ),
            title="send blue text",
            description="so many retarded animals...")
    ], 0, False)
