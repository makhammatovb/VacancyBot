import asyncio
from database import Database
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import aiogram

import os
import django
from vacation import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vacation.settings')
django.setup()

bot = Bot("7448678922:AAHkZkmXViaNENu-vGTQOodsbI60dBsWF7U")
# https://t.me/botvacationbot  BOT URL
dp = Dispatcher(bot=bot,storage=MemoryStorage())
db = Database('vacation.db')
db.init_db()

class Form(StatesGroup):
    name = State()
    surname = State()
    birth_date = State()
    region = State()
    education = State()
    languages = State()
    confirmation = State()
    duplicate_contact = State()
    vacation_types = State()
    vacations = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    button_uzbek = types.KeyboardButton("Ўзбек")
    button_russian = types.KeyboardButton("Русский")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_uzbek, button_russian)

    await message.answer("Выберите язык:", reply_markup=keyboard)
    dp.register_message_handler(ask_language, content_types=types.ContentTypes.TEXT)

async def ask_language(message: types.Message):
    if message.text == "Ўзбек":
        lang = "UZ"
        text = "Telefon raqamingizni yuboring"
        contact_button = "Kontakt ulashish"
        name_text = "Ismingizni kiriting"
        surname_text = "Familiyangizni kiriting"
        birth_date_text = "Tug'ilgan sanangizni kiriting (Masalan: 15.12.2004)"
    else:
        lang = "RU"
        text = "Отправьте свой контактный номер телефона"
        contact_button = "Отправить контакт"
        name_text = "Введите ваше имя"
        surname_text = "Введите вашу фамилию"
        birth_date_text = "Введите вашу дату рождения (Например: 15.12.2004)"

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(contact_button, request_contact=True))

    await message.answer(text, reply_markup=keyboard)
    dp.register_message_handler(ask_name, content_types=types.ContentTypes.CONTACT, state="*")

    await dp.current_state(user=message.from_user.id).update_data(
        name_text=name_text, surname_text=surname_text, birth_date_text=birth_date_text, lang=lang,
    )

async def ask_name(message: types.Message):
    contact = message.contact
    if contact is None:
        return

    data = await dp.current_state().get_data()
    name_text = data.get("name_text")
    if not name_text:
        name_text = "Введите ваше имя"

    await bot.send_message(message.chat.id, name_text)
    dp.register_message_handler(process_name, content_types=types.ContentTypes.TEXT, state="name")

    await dp.current_state().set_state("name")
    await dp.current_state().update_data(contact=contact)

async def process_name(message: types.Message):
    if (await dp.current_state().get_state()) == "name":
        name = message.text

        data = await dp.current_state().get_data()
        surname_text = data.get("surname_text")
        if not surname_text:
            surname_text = "Введите вашу фамилию"
        await bot.send_message(message.chat.id, surname_text)

        await dp.current_state().set_state("surname")
        await dp.current_state().update_data(name=name)

        dp.register_message_handler(process_surname, content_types=types.ContentTypes.TEXT, state="surname")

async def process_surname(message: types.Message, state: FSMContext):
    if (await dp.current_state().get_state()) == "surname":
        surname = message.text

        data = await dp.current_state().get_data()
        contact = data.get("contact")


        if data.get("lang") == "UZ":
            birth_date_text = data.get("birth_date_text")
            await message.answer(birth_date_text)
            await dp.current_state().set_state("birth_date")
            await state.update_data(surname=surname, contact=contact)
        else:
            await message.answer("Введите вашу дату рождения (Например: 12.12.2004)")
            await dp.current_state().set_state("birth_date")
            await dp.current_state().update_data(surname=surname, contact=contact, language=message.text)
        dp.register_message_handler(process_birth_date, content_types=types.ContentTypes.TEXT, state="birth_date")

async def process_birth_date(message: types.Message, state: FSMContext):
    if (await dp.current_state().get_state()) == "birth_date":
        birth_date = message.text
        data = await dp.current_state().get_data()
        lang = data.get("lang")

        await state.update_data(birth_date=birth_date)

        if lang == "UZ":
                region_text = "Viloyatingizni tanlang:"
                button1 = types.KeyboardButton("Andijon")
                button2 = types.KeyboardButton("Farg'ona")
                button3 = types.KeyboardButton("Toshkent")
                button4 = types.KeyboardButton("Toshkent viloyati")
                button5 = types.KeyboardButton("Namangan")
                button6 = types.KeyboardButton("Navoi")
                button7 = types.KeyboardButton("Qashqadaryo")
                button8 = types.KeyboardButton("Surxondaryo")
                button9 = types.KeyboardButton("Samarqand")
                button10 = types.KeyboardButton("Jizzax")
                button11 = types.KeyboardButton("Sirdaryo")
                button12 = types.KeyboardButton("Buxoro")
                button13 = types.KeyboardButton("Xorazm")
                button14 = types.KeyboardButton("Qoraqalpog'iston Respublikasi")
        else:
                region_text = "Выберите свой регион:"
                button1 = types.KeyboardButton("Андижан")
                button2 = types.KeyboardButton("Фергана")
                button3 = types.KeyboardButton("Ташкент")
                button4 = types.KeyboardButton("Ташкентская область")
                button5 = types.KeyboardButton("Наманган")
                button6 = types.KeyboardButton("Навои")
                button7 = types.KeyboardButton("Кашкадарья")
                button8 = types.KeyboardButton("Сурхандарья")
                button9 = types.KeyboardButton("Самарканд")
                button10 = types.KeyboardButton("Джизак")
                button11 = types.KeyboardButton("Сырдарья")
                button12 = types.KeyboardButton("Бухара")
                button13 = types.KeyboardButton("Хорезм")
                button14 = types.KeyboardButton("Республика Каракалпакстан")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12, button13, button14)

        await message.answer(f"{region_text}", reply_markup=keyboard)
        await state.set_state("region")
        dp.register_message_handler(process_region, content_types=types.ContentTypes.TEXT, state="region")

async def process_region(message: types.Message, state: FSMContext):
    region = message.text

    data = await state.get_data()
    lang = data.get("lang")

    await state.update_data(region=region)
    await state.set_state("education")

    if lang == "UZ":
        education_text = "Ma'lumotingiz"
        button1 = types.KeyboardButton("Oliy")
        button2 = types.KeyboardButton("O'rta")
        button3 = types.KeyboardButton("Boshlang'ich")
    else:
        education_text = "Образование"
        button1 = types.KeyboardButton("Высшее")
        button2 = types.KeyboardButton("Среднее")
        button3 = types.KeyboardButton("Начальнoe")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button1, button2, button3)

    await message.answer(f"{education_text}:", reply_markup=keyboard)
    await state.set_state("education")

@dp.message_handler(state="education")
async def process_education(message: types.Message, state: FSMContext):
    education = message.text

    data = await dp.current_state().get_data()

    await state.update_data(education=education)
    await state.set_state("languages")

    lang = data.get("lang")
    if lang == "UZ":
        language_text = "Tillarni tanlang (bir nechta tanlashingiz mumkin):"
        button1_text = "Inglizcha"
        button2_text = "Ruscha"
        button3_text = "O'zbekcha"
        button4_text = "Barcha ma'lumotlar"
    else:
        language_text = "Выберите языки (можно выбрать несколько):"
        button1_text = "Английский"
        button2_text = "Русский"
        button3_text = "Узбекский"
        button4_text = "Все данные"

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.InlineKeyboardButton(text=button1_text))
    keyboard.row(types.InlineKeyboardButton(text=button2_text))
    keyboard.row(types.InlineKeyboardButton(text=button3_text))
    keyboard.row(types.InlineKeyboardButton(text=button4_text))

    await message.answer(language_text, reply_markup=keyboard)
    dp.register_message_handler(process_languages, content_types=types.ContentTypes.TEXT, state="languages")
    await state.set_state("languages")


@dp.message_handler(state=Form.languages)
async def process_languages(message: types.Message, state: FSMContext):
    selected = message.text

    data = await state.get_data()
    current_languages = data.get("languages", [])

    if selected in ["Inglizcha", "Английский"]:
        if data.get("lang") == "UZ":
            current_languages.append("Inglizcha")
        else:
            current_languages.append("Английский")
    elif selected in ["Ruscha", "Русский"]:
        if data.get("lang") == "UZ":
            current_languages.append("Ruscha")
        else:
            current_languages.append("Русский")
    elif selected in ["O'zbekcha", "Узбекский"]:
        if data.get("lang") == "UZ":
            current_languages.append("O'zbekcha")
        else:
            current_languages.append("Узбекский")
    elif selected in ["Barcha ma'lumotlar", "Все данные"]:
        if not current_languages:
            if data.get("lang") == "UZ":
                await message.answer("Iltimos, o'zingiz bilgan tillarni tanlang!")
            else:
                await message.answer("Пожалуйста, выберите языки, которые вы знаете!")
            return

        name = data.get("name")
        surname = data.get("surname")
        contact = data.get("contact")
        birth_date = data.get("birth_date")
        region = data.get("region")
        education = data.get("education")
        if data.get("lang") == "UZ":
            info_message = (f"Ism: {name}\n"
                        f"Familiya: {surname}\n"
                        f"Telefon raqam: {contact['phone_number']}\n"
                        f"Tug'ilgan sana: {birth_date}\n"
                        f"Viloyat: {region}\n"
                        f"Ma'lumot: {education}\n"
                        f"Tillar: {', '.join(current_languages)}")
            await message.answer(info_message)
        else:
            info_message = (f"Имя: {name}\n"
                            f"Фамилия: {surname}\n"
                            f"Номер телефона: {contact['phone_number']}\n"
                            f"Дата рождения: {birth_date}\n"
                            f"Регион: {region}\n"
                            f"Образование: {education}\n"
                            f"Языки: {', '.join(current_languages)}")
            await message.answer(info_message)

        if data.get("lang") == "UZ":
            confirmation_text = "Ma'lumotlar to'g'ri kiritilganmi?"
            yes_text = "Ha"
            no_text = "Yo'q"
        else:
            confirmation_text = "Данные введены правильно?"
            yes_text = "Да"
            no_text = "Нет"

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(types.KeyboardButton(text=yes_text), types.KeyboardButton(text=no_text))

        await message.answer(confirmation_text, reply_markup=keyboard)
        await Form.confirmation.set()
        return

    await state.update_data(languages=current_languages)

@dp.message_handler(state=Form.confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    response = message.text.lower()

    if response in ["ha", "да"]:
        data = await state.get_data()

        user_info = {
            "name": data.get("name"),
            "surname": data.get("surname"),
            "contact": data.get("contact")["phone_number"],
            "birth_date": data.get("birth_date"),
            "city": data.get("region"),
            "education": data.get("education"),
            "languages": ", ".join(data.get("languages", []))
        }

        db.insert_user_data(user_info)
        await message.answer("Ma'lumotlaringiz saqlandi!" if data.get("lang") == "UZ" else "Ваши данные сохранены!",
                             reply_markup = types.ReplyKeyboardRemove())
        await state.finish()

        vacation_types = db.get_vacation_type()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for vacation_type in vacation_types:
            keyboard.row(types.KeyboardButton(text=vacation_type))

        if data.get("lang") == "UZ":
            await message.answer("O'zingizga ma'qul yo'nalishni tanlang:", reply_markup=keyboard)
        else:
            await message.answer("Выберите свое направление:", reply_markup=keyboard)
        await Form.vacation_types.set()
        await state.update_data(lang=data.get("lang"))
        dp.register_message_handler(process_vacation_selection, content_types=types.ContentTypes.TEXT, state="vacations")
    else:
        await state.finish()
        await start(message)

@dp.message_handler(state=Form.duplicate_contact)
async def process_duplicate_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    response = message.text.lower()
    lang = data.get("lang")

    if response in ["ha", "да"]:
        await state.finish()
        await start(message)
    else:
        await state.finish()
        await message.answer(
            "Спасибо! Будьте здоровы!" if lang != "UZ" else "Rahmat! Sog' bo'ling!",
            reply_markup = types.ReplyKeyboardRemove()
        )


@dp.message_handler(state=Form.vacation_types)
async def process_vacation_selection(message: types.Message, state: FSMContext):
    selected_vacation_type = message.text
    await state.update_data(vacation_type=selected_vacation_type)
    data = await state.get_data("lang")
    lang = data.get("lang")

    vacations = db.get_vacations(selected_vacation_type, lang)

    if vacations:
        for vacation in vacations:
            if lang == "UZ":
                if len(vacation) >= 10:
                    image_uz, name_uz, company, location_uz, requirements_uz, amenities_uz, salary, experience, contacts1, contacts2 = vacation[:10]
                else:
                    print("Unexpected number of fields:", len(vacation))
                    continue

                if image_uz:
                    image_uz_path = f"media/{image_uz.strip()}"
                    try:
                        with open(image_uz_path, "rb") as photo:
                            caption = (
                                f"🔰<b>Ishchi:</b> {name_uz.strip()}\n\n"
                                f"🏢<b>Kompaniya:</b> {company.strip()}\n\n"
                                f"📍<b>Manzil:</b> {location_uz.strip()}\n\n"
                                f"❗️<b>Talablar:</b>\n {requirements_uz.strip()}\n\n"
                                f"✅<b>Qulayliklar:</b>\n {amenities_uz.strip()}\n\n"
                                f"💵<b>Maosh:</b> ${salary.strip()}\n\n"
                                f"📊<b>Tajriba:</b> {experience.strip()} yil\n\n"
                                f"☎️<b>Aloqa uchun:</b> {contacts1.strip()}"
                            )
                            await bot.send_photo(message.chat.id, photo=photo, caption=caption, parse_mode='HTML')
                    except FileNotFoundError:
                        print(f"Image file not found: {image_uz_path}")
                        await message.answer("An error occurred while displaying the image: File not found.")
                        continue
                    except aiogram.utils.exceptions.BadRequest as e:
                        print(f"Failed to send photo: {e}")
                        await message.answer(f"An error occurred while displaying the image for {name_uz}.")
                        continue
                else:
                    vacation_info = (
                        f"🔰*Ishchi:* {name_uz.strip()}\n\n"
                        f"🏢*Kompaniya:* {company.strip()}\n\n"
                        f"📍*Manzil:* {location_uz.strip()}\n\n"
                        f"❗️*Talablar:*\n {requirements_uz.strip()}\n\n"
                        f"✅*Qulayliklar:*\n {amenities_uz.strip()}\n\n"
                        f"💵*Maosh:* ${salary.strip()}\n\n"
                        f"📊*Tajriba:* {experience.strip()} yil\n\n"
                        f"☎️*Aloqa uchun:* {contacts1.strip()}"
                    )

                    await message.answer(vacation_info, parse_mode='Markdown')
                await Form.vacation_types.set()
            else:
                if len(vacation) >= 9:
                    image_ru, name_ru, company, location_ru, requirements_ru, amenities_ru, salary, experience, contacts1, contacts2 = vacation[:10]
                else:
                    print("Unexpected number of fields:", len(vacation))
                    continue

                if image_ru:
                    image_ru_path = f"media/{image_ru.strip()}"
                    try:
                        with open(image_ru_path, "rb") as photo:
                            caption = (
                                f"🔰<b>Рабочий:</b> {name_ru.strip()}\n\n"
                                f"🏢<b>Компания:</b> {company.strip()}\n\n"
                                f"📍<b>Местоположение:</b> {location_ru.strip()}\n\n"
                                f"❗️<b>Требования:</b>\n {requirements_ru.strip()}\n\n"
                                f"✅<b>Удобства:</b>\n {amenities_ru.strip()}\n\n"
                                f"💵<b>Заработная плата:</b> ${salary.strip()}\n\n"
                                f"📊<b>Опыт:</b> {experience.strip()} годы\n\n"
                                f"☎️<b>Для контакта:</b> {contacts1.strip()}"
                            )
                            await bot.send_photo(message.chat.id, photo=photo, caption=caption, parse_mode='HTML')
                    except FileNotFoundError:
                        print(f"Image file not found: {image_ru_path}")
                        await message.answer("An error occurred while displaying the image: File not found.")
                        continue
                    except aiogram.utils.exceptions.BadRequest as e:
                        print(f"Failed to send photo: {e}")
                        await message.answer(f"An error occurred while displaying the image for {name_ru}.")
                        continue
                else:
                    vacation_info = (
                        f"🔰*Рабочий:* {name_ru.strip()}\n\n"
                        f"🏢*Компания:* {company.strip()}\n\n"
                        f"📍*Местоположение:* {location_ru.strip()}\n\n"
                        f"❗️*Требования:*\n {requirements_ru.strip()}\n\n"
                        f"✅*Удобства:*\n {amenities_ru.strip()}\n\n"
                        f"💵*Заработная плата:* ${salary.strip()}\n\n"
                        f"📊*Опыт:* {experience.strip()} годы\n\n"
                        f"☎️*Для контакта:* {contacts1.strip()}"
                    )

                    await message.answer(vacation_info, parse_mode='Markdown')
                await Form.vacation_types.set()
    else:
        await message.answer("No vacations found for the selected type. Please select another type.")
        await Form.vacation_types.set()



async def main():
    await dp.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()