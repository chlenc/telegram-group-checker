from telegram.ext import Updater
import pandas as pd
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
updater = Updater(BOT_TOKEN)
bot = updater.bot

def get_user_info(user_id):
    """Получить информацию о пользователе"""
    try:
        user = bot.get_chat_member(user_id, user_id).user
        return {
            'name': f"{user.first_name or ''} {user.last_name or ''}".strip(),
            'userId': user.id,
            'username': user.username
        }
    except Exception as e:
        print(f"Ошибка при получении информации о пользователе {user_id}: {e}")
        return {
            'name': 'Unknown',
            'userId': user_id,
            'username': None
        }

def check_user_in_group(user_id, group_id):
    """Проверить, находится ли пользователь в группе"""
    try:
        member = bot.get_chat_member(group_id, user_id)
        return member.status not in ['left', 'kicked', 'restricted']
    except Exception as e:
        print(f"Ошибка при проверке пользователя {user_id} в группе {group_id}: {e}")
        return False

def main():
    # Читаем ID пользователей и групп из файлов
    with open('users', 'r') as f:
        user_ids = [line.strip() for line in f if line.strip()]
    
    with open('groups', 'r') as f:
        group_ids = [line.strip() for line in f if line.strip()]

    # Получаем информацию о пользователях
    users_info = []
    for user_id in user_ids:
        user_info = get_user_info(user_id)
        users_info.append(user_info)

    # Проверяем участие пользователей в группах
    results = []
    for user_info in users_info:
        user_result = user_info.copy()
        for group_id in group_ids:
            is_member = check_user_in_group(user_info['userId'], group_id)
            user_result[f'group_{group_id}'] = is_member
        results.append(user_result)

    # Создаем DataFrame
    df = pd.DataFrame(results)
    
    # Сохраняем результат в Excel
    df.to_excel('membership_results.xlsx', index=False)
    print("Результаты сохранены в файл 'membership_results.xlsx'")

if __name__ == '__main__':
    main()
