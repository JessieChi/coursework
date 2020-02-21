from BFS import BFS
from DFS import DFS
from ID_DFS import ID_DFS
from A_star import A_star
import generator


# Print out the solution found by the algorithm
def print_solution(final_puzzle):
    # print(final_puzzle.array)
    solution = list()
    while final_puzzle.parent_action != None:
        solution.insert(0, final_puzzle.parent_action)
        final_puzzle = final_puzzle.parent_puzzle
    print(solution)


# Print out the solution found by the algorithm as blocks
def print_blocks_path(final_puzzle):
    while final_puzzle.parent_action != None:
        print(final_puzzle.array)
        final_puzzle = final_puzzle.parent_puzzle
    print(final_puzzle.array)


# Print out some of the details of the solution
def print_detail(result):
    if result["is_found"]:
        print("Successful!!!")
        print("Solution:")
        if result["steps"] > 500:
            print("need more than 500 steps")
        else:
            # pass
            print_solution(result["final_puzzle"])
        print("steps：" + str(result["steps"]))
        print("time：" + str(result["time"]))
        print("iterations：" + str(result["iterations"]))
        # print_blocks_path(result["final_puzzle"])
    else:
        print("Unsuccesful:(")
        print("time：" + str(result["time"]))
        print("iterations：" + str(result["iterations"]))
    print("")


# Find solution
def find_solution(size=4, number_of_blocks=3, number_of_barricade=0, initial_array=None,
                  goal_array=None, repeat_time=2):
    results = {}
    methods = ["bfs", "dfs", "id_dfs", "a_star"]

    single_result = None
    for method in methods:
        results[method] = {}
        results[method]["times"] = []
        results[method]["iterations"] = []
        results[method]["steps"] = []

    for i in range(repeat_time):
        print("")

        # print("BFS")
        # BFSTool = BFS(size, number_of_blocks, number_of_barricade,initial_array,goal_array)
        # single_result = BFSTool.bfs()
        # print_detail(single_result)
        # results["bfs"]['times'].append(single_result["time"])
        # results["bfs"]['iterations'].append(single_result["iterations"])
        # results["bfs"]['steps'].append(single_result["steps"])
        #
        # initial_array = single_result["initial_puzzle"].array
        # goal_array = single_result["final_puzzle"].array
        #
        print("DFS")
        DFSTool = DFS(size, number_of_blocks, number_of_barricade,initial_array,goal_array)
        single_result = DFSTool.dfs()
        print_detail(single_result)
        results["dfs"]['times'].append(single_result["time"])
        results["dfs"]['iterations'].append(single_result["iterations"])
        results["dfs"]['steps'].append(single_result["steps"])
        #
        # print("ID_DFS")
        # ID_DFSTool = ID_DFS(size, number_of_blocks, number_of_barricade,initial_array,goal_array)
        # single_result = ID_DFSTool.id_dfs()
        # print_detail(single_result)
        # results["id_dfs"]['times'].append(single_result["time"])
        # results["id_dfs"]['iterations'].append(single_result["iterations"])
        # results["id_dfs"]['steps'].append(single_result["steps"])
        #
        # print("A*")
        # A_star_Tool = A_star(size, number_of_blocks, number_of_barricade,initial_array,goal_array)
        # single_result = A_star_Tool.a_star()
        # print_detail(single_result)
        # results["a_star"]['times'].append(single_result["time"])
        # results["a_star"]['iterations'].append(single_result["iterations"])
        # results["a_star"]['steps'].append(single_result["steps"])

    initial_puzzle = single_result["initial_puzzle"]
    distance = initial_puzzle.manhattan_distance()

    return distance, results


if __name__ == "__main__":
    initial = generator.initial_test()
    goal = generator.goal_test()

    results = find_solution(4, 3, 0,initial,goal)
    print(results[1])




    # record_time = {"bfs":[], "dfs":[], "id_dfs":[], "a_star":[]}
    # record_iteration = {"bfs": [], "dfs": [], "id_dfs": [], "a_star": []}
    # for i in range(8):
    #     total_results = solve_blocksword_puzzle(4, 7, 0)
    #     record_time["bfs"].append(sum(total_results[1]["bfs"]["times"])/ len(total_results[1]["bfs"]["times"]))
    #     record_time["dfs"].append(sum(total_results[1]["dfs"]["times"]) / len(total_results[1]["dfs"]["times"]))
    #     record_time["id_dfs"].append(sum(total_results[1]["id_dfs"]["times"]) / len(total_results[1]["id_dfs"]["times"]))
    #     record_time["a_star"].append(sum(total_results[1]["a_star"]["times"]) / len(total_results[1]["a_star"]["times"]))
    #     record_iteration["bfs"].append(sum(total_results[1]["bfs"]["iterations"]) / len(total_results[1]["bfs"]["iterations"]))
    #     record_iteration["dfs"].append(sum(total_results[1]["dfs"]["iterations"]) / len(total_results[1]["dfs"]["iterations"]))
    #     record_iteration["id_dfs"].append(sum(total_results[1]["id_dfs"]["iterations"]) / len(total_results[1]["id_dfs"]["iterations"]))
    #     record_iteration["a_star"].append(sum(total_results[1]["a_star"]["iterations"]) / len(total_results[1]["a_star"]["iterations"]))
    #
    # print(record_iteration,record_time)

    # bfs_time=sum(total_results[1]["bfs"]["times"]) / len(total_results[1]["bfs"]["times"])
    # dfs_time=sum(total_results[1]["dfs"]["times"]) / len(total_results[1]["dfs"]["times"])
    # id_dfs_time = sum(total_results[1]["id_dfs"]["times"]) / len(total_results[1]["id_dfs"]["times"])
    # a_star_time = sum(total_results[1]["a_star"]["times"]) / len(total_results[1]["a_star"]["times"])
    # bfs_iteration = sum(total_results[1]["bfs"]["iterations"]) / len(total_results[1]["bfs"]["iterations"])
    # dfs_iteration = sum(total_results[1]["dfs"]["iterations"]) / len(total_results[1]["dfs"]["iterations"])
    # id_dfs_iteration = sum(total_results[1]["id_dfs"]["iterations"]) / len(total_results[1]["id_dfs"]["iterations"])
    # a_star_iteration = sum(total_results[1]["a_star"]["iterations"]) / len(total_results[1]["a_star"]["iterations"])
    # print(bfs_time,dfs_time,id_dfs_time,a_star_time,bfs_iteration,dfs_iteration,id_dfs_iteration,a_star_iteration)

    # complexity=[]
    # bfs_time = []
    # dfs_time = []
    # id_dfs_time = []
    # a_star_time = []
    # bfs_iteration = []
    # dfs_iteration = []
    # id_dfs_iteration = []
    # a_star_iteration = []
    # for i in range(15):
    #     total_results = solve_blocksword_puzzle(4,3,0)
    #     complexity.append(total_results[0])
    #     bfs_time.append(sum(total_results[1]["bfs"]["times"]) / len(total_results[1]["bfs"]["times"]))
    #     dfs_time.append(sum(total_results[1]["dfs"]["times"]) / len(total_results[1]["dfs"]["times"]))
    #     id_dfs_time.append(sum(total_results[1]["id_dfs"]["times"]) / len(total_results[1]["id_dfs"]["times"]))
    #     a_star_time.append(sum(total_results[1]["a_star"]["times"]) / len(total_results[1]["a_star"]["times"]))
    #     bfs_time.append(sum(total_results[1]["bfs"]["iterations"]) / len(total_results[1]["bfs"]["iterations"]))
    #     bfs_time.append(sum(total_results[1]["dfs"]["iterations"]) / len(total_results[1]["dfs"]["iterations"]))
    #     bfs_time.append(sum(total_results[1]["id_dfs"]["iterations"]) / len(total_results[1]["id_dfs"]["iterations"]))
    #     bfs_time.append(sum(total_results[1]["a_star"]["iterations"]) / len(total_results[1]["a_star"]["iterations"]))
    #
    # l1, = plt.plot(complexity, bfs_time, "r")
    # l2, = plt.plot(complexity, dfs_time, "k")
    # l3, = plt.plot(complexity, id_dfs_time, "b")
    # l4, = plt.plot(complexity, a_star_time, "g")
    # plt.legend(handles=[l1, l2, l3, l4], labels=['bfs', 'dfs', "id_dfs", "a_star"], loc='best')
    # plt.xlabel('Distance')
    # plt.ylabel('time')
    # plt.show()
    #
    # l1, = plt.plot(complexity, bfs_iteration, "r")
    # l2, = plt.plot(complexity, dfs_iteration, "k")
    # l3, = plt.plot(complexity, id_dfs_iteration, "b")
    # l4, = plt.plot(complexity, a_star_iteration, "g")
    # plt.legend(handles=[l1, l2, l3, l4], labels=['bfs', 'dfs', "id_dfs", "a_star"], loc='best')
    # plt.xlabel('Distance')
    # plt.ylabel('iteration')
    # plt.show()
