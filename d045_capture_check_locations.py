import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import TextBox, Button

regions_file = "regions/regions.json"

print("reloading")
df = pd.read_json(regions_file, lines=True)
df.index = df["label"]

if "starTop" in df.columns:
    # df = df[df.starTop.isna()]
    pass
else:
    df["starTop"] = pd.NA
    df["starLeft"] = pd.NA


def get_point(img_id, point_id):

    img_file = f"southbank/images/img{img_id}.png"
    img = mpimg.imread(img_file)
    print("Image shape:", img.shape)

    current_point = None
    point_data = {}
    last_marker = None

    def on_click(event):
        """Callback for mouse click to capture coordinates."""
        nonlocal current_point, last_marker
        if event.inaxes is ax:
            # Remove previous marker
            if last_marker is not None:
                last_marker.remove()

            print("evento:", event)
                
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            current_point = (x, y)
            print(f"Captured point: x={x}, y={y}")
            # Mark the point on the image with a red dot
            last_marker = ax.plot(x, y, "r*", markersize=20)[0]
            plt.draw()

    def on_confirm(event):
        """Callback for the 'Confirm' button."""
        nonlocal current_point
        nonlocal point_data
        label = text_box.text
        if current_point and label:
            point_data["starLeft"] = current_point[0]
            point_data["starTop"] = current_point[1]
            point_data["label"] = label
            print("POINT DATA:", point_data)
            plt.close()
        else:
            print("POINT NOT CAPTURED OR LABEL MISSING")

    fig, ax = plt.subplots()

    # Make fullscreen
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()  # Toggle fullscreen mode
    # OR use one of these alternatives:
    # manager.window.showMaximized()  # For Qt backend (maximized window)
    # manager.resize(*manager.window.maxsize())  # For Tk backend

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0.18)
    ax.imshow(img)

    # Draw the rectangle for visual purposes
    x1 = int(df.loc[point_id, "x1"])
    y1 = int(df.loc[point_id, "y1"])
    width = int(df.loc[point_id, "x2"] - df.loc[point_id, "x1"])
    height = int(df.loc[point_id, "y2"] - df.loc[point_id, "y1"])
    rect = plt.Rectangle(
        (x1, y1), width, height, linewidth=2, edgecolor="b", facecolor="none"
    )
    ax.add_patch(rect)

    # Connect mouse click event
    fig.canvas.mpl_connect("button_press_event", on_click)

    axbox = plt.axes([0.1, 0.1, 0.3, 0.05])
    text_box = TextBox(axbox, "Label: ", initial=point_id)

    axbutton = plt.axes([0.5, 0.1, 0.15, 0.05])
    button = Button(axbutton, "Confirm")
    button.on_clicked(on_confirm)

    plt.show()

    print("POINT FINAL:", point_data)
    return point_data


for label in df.loc[df.starTop.isna(), "label"]:
    print(label)
    img_id = label.replace("r", "").split("_")[0]
    res = get_point(img_id=img_id, point_id=label)
    df.at[label, "starTop"] = res["starTop"]
    df.at[label, "starLeft"] = res["starLeft"]
    df.to_json(regions_file, orient="records", lines=True)
