#!/usr/bin/python2.7

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

def reverse(s):
   name_map = {}
   reverse = ""
   length = len(s)
   for i in range(length):
      if s[length - i - 1] not in name_map:
         name_map[s[length - i - 1]] = s[i]
      reverse += name_map[s[length - i - 1]]
   return reverse

def condenser(all_sets):
   set_condenser = {}
   for s in all_sets:
      if s not in set_condenser:
         set_condenser[s] = s
         set_condenser[reverse(s)] = s
   condensed = []
   for s in set_condenser.values():
      if s not in condensed:
         condensed.append(s)
   return condensed


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
   path_columns.append({0:[(a + c + b, 0, 1), (c + a + b, 0, 1), (c + b + a, 0, 1)], n - 1:[(b + a + c, 0, 1), (b + c + a, 0, 1)], n:[(a + b + c, 0, 1)]})
   for i in range(n - 1):
      path_columns.append({})
      d3_path_column_maker(a + b + c, (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1])
      d3_path_column_maker(a + c + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1])
      d3_path_column_maker(b + a + c, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1])
      d3_path_column_maker(b + c + a, (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1])
      d3_path_column_maker(c + a + b, (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1])
      d3_path_column_maker(c + b + a, (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
   return path_columns

def d3_path_column_maker(group, addition, previous_path_column, current_path_column):
   for path_num in previous_path_column:
      if path_num + addition not in current_path_column:
         current_path_column[path_num + addition] = []
      num_options = 0
      for option in previous_path_column[path_num]:
         num_options += option[2]
      current_path_column[path_num + addition].append((group, path_num, num_options))


def d3_path_finder(n):
   abc_path_columns = d3_path_maker(n, 'a', 'b', 'c')
   acb_path_columns = d3_path_maker(n, 'a', 'c', 'b')
   bac_path_columns = d3_path_maker(n, 'b', 'a', 'c')
   bca_path_columns = d3_path_maker(n, 'b', 'c', 'a')
   cab_path_columns = d3_path_maker(n, 'c', 'a', 'b')
   cba_path_columns = d3_path_maker(n, 'c', 'b', 'a')
   share = pow(n, 3) / math.factorial(3)
   #print(share)
   return d3_path_finder_recursive(n, share, share, share, share, share, share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns)

def d3_path_finder_recursive(n, abc_share, acb_share, bac_share, bca_share, cab_share, cba_share, abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=0, so_far=''):
   solution = None
   options = {}
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
                                       solution = so_far + abc_possibility[0]
                                    else:
                                       options[(abc_possibility[2] + acb_possibility[2] + bac_possibility[2] + bca_possibility[2] + cab_possibility[2] + cba_possibility[2]) / 6.0] = [abc_possibility[1], acb_possibility[1], bac_possibility[1], bca_possibility[1], cab_possibility[1], cba_possibility[1], so_far + abc_possibility[0]]
   if solution:
      return solution
   sorted_options = sorted(options.keys())
   for i in range(len(sorted_options) - 1, -1, -1):
      print(depth)
      print(sorted_options[i])
      solution = d3_path_finder_recursive(n, options[sorted_options[i]][0], options[sorted_options[i]][1], options[sorted_options[i]][2], options[sorted_options[i]][3], options[sorted_options[i]][4], options[sorted_options[i]][5], abc_path_columns, acb_path_columns, bac_path_columns, bca_path_columns, cab_path_columns, cba_path_columns, depth=depth+1, so_far=options[sorted_options[i]][6])
      if solution:
         return solution
   return solution


def d4_path_maker(n, a, b, c, d): #n is for number of sides of dice
   path_columns = []
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column.
   #the second map inside the first and the second int in the tuple are how many cd strings are downstream.
   path_columns.append({0:{0:{a + b + d + c:(0, 0, 1), a + d + b + c: (0, 0, 1), a + d + c + b:(0, 0, 1), b + a + d + c:(0, 0, 1), b + d + a + c:(0, 0, 1), b + d + c + a:(0, 0, 1), d + a + b + c:(0, 0, 1), d + a + c + b:(0, 0, 1), d + b + a + c:(0, 0, 1), d + b + c + a:(0, 0, 1), d + c + a + b:(0, 0, 1), d + c + b + a:(0, 0, 1)}, 1:{a + c + b + d:(0, 0, 1), a + c + d + b:(0, 0, 1), c + a + b + d:(0, 0, 1), c + a + d + b:(0, 0, 1), c + b + a + d:(0, 0, 1), c + b + d + a:(0, 0, 1), c + d + a + b:(0, 0, 1), c + d + b + a:(0, 0, 1)}}, n - 1:{1:{b + a + c + d:(0, 0, 1), b + c + a + d:(0, 0, 1), b + c + d + a:(0, 0, 1)}}, n:{1:{a + b + c + d:(0, 0, 1)}}})
   for i in range(n - 1):
      path_columns.append({})
      d4_path_column_maker(a + b + c + d, (n - i - 1), (i + 2), (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(a + b + d + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(a + c + b + d, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(a + c + d + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(a + d + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(a + d + c + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + a + c + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + a + d + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + c + a + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + c + d + a, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + d + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(b + d + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + a + b + d, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + a + d + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + b + a + d, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + b + d + a, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + d + a + b, (n - i - 1), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(c + d + b + a, (n - i - 2), (i + 2), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + a + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + a + c + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + b + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + b + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + c + a + b, (n - i - 1), (i + 1), 0, path_columns[i], path_columns[i + 1])
      d4_path_column_maker(d + c + b + a, (n - i - 2), (i + 1), 0, path_columns[i], path_columns[i + 1])
   return path_columns

def d4_path_column_maker(group, num_abs, add_cds, addition, previous_path_column, current_path_column):
   for path_num in previous_path_column:
      for path_cd_num in previous_path_column[path_num]:
         if path_num + addition + (num_abs * path_cd_num) not in current_path_column:
            current_path_column[path_num + addition + (num_abs * path_cd_num)] = {}
         if path_cd_num + add_cds not in current_path_column[path_num + addition + (num_abs * path_cd_num)]:
            current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds] = {}
         if group in current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds]:
            print('uh oh')
         num_options = 0
         for egroup in previous_path_column[path_num][path_cd_num]:
            num_options += previous_path_column[path_num][path_cd_num][egroup][2]
         current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds][group] = (path_num, path_cd_num, num_options)


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
   #print(share)
   return ""
   return d4_path_finder_recursive(n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)

def d4_path_finder_recursive(n, abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share, ab_share, ac_share, ad_share, ba_share, bc_share, bd_share, ca_share, cb_share, cd_share, da_share, db_share, dc_share, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0, so_far=''):
   solution = None
   options = {}
   for abcd_possibility in abcd_path_columns[n - depth - 1][abcd_share][cd_share]:
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
                                                                              solution = so_far + abcd_possibility
                                                                           else:
                                                                              av = (abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][2] + abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][2] + acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][2] + acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][2] + adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][2] + adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][2] + bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][2] + badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][2] + bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][2] + bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][2] + bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][2] + bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][2] + cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][2] + cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][2] + cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][2] + cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][2] + cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][2] + cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][2] + dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][2] + dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][2] + dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][2] + dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][2] + dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][2] + dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][2]) / 24.0
                                                                              options[av] = [abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], so_far + abcd_possibility]
   if solution:
      return solution
   sorted_options = sorted(options.keys())
   for i in range(len(sorted_options) - 1, -1, -1):
      print(depth)
      print(sorted_options[i])
      solution = d4_path_finder_recursive(n, options[sorted_options[i]][0], options[sorted_options[i]][1], options[sorted_options[i]][2], options[sorted_options[i]][3], options[sorted_options[i]][4], options[sorted_options[i]][5], options[sorted_options[i]][6], options[sorted_options[i]][7], options[sorted_options[i]][8], options[sorted_options[i]][9], options[sorted_options[i]][10], options[sorted_options[i]][11], options[sorted_options[i]][12], options[sorted_options[i]][13], options[sorted_options[i]][14], options[sorted_options[i]][15], options[sorted_options[i]][16], options[sorted_options[i]][17], options[sorted_options[i]][18], options[sorted_options[i]][19], options[sorted_options[i]][20], options[sorted_options[i]][21], options[sorted_options[i]][22], options[sorted_options[i]][23], options[sorted_options[i]][24], options[sorted_options[i]][25], options[sorted_options[i]][26], options[sorted_options[i]][27], options[sorted_options[i]][28], options[sorted_options[i]][29], options[sorted_options[i]][30], options[sorted_options[i]][31], options[sorted_options[i]][32], options[sorted_options[i]][33], options[sorted_options[i]][34], options[sorted_options[i]][35], abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=depth+1, so_far=options[sorted_options[i]][36])
      if solution:
         return solution
   return solution


d = 4
n = 18
share = pow(n, d) / math.factorial(d)
if d == 3:
   solution = d3_path_finder(n)
elif d == 4:
   solution = d4_path_finder(n)
if not checker(solution, d, share):
   print('oh no!')
print(solution)
