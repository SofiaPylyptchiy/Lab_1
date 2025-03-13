import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Фінансовий щоденник")
        self.geometry("800x600")
        self.configure(bg="#000000")
        self.create_main_menu()
        self.show_date()

        # Глобальні змінні для зберігання даних
        self.income = 0
        self.expenses = 0
        self.net_income = self.income - self.expenses

        # Мета заощаджень
        self.savings_goal = 0
        self.savings_progress = 0

        # Список категорій витрат та словник для збереження витрат за категоріями
        self.expense_categories = ['FOOD', 'Transport', 'Apartment', 'Activity', 'Clother', 'Health', 'Other']
        self.expense_details = {category: [] for category in self.expense_categories}

        # Налаштування за замовчуванням
        self.currency = tk.StringVar(value="грн")

    def create_main_menu(self):
        main_menu_frame = tk.Frame(self, bg="#000000")
        main_menu_frame.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(main_menu_frame, text="Твій фінансовий щоденник", font=("Helvetica", 24), bg="#000000", fg="#FFFFFF")
        label.pack(pady=20)

        buttons = [
            ("Налаштування", self.show_settings),
            ("Мета заощаджень", self.set_savings_goal),
            ("Витрати", self.show_expenses),
            ("Дохід", self.show_income),
            ("Переглянути детальніше", self.show_expense_details),
            ("Вихід", self.quit)
        ]

        for button_text, command in buttons:
            button = tk.Button(main_menu_frame, text=button_text, command=command, bg="#9400D3", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
            button.pack(pady=10)

    def show_date(self):
        current_date = datetime.now().strftime("%d.%m.%Y")
        date_label = tk.Label(self, text=f"Сьогоднішня дата: {current_date}", font=("Helvetica", 10), bg="#000000", fg="#FFFFFF")
        date_label.pack(side=tk.BOTTOM, pady=10, anchor="s")

    def show_settings(self):
        SettingsWindow(self)

    def set_savings_goal(self):
        SavingsWindow(self)

    def show_expenses(self):
        ExpensesWindow(self)

    def show_income(self):
        IncomeWindow(self)

    def show_expense_details(self):
        ExpenseDetailsWindow(self)

    def set_goal_amount(self, amount, window):
        try:
            self.savings_goal = float(amount)
            messagebox.showinfo("Успіх", f"Мета заощаджень встановлена: {self.savings_goal:.2f} {self.currency.get()}")
            window.destroy()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректну суму")

    def record_income(self, amount, window):
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Помилка", "Сума доходу повинна бути більше нуля")
                return
            self.income += amount
            self.net_income = self.income - self.expenses
            messagebox.showinfo("Успіх", f"Дохід {amount:.2f} {self.currency.get()} додано")
            window.destroy()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректну суму")

    def record_expenses(self, amount, category, window):
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Помилка", "Сума витрат повинна бути більше нуля")
                return
            self.expenses += amount
            self.expense_details[category].append(amount)
            self.net_income = self.income - self.expenses
            messagebox.showinfo("Успіх", f"Витрати {amount:.2f} {self.currency.get()} на {category} додано")
            window.destroy()
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректну суму")

class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Налаштування")
        self.configure(bg="#000000")

        label_currency = tk.Label(self, text="Виберіть валюту:", bg="#000000", fg="#FFFFFF")
        label_currency.pack(pady=5)

        currency_options = ["грн", "$", "€"]
        currency_menu = tk.OptionMenu(self, master.currency, *currency_options)
        currency_menu.configure(bg="#9400D3", fg="#FFFFFF", font=("Helvetica", 10))
        currency_menu.pack(pady=5)

        save_button = tk.Button(self, text="Зберегти", command=self.destroy, bg="#9400D3", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
        save_button.pack(pady=10)

class SavingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Мета заощаджень")
        self.configure(bg="#000000")

        label = tk.Label(self, text="Введіть суму мети заощаджень:", bg="#000000", fg="#FFFFFF")
        label.pack(pady=10)

        savings_entry = tk.Entry(self)
        savings_entry.pack(pady=5)

        confirm_button = tk.Button(self, text="Підтвердити", command=lambda: master.set_goal_amount(savings_entry.get(), self), bg="#9400D3", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
        confirm_button.pack(pady=10)

class ExpenseDetailsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Детальна інформація про витрати")
        self.configure(bg="#000000")

        for category, expenses in master.expense_details.items():
            text = f"{category}: {sum(expenses):.2f} {master.currency.get()}" if expenses else f"{category}: -"
            label = tk.Label(self, text=text, bg="#000000", fg="#FFFFFF", font=("Helvetica", 12))
            label.pack(pady=5)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

