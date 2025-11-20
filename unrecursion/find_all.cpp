#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <math.h>
#include <unordered_map>
#include <deque>

// Options: SEARCH_3d6
#define SEARCH_3d6

using namespace std;

static string get_group_3d[6] = {"abc", "acb", "bac", "bca", "cab", "cba"};
static string get_group_4d[24] = {"abcd", "abdc", "acbd", "acdb", "adbc", "adcb", "bacd", "badc", "bcad", "bcda", "bdac", "bdca", "cabd", "cadb", "cbad", "cbda", "cdab", "cdba", "dabc", "dacb", "dbac", "dbca", "dcab", "dcba"};


#ifdef SEARCH_3d6
   #define N 6
   #define HALF_COLS (N / 2)
   #define MAX_SHARE 16
   #define NUM_SHARES (MAX_SHARE + 1)
#endif


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


// global variables
int paths[HALF_COLS][NUM_SHARES][4];
btw_3d_map_t btw_map[HALF_COLS];
btw_3d_map_t joining;


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
   int group_to_grouptype[6][6] = {{3, 2, 1, 1, 2, 0},
                                   {2, 3, 2, 0, 1, 1},
                                   {1, 1, 3, 2, 0, 2},
                                   {2, 0, 2, 3, 1, 1},
                                   {1, 1, 0, 2, 3, 2},
                                   {0, 2, 1, 1, 2, 3}};
   int translator[6][6] = {{0, 1, 2, 3, 4, 5}, //from is abc, to is first index, perm is second index. result is perm.
                           {1, 0, 4, 5, 2, 3},
                           {2, 3, 0, 1, 5, 4},
                           {4, 5, 1, 0, 3, 2},
                           {3, 2, 5, 4, 0, 1},
                           {5, 4, 3, 2, 1, 0}};
   btw_map[0][make_tuple(N, N - 1, 0, 0, N - 1, 0)].push_back(make_tuple(make_tuple(0, 0, 0, 0, 0, 0), 0));
   for (int between = 1; between < HALF_COLS; between++) {
      for (auto kv : btw_map[between - 1]) {
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
void print_path_search_3d() {
   for (int between = 0; between < HALF_COLS; between++) {
      cout << "between columns " << between << " and " << between + 1 << " has " << btw_map[between].size() << "\n";
   }
   cout << "joining has " << joining.size() << "\n";
   for (int between = 0; between < HALF_COLS; between++) {
      for (auto kv : btw_map[between]) {
         cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ") ";
      }
      cout << "\n";
   }
   for (auto kv : joining) {
      cout << "(" << get<0>(kv.first) << ","  << get<1>(kv.first) << ","  << get<2>(kv.first) << ","  << get<3>(kv.first) << ","  << get<4>(kv.first) << ","  << get<5>(kv.first) << ") ";
   }
   cout << "\n";
}


int main() {
   path_maker_3d();
   print_path_3d();
   path_finder_3d();
   print_path_search_3d();
}
