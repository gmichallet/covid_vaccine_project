# import necessary libraries
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://qxwnlxynpgfjcw:0a247bbdc12f42f2d44a8744c4924a14ee79a1841769476c5342bfee8692d817@ec2-54-90-211-192.compute-1.amazonaws.com:5432/d9ov1cv3red323').replace("://", "ql://", 1) or "postgresql://postgres:postgres@localhost:5432/flask"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

vaccine = create_classes(db)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        age = request.form["age"]
        gender = request.form["gender"]
        brand = request.form["brand"]
        symptoms = request.form["symptom"]
        lat = request.form["vaccineLat"]
        lon = request.form["vaccineLon"]

        vaccine = vaccine(age=age, gender=gender, brand=brand, symptoms=symptoms, lat=lat, lon=lon)
        db.session.add(vaccine)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/vaccine")
def pals():
    results = db.session.query(vaccine.age, vaccine.lat, vaccine.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(vaccine_data)


if __name__ == "__main__":
    app.run()
