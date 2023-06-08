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

# Creación de pregunta 2 sobre el Valor Ganado
# Autor: Álvaro Hoyuelos Martín

def EVM_xml(rangoTiempoV, rangoCostesV, numPreguntasV):
    # Transformar el rango introducido en valores numéricos
    tiempoMinV, tiempoMaxV = map(int, rangoTiempoV.split(','))
    costeMinV, costeMaxV = map(int, rangoCostesV.split(','))

    # Crear el elemento raíz 'quiz'
    quiz = etree.Element('quiz')

    # Crear una pregunta nueva para cada número de pregunta
    for numPreguntasV in range(1, numPreguntasV + 1):
        # Definir valores aleatorios a partir del rango para el tiempo y el coste final
        tiempoTotalV = random.randrange(tiempoMinV, tiempoMaxV + 1, 2)   
        costeTotalV = random.randrange(costeMinV // 1000 * 1000, (costeMaxV + 999) // 1000 * 1000 + 1, 1000)

        # Generar dos números aleatorios para la recta sigmoidal de EV y AC
        rand1 = np.random.uniform(0.6, 1.4)
        rand2 = np.random.uniform(0.6, 1.4)

        # Dibujar la gráfica con las rectas sigmoidales
        tiempoInicialV = 0
        rectaV = np.linspace(tiempoInicialV, tiempoTotalV, 100)
        pv = (1 / (1 + np.exp(-10 * (rectaV / tiempoTotalV - 0.5))))
        ev = (1 / (1 + np.exp(-10 * (rectaV / (tiempoTotalV * rand1) - 0.5))))
        ac = (1 / (1 + np.exp(-10 * (rectaV / (tiempoTotalV * rand2) - 0.5))))
        plt.plot(rectaV, pv * costeTotalV, 'r', label = 'PV')
        plt.plot(rectaV[:50], ev[:50] * costeTotalV, 'g', label = 'EV')
        plt.plot(rectaV[:50], ac[:50] * costeTotalV, 'm', label = 'AC')

        # Añadir el valor del coste de PV, EV y AC a la gráfica en los momentos a anlizar
        mitadTiempo = int(len(rectaV) / 2)
        valorTiempoMedio = rectaV[mitadTiempo]          
        valorPV = round(pv[mitadTiempo] * costeTotalV / 100) * 100
        valorEV = round(ev[mitadTiempo] * costeTotalV / 100) * 100
        valorAC = round(ac[mitadTiempo] * costeTotalV / 100) * 100     
        valorFinalPV = round(pv[-1] * costeTotalV / 1000) * 1000
        plt.hlines(y = valorPV, xmin = 0, xmax = valorTiempoMedio, color = 'r', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorPV, f'{valorPV:.2f} €', color = 'r')       
        plt.hlines(y = valorEV, xmin = 0, xmax = valorTiempoMedio, color = 'g', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorEV, f'{valorEV:.2f} €', color = 'g')     
        plt.hlines(y = valorAC, xmin = 0, xmax = valorTiempoMedio, color = 'm', linestyle = '--')
        plt.text(valorTiempoMedio + 0.5, valorAC, f'{valorAC:.2f} €', color = 'm')
        plt.axhline(y = valorFinalPV, color = 'r', linestyle = '--')
        plt.axvline(x = tiempoTotalV, color = 'r', linestyle = ':')
        plt.text(tiempoTotalV - 2, valorFinalPV, f'{valorFinalPV:.2f} €', color = 'r')     

        # Añadir leyenda y título a la x e y de la gráfica y guardar la gráfica como una imagen
        plt.xlabel('Tiempo (meses)')
        plt.ylabel('Coste acumulado (€)')
        plt.legend()
        plt.savefig(f'ValorGanadoEjercicio{numPreguntasV}.jpg')
        plt.close()
        graficaV = plt.imread(f'ValorGanadoEjercicio{numPreguntasV}.jpg')
   
        # Convertir la imagen de un arreglo de NumPy a un objeto de imagen de PIL
        graficaPil = Image.fromarray(np.uint8(graficaV))
        # Guardar el gráfico en un objeto BytesIO
        buffered = BytesIO()
        graficaPil.save(buffered, format="JPEG")       
        # Codificar la gráfica en base64 para conseguir la linea de texto
        grafica64 = base64.b64encode(buffered.getvalue())
        graficaCodificadaV = grafica64.decode("utf-8")

        # Métodos para calcular las preguntas del cuestionario
        # Para el coste
        estadoCoste = ""
        if valorEV > valorAC:
            estadoCoste = 'Con ahorro en coste'
        elif valorEV < valorAC:
            estadoCoste = 'Con sobrecoste'
        else:
            estadoCoste = 'Con costes de acuerdo a lo planificado'        
        # Para el tiempo 
        estadoPlazo = ""    
        if valorEV > valorPV:
            estadoPlazo = 'En adelanto'
        elif valorEV < valorPV:
            estadoPlazo = 'En retraso'
        else:
            estadoPlazo = 'De acuerdo a lo planificado en plazo'
        # Para el coste final
        cpi = valorEV / valorAC
        costeFinal = round(valorFinalPV / cpi, 2)
        # Para el tiempo final
        spi = valorEV / valorPV
        tiempoFinal = round(tiempoTotalV / spi, 2)
        
        # Crear el elemento 'question'
        question = etree.SubElement(quiz, 'question')
        question.set('type', 'cloze')

        # Crear el elemento 'questiontext'   
        name = etree.SubElement(question, 'name')
        text = etree.SubElement(name, 'text')
        text.text = f'Problema Valor ganado {numPreguntasV}'

        # Crear el elemento 'questiontext'
        questiontext = etree.SubElement(question, 'questiontext')
        questiontext.set('format', 'html')

        # Calcular el valor de la preguntas MULTICHOICE_V
        adelanto = 0
        planificado = 0
        retraso = 0   
        sobrecoste = 0
        acordado = 0
        ahorro = 0         
        if estadoCoste == 'Con sobrecoste':
            sobrecoste = 100
        if estadoCoste == 'Con costes de acuerdo a lo planificado':
            acordado = 100
        if estadoCoste == 'Con ahorro en coste':
            ahorro = 100
        if estadoPlazo == 'En adelanto':
            adelanto = 100 
        if estadoPlazo == 'De acuerdo a lo planificado en plazo':
            planificado = 100
        if estadoPlazo == 'En retraso':
            retraso = 100

        # Crear el elemento 'text' dentro de 'questiontext' y su contenido
        text = etree.SubElement(questiontext, 'text')
        text_content = f"""
            <p>Le presentan el informe de valor ganado de un proyecto en curso (ver figura).<br></p>
            <p><img src="@@PLUGINFILE@@/ValorGanadoEjercicio{numPreguntasV}.jpg" alt="" width="574" height="372" role="presentation" style="vertical-align:text-bottom; margin: 0 .5em;" class="img-responsive"><br></p>
            <p>En vista de los datos, ¿cómo va el proyecto en costes?</p>
            <p>{{1:MULTICHOICE_V:%{sobrecoste}%Con sobrecoste#~%{acordado}%Con costes de acuerdo a lo planificado#~%{ahorro}%Con ahorro en coste#}}</p>
            <p>¿Y en tiempo?</p>
            <p>{{1:MULTICHOICE_V:%{adelanto}%En adelanto#~%{planificado}%De acuerdo a lo planificado en plazo#~%{retraso}%En retraso#}}</p>
            <p>¿qué estimación de coste final para el proyecto haría? (en €)&nbsp;{{1:NUMERICAL:%100%{costeFinal}:50#}}</p>
            <p>¿qué estimación de tiempo haría si utilizase el método del valor ganado? (en meses con dos decimales)&nbsp;{{1:NUMERICAL:%100%{tiempoFinal}:0.5#}}</p><br></p>
            """    
        text.text = etree.CDATA(text_content)
            
        # Crear el elemento 'file' dentro de 'questiontext'
        file = etree.SubElement(questiontext, 'file')
        file.set('name', f"ValorGanadoEjercicio{numPreguntasV}.jpg")
        file.set('path', "/")
        file.set('encoding', "base64")
        file.text = f"""{graficaCodificadaV}"""

        # Crear los elementos restantes
        generalfeedback = etree.SubElement(question, 'generalfeedback')
        generalfeedback.set('format', 'html')   
        text = etree.SubElement(generalfeedback, 'text')  
        penalty = etree.SubElement(question, 'penalty')
        penalty.text = '0.3333333'   
        hidden = etree.SubElement(question, 'hidden')
        hidden.text = '0'   
        idnumber = etree.SubElement(question, 'idnumber')
        # Cierra la imagen y la elimina para poder crear otra gráfica desde 0
        # plt.close()
        os.remove(f'ValorGanadoEjercicio{numPreguntasV}.jpg')
        
    # Convertir el árbol XML a una cadena y guardarla en el archivo 'ValorGanado.xml'
    xml_str = etree.tostring(quiz, pretty_print=True, encoding='UTF-8').decode('utf-8')  
    with open('ValorGanado.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)