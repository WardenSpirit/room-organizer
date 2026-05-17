import gurobipy as g


M: int


def _init_big_m(room_size):
    global M
    M = sum(room_size) 

def _create_items(model: g.Model, item_sizes):

    items_n = len(item_sizes)

    coords = model.addVars(items_n, 2, vtype=g.GRB.CONTINUOUS, name = "item_coords_x_y")
    sizes = model.addVars(items_n, 2, vtype=g.GRB.CONTINUOUS, name = "item_sizes_w_h")
    rotations = model.addVars(items_n, vtype=g.GRB.BINARY, name = "item_rotations")

    for i in range(items_n):
        model.addConstr(sizes[i, 0] == (1 - rotations[i]) * item_sizes[i][0] + rotations[i] * item_sizes[i][1], name = f"{i}'s effective width")
        model.addConstr(sizes[i, 1] == (1 - rotations[i]) * item_sizes[i][1] + rotations[i] * item_sizes[i][0], name = f"{i}'s effective height")

    return coords, sizes, rotations

def _constrain_items_in_room(model: g.Model, room_size, item_vars):

    coords, sizes, _ = item_vars

    items_n = len(coords)

    for i in range(items_n):
        coords[i, 0].LB = 0
        coords[i, 1].LB = 0

        model.addConstr(coords[i, 0] + sizes[i, 0] <= room_size[0])
        model.addConstr(coords[i, 1] + sizes[i, 1] <= room_size[1])

def _constrain_items_not_overlapping(model: g.Model, item_vars):

    coords, sizes, _ = item_vars
    items_n = len(coords)

    for i in range(items_n):
        for j in range(i + 1, items_n):

            left = model.addVar(vtype=g.GRB.BINARY, name=f"{i}_left_from_{j}")
            right = model.addVar(vtype=g.GRB.BINARY, name=f"{i}_right_from_{j}")
            below = model.addVar(vtype=g.GRB.BINARY, name=f"{i}_below_{j}")
            above = model.addVar(vtype=g.GRB.BINARY, name=f"{i}_above_{j}")

            model.addConstr(left + right + below + above >= 1, name = "one_relation_effective")
            model.addConstr(coords[i, 0] + sizes[i, 0] <= coords[j, 0] + M * (1 - left), name = f"{i}_left_from_{j}")
            model.addConstr(coords[j, 0] + sizes[j, 0] <= coords[i, 0] + M * (1 - right), name = f"{i}_right_from_{j}")
            model.addConstr(coords[i, 1] + sizes[i, 1] <= coords[j, 1] + M * (1 - below), name = f"{i}_below_{j}")
            model.addConstr(coords[j, 1] + sizes[j, 1] <= coords[i, 1] + M * (1 - above), name = f"{i}_above_{j}")

def _get_result(item_vars):

    coords, sizes, _ = item_vars
    items_n = len(coords)

    result = []
    for i in range(items_n):
        result.append({
            "x": coords[i, 0].X,
            "y": coords[i, 1].X,
            "w": sizes[i, 0].X,
            "h": sizes[i, 1].X,
        })

    return result

def solve(room_size, names, sizes):
    model = g.Model()

    _init_big_m()

    item_vars = _create_items(model, sizes)

    _constrain_items_in_room(model, room_size, item_vars)
    _constrain_items_not_overlapping(model, item_vars)

    model.optimize()

    return _get_result(item_vars)