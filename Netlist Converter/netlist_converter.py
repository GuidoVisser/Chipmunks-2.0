# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 23:51:00 2016

@author: Laura
"""
count_prints = 0
list_info = []
net = []

# read information from netlist.txt
txt_file = open('netlists.txt', 'r')
lines = txt_file.readlines()
for line in lines:
    if line.startswith('# print '):
        count_prints += 1
    if line.startswith('# lengte '):
        list_info.append(count_prints)
        number = line[9:11]
        list_info.append(int(number))
    if line.startswith('netlist_'):
        list = line[14:(len(line)-3)]
        split = list.split('), (')
        for item in split:
            split2 = item.split(', ')
            path = [int(split2[0]), int(split2[1])]
            net.append(path)
        list_info.append(net)
        net = []

txt_file.close()

# write information to formated .csv  
i = 0
while i < len(list_info):
    netlist = 'netlist%s_%s.csv' % (list_info[i], list_info[i+1])
    list_file = open(netlist, 'w')
    path = 0
    while path < len(list_info[i + 2]):
        list_file.write('%s,%s\n' % (list_info[i + 2][path][0], list_info[i + 2][path][1]))
        path += 1
    list_file.close() 
    i += 3