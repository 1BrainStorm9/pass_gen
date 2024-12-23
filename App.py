import tkinter as tk
from tkinter import messagebox
from Tool import PasswordUtils

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        self.dark_theme = {
            'bg': "#2E2E2E",  # Фон приложения
            'fg': "#FFFFFF",  # Цвет текста
            'btn_bg': "#424242",  # Фон кнопок
            'entry_bg': "#616161",  # Фон полей ввода
            'button_fg': "white"  # Цвет текста на кнопках
        }

        self.current_theme = self.dark_theme
        self.root.configure(bg=self.current_theme['bg'])

        # Заголовок
        title_label = tk.Label(root, text="Создайте безопасный пароль", font=("Helvetica", 18, "bold"), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        title_label.pack(pady=10)

        # Поле для длины пароля
        length_frame = tk.Frame(root, bg=self.current_theme['bg'])
        length_frame.pack(pady=5)
        tk.Label(length_frame, text="Укажите длину пароля:", font=("Helvetica", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg']).pack(side="left", padx=5)
        self.length_entry = tk.Entry(length_frame, width=5, font=("Helvetica", 12), bg=self.current_theme['entry_bg'], fg=self.current_theme['fg'])
        self.length_entry.pack(side="left", padx=5)
        self.length_entry.insert(0, "12")  # Значение по умолчанию

        # Опции
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)

        options_frame = tk.Frame(root, bg=self.current_theme['bg'])
        options_frame.pack(pady=10)
        tk.Checkbutton(options_frame, text="Заглавные буквы", variable=self.include_uppercase,
                       font=("Helvetica", 12), bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                       selectcolor=self.current_theme['entry_bg']).grid(row=0, column=0, padx=10, pady=5)
        tk.Checkbutton(options_frame, text="Цифры", variable=self.include_numbers,
                       font=("Helvetica", 12), bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                       selectcolor=self.current_theme['entry_bg']).grid(row=0, column=1, padx=10, pady=5)
        tk.Checkbutton(options_frame, text="Специальные символы", variable=self.include_special,
                       font=("Helvetica", 12), bg=self.current_theme['bg'], fg=self.current_theme['fg'],
                       selectcolor=self.current_theme['entry_bg']).grid(row=0, column=2, padx=10, pady=5)

        # Поле для пользовательских ключевых слов
        self.custom_keywords_label = tk.Label(root, text="Ваши ключевые слова:", font=("Helvetica", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.custom_keywords_label.pack(pady=5)
        self.custom_keywords_entry = tk.Entry(root, width=50, font=("Helvetica", 12), bg=self.current_theme['entry_bg'], fg=self.current_theme['fg'])
        self.custom_keywords_entry.pack(pady=5)

        # Кнопки
        buttons_frame = tk.Frame(root, bg=self.current_theme['bg'])
        buttons_frame.pack(pady=20)
        self.generate_button = tk.Button(buttons_frame, text="Создать пароль", command=self.generate_password,
                                         font=("Helvetica", 14), bg=self.current_theme['btn_bg'], fg=self.current_theme['button_fg'], relief="flat", padx=10, pady=5)
        self.generate_button.grid(row=0, column=0, padx=10)
        self.copy_button = tk.Button(buttons_frame, text="Копировать пароль", command=self.copy_to_clipboard,
                                     font=("Helvetica", 14), bg=self.current_theme['btn_bg'], fg=self.current_theme['button_fg'], relief="flat", padx=10, pady=5, state=tk.DISABLED)
        self.copy_button.grid(row=0, column=1, padx=10)

        # Поле для вывода результата
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=750, fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.result_label.pack(pady=10)

        # Поле для оценки времени взлома
        self.crack_time_label = tk.Label(root, text="", font=("Helvetica", 12), fg=self.current_theme['fg'], bg=self.current_theme['bg'])
        self.crack_time_label.pack(pady=5)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            include_uppercase = self.include_uppercase.get()
            include_numbers = self.include_numbers.get()
            include_special = self.include_special.get()
            custom_keywords = self.custom_keywords_entry.get()

            password = PasswordUtils.generate_password(length, include_uppercase, include_numbers, include_special, custom_keywords)
            password_strength = PasswordUtils.evaluate_password(password)
            crack_time = PasswordUtils.calculate_crack_time(password, include_uppercase, include_numbers, include_special)

            self.result_label.config(text=f"Пароль: {password}\nНадежность: {password_strength}")
            self.crack_time_label.config(text=f"Оценка времени взлома: {crack_time}")
            self.copy_button.config(state=tk.NORMAL)

            # Сохранение пароля в файл
            PasswordUtils.save_password_to_file(password, custom_keywords)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_to_clipboard(self):
        password = self.result_label.cget("text").split("\n")[0].split(": ")[1]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
