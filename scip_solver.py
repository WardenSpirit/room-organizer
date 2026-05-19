from typing import Any
from pyscipopt import Model


M: int


def _init_big_m(room_size):
    global M
    M = sum(room_size)

def _create_items(model: Model, items: list[dict]):

    items_n = len(items)

    coords = {}
    sizes = {}
    rotations = {}

    for i in range(items_n):

        coords[i, 0] = model.addVar(name = f"item_coords_x_{i}")
        coords[i, 1] = model.addVar(name = f"item_coords_y_{i}")

        if "x" in items[i]:
            model.chgVarLb(coords[i, 0], items[i]["x"])
            model.chgVarUb(coords[i, 0], items[i]["x"])
        if "y" in items[i]:
            model.chgVarLb(coords[i, 1], items[i]["y"])
            model.chgVarUb(coords[i, 1], items[i]["y"])

        sizes[i, 0] = model.addVar(name = f"item_sizes_w_{i}")
        sizes[i, 1] = model.addVar(name = f"item_sizes_h_{i}")

        rotations[i] = model.addVar(vtype = "B", name = f"item_rotations_{i}")

    for i in range(items_n):
        default_width, default_height = items[i]["size"]
        model.addCons(
            sizes[i, 0] == (1 - rotations[i]) * default_width + rotations[i] * default_height,
            name = f"{i}'s effective width",
        )
        model.addCons(
            sizes[i, 1] == (1 - rotations[i]) * default_height + rotations[i] * default_width,
            name = f"{i}'s effective height",
        )

    return coords, sizes, rotations

def _constrain_items_in_room(model: Model, room_size, item_vars):

    coords, sizes, _ = item_vars
    items_n = len({i for (i, _) in coords})

    for i in range(items_n):
        model.addCons(coords[i, 0] + sizes[i, 0] <= room_size[0])
        model.addCons(coords[i, 1] + sizes[i, 1] <= room_size[1])

def _constrain_items_not_overlapping(model: Model, item_vars):

    coords, sizes, _ = item_vars
    relations: list[dict[int: dict[str, Any]]] = []
    items_n = len({i for (i, _) in coords})

    for i in range(items_n):
        relations.append({})
        for j in range(i + 1, items_n):

            left  = model.addVar(vtype = "B", name = f"{i}_left_from_{j}")
            right = model.addVar(vtype = "B", name = f"{i}_right_from_{j}")
            below = model.addVar(vtype = "B", name = f"{i}_below_{j}")
            above = model.addVar(vtype = "B", name = f"{i}_above_{j}")

            model.addCons(left + right + below + above >= 1, name = "one_relation_effective")

            model.addCons(coords[i, 0] + sizes[i, 0] <= coords[j, 0] + M * (1 - left), name = f"{i}_left_from_{j}")
            model.addCons(coords[j, 0] + sizes[j, 0] <= coords[i, 0] + M * (1 - right), name = f"{i}_right_from_{j}")
            model.addCons(coords[i, 1] + sizes[i, 1] <= coords[j, 1] + M * (1 - below), name = f"{i}_below_{j}")
            model.addCons(coords[j, 1] + sizes[j, 1] <= coords[i, 1] + M * (1 - above), name = f"{i}_above_{j}")

            model.addCons(coords[i, 0] + sizes[i, 0] >= coords[j, 0] - M * (left), name = f"{i}_not_left_from_{j}")
            model.addCons(coords[j, 0] + sizes[j, 0] >= coords[i, 0] - M * (right), name = f"{i}_not_right_from_{j}")
            model.addCons(coords[i, 1] + sizes[i, 1] >= coords[j, 1] - M * (below), name = f"{i}_not_below_{j}")
            model.addCons(coords[j, 1] + sizes[j, 1] >= coords[i, 1] - M * (above), name = f"{i}_not_above_{j}")

            relations[i][j] = {
                "left": left,
                "right": right,
                "below": below,
                "above": above
            }

    return (*item_vars, relations)

def _constrain_items_against_wall(model: Model, room_size, items, item_vars):

    coords, sizes, rotations, _ = item_vars
    items_n = len({i for (i, _) in coords})

    for i in range(items_n):
        item = items[i]
        if "against_wall" not in item:
            continue

        rule = item["against_wall"]
        if "allowed_walls" not in rule:
            walls = ["left", "right", "bottom", "top"]
        else:
            walls = rule["allowed_walls"]

        against_horizontal_walls = []
        against_vertical_walls = []
        if "left" in walls:
            against_left = model.addVar(vtype = "B", name = f"{i}_against_left_wall")
            against_horizontal_walls.append(against_left)
            model.addCons(coords[i, 0] <= 0 + M * (1 - against_left), name = f"{i}_against_left_wall")
        if "right" in walls:
            against_right = model.addVar(vtype = "B", name = f"{i}_against_right_wall")
            against_horizontal_walls.append(against_right)
            model.addCons(coords[i, 0] + sizes[i, 0] >= room_size[0] - M * (1 - against_right), name = f"{i}_against_right_wall")
        if "bottom" in walls:
            against_bottom = model.addVar(vtype = "B", name = f"{i}_against_bottom_wall")
            against_vertical_walls.append(against_bottom)
            model.addCons(coords[i, 1] <= 0 + M * (1 - against_bottom), name = f"{i}_against_bottom_wall")
        if "top" in walls:
            against_top = model.addVar(vtype = "B", name = f"{i}_against_top_wall")
            against_vertical_walls.append(against_top)
            model.addCons(coords[i, 1] + sizes[i, 1] >= room_size[1] - M * (1 - against_top), name = f"{i}_against_top_wall")

        if "with_side" not in rule:
            model.addCons(sum(against_horizontal_walls + against_vertical_walls) >= 1, name = "one_wall_effective")
        elif rule["with_side"] == "horizontal":
            model.addCons(sum(against_horizontal_walls) >= 1 - M * (rotations[i]), name = "one_horizontal_wall_effective_when_not_rotated")
            model.addCons(sum(against_vertical_walls) >= 1 - M * (1 - rotations[i]), name = "one_vertical_wall_effective_when_rotated")
        elif rule["with_side"] == "vertical":
            model.addCons(sum(against_horizontal_walls) >= 1 - M * (1 - rotations[i]), name = "one_horizontal_wall_effective_when_rotated")
            model.addCons(sum(against_vertical_walls) >= 1 - M * (rotations[i]), name = "one_vertical_wall_effective_when_not_rotated")

def _constrain_item_mutual_besideness(model, items, item_vars):
    coords, sizes, rotations, relations = item_vars
    items_n = len(rotations)

    for i in range(items_n):
        item = items[i]
        if "beside" not in item:
            continue

        besideness = item["beside"]
        j = next((i for i, iterated_item in enumerate(items) if iterated_item["name"] == besideness["name"]), None)

        # relations jsou jen pro i < j, takže musíme normalizovat pořadí
        if i < j:
            i_side = besideness["self_side"]
            j_side = besideness["that_side"]
        else:
            i, j = j, i
            i_side = besideness["that_side"]
            j_side = besideness["self_side"]

        relation = relations[i][j]
        left = relation["left"]
        right = relation["right"]
        below = relation["below"]
        above = relation["above"]

        if i_side == j_side:
            model.addCons(rotations[i] == rotations[j], name = "i_rotated_iff_j_rotated")
        else:
            model.addCons(rotations[i] + rotations[j] == 1, name = "exactly_one_of_i_and_j_rotated")

        if i_side == "horizontal":
            i_flipped_axis = rotations[i]
        else:
            i_flipped_axis = 1 - rotations[i]

        model.addCons(below + above <= 0 + M * (i_flipped_axis), name = "{i}_intersects_on_y_axis_with_{j}")
        model.addCons(left + right <= 0 + M * (1 - i_flipped_axis), name = "{i}_intersects_on_x_axis_with_{j}")

        model.addCons(coords[i,0] + sizes[i,0] >= coords[j,0] - M * (i_flipped_axis), name = "{i}_not_far_on_left_from_{j}")
        model.addCons(coords[i,0] <= coords[j,0] + sizes[j,0] + M * (i_flipped_axis), name = "{i}_not_far_on_right_from_{j}")
        model.addCons(coords[i,1] + sizes[i,1] >= coords[j,1] - M * (1 - i_flipped_axis), name = "{i}_not_far_below_{j}")
        model.addCons(coords[i,1] <= coords[j,1] + sizes[j,1] + M * (1 - i_flipped_axis), name = "{i}_not_far_above_{j}")

def _extract_distance_bonuses(model: Model, items, item_vars):
    coords, sizes, rotations, relations = item_vars
    items_n = len(rotations)

    expression = 0.0
    for i in range(items_n):
        item = items[i]
        if "distance_bonus" not in item:
            continue

        distance_bonus = item["distance_bonus"]
        j = next((i for i, iterated_item in enumerate(items) if iterated_item["name"] == distance_bonus["name"]), None)

        if i > j:
            i, j = j, i
        relation = relations[i][j]

        dx = model.addVar(lb = 0.0, ub = None, name = f"dx_between_{i}_{j}")
        dy = model.addVar(lb = 0.0, ub = None, name = f"dy_between_{i}_{j}")

        model.addCons(dx >= coords[j,0] - coords[i,0] - sizes[i,0])
        model.addCons(dx >= coords[i,0] - coords[j,0] - sizes[j,0])
        model.addCons(dx <= coords[j,0] - coords[i,0] - sizes[i,0] + M * (1 - relation["left"]))
        model.addCons(dx <= coords[i,0] - coords[j,0] - sizes[j,0] + M * (1 - relation["right"]))
        model.addCons(dx <= 0 + M * (relation["left"] + relation["right"]))
        model.addCons(dx >= 0 - M * (relation["left"] + relation["right"]))

        model.addCons(dy >= coords[j,1] - coords[i,1] - sizes[i,1])
        model.addCons(dy >= coords[i,1] - coords[j,1] - sizes[j,1])
        model.addCons(dy <= coords[j,1] - coords[i,1] - sizes[i,1] + M * (1 - relation["below"]))
        model.addCons(dy <= coords[i,1] - coords[j,1] - sizes[j,1] + M * (1 - relation["above"]))
        model.addCons(dy <= 0 + M * (relation["below"] + relation["above"]))
        model.addCons(dy >= 0 - M * (relation["below"] + relation["above"]))

        min_dd  = model.addVar(lb = 0.0, ub = None, name = f"min(dx,dy)_between_{i}_{j}")
        dx_gt_dy = model.addVar(vtype = "B", name = f"between_{i}_{j}_dx_is_higher_than_dy")

        model.addCons(min_dd <= dx)
        model.addCons(min_dd <= dy)
        model.addCons(min_dd >= dx - M * dx_gt_dy)
        model.addCons(min_dd >= dy - M * (1 - dx_gt_dy))

        dd  = model.addVar(lb = 0.0, ub = None, name = f"abs(dx-dy)_between_{i}_{j}")
        model.addCons(dd == dx + dy - 2 * min_dd)

        distance = (2**0.5) * min_dd + dd

        weight = distance_bonus["weight"] if "weight" in distance_bonus else 1
        expression += weight * distance

    return expression


def _get_result(model: Model, item_vars):

    coords, sizes, _, _ = item_vars
    items_n = len({i for (i, _) in coords})

    result = []
    for i in range(items_n):
        result.append({
            "x": model.getVal(coords[i, 0]),
            "y": model.getVal(coords[i, 1]),
            "w": model.getVal(sizes[i, 0]),
            "h": model.getVal(sizes[i, 1]),
        })

    return result

def solve(problem):

    room_size = problem["room_size"]
    items = problem["items"]

    model = Model()
    model.hideOutput()

    _init_big_m(room_size)

    item_vars = _create_items(model, items)

    _constrain_items_in_room(model, room_size, item_vars)
    item_vars = _constrain_items_not_overlapping(model, item_vars)
    _constrain_items_against_wall(model, room_size, items, item_vars)
    _constrain_item_mutual_besideness(model, items, item_vars)

    expr = 0.0
    expr -= _extract_distance_bonuses(model, items, item_vars)
    model.setObjective(expr)

    model.optimize()

    status = model.getStatus()
    if status not in ("optimal", "feasible"):
        raise RuntimeError(f"SCIP nenašel validní řešení (status: {status})")

    return _get_result(model, item_vars)