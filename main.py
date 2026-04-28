import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("700x500")
        
        self.trainings = self.load_data()
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # --- Секция ввода ---
        input_frame = tk.LabelFrame(self.root, text="Добавить тренировку", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.entry_date = tk.Entry(input_frame)
        self.entry_date.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Тип:").grid(row=0, column=2)
        self.entry_type = ttk.Combobox(input_frame, values=["Силовая", "Кардио", "Йога", "Плавание"])
        self.entry_type.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Мин:").grid(row=0, column=4)
        self.entry_duration = tk.Entry(input_frame, width=10)
        self.entry_duration.grid(row=0, column=5, padx=5)

        btn_add = tk.Button(input_frame, text="Добавить", command=self.add_training, bg="#4CAF50", fg="white")
        btn_add.grid(row=0, column=6, padx=10)

        # --- Секция фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Тип:").grid(row=0, column=0)
        self.filter_type = tk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1, padx=5)
        self.filter_type.bind("<KeyRelease>", lambda e: self.refresh_table())

        tk.Label(filter_frame, text="Дата:").grid(row=0, column=2)
        self.filter_date = tk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=3, padx=5)
        self.filter_date.bind("<KeyRelease>", lambda e: self.refresh_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(self.root, columns=("Date", "Type", "Duration"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип тренировки")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_training(self):
        date_str = self.entry_date.get()
        t_type = self.entry_type.get()
        duration_str = self.entry_duration.get()

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            duration = int(duration_str)
            if duration <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты (ДД.ММ.ГГГГ) или длительности (>0)")
            return

        if not t_type:
            messagebox.showwarning("Внимание", "Выберите тип тренировки")
            return

        new_training = {"date": date_str, "type": t_type, "duration": duration}
        self.trainings.append(new_training)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.entry_duration.delete(0, tk.END)

    def refresh_table(self):
        # Очистка
        for item in self.tree.get_children():
            self.tree.delete(item)

        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get().lower()

        # Отображение с фильтром
        for t in self.trainings:
            if f_type in t['type'].lower() and f_date in t['date'].lower():
                self.tree.insert("", tk.END, values=(t['date'], t['type'], t['duration']))

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
