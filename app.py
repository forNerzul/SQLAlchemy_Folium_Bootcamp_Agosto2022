# importamos las librerias necesarias
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import folium



#CRUD - Create, Read, Update, Delete

# instanciamos la aplicacion Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Creando los modelos de la base de datos
class Emprendimientos(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    contacto = db.Column(db.String(10), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, descripcion, contacto, lat, lon):
        self.nombre = nombre
        self.descripcion = descripcion
        self.contacto = contacto
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return print(f'Emprendimiento: {self.nombre} Descripcion: {self.descripcion} Contacto: {self.contacto} Latitud: {self.lat} Longitud: {self.lon}')

    def __repr__(self):
        return print(f'Emprendimientos(nombre={self.nombre}, descripcion={self.descipciom}, contacto={self.contacto},lat={self.lat},lon={self.lon})')

# definimos la ruta de la aplicacion
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    # variables de coordenadas
    coor_mapa = [-25.302223289426216, -57.58111798774653]
    coor_1 = [-25.302223289426216, -57.58111798774653]

    #creacion del mapa
    mapa = folium.Map(location=coor_mapa, zoom_start=12)

    # creacion de los marcadores

    emprendimientos = Emprendimientos.query.all()
    for emprendimiento in emprendimientos:
        folium.Marker(location=[emprendimiento.lat, emprendimiento.lon], popup=f'''
                <h2>{emprendimiento.nombre}</h2>
                <p>{emprendimiento.descripcion}</p>
                <p>Tel.: {emprendimiento.contacto}</p>
            ''').add_to(mapa)

    folium.Marker(
        location=coor_1, 
        popup='''
                <h2>Penguin House 2.0</h2>
                <hr>
                <img src="static/img/penguin_house.jpeg" width="250px">
                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quisquam, quidem, ipsa, quis, saepe, ipsam, obcaecati, quos, ipsum, quas, dolorem, aliquam.</p>
                <h3>Servicios:</h3>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</li>
                    <li>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</li>
                    <li>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</li>
                </ul>

                <hr>
                <a href="#">WhatsApp</a>

            ''',
        tooltip="Penguin House 2.0",
        ).add_to(mapa)

    # guardamos el mapa en un archivo html
    mapa.save('templates/map.html')

    return render_template('map.html')

@app.route('/registro', methods=['GET', 'POST']) 
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        contacto = request.form['contacto']
        lat = request.form['latitud']
        lon = request.form['longitud']

        emprendimiento = Emprendimientos(nombre, descripcion, contacto, lat, lon)
        db.session.add(emprendimiento) # agregamos el emprendimiento a la base de datos
        db.session.commit()# guardamos los cambios en la base de datos

    return render_template('registro.html')

@app.route('/emprendimientos')
def emprendimientos():
    emprendimientos = Emprendimientos.query.all()
    return render_template('emprendimientos.html', emprendimientos=emprendimientos)

@app.route('/emprendimiento/<int:id>/borrar')
def borrar(id):
    emprendimiento = Emprendimientos.query.get(id)
    db.session.delete(emprendimiento)
    db.session.commit()

    return redirect(url_for('emprendimientos'))

@app.route('/geo')
def geo():
    # variables de coordenadas
    coor_mapa = [-25.302223289426216, -57.58111798774653]
    geojson = r'./static/geojson/paraguay.json'

    #creacion del mapa
    mapa = folium.Map(location=coor_mapa, zoom_start=6)

    mapa.get_root().html.add_child(folium.Element('<h1>Mapa de Paraguay</h1>'))
    mapa.get_root().html.add_child(folium.Element('<p>Este mapa muestra los departamentos de Paraguay</p>'))

    geo_object = folium.GeoJson(
        geojson, 
        name="paraguay"
    ).add_to(mapa)

    folium.GeoJsonTooltip(
        fields=["Departamento", "Numero"]
    ).add_to(geo_object)

    # guardamos el mapa en un archivo html
    mapa.save('templates/geo.html')

    return render_template('geo.html')



# con esta condicion no necesitamos ejecutar flask run y le decimos que inicie la aplicacion en modo debug    
if __name__ == '__main__':
    # creamos la base de datos al darle "python3 app.py"
    db.create_all()
    # iniciamos la aplicacion en modo debug para que se reinicie automaticamente cuando guardamos cambios
    app.run(debug=True)