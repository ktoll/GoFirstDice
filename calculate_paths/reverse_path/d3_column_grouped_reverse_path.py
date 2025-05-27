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
         continue
      for ba_possibility in ba_path_columns[n - depth - 1][ba_share]:
         if ab_possibility[0] == ba_possibility[0]:
            if depth == n - 1:
               solutions.append(so_far + ab_possibility[0])
            else:
               solutions.extend(d2_path_finder_recursive(n, ab_possibility[1], ba_possibility[1], ab_path_columns, ba_path_columns, depth=depth+1, so_far=so_far + ab_possibility[0]))
   return solutions


def d3_path_maker(n, a, b, c): #n is for number of sides of dice
   path_columns = []
   path_lengths = []
   path_columns.append({0:{a + c + b: 0, c + a + b: 0, c + b + a: 0}, n - 1:{b + a + c: 0, b + c + a: 0}, n:{a + b + c: 0}})
   path_lengths.append({0:3, n - 1:2, n:1})
   for i in range(n - 1):
      path_columns.append({})
      path_lengths.append({})
      d3_path_column_maker(a + b + c, (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d3_path_column_maker(a + c + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d3_path_column_maker(b + a + c, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d3_path_column_maker(b + c + a, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d3_path_column_maker(c + a + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d3_path_column_maker(c + b + a, (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
   return path_columns, path_lengths

def d3_path_column_maker(group, addition, previous_path_column, current_path_column, previous_path_length, current_path_length):
   for path_num in previous_path_column:
      if path_num + addition not in current_path_column:
         #current_path_column[path_num + addition] = []
         current_path_column[path_num + addition] = {}
      if path_num + addition not in current_path_length:
         current_path_length[path_num + addition] = 0
      #current_path_column[path_num + addition].append((group, path_num))
      current_path_column[path_num + addition][group] = path_num
      current_path_length[path_num + addition] += previous_path_length[path_num]


def d3_path_finder_maker_reverse(n):
   share = pow(n, 3) / math.factorial(3)
   abc_path_columns, abc_path_lengths = d3_path_maker(n, 'a', 'b', 'c')
   print(abc_path_lengths[n - 1][share])
   acb_path_columns, acb_path_lengths = d3_path_maker(n, 'a', 'c', 'b')
   bac_path_columns, bac_path_lengths = d3_path_maker(n, 'b', 'a', 'c')
   bca_path_columns, bca_path_lengths = d3_path_maker(n, 'b', 'c', 'a')
   cab_path_columns, cab_path_lengths = d3_path_maker(n, 'c', 'a', 'b')
   cba_path_columns, cba_path_lengths = d3_path_maker(n, 'c', 'b', 'a')
   reverse_path_columns = []
   for i in range(n):
      reverse_path_columns.append({})
   abc_init = abc_path_columns[n - 1][share]['abc']
   acb_init = acb_path_columns[n - 1][share]['abc']
   bac_init = bac_path_columns[n - 1][share]['abc']
   bca_init = bca_path_columns[n - 1][share]['abc']
   cab_init = cab_path_columns[n - 1][share]['abc']
   cba_init = cba_path_columns[n - 1][share]['abc']
   reverse_path_columns[n - 1][(abc_init, acb_init, bac_init, bca_init, cab_init, cba_init)] = {}
   reverse_path_columns[n - 1][(abc_init, acb_init, bac_init, bca_init, cab_init, cba_init)]['abc'] = (share, share, share, share, share, share)
   for i in range(n - 2, -1, -1):
      d3_reverse_path_column_maker(abc_path_columns[i], acb_path_columns[i], bac_path_columns[i], bca_path_columns[i], cab_path_columns[i], cba_path_columns[i], reverse_path_columns[i + 1], reverse_path_columns[i])
   return reverse_path_columns

def d3_reverse_path_column_maker(abc_path_column, acb_path_column, bac_path_column, bca_path_column, cab_path_column, cba_path_column, previous_reverse_path_column, current_reverse_path_column):
   for previous in previous_reverse_path_column:
      for group in abc_path_column[previous[0]]:
         if group in acb_path_column[previous[1]]:
            if group in bac_path_column[previous[2]]:
               if group in bca_path_column[previous[3]]:
                  if group in cab_path_column[previous[4]]:
                     if group in cba_path_column[previous[5]]:
                        current = (abc_path_column[previous[0]][group], acb_path_column[previous[1]][group], bac_path_column[previous[2]][group], bca_path_column[previous[3]][group], cab_path_column[previous[4]][group], cba_path_column[previous[5]][group])
                        if current not in current_reverse_path_column:
                           current_reverse_path_column[current] = {}
                        current_reverse_path_column[current][group] = previous
   

def d3_path_finder_reverse(n):
   reverse_paths = d3_path_finder_maker_reverse(n)
   for i in range(n):
      print('')
      #print(reverse_paths[i])
      l = 0
      for j in reverse_paths[i]:
         l += len(reverse_paths[i][j])
      print(l)
   return d3_path_finder_reverse_recursive(n, reverse_paths)

def d3_path_finder_reverse_recursive(n, reverse_paths, shares=(0, 0, 0, 0, 0, 0), depth=0, so_far=''):
   solutions = []
   for group_option in reverse_paths[depth][shares]:
      if depth == n - 1:
         solutions.append(group_option + so_far)
      else:
         solutions.extend(d3_path_finder_reverse_recursive(n, reverse_paths, reverse_paths[depth][shares][group_option], depth + 1, group_option + so_far))
   return solutions


def d3_path_finder(n):
   share = pow(n, 3) / math.factorial(3)
   abc_path_columns, abc_path_lengths = d3_path_maker(n, 'a', 'b', 'c')
   print(abc_path_lengths[n - 1][share])
   acb_path_columns, acb_path_lengths = d3_path_maker(n, 'a', 'c', 'b')
   bac_path_columns, bac_path_lengths = d3_path_maker(n, 'b', 'a', 'c')
   bca_path_columns, bca_path_lengths = d3_path_maker(n, 'b', 'c', 'a')
   cab_path_columns, cab_path_lengths = d3_path_maker(n, 'c', 'a', 'b')
   cba_path_columns, cba_path_lengths = d3_path_maker(n, 'c', 'b', 'a')
   #print(share)
   return d3_path_finder_recursive(n, share, share, share, share, share, share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns)

def d3_path_finder_recursive(n, abc_share, acb_share, bac_share, bca_share, cab_share, cba_share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=0, so_far=''):
   solutions = []
   for abc_possibility in abc_path_columns[n - depth - 1][abc_share]:
      if depth == 0 and abc_possibility[0] != 'abc':
         continue
      for acb_possibility in acb_path_columns[n - depth - 1][acb_share]:
         if abc_possibility[0] == acb_possibility[0]:
            for bac_possibility in bac_path_columns[n - depth - 1][bac_share]:
               if abc_possibility[0] == bac_possibility[0]:
                  for bca_possibility in bca_path_columns[n - depth - 1][bca_share]:
                     if abc_possibility[0] == bca_possibility[0]:
                        for cab_possibility in cab_path_columns[n - depth - 1][cab_share]:
                           if abc_possibility[0] == cab_possibility[0]:
                              for cba_possibility in cba_path_columns[n - depth - 1][cba_share]:
                                 if abc_possibility[0] == cba_possibility[0]:
                                    if depth == n - 1:
                                       solutions.append(so_far + abc_possibility[0])
                                    else:
                                       solutions.extend(d3_path_finder_recursive(n, abc_possibility[1], acb_possibility[1], bac_possibility[1], bca_possibility[1], cab_possibility[1], cba_possibility[1], abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=depth+1, so_far=so_far + abc_possibility[0]))
   return solutions

#for path_column in d3_path_maker(6, 'a', 'b', 'c'):
#   print(path_column)

n = 12
solutions = d3_path_finder_reverse(n)
share = pow(n, 3) / math.factorial(3)
for solution in condenser(solutions):
   if not checker(solution, 3, share):
      print('oh no!')
   print(solution)
