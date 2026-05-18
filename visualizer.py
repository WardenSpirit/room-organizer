import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects


def visualize(problem, result):
    _, ax = plt.subplots(figsize = (10, 6))

    room_size = problem["room_size"]
    ax.add_patch(
        patches.Rectangle(
            (0, 0), room_size[0], room_size[1],
            fill = False, edgecolor = "black", linewidth = 3
        )
    )

    items = problem["items"]
    for i in range(len(items)):
        result_item = result[i]
        item = items[i]

        x, y = result_item["x"], result_item["y"]
        w, h = result_item["w"], result_item["h"]

        rect = patches.Rectangle(
            (x, y), w, h,
            fill = True, alpha = 0.6,
            facecolor = item.get("color", "blue"),
            edgecolor = item.get("color", "blue")
        )
        ax.add_patch(rect)

        ax.text(
            x + w/2, y + h/2,
            f"{item["name"]}",
            ha = "center", va = "center",
            fontweight = "bold",
            color = "white"
        ).set_path_effects([
            path_effects.Stroke(linewidth = 3, foreground = "black"),
            path_effects.Normal()
        ])

    ax.set_xlim(0, room_size[0])
    ax.set_ylim(0, room_size[1])
    ax.set_aspect("equal")
    plt.show()
