# You Li, Zijing Zhao

from numpy import random, mean

params = {'world_size':(20,20),
          'num_agents':380,
          'same_pref' :0.4,
          'max_iter'  :100,
          'out_path'  :r'/Users/crystal/Documents/GitHub/simple_abm/abm_results.csv' }

class Agent():
    def __init__(self, world, kind, same_pref):
        self.world = world
        self.kind = kind
        self.same_pref = same_pref
        self.location = None

    def move(self):
        if not self.am_i_happy():
            vacancies = self.world.find_vacant()
            for patch in vacancies:
                if self.am_i_happy(loc=patch):
                    self.world.grid[self.location] = None
                    self.location = patch
                    self.world.grid[patch] = self
                    return 1
            return 2
        return 0

    def am_i_happy(self, loc=None):
        if loc is None:
            loc = self.location
        neighbors = self.world.get_neighbors(loc)
        neighbor_agents = [self.world.grid[n] for n in neighbors if self.world.grid[n] is not None]
        num_like_me = sum(agent.kind == self.kind for agent in neighbor_agents)
        if len(neighbor_agents) == 0:
            return False
        perc_like_me = num_like_me / len(neighbor_agents)
        return perc_like_me >= self.same_pref

class World:
    def __init__(self, params):
        assert params['world_size'][0] * params['world_size'][1] > params['num_agents'], 'Grid too small for number of agents.'
        self.params = params
        self.grid = self.build_grid(params['world_size'])
        self.agents = self.build_agents(params['num_agents'], params['same_pref'])
        self.init_world()

    def build_grid(self, world_size):
        return {(i, j): None for i in range(world_size[0]) for j in range(world_size[1])}

    def build_agents(self, num_agents, same_pref):
        agents = [Agent(self, 'red' if i < num_agents // 2 else 'blue', same_pref) for i in range(num_agents)]
        random.shuffle(agents)
        return agents

    def init_world(self):
        for agent in self.agents:
            loc = self.find_vacant()[0]
            self.grid[loc] = agent
            agent.location = loc

    def find_vacant(self):
        return [loc for loc, occupant in self.grid.items() if occupant is None]

    def get_neighbors(self, loc):
        x, y = loc
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1),
                     (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        x_max, y_max = self.params['world_size']
        x_max -= 1
        y_max -= 1
        def edge_fixer(x, y):
            if x < 0:
                x = x_max
            elif x > x_max:
                x = 0
            if y < 0:
                y = y_max
            elif y > y_max:
                y = 0
            return x, y
        return [edge_fixer(nx, ny) for nx, ny in neighbors]

    def run(self):
        for iteration in range(self.params['max_iter']):
            random.shuffle(self.agents)
            move_results = [agent.move() for agent in self.agents]

            num_happy = move_results.count(0)
            num_moved = move_results.count(1)
            num_unhappy = move_results.count(2)

            print(f"Iteration {iteration}: Happy={num_happy}, Moved={num_moved}, Unhappy={num_unhappy}")

            if num_moved == 0 and num_unhappy == 0:
                print(f'Everyone is happy! Stopping after iteration {iteration}.')
                break
            elif num_moved == 0 and num_unhappy > 0:
                print(f'Some agents are unhappy, but they cannot find anywhere to move to. Stopping after iteration {iteration}.')
                break

world = World(params)
world.run()