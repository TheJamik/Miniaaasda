# 🚀 **Ручное развертывание Telegram App на Railway**

## 📋 **Пошаговая инструкция:**

### **Шаг 1: Установите Git**
1. Скачайте Git с https://git-scm.com/
2. Установите с настройками по умолчанию
3. Перезапустите PowerShell

### **Шаг 2: Создайте GitHub репозиторий**
1. Откройте https://github.com
2. Нажмите "New repository"
3. Введите название: `telegram-finance-app`
4. Выберите "Public"
5. НЕ ставьте галочки на README, .gitignore, license
6. Нажмите "Create repository"

### **Шаг 3: Загрузите файлы на GitHub**
В PowerShell выполните:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-finance-app.git
git push -u origin main
```

### **Шаг 4: Разверните на Railway**
1. Откройте https://railway.app
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Найдите ваш репозиторий
5. Нажмите "Deploy Now"
6. Дождитесь завершения развертывания

### **Шаг 5: Получите URL**
После развертывания Railway даст вам URL вида:
`https://your-app-name.railway.app`

### **Шаг 6: Настройте BotFather**
1. Откройте @BotFather в Telegram
2. Отправьте `/newapp`
3. Выберите вашего бота
4. Введите название: `Finance Tracker`
5. Введите описание: `Финансовый трекер для учета доходов и расходов`
6. Загрузите иконку (16x16, 32x32, 128x128)
7. Введите URL из Railway

### **Шаг 7: Обновите бота**
В файле `simple_bot.py` замените:
```python
self.webapp_url = "https://your-app-name.railway.app"  # Ваш URL
```

### **Шаг 8: Запустите бота**
```bash
python simple_bot.py
```

## 🎉 **Готово!**

Теперь когда пользователь нажмет `/start`, он увидит кнопку "📱 Открыть приложение" и сможет открыть веб-приложение прямо в Telegram!

## 📁 **Необходимые файлы:**
- ✅ `telegram_app.py`
- ✅ `simple_bot.py`
- ✅ `requirements.txt`
- ✅ `templates/telegram_app.html`
- ✅ `static/` папка
- ✅ `railway.json`
- ✅ `README.md`

## ⚠️ **Важно:**
- Telegram App требует HTTPS URL
- localhost не поддерживается
- Railway дает бесплатный HTTPS URL
- URL постоянный и не меняется
