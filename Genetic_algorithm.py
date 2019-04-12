import Virtual_machine as virtual
import random, json
from copy import deepcopy

CROSSRATE = 0.7
MUTATERATE = 0.07


def crossover(mom, dad):
    pivot1 = random.randrange(0, 31)
    pivot2 = random.randrange(32, 63)

    child1 = {"fitness": 0,
              "gene": []}
    child1["gene"].extend(dad["gene"][0:pivot1])
    child1["gene"].extend(mom["gene"][pivot1:pivot2])
    child1["gene"].extend(mom["gene"][pivot2:64])

    child2 = {"fitness": 0,
              "gene": []}
    child2["gene"].extend(mom["gene"][0:pivot1])
    child2["gene"].extend(dad["gene"][pivot1:pivot2])
    child2["gene"].extend(dad["gene"][pivot2:64])

    return child1, child2


def roulette(fitness_sum, subjects):
    pick_line = random.uniform(0, fitness_sum)
    current = 0

    for subject in subjects:
        current += subject["fitness"]
        if current >= pick_line:
            return deepcopy(subject)


def reverse_bit(num):
    result = 0
    while num:
        result = (result << 1) + (num & 1)
        num >>= 1
    return result


def mutate_1(child):
    for i in range(0, 30):
        r1 = random.randrange(0, 63)
        r2 = random.randrange(0, 63)
        child["gene"][r1], child["gene"][r2] = child["gene"][r2], child["gene"][r1]

    return child


def mutate_2(child):
    for i in range(0, 30):
        r1 = random.randrange(0, 63)
        child["gene"][r1] = random.randrange(0, 254)

    return child


def find_solution(subjects, maze, generations, individuals):
    iteration = 0
    while iteration < int(generations):
        print("Generation", iteration)

        for subject in subjects:
            virtual.run_generator(subject, maze)

            #    print(subjects)

            #    for sub in subjects:
            #        print(sub)

        fitness_sum = 0
        fit_sort = {}

        for subject in subjects:
            fitness_sum += subject["fitness"]
            fit_sort[subjects.index(subject)] = subject["fitness"]

        sorted_d = sorted(fit_sort.items(), key=lambda kv: kv[1], reverse=True)

        new_population = []

        # elitarism
        elitarism = True
        print("Best fitness this generation: ", sorted_d[0][1])
        if elitarism == True:
            for item_index in sorted_d:
                sbj = deepcopy(subjects[item_index[0]])
                new_population.append(sbj)

                if len(new_population) == 2:
                    break

        while len(new_population) < int(individuals):

            mom = roulette(fitness_sum, subjects)
            dad = roulette(fitness_sum, subjects)
            if mom == dad:
                continue

            if random.random() < CROSSRATE:
                c1, c2 = crossover(mom, dad)
            else:
                c1 = deepcopy(mom)
                c2 = deepcopy(dad)

            if random.random() < MUTATERATE:
                c1 = mutate_1(c1)
                c2 = mutate_2(c2)

            new_population.append(c1)
            new_population.append(c2)

        subjects.clear()
        subjects = deepcopy(new_population)

        iteration += 1

    return subjects


subjects = []

start_flag = True

generations = input("Number of generations?: ")
individuals = input("Number of invididuals per generation?: ")
# initialize subjects with random values
for j in range(0, int(individuals)):
    subjects.append({"fitness": 0,
                     "gene": []})
    for i in range(0, 64):
        if i < 20:
            subjects[j]["gene"].append(random.randrange(0, 255))
        else:
            subjects[j]["gene"].append(0)

with open("maze.json") as in_fl:
    maze = json.load(in_fl)

while True:
    if start_flag is True:
        subjects = find_solution(subjects, maze, generations, individuals)
        start_flag = False
    else:
        repeat = input("Algorithm haven't found solution, do you want o retry?(yes/no): ")
        if repeat == "yes":
            new_subjects = input("Generate new subjects, or continue?(yes/no): ")
            if new_subjects == "yes":
                subjects.clear()
                for j in range(0, 30):
                    subjects.append({"fitness": 0,
                                     "gene": []})
                    for i in range(0, 64):
                        if i < 20:
                            subjects[j]["gene"].append(random.randrange(0, 255))
                        else:
                            subjects[j]["gene"].append(0)
                subjects = find_solution(subjects, maze, generations, individuals)
            else:
                subjects = find_solution(subjects, maze, generations, individuals)
        elif repeat == "no":
            break
        else:
            print("You failed")
            exit(1)
