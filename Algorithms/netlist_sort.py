"""
Different netlist sorting algorithms for optimization
"""
from Queue import PriorityQueue

"""
Sort netlist by the summed frequencies of gates per tuple, then length of path
This way high priority lines are laid out first, all the same ordered short to long
"""
def totalfreq_to_length(gates, netlist):
    # determine frequency of gates in netlist and highest frequency
    freq = [0] * len(gates)
    for line in netlist:
        for item in line:
            freq[item] += 1
    highest_freq = max(freq)
    
    # set up arrays for netlist sorting
    queue = PriorityQueue()
    freq_sort = []
    length_sort = []
    sorted_netlist = []
    
    # from each tuple in netlist, add the summed frequencies of both gates to freq_sort
    for elem in netlist:
        totalocc = freq[elem[0]] + freq[elem[1]]
        freq_sort.append(totalocc)
    
    # iterate over freq_sort, sort netlist tuples of same summed frequency according to length in sorted_netlist
    for i in xrange(0, (highest_freq*2)):
        for j in xrange(0, len(freq_sort)):
            if freq_sort[j] == ((highest_freq*2) - i):
                length_sort.append(netlist[j])
        for elem in length_sort:
            queue.put((gates[elem[0]].getDist(gates[elem[1]]), elem))
        for i in xrange(0, len(length_sort)):
            sorted_netlist.append(queue.get()[1])
        length_sort = []
    
    return sorted_netlist

def on_length(gates, netlist):
    queue = PriorityQueue()
    sorted_netlist = []
    for elem in netlist:
        queue.put((gates[elem[0]].getDist(gates[elem[1]]), elem))

    for i in xrange(0, len(netlist)):
        sorted_netlist.append(queue.get()[1])

    return sorted_netlist

def on_original(gates, netlist):
    sorted_netlist = netlist
    return sorted_netlist