# Django Articles  

Django Articles — это веб-приложение для публикации статей о известных людях.  
Проект включает аутентификацию, управление записями и авторизацию через GitHub.  

## Описание функциональности  
- Регистрация и аутентификация пользователей (включая OAuth через GitHub)  
- CRUD-операции для постов (создание, редактирование, удаление)  
- Панель администратора Django  
- Разделение пользователей на группы с разными уровнями доступа  

## Используемые технологии  
- **Backend:** Django, Python  
- **Database:** PostgreSQL  
- **Frontend:** HTML, CSS  
- **Аутентификация:** OAuth 2.0 (GitHub)  
- **Кэширование:** Redis  
- **Тестирование:** Django Unittest  
- **Деплой:** Nginx, Gunicorn, Ubuntu  

## Установка и запуск  

### 1. Клонирование репозитория  
```sh
git clone https://github.com/pav046/my_django
cd my_django
```

### 2. Установка зависимостей
```sh
python -m venv venv  
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Применение миграций и запуск сервера
```sh
python manage.py migrate  
python manage.py runserver  
```
