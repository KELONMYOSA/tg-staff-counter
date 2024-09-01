from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils.handle_messages import get_report
from src.utils.transformations import get_month_name

router = Router()


@router.message(Command("get_report"))
async def cmd_get_report(message: Message):
    now = message.date
    current_month = get_month_name(now.month)
    previous_month = get_month_name((now.replace(day=1) - timedelta(days=1)).month)

    keyboard = InlineKeyboardBuilder()
    keyboard.max_width = 2
    buttons = [
        InlineKeyboardButton(text=current_month, callback_data="rep_current_month"),
        InlineKeyboardButton(text=previous_month, callback_data="rep_previous_month"),
        InlineKeyboardButton(text="Свои даты", callback_data="rep_custom_dates"),
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите период для отчета:", reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "rep_current_month")
async def get_report_cur_month(call: CallbackQuery):
    now = call.message.date
    start_date = now.replace(day=1, hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    end_date = now.strftime("%Y-%m-%d %H:%M:%S")

    await call.answer()
    await call.message.delete()
    await call.message.answer(get_report(start_date, end_date), parse_mode="HTML")


@router.callback_query(F.data == "rep_previous_month")
async def get_report_prev_month(call: CallbackQuery):
    now = call.message.date
    start_date = (
        (now.replace(day=1) - timedelta(days=1))
        .replace(day=1, hour=0, minute=0, second=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    end_date = (
        (now.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S")
    )

    await call.answer()
    await call.message.delete()
    await call.message.answer(get_report(start_date, end_date), parse_mode="HTML")


@router.callback_query(F.data == "rep_custom_dates")
async def get_report_custom_dates(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.set_state("rep_get_dates")
    await call.message.answer("Пожалуйста, введите диапазон дат в формате:\n" "'YYYY-MM-DD YYYY-MM-DD'.")


@router.message(StateFilter("rep_get_dates"))
async def get_report_custom_dates_txt(message: Message, state: FSMContext):
    try:
        dates = message.text.split()
        start_date = f"{dates[0]} 00:00:00"
        end_date = f"{dates[1]} 23:59:59"
        await state.clear()
        await message.answer(get_report(start_date, end_date), parse_mode="HTML")
    except Exception as e:
        print(e)
        await message.reply("Неправильный формат даты.\n" "Используйте формат: 'YYYY-MM-DD YYYY-MM-DD'.")
