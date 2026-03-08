import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import PolygonSelector, TextBox, Button

regions_file = "regions/regions.json"

print("reloading")
df = pd.read_json(regions_file, lines=True)
df.index = df["label"]

if "polygon" in df.columns:
    # df = df[df.polygon.isna()]
    pass
else:
    df['polygon'] = pd.NA


def get_polygon(img_id, polygon_id):

    img_file = f"southbank/images/img{img_id}.png"
    img = mpimg.imread(img_file)
    print("Image shape:", img.shape)

    current_polygon_verts = []
    region = {}

    def onselect(verts):
        """Callback for the PolygonSelector."""
        nonlocal current_polygon_verts
        # Convert vertices to a list of integer tuples
        current_polygon_verts = [(int(round(x)), int(round(y))) for x, y in verts]
        print(f"Selected polygon vertices: {current_polygon_verts}")
        plt.draw()

    def on_confirm(event):
        """Callback for the 'Confirm' button."""
        nonlocal current_polygon_verts
        nonlocal region
        label = text_box.text
        if current_polygon_verts and label:
            region["verts"] = current_polygon_verts
            region["label"] = label
            print("REGION I:", region)
            plt.close()
        else:
            print("SOMETHING MISSING")

    fig, ax = plt.subplots()

    # Make fullscreen
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()  # Toggle fullscreen mode
    # OR use one of these alternatives:
    # manager.window.showMaximized()  # For Qt backend (maximized window)
    # manager.resize(*manager.window.maxsize())  # For Tk backend

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0.18)
    ax.imshow(img)

    x1 = int(df.loc[label, "x1"])
    y1 = int(df.loc[label, "y1"])
    width = int(df.loc[label, "x2"] - df.loc[label, "x1"])
    height = int(df.loc[label, "y2"] - df.loc[label, "y1"])
    rect = plt.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='b', facecolor='none')
    ax.add_patch(rect)

    # Use PolygonSelector instead of RectangleSelector
    # Left-click to place vertices, right-click to remove the last one.
    # Press 'enter' or 'escape' to finish.
    _ = PolygonSelector(
        ax,
        onselect,
        useblit=True,
        props=dict(color='cyan', linestyle='-', linewidth=2, alpha=0.7),
        handle_props=dict(marker='o', markersize=5, markerfacecolor='white'),
    )

    axbox = plt.axes([0.1, 0.1, 0.3, 0.05])
    text_box = TextBox(axbox, "Label: ", initial=polygon_id)

    axbutton = plt.axes([0.5, 0.1, 0.15, 0.05])
    button = Button(axbutton, "Confirm")
    button.on_clicked(on_confirm)

    plt.show()

    print("REGION F:", region)
    return region


for label in df.loc[df.polygon.isna(), "label"]:
    print(label)
    img_id = label.replace("r", "").split("_")[0]
    res = get_polygon(img_id=img_id, polygon_id=label)
    df.at[label, "polygon"] = res["verts"]
    df.to_json(regions_file, orient="records", lines=True)
