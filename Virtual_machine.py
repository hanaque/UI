from copy import deepcopy

def run_generator(subject, maze):
    result_steps = []
    memory = deepcopy(subject["gene"])
    subject["fitness"] = 0
    found_tresures = []

    x_axis = maze["startX"]
    y_axis = maze["startY"]

    path = []

    iterations = 0
    state = 0
    while iterations < 500:
        if state > 63:
            state = 0

        temp = deepcopy(memory[state])

        temp >>= 6

        if temp == 0:
            tmp = int(memory[state] & 0b111111)
            if memory[tmp] == 255:
                memory[tmp] = 0
            else:
                memory[tmp] += 1
        elif temp == 1:
            tmp = int(memory[state] & 0b111111)
            if memory[tmp] == 0:
                memory[tmp] = 255
            else:
                memory[tmp] -= 1
        elif temp == 2:
            state = int(memory[state] & 0b111111)
        else:
            bitlist = [int(x) for x in bin(memory[state])[2:]]

            num_of_pos_bits = 0
            for i in range(0,8):
                if bitlist[i] == 1:
                    num_of_pos_bits += 1

            if num_of_pos_bits == 2:
                step = "H"
            elif num_of_pos_bits == 3 or num_of_pos_bits == 5:
                step = "D"
            elif num_of_pos_bits == 6 or num_of_pos_bits == 4:
                step = "L"
            else:
                step = "P"

            """here"""
            path.append(step)
            if step == 'H':
                x_axis -= 1
            elif step == 'D':
                x_axis += 1
            elif step == 'L':
                y_axis -= 1
            elif step == 'P':
                y_axis += 1

            if x_axis == 0 or x_axis == (maze["X"] + 1) or y_axis == 0 or y_axis == (maze["Y"] + 1):
                return subject

            location = {
                "X": x_axis,
                "Y": y_axis
            }

            if location in maze["tresure"] and location not in found_tresures:
                subject["fitness"] += 1
                found_tresures.append(location)
                # if all tresures were found exit with success
                if len(found_tresures) == len(maze["tresure"]):
                    print("Algorithm found solution: ", path)
                    exit(0)

        state += 1
        iterations += 1

    addition_to_fitness = 1 - (len(path) / 1000)
    subject["fitness"] += addition_to_fitness

#    print(path)

    if len(path) == 0:
        subject["fitness"] = 0

    return 0

