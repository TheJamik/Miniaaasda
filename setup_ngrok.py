#!/usr/bin/env python3
"""
Скрипт для настройки ngrok туннеля для Telegram App
"""

import subprocess
import sys
import os
import time
import requests

def check_ngrok():
    """Проверить, установлен ли ngrok"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok уже установлен")
            return True
    except FileNotFoundError:
        print("❌ ngrok не найден")
        return False

def install_ngrok():
    """Установить ngrok"""
    print("📥 Установка ngrok...")
    
    # Скачать ngrok для Windows
    ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    
    try:
        # Скачиваем ngrok
        print("Скачиваем ngrok...")
        response = requests.get(ngrok_url)
        
        with open("ngrok.zip", "wb") as f:
            f.write(response.content)
        
        # Распаковываем
        import zipfile
        with zipfile.ZipFile("ngrok.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Удаляем zip файл
        os.remove("ngrok.zip")
        
        print("✅ ngrok установлен")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка установки ngrok: {e}")
        return False

def start_ngrok_tunnel(port=3000):
    """Запустить ngrok туннель"""
    print(f"🚀 Запуск ngrok туннеля для порта {port}...")
    
    try:
        # Запускаем ngrok в фоновом режиме
        process = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем немного для запуска
        time.sleep(3)
        
        # Получаем URL туннеля
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()['tunnels']
            
            if tunnels:
                public_url = tunnels[0]['public_url']
                print(f"✅ Ngrok туннель запущен!")
                print(f"🌐 Публичный URL: {public_url}")
                print(f"📱 Используйте этот URL в BotFather для Telegram App")
                return public_url
            else:
                print("❌ Не удалось получить URL туннеля")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка получения URL туннеля: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запуска ngrok: {e}")
        return None

def main():
    """Главная функция"""
    print("🚀 Настройка ngrok для Telegram App")
    print("=" * 50)
    
    # Проверяем ngrok
    if not check_ngrok():
        if not install_ngrok():
            print("❌ Не удалось установить ngrok")
            return
    
    # Запускаем туннель
    public_url = start_ngrok_tunnel(3000)
    
    if public_url:
        print("\n" + "=" * 50)
        print("🎉 Настройка завершена!")
        print(f"📱 Используйте URL: {public_url}")
        print("\n📋 Следующие шаги:")
        print("1. Откройте @BotFather в Telegram")
        print("2. Отправьте /newapp")
        print("3. Выберите вашего бота")
        print(f"4. Введите URL: {public_url}")
        print("5. Загрузите иконку и описание")
        print("\n⚠️  Внимание: ngrok URL меняется при каждом перезапуске!")
    else:
        print("❌ Не удалось настроить ngrok туннель")

if __name__ == "__main__":
    main()
