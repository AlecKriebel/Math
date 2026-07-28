// Discovery-only complex Grassmann search for a negative rank-two code
// projection at the Werner endpoint.  This is the complex analogue of
// search_code_projection_real.cpp; output is never treated as proof.

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
  int d, n, D;
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};

  Search(int d_, int n_, std::uint64_t seed)
      : d(d_), n(n_), D(1), rng(seed) {
    for (int i = 0; i < n; ++i) D *= d;
  }

  void orthonormalize(Vec& U) const {
    for (int a = 0; a < 2; ++a) {
      for (int b = 0; b < a; ++b) {
        Complex dot = 0.0;
        for (int i = 0; i < D; ++i)
          dot += std::conj(U[2 * i + b]) * U[2 * i + a];
        for (int i = 0; i < D; ++i) U[2 * i + a] -= dot * U[2 * i + b];
      }
      double norm = 0.0;
      for (int i = 0; i < D; ++i) norm += std::norm(U[2 * i + a]);
      norm = std::sqrt(std::max(norm, 1e-300));
      for (int i = 0; i < D; ++i) U[2 * i + a] /= norm;
    }
  }

  Vec projection(const Vec& U) const {
    Vec P(D * D);
    for (int i = 0; i < D; ++i)
      for (int j = 0; j < D; ++j)
        P[i * D + j] =
            U[2 * i] * std::conj(U[2 * j]) +
            U[2 * i + 1] * std::conj(U[2 * j + 1]);
    return P;
  }

  Vec apply_l(Vec C) const {
    Vec next(D * D);
    int power = 1;
    for (int site = 0; site < n; ++site) {
      next = C;
      for (int i = 0; i < D; ++i) {
        const int ii = (i / power) % d;
        for (int j = 0; j < D; ++j) {
          if ((j / power) % d != ii) continue;
          Complex trace = 0.0;
          for (int z = 0; z < d; ++z) {
            const int iz = i + (z - ii) * power;
            const int jz = j + (z - ii) * power;
            trace += C[iz * D + jz];
          }
          next[i * D + j] -= 0.5 * trace;
        }
      }
      C.swap(next);
      power *= d;
    }
    return C;
  }

  double value_and_gradient(const Vec& U, Vec* gradient) const {
    const Vec P = projection(U);
    const Vec A = apply_l(P);
    double q = 0.0;
    for (int k = 0; k < D * D; ++k)
      q += std::real(std::conj(P[k]) * A[k]);
    if (!gradient) return q;

    gradient->assign(2 * D, 0.0);
    for (int i = 0; i < D; ++i)
      for (int j = 0; j < D; ++j)
        for (int a = 0; a < 2; ++a)
          (*gradient)[2 * i + a] +=
              4.0 * A[i * D + j] * U[2 * j + a];

    Complex gram[2][2] = {};
    for (int a = 0; a < 2; ++a)
      for (int b = 0; b < 2; ++b)
        for (int i = 0; i < D; ++i)
          gram[a][b] +=
              std::conj(U[2 * i + a]) * (*gradient)[2 * i + b];
    const Complex off =
        0.5 * (gram[0][1] + std::conj(gram[1][0]));
    gram[0][0] = std::real(gram[0][0]);
    gram[1][1] = std::real(gram[1][1]);
    gram[0][1] = off;
    gram[1][0] = std::conj(off);
    for (int i = 0; i < D; ++i)
      for (int a = 0; a < 2; ++a)
        for (int b = 0; b < 2; ++b)
          (*gradient)[2 * i + a] -= U[2 * i + b] * gram[b][a];
    return q;
  }

  double one_start(int iterations) {
    Vec U(2 * D);
    for (Complex& x : U) x = Complex(normal(rng), normal(rng));
    orthonormalize(U);
    double best = std::numeric_limits<double>::infinity();
    double step = 0.1;
    for (int iter = 0; iter < iterations; ++iter) {
      Vec grad;
      const double q = value_and_gradient(U, &grad);
      best = std::min(best, q);
      double norm2 = 0.0;
      for (const Complex& x : grad) norm2 += std::norm(x);
      if (norm2 < 1e-24) break;
      bool accepted = false;
      double trial = step;
      for (int bt = 0; bt < 20; ++bt) {
        Vec V = U;
        for (int k = 0; k < 2 * D; ++k) V[k] -= trial * grad[k];
        orthonormalize(V);
        const double qv = value_and_gradient(V, nullptr);
        if (qv <= q - 1e-4 * trial * norm2 || qv <= q + 1e-14) {
          U.swap(V);
          step = std::min(0.1, trial * 1.1);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    return best;
  }

  void run(int starts, int iterations) {
    double best = std::numeric_limits<double>::infinity();
    for (int s = 0; s < starts; ++s) {
      const double q = one_start(iterations);
      best = std::min(best, q);
      std::cout << "start " << s << " value " << std::setprecision(17) << q
                << " global " << best << "\n";
    }
    std::cout << "best " << std::setprecision(17) << best << "\n";
  }
};

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr << "usage: search_code_projection_complex d n starts iterations "
                 "[seed]\n";
    return 2;
  }
  const int d = std::stoi(argv[1]);
  const int n = std::stoi(argv[2]);
  const int starts = std::stoi(argv[3]);
  const int iterations = std::stoi(argv[4]);
  const std::uint64_t seed =
      argc >= 6 ? std::stoull(argv[5]) : UINT64_C(20260728);
  Search(d, n, seed).run(starts, iterations);
  return 0;
}
