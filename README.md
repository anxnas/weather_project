# Weather Report Application

Это приложение для отображения прогноза погоды, созданное с использованием Django и Docker. Приложение позволяет пользователям вводить название города и получать текущую информацию о погоде. Также сохраняется история последних 15 запросов в куки.

## Используемые технологии

- **Django**: Веб-фреймворк для создания веб-приложений на Python.
- **Docker**: Платформа для разработки, доставки и запуска приложений в контейнерах.
- **Bootstrap**: CSS-фреймворк для создания адаптивных и стильных интерфейсов.

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/anxnas/weather_project.git
cd weather-report
```

### 2. Создание и активация виртуального окружения (опционально)

**Для Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```
**Для Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Создание и запуск Docker контейнеров

#### Сборка и запуск контейнеров
```bash
docker-compose up --build
```

### 5. Доступ к приложению

Откройте браузер и перейдите по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Тестирование

Для запуска тестов используйте следующую команду:
```bash
python manage.py test weather_report
```

## Заключение

Это приложение демонстрирует использование Django для отображения погоды в веб-приложений.

## Лицензия

Этот проект лицензируется на условиях лицензии MIT. Подробности см. в файле LICENSE.
