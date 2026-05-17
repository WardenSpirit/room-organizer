import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize(problem, result):
    _, ax = plt.subplots(figsize=(10, 6))

    room_size = problem["room_size"]
    ax.add_patch(
        patches.Rectangle(
            (0, 0), room_size[0], room_size[1],
            fill=False, edgecolor="black", linewidth=3
        )
    )

    items = problem["items"]
    for i in range(len(items)):
        item = result[i]
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
            f"{items[i]["name"]}",
            ha="center", va="center"
        )

    ax.set_xlim(0, room_size[0])
    ax.set_ylim(0, room_size[1])
    ax.set_aspect("equal")
    plt.show()
