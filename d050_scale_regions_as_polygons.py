# LATEST RESIZING SCRIPT
import os
import json
import numpy as np
import pandas as pd
import matplotlib.image as mpimg

pd.set_option('display.width', 500)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

os.makedirs("regions", exist_ok=True)
regions_file = "regions/regions.json"

if os.path.exists(regions_file):
    print("reloading")
    df = pd.read_json(regions_file, lines=True)
    df.index = df["label"]
else:
    print("new df")
    df = pd.DataFrame(columns=["x1", "y1", "x2", "y2", "label"])


df[["question", "response"]] = df["label"].str.replace("r", "").str.split("_", expand=True)

df[["tot_ht", "tot_wd"]] = pd.NA

for img_id in df["question"].unique():
    print(img_id)
    img_file = f"southbank/images/img{img_id}.png"
    img = mpimg.imread(img_file)
    tot_ht, tot_wd, _ = img.shape

    df.loc[df.question == img_id, "tot_ht"] = tot_ht
    df.loc[df.question == img_id, "tot_wd"] = tot_wd

df["tot_ht"] = df["tot_ht"].astype(float)
df["tot_wd"] = df["tot_wd"].astype(float)

df["wd"] = df["x2"] - df["x1"]
df["ht"] = df["y2"] - df["y1"]

df["width"]  = (100 * df["wd"] / df["tot_wd"]).round(2).astype(str) + "%"
df["height"] = (100 * df["ht"] / df["tot_ht"]).round(2).astype(str) + "%"

df["left"] = (100 * df["x1"] / df["tot_wd"]).round(2).astype(str) + "%"
df["top"]  = (100 * df["y1"] / df["tot_ht"]).round(2).astype(str) + "%"


df = df.rename(columns={"polygon": "polygon_list"})
df["polygon"] = ""
df
for i, r in df.iterrows():
    print(i)
    if r["polygon_list"]:
        polygon_string_list = []
        for x, y in r["polygon_list"]:
            xp = 100 * (x - r["x1"]) / r["wd"]
            yp = 100 * (y - r["y1"]) / r["ht"]
            scaled_coordinates = f"{round(xp, 2)}% {round(yp, 2)}%"
            polygon_string_list.append(scaled_coordinates)

        df.loc[i, "polygon"] = ", ".join(polygon_string_list)


# bckkp
df["_starTop"] = df["starTop"]
df["_starLeft"] = df["starLeft"]

df["starLeft"] = (100 * df["_starLeft"] / df["tot_wd"]).round(2).astype(str) + "%"
df["starTop"]  = (100 * df["_starTop"] / df["tot_ht"]).round(2).astype(str) + "%"

json_data = {}
for i, img_id in enumerate(df["question"].unique()):
    print(i, img_id)
    json_data[i] = df.rename(columns={"label": "id"}).loc[
        df.question == img_id,
        [
            "id",
            "question",
            "response",
            "left",
            "top",
            "width",
            "height",
            "starTop",
            "starLeft",
            "polygon",
        ]
    ].to_dict(orient="records")

json_data

with open("southbank/overlays.json", "wt") as fou:
    json.dump(json_data, fou, indent=2)


df
