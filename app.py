from model import *
from model import ugovor
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO
from flask_cors import CORS
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'ugovor',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=json_deserializer,
    group_id='test-group',
    auto_offset_reset='earliest'
)

kafka_thread = None


@app.route("/")
def index ():
    classes = session.query(Ugovor).all()
    return render_template('classes.html', classes=classes)

@app.route("/classes/delete/<int:id_ugovora>", methods=["DELETE"])
def delete_class(id_ugovora):
    # ID se sada prenosi putem URL-a
    # Dohvati objekt Ugovor sa navedenim ID-om
    razred = session.query(Ugovor).get(id_ugovora)

    if Klijent:  # ako Ugovor s ovim ID-om postoji
        session.delete(Automobil)
        session.commit()
        # Uspješno izbrisano
        return jsonify({'message': f'Ugovor sa ID {id_ugovora} je izbrisan.'}), 200
    else:
        # Nema ugovora s ovim ID-om
        return jsonify({'message': f'Nema ugovora s ID {id_ugovora}.'}), 404

@app.route("/classes/<int:id_razreda>", methods=["GET"])
def get_class(id_ugovora):
    razred = region.get_or_create(
        f'Ugovor:{id_ugovora}', 
        creator=lambda: session.query(Ugovor).get(id_ugovora),
        expiration_time=60  # The time after which to expire the cache
    )
    if Klijent:
        # pretvoriti objekt Ugovor u rječnik
        # Uspješno dohvaćeno
        return jsonify([{"ID_ugovora": Automobil.ID_ugovora, "datum_zavrsetka": Automobil.datum_zavrsetka, "datum_pocetka": Automobil.datum_pocetka, "cijena": ugovor.cijena}]), 200
    else:
        # Nema Ugovora s ovim ID-om
        return jsonify({'message': f'Nema ugovora s ID {id_ugovora}.'}), 404

@app.route("/classes/edit", methods=["PUT"])
def edit_class():
    id_ugovora = request.form.get("ID_ugovora")
    datum_zavrsetka = request.form.get("datum_zavrestka")
    datum_pocetka = request.form.get("datum_pocetka")
    cijena = request.form.get("cijena")

    if id_ugovora:  
        # Dohvati objekt Ugovor sa navedenim ID-om
        ugovor = session.query(Ugovor).get(id_ugovora)
        if ugovor:  # ako Ugovor s ovim ID-om postoji
            # Ažurirati atribute objekta Ugovor
            if datum_zavrsetka: 
                ugovor.datum_zavrestka = datum_zavrsetka
            if datum_pocetka:
                ugovor.datum_pocetka = datum_pocetka
            if cijena: 
                ugovor.cijena = cijena
            
            session.commit()

            producer.send("ugovor", [{"ID_ugovora": ugovor.ID_ugovora, "datum_zavrestka": ugovor.datum_zavrestka, "datum_pocetka": ugovor.datum_pocetka, "cijena": ugovor.cijena}])
            producer.flush()

            # Uspješno ažurirano
            return jsonify({'message': f'Ugovor sa ID {id_ugovora} je ažuriran.'}), 200
        else:
            # Nema Razreda s ovim ID-om
            return jsonify({'message': f'Nema ugovora s ID {id_ugovora}.'}), 404
    else:
        # Nije pružen ID
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/classes/add", methods=["POST"])
def add_class():
    # Dohvati 'datum_zavrestka', 'datum_pocetka' i 'cijena'
    datum_zavrestka = request.form.get("datum_zavrestka")
    datum_pocetka = request.form.get("datum_pocetka")
    cijena = request.form.get("cijena")
    
    # Dodaj novi ugovor
    ugovor = Ugovor(datum_zavrestka=datum_zavrestka, datum_pocetka=datum_pocetka, cijena=cijena)
    session.add(ugovor)
    session.commit()

    producer.send("ugovor", [{"ID_ugovora": ugovor.ID_ugovora, "datum_zavrestka": ugovor.datum_zavrsetka, "datum_pocetka": ugovor.datum_pocetka, "cijena": ugovor.cijena}])
    producer.flush()

    # Dobra je praksa vratiti ispravan JSON zahtjev
    return jsonify({'message': 'Dodan novi ugovor u bazu.'})

@socketio.on('connect', namespace='/kafka')
def connect():
    global kafka_thread
    if kafka_thread is None or not kafka_thread.is_alive():
        kafka_thread = threading.Thread(target=kafka_consumer)
        kafka_thread.start()

def kafka_consumer():
    for poruka in consumer:
        ugovor = poruka.value
        socketio.emit('data', {'ugovor': ugovor}, namespace='/kafka')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)