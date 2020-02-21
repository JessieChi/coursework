import hashlib
from functools import total_ordering
from Tool import *
import numpy as np

@total_ordering
class Puzzle:
    def __init__(self, array, goal_state=None, steps=0, parent_puzzle=None, parent_action=None):
        self.array = np.array(array, dtype=np.int)
        self.goal_state = goal_state
        self.parent_puzzle = parent_puzzle
        self.parent_action = parent_action
        self.steps = steps

    def __eq__(self, other):
        return self.steps == other.steps

    def __lt__(self, other):
        return self.steps > other.steps

    @property
    def get_agent(self):
        return 0

    def agent_x(self):
        agent_position = self.agent_position
        agent_x = agent_position().get_x()
        return agent_x

    def agent_y(self):
        agent_position = self.agent_position
        agent_y = agent_position().get_y()
        return agent_y

    @property
    def get_height(self):
        return self.array.shape[0]

    @property
    def get_width(self):
        return self.array.shape[1]

    # All directions in str:tuples.
    @property
    def direction_to_tuple(self):
        all_directions = {'left': (0, 1), 'up': (1, 0), 'right': (0, -1), 'down': (-1, 0)}
        return all_directions

    # All directions in tuples:str.
    @property
    def tuple_to_direction(self):
        all_tuple = {(0, 1): "left", (1, 0): "up", (0, -1): "right", (-1, 0): "down"}
        return all_tuple

    # Determine if _dict is a valid position.
    def is_valid(self, _dict):
        if 0 <= _dict.get_x() < self.get_width:
            if 0 <= _dict.get_y() < self.get_height:
                return True
        return False

    # The location of any block
    def one_block_position(self, block):
        position = Position(None, None)
        for i in range(self.get_height):
            for j in range(self.get_width):
                if block == self.array[i][j]:
                    position = Position(i, j)
        return position

    def agent_position(self):
        position = Position(None, None)
        for i in range(self.get_height):
            for j in range(self.get_width):
                if self.array[i][j] == 0:
                    position = Position(i, j)
        return position

    # Get all the blocks.
    def get_all_blocks_list(self):
        blocks = []
        for i in range(self.get_height):
            for j in range(self.get_width):
                blocks.append(self.array[i][j])
        return blocks

    # Get all the target blocks
    def get_goal_blocks_list(self):
        goal_blocks_position = []
        for block in self.get_all_blocks_list():
            block_position = self.one_block_position(block)
            if block != 0 and block != 1 and block != -1:
                goal_blocks_position.append(block_position)
        return goal_blocks_position

    def single_manhattan_distance(self, vector1, vector2):
        single_distance = sum(map(lambda i, j: abs(i - j), vector1, vector2))
        return single_distance

    # Manhattan distance from current state to target state
    def manhattan_distance(self):
        goal_blocks_position = self.get_goal_blocks_list
        sum = 0
        blocks = self.get_all_blocks_list()

        for block in blocks:
            if block != 0 and block != 1 and block != -1:
                goal_blocks_position = self.one_block_position(block)
                vector1 = self.get_one_goal_position(block)
                vector2 = (goal_blocks_position.get_x(), goal_blocks_position.get_y())
                sum += self.single_manhattan_distance(vector1, vector2)
        return sum

    # To facilitate storage and comparison, convert the puzzle to a hash value.
    def puzzle_store_format(self):
        md = hashlib.md5()
        md.update(self.array)
        result = md.digest()
        return result

    # Gets the location of the specified target block.
    def get_one_goal_position(self, block):
        for i in range(self.get_height):
            for j in range(self.get_width):
                if self.goal_state[i][j] == block:
                    position = (i, j)
                    return position

    # After the agent moves once, the position of certain block
    def new_block_position(self, agent_position, direction):
        return Position(agent_position.get_x() + direction[0], agent_position.get_y() + direction[1])

    # Determine if certain location is a barricade.
    def is_not_barricade(self, block_position):
        if self.array[block_position.get_x()][block_position.get_y()] != -1:
            return True
        return False

    # All directions in tuples.
    def all_directions_move(self):
        return np.array([(1, 0), (0, -1), (-1, 0), (0, 1)])

    # Valid sub node for current node.
    def valid_new_blocks_position(self):
        valid_new_blocks_position = []
        for possible_dir in self.all_directions_move():
            new_block_position = self.new_block_position(self.agent_position(), possible_dir)
            if self.is_valid(new_block_position) and self.is_not_barricade(new_block_position):
                valid_new_blocks_position.append(new_block_position)
        return valid_new_blocks_position

    # move the sub node to a set for random selection
    def valid_sub_puzzle(self):
        # direction_position = []
        direction_position = set()

        for valid_new_block_position in self.valid_new_blocks_position():
            # direction_position.append(valid_new_block_position)
            direction_position.add(valid_new_block_position)
        return direction_position

    # Get the new puzzle, give the direction of movement
    def move_to_puzzle(self, move):
        puzzle = self.new_puzzle(move)
        return puzzle

    # all sub node for current node
    def next_generation(self):
        valid_action = self.valid_sub_puzzle()
        next_generation = []
        for action in valid_action:
            next_generation.append(self.move_to_puzzle(action))
        return next_generation

    # Gets the block at the specified location
    def position_to_block(self, position):
        block = self.array[position.get_x()][position.get_y()]
        return block

    # New puzzle after the agent moves once
    def new_puzzle(self, goal_position):
        new_blocks = np.copy(self.array)
        new_blocks[self.agent_x()][self.agent_y()] = self.position_to_block(goal_position)
        new_blocks[goal_position.get_x()][goal_position.get_y()] = self.get_agent
        new_steps = self.steps + 1
        direction_guide = (self.agent_x() - goal_position.get_x(), self.agent_y() - goal_position.get_y())
        direction = self.tuple_to_direction[direction_guide]
        new_parent_puzzle = self
        new_parent_action = direction

        return Puzzle(new_blocks, self.goal_state, new_steps, new_parent_puzzle, new_parent_action)