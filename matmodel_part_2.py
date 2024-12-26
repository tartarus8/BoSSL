import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
M_planet = 5,2915793e22  # Масса планеты (Земля), кг
R_planet = 6000  # Радиус планеты, м
h1 = 200000  # Высота начальной орбиты, м
h2 = 384400000 - R_planet  # Высота орбиты апогея (примерно расстояние до Луны), м
h3 = 100000  # Финальная круговая орбита, м


def orbital_velocity(radius):
    return np.sqrt(G * M_planet / radius)

def delta_v1(h1, h2):
    r1 = R_planet + h1
    r2 = R_planet + h2
    a = (r1 + r2) / 2
    v_peri = np.sqrt(G * M_planet * (2 / r1 - 1 / a))
    v_start = orbital_velocity(r1)
    return v_peri - v_start

def delta_v2(h2, h3):
    r2 = R_planet + h2
    r3 = R_planet + h3
    v_apo = np.sqrt(G * M_planet * (2 / r2 - 1 / ((r2 + r3) / 2)))
    v_circular = orbital_velocity(r3)
    return v_circular - v_apo

def maneuver_time(a):
    return np.pi * np.sqrt(a**3 / (G * M_planet))

# Начальные расчеты
r1 = R_planet + h1
r2 = R_planet + h2
r3 = R_planet + h3
a1 = (r1 + r2) / 2
a2 = (r2 + r3) / 2

dv1 = delta_v1(h1, h2)
dv2 = delta_v2(h2, h3)
t1 = maneuver_time(a1)
t2 = maneuver_time(a2)

print("\u0394v1 (переход на эллиптическую орбиту):", dv1, "м/с")
print("\u0394v2 (захват в круговую орбиту):", dv2, "м/с")
print("Время маневра 1:", t1, "с")
print("Время маневра 2:", t2, "с")

# Численный метод (Рунге-Кутта) для построения графиков

def simulate_transfer(h1, h2, h3, dt):
    time = [0]
    velocities = [orbital_velocity(R_planet + h1)]
    masses = [100000]  # Примерная начальная масса аппарата, кг

    r_current = R_planet + h1
    v_current = orbital_velocity(r_current)
    m_current = masses[0]

    while time[-1] < t1 + t2:
        if time[-1] < t1:
            # Фаза 1: Ускорение до v_peri
            dv = dv1 / t1 * dt
        elif time[-1] < t1 + t2:
            # Фаза 2: Ускорение до v_circular
            dv = dv2 / t2 * dt
        else:
            dv = 0

        v_current += dv
        m_current -= 15 * abs(dv)  # Примерный расход топлива
        r_current = R_planet + h1 if time[-1] < t1 else R_planet + h3

        time.append(time[-1] + dt)
        velocities.append(v_current)
        masses.append(m_current)

    return np.array(time), np.array(velocities), np.array(masses)

# Симуляция
dt = 10  # Шаг по времени, с
time, velocities, masses = simulate_transfer(h1, h2, h3, dt)

# Построение графиков
plt.figure(figsize=(10, 5))
plt.plot(time, velocities, label="Velocity", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity vs Time")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(time, masses, label="Mass", color="orange")
plt.xlabel("Time (s)")
plt.ylabel("Mass (kg)")
plt.title("Mass vs Time")
plt.legend()
plt.grid()
plt.show()
