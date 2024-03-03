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