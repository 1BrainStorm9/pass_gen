import unittest
from Tool import PasswordUtils

class TestPasswordUtils(unittest.TestCase):

    def test_generate_password_min_length(self):
        # Проверяем, что минимальная длина работает корректно
        password = PasswordUtils.generate_password(4, True, True, True, "")
        self.assertEqual(len(password), 4, "Пароль должен быть длиной 4 символа")

    def test_generate_password_max_length(self):
        # Проверяем, что максимальная длина работает корректно
        password = PasswordUtils.generate_password(50, True, True, True, "")
        self.assertEqual(len(password), 50, "Пароль должен быть длиной 50 символов")

    def test_generate_password_contains_uppercase(self):
        # Проверяем, что пароль содержит заглавные буквы
        password = PasswordUtils.generate_password(8, True, False, False, "")
        self.assertTrue(any(c.isupper() for c in password), "Пароль должен содержать заглавные буквы")

    def test_generate_password_contains_numbers(self):
        # Проверяем, что пароль содержит цифры
        password = PasswordUtils.generate_password(8, False, True, False, "")
        self.assertTrue(any(c.isdigit() for c in password), "Пароль должен содержать цифры")

    def test_generate_password_contains_special_chars(self):
        # Проверяем, что пароль содержит специальные символы
        password = PasswordUtils.generate_password(8, False, False, True, "")
        self.assertTrue(any(c in "!@#$%^&*()-_=+" for c in password), "Пароль должен содержать специальные символы")

    def test_generate_password_with_custom_keywords(self):
        # Проверяем, что пользовательские ключевые слова включены в пароль
        custom_keywords = "test"
        password = PasswordUtils.generate_password(8, False, False, False, custom_keywords)
        self.assertIn(custom_keywords, password, "Пароль должен содержать пользовательские ключевые слова")

    def test_evaluate_password_strong(self):
        # Проверяем оценку "Надежный"
        password = "A1b2C3d4!"
        self.assertEqual(PasswordUtils.evaluate_password(password), "Надежный", "Пароль должен быть оценен как 'Надежный'")

    def test_evaluate_password_medium(self):
        # Проверяем оценку "Средний"
        password = "abc12345"
        self.assertEqual(PasswordUtils.evaluate_password(password), "Средний", "Пароль должен быть оценен как 'Средний'")

    def test_evaluate_password_weak(self):
        # Проверяем оценку "Слабый"
        password = "abcdef"
        self.assertEqual(PasswordUtils.evaluate_password(password), "Слабый", "Пароль должен быть оценен как 'Слабый'")

    def test_calculate_crack_time_large(self):
        # Проверяем расчет времени для сложного пароля
        password = "A1b2C3d4!"
        time = PasswordUtils.calculate_crack_time(password, True, True, True)
        self.assertIn("лет", time, "Ожидается время взлома в годах")

    def test_calculate_crack_time_small(self):
        # Проверяем расчет времени для простого пароля
        password = "abc"
        time = PasswordUtils.calculate_crack_time(password, False, False, False)
        self.assertIn("секунд", time, "Ожидается время взлома в секундах")

    def test_save_password_to_file_valid(self):
        # Проверяем успешное сохранение пароля в файл
        password = "A1b2C3d4"
        custom_keywords = "test"
        try:
            PasswordUtils.save_password_to_file(password, custom_keywords)
            with open("generated_passwords.txt", "r", encoding="utf-8") as file:
                content = file.read()
                self.assertIn(password, content, "Пароль должен быть сохранен в файл")
                self.assertIn(custom_keywords, content, "Ключевые слова должны быть сохранены в файл")
        except Exception as e:
            self.fail(f"Ошибка при сохранении пароля в файл: {e}")

if __name__ == '__main__':
    unittest.main()
