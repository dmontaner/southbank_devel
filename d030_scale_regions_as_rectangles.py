# THIS SCRIPT IS NOT NEEDED ANY MORE
import os
import json
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


df["wd"] = df["x2"] - df["x1"]
df["ht"] = df["y2"] - df["y1"]

df["width"]  = (100 * df["wd"] / tot_wd).round(2).astype(str) + "%"
df["height"] = (100 * df["ht"] / tot_ht).round(2).astype(str) + "%"

df["left"] = (100 * df["x1"] / tot_wd).round(2).astype(str) + "%"
df["top"]  = (100 * df["y1"] / tot_ht).round(2).astype(str) + "%"

df["polygon"] = '0% 0%, 100% 0%, 100% 100%, 0% 100%'  # full rectangle


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
            "polygon",
        ]
    ].to_dict(orient="records")

json_data

# NO NEED TO SAVE
with open("southbank/overlays.json", "wt") as fou:
    json.dump(json_data, fou, indent=2)
