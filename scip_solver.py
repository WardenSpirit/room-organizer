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
    # v coords jsou klíče (i, 0) a (i, 1)
    items_n = len({i for (i, _) in coords})

    for i in range(items_n):
        # LB už jsme dali při addVar, tady jen hranice místnosti
        model.addCons(coords[i, 0] + sizes[i, 0] <= room_size[0])
        model.addCons(coords[i, 1] + sizes[i, 1] <= room_size[1])

def _constrain_items_not_overlapping(model: Model, item_vars):

    coords, sizes, _ = item_vars
    items_n = len({i for (i, _) in coords})

    for i in range(items_n):
        for j in range(i + 1, items_n):

            left  = model.addVar(vtype="B", name = f"{i}_left_from_{j}")
            right = model.addVar(vtype="B", name = f"{i}_right_from_{j}")
            below = model.addVar(vtype="B", name = f"{i}_below_{j}")
            above = model.addVar(vtype="B", name = f"{i}_above_{j}")

            model.addCons(left + right + below + above >= 1, name="one_relation_effective")

            model.addCons(
                coords[i, 0] + sizes[i, 0] <= coords[j, 0] + M * (1 - left),
                name = f"{i}_left_from_{j}",
            )
            model.addCons(
                coords[j, 0] + sizes[j, 0] <= coords[i, 0] + M * (1 - right),
                name = f"{i}_right_from_{j}",
            )
            model.addCons(
                coords[i, 1] + sizes[i, 1] <= coords[j, 1] + M * (1 - below),
                name = f"{i}_below_{j}",
            )
            model.addCons(
                coords[j, 1] + sizes[j, 1] <= coords[i, 1] + M * (1 - above),
                name = f"{i}_above_{j}",
            )

def _get_result(model: Model, item_vars):

    coords, sizes, _ = item_vars
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
    _constrain_items_not_overlapping(model, item_vars)

    model.setObjective(0.0)
    model.optimize()

    status = model.getStatus()
    if status not in ("optimal", "feasible"):
        raise RuntimeError(f"SCIP nenašel validní řešení (status: {status})")

    return _get_result(model, item_vars)