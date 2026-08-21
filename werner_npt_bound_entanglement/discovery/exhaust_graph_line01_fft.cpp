// Exhaustive exact Fourier search for the line (a,b)=(0,1).
//
// For f_A(t)=prod_i eta(t_i,(At)_i), eta(0,0)=-1 and eta=2
// otherwise, the fixed-line numerator is
//     Delta_01(A,s) = F_A(0)+F_A(s),
// where F_A is the ternary Fourier transform of f_A.  This program
// computes every F_A(s) simultaneously over Z[omega].

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

using i64 = std::int64_t;
using Eis = std::array<i64, 2>;  // a+b*omega, omega^2=-1-omega

static Eis add(Eis x, Eis y) { return {x[0] + y[0], x[1] + y[1]}; }
static Eis mul(Eis x, Eis y) {
  return {x[0] * y[0] - x[1] * y[1],
          x[0] * y[1] + x[1] * y[0] - x[1] * y[1]};
}

static int ipow(int a, int n) {
  int value = 1;
  while (n-- > 0) value *= a;
  return value;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: exhaust_graph_line01_fft n\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  if (n < 1 || n > 5) return 2;
  const int N = ipow(3, n);
  const int edges = n * (n - 1) / 2;
  const int graphs = ipow(3, edges);
  const std::array<Eis, 3> omega = {
      Eis{1, 0}, Eis{0, 1}, Eis{-1, -1}};

  std::vector<std::vector<int>> words(N, std::vector<int>(n));
  for (int code = 0; code < N; ++code) {
    int x = code;
    for (int i = 0; i < n; ++i) {
      words[code][i] = x % 3;
      x /= 3;
    }
  }

  i64 global_min_plus = std::numeric_limits<i64>::max();
  i64 global_min_minus = std::numeric_limits<i64>::max();
  std::uint64_t zeros = 0, bad_zero_without_active_isolate = 0;

  for (int graph = 0; graph < graphs; ++graph) {
    std::vector<std::vector<int>> A(n, std::vector<int>(n));
    int code = graph;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        A[i][j] = A[j][i] = code % 3;
        code /= 3;
      }

    std::vector<Eis> transform(N);
    for (int index = 0; index < N; ++index) {
      const auto& t = words[index];
      int weight = 0;
      for (int i = 0; i < n; ++i) {
        int at = 0;
        for (int j = 0; j < n; ++j) at += A[i][j] * t[j];
        at %= 3;
        if (t[i] != 0 || at != 0) ++weight;
      }
      const i64 value = ((n - weight) & 1 ? -1 : 1)
                        * (i64(1) << weight);
      transform[index] = {value, 0};
    }

    int stride = 1;
    for (int coordinate = 0; coordinate < n; ++coordinate) {
      for (int block = 0; block < N; block += 3 * stride)
        for (int offset = 0; offset < stride; ++offset) {
          const Eis x0 = transform[block + offset];
          const Eis x1 = transform[block + offset + stride];
          const Eis x2 = transform[block + offset + 2 * stride];
          transform[block + offset] = add(add(x0, x1), x2);
          transform[block + offset + stride] =
              add(add(x0, mul(omega[1], x1)), mul(omega[2], x2));
          transform[block + offset + 2 * stride] =
              add(add(x0, mul(omega[2], x1)), mul(omega[1], x2));
        }
      stride *= 3;
    }

    const i64 dc = transform[0][0];
    if (transform[0][1] != 0) return 3;
    for (int syndrome = 1; syndrome < N; ++syndrome) {
      if (transform[syndrome][1] != 0) {
        std::cerr << "non-real Fourier coefficient\n";
        return 3;
      }
      const i64 plus = dc + transform[syndrome][0];
      const i64 minus = dc - transform[syndrome][0];
      global_min_plus = std::min(global_min_plus, plus);
      global_min_minus = std::min(global_min_minus, minus);
      if (plus < 0 || minus < 0) {
        std::cout << "EXACT VIOLATION graph " << graph
                  << " syndrome " << syndrome << " F0 " << dc
                  << " Fs " << transform[syndrome][0] << "\n";
        return 0;
      }
      if (plus == 0) {
        ++zeros;
        bool active_isolate = false;
        for (int i = 0; i < n; ++i)
          if (words[syndrome][i] != 0) {
            bool isolate = true;
            for (int j = 0; j < n; ++j)
              if (A[i][j] != 0) isolate = false;
            active_isolate = active_isolate || isolate;
          }
        if (!active_isolate) ++bad_zero_without_active_isolate;
      }
    }
  }
  std::cout << "graphs " << graphs << " line instances "
            << std::uint64_t(graphs) * (N - 1)
            << " min(F0+Fs) " << global_min_plus
            << " min(F0-Fs) " << global_min_minus
            << " zeros " << zeros
            << " zeros_without_active_isolate "
            << bad_zero_without_active_isolate << "\n";
}
