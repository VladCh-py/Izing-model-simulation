import numpy as np  # Импортируем библиотеку NumPy для работы с массивами
import matplotlib.pyplot as plt  # Импортируем библиотеку Matplotlib для визуализации
'''
Данная программа позволяет проводить симуляцию 1 размерной модели Изинга методом Монте-Карло.
Главный класс "IsingModel" содержит все необходимые параметры исследуемого намагничиваемого образца, значения внешнего магнитного поля и количества шагов симуляции.
В результате работы программа отображает петлю гистерезиса и главную кривую намагничивания. Возможно изменить количество точек намагничиваемого образца и внешнего магнит-
ного поля.
'''

class IsingModel:
    def __init__(self, size, steps, min_field, max_field):
        self.size = size  # Устанавливаем размер модели
        self.steps = steps  # Устанавливаем количество шагов симуляции
        self.min_field = min_field  # Устанавливаем минимальное значение внешнего поля
        self.max_field = max_field  # Устанавливаем максимальное значение внешнего поля
        self.spins = np.random.choice([-1, 1], size=self.size)  # Инициализируем спины случайным образом
        self.magnetization = []  # Список для хранения значений намагниченности
        self.magnetization_memory=[]

    def calculate_magnetization(self):
        return np.sum(self.spins) / self.size  # Рассчитываем намагниченность

    def monte_carlo_step(self, external_field):
        for _ in range(self.size):  # Проходим по всем спинам
            i = np.random.randint(0, self.size)  # Случайно выбираем индекс спина
            delta_energy = 2 * self.spins[i] * (external_field + self.spins[(i + 1) % self.size] + self.spins[(i - 1) % self.size])  # Рассчитываем изменение энергии
            if delta_energy < 0 or np.random.rand() < np.exp(-delta_energy):  # Условие для изменения спина
                self.spins[i] *= -1  # Инвертируем спин

    def demagnitization(self):
        for i in range(self.size):  # Проходим по всем спинам
            self.spins[i] = (-1)**i  # Инвертируем спин
        # print(self.spins)

    def run_simulation(self, type):
        if type=="Hist":
            # эта часть нужна, чтобы намагнитить образец до максимума
            fields = np.linspace(0, self.max_field,  self.steps)  # Обратный порядок
            for field in fields:  # Проходим по всем значениям поля
                self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
            
            fields = np.linspace(self.max_field, self.min_field, self.steps)  # Обратный порядок
            for field in fields:  # Проходим по всем значениям поля
                self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
                self.magnetization.append(self.calculate_magnetization())  # Сохраняем намагниченность
            
            fields = np.linspace(self.min_field, self.max_field, self.steps)  # Обратный порядок
            for field in fields:  # Проходим по всем значениям поля
                self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
                self.magnetization.append(self.calculate_magnetization())  # Сохраняем намагниченность

            # fields = np.concatenate((np.linspace(self.min_field, self.max_field, self.steps),  # Генерируем массив значений внешнего поля
            #                         np.linspace(self.max_field, self.min_field, self.steps)))  # Обратный порядок
            # for field in fields:  # Проходим по всем значениям поля
            #     self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
            #     self.magnetization.append(self.calculate_magnetization())  # Сохраняем намагниченность
            self.magnetization_memory=self.magnetization

        if type=="Curve":
            self.magnetization = []

            self.demagnitization()

            fields = np.linspace(0, self.min_field,  self.steps)  # Обратный порядок
            for field in fields:  # Проходим по всем значениям поля
                self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
                self.magnetization.insert(0, self.calculate_magnetization())  # Сохраняем намагниченность
                
            self.demagnitization()            
            
            fields = np.linspace(0, self.max_field, self.steps)  # Обратный порядок
            print(len(fields))
            for field in fields:  # Проходим по всем значениям поля
                self.monte_carlo_step(field)  # Выполняем шаг Монте-Карло
                self.magnetization.append(self.calculate_magnetization())  # Сохраняем намагниченность

    def plot_hysteresis(self, type):
        if type == "Hist":
            plt.plot(np.concatenate((np.linspace(self.max_field, self.min_field, self.steps),  # Визуализируем гистерезис
                                    np.linspace(self.min_field, self.max_field, self.steps))),
                    self.magnetization_memory)  # Строим график
            plt.title('Петля гистерезиса')  # Заголовок графика
            plt.xlabel('Напряженность внешнего магнитного поля')  # Подпись оси X
            plt.ylabel('Намагниченность')  # Подпись оси Y
            plt.axhline(0, color='black', lw=0.5, ls='--')
            plt.axvline(0, color='black', lw=0.5, ls='--')
            plt.grid()  # Включаем сетку
            plt.show()  # Отображаем график
        
        if type == "Curve":
            plt.scatter(np.linspace(self.min_field, self.max_field, self.steps*2), self.magnetization)  # Строим график
            plt.title('Главная кривая намагниченности')  # Заголовок графика
            plt.xlabel('Напряженность внешнего магнитного поля')  # Подпись оси X
            plt.ylabel('Намагниченность')  # Подпись оси Y
            plt.axhline(0, color='black', lw=0.5, ls='--')
            plt.axvline(0, color='black', lw=0.5, ls='--')
            plt.grid()  # Включаем сетку
            plt.show()  # Отображаем график

        if type == "Both":
            plt.scatter(np.linspace(self.min_field, self.max_field, self.steps*2), self.magnetization, label="Главная кривая намагниченности", color="red", s=5)  # Строим график
            plt.scatter(np.concatenate((np.linspace(self.max_field, self.min_field, self.steps),  # Визуализируем гистерезис
                                    np.linspace(self.min_field, self.max_field, self.steps))),
                    self.magnetization_memory, label="Гистерезис", color="black", s=5)  # Строим график
            plt.title('Симуляция 1Д модели Изинга')  # Заголовок графика
            plt.xlabel('Напряженность внешнего магнитного поля')  # Подпись оси X
            plt.ylabel('Намагниченность')  # Подпись оси Y
            plt.legend()
            plt.axhline(0, color='black', lw=0.5, ls='--')
            plt.axvline(0, color='black', lw=0.5, ls='--')
            plt.grid()  # Включаем сетку
            plt.show()  # Отображаем график


# Параметры модели
size = 5000  # Размер модели
steps = 100  # Количество шагов
min_field = -0.3  # Минимальное значение внешнего поля
max_field = 0.3  # Максимальное значение внешнего поля


# Создание и запуск модели
ising_model = IsingModel(size, steps, min_field, max_field)  # Инициализация модели

ising_model.run_simulation(type="Hist")  # Запуск симуляции

ising_model.plot_hysteresis(type="Hist")  # Визуализация результатов

ising_model.demagnitization() #


ising_model.run_simulation(type="Curve")  # Запуск симуляции
ising_model.plot_hysteresis(type="Curve")  # Визуализация результатов

ising_model.plot_hysteresis(type="Both")  # Визуализация результатов
