#!/usr/bin/python3

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
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column.
   path_columns.append({0:[(a + c + b, 0), (c + a + b, 0), (c + b + a, 0)], n - 1:[(b + a + c, 0), (b + c + a, 0)], n:[(a + b + c, 0)]})
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
      current_path_column[path_num + addition].append((group, path_num))


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


def d4_path_maker(n, a, b, c, d): #n is for number of sides of dice
   path_columns = []
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column. 
   #the second map inside the first and the second int in the tuple are how many cd strings are downstream.
   path_columns.append({0:{0:{a + b + d + c:(0, 0), a + d + b + c: (0, 0), a + d + c + b:(0, 0), b + a + d + c:(0, 0), b + d + a + c:(0, 0), b + d + c + a:(0, 0), d + a + b + c:(0, 0), d + a + c + b:(0, 0), d + b + a + c:(0, 0), d + b + c + a:(0, 0), d + c + a + b:(0, 0), d + c + b + a:(0, 0)}, 1:{a + c + b + d:(0, 0), a + c + d + b:(0, 0), c + a + b + d:(0, 0), c + a + d + b:(0, 0), c + b + a + d:(0, 0), c + b + d + a:(0, 0), c + d + a + b:(0, 0), c + d + b + a:(0, 0)}}, n - 1:{1:{b + a + c + d:(0, 0), b + c + a + d:(0, 0), b + c + d + a:(0, 0)}}, n:{1:{a + b + c + d:(0, 0)}}})
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
   #print(share)
   return d4_path_finder_recursive(n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)

#abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], 

#cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], 

#abcd, abdc, acbd, acdb, adbc, adcb, bacd, badc, bcad, bcda, bdac, bdca, cabd, cadb, cbad, cbda, cdab, cdba, dabc, dacb, dbac, dbca, dcab, dcba, 
def d4_path_finder_recursive(n, abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share, ab_share, ac_share, ad_share, ba_share, bc_share, bd_share, ca_share, cb_share, cd_share, da_share, db_share, dc_share, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0, so_far=''):
   solutions = []
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
                                                                              solutions.append(so_far + abcd_possibility)
                                                                           else:
                                                                              solutions.extend(d4_path_finder_recursive(n, abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=depth+1, so_far=so_far + abcd_possibility))
   return solutions


#abcde
#abced
#abdce
#abdec
#abecd
#abedc
#acbde
#acbed
#acdbe
#acdeb
#acebd
#acedb
#adbce
#adbec
#adcbe
#adceb
#adebc
#adecb
#aebcd
#aebdc
#aecbd
#aecdb
#aedbc
#aedcb
#bacde
#baced
#badce
#badec
#baecd
#baedc
#bcade
#bcaed
#bcdae
#bcdea
#bcead
#bceda
#bdace
#bdaec
#bdcae
#bdcea
#bdeac
#bdeca
#beacd
#beadc
#becad
#becda
#bedac
#bedca
#cabde
#cabed
#cadbe
#cadeb
#caebd
#caedb
#cbade
#cbaed
#cbdae
#cbdea
#cbead
#cbeda
#cdabe
#cdaeb
#cdbae
#cdbea
#cdeab
#cdeba
#ceabd
#ceadb
#cebad
#cebda
#cedab
#cedba
#dabce
#dabec
#dacbe
#daceb
#daebc
#daecb
#dbace
#dbaec
#dbcae
#dbcea
#dbeac
#dbeca
#dcabe
#dcaeb
#dcbae
#dcbea
#dceab
#dceba
#deabc
#deacb
#debac
#debca
#decab
#decba
#eabcd
#eabdc
#eacbd
#eacdb
#eadbc
#eadcb
#ebacd
#ebadc
#ebcad
#ebcda
#ebdac
#ebdca
#ecabd
#ecadb
#ecbad
#ecbda
#ecdab
#ecdba
#edabc
#edacb
#edbac
#edbca
#edcab
#edcba


def d5_path_maker(n, a, b, c, d, e): #n is for number of sides of dice
   path_columns = []
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column. 
   #the second map inside the first and the second int in the tuple are how many cde strings are downstream. The third of each is de strings.
   #                    abcde
   #                    |      cde
   #                    |      |  de
   #                    |      |  |
   #path_columns.append({n:    {1:{1:{a + b + c + d + e:(0, 0, 0)}}}, \
   #                     n - 1:{1:{1:{b + a + c + d + e:(0, 0, 0), \
   #                                  b + c + a + d + e:(0, 0, 0), \
   #                                  b + c + d + a + e:(0, 0, 0), \
   #                                  b + c + d + e + a:(0, 0, 0)}}}, \
   #                     0:    {1:{1:{a + c + b + d + e:(0, 0, 0), \
   #                                  a + c + d + b + e:(0, 0, 0), \
   #                                  a + c + d + e + b:(0, 0, 0), \
   #                                  c + a + b + d + e:(0, 0, 0), \
   #                                  c + a + d + b + e:(0, 0, 0), \
   #                                  c + a + d + e + b:(0, 0, 0), \
   #                                  c + b + a + d + e:(0, 0, 0), \
   #                                  c + b + d + a + e:(0, 0, 0), \
   #                                  c + b + d + e + a:(0, 0, 0), \
   #                                  c + d + a + b + e:(0, 0, 0), \
   #                                  c + d + a + e + b:(0, 0, 0), \
   #                                  c + d + b + a + e:(0, 0, 0), \
   #                                  c + d + b + e + a:(0, 0, 0), \
   #                                  c + d + e + a + b:(0, 0, 0), \
   #                                  c + d + e + b + a:(0, 0, 0)}}, \
   #                            0:{1:{a + b + d + c + e:(0, 0, 0), \
   #                                  a + b + d + e + c:(0, 0, 0), \
   #                                  a + d + b + c + e:(0, 0, 0), \
   #                                  a + d + b + e + c:(0, 0, 0), \
   #                                  a + d + c + b + e:(0, 0, 0), \
   #                                  a + d + c + e + b:(0, 0, 0), \
   #                                  a + d + e + b + c:(0, 0, 0), \
   #                                  a + d + e + c + b:(0, 0, 0), \
   #                                  b + a + d + c + e:(0, 0, 0), \
   #                                  b + a + d + e + c:(0, 0, 0), \
   #                                  b + d + a + c + e:(0, 0, 0), \
   #                                  b + d + a + e + c:(0, 0, 0), \
   #                                  b + d + c + a + e:(0, 0, 0), \
   #                                  b + d + c + e + a:(0, 0, 0), \
   #                                  b + d + e + a + c:(0, 0, 0), \
   #                                  b + d + e + c + a:(0, 0, 0), \
   #                                  d + a + b + c + e:(0, 0, 0), \
   #                                  d + a + b + e + c:(0, 0, 0), \
   #                                  d + a + c + b + e:(0, 0, 0), \
   #                                  d + a + c + e + b:(0, 0, 0), \
   #                                  d + a + e + b + c:(0, 0, 0), \
   #                                  d + a + e + c + b:(0, 0, 0), \
   #                                  d + b + a + c + e:(0, 0, 0), \
   #                                  d + b + a + e + c:(0, 0, 0), \
   #                                  d + b + c + a + e:(0, 0, 0), \
   #                                  d + b + c + e + a:(0, 0, 0), \
   #                                  d + b + e + a + c:(0, 0, 0), \
   #                                  d + b + e + c + a:(0, 0, 0), \
   #                                  d + c + a + b + e:(0, 0, 0), \
   #                                  d + c + a + e + b:(0, 0, 0), \
   #                                  d + c + b + a + e:(0, 0, 0), \
   #                                  d + c + b + e + a:(0, 0, 0), \
   #                                  d + c + e + a + b:(0, 0, 0), \
   #                                  d + c + e + b + a:(0, 0, 0), \
   #                                  d + e + a + b + c:(0, 0, 0), \
   #                                  d + e + a + c + b:(0, 0, 0), \
   #                                  d + e + b + a + c:(0, 0, 0), \
   #                                  d + e + b + c + a:(0, 0, 0), \
   #                                  d + e + c + a + b:(0, 0, 0), \
   #                                  d + e + c + b + a:(0, 0, 0)}, \
   #                               0:{a + b + c + e + d:(0, 0, 0), \
   #                                  a + b + e + c + d:(0, 0, 0), \
   #                                  a + b + e + d + c:(0, 0, 0), \
   #                                  a + c + b + e + d:(0, 0, 0), \
   #                                  a + c + e + b + d:(0, 0, 0), \
   #                                  a + c + e + d + b:(0, 0, 0), \
   #                                  a + e + b + c + d:(0, 0, 0), \
   #                                  a + e + b + d + c:(0, 0, 0), \
   #                                  a + e + c + b + d:(0, 0, 0), \
   #                                  a + e + c + d + b:(0, 0, 0), \
   #                                  a + e + d + b + c:(0, 0, 0), \
   #                                  a + e + d + c + b:(0, 0, 0), \
   #                                  b + a + c + e + d:(0, 0, 0), \
   #                                  b + a + e + c + d:(0, 0, 0), \
   #                                  b + a + e + d + c:(0, 0, 0), \
   #                                  b + c + a + e + d:(0, 0, 0), \
   #                                  b + c + e + a + d:(0, 0, 0), \
   #                                  b + c + e + d + a:(0, 0, 0), \
   #                                  b + e + a + c + d:(0, 0, 0), \
   #                                  b + e + a + d + c:(0, 0, 0), \
   #                                  b + e + c + a + d:(0, 0, 0), \
   #                                  b + e + c + d + a:(0, 0, 0), \
   #                                  b + e + d + a + c:(0, 0, 0), \
   #                                  b + e + d + c + a:(0, 0, 0), \
   #                                  c + a + b + e + d:(0, 0, 0), \
   #                                  c + a + e + b + d:(0, 0, 0), \
   #                                  c + a + e + d + b:(0, 0, 0), \
   #                                  c + b + a + e + d:(0, 0, 0), \
   #                                  c + b + e + a + d:(0, 0, 0), \
   #                                  c + b + e + d + a:(0, 0, 0), \
   #                                  c + e + a + b + d:(0, 0, 0), \
   #                                  c + e + a + d + b:(0, 0, 0), \
   #                                  c + e + b + a + d:(0, 0, 0), \
   #                                  c + e + b + d + a:(0, 0, 0), \
   #                                  c + e + d + a + b:(0, 0, 0), \
   #                                  c + e + d + b + a:(0, 0, 0), \
   #                                  e + a + b + c + d:(0, 0, 0), \
   #                                  e + a + b + d + c:(0, 0, 0), \
   #                                  e + a + c + b + d:(0, 0, 0), \
   #                                  e + a + c + d + b:(0, 0, 0), \
   #                                  e + a + d + b + c:(0, 0, 0), \
   #                                  e + a + d + c + b:(0, 0, 0), \
   #                                  e + b + a + c + d:(0, 0, 0), \
   #                                  e + b + a + d + c:(0, 0, 0), \
   #                                  e + b + c + a + d:(0, 0, 0), \
   #                                  e + b + c + d + a:(0, 0, 0), \
   #                                  e + b + d + a + c:(0, 0, 0), \
   #                                  e + b + d + c + a:(0, 0, 0), \
   #                                  e + c + a + b + d:(0, 0, 0), \
   #                                  e + c + a + d + b:(0, 0, 0), \
   #                                  e + c + b + a + d:(0, 0, 0), \
   #                                  e + c + b + d + a:(0, 0, 0), \
   #                                  e + c + d + a + b:(0, 0, 0), \
   #                                  e + c + d + b + a:(0, 0, 0), \
   #                                  e + d + a + b + c:(0, 0, 0), \
   #                                  e + d + a + c + b:(0, 0, 0), \
   #                                  e + d + b + a + c:(0, 0, 0), \
   #                                  e + d + b + c + a:(0, 0, 0), \
   #                                  e + d + c + a + b:(0, 0, 0), \
   #                                  e + d + c + b + a:(0, 0, 0)}}}})
   path_columns.append({0:    {0:{0:{a + b + c + d + e:(0, 0, 0)}}}})
   #for i in range(n - 1):
   for i in range(n - 1):
      path_columns.append({})
      #                    group,             num_as_bcd_es,         num_as_bc,   num_as_b,    num_cd_es, num_d_es, previous_path_column, current_path_column
      d5_path_column_maker(a + b + c + d + e, (n - i - 1) * (i + 2), (n - i - 1), (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + b + c + e + d, (n - i - 1) * (i + 1), (n - i - 1), (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + b + d + c + e, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + b + d + e + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + b + e + c + d, (n - i - 1) * (i + 1), (n - i - 1), (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + b + e + d + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + b + d + e, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + b + e + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + d + b + e, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + d + e + b, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + e + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + c + e + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + b + c + e, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + b + e + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + c + b + e, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + c + e + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + e + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + d + e + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + b + c + d, (n - i - 1) * (i + 1), (n - i - 1), (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + b + d + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + c + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + c + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + d + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(a + e + d + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + c + d + e, (n - i - 2) * (i + 2), (n - i - 2), (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + c + e + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + d + c + e, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + d + e + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + e + c + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + a + e + d + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + a + d + e, (n - i - 2) * (i + 2), (n - i - 2), (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + a + e + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + d + a + e, (n - i - 2) * (i + 2), (n - i - 2), (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + d + e + a, (n - i - 2) * (i + 2), (n - i - 2), (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + e + a + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + c + e + d + a, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + a + c + e, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + a + e + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + c + a + e, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + c + e + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + e + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + d + e + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + a + c + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + a + d + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + c + a + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + c + d + a, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + d + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(b + e + d + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + b + d + e, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + b + e + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + d + b + e, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + d + e + b, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + e + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + a + e + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + a + d + e, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + a + e + d, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + d + a + e, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + d + e + a, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + e + a + d, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + b + e + d + a, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + a + b + e, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + a + e + b, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + b + a + e, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + b + e + a, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + e + a + b, 0                    , 0          , (n - i - 1), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + d + e + b + a, 0                    , 0          , (n - i - 2), (i + 2),   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + a + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + a + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + b + a + d, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + b + d + a, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + d + a + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(c + e + d + b + a, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + b + c + e, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + b + e + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + c + b + e, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + c + e + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + e + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + a + e + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + a + c + e, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + a + e + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + c + a + e, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + c + e + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + e + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + b + e + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + a + b + e, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + a + e + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + b + a + e, 0                    , 0          , (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + b + e + a, 0                    , 0          , (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + e + a + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + c + e + b + a, 0                    , 0          , (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + a + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + a + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + b + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + b + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + c + a + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(d + e + c + b + a, 0                    , 0          , (n - i - 2), 0      ,   (i + 2),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + b + c + d, (n - i - 1) * (i + 1), (n - i - 1), (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + b + d + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + c + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + c + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + d + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + a + d + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + a + c + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + a + d + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + c + a + d, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + c + d + a, (n - i - 2) * (i + 1), (n - i - 2), (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + d + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + b + d + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + a + b + d, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + a + d + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + b + a + d, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + b + d + a, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + d + a + b, 0                    , 0          , (n - i - 1), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + c + d + b + a, 0                    , 0          , (n - i - 2), (i + 1),   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + a + b + c, 0                    , (n - i - 1), (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + a + c + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + b + a + c, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + b + c + a, 0                    , (n - i - 2), (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + c + a + b, 0                    , 0          , (n - i - 1), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
      d5_path_column_maker(e + d + c + b + a, 0                    , 0          , (n - i - 2), 0      ,   (i + 1),  path_columns[i],      path_columns[i + 1])
   return path_columns

def d5_path_column_maker(group, num_as_bcd_es, num_as_bc, num_as_b, num_cd_es, num_d_es, previous_path_column, current_path_column):
   for path_num in previous_path_column:
      for path_cde_num in previous_path_column[path_num]:
         for path_de_num in previous_path_column[path_num][path_cde_num]:
            total = path_num + (num_as_b * path_cde_num) + (num_as_bc * path_de_num) + num_as_bcd_es
            so_far_cde = path_cde_num + path_de_num + num_cd_es
            so_far_de = path_de_num + num_d_es
            if total not in current_path_column:
               current_path_column[total] = {}
            if so_far_cde not in current_path_column[total]:
               current_path_column[total][so_far_cde] = {}
            if so_far_de not in current_path_column[total][so_far_cde]:
               current_path_column[total][so_far_cde][so_far_de] = {}
            if group in current_path_column[total][so_far_cde][so_far_de]:
               print('uh oh')
               print(current_path_column[total][so_far_cde][so_far_de][group])
               print(group)
               print(total)
               print(so_far_cde)
               print(so_far_de)
               print('old:')
               print(path_num)
               print(path_cde_num)
               print(path_de_num)
            current_path_column[total][so_far_cde][so_far_de][group] = (path_num, path_cde_num, path_de_num)


def d5_path_finder(n):
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
   return d4_path_finder_recursive(n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns)

def d5_path_finder_recursive(n, abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share, ab_share, ac_share, ad_share, ba_share, bc_share, bd_share, ca_share, cb_share, cd_share, da_share, db_share, dc_share, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0, so_far=''):
   solutions = []
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
                                                                              solutions.append(so_far + abcd_possibility)
                                                                           else:
                                                                              solutions.extend(d4_path_finder_recursive(n, abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=depth+1, so_far=so_far + abcd_possibility))
   return solutions


#i = 0
#for path_column in d3_path_maker(12, 'a', 'b', 'c'):
#   print(i)
#   n = 0
#   for num_abc in path_column:
#      n += len(path_column[num_abc])
#   print(n)
#   #print(path_column)
#   i += 1

n = 6
abc_path_columns = d3_path_maker(n, 'a', 'b', 'c')
acb_path_columns = d3_path_maker(n, 'a', 'c', 'b')
bac_path_columns = d3_path_maker(n, 'b', 'a', 'c')
bca_path_columns = d3_path_maker(n, 'b', 'c', 'a')
cab_path_columns = d3_path_maker(n, 'c', 'a', 'b')
cba_path_columns = d3_path_maker(n, 'c', 'b', 'a')
solutions = d3_path_finder(n)


print('solution,permutation,col5,col4,col3,col2,col1,col0')
for solution in solutions:
   #print(solution)
   #print('   abc:')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',abc'), end='')
   for i in range(n):
      #print('      column ' + str(n - 1 - i) + ': ' + str(share))
      print(',' + str(share), end='')
      for maybe_answer in abc_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',acb'), end='')
   for i in range(n):
      print(',' + str(share), end='')
      for maybe_answer in acb_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',bac'), end='')
   for i in range(n):
      print(',' + str(share), end='')
      for maybe_answer in bac_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',bca'), end='')
   for i in range(n):
      print(',' + str(share), end='')
      for maybe_answer in bca_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',cab'), end='')
   for i in range(n):
      print(',' + str(share), end='')
      for maybe_answer in cab_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')
   share = pow(n, 3) / math.factorial(3)
   print((solution + ',cba'), end='')
   for i in range(n):
      print(',' + str(share), end='')
      for maybe_answer in cba_path_columns[n - i - 1][share]:
         if maybe_answer[0] == solution[i * 3:(i * 3) + 3]:
            share = maybe_answer[1]
   print('')

#i = 0
#for path_column in d4_path_maker(12, 'a', 'b', 'c', 'd'):
#   print(i)
#   #n = 0
#   for num_abcd in path_column:
#      j = 0
#      for num_cd in path_column[num_abcd]:
#         #n += len(path_column[num_abcd][num_cd])
#         j += len(path_column[num_abcd][num_cd])
#      print('has ' + str(j) + ' ' + str(num_abcd) + "'s")
#   #print(n)
#   print(path_column)
#   i += 1

#i = 0
#for path_column in d5_path_maker(6, 'a', 'b', 'c', 'd', 'e'):
#   print(i)
#   #n = 0
#   for num_abcde in path_column:
#      j = 0
#      for num_cde in path_column[num_abcde]:
#         for num_de in path_column[num_abcde][num_cde]:
#            #n += len(path_column[num_abcde][num_cde][num_de])
#            j += len(path_column[num_abcde][num_cde][num_de])
#      print('has ' + str(j) + ' ' + str(num_abcde) + "'s")
#   #print(n)
#   #print(path_column)
#   i += 1

#print(d5_path_maker(30, 'a', 'b', 'c', 'd', 'e')[29][202500][4500][450])
#print(d5_path_maker(2, 'a', 'b', 'c', 'd', 'e')[1])

#count = {"" : 1}
#for c in 'aaaaaaaaaaaabcd':
#   for k in count.keys():
#      if k.count(c)==0:
#         k2 = k + c
#         count[k2] = count.get(k2,0) + count[k]
#print(count)


#solutions = d4_path_finder(12)
#print(len(solutions))
#for solution in condenser(solutions):
#   if not checker(solution, 4, 864):
#      print('oh no!')
#   print(solution)
