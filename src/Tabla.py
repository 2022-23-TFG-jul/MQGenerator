from lxml import etree
from string import ascii_uppercase
import random

# Creación de pregunta 1 tipo tabla
# Autor: Álvaro Hoyuelos Martín

def create_xml():
    # Solicitar al usuario el número de tareas y un rango de costes
    tareasMax = int(input("Indique el número máximo de tareas(mínimo 6): "))
    rangoCostes = input('Introduce el rango de costes para CPTP y CRTR separado por comas (ejemplo: 2000,5000): ')
    costeMin, costeMax = map(int, rangoCostes.split(','))
    numTareas = random.randrange(6, tareasMax)

    # Crear una lista para almacenar la información de las tareas
    tareas = []

    # Variable para verificar si una tarea no está 100% completada
    tareaIncompleta = False

    # Inicializar variables para calcular PV, AC y EV
    valorPlanificado = 0
    costeActual = 0
    valorGanado = 0
    
    # Solicitar al usuario la información de cada tarea
    for i in range(numTareas):
        nombreTarea = ascii_uppercase[i]
        CPTP = random.randrange(costeMin // 100 * 100, (costeMax + 99) // 100 * 100 + 1, 100)
        # Para las tareas empezadas o completadas sí que se necesita su CRTR y %Completado
        if not tareaIncompleta:
            CRTR = random.randrange(costeMin // 100 * 100, (costeMax + 99) // 100 * 100 + 1, 100)
            if i < 5:
                porcentaje = 100
            elif i == 5:
                porcentaje = random.randint(1, 9) * 10
        else:
            CRTR = 0
            porcentaje = 0
        
        tareas.append({'Tareas': nombreTarea, 'CPTP': CPTP, 'CRTR': CRTR, '%Completado': porcentaje})
        # Calcular valor planificado, coste actual y valor ganado
        if porcentaje == 100:
            valorPlanificado += CPTP
        costeActual += CRTR
        valorGanado += CPTP * (porcentaje / 100)
        
        if porcentaje < 100:
            tareaIncompleta = True
    
    # Calcular CPI y SPI
    cpi = valorGanado / costeActual
    spi = valorGanado / valorPlanificado

    # Crear el elemento raíz 'quiz'
    quiz = etree.Element('quiz')

    # Crear el elemento 'question'
    question = etree.SubElement(quiz, 'question')
    question.set('type', 'cloze')

    # Crear el elemento 'questiontext'   
    name = etree.SubElement(question, 'name')
    text = etree.SubElement(name, 'text')
    text.text = 'Datos básicos'

    # Crear el elemento 'questiontext'
    questiontext = etree.SubElement(question, 'questiontext')
    questiontext.set('format', 'html')
    
    # Crear el elemento 'text' dentro de 'questiontext'
    text = etree.SubElement(questiontext, 'text')
    
    # Crear el contenido del elemento 'text'
    text_content = """
    <p>Suponga un proyecto en el que en el momento actual y de acuerdo al plan de proyecto<b><u> las actividades desde la A hasta la E</u></b> deberían estar ya completadas y el resto de actividades no comenzadas.</p>
    <p>El informe de seguimiento del proyecto es el siguiente:</p>
    <table border="0" cellpadding="0" cellspacing="0" width="320" style="text-align: center; ">
        <colgroup><col width="80" span="4"></colgroup>
        <tbody>
            <tr height="19">
                <td height="19" width="80"><b>Tareas</b></td>
                <td width="80"><b>CPTP</b></td>
                <td width="80"><b>CRTR</b></td>
                <td width="80"><b>%Completado</b></td>
            </tr>"""

    # Agregar una fila a la tabla para cada tarea
    for tarea in tareas:
        if tarea['%Completado'] == 100:
            text_content += f"""
            <tr height="19">
                <td height="19"><b>{tarea['Tareas']}</b></td>
                <td align="right" style="text-align: center; "><b>{tarea['CPTP']}</b></td>
                <td align="right" style="text-align: center; "><b>{tarea['CRTR']}</b></td>
                <td align="right" style="text-align: center; "><b>{tarea['%Completado']}%</b></td>
            </tr>"""
        else:            
            if tarea['%Completado'] > 0:
                text_content += f"""
            <tr height="19">
                <td height="19">{tarea['Tareas']}</td>
                <td align="right" style="text-align: center; ">{tarea['CPTP']}</td>
                <td align="right" style="text-align: center; ">{tarea['CRTR']}</td>
                <td align="right" style="text-align: center; ">{tarea['%Completado']}%</td>
            </tr>"""   
            elif tareaIncompleta:
                text_content += f"""
                <tr height="19">
                    <td height="19">{tarea['Tareas']}</td>
                    <td align="right" style="text-align: center; ">{tarea['CPTP']}</td>
                    <td align="right" style="text-align: center; "></td>
                    <td align="right" style="text-align: center; "></td>
                </tr>"""
             
    text_content += f"""
        </tbody></table><br>Calcule:
        <p>El valor planificado (PV) en el momento actual {{1:NUMERICAL:%100%{valorPlanificado}:0#}}</p>
        <p>El coste actual (AC) en el momento actual {{1:NUMERICAL:%100%{costeActual}:0#}}</p>
        <p>El valor ganado (EV) en el momento actual {{1:NUMERICAL:%100%{valorGanado}:0#}}</p>
        <p>El CPI del proyecto (con dos decimales) {{1:NUMERICAL:%100%{round(cpi,2)}:0.01#{valorGanado}/{costeActual}}}</p>
        <p>El SPI del proyecto (con dos decimales) {{1:NUMERICAL:%100%{round(spi,2)}:0.01#{valorGanado}/{valorPlanificado}}}</p><br><p></p>
        """
    
    text.text = etree.CDATA(text_content)
    
    # Crear los elementos restantes
    generalfeedback = etree.SubElement(question, 'generalfeedback')
    generalfeedback.set('format', 'html')
    
    text = etree.SubElement(generalfeedback, 'text')
    text.text = "Para calcular PV= Sumar el CPTP de todas las tareas completadas. <br>Para calcular AC= Sumar todos los CRTR.<br>Para calcular EV= Multiplicar los CPTP por sus respectivos porcentajes y sumarlos.<br>Para calcular CPI= Dividir EV por el AC.<br>Para calcular SPI= Dividir EV por el PV. "
    
    penalty = etree.SubElement(question, 'penalty')
    penalty.text = '0.3333333'
    
    hidden = etree.SubElement(question, 'hidden')
    hidden.text = '0'
    
    idnumber = etree.SubElement(question, 'idnumber')
    
    # Convertir el árbol XML a una cadena y guardarla en un archivo
    xml_str = etree.tostring(quiz, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('utf-8')
    
    with open('Tabla.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

# Crear una pregunta nueva 
create_xml()