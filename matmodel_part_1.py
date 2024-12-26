import numpy as np
import matplotlib.pyplot as plt

def g(h):
    R_earth = 6000e3
    g0 = 9.81
    return g0 * (R_earth / (R_earth + h))**2

def rho(h):
    rho0 = 1.225
    H = 8500
    return rho0 * np.exp(-h / H)

def rocket_stage_params(stage):
    """Параметры ракеты для каждой ступени: [тяга, масса топлива, масса конструкции, Cd, A, Isp]"""
    stages = [
        [1500000, 150000, 10000, 0.5, 10, 300],
        [800000, 50000, 5000, 0.5, 8, 320],
        [300000, 20000, 3000, 0.5, 6, 340],
        [100000, 5000, 1000, 0.5, 4, 350]
    ]
    return stages[stage]

def rocket_dynamics(t, y, F, Isp, A, Cd):
    """Сама система дифференциальных уравнений."""
    v, h, m = y
    dvdt = F / m - g(h) - (rho(h) * v**2 * Cd * A) / (2 * m)
    dhdt = v
    dmdt = -F / (Isp * 9.81)
    return np.array([dvdt, dhdt, dmdt])

def runge_kutta4(f, t0, y0, tf, dt, stages):
    t = [t0]
    y = [y0]
    current_stage = 0
    F, mfuel, mstruct, Cd, A, Isp = rocket_stage_params(current_stage)
    m = y0[2] + mfuel + mstruct

    while t[-1] < tf and y[-1][1] < 200e3:
        if m - mstruct <= 0 and current_stage < len(stages) - 1:
            current_stage += 1
            F, mfuel, mstruct, Cd, A, Isp = rocket_stage_params(current_stage)
            m = mstruct + mfuel

        k1 = dt * f(t[-1], y[-1], F, Isp, A, Cd)
        k2 = dt * f(t[-1] + dt/2, y[-1] + k1/2, F, Isp, A, Cd)
        k3 = dt * f(t[-1] + dt/2, y[-1] + k2/2, F, Isp, A, Cd)
        k4 = dt * f(t[-1] + dt, y[-1] + k3, F, Isp, A, Cd)

        y_next = y[-1] + (k1 + 2*k2 + 2*k3 + k4) / 6
        y_next[2] = max(y_next[2], 0)
        t.append(t[-1] + dt)
        y.append(y_next)

    return np.array(t), np.array(y)

# Начальные параметры
v0 = 0  # Начальная скорость, м/с
h0 = 0  # Начальная высота, м
m0 = 10000  # Масса полезной нагрузки, кг

t0, tf, dt = 0, 500, 0.1  # Время старта, конец и шаг интегрирования
stages = [0, 1, 2, 3]  # Индексы ступеней

y0 = np.array([v0, h0, m0])
t, y = runge_kutta4(rocket_dynamics, t0, y0, tf, dt, stages)

plt.figure()
plt.plot(t, y[:, 0])
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.title('График скорости от времени')
plt.grid()

plt.figure()
plt.plot(t, y[:, 2])
plt.xlabel('Время (с)')
plt.ylabel('Масса (кг)')
plt.title('График массы от времени')
plt.grid()

plt.show()
