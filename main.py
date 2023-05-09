#!/usr/bin/env python3

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter

from db import MeetingDb, MeetingDbException

logging.basicConfig(level=logging.INFO)

API_TOKEN: str = os.environ.get('API_KEY')  # type: ignore

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = MeetingDb()


class AdminFilter(BoundFilter):
    """
    Filter for checking if user is admin
    """
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return chat_member.is_chat_admin()


dp.filters_factory.bind(AdminFilter)


###############################################################################


@dp.message_handler(commands=['meet'])
async def add_meeting(message: types.Message):
    """
    Adding meet to current meetings
    """
    global conn

    descr = message.reply_to_message.text
    start_date = '11.11.11'
    end_date = '12.11.11'

    try:
        ins_id: int = db.addMeetings(descr, start_date, end_date)
    except MeetingDbException as e:
        await message.reply(str(e))
        return

    await message.reply(f"Добавлена сходка #{ins_id}")


@dp.message_handler(commands=['unmeet'])
async def remove_meeting(message: types.Message):
    """
    Remote meetings from current meetings by command
    """
    await message.reply("Сходка ... убрана или закончена")


@dp.message_handler(commands=['was'])
async def was_on_meeting(message: types.Message):
    """
    Add user as meeting participant
    """
    await message.reply("Юзеры ... посетили сходку ...")


@dp.message_handler(commands=['unwas'])
async def unwas_on_meeting(message: types.Message):
    """
    Remove user as meeting participant
    """
    await message.reply("Юзеры ... убраны из сходки ...")


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(str(message))


###############################################################################


if __name__ == '__main__':
    with db as _:
        executor.start_polling(dp, skip_updates=True)
