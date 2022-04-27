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

def distance_between(coordinate1, coordinate2):
    return math.sqrt((coordinate1[0] - coordinate2[0])**2 + (coordinate1[1] - coordinate2[2])**2)

generate_solution()