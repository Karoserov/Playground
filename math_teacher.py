import tkinter as tk
from tkinter import messagebox
import random
from math import pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Показване на графика
def show_graph(task_type):
    if task_type == "Геометрия":
        radius = random.randint(1, 10)
        figure, ax = plt.subplots()
        circle = plt.Circle((0, 0), radius, color='blue', fill=False)
        ax.add_patch(circle)
        ax.set_xlim(-radius - 1, radius + 1)
        ax.set_ylim(-radius - 1, radius + 1)
        ax.set_aspect('equal')
        ax.set_title(f"Кръг с радиус {radius}")

        graph_window = tk.Toplevel(root)
        graph_window.title("Графична визуализация")
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showinfo("Графика", "Няма графична визуализация за този тип задача.")


# Показване на решението стъпка по стъпка
def show_step_by_step(solution_steps):
    step_window = tk.Toplevel(root)
    step_window.title("Решение стъпка по стъпка")

    step_label = tk.Label(step_window, text="Стъпки на решението:", font=("Arial", 14))
    step_label.pack(pady=10)

    for step in solution_steps:
        step_text = tk.Label(step_window, text=step, font=("Arial", 12), anchor="w", justify="left")
        step_text.pack(padx=10, pady=5)


# Проверка на отговор
def check_answer(correct_answer, task_type):
    def validate_answer():
        user_answer = float(answer_entry.get())
        if abs(user_answer - correct_answer) < 0.01:  # Толеранс за закръгляне
            messagebox.showinfo("Резултат", "Поздравления! Отговорът е правилен.")
        else:
            messagebox.showerror("Грешка", f"Грешен отговор. Правилният е {correct_answer:.2f}.")

    answer_window = tk.Toplevel(root)
    answer_window.title("Проверка на отговор")

    tk.Label(answer_window, text=f"Въведете вашия отговор за {task_type}:", font=("Arial", 12)).pack(pady=10)
    answer_entry = tk.Entry(answer_window, font=("Arial", 12))
    answer_entry.pack(pady=5)
    tk.Button(answer_window, text="Проверете", command=validate_answer).pack(pady=10)


# Функция за генериране на задачи
def generate_task(task_type):
    if task_type == "Уравнения":
        a, b = random.randint(1, 10), random.randint(1, 10)
        solution = b / a
        steps = [
            f"Дадено уравнение: {a}x = {b}",
            f"Разделяме двете страни на {a}: x = {b}/{a}",
            f"Изчисляваме: x = {solution:.2f}"
        ]
        task_label.config(text=f"Намерете x: {a}x = {b}")
        solution_button.config(command=lambda: show_step_by_step(steps))
        check_button.config(command=lambda: check_answer(solution, "Уравнения"))
        graph_button.config(command=lambda: show_graph(task_type))
    elif task_type == "Геометрия":
        radius = random.randint(1, 10)
        area = pi * radius ** 2
        steps = [
            f"Дадено: радиус r = {radius} см",
            "Формулата за лице на кръг: S = πr²",
            f"Заместваме: S = π({radius})²",
            f"Изчисляваме: S = {area:.2f} см²"
        ]
        task_label.config(text=f"Намерете лицето на кръг с радиус {radius} см")
        solution_button.config(command=lambda: show_step_by_step(steps))
        check_button.config(command=lambda: check_answer(area, "Геометрия"))
        graph_button.config(command=lambda: show_graph(task_type))
    elif task_type == "Дроби":
        numerator, denominator = random.randint(1, 10), random.randint(1, 10)
        solution = numerator / denominator
        steps = [
            f"Дадена дроб: {numerator}/{denominator}",
            f"Разделяме числителя на знаменателя: {numerator} ÷ {denominator}",
            f"Резултат: {solution:.2f}"
        ]
        task_label.config(text=f"Определете: {numerator}/{denominator} = ?")
        solution_button.config(command=lambda: show_step_by_step(steps))
        check_button.config(command=lambda: check_answer(solution, "Дроби"))
        graph_button.config(command=lambda: show_graph(task_type))
    else:
        task_label.config(text="Изберете тип задача!")
        solution_button.config(command=lambda: None)
        check_button.config(command=lambda: None)
        graph_button.config(command=lambda: None)


# Основен прозорец
root = tk.Tk()
root.title("Математически помощник за 5-7 клас")

# Бутони за избор на тип задача
task_type_label = tk.Label(root, text="Изберете тип задача:", font=("Arial", 14))
task_type_label.pack(pady=10)

btn_equations = tk.Button(root, text="Уравнения", command=lambda: generate_task("Уравнения"))
btn_geometry = tk.Button(root, text="Геометрия", command=lambda: generate_task("Геометрия"))
btn_fractions = tk.Button(root, text="Дроби", command=lambda: generate_task("Дроби"))

btn_equations.pack(pady=5)
btn_geometry.pack(pady=5)
btn_fractions.pack(pady=5)

# Полета за задачи и бутони за взаимодействие
task_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
task_label.pack(pady=10)

solution_button = tk.Button(root, text="Покажи решението", font=("Arial", 12))
solution_button.pack(pady=10)

check_button = tk.Button(root, text="Проверете отговор", font=("Arial", 12))
check_button.pack(pady=10)

graph_button = tk.Button(root, text="Визуализирай графика", font=("Arial", 12))
graph_button.pack(pady=10)

# Стартиране на интерфейса
root.mainloop()
