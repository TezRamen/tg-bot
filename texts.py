# -*- coding: utf-8 -*-
"""Тексты бота на трёх языках: русский, английский, узбекский."""

# Приветствие показывается сразу на трёх языках (до выбора языка)
WELCOME = (
    "🍜 <b>Вас приветствует TezRamen бот!</b>\n"
    "Пожалуйста, выберите язык.\n\n"
    "🍜 <b>Welcome to the TezRamen bot!</b>\n"
    "Please choose your language.\n\n"
    "🍜 <b>TezRamen botiga xush kelibsiz!</b>\n"
    "Iltimos, tilni tanlang."
)

# Названия языков на кнопках
LANG_BUTTONS = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 O'zbekcha",
}

TEXTS = {
    "ru": {
        "menu_title": "Выберите, что вас интересует:",
        "btn_review": "💬 Отзывы / Комментарии / Предложения",
        "btn_partner": "🤝 Заявки на партнёрство",
        "btn_back": "⬅️ Назад",
        "btn_change_lang": "🌐 Сменить язык",
        # Отзывы
        "review_ask_machine": "Выберите автомат, которым вы воспользовались:",
        "review_ask_rating": "Пожалуйста, оцените нас от 1 до 5:",
        "review_ask_text": "Спасибо за оценку! Теперь напишите ваш отзыв, комментарий или предложение:",
        "review_ask_phone": "И последнее — поделитесь номером телефона (можно нажать кнопку ниже):",
        "review_done": "Спасибо за ваш отзыв! 🙏 Мы обязательно его учтём.",
        # Партнёрство
        "partner_ask_name": "Отлично! Как вас зовут?",
        "partner_ask_phone": "Укажите ваш номер телефона (можно нажать кнопку ниже):",
        "partner_btn_share_phone": "📱 Отправить мой номер",
        "partner_ask_text": "Кратко опишите ваше предложение о партнёрстве:",
        "partner_done": "Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время. 🤝",
        "cancelled": "Действие отменено. Возвращаю в меню.",
    },
    "en": {
        "menu_title": "Please choose what you are interested in:",
        "btn_review": "💬 Reviews / Comments / Suggestions",
        "btn_partner": "🤝 Partnership requests",
        "btn_back": "⬅️ Back",
        "btn_change_lang": "🌐 Change language",
        "review_ask_machine": "Choose the machine you used:",
        "review_ask_rating": "Please rate us from 1 to 5:",
        "review_ask_text": "Thanks for the rating! Now please write your review, comment or suggestion:",
        "review_ask_phone": "One last thing — please share your phone number (you can tap the button below):",
        "review_done": "Thank you for your feedback! 🙏 We really appreciate it.",
        "partner_ask_name": "Great! What is your name?",
        "partner_ask_phone": "Please share your phone number (you can tap the button below):",
        "partner_btn_share_phone": "📱 Share my number",
        "partner_ask_text": "Please briefly describe your partnership proposal:",
        "partner_done": "Thank you! Your request has been received. We will contact you soon. 🤝",
        "cancelled": "Action cancelled. Returning to the menu.",
    },
    "uz": {
        "menu_title": "Sizni nima qiziqtirayotganini tanlang:",
        "btn_review": "💬 Sharhlar / Izohlar / Takliflar",
        "btn_partner": "🤝 Hamkorlik uchun arizalar",
        "btn_back": "⬅️ Orqaga",
        "btn_change_lang": "🌐 Tilni o'zgartirish",
        "review_ask_machine": "Foydalangan avtomatingizni tanlang:",
        "review_ask_rating": "Iltimos, bizni 1 dan 5 gacha baholang:",
        "review_ask_text": "Baho uchun rahmat! Endi sharhingiz, izohingiz yoki taklifingizni yozing:",
        "review_ask_phone": "Va oxirgisi — telefon raqamingizni yuboring (quyidagi tugmani bosishingiz mumkin):",
        "review_done": "Sharhingiz uchun rahmat! 🙏 Biz uni albatta hisobga olamiz.",
        "partner_ask_name": "Ajoyib! Ismingiz nima?",
        "partner_ask_phone": "Telefon raqamingizni yuboring (quyidagi tugmani bosishingiz mumkin):",
        "partner_btn_share_phone": "📱 Raqamimni yuborish",
        "partner_ask_text": "Hamkorlik taklifingizni qisqacha tavsiflang:",
        "partner_done": "Rahmat! Arizangiz qabul qilindi. Tez orada siz bilan bog'lanamiz. 🤝",
        "cancelled": "Amal bekor qilindi. Menyuga qaytamiz.",
    },
}

# --------------------------------------------------------------------------- #
# Список автоматов Tez Ramen.
# ВРЕМЕННЫЙ список-пример — позже замени на реальные локации.
# Чтобы добавить/убрать автомат, просто правь этот список.
#   id  — внутренний код (латиницей, без пробелов), менять не обязательно
#   ru/uz/en — подпись на кнопке на каждом языке
# --------------------------------------------------------------------------- #
MACHINES = [
    {"id": "seul_mun",       "ru": "Сеул-Мун",        "uz": "Seul-Mun",        "en": "Seul-Mun"},
    {"id": "skver_timura",   "ru": "Сквер А.Тимура",  "uz": "Skver A.Timur",   "en": "A.Timur Square"},
    {"id": "m_kosmonavtov",  "ru": "М.Космонавтов",   "uz": "M.Kosmonavtov",   "en": "Kosmonavtov metro"},
    {"id": "severny_vokzal", "ru": "Северный вокзал", "uz": "Severniy vokzal", "en": "Northern station"},
    {"id": "shevchenko",     "ru": "Шевченко",        "uz": "Shevchenko",      "en": "Shevchenko str"},
]

# Кнопка «Другой / не указан» на случай, если автомата нет в списке
MACHINE_OTHER = {
    "id": "other",
    "ru": "Другой / не указан",
    "uz": "Boshqa / ko'rsatilmagan",
    "en": "Other / not specified",
}


def machine_label(machine_id: str, lang: str) -> str:
    """Подпись автомата на нужном языке по его id (с откатом на русский)."""
    for m in MACHINES + [MACHINE_OTHER]:
        if m["id"] == machine_id:
            return m.get(lang) or m["ru"]
    return machine_id


# Подписи разделов для уведомления в группу (на русском, для админов)
SECTION_LABELS = {
    "ru": "Русский",
    "en": "English",
    "uz": "O'zbekcha",
}


def t(lang: str, key: str) -> str:
    """Достаёт текст по языку и ключу, с откатом на русский."""
    return TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
