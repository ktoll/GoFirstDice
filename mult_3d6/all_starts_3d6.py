#!/usr/bin/python3
normal = ["abcbcacabcbaacbbac", \
          "abccabbcacbabacacb", \
          "abccbabaccabcabbac", \
          "abccbabaccabcbaabc", \
          "abccbabcaacbcabbac", \
          "abccbabcaacbcbaabc", \
          "abccbacabbacbaccab", \
          "abccbacabbacbcaacb", \
          "abccbacbaabcbaccab", \
          "abccbacbaabcbcaacb"]

scrambles = [{'a': 'a', 'b': 'b', 'c': 'c'}, \
             {'a': 'a', 'b': 'c', 'c': 'b'}, \
             {'a': 'b', 'b': 'a', 'c': 'c'}, \
             {'a': 'b', 'b': 'c', 'c': 'a'}, \
             {'a': 'c', 'b': 'a', 'c': 'b'}, \
             {'a': 'c', 'b': 'b', 'c': 'a'}]
for s in scrambles:
   for n in normal:
      scrambled = ''
      for f in n:
         scrambled += s[f]
      print(scrambled)
