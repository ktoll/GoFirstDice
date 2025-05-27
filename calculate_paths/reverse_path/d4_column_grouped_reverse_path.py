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
   path_lengths = []
   #these tuples point to the map value of the previous column, in this case, all 0 because there isn't a previous column. 
   #the second map inside the first and the second int in the tuple are how many cd strings are downstream.
   path_columns.append({0:{0:{a + b + d + c:(0, 0), a + d + b + c: (0, 0), a + d + c + b:(0, 0), b + a + d + c:(0, 0), b + d + a + c:(0, 0), b + d + c + a:(0, 0), d + a + b + c:(0, 0), d + a + c + b:(0, 0), d + b + a + c:(0, 0), d + b + c + a:(0, 0), d + c + a + b:(0, 0), d + c + b + a:(0, 0)}, 1:{a + c + b + d:(0, 0), a + c + d + b:(0, 0), c + a + b + d:(0, 0), c + a + d + b:(0, 0), c + b + a + d:(0, 0), c + b + d + a:(0, 0), c + d + a + b:(0, 0), c + d + b + a:(0, 0)}}, n - 1:{1:{b + a + c + d:(0, 0), b + c + a + d:(0, 0), b + c + d + a:(0, 0)}}, n:{1:{a + b + c + d:(0, 0)}}})
   path_lengths.append({0:{0:12, 1:8}, n - 1:{1:3}, n:{1:1}})
   for i in range(n - 1):
      path_columns.append({})
      path_lengths.append({})
      d4_path_column_maker(a + b + c + d, (n - i - 1), (i + 2), (n - i - 1) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(a + b + d + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(a + c + b + d, (n - i - 1), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(a + c + d + b, (n - i - 1), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(a + d + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(a + d + c + b, (n - i - 1), (i + 1), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + a + c + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + a + d + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + c + a + d, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + c + d + a, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + d + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(b + d + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + a + b + d, (n - i - 1), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + a + d + b, (n - i - 1), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + b + a + d, (n - i - 2), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + b + d + a, (n - i - 2), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + d + a + b, (n - i - 1), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(c + d + b + a, (n - i - 2), (i + 2), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + a + b + c, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + a + c + b, (n - i - 1), (i + 1), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + b + a + c, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + b + c + a, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + c + a + b, (n - i - 1), (i + 1), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
      d4_path_column_maker(d + c + b + a, (n - i - 2), (i + 1), 0                    , path_columns[i], path_columns[i + 1], path_lengths[i], path_lengths[i + 1])
   return path_columns, path_lengths

def d4_path_column_maker(group, num_abs, add_cds, addition, previous_path_column, current_path_column, previous_path_length, current_path_length):
   for path_num in previous_path_column:
      for path_cd_num in previous_path_column[path_num]:
         if path_num + addition + (num_abs * path_cd_num) not in current_path_column:
            current_path_column[path_num + addition + (num_abs * path_cd_num)] = {}
         if path_num + addition + (num_abs * path_cd_num) not in current_path_length:
            current_path_length[path_num + addition + (num_abs * path_cd_num)] = {}
         if path_cd_num + add_cds not in current_path_column[path_num + addition + (num_abs * path_cd_num)]:
            current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds] = {}
         if path_cd_num + add_cds not in current_path_length[path_num + addition + (num_abs * path_cd_num)]:
            current_path_length[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds] = 0
         if group in current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds]:
            print('uh oh')
         current_path_column[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds][group] = (path_num, path_cd_num)
         current_path_length[path_num + addition + (num_abs * path_cd_num)][path_cd_num + add_cds] += previous_path_length[path_num][path_cd_num]


def d4_path_finder_maker_reverse(n):
   share = pow(n, 4) / math.factorial(4)
   share_cd = pow(n, 2) / math.factorial(2)
   abcd_path_columns, abcd_path_lengths = d4_path_maker(n, 'a', 'b', 'c', 'd')
   print(abcd_path_lengths[n - 1][share][share_cd])
   abdc_path_columns, abdc_path_lengths = d4_path_maker(n, 'a', 'b', 'd', 'c')
   acbd_path_columns, acbd_path_lengths = d4_path_maker(n, 'a', 'c', 'b', 'd')
   acdb_path_columns, acdb_path_lengths = d4_path_maker(n, 'a', 'c', 'd', 'b')
   adbc_path_columns, adbc_path_lengths = d4_path_maker(n, 'a', 'd', 'b', 'c')
   adcb_path_columns, adcb_path_lengths = d4_path_maker(n, 'a', 'd', 'c', 'b')
   bacd_path_columns, bacd_path_lengths = d4_path_maker(n, 'b', 'a', 'c', 'd')
   badc_path_columns, badc_path_lengths = d4_path_maker(n, 'b', 'a', 'd', 'c')
   bcad_path_columns, bcad_path_lengths = d4_path_maker(n, 'b', 'c', 'a', 'd')
   bcda_path_columns, bcda_path_lengths = d4_path_maker(n, 'b', 'c', 'd', 'a')
   bdac_path_columns, bdac_path_lengths = d4_path_maker(n, 'b', 'd', 'a', 'c')
   bdca_path_columns, bdca_path_lengths = d4_path_maker(n, 'b', 'd', 'c', 'a')
   cabd_path_columns, cabd_path_lengths = d4_path_maker(n, 'c', 'a', 'b', 'd')
   cadb_path_columns, cadb_path_lengths = d4_path_maker(n, 'c', 'a', 'd', 'b')
   cbad_path_columns, cbad_path_lengths = d4_path_maker(n, 'c', 'b', 'a', 'd')
   cbda_path_columns, cbda_path_lengths = d4_path_maker(n, 'c', 'b', 'd', 'a')
   cdab_path_columns, cdab_path_lengths = d4_path_maker(n, 'c', 'd', 'a', 'b')
   cdba_path_columns, cdba_path_lengths = d4_path_maker(n, 'c', 'd', 'b', 'a')
   dabc_path_columns, dabc_path_lengths = d4_path_maker(n, 'd', 'a', 'b', 'c')
   dacb_path_columns, dacb_path_lengths = d4_path_maker(n, 'd', 'a', 'c', 'b')
   dbac_path_columns, dbac_path_lengths = d4_path_maker(n, 'd', 'b', 'a', 'c')
   dbca_path_columns, dbca_path_lengths = d4_path_maker(n, 'd', 'b', 'c', 'a')
   dcab_path_columns, dcab_path_lengths = d4_path_maker(n, 'd', 'c', 'a', 'b')
   dcba_path_columns, dcba_path_lengths = d4_path_maker(n, 'd', 'c', 'b', 'a')
   reverse_path_columns = []
   for i in range(n):
      reverse_path_columns.append({})
   abcd_init = abcd_path_columns[n - 1][share][share_cd]['abcd'][0]
   abdc_init = abdc_path_columns[n - 1][share][share_cd]['abcd'][0]
   acbd_init = acbd_path_columns[n - 1][share][share_cd]['abcd'][0]
   acdb_init = acdb_path_columns[n - 1][share][share_cd]['abcd'][0]
   adbc_init = adbc_path_columns[n - 1][share][share_cd]['abcd'][0]
   adcb_init = adcb_path_columns[n - 1][share][share_cd]['abcd'][0]
   bacd_init = bacd_path_columns[n - 1][share][share_cd]['abcd'][0]
   badc_init = badc_path_columns[n - 1][share][share_cd]['abcd'][0]
   bcad_init = bcad_path_columns[n - 1][share][share_cd]['abcd'][0]
   bcda_init = bcda_path_columns[n - 1][share][share_cd]['abcd'][0]
   bdac_init = bdac_path_columns[n - 1][share][share_cd]['abcd'][0]
   bdca_init = bdca_path_columns[n - 1][share][share_cd]['abcd'][0]
   cabd_init = cabd_path_columns[n - 1][share][share_cd]['abcd'][0]
   cadb_init = cadb_path_columns[n - 1][share][share_cd]['abcd'][0]
   cbad_init = cbad_path_columns[n - 1][share][share_cd]['abcd'][0]
   cbda_init = cbda_path_columns[n - 1][share][share_cd]['abcd'][0]
   cdab_init = cdab_path_columns[n - 1][share][share_cd]['abcd'][0]
   cdba_init = cdba_path_columns[n - 1][share][share_cd]['abcd'][0]
   dabc_init = dabc_path_columns[n - 1][share][share_cd]['abcd'][0]
   dacb_init = dacb_path_columns[n - 1][share][share_cd]['abcd'][0]
   dbac_init = dbac_path_columns[n - 1][share][share_cd]['abcd'][0]
   dbca_init = dbca_path_columns[n - 1][share][share_cd]['abcd'][0]
   dcab_init = dcab_path_columns[n - 1][share][share_cd]['abcd'][0]
   dcba_init = dcba_path_columns[n - 1][share][share_cd]['abcd'][0]
   cd_init = abcd_path_columns[n - 1][share][share_cd]['abcd'][1]
   dc_init = abdc_path_columns[n - 1][share][share_cd]['abcd'][1]
   bd_init = acbd_path_columns[n - 1][share][share_cd]['abcd'][1]
   db_init = acdb_path_columns[n - 1][share][share_cd]['abcd'][1]
   bc_init = adbc_path_columns[n - 1][share][share_cd]['abcd'][1]
   cb_init = adcb_path_columns[n - 1][share][share_cd]['abcd'][1]
   ad_init = bcad_path_columns[n - 1][share][share_cd]['abcd'][1]
   da_init = bcda_path_columns[n - 1][share][share_cd]['abcd'][1]
   ac_init = bdac_path_columns[n - 1][share][share_cd]['abcd'][1]
   ca_init = bdca_path_columns[n - 1][share][share_cd]['abcd'][1]
   ab_init = cdab_path_columns[n - 1][share][share_cd]['abcd'][1]
   ba_init = cdba_path_columns[n - 1][share][share_cd]['abcd'][1]
   init = (abcd_init, abdc_init, acbd_init, acdb_init, adbc_init, adcb_init, bacd_init, badc_init, bcad_init, bcda_init, bdac_init, bdca_init, cabd_init, cadb_init, cbad_init, cbda_init, cdab_init, cdba_init, dabc_init, dacb_init, dbac_init, dbca_init, dcab_init, dcba_init, ab_init, ac_init, ad_init, ba_init, bc_init, bd_init, ca_init, cb_init, cd_init, da_init, db_init, dc_init)
   cheatsheet = {'abcd':0, 'abdc':1, 'acbd':2, 'acdb':3, 'adbc':4, 'adcb':5, 'bacd':6, 'badc':7, 'bcad':8, 'bcda':9, 'bdac':10, 'bdca':11, 'cabd':12, 'cadb':13, 'cbad':14, 'cbda':15, 'cdab':16, 'cdba':17, 'dabc':18, 'dacb':19, 'dbac':20, 'dbca':21, 'dcab':22, 'dcba':23, 'ab':24, 'ac':25, 'ad':26, 'ba':27, 'bc':28, 'bd':29, 'ca':30, 'cb':31, 'cd':32, 'da':33, 'db':34, 'dc':35}
   reverse_path_columns[n - 1][init] = {}
   reverse_path_columns[n - 1][init]['abcd'] = (share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd)
   for i in range(n - 2, -1, -1):
      d4_reverse_path_column_maker(abcd_path_columns[i], abdc_path_columns[i], acbd_path_columns[i], acdb_path_columns[i], adbc_path_columns[i], adcb_path_columns[i], bacd_path_columns[i], badc_path_columns[i], bcad_path_columns[i], bcda_path_columns[i], bdac_path_columns[i], bdca_path_columns[i], cabd_path_columns[i], cadb_path_columns[i], cbad_path_columns[i], cbda_path_columns[i], cdab_path_columns[i], cdba_path_columns[i], dabc_path_columns[i], dacb_path_columns[i], dbac_path_columns[i], dbca_path_columns[i], dcab_path_columns[i], dcba_path_columns[i], reverse_path_columns[i + 1], reverse_path_columns[i], cheatsheet)
   return reverse_path_columns

def d4_reverse_path_column_maker(abcd_path_column, abdc_path_column, acbd_path_column, acdb_path_column, adbc_path_column, adcb_path_column, bacd_path_column, badc_path_column, bcad_path_column, bcda_path_column, bdac_path_column, bdca_path_column, cabd_path_column, cadb_path_column, cbad_path_column, cbda_path_column, cdab_path_column, cdba_path_column, dabc_path_column, dacb_path_column, dbac_path_column, dbca_path_column, dcab_path_column, dcba_path_column, previous_reverse_path_column, current_reverse_path_column, cheatsheet):
   for previous in previous_reverse_path_column:
      for group in abcd_path_column[previous[cheatsheet['abcd']]][previous[cheatsheet['cd']]]:
         if group in abdc_path_column[previous[cheatsheet['abdc']]][previous[cheatsheet['dc']]] and group in acbd_path_column[previous[cheatsheet['acbd']]][previous[cheatsheet['bd']]] and group in acdb_path_column[previous[cheatsheet['acdb']]][previous[cheatsheet['db']]] and group in adbc_path_column[previous[cheatsheet['adbc']]][previous[cheatsheet['bc']]] and group in adcb_path_column[previous[cheatsheet['adcb']]][previous[cheatsheet['cb']]] and group in bacd_path_column[previous[cheatsheet['bacd']]][previous[cheatsheet['cd']]] and group in badc_path_column[previous[cheatsheet['badc']]][previous[cheatsheet['dc']]] and group in bcad_path_column[previous[cheatsheet['bcad']]][previous[cheatsheet['ad']]] and group in bcda_path_column[previous[cheatsheet['bcda']]][previous[cheatsheet['da']]] and group in bdac_path_column[previous[cheatsheet['bdac']]][previous[cheatsheet['ac']]] and group in bdca_path_column[previous[cheatsheet['bdca']]][previous[cheatsheet['ca']]] and group in cabd_path_column[previous[cheatsheet['cabd']]][previous[cheatsheet['bd']]] and group in cadb_path_column[previous[cheatsheet['cadb']]][previous[cheatsheet['db']]] and group in cbad_path_column[previous[cheatsheet['cbad']]][previous[cheatsheet['ad']]] and group in cbda_path_column[previous[cheatsheet['cbda']]][previous[cheatsheet['da']]] and group in cdab_path_column[previous[cheatsheet['cdab']]][previous[cheatsheet['ab']]] and group in cdba_path_column[previous[cheatsheet['cdba']]][previous[cheatsheet['ba']]] and group in dabc_path_column[previous[cheatsheet['dabc']]][previous[cheatsheet['bc']]] and group in dacb_path_column[previous[cheatsheet['dacb']]][previous[cheatsheet['cb']]] and group in dbac_path_column[previous[cheatsheet['dbac']]][previous[cheatsheet['ac']]] and group in dbca_path_column[previous[cheatsheet['dbca']]][previous[cheatsheet['ca']]] and group in dcab_path_column[previous[cheatsheet['dcab']]][previous[cheatsheet['ab']]] and group in dcba_path_column[previous[cheatsheet['dcba']]][previous[cheatsheet['ba']]]:
            current = (abcd_path_column[previous[cheatsheet['abcd']]][previous[cheatsheet['cd']]][group][0], abdc_path_column[previous[cheatsheet['abdc']]][previous[cheatsheet['dc']]][group][0], acbd_path_column[previous[cheatsheet['acbd']]][previous[cheatsheet['bd']]][group][0], acdb_path_column[previous[cheatsheet['acdb']]][previous[cheatsheet['db']]][group][0], adbc_path_column[previous[cheatsheet['adbc']]][previous[cheatsheet['bc']]][group][0], adcb_path_column[previous[cheatsheet['adcb']]][previous[cheatsheet['cb']]][group][0], bacd_path_column[previous[cheatsheet['bacd']]][previous[cheatsheet['cd']]][group][0], badc_path_column[previous[cheatsheet['badc']]][previous[cheatsheet['dc']]][group][0], bcad_path_column[previous[cheatsheet['bcad']]][previous[cheatsheet['ad']]][group][0], bcda_path_column[previous[cheatsheet['bcda']]][previous[cheatsheet['da']]][group][0], bdac_path_column[previous[cheatsheet['bdac']]][previous[cheatsheet['ac']]][group][0], bdca_path_column[previous[cheatsheet['bdca']]][previous[cheatsheet['ca']]][group][0], cabd_path_column[previous[cheatsheet['cabd']]][previous[cheatsheet['bd']]][group][0], cadb_path_column[previous[cheatsheet['cadb']]][previous[cheatsheet['db']]][group][0], cbad_path_column[previous[cheatsheet['cbad']]][previous[cheatsheet['ad']]][group][0], cbda_path_column[previous[cheatsheet['cbda']]][previous[cheatsheet['da']]][group][0], cdab_path_column[previous[cheatsheet['cdab']]][previous[cheatsheet['ab']]][group][0], cdba_path_column[previous[cheatsheet['cdba']]][previous[cheatsheet['ba']]][group][0], dabc_path_column[previous[cheatsheet['dabc']]][previous[cheatsheet['bc']]][group][0], dacb_path_column[previous[cheatsheet['dacb']]][previous[cheatsheet['cb']]][group][0], dbac_path_column[previous[cheatsheet['dbac']]][previous[cheatsheet['ac']]][group][0], dbca_path_column[previous[cheatsheet['dbca']]][previous[cheatsheet['ca']]][group][0], dcab_path_column[previous[cheatsheet['dcab']]][previous[cheatsheet['ab']]][group][0], dcba_path_column[previous[cheatsheet['dcba']]][previous[cheatsheet['ba']]][group][0], cdab_path_column[previous[cheatsheet['cdab']]][previous[cheatsheet['ab']]][group][1], bdac_path_column[previous[cheatsheet['bdac']]][previous[cheatsheet['ac']]][group][1], cbad_path_column[previous[cheatsheet['cbad']]][previous[cheatsheet['ad']]][group][1], cdba_path_column[previous[cheatsheet['cdba']]][previous[cheatsheet['ba']]][group][1], adbc_path_column[previous[cheatsheet['adbc']]][previous[cheatsheet['bc']]][group][1], acbd_path_column[previous[cheatsheet['acbd']]][previous[cheatsheet['bd']]][group][1], bdca_path_column[previous[cheatsheet['bdca']]][previous[cheatsheet['ca']]][group][1], adcb_path_column[previous[cheatsheet['adcb']]][previous[cheatsheet['cb']]][group][1], bacd_path_column[previous[cheatsheet['bacd']]][previous[cheatsheet['cd']]][group][1], bcda_path_column[previous[cheatsheet['bcda']]][previous[cheatsheet['da']]][group][1], acdb_path_column[previous[cheatsheet['acdb']]][previous[cheatsheet['db']]][group][1], badc_path_column[previous[cheatsheet['badc']]][previous[cheatsheet['dc']]][group][1])
            if current not in current_reverse_path_column:
               current_reverse_path_column[current] = {}
            current_reverse_path_column[current][group] = previous


def d4_path_finder_reverse(n):
   reverse_paths = d4_path_finder_maker_reverse(n)
   for i in range(n):
      print('')
      #print(reverse_paths[i])
      l = 0
      for j in reverse_paths[i]:
         l += len(reverse_paths[i][j])
      print(l)
   #print(reverse_paths[0])
   #print(reverse_paths[n - 1])
   return d4_path_finder_reverse_recursive(n, reverse_paths)

def d4_path_finder_reverse_recursive(n, reverse_paths, shares=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), depth=0, so_far=''):
   solutions = []
   for group_option in reverse_paths[depth][shares]:
      if depth == n - 1:
         solutions.append(group_option + so_far)
      else:
         solutions.extend(d4_path_finder_reverse_recursive(n, reverse_paths, reverse_paths[depth][shares][group_option], depth + 1, group_option + so_far))
   return solutions


def d4_path_finder(n):
   share = pow(n, 4) / math.factorial(4)
   share_cd = pow(n, 2) / math.factorial(2)
   abcd_path_columns, abcd_path_lengths = d4_path_maker(n, 'a', 'b', 'c', 'd')
   print(abcd_path_lengths[n - 1][share][share_cd])
   abdc_path_columns, abdc_path_lengths = d4_path_maker(n, 'a', 'b', 'd', 'c')
   acbd_path_columns, acbd_path_lengths = d4_path_maker(n, 'a', 'c', 'b', 'd')
   acdb_path_columns, acdb_path_lengths = d4_path_maker(n, 'a', 'c', 'd', 'b')
   adbc_path_columns, adbc_path_lengths = d4_path_maker(n, 'a', 'd', 'b', 'c')
   adcb_path_columns, adcb_path_lengths = d4_path_maker(n, 'a', 'd', 'c', 'b')
   bacd_path_columns, bacd_path_lengths = d4_path_maker(n, 'b', 'a', 'c', 'd')
   badc_path_columns, badc_path_lengths = d4_path_maker(n, 'b', 'a', 'd', 'c')
   bcad_path_columns, bcad_path_lengths = d4_path_maker(n, 'b', 'c', 'a', 'd')
   bcda_path_columns, bcda_path_lengths = d4_path_maker(n, 'b', 'c', 'd', 'a')
   bdac_path_columns, bdac_path_lengths = d4_path_maker(n, 'b', 'd', 'a', 'c')
   bdca_path_columns, bdca_path_lengths = d4_path_maker(n, 'b', 'd', 'c', 'a')
   cabd_path_columns, cabd_path_lengths = d4_path_maker(n, 'c', 'a', 'b', 'd')
   cadb_path_columns, cadb_path_lengths = d4_path_maker(n, 'c', 'a', 'd', 'b')
   cbad_path_columns, cbad_path_lengths = d4_path_maker(n, 'c', 'b', 'a', 'd')
   cbda_path_columns, cbda_path_lengths = d4_path_maker(n, 'c', 'b', 'd', 'a')
   cdab_path_columns, cdab_path_lengths = d4_path_maker(n, 'c', 'd', 'a', 'b')
   cdba_path_columns, cdba_path_lengths = d4_path_maker(n, 'c', 'd', 'b', 'a')
   dabc_path_columns, dabc_path_lengths = d4_path_maker(n, 'd', 'a', 'b', 'c')
   dacb_path_columns, dacb_path_lengths = d4_path_maker(n, 'd', 'a', 'c', 'b')
   dbac_path_columns, dbac_path_lengths = d4_path_maker(n, 'd', 'b', 'a', 'c')
   dbca_path_columns, dbca_path_lengths = d4_path_maker(n, 'd', 'b', 'c', 'a')
   dcab_path_columns, dcab_path_lengths = d4_path_maker(n, 'd', 'c', 'a', 'b')
   dcba_path_columns, dcba_path_lengths = d4_path_maker(n, 'd', 'c', 'b', 'a')
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

#i = 0
#for path_column in d4_path_maker(2, 'a', 'b', 'c', 'd'):
#   print(i)
#   print(path_column)
#   n = 0
#   if i == 1:
#      for index in path_column:
#         n += index
#   print(n)
#   i += 1

#print(d4_path_maker(12, 'a', 'b', 'c', 'd')[11][864][72])
#print(d4_path_maker(6, 'a', 'b', 'c', 'd')[5][54][18])

solutions = d4_path_finder_reverse(12)
#solutions = d4_path_finder(18)
print(len(solutions))
i = 0
for solution in condenser(solutions):
   if not checker(solution, 4, 864):
   #if not checker(solution, 4, 4374):
      print('oh no!')
   print(solution)
   i += 1
print(i)
