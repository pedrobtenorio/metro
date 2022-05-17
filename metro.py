import numpy as np

class Metro():
    
    def __init__(self, last_station, time, trace, operator, connections):
        self.operator = operator
        self.time = self.travel_time(time)
        self.last_station = last_station
        self.trace = trace
        self.trace.append(self.operator[1])
        self.sons = self.paths()
        self.connections = connections
        self.connections.append(self.operator[4])

    def get_current_station(self):
        return self.operator[1]

    def get_current_time(self):
        return self.time

    def get_trace_value(self):
        return list(self.trace)

    def get_connections_value(self):
        return list(self.connections)

    def paths(self):
        track = Track()
        operators = track.find_neighbor_estations(self.operator[1], self.operator[3], self.last_station)
        return operators

    def travel_time(self, time):
        if self.operator[0] != -1:
            return time + self.operator[2] + Track().track[self.operator[0]][self.operator[1]]
        else: 
            return 0

class Track():

    def __init__(self):
        self.track = [[0]*15]*15
        self.track[1]= 0, 99999, 11, 20, 27, 40, 43, 39, 28, 18, 10, 18, 30, 30, 32
        self.track[2]= 0, 11, 99999, 9, 16, 29, 32, 28, 19, 11, 4, 17, 23, 21, 24
        self.track[3]= 0, 20, 9, 99999, 7, 20, 22, 19, 15, 10, 11, 21, 21, 13, 18
        self.track[4]= 0, 27, 16, 7, 99999, 13, 16, 12, 13, 13, 18, 26, 21, 11, 17
        self.track[5]= 0, 40, 29, 20, 13, 99999, 3, 2, 21, 25, 31, 38, 27, 16, 20
        self.track[6]= 0, 43, 32, 22, 16, 3, 99999, 4, 23, 28, 33, 41, 30, 17, 20
        self.track[7]= 0, 39, 28, 19, 12, 2, 4, 99999, 22, 25, 29, 38, 28, 13, 17
        self.track[8]= 0, 28, 19, 15, 13, 21, 23, 22, 99999, 9, 22, 18, 7, 25, 30
        self.track[9]= 0, 18, 11, 10, 13, 25, 28, 25, 9, 99999, 13, 12, 12, 23, 28
        self.track[10]= 0, 10, 4, 11, 18, 31, 33, 29, 22, 13, 99999, 20, 27, 20, 23
        self.track[11]= 0, 18, 17, 21, 26, 38, 41, 38, 18, 12, 20, 99999, 15, 35, 39
        self.track[12]= 0, 30, 23, 21, 21, 27, 30, 28, 7, 12, 27, 15, 99999, 31, 37
        self.track[13]= 0, 30, 21, 13, 11, 16, 17, 13, 25, 23, 20, 35, 31, 99999, 5
        self.track[14]= 0, 32, 24, 18, 17, 20, 20, 17, 30, 28, 23, 39, 37, 5, 99999
        self.track = self.__generate_track_table(self.track)
        self.Lines = self.__lines()
        
    def __generate_track_table(self,table):
        return np.multiply(table, 2)

    def __lines(self):
        a = [1, 2, 3, 4, 5, 6]
        b = [11, 9, 3, 13]
        c = [12, 8, 4, 13, 14]
        d = [7, 5, 8, 9, 2, 10]
        lines = [a, b, c, d]
        return lines

    def find_neighbor_estations(self, estation, line, last_estation):
        neighbors = []
        for i in range(4):
            k = 0
            for j in self.Lines[i]:
                if j == estation:
                    if line != i:
                        extra_time = 4
                        conection = (estation, line, i)
                    else:
                        conection = -1
                        extra_time = 0
                    if k+1 < len(self.Lines[i]):
                        neighbors.append((self.Lines[i][k+1], extra_time, i, conection))
                    if k-1 >= 0:
                        neighbors.append((self.Lines[i][k-1], extra_time, i, conection))
                k += 1
        operators = []
        for i in neighbors:
            if last_estation != i[0] or len(neighbors) == 1:
                operators.append((estation, i[0], i[1], i[2], i[3]))
        return operators

class Passenger():

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.border = self.initial_border()

    def initial_border(self):
        lines = []
        border = []
        for i in range(4):
            for j in Track().Lines[i]:
                if j == self.start:
                    lines.append(i)
        for i in lines:
            border.append(Metro(-1, 0, [], (-1, self.start, 0, i, -1), []))

        return border

    def route(self):
        while len(self.border)!=0:
            metro = self.find_min()
            if metro.operator[1] == self.end:
                    return (metro.trace, metro.time, self.metro_connections(metro.connections))
            for i in metro.sons:
                new_son = Metro(metro.get_current_station(), metro.get_current_time(), metro.get_trace_value(), i, metro.get_connections_value())
                self.border.append(new_son)
            self.border.remove(metro)

    def find_min(self):
        min = (self.border[0]).get_current_time()
        index = 0
        for i in range(len(self.border)):
            if self.border[i].get_current_time() < min:
                min = self.border[i].get_current_time()
                index = i
        return self.border[index]

    def metro_connections(self, connections_list):
        connections = []
        for i in connections_list:
            if i != -1:
                connections.append(i)
        
        return connections

    def lines(self, line):
        names = ["A", "B", "C", "D"]
        return names[line]


def main():
    #initial station and destination show be from 1 to 14
    start = int(input(f"Enter the initial station: (1 to 14)"))
    end = int(input(f"enter the destination: (1 to 14)"))
    passanger = Passenger(start, end)
    path = passanger.route()
    print("\n----------------Processing-----------------------------\n")
    
    print(f"the shortest path is: {path[0]} and  will take {path[1]} minutes")
    for i in path[2]:
        print(f"change on station {i[0]} from line {passanger.lines(i[1])} to line {passanger.lines(i[2])}.")

    print("\n----------------------------------------------------------------------------------------------------\n")

main()