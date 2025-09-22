import os
from os import path
from collections import defaultdict

import numpy as np
from PIL import Image, ImagePalette, ImageColor
from PIL.ImageColor import getcolor
import pandas as pd
from flask import *
import webcolors
import easygui
from flask_wtf import FlaskForm
from wtforms import IntegerField
from flask_wtf.file import FileField
from webcolors import hex_to_name, rgb_to_name, name_to_hex
from werkzeug.utils import secure_filename
import webcolors
from flask_bootstrap import Bootstrap4
from matplotlib.colors import hex2color, XKCD_COLORS


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


def rgb_to_hex(r, g, b):
    return ('{:02X}' * 3).format(r, g, b)


def im_process(filename):
    raw_list = []
    image = np.array(Image.open(filename))

    for x in image:

        for y in x:
            raw_list.append(y)

    c_list = [tuple([item[0].item(), item[1].item(), item[2].item()]) for item in raw_list]

    names_list = [get_colour_name(color)[1] for color in c_list]
    color_series1 = pd.DataFrame({"color": c_list, "name": names_list, "count": 0})
    color_series1["count"] = color_series1.groupby("name")["name"].transform('count')
    new_df = color_series1.drop_duplicates(subset=["name"])
    constant = new_df["count"].sum()

    new_df["percentage"] = (new_df["count"] / constant) * 100
    color_hex = [name_to_hex(color) for color in new_df["name"].values]
    new_df["hex"] = color_hex
    print(new_df)

    return new_df.sort_values(by=["percentage"], ascending=False)[:10]


@app.route('/', methods=["GET", "POST"])
def index():
    colors_list = []
    new_df = pd.DataFrame(data={})
    form = UploadForm()

    if form.validate_on_submit():
        f = request.files['file']
        # filename = secure_filename(form.file.data.filename)
        # f.save(f.filename)
        f.save(os.path.join("static", f.filename))

        new_df = im_process(f)
        # new_df = im_process(f"C:/Users/olcza/Desktop/{filename}")
        # color_hex = [name_to_hex(color) for color in colors_list]
        print(colors_list)
        length = len(new_df.index)
        return render_template("index.html", new_df=new_df, form=form, length=length, file=f)
    return render_template("index.html", form=form, new_df=new_df)


if __name__ == '__main__':
    app.run(debug=True)
