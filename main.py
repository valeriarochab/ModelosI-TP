import math
import os

data = {}

branch_offices = {}
coordinates = {}

def parse_file():
    branch_offices_lines = []
    coordinates_lines = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("{}/problema_uno.txt".format(current_path)) as fp:
        lines = [line for line in fp]

        for line in lines:
            elements = line.split()
            if elements[0] == 'CAPACIDAD:':
                data["capacity"] = int(elements[1])
            elif elements[0] == 'DIMENSION:':
                data["dimension"] = int(elements[1])
            elif elements[0] == 'DEMANDAS':
                n = data["dimension"]
                branch_offices_lines = lines[3:3 + n]
                coordinates_lines = lines[6 + n:6 + 2 * n]
                break

    parse_branch_offices(branch_offices_lines)
    parse_coordinates(coordinates_lines)


def parse_branch_offices(branch_offices_lines):
    for office in branch_offices_lines:
        elements = office.split()
        branch_offices[elements[0]] = int(elements[1])


def parse_coordinates(coordinates_lines):
    for coordinate in coordinates_lines:
        elements = coordinate.split()
        coordinates[elements[0]] = (float(elements[1]), float(elements[2].split("\n")[0]))


def main():
    parse_file()
    best_result, best_cost = generate_multiple_solutions()
    print("Total cost: ", best_cost)
    save_result(best_result)


def generate_multiple_solutions():
    best_result, best_cost, last_candidate = process_offices("1")
    best_cost += distance_between(coordinates[last_candidate[0]], coordinates["1"])

    for i in range(2, data["dimension"] + 1):
        if branch_offices[str(i)] > 0:
            result, cost, last_candidate = process_offices(str(i))
            cost += distance_between(coordinates[last_candidate[0]], coordinates[str(i)])
            if cost < best_cost:
                best_result = result
                best_cost = cost
    return best_result, best_cost


def process_offices(n):
    result, last_candidate = custom_algorithm(n)
    cost = sum(k for i, j, k in result)
    return result, cost, last_candidate


def custom_algorithm(n):
    init = (n, branch_offices[n], 0)
    aux_branch_offices = branch_offices.copy()
    aux_branch_offices.pop(n)
    candidate = init
    result = [candidate]
    total = candidate[1]

    offices = list(aux_branch_offices.items())
    end = False

    while not end:
        candidate, offices = find_the_closest(candidate, offices, total)
        total += candidate[1]
        result.append(candidate)
        if len(offices) == 1:
            last_candidate = candidate
            candidate = offices[0]
            total += candidate[1]
            result.append((candidate[0], candidate[1],
                           distance_between(coordinates[last_candidate[0]], coordinates[candidate[0]])))
            end = True
    return result, candidate


def save_result(list):
    file = open("result.txt", "w")
    for x in list:
        file.write("{} ".format(x[0]))
    file.close()


def find_the_closest(office, offices, total):
    distances = []
    for element in offices:
        distances.append((element[0], element[1], distance_between(coordinates[office[0]], coordinates[element[0]])))

    distances = sorted(distances, key=lambda x: x[2])
    for element in distances:
        if (element[2] != 0 and total + element[1] >= 0 and total + element[1] <= data["capacity"]):
            offices.remove((element[0], element[1]))
            return element, offices


def distance_between(coordinate1, coordinate2):
    return math.sqrt((coordinate1[0] - coordinate2[0]) ** 2 + (coordinate1[1] - coordinate2[1]) ** 2)


### Other algorithm ###
def generate_best_solution():
    best_result, best_cost, last_candidate = get_solution("1")
    best_cost += distance_between(coordinates[last_candidate[0]], coordinates["1"])

    for i in range(2, data["dimension"] + 1):
        if branch_offices[str(i)] > 0:
            result, cost, last_candidate = process_offices(str(i))
            cost += distance_between(coordinates[last_candidate[0]], coordinates[str(i)])
            if cost < best_cost:
                best_result = result
                best_cost = cost
    return best_result, best_cost


def get_solution(n):
    aux_branch_offices = branch_offices.copy()
    offices = list(aux_branch_offices.items())
    first = (str(n), branch_offices[str(n)], 0, 0)
    total = first[1]
    second, offices = find_the_closest(first, offices, total)
    result = [first, (second[0], second[1], 0, second[2])]

    end = False
    while not end:
        first = second
        second, offices = find_next(first, second, offices, total)

        total += second[1]
        result.append(second)
        if len(offices) == 1:
            last_candidate = second
            candidate = offices[0]
            total += second[1]
            result.append((candidate[0], candidate[1], 0,
                           distance_between(coordinates[last_candidate[0]], coordinates[candidate[0]])))
            end = True

    cost = sum(l for i, j, k, l in result)
    return result, cost, last_candidate


def find_next(first, second, offices, total):
    distances = []
    for element in offices:
        distances.append((element[0], element[1], distance_between(coordinates[first[0]], coordinates[element[0]]) +
                          distance_between(coordinates[second[0]], coordinates[element[0]]),
                          distance_between(coordinates[second[0]], coordinates[element[0]])))

    distances = sorted(distances, key=lambda x: x[2])
    for element in distances:
        if element[3] != 0 and 0 <= total + element[1] <= data["capacity"]:
            offices.remove((element[0], element[1]))
            return element, offices

####### Entrega 2 ########
def main2():
    parse_file()
    calculate_distances()
    #best_result, best_cost = generate_multiple_solutions2()
    #print("Total cost: ", best_cost)
    #save_result(best_result)


def calculate_distances():
    best_cost = 100000
    best_result = []
    for i in range(0, data["dimension"]):
        if branch_offices[str(i+1)] > 0:
            offices_visited = []
            aux_branch_offices = branch_offices.copy()
            offices = list(aux_branch_offices.items())
            initial_office = offices[i]
            money = initial_office[1]
            total_cost = money
            offices.remove(initial_office)
            offices_visited.append(initial_office[0])
            next_office, money, total_cost = select_next_office(initial_office, money, total_cost, offices, offices_visited)

            while offices:
                next_office, money, total_cost = select_next_office(next_office, money, total_cost, offices, offices_visited)

            total_cost += distance_between(coordinates[initial_office[0]], coordinates[next_office[0]])

            if total_cost < best_cost:
                best_result = offices_visited.copy()
                best_cost = total_cost

    print("Total cost: ", best_cost)
    print("best result", len(best_result))


def select_next_office(initial_office, money, total_cost, offices, offices_visited):
    distances = []
    for office in offices:
        if 0 <= money + office[1] <= data["capacity"]:
            distances.append((office[0], distance_between(coordinates[initial_office[0]], coordinates[office[0]])))

    distances = sorted(distances, key=lambda x: x[1])
    candidate = distances[0]
    total_cost += candidate[1]
    next_office = (candidate[0], branch_offices[candidate[0]])
    money += next_office[1]
    offices.remove(next_office)
    offices_visited.append(next_office[0])
    return next_office, money, total_cost


main2()
