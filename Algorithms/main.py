"""
MAIN
accompaniying python files are Astar, visualisation and netlist_sort
TODO
    profiler implementeren: Guido
    rearrange: Guido
    cost rondom gates: Laura (afh van freq, verhouding (grid search?))
    z = 0, z = 1 extra cost: Laura
    (label fade: Laura)
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
import winsound
import copy
from time import localtime, strftime

# enable iteration
for iteration in range(0, 1):
    # indicate start
    print 'running...'

    # load board data
    print_file = '../Netlists and prints/testprint.csv'
    print_index = 0 #int(print_file[-5])
    netlist_file = '../Netlists and prints/testnetlist.csv'

    # board dimensions
    width = 3
    height = 2
    if print_index == 1:
        height = 12
    elif print_index == 2:
        height = 16

    # width = 7
    # height = 6

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
    total_length, count, max_count = 0, 1, 1


    sequence_position, stepBack, rearrange_count, all_sequences = 0, 0, 0, []

    first_sequence = []
    for i in xrange(0, len(sorted_netlist)):
        first_sequence.append(i)
    all_sequences.append(first_sequence)

    # run A-Star solver per netlist item, break if goal not possible
    while sequence_position < len(sorted_netlist):
        current_sequence = copy.copy(all_sequences[-1])
        for connection in sorted_netlist[sequence_position:]:
            a = Astar.AStar_Solver(grid, gates[connection[0]], gates[connection[1]])

            if not a.Solve():
                if sequence_position > stepBack and stepBack != 0:

                    # remove latest paths from walls
                    for path in all_paths[-stepBack:]:
                        total_length -= len(path)
                        for position in path:
                            grid.walls.remove(position)

                    # remove latest paths from all_paths
                    all_paths = all_paths[:-stepBack]

                    # rearrange sorted_netlist so that latest paths are put at the end
                    sorted_netlist += sorted_netlist[sequence_position-stepBack:sequence_position]
                    current_sequence += current_sequence[sequence_position-stepBack:sequence_position]
                    for k in xrange(0, stepBack):
                        sorted_netlist.remove(sorted_netlist[sequence_position-stepBack])
                        current_sequence.remove(current_sequence[sequence_position-stepBack])

                    # set values i and count back
                    sequence_position -= stepBack
                    count -= stepBack
                    rearrange_count += 1

                    if current_sequence in all_sequences:
                        print "breaking out of loop"
                        sequence_position += len(sorted_netlist)
                        break
                    else:
                        all_sequences.append(current_sequence)

                    # message
                    print "path not possible"
                    print "removing last %i paths, and resuming" % (stepBack)

                    # break out of for loop
                    break

                else:
                    print "Goal is not possible."
                    sequence_position += len(sorted_netlist)
                    break

            # add found path to walls and all paths
            grid.walls += a.path
            all_paths.append(a.path)

            # record procress
            print 'Line %s solved, of length %s. Lowest possible is %s' % (
            count, len(a.path) - 1, gates[connection[0]].getDist(gates[connection[1]]))

            # add path length to total
            total_length += len(a.path) - 1
            count += 1
            sequence_position += 1
            if count > max_count:
                max_count = count

    # print to output file (results[print]_[netlist]_[solved]_[length])
    filename = '../Diagnostics/%s_%s/result_%s_%s_%s_%s_%s_%s.txt' % (
    print_index, len(sorted_netlist), print_index, len(sorted_netlist), max_count - 1, total_length, iteration, (strftime("(%H.%M.%S, %dth)", localtime())))
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
    print 'Number of paths found: %s / %s' % (max_count - 1, len(sorted_netlist))
    print 'The lower boundary for this netlist: %s' % (min_dist)
    print 'The total length of this run: ', total_length
    output.write('Number of paths found: %s / %s\n' % (max_count - 1, len(sorted_netlist)))
    output.write('The total length is: %s\n' % (total_length))

    output.close()

    # indicate solution
    freq = 1000
    dur = 500
    # winsound.Beep(freq,dur)

    # define input for visualisation
    moves_raw = np.array((moves_x, moves_y, moves_z))
    moves = np.transpose(moves_raw)

    # visualise board by Visualisation.py (disable in iteration)
    visualisation.init(width, height, gates, moves, path_lengths, total_length)
    
