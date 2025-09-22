import numpy as np
import pandas as pd
from PIL import Image
from collections import defaultdict

from webcolors import hex_to_name, rgb_to_name, name_to_hex

# Open an image
im = Image.open("C:/Users/olcza/Desktop/image.jpg")


def rgb_to_hex(r, g, b):
    return ('{:02X}' * 3).format(r, g, b)


def im_process(filename):
    raw_list = []
    image = np.array(Image.open(filename))
    print(im.size)
    for x in image:

        for y in x:
            raw_list.append(y)
    c_list = [tuple([item[0].item(), item[1].item(), item[2].item()]) for item in raw_list]

    color_series = pd.Series(data=c_list).value_counts().index.tolist()

    color_series1 = pd.DataFrame({"color": c_list,"name":"","count":0})
    color_text_list = []
    for color in color_series1["color"]:
        try:
            name = rgb_to_name(color)
        except ValueError:
            name = "gray"
        color_text_list.append(name)
    color_series1["name"] = color_text_list
    color_series1["count"] = color_series1.groupby("name")["name"].transform('count')
    new_df = color_series1.drop_duplicates(subset=["name"])
    constant = new_df["count"].sum()
    print(constant)

    new_df["percentage"] = (new_df["count"] / constant) * 100
    # color_s = pd.DataFrame(data=color_text_list, columns=["color"]).drop_duplicates()[:30]
    color_names = [color for color in new_df["name"].values]
    color_hex = [name_to_hex(color) for color in new_df["name"].values]
    new_df["hex"] = color_hex
    print(new_df)

    # # color_names = [hex_to_name(item) for item in color_text_list]
    #

@app.route('/', methods=["GET", "POST"])
def index():
    colors_list = []

    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        colors_list = im_process(f"C:/Users/olcza/Desktop/{filename}")
        color_hex = [name_to_hex(color) for color in colors_list]
        print(colors_list)

        return render_template("index.html", colors_list=colors_list, form=form, filename=filename, color_hex=color_hex)
    return render_template("index.html", form=form)
im_process("C:/Users/olcza/Desktop/image.jpg")
