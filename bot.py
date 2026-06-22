# -*- coding: utf-8 -*-
"""
TezRamen бот.

Разделы:
  1) Отзывы / Комментарии / Предложения — оценка (1–5) + текст
  2) Заявки на партнёрство — имя + телефон + текст

Все обращения отправляются в группу/канал (GROUP_CHAT_ID).
Язык интерфейса: русский / английский / узбекский.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from texts import (
    LANG_BUTTONS,
    MACHINE_OTHER,
    MACHINES,
    SECTION_LABELS,
    WELCOME,
    machine_label,
    t,
)

# --------------------------------------------------------------------------- #
# Конфигурация (из переменных окружения)
# --------------------------------------------------------------------------- #
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "").strip()  # напр. -1001234567890

if not BOT_TOKEN:
    raise RuntimeError("Не задана переменная окружения BOT_TOKEN")
if not GROUP_CHAT_ID:
    raise RuntimeError("Не задана переменная окружения GROUP_CHAT_ID")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("tezramen-bot")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


# --------------------------------------------------------------------------- #
# Состояния (FSM)
# --------------------------------------------------------------------------- #
class ReviewForm(StatesGroup):
    machine = State()
    rating = State()
    text = State()


class PartnerForm(StatesGroup):
    name = State()
    phone = State()
    text = State()


# --------------------------------------------------------------------------- #
# Клавиатуры
# --------------------------------------------------------------------------- #
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=LANG_BUTTONS["ru"], callback_data="lang:ru")],
            [InlineKeyboardButton(text=LANG_BUTTONS["en"], callback_data="lang:en")],
            [InlineKeyboardButton(text=LANG_BUTTONS["uz"], callback_data="lang:uz")],
        ]
    )


def menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_review"), callback_data="sec:review")],
            [InlineKeyboardButton(text=t(lang, "btn_partner"), callback_data="sec:partner")],
            [InlineKeyboardButton(text=t(lang, "btn_change_lang"), callback_data="change_lang")],
        ]
    )


def machine_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=m[lang], callback_data=f"rmach:{m['id']}")]
        for m in MACHINES
    ]
    rows.append(
        [InlineKeyboardButton(text=MACHINE_OTHER[lang], callback_data=f"rmach:{MACHINE_OTHER['id']}")]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def rating_keyboard() -> InlineKeyboardMarkup:
    row = [
        InlineKeyboardButton(text=f"{n} ⭐", callback_data=f"rate:{n}")
        for n in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[row])


def phone_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "partner_btn_share_phone"), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# --------------------------------------------------------------------------- #
# Вспомогательное
# --------------------------------------------------------------------------- #
async def get_lang(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("lang", "ru")


def user_link(message_or_query) -> str:
    user = message_or_query.from_user
    name = user.full_name or "—"
    if user.username:
        return f'<a href="https://t.me/{user.username}">{name}</a> (@{user.username}, id={user.id})'
    return f"{name} (id={user.id})"


async def send_to_group(text: str) -> None:
    try:
        await bot.send_message(GROUP_CHAT_ID, text, disable_web_page_preview=True)
    except Exception as exc:  # noqa: BLE001
        logger.error("Не удалось отправить сообщение в группу %s: %s", GROUP_CHAT_ID, exc)


# --------------------------------------------------------------------------- #
# /start и выбор языка
# --------------------------------------------------------------------------- #
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=lang_keyboard())


@dp.callback_query(F.data == "change_lang")
async def on_change_lang(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.message.edit_text(WELCOME, reply_markup=lang_keyboard())
    await query.answer()


@dp.callback_query(F.data.startswith("lang:"))
async def on_lang_chosen(query: CallbackQuery, state: FSMContext) -> None:
    lang = query.data.split(":", 1)[1]
    await state.update_data(lang=lang)
    await query.message.edit_text(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))
    await query.answer()


@dp.callback_query(F.data == "back")
async def on_back(query: CallbackQuery, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.set_state(None)
    await query.message.edit_text(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))
    await query.answer()


# --------------------------------------------------------------------------- #
# Раздел 1. Отзывы
# --------------------------------------------------------------------------- #
@dp.callback_query(F.data == "sec:review")
async def review_start(query: CallbackQuery, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.set_state(ReviewForm.machine)
    await query.message.edit_text(t(lang, "review_ask_machine"), reply_markup=machine_keyboard(lang))
    await query.answer()


@dp.callback_query(ReviewForm.machine, F.data.startswith("rmach:"))
async def review_machine(query: CallbackQuery, state: FSMContext) -> None:
    lang = await get_lang(state)
    machine_id = query.data.split(":", 1)[1]
    await state.update_data(machine_id=machine_id)
    await state.set_state(ReviewForm.rating)
    await query.message.edit_text(t(lang, "review_ask_rating"), reply_markup=rating_keyboard())
    await query.answer()


@dp.callback_query(ReviewForm.rating, F.data.startswith("rate:"))
async def review_rating(query: CallbackQuery, state: FSMContext) -> None:
    lang = await get_lang(state)
    rating = int(query.data.split(":", 1)[1])
    await state.update_data(rating=rating)
    await state.set_state(ReviewForm.text)
    await query.message.edit_text(t(lang, "review_ask_text"))
    await query.answer()


@dp.message(ReviewForm.text, F.text)
async def review_text(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    data = await state.get_data()
    rating = data.get("rating", "—")
    machine_id = data.get("machine_id", "")
    machine_ru = machine_label(machine_id, "ru") if machine_id else "—"

    group_text = (
        "💬 <b>Новый отзыв</b>\n"
        f"Язык: {SECTION_LABELS.get(lang, lang)}\n"
        f"Автомат: {machine_ru}\n"
        f"Оценка: {'⭐' * int(rating) if str(rating).isdigit() else rating} ({rating}/5)\n"
        f"От: {user_link(message)}\n\n"
        f"Текст:\n{message.text}"
    )
    await send_to_group(group_text)

    await state.set_state(None)
    await message.answer(t(lang, "review_done"))
    await message.answer(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))


# --------------------------------------------------------------------------- #
# Раздел 2. Партнёрство
# --------------------------------------------------------------------------- #
@dp.callback_query(F.data == "sec:partner")
async def partner_start(query: CallbackQuery, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.set_state(PartnerForm.name)
    await query.message.edit_text(t(lang, "partner_ask_name"))
    await query.answer()


@dp.message(PartnerForm.name, F.text)
async def partner_name(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.update_data(name=message.text.strip())
    await state.set_state(PartnerForm.phone)
    await message.answer(t(lang, "partner_ask_phone"), reply_markup=phone_keyboard(lang))


@dp.message(PartnerForm.phone, F.contact)
async def partner_phone_contact(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(PartnerForm.text)
    await message.answer(t(lang, "partner_ask_text"), reply_markup=ReplyKeyboardRemove())


@dp.message(PartnerForm.phone, F.text)
async def partner_phone_text(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.update_data(phone=message.text.strip())
    await state.set_state(PartnerForm.text)
    await message.answer(t(lang, "partner_ask_text"), reply_markup=ReplyKeyboardRemove())


@dp.message(PartnerForm.text, F.text)
async def partner_text(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    data = await state.get_data()

    group_text = (
        "🤝 <b>Новая заявка на партнёрство</b>\n"
        f"Язык: {SECTION_LABELS.get(lang, lang)}\n"
        f"Имя: {data.get('name', '—')}\n"
        f"Телефон: {data.get('phone', '—')}\n"
        f"От: {user_link(message)}\n\n"
        f"Сообщение:\n{message.text}"
    )
    await send_to_group(group_text)

    await state.set_state(None)
    await message.answer(t(lang, "partner_done"))
    await message.answer(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))


# --------------------------------------------------------------------------- #
# /cancel и подсказка по неожиданному вводу
# --------------------------------------------------------------------------- #
@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    await state.set_state(None)
    await message.answer(t(lang, "cancelled"), reply_markup=ReplyKeyboardRemove())
    await message.answer(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))


@dp.message()
async def fallback(message: Message, state: FSMContext) -> None:
    lang = await get_lang(state)
    await message.answer(t(lang, "menu_title"), reply_markup=menu_keyboard(lang))


# --------------------------------------------------------------------------- #
# Запуск (long-polling)
# --------------------------------------------------------------------------- #
async def main() -> None:
    logger.info("TezRamen бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
