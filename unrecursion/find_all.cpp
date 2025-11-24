#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <math.h>
#include <unordered_map>
#include <deque>

// Options: SEARCH_3d6, SEARCH_3d12, SEARCH_3d18, SEARCH_3d24, SEARCH_4d6
#define SEARCH_4d12

using namespace std;

static string get_group_3d[6] = {"abc", "acb", "bac", "bca", "cab", "cba"};
static string get_group_4d[24] = {"abcd", "abdc", "acbd", "acdb", "adbc", "adcb", "bacd", "badc", "bcad", "bcda", "bdac", "bdca", "cabd", "cadb", "cbad", "cbda", "cdab", "cdba", "dabc", "dacb", "dbac", "dbca", "dcab", "dcba"};


#ifdef SEARCH_4d6
   #define FOUR_D
   #define SEARCH_3d6
   //#define MAX_SHARE_4d 39 // for normalized
   #define MAX_SHARE_4d (N * N * N * N / 24)
   #define MAX_SHARE_4d_2d 18
#endif

#ifdef SEARCH_4d12
   #define FOUR_D
   #define SEARCH_3d12
   //#define MAX_SHARE_4d 369 // for normalized
   #define MAX_SHARE_4d (N * N * N * N / 24)
   #define MAX_SHARE_4d_2d 72
#endif

#ifdef SEARCH_3d6
   #define THREE_D
   #define N 6
   #define MAX_SHARE 16
#endif

#ifdef SEARCH_3d12
   #define THREE_D
   #define N 12
   #define MAX_SHARE 68
#endif

#ifdef SEARCH_3d18
   #define THREE_D
   #define N 18
   #define MAX_SHARE 156
#endif

#ifdef SEARCH_3d24
   #define THREE_D
   #define N 24
   #define MAX_SHARE 280
#endif

#ifdef FOUR_D
   #define NUM_SHARES_4d (MAX_SHARE_4d + 1)
#endif

#ifdef THREE_D
   #define HALF_COLS (N / 2)
   #define NUM_SHARES (MAX_SHARE + 1)
   //int translator[6][6] = {{5, 3, 4, 1, 2, 0}, //from is abc, to is first index, perm is second index. result is perm.
   //                        {3, 5, 2, 0, 4, 1},
   //                        {4, 1, 5, 3, 0, 2},
   //                        {1, 4, 0, 2, 5, 3},
   //                        {2, 0, 3, 5, 1, 4},
   //                        {0, 2, 1, 4, 3, 5}};
   //int translator[6][6] = {{5, 3, 4, 1, 2, 0}, //from is abc, to is first index, perm is second index. result is perm.
   //                        {3, 5, 2, 0, 4, 1},
   //                        {4, 1, 5, 3, 0, 2},
   //                        {2, 0, 3, 5, 1, 4},
   //                        {1, 4, 0, 2, 5, 3},
   //                        {0, 2, 1, 4, 3, 5}};
#endif

int translator_unbackwards[6][6] = {{0, 1, 2, 3, 4, 5}, //from is abc, to is first index, perm is second index. result is perm.
                                    {1, 0, 4, 5, 2, 3},
                                    {2, 3, 0, 1, 5, 4},
                                    {4, 5, 1, 0, 3, 2},
                                    {3, 2, 5, 4, 0, 1},
                                    {5, 4, 3, 2, 1, 0}};
int backwards[6] = {5, 3, 4, 1, 2, 0};
int translator[6][6];
int translator_4d[24][24] = {{ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}, \
                             { 1,  0,  4,  5,  2,  3,  7,  6, 10, 11,  8,  9, 18, 19, 20, 21, 22, 23, 12, 13, 14, 15, 16, 17}, \
                             { 2,  3,  0,  1,  5,  4, 12, 13, 14, 15, 16, 17,  6,  7,  8,  9, 10, 11, 19, 18, 22, 23, 20, 21}, \
                             { 4,  5,  1,  0,  3,  2, 18, 19, 20, 21, 22, 23,  7,  6, 10, 11,  8,  9, 13, 12, 16, 17, 14, 15}, \
                             { 3,  2,  5,  4,  0,  1, 13, 12, 16, 17, 14, 15, 19, 18, 22, 23, 20, 21,  6,  7,  8,  9, 10, 11}, \
                             { 5,  4,  3,  2,  1,  0, 19, 18, 22, 23, 20, 21, 13, 12, 16, 17, 14, 15,  7,  6, 10, 11,  8,  9}, \
                             { 6,  7,  8,  9, 10, 11,  0,  1,  2,  3,  4,  5, 14, 15, 12, 13, 17, 16, 20, 21, 18, 19, 23, 22}, \
                             { 7,  6, 10, 11,  8,  9,  1,  0,  4,  5,  2,  3, 20, 21, 18, 19, 23, 22, 14, 15, 12, 13, 17, 16}, \
                             {12, 13, 14, 15, 16, 17,  2,  3,  0,  1,  5,  4,  8,  9,  6,  7, 11, 10, 22, 23, 19, 18, 21, 20}, \
                             {18, 19, 20, 21, 22, 23,  4,  5,  1,  0,  3,  2, 10, 11,  7, 6,  9,  8,  16, 17, 13, 12, 15, 14}, \
                             {13, 12, 16, 17, 14, 15,  3,  2,  5,  4,  0,  1, 22, 23, 19, 18, 21, 20,  8,  9,  6,  7, 11, 10}, \
                             {19, 18, 22, 23, 20, 21,  5,  4,  3,  2,  1,  0, 16, 17, 13, 12, 15, 14, 10, 11,  7,  6,  9,  8}, \
                             { 8,  9,  6,  7, 11, 10, 14, 15, 12, 13, 17, 16,  0,  1,  2,  3,  4,  5, 21, 20, 23, 22, 18, 19}, \
                             {10, 11,  7,  6,  9,  8, 20, 21, 18, 19, 23, 22,  1,  0,  4,  5,  2,  3, 15, 14, 17, 16, 12, 13}, \
                             {14, 15, 12, 13, 17, 16,  8,  9,  6,  7, 11, 10,  2,  3,  0,  1,  5,  4, 23, 22, 21, 20, 19, 18}, \
                             {20, 21, 18, 19, 23, 22, 10, 11,  7,  6,  9,  8,  4,  5,  1,  0,  3,  2, 17, 16, 15, 14, 13, 12}, \
                             {16, 17, 13, 12, 15, 14, 22, 23, 19, 18, 21, 20,  3,  2,  5,  4,  0,  1,  9,  8, 11, 10,  6,  7}, \
                             {22, 23, 19, 18, 21, 20, 16, 17, 13, 12, 15, 14,  5,  4,  3,  2,  1,  0, 11, 10,  9,  8,  7,  6}, \
                             { 9,  8, 11, 10,  6,  7, 15, 14, 17, 16, 12, 13, 21, 20, 23, 22, 18, 19,  0,  1,  2,  3,  4,  5}, \
                             {11, 10,  9,  8,  7,  6, 21, 20, 23, 22, 18, 19, 15, 14, 17, 16, 12, 13,  1,  0,  4,  5,  2,  3}, \
                             {15, 14, 17, 16, 12, 13,  9,  8, 11, 10,  6,  7, 23, 22, 21, 20, 19, 18,  2,  3,  0,  1,  5,  4}, \
                             {21, 20, 23, 22, 18, 19, 11, 10,  9,  8,  7,  6, 17, 16, 15, 14, 13, 12,  4,  5,  1,  0,  3,  2}, \
                             {17, 16, 15, 14, 13, 12, 23, 22, 21, 20, 19, 18,  9,  8, 11, 10,  6,  7,  3,  2,  5,  4,  0,  1}, \
                             {23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0}};
int translator_4d_backwards[24][24];
                      // 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
int backwards_4d[24] = {23, 17, 21, 11, 15,  9, 22, 16, 19,  5, 13,  3, 20, 10, 18,  4,  7,  1, 14,  8, 12,  2,  6,  0};
int translator_4d_2d[24][12] = {{ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11}, // this needs backwarding also
                                { 0,  2,  1,  3,  5,  4,  9, 10, 11,  6,  7,  8},
                                { 1,  0,  2,  6,  7,  8,  3,  4,  5,  9, 11, 10},
                                { 1,  2,  0,  6,  8,  7,  9, 11, 10,  3,  4,  5},
                                { 2,  0,  1,  9, 10, 11,  3,  5,  4,  6,  8,  7},
                                { 2,  1,  0,  9, 11, 10,  6,  8,  7,  3,  5,  4},
                                { 3,  4,  5,  0,  1,  2,  7,  6,  8, 10,  9, 11},
                                { 3,  5,  4,  0,  2,  1, 10,  9, 11,  7,  6,  8},
                                { 4,  3,  5,  7,  6,  8,  0,  1,  2, 10, 11,  9},
                                { 4,  5,  3,  7,  8,  6, 10, 11,  9,  0,  1,  2},
                                { 5,  3,  4, 10,  9, 11,  0,  2,  1,  7,  8,  6},
                                { 5,  4,  3, 10, 11,  9,  7,  8,  6,  0,  2,  1},
                                { 6,  7,  8,  1,  0,  2,  4,  3,  5, 11,  9, 10},
                                { 6,  8,  7,  1,  2,  0, 11,  9, 10,  4,  3,  5},
                                { 7,  6,  8,  4,  3,  5,  1,  0,  2, 11, 10,  9},
                                { 7,  8,  6,  4,  5,  3, 11, 10,  9,  1,  0,  2},
                                { 8,  6,  7, 11,  9, 10,  1,  2,  0,  4,  5,  3},
                                { 8,  7,  6, 11, 10,  9,  4,  5,  3,  1,  2,  0},
                                { 9, 10, 11,  2,  0,  1,  5,  3,  4,  8,  6,  7},
                                { 9, 11, 10,  2,  1,  0,  8,  6,  7,  5,  3,  4},
                                {10,  9, 11,  5,  3,  4,  2,  0,  1,  8,  7,  6},
                                {10, 11,  9,  5,  4,  3,  8,  7,  6,  2,  0,  1},
                                {11,  9, 10,  8,  6,  7,  2,  1,  0,  5,  4,  3},
                                {11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0}};
int translator_4d_2d_backwards[24][12];


void initialize_stuff() {
   for (int i = 0; i < 6; i++) {
      for (int j = 0; j < 6; j++) {
         translator[i][j] = translator_unbackwards[i][backwards[j]];
      }
   }
   for (int i = 0; i < 24; i++) {
      for (int j = 0; j < 24; j++) {
         translator_4d_backwards[i][j] = translator_4d[i][backwards_4d[j]];
      }
      for (int j = 0; j < 12; j++) {
         translator_4d_2d_backwards[i][j] = translator_4d_2d[i][backwards_4d[j * 2] / 2];
      }
   }
   //for (int i = 0; i < 24; i++) {
   //   for (int j = 0; j < 24; j++) {
   //      cout << translator_4d_backwards[i][j] << ",";
   //   }
   //   cout << "\n";
   //}
   //for (int i = 0; i < 24; i++) {
   //   for (int j = 0; j < 12; j++) {
   //      cout << translator_4d_2d[i][j] << " ";
   //   }
   //   cout << "\n";
   //}
   //for (int i = 0; i < 24; i++) {
   //   for (int j = 0; j < 12; j++) {
   //      cout << translator_4d_2d_backwards[i][j] << " ";
   //   }
   //   cout << "\n";
   //}
}


// 3d ----------------------------------------------------------------------------------------------
// between tuple struct map queue stuff
typedef tuple<int, int, int, int, int, int> btw_3d_key_t;
typedef deque<tuple<btw_3d_key_t, int>> btw_3d_data_t; // perms, then group

struct key_hash : public unary_function<btw_3d_key_t, size_t> {
   size_t operator()(const btw_3d_key_t& k) const {
      return (get<0>(k) * 5) + (get<1>(k) * 4) + (get<2>(k) * 3) + (get<3>(k) * 2) + get<4>(k);
   }
};

struct key_equal : public binary_function<btw_3d_key_t, btw_3d_key_t, size_t> {
   bool operator()(const btw_3d_key_t& k0, const btw_3d_key_t& k1) const {
      return (get<0>(k0) == get<0>(k1) &&
              get<1>(k0) == get<1>(k1) &&
              get<2>(k0) == get<2>(k1) &&
              get<3>(k0) == get<3>(k1) &&
              get<4>(k0) == get<4>(k1) &&
              get<5>(k0) == get<5>(k1));
   }
};

typedef unordered_map<const btw_3d_key_t, btw_3d_data_t, key_hash, key_equal> btw_3d_map_t;
typedef unordered_map<const btw_3d_key_t, unordered_map<int, btw_3d_key_t>, key_hash, key_equal> btw_3d_map_sols_t;


// global variables
int paths[HALF_COLS][NUM_SHARES][4];
btw_3d_map_t btw_map[HALF_COLS];
btw_3d_map_t joining;
btw_3d_map_sols_t btw_map_solutions[HALF_COLS - 1];


// path making
void path_maker_3d() {
   for (int i = 0; i < HALF_COLS; i++) {
      for (int j = 0; j < NUM_SHARES; j++) {
         for (int k = 0; k < 4; k++) {
            paths[i][j][k] = -1;
         }
      }
   }
   int grouptype_add[] = {0, 0, N - 1, N};
   for (int grouptype = 0; grouptype < 4; grouptype++) {
      paths[0][0][grouptype] = grouptype_add[grouptype];
   }
   for (int between = 1; between < HALF_COLS; between++) {
      grouptype_add[0] = between * (N - 1 - between);
      grouptype_add[1] = between * (N - between);
      grouptype_add[2] = (between + 1) * (N - 1 - between);
      grouptype_add[3] = (between + 1) * (N - between);
      for (int grouptype = 3; grouptype >= 0; grouptype--) {
         grouptype_add[grouptype] -= grouptype_add[0];
      }
      for (int share = 0; share < NUM_SHARES; share++) {
         for (int prev_grouptype = 0; prev_grouptype < 4; prev_grouptype++) {
            if (paths[between - 1][share][prev_grouptype] > -1) {
               for (int grouptype = 0; grouptype < 4; grouptype++) {
                  if (paths[between - 1][share][prev_grouptype] + grouptype_add[grouptype] < NUM_SHARES) {
                     paths[between][paths[between - 1][share][prev_grouptype]][grouptype] = paths[between - 1][share][prev_grouptype] + grouptype_add[grouptype];
                  }
               }
            }
         }
      }
   }
}


// path printing
void print_path_3d() {
   cout << 0 << "\n";
   for (int between = 0; between < HALF_COLS; between++) {
      int shares[NUM_SHARES];
      for (int i = 0; i < NUM_SHARES; i++) {
         shares[i] = 0;
      }
      for (int share = 0; share < NUM_SHARES; share++) {
         for (int grouptype = 0; grouptype < 4; grouptype++) {
            if (paths[between][share][grouptype] > -1) {
               shares[paths[between][share][grouptype]] = 1;
            }
         }
      }
      for (int share = 0; share < NUM_SHARES; share++) {
         if (shares[share] > 0) {
            if (share < 10) {
               cout << share << "   ";
            }
            else if (share < 100) {
               cout << share << "  ";
            }
            else {
               cout << share << " ";
            }
         }
         else {
            cout << "    ";
         }
      }
      cout << "\n";
   }
   //for (int between = 0; between < HALF_COLS; between++) {
   //   for (int share = 0; share < NUM_SHARES; share++) {
   //      for (int grouptype = 0; grouptype < 4; grouptype++) {
   //         cout << paths[between][share][grouptype] << " ";
   //      }
   //      cout << ": ";
   //   }
   //   cout << "\n";
   //}
}


// path searching
void path_finder_3d() {
   int group_to_grouptype[6][6] = {{3, 2, 1, 2, 1, 0},
                                   {2, 3, 1, 0, 1, 2},
                                   {1, 2, 3, 2, 0, 1},
                                   {1, 0, 2, 3, 2, 1},
                                   {2, 1, 0, 1, 3, 2},
                                   {0, 1, 2, 1, 2, 3}};
   btw_map[0][make_tuple(N, N - 1, 0, N - 1, 0, 0)].push_back(make_tuple(make_tuple(0, 0, 0, 0, 0, 0), 0));
   for (int between = 1; between < HALF_COLS; between++) {
      for (auto kv : btw_map[between - 1]) {
         // ^should be able to parallelize this for loop
         for (int group = 0; group < 6; group++) {
            if ((paths[between][get<0>(kv.first)][group_to_grouptype[group][0]] > -1) &&
                (paths[between][get<1>(kv.first)][group_to_grouptype[group][1]] > -1) &&
                (paths[between][get<2>(kv.first)][group_to_grouptype[group][2]] > -1) &&
                (paths[between][get<3>(kv.first)][group_to_grouptype[group][3]] > -1) &&
                (paths[between][get<4>(kv.first)][group_to_grouptype[group][4]] > -1) &&
                (paths[between][get<5>(kv.first)][group_to_grouptype[group][5]] > -1)) {
               btw_map[between][make_tuple(paths[between][get<0>(kv.first)][group_to_grouptype[group][0]],
                                           paths[between][get<1>(kv.first)][group_to_grouptype[group][1]],
                                           paths[between][get<2>(kv.first)][group_to_grouptype[group][2]],
                                           paths[between][get<3>(kv.first)][group_to_grouptype[group][3]],
                                           paths[between][get<4>(kv.first)][group_to_grouptype[group][4]],
                                           paths[between][get<5>(kv.first)][group_to_grouptype[group][5]])].push_back(make_tuple(kv.first, group));
            }
         }
      }
   }
   int current_flipped[6];
   for (auto kv : btw_map[HALF_COLS - 1]) {
      // ^should be able to parallelize this for loop
      current_flipped[0] = MAX_SHARE - get<0>(kv.first);
      current_flipped[1] = MAX_SHARE - get<1>(kv.first);
      current_flipped[2] = MAX_SHARE - get<2>(kv.first);
      current_flipped[3] = MAX_SHARE - get<3>(kv.first);
      current_flipped[4] = MAX_SHARE - get<4>(kv.first);
      current_flipped[5] = MAX_SHARE - get<5>(kv.first);
      for (int translation = 0; translation < 6; translation++) {
         btw_3d_key_t translated_key = make_tuple(current_flipped[translator[translation][0]],
                                                  current_flipped[translator[translation][1]],
                                                  current_flipped[translator[translation][2]],
                                                  current_flipped[translator[translation][3]],
                                                  current_flipped[translator[translation][4]],
                                                  current_flipped[translator[translation][5]]);
         if (btw_map[HALF_COLS - 1].find(translated_key) != btw_map[HALF_COLS - 1].end()) {
            joining[kv.first].push_back(make_tuple(translated_key, translation));
         }
      }
   }
}


// path search printing
void print_path_search_3d(bool only_count) {
   cout << "\n";
   for (int between = 0; between < HALF_COLS; between++) {
      cout << "between columns " << between << " and " << between + 1 << " has " << btw_map[between].size() << "\n";
   }
   cout << "joining has " << joining.size() << "\n\n";

   if (!only_count) {
      for (int between = 0; between < HALF_COLS; between++) {
         for (auto kv : btw_map[between]) {
            cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ") ";
         }
         cout << "\n\n";
      }
      for (auto kv : joining) {
         cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ") \n";
         for (auto kg : kv.second) {
            cout << "  " << get<1>(kg) << " (" << get<0>(get<0>(kg)) << ","  << get<1>(get<0>(kg)) << ","  << get<2>(get<0>(kg)) << ","  << get<3>(get<0>(kg)) << ","  << get<4>(get<0>(kg)) << ","  << get<5>(get<0>(kg)) << ") \n";
         }
      }
      cout << "\n";
   }
}


// answer printing
vector<string> recursive_print_answers_3d(int depth, btw_3d_key_t base, string so_far, int translation) {
   vector<string> solutions = {};
   if (depth == -1) {
      solutions.push_back(so_far);
   }
   else {
      for (auto qp : btw_map[depth][base]) {
         vector<string> more_solutions;
         if (translation < 0) {
            more_solutions = recursive_print_answers_3d(depth - 1, get<0>(qp), get_group_3d[get<1>(qp)] + so_far, translation);
         }
         else {
            more_solutions = recursive_print_answers_3d(depth - 1, get<0>(qp), so_far + get_group_3d[translator[translation][get<1>(qp)]], translation);
         }
         solutions.insert(solutions.end(), more_solutions.begin(), more_solutions.end());
      }
   }
   return solutions;
}

void print_answers_3d(bool only_count) {
   btw_3d_key_t front_base;
   int groups[N];
   int count = 0;
   for (auto meeting : joining) {
      // ^should be able to parallelize this for loop
      front_base = meeting.first;
      vector<string> front_solutions = recursive_print_answers_3d(HALF_COLS - 1, front_base, "", -1);
      for (auto shuffle_qp : meeting.second) {
         vector<string> back_solutions = recursive_print_answers_3d(HALF_COLS - 1, get<0>(shuffle_qp), "", get<1>(shuffle_qp));
         if (!only_count) {
            for (auto fs : front_solutions) {
               for (auto bs : back_solutions) {
                  cout << fs << bs << "\n";
               }
            }
         }
         count += front_solutions.size() * back_solutions.size();
      }
   }
   cout << "Total 3d" << N << " solutions: " << count << "\n";
}


// making answer tree
void make_answer_tree_3d() {
   for (auto kv : joining) {
      for (auto kg : btw_map[HALF_COLS - 1][kv.first]) {
         btw_map_solutions[HALF_COLS - 2][get<0>(kg)][get<1>(kg)] = kv.first;
      }
   }
   for (int between = HALF_COLS - 3; between >= 0; between--) {
      for (auto kv : btw_map_solutions[between + 1]) {
         for (auto kg : btw_map[between + 1][kv.first]) {
            btw_map_solutions[between][get<0>(kg)][get<1>(kg)] = kv.first;
         }
      }
   }
}


// print answer tree
void print_answer_tree_3d(bool only_count) {
   cout << "\nanswer tree:\n";
   for (int between = 0; between < HALF_COLS - 1; between++) {
      cout << "between columns " << between << " and " << between + 1 << " has " << btw_map_solutions[between].size() << "\n";
   }
   cout << "joining has " << joining.size() << "\n\n";

   if (!only_count) {
      for (int between = 0; between < HALF_COLS - 1; between++) {
         for (auto kv : btw_map_solutions[between]) {
            cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ") ";
         }
         cout << "\n\n";
      }
      for (auto kv : joining) {
         cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ")  ";
      }
      cout << "\n\n";
   }
}

// 4d ----------------------------------------------------------------------------------------------
// between tuple struct map queue stuff
typedef tuple<int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int> btw_4d_key_t; // 24 4 letter perms, 12 2 letter perms
typedef deque<tuple<btw_4d_key_t, int>> btw_4d_data_t;

// abcd abdc acbd acdb adbc adcb
// bacd badc bcad bcda bdac bdca
// cabd cadb cbad cbda cdab cdba
// dabc dacb dbac dbca dcab dcba

struct key_hash_4d : public unary_function<btw_4d_key_t, size_t> {
   size_t operator()(const btw_4d_key_t& k) const {
      return (get<24 + 0>(k) << 22) + (get<24 + 1>(k) << 21) + (get<24 + 2>(k) << 20) + (get<24 + 4>(k) << 19) + (get<24 + 5>(k) << 18) + (get<24 + 8>(k) << 18) + (get<0>(k) << 17) + (get<1>(k) << 16) + (get<2>(k) << 15) + (get<3>(k) << 14) + (get<4>(k) << 13) + (get<5>(k) << 12) + (get<6>(k) << 11) + (get<7>(k) << 10) + (get<8>(k) << 9) + (get<9>(k) << 8) + (get<10>(k) << 7) + (get<11>(k) << 6) + (get<12>(k) << 5) + (get<13>(k) << 4) + (get<14>(k) << 3) + (get<15>(k) << 2) + (get<16>(k) << 1) + get<17>(k);
   }
};

struct key_equal_4d : public binary_function<btw_4d_key_t, btw_4d_key_t, size_t> {
   bool operator()(const btw_4d_key_t& k0, const btw_4d_key_t& k1) const {
      return (get<0>(k0) == get<0>(k1) &&
              get<1>(k0) == get<1>(k1) &&
              get<2>(k0) == get<2>(k1) &&
              get<3>(k0) == get<3>(k1) &&
              get<4>(k0) == get<4>(k1) &&
              get<5>(k0) == get<5>(k1) &&
              get<6>(k0) == get<6>(k1) &&
              get<7>(k0) == get<7>(k1) &&
              get<8>(k0) == get<8>(k1) &&
              get<9>(k0) == get<9>(k1) &&
              get<10>(k0) == get<10>(k1) &&
              get<11>(k0) == get<11>(k1) &&
              get<12>(k0) == get<12>(k1) &&
              get<13>(k0) == get<13>(k1) &&
              get<14>(k0) == get<14>(k1) &&
              get<15>(k0) == get<15>(k1) &&
              get<16>(k0) == get<16>(k1) &&
              get<17>(k0) == get<17>(k1) &&
              get<18>(k0) == get<18>(k1) &&
              get<19>(k0) == get<19>(k1) &&
              get<20>(k0) == get<20>(k1) &&
              get<21>(k0) == get<21>(k1) &&
              get<22>(k0) == get<22>(k1) &&
              get<23>(k0) == get<23>(k1));
   }
};

typedef unordered_map<const btw_4d_key_t, btw_4d_data_t, key_hash_4d, key_equal_4d> btw_4d_map_t;
typedef unordered_map<const btw_4d_key_t, deque<tuple<btw_3d_key_t, btw_3d_key_t, btw_3d_key_t, btw_3d_key_t>>, key_hash_4d, key_equal_4d> btw_4d_to_btw_3d_t;


// global variables
btw_4d_map_t btw_map_4d[HALF_COLS];
btw_4d_to_btw_3d_t btw_map_4d_3d[HALF_COLS];
btw_4d_map_t joining_4d;


// path searching
btw_4d_key_t get_next_key_4d(btw_4d_key_t prev_4d_key, int group, int column) {
   int n = column;
   int m = N - column - 1;
   //                                  add,               add*q,   ab add
   int grouptype_to_addition[8][3] = {{0,                 m,       n},
                                      {0,                 (m + 1), n},
                                      {0,                 m,       (n + 1)},
                                      {0,                 (m + 1), (n + 1)},
                                      {n       * m,       m,       n},
                                      {n       * (m + 1), (m + 1), n},
                                      {(n + 1) * m,       m,       (n + 1)},
                                      {(n + 1) * (m + 1), (m + 1), (n + 1)}};
   // perm = 0, index is group
   int group_to_grouptype[24] = {7, 6, 3, 3, 6, 2, 5, 4, 5, 5, 4, 4, 3, 3, 1, 1, 3, 1, 6, 2, 4, 4, 2, 0};
   // [perm][group]
   int prev_key[36];
   int next_key[36];
   prev_key[ 0] = get< 0>(prev_4d_key);
   prev_key[ 1] = get< 1>(prev_4d_key);
   prev_key[ 2] = get< 2>(prev_4d_key);
   prev_key[ 3] = get< 3>(prev_4d_key);
   prev_key[ 4] = get< 4>(prev_4d_key);
   prev_key[ 5] = get< 5>(prev_4d_key);
   prev_key[ 6] = get< 6>(prev_4d_key);
   prev_key[ 7] = get< 7>(prev_4d_key);
   prev_key[ 8] = get< 8>(prev_4d_key);
   prev_key[ 9] = get< 9>(prev_4d_key);
   prev_key[10] = get<10>(prev_4d_key);
   prev_key[11] = get<11>(prev_4d_key);
   prev_key[12] = get<12>(prev_4d_key);
   prev_key[13] = get<13>(prev_4d_key);
   prev_key[14] = get<14>(prev_4d_key);
   prev_key[15] = get<15>(prev_4d_key);
   prev_key[16] = get<16>(prev_4d_key);
   prev_key[17] = get<17>(prev_4d_key);
   prev_key[18] = get<18>(prev_4d_key);
   prev_key[19] = get<19>(prev_4d_key);
   prev_key[20] = get<20>(prev_4d_key);
   prev_key[21] = get<21>(prev_4d_key);
   prev_key[22] = get<22>(prev_4d_key);
   prev_key[23] = get<23>(prev_4d_key);
   prev_key[24] = get<24>(prev_4d_key);
   prev_key[25] = get<25>(prev_4d_key);
   prev_key[26] = get<26>(prev_4d_key);
   prev_key[27] = get<27>(prev_4d_key);
   prev_key[28] = get<28>(prev_4d_key);
   prev_key[29] = get<29>(prev_4d_key);
   prev_key[30] = get<30>(prev_4d_key);
   prev_key[31] = get<31>(prev_4d_key);
   prev_key[32] = get<32>(prev_4d_key);
   prev_key[33] = get<33>(prev_4d_key);
   prev_key[34] = get<34>(prev_4d_key);
   prev_key[35] = get<35>(prev_4d_key);
   for (int i = 0; i < 24; i++) {
      next_key[i] = prev_key[i] + grouptype_to_addition[group_to_grouptype[translator_4d[i][group]]][0] + (prev_key[24 + (i / 2)] * grouptype_to_addition[group_to_grouptype[translator_4d[i][group]]][1]);
   }
   for (int i = 0; i < 12; i++) {
      next_key[24 + i] = prev_key[24 + i] + grouptype_to_addition[group_to_grouptype[translator_4d[i * 2][group]]][2];
   }
   btw_4d_key_t next_4d_key = make_tuple(next_key[ 0],
                                         next_key[ 1],
                                         next_key[ 2],
                                         next_key[ 3],
                                         next_key[ 4],
                                         next_key[ 5],
                                         next_key[ 6],
                                         next_key[ 7],
                                         next_key[ 8],
                                         next_key[ 9],
                                         next_key[10],
                                         next_key[11],
                                         next_key[12],
                                         next_key[13],
                                         next_key[14],
                                         next_key[15],
                                         next_key[16],
                                         next_key[17],
                                         next_key[18],
                                         next_key[19],
                                         next_key[20],
                                         next_key[21],
                                         next_key[22],
                                         next_key[23],
                                         next_key[24],
                                         next_key[25],
                                         next_key[26],
                                         next_key[27],
                                         next_key[28],
                                         next_key[29],
                                         next_key[30],
                                         next_key[31],
                                         next_key[32],
                                         next_key[33],
                                         next_key[34],
                                         next_key[35]);
   return next_4d_key;
}

void path_finder_4d() {
   int combine_3d_to_4d[6][4][4] = {{{0, 0, 0,  0},
                                     {0, 1, 1,  1},
                                     {1, 1, 4,  4},
                                     {4, 4, 4, 18}},
                                    {{0, 0, 2,  2},
                                     {1, 0, 3,  3},
                                     {1, 1, 5,  5},
                                     {4, 4, 5, 19}},
                                    {{2, 0, 0,  6},
                                     {2, 1, 1,  7},
                                     {3, 4, 1, 10},
                                     {5, 4, 4, 20}},
                                    {{2, 2, 0,  8},
                                     {3, 3, 0,  9},
                                     {3, 5, 1, 11},
                                     {5, 5, 4, 21}},
                                    {{0, 2, 2, 12},
                                     {1, 2, 3, 13},
                                     {4, 3, 3, 16},
                                     {4, 5, 5, 22}},
                                    {{2, 2, 2, 14},
                                     {3, 3, 2, 15},
                                     {5, 3, 3, 17},
                                     {5, 5, 5, 23}}};
   btw_3d_key_t next_3d_key = make_tuple(N, N - 1, 0, N - 1, 0, 0);
   btw_4d_key_t next_4d_key = get_next_key_4d(make_tuple(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 0, 0);
   btw_map_4d_3d[0][next_4d_key].push_back(make_tuple(next_3d_key, next_3d_key, next_3d_key, next_3d_key));
   btw_map_4d[0][next_4d_key].push_back(make_tuple(make_tuple(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 0));
   for (int between = 1; between < HALF_COLS; between++) {
      for (auto kv : btw_map_4d[between - 1]) {
         for (auto set_3d : btw_map_4d_3d[between - 1][kv.first]) {
            for (auto abc_option : btw_map_solutions[between - 1][get<0>(set_3d)]) {
               for (int i = 0; i < 4; i++) {
                  bool good = true;
                  good &= (btw_map_solutions[between - 1][get<1>(set_3d)].find(combine_3d_to_4d[abc_option.first][i][0]) != btw_map_solutions[between - 1][get<0>(set_3d)].end());
                  good &= (btw_map_solutions[between - 1][get<2>(set_3d)].find(combine_3d_to_4d[abc_option.first][i][1]) != btw_map_solutions[between - 1][get<0>(set_3d)].end());
                  good &= (btw_map_solutions[between - 1][get<3>(set_3d)].find(combine_3d_to_4d[abc_option.first][i][2]) != btw_map_solutions[between - 1][get<0>(set_3d)].end());
                  if (good) {
                     next_4d_key = get_next_key_4d(kv.first, combine_3d_to_4d[abc_option.first][i][3], between);
                     btw_map_4d_3d[between][next_4d_key].push_back(make_tuple(btw_map_solutions[between - 1][get<0>(set_3d)][abc_option.first],
                                                                              btw_map_solutions[between - 1][get<1>(set_3d)][combine_3d_to_4d[abc_option.first][i][0]],
                                                                              btw_map_solutions[between - 1][get<2>(set_3d)][combine_3d_to_4d[abc_option.first][i][1]],
                                                                              btw_map_solutions[between - 1][get<3>(set_3d)][combine_3d_to_4d[abc_option.first][i][2]]));
                     btw_map_4d[between][next_4d_key].push_back(make_tuple(kv.first, combine_3d_to_4d[abc_option.first][i][3]));
                  }
               }
            }
         }
      }
   }

   int current_flipped[36];
   for (auto kv : btw_map_4d[HALF_COLS - 1]) {
      // ^should be able to parallelize this for loop
      current_flipped[ 0] = MAX_SHARE_4d - get< 0>(kv.first);
      current_flipped[ 1] = MAX_SHARE_4d - get< 1>(kv.first);
      current_flipped[ 2] = MAX_SHARE_4d - get< 2>(kv.first);
      current_flipped[ 3] = MAX_SHARE_4d - get< 3>(kv.first);
      current_flipped[ 4] = MAX_SHARE_4d - get< 4>(kv.first);
      current_flipped[ 5] = MAX_SHARE_4d - get< 5>(kv.first);
      current_flipped[ 6] = MAX_SHARE_4d - get< 6>(kv.first);
      current_flipped[ 7] = MAX_SHARE_4d - get< 7>(kv.first);
      current_flipped[ 8] = MAX_SHARE_4d - get< 8>(kv.first);
      current_flipped[ 9] = MAX_SHARE_4d - get< 9>(kv.first);
      current_flipped[10] = MAX_SHARE_4d - get<10>(kv.first);
      current_flipped[11] = MAX_SHARE_4d - get<11>(kv.first);
      current_flipped[12] = MAX_SHARE_4d - get<12>(kv.first);
      current_flipped[13] = MAX_SHARE_4d - get<13>(kv.first);
      current_flipped[14] = MAX_SHARE_4d - get<14>(kv.first);
      current_flipped[15] = MAX_SHARE_4d - get<15>(kv.first);
      current_flipped[16] = MAX_SHARE_4d - get<16>(kv.first);
      current_flipped[17] = MAX_SHARE_4d - get<17>(kv.first);
      current_flipped[18] = MAX_SHARE_4d - get<18>(kv.first);
      current_flipped[19] = MAX_SHARE_4d - get<19>(kv.first);
      current_flipped[20] = MAX_SHARE_4d - get<20>(kv.first);
      current_flipped[21] = MAX_SHARE_4d - get<21>(kv.first);
      current_flipped[22] = MAX_SHARE_4d - get<22>(kv.first);
      current_flipped[23] = MAX_SHARE_4d - get<23>(kv.first);
      current_flipped[24] = MAX_SHARE_4d_2d - get<24>(kv.first);
      current_flipped[25] = MAX_SHARE_4d_2d - get<25>(kv.first);
      current_flipped[26] = MAX_SHARE_4d_2d - get<26>(kv.first);
      current_flipped[27] = MAX_SHARE_4d_2d - get<27>(kv.first);
      current_flipped[28] = MAX_SHARE_4d_2d - get<28>(kv.first);
      current_flipped[29] = MAX_SHARE_4d_2d - get<29>(kv.first);
      current_flipped[30] = MAX_SHARE_4d_2d - get<30>(kv.first);
      current_flipped[31] = MAX_SHARE_4d_2d - get<31>(kv.first);
      current_flipped[32] = MAX_SHARE_4d_2d - get<32>(kv.first);
      current_flipped[33] = MAX_SHARE_4d_2d - get<33>(kv.first);
      current_flipped[34] = MAX_SHARE_4d_2d - get<34>(kv.first);
      current_flipped[35] = MAX_SHARE_4d_2d - get<35>(kv.first);
      for (int translation = 0; translation < 24; translation++) {
         btw_4d_key_t translated_key = make_tuple(current_flipped[translator_4d_backwards[translation][ 0]],
                                                  current_flipped[translator_4d_backwards[translation][ 1]],
                                                  current_flipped[translator_4d_backwards[translation][ 2]],
                                                  current_flipped[translator_4d_backwards[translation][ 3]],
                                                  current_flipped[translator_4d_backwards[translation][ 4]],
                                                  current_flipped[translator_4d_backwards[translation][ 5]],
                                                  current_flipped[translator_4d_backwards[translation][ 6]],
                                                  current_flipped[translator_4d_backwards[translation][ 7]],
                                                  current_flipped[translator_4d_backwards[translation][ 8]],
                                                  current_flipped[translator_4d_backwards[translation][ 9]],
                                                  current_flipped[translator_4d_backwards[translation][10]],
                                                  current_flipped[translator_4d_backwards[translation][11]],
                                                  current_flipped[translator_4d_backwards[translation][12]],
                                                  current_flipped[translator_4d_backwards[translation][13]],
                                                  current_flipped[translator_4d_backwards[translation][14]],
                                                  current_flipped[translator_4d_backwards[translation][15]],
                                                  current_flipped[translator_4d_backwards[translation][16]],
                                                  current_flipped[translator_4d_backwards[translation][17]],
                                                  current_flipped[translator_4d_backwards[translation][18]],
                                                  current_flipped[translator_4d_backwards[translation][19]],
                                                  current_flipped[translator_4d_backwards[translation][20]],
                                                  current_flipped[translator_4d_backwards[translation][21]],
                                                  current_flipped[translator_4d_backwards[translation][22]],
                                                  current_flipped[translator_4d_backwards[translation][23]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 0]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 1]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 2]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 3]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 4]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 5]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 6]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 7]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 8]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][ 9]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][10]],
                                                  current_flipped[24 + translator_4d_2d_backwards[translation][11]]);
         if (btw_map_4d[HALF_COLS - 1].find(translated_key) != btw_map_4d[HALF_COLS - 1].end()) {
            joining_4d[kv.first].push_back(make_tuple(translated_key, translation));
         }
      }
   }
}


// path search printing
void print_path_search_4d(bool only_count) {
   cout << "\n";
   for (int between = 0; between < HALF_COLS; between++) {
      cout << "between columns " << between << " and " << between + 1 << " has " << btw_map_4d[between].size() << "\n";
   }
   cout << "joining has " << joining_4d.size() << "\n\n";

   if (!only_count) {
      for (int between = 0; between < HALF_COLS; between++) {
         for (auto kv : btw_map_4d[between]) {
            cout << "((" << get< 0>(kv.first);
            cout <<  "," << get< 1>(kv.first);
            cout <<  "," << get< 2>(kv.first);
            cout <<  "," << get< 3>(kv.first);
            cout <<  "," << get< 4>(kv.first);
            cout <<  "," << get< 5>(kv.first);
            cout <<  "," << get< 6>(kv.first);
            cout <<  "," << get< 7>(kv.first);
            cout <<  "," << get< 8>(kv.first);
            cout <<  "," << get< 9>(kv.first);
            cout <<  "," << get<10>(kv.first);
            cout <<  "," << get<11>(kv.first);
            cout <<  "," << get<12>(kv.first);
            cout <<  "," << get<13>(kv.first);
            cout <<  "," << get<14>(kv.first);
            cout <<  "," << get<15>(kv.first);
            cout <<  "," << get<16>(kv.first);
            cout <<  "," << get<17>(kv.first);
            cout <<  "," << get<18>(kv.first);
            cout <<  "," << get<19>(kv.first);
            cout <<  "," << get<20>(kv.first);
            cout <<  "," << get<21>(kv.first);
            cout <<  "," << get<22>(kv.first);
            cout <<  "," << get<23>(kv.first);
            cout << ")(" << get<24>(kv.first);
            cout <<  "," << get<25>(kv.first);
            cout <<  "," << get<26>(kv.first);
            cout <<  "," << get<27>(kv.first);
            cout <<  "," << get<28>(kv.first);
            cout <<  "," << get<29>(kv.first);
            cout <<  "," << get<30>(kv.first);
            cout <<  "," << get<31>(kv.first);
            cout <<  "," << get<32>(kv.first);
            cout <<  "," << get<33>(kv.first);
            cout <<  "," << get<34>(kv.first);
            cout <<  "," << get<35>(kv.first) << "))";
         }
         cout << "\n\n";
      }
      //for (auto kv : joining_4d) {
      //   cout << "((" << get< 0>(kv.first);
      //   cout <<  "," << get< 1>(kv.first);
      //   cout <<  "," << get< 2>(kv.first);
      //   cout <<  "," << get< 3>(kv.first);
      //   cout <<  "," << get< 4>(kv.first);
      //   cout <<  "," << get< 5>(kv.first);
      //   cout <<  "," << get< 6>(kv.first);
      //   cout <<  "," << get< 7>(kv.first);
      //   cout <<  "," << get< 8>(kv.first);
      //   cout <<  "," << get< 9>(kv.first);
      //   cout <<  "," << get<10>(kv.first);
      //   cout <<  "," << get<11>(kv.first);
      //   cout <<  "," << get<12>(kv.first);
      //   cout <<  "," << get<13>(kv.first);
      //   cout <<  "," << get<14>(kv.first);
      //   cout <<  "," << get<15>(kv.first);
      //   cout <<  "," << get<16>(kv.first);
      //   cout <<  "," << get<17>(kv.first);
      //   cout <<  "," << get<18>(kv.first);
      //   cout <<  "," << get<19>(kv.first);
      //   cout <<  "," << get<20>(kv.first);
      //   cout <<  "," << get<21>(kv.first);
      //   cout <<  "," << get<22>(kv.first);
      //   cout <<  "," << get<23>(kv.first);
      //   cout <<  "," << get<24>(kv.first);
      //   cout <<  "," << get<25>(kv.first);
      //   cout << ")(" << get<26>(kv.first);
      //   cout <<  "," << get<27>(kv.first);
      //   cout <<  "," << get<28>(kv.first);
      //   cout <<  "," << get<29>(kv.first);
      //   cout <<  "," << get<30>(kv.first);
      //   cout <<  "," << get<31>(kv.first);
      //   cout <<  "," << get<32>(kv.first);
      //   cout <<  "," << get<33>(kv.first);
      //   cout <<  "," << get<34>(kv.first);
      //   cout <<  "," << get<35>(kv.first) << "))\n";
      //   for (auto kg : kv.second) {
      //      cout << "((" << get< 0>(kg);
      //      cout <<  "," << get< 1>(kg);
      //      cout <<  "," << get< 2>(kg);
      //      cout <<  "," << get< 3>(kg);
      //      cout <<  "," << get< 4>(kg);
      //      cout <<  "," << get< 5>(kg);
      //      cout <<  "," << get< 6>(kg);
      //      cout <<  "," << get< 7>(kg);
      //      cout <<  "," << get< 8>(kg);
      //      cout <<  "," << get< 9>(kg);
      //      cout <<  "," << get<10>(kg);
      //      cout <<  "," << get<11>(kg);
      //      cout <<  "," << get<12>(kg);
      //      cout <<  "," << get<13>(kg);
      //      cout <<  "," << get<14>(kg);
      //      cout <<  "," << get<15>(kg);
      //      cout <<  "," << get<16>(kg);
      //      cout <<  "," << get<17>(kg);
      //      cout <<  "," << get<18>(kg);
      //      cout <<  "," << get<19>(kg);
      //      cout <<  "," << get<20>(kg);
      //      cout <<  "," << get<21>(kg);
      //      cout <<  "," << get<22>(kg);
      //      cout <<  "," << get<23>(kg);
      //      cout <<  "," << get<24>(kg);
      //      cout <<  "," << get<25>(kg);
      //      cout << ")(" << get<26>(kg);
      //      cout <<  "," << get<27>(kg);
      //      cout <<  "," << get<28>(kg);
      //      cout <<  "," << get<29>(kg);
      //      cout <<  "," << get<30>(kg);
      //      cout <<  "," << get<31>(kg);
      //      cout <<  "," << get<32>(kg);
      //      cout <<  "," << get<33>(kg);
      //      cout <<  "," << get<34>(kg);
      //      cout <<  "," << get<35>(kg) << "))\n";
      //   }
      //}
      //cout << "\n";
   }
}


int main() {
   #ifdef THREE_D
      initialize_stuff();
      path_maker_3d();
      print_path_3d();
      path_finder_3d();
      print_path_search_3d(true); // true for just number of solutions
      print_answers_3d(true); // true for just number of solutions
      make_answer_tree_3d();
      print_answer_tree_3d(true); // true for just search width
   #endif
   #ifdef FOUR_D
      path_finder_4d();
      print_path_search_4d(true); // true for just number of solutions
   #endif
}
