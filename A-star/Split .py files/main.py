"""
MAIN
accompaniying python files are Astar (class), Visualisation (class), and netlist_sort (def)

TODO
in main:
    profiler implementeren per 'line n solved, of length x' (bij 'vastlopen')

in Astar:    
    volgorde x-, y-, z-bewegingen vastleggen (ligt aan PriorityQueue A-star)
    verhouding cost children en grandchildren van gates (+ optimalisatie)
    cost af laten hangen van gatefrequentie (+ optimalisatie)
    hoogtecost verlagen?

aandacht:    
    Create children in positie te zetten (gedaan?)
    dynamic en static cost (nog meer?)
    hou de cost van het pad bij ipv de lengte (is dit nu het geval?)
"""
import Astar
import Visualisation
import netlist_sort
import numpy as np

# indicate start
print 'running...'

# load board data
print_file = '../testprint.csv'
#print_index = int(print_file[5])
netlist_file = '../testnetlist.csv'

width = 3
height = 2
"""
# board dimensions
width = 17
if print_index == 1:
    height = 12
elif print_index == 2:
    height = 16
"""
# initialize gates, netlist and grid
gates = Astar.create_print(print_file)
netlist = Astar.create_netlist(netlist_file)
grid = Astar.Grid(gates, width, height)

# lower boundary (ondergrens) for netlist
min_dist = 0
for elem in netlist:
    min_dist += gates[elem[0]].getDist(gates[elem[1]])

# sort netlist
sorted_netlist = netlist_sort.totalfreq_to_length(gates, netlist)

# array of found paths
all_paths = []

# initialize resulting length, iteration count
total_length, count = 0, 1

# run A-Star solver per netlist item, break if goal not possible
for connection in sorted_netlist:
    a = Astar.AStar_Solver(grid, gates[connection[0]], gates[connection[1]])
    
    if not a.Solve():
        print "Goal is not possible."
        break
    
    # add found path to walls and all paths
    grid.walls += a.path
    all_paths.append(a.path)
    
    # record procress
    print 'Line %s solved, of length %s' % (count, len(a.path))
    
    # add path length to total
    total_length += len(a.path) - 1
    count += 1
print gates[0].x, gates[0].y, gates[0].z
    
# print to output file (results[print]_[netlist]_[solved]_[length])
filename = 'result%s_%s_%s_%s.txt' % (print_index, len(sorted_netlist), count - 1, total_length)
output = open(filename, "w")
output.write('%s\n' % (sorted_netlist))
output.write('The lower boundary for this netlist: %s\n\n' % (min_dist))

# print moves to output file
path_lengths, moves_x, moves_y, moves_z, count = [], [], [], [], 1
for path in all_paths:

    # print length of individual paths
    output.write('Length of path # %s : %s\n' % (count, (len(path) - 1)))
    path_lengths.append(len(path) - 1)

    # print positions in individual paths
    for position in path:
        moves_x.append(position.x)
        moves_y.append(position.y)
        moves_z.append(position.z)
        output.write('%s %s %s\n' % (position.x, position.y, position.z))
    count += 1
 
# print score compared to lower bound
print 'Number of paths found: %s / %s' % (count - 1, len(sorted_netlist))
print 'The lower boundary for this netlist: %s' % (min_dist)
print 'The total length of this run: ', total_length
output.write('Number of paths found: %s / %s\n' % (count - 1, len(sorted_netlist)))
output.write('The total length is: %s\n' % (total_length))

output.close()

# define input for visualisation
moves_raw = np.array((moves_x, moves_y, moves_z))
moves = np.transpose(moves_raw)

# visualise board
Visualisation.DrawScatter(width, height, gates)
Visualisation.drawMoves(moves, path_lengths, total_length)
Visualisation.drawXYplane(width, height)