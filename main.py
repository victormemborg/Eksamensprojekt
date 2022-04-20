#Importerer libraries 
import numpy as np
import os
from flask import Flask, request, render_template, redirect, url_for
import pickle
from werkzeug.utils import secure_filename
import tensorflow.keras
from PIL import Image, ImageOps

app = Flask(__name__)

#UPLOAD CONFIG
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#Loader pickle som der blev dannet i demo.ibynp. Denne bliver tildelt variablen "model"
model = pickle.load(open("static\data\Risiko.pkl", "rb"))

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
    np.set_printoptions(suppress=True)

    #Loader vores teachable machine.
    model = tensorflow.keras.models.load_model('static\data\Leukemia\keras_model.h5')

    #Former vores teachable machine data ind i et array.
    data = np.ndarray(shape=(1, 224, 224, 4), dtype=np.float32)
    image = Image.open('uploads\image.png')

    #Resizer billedet som brugeren har taget, så det passer perfekt til vores data.
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #Laver billedet som brugeren har taget om til et array, så den kan sammenligne med den data som AI har.
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    #Loader billedet ind i et array.
    data[0] = normalized_image_array


    #Sammenligner hvor meget billedet, som brugeren har taget, matcher med det data som AI har. 1 betyder at billedet er identitsk med de data som AI har. 
    prediction = model.predict(data)

    #Afrunder til 2 decimaler, og ganger med 100, for at få tallet i en procent.
    print("Resultater (hvor meget ligner billedet de to materialer):")
    print("Start: ", np.round(prediction[0][0]*100, decimals=2), "%")
    print("I udbrud: ", np.round(prediction[0][1]*100, decimals=2), "%")
    print("Før behandling: ", np.round(prediction[0][2]*100, decimals=2), "%")
    print("Efter behandling: ", np.round(prediction[0][3]*100, decimals=2), "%")
    return render_template("resultat.html")

if __name__ == "__main__":
    app.run(debug=True)