from flask import render_template, Flask, request, send_file, url_for, redirect
import src.Tabla
import src.ValorGanado
import src.ProgramacionGanada

app = Flask(__name__)
app.secret_key = 'Estoesunaclavesecreto'  # Clave secreta
DEBUG = True
PORT = 5000
app.config['UPLOAD_FOLDER'] = 'src'

@app.route('/')
def index():
    return render_template('inicio.html')

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
    idiomaT = request.form.get('idiomaT')
    src.Tabla.create_xml(tareasMax, rangoCostes, numPreguntas, idiomaT)
    return redirect(url_for('resultadoT'))

@app.route('/ProgramaValor', methods=['GET', 'POST'])
def ProgramaValor():
    if request.method == 'GET':
        return render_template('ProgramaValor.html')
    rangoTiempoV = request.form.get('rangoTiempoV')      
    rangoCostesV = request.form.get('rangoCostesV')
    numPreguntasV = int(request.form.get('numPreguntasV'))
    idiomaV = request.form.get('idiomaV')
    src.ValorGanado.EVM_xml(rangoTiempoV, rangoCostesV, numPreguntasV, idiomaV)
    return redirect(url_for('resultadoV'))

@app.route('/ProgramaProgramacion', methods=['GET', 'POST'])
def ProgramaProgramacion():
    if request.method == 'GET':
        return render_template('ProgramaProgramacion.html')
    rangoTiempoP = request.form.get('rangoTiempoP')      
    rangoCostesP = request.form.get('rangoCostesP')
    numPreguntasP = int(request.form.get('numPreguntasP'))
    idiomaP = request.form.get('idiomaP')
    src.ProgramacionGanada.ES_xml(rangoTiempoP, rangoCostesP, numPreguntasP, idiomaP)
    return redirect(url_for('resultadoP'))

@app.route('/resultadoV', methods=['GET', 'POST'])
def resultadoV():
    return render_template('resultadoV.html')

@app.route('/resultadoP', methods=['GET', 'POST'])
def resultadoP():
    return render_template('resultadoP.html')

@app.route('/resultadoT', methods=['GET', 'POST'])
def resultadoT():
    return render_template('resultadoT.html')

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

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    file_path = ''
    if filename == 'ValorGanado.xml':
        file_path = 'ValorGanado.xml'
    elif filename == 'Tabla.xml':
        file_path = 'Tabla.xml'
    elif filename == 'ProgramacionGanada.xml':
        file_path = 'ProgramacionGanada.xml'
    else:
        # Si se proporciona un nombre de archivo desconocido, devuelve un error 404
        return 'Archivo no encontrado', 404
    # Descargar el archivo
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)