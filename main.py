#Importerer libraries 
import numpy as np
from flask import Flask, request, render_template
import pickle
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static\data\Leukemia\Billede"

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

    int_features = request.form['userinput']
    #int_features = [int(x) for x in request.form.values()]
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
      f = request.files['filename']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(debug=True)