import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import RectangleSelector, TextBox, Button

os.makedirs("regions", exist_ok=True)
regions_file = "regions/regions.json"

if os.path.exists(regions_file):
    print("reloading", flush=True)
    df = pd.read_json(regions_file, lines=True)
    df.index = df["label"]
else:
    print("new df", flush=True)
    df = pd.DataFrame(columns=["x1", "y1", "x2", "y2", "label"])


def get_rectangle(img_id, rectangle_id):

    img_file = f"southbank/images/img{img_id}.png"
    img = mpimg.imread(img_file)
    print("Image shape:", img.shape)

    # global current_rect
    current_rect = {}
    region = {}

    def onselect(eclick, erelease):
        nonlocal current_rect
        x1, y1 = int(round(eclick.xdata)), int(round(eclick.ydata))
        x2, y2 = int(round(erelease.xdata)), int(round(erelease.ydata))
        current_rect = {
            "x1": min(x1, x2),
            "y1": min(y1, y2),
            "x2": max(x1, x2),
            "y2": max(y1, y2),
        }
        print(f"Selected rectangle: {current_rect}")
        plt.draw()

    def on_confirm(event):
        nonlocal current_rect
        nonlocal region
        label = text_box.text
        if current_rect and label:
            region = current_rect.copy()
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

    _ = RectangleSelector(
        ax,
        onselect,
        useblit=True,
        button=[1],
        minspanx=5,
        minspany=5,
        spancoords="pixels",
        interactive=True,
    )

    axbox = plt.axes([0.1, 0.1, 0.3, 0.05])
    text_box = TextBox(axbox, "Label: ", initial=f"r{img_id}_{rectangle_id}")

    axbutton = plt.axes([0.5, 0.1, 0.15, 0.05])
    button = Button(axbutton, "Confirm")
    button.on_clicked(on_confirm)

    plt.show()

    print("REGION F:", region)
    return region


for img_id in ["{:02d}".format(i) for i in range(1, 14)]:
    for rectangle_id in range(1, 6):
        label = f"r{img_id}_{rectangle_id}"
        if label in df.index:
            print(label, "registered")
        else:
            print()
            print(label)
            res = get_rectangle(img_id=img_id, rectangle_id=rectangle_id)
            print("REGION Z:", res)
            df.loc[res["label"]] = res
            df.to_json(regions_file, orient="records", lines=True)
