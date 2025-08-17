#!/usr/bin/env python3
"""
Быстрое развертывание Telegram App на Vercel
"""

import os
import subprocess
import sys

def check_node():
    """Проверить, установлен ли Node.js"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js установлен: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("❌ Node.js не найден")
        return False

def install_vercel():
    """Установить Vercel CLI"""
    try:
        print("📥 Установка Vercel CLI...")
        subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
        print("✅ Vercel CLI установлен")
        return True
    except subprocess.CalledProcessError:
        print("❌ Ошибка установки Vercel CLI")
        return False

def deploy_to_vercel():
    """Развернуть на Vercel"""
    try:
        print("🚀 Развертывание на Vercel...")
        print("📋 Следуйте инструкциям в браузере...")
        
        # Запускаем vercel
        subprocess.run(['vercel', '--prod'], check=True)
        
        print("✅ Развертывание завершено!")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Ошибка развертывания")
        return False

def create_vercel_config():
    """Создать конфигурацию Vercel"""
    config = '''{
  "version": 2,
  "builds": [
    {
      "src": "telegram_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "telegram_app.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}'''
    
    with open('vercel.json', 'w') as f:
        f.write(config)
    
    print("✅ Создан vercel.json")

def main():
    """Главная функция"""
    print("🚀 Быстрое развертывание Telegram App")
    print("=" * 50)
    
    # Проверяем Node.js
    if not check_node():
        print("❌ Установите Node.js с https://nodejs.org/")
        return
    
    # Создаем конфигурацию
    create_vercel_config()
    
    # Устанавливаем Vercel CLI
    if not install_vercel():
        print("❌ Не удалось установить Vercel CLI")
        return
    
    # Развертываем
    if deploy_to_vercel():
        print("\n" + "=" * 50)
        print("🎉 Развертывание завершено!")
        print("\n📋 Следующие шаги:")
        print("1. Скопируйте URL из браузера")
        print("2. Откройте @BotFather в Telegram")
        print("3. Отправьте /newapp")
        print("4. Выберите вашего бота")
        print("5. Введите скопированный URL")
        print("6. Загрузите иконку и описание")
    else:
        print("❌ Не удалось развернуть приложение")

if __name__ == "__main__":
    main()
