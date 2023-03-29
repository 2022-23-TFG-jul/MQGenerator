 # pip install pandas

import random
import string
# import pandas as pd


class Tabla:
    def __init__(self):
        self.columnas = 4
        self.filas = random.randint(6, 15)
        self.tabla = []

        # Agrego el título de las columnas en la fila 1
        self.tabla.append(['Tareas', 'CPTP', 'CRTR', '%Completado'])

        # Agrego los datos a la tabla
        for i in range(self.filas):
            fila = []

            # Agrego los identificadores de tareas de la A a la Z
            tarea_id = chr(ord('A') + i)
            fila.append(tarea_id)

            # Agrego valores aleatorios entre 1000 y 6000 (múltiplos de 1000) a la segunda columna
            valor_cptp = random.randint(1, 6) * 1000
            fila.append(valor_cptp)

            # Agrego valores aleatorios entre 1000 y 5000 (múltiplos de 100) a la tercera columna (solo en las primeras 6 filas)
            if i < 6:
                valor_crtr = random.randint(10, 50) * 100
            else:
                valor_crtr = ""
            fila.append(valor_crtr)

            # Agrego valores a la cuarta columna
            if i < 5:
                # Las primeras 5 filas tienen 100% de completado
                completado = 100
            elif i == 5:
                # La sexta fila tiene un valor aleatorio entre 0% y 90% de completado (múltiplo de 10)
                completado = random.randint(0, 9) * 10
            else:
                # El resto de las filas no tienen valor en la cuarta columna
                completado = ""
            fila.append(completado)

            # Agrego la fila a la tabla
            self.tabla.append(fila)

    def imprimir_tabla(self):
        # Calcula el ancho máximo de cada columna
        anchos = [max(len(str(fila[i])) for fila in self.tabla) for i in range(len(self.tabla[0]))]
        
        # Imprime la tabla con las columnas centradas
        for fila in self.tabla:
            print("| " + " | ".join(str(elem).center(anchos[i]) for i, elem in enumerate(fila)) + " |")

    def valor_planificado(self):
        PV = 0
        for row in self.tabla:
            # Si la tarea esta al 100% completado se suma su CPTP
            if row[3] == 100:
                PV += row[1]
        return PV

tabla = Tabla()
tabla.imprimir_tabla()
print("El valor planificado (PV) en el momento actual "+ str(tabla.valor_planificado()))

