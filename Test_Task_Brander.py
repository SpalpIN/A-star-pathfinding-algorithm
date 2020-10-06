from numpy import shape
from re import findall

class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 #cost from start to current Node
        self.h = 0 #heuristic based estimated cost for current Node to end Node
        self.f = 0 #total cost of present node i.e. :  f = g + h
    def __eq__(self, other):
        return self.position == other.position

def return_path(current_node, playing_field):
    path = []
    global direction
    direction = []
    no_rows, no_columns = shape(playing_field)
    # create the initialized result maze with 'point' in every position
    result = [['\u00B7' for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)   
        #adding a chain of direction
        try:
            if  current.parent.position[1] > current.position[1] and current.parent.position[0] == current.position[0]:
                direction.append('R')
            elif  current.parent.position[1] < current.position[1] and current.parent.position[0] == current.position[0]:
                direction.append('L')
            elif  current.parent.position[0] > current.position[0] and current.parent.position[1] == current.position[1]:
                direction.append('U')
            elif  current.parent.position[0] < current.position[0] and current.parent.position[1] == current.position[1]:
                direction.append('D')
            else: pass
        except: direction.append("F")
        current = current.parent

    path = path[::-1] #reversed path to show from start to end path
    global stepts_count
    stepts_count = 0
    #update the path by A-star serch with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = direction[i]
        stepts_count += 1
        #dirct_count = direction[i];
    #print(path)
    #print(direction)
    #print(result)
    return result


def search(playing_field, cost, start, end):

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0
       
    yet_to_visit_list = []  
    visited_list = []     
    yet_to_visit_list.append(start_node)
    outer_iterations = 0

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ]] # go right


    #how many rows and columns 
    no_rows, no_columns = shape(playing_field)
    
    while len(yet_to_visit_list) > 0:
        outer_iterations += 1    

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node,playing_field)

        children = []

        for new_position in move: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            if playing_field[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)


if __name__ == '__main__':

    start = []
    end = []
    playing_field = []

    with open('input.txt') as f:
        rows = int(f.readline())
        cols = int(f.readline())

        for i in findall(r'\d+',  f.readline()):
            start.append(int(i))    
            
        for i in findall(r'\d+',  f.readline()):
            end.append(int(i))

        count_lines = 1

        while True:
            line = f.readline()

            if line != '\n':
                count_lines += 1
                query = []

                for i in findall(r'\d+',  line):
                    query.append(int(i))
                playing_field.append(query)

            if count_lines > rows:
                break      

    #playing_field = [[0, 0, 1, 1, 1, 0, 0, 0, 0],
    #                [0, 1, 0, 0, 0, 0, 0, 0, 0],
    #                [1, 1, 1, 1, 0, 1, 0, 0, 1],
    #                [0, 0, 0, 0, 1, 0, 0, 1, 1],
    #                [1, 0, 1, 0, 0, 0, 0, 0, 0],
    #                [1, 1, 1, 1, 0, 0, 0, 1, 0],
    #                [0, 0, 1, 0, 0, 1, 1, 0, 0],
    #                [0, 0, 0, 0, 0, 1, 0, 0, 0],
    #                [0, 0, 0, 0, 0, 1, 0, 0, 0]]    
    #start = [4, 0]
    #end = [6,0] 

    cost = 1 # cost per movement

    if playing_field[start[0]][start[1]] == 0:
        print('You have to choose a ball as a start position') #exception if user try to take an empty space as a gameball
    elif playing_field[end[0]][end[1]] == 1:
        print('You can not move gameball here, pick an empty space(make sure you count from 0)') #exception if user try to pick not empty space
    else:    
        path = search(playing_field,cost, start, end)       
        
        if path == None:
            print("there is no path")
        else:  
            for i in range(len(path)):
                for j in range(len(path[i])):
                    if playing_field[i][j] == 1 and (i,j) != (start[0], start[1]):
                        path[i][j] = 'O'      
                    print(path[i][j], end=' ')
                print()
            print()
            print('shortest path as a sequence of steps: ', end='')

            for elem in direction:
                print(elem, end =' ')

            print()              
            print('number of steps in the shortest path: {}'.format(stepts_count))