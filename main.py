import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

DB = {
    'easy': [
        {'q': 'Как вывести текст на экран в Python?', 'options': ['print()', 'echo()', 'show()'], 'a': 'print()', 'cat': 'syntax'},
        {'q': 'Что хранит переменная x после: x = 5?', 'options': ['число 5', 'строку "5"', 'ничего'], 'a': 'число 5', 'cat': 'syntax'},
        {'q': 'Результат: 2 + 2 ?', 'options': ['3', '4', '22'], 'a': '4', 'cat': 'syntax'},
        {'q': 'Какой тип у 10?', 'options': ['int', 'float', 'str'], 'a': 'int', 'cat': 'theory'},
        {'q': 'Как получить длину строки "hi"?', 'options': ['size("hi")', 'len("hi")', 'count("hi")'], 'a': 'len("hi")', 'cat': 'syntax'},

        {'q': 'Как создать пустой список?', 'options': ['[]', '{}', '()'], 'a': '[]', 'cat': 'syntax'},
        {'q': 'Строки заключаются в…', 'options': ['кавычки', 'круглые скобки', 'фигурные скобки'], 'a': 'кавычки', 'cat': 'theory'},
        {'q': 'Как сделать комментарий?', 'options': ['//', '#', '--'], 'a': '#', 'cat': 'syntax'},
        {'q': 'Какой тип у "hello"?', 'options': ['int', 'str', 'list'], 'a': 'str', 'cat': 'theory'},
        {'q': 'Что делает print("A" * 3)?', 'options': ['AAA', 'A3', 'Ошибка'], 'a': 'AAA', 'cat': 'syntax'},
    ],

    'medium': [
        {'q': 'Как обратиться к первому элементу списка a = [10, 20, 30]?', 'options': ['a[1]', 'a[0]', 'a(first)'], 'a': 'a[0]', 'cat': 'syntax'},
        {'q': 'Как добавить элемент в список?', 'options': ['add()', 'append()', 'push()'], 'a': 'append()', 'cat': 'syntax'},
        {'q': 'Что выведет print("3" + "2")?', 'options': ['5', '32', 'Ошибка'], 'a': '32', 'cat': 'syntax'},
        {'q': 'Как преобразовать число в строку?', 'options': ['str()', 'int()', 'text()'], 'a': 'str()', 'cat': 'theory'},
        {'q': 'Что вернёт len([1,2,3])?', 'options': ['2', '3', '4'], 'a': '3', 'cat': 'theory'},

        {'q': 'Что делает функция input()?', 'options': ['Выводит текст', 'Читает ввод пользователя', 'Закрывает программу'], 'a': 'Читает ввод пользователя', 'cat': 'theory'},
        {'q': 'Как сделать строку заглавной?', 'options': ['upper()', 'big()', 'cap()'], 'a': 'upper()', 'cat': 'syntax'},
        {'q': 'Как проверить равенство: a равно b?', 'options': ['a = b', 'a == b', 'a equals b'], 'a': 'a == b', 'cat': 'syntax'},
        {'q': 'Что хранит список?', 'options': ['только числа', 'только строки', 'любые элементы'], 'a': 'любые элементы', 'cat': 'theory'},
        {'q': 'Как создать словарь?', 'options': ['[]', '{}', '()'], 'a': '{}', 'cat': 'syntax'},
    ],

    'hard': [
        {'q': 'Что делает range(3)?', 'options': ['[0,1,2]', '[1,2,3]', 'три случайных числа'], 'a': '[0,1,2]', 'cat': 'theory'},
        {'q': 'Что делает список: [x for x in range(3)]?', 'options': ['Генерирует [0, 1, 2]', 'Создает пустой список', 'Ошибка'], 'a': 'Генерирует [0, 1, 2]', 'cat': 'syntax'},
        {'q': 'Что выводит print(type([]))?', 'options': ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>"], 'a': "<class 'list'>", 'cat': 'syntax'},
        {'q': 'Как определить функцию?', 'options': ['def my():', 'func my():', 'function my():'], 'a': 'def my():', 'cat': 'syntax'},
        {'q': 'Что делает return в функции?', 'options': ['останавливает функцию и возвращает значение', 'удаляет переменную', 'ничего'], 'a': 'останавливает функцию и возвращает значение', 'cat': 'theory'},

        {'q': 'Что делает list("abc")?', 'options': ['["a", "b", "c"]', '["abc"]', 'Ошибка'], 'a': '["a", "b", "c"]', 'cat': 'syntax'},
        {'q': 'Какое значение истинности у пустого списка?', 'options': ['True', 'False', 'Ошибка'], 'a': 'False', 'cat': 'theory'},
        {'q': 'Что выведет print("a" in "cat")?', 'options': ['True', 'False', 'Ошибка'], 'a': 'True', 'cat': 'syntax'},
        {'q': 'Как создать функцию без параметров?', 'options': ['def f:', 'def f():', 'func f()'], 'a': 'def f():', 'cat': 'syntax'},
        {'q': 'Как объединить списки a + b?', 'options': ['склеивает списки', 'умножает', 'сортирует'], 'a': 'склеивает списки', 'cat': 'theory'},
    ]
}


def generate_quiz():
    """Собирает 15 вопросов с фиксированным максимальным баллом 100"""
    easy_part = random.sample(DB['easy'], 5)
    medium_part = random.sample(DB['medium'], 5)
    hard_part = random.sample(DB['hard'], 5)
    
    for q in easy_part: q['points'] = 4
    for q in medium_part: q['points'] = 6
    for q in hard_part: q['points'] = 10
    
    full_quiz = easy_part + medium_part + hard_part
    random.shuffle(full_quiz)
    return full_quiz

async def send_question(chat_id: int, bot: Bot):
    """Отправляет текущий вопрос пользователю"""
    data = user_data[chat_id]
    
    if data['current'] >= len(data['questions']):
        await finish_game(chat_id, bot)
        return

    q_data = data['questions'][data['current']]
    points = q_data['points']
    
    cat_icon = "📚 Теория" if q_data['cat'] == 'theory' else "💻 Синтаксис"
    
    buttons = []
    for opt in q_data['options']:
        is_correct = 1 if opt == q_data['a'] else 0
        buttons.append(InlineKeyboardButton(text=opt, callback_data=f"ans_{is_correct}_{points}"))
    
    random.shuffle(buttons)
    
    markup = InlineKeyboardMarkup(
    inline_keyboard=[[btn] for btn in buttons])

    

    text = (f"Вопрос {data['current']+1}/15  |  {cat_icon}\n"
            f"Баллов за ответ: <b>{points}</b>\n\n"
            f"<code>{q_data['q']}</code>")
    
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode='HTML')


@dp.message(F.text == "/start")
async def start_game(message: types.Message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    
    questions = generate_quiz()
    user_data[chat_id] = {'score': 0, 'current': 0, 'questions': questions}
    
    await message.answer("🐍 <b>Python Quiz Bot</b>\n\nВас ждут 15 вопросов по теории и синтаксису.\nМаксимум 100 баллов.\Начинаем!", parse_mode='HTML')
    
    await send_question(chat_id, message.bot)


@dp.callback_query(F.data.startswith('ans_'))
async def handle_answer(call: types.CallbackQuery):
    """Обработчик нажатия на кнопку-ответ"""
    chat_id = call.message.chat.id
    
    if chat_id not in user_data:
        await call.answer("Сессия устарела. Напишите /start")
        return

    _, is_correct, points = call.data.split('_')
    
    if int(is_correct):
        user_data[chat_id]['score'] += int(points)
        await call.answer("✅ Верно!")
    else:
        await call.answer("❌ Неверно!")

    await call.message.edit_reply_markup(reply_markup=None)
    
    user_data[chat_id]['current'] += 1
    
    await send_question(chat_id, call.bot)


async def finish_game(chat_id: int, bot: Bot):
    """Завершение игры и вывод результатов"""
    score = user_data[chat_id]['score']
    text = f"🏁 <b>Тест завершен!</b>\n\nТвой результат: {score} из 100."
    
    if score == 100: text += "\nИДЕАЛЬНО !!!"
    elif score >= 90: text += "\nТвоя оценка 5 !!!"
    elif score >= 85: text += "\nТвоя оценка 4 !!!"
    elif score >= 60: text += "\nТвоя оценка 3 !!!"
    else: text += "\n🌚 Иди учить уроки."
    
    text += "\n\n/start — попробовать еще раз"
    
    await bot.send_message(chat_id, text, parse_mode='HTML')
    del user_data[chat_id]


async def main():
    print("бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())