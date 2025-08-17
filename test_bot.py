#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности бота
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Тест импорта модулей"""
    print("🔍 Тестирование импортов...")
    
    try:
        from modules.finance_tracker import FinanceTracker
        print("✅ Модуль finance_tracker импортирован успешно")
    except ImportError as e:
        print(f"❌ Ошибка импорта finance_tracker: {e}")
        return False
    
    try:
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
        print("✅ Telegram библиотеки импортированы успешно")
    except ImportError as e:
        print(f"❌ Ошибка импорта telegram: {e}")
        return False
    
    return True

def test_config():
    """Тест конфигурации"""
    print("\n🔍 Тестирование конфигурации...")
    
    load_dotenv()
    
    token = os.getenv('BOT_TOKEN')
    if not token or token == 'your_bot_token_here':
        print("❌ BOT_TOKEN не настроен в .env файле")
        print("💡 Создайте файл .env и добавьте ваш токен")
        return False
    
    print("✅ BOT_TOKEN найден")
    return True

def test_finance_tracker():
    """Тест финансового трекера"""
    print("\n🔍 Тестирование финансового трекера...")
    
    try:
        from modules.finance_tracker import FinanceTracker
        
        tracker = FinanceTracker()
        print("✅ Финансовый трекер инициализирован")
        
        # Тест категорий
        if tracker.categories['expenses'] and tracker.categories['income']:
            print(f"✅ Категории загружены: {len(tracker.categories['expenses'])} расходов, {len(tracker.categories['income'])} доходов")
        else:
            print("❌ Категории не загружены")
            return False
        
        # Тест данных
        test_user_id = 12345
        user_data = tracker.get_user_data(test_user_id)
        if user_data:
            print("✅ Данные пользователя созданы")
        else:
            print("❌ Ошибка создания данных пользователя")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования финансового трекера: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 Тестирование финансового трекера Telegram бота")
    print("=" * 50)
    
    # Тест импортов
    if not test_imports():
        print("\n❌ Тест импортов не пройден")
        sys.exit(1)
    
    # Тест конфигурации
    if not test_config():
        print("\n❌ Тест конфигурации не пройден")
        print("💡 Смотрите QUICK_START.md для настройки")
        sys.exit(1)
    
    # Тест финансового трекера
    if not test_finance_tracker():
        print("\n❌ Тест финансового трекера не пройден")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Все тесты пройдены успешно!")
    print("✅ Бот готов к запуску")
    print("\n💡 Для запуска выполните: python main.py")
    print("📖 Подробности в README.md")

if __name__ == "__main__":
    main()
