// Discovery-only exact search for qutrit graph-orbit endpoint violations.
//
// For a symmetric zero-diagonal A over F_3 and nonzero s, this evaluates
// K_{a,b} directly while visiting F_3^n in a ternary Gray order.  Every
// step changes one t-coordinate, so At and the two support counts can be
// updated in O(n).  All objective arithmetic is signed 64-bit integer
// arithmetic; n <= 20 keeps the trivial 3*6^n bound in range.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <vector>

using i64 = std::int64_t;

struct Result {
  std::array<std::array<i64, 3>, 2> K{};
  std::array<i64, 4> delta{};
};

struct Evaluator {
  int n;
  std::vector<i64> pow2;

  explicit Evaluator(int n_) : n(n_), pow2(n + 1, 1) {
    for (int i = 1; i <= n; ++i) pow2[i] = 2 * pow2[i - 1];
  }

  static int mod3(int x) {
    x %= 3;
    return x < 0 ? x + 3 : x;
  }

  Result evaluate(const std::vector<std::vector<int>>& A,
                  const std::vector<int>& s) const {
    Result out;
    std::vector<int> t(n), direction(n, 1), at(n);
    int dot = 0;
    int w0 = 0;
    int w1 = 0;
    for (int i = 0; i < n; ++i)
      if (s[i] != 0) ++w1;

    auto add_current = [&]() {
      const int b = mod3(-dot);
      const i64 v0 = ((n - w0) & 1 ? -1 : 1) * pow2[w0];
      const i64 v1 = ((n - w1) & 1 ? -1 : 1) * pow2[w1];
      out.K[0][b] += v0;
      out.K[1][b] += v1;
    };

    add_current();
    i64 remaining = 1;
    for (int i = 0; i < n; ++i) remaining *= 3;
    for (i64 step = 1; step < remaining; ++step) {
      int changed = 0;
      while (changed < n &&
             (t[changed] + direction[changed] < 0 ||
              t[changed] + direction[changed] > 2)) {
        ++changed;
      }
      if (changed == n) {
        std::cerr << "internal Gray-code failure\n";
        std::exit(3);
      }

      for (int j = 0; j < changed; ++j) direction[j] *= -1;
      const int increment = direction[changed];

      for (int j = 0; j < n; ++j) {
        w0 -= (t[j] != 0 || at[j] != 0);
        w1 -= (t[j] != 0 || mod3(at[j] + s[j]) != 0);
      }
      t[changed] += increment;
      dot = mod3(dot + increment * s[changed]);
      for (int j = 0; j < n; ++j)
        at[j] = mod3(at[j] + increment * A[j][changed]);
      for (int j = 0; j < n; ++j) {
        w0 += (t[j] != 0 || at[j] != 0);
        w1 += (t[j] != 0 || mod3(at[j] + s[j]) != 0);
      }
      add_current();
    }

    out.delta = {
        2 * out.K[0][0] + out.K[1][0],
        2 * out.K[0][0] + out.K[0][1],
        2 * out.K[0][0] + out.K[1][1],
        2 * out.K[0][0] + out.K[1][2],
    };
    return out;
  }
};

static void print_instance(const std::vector<std::vector<int>>& A,
                           const std::vector<int>& s,
                           const Result& result) {
  std::cout << "s";
  for (int x : s) std::cout << " " << x;
  std::cout << "\nA\n";
  for (const auto& row : A) {
    for (int x : row) std::cout << x;
    std::cout << "\n";
  }
  std::cout << "K00 " << result.K[0][0] << " K01 " << result.K[0][1]
            << " K10 " << result.K[1][0]
            << " K11 " << result.K[1][1]
            << " K12 " << result.K[1][2] << "\ndelta";
  for (i64 x : result.delta) std::cout << " " << x;
  std::cout << "\n";
}

int main(int argc, char** argv) {
  if (argc < 3 || argc > 5) {
    std::cerr << "usage: search_arbitrary_graph_codes_fast n samples [seed]"
                 " [apex]\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  const int samples = std::stoi(argv[2]);
  const std::uint64_t seed =
      argc >= 4 ? std::stoull(argv[3]) : UINT64_C(20260728);
  const bool apex_mode = argc == 5 && std::string(argv[4]) == "apex";
  if (n < 1 || n > 20 || samples < 1) return 2;

  std::mt19937_64 rng(seed);
  std::uniform_int_distribution<int> ternary(0, 2);
  Evaluator evaluator(n);
  i64 best_delta = std::numeric_limits<i64>::max();
  i64 best_nontrivial_k = std::numeric_limits<i64>::max();
  std::vector<std::vector<int>> best_A;
  std::vector<int> best_s;
  Result best_result;

  std::uint64_t tested = 0;
  for (int sample = 0; sample < samples; ++sample) {
    std::vector<std::vector<int>> A(n, std::vector<int>(n));
    const int first_random_vertex = apex_mode ? 1 : 0;
    for (int i = first_random_vertex; i < n; ++i)
      for (int j = i + 1; j < n; ++j)
        A[i][j] = A[j][i] = ternary(rng);
    std::vector<int> s(n);
    i64 neighborhoods = 1;
    if (apex_mode) {
      s[0] = 1;
      for (int i = 1; i < n; ++i) neighborhoods *= 3;
    } else {
      do {
        for (int& x : s) x = ternary(rng);
      } while (
          std::all_of(s.begin(), s.end(), [](int x) { return x == 0; }));
    }

    const i64 first_neighborhood = apex_mode ? 1 : 0;
    for (i64 neighborhood = first_neighborhood;
         neighborhood < neighborhoods; ++neighborhood) {
      if (apex_mode) {
        i64 code = neighborhood;
        for (int i = 1; i < n; ++i) {
          A[0][i] = A[i][0] = code % 3;
          code /= 3;
        }
      }
      const Result result = evaluator.evaluate(A, s);
      ++tested;
      const i64 local_delta =
          *std::min_element(result.delta.begin(), result.delta.end());
      const i64 local_k =
          std::min({result.K[0][1], result.K[1][0],
                    result.K[1][1], result.K[1][2]});
      best_nontrivial_k = std::min(best_nontrivial_k, local_k);
      if (local_delta < best_delta) {
        best_delta = local_delta;
        best_A = A;
        best_s = s;
        best_result = result;
        std::cout << "sample " << sample + 1 << " tested " << tested
                  << " best_delta " << best_delta
                  << " best_nontrivial_K " << best_nontrivial_k << "\n";
        print_instance(best_A, best_s, best_result);
      }
      if (local_delta < 0) {
        std::cout << "EXACT NEGATIVE FOUND\n";
        return 0;
      }
    }
  }
  std::cout << "no negative in " << tested << " exact instances\n";
  std::cout << "best_delta " << best_delta
            << " best_nontrivial_K " << best_nontrivial_k << "\n";
  print_instance(best_A, best_s, best_result);
}
