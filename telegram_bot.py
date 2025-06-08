import logging
import os
import signal
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = os.getenv("TOKEN", "7784851665:AAH-AkFYh1tgcYxG9ti4DZJvogAseC5hVAM")

# Список товаров
PRODUCTS = [
    {"name": "Буст макс ранга", "price": "200 руб", "image": "https://imgur.com/aX1QifJ"},
    {"name": "Буст мифик лиги", "price": "200 руб",
     "image": "https://imgur.com/r6xHSuB"},
    {"name": "Буст кубки от 0 до 500 и от 500 до 1000 кубков", "price": "от 100 рублей до 150 рублей (цена договорная)",
     "image": "https://imgur.com/x9YixzM"},
    {"name": "Буст квестов", "price": "150 руб", "image": "https://imgur.com/qIwBeF5"},
    {"name": "Предложить свою услугу", "price": "цену обговорим",
     "image": "https://via.placeholder.com/150?text=Custom+Service"}
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [[InlineKeyboardButton("Список товаров", callback_data='catalog')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = (
        "Привет! Ты попал в моего бота! 😎\n"
        "В этом боте ты можешь ознакомиться с моими услугами.\n"
        "Все проходит строго лично через меня.\n"
        "Напиши мне, пожалуйста, если тебе что-то приглянется!"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    logger.info("Команда /start выполнена")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    logger.info(f"Получен callback: {query.data}")

    try:
        if query.data == 'catalog':
            await query.message.reply_text("📋 Мои услуги:")
            for i, product in enumerate(PRODUCTS, 1):
                message = f"{i}. {product['name']} - {product['price']}"
                keyboard = [[InlineKeyboardButton("Выбрать", callback_data=f"product_{i}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                try:
                    await query.message.reply_photo(
                        photo=product['image'],
                        caption=message,
                        reply_markup=reply_markup
                    )
                except TelegramError as e:
                    logger.error(f"Ошибка при отправке фото для {product['name']}: {e}")
                    await query.message.reply_text(message, reply_markup=reply_markup)

        elif query.data.startswith('product_'):
            try:
                product_index = int(query.data.split('_')[1]) - 1
                if 0 <= product_index < len(PRODUCTS):
                    product = PRODUCTS[product_index]
                    requisites_message = (
                        f"Вы выбрали: {product['name']} - {product['price']}\n\n"
                        "Реквизиты:\n"
                        "@Tyezik (пишите только по делу, прошу не спамить, могу не отвечать)\n"
                        "Ссылка на https://www.donationalerts.com/r/makarovbyshop\n"
                        "(прошу отправляйте точную сумму и в комментарий поясните за что платите, "
                        "также не оплачивайте сразу, только после консультации со мной)\n"
                        "Также гарантированно верну деньги, если не смогу выполнить заказ"
                    )
                    await query.message.reply_text(requisites_message)
                    logger.info(f"Отправлены реквизиты для продукта {product['name']}")
                else:
                    await query.message.reply_text("Ошибка: выбран некорректный товар.")
                    logger.error(f"Некорректный индекс продукта: {product_index}")
            except ValueError as e:
                logger.error(f"Ошибка обработки callback_data {query.data}: {e}")
                await query.message.reply_text("Ошибка при выборе товара.")

    except TelegramError as e:
        logger.error(f"Ошибка Telegram API: {e}")
        await query.message.reply_text("Произошла ошибка, попробуйте позже.")


async def main() -> None:
    """Запуск бота"""
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_callback))
        await application.initialize()
        await application.start()
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Бот запущен")

        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Получен сигнал завершения, останавливаем бот...")
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())