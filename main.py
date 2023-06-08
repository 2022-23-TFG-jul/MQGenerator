from flask import render_template, Flask, request, send_file, url_for, redirect, flash , json, make_response, g, session, send_from_directory
import src.Tabla
import src.ValorGanado
import src.ProgramacionGanada
import tkinter as tk

app = Flask(__name__)
DEBUG = True
PORT = 5000
app.config['UPLOAD_FOLDER'] = 'src'

def esperar(tiempo):
    ventana.after(tiempo * 1000, ventana.destroy)

ventana = tk.Tk()
ventana.withdraw()
tiempo_espera = 5  # Tiempo en segundos
esperar(tiempo_espera)
ventana.mainloop()

@app.route('/')
def index():
    return render_template('registrarvista.html')

@app.route('/registrarvista', methods=['GET', 'POST'])
def registrarvista():
    return render_template('registrarvista.html')

@app.route('/loginvista', methods = ['GET','POST'])
def loginvista():
    return render_template('loginvista.html')

@app.route('/inicio', methods = ['GET','POST'])
def inicio():
    return render_template('inicio.html')

@app.route('/programas', methods = ['GET','POST'])
def programas():
    return render_template('programas.html')

@app.route('/principal', methods = ['GET','POST'])
def principal():
    return render_template('principal.html')

@app.route('/ProgramaTabla', methods = ['GET','POST'])
def ProgramaTabla():       
    if request.method == 'GET':
        return render_template('ProgramaTabla.html')
    tareasMax = int(request.form.get('tareasMax'))        
    rangoCostes = request.form.get('rangoCostes')
    numPreguntas = int(request.form.get('numPreguntas'))
    src.Tabla.create_xml(tareasMax, rangoCostes, numPreguntas)
    return render_template('ProgramaTabla.html')

@app.route('/ProgramaValor', methods=['GET', 'POST'])
def ProgramaValor():
    if request.method == 'GET':
        return render_template('ProgramaValor.html')
    rangoTiempoV = request.form.get('rangoTiempoV')      
    rangoCostesV = request.form.get('rangoCostesV')
    numPreguntasV = int(request.form.get('numPreguntasV'))
    #src.ValorGanado.EVM_xml(rangoTiempoV, rangoCostesV, numPreguntasV)
    try:
        src.ValorGanado.EVM_xml(rangoTiempoV, rangoCostesV, numPreguntasV)
        flash("El cálculo del valor ganado se ha completado correctamente.", "success")
    except Exception as e:
        flash("Error en el cálculo del valor ganado: " + str(e), "error")

    return render_template('ProgramaValor.html')

@app.route('/ProgramaProgramacion', methods=['GET', 'POST'])
def ProgramaProgramacion():
    if request.method == 'GET':
        return render_template('ProgramaProgramacion.html')
    rangoTiempoP = request.form.get('rangoTiempoP')      
    rangoCostesP = request.form.get('rangoCostesP')
    numPreguntasP = int(request.form.get('numPreguntasP'))
    #src.ProgramacionGanada.ES_xml(rangoTiempoP, rangoCostesP, numPreguntasP)
    try:
        src.ProgramacionGanada.ES_xml(rangoTiempoP, rangoCostesP, numPreguntasP)
        flash("El cálculo del valor ganado se ha completado correctamente.", "success")
    except Exception as e:
        flash("Error en el cálculo del valor ganado: " + str(e), "error")

    return render_template('ProgramaProgramacion.html')

def shutdown_server():
    # Detener el servidor Flask
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('No se pudo cerrar el servidor de manera adecuada')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'La aplicación se ha cerrado correctamente.'

#@app.route('/download/<path:filename>')
#def download_file(filename):
    # DEscargar  xml , recach
#    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.secret_key = 'key'  # Clave secreta para usar flash
    app.run(port = PORT, debug = DEBUG)