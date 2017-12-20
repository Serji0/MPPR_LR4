from random import random, randint

import numpy as np

NODE_COUNT = 20
PATHS_COUNT = 20
PATH_LENGTH = 20
GENERATION_COUNT = 1000


def sort_by_length(path):
    return path.length()


class Path:
    def __init__(self, start, end, nodes, network):
        self.start = start
        self.end = end
        self.nodes = nodes
        self.net = network.get()

    def mutate(self):
        self.nodes[randint(0, PATH_LENGTH - 3)] = randint(1, NODE_COUNT)

    def length(self):
        path = self.get_path()
        length = 0

        for i in range(PATH_LENGTH - 1):
            length += self.net[path[i] - 1, path[i+1] - 1]
        return length

    def get_path(self):
        path = []
        path.append(self.start)
        path += self.nodes
        path.append(self.end)
        return path


class Network:
    def __init__(self):
        self.net = np.array([[random() for j in range(NODE_COUNT)] for i in range(NODE_COUNT)])
        for i in range(NODE_COUNT):
            self.net[i][i] = 0

    def get(self):
        return self.net

    def print(self):
        for row in self.net:
            for column in row:
                print('%.2f ' % column, end='')
            print()


class Generation:
    min_length = np.inf
    min_path = None

    def __init__(self, start, end, network, paths):
        self.mutations = []
        self.cross = []

        self.paths = paths
        self.start = start
        self.end = end
        self.network = network

        min_path = min(paths, key=sort_by_length)
        if min_path.length() < Generation.min_length:
            Generation.min_path = min_path
            Generation.min_length = min_path.length()
        print('Min path:', Generation.min_path.get_path())
        print('Min length:', Generation.min_length)

    def crossover(self, path1, path2):
        template = [randint(0, 1) for i in range(PATH_LENGTH - 2)]
        nodes = []
        for i in range(PATH_LENGTH - 2):
            if template[i]:
                nodes.append(path1.nodes[i])
            else:
                nodes.append(path2.nodes[i])
        return Path(self.start, self.end, nodes, self.network)

    def _next(self):
        descendants = []

        self.paths.sort(key=sort_by_length)
        descendants.append(self.paths.pop(0))

        for i in range(int(np.ceil(PATHS_COUNT / 10))):
            mutation = {}

            path = self.paths[randint(0, PATHS_COUNT - 2)]
            mutation['before'] = path.get_path()
            path.mutate()
            mutation['after'] = path.get_path()

            self.mutations.append(mutation)
            descendants.append(path)

        while len(descendants) < PATHS_COUNT:
            cross = {}

            parent1 = self.paths[randint(0, PATHS_COUNT - 2)]
            cross['parent1'] = parent1.get_path()
            parent2 = self.paths[randint(0, PATHS_COUNT - 2)]
            cross['parent2'] = parent2.get_path()

            path = self.crossover(parent1, parent2)
            cross['child'] = path.get_path()

            self.cross.append(cross)
            descendants.append(path)

        return descendants

    def next(self, out=False):
        new_generation = self._next()
        if out:
            self.print_info()
        return Generation(self.start, self.end, self.network, new_generation)

    def print_info(self):
        print('Mutations:')
        for m in self.mutations:
            print('\tBefore:\t', m['before'], '\n\tAfter:\t', m['after'])
            print()

        print('Crosses:')
        for c in self.cross:
            print('\tFather:\t', c['parent1'], '\n\tMother:\t', c['parent2'], '\n\tChild:\t', c['child'])
            print()


def first_generation(start, end, network):
    paths = []

    for i in range(PATHS_COUNT):
        nodes = []
        for j in range(PATH_LENGTH - 2):
            nodes.append(randint(1, NODE_COUNT))
        paths.append(Path(start, end, nodes, network))

    return paths


def main():
    network = Network()
    print('Network:')
    network.print()
    print()

    start = int(input('Компьютер-отправитель: '))
    end = int(input('Компьютер-получатель: '))

    print('Generation 0:')
    paths = first_generation(start, end, network)
    for path in paths:
        print(path.get_path())
    print()

    generation = Generation(start, end, network, paths)
    for i in range(1, GENERATION_COUNT + 1):
        print('\nGeneration ', i, ':', sep='')
        out = i == 1 or i == GENERATION_COUNT
        generation = generation.next(out=out)


if __name__ == '__main__':
    main()
