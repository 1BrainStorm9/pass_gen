import random
import string
from datetime import datetime

class PasswordUtils:
    @staticmethod
    def generate_password(length, include_uppercase, include_numbers, include_special, custom_keywords):
        if not 4 <= length <= 50:
            raise ValueError("Длина пароля должна быть от 4 до 50 символов")

        if not (include_uppercase or include_numbers or include_special or custom_keywords):
            raise ValueError("Необходимо выбрать хотя бы одну категорию символов или добавить ключевые слова")

        char_pool = string.ascii_lowercase
        required_chars = []

        if include_uppercase:
            char_pool += string.ascii_uppercase
            required_chars.append(random.choice(string.ascii_uppercase))

        if include_numbers:
            char_pool += string.digits
            required_chars.append(random.choice(string.digits))

        if include_special:
            special_chars = "!@#$%^&*()-_=+"
            char_pool += special_chars
            required_chars.append(random.choice(special_chars))

        if custom_keywords:
            custom_keywords_list = custom_keywords.split()
            required_chars += custom_keywords_list

        remaining_length = max(0, length - len(required_chars))
        password = random.choices(char_pool, k=remaining_length) + required_chars
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def evaluate_password(password):
        score_criteria = [
            len(password) >= 8,
            any(char.isupper() for char in password),
            any(char.isdigit() for char in password),
            any(char in "!@#$%^&*()-_=+" for char in password)
        ]
        score = sum(score_criteria)

        return "Надежный" if score == 4 else "Средний" if score == 3 else "Слабый"

    @staticmethod
    def calculate_crack_time(password, include_uppercase, include_numbers, include_special):
        char_set = string.ascii_lowercase
        if include_uppercase:
            char_set += string.ascii_uppercase
        if include_numbers:
            char_set += string.digits
        if include_special:
            char_set += "!@#$%^&*()-_=+"

        num_combinations = len(char_set) ** len(password)
        guesses_per_second = 10 ** 11  # 100 миллиардов
        time_seconds = num_combinations / guesses_per_second

        time_units = [
            (60, "секунд"),
            (3600, "минут"),
            (86400, "часов"),
            (31536000, "дней"),
            (315360000, "лет")
        ]

        for threshold, unit in time_units:
            if time_seconds < threshold:
                return f"{time_seconds / (threshold / 60 if unit != 'секунд' else 1):.2f} {unit}"
        return "Больше 10 лет"

    @staticmethod
    def save_password_to_file(password, custom_keywords):
        try:
            with open("generated_passwords.txt", "a", encoding="utf-8") as file:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{current_time} | Пароль: {password} | Ключевые слова: {custom_keywords}\n")
        except Exception as e:
            raise ValueError(f"Произошла ошибка при сохранении пароля: {e}")
