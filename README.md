# TezRamen Bot

Telegram-бот на aiogram 3 с двумя разделами:

- **Отзывы / Комментарии / Предложения** — оценка 1–5 ⭐ + текст
- **Заявки на партнёрство** — имя + телефон + текст

Интерфейс на трёх языках: русский, английский, узбекский. Все обращения пересылаются в указанную группу/канал.

## Переменные окружения

| Переменная | Описание |
|---|---|
| `BOT_TOKEN` | Токен бота от [@BotFather](https://t.me/BotFather) |
| `GROUP_CHAT_ID` | ID группы/канала, куда летят обращения (напр. `-1001234567890`) |

## Как узнать GROUP_CHAT_ID

1. Создай группу (или канал) и добавь туда своего бота.
2. Для группы — дай боту право читать сообщения (или сделай админом, для каналов — обязательно админом).
3. Напиши любое сообщение в группе.
4. Открой в браузере: `https://api.telegram.org/bot<ТОКЕН>/getUpdates`
5. Найди `"chat":{"id":-100...}` — это и есть `GROUP_CHAT_ID`.

> Совет: можно добавить в группу бота `@getmyid_bot` или `@username_to_id_bot`, он сразу покажет ID.

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env   # заполни BOT_TOKEN и GROUP_CHAT_ID
export $(cat .env | xargs)   # или задай переменные вручную
python bot.py
```

## Деплой на Render (бесплатно)

Бот работает на long-polling, поэтому на Render нужен **Background Worker**, а не Web Service.

1. Залей этот репозиторий на GitHub.
2. На [render.com](https://render.com) → **New +** → **Background Worker**.
3. Подключи свой GitHub-репозиторий.
4. Настройки:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** Free
5. В разделе **Environment** добавь переменные `BOT_TOKEN` и `GROUP_CHAT_ID`.
6. **Create Background Worker** — деплой пойдёт автоматически.

Либо через `render.yaml`: **New +** → **Blueprint** → выбрать репозиторий (переменные всё равно нужно задать вручную).

## Команды бота

- `/start` — приветствие и выбор языка
- `/cancel` — отменить текущее действие и вернуться в меню
