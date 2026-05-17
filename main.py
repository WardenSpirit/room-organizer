import loader
import scip_solver as lp_solver
import visualizer


PROBLEM_FILE = "problem.json"


def main():
    problem = loader.load_problem(PROBLEM_FILE)
    result = lp_solver.solve(problem)
    visualizer.visualize(problem, result)

if __name__ == "__main__":
    main()
