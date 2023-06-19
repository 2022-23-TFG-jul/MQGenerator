from lxml import etree
import matplotlib
matplotlib.use('Agg')  # Establecer el backend a 'Agg'
import matplotlib.pyplot as plt
import numpy as np
import random
import base64
from PIL import Image
from io import BytesIO
import os

# Creación de pregunta 3 sobre la Programación Ganada
# Autor: Álvaro Hoyuelos Martín

def ES_xml(rangoTiempoP, rangoCostesP, numPreguntasP, idiomaP):
    # Transformar el rango introducido en valores numéricos
    tiempoMinP, tiempoMaxP = map(int, rangoTiempoP.split(','))
    costeMinP, costeMaxP = map(int, rangoCostesP.split(','))

    # Crear el elemento raíz 'quiz'
    quiz = etree.Element('quiz')

    # Crear una pregunta nueva para cada número de pregunta
    for numPreguntasP in range(1, numPreguntasP + 1):
        # Definir valores aleatorios a partir del rango para el tiempo y el coste final
        tiempoTotalP = random.randrange(tiempoMinP, tiempoMaxP + 1, 2)   
        costeTotalP = random.randrange(costeMinP // 1000 * 1000, (costeMaxP + 999) // 1000 * 1000 + 1, 1000)

        # Generar dos números aleatorios para la recta sigmoidal de EV y AC
        rand1 = np.random.uniform(0.6, 1.4)
        rand2 = np.random.uniform(0.6, 1.4)

        # Dibujar la gráfica con las rectas sigmoidales
        tiempoInicialP = 0
        rectaP = np.linspace(tiempoInicialP, tiempoTotalP, 100)
        pv = (1 / (1 + np.exp(-10 * (rectaP / tiempoTotalP - 0.5))))
        ev = (1 / (1 + np.exp(-10 * (rectaP / (tiempoTotalP * rand1) - 0.5))))
        ac = (1 / (1 + np.exp(-10 * (rectaP / (tiempoTotalP * rand2) - 0.5))))
        plt.plot(rectaP, pv * costeTotalP, 'r', label = 'PV')
        plt.plot(rectaP[:50], ev[:50] * costeTotalP, 'g', label = 'EV')
        plt.plot(rectaP[:50], ac[:50] * costeTotalP, 'm', label = 'AC')

        # Añadir el valor del coste de PV, EV y AC a la gráfica en los momentos a anlizar
        mitadTiempo = int(len(rectaP) / 2)
        valorTiempoMedio = rectaP[mitadTiempo]          
        valorPV = round(pv[mitadTiempo] * costeTotalP / 100) * 100
        valorEV = round(ev[mitadTiempo] * costeTotalP / 100) * 100
        valorAC = round(ac[mitadTiempo] * costeTotalP / 100) * 100     
        valorFinalPV = round(pv[-1] * costeTotalP / 1000) * 1000
        # Encontrar el tiempo donde PV = EV y PV = AC para hacer más facil el cálculo de la diferencia de meses
        indice_pv_ev = np.argmin(np.abs(pv * costeTotalP - valorEV))
        indice_pv_ac = np.argmin(np.abs(pv * costeTotalP - valorAC))
        plt.hlines(y = valorPV, xmin = 0, xmax = valorTiempoMedio, color = 'r', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorPV, f'{valorPV:.2f} €', color = 'r')       
        plt.hlines(y = valorEV, xmin = 0, xmax = valorTiempoMedio, color = 'g', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorEV, f'{valorEV:.2f} €', color = 'g')     
        plt.hlines(y = valorAC, xmin = 0, xmax = valorTiempoMedio, color = 'm', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorAC, f'{valorAC:.2f} €', color = 'm')
        plt.axhline(y = valorFinalPV, color = 'r', linestyle = '--')
        plt.axvline(x = tiempoTotalP, color = 'r', linestyle = ':')    
        plt.text(tiempoTotalP - 2, valorFinalPV, f'{valorFinalPV:.2f} €', color = 'r')     
        plt.axvline(x = valorTiempoMedio, color = 'gray', linestyle = ':')
        plt.axvline(x = rectaP[indice_pv_ev], color = 'gray', linestyle = ':')
        plt.text(rectaP[indice_pv_ev] + 0.1, rectaP[indice_pv_ev], f'{rectaP[indice_pv_ev]:.2f}', color = 'gray')
        plt.axvline(x = rectaP[indice_pv_ac], color = 'gray', linestyle = ':')
        plt.text(rectaP[indice_pv_ac] + 0.1, rectaP[indice_pv_ac] + 2000, f'{rectaP[indice_pv_ac]:.2f}', color = 'gray')

        if idiomaP == 'esp':
        # Añadir leyenda y título a la x e y de la gráfica y guardar la gráfica como una imagen
            plt.xlabel('Tiempo (meses)')
            plt.ylabel('Coste acumulado (€)')
        else: 
            plt.xlabel('Time (months)')
            plt.ylabel('Accumulated Cost (€)')
        plt.legend()
        plt.savefig(f'ProgramacionGanadaEjercicio{numPreguntasP}.jpg')
        plt.close()
        graficaP = plt.imread(f'ProgramacionGanadaEjercicio{numPreguntasP}.jpg')

        # Convertir la imagen de un arreglo de NumPy a un objeto de imagen de PIL
        graficaPil = Image.fromarray(np.uint8(graficaP))
        # Guardar el gráfico en un objeto BytesIO
        buffered = BytesIO()
        graficaPil.save(buffered, format="JPEG")
        # Codificar la gráfica en base64 para conseguir la linea de texto
        grafica64 = base64.b64encode(buffered.getvalue())
        graficaCodificadaP = grafica64.decode("utf-8")

        # Métodos para calcular las preguntas del cuestionario
        # Para el CV
        costVariance = valorEV - valorAC
        # Para el SPI
        spi = valorEV / valorPV
        calculoSPI = round(spi, 2)
        # Para el tiempo programado
        tiempoProgramado = ""
        if valorEV > valorPV:
            tiempoProgramado = 'Adelantado'
        elif valorEV < valorPV:
            tiempoProgramado = 'Retrasado'
        else:
            tiempoProgramado = 'De acuerdo a lo planificado'
        # Para los meses de diferencia
        rectaP[mitadTiempo] = round(rectaP[mitadTiempo], 0)
        rectaP[indice_pv_ev] = round(rectaP[indice_pv_ev], 2)
        meses_diferencia = abs(rectaP[indice_pv_ev] - rectaP[mitadTiempo])   
        mesesDiferencia = round(meses_diferencia,2)

        # Crear el elemento 'question'
        question = etree.SubElement(quiz, 'question')
        question.set('type', 'cloze')

        # Crear el elemento 'questiontext'   
        name = etree.SubElement(question, 'name')
        text = etree.SubElement(name, 'text')
        if idiomaP == 'esp':
            text.text = f'Problema Programación ganada {numPreguntasP}'
        else:
            text.text = f'Earned Scheduling problem {numPreguntasP}'

        # Crear el elemento 'questiontext'
        questiontext = etree.SubElement(question, 'questiontext')
        questiontext.set('format', 'html')
        
        # Calcular el valor de la preguntas MULTICHOICE_V
        adelantado = 0
        planificada = 0
        retrasado = 0        
        if tiempoProgramado == 'Adelantado':
            adelantado = 100 
        if tiempoProgramado == 'De acuerdo a lo planificado':
            planificada = 100
        if tiempoProgramado == 'Retrasado':
            retrasado = 100

        # Crear el elemento 'text' dentro de 'questiontext' y su contenido
        text = etree.SubElement(questiontext, 'text')
        # Para el español
        if idiomaP == 'esp':
            text_content = f"""
            <p></p><p>Le presentan el informe de valor ganado de un proyecto en curso (ver figura).&nbsp;</p>
            <p><img src="@@PLUGINFILE@@/ProgramacionGanadaEjercicio{numPreguntasP}.jpg" alt="" width="574" height="409" role="presentation" style="vertical-align:text-bottom; margin: 0 .5em;" class="img-responsive"><br></p>
            <p>En vista de los datos,&nbsp;</p>
            <p>¿Cuál es el Cost Variance del proyecto? (introducir con el signo apropiado) {{1:NUMERICAL:%100%{costVariance}:0#}}</p>
            <p>¿Cuál es el SPI? (con dos decimales) {{1:NUMERICAL:%100%{calculoSPI}:0.1#}}</p>
            <p>De acuerdo a la Programación Ganada el proyecto va: {{1:MULTICHOICE_V:%{retrasado}%Retrasado#~%{adelantado}%Adelantado#~%{planificada}%De acuerdo a lo planificado#}} &nbsp;¿cuánto? (introducir en meses sin signo y 2 decimales)&nbsp;{{1:NUMERICAL:%100%{mesesDiferencia}:0#}}</p><br></p>
            """ 
        else:
            text_content = f"""
            <p></p><p>You are presented with the Earned Value report of an ongoing project (see the figure).&nbsp;</p>
            <p><img src="@@PLUGINFILE@@/ProgramacionGanadaEjercicio{numPreguntasP}.jpg" alt="" width="574" height="409" role="presentation" style="vertical-align:text-bottom; margin: 0 .5em;" class="img-responsive"><br></p>
            <p>Based on the data,&nbsp;</p>
            <p>What is the Cost Variance of the project (enter with the appropriate sign)? {{1:NUMERICAL:%100%{costVariance}:0#}}</p>
            <p>What is the SPI (to two decimals)? {{1:NUMERICAL:%100%{calculoSPI}:0.1#}}</p>
            <p>According to the Earned Scheduling the project goes: {{1:MULTICHOICE_V:%{retrasado}%Delayed#~%{adelantado}%Advanced#~%{planificada}%According to plan#}} &nbsp;How much? (enter in months without sign and 2 decimals)&nbsp;{{1:NUMERICAL:%100%{mesesDiferencia}:0#}}</p><br></p>
            """             
        text.text = etree.CDATA(text_content)
  
        # Crear el elemento 'file' dentro de 'questiontext'
        file = etree.SubElement(questiontext, 'file')
        file.set('name', f"ProgramacionGanadaEjercicio{numPreguntasP}.jpg")
        file.set('path', "/")
        file.set('encoding', "base64")
        file.text = f"""{graficaCodificadaP}"""

        # Crear los elementos restantes
        generalfeedback = etree.SubElement(question, 'generalfeedback')
        generalfeedback.set('format', 'html')   
        text = etree.SubElement(generalfeedback, 'text')  
        penalty = etree.SubElement(question, 'penalty')
        penalty.text = '0.3333333'   
        hidden = etree.SubElement(question, 'hidden')
        hidden.text = '0'   
        idnumber = etree.SubElement(question, 'idnumber')
        # Cierra la imagen para poder crear otra gráfica desde 0
        os.remove(f'ProgramacionGanadaEjercicio{numPreguntasP}.jpg')

    # Convertir el árbol XML a una cadena y guardarla en el archivo 'ValorGanado.xml'
    xml_str = etree.tostring(quiz, pretty_print=True, encoding='UTF-8').decode('UTF-8')  
    with open('ProgramacionGanada.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)