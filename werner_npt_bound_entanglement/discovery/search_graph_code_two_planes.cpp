// Discovery-only search over arbitrary two-planes inside 3-dimensional
// qutrit graph-state orbit codes.
//
// For a graph state |G> and nonzero syndrome s, the three orthonormal
// vectors |k> = Z^(k s)|G>, k=0,1,2, span a qutrit code.  A rank-two
// projection in this code is
//
//     P_z = U (I_3 - |z><z|) U^dagger,  ||z||=1.
//
// This program samples/descends in z and evaluates the endpoint form
// directly.  Floating-point output is discovery data only.

#include <algorithm>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

using Complex = std::complex<double>;
using Vec = std::vector<Complex>;

struct Search {
  int n;
  int D;
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};
  const Complex omega =
      std::exp(Complex(0.0, 2.0 * std::acos(-1.0) / 3.0));

  explicit Search(int n_, std::uint64_t seed) : n(n_), D(1), rng(seed) {
    for (int i = 0; i < n; ++i) D *= 3;
  }

  std::vector<int> digits(int x) const {
    std::vector<int> out(n);
    for (int i = 0; i < n; ++i) {
      out[i] = x % 3;
      x /= 3;
    }
    return out;
  }

  Vec apply_l(Vec input) const {
    Vec next(D * D);
    int power = 1;
    for (int site = 0; site < n; ++site) {
      next = input;
      for (int r = 0; r < D; ++r) {
        const int ri = (r / power) % 3;
        for (int c = 0; c < D; ++c) {
          if (ri != (c / power) % 3) continue;
          Complex trace = 0.0;
          for (int z = 0; z < 3; ++z) {
            const int rz = r + (z - ri) * power;
            const int cz = c + (z - ri) * power;
            trace += input[rz * D + cz];
          }
          next[r * D + c] -= 0.5 * trace;
        }
      }
      input.swap(next);
      power *= 3;
    }
    return input;
  }

  Vec graph_basis(int graph_code, int syndrome_code) const {
    std::vector<std::vector<int>> A(n, std::vector<int>(n));
    int g = graph_code;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        A[i][j] = A[j][i] = g % 3;
        g /= 3;
      }
    std::vector<int> s = digits(syndrome_code);
    Vec U(3 * D);
    const double scale = 1.0 / std::sqrt(static_cast<double>(D));
    for (int x = 0; x < D; ++x) {
      const auto t = digits(x);
      int quadratic = 0;
      int linear = 0;
      for (int i = 0; i < n; ++i) {
        linear += s[i] * t[i];
        for (int j = i + 1; j < n; ++j)
          quadratic += A[i][j] * t[i] * t[j];
      }
      for (int k = 0; k < 3; ++k)
        U[3 * x + k] =
            scale * std::pow(omega, (quadratic + k * linear) % 3);
    }
    return U;
  }

  Vec random_unit() {
    Vec z(3);
    double norm = 0.0;
    for (Complex& x : z) {
      x = Complex(normal(rng), normal(rng));
      norm += std::norm(x);
    }
    norm = std::sqrt(norm);
    for (Complex& x : z) x /= norm;
    return z;
  }

  Vec projection(const Vec& U, const Vec& z) const {
    Vec P(D * D);
    for (int x = 0; x < D; ++x)
      for (int y = 0; y < D; ++y) {
        Complex value = 0.0;
        for (int a = 0; a < 3; ++a)
          for (int b = 0; b < 3; ++b) {
            const Complex logical =
                (a == b ? Complex(1.0) : Complex(0.0)) -
                z[a] * std::conj(z[b]);
            value += U[3 * x + a] * logical *
                     std::conj(U[3 * y + b]);
          }
        P[x * D + y] = value;
      }
    return P;
  }

  double objective(const Vec& U, const Vec& z) const {
    const Vec P = projection(U, z);
    const Vec LP = apply_l(P);
    double q = 0.0;
    for (int i = 0; i < D * D; ++i)
      q += std::real(std::conj(P[i]) * LP[i]);
    return q;
  }

  void run(int codes, int samples) {
    const int graphs = static_cast<int>(
        std::round(std::pow(3.0, n * (n - 1) / 2)));
    const int syndromes = D - 1;
    double best = std::numeric_limits<double>::infinity();
    int best_g = -1, best_s = -1;
    Vec best_z;
    std::uniform_int_distribution<int> graph_dist(0, graphs - 1);
    std::uniform_int_distribution<int> syndrome_dist(1, syndromes);
    for (int c = 0; c < codes; ++c) {
      const int g = graph_dist(rng);
      const int s = syndrome_dist(rng);
      const Vec U = graph_basis(g, s);
      for (int k = 0; k < samples; ++k) {
        const Vec z = random_unit();
        const double q = objective(U, z);
        if (q < best) {
          best = q;
          best_g = g;
          best_s = s;
          best_z = z;
        }
      }
      if ((c + 1) % 10 == 0)
        std::cout << "codes " << c + 1 << " best "
                  << std::setprecision(17) << best << "\n";
    }
    std::cout << "best " << std::setprecision(17) << best << " graph "
              << best_g << " syndrome " << best_s << "\nz";
    for (const Complex& x : best_z)
      std::cout << " (" << x.real() << "," << x.imag() << ")";
    std::cout << "\n";
  }
};

int main(int argc, char** argv) {
  if (argc < 4) {
    std::cerr << "usage: search_graph_code_two_planes n codes samples [seed]\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  const int codes = std::stoi(argv[2]);
  const int samples = std::stoi(argv[3]);
  const std::uint64_t seed =
      argc >= 5 ? std::stoull(argv[4]) : UINT64_C(20260728);
  if (n < 2 || n > 5) {
    std::cerr << "implemented for 2 <= n <= 5\n";
    return 2;
  }
  Search(n, seed).run(codes, samples);
  return 0;
}
