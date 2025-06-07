import logging
import os
import signal
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (рекомендуется использовать переменную окружения)
TOKEN = os.getenv("TOKEN", "7784851665:AAH-AkFYh1tgcYxG9ti4DZJvogAseC5hVAM")

# Список товаров с URL-адресами изображений
PRODUCTS = [
    {"name": "Буст макс ранга", "price": "200 руб", "image": "https://via.placeholder.com/150?text=Max+Rank+Boost"},
    {"name": "Буст мифик лиги", "price": "200 руб",
     "image": "https://via.placeholder.com/150?text=Mythic+League+Boost"},
    {"name": "Буст кубки от 0 до 500 и от 500 до 1000 кубков", "price": "от 100 рублей до 150 рублей (цена договорная)",
     "image": "https://via.placeholder.com/150?text=Cups+Boost"},
    {"name": "Буст квестов", "price": "150 руб", "image": "https://via.placeholder.com/150?text=Quests+Boost"},
    {"name": "Предложить свою услугу", "price": "цену обговорим",
     "image": "https://via.placeholder.com/150?text=Custom+Service"}
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Список товаров", callback_data='catalog')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "Привет! Ты попал в моего бота! 😎\n"
        "В этом боте ты можешь ознакомиться с моими услугами.\n"
        "Все проходит строго лично через меня.\n"
        "Напиши мне, пожалуйста, если тебе что-то приглянется!"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == 'catalog':
        await query.message.reply_text("📋 Мои услуги:")

        for i, product in enumerate(PRODUCTS, 1):
            message = f"{i}. {product['name']} - {product['price']}"
            # Создаем inline-клавиатуру для каждой картинки
            keyboard = [[InlineKeyboardButton("Выбрать", callback_data=f"product_{i}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if product['image']:
                await query.message.reply_photo(
                    photo=product['image'],
                    caption=message,
                    reply_markup=reply_markup
                )
            else:
                await query.message.reply_text(message)

        # Создаем общую клавиатуру с товарами
        keyboard = [
            [InlineKeyboardButton(product['name'], callback_data=f"product_{i}")]
            for i, product in enumerate(PRODUCTS)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выберите услугу:", reply_markup=reply_markup)

    elif query.data.startswith('product_'):
        product_index = int(query.data.split('_')[1]) - 1
        requisites_message = (
            "Реквизиты:\n"
            "@Tyezik (пишите только по делу, прошу не спамить, могу не отвечать)\n"
            "Ссылка на https://www.donationalerts.com/r/makarovbyshop\n"
            "(прошу отправляйте точную сумму и в комментарий поясните за что платите, "
            "также не оплачивайте сразу, только после консультации со мной)\n"
            "Также гарантированно верну деньги, если не смогу выполнить заказ"
        )
        await query.message.reply_text(requisites_message)


async def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота в режиме polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    # Ожидаем сигнал завершения
    try:
        while True:
            await asyncio.sleep(3600)  # Спим 1 час, чтобы не нагружать CPU
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения, останавливаем бот...")
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())