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
            break
      elif s2[len(s2) - i - 1] not in name_map.values():
         name_map[s1[i]] = s2[len(s2) - i - 1]
      else:
         equivalent = False
         break
   return equivalent

def condenser(all_sets):
   condensed_sets = []
   for s in all_sets:
      already_there = False
      for c in condensed_sets:
         if equivalence_checker(s, c):
            already_there = True
            break
      if not already_there:
         condensed_sets.append(s)
   return condensed_sets


def d2_path_maker(n, a, b): #n is for number of sides of dice
   path_columns = []
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column.
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
   #minimums = [0, 4, 13, 21, 30, 36]
   #maximums = [6, 15, 23, 32, 36, 36]
   minimums = [0, 10, 28, 53, 88, 124, 159, 191, 225, 254, 276, 288]
   maximums = [12, 34, 63, 97, 129, 164, 200, 235, 260, 278, 288, 288]
   #minimums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   #maximums = [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column.
   path_columns.append({0:[(a + c + b, 0), (c + a + b, 0), (c + b + a, 0)], n - 1:[(b + a + c, 0), (b + c + a, 0)], n:[(a + b + c, 0)]})
   for i in range(n - 1):
      path_columns.append({})
      d3_path_column_maker(a + b + c, (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d3_path_column_maker(a + c + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d3_path_column_maker(b + a + c, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d3_path_column_maker(b + c + a, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d3_path_column_maker(c + a + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d3_path_column_maker(c + b + a, (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
   return path_columns

def d3_path_column_maker(group, addition, previous_path_column, current_path_column, minimum, maximum):
   for path_num in previous_path_column:
      if (path_num + addition >= minimum) and (path_num + addition <= maximum):
         if (path_num + addition not in current_path_column):
            current_path_column[path_num + addition] = []
         current_path_column[path_num + addition].append((group, path_num))


def d3_path_finder(n):
   abc_path_columns = d3_path_maker(n, 'a', 'b', 'c')
   acb_path_columns = d3_path_maker(n, 'a', 'c', 'b')
   bac_path_columns = d3_path_maker(n, 'b', 'a', 'c')
   bca_path_columns = d3_path_maker(n, 'b', 'c', 'a')
   cab_path_columns = d3_path_maker(n, 'c', 'a', 'b')
   cba_path_columns = d3_path_maker(n, 'c', 'b', 'a')
   share = pow(n, 3) / math.factorial(3)
   print(share)
   global a_global
   a_global = 0
   return d3_path_finder_recursive(n, share, share, share, share, share, share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns)

def d3_path_finder_recursive(n, abc_share, acb_share, bac_share, bca_share, cab_share, cba_share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=0, so_far='', so_far_mins = [], so_far_maxes = []):
   global a_global
   solutions = []
   for abc_possibility in abc_path_columns[n - depth - 1][abc_share]:
      a_global += 1
      if depth == 0 and abc_possibility[0] != 'abc':
         continue
      for acb_possibility in acb_path_columns[n - depth - 1][acb_share]:
         a_global += 1
         if abc_possibility[0] == acb_possibility[0]:
            for bac_possibility in bac_path_columns[n - depth - 1][bac_share]:
               a_global += 1
               if abc_possibility[0] == bac_possibility[0]:
                  for bca_possibility in bca_path_columns[n - depth - 1][bca_share]:
                     a_global += 1
                     if abc_possibility[0] == bca_possibility[0]:
                        for cab_possibility in cab_path_columns[n - depth - 1][cab_share]:
                           a_global += 1
                           if abc_possibility[0] == cab_possibility[0]:
                              for cba_possibility in cba_path_columns[n - depth - 1][cba_share]:
                                 a_global += 1
                                 if abc_possibility[0] == cba_possibility[0]:
                                    if depth == n - 1:
                                       solutions.append(so_far + abc_possibility[0])
                                       #print('mins:')
                                       #print(so_far_mins + [min(abc_share, acb_share, bac_share, bca_share, cab_share, cba_share)])
                                       #print('maxes:')
                                       #print(so_far_maxes + [max(abc_share, acb_share, bac_share, bca_share, cab_share, cba_share)])
                                    else:
                                       solutions.extend(d3_path_finder_recursive(n, abc_possibility[1], acb_possibility[1], bac_possibility[1], bca_possibility[1], cab_possibility[1], cba_possibility[1], abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=depth+1, so_far=so_far + abc_possibility[0], so_far_mins=so_far_mins + [min(abc_share, acb_share, bac_share, bca_share, cab_share, cba_share)], so_far_maxes=so_far_maxes + [max(abc_share, acb_share, bac_share, bca_share, cab_share, cba_share)]))
   return solutions


def d4_path_maker(n, a, b, c, d): #n is for number of sides of dice
   path_columns = []
   #minimums = [0, 0, 18, 84, 140, 226, 356, 498, 594, 742, 792, 864]
   #maximums = [12, 22, 70, 110, 206, 314, 424, 524, 684, 764, 864, 864]
   minimums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   maximums = [10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000]
   #minimums = [0, 0, 15, 57, 232, 390, 598, 855, 1147, 1468, 1856, 2308, 2786, 3243, 3535, 3922, 4212, 4374]
   #maximums = [18, 69, 165, 315, 428, 663, 956, 1305, 1678, 2036, 2423, 2813, 3202, 3573, 4025, 4247, 4374, 4374]
   #minimums = [0, 0, 15, 57, 252, 417, 634, 900, 1200, 1525, 1913, 2359, 2828, 3276, 3535, 3922, 4212, 4374]
   #maximums = [18, 69, 165, 315, 408, 636, 920, 1260, 1625, 1980, 2366, 2762, 3160, 3540, 4025, 4247, 4374, 4374]
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column. 
   #the second map inside the first and the second int in the tuple are how many cd strings are downstream.
   path_columns.append({0:{0:{a + b + d + c:(0, 0), a + d + b + c: (0, 0), a + d + c + b:(0, 0), b + a + d + c:(0, 0), b + d + a + c:(0, 0), b + d + c + a:(0, 0), d + a + b + c:(0, 0), d + a + c + b:(0, 0), d + b + a + c:(0, 0), d + b + c + a:(0, 0), d + c + a + b:(0, 0), d + c + b + a:(0, 0)}, 1:{a + c + b + d:(0, 0), a + c + d + b:(0, 0), c + a + b + d:(0, 0), c + a + d + b:(0, 0), c + b + a + d:(0, 0), c + b + d + a:(0, 0), c + d + a + b:(0, 0), c + d + b + a:(0, 0)}}, n - 1:{1:{b + a + c + d:(0, 0), b + c + a + d:(0, 0), b + c + d + a:(0, 0)}}, n:{1:{a + b + c + d:(0, 0)}}})
   for i in range(n - 1):
      path_columns.append({})
      d4_path_column_maker(a + b + c + d, (n - i - 1), (i + 2), (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(a + b + d + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(a + c + b + d, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(a + c + d + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(a + d + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(a + d + c + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + a + c + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + a + d + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + c + a + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + c + d + a, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + d + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(b + d + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + a + b + d, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + a + d + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + b + a + d, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + b + d + a, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + d + a + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(c + d + b + a, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + a + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + a + c + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + b + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + b + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + c + a + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
      d4_path_column_maker(d + c + b + a, (n - i - 2), (i + 1), 0, path_columns[i], path_columns[i + 1], minimums[i + 1], maximums[i + 1])
   return path_columns

def d4_path_column_maker(group, num_abs, add_cds, addition, previous_path_column, current_path_column, minimum, maximum):
   for path_num in previous_path_column:
      for path_cd_num in previous_path_column[path_num]:
         if (path_num + addition + (num_abs * path_cd_num) >= minimum) and (path_num + addition + (num_abs * path_cd_num) <= maximum):
            if path_num + addition + (num_abs * path_cd_num) not in current_path_column:
               current_path_column[path_num + addition + (num_abs * path_cd_num)] = {}
            if path_cd_num + add_cds not in current_path_column[path_num + addition + (num_abs * path_cd_num)]:
               current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds] = {}
            if group in current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds]:
               print('uh oh')
            current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds][group] = (path_num, path_cd_num)


def d4_path_finder(n):
   abcd_path_columns = d4_path_maker(n, 'a', 'b', 'c', 'd')
   abdc_path_columns = d4_path_maker(n, 'a', 'b', 'd', 'c')
   acbd_path_columns = d4_path_maker(n, 'a', 'c', 'b', 'd')
   acdb_path_columns = d4_path_maker(n, 'a', 'c', 'd', 'b')
   adbc_path_columns = d4_path_maker(n, 'a', 'd', 'b', 'c')
   adcb_path_columns = d4_path_maker(n, 'a', 'd', 'c', 'b')
   bacd_path_columns = d4_path_maker(n, 'b', 'a', 'c', 'd')
   badc_path_columns = d4_path_maker(n, 'b', 'a', 'd', 'c')
   bcad_path_columns = d4_path_maker(n, 'b', 'c', 'a', 'd')
   bcda_path_columns = d4_path_maker(n, 'b', 'c', 'd', 'a')
   bdac_path_columns = d4_path_maker(n, 'b', 'd', 'a', 'c')
   bdca_path_columns = d4_path_maker(n, 'b', 'd', 'c', 'a')
   cabd_path_columns = d4_path_maker(n, 'c', 'a', 'b', 'd')
   cadb_path_columns = d4_path_maker(n, 'c', 'a', 'd', 'b')
   cbad_path_columns = d4_path_maker(n, 'c', 'b', 'a', 'd')
   cbda_path_columns = d4_path_maker(n, 'c', 'b', 'd', 'a')
   cdab_path_columns = d4_path_maker(n, 'c', 'd', 'a', 'b')
   cdba_path_columns = d4_path_maker(n, 'c', 'd', 'b', 'a')
   dabc_path_columns = d4_path_maker(n, 'd', 'a', 'b', 'c')
   dacb_path_columns = d4_path_maker(n, 'd', 'a', 'c', 'b')
   dbac_path_columns = d4_path_maker(n, 'd', 'b', 'a', 'c')
   dbca_path_columns = d4_path_maker(n, 'd', 'b', 'c', 'a')
   dcab_path_columns = d4_path_maker(n, 'd', 'c', 'a', 'b')
   dcba_path_columns = d4_path_maker(n, 'd', 'c', 'b', 'a')
   share = pow(n, 4) / math.factorial(4)
   share_cd = pow(n, 2) / math.factorial(2)
   print(share)
   print(share_cd)
   global a_global
   a_global = 0
   #return d4_path_finder_recursive(n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)
   #return d4_path_finder_loop(n, {(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):{(share, share, share_cd):['']}}}}}}}}}}}}, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)
   new_abcd_path_columns = []
   for i in range(n):
      new_abcd_path_columns.append({})
   #d4_path_finder_loop_2(abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, [(share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd, share, share_cd)], n - 1, new_abcd_path_columns)
   d4_path_finder_loop_2(abcd_path_columns, dcba_path_columns, [(share, share_cd, share, share_cd)], n - 1, new_abcd_path_columns)
   print(new_abcd_path_columns[11][864][72])
   return d4_path_finder_recursive(n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, new_abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)

#abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][ebac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], 

#cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], 

#abcd, abdc, acbd, acdb, adbc, adcb, bacd, badc, bcad, bcda, bdac, bdca, cabd, cadb, cbad, cbda, cdab, cdba, dabc, dacb, dbac, dbca, dcab, dcba, 
def d4_path_finder_recursive(n, abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share, ab_share, ac_share, ad_share, ba_share, bc_share, bd_share, ca_share, cb_share, cd_share, da_share, db_share, dc_share, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0, so_far='', so_far_mins = [], so_far_maxes = []):
   global a_global
   solutions = []
   if abcd_share in abcd_path_columns[n - depth - 1]:
      if cd_share in abcd_path_columns[n - depth - 1][abcd_share]:
         for abcd_possibility in abcd_path_columns[n - depth - 1][abcd_share][cd_share]:
            a_global += 1
            if depth == 0 and abcd_possibility != 'abcd':
               continue
            if abcd_possibility in abdc_path_columns[n - depth - 1][abdc_share][dc_share]:
               if abcd_possibility in acbd_path_columns[n - depth - 1][acbd_share][bd_share]:
                  if abcd_possibility in acdb_path_columns[n - depth - 1][acdb_share][db_share]:
                     if abcd_possibility in adbc_path_columns[n - depth - 1][adbc_share][bc_share]:
                        if abcd_possibility in adcb_path_columns[n - depth - 1][adcb_share][cb_share]:
                           if abcd_possibility in bacd_path_columns[n - depth - 1][bacd_share][cd_share]:
                              if abcd_possibility in badc_path_columns[n - depth - 1][badc_share][dc_share]:
                                 if abcd_possibility in bcad_path_columns[n - depth - 1][bcad_share][ad_share]:
                                    if abcd_possibility in bcda_path_columns[n - depth - 1][bcda_share][da_share]:
                                       if abcd_possibility in bdac_path_columns[n - depth - 1][bdac_share][ac_share]:
                                          if abcd_possibility in bdca_path_columns[n - depth - 1][bdca_share][ca_share]:
                                             if abcd_possibility in cabd_path_columns[n - depth - 1][cabd_share][bd_share]:
                                                if abcd_possibility in cadb_path_columns[n - depth - 1][cadb_share][db_share]:
                                                   if abcd_possibility in cbad_path_columns[n - depth - 1][cbad_share][ad_share]:
                                                      if abcd_possibility in cbda_path_columns[n - depth - 1][cbda_share][da_share]:
                                                         if abcd_possibility in cdab_path_columns[n - depth - 1][cdab_share][ab_share]:
                                                            if abcd_possibility in cdba_path_columns[n - depth - 1][cdba_share][ba_share]:
                                                               if abcd_possibility in dabc_path_columns[n - depth - 1][dabc_share][bc_share]:
                                                                  if abcd_possibility in dacb_path_columns[n - depth - 1][dacb_share][cb_share]:
                                                                     if abcd_possibility in dbac_path_columns[n - depth - 1][dbac_share][ac_share]:
                                                                        if abcd_possibility in dbca_path_columns[n - depth - 1][dbca_share][ca_share]:
                                                                           if abcd_possibility in dcab_path_columns[n - depth - 1][dcab_share][ab_share]:
                                                                              if abcd_possibility in dcba_path_columns[n - depth - 1][dcba_share][ba_share]:
                                                                                 if depth == n - 1:
                                                                                    solutions.append(so_far + abcd_possibility)
                                                                                    print('mins:')
                                                                                    print(so_far_mins + [min(abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share)])
                                                                                    print('maxes:')
                                                                                    print(so_far_maxes + [max(abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share)])
                                                                                 else:
                                                                                    solutions.extend(d4_path_finder_recursive(n, abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=depth+1, so_far=so_far + abcd_possibility, so_far_mins=so_far_mins + [min(abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share)], so_far_maxes=so_far_maxes + [max(abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share)]))
   return solutions

def d4_path_finder_loop(n, options_map, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0):
   print(depth)
   global a_global
   next_options_map = {}
   solutions = []
   for cd_tuple in options_map:
      abcd_share = cd_tuple[0]
      bacd_share = cd_tuple[1]
      cd_share = cd_tuple[2]
      for abcd_possibility in abcd_path_columns[n - depth - 1][abcd_share][cd_share]:
         a_global += 1
         if depth == 0 and abcd_possibility != 'abcd':
            continue
         if abcd_possibility in bacd_path_columns[n - depth - 1][bacd_share][cd_share]:
            for bd_tuple in options_map[cd_tuple]:
               acbd_share = bd_tuple[0]
               cabd_share = bd_tuple[1]
               bd_share = bd_tuple[2]
               if abcd_possibility in acbd_path_columns[n - depth - 1][acbd_share][bd_share]:
                  if abcd_possibility in cabd_path_columns[n - depth - 1][cabd_share][bd_share]:
                     for bc_tuple in options_map[cd_tuple][bd_tuple]:
                        adbc_share = bc_tuple[0]
                        dabc_share = bc_tuple[1]
                        bc_share = bc_tuple[2]
                        if abcd_possibility in adbc_path_columns[n - depth - 1][adbc_share][bc_share]:
                           if abcd_possibility in dabc_path_columns[n - depth - 1][dabc_share][bc_share]:
                              for dc_tuple in options_map[cd_tuple][bd_tuple][bc_tuple]:
                                 abdc_share = dc_tuple[0]
                                 badc_share = dc_tuple[1]
                                 dc_share = dc_tuple[2]
                                 if abcd_possibility in abdc_path_columns[n - depth - 1][abdc_share][dc_share]:
                                    if abcd_possibility in badc_path_columns[n - depth - 1][badc_share][dc_share]:
                                       for db_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple]:
                                          acdb_share = db_tuple[0]
                                          cadb_share = db_tuple[1]
                                          db_share = db_tuple[2]
                                          if abcd_possibility in acdb_path_columns[n - depth - 1][acdb_share][db_share]:
                                             if abcd_possibility in cadb_path_columns[n - depth - 1][cadb_share][db_share]:
                                                for cb_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple]:
                                                   adcb_share = cb_tuple[0]
                                                   dacb_share = cb_tuple[1]
                                                   cb_share = cb_tuple[2]
                                                   if abcd_possibility in adcb_path_columns[n - depth - 1][adcb_share][cb_share]:
                                                      if abcd_possibility in dacb_path_columns[n - depth - 1][dacb_share][cb_share]:
                                                         for ad_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple]:
                                                            bcad_share = ad_tuple[0]
                                                            cbad_share = ad_tuple[1]
                                                            ad_share = ad_tuple[2]
                                                            if abcd_possibility in bcad_path_columns[n - depth - 1][bcad_share][ad_share]:
                                                               if abcd_possibility in cbad_path_columns[n - depth - 1][cbad_share][ad_share]:
                                                                  for ac_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple]:
                                                                     bdac_share = ac_tuple[0]
                                                                     dbac_share = ac_tuple[1]
                                                                     ac_share = ac_tuple[2]
                                                                     if abcd_possibility in bdac_path_columns[n - depth - 1][bdac_share][ac_share]:
                                                                        if abcd_possibility in dbac_path_columns[n - depth - 1][dbac_share][ac_share]:
                                                                           for da_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple]:
                                                                              bcda_share = da_tuple[0]
                                                                              cbda_share = da_tuple[1]
                                                                              da_share = da_tuple[2]
                                                                              if abcd_possibility in bcda_path_columns[n - depth - 1][bcda_share][da_share]:
                                                                                 if abcd_possibility in cbda_path_columns[n - depth - 1][cbda_share][da_share]:
                                                                                    for ca_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple][da_tuple]:
                                                                                       bdca_share = ca_tuple[0]
                                                                                       dbca_share = ca_tuple[1]
                                                                                       ca_share = ca_tuple[2]
                                                                                       if abcd_possibility in bdca_path_columns[n - depth - 1][bdca_share][ca_share]:
                                                                                          if abcd_possibility in dbca_path_columns[n - depth - 1][dbca_share][ca_share]:
                                                                                             for ab_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple][da_tuple][ca_tuple]:
                                                                                                cdab_share = ab_tuple[0]
                                                                                                dcab_share = ab_tuple[1]
                                                                                                ab_share = ab_tuple[2]
                                                                                                if abcd_possibility in cdab_path_columns[n - depth - 1][cdab_share][ab_share]:
                                                                                                   if abcd_possibility in dcab_path_columns[n - depth - 1][dcab_share][ab_share]:
                                                                                                      for ba_tuple in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple][da_tuple][ca_tuple][ab_tuple]:
                                                                                                         cdba_share = ba_tuple[0]
                                                                                                         dcba_share = ba_tuple[1]
                                                                                                         ba_share = ba_tuple[2]
                                                                                                         if abcd_possibility in cdba_path_columns[n - depth - 1][cdba_share][ba_share]:
                                                                                                            if abcd_possibility in dcba_path_columns[n - depth - 1][dcba_share][ba_share]:
                                                                                                               if depth == n - 1:
                                                                                                                  for so_far in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple][da_tuple][ca_tuple][ab_tuple][ba_tuple]:
                                                                                                                     solutions.append(so_far + abcd_possibility)
                                                                                                               else:
                                                                                                                  next_abcd_share = abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0]
                                                                                                                  next_abdc_share = abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0]
                                                                                                                  next_acbd_share = acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0]
                                                                                                                  next_acdb_share = acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0]
                                                                                                                  next_adbc_share = adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0]
                                                                                                                  next_adcb_share = adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0]
                                                                                                                  next_bacd_share = bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0]
                                                                                                                  next_badc_share = badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0]
                                                                                                                  next_bcad_share = bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0]
                                                                                                                  next_bcda_share = bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0]
                                                                                                                  next_bdac_share = bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0]
                                                                                                                  next_bdca_share = bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0]
                                                                                                                  next_cabd_share = cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0]
                                                                                                                  next_cadb_share = cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0]
                                                                                                                  next_cbad_share = cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0]
                                                                                                                  next_cbda_share = cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0]
                                                                                                                  next_cdab_share = cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0]
                                                                                                                  next_cdba_share = cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0]
                                                                                                                  next_dabc_share = dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0]
                                                                                                                  next_dacb_share = dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0]
                                                                                                                  next_dbac_share = dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0]
                                                                                                                  next_dbca_share = dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0]
                                                                                                                  next_dcab_share = dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0]
                                                                                                                  next_dcba_share = dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0]
                                                                                                                  next_cd_share = abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1]
                                                                                                                  next_dc_share = abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1]
                                                                                                                  next_bd_share = acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1]
                                                                                                                  next_db_share = acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1]
                                                                                                                  next_bc_share = adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1]
                                                                                                                  next_cb_share = adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1]
                                                                                                                  next_ad_share = bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1]
                                                                                                                  next_da_share = bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1]
                                                                                                                  next_ac_share = bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1]
                                                                                                                  next_ca_share = bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1]
                                                                                                                  next_ab_share = cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1]
                                                                                                                  next_ba_share = cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1]
                                                                                                                  next_cd_tuple = (next_abcd_share, next_bacd_share, next_cd_share)
                                                                                                                  next_bd_tuple = (next_acbd_share, next_cabd_share, next_bd_share)
                                                                                                                  next_bc_tuple = (next_adbc_share, next_adbc_share, next_bc_share)
                                                                                                                  next_dc_tuple = (next_abdc_share, next_abdc_share, next_dc_share)
                                                                                                                  next_db_tuple = (next_acdb_share, next_acdb_share, next_db_share)
                                                                                                                  next_cb_tuple = (next_adcb_share, next_adcb_share, next_cb_share)
                                                                                                                  next_ad_tuple = (next_bcad_share, next_bcad_share, next_ad_share)
                                                                                                                  next_ac_tuple = (next_bdac_share, next_bdac_share, next_ac_share)
                                                                                                                  next_da_tuple = (next_bcda_share, next_bcda_share, next_da_share)
                                                                                                                  next_ca_tuple = (next_bdca_share, next_bdca_share, next_ca_share)
                                                                                                                  next_ab_tuple = (next_cdab_share, next_cdab_share, next_ab_share)
                                                                                                                  next_ba_tuple = (next_cdba_share, next_cdba_share, next_ba_share)
                                                                                                                  if next_cd_tuple not in next_options_map:
                                                                                                                     next_options_map[next_cd_tuple] = {}
                                                                                                                  if next_bd_tuple not in next_options_map[next_cd_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple] = {}
                                                                                                                  if next_bc_tuple not in next_options_map[next_cd_tuple][next_bd_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple] = {}
                                                                                                                  if next_dc_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple] = {}
                                                                                                                  if next_db_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple] = {}
                                                                                                                  if next_cb_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple] = {}
                                                                                                                  if next_ad_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple] = {}
                                                                                                                  if next_ac_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple] = {}
                                                                                                                  if next_da_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple] = {}
                                                                                                                  if next_ca_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple] = {}
                                                                                                                  if next_ab_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple][next_ab_tuple] = {}
                                                                                                                  if next_ba_tuple not in next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple][next_ab_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple][next_ab_tuple][next_ba_tuple] = []
                                                                                                                  for so_far in options_map[cd_tuple][bd_tuple][bc_tuple][dc_tuple][db_tuple][cb_tuple][ad_tuple][ac_tuple][da_tuple][ca_tuple][ab_tuple][ba_tuple]:
                                                                                                                     next_options_map[next_cd_tuple][next_bd_tuple][next_bc_tuple][next_dc_tuple][next_db_tuple][next_cb_tuple][next_ad_tuple][next_ac_tuple][next_da_tuple][next_ca_tuple][next_ab_tuple][next_ba_tuple].append(so_far + abcd_possibility)
   if depth == n - 1:
      return solutions
   else:
      return d4_path_finder_loop(n, next_options_map, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth = depth + 1)

def d4_path_finder_loop_2(abcd_path_columns, dcba_path_columns, path_options, depth, new_abcd_path_columns):
   print(len(path_options))
   next_path_options = []
   for path_option in path_options:
      for group in abcd_path_columns[depth][path_option[0]][path_option[1]]:
         if group in dcba_path_columns[depth][path_option[2]][path_option[3]]:
            if (abcd_path_columns[depth][path_option[0]][path_option[1]][group][0], abcd_path_columns[depth][path_option[0]][path_option[1]][group][1], dcba_path_columns[depth][path_option[2]][path_option[3]][group][0], dcba_path_columns[depth][path_option[2]][path_option[3]][group][1]) not in next_path_options:
               next_path_options.append((abcd_path_columns[depth][path_option[0]][path_option[1]][group][0], abcd_path_columns[depth][path_option[0]][path_option[1]][group][1], dcba_path_columns[depth][path_option[2]][path_option[3]][group][0], dcba_path_columns[depth][path_option[2]][path_option[3]][group][1]))
            if path_option[0] not in new_abcd_path_columns[depth]:
               new_abcd_path_columns[depth][path_option[0]] = {}
            if path_option[1] not in new_abcd_path_columns[depth][path_option[0]]:
               new_abcd_path_columns[depth][path_option[0]][path_option[1]] = {}
            if group not in new_abcd_path_columns[depth][path_option[0]][path_option[1]]:
               new_abcd_path_columns[depth][path_option[0]][path_option[1]][group] = abcd_path_columns[depth][path_option[0]][path_option[1]][group]
   if depth:
      d4_path_finder_loop_2(abcd_path_columns, dcba_path_columns, next_path_options, depth - 1, new_abcd_path_columns)
#def d4_path_finder_loop_2(abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, path_options, depth, new_abcd_path_columns):
#   print(len(path_options))
#   next_path_options = []
#   for path_option in path_options:
#      for group in abcd_path_columns[depth][path_option[0]][path_option[1]]:
#         if group in abdc_path_columns[depth][path_option[2]][path_option[3]] and \
#            group in acbd_path_columns[depth][path_option[4]][path_option[5]] and \
#            group in acdb_path_columns[depth][path_option[6]][path_option[7]] and \
#            group in adbc_path_columns[depth][path_option[8]][path_option[9]] and \
#            group in adcb_path_columns[depth][path_option[10]][path_option[11]] and \
#            group in bacd_path_columns[depth][path_option[12]][path_option[13]] and \
#            group in badc_path_columns[depth][path_option[14]][path_option[15]] and \
#            group in bcad_path_columns[depth][path_option[16]][path_option[17]] and \
#            group in bcda_path_columns[depth][path_option[18]][path_option[19]] and \
#            group in bdac_path_columns[depth][path_option[20]][path_option[21]] and \
#            group in bdca_path_columns[depth][path_option[22]][path_option[23]] and \
#            group in cabd_path_columns[depth][path_option[24]][path_option[25]] and \
#            group in cadb_path_columns[depth][path_option[26]][path_option[27]] and \
#            group in cbad_path_columns[depth][path_option[28]][path_option[29]] and \
#            group in cbda_path_columns[depth][path_option[30]][path_option[31]] and \
#            group in cdab_path_columns[depth][path_option[32]][path_option[33]] and \
#            group in cdba_path_columns[depth][path_option[34]][path_option[35]] and \
#            group in dabc_path_columns[depth][path_option[36]][path_option[37]] and \
#            group in dacb_path_columns[depth][path_option[38]][path_option[39]] and \
#            group in dbac_path_columns[depth][path_option[40]][path_option[41]] and \
#            group in dbca_path_columns[depth][path_option[42]][path_option[43]] and \
#            group in dcab_path_columns[depth][path_option[44]][path_option[45]] and \
#            group in dcba_path_columns[depth][path_option[46]][path_option[47]]:
#            new_tuple = (abcd_path_columns[depth][path_option[0]][path_option[1]][group][0], \
#                         abcd_path_columns[depth][path_option[0]][path_option[1]][group][1], \
#                         abdc_path_columns[depth][path_option[2]][path_option[3]][group][0], \
#                         abdc_path_columns[depth][path_option[2]][path_option[3]][group][1], \
#                         acbd_path_columns[depth][path_option[4]][path_option[5]][group][0], \
#                         acbd_path_columns[depth][path_option[4]][path_option[5]][group][1], \
#                         acdb_path_columns[depth][path_option[6]][path_option[7]][group][0], \
#                         acdb_path_columns[depth][path_option[6]][path_option[7]][group][1], \
#                         adbc_path_columns[depth][path_option[8]][path_option[9]][group][0], \
#                         adbc_path_columns[depth][path_option[8]][path_option[9]][group][1], \
#                         adcb_path_columns[depth][path_option[10]][path_option[11]][group][0], \
#                         adcb_path_columns[depth][path_option[10]][path_option[11]][group][1], \
#                         bacd_path_columns[depth][path_option[12]][path_option[13]][group][0], \
#                         bacd_path_columns[depth][path_option[12]][path_option[13]][group][1], \
#                         badc_path_columns[depth][path_option[14]][path_option[15]][group][0], \
#                         badc_path_columns[depth][path_option[14]][path_option[15]][group][1], \
#                         bcad_path_columns[depth][path_option[16]][path_option[17]][group][0], \
#                         bcad_path_columns[depth][path_option[16]][path_option[17]][group][1], \
#                         bcda_path_columns[depth][path_option[18]][path_option[19]][group][0], \
#                         bcda_path_columns[depth][path_option[18]][path_option[19]][group][1], \
#                         bdac_path_columns[depth][path_option[20]][path_option[21]][group][0], \
#                         bdac_path_columns[depth][path_option[20]][path_option[21]][group][1], \
#                         bdca_path_columns[depth][path_option[22]][path_option[23]][group][0], \
#                         bdca_path_columns[depth][path_option[22]][path_option[23]][group][1], \
#                         cabd_path_columns[depth][path_option[24]][path_option[25]][group][0], \
#                         cabd_path_columns[depth][path_option[24]][path_option[25]][group][1], \
#                         cadb_path_columns[depth][path_option[26]][path_option[27]][group][0], \
#                         cadb_path_columns[depth][path_option[26]][path_option[27]][group][1], \
#                         cbad_path_columns[depth][path_option[28]][path_option[29]][group][0], \
#                         cbad_path_columns[depth][path_option[28]][path_option[29]][group][1], \
#                         cbda_path_columns[depth][path_option[30]][path_option[31]][group][0], \
#                         cbda_path_columns[depth][path_option[30]][path_option[31]][group][1], \
#                         cdab_path_columns[depth][path_option[32]][path_option[33]][group][0], \
#                         cdab_path_columns[depth][path_option[32]][path_option[33]][group][1], \
#                         cdba_path_columns[depth][path_option[34]][path_option[35]][group][0], \
#                         cdba_path_columns[depth][path_option[34]][path_option[35]][group][1], \
#                         dabc_path_columns[depth][path_option[36]][path_option[37]][group][0], \
#                         dabc_path_columns[depth][path_option[36]][path_option[37]][group][1], \
#                         dacb_path_columns[depth][path_option[38]][path_option[39]][group][0], \
#                         dacb_path_columns[depth][path_option[38]][path_option[39]][group][1], \
#                         dbac_path_columns[depth][path_option[40]][path_option[41]][group][0], \
#                         dbac_path_columns[depth][path_option[40]][path_option[41]][group][1], \
#                         dbca_path_columns[depth][path_option[42]][path_option[43]][group][0], \
#                         dbca_path_columns[depth][path_option[42]][path_option[43]][group][1], \
#                         dcab_path_columns[depth][path_option[44]][path_option[45]][group][0], \
#                         dcab_path_columns[depth][path_option[44]][path_option[45]][group][1], \
#                         dcba_path_columns[depth][path_option[46]][path_option[47]][group][0], \
#                         dcba_path_columns[depth][path_option[46]][path_option[47]][group][1])
#            if new_tuple not in next_path_options:
#               next_path_options.append(new_tuple)
#            if path_option[0] not in new_abcd_path_columns[depth]:
#               new_abcd_path_columns[depth][path_option[0]] = {}
#            if path_option[1] not in new_abcd_path_columns[depth][path_option[0]]:
#               new_abcd_path_columns[depth][path_option[0]][path_option[1]] = {}
#            if group not in new_abcd_path_columns[depth][path_option[0]][path_option[1]]:
#               new_abcd_path_columns[depth][path_option[0]][path_option[1]][group] = abcd_path_columns[depth][path_option[0]][path_option[1]][group]
#   if depth:
#      d4_path_finder_loop_2(abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, next_path_options, depth - 1, new_abcd_path_columns)

#i = 0
#for path_column in d4_path_maker(12, 'a', 'b', 'c', 'd'):
#   print(i)
#   n = 0
#   if i == 2:
#      print(path_column)
#      for index in path_column:
#         n += index
#   print(n)
#   if i == 11:
#      print(path_column[864].keys())
#   i += 1

n = 12
path_columns = d4_path_maker(n, 'a', 'b', 'c', 'd')
print(path_columns[11][864][72])
minimums = []
maximums = []
for i in range(n):
   minimums.append(10000000)
   maximums.append(0)
def minmaxfinder(path_columns, path_options, minimums, maximums, depth):
   print(len(path_options))
   next_path_options = []
   for path_option in path_options:
      if path_option[0] > maximums[depth]:
         maximums[depth] = path_option[0]
      if path_option[0] < minimums[depth]:
         minimums[depth] = path_option[0]
      if depth:
         for group in path_columns[depth][path_option[0]][path_option[1]]:
            if path_columns[depth][path_option[0]][path_option[1]][group] not in next_path_options:
               next_path_options.append(path_columns[depth][path_option[0]][path_option[1]][group])
   if depth:
      minmaxfinder(path_columns, next_path_options, minimums, maximums, depth - 1)
minmaxfinder(path_columns, [(pow(n, 4) / math.factorial(4), pow(n, 2) / math.factorial(2))], minimums, maximums, n - 1)
print('minimums:')
print(minimums)
print('maximums:')
print(maximums)
solutions = d4_path_finder(n)

##solutions = d2_path_finder(2)
##solutions = d2_path_finder(4)
##solutions = d3_path_finder(6)
##solutions = d3_path_finder(12)
##solutions = d3_path_finder(18)
#solutions = d4_path_finder(12)
##solutions = d4_path_finder(18)
print(len(solutions))
i = 0
for solution in condenser(solutions):
   #if not checker(solution, 2, 2):
   #if not checker(solution, 2, 8):
   #if not checker(solution, 3, 36):
   #if not checker(solution, 3, 288):
   #if not checker(solution, 3, 972):
   if not checker(solution, 4, 864):
   #if not checker(solution, 4, 4374):
      print('oh no!')
   #print(solution)
   i += 1
print(i)
#print(a_global)
