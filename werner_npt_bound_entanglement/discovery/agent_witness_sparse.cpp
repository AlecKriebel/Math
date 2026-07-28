// Discovery-only exact-integer search over sparse real Schmidt factors.
//
// For alpha=-1/2 this computes
//   R(C,D) = 2^n <C,L_{-1/2}^{tensor n}(D)>
// exactly as a signed 64-bit integer.  A two-term span contains a negative
// vector exactly when R12^2 > R11 R22 (assuming the rank-one diagonals are
// nonnegative).  Random absence of such a pair is not proof.
//
// Build:
//   c++ -O3 -std=c++17 agent_witness_sparse.cpp -o agent_witness_sparse
// Run:
//   ./agent_witness_sparse <d> <n> <trials> <max_support> <seed>
//       [require_common_full_support]

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <random>
#include <utility>
#include <vector>

struct SparseVector {
  std::vector<std::pair<int, int>> x;  // (basis index, nonzero integer)
};

struct SparseMatrix {
  struct Entry { int a, b, z; };
  std::vector<Entry> x;
};

static int ipow(int a, int n) {
  int r = 1;
  while (n--) r *= a;
  return r;
}

static SparseVector random_sparse_vector(int D, int k, std::mt19937_64& rng) {
  std::vector<int> support(D);
  for (int i = 0; i < D; ++i) support[i] = i;
  std::shuffle(support.begin(), support.end(), rng);
  SparseVector v;
  for (int j = 0; j < k; ++j) {
    const int magnitude = 1 + int(rng() % 2);
    const int sign = (rng() & 1) ? 1 : -1;
    v.x.push_back({support[j], sign * magnitude});
  }
  return v;
}

static SparseVector mutate(const SparseVector& source, int D, int max_support,
                           std::mt19937_64& rng) {
  std::map<int, int> z;
  for (auto [i, a] : source.x) z[i] = a;
  const int changes = 1 + int(rng() % 3);
  for (int t = 0; t < changes; ++t) {
    const int action = int(rng() % 3);
    if (action == 0 && !z.empty()) {
      auto it = z.begin();
      std::advance(it, rng() % z.size());
      z.erase(it);
    } else if (action == 1 && int(z.size()) < max_support) {
      z[int(rng() % D)] = (rng() & 1) ? 1 : -1;
    } else if (!z.empty()) {
      auto it = z.begin();
      std::advance(it, rng() % z.size());
      it->second = -it->second;
    }
  }
  if (z.empty()) z[int(rng() % D)] = 1;
  SparseVector out;
  for (auto p : z) out.x.push_back(p);
  return out;
}

static SparseMatrix outer(const SparseVector& u, const SparseVector& v) {
  SparseMatrix C;
  for (auto [a, x] : u.x)
    for (auto [b, y] : v.x)
      C.x.push_back({a, b, x * y});
  return C;
}

static bool proportional(const SparseVector& u, const SparseVector& v) {
  std::map<int, int> a, b;
  for (auto [i,z] : u.x) a[i] = z;
  for (auto [i,z] : v.x) b[i] = z;
  if (a.size() != b.size() || a.empty()) return false;
  auto ia = a.begin(), ib = b.begin();
  const int x0 = ia->second, y0 = ib->second;
  for (; ia != a.end(); ++ia, ++ib) {
    if (ia->first != ib->first ||
        int64_t(ia->second) * y0 != int64_t(ib->second) * x0)
      return false;
  }
  return true;
}

static bool local_full_support(const SparseVector& u, const SparseVector& v,
                               int site, int d) {
  const int stride = ipow(d, site);
  std::map<std::pair<int,int>, std::vector<int64_t>> fibers;
  for (int r = 0; r < 2; ++r) {
    const SparseVector& w = (r == 0 ? u : v);
    for (auto [index,z] : w.x) {
      const int digit = (index / stride) % d;
      const int rest = index % stride + stride * (index / (stride * d));
      auto& f = fibers[{r,rest}];
      if (f.empty()) f.assign(d, 0);
      f[digit] = z;
    }
  }
  // This exact search is used with d=3.  Rank three is detected by one
  // nonzero scalar triple product of fiber columns.
  if (d != 3) return false;
  std::vector<std::vector<int64_t>> f;
  for (auto& kv : fibers) f.push_back(kv.second);
  for (size_t i = 0; i < f.size(); ++i)
    for (size_t j = i + 1; j < f.size(); ++j) {
      const int64_t c0 = f[i][1]*f[j][2] - f[i][2]*f[j][1];
      const int64_t c1 = f[i][2]*f[j][0] - f[i][0]*f[j][2];
      const int64_t c2 = f[i][0]*f[j][1] - f[i][1]*f[j][0];
      if (c0 == 0 && c1 == 0 && c2 == 0) continue;
      for (size_t k = j + 1; k < f.size(); ++k)
        if (c0*f[k][0] + c1*f[k][1] + c2*f[k][2] != 0)
          return true;
    }
  return false;
}

static bool common_full_site(const SparseVector& u1, const SparseVector& u2,
                             const SparseVector& v1, const SparseVector& v2,
                             int d, int n) {
  for (int site = 0; site < n; ++site)
    if (local_full_support(u1, u2, site, d) &&
        local_full_support(v1, v2, site, d))
      return true;
  return false;
}

// Matrix element of (2 I - T^* T)^{tensor n}.
static int kernel(int a, int b, int c, int e, int d, int n) {
  int z = 1;
  for (int site = 0; site < n; ++site) {
    const int ai = a % d, bi = b % d, ci = c % d, ei = e % d;
    const int local =
        2 * ((ai == ci && bi == ei) ? 1 : 0)
        - ((ai == bi && ci == ei) ? 1 : 0);
    z *= local;
    if (z == 0) return 0;
    a /= d; b /= d; c /= d; e /= d;
  }
  return z;
}

static int64_t form(const SparseMatrix& C, const SparseMatrix& D,
                    int d, int n) {
  int64_t s = 0;
  for (const auto& p : C.x)
    for (const auto& q : D.x)
      s += int64_t(p.z) * q.z * kernel(p.a, p.b, q.a, q.b, d, n);
  return s;
}

static void print_vector(const char* name, const SparseVector& u) {
  std::cout << name << " =";
  for (auto [i,z] : u.x) std::cout << " (" << i << "," << z << ")";
  std::cout << "\n";
}

int main(int argc, char** argv) {
  if (argc != 6 && argc != 7) {
    std::cerr << "usage: " << argv[0]
              << " d n trials max_support seed [require_common_full]\n";
    return 2;
  }
  const int d = std::atoi(argv[1]), n = std::atoi(argv[2]);
  const int trials = std::atoi(argv[3]);
  const int max_support = std::min(std::atoi(argv[4]), ipow(d, n));
  const uint64_t seed = std::strtoull(argv[5], nullptr, 10);
  const bool require_common_full = argc == 7 && std::atoi(argv[6]) != 0;
  const int D = ipow(d, n);
  std::mt19937_64 rng(seed);
  long double best_ratio = 0.0L;
  int64_t best11 = 0, best12 = 0, best22 = 0;
  SparseVector bu1, bv1, bu2, bv2;
  for (int trial = 0; trial < trials; ++trial) {
    const int k1 = 1 + int(rng() % max_support);
    const int l1 = 1 + int(rng() % max_support);
    SparseVector u1 = random_sparse_vector(D, k1, rng);
    SparseVector v1 = random_sparse_vector(D, l1, rng);
    // Half independent trials, half nearby pairs to encourage a large cross
    // term in the indefinite quadratic form.
    SparseVector u2, v2;
    if (rng() & 1) {
      u2 = random_sparse_vector(D, 1 + int(rng() % max_support), rng);
      v2 = random_sparse_vector(D, 1 + int(rng() % max_support), rng);
    } else {
      u2 = mutate(u1, D, max_support, rng);
      v2 = mutate(v1, D, max_support, rng);
    }
    // Deliberately sample Hermitian rank-two spans as well; these are easy to
    // miss under four independent sparse factors.
    if (rng() % 4 == 0) {
      v1 = u1;
      v2 = u2;
    }
    if (proportional(u1, u2) && proportional(v1, v2)) {
      --trial;
      continue;
    }
    if (require_common_full &&
        !common_full_site(u1, u2, v1, v2, d, n)) {
      --trial;
      continue;
    }
    SparseMatrix C1 = outer(u1, v1), C2 = outer(u2, v2);
    const int64_t r11 = form(C1, C1, d, n);
    const int64_t r12 = form(C1, C2, d, n);
    const int64_t r22 = form(C2, C2, d, n);
    if (r11 < 0 || r22 < 0 ||
        (__int128)r12 * r12 > (__int128)r11 * r22) {
      std::cout << "NEGATIVE TWO-TERM SPAN at trial " << trial << "\n";
      std::cout << "R11 " << r11 << " R12 " << r12
                << " R22 " << r22 << "\n";
      print_vector("u1", u1); print_vector("v1", v1);
      print_vector("u2", u2); print_vector("v2", v2);
      return 0;
    }
    if (r11 > 0 && r22 > 0) {
      const long double ratio =
          (long double)r12 * r12 / ((long double)r11 * r22);
      if (ratio > best_ratio) {
        best_ratio = ratio;
        best11 = r11; best12 = r12; best22 = r22;
        bu1=u1; bv1=v1; bu2=u2; bv2=v2;
      }
    }
  }
  std::cout.precision(18);
  std::cout << "no negative span; best squared cross ratio "
            << best_ratio << "\n";
  std::cout << "R11 " << best11 << " R12 " << best12
            << " R22 " << best22 << "\n";
  print_vector("u1", bu1); print_vector("v1", bv1);
  print_vector("u2", bu2); print_vector("v2", bv2);
}
