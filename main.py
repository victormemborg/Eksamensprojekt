#Importerer libraries 
import numpy as np
import os
from flask import Flask, request, render_template, redirect, url_for
import pickle
from werkzeug.utils import secure_filename
from keras.models import load_model
from PIL import Image, ImageOps

app = Flask(__name__)

#UPLOAD CONFIG
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#Loader pickle som der blev dannet i demo.ibynp. Denne bliver tildelt variablen "model"
model = pickle.load(open("static\data\Risiko.pkl", "rb"))

#ML funktion
def ml():
    #Loader modellen.
    model = load_model('static\data\Leukemia\keras_model.h5')

    #Opstiller array'et som der skal feedes til keras modellen.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    #Loader billedet, som brugeren har uploadet
    image = Image.open('uploads\image.png')
    
    #Resizer billedet til 224x224 og beskære det til midten.
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #Indsætter billedet i et numpy array.
    image_array = np.asarray(image)

    #Normaliserer array.
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    #Feeder modellen med dataen.
    prediction = model.predict(data)

    #variable der skal bruges på frontend siden, samt viser det procentvis.
    global startfase
    global udbrud 
    global prebehandling
    global probehandling
    startfase = np.round(prediction[0][0]*100, decimals=2)
    udbrud = np.round(prediction[0][1]*100, decimals=2)
    prebehandling = np.round(prediction[0][2]*100, decimals=2)
    probehandling = np.round(prediction[0][3]*100, decimals=2)



#Laver et index route, som indlæser "index.html"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/model")
def cancer():
    return render_template("skema.html")

#Laver en /predict route, som poster de informationer, som er blevet indtastet af brugeren.
@app.route("/predict", methods=["POST"])
def predict():

    int_features = [int(x) for x in request.form.values()]
    print(int_features)
    final_features = [np.array(int_features)]
    print(final_features)
    prediction = model.predict(final_features)

    output = prediction[0]

    risiko = ["Nej", "Ja"]

#Laver en text, som giver den sandsynlige løn.
    return render_template(
        "skema.html", prediction_text="Risiko for blodprop: {}".format(risiko[output])
    )

@app.route("/cancer")
def genkender():
    return render_template("genkender.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['filename[]']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], "image.png"))
      return redirect(url_for('resultat'))

@app.route("/result")
def resultat():
    ml()
    return render_template('resultat.html', start=startfase, udbrud=udbrud, prebe=prebehandling, probe=probehandling)

if __name__ == "__main__":
    app.run(debug=True)