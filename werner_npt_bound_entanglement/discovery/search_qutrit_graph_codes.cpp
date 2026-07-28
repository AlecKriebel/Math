// Discovery-only exact search over two-dimensional qutrit graph-state codes.
//
// Let |G_A> be the qutrit graph state with stabilizer labels
//     (X^t, Z^(A t)),  t in F_3^n,
// for a symmetric zero-diagonal adjacency matrix A.  For every nonzero
// syndrome s, search the rank-two projection onto
//     span{|G_A>, Z^s |G_A>}.
//
// All endpoint arithmetic is integral.  If N_T(S) counts stabilizers that
// are identity on T, and N_T(S Z^{-s}) counts elements of the indicated
// coset that are identity on T, then
//
//   6^n Q_n(P) / 2
//     = sum_T (-1)^|T| [
//         2^(n-|T|) 3^|T| N_T(S)
//         + 6^(n-|T|) N_{T^c}(S Z^{-s}) ].
//
// A negative integer would therefore be an exact witness within this
// finite ansatz.  Absence of one is discovery data only.

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <vector>

using i64 = std::int64_t;

static int ipow(int a, int n) {
  int z = 1;
  while (n-- > 0) z *= a;
  return z;
}

struct Search {
  int n;
  int n_subsets;
  int n_vectors;
  int n_edges;
  std::vector<std::vector<int>> vectors;
  std::vector<int> popcount;

  explicit Search(int n_)
      : n(n_),
        n_subsets(1 << n),
        n_vectors(ipow(3, n)),
        n_edges(n * (n - 1) / 2),
        vectors(n_vectors, std::vector<int>(n)),
        popcount(n_subsets) {
    for (int x = 0; x < n_vectors; ++x) {
      int y = x;
      for (int i = 0; i < n; ++i) {
        vectors[x][i] = y % 3;
        y /= 3;
      }
    }
    for (int mask = 0; mask < n_subsets; ++mask)
      popcount[mask] = __builtin_popcount(static_cast<unsigned>(mask));
  }

  std::vector<std::vector<int>> adjacency(int code) const {
    std::vector<std::vector<int>> A(n, std::vector<int>(n));
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        const int a = code % 3;
        code /= 3;
        A[i][j] = A[j][i] = a;
      }
    return A;
  }

  i64 evaluate(const std::vector<std::vector<int>>& A,
               const std::vector<int>& syndrome) const {
    std::vector<int> stabilizer_counts(n_subsets);
    std::vector<int> coset_counts(n_subsets);

    for (const auto& t : vectors) {
      int support_stabilizer = 0;
      int support_coset = 0;
      for (int i = 0; i < n; ++i) {
        int at = 0;
        for (int j = 0; j < n; ++j) at += A[i][j] * t[j];
        at %= 3;
        if (t[i] != 0 || at != 0) support_stabilizer |= 1 << i;
        int shifted = at - syndrome[i];
        shifted %= 3;
        if (shifted < 0) shifted += 3;
        if (t[i] != 0 || shifted != 0) support_coset |= 1 << i;
      }

      // The Pauli is identity on every site in mask iff its support is
      // disjoint from mask.
      for (int mask = 0; mask < n_subsets; ++mask) {
        if ((support_stabilizer & mask) == 0)
          ++stabilizer_counts[mask];
        if ((support_coset & mask) == 0) ++coset_counts[mask];
      }
    }

    i64 z = 0;
    const int all = n_subsets - 1;
    for (int mask = 0; mask < n_subsets; ++mask) {
      const int k = popcount[mask];
      const i64 sign = (k & 1) ? -1 : 1;
      const i64 diagonal_weight =
          static_cast<i64>(ipow(2, n - k)) * ipow(3, k);
      const i64 cross_weight = ipow(6, n - k);
      z += sign *
           (diagonal_weight * stabilizer_counts[mask] +
            cross_weight * coset_counts[all ^ mask]);
    }
    return z;
  }

  void run() const {
    const int n_graphs = ipow(3, n_edges);
    i64 best = std::numeric_limits<i64>::max();
    int best_graph = -1;
    int best_syndrome = -1;
    std::uint64_t tested = 0;
    for (int graph = 0; graph < n_graphs; ++graph) {
      const auto A = adjacency(graph);
      for (int s = 1; s < n_vectors; ++s) {
        const i64 value = evaluate(A, vectors[s]);
        ++tested;
        if (value < best) {
          best = value;
          best_graph = graph;
          best_syndrome = s;
        }
        if (value < 0) {
          std::cout << "NEGATIVE exact graph-code projection\n";
          std::cout << "n " << n << " graph " << graph
                    << " syndrome " << s << " scaled_half_Q " << value
                    << "\n";
          return;
        }
      }
    }
    std::cout << "no negative among " << tested << " codes\n";
    std::cout << "best scaled_half_Q " << best << " graph " << best_graph
              << " syndrome " << best_syndrome << "\n";
  }
};

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: search_qutrit_graph_codes n\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  if (n < 1 || n > 6) {
    std::cerr << "implemented for 1 <= n <= 6\n";
    return 2;
  }
  Search(n).run();
  return 0;
}
