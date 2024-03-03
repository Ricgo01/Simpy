import simpy
import random
import statistics
import csv

def ejecutar_simulacion(NUM_PROCESOS, INTERVALO_GENERACION, CAPACIDAD_RAM, VELOCIDAD_CPU, CAPACIDAD_CPU, TIEMPO_SIMULACION):
    env = simpy.Environment()
    RAM = simpy.Container(env, init=CAPACIDAD_RAM, capacity=CAPACIDAD_RAM)
    CPU = simpy.Resource(env, capacity=CAPACIDAD_CPU)
    tiempos_totales = []

    def proceso(env, nombre, memoria_req, instrucciones, RAM, CPU):
        tiempo_llegada = env.now
        yield RAM.get(memoria_req)
        with CPU.request() as req:
            yield req
            yield env.timeout(instrucciones / VELOCIDAD_CPU)
        yield RAM.put(memoria_req)
        tiempos_totales.append(env.now - tiempo_llegada)

    def generador_procesos(env, NUM_PROCESOS, INTERVALO_GENERACION, RAM, CPU):
        for i in range(NUM_PROCESOS):
            tiempo_espera = random.expovariate(1.0 / INTERVALO_GENERACION)
            yield env.timeout(tiempo_espera)
            memoria_req = random.randint(1, 10)
            instrucciones = random.randint(1, 20)
            env.process(proceso(env, f'Proceso {i}', memoria_req, instrucciones, RAM, CPU))
    
    env.process(generador_procesos(env, NUM_PROCESOS, INTERVALO_GENERACION, RAM, CPU))
    env.run(until=TIEMPO_SIMULACION)

    return statistics.mean(tiempos_totales) if tiempos_totales else 0

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
INTERVALO_GENERACION = 10
CAPACIDAD_RAM = 100
VELOCIDAD_CPU = 3
CAPACIDAD_CPU = 2
TIEMPO_SIMULACION = 1000
resultados = [("Num Procesos", "Tiempo Promedio")]

for NUM_PROCESOS in [25, 50, 100, 150, 200]:
    promedio = ejecutar_simulacion(NUM_PROCESOS, INTERVALO_GENERACION, CAPACIDAD_RAM, VELOCIDAD_CPU, CAPACIDAD_CPU, TIEMPO_SIMULACION)
    resultados.append((NUM_PROCESOS, promedio))


with open("resultados_simulacion.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(resultados)

print("Resultados exportados a resultados_simulacion.csv")