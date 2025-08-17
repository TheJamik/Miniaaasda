#!/usr/bin/env python3
"""
Telegram App - Полноценное веб-приложение для Telegram
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FinanceApp:
    def __init__(self):
        self.app = FastAPI(
            title="Finance Tracker App",
            description="Полноценное приложение для учета финансов",
            version="1.0.0"
        )
        
        # Настройка CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Подключаем статические файлы
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Настройка шаблонов
        self.templates = Jinja2Templates(directory="templates")
        
        # Данные приложения
        self.data_file = "app_data.json"
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
        self.setup_routes()
    
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
    
    def get_user_data(self, user_id: str) -> Dict:
        """Получить данные пользователя"""
        if user_id not in self.data:
            self.data[user_id] = {
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
        return self.data[user_id]
    
    def setup_routes(self):
        """Настройка маршрутов приложения"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Главная страница приложения"""
            return self.templates.TemplateResponse("index.html", {
                "request": request,
                "title": "Finance Tracker App"
            })
        
        @self.app.get("/app", response_class=HTMLResponse)
        async def app_main(request: Request):
            """Основное приложение"""
            return self.templates.TemplateResponse("app.html", {
                "request": request,
                "title": "Finance Tracker",
                "categories": self.categories
            })
        
        @self.app.get("/api/user/{user_id}")
        async def get_user_data(user_id: str):
            """Получить данные пользователя"""
            user_data = self.get_user_data(user_id)
            return JSONResponse(content=user_data)
        
        @self.app.post("/api/transaction")
        async def add_transaction(request: Request):
            """Добавить транзакцию"""
            try:
                data = await request.json()
                user_id = data.get('user_id')
                transaction_type = data.get('type')
                category = data.get('category')
                amount = float(data.get('amount', 0))
                description = data.get('description', '')
                
                if not all([user_id, transaction_type, category, amount > 0]):
                    raise HTTPException(status_code=400, detail="Неверные данные")
                
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
                
                return JSONResponse(content={
                    "success": True,
                    "transaction": transaction,
                    "message": "Транзакция добавлена"
                })
                
            except Exception as e:
                logger.error(f"Ошибка добавления транзакции: {e}")
                raise HTTPException(status_code=500, detail="Ошибка сервера")
        
        @self.app.get("/api/statistics/{user_id}")
        async def get_statistics(user_id: str, period: str = "month"):
            """Получить статистику"""
            try:
                user_data = self.get_user_data(user_id)
                
                # Фильтрация по периоду
                now = datetime.now()
                if period == "week":
                    start_date = now.replace(day=now.day - 7)
                elif period == "month":
                    start_date = now.replace(day=1)
                elif period == "year":
                    start_date = now.replace(month=1, day=1)
                else:
                    start_date = now.replace(day=1)
                
                filtered_transactions = [
                    t for t in user_data['transactions']
                    if datetime.fromtimestamp(t['timestamp']) >= start_date
                ]
                
                total_income = sum(t['amount'] for t in filtered_transactions if t['type'] == 'income')
                total_expenses = sum(t['amount'] for t in filtered_transactions if t['type'] == 'expense')
                balance = total_income - total_expenses
                
                # Топ категорий расходов
                expense_categories = {}
                for t in filtered_transactions:
                    if t['type'] == 'expense':
                        cat = t['category']
                        expense_categories[cat] = expense_categories.get(cat, 0) + t['amount']
                
                top_expenses = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)[:5]
                
                return JSONResponse(content={
                    "period": period,
                    "total_income": total_income,
                    "total_expenses": total_expenses,
                    "balance": balance,
                    "top_expenses": top_expenses,
                    "currency": user_data['currency']
                })
                
            except Exception as e:
                logger.error(f"Ошибка получения статистики: {e}")
                raise HTTPException(status_code=500, detail="Ошибка сервера")
        
        @self.app.post("/api/goal")
        async def add_goal(request: Request):
            """Добавить финансовую цель"""
            try:
                data = await request.json()
                user_id = data.get('user_id')
                name = data.get('name')
                target = float(data.get('target', 0))
                deadline = data.get('deadline')
                
                if not all([user_id, name, target > 0]):
                    raise HTTPException(status_code=400, detail="Неверные данные")
                
                user_data = self.get_user_data(user_id)
                
                goal = {
                    'id': len(user_data.get('goals', [])) + 1,
                    'name': name,
                    'target': target,
                    'saved': 0,
                    'deadline': deadline,
                    'created_at': datetime.now().isoformat()
                }
                
                if 'goals' not in user_data:
                    user_data['goals'] = []
                
                user_data['goals'].append(goal)
                self.save_data()
                
                return JSONResponse(content={
                    "success": True,
                    "goal": goal,
                    "message": "Цель добавлена"
                })
                
            except Exception as e:
                logger.error(f"Ошибка добавления цели: {e}")
                raise HTTPException(status_code=500, detail="Ошибка сервера")
        
        @self.app.post("/api/budget")
        async def add_budget(request: Request):
            """Добавить бюджет"""
            try:
                data = await request.json()
                user_id = data.get('user_id')
                category = data.get('category')
                amount = float(data.get('amount', 0))
                
                if not all([user_id, category, amount > 0]):
                    raise HTTPException(status_code=400, detail="Неверные данные")
                
                user_data = self.get_user_data(user_id)
                
                if 'budgets' not in user_data:
                    user_data['budgets'] = {}
                
                user_data['budgets'][category] = {
                    'amount': amount,
                    'created_at': datetime.now().isoformat()
                }
                
                self.save_data()
                
                return JSONResponse(content={
                    "success": True,
                    "budget": user_data['budgets'][category],
                    "message": "Бюджет добавлен"
                })
                
            except Exception as e:
                logger.error(f"Ошибка добавления бюджета: {e}")
                raise HTTPException(status_code=500, detail="Ошибка сервера")
        
        @self.app.get("/api/categories")
        async def get_categories():
            """Получить категории"""
            return JSONResponse(content=self.categories)
        
        @self.app.get("/health")
        async def health_check():
            """Проверка здоровья приложения"""
            return JSONResponse(content={
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            })
    
    def run(self, host: str = "0.0.0.0", port: int = 8080):
        """Запуск приложения"""
        logger.info(f"🚀 Запуск Finance Tracker App на {host}:{port}")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )

def main():
    """Главная функция"""
    app = FinanceApp()
    app.run()

if __name__ == "__main__":
    main()
