from lxml import etree
from string import ascii_uppercase

# Creación de pregunta 0 tipo tabla
# Autor: Álvaro Hoyuelos Martín

def create_xml():
    # Solicitar al usuario el número de tareas
    num_tasks = int(input("Indique el número de tareas(mínimo 6): "))
    
    # Crear una lista para almacenar la información de las tareas
    tasks = []

    # Variable para verificar si una tarea no está 100% completada
    incomplete_task_found = False

    # Inicializar variables para calcular PV, AC y EV
    valor_planificado = 0
    coste_actual = 0
    valor_ganado = 0
    
# Solicitar al usuario la información de cada tarea
    for i in range(num_tasks):
        task_name = ascii_uppercase[i]
        CPTP = int(input(f"Introduce el CPTP para la tarea {task_name}: "))
        # Para las tareas empezadas o completadas sí que se necesita su CRTR y %Completado
        if not incomplete_task_found:
            CRTR = int(input(f"Introduce el CRTR para la tarea {task_name}: "))
            percent_completed = int(input(f"Introduce el % completado para la tarea {task_name}: "))
        else:
            CRTR = 0
            percent_completed = 0
        
        tasks.append({'Tareas': task_name, 'CPTP': CPTP, 'CRTR': CRTR, '%Completado': percent_completed})
        # Calcular valor planificado, coste actual y valor ganado
        if percent_completed == 100:
            valor_planificado += CPTP
        coste_actual += CRTR
        valor_ganado += CPTP * (percent_completed / 100)
        
        if percent_completed < 100:
            incomplete_task_found = True
    
    # Calcular CPI y SPI
    cpi = valor_ganado / coste_actual
    spi = valor_ganado / valor_planificado
    
    # Crear el elemento raíz 'question'
    question = etree.Element('question')
    question.set('type', 'cloze')
    
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
    for task in tasks:
        if task['%Completado'] == 100:
            text_content += f"""
            <tr height="19">
                <td height="19"><b>{task['Tareas']}</b></td>
                <td align="right" style="text-align: center; "><b>{task['CPTP']}</b></td>
                <td align="right" style="text-align: center; "><b>{task['CRTR']}</b></td>
                <td align="right" style="text-align: center; "><b>{task['%Completado']}%</b></td>
            </tr>"""
        else:            
            if task['%Completado'] > 0:
                text_content += f"""
            <tr height="19">
                <td height="19">{task['Tareas']}</td>
                <td align="right" style="text-align: center; ">{task['CPTP']}</td>
                <td align="right" style="text-align: center; ">{task['CRTR']}</td>
                <td align="right" style="text-align: center; ">{task['%Completado']}%</td>
            </tr>"""   
            elif incomplete_task_found:
                text_content += f"""
                <tr height="19">
                    <td height="19">{task['Tareas']}</td>
                    <td align="right" style="text-align: center; ">{task['CPTP']}</td>
                    <td align="right" style="text-align: center; "></td>
                    <td align="right" style="text-align: center; "></td>
                </tr>"""
             
    text_content += f"""
        </tbody></table><br>Calcule:
        <p>El valor planificado (PV) en el momento actual {{1:NUMERICAL:%100%{valor_planificado}:0#}}</p>
        <p>El coste actual (AC) en el momento actual {{1:NUMERICAL:%100%{coste_actual}:0#}}</p>
        <p>El valor ganado (EV) en el momento actual {{1:NUMERICAL:%100%{valor_ganado}:0#}}</p>
        <p>El CPI del proyecto (con dos decimales) {{1:NUMERICAL:%100%{round(cpi,2)}:0.01#{valor_ganado}/{coste_actual}}}</p>
        <p>El SPI del proyecto (con dos decimales) {{1:NUMERICAL:%100%{round(spi,2)}:0.01#{valor_ganado}/{valor_planificado}}}</p><br><p></p>
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
    xml_str = etree.tostring(question, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('utf-8')
    
    with open('Tabla.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)

# Crear una pregunta nueva 
create_xml()