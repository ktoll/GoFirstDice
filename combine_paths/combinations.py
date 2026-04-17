#!/usr/bin/python3

group_name_map = ["abc", "acb", "bac", "bca", "cab", "cba"]
num_perms = 6
# perm_additions[group][perm][0=ns, 1=ps, 2=ints]
perm_additions = (((1, 0, 0), (1, -1, -1), (0, 1, 0), (1, -1, -1), (0, 1, 0), (0, 0, 0)),
                  ((1, -1, -1), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 1, 0), (1, -1, -1)),
                  ((0, 1, 0), (1, -1, -1), (1, 0, 0), (1, -1, -1), (0, 0, 0), (0, 1, 0)),
                  ((0, 1, 0), (0, 0, 0), (1, -1, -1), (1, 0, 0), (1, -1, -1), (0, 1, 0)),
                  ((1, -1, -1), (0, 1, 0), (0, 0, 0), (0, 1, 0), (1, 0, 0), (1, -1, -1)),
                  ((0, 0, 0), (0, 1, 0), (1, -1, -1), (0, 1, 0), (1, -1, -1), (1, 0, 0)))

columns = 6

solutions = {}

def add_perms(depth, group, current_perms):
    perms = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for perm in range(num_perms):
        for i in range(3):
            perms[perm][i] = current_perms[perm][i]
        perms[perm][0] += perm_additions[group][perm][0]
        perms[perm][1] += perm_additions[group][perm][1]
        perms[perm][2] += perm_additions[group][perm][2] + (depth * perm_additions[group][perm][1])
    return perms

def recursive_comb(depth, perms, so_far): #perms is: [[num_ns, num_ps, num_ints], [], [], [], [], []]
    if depth == columns:
        solution = make_sol_string(perms)
        if solution not in solutions:
            solutions[solution] = []
        solutions[solution].append(so_far)
    else:
        for group in range(num_perms):
            recursive_comb(depth + 1, add_perms(depth, group, perms), so_far + group_name_map[group])

def make_sol_string(perms):
    solution = ""
    for perm in range(num_perms):
        solution += str(perms[perm][0]) + "n"
        if perms[perm][1] >= 0:
            solution += "+"
        solution += str(perms[perm][1]) + "p"
        if perms[perm][2] >= 0:
            solution += "+"
        solution += str(perms[perm][2]) + ","
    return solution

recursive_comb(0, [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], "")
num_combs = {}

for solution in solutions:
    #print(solution + ": " + str(len(solutions[solution])))

    #if len(solutions[solution]) > 2:
    #    print(solution + ": " + str(len(solutions[solution])))
    #    for comb in solutions[solution]:
    #        print(comb)

    comb_type = len(solutions[solution])
    if comb_type not in num_combs:
        num_combs[comb_type] = 0
    num_combs[comb_type] += 1

for comb_type in num_combs:
    print(str(comb_type) + "s: " + str(num_combs[comb_type]))

print(len(solutions))
