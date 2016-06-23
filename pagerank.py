import sys

def make_nodelist(lines):
    index = 0
    node_number = 0
    nodes = []
    while lines[0][index] != '\n':
        node_number = node_number * 10 + int(lines[0][index])
        index += 1
    index = 1
    while index < node_number + 1:
        node = {'name': lines[index].rstrip("\n"), 'edges': [], 'point': 100.0, 'temp': 0.0}
        nodes.append(node)
        index += 1
    return nodes, node_number

def make_edgelist(lines, nodes, node_number):
    index = 0
    edge_number = 0
    while lines[node_number + 1][index] != '\n':
        edge_number = edge_number * 10 + int(lines[node_number + 1][index])
        index += 1
    index = node_number + 2
    while index < len(lines):
        node_index = 0
        while node_index < node_number:
            edge = lines[index].split()
            if edge[0] == nodes[node_index]['name']:
                nodes[node_index]['edges'].append(edge[1])
            node_index += 1
        index += 1

def give_point2(node, nodes):
    index = 0
    while index < len(node['edges']):
        index2 = 0
        while index2 < len(nodes):
            if node['edges'][index] == nodes[index2]['name']:
                nodes[index2]['temp'] += node['point'] / len(node['edges'])
            index2 += 1
        index += 1

def give_point(nodes):
    index = 0
    while index < len(nodes):
        give_point2(nodes[index], nodes)
        index += 1

def pagerank(nodes):
    index = 0
    sum = 0
    flag = []
    flag_sum = 0
    give_point(nodes)
    while index < len(nodes):
        if abs(nodes[index]['point'] - nodes[index]['temp']) < 0.001:
            flag.append(0)
        else:
            flag.append(1)
        nodes[index]['point'] = nodes[index]['temp']
        nodes[index]['temp'] = 0
        sum += nodes[index]['point']
        index += 1
    index = 0
    while index < len(nodes):
        flag_sum += flag[index]
        index += 1
    if flag_sum == 0:
        return 0
    else:
        return 1

def main():
    i = 0
    index = 0
    sum = 0
    f = open('./homework4/large_data.txt')
    lines = f.readlines()
    (nodes, node_number) = make_nodelist(lines)
    make_edgelist(lines, nodes, node_number)
    f.close()
    while i < 1000:
        flag = pagerank(nodes)
        if flag == 0:
            break
        i += 1
    while index < len(nodes):
        print nodes[index]['name'] + ': ' + str(nodes[index]['point'])
        sum += nodes[index]['point']
        index += 1
    print 'sum: ' + str(sum)
    sys.exit(0)
    
if __name__ == '__main__':
    main()
