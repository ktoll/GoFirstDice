#include <iostream>
#include <vector>
#include <string>
#include <math.h>

using namespace std;

int factorial(int d) {
   int fact = 1;
   for (int i = 1; i <= d; i++) {
      fact *= i;
   }
   return fact;
}

void path_column_maker_3d(int group, int old_maximum, int addition, int *** previous_path_column, int *** current_path_column) {
   int num_options;
   for (int i = 0; i < old_maximum + 1; i++) {
      if (previous_path_column[i]) {
         if (not current_path_column[i + addition]) {
            current_path_column[i + addition] = new int * [6];
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
         current_path_column[i + addition][group] = new int [2];
         current_path_column[i + addition][group][0] = i;
         current_path_column[i + addition][group][1] = num_options;
      }
   }
}

void path_maker_3d(int n, int **** paths) {
   paths[0] = new int ** [n + 1];
   paths[0][0] = new int * [6];
   paths[0][n - 1] = new int * [6];
   paths[0][n] = new int * [6];
   for (int i = 0; i < 6; i++) {
      paths[0][0][i] = NULL;
      paths[0][n - 1][i] = NULL;
      paths[0][n][i] = NULL;
   }
   paths[0][n][0] = new int [2];
   paths[0][n][0][0] = 0;
   paths[0][n][0][1] = 1;
   paths[0][0][1] = new int [2];
   paths[0][0][1][0] = 0;
   paths[0][0][1][1] = 1;
   paths[0][n - 1][2] = new int [2];
   paths[0][n - 1][2][0] = 0;
   paths[0][n - 1][2][1] = 1;
   paths[0][n - 1][3] = new int [2];
   paths[0][n - 1][3][0] = 0;
   paths[0][n - 1][3][1] = 1;
   paths[0][0][4] = new int [2];
   paths[0][0][4][0] = 0;
   paths[0][0][4][1] = 1;
   paths[0][0][5] = new int [2];
   paths[0][0][5][0] = 0;
   paths[0][0][5][1] = 1;
   int maximum = n;
   int old_maximum = 0;
   for (int i = 0; i < n - 1; i++) {
      old_maximum = maximum;
      maximum += (i + 2) * (n - i - 1);
      paths[i + 1] = new int ** [maximum + 1];
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

void print_path_column(int n, int column, int **** paths) {
   cout << "column: ";
   cout << column;
   cout << "\n";
   int maximum = n;
   for (int i = 0; i < column; i++) {
      maximum += (i + 2) * (n - i - 1);
      paths[i] = new int ** [maximum];
      for (int j = 0; j < maximum; j++) {
         paths[i][j] = NULL;
      }
   }
   if (paths[column]) {
      for (int i = 0; i < maximum + 1; i++) {
         if (paths[column][i]) {
            cout << "   share: ";
            cout << i;
            cout << "\n";
            for (int j = 0; j < 6; j++) {
               if (paths[column][i][j]) {
                  if (j == 0) {
                     cout << "      abc\n";
                  } else if (j == 1) {
                     cout << "      acb\n";
                  } else if (j == 2) {
                     cout << "      bac\n";
                  } else if (j == 3) {
                     cout << "      bca\n";
                  } else if (j == 4) {
                     cout << "      cab\n";
                  } else if (j == 5) {
                     cout << "      cba\n";
                  }
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

void why(int **** paths) {
   cout << "&paths ";
   cout << &paths;
   cout << "\n";
   cout << "paths ";
   cout << paths;
   cout << "\n";
   cout << "&paths[0] ";
   cout << &paths[0];
   cout << "\n";
   cout << "paths[0] ";
   cout << paths[0];
   cout << "\n";
}

int main() {
   int d = 3;
   int n = 6;
   int share = pow(n, d) / factorial(d);
   if (d == 3) {
      int **** paths;
      paths = new int *** [n];
      path_maker_3d(n, paths);
      //why(paths);
      print_path_column(n, 0, paths);
      print_path_column(n, n - 1, paths);
   }
}
