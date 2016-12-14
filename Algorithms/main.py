"""
MAIN
accompaniying python files are Astar, visualisation and netlist_sort

TODO
    profiler implementeren: Guido
    rearrange: Guido
    cost rondom gates: Laura (afh van freq, verhouding (grid search?), nog een generatie)
    z = 0, z = 1 extra cost: Laura
    verschillende kleuren lijnen: Laura
    label fade: Laura
    foutmelding visualisatie: Guido en Floris
    paper: Floris
    presentatie: Floris
    garafieken maken: iedereen
    statespace: optioneel
"""
import Astar
import netlist_sort
import visualisation
import numpy as np

# indicate start
print 'running...'

# load board data
print_file = '../Netlists and prints/print1.csv'
print_index = int(print_file[28])
netlist_file = '../Netlists and prints/netlist1_30.csv'

# board dimensions
width = 17
if print_index == 1:
    height = 12
elif print_index == 2:
    height = 16

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
    print 'Line %s solved, of length %s' % (count, len(a.path) - 1)
    
    # add path length to total
    total_length += len(a.path) - 1
    count += 1
    
# print to output file (results[print]_[netlist]_[solved]_[length])
filename = '../Diagnostics/%s_%s/result%s_%s_%s_%s.txt' % (print_index, len(sorted_netlist), print_index, len(sorted_netlist), count - 1, total_length)
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

# visualise board by Visualisation.py
visualisation.init(width, height, gates, moves, path_lengths, total_length)