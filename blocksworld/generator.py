import numpy as np

# 0 represents agent
#1 represents background
# -1 represents barricade
#other number represents blocks


# generate certian initial puzzle
def initial_test():
    initial_blocks = np.array([
        # [2, 1, 1, 1, 1, 1],
        # [5, 1, 1, 0, 1, 1],
        # [1, 1, 1, 4, 1, 1],
        # [1, 1, 1, 1, 1, 1],
        # [1, 1, 1, 1, 3, 1],
        # [1, 1, 1, 1, 1, 1]
        [2, 1, 1, 1],
        [1, 4, 1, 1],
        [1, 0, 3, 1],
        [1, 1, 1, 1]
        # [1, 1, 1],
        # [1, 1, 0],
        # [2, 3, 4]
        # [4, 1, 1, 2, 1],
        # [0, 1, 1, 1, -1],
        # [1, 1, -1, 1, 1],
        # [1, 1, 1, -1, 1],
        # [1, 1, 3, 1, 1]
                     ])
    return initial_blocks

#generate certain goal
def goal_test():
    goal_blocks = np.array([
        # [1, 1, 1, 5, 1, 1],
        # [2, 1, 1, 1, 0, 1],
        # [1, 1, 1, 1, 1, 1],
        # [1, 1, 1, 1, 3, 1],
        # [1, 1, 1, 4, 1, 1],
        # [1, 1, 1, 1, 1, 1]
        [1, 4, 1, 1],
        [1, 1, 3, 1],
        [1, 1, 0, 1],
        [1, 1, 2, 1]
        # [1, 4, 1],
        # [1, 3, 0],
        # [1, 2, 1]
        # [2, 1, 1, 1, 1],
        # [0, 1, 1, 1, -1],
        # [1, 1, -1, 1, 1],
        # [1, 3, 1, -1, 1],
        # [1, 1, 1, 4, 1]
                    ])
    return goal_blocks

# generate initial puzzle randomly
def initial_blocks(size=4, number_of_blocks=3, number_of_barricade=0):
    initial_puzzle = np.ones((size,size))
    list_cor = set()
    while len(list_cor) < number_of_blocks+number_of_barricade + 1:
        x = np.random.randint(0,size-1)
        y = np.random.randint(0,size-1)
        z = (x,y)
        list_cor.add(z)

    z = list_cor.pop()
    initial_puzzle[z]=0

    j = 2
    for i in range(number_of_blocks):
        z = list_cor.pop()
        initial_puzzle[z]= j
        j += 1

    for i in range(number_of_barricade):
        z=list_cor.pop()
        initial_puzzle[z] = -1

    return initial_puzzle

# generate goal randomly
def goal_blocks(initial_state):
    size= initial_state.shape[0]
    number_of_blocks=0
    for i in range(size):
        for k in range(size):
            if initial_state[i][k]!=1 and initial_state[i][k]!=0 and initial_state[i][k]!=-1:
                number_of_blocks+=1

    goal_puzzle = np.ones((size,size))

    barricade_list_original=np.where(initial_state==-1)
    barricade_list = []
    list_cor = set()
    for i in range(len(barricade_list_original[0])):
        x = barricade_list_original[0][i]
        y = barricade_list_original[1][i]
        z = (x,y)
        barricade_list.append(z)

    for i in barricade_list:
        list_cor.add(i)

    while len(list_cor) < number_of_blocks+len(barricade_list) + 1:
        x = np.random.randint(0,size-1)
        y = np.random.randint(0,size-1)
        z = (x,y)
        list_cor.add(z)

    while True:
        z = list_cor.pop()
        if z not in barricade_list:
            goal_puzzle[z]=0
            break
        else:
            list_cor.add(z)

    blocks_list= list_cor-set(barricade_list)
    j = 2
    for i in range(len(blocks_list)):
        z = blocks_list.pop()
        goal_puzzle[z]= j
        j += 1

    for i in range(len(barricade_list)):
        z=barricade_list.pop()
        goal_puzzle[z] = -1

    return goal_puzzle


# [1, 1, 1, 1],
# [1, 4, 1, 1],
# [1, 3, 1, 1],
# [0, 2, 1, 1]
# [1, 1, 1, 5, 1, 1],
# [2, 1, 1, 1, 0, 1],
# [1, 1, 1, 1, 1, 1],
# [1, 1, 1, 1, 3, 1],
# [1, 1, 1, 4, 1, 1],
# [1, 1, 1, 1, 1, 1]

if __name__ == "__main__":
    a=initial_blocks(4,3,0)
    print(a)
    print(goal_blocks(a))