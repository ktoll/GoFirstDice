#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <math.h>
#include <unordered_map>
#include <deque>

using namespace std;

static string get_group_3d[6] = {"abc", "acb", "bac", "bca", "cab", "cba"};
static string get_group_4d[24] = {"abcd", "abdc", "acbd", "acdb", "adbc", "adcb", "bacd", "badc", "bcad", "bcda", "bdac", "bdca", "cabd", "cadb", "cbad", "cbda", "cdab", "cdba", "dabc", "dacb", "dbac", "dbca", "dcab", "dcba"};


int factorial(int d) {
   int fact = 1;
   for (int i = 1; i <= d; i++) {
      fact *= i;
   }
   return fact;
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


// path making
void path_column_maker_3d(int group, int old_maximum, int addition, tuple<unsigned int, double> *** previous_path_column, tuple<unsigned int, double> *** current_path_column) {
   double num_options;
   for (unsigned int i = 0; i < old_maximum + 1; i++) {
      if (previous_path_column[i]) {
         if (not current_path_column[i + addition]) {
            current_path_column[i + addition] = new tuple<unsigned int, double> * [6];
            for (int j = 0; j < 6; j++) {
               current_path_column[i + addition][j] = NULL;
            }
         }
         num_options = 0;
         for (int j = 0; j < 6; j++) {
            if (previous_path_column[i][j]) {
               num_options += get<1>(*previous_path_column[i][j]);
            }
         }
         current_path_column[i + addition][group] = new tuple<unsigned int, double>;
         *current_path_column[i + addition][group] = make_tuple(i, num_options);
      }
   }
}

void path_maker_3d(int n, tuple<unsigned int, double> **** paths) {
   paths[0] = new tuple<unsigned int, double> ** [n + 1];
   for (int i = 0; i < n + 1; i++) {
      paths[0][i] = NULL;
   }
   paths[0][0] = new tuple<unsigned int, double> * [6];
   paths[0][n - 1] = new tuple<unsigned int, double> * [6];
   paths[0][n] = new tuple<unsigned int, double> * [6];
   for (int i = 0; i < 6; i++) {
      paths[0][0][i] = NULL;
      paths[0][n - 1][i] = NULL;
      paths[0][n][i] = NULL;
   }
   paths[0][n][0] = new tuple<unsigned int, double>;
   *paths[0][n][0] = make_tuple(0, 1);
   paths[0][0][1] = new tuple<unsigned int, double>;
   *paths[0][0][1] = make_tuple(0, 1);
   paths[0][n - 1][2] = new tuple<unsigned int, double>;
   *paths[0][n - 1][2] = make_tuple(0, 1);
   paths[0][n - 1][3] = new tuple<unsigned int, double>;
   *paths[0][n - 1][3] = make_tuple(0, 1);
   paths[0][0][4] = new tuple<unsigned int, double>;
   *paths[0][0][4] = make_tuple(0, 1);
   paths[0][0][5] = new tuple<unsigned int, double>;
   *paths[0][0][5] = make_tuple(0, 1);
   int maximum = n;
   int old_maximum = 0;
   for (int i = 0; i < n - 1; i++) {
      old_maximum = maximum;
      maximum += (i + 2) * (n - i - 1);
      paths[i + 1] = new tuple<unsigned int, double> ** [maximum + 1];
      for (int j = 0; j < maximum + 1; j++) {
         paths[i + 1][j] = NULL;
      }
      path_column_maker_3d(0, old_maximum, (n - i - 1) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_3d(1, old_maximum, (n - i - 1) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_3d(2, old_maximum, (n - i - 2) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_3d(3, old_maximum, (n - i - 2) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_3d(4, old_maximum, (n - i - 1) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_3d(5, old_maximum, (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
   }
}


// path printing
void print_path_column_3d(int n, int column, tuple<unsigned int, double> **** paths) {
   cout << "column: ";
   cout << column;
   cout << "\n";
   int maximum = n;
   for (int i = 0; i < column; i++) {
      maximum += (i + 2) * (n - i - 1);
   }
   if (paths[column]) {
      for (int i = 0; i < maximum + 1; i++) {
         if (paths[column][i]) {
            cout << "   share: ";
            cout << i;
            cout << "\n";
            for (int j = 0; j < 6; j++) {
               if (paths[column][i][j]) {
                  cout << "      ";
                  cout << get_group_3d[j];
                  cout << "\n";
                  cout << "         prev share: ";
                  cout << get<0>(*paths[column][i][j]);
                  cout << "\n";
                  cout << "         num paths: ";
                  cout << get<1>(*paths[column][i][j]);
                  cout << "\n";
               }
            }
         }
      }
   }
}


// path searching
void path_finder_one_step_3d(int n, int translator[6][6], tuple<unsigned int, double> **** paths, int depth, btw_3d_key_t btw_key, btw_3d_map_t btw_map[]) {
   int maximum;
   if (depth == 0) {
      maximum = 1;
   } else {
      maximum = 6;
   }
   for (int i = 0; i < maximum; i++) { // i is group we might assign
      bool good = true;
      int next_shares[6] = {-1, -1, -1, -1, -1, -1};
      // paths[column][shares][group]
      // j = 0
      if (paths[n - depth - 1][get<0>(btw_key)][translator[0][i]]) {
         next_shares[0] = get<0>(*paths[n - depth - 1][get<0>(btw_key)][translator[0][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<1>(btw_key)][translator[1][i]]) {
         next_shares[1] = get<0>(*paths[n - depth - 1][get<1>(btw_key)][translator[1][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<2>(btw_key)][translator[2][i]]) {
         next_shares[2] = get<0>(*paths[n - depth - 1][get<2>(btw_key)][translator[2][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<3>(btw_key)][translator[3][i]]) {
         next_shares[3] = get<0>(*paths[n - depth - 1][get<3>(btw_key)][translator[3][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<4>(btw_key)][translator[4][i]]) {
         next_shares[4] = get<0>(*paths[n - depth - 1][get<4>(btw_key)][translator[4][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<5>(btw_key)][translator[5][i]]) {
         next_shares[5] = get<0>(*paths[n - depth - 1][get<5>(btw_key)][translator[5][i]]);
      } else {
         good = false;
      }
      if (good) {
         btw_3d_key_t next_key = make_tuple(next_shares[0], next_shares[1], next_shares[2], next_shares[3], next_shares[4], next_shares[5]);
         tuple<btw_3d_key_t, int> prev_val = make_tuple(btw_key, i);
         if (btw_map[n - depth - 1].find(next_key) == btw_map[n - depth - 1].end()) {
            btw_map[n - depth - 1][next_key] = {};
         }
         btw_map[n - depth - 1][next_key].push_back(prev_val);
      }
   }
}

void path_finder_unrecursive_3d(int n, int translator[6][6], tuple<unsigned int, double> **** paths, int depth, btw_3d_map_t btw_map[]) {
   btw_map[n - depth - 1] = {};
   if (depth == 0) {
      int share = pow(n, 3) / 6;
      btw_3d_key_t shares = make_tuple(share, share, share, share, share, share);
      path_finder_one_step_3d(n, translator, paths, depth, shares, btw_map);
   }
   else {
      for (auto kv : btw_map[n - depth]) {
         path_finder_one_step_3d(n, translator, paths, depth, kv.first, btw_map);
      }
   }
}

vector<string> path_finder_recursive_3d(int n, btw_3d_key_t btw_key, btw_3d_map_t btw_map[], int depth, string so_far) {
   vector<string> solutions = {};
   for (auto d : btw_map[depth][btw_key]) {
      if (depth < n - 1) {
            vector<string> more_solutions = path_finder_recursive_3d(n, get<0>(d), btw_map, depth + 1, get_group_3d[get<1>(d)] + so_far);
            solutions.insert(solutions.end(), more_solutions.begin(), more_solutions.end());
      } else {
         solutions.push_back(get_group_3d[get<1>(d)] + so_far);
      }
   }
   return solutions;
}

vector<string> path_finder_3d(int n, int share, int w, tuple<unsigned int, double> **** paths) {
   int translator[6][6] = {{0, 1, 2, 3, 4, 5}, \
                           {1, 0, 4, 5, 2, 3}, \
                           {2, 3, 0, 1, 5, 4}, \
                           {4, 5, 1, 0, 3, 2}, \
                           {3, 2, 5, 4, 0, 1}, \
                           {5, 4, 3, 2, 1, 0}};
   btw_3d_map_t btw_map[n];
   for (int i = 0; i < n; i++) {
      path_finder_unrecursive_3d(n, translator, paths, i, btw_map);
   }
   vector<string> solutions = path_finder_recursive_3d(n, make_tuple(0, 0, 0, 0, 0, 0), btw_map, 0, "");
   return solutions;
}


// 4d ----------------------------------------------------------------------------------------------
// between tuple struct map queue stuff
typedef tuple<int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int> btw_4d_key_t; // 24 4 letter perms, 12 2 letter perms
typedef deque<tuple<btw_4d_key_t, int>> btw_4d_data_t; // perms, then group

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


// path making
void path_column_maker_4d(int group, int old_maximum, int old_maximum_cd, int maximum_cd, int num_abs, int add_cds, int addition, tuple<unsigned int, unsigned int, double> **** previous_path_column, tuple<unsigned int, unsigned int, double> **** current_path_column) {
   double num_options;
   for (unsigned int i = 0; i < old_maximum + 1; i++) {
      if (previous_path_column[i]) {
         for (unsigned int j = 0; j < old_maximum_cd + 1; j++) {
            if (previous_path_column[i][j]) {
               if (not current_path_column[i + addition + (num_abs * j)]) {
                  current_path_column[i + addition + (num_abs * j)] = new tuple<unsigned int, unsigned int, double> ** [maximum_cd + 1];
                  for (int k = 0; k < maximum_cd + 1; k++) {
                     current_path_column[i + addition + (num_abs * j)][k] = NULL;
                  }
               }
               if (not current_path_column[i + addition + (num_abs * j)][j + add_cds]) {
                  current_path_column[i + addition + (num_abs * j)][j + add_cds] = new tuple<unsigned int, unsigned int, double> * [24];
                  for (int k = 0; k < 24; k++) {
                     current_path_column[i + addition + (num_abs * j)][j + add_cds][k] = NULL;
                  }
               }
               num_options = 0;
               for (int k = 0; k < 24; k++) {
                  if (previous_path_column[i][j][k]) {
                     num_options += get<2>(*previous_path_column[i][j][k]);
                  }
               }
               current_path_column[i + addition + (num_abs * j)][j + add_cds][group] = new tuple<unsigned int, unsigned int, double>;
               *current_path_column[i + addition + (num_abs * j)][j + add_cds][group] = make_tuple(i, j, num_options);
            }
         }
      }
   }
}

void path_maker_4d(int n, tuple<unsigned int, unsigned int, double> ***** paths) {
   paths[0] = new tuple<unsigned int, unsigned int, double> *** [n + 1];
   for (int i = 0; i < n + 1; i++) {
      paths[0][i] = NULL;
   }
   paths[0][0] = new tuple<unsigned int, unsigned int, double> ** [2];
   paths[0][n - 1] = new tuple<unsigned int, unsigned int, double> ** [2];
   paths[0][n] = new tuple<unsigned int, unsigned int, double> ** [2];
   for (int i = 0; i < 2; i++) {
      paths[0][0][i] = NULL;
      paths[0][n - 1][i] = NULL;
      paths[0][n][i] = NULL;
   }
   paths[0][0][0] = new tuple<unsigned int, unsigned int, double>* [24];
   paths[0][0][1] = new tuple<unsigned int, unsigned int, double> * [24];
   paths[0][n - 1][0] = NULL;
   paths[0][n - 1][1] = new tuple<unsigned int, unsigned int, double> * [24];
   paths[0][n][0] = NULL;
   paths[0][n][1] = new tuple<unsigned int, unsigned int, double> * [24];
   for (int i = 0; i < 24; i++) {
      paths[0][0][0][i] = NULL;
      paths[0][0][1][i] = NULL;
      paths[0][n - 1][1][i] = NULL;
      paths[0][n][1][i] = NULL;
   }
   paths[0][n][1][0] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][n][1][0] = make_tuple(0, 0, 1);
   paths[0][0][0][1] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][1] = make_tuple(0, 0, 1);
   paths[0][0][1][2] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][2] = make_tuple(0, 0, 1);
   paths[0][0][1][3] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][3] = make_tuple(0, 0, 1);
   paths[0][0][0][4] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][4] = make_tuple(0, 0, 1);
   paths[0][0][0][5] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][5] = make_tuple(0, 0, 1);
   paths[0][n - 1][1][6] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][n - 1][1][6] = make_tuple(0, 0, 1);
   paths[0][0][0][7] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][7] = make_tuple(0, 0, 1);
   paths[0][n - 1][1][8] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][n - 1][1][8] = make_tuple(0, 0, 1);
   paths[0][n - 1][1][9] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][n - 1][1][9] = make_tuple(0, 0, 1);
   paths[0][0][0][10] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][10] = make_tuple(0, 0, 1);
   paths[0][0][0][11] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][11] = make_tuple(0, 0, 1);
   paths[0][0][1][12] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][12] = make_tuple(0, 0, 1);
   paths[0][0][1][13] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][13] = make_tuple(0, 0, 1);
   paths[0][0][1][14] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][14] = make_tuple(0, 0, 1);
   paths[0][0][1][15] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][15] = make_tuple(0, 0, 1);
   paths[0][0][1][16] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][16] = make_tuple(0, 0, 1);
   paths[0][0][1][17] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][1][17] = make_tuple(0, 0, 1);
   paths[0][0][0][18] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][18] = make_tuple(0, 0, 1);
   paths[0][0][0][19] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][19] = make_tuple(0, 0, 1);
   paths[0][0][0][20] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][20] = make_tuple(0, 0, 1);
   paths[0][0][0][21] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][21] = make_tuple(0, 0, 1);
   paths[0][0][0][22] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][22] = make_tuple(0, 0, 1);
   paths[0][0][0][23] = new tuple<unsigned int, unsigned int, double>;
   *paths[0][0][0][23] = make_tuple(0, 0, 1);
   int maximum = n;
   int maximum_cd = 1;
   int old_maximum = 0;
   int old_maximum_cd = 0;
   for (int i = 0; i < n - 1; i++) {
      old_maximum = maximum;
      old_maximum_cd = maximum_cd;
      maximum += ((n - i - 1) * (i + 2)) + ((n - i - 1) * maximum_cd);
      maximum_cd += i + 2;
      paths[i + 1] = new tuple<unsigned int, unsigned int, double> *** [maximum + 1];
      for (int j = 0; j < maximum + 1; j++) {
         paths[i + 1][j] = NULL;
      }
      path_column_maker_4d( 0, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2), (n - i - 1) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_4d( 1, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d( 2, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d( 3, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d( 4, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d( 5, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d( 6, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_4d( 7, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d( 8, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_4d( 9, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2), (n - i - 2) * (i + 2), paths[i], paths[i + 1]);
      path_column_maker_4d(10, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d(11, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d(12, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(13, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(14, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(15, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(16, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(17, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 2),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(18, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1), (n - i - 1) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d(19, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(20, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d(21, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1), (n - i - 2) * (i + 1), paths[i], paths[i + 1]);
      path_column_maker_4d(22, old_maximum, old_maximum_cd, maximum_cd, (n - i - 1), (i + 1),                     0, paths[i], paths[i + 1]);
      path_column_maker_4d(23, old_maximum, old_maximum_cd, maximum_cd, (n - i - 2), (i + 1),                     0, paths[i], paths[i + 1]);
   }
}


// path printing
void print_path_column_4d(int n, int column, tuple<unsigned int, unsigned int, double> ***** paths) {
   cout << "column: ";
   cout << column;
   cout << "\n";
   int maximum = n;
   int maximum_cd = 1;
   for (int i = 0; i < column; i++) {
      maximum += ((n - i - 1) * (i + 2)) + ((n - i - 1) * maximum_cd);
      maximum_cd += i + 2;
   }
   if (paths[column]) {
      for (int i = 0; i < maximum + 1; i++) {
         if (paths[column][i]) {
            cout << "   share: ";
            cout << i;
            cout << "\n";
            for (int j = 0; j < maximum_cd + 1; j++) {
               if (paths[column][i][j]) {
                  cout << "      share_cd: ";
                  cout << j;
                  cout << "\n";
                  for (int k = 0; k < 24; k++) {
                     if (paths[column][i][j][k]) {
                        cout << "         " + get_group_4d[k] + "\n";
                        cout << "         prev share: ";
                        cout << get<0>(*paths[column][i][j][k]);
                        cout << "\n";
                        cout << "         prev share_cd: ";
                        cout << get<1>(*paths[column][i][j][k]);
                        cout << "\n";
                        cout << "         num paths: ";
                        cout << get<2>(*paths[column][i][j][k]);
                        cout << "\n";
                     }
                  }
               }
            }
         }
      }
   }
}


// path searching
void path_finder_one_step_4d(int n, int translator[24][24], int translator_cd[24], tuple<unsigned int, unsigned int, double> ***** paths, int depth, btw_4d_key_t btw_key, btw_4d_map_t btw_map[]) {
   int maximum;
   if (depth == 0) {
      maximum = 1;
   } else {
      maximum = 24;
   }
   for (int i = 0; i < maximum; i++) { // i is group we might assign
      bool good = true;
      int next_shares[36] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
      // paths[column][shares][group]
      // j = 0
      //cout << n - depth - 1 << " " << get<0>(btw_key) << " " << get<24 + 8>(btw_key) << " " << translator[0][i] << "\n";
      //cout << "paths[n - depth - 1] = " << paths[n - depth - 1] << "\n";
      //cout << "paths[n - depth - 1][get<0>(btw_key)] = " << paths[n - depth - 1][get<0>(btw_key)] << "\n";
      //cout << "paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)] = " << paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)] << "\n";
      //cout << "paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)][translator[0][i]] = " << paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)][translator[0][i]] << "\n";
      if (paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)][translator[0][i]]) {
         next_shares[0] = get<0>(*paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)][translator[0][i]]);
         next_shares[24 + 8] = get<1>(*paths[n - depth - 1][get<0>(btw_key)][get<24 + 8>(btw_key)][translator[0][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<1>(btw_key)][get<24 + 11>(btw_key)][translator[1][i]]) {
         next_shares[1] = get<0>(*paths[n - depth - 1][get<1>(btw_key)][get<24 + 11>(btw_key)][translator[1][i]]);
         next_shares[24 + 11] = get<1>(*paths[n - depth - 1][get<1>(btw_key)][get<24 + 11>(btw_key)][translator[1][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<2>(btw_key)][get<24 + 5>(btw_key)][translator[2][i]]) {
         next_shares[2] = get<0>(*paths[n - depth - 1][get<2>(btw_key)][get<24 + 5>(btw_key)][translator[2][i]]);
         next_shares[24 + 5] = get<1>(*paths[n - depth - 1][get<2>(btw_key)][get<24 + 5>(btw_key)][translator[2][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<3>(btw_key)][get<24 + 10>(btw_key)][translator[3][i]]) {
         next_shares[3] = get<0>(*paths[n - depth - 1][get<3>(btw_key)][get<24 + 10>(btw_key)][translator[3][i]]);
         next_shares[24 + 10] = get<1>(*paths[n - depth - 1][get<3>(btw_key)][get<24 + 10>(btw_key)][translator[3][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<4>(btw_key)][get<24 + 4>(btw_key)][translator[4][i]]) {
         next_shares[4] = get<0>(*paths[n - depth - 1][get<4>(btw_key)][get<24 + 4>(btw_key)][translator[4][i]]);
         next_shares[24 + 4] = get<1>(*paths[n - depth - 1][get<4>(btw_key)][get<24 + 4>(btw_key)][translator[4][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<5>(btw_key)][get<24 + 7>(btw_key)][translator[5][i]]) {
         next_shares[5] = get<0>(*paths[n - depth - 1][get<5>(btw_key)][get<24 + 7>(btw_key)][translator[5][i]]);
         next_shares[24 + 7] = get<1>(*paths[n - depth - 1][get<5>(btw_key)][get<24 + 7>(btw_key)][translator[5][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<6>(btw_key)][get<24 + 8>(btw_key)][translator[6][i]]) {
         next_shares[6] = get<0>(*paths[n - depth - 1][get<6>(btw_key)][get<24 + 8>(btw_key)][translator[6][i]]);
         next_shares[24 + 8] = get<1>(*paths[n - depth - 1][get<6>(btw_key)][get<24 + 8>(btw_key)][translator[6][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<7>(btw_key)][get<24 + 11>(btw_key)][translator[7][i]]) {
         next_shares[7] = get<0>(*paths[n - depth - 1][get<7>(btw_key)][get<24 + 11>(btw_key)][translator[7][i]]);
         next_shares[24 + 11] = get<1>(*paths[n - depth - 1][get<7>(btw_key)][get<24 + 11>(btw_key)][translator[7][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<8>(btw_key)][get<24 + 2>(btw_key)][translator[8][i]]) {
         next_shares[8] = get<0>(*paths[n - depth - 1][get<8>(btw_key)][get<24 + 2>(btw_key)][translator[8][i]]);
         next_shares[24 + 2] = get<1>(*paths[n - depth - 1][get<8>(btw_key)][get<24 + 2>(btw_key)][translator[8][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<9>(btw_key)][get<24 + 9>(btw_key)][translator[9][i]]) {
         next_shares[9] = get<0>(*paths[n - depth - 1][get<9>(btw_key)][get<24 + 9>(btw_key)][translator[9][i]]);
         next_shares[24 + 9] = get<1>(*paths[n - depth - 1][get<9>(btw_key)][get<24 + 9>(btw_key)][translator[9][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<10>(btw_key)][get<24 + 1>(btw_key)][translator[10][i]]) {
         next_shares[10] = get<0>(*paths[n - depth - 1][get<10>(btw_key)][get<24 + 1>(btw_key)][translator[10][i]]);
         next_shares[24 + 1] = get<1>(*paths[n - depth - 1][get<10>(btw_key)][get<24 + 1>(btw_key)][translator[10][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<11>(btw_key)][get<24 + 6>(btw_key)][translator[11][i]]) {
         next_shares[11] = get<0>(*paths[n - depth - 1][get<11>(btw_key)][get<24 + 6>(btw_key)][translator[11][i]]);
         next_shares[24 + 6] = get<1>(*paths[n - depth - 1][get<11>(btw_key)][get<24 + 6>(btw_key)][translator[11][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<12>(btw_key)][get<24 + 5>(btw_key)][translator[12][i]]) {
         next_shares[12] = get<0>(*paths[n - depth - 1][get<12>(btw_key)][get<24 + 5>(btw_key)][translator[12][i]]);
         next_shares[24 + 5] = get<1>(*paths[n - depth - 1][get<12>(btw_key)][get<24 + 5>(btw_key)][translator[12][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<13>(btw_key)][get<24 + 10>(btw_key)][translator[13][i]]) {
         next_shares[13] = get<0>(*paths[n - depth - 1][get<13>(btw_key)][get<24 + 10>(btw_key)][translator[13][i]]);
         next_shares[24 + 10] = get<1>(*paths[n - depth - 1][get<13>(btw_key)][get<24 + 10>(btw_key)][translator[13][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<14>(btw_key)][get<24 + 2>(btw_key)][translator[14][i]]) {
         next_shares[14] = get<0>(*paths[n - depth - 1][get<14>(btw_key)][get<24 + 2>(btw_key)][translator[14][i]]);
         next_shares[24 + 2] = get<1>(*paths[n - depth - 1][get<14>(btw_key)][get<24 + 2>(btw_key)][translator[14][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<15>(btw_key)][get<24 + 9>(btw_key)][translator[15][i]]) {
         next_shares[15] = get<0>(*paths[n - depth - 1][get<15>(btw_key)][get<24 + 9>(btw_key)][translator[15][i]]);
         next_shares[24 + 9] = get<1>(*paths[n - depth - 1][get<15>(btw_key)][get<24 + 9>(btw_key)][translator[15][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<16>(btw_key)][get<24 + 0>(btw_key)][translator[16][i]]) {
         next_shares[16] = get<0>(*paths[n - depth - 1][get<16>(btw_key)][get<24 + 0>(btw_key)][translator[16][i]]);
         next_shares[24 + 0] = get<1>(*paths[n - depth - 1][get<16>(btw_key)][get<24 + 0>(btw_key)][translator[16][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<17>(btw_key)][get<24 + 3>(btw_key)][translator[17][i]]) {
         next_shares[17] = get<0>(*paths[n - depth - 1][get<17>(btw_key)][get<24 + 3>(btw_key)][translator[17][i]]);
         next_shares[24 + 3] = get<1>(*paths[n - depth - 1][get<17>(btw_key)][get<24 + 3>(btw_key)][translator[17][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<18>(btw_key)][get<24 + 4>(btw_key)][translator[18][i]]) {
         next_shares[18] = get<0>(*paths[n - depth - 1][get<18>(btw_key)][get<24 + 4>(btw_key)][translator[18][i]]);
         next_shares[24 + 4] = get<1>(*paths[n - depth - 1][get<18>(btw_key)][get<24 + 4>(btw_key)][translator[18][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<19>(btw_key)][get<24 + 7>(btw_key)][translator[19][i]]) {
         next_shares[19] = get<0>(*paths[n - depth - 1][get<19>(btw_key)][get<24 + 7>(btw_key)][translator[19][i]]);
         next_shares[24 + 7] = get<1>(*paths[n - depth - 1][get<19>(btw_key)][get<24 + 7>(btw_key)][translator[19][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<20>(btw_key)][get<24 + 1>(btw_key)][translator[20][i]]) {
         next_shares[20] = get<0>(*paths[n - depth - 1][get<20>(btw_key)][get<24 + 1>(btw_key)][translator[20][i]]);
         next_shares[24 + 1] = get<1>(*paths[n - depth - 1][get<20>(btw_key)][get<24 + 1>(btw_key)][translator[20][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<21>(btw_key)][get<24 + 6>(btw_key)][translator[21][i]]) {
         next_shares[21] = get<0>(*paths[n - depth - 1][get<21>(btw_key)][get<24 + 6>(btw_key)][translator[21][i]]);
         next_shares[24 + 6] = get<1>(*paths[n - depth - 1][get<21>(btw_key)][get<24 + 6>(btw_key)][translator[21][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<22>(btw_key)][get<24 + 0>(btw_key)][translator[22][i]]) {
         next_shares[22] = get<0>(*paths[n - depth - 1][get<22>(btw_key)][get<24 + 0>(btw_key)][translator[22][i]]);
         next_shares[24 + 0] = get<1>(*paths[n - depth - 1][get<22>(btw_key)][get<24 + 0>(btw_key)][translator[22][i]]);
      } else {
         good = false;
      }
      if (paths[n - depth - 1][get<23>(btw_key)][get<24 + 3>(btw_key)][translator[23][i]]) {
         next_shares[23] = get<0>(*paths[n - depth - 1][get<23>(btw_key)][get<24 + 3>(btw_key)][translator[23][i]]);
         next_shares[24 + 3] = get<1>(*paths[n - depth - 1][get<23>(btw_key)][get<24 + 3>(btw_key)][translator[23][i]]);
      } else {
         good = false;
      }
      if (good) {
         btw_4d_key_t next_key = make_tuple(next_shares[0], next_shares[1], next_shares[2], next_shares[3], next_shares[4], next_shares[5], next_shares[6], next_shares[7], next_shares[8], next_shares[9], next_shares[10], next_shares[11], next_shares[12], next_shares[13], next_shares[14], next_shares[15], next_shares[16], next_shares[17], next_shares[18], next_shares[19], next_shares[20], next_shares[21], next_shares[22], next_shares[23], next_shares[24], next_shares[25], next_shares[26], next_shares[27], next_shares[28], next_shares[29], next_shares[30], next_shares[31], next_shares[32], next_shares[33], next_shares[34], next_shares[35]);
         tuple<btw_4d_key_t, int> prev_val = make_tuple(btw_key, i);
         if (btw_map[n - depth - 1].find(next_key) == btw_map[n - depth - 1].end()) {
            btw_map[n - depth - 1][next_key] = {};
         }
         btw_map[n - depth - 1][next_key].push_back(prev_val);
      }
   }
}

void path_finder_unrecursive_4d(int n, int translator[24][24], int translator_cd[24], tuple<unsigned int, unsigned int, double> ***** paths, int depth, btw_4d_map_t btw_map[]) {
   cout << depth << "\n";
   btw_map[n - depth - 1] = {};
   if (depth == 0) {
      int share = pow(n, 4) / 24;
      int share_cd = pow(n, 2) / 2;
      btw_4d_key_t shares = make_tuple(share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd, share_cd);
      path_finder_one_step_4d(n, translator, translator_cd, paths, depth, shares, btw_map);
      cout << 1 << "\n";
   }
   else {
      for (auto kv : btw_map[n - depth]) {
         path_finder_one_step_4d(n, translator, translator_cd, paths, depth, kv.first, btw_map);
      }
      cout << btw_map[n - depth - 1].size() << "\n";
   }
}

vector<string> path_finder_recursive_4d(int n, btw_4d_key_t btw_key, btw_4d_map_t btw_map[], int depth, string so_far) {
   vector<string> solutions = {};
   for (auto d : btw_map[depth][btw_key]) {
      if (depth < n - 1) {
            vector<string> more_solutions = path_finder_recursive_4d(n, get<0>(d), btw_map, depth + 1, get_group_4d[get<1>(d)] + so_far);
            solutions.insert(solutions.end(), more_solutions.begin(), more_solutions.end());
      } else {
         solutions.push_back(get_group_4d[get<1>(d)] + so_far);
      }
   }
   return solutions;
}

vector<string> path_finder_4d(int n, int share, int w, tuple<unsigned int, unsigned int, double> ***** paths) {
   int translator[24][24] = {{ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}, \
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
   int translator_cd[24] =   { 8, 11,  5, 10,  4,  7,  8, 11,  2,  9,  1,  6,  5, 10,  2,  9,  0,  3,  4,  7,  1,  6,  0,  3};
   btw_4d_map_t btw_map[n];
   for (int i = 0; i < n; i++) {
      path_finder_unrecursive_4d(n, translator, translator_cd, paths, i, btw_map);
   }
   return path_finder_recursive_4d(n, make_tuple(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), btw_map, 0, "");
}


// path search analysis
int evaluate_distance(int current_group, tuple<unsigned int, unsigned int, double> ***** paths, int shares[], int shares_cd[], int translator[24][24], int translator_cd[], int column) {
   int distance = 0;
   double cmpval = 0;
   double cmpval2 = 0;
   bool good = true;
   for (int j = 0; j < 24; j++) {
      if (paths[column][shares[j]][shares_cd[translator_cd[j]]][translator[j][current_group]]) {
         cmpval += get<2>(*paths[column][shares[j]][shares_cd[translator_cd[j]]][translator[j][current_group]]);
      }
   }
   for (int i = 0; i < 24; i++) {
      cmpval2 = 0;
      for (int j = 0; j < 24; j++) {
         if (paths[column][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]) {
            cmpval2 += get<2>(*paths[column][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]);
         } else {
            good = false;
         }
      }
      if (good && (cmpval2 > cmpval) && (i != current_group)) {
         distance++;
      }
   }
   return distance;
}

void path_analysis_recursive_4d(int n, int shares[], int shares_cd[], int translator[24][24], int translator_cd[], int w, tuple<unsigned int, unsigned int, double> ***** paths, int depth, string solution) {
   //cout << "depth " << depth << "\n";
   //cout << solution.substr(depth * 4, 4) << "\n";
   //for (int i = 0; i < 24; i++) {
   //   cout << shares[i] << " ";
   //}
   //cout << "\n";
   //for (int i = 0; i < 12; i++) {
   //   cout << shares_cd[i] << " ";
   //}
   //cout << "\n";
   int current_group = -1;
   for (int i = 0; i < 24; i++) {
      if (solution.substr(depth * 4, 4) == get_group_4d[i]) {
         current_group = i;
      }
   }
   if (current_group < 0) {
      cout << "oh nooo\n";
      return;
   }
   int maximum;
   int likeliests[w][24] = {{-1}};
   int likeliests_cd[w][12] = {{-1}};
   double likeliest_quantity[w] = {0};
   string likeliest_group[w] = {""};
   for (int i = 0; i < w; i++) {
      likeliest_quantity[i] = 0;
      likeliest_group[i] = "";
      for (int j = 0; j < 24; j++) {
         likeliests[i][j] = -1;
      }
      for (int j = 0; j < 12; j++) {
         likeliests_cd[i][j] = -1;
      }
   }
   if (depth == 0) {
      maximum = 1;
   } else {
      maximum = 24;
   }
   for (int i = 0; i < maximum; i++) {
      if (paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][translator[0][i]]) {
         bool good = true;
         int next_shares[24] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
         int next_shares_cd[12] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
         double combined_path_options = get<2>(*paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][translator[0][i]]);
         next_shares[0] = get<0>(*paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][translator[0][i]]);
         next_shares_cd[translator_cd[0]] = get<1>(*paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][translator[0][i]]);
         for (int j = 1; j < 24; j++) {
            if (paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]) {
               next_shares[j] = get<0>(*paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]);
               combined_path_options += get<2>(*paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]);
               if (next_shares_cd[translator_cd[j]] > -1) {
                  if (next_shares_cd[translator_cd[j]] != get<1>(*paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]])) {
                     cout << "uh oh\n";
                     good = false;
                  }
               }
               next_shares_cd[translator_cd[j]] = get<1>(*paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]);
            } else {
               good = false;
            }
         }
         if (good) {
            //cout << "option: " << get_group_4d[i] << " " << combined_path_options;
            //for (int g = 0; g < 24; g++) {
            //   cout << " " << get<0>(*paths[n - depth - 1][shares[g]][shares_cd[translator_cd[g]]][translator[g][i]]);
            //}
            if (current_group == i) {
               //cout << " should pick!\n";
               for (int m = 0; m < 24; m++) {
                  likeliests[0][m] = next_shares[m];
               }
               for (int m = 0; m < 12; m++) {
                  likeliests_cd[0][m] = next_shares_cd[m];
               }
            }
            //else {
            //   cout << "\n";
            //}
         }
      }
   }
   cout << evaluate_distance(current_group, paths, shares, shares_cd, translator, translator_cd, n - depth - 1) << " ";
   for (int k = 0; k < w; k++) {
      if (depth == n - 1) {
      } else {
         path_analysis_recursive_4d(n, likeliests[k], likeliests_cd[k], translator, translator_cd, w, paths, depth + 1, solution);
      }
   }
}

void path_analysis_4d(int n, int share, int w, tuple<unsigned int, unsigned int, double> ***** paths, string solution) {
   cout << solution << "\n";
   int share_cd = pow(n, 2) / factorial(2);
   int shares[24] = {share};
   for (int i = 0; i < 24; i++) {
      shares[i] = share;
   }
   int shares_cd[12] = {share_cd};
   for (int i = 0; i < 12; i++) {
      shares_cd[i] = share_cd;
   }
   int translator[24][24] = {{ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}, \
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
   int translator_cd[24] =   { 8, 11,  5, 10,  4,  7,  8, 11,  2,  9,  1,  6,  5, 10,  2,  9,  0,  3,  4,  7,  1,  6,  0,  3};
   path_analysis_recursive_4d(n, shares, shares_cd, translator, translator_cd, 1, paths, 0, solution);
   cout << "\n";
}


int main() {
   int d = 4;
   int n = 12;
   int w = 24; // search width
   int share = pow(n, d) / factorial(d);
   // max order of magnitude
   double magnitude = 0;
   for (int i = 0; i < n; i++) {
      magnitude += pow(w, i);
   }
//   cout << magnitude << "\n";
   if (d == 3) {
      tuple<unsigned int, double> **** paths = new tuple<unsigned int, double> *** [n];
      path_maker_3d(n, paths);
      vector<string> solutions = path_finder_3d(n, share, w, paths);
      for (string solution: solutions) {
         cout << solution + "\n";
      }
      //print_path_column_3d(n, 0, paths);
      //print_path_column_3d(n, 1, paths);
      //print_path_column_3d(n, n - 1, paths);
   } else if (d == 4) {
      tuple<unsigned int, unsigned int, double> ***** paths = new tuple<unsigned int, unsigned int, double> **** [n];
      path_maker_4d(n, paths);
      //print_path_column_4d(n, 0, paths);
      //print_path_column_4d(n, 1, paths);
      //print_path_column_4d(n, 2, paths);
      //print_path_column_4d(n, 3, paths);
      //print_path_column_4d(n, 4, paths);
      //print_path_column_4d(n, n - 1, paths);
      vector<string> solutions = path_finder_4d(n, share, w, paths);
      //for (string solution: solutions) {
      //   cout << solution + "\n";
      //}
      for (string solution: solutions) {
         path_analysis_4d(n, share, 1, paths, solution);
      }
      //print_path_column_4d(n, 0, paths);
      //print_path_column_4d(n, 1, paths);
      //print_path_column_4d(n, n - 1, paths);
   }
}
