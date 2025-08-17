#!/usr/bin/env python3
"""
Простой Telegram Bot для тестирования
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleFinanceBot:
    def __init__(self):
        # Жестко заданный токен
        self.bot_token = "8008868923:AAFoy6ZTFhSPz37XzVOOft5oXuW8DDVjgZ0"
        self.webapp_url = "http://localhost:3000"
        self.data_file = "simple_bot_data.json"
        self.categories = {
            'expenses': {
                '🍔 Еда': 'food',
                '🚗 Транспорт': 'transport',
                '🏠 Жилье': 'housing',
                '👕 Одежда': 'clothing',
                '💊 Здоровье': 'health',
                '🎮 Развлечения': 'entertainment',
                '📚 Образование': 'education',
                '💳 Кредиты': 'loans',
                '📱 Технологии': 'technology',
                '🏦 Налоги': 'taxes',
                '🎁 Подарки': 'gifts',
                '✈️ Путешествия': 'travel',
                '💼 Бизнес': 'business',
                '🔧 Услуги': 'services',
                '📦 Покупки': 'shopping',
                '💰 Другое': 'other'
            },
            'income': {
                '💼 Зарплата': 'salary',
                '🏢 Бизнес': 'business',
                '📈 Инвестиции': 'investments',
                '🎁 Подарки': 'gifts',
                '🏠 Аренда': 'rental',
                '💻 Фриланс': 'freelance',
                '🎯 Премии': 'bonuses',
                '💰 Другое': 'other'
            }
        }
        
        self.load_data()
        self.setup_handlers()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                self.data = {}
        else:
            self.data = {}
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user_data(self, user_id: int) -> Dict:
        """Получить данные пользователя"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                'transactions': [],
                'budgets': {},
                'goals': [],
                'currency': 'RUB',
                'settings': {
                    'theme': 'light',
                    'notifications': True,
                    'language': 'ru'
                }
            }
        return self.data[user_id_str]
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application = Application.builder().token(self.bot_token).build()
        
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("finance", self.finance_command))
        self.application.add_handler(CommandHandler("app", self.app_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        
        # Обработка callback запросов
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Обработка сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        welcome_text = f"""
🎉 Привет, {user.first_name}!

Я ваш персональный финансовый помощник! 💰

📱 **Доступные функции:**
• /app - Открыть веб-приложение
• /finance - Быстрый учет финансов
• /stats - Статистика
• /balance - Текущий баланс
• /help - Помощь

Выберите действие:
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📱 Открыть приложение", web_app=WebAppInfo(url=self.webapp_url)),
                InlineKeyboardButton("💰 Финансы", callback_data="finance_menu")
            ],
            [
                InlineKeyboardButton("📊 Статистика", callback_data="show_stats"),
                InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
📖 **Справка по командам:**

🔹 **Основные команды:**
• /start - Главное меню
• /app - Открыть веб-приложение
• /finance - Быстрый учет финансов
• /stats - Показать статистику
• /balance - Текущий баланс

🔹 **Быстрые действия:**
• Напишите сумму с + для дохода: `+5000`
• Напишите сумму с - для расхода: `-1500`
• Добавьте описание: `+5000 зарплата`

🔹 **Примеры:**
• `+50000` - добавить доход 50000₽
• `-1500 еда` - добавить расход 1500₽ на еду
• `+100000 зарплата` - доход 100000₽ с описанием

💡 **Совет:** Используйте веб-приложение для более удобной работы!
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Открыть приложение", web_app=WebAppInfo(url=self.webapp_url))],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def app_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /app - открытие веб-приложения"""
        keyboard = [
            [InlineKeyboardButton("📱 Открыть Finance Tracker", web_app=WebAppInfo(url=self.webapp_url))],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🚀 **Finance Tracker App**\n\n"
            "Откройте полноценное веб-приложение для управления финансами:\n"
            "• 📊 Дашборд со статистикой\n"
            "• 💰 Управление транзакциями\n"
            "• 🎯 Финансовые цели\n"
            "• ⚙️ Настройки и персонализация\n\n"
            "Нажмите кнопку ниже, чтобы открыть приложение:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def finance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /finance"""
        await self.show_finance_menu(update, context)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /stats"""
        await self.show_statistics(update, context)
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /balance"""
        await self.show_balance(update, context)
    
    async def show_finance_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать меню финансов"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Доход", callback_data="add_income"),
                InlineKeyboardButton("➖ Расход", callback_data="add_expense")
            ],
            [
                InlineKeyboardButton("📊 Статистика", callback_data="show_stats"),
                InlineKeyboardButton("📋 История", callback_data="show_history")
            ],
            [
                InlineKeyboardButton("📱 Веб-приложение", web_app=WebAppInfo(url=self.webapp_url))
            ],
            [
                InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = "💰 **Управление финансами**\n\nВыберите действие:"
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def show_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику"""
        user_id = update.effective_user.id
        user_data = self.get_user_data(user_id)
        
        # Расчет статистики
        transactions = user_data.get('transactions', [])
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        balance = total_income - total_expenses
        
        # Топ категорий расходов
        expense_categories = {}
        for t in transactions:
            if t['type'] == 'expense':
                cat = t['category']
                expense_categories[cat] = expense_categories.get(cat, 0) + t['amount']
        
        top_expenses = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        stats_text = f"""
📊 **Статистика финансов**

💰 **Общий баланс:** {balance:,.0f}₽
📈 **Доходы:** {total_income:,.0f}₽
📉 **Расходы:** {total_expenses:,.0f}₽

📋 **Всего транзакций:** {len(transactions)}

🔝 **Топ расходов:**
"""
        
        for i, (category, amount) in enumerate(top_expenses, 1):
            category_name = self.get_category_name(category, 'expenses')
            stats_text += f"{i}. {category_name}: {amount:,.0f}₽\n"
        
        if not top_expenses:
            stats_text += "Нет данных о расходах\n"
        
        keyboard = [
            [InlineKeyboardButton("📱 Подробная статистика", web_app=WebAppInfo(url=self.webapp_url))],
            [InlineKeyboardButton("🔙 Назад", callback_data="finance_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def show_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать текущий баланс"""
        user_id = update.effective_user.id
        user_data = self.get_user_data(user_id)
        
        transactions = user_data.get('transactions', [])
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        balance = total_income - total_expenses
        
        balance_text = f"""
💰 **Текущий баланс**

💵 **Баланс:** {balance:,.0f}₽
📈 **Доходы:** {total_income:,.0f}₽
📉 **Расходы:** {total_expenses:,.0f}₽

{'🎉 Отличная работа!' if balance > 0 else '⚠️ Внимание к расходам!' if balance < 0 else '⚖️ Баланс сбалансирован!'}
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Детальная аналитика", web_app=WebAppInfo(url=self.webapp_url))],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            balance_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка callback запросов"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "main_menu":
            await self.start_command(update, context)
        elif query.data == "finance_menu":
            await self.show_finance_menu(update, context)
        elif query.data == "show_stats":
            await self.show_statistics(update, context)
        elif query.data == "add_income":
            await self.show_category_selection(update, context, "income")
        elif query.data == "add_expense":
            await self.show_category_selection(update, context, "expense")
        elif query.data.startswith("category_"):
            parts = query.data.split("_")
            if len(parts) >= 3:
                transaction_type = parts[1]
                category = parts[2]
                await self.request_amount(update, context, transaction_type, category)
        elif query.data == "settings":
            await self.show_settings(update, context)
    
    async def show_category_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, transaction_type: str):
        """Показать выбор категории"""
        categories = self.categories[transaction_type]
        
        keyboard = []
        row = []
        for name, code in categories.items():
            row.append(InlineKeyboardButton(name, callback_data=f"category_{transaction_type}_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="finance_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        type_text = "доход" if transaction_type == "income" else "расход"
        
        await update.callback_query.edit_message_text(
            f"Выберите категорию для {type_text}:",
            reply_markup=reply_markup
        )
    
    async def request_amount(self, update: Update, context: ContextTypes.DEFAULT_TYPE, transaction_type: str, category: str):
        """Запросить сумму транзакции"""
        context.user_data['pending_transaction'] = {
            'type': transaction_type,
            'category': category
        }
        
        type_text = "дохода" if transaction_type == "income" else "расхода"
        category_name = self.get_category_name(category, transaction_type)
        
        await update.callback_query.edit_message_text(
            f"💰 Введите сумму {type_text} для категории '{category_name}':\n\n"
            f"Примеры:\n"
            f"• 5000\n"
            f"• 5000 зарплата\n"
            f"• 1500.50 обед",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Отмена", callback_data="finance_menu")
            ]])
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        text = update.message.text.strip()
        user_id = update.effective_user.id
        
        # Проверяем, есть ли ожидающая транзакция
        if 'pending_transaction' in context.user_data:
            await self.process_transaction_input(update, context, text)
            return
        
        # Быстрый ввод транзакций
        if text.startswith('+') or text.startswith('-'):
            await self.process_quick_transaction(update, context, text)
            return
        
        # Обычные сообщения
        await update.message.reply_text(
            "💡 Используйте команды:\n"
            "• /start - главное меню\n"
            "• /app - открыть приложение\n"
            "• /finance - управление финансами\n"
            "• /help - справка\n\n"
            "Или введите сумму с + или - для быстрого добавления транзакции!"
        )
    
    async def process_transaction_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Обработка ввода транзакции"""
        try:
            parts = text.split(' ', 1)
            amount = float(parts[0])
            description = parts[1] if len(parts) > 1 else ""
            
            if amount <= 0:
                await update.message.reply_text("❌ Сумма должна быть больше 0!")
                return
            
            pending = context.user_data['pending_transaction']
            user_id = update.effective_user.id
            user_data = self.get_user_data(user_id)
            
            transaction = {
                'id': len(user_data['transactions']) + 1,
                'type': pending['type'],
                'category': pending['category'],
                'amount': amount,
                'description': description,
                'date': datetime.now().isoformat(),
                'timestamp': datetime.now().timestamp()
            }
            
            user_data['transactions'].append(transaction)
            self.save_data()
            
            type_text = "доход" if pending['type'] == 'income' else "расход"
            category_name = self.get_category_name(pending['category'], pending['type'])
            
            await update.message.reply_text(
                f"✅ {type_text.title()} добавлен!\n\n"
                f"💰 Сумма: {amount:,.0f}₽\n"
                f"📂 Категория: {category_name}\n"
                f"📝 Описание: {description or 'Не указано'}\n\n"
                f"Используйте /stats для просмотра статистики!"
            )
            
            del context.user_data['pending_transaction']
            
        except ValueError:
            await update.message.reply_text("❌ Неверный формат суммы! Введите число.")
        except Exception as e:
            await update.message.reply_text("❌ Ошибка при добавлении транзакции!")
            logger.error(f"Ошибка добавления транзакции: {e}")
    
    async def process_quick_transaction(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Обработка быстрой транзакции"""
        try:
            parts = text.split(' ', 1)
            amount_str = parts[0][1:]  # Убираем + или -
            amount = float(amount_str)
            description = parts[1] if len(parts) > 1 else ""
            
            if amount <= 0:
                await update.message.reply_text("❌ Сумма должна быть больше 0!")
                return
            
            transaction_type = 'income' if text.startswith('+') else 'expense'
            category = 'other'  # По умолчанию
            
            user_id = update.effective_user.id
            user_data = self.get_user_data(user_id)
            
            transaction = {
                'id': len(user_data['transactions']) + 1,
                'type': transaction_type,
                'category': category,
                'amount': amount,
                'description': description,
                'date': datetime.now().isoformat(),
                'timestamp': datetime.now().timestamp()
            }
            
            user_data['transactions'].append(transaction)
            self.save_data()
            
            type_text = "доход" if transaction_type == 'income' else "расход"
            
            await update.message.reply_text(
                f"✅ {type_text.title()} добавлен!\n\n"
                f"💰 Сумма: {amount:,.0f}₽\n"
                f"📝 Описание: {description or 'Не указано'}\n\n"
                f"💡 Для более детального учета используйте /finance или /app!"
            )
            
        except ValueError:
            await update.message.reply_text("❌ Неверный формат суммы! Пример: +5000 или -1500")
        except Exception as e:
            await update.message.reply_text("❌ Ошибка при добавлении транзакции!")
            logger.error(f"Ошибка быстрой транзакции: {e}")
    
    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать настройки"""
        keyboard = [
            [InlineKeyboardButton("📱 Открыть приложение", web_app=WebAppInfo(url=self.webapp_url))],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            "⚙️ **Настройки**\n\n"
            "Для изменения настроек используйте веб-приложение:\n"
            "• 💱 Валюта\n"
            "• 🎨 Тема оформления\n"
            "• 🔔 Уведомления\n"
            "• 🌍 Язык",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def get_category_name(self, category_code: str, transaction_type: str) -> str:
        """Получить название категории по коду"""
        categories = self.categories[transaction_type]
        for name, code in categories.items():
            if code == category_code:
                return name
        return category_code
    
    async def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск простого Finance Bot")
        await self.application.run_polling()

def main():
    """Главная функция"""
    bot = SimpleFinanceBot()
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()
