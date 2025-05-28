#!/usr/bin/python2.7

import math, argparse

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


def get_d4_perm3_list(d4_perm3_path):
   d4_perm3_list = []
   with open(d4_perm3_path, 'r') as d4_perm3_file:
      d4_perm3_list = d4_perm3_file.read().splitlines()
   return d4_perm3_list


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


def d4_path_finder(d4_perm3_list, n):
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
   solutions = []
   for d4_perm3 in d4_perm3_list:
      if d4_path_finder_recursive(d4_perm3, n, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns):
         solutions.append(d4_perm3)
   return solutions

#abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], 

#cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], 

#abcd, abdc, acbd, acdb, adbc, adcb, bacd, badc, bcad, bcda, bdac, bdca, cabd, cadb, cbad, cbda, cdab, cdba, dabc, dacb, dbac, dbca, dcab, dcba, 
def d4_path_finder_recursive(d4_perm3, n, abcd_share, abdc_share, acbd_share, acdb_share, adbc_share, adcb_share, bacd_share, badc_share, bcad_share, bcda_share, bdac_share, bdca_share, cabd_share, cadb_share, cbad_share, cbda_share, cdab_share, cdba_share, dabc_share, dacb_share, dbac_share, dbca_share, dcab_share, dcba_share, ab_share, ac_share, ad_share, ba_share, bc_share, bd_share, ca_share, cb_share, cd_share, da_share, db_share, dc_share, abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=0):
   solution = False
   abcd_possibility = d4_perm3[depth * 4:(depth * 4) + 4]
   if abcd_possibility in abcd_path_columns[n - depth - 1][abcd_share][cd_share]:
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
                                                                              solution = True
                                                                           else:
                                                                              solution = d4_path_finder_recursive(d4_perm3, n, abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][0], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][0], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][0], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][0], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][0], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][0], bacd_path_columns[n - depth - 1][bacd_share][cd_share][abcd_possibility][0], badc_path_columns[n - depth - 1][badc_share][dc_share][abcd_possibility][0], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][0], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][0], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][0], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][0], cabd_path_columns[n - depth - 1][cabd_share][bd_share][abcd_possibility][0], cadb_path_columns[n - depth - 1][cadb_share][db_share][abcd_possibility][0], cbad_path_columns[n - depth - 1][cbad_share][ad_share][abcd_possibility][0], cbda_path_columns[n - depth - 1][cbda_share][da_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][0], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][0], dabc_path_columns[n - depth - 1][dabc_share][bc_share][abcd_possibility][0], dacb_path_columns[n - depth - 1][dacb_share][cb_share][abcd_possibility][0], dbac_path_columns[n - depth - 1][dbac_share][ac_share][abcd_possibility][0], dbca_path_columns[n - depth - 1][dbca_share][ca_share][abcd_possibility][0], dcab_path_columns[n - depth - 1][dcab_share][ab_share][abcd_possibility][0], dcba_path_columns[n - depth - 1][dcba_share][ba_share][abcd_possibility][0], cdab_path_columns[n - depth - 1][cdab_share][ab_share][abcd_possibility][1], bdac_path_columns[n - depth - 1][bdac_share][ac_share][abcd_possibility][1], bcad_path_columns[n - depth - 1][bcad_share][ad_share][abcd_possibility][1], cdba_path_columns[n - depth - 1][cdba_share][ba_share][abcd_possibility][1], adbc_path_columns[n - depth - 1][adbc_share][bc_share][abcd_possibility][1], acbd_path_columns[n - depth - 1][acbd_share][bd_share][abcd_possibility][1], bdca_path_columns[n - depth - 1][bdca_share][ca_share][abcd_possibility][1], adcb_path_columns[n - depth - 1][adcb_share][cb_share][abcd_possibility][1], abcd_path_columns[n - depth - 1][abcd_share][cd_share][abcd_possibility][1], bcda_path_columns[n - depth - 1][bcda_share][da_share][abcd_possibility][1], acdb_path_columns[n - depth - 1][acdb_share][db_share][abcd_possibility][1], abdc_path_columns[n - depth - 1][abdc_share][dc_share][abcd_possibility][1], abcd_path_columns, abdc_path_columns, acbd_path_columns, acdb_path_columns, adbc_path_columns, adcb_path_columns, bacd_path_columns, badc_path_columns, bcad_path_columns, bcda_path_columns, bdac_path_columns, bdca_path_columns, cabd_path_columns, cadb_path_columns, cbad_path_columns, cbda_path_columns, cdab_path_columns, cdba_path_columns, dabc_path_columns, dacb_path_columns, dbac_path_columns, dbca_path_columns, dcab_path_columns, dcba_path_columns, depth=depth+1)
   return solution


parser = argparse.ArgumentParser()
parser.add_argument('d4_perm3_path')
parser.add_argument('n')
args = parser.parse_args()

n = int(args.n)
d4_perm3_list = get_d4_perm3_list(args.d4_perm3_path)


solutions = d4_path_finder(d4_perm3_list, n)
share = pow(n, 4) / math.factorial(4)
print(len(solutions))
i = 0
#for solution in condenser(solutions):
for solution in solutions:
   if not checker(solution, 4, share):
      print('oh no!')
   print(solution)
   i += 1
print(i)
