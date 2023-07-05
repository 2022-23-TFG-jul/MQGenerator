![image](https://github.com/xhm1001/MQGenerator/assets/74598820/235dfdf7-b1d5-44d8-a995-0a450fb3c967)

# MQGenerator

Esta aplicación web es un proyecto relizado por la Universidad de Burgos que utiliza una herramienta automática de generación de cuestionarios para la plataforma Moodle, a partir de ficheros .XML creados completamente en lenguaje Python.
La aplicación web constará de una interfaz gráfica donde los usuarios deben seleccionar entre los diferentes tipos de preguntas y rellenar los datos necesarios para que la herramienta genere automáticamente problemas de control integrado de proyectos, fundamentalmente mediante técnicas de valor ganado y programación.

En este repositorio de GitHub se encuentra toda la información sobre el desarroyo del proyecto, en la carpeta "doc" con toda la documentación necesaria y los manuales de uso de la aplicación.

## Instalación en local:

Para la instalación de todos los componentes necesarios para el despliegue de la aplicación en local, sólo debemos de instalar los componentes necesarios que usaremos que serán los siguientes:

* **Python:** *versión 3.9.13*
* **Flask:** *versión 2.3.2*
* **lxml:** *versión 4.9.2*
* **matplotlib:** *3.7.1*
* **numpy:** *versión 1.24.3*
* **Pillow:** *versión 9.5*
* **gunicorn:** *versión 20.1*

Estos requisitos se pueden instalar mediante la ejecución del  comando: 

    $ pip install -r requirements.txt

Después  nos ubicamos en la carpeta donde se encuentre el proyecto y ejecutaremos el comando:

    $ python main.py

Para que el proyecto esté corriendo en local:

![image](https://github.com/xhm1001/MQGenerator/assets/74598820/b0cc729f-6251-43f6-8890-7f0c08ec3bba)

Finalmente la línea de comandos deberá mostrar, con diferente ruta de directorios, una dirección http://127.0.0.1:5000/ y ya podremos utilizar la aplicación en local en el navegador web.

## Aplicación desplegada:

La aplicación web está  desplegada en Heroku.
Para poder acceder a la aplicación se debe acceder al siguiente link: 
https://mqgenerator.herokuapp.com/ .

------------------------------------------------------------------------------------------------------------------------------------

# MQGenerator

This web application is a project carried out by the University of Burgos that uses an automatic questionnaire generation tool for the Moodle platform, based on .XML files created entirely in Python language.
The web application will consist of a graphical interface where users must select between different types of questions and fill in the necessary data for the tool to automatically generate integrated project control problems, mainly through earned value and scheduling techniques.

In this GitHub repository you can find all the information about the development of the project, in the "doc" folder with all the necessary documentation and the user manuals of the application.

## Local instalation:

For the installation of all the necessary components for the deployment of the application locally, we only need to install the necessary components that we will use, which will be the following:

* **Python:** *versión 3.9.13*
* **Flask:** *versión 2.3.2*
* **lxml:** *versión 4.9.2*
* **matplotlib:** *3.7.1*
* **numpy:** *versión 1.24.3*
* **Pillow:** *versión 9.5*
* **gunicorn:** *versión 20.1*

These requirements can be installed by executing the command: 

    $ pip install -r requirements.txt

Then we go to the folder where the project is located and execute the command:

    $ python main.py

For the project to be running localy:

![image](https://github.com/xhm1001/MQGenerator/assets/74598820/b0cc729f-6251-43f6-8890-7f0c08ec3bba)

Finally, the command line should display, with a different directory path, an address http://127.0.0.1:5000/ and you will be able to use the application locally in the web browser.

## Application deployed:

The web application is deployed on Heroku.
To access the application you must access the following link: 
https://mqgenerator.herokuapp.com/ .
