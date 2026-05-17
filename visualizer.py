import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize(room_size, names, items):

    _, ax = plt.subplots(figsize=(10, 6))

    ax.add_patch(
        patches.Rectangle(
            (0, 0), room_size[0], room_size[1],
            fill=False, edgecolor="black", linewidth=3
        )
    )

    for i in range(len(items)):
        item = items[i]
        x, y = item["x"], item["y"]
        w, h = item["w"], item["h"]

        rect = patches.Rectangle(
            (x, y), w, h,
            fill = True, alpha = 0.4,
            edgecolor="blue"
        )
        ax.add_patch(rect)

        ax.text(
            x + w/2, y + h/2,
            f"{names[i]}",
            ha="center", va="center"
        )

    ax.set_xlim(0, room_size[0])
    ax.set_ylim(0, room_size[1])
    ax.set_aspect("equal")
    plt.show()
