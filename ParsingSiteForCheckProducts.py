import logging
import asyncio
import random
from aiogram import Bot, Dispatcher, executor, utils, types
from aiogram.types import ParseMode
from config import TOKEN, MAP_URL
from db import process_search_model, init_db, find_id_search, find_all_products, delete_products_by_id
from parser_site import ParseProducts
from parser_site import ParseProductsDns


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='list')
async def send_list(message: types.Message):
    search_models = find_id_search(message.chat.id)
    products = find_all_products()
    for product in products:
        product_title = product.title
        for search_model in search_models:
            search_title = search_model.title
            if product_title.find(search_title) >= 0:
                message_text = 'Строка поиска {} \r\n Найдено {}'.format(search_title, utils.markdown.hlink(product_title, product.url))
                await message.answer(text=message_text, parse_mode=ParseMode.HTML)

@dp.message_handler(commands='search')
async def send_search(message: types.Message):
    search_models = find_id_search(message.chat.id)
    for search_model in search_models:    
        await message.answer(text=search_model.title)

@dp.message_handler(commands='clear')
async def send_clear_db(message: types.Message):
    message_text = delete_products_by_id(message.chat.id)
    await message.answer(text=message_text)

@dp.message_handler(commands='help')
async def send_help(message: types.Message):
    message_text = 'Поиск продукта по ключевым словам. Введенное слово добавляется в список искомых, повторный ввод слова удаляет его из списка. \
    Все команды: \n \
    /search - слова поиска; \n\
    /list - список найденных товаров; \n\
    /clear - очистка базы данных с товарами; \n\
    /sites - список сайтов'

    await message.answer(text=message_text)

@dp.message_handler(commands='sites')
async def send_list_sites(message: types.Message):
    message_text = 'SONY: {} \n DNS: {}'.format(MAP_URL['SONY'], MAP_URL['DNS'])
    await message.answer(text=message_text)

@dp.message_handler()
async def echo(message: types.Message):    
    await process_search_model(message)


async def scheduled(wait_for, parser):
    while True:
       await asyncio.sleep(wait_for)
       await parser.parse()

if __name__ == '__main__':
    init_db()
    parser = ParseProducts(url=MAP_URL["SONY"], bot=bot)
    parserDns = ParseProductsDns(url=MAP_URL["DNS"], bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(random.randint(30,50), parser))
    loop.create_task(scheduled(random.randint(30,50), parserDns))
    executor.start_polling(dp, skip_updates=True)