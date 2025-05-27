#!/usr/bin/python

import math

def checker(s, l, q):
   count = {"" : 1}
   for c in s:
      for k in count.keys():
         if k.count(c)==0:
            k2 = k + c
            count[k2] = count.get(k2,0) + count[k]
   good = True
   for k in count.keys():
      if len(k) == l:
         good &= count[k] == q
   return good

def equivalence_checker(s1, s2):
   name_map = {}
   equivalent = True
   for i in range(len(s1)):
      if s1[i] in name_map:
         if s2[len(s2) - i - 1] != name_map[s1[i]]:
            equivalent = False
      elif s2[len(s2) - i - 1] not in name_map.values():
         name_map[s1[i]] = s2[len(s2) - i - 1]
      else:
         equivalent = False
   return equivalent

def condenser(all_sets):
   condensed_sets = []
   for s in all_sets:
      already_there = False
      for c in condensed_sets:
         if equivalence_checker(s, c):
            already_there = True
      if not already_there:
         condensed_sets.append(s)
   return condensed_sets


def d2_path_maker(n, a, b): #n is for number of sides of dice
   path_columns = []
   path_columns.append({n - 1:[(b + a, 0)], n:[(a + b, 0)]})
   for i in range(n - 1):
      path_columns.append({})
      d2_path_column_maker(a + b, n - i - 1, path_columns[i], path_columns[i + 1])
      d2_path_column_maker(b + a, n - i - 2, path_columns[i], path_columns[i + 1])
   return path_columns

def d2_path_column_maker(group, addition, previous_path_column, current_path_column):
   for path_num in previous_path_column:
      if path_num + addition not in current_path_column:
         current_path_column[path_num + addition] = []
      current_path_column[path_num + addition].append((group, path_num))


def d2_path_finder(n):
   ab_path_columns = d2_path_maker(n, 'a', 'b')
   ba_path_columns = d2_path_maker(n, 'b', 'a')
   share = pow(n, 2) / math.factorial(2)
   return d2_path_finder_recursive(n, share, share, ab_path_columns, ba_path_columns)

def d2_path_finder_recursive(n, ab_share, ba_share, ab_path_columns, ba_path_columns, depth=0, so_far=''):
   solutions = []
   for ab_possibility in ab_path_columns[n - depth - 1][ab_share]:
      if depth == 0 and ab_possibility[0] != 'ab':
         break
      for ba_possibility in ba_path_columns[n - depth - 1][ba_share]:
         if ab_possibility[0] == ba_possibility[0]:
            if depth == n - 1:
               solutions.append(so_far + ab_possibility[0])
            else:
               solutions.extend(d2_path_finder_recursive(n, ab_possibility[1], ba_possibility[1], ab_path_columns, ba_path_columns, depth=depth+1, so_far=so_far + ab_possibility[0]))
   return solutions


for solution in d2_path_finder(8):
   print(solution)
