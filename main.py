import loader
import scip_solver as lp_solver
import visualizer


INSTANCE = "problem.json"


def main():
    loader.load_problem(INSTANCE)
    result = lp_solver.solve(loader.ROOM_SIZE, loader.NAMES, loader.SIZES)
    visualizer.visualize(loader.ROOM_SIZE, loader.NAMES, result)

if __name__ == "__main__":
    main()
