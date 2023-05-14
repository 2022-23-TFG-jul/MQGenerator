from lxml import etree
import matplotlib.pyplot as plt
import numpy as np
import random

# Creación de pregunta 2 sobre el Valor Ganado
# Autor: Álvaro Hoyuelos Martín

def crearGrafico():
    # Pedir al usuario que introduzca los datos necesarios para la gráfica
    rangoTiempo  = input('Introduce el rango de tiempo final (meses) separado por comas (ejemplo: 10,20): ')
    rangoCoste = input('Introduce el rango de coste acumulado final (€) separado por comas (ejemplo: 2000,50000): ')

    # Transformar el rango introducido en valores numéricos
    tiempoMin, tiempoMax = map(int, rangoTiempo.split(','))
    costeMin, costeMax = map(int, rangoCoste.split(','))

    # Definir valores aleatorios a partir del rango para el tiempo y el coste final
    tiempoTotal = random.randrange(tiempoMin, tiempoMax + 1, 2)   
    costeTotal = random.randrange(costeMin // 1000 * 1000, (costeMax + 999) // 1000 * 1000 + 1, 1000)

    # Generar dos números aleatorios para la recta sigmoidal de EV y AC
    rand1 = np.random.uniform(0.6, 1.4)
    rand2 = np.random.uniform(0.6, 1.4)

    # Dibujar la gráfica con las rectas sigmoidales
    tiempoInicial = 0
    recta = np.linspace(tiempoInicial, tiempoTotal, 100)
    pv = (1 / (1 + np.exp(-10 * (recta / tiempoTotal - 0.5))))
    ev = (1 / (1 + np.exp(-10 * (recta / (tiempoTotal * rand1) - 0.5))))
    ac = (1 / (1 + np.exp(-10 * (recta / (tiempoTotal * rand2) - 0.5))))
    plt.plot(recta, pv * costeTotal, 'r', label = 'PV')
    plt.plot(recta[:50], ev[:50] * costeTotal, 'g', label = 'EV')
    plt.plot(recta[:50], ac[:50] * costeTotal, 'm', label = 'AC')

    # Añadir el valor del coste de PV, EV y AC a la gráfica en los momentos a anlizar
    mitadTiempo = int(len(recta) / 2)
    valorTiempoMedio = recta[mitadTiempo]          
    valorPV = round(pv[mitadTiempo] * costeTotal / 100) * 100
    valorEV = round(ev[mitadTiempo] * costeTotal / 100) * 100
    valorAC = round(ac[mitadTiempo] * costeTotal / 100) * 100     
    valorFinalPV = round(pv[-1] * costeTotal / 1000) * 1000
    plt.hlines(y = valorPV, xmin = 0, xmax = valorTiempoMedio, color = 'r', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorPV, f'{valorPV:.2f} €', color = 'r')       
    plt.hlines(y = valorEV, xmin = 0, xmax = valorTiempoMedio, color = 'g', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorEV, f'{valorEV:.2f} €', color = 'g')     
    plt.hlines(y = valorAC, xmin = 0, xmax = valorTiempoMedio, color = 'm', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorAC, f'{valorAC:.2f} €', color = 'm')
    plt.axhline(y = valorFinalPV, color = 'r', linestyle = '--')
    plt.axvline(x = tiempoTotal, color = 'r', linestyle = ':')
    plt.text(tiempoTotal + 0.5, valorFinalPV, f'{valorFinalPV:.2f} €', color = 'r')  

    # Añadir leyenda y título a la x e y de la gráfica y guardar la gráfica como una imagen
    plt.xlabel('Tiempo (meses)')
    plt.ylabel('Coste acumulado (€)')
    plt.legend()
    plt.savefig('ValorGanadoEjercicio.jpg')
    
    # Creación del fichero xml y calculo de los métodos
    estadoCosteF = estadoCoste(valorEV, valorAC)
    estadoPlazoF = estadoPlazo(valorEV, valorPV)    
    costeFinalF = costeFinal(valorEV, valorAC, valorFinalPV)    
    tiempoFinalF = tiempoFinal(valorEV, valorPV, tiempoTotal)   
    EVM_xml(estadoCosteF, estadoPlazoF, costeFinalF, tiempoFinalF)

# Métodos para calcular las preguntas del cuestionario
def estadoCoste(valorEV, valorAC):
    if valorEV > valorAC:
        return 'Con ahorro en coste'
    elif valorEV < valorAC:
        return 'Con sobrecoste'
    else:
        return 'Con costes de acuerdo a lo planificado'

def estadoPlazo(valorEV, valorPV):    
    if valorEV > valorPV:
        return 'En adelanto'
    elif valorEV < valorPV:
        return 'En retraso'
    else:
        return 'De acuerdo a lo planificado en plazo'

def costeFinal(valorEV, valorAC, valorFinalPV):
    cpi = valorEV / valorAC
    return round(valorFinalPV / cpi, 2)

def tiempoFinal(valorEV, valorPV, tiempoTotal):
    spi = valorEV / valorPV
    return round(tiempoTotal / spi, 2)

def EVM_xml(estadoCoste, estadoPlazo, costeFinal, tiempoFinal):  
    # Crear el elemento raíz 'question'
    question = etree.Element('question')
    question.set('type', 'cloze')

    # Crear el elemento 'questiontext'   
    name = etree.SubElement(question, 'name')
    text = etree.SubElement(name, 'text')
    text.text = 'Problema Valor ganado'

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
        <p><img src="ValorGanadoEjercicio.jpg" alt="" width="574" height="372" role="presentation" style="vertical-align:text-bottom; margin: 0 .5em;" class="img-responsive"><br></p>
        <p>En vista de los datos, ¿cómo va el proyecto en costes?</p>
        <p>{{1:MULTICHOICE_V:{sobrecoste}%Con sobrecoste#~{acordado}%Con costes de acuerdo a lo planificado#~{ahorro}%Con ahorro en coste#}}</p>
        <p>¿Y en tiempo?</p>
        <p>{{1:MULTICHOICE_V:{adelanto}%En adelanto#~{planificado}%De acuerdo a lo planificado en plazo#~{retraso}%En retraso#}}</p>
        <p>¿qué estimación de coste final para el proyecto haría? (en €)&nbsp;<{{1:NUMERICAL:%100%{costeFinal}:50#}}</p>
        <p>¿qué estimación de tiempo haría si utilizase el método del valor ganado? (en meses)&nbsp;{{1:NUMERICAL:%100%{tiempoFinal}:0.5#}}</p><br></p>
        """    
    text.text = etree.CDATA(text_content)
    
    # Crear los elementos restantes
    generalfeedback = etree.SubElement(question, 'generalfeedback')
    generalfeedback.set('format', 'html')   
    text = etree.SubElement(generalfeedback, 'text')  
    penalty = etree.SubElement(question, 'penalty')
    penalty.text = '0.3333333'   
    hidden = etree.SubElement(question, 'hidden')
    hidden.text = '0'   
    idnumber = etree.SubElement(question, 'idnumber')
    
    # Convertir el árbol XML a una cadena y guardarla en el archivo 'ValorGanado.xml'
    xml_str = etree.tostring(question, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('utf-8')  
    with open('ValorGanado.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

# Crear una pregunta nueva 
crearGrafico()