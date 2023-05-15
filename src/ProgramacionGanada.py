from lxml import etree
import matplotlib.pyplot as plt
import numpy as np
import random

# Creación de pregunta 3 sobre la Programación Ganada
# Autor: Álvaro Hoyuelos Martín

def graficoProgramado():
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
    # Encontrar el tiempo donde PV = EV y PV = AC para hacer más facil el cálculo de la diferencia de meses
    indice_pv_ev = np.argmin(np.abs(pv * costeTotal - valorEV))
    indice_pv_ac = np.argmin(np.abs(pv * costeTotal - valorAC))
    plt.hlines(y = valorPV, xmin = 0, xmax = valorTiempoMedio, color = 'r', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorPV, f'{valorPV:.2f} €', color = 'r')       
    plt.hlines(y = valorEV, xmin = 0, xmax = valorTiempoMedio, color = 'g', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorEV, f'{valorEV:.2f} €', color = 'g')     
    plt.hlines(y = valorAC, xmin = 0, xmax = valorTiempoMedio, color = 'm', linestyle = '--')
    plt.text(valorTiempoMedio + 0.5, valorAC, f'{valorAC:.2f} €', color = 'm')
    plt.axhline(y = valorFinalPV, color = 'r', linestyle = '--')
    plt.axvline(x = tiempoTotal, color = 'r', linestyle = ':')    
    plt.text(tiempoTotal - 2, valorFinalPV, f'{valorFinalPV:.2f} €', color = 'r')     
    plt.axvline(x = valorTiempoMedio, color = 'gray', linestyle = ':')
    plt.axvline(x = recta[indice_pv_ev], color = 'gray', linestyle = ':')
    plt.text(recta[indice_pv_ev] + 0.1, recta[indice_pv_ev], f'{recta[indice_pv_ev]:.2f}', color = 'gray')
    plt.axvline(x = recta[indice_pv_ac], color = 'gray', linestyle = ':')
    plt.text(recta[indice_pv_ac] + 0.1, recta[indice_pv_ac] + 2000, f'{recta[indice_pv_ac]:.2f}', color = 'gray')

    # Añadir leyenda y título a la x e y de la gráfica y guardar la gráfica como una imagen
    plt.xlabel('Tiempo (meses)')
    plt.ylabel('Coste acumulado (€)')
    plt.legend()
    plt.savefig('ProgramacionGanadaEjercicio.jpg')
    
    # Creación del fichero xml y calculo de los métodos
    costVarianceF = costVariance(valorEV, valorAC)
    calculoSPIF = calculoSPI(valorEV, valorPV)     
    tiempoProgramadoF  = tiempoProgramado(valorEV, valorPV) 
    mesesDiferenciaF = mesesDiferencia(mitadTiempo, indice_pv_ev, recta) 
    ES_xml(costVarianceF, calculoSPIF, tiempoProgramadoF, mesesDiferenciaF)

# Métodos para calcular las preguntas del cuestionario
def costVariance(valorEV, valorAC):
    CV = valorEV - valorAC
    return CV

def calculoSPI(valorEV, valorPV):
    spi = valorEV / valorPV
    return round(spi, 2)

def tiempoProgramado(valorEV, valorPV):    
    if valorEV > valorPV:
        return 'Adelantado'
    elif valorEV < valorPV:
        return 'Retrasado'
    else:
        return 'De acuerdo a lo planificado'

def mesesDiferencia(mitadTiempo, indice_pv_ev, recta):
    recta[mitadTiempo] = round(recta[mitadTiempo], 0)
    recta[indice_pv_ev] = round(recta[indice_pv_ev], 2)
    meses_diferencia = abs(recta[indice_pv_ev] - recta[mitadTiempo])   
    return round(meses_diferencia,2)

def ES_xml(costVariance, calculoSPI, tiempoProgramado, mesesDiferencia):
    # Crear el elemento raíz 'question'
    question = etree.Element('question')
    question.set('type', 'cloze')

    # Crear el elemento 'questiontext'   
    name = etree.SubElement(question, 'name')
    text = etree.SubElement(name, 'text')
    text.text = 'Problema Programación ganada'

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
    text_content = f"""
        <p></p><p>Le presentan el informe de valor ganado de un proyecto en curso (ver figura).&nbsp;</p>
        <p><img src="ProgramacionGanadaEjercicio.jpg" alt="" width="861" height="614" role="presentation" style="vertical-align:text-bottom; margin: 0 .5em;" class="img-responsive"><br></p>
        <p>En vista de los datos,&nbsp;</p>
        <p>¿cuál es el Cost Variance del proyecto? (introducir con el signo apropiado) {{1:NUMERICAL:%100%{costVariance}:0#}}</p>
        <p>¿cuál es el SPI? (con dos decimales) {{1:NUMERICAL:%100%{calculoSPI}:0.1#}}</p>
        <p>De acuerdo a la programación ganada el proyecto va: {{1:MULTICHOICE_V:{retrasado}%Retrasado#~{adelantado}%Adelantado#~{planificada}%De acuerdo a lo planificado#}} &nbsp;¿cuánto? (introducir en meses sin signo)&nbsp;{{1:NUMERICAL:%100%{mesesDiferencia}:0#}}</p><br></p>
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
    
    # Convertir el árbol XML a una cadena y guardarla en el archivo 'ProgramacionGanada.xml'
    xml_str = etree.tostring(question, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('utf-8')  
    with open('ProgramacionGanada.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

# Crear una pregunta nueva 
graficoProgramado()