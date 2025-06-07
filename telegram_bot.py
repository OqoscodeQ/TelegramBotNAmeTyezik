import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "7784851665:AAH-AkFYh1tgcYxG9ti4DZJvogAseC5hVAM"

# Список товаров
PRODUCTS = [
    {"name": "Буст макс ранга", "price": "200 руб", "image": None},
    {"name": "Буст мифик лиги", "price": "200 руб", "image": None},
    {"name": "Буст кубки от 100 кубков", "price": "от 50 рублей (цена договорная)", "image": None},
    {"name": "Предложить свою услугу", "price": "цену обговорим", "image": None}
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
            # Если в будущем добавите изображения, можно будет раскомментировать
            # if product['image']:
            #     await query.message.reply_photo(photo=product['image'], caption=message)
            # else:
            await query.message.reply_text(message)

        # Создаем клавиатуру с товарами
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


def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()