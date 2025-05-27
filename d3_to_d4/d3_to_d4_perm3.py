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


def get_d3_list(d3_path):
   d3_list = []
   with open(d3_path, 'r') as d3_file:
      d3_list = d3_file.read().splitlines()
   return d3_list


def make_graph(d3_list):
   d2_qty = 0
   d2_values = []
   d2_labels = {}
   d3_qty = 0
   d3s = []
   d3_labels = {}
   for i in range(len(d3_list)):
      #print(d3_list[i])
      ab1, ab2, ac1, ac2, bc1, bc2 = get_d2_labels(d3_list[i])
      #print(ab1)
      #print(ab2)
      #print(ac1)
      #print(ac2)
      #print(bc1)
      #print(bc2)
      if ab1 not in d2_labels:
         d2_values.append(set())
         d2_labels[ab1] = d2_qty
         d2_qty += 1
      if ac1 not in d2_labels:
         d2_values.append(set())
         d2_labels[ac1] = d2_qty
         d2_qty += 1
      if bc1 not in d2_labels:
         d2_values.append(set())
         d2_labels[bc1] = d2_qty
         d2_qty += 1
      if ab2 not in d2_labels:
         d2_values.append(set())
         d2_labels[ab2] = d2_qty
         d2_qty += 1
      if ac2 not in d2_labels:
         d2_values.append(set())
         d2_labels[ac2] = d2_qty
         d2_qty += 1
      if bc2 not in d2_labels:
         d2_values.append(set())
         d2_labels[bc2] = d2_qty
         d2_qty += 1
      if d3_list[i] not in d3_labels:
         d3s.append((d2_labels[ab1], d2_labels[ac1], d2_labels[bc1], d3_list[i]))
         d3_labels[d3_list[i]] = d3_qty
         d3_qty += 1
      rev = get_d3_reverse(d3_list[i])
      if rev not in d3_labels:
         d3s.append((d2_labels[ab2], d2_labels[ac2], d2_labels[bc2], rev))
         d3_labels[rev] = d3_qty
         d3_qty += 1
      #print(d3_list[i] == rev)
      #put d3 links in d2s
      d2_values[d2_labels[ab1]].add(d3_labels[d3_list[i]])
      d2_values[d2_labels[ac1]].add(d3_labels[d3_list[i]])
      d2_values[d2_labels[bc1]].add(d3_labels[d3_list[i]])
      d2_values[d2_labels[ab2]].add(d3_labels[rev])
      d2_values[d2_labels[ac2]].add(d3_labels[rev])
      d2_values[d2_labels[bc2]].add(d3_labels[rev])
      #put d2 links in d3
      #d3s.append((d2_labels[ab1], d2_labels[ac1], d2_labels[bc1], d3_list[i]))
      #d3s.append((d2_labels[ab2], d2_labels[ac2], d2_labels[bc2], get_d3_reverse(d3_list[i])))
   #   print(d2_values)
   #   print(d2_labels)
   #   print(d3s)
   #print(d2_labels)

   #total_d2s = 0
   #total_values = 0
   #for d2 in d2_values:
   #   total_values += len(d2)
   #   total_d2s += 1
   #print(total_values / total_d2s)
   return d3s, d2_values, d3_labels

def get_d2_labels(d3):
   ab1 = ''
   ac1 = ''
   bc1 = ''
   for face in d3:
      if face == 'a':
         ab1 = ab1 + 'a'
         ac1 = ac1 + 'a'
      elif face == 'b':
         ab1 = ab1 + 'b'
         bc1 = bc1 + 'a'
      elif face == 'c':
         ac1 = ac1 + 'b'
         bc1 = bc1 + 'b'
      else:
         print("We've got a problem with the input file")
   ab2 = get_reverse(ab1)
   ac2 = get_reverse(ac1)
   bc2 = get_reverse(bc1)
   return ab1, ab2, ac1, ac2, bc1, bc2

def get_reverse(ab1):
   ab2 = ''
   if ab1[len(ab1) - 1] == 'a':
      ab2 = ab1[::-1]
   else:
      for face in ab1[::-1]:
         if face == 'a':
            ab2 = ab2 + 'b'
         else:
            ab2 = ab2 + 'a'
   return ab2

def get_d3_reverse(d3):
   a = d3[len(d3) - 1]
   b = d3[len(d3) - 2]
   c = d3[len(d3) - 3]
   answer = ''
   for face in d3:
      if face == a:
         answer = 'a' + answer
      elif face == b:
         answer = 'b' + answer
      elif face == c:
         answer = 'c' + answer
      else:
         print("We've got a problem with the input file :(")
   return answer
         


def search_graph(d3s, d2s, d3_labels):
   d4s = []
   burned = []
   for abc in range(len(d3s)):
      if abc not in burned:
         ab = d3s[abc][0]
         ac = d3s[abc][1]
         bc = d3s[abc][2]
         #print(abc)
         #print('abc ' + str(abc))
         #print(d3s[abc][3])
         #print('ab ' + str(ab))
         #print('ac ' + str(ac))
         #print('bc ' + str(bc))
         for abd in d2s[ab]:
            if d3s[abd][0] == ab:
               #print('  ' + str(abd))
               #print('  ' + d3s[abd][3])
               ad = d3s[abd][1]
               bd = d3s[abd][2]
               for bcd in d2s[bc].intersection(d2s[bd]):
                  if d3s[bcd][0] == bc and d3s[bcd][1] == bd:
                     #print('    ' + str(bcd))
                     #print('    ' + d3s[bcd][3])
                     cd = d3s[bcd][2]
                     for acd in d2s[ac].intersection(d2s[ad].intersection(d2s[cd])):
                        if d3s[acd][0] == ac and d3s[acd][1] == ad and d3s[acd][2] == cd:
                           #print('      ' + str(acd))
                           #print('      ' + d3s[acd][3])
                           #print('' + str(abc) + ' ' + str(abd) + ' ' + str(acd) + ' ' + str(bcd))
                           d4s.append((d3s[abc][3], d3s[abd][3], d3s[acd][3], d3s[bcd][3]))
         #if abc in d2s[ab]:
         #   d2s[ab].remove(abc)
         #if abc in d2s[ac]:
         #   d2s[ac].remove(abc)
         #if abc in d2s[bc]:
         #   d2s[bc].remove(abc)
         #rev = get_d3_reverse(d3s[abc][3])
         #cba = d3_labels[rev]
         #if d3s[abc] != rev:
         #   ba = d3s[cba][0]
         #   ca = d3s[cba][1]
         #   cb = d3s[cba][2]
         #   if cba in d2s[ba]:
         #      d2s[ba].remove(cba)
         #   if cba in d2s[ca]:
         #      d2s[ca].remove(cba)
         #   if cba in d2s[cb]:
         #      d2s[cb].remove(cba)
         #   burned.append(cba)
   return d4s


def d4_translator(d4s):
   #print(d4s)
   #print(len(d4s))
   solutions = []
   uh_oh = 0
   for d4 in d4s:
      solution = ''
      abc_full = d4[0]
      abd_full = d4[1]
      acd_full = d4[2]
      bcd_full = d4[3]
      uh_oh_flag = False
      for i in range(0, len(abc_full), 3):
         abc = abc_full[i:i + 3]
         abd = abd_full[i:i + 3]
         acd = acd_full[i:i + 3]
         bcd = bcd_full[i:i + 3]
         if abc == 'abc':
            if acd == 'abc' and abd == 'abc' and bcd == 'abc': #abcd
               solution = solution + 'abcd'
            elif bcd == 'acb' and abd == 'abc' and acd == 'acb': #abdc
               solution = solution + 'abdc'
            elif abd == 'acb' and acd == 'acb' and bcd == 'cab': #adbc
               solution = solution + 'adbc'
            elif abd == 'cab' and acd == 'cab' and bcd == 'cab': #dabc
               solution = solution + 'dabc'
            else:
               uh_oh += 1
               uh_oh_flag = True
         elif abc == 'acb':
            if bcd == 'bac' and abd == 'abc' and acd == 'abc': #acbd
               solution = solution + 'acbd'
            elif bcd == 'bca' and abd == 'acb' and acd == 'abc': #acdb
               solution = solution + 'acdb'
            elif acd == 'acb' and abd == 'acb' and bcd == 'cba': #adcb
               solution = solution + 'adcb'
            elif abd == 'cab' and acd == 'cab' and bcd == 'cba': #dacb
               solution = solution + 'dacb'
            else:
               uh_oh += 1
               uh_oh_flag = True
         elif abc == 'bac':
            if acd == 'abc' and abd == 'bac' and bcd == 'abc': #bacd
               solution = solution + 'bacd'
            elif acd == 'acb' and abd == 'bac' and bcd == 'acb': #badc
               solution = solution + 'badc'
            elif abd == 'bca' and acd == 'cab' and bcd == 'acb': #bdac
               solution = solution + 'bdac'
            elif abd == 'cba' and acd == 'cab' and bcd == 'cab': #dbac
               solution = solution + 'dbac'
            else:
               uh_oh += 1
               uh_oh_flag = True
         elif abc == 'bca':
            if abd == 'bac' and acd == 'bac' and bcd == 'abc': #bcad
               solution = solution + 'bcad'
            elif acd == 'bca' and abd == 'bca' and bcd == 'abc': #bcda
               solution = solution + 'bcda'
            elif bcd == 'acb' and abd == 'bca' and acd == 'cba': #bdca
               solution = solution + 'bdca'
            elif abd == 'cba' and acd == 'cba' and bcd == 'cab': #dbca
               solution = solution + 'dbca'
            else:
               uh_oh += 1
               uh_oh_flag = True
         elif abc == 'cab':
            if abd == 'abc' and acd == 'bac' and bcd == 'bac': #cabd
               solution = solution + 'cabd'
            elif abd == 'acb' and acd == 'bac' and bcd == 'bca': #cadb
               solution = solution + 'cadb'
            elif acd == 'bca' and abd == 'cab' and bcd == 'bca': #cdab
               solution = solution + 'cdab'
            elif acd == 'cba' and abd == 'cab' and bcd == 'cba': #dcab
               solution = solution + 'dcab'
            else:
               uh_oh += 1
               uh_oh_flag = True
         elif abc == 'cba':
            if abd == 'bac' and acd == 'bac' and bcd == 'bac': #cbad
               solution = solution + 'cbad'
            elif abd == 'bca' and acd == 'bca' and bcd == 'bac': #cbda
               solution = solution + 'cbda'
            elif bcd == 'bca' and abd == 'cba' and acd == 'bca': #cdba
               solution = solution + 'cdba'
            elif acd == 'cba' and abd == 'cba' and bcd == 'cba': #dcba
               solution = solution + 'dcba'
            else:
               uh_oh += 1
               uh_oh_flag = True
         else:
            uh_oh += 1
            uh_oh_flag = True
      if not uh_oh_flag:
         solutions.append(solution)
   #print("uh ohs: " + str(uh_oh))
   return solutions


parser = argparse.ArgumentParser()
parser.add_argument("d3_path")
args = parser.parse_args()

d3_list = get_d3_list(args.d3_path)
#print(d3_list)
d3s, d2s, d3_labels = make_graph(d3_list)
#print(d3s)
#print(d2s)
d4s = search_graph(d3s, d2s, d3_labels)
#print(len(d4s))
solutions = d4_translator(d4s)
#print(len(solutions))

n = 12
#condensed_len = 0
share = pow(n, 4) / math.factorial(4)
#for solution in condenser(solutions):
for solution in solutions:
   #condensed_len += 1
   #if not checker(solution, 4, share):
   #   print('oh no!')
   print(solution)
#print(condensed_len)
