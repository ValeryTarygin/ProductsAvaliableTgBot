from aiogram.types import ParseMode
from aiogram import utils 
from peewee import *

db = SqliteDatabase('video.db')

class BaseModel(Model):
    class Meta:
        database = db


class Products(BaseModel):
    title = CharField()
    url = TextField()


class SearchModel(BaseModel):
    title = CharField()
    chatid = CharField()


def find_all_products():
    return Products.select()


def find_id_search(chat_id):
    return SearchModel.select().where(SearchModel.chatid == chat_id)


def find_all_search():
    return SearchModel.select()


async def process_search_model(message):
    search_exist = True
    try: 
        search = SearchModel.select().where(SearchModel.title == message.text, SearchModel.chatid == message.chat.id).get()
        search.delete_instance()
        await message.answer('Строка поиска {} удалена'.format(message.text))
        return search_exist
    except DoesNotExist as de:
        search_exist = False

    if not search_exist:
        rec = SearchModel(title=message.text, chatid=message.chat.id)
        rec.save()
        await message.answer('Строка поиска {} добавлена'.format(message.text))
    else:
        await message.answer('Строка поиска {} уже есть'.format(message.text))
    return search_exist


async def process_product(title, url, chat_id, bot):
    product_exist = True
    try:
        product = Products.select().where(Products.title == title).get()
    except DoesNotExist as de:
        product_exist = False

    if not product_exist:
        rec = Products(title=title, url=url)
        rec.save()
        message_text = utils.markdown.hlink(title, url)
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)
    return product_exist


def init_db():
    db.create_tables([Products, SearchModel])