import random
import string
import pandas as pd
from termcolor import colored

# Creación de pregunta 0 tipo tabla
# Autor: Álvaro Hoyuelos Martín

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
            
            # Agrega la fila a la tabla
            self.tabla.append(fila)

    def imprimir_tabla(self):
        # Añade al porcentaje completado el simbolo %
        for columna in self.tabla:
            if columna[3] != "" and columna[3] != "%Completado":                
                columna[3] = str(columna[3]) + "%"

        # Calcula el ancho máximo de cada columna
        anchos = [max(len(str(fila[i])) for fila in self.tabla) for i in range(len(self.tabla[0]))]
        
        # Imprime la tabla con las columnas centradas
        for columna in self.tabla:
            # Si la tarea está al 100% se pone en negrita
            if columna[3] == "100%":
                print(colored("| " + " | ".join(str(elem).center(anchos[i]) for i, elem in enumerate(columna)) + " |", attrs=['bold']))
            else:
                print("| " + " | ".join(str(elem).center(anchos[i]) for i, elem in enumerate(columna)) + " |")
               
    def valor_planificado(self):
        PV = 0
        for columna in self.tabla:
            # Si la tarea esta al 100% se suma su CPTP
            if columna[3] == 100:
                PV += columna[1]
        return PV
    
    def coste_actual(self):
        AC = 0
        for columna in self.tabla:
            # Verifica si tiene CRTR la tarea
            if isinstance(columna[2], int):                
                # Convierte el valor en un entero
                AC += int(columna[2])
        return AC

    def valor_ganado(self):
        EV = 0
        for columna in self.tabla:
            # Verifica si la tarea está empezada
             if isinstance(columna[3], int):
                # Multiplica el CPTP con su porcentaje completado
                EV += columna[1] * columna [3] / 100                 
        return EV
    
    def CPI(self):
        EV = self.valor_ganado()
        AC = self.coste_actual()
        # Verifica si AC es 0, para que no de error
        if AC == 0:
            return 0
        # Se redondea a dos decimales
        cpi = round(EV / AC, 2)
        return cpi

    def SPI(self):
        EV = self.valor_ganado()
        PV = self.valor_planificado()
        # Verifica si PV es 0, para que no de error
        if PV == 0:
            return 0
        # Se redondea a dos decimales
        spi = round(EV / PV, 2)
        return spi
    
# SALIDA POR PANTALLA
tabla = Tabla()
valor_planificado = str(tabla.valor_planificado())
coste_actual = str(tabla.coste_actual()) 
valor_ganado = str(tabla.valor_ganado())
cpi = str(tabla.CPI())
spi = str(tabla.SPI())
tabla.imprimir_tabla()
print("El valor planificado (PV) en el momento actual "+ valor_planificado)
print("El coste actual (AC) en el momento actual "+ coste_actual)
print("El valor ganado (EV) en el momento actual "+ valor_ganado)
print("El CPI del proyecto (con dos decimales) "+ cpi)
print("El SPI del proyecto (con dos decimales) "+ spi)