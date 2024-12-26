import krpc
import time
import pandas as pd

# Подключаемся к KRPC
conn = krpc.connect(name='Flight to Mun Logger')
vessel = conn.space_center.active_vessel

# Инициализация списков для записи данных
times = []
velocities = []
masses = []

# Функция для проверки, находится ли корабль на орбите вокруг Муны
def is_in_orbit_around_mun():
    return (vessel.orbit.body.name == "Mun" and 
            vessel.orbit.periapsis_altitude > 0 and 
            vessel.orbit.apoapsis_altitude > 0)

# Ожидание старта (корабль переходит в состояние полета)
print("Ожидание взлета...")
while vessel.situation != conn.space_center.VesselSituation.flying:
    time.sleep(0.1)

# Запуск таймера для записи данных
print("Начало записи данных...")
start_time = time.time()

# Запись данных до выхода на орбиту Муны
while not is_in_orbit_around_mun():
    current_time = time.time() - start_time
    times.append(current_time)
    velocities.append(vessel.flight(vessel.orbit.body.reference_frame).speed)
    masses.append(vessel.mass)
    time.sleep(0.1)

print("Корабль вышел на орбиту Муны. Запись завершена.")

# Сохранение данных в CSV
data = pd.DataFrame({'Time (s)': times, 'Velocity (m/s)': velocities, 'Mass (kg)': masses})
data.to_csv('flight_to_mun_data.csv', index=False)
print("Данные сохранены в 'flight_to_mun_data.csv'.")