import tkinter as tk
from ErrorCatcher import CatchFloatError as cfe
from math import sqrt, ceil
from tkinter.filedialog import *
import copy
from itertools import combinations


class Graph:
    def __init__(self, parent):
        self.parent = parent
        parent.title('Triangle')
        self.canv_width = 200
        self.canv_height = 200
        self.width = 600
        self.height = 700
        self.x1 = 10
        self.x2 = 410
        self.y1 = 10
        self.y2 = 660
        self.center_x = (self.x2 - self.x1) // 2 + self.x1
        self.center_y = (self.y2 - self.y1) // 2 + self.y1

        self.parent.resizable(width=False, height=False)  # запрет на изменение размера

        self.canvas = tk.Canvas(root, height=self.height,
                                width=self.width, bg='light grey')
        self.canvas.grid(row=0, column=0)
        self.canvas.create_rectangle(self.x1 - 10, self.y1 - 10,
                                     self.x2 + 10, self.y2 + 10,
                                     fill='white',
                                     outline='white')

        self.canvas.create_text(450, 25, text='Введите координаты \n через пробел:',
                                anchor='w')

        self.add_button = tk.Button(self.canvas, text='Add')
        self.add_button.bind('<Button-1>', self.getter)
        self.add_button.place(x=550, y=50)

        self.add_entry = tk.Entry(self.canvas, width=10, bd=3)
        self.add_entry.bind('<Return>', self.getter)
        self.add_entry.place(x=450, y=50)
        # self.add_entry.bind('<Return>', lambda e: self.getter)

        self.show_button = tk.Button(self.canvas, text='Show graph')
        self.show_button.bind('<Button-1>', self.point_drawer)
        self.show_button.place(x=450, y=110)

        self.clear_button = tk.Button(self.canvas, text='Clear all')
        self.clear_button.bind('<Button-1>', self.clear_all)
        self.clear_button.place(x=450, y=640)

        self.text = tk.Text(root, width=15, height=30)
        self.text.place(x=450, y=150)
        self.text.config(takefocus=0)

        self.canvas.create_rectangle(450, 80, 600, 100, fill='light green',
                                     outline='light green')

        self.coords_str = ''
        self.normal_coords = []
        self.min_coords = []


    def getter(self, event):
        self.canvas.create_rectangle(450, 80, 600, 100, fill='light green',
                                     outline='light green')
        # Каждый раз при нажатии на кнопку Add рисуется зеленый индикатор
        # Если ввод некорректный, рисуется красный индикатор

        new_coords = self.add_entry.get() # Строка с введенными пользоавтелем данными

        f = 0 # флаг для попытки преобразовать введенные данные в координаты типа float
        new_coords = new_coords.strip() # удаляем лишние знаки по краям строки

        for i in range(len(new_coords)): # пытаемся сделать сплит по пробелу
            if new_coords[i] == ' ':
                if f != 0:
                    f = 1
                else:
                    f = 2
        if f != 2: # сплит по пробелу не получился
            self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                         outline='pink')
            self.canvas.create_text(450, 90, text='Некорректный ввод', anchor='w')
        else:  # сплит по пробелу получился
            x, y = new_coords.split()
            x = cfe(x)
            y = cfe(y) # пытаемся преобразовать координаты в тип float с помощью ErrorCatcher
            if type(x) != float or type(y) != float:
                self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                             outline='pink')
                self.canvas.create_text(450, 90, text='Некорректный ввод', anchor='w')
            else: # удалось преобразовать координаты в тип float
                new_coords_arr = [] # создаем массив, записываем туда новые координаты
                new_coords_arr.append(x)
                new_coords_arr.append(y)
                # смотрим, не ввел ли пользователь одну и ту же точку несколько разd(y)
                if new_coords_arr in self.normal_coords:
                    self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                                 outline='pink')
                    self.canvas.create_text(450, 90, text='Эта точка уже есть', anchor='w')
                else:
                    self.coords_str += new_coords + '\n'
                    self.normal_coords.append([x, y])

        self.add_entry.delete(0, END) # удаляем символы из поля ввода
        self.shower(self) # переносим все координаты в поле вывода
        # если новые коориднаты были введены без ошибки, их тоже выводим
        # если с ошибкой - выводим список старых координат


    def shower(self, event):
        self.text.delete('1.0', END)
        self.text.insert(END, self.coords_str)


    def clear_all(self, event):
        #отчищает все поля
        self.coords_str = ''
        self.normal_coords = []
        self.shower(self.coords_str)
        self.canvas.create_rectangle(self.x1 - 10, self.y1 - 10,
                                     self.x2 + 10, self.y2 + 10,
                                     fill='white',
                                     outline='white')
        self.min_coords = []

    def point_drawer(self, event):
        # рисует все точки, введенные пользователем
        # если точек больше трех и они не лежат на одной прямой,
        # вызывает функцию, которая выбирает точки для треугольника
        if len(self.normal_coords) != 0: # если пользователь ввел хотя бы  одну точку, а не просто тыкнул на кнопку
            self.canvas.create_rectangle(self.x1 - 10, self.y1 - 10,
                                         self.x2 + 10, self.y2 + 10,
                                         fill='white',
                                         outline='white')

            # считаем коэффицент для масштабирования
            # отдельно для x, отдельно для y
            # из этих двух коэффицентов выбирается минимальный
            x_max = abs(self.normal_coords[0][0])
            y_max = abs(self.normal_coords[0][1])
            for i in range(len(self.normal_coords)):
                if abs(self.normal_coords[i][0]) > x_max:
                    x_max = abs(self.normal_coords[i][0])
                if abs(self.normal_coords[i][1]) > y_max:
                    y_max = abs(self.normal_coords[i][1])
            self.l_x = self.center_x - self.x1
            self.l_y = self.center_y - self.y1
            if x_max >= 1:
                x_max += 1
            else:
                x_max += 0.1
            if y_max >= 1:
                y_max += 1
            else:
                y_max += 0.1
            kf_x = self.l_x / x_max
            kf_y = self.l_y / y_max
            self.kf = min(kf_x, kf_y)
            self.kf = round(self.kf, 6)

            # пересчитываем координаты из ДСК в координатную систему холста
            for i in range(len(self.normal_coords)):
                x = self.normal_coords[i][0]
                if abs(x) > self.l_x:
                    x = ceil(x * self.kf)

                else:
                    if self.kf != 0:
                        x = ceil(x * self.kf)

                y = self.normal_coords[i][1]
                if abs(y) > self.l_y:
                    y = ceil(y * self.kf)
                else:
                    if self.kf != 0:
                        y = ceil(y * self.kf)

                x += self.center_x
                if y > 0:
                    y = self.center_y - y
                else:
                    y = self.center_y + abs(y)

                # рисуем точки в форме плюсиков
                self.canvas.create_line(x - 5, y,
                                        x + 5, y,
                                        width=1)
                self.canvas.create_line(x, y - 5,
                                        x, y + 5,
                                        width=1)
            # если точек больше трех, вызываем функцию, которая будет пытаться выбрать три точки для треугольника
            if len(self.normal_coords) >= 3:
                self.choose_points(self)
        else:
            self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                         outline='pink')
            self.canvas.create_text(450, 90, text='Вы не ввели точки', anchor='w')


    def coords_ch(self, st):
        # функция преобразует координаты из ДКС в координаты холста
        # надо бы ее еще в point_drawer применить, но мне лень
        if st[0] > self.l_x:
            st[0] = ceil(st[0] * self.kf)
        else:
            if self.kf != 0:
                st[0] = ceil(st[0] * self.kf)

        if st[1] > self.l_y:
            st[1] = ceil(st[1] * self.kf)
        else:
            if self.kf != 0:
                st[1] = ceil(st[1] * self.kf)

        st[0] += self.center_x
        if st[1] > 0:
            st[1] = self.center_y - st[1]
        else:
            st[1] = self.center_y + abs(st[1])

        return st


    def triangle_drawer(self, event):
        # рисует треугольник
        if len(self.min_coords) != 0:
            p1 = copy.deepcopy(self.min_coords[0])
            p2 = copy.deepcopy(self.min_coords[1])
            p3 = copy.deepcopy(self.min_coords[2])
            p1 = self.coords_ch(p1)
            p2 = self.coords_ch(p2)
            p3 = self.coords_ch(p3)
            self.canvas.create_line(p1[0], p1[1],
                                    p2[0], p2[1],
                                    width=1)
            self.canvas.create_line(p1[0], p1[1],
                                    p3[0], p3[1],
                                    width=1)
            self.canvas.create_line(p2[0], p2[1],
                                    p3[0], p3[1],
                                    width=1)
        else:
            self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                         outline='pink')
            self.canvas.create_text(450, 90, text='Теругольника нет', anchor='w')


    def choose_points(self, event):
        # ищем комбинацию из трех точек, где разница минимальна
        # проверяем, не лежат ли все введенные точки на одной прямой
        min_dif = 1 # минимальная разность
        flag_min_dif = 0 # флаг для того, чтобы при первом вычислении текущей разности не сравниавть ее с минимальной
        fd = 0  # флаг на ошибку, если точки лежат на одной прямой
        combs = list(combinations(self.normal_coords, 3)) # массив массивов массивов;
        # все возможные комбинации введеных точек с длиной 3
        # они еще и повторяются по три раза каждая
        # дальше какая-то дичь сам не понял лучше не смотрите
        # но оно работает
        # почти всегда
        for i in range(len(combs)):
            point1 = combs[i][0]
            point2 = combs[i][1]
            point3 = combs[i][2]
            points_out = 0
            points_in = 0
            if not flag_min_dif:
                self.min_coords.append(point1)
                self.min_coords.append(point2)
                self.min_coords.append(point3)
            a = round(sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2)), 4)
            b = round(sqrt(((point3[0] - point1[0]) ** 2) + ((point3[1] - point1[1]) ** 2)), 4)
            c = round(sqrt(((point3[0] - point2[0]) ** 2) + ((point3[1] - point2[1]) ** 2)), 4)
            if a + b > c and a + c > b and b + c > a:
                fd = 1
                #print(combs[i])
                for t in range(len(self.normal_coords)):
                    cur_point = self.normal_coords[t]
                    if cur_point != point1 and \
                                    cur_point != point2 and \
                                    cur_point != point3:
                        x = cur_point[0]
                        y = cur_point[1]
                        xa = point1[0]
                        ya = point1[1]
                        xb = point2[0]
                        yb = point2[1]
                        xc = point3[0]
                        yc = point3[1]
                        S = round(abs((xa - xc) * (yb - yc) - (xb - xc) * (ya - yc)) / 2, 2)
                        S1 = round(abs((xa - x) * (yb - y) - (xb - x) * (ya - y)) / 2, 2)
                        S2 = round(abs((xa - x) * (yc - y) - (xc - x) * (ya - y)) / 2, 2)
                        S3 = round(abs((xb - x) * (yc - y) - (xc - x) * (yb - y)) / 2, 2)
                        if S1 + S2 + S3 == S:
                            h1 = (x - xa) * (ya - yb) - (y - ya) * (xa - xb) == 0
                            h2 = (x - xb) * (yb - yc) - (y - yb) * (xb - xc) == 0
                            h3 = (x - xc) * (yc - ya) - (y - ya) * (xc - xa) == 0

                            if (h1 > 0 and h2 >0 and h3 > 0) or \
                               (h1 < 0 and h2 < 0 and h3 < 0):
                                points_in += 1
                                #print(self.normal_coords[t], 'IN')
                            else:
                                #print(self.normal_coords[t], 'ON')
                                pass

                                

                        else:
                            points_out += 1
                            #print(self.normal_coords[t], 'OUT')
                #print(points_in, points_out)
                cur_dif = abs(points_out - points_in)
                if not flag_min_dif:
                    # если считаем разность первый раз и сравнивать не с чем
                    min_dif = cur_dif
                    flag_min_dif = 1
                    self.min_coords = []
                    self.min_coords.append(point1)
                    self.min_coords.append(point2)
                    self.min_coords.append(point3)

                else:
                    if cur_dif < min_dif:
                        min_dif = cur_dif
                        self.min_coords = []
                        self.min_coords.append(point1)
                        self.min_coords.append(point2)
                        self.min_coords.append(point3)
                        if min_dif == 0: # если разность 0, то дальше искать нет смысла
                            break
        if fd:
            self.triangle_drawer(self)
        else:
            self.canvas.create_rectangle(450, 80, 600, 100, fill='pink',
                                         outline='pink')
            self.canvas.create_text(450, 90, text='Это прямая', anchor='w')


root = tk.Tk()
graph = Graph(root)
root.mainloop()
