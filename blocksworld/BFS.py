import queue
from collections import deque
import datetime as dt
import generator
from Node import Puzzle
import numpy as np


class BFS:
    def __init__(self, size=4, number_of_blocks=3, number_of_barricade=0, initial_puzzle_array=None, goal_array=None):
        if initial_puzzle_array is None :
            blocks = generator.initial_blocks(size, number_of_blocks, number_of_barricade)
            self.initial_puzzle = Puzzle(blocks, generator.goal_blocks(blocks))
        else:
            self.initial_puzzle = Puzzle(initial_puzzle_array, goal_array)
        self.puzzle = self.initial_puzzle
        self.iterations = 0
        self.container = None
        self.checked = {}
        self.is_found = False

    def is_goal(self, blocks, goal):
        if np.count_nonzero(blocks != goal) == 0:
            return True
        elif np.count_nonzero(blocks != goal) == 2:
            test1 = np.copy(blocks)
            test2 = np.copy(goal)
            test1[test1 == 0] = 1
            test2[test2 == 0] = 1
            if np.count_nonzero(test1 != test2) == 0:
                return True
        return False

    def is_contained(self, element, container):
        return element in container

    # Convert the element to the appropriate storage form
    def puzzle_store(self):
        puzzle_store_format = self.puzzle.puzzle_store_format()
        return puzzle_store_format

    # Criteria for the end of all search algorithm
    def is_target(self):
        return self.is_goal(self.puzzle.array, self.puzzle.goal_state)

    # New element added to container
    def valid_sub(self):
        valid_sub = []
        next_generation = self.puzzle.next_generation()
        for one in next_generation:
            # graph search
            # if not self.is_contained(one.puzzle_store_format(), self.checked):
            #     valid_sub.append(one)

            #tree search
            valid_sub.append(one)
        return valid_sub

    def updated_container_bfs(self):
        updated_container = self.container
        sub = self.valid_sub()
        for i in sub:
            updated_container.append(i)
        return updated_container

    def updated_checked_bfs(self):
        updated_checked = self.checked
        updated_checked.add(self.puzzle_store())
        return updated_checked

    # Breadth First Search
    def bfs(self):
        self.iterations = 0
        self.container = deque()
        self.checked = set()
        self.puzzle = self.initial_puzzle
        self.container.append(self.puzzle)
        start = dt.datetime.now()
        while len(self.container) > 0:
            if self.iterations > 10000000:
                self.is_found =  False
                end = dt.datetime.now()
                result = {'final_puzzle': self.puzzle,
                          "is_found": self.is_found,
                          "iterations": self.iterations,
                          "steps": self.puzzle.steps,
                          "time": end - start,
                          "initial_puzzle": self.initial_puzzle}
                return result

            self.puzzle = self.container.popleft()
            self.checked = self.updated_checked_bfs()
            self.container = self.updated_container_bfs()
            self.iterations += 1

            if self.is_target():
                self.is_found = True
                end = dt.datetime.now()
                result = {'final_puzzle': self.puzzle,
                          "is_found": self.is_found,
                          "iterations": self.iterations,
                          "steps": self.puzzle.steps,
                          "time": end - start,
                          "initial_puzzle": self.initial_puzzle}
                return result

        self.is_found = False
        end = dt.datetime.now()
        result = {'final_puzzle': self.puzzle,
                  "is_found": self.is_found,
                  "iterations": self.iterations,
                  "steps": self.puzzle.steps,
                  "time": end - start,
                  "initial_puzzle": self.initial_puzzle}
        return result
