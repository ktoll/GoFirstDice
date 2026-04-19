#!/usr/bin/python3

#addition_map[group][0,1,2,3] = list of perms that get that addition where 0,1,2,3 is n,n-p-1,p,0.
addition_map = {0:[[0],[1,3],[2,4],[5]],
                1:[[1],[0,5],[2,4],[3]],
                2:[[2],[1,3],[0,5],[4]],
                3:[[3],[2,4],[0,5],[1]],
                4:[[4],[0,5],[1,3],[2]],
                5:[[5],[2,4],[1,3],[0]]}
string_map = ["abc", "acb", "bac", "bca", "cab", "cba"]

def sum_from_1(endpoint):
   s = 0
   for i in range(endpoint + 1):
      s += i
   return s

def get_goal(n):
   knowns = 2 * n * sum_from_1(n - 2)
   return int((pow(n, 3) - knowns) / 6)

def get_node_string(node, n):
   node_string = ""
   if node:
      for column in range(n):
         group = int(((node % pow(6, (n - column))) - (node % pow(6, (n - column - 1)))) / pow(6, (n - column - 1)))
         node_string += string_map[group]
   else:
      node_string = ":("
   return node_string

def get_delta(node, n, goal):
   perms = [0, 0, 0, 0, 0, 0]
   for column in range(n):
      group = ((node % pow(6, (n - column))) - (node % pow(6, (n - column - 1)))) / pow(6, (n - column - 1))
      perms[addition_map[group][0][0]] += n
      perms[addition_map[group][1][0]] += n - column - 1
      perms[addition_map[group][1][1]] += n - column - 1
      perms[addition_map[group][2][0]] += column
      perms[addition_map[group][2][1]] += column
      #perms[addition_map[group][3][0]] += 0
   delta = 0
   for perm in perms:
      delta += abs(perm - goal)
   return delta

def get_neighbors(node, n):
   neighbors = []
   for column in range(n):
      base_node = node - (node % pow(6, (n - column)) - (node % pow(6, (n - column - 1))))
      for group in range(6):
         neighbor = base_node + group * pow(6, (n - column - 1))
         if neighbor != node:
            neighbors.append(neighbor)
   return neighbors

def a_star(max_iters, n, goal):
   open_deltas = []
   open_nodes = {}
   closed = {}
   i = 0

   initial_node = 0
   initial_delta = get_delta(initial_node, n, goal)
   open_deltas.append(initial_delta)
   open_nodes[initial_delta] = [initial_node]

   while (i < max_iters) and open_deltas:
      i += 1
      current_delta = open_deltas[0]
      for delta in open_deltas:
         if delta < current_delta:
            current_delta = delta
      current_node = open_nodes[current_delta][0]
      open_nodes[current_delta].remove(current_node)
      if not open_nodes[current_delta]:
         open_deltas.remove(current_delta)
      closed[current_node] = current_delta

      #print(str(i) + ": " + str(current_node))

      if current_delta == 0:
         print("iters: " + str(i))
         return current_node

      for neighbor in get_neighbors(current_node, n):
         if not neighbor in closed:
            delta = get_delta(neighbor, n, goal)
            if not delta in open_deltas:
               open_deltas.append(delta)
               open_nodes[delta] = []
            if not neighbor in open_nodes[delta]:
               open_nodes[delta].append(neighbor)

#for i in range(1, 20):
for n in [54, 66]:
   #n = 6 * i
   goal = get_goal(n)
   print("n = " + str(n))
   print(get_node_string(a_star(1000, n, goal), n))
