#!/usr/bin/env python3
"""
Telegram Bot - Основной файл приложения
"""

import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# Импортируем модули
from modules.finance_tracker import FinanceTracker

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        if not self.token:
            raise ValueError("BOT_TOKEN не найден в переменных окружения!")
        
        self.application = Application.builder().token(self.token).build()
        
        # Инициализируем модули
        self.finance_tracker = FinanceTracker()
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("finance", self.finance_command))
        
        # Обработка нажатий на кнопки
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработка текстовых сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Обработка ошибок
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        welcome_message = f"""
🤖 Добро пожаловать, {user.first_name}!

Я умный Telegram бот с множеством полезных функций.

📋 Доступные команды:
/start - Начать работу с ботом
/help - Показать справку
/info - Информация о боте
/menu - Главное меню

Выберите действие или используйте команду /menu для навигации.
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Главное меню", callback_data="main_menu")],
            [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
📚 **Справка по командам:**

🔹 `/start` - Начать работу с ботом
🔹 `/help` - Показать эту справку
🔹 `/info` - Информация о боте
🔹 `/menu` - Открыть главное меню

💡 **Дополнительные функции:**
• Отправьте мне любой текст, и я отвечу
• Используйте кнопки для быстрой навигации
• Бот работает 24/7

🆘 **Нужна помощь?**
Обратитесь к администратору или используйте команду /info
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /info"""
        info_text = f"""
ℹ️ **Информация о боте:**

🤖 **Название:** {os.getenv('BOT_NAME', 'Telegram Bot')}
📝 **Описание:** {os.getenv('BOT_DESCRIPTION', 'Умный Telegram бот')}
🕒 **Время запуска:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🐍 **Версия Python:** {asyncio.get_event_loop().get_debug()}
📊 **Статус:** Активен ✅

🔧 **Технологии:**
• python-telegram-bot
• asyncio
• python-dotenv

💻 **Разработчик:** Создано с помощью Cursor AI
        """
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /menu"""
        await self.show_main_menu(update, context)
    
    async def finance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /finance"""
        await self.finance_tracker.show_finance_menu(update, context)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать главное меню"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Финансовый трекер", callback_data="finance_menu"),
                InlineKeyboardButton("📝 Текстовые функции", callback_data="text_functions")
            ],
            [
                InlineKeyboardButton("🎮 Игры", callback_data="games"),
                InlineKeyboardButton("📊 Утилиты", callback_data="utilities")
            ],
            [
                InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
                InlineKeyboardButton("ℹ️ Информация", callback_data="info")
            ],
            [
                InlineKeyboardButton("❓ Помощь", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = """
🎯 **Главное меню**

Выберите категорию функций:
        """
        
        if update.callback_query:
            await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        # Финансовый трекер
        if query.data.startswith("finance_"):
            await self.handle_finance_callback(update, context)
            return
        
        if query.data == "main_menu":
            await self.show_main_menu(update, context)
        
        elif query.data == "help":
            help_text = """
📚 **Справка по функциям:**

💰 **Финансовый трекер** - учет доходов и расходов
🔹 **Текстовые функции** - работа с текстом
🔹 **Игры** - мини-игры для развлечения
🔹 **Утилиты** - полезные инструменты
🔹 **Настройки** - настройка бота
🔹 **Информация** - данные о боте

💡 Используйте кнопки для навигации по меню.
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "stats":
            stats_text = f"""
📊 **Статистика бота:**

👥 **Пользователь:** {update.effective_user.first_name}
🆔 **ID:** {update.effective_user.id}
🕒 **Время:** {datetime.now().strftime('%H:%M:%S')}
📅 **Дата:** {datetime.now().strftime('%Y-%m-%d')}

⚡ **Статус:** Активен
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "text_functions":
            text_func_text = """
📝 **Текстовые функции:**

🔹 Отправьте мне любой текст
🔹 Я отвечу на ваше сообщение
🔹 Поддерживаю эмодзи и форматирование
🔹 Могу анализировать текст

💡 Просто напишите мне что-нибудь!
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text_func_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "games":
            games_text = """
🎮 **Игры:**

🎲 **Кнопка "Игры"** - скоро здесь появятся мини-игры!

Планируемые игры:
• 🎯 Угадай число
• ✂️ Камень, ножницы, бумага
• 🎲 Кости
• 🧩 Викторины

🔧 В разработке...
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(games_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "utilities":
            utils_text = """
📊 **Утилиты:**

🔧 **Доступные инструменты:**
• 📅 Калькулятор времени
• 📏 Конвертер единиц
• 🌤️ Погода (в разработке)
• 📰 Новости (в разработке)

💡 Выберите нужную утилиту
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(utils_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "settings":
            settings_text = """
⚙️ **Настройки:**

🔧 **Доступные настройки:**
• 🌍 Язык интерфейса
• 🔔 Уведомления
• 🎨 Тема оформления
• 📊 Статистика

💡 Настройки будут доступны в следующих версиях
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif query.data == "info":
            info_text = f"""
ℹ️ **Информация о боте:**

🤖 **Название:** {os.getenv('BOT_NAME', 'Telegram Bot')}
📝 **Описание:** {os.getenv('BOT_DESCRIPTION', 'Умный Telegram бот')}
🕒 **Время запуска:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 **Статус:** Активен ✅

🔧 **Технологии:**
• python-telegram-bot
• asyncio
• python-dotenv

💻 **Разработчик:** Создано с помощью Cursor AI
            """
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(info_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_finance_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка callback'ов финансового трекера"""
        query = update.callback_query
        
        if query.data == "finance_menu":
            await self.finance_tracker.show_finance_menu(update, context)
        
        elif query.data == "finance_add_income":
            await self.finance_tracker.show_category_selection(update, context, "income")
        
        elif query.data == "finance_add_expense":
            await self.finance_tracker.show_category_selection(update, context, "expense")
        
        elif query.data.startswith("finance_cat_"):
            await self.finance_tracker.handle_category_selection(update, context)
        
        elif query.data == "finance_stats":
            await self.finance_tracker.show_statistics(update, context)
        
        elif query.data == "finance_history":
            await self.finance_tracker.show_history(update, context)
        
        elif query.data == "finance_goals":
            await self.finance_tracker.show_goals(update, context)
        
        elif query.data == "finance_budgets":
            await self.finance_tracker.show_budgets(update, context)
        
        elif query.data == "finance_settings":
            await self.finance_tracker.show_settings(update, context)
        
        elif query.data == "finance_reports":
            await self.finance_tracker.show_reports(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_message = update.message.text
        user = update.effective_user
        
        # Проверяем, находится ли пользователь в процессе добавления транзакции
        if 'finance_type' in context.user_data:
            # Обрабатываем ввод для финансового трекера
            if 'finance_amount' not in context.user_data:
                # Пользователь вводит сумму
                handled = await self.finance_tracker.handle_amount_input(update, context)
                if handled:
                    return
            else:
                # Пользователь вводит описание
                handled = await self.finance_tracker.handle_description_input(update, context)
                if handled:
                    return
        
        # Простой ответ на сообщение
        response = f"""
💬 **Ваше сообщение:** {user_message}

👋 Привет, {user.first_name}! 

Я получил ваше сообщение и готов помочь. Используйте команду /menu для доступа к функциям бота или /help для справки.

🕒 **Время:** {datetime.now().strftime('%H:%M:%S')}
        """
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ошибок"""
        logger.error(f"Ошибка при обработке обновления {update}: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка при обработке вашего запроса. Попробуйте еще раз или используйте /help для справки."
            )
    
    async def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск Telegram бота...")
        
        # Запуск бота
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("✅ Бот успешно запущен!")
        
        # Ожидание завершения
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("🛑 Получен сигнал остановки...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("👋 Бот остановлен")

async def main():
    """Главная функция"""
    try:
        bot = TelegramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
