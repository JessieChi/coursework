from queue import PriorityQueue
import datetime as dt
import generator
from Node import Puzzle
import numpy as np


class A_star:
    def __init__(self, size=4, number_of_blocks=3, number_of_barricade=0, initial_puzzle_array=None, goal_array=None):
        if initial_puzzle_array is None:
            blocks = generator.initial_blocks(size, number_of_blocks, number_of_barricade)
            self.initial_puzzle = Puzzle(blocks, generator.goal_blocks(blocks))
        else:
            self.initial_puzzle = Puzzle(initial_puzzle_array, goal_array)
        self.puzzle = self.initial_puzzle
        self.iterations = 0
        self.container = None
        self.checked = {}
        self.is_found = False

    def is_contained(self, element, container):
        return element in container

    # Computes the value of the heuristic function for the current state
    def to_goal(self, blocks):
        return blocks.manhattan_distance()

    # Calculate the elements in the priority queue
    def element_in_prio(self, puzzle1, puzzle2):
        to_goal = self.to_goal(puzzle2)
        evaluation = puzzle1.steps + to_goal
        return evaluation, puzzle1

    # Determine whether the current state is already the target state
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

            # tree search
            valid_sub.append(one)
        return valid_sub

    def updated_checked_a_star(self):
        updated_checked = self.checked
        updated_checked.add(self.puzzle_store())
        return updated_checked

    # New elements in the priority queue
    def valid_element(self, valid_sub):
        return self.element_in_prio(valid_sub, self.puzzle)

    def updated_container_a_star(self):
        new_element = None
        for valid_one in self.valid_sub():
            new_element = self.element_in_prio(valid_one, self.puzzle)
            self.container.put(new_element)
        return self.container

    # A* Search
    def a_star(self):
        self.iterations = 0
        self.container = PriorityQueue()
        self.checked = set()
        self.puzzle = self.initial_puzzle
        self.container.put((-1, self.puzzle))
        start = dt.datetime.now()
        while not self.container.empty():
            if self.iterations > 10000000:
                self.is_found = False
                end = dt.datetime.now()
                result = {'final_puzzle': self.puzzle,
                          "is_found": self.is_found,
                          "iterations": self.iterations,
                          "steps": self.puzzle.steps,
                          "time": end - start,
                          "initial_puzzle": self.initial_puzzle}
                return result

            priority_best = self.container.get()
            self.puzzle = priority_best[1]
            self.checked = self.updated_checked_a_star()
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

            self.container = self.updated_container_a_star()

        self.is_found = False
        end = dt.datetime.now()
        result = {'final_puzzle': self.puzzle,
                  "is_found": self.is_found,
                  "iterations": self.iterations,
                  "steps": self.puzzle.steps,
                  "time": end - start,
                  "initial_puzzle": self.initial_puzzle}
        return result
