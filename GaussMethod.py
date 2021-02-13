from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk

import numpy as np

from WindowPattern import WindowPattern


class GaussMethod(WindowPattern):
    number_var = 0

    def __init__(self):
        super().__init__("Gauss method")

    def _set_number_var(self, event=None):
        inp_str = self.spinbox.get()
        if not inp_str.isdigit():
            messagebox.showerror("Ошибка", "Ожидается ввод числа")
        elif int(inp_str) > 100 or int(inp_str) < 2:
            messagebox.showerror("Ошибка", "Ожидается число в диапазоне от 2 до 100")
        else:
            self.number_var = int(inp_str)
            self.dialog_window.destroy()
            self._build_matrix()

    def _new_command(self):
        self.dialog_window = tk.Tk()
        self.dialog_window.geometry("300x100")
        self.dialog_window.resizable(False, False)
        label = tk.Label(self.dialog_window, text="Введите количество уравнений в системе\n"
                                                  "Количество переменных должно быть равно\n"
                                                  " количеству уравнений, но не больше 100",
                         font=("Times new Roman", 10))
        label.pack()
        self.spinbox = tk.Spinbox(self.dialog_window, from_=2, to=100, width=7, font="10")
        self.spinbox.bind('<Return>', self._set_number_var)
        self.spinbox.pack()
        button = tk.Button(self.dialog_window, text="Ввод", command=self._set_number_var, font="10")
        button.pack()

    def _open_command(self):
        self.file = filedialog.askopenfilename(filetypes=(("Comma separate values", "*.csv"), ("all files", "*.*")))
        self._read_from_file()
        self._start_calculations(True)

    def _build_matrix(self):
        self._matrix = [[None for _ in range(0, self.number_var)] for _ in range(0, self.number_var)]
        self._answers = [None for _ in range(0, self.number_var)]

        for y in range(0, self.number_var):
            for x in range(0, self.number_var):
                self._matrix[y][x] = tk.StringVar()
                tk.Entry(textvariable=self._matrix[y][x], width=10).grid(row=y, column=x, padx=5, pady=5)

            self._answers[y] = tk.StringVar()
            tk.Entry(textvariable=self._answers[y], width=10).grid(row=y, column=self.number_var, padx=20, pady=5)

        tk.Button(text="Расчет", command=self._start_calculations, width=20). \
            grid(row=self.number_var, columnspan=self.number_var)

    def _read_from_file(self):
        with open(self.file, "r") as f:
            lines = f.readlines()
            size = len(lines)
            self._float_matrix = [[0.0 for _ in range(0, size)] for _ in range(0, size)]
            self._float_answers = []
            for line in range(0, len(lines)):
                l = lines[line].strip().split(',')
                for i in range(0, len(l)-1):
                    try:
                        tmp = float(l[i])
                    except ValueError:
                        messagebox.showerror("Ошибка", "Данные в файле повреждены")
                        return None
                    self._float_matrix[line][i] = tmp

                try:
                    tmp = float(l[len(l)-1])
                except ValueError:
                    return None
                self._float_answers.append(tmp)


    def _start_calculations(self, valid=False):
        if not valid:
            valid = self._check_valid()
        if valid:
            det = np.linalg.det(self._float_matrix)
            tk.Label(text="det = {}".format(round(det, 2))).grid(row=self.number_var + 1, columnspan=3)
            if det == 0:
                messagebox.showerror("Ошибка", "Определить равен нулю")
            else:
                for v in range(0, len(self._float_matrix)):
                    tmp = self._float_matrix[v][v]
                    for x in range(0, len(self._float_matrix[0])):
                        self._float_matrix[v][x] /= tmp
                    self._float_answers[v] /= tmp

                    for y in range(0, len(self._float_matrix)):
                        if y != v:
                            multiplier = self._float_matrix[y][v]
                            for x in range(0, len(self._float_matrix[0])):
                                self._float_matrix[y][x] -= self._float_matrix[v][x] * multiplier

                            self._float_answers[y] -= self._float_answers[v] * multiplier

                for i in range(0, len(self._float_answers)):
                    tk.Label(text="x{0} = {1}".format(i + 1, round(self._float_answers[i], 2))). \
                        grid(row=self.number_var + 2 + i, columnspan=3)
        else:
            messagebox.showerror("Ошибка", "Ожидается ввод числа")

    def _check_valid(self):
        self._float_matrix = [[0.0 for _ in range(0, self.number_var)] for _ in range(0, self.number_var)]
        self._float_answers = [0.0 for _ in range(0, self.number_var)]
        for y in range(0, len(self._matrix)):
            for x in range(0, len(self._matrix[y])):
                try:
                    tmp = float(self._matrix[y][x].get())
                except ValueError:
                    return False
                self._float_matrix[y][x] = tmp

        for i in range(0, len(self._answers)):
            try:
                tmp = float(self._answers[i].get())
            except ValueError:
                return False
            self._float_answers[i] = tmp

        return True
