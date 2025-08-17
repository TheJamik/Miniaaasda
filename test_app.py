#!/usr/bin/env python3
"""
Тестовый скрипт для проверки веб-приложения Finance Tracker
"""

import requests
import json
import time

def test_app():
    """Тестирование веб-приложения"""
    base_url = "http://localhost:8080"
    
    print("🧪 Тестирование Finance Tracker Web App")
    print("=" * 50)
    
    # Тест 1: Проверка здоровья приложения
    print("1. Проверка здоровья приложения...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Приложение работает! Статус: {data['status']}")
            print(f"   Версия: {data['version']}")
            print(f"   Время: {data['timestamp']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    # Тест 2: Проверка главной страницы
    print("\n2. Проверка главной страницы...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Главная страница загружается")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 3: Проверка API категорий
    print("\n3. Проверка API категорий...")
    try:
        response = requests.get(f"{base_url}/api/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Категории загружены:")
            print(f"   Расходы: {len(categories.get('expenses', {}))} категорий")
            print(f"   Доходы: {len(categories.get('income', {}))} категорий")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 4: Проверка API пользователя
    print("\n4. Проверка API пользователя...")
    test_user_id = "test_user_123"
    try:
        response = requests.get(f"{base_url}/api/user/{test_user_id}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Данные пользователя загружены:")
            print(f"   Транзакций: {len(user_data.get('transactions', []))}")
            print(f"   Валюта: {user_data.get('currency', 'N/A')}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 5: Проверка статистики
    print("\n5. Проверка API статистики...")
    try:
        response = requests.get(f"{base_url}/api/statistics/{test_user_id}")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Статистика загружена:")
            print(f"   Доходы: {stats.get('total_income', 0)}")
            print(f"   Расходы: {stats.get('total_expenses', 0)}")
            print(f"   Баланс: {stats.get('balance', 0)}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 6: Добавление тестовой транзакции
    print("\n6. Тест добавления транзакции...")
    test_transaction = {
        "user_id": test_user_id,
        "type": "income",
        "category": "salary",
        "amount": 50000.0,
        "description": "Тестовая зарплата"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/transaction",
            json=test_transaction,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Транзакция добавлена:")
            print(f"   ID: {result.get('transaction', {}).get('id', 'N/A')}")
            print(f"   Сумма: {result.get('transaction', {}).get('amount', 'N/A')}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print(f"💡 Откройте браузер и перейдите по адресу: {base_url}")
    print("📖 Подробности в README_APP.md")

if __name__ == "__main__":
    test_app()
