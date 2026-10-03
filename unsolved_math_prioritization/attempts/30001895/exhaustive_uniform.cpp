#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

// Exhausts every simple r-uniform hypergraph on a fixed labelled n-vertex set.
// The complete edge set must have at most 24 members. No floating-point solver.
int main(int argc, char** argv) {
  if (argc != 3) return 2;
  int n = std::atoi(argv[1]), r = std::atoi(argv[2]);
  if (n < 1 || n > 20 || r < 1 || r > n) return 2;
  std::vector<uint32_t> edges;
  for (uint32_t e = 1; e < (1u << n); ++e)
    if (__builtin_popcount(e) == r) edges.push_back(e);
  int m = edges.size();
  if (m > 24) return 2;
  uint32_t N = 1u << m;
  std::vector<uint32_t> incident(n, 0);
  for (int e = 0; e < m; ++e)
    for (int v = 0; v < n; ++v)
      if (edges[e] & (1u << v)) incident[v] |= 1u << e;
  std::vector<uint8_t> tau(N, 0), packing(N, 0);
  uint64_t proper = 0, violations = 0, equalities = 0;
  for (uint32_t H = 1; H < N; ++H) {
    int first = __builtin_ctz(H), best_tau = n, delta = 0;
    for (int v = 0; v < n; ++v) {
      delta = std::max(delta, __builtin_popcount(H & incident[v]));
      if (edges[first] & (1u << v))
        best_tau = std::min(best_tau, 1 + int(tau[H & ~incident[v]]));
    }
    tau[H] = best_tau;
    if (delta <= r) packing[H] = __builtin_popcount(H);
    else {
      int best_pack = 0;
      for (uint32_t rest = H; rest; rest &= rest - 1) {
        uint32_t bit = rest & -rest;
        best_pack = std::max(best_pack, int(packing[H ^ bit]));
      }
      packing[H] = best_pack;
      ++proper;
      int gap = int(tau[H]) + r - 1 - int(packing[H]);
      equalities += (gap == 0);
      if (gap > 0) {
        ++violations;
        if (violations <= 10)
          std::cout << "VIOLATION mask=" << H << " tau=" << int(tau[H])
                    << " nu_r=" << int(packing[H]) << " delta=" << delta << '\n';
      }
    }
  }
  std::cout << "{\"n\":" << n << ",\"r\":" << r
            << ",\"complete_edges\":" << m << ",\"families\":" << N
            << ",\"delta_gt_r\":" << proper << ",\"equalities\":" << equalities
            << ",\"violations\":" << violations << "}\n";
  return violations ? 1 : 0;
}
