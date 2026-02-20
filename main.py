import os
import numpy as np
from PIL import Image, ImagePalette, ImageColor
import pandas as pd
from flask import *
from flask_wtf import FlaskForm
from wtforms import IntegerField
from flask_wtf.file import FileField
from webcolors import hex_to_name, rgb_to_name, name_to_hex
import webcolors
from flask_bootstrap import Bootstrap4
from sklearn.cluster import KMeans


class UploadForm(FlaskForm):
    file = FileField()
    number = IntegerField()


def closest_colour(requested_colour):
    distances = {}
    for name in webcolors.names():
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        distances[name] = rd + gd + bd
    return min(distances, key=distances.get)


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


app = Flask(__name__)
bootstrap = Bootstrap4(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = "static"


def im_process(filename):
    image = Image.open(filename).resize((120,120)).convert("RGB")
    image = np.array(image)
    image_kmeans = image.reshape((-1,3))
    kmeans = KMeans(n_clusters=10, random_state=0, n_init="auto").fit(image_kmeans)
    rgb_centroids = tuple((kmeans.cluster_centers_).astype(int))
    colors_name = [get_colour_name(color)[1] for color in rgb_centroids]
    new_df = pd.DataFrame({"name":colors_name, "color":rgb_centroids,})
    color_set = set(list(kmeans.labels_))
    count = [list(kmeans.labels_).count(color) for color in color_set]
    new_df["count"] = count
    new_df["hex"]= [name_to_hex(color) for color in new_df["name"].values]
    constant = new_df["count"].sum()

    new_df["percentage"] = ((new_df["count"] / constant) * 100).round(2)
    print(count)
    print(new_df)

    return new_df.sort_values(by=["percentage"], ascending=False)


@app.route('/', methods=["GET", "POST"])
def index():
    new_df = pd.DataFrame(data={})
    form = UploadForm()

    if form.validate_on_submit():
        f = request.files['file']
        n = request.form.get("number")
        print(n)
        f.save(os.path.join("static", f.filename))
        new_df = im_process(f)
        return render_template("index.html", new_df=new_df, form=form, file=f)
    return render_template("index.html", form=form, new_df=new_df)


if __name__ == '__main__':
    app.run(debug=True)
