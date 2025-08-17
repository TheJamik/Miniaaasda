#!/usr/bin/env python3
"""
Автоматическое развертывание на Railway
"""

import os
import subprocess
import webbrowser
import time

def check_git():
    """Проверить, установлен ли Git"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git установлен: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ Git не найден")
        return False

def init_git_repo():
    """Инициализировать Git репозиторий"""
    try:
        # Проверяем, есть ли уже Git репозиторий
        if os.path.exists('.git'):
            print("✅ Git репозиторий уже инициализирован")
            return True
        
        print("📁 Инициализация Git репозитория...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git репозиторий создан")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка инициализации Git: {e}")
        return False

def create_github_repo():
    """Создать репозиторий на GitHub"""
    print("\n🌐 Создание репозитория на GitHub...")
    print("📋 Следуйте инструкциям:")
    print("1. Откройте https://github.com")
    print("2. Нажмите 'New repository'")
    print("3. Введите название: telegram-finance-app")
    print("4. Выберите 'Public'")
    print("5. НЕ ставьте галочки на README, .gitignore, license")
    print("6. Нажмите 'Create repository'")
    
    # Открываем GitHub в браузере
    webbrowser.open('https://github.com/new')
    
    input("\n⏳ После создания репозитория нажмите Enter...")
    return True

def push_to_github():
    """Загрузить код на GitHub"""
    print("\n📤 Загрузка кода на GitHub...")
    
    # Запрашиваем URL репозитория
    repo_url = input("🔗 Введите URL вашего GitHub репозитория (например, https://github.com/username/telegram-finance-app): ")
    
    try:
        # Добавляем remote и пушим
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ Код загружен на GitHub")
        return repo_url
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка загрузки на GitHub: {e}")
        return None

def deploy_to_railway(repo_url):
    """Развернуть на Railway"""
    print("\n🚀 Развертывание на Railway...")
    print("📋 Следуйте инструкциям:")
    print("1. Откройте https://railway.app")
    print("2. Нажмите 'New Project'")
    print("3. Выберите 'Deploy from GitHub repo'")
    print(f"4. Найдите ваш репозиторий: {repo_url}")
    print("5. Нажмите 'Deploy Now'")
    print("6. Дождитесь завершения развертывания")
    
    # Открываем Railway в браузере
    webbrowser.open('https://railway.app/new')
    
    input("\n⏳ После развертывания нажмите Enter...")
    return True

def get_railway_url():
    """Получить URL приложения на Railway"""
    print("\n🌐 Получение URL приложения...")
    railway_url = input("🔗 Введите URL вашего приложения на Railway (например, https://your-app.railway.app): ")
    return railway_url

def update_bot_url(railway_url):
    """Обновить URL в боте"""
    print(f"\n🤖 Обновление URL в боте: {railway_url}")
    
    # Читаем файл simple_bot.py
    with open('simple_bot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем URL
    old_url = 'http://localhost:3000'
    new_content = content.replace(old_url, railway_url)
    
    # Записываем обратно
    with open('simple_bot.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ URL в боте обновлен")

def setup_botfather():
    """Настройка BotFather"""
    print("\n📱 Настройка BotFather...")
    print("📋 Следуйте инструкциям:")
    print("1. Откройте @BotFather в Telegram")
    print("2. Отправьте /newapp")
    print("3. Выберите вашего бота")
    print("4. Введите название: Finance Tracker")
    print("5. Введите описание: Финансовый трекер для учета доходов и расходов")
    print("6. Загрузите иконку (16x16, 32x32, 128x128)")
    print("7. Введите URL вашего приложения")
    
    input("\n⏳ После настройки BotFather нажмите Enter...")

def main():
    """Главная функция"""
    print("🚀 Автоматическое развертывание Telegram App на Railway")
    print("=" * 60)
    
    # Проверяем Git
    if not check_git():
        print("❌ Установите Git с https://git-scm.com/")
        return
    
    # Инициализируем Git репозиторий
    if not init_git_repo():
        return
    
    # Создаем репозиторий на GitHub
    if not create_github_repo():
        return
    
    # Загружаем код на GitHub
    repo_url = push_to_github()
    if not repo_url:
        return
    
    # Развертываем на Railway
    if not deploy_to_railway(repo_url):
        return
    
    # Получаем URL приложения
    railway_url = get_railway_url()
    if not railway_url:
        return
    
    # Обновляем URL в боте
    update_bot_url(railway_url)
    
    # Настраиваем BotFather
    setup_botfather()
    
    print("\n" + "=" * 60)
    print("🎉 Развертывание завершено!")
    print(f"🌐 URL приложения: {railway_url}")
    print("\n📋 Что делать дальше:")
    print("1. Запустите бота: python simple_bot.py")
    print("2. Откройте бота в Telegram")
    print("3. Отправьте /start")
    print("4. Нажмите '📱 Открыть приложение'")
    print("5. Наслаждайтесь вашим Telegram App! 🎉")

if __name__ == "__main__":
    main()
