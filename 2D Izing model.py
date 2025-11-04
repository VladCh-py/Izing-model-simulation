import numpy as np
import matplotlib.pyplot as plt
from random import random
# Параметры модели
L = 40  # Размер решетки
J = 2.0  # Обменное взаимодействие
kT = 4 # Температура в единицах kT

H_max = 3  # Максимальное значение магнитного поля
H_min = -H_max  # Минимальное значение магнитного поля

Steps = 100  # Количество шагов изменения поля
Steps_Monte_carlo=4000
# yes  / no
simulation_run="yes"
# инициализация размагниченной решетки
lattice = np.zeros((L, L))
for i in range(L):
    for j in range(L):
        lattice[i, j] = 1 if random() < 0.5 else -1

def spins_draw(spins, title, H, magnetization, clear):
    plt.subplot(1, 2, 1)
    plt.title("Гистерезис")
    plt.scatter(H, magnetization, color='black')
    plt.scatter(H[-1], magnetization[-1], color='red')
    plt.ylim(-1.1, 1.1)
    plt.xlim(-H_max-0.1*H_max, H_max+0.1*H_max)
    plt.xlabel('Напряженность внешнего магнитного поля (H)')
    plt.ylabel('Намагниченность (M)')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.title(title)
    plt.imshow(spins, cmap='gnuplot2')
    

    plt.pause(0.1)
    plt.draw()
    if clear!="no": plt.clf()

# Размагничивание
def demagnitisation(spins, l):
    for i in range(l):
        for j in range(l):
            spins[i, j] = 1 if (i + j) % 2 == 0 else -1
    return spins
# Шаг Монте-Карло
def monyte_carlo_step(spins, h):
    x, y = np.random.randint(0, L, size=2)
    delta_E = 2 * J * spins[x, y] * (spins[(x+1)%L, y] + spins[x, (y+1)%L] + spins[(x-1)%L, y] + spins[x, (y-1)%L]) + 2 * h * spins[x, y]
    if delta_E < 0 or np.random.rand() < np.exp(-delta_E / kT):
        spins[x, y] *= -1
    return spins

# Функция для вычисления намагниченности
def simulation(h_max, h_min, spins, size, steps, type):

    if type=="Histeresis":
        magnetization = []
        H=[]

        fields = np.linspace(0, h_max,  steps)
        for h in fields:  # Проходим по всем значениям поля
            # Обновление спинов (простая модель Метрополиса)
            for _ in range(Steps_Monte_carlo):  # Количество итераций
                monyte_carlo_step(spins, h)

            # magnetization.append(np.sum(spins) / (size * size))
            # H.append(h)
            # plt.scatter(h, magnetization, color='black')
            # spins_draw(spins, title="0-->H_max")

        fields = np.linspace(h_max, h_min,  steps)  # Обратный порядок
        for h in fields:  # Проходим по всем значениям поля
            # Обновление спинов (простая модель Метрополиса)
            for _ in range(Steps_Monte_carlo):  # Количество итераций
                monyte_carlo_step(spins, h)

            magnetization.append(np.sum(spins) / (size * size))
            H.append(h)
            
            if simulation_run=="yes": spins_draw(spins, title="H_max-->H_min", H=H, magnetization=magnetization, clear="yes")

        fields = np.linspace(h_min, h_max,  steps) 
        for h in fields:  # Проходим по всем значениям поля
            # Обновление спинов (простая модель Метрополиса)
            for _ in range(Steps_Monte_carlo):  # Количество итераций
                monyte_carlo_step(spins, h)

            magnetization.append(np.sum(spins) / (size * size))
            H.append(h)

            if simulation_run=="yes": spins_draw(spins, title="H_min-->H_max", H=H, magnetization=magnetization, clear="yes")

    # если хотим отрисовать Кривую
    if type=="Curve":
        magnetization = []
        H=[]
        # сначала размагничиваем
        spins=demagnitisation(spins, size)
# идем от нуля к минимуму
        fields = np.linspace(0, h_min, steps)  # Обратный порядок
        for h in fields:  # Проходим по всем значениям поля
            # Обновление спинов (простая модель Метрополиса)
            for _ in range(Steps_Monte_carlo):  # Количество итераций
                monyte_carlo_step(spins, h)

            magnetization.insert(0, np.sum(spins) / (size * size))
            H.insert(0, h)
        
        spins=demagnitisation(spins, size)

        fields = np.linspace(0, h_max,  steps)  # Обратный порядок
        for h in fields:  # Проходим по всем значениям поля
            # Обновление спинов (простая модель Метрополиса)
            for _ in range(Steps_Monte_carlo):  # Количество итераций
                monyte_carlo_step(spins, h)

            magnetization.append(np.sum(spins) / (size * size))
            H.append(h)
    if simulation_run=="yes": spins_draw(spins, title="H_min-->H_max", H=H, magnetization=magnetization, clear="no")
        

        

    return magnetization, H




# Вычисление намагниченности           Histeresis    Curve
magnetization, H = simulation(H_max, H_min, lattice, L, Steps, type="Histeresis")
magnetization2, H2 = simulation(H_max, H_min, lattice, L, Steps, type="Curve")
# Построение графика
plt.figure(figsize=(7, 7))
plt.scatter(H, magnetization, color='black')
plt.scatter(H2, magnetization2, color='red')
plt.title('Симуляция 2Д модели Изинга')
plt.xlabel('Напряженность внешнего магнитного поля (H)')
plt.ylabel('Намагниченность (M)')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.grid()
plt.show()