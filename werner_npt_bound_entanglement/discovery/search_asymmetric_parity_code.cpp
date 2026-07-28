// Discovery-only optimization of an asymmetric extension of the exact
// all-copy parity family.
//
//   u = a0 |1...1> + sum_i a_i |e_i>
//   v = b0 |0...0> + sum_i b_i |1...1-e_i>.
//
// The supports are disjoint for n >= 3, so normalized u,v are orthogonal
// and P=|u><u|+|v><v| is an exact rank-two code projection.  The objective
// is evaluated directly from the one-site matrix-unit pairing
//
//   B(E_ab,E_cd)=delta_ac delta_bd - (1/2)delta_ab delta_cd.
//
// Floating-point output is discovery data only.
//
// Build:
//   c++ -O3 -std=c++17 search_asymmetric_parity_code.cpp \
//       -o search_asymmetric_parity_code
// Run:
//   ./search_asymmetric_parity_code n restarts iterations seed

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

using Vec = std::vector<double>;

struct Search {
  int n, m;
  std::vector<std::uint64_t> su, sv;
  Vec kaa, kbb, kab;

  explicit Search(int n_) : n(n_), m(n + 1), su(m), sv(m) {
    const std::uint64_t all = (UINT64_C(1) << n) - 1;
    su[0] = all;
    sv[0] = 0;
    for (int i = 0; i < n; ++i) {
      su[i + 1] = UINT64_C(1) << i;
      sv[i + 1] = all ^ (UINT64_C(1) << i);
    }
    const std::size_t count =
        static_cast<std::size_t>(m) * m * m * m;
    kaa.resize(count);
    kbb.resize(count);
    kab.resize(count);
    for (int x = 0; x < m; ++x)
      for (int y = 0; y < m; ++y)
        for (int z = 0; z < m; ++z)
          for (int w = 0; w < m; ++w) {
            const std::size_t j = flat(x, y, z, w);
            kaa[j] = kernel(su[x], su[y], su[z], su[w]);
            kbb[j] = kernel(sv[x], sv[y], sv[z], sv[w]);
            kab[j] = kernel(su[x], su[y], sv[z], sv[w]);
          }
  }

  std::size_t flat(int x, int y, int z, int w) const {
    return ((static_cast<std::size_t>(x) * m + y) * m + z) * m + w;
  }

  double kernel(std::uint64_t x, std::uint64_t y,
                std::uint64_t z, std::uint64_t w) const {
    double out = 1.0;
    for (int i = 0; i < n; ++i) {
      const int a = (x >> i) & 1;
      const int b = (y >> i) & 1;
      const int c = (z >> i) & 1;
      const int d = (w >> i) & 1;
      const double local =
          ((a == c && b == d) ? 1.0 : 0.0)
          - ((a == b && c == d) ? 0.5 : 0.0);
      out *= local;
      if (out == 0.0) break;
    }
    return out;
  }

  double evaluate(const Vec& a, const Vec& b, Vec* ga, Vec* gb) const {
    if (ga) ga->assign(m, 0.0);
    if (gb) gb->assign(m, 0.0);
    double q = 0.0;
    for (int x = 0; x < m; ++x)
      for (int y = 0; y < m; ++y)
        for (int z = 0; z < m; ++z)
          for (int w = 0; w < m; ++w) {
            const std::size_t j = flat(x, y, z, w);
            const double pa = a[x] * a[y] * a[z] * a[w];
            const double pb = b[x] * b[y] * b[z] * b[w];
            const double pc = a[x] * a[y] * b[z] * b[w];
            q += kaa[j] * pa + kbb[j] * pb + 2.0 * kab[j] * pc;
            if (ga) {
              (*ga)[x] += kaa[j] * a[y] * a[z] * a[w]
                        + 2.0 * kab[j] * a[y] * b[z] * b[w];
              (*ga)[y] += kaa[j] * a[x] * a[z] * a[w]
                        + 2.0 * kab[j] * a[x] * b[z] * b[w];
              (*ga)[z] += kaa[j] * a[x] * a[y] * a[w];
              (*ga)[w] += kaa[j] * a[x] * a[y] * a[z];
              (*gb)[x] += kbb[j] * b[y] * b[z] * b[w];
              (*gb)[y] += kbb[j] * b[x] * b[z] * b[w];
              (*gb)[z] += kbb[j] * b[x] * b[y] * b[w]
                        + 2.0 * kab[j] * a[x] * a[y] * b[w];
              (*gb)[w] += kbb[j] * b[x] * b[y] * b[z]
                        + 2.0 * kab[j] * a[x] * a[y] * b[z];
            }
          }
    return q;
  }

  static void normalize(Vec& x) {
    double z = 0.0;
    for (double y : x) z += y * y;
    z = std::sqrt(z);
    for (double& y : x) y /= z;
  }
};

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: " << argv[0]
              << " n restarts iterations seed\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  if (n < 3 || n > 62) {
    std::cerr << "require 3 <= n <= 62\n";
    return 2;
  }
  const int restarts = std::stoi(argv[2]);
  const int iterations = std::stoi(argv[3]);
  const std::uint64_t seed = std::stoull(argv[4]);
  Search search(n);
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  double global = 1e100;
  Vec besta, bestb;

  std::cout << std::setprecision(17);
  for (int restart = 0; restart < restarts; ++restart) {
    Vec a(search.m), b(search.m);
    for (double& x : a) x = normal(rng);
    for (double& x : b) x = normal(rng);
    Search::normalize(a);
    Search::normalize(b);
    double value = search.evaluate(a, b, nullptr, nullptr);
    double step = 0.05;
    for (int iter = 0; iter < iterations; ++iter) {
      Vec ga, gb;
      search.evaluate(a, b, &ga, &gb);
      double da = 0.0, db = 0.0;
      for (int i = 0; i < search.m; ++i) {
        da += a[i] * ga[i];
        db += b[i] * gb[i];
      }
      double normg = 0.0;
      for (int i = 0; i < search.m; ++i) {
        ga[i] -= da * a[i];
        gb[i] -= db * b[i];
        normg += ga[i] * ga[i] + gb[i] * gb[i];
      }
      if (normg < 1e-24) break;
      bool accepted = false;
      double trial = step;
      for (int bt = 0; bt < 24; ++bt) {
        Vec at = a, btvec = b;
        for (int i = 0; i < search.m; ++i) {
          at[i] -= trial * ga[i];
          btvec[i] -= trial * gb[i];
        }
        Search::normalize(at);
        Search::normalize(btvec);
        double next = search.evaluate(at, btvec, nullptr, nullptr);
        if (next <= value - 1e-6 * trial * normg) {
          a.swap(at);
          b.swap(btvec);
          value = next;
          step = std::min(0.2, trial * 1.1);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    if (value < global) {
      global = value;
      besta = a;
      bestb = b;
    }
    std::cout << "restart " << restart << " value " << value
              << " best " << global << "\n";
  }
  std::cout << "best " << global << "\na";
  for (double x : besta) std::cout << " " << x;
  std::cout << "\nb";
  for (double x : bestb) std::cout << " " << x;
  std::cout << "\n";
}
