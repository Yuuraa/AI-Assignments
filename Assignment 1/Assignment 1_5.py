import sys
import numpy

'''
Implement a performance-measuring environment simulator 
for the vacuum-cleaner world.

This world can be described as follows: 
Percepts: Each vacuum-cleaner agent gets a 
three-element percent vector on each turn.

The first element, a touch sensor, 
should be a 1 if the machine has bumped into something 
and a 0 otherwise. 

The second comes from a photo sensor under the machine, 
which emits a 1 if there is dirt there and 0 otherwise

The third comes from an infrared sensor,
which emits a 1 when the agent is in home location,
and a 0 otherwise.
'''


'''
My trial: 
def checkDirty():

def takeAction():


def main():



if __name__ == '__main__':
    main()
'''

'''
다른 사람 코드
from environments import VacuumEnvironment
from Agents import RandomAgent, ReflexAgent, InternalAgent

ENV_SIZE = (12, 12)
DIRT_CHANCE = 0.05


def main():
    env = VacuumEnvironment(ENV_SIZE, DIRT_CHANCE)
    agent = InternalAgent()

    print (env.room[0])
    print (env.room[1])

    observation = env.state()
    reward = 0
    done = False
    action = agent.act(observation, reward)
    turn = 1

    while not done:

        observation, reward, done = env.step(action[0])
        print ("Step {0}: Action - {1}".format(turn, action[1]))

        action = agent.act(observation, reward)
        # print "Reward {0}   Total Reward {1}".format(reward, agent.reward)
        turn += 1

    print (env.room[0])

if __name__ == "__main__":
    main()
Include this as your environments.py file

import numpy as np


class VacuumEnvironment(object):
    def __init__(self, size, dirt):
        self.size = size
        self.dirt = dirt

        self.agent_x = np.random.randint(self.size[0])
        self.agent_y = np.random.randint(self.size[1])
        self.agent_facing = np.random.randint(4)    # 0-up, 1-right, 2-down, 3-left

        # Layer 0: dirt, layer 1: objects/home
        self.room = np.zeros((2, self.size[0], self.size[1]))

        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if np.random.uniform() < self.dirt:
                    self.room[0][row][col] = 1

        # Set home base
        home_x = np.random.randint(self.size[0])
        home_y = np.random.randint(self.size[1])
        self.room[1][home_x][home_y] = 1

    def state(self, obstacle=False):
        return {"obstacle": int(obstacle),
                "dirt": self.room[0][self.agent_x][self.agent_y],
                "home": self.room[1][self.agent_x][self.agent_y],
                "agent": (self.agent_x, self.agent_y)}

    def has_hit_obstacle(self):
        if (self.agent_facing == 0 and self.agent_x == 0) or \
           (self.agent_facing == 1 and self.agent_y == self.size[1] - 1) or \
           (self.agent_facing == 2 and self.agent_x == self.size[0] - 1) or \
           (self.agent_facing == 3 and self.agent_y == 0):
            return True

        return False

    def move_forward(self):
        """
        Updates agents position
        :return: Whether agent hit obstacle
        """
        if self.has_hit_obstacle():
            return True

        if self.agent_facing == 0:
            self.agent_x -= 1

        elif self.agent_facing == 1:
            self.agent_y += 1

        elif self.agent_facing == 2:
            self.agent_x += 1

        elif self.agent_facing == 3:
            self.agent_y -= 1

        return False

    def step(self, action):
        obstacle = False
        reward = -1  # Default -1 for each action taken
        done = False

        if action == 0:
            obstacle = self.move_forward()

        elif action == 1:
            self.agent_facing = (self.agent_facing + 1) % 4

        elif action == 2:
            self.agent_facing = (self.agent_facing - 1) % 4

        elif action == 3:
            # Reward of +100 for sucking up dirt
            if self.room[0][self.agent_x][self.agent_y] == 1:
                reward += 100
                self.room[0][self.agent_x][self.agent_y] = 0

        elif action == 4:
            # If not on home base when switching off give reward of -1000
            if self.room[1][self.agent_x][self.agent_y] != 1:
                reward -= 1000

            done = True

        return self.state(obstacle), reward, done
Include this as your Agents.py file

import numpy as np

ACTIONS = ((0, "Go Forward"),
           (1, "Turn Right"),
           (2, "Turn Left"),
           (3, "Suck Dirt"),
           (4, "Turn Off"),
           (-1, "Break"),)


class RandomAgent(object):
    def __init__(self):
        self.reward = 0

    def act(self, observation, reward):
        self.reward += reward

        action = ACTIONS[np.random.randint(len(ACTIONS))]
        return action


class ReflexAgent(object):
    def __init__(self):
        self.reward = 0

    def act(self, observation, reward):
        self.reward += reward

        # If dirt then suck
        if observation['dirt'] == 1:
            return ACTIONS[3]

        # If obstacle then turn
        if observation['obstacle'] == 1:
            return ACTIONS[1]

        # Else randomly choose from first 3 actions (stops infinite loop circling edge)
        return ACTIONS[np.random.randint(3)]


class InternalAgent(object):
    def __init__(self):
        self.reward = 0
        self.map = [[-1, -1], [-1, -1]]  # 0-Empty, 1-Dirt, 2-Obstacle, 3-Home

        # Agent's relative position to map and direction
        self.x = 0
        self.y = 0
        self.facing = 0  # -1-Unknown, 0-Up, 1-Right, 2-Down, 3-Left

    def add_map(self):

        side = self.is_on_edge()

        while side >= 0:
            if side == 0:  # Top
                self.map.insert(0, [-1] * len(self.map[0]))
                self.x += 1

            elif side == 1:  # Right
                for row in self.map:
                    row.append(-1)

            elif side == 2:  # Down
                self.map.append([-1] * len(self.map[0]))

            elif side == 3:  # Left
                for row in self.map:
                    row.insert(0, -1)
                self.y += 1

            side = self.is_on_edge()

    def is_on_edge(self):
        if self.x == 0:
            return 0

        elif self.y == len(self.map[0]) - 1:
            return 1

        elif self.x == len(self.map) - 1:
            return 2

        elif self.y == 0:
            return 3

        return -1

    def move_forward(self):
        if self.facing == 0:
            self.x -= 1

        elif self.facing == 1:
            self.y += 1

        elif self.facing == 2:
            self.x += 1

        elif self.facing == 3:
            self.y -= 1

    # If obstacle in position then move back to previous square
    def move_backwards(self):
        if self.facing == 0:
            self.x += 1

        elif self.facing == 1:
            self.y -= 1

        elif self.facing == 2:
            self.x -= 1

        elif self.facing == 3:
            self.y += 1

    def update_map(self, observation):
        if observation['dirt'] == 1:
            self.map[self.x][self.y] = 1

        elif observation['home'] == 1:
            self.map[self.x][self.y] = 3

        else:
            self.map[self.x][self.y] = 0

        if observation['obstacle'] == 1:
            self.map[self.x][self.y] = 2
            self.move_backwards()

        # Fill in borders
        x_len = len(self.map) - 1
        y_len = len(self.map[0]) - 1

        if self.map[0][1] == 2 and self.map[1][0] == 2:
            self.map[0][0] = 2

        if self.map[0][y_len - 1] == 2 and self.map[1][y_len] == 2:
            self.map[0][y_len] = 2

        if self.map[x_len - 1][0] == 2 and self.map[x_len][1] == 2:
            self.map[x_len][0] = 2

        if self.map[x_len][y_len - 1] == 2 and self.map[x_len - 1][y_len] == 2:
            self.map[x_len][y_len] = 2

    # Determine next action needed to move towards next_square from current position
    def next_step(self, next_square):
        if next_square[0] < self.x and self.facing != 0 and self.map[self.x - 1][self.y] != 2:
            action = ACTIONS[2]

        elif next_square[0] < self.x and self.facing == 0 and self.map[self.x - 1][self.y] != 2:
            action = ACTIONS[0]

        elif next_square[0] > self.x and self.facing != 2 and self.map[self.x + 1][self.y] != 2:
            action = ACTIONS[2]

        elif next_square[0] > self.x and self.facing == 2 and self.map[self.x + 1][self.y] != 2:
            action = ACTIONS[0]

        elif next_square[1] > self.y and self.facing != 1 and self.map[self.x][self.y + 1] != 2:
            action = ACTIONS[2]

        elif next_square[1] > self.y and self.facing == 1 and self.map[self.x][self.y + 1] != 2:
            action = ACTIONS[0]

        elif next_square[1] < self.y and self.facing != 3 and self.map[self.x][self.y - 1] != 2:
            action = ACTIONS[2]

        elif next_square[1] < self.y and self.facing == 3 and self.map[self.x][self.y - 1] != 2:
            action = ACTIONS[0]

        else:
            action = ACTIONS[4]

        # If moving forward check if map needs to be expanded
        if action[0] == 0:
            self.move_forward()

        if action[0] == 2:
            self.facing = (self.facing - 1) % 4

        return action

    def find_nearest(self, square_type):
        # Else move towards nearest unknown
        min_dist = None
        next_square = None

        for i, row in enumerate(self.map):
            for j, square in enumerate(row):
                if square == square_type:
                    dist = (self.x - i) ** 2 + (self.y - j) ** 2
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        next_square = (i, j)

        return next_square

    def choose_action(self):
        # If on a patch of dirt then suck it up
        if self.map[self.x][self.y] == 1:
            return ACTIONS[3]

        next_square = self.find_nearest(-1)

        # If no more unknowns then head home
        if next_square is None:
            next_square = self.find_nearest(3)

        return self.next_step(next_square)

    def act(self, observation, reward):
        self.reward += reward

        self.update_map(observation)
        self.add_map()

        # Choose action (based on map)
        return self.choose_action()
'''