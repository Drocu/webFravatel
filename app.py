from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import text
import datetime

app = Flask(__name__)

def create_graph():
    # Configuracion al DB
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://diafaan:Fr4v4t3l.2024$@172.24.3.180/smsserver'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    #Ruta Principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Ruta para obtener los datos para lso graficos:
    @app.route('/data/<gateway>')
    def get_data(gateway):

        # obtener la fecha actual
        today = datetime.date.today()

        # Realiza la consulta para el gateway especifico
        query = text("""
            SELECT StatusCode, COUNT(*)
            FROM smsserver.messagelog
            WHERE Date(SendTime) = :today
            AND Gateway = :gateway
            GROUP BY StatusCode
        """)
        
        try:
            # Ejecutar la consulta con los parametros
            results = db.session.execute(query, {'today':today, 'gateway': gateway}).fetchall()
        except Exception as e:
            return jsonify({'error': str(e)}),500


        # Inicialzar los datos para los estados
        status_code = [200,201,300,301]
        data_dict = {status: 0 for status in status_code}

        # Agregar los datos de la consulta al diccionario
        for row in results:
            data_dict[row[0]] = row[1]

        # Prepara las etiquietas y valores para el frontend
        labels = list(data_dict.keys())
        values = list(data_dict.values())

        return jsonify({'labels':labels, 'values': values})
    
if __name__ == '__main__':
    app.run(debug=True)
