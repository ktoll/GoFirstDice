#include <iostream>
#include <vector>
#include <string>
#include <math.h>

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
// path making
void path_column_maker_3d(int group, int old_maximum, int addition, unsigned int *** previous_path_column, unsigned int *** current_path_column) {
   unsigned int num_options;
   for (int i = 0; i < old_maximum + 1; i++) {
      if (previous_path_column[i]) {
         if (not current_path_column[i + addition]) {
            current_path_column[i + addition] = new unsigned int * [6];
            for (int j = 0; j < 6; j++) {
               current_path_column[i + addition][j] = NULL;
            }
         }
         num_options = 0;
         for (int j = 0; j < 6; j++) {
            if (previous_path_column[i][j]) {
               num_options += previous_path_column[i][j][1];
            }
         }
         current_path_column[i + addition][group] = new unsigned int [2];
         current_path_column[i + addition][group][0] = i;
         current_path_column[i + addition][group][1] = num_options;
      }
   }
}

void path_maker_3d(int n, unsigned int **** paths) {
   paths[0] = new unsigned int ** [n + 1];
   for (int i = 0; i < n + 1; i++) {
      paths[0][i] = NULL;
   }
   paths[0][0] = new unsigned int * [6];
   paths[0][n - 1] = new unsigned int * [6];
   paths[0][n] = new unsigned int * [6];
   for (int i = 0; i < 6; i++) {
      paths[0][0][i] = NULL;
      paths[0][n - 1][i] = NULL;
      paths[0][n][i] = NULL;
   }
   paths[0][n][0] = new unsigned int [2];
   paths[0][n][0][0] = 0;
   paths[0][n][0][1] = 1;
   paths[0][0][1] = new unsigned int [2];
   paths[0][0][1][0] = 0;
   paths[0][0][1][1] = 1;
   paths[0][n - 1][2] = new unsigned int [2];
   paths[0][n - 1][2][0] = 0;
   paths[0][n - 1][2][1] = 1;
   paths[0][n - 1][3] = new unsigned int [2];
   paths[0][n - 1][3][0] = 0;
   paths[0][n - 1][3][1] = 1;
   paths[0][0][4] = new unsigned int [2];
   paths[0][0][4][0] = 0;
   paths[0][0][4][1] = 1;
   paths[0][0][5] = new unsigned int [2];
   paths[0][0][5][0] = 0;
   paths[0][0][5][1] = 1;
   int maximum = n;
   int old_maximum = 0;
   for (int i = 0; i < n - 1; i++) {
      old_maximum = maximum;
      maximum += (i + 2) * (n - i - 1);
      paths[i + 1] = new unsigned int ** [maximum + 1];
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
void print_path_column_3d(int n, int column, unsigned int **** paths) {
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
                  cout << paths[column][i][j][0];
                  cout << "\n";
                  cout << "         num paths: ";
                  cout << paths[column][i][j][1];
                  cout << "\n";
               }
            }
         }
      }
   }
}


// path searching
vector<string> path_finder_recursive_3d(int n, int shares[], int translator[6][6], int w, unsigned int **** paths, int depth, string so_far) {
   cout << "depth ";
   cout << depth;
   cout << "\n";
   vector<string> solutions = {};
   int maximum;
   int likeliests[w][6] = {{-1}};
   long likeliest_quantity[w] = {-1};
   string likeliest_group[w] = {""};
   if (depth == 0) {
      maximum = 1;
   } else {
      maximum = 6;
   }
   for (int i = 0; i < maximum; i++) {
      cout << "group " + get_group_3d[i] + "\n";
      if (paths[n - depth - 1][shares[0]][i]) {
         bool good = true;
         int next_shares[6] = {-1, -1, -1, -1, -1, -1};
         long combined_path_options = paths[n - depth - 1][shares[0]][i][1];
         next_shares[0] = paths[n - depth - 1][shares[0]][i][0];
         //cout << paths[n - depth - 1][shares[0]][translator[0][i]][1];
         //cout << "\n";
         for (int j = 1; j < 6; j++) {
            if (paths[n - depth - 1][shares[j]][translator[j][i]]) {
               next_shares[j] = paths[n - depth - 1][shares[j]][translator[j][i]][0];
               combined_path_options += paths[n - depth - 1][shares[j]][translator[j][i]][1];
               //cout << paths[n - depth - 1][shares[j]][translator[j][i]][1];
               //cout << "\n";
            } else {
               good = false;
            }
         }
         cout << combined_path_options;
         cout << "\n";
         if (good) {
            int insertion_point = -1;
            for (int k = 0; k < w; k++) {
               if (combined_path_options >= likeliest_quantity[k]) {
                  if (insertion_point == -1) {
                     insertion_point = k;
                  }
               } else if (combined_path_options < -1) {
                  cout << "oh no!\n";
                  cout << combined_path_options;
                  cout << "\n";
               }
            }
            if (insertion_point > -1) {
               for (int k = w - 1; k > insertion_point; k--) {
                  for (int m = 0; m < 6; m++) {
                     likeliests[k][m] = likeliests[k - 1][m];
                  }
                  likeliest_quantity[k] = likeliest_quantity[k - 1];
                  likeliest_group[k] = likeliest_group[k - 1];
               }
               for (int m = 0; m < 6; m++) {
                  likeliests[insertion_point][m] = next_shares[m];
               }
               likeliest_quantity[insertion_point] = combined_path_options;
               likeliest_group[insertion_point] = get_group_3d[i];
            }
         }
      }
   }
   cout << "likeliest_quantity[0] ";
   cout << likeliest_quantity[0];
   cout << "\n";
   for (int k = 0; k < w; k++) {
      if (likeliest_quantity[k] > 0) {
         cout << "likeliest_group[k] ";
         cout << likeliest_group[k];
         cout << "\n";
         if (depth == n - 1) {
            solutions.push_back(so_far + likeliest_group[k]);
         } else {
            vector<string> more_solutions = path_finder_recursive_3d(n, likeliests[k], translator, w, paths, depth + 1, so_far + likeliest_group[k]);
            solutions.insert(solutions.end(), more_solutions.begin(), more_solutions.end());
         }
      }
   }
   return solutions; 
}

vector<string> path_finder_3d(int n, int share, int w, unsigned int **** paths) {
   int shares[6] = {share, share, share, share, share, share};
   int translator[6][6] = {{0, 1, 2, 3, 4, 5}, \
                           {1, 0, 4, 5, 2, 3}, \
                           {2, 3, 0, 1, 5, 4}, \
                           {4, 5, 1, 0, 3, 2}, \
                           {3, 2, 5, 4, 0, 1}, \
                           {5, 4, 3, 2, 1, 0}};
   return path_finder_recursive_3d(n, shares, translator, w, paths, 0, "");
}


// 4d ----------------------------------------------------------------------------------------------
// path making
void path_column_maker_4d(int group, int old_maximum, int old_maximum_cd, int maximum_cd, int num_abs, int add_cds, int addition, unsigned int **** previous_path_column, unsigned int **** current_path_column) {
   unsigned int num_options;
   for (int i = 0; i < old_maximum + 1; i++) {
      if (previous_path_column[i]) {
         for (int j = 0; j < old_maximum_cd + 1; j++) {
            if (previous_path_column[i][j]) {
               if (not current_path_column[i + addition + (num_abs * j)]) {
                  current_path_column[i + addition + (num_abs * j)] = new unsigned int ** [maximum_cd + 1];
                  for (int k = 0; k < maximum_cd + 1; k++) {
                     current_path_column[i + addition + (num_abs * j)][k] = NULL;
                  }
               }
               if (not current_path_column[i + addition + (num_abs * j)][j + add_cds]) {
                  current_path_column[i + addition + (num_abs * j)][j + add_cds] = new unsigned int * [24];
                  for (int k = 0; k < 24; k++) {
                     current_path_column[i + addition + (num_abs * j)][j + add_cds][k] = NULL;
                  }
               }
               num_options = 0;
               for (int k = 0; k < 24; k++) {
                  if (previous_path_column[i][j][k]) {
                     num_options += previous_path_column[i][j][k][2];
                  }
               }
               current_path_column[i + addition + (num_abs * j)][j + add_cds][group] = new unsigned int [3];
               current_path_column[i + addition + (num_abs * j)][j + add_cds][group][0] = i;
               current_path_column[i + addition + (num_abs * j)][j + add_cds][group][1] = j;
               current_path_column[i + addition + (num_abs * j)][j + add_cds][group][2] = num_options;
            }
         }
      }
   }
}

void path_maker_4d(int n, unsigned int ***** paths) {
   paths[0] = new unsigned int *** [n + 1];
   for (int i = 0; i < n + 1; i++) {
      paths[0][i] = NULL;
   }
   paths[0][0] = new unsigned int ** [2];
   paths[0][n - 1] = new unsigned int ** [2];
   paths[0][n] = new unsigned int ** [2];
   for (int i = 0; i < 2; i++) {
      paths[0][0][i] = NULL;
      paths[0][n - 1][i] = NULL;
      paths[0][n][i] = NULL;
   }
   paths[0][0][0] = new unsigned int * [24];
   paths[0][0][1] = new unsigned int * [24];
   paths[0][n - 1][0] = NULL;
   paths[0][n - 1][1] = new unsigned int * [24];
   paths[0][n][0] = NULL;
   paths[0][n][1] = new unsigned int * [24];
   for (int i = 0; i < 24; i++) {
      paths[0][0][0][i] = NULL;
      paths[0][0][1][i] = NULL;
      paths[0][n - 1][1][i] = NULL;
      paths[0][n][1][i] = NULL;
   }
   paths[0][n][1][0] = new unsigned int [3];
   paths[0][n][1][0][0] = 0;
   paths[0][n][1][0][1] = 0;
   paths[0][n][1][0][2] = 1;
   paths[0][0][0][1] = new unsigned int [3];
   paths[0][0][0][1][0] = 0;
   paths[0][0][0][1][1] = 0;
   paths[0][0][0][1][2] = 1;
   paths[0][0][1][2] = new unsigned int [3];
   paths[0][0][1][2][0] = 0;
   paths[0][0][1][2][1] = 0;
   paths[0][0][1][2][2] = 1;
   paths[0][0][1][3] = new unsigned int [3];
   paths[0][0][1][3][0] = 0;
   paths[0][0][1][3][1] = 0;
   paths[0][0][1][3][2] = 1;
   paths[0][0][0][4] = new unsigned int [3];
   paths[0][0][0][4][0] = 0;
   paths[0][0][0][4][1] = 0;
   paths[0][0][0][4][2] = 1;
   paths[0][0][0][5] = new unsigned int [3];
   paths[0][0][0][5][0] = 0;
   paths[0][0][0][5][1] = 0;
   paths[0][0][0][5][2] = 1;
   paths[0][n - 1][1][6] = new unsigned int [3];
   paths[0][n - 1][1][6][0] = 0;
   paths[0][n - 1][1][6][1] = 0;
   paths[0][n - 1][1][6][2] = 1;
   paths[0][0][0][7] = new unsigned int [3];
   paths[0][0][0][7][0] = 0;
   paths[0][0][0][7][1] = 0;
   paths[0][0][0][7][2] = 1;
   paths[0][n - 1][1][8] = new unsigned int [3];
   paths[0][n - 1][1][8][0] = 0;
   paths[0][n - 1][1][8][1] = 0;
   paths[0][n - 1][1][8][2] = 1;
   paths[0][n - 1][1][9] = new unsigned int [3];
   paths[0][n - 1][1][9][0] = 0;
   paths[0][n - 1][1][9][1] = 0;
   paths[0][n - 1][1][9][2] = 1;
   paths[0][0][0][10] = new unsigned int [3];
   paths[0][0][0][10][0] = 0;
   paths[0][0][0][10][1] = 0;
   paths[0][0][0][10][2] = 1;
   paths[0][0][0][11] = new unsigned int [3];
   paths[0][0][0][11][0] = 0;
   paths[0][0][0][11][1] = 0;
   paths[0][0][0][11][2] = 1;
   paths[0][0][1][12] = new unsigned int [3];
   paths[0][0][1][12][0] = 0;
   paths[0][0][1][12][1] = 0;
   paths[0][0][1][12][2] = 1;
   paths[0][0][1][13] = new unsigned int [3];
   paths[0][0][1][13][0] = 0;
   paths[0][0][1][13][1] = 0;
   paths[0][0][1][13][2] = 1;
   paths[0][0][1][14] = new unsigned int [3];
   paths[0][0][1][14][0] = 0;
   paths[0][0][1][14][1] = 0;
   paths[0][0][1][14][2] = 1;
   paths[0][0][1][15] = new unsigned int [3];
   paths[0][0][1][15][0] = 0;
   paths[0][0][1][15][1] = 0;
   paths[0][0][1][15][2] = 1;
   paths[0][0][1][16] = new unsigned int [3];
   paths[0][0][1][16][0] = 0;
   paths[0][0][1][16][1] = 0;
   paths[0][0][1][16][2] = 1;
   paths[0][0][1][17] = new unsigned int [3];
   paths[0][0][1][17][0] = 0;
   paths[0][0][1][17][1] = 0;
   paths[0][0][1][17][2] = 1;
   paths[0][0][0][18] = new unsigned int [3];
   paths[0][0][0][18][0] = 0;
   paths[0][0][0][18][1] = 0;
   paths[0][0][0][18][2] = 1;
   paths[0][0][0][19] = new unsigned int [3];
   paths[0][0][0][19][0] = 0;
   paths[0][0][0][19][1] = 0;
   paths[0][0][0][19][2] = 1;
   paths[0][0][0][20] = new unsigned int [3];
   paths[0][0][0][20][0] = 0;
   paths[0][0][0][20][1] = 0;
   paths[0][0][0][20][2] = 1;
   paths[0][0][0][21] = new unsigned int [3];
   paths[0][0][0][21][0] = 0;
   paths[0][0][0][21][1] = 0;
   paths[0][0][0][21][2] = 1;
   paths[0][0][0][22] = new unsigned int [3];
   paths[0][0][0][22][0] = 0;
   paths[0][0][0][22][1] = 0;
   paths[0][0][0][22][2] = 1;
   paths[0][0][0][23] = new unsigned int [3];
   paths[0][0][0][23][0] = 0;
   paths[0][0][0][23][1] = 0;
   paths[0][0][0][23][2] = 1;
   int maximum = n;
   int maximum_cd = 1;
   int old_maximum = 0;
   int old_maximum_cd = 0;
   for (int i = 0; i < n - 1; i++) {
      old_maximum = maximum;
      old_maximum_cd = maximum_cd;
      maximum += ((n - i - 1) * (i + 2)) + ((n - i - 1) * maximum_cd);
      maximum_cd += i + 2;
      paths[i + 1] = new unsigned int *** [maximum + 1];
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
void print_path_column_4d(int n, int column, unsigned int ***** paths) {
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
                        cout << paths[column][i][j][k][0];
                        cout << "\n";
                        cout << "         prev share_cd: ";
                        cout << paths[column][i][j][k][1];
                        cout << "\n";
                        cout << "         num paths: ";
                        cout << paths[column][i][j][k][2];
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
vector<string> path_finder_recursive_4d(int n, int shares[], int shares_cd[], int translator[24][24], int translator_cd[], int w, unsigned int ***** paths, int depth, string so_far) {
   vector<string> solutions = {};
   int maximum;
   int likeliests[w][24] = {{-1}};
   int likeliests_cd[w][12] = {{-1}};
   long likeliest_quantity[w] = {-1};
   string likeliest_group[w] = {""};
   for (int i = 0; i < w; i++) {
      likeliest_quantity[i] = -1;
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
      if (paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][i]) {
         bool good = true;
         int next_shares[24] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
         int next_shares_cd[12] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
         long combined_path_options = paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][i][2];
         next_shares[0] = paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][i][0];
         next_shares_cd[translator_cd[0]] = paths[n - depth - 1][shares[0]][shares_cd[translator_cd[0]]][i][1];
         for (int j = 1; j < 24; j++) {
            if (paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]]) {
               next_shares[j] = paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][0];
               combined_path_options += paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][2];
               if (next_shares_cd[translator_cd[j]] > -1) {
                  if (next_shares_cd[translator_cd[j]] != paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][1]) {
                     cout << "depth ";
                     cout << depth;
                     cout << "\n";
                     cout << "i ";
                     cout << i;
                     cout << "\n";
                     cout << "j ";
                     cout << j;
                     cout << "\n";
                     cout << "next_shares_cd[translator_cd[j]] ";
                     cout << next_shares_cd[translator_cd[j]];
                     cout << "\n";
                     cout << "paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][1] ";
                     cout << paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][1];
                     cout << "\n";
                     cout << "uh oh\n";
                     good = false;
                  }
               }
               next_shares_cd[translator_cd[j]] = paths[n - depth - 1][shares[j]][shares_cd[translator_cd[j]]][translator[j][i]][1];
            } else {
               good = false;
            }
         }
         if (good) {
            int insertion_point = -1;
            for (int k = 0; k < w; k++) {
               if (combined_path_options > likeliest_quantity[k]) {
                  if (insertion_point == -1) {
                     insertion_point = k;
                  }
               }
            }
            if (insertion_point > -1) {
               for (int k = w - 1; k > insertion_point; k--) {
                  for (int m = 0; m < 24; m++) {
                     likeliests[k][m] = likeliests[k - 1][m];
                  }
                  for (int m = 0; m < 12; m++) {
                     likeliests_cd[k][m] = likeliests_cd[k - 1][m];
                  }
                  likeliest_quantity[k] = likeliest_quantity[k - 1];
                  likeliest_group[k] = likeliest_group[k - 1];
               }
               for (int m = 0; m < 24; m++) {
                  likeliests[insertion_point][m] = next_shares[m];
               }
               for (int m = 0; m < 12; m++) {
                  likeliests_cd[insertion_point][m] = next_shares_cd[m];
               }
               likeliest_quantity[insertion_point] = combined_path_options;
               likeliest_group[insertion_point] = get_group_4d[i];
            }
         }
      }
   }
   for (int k = 0; k < w; k++) {
      if (likeliest_quantity[k] > 0) {
         if (depth == n - 1) {
            solutions.push_back(so_far + likeliest_group[k]);
         } else {
            vector<string> more_solutions = path_finder_recursive_4d(n, likeliests[k], likeliests_cd[k], translator, translator_cd, w, paths, depth + 1, so_far + likeliest_group[k]);
            solutions.insert(solutions.end(), more_solutions.begin(), more_solutions.end());
         }
      }
   }
   return solutions; 
}

vector<string> path_finder_4d(int n, int share, int w, unsigned int ***** paths) {
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
   return path_finder_recursive_4d(n, shares, shares_cd, translator, translator_cd, w, paths, 0, "");
}


int main() {
   int d = 3;
   int n = 24;
   int w = 1; // search width
   int share = pow(n, d) / factorial(d);
   if (d == 3) {
      unsigned int **** paths = new unsigned int *** [n];
      path_maker_3d(n, paths);
      vector<string> solutions = path_finder_3d(n, share, w, paths);
      for (string solution: solutions) {
         cout << solution + "\n";
      }
      //print_path_column_3d(n, 0, paths);
      //print_path_column_3d(n, 1, paths);
      //print_path_column_3d(n, n - 1, paths);
   } else if (d == 4) {
      unsigned int ***** paths = new unsigned int **** [n];
      path_maker_4d(n, paths);
      vector<string> solutions = path_finder_4d(n, share, w, paths);
      for (string solution: solutions) {
         cout << solution + "\n";
      }
      //print_path_column_4d(n, 0, paths);
      //print_path_column_4d(n, 1, paths);
      //print_path_column_4d(n, n - 1, paths);
   }
}
