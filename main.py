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
                branch_offices_lines = lines[3:3+n]
                coordinates_lines = lines[6+n:6+2*n]
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

def generate_solution():
    parse_file()
    init = ("1", branch_offices["1"])
    branch_offices.pop("1")
    result = ["1"]
    total = data["capacity"]

    offices = list(branch_offices.items())
    end = False
    candidate = init

    while(not end):
        candidate, offices = find_the_closest(candidate, offices, total)
        total += candidate[1]
        result.append(candidate[0])
        if(len(offices) == 1):
            candidate = offices[0]
            total += candidate[1]
            result.append(candidate[0])
            end = True

    save_result(result)
    #offices = sorted(offices, key=lambda x: x[1], reverse=True)

def save_result(list):
    file = open("result.txt", "w")
    for x in list:
        file.write("{} ".format(x))
    file.close()

def find_the_closest(office, offices, total):
    distances = []
    for element in offices:
        distances.append((element[0], element[1], distance_between(coordinates[office[0]], coordinates[element[0]])))

    distances = sorted(distances, key=lambda x: x[2], reverse=True)
    for element in distances:
        if(element[2] != 0 and total+element[1] >= 0 and total+element[1] <= data["capacity"]):
            offices.remove((element[0], element[1]))
            return element, offices


def distance_between(coordinate1, coordinate2):
    return math.sqrt((coordinate1[0] - coordinate2[0])**2 + (coordinate1[1] - coordinate2[1])**2)


generate_solution()