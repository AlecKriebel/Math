// Discovery-only real rank-two search for Q_n(C).
//
// This deliberately uses no external libraries.  It performs projected
// gradient descent on C = U V^T with U^T U = I_2 and ||V||_F = 1.  Its output
// is conjecture-generation data, never a certificate.

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

struct Search {
  int d;
  int n;
  int D;
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};

  explicit Search(int d_, int n_, std::uint64_t seed)
      : d(d_), n(n_), D(1), rng(seed) {
    for (int i = 0; i < n; ++i) D *= d;
  }

  int digit(int x, int place) const {
    for (int i = 0; i < place; ++i) x /= d;
    return x % d;
  }

  int replace_digit(int x, int place, int value) const {
    int power = 1;
    for (int i = 0; i < place; ++i) power *= d;
    return x + (value - ((x / power) % d)) * power;
  }

  std::vector<double> apply_k(const std::vector<double>& input) const {
    std::vector<double> current = input;
    std::vector<double> next(D * D);
    for (int place = 0; place < n; ++place) {
      next = current;
      for (int r = 0; r < D; ++r) {
        for (int c = 0; c < D; ++c) {
          if (digit(r, place) != digit(c, place)) continue;
          double partial_trace = 0.0;
          for (int z = 0; z < d; ++z) {
            const int rz = replace_digit(r, place, z);
            const int cz = replace_digit(c, place, z);
            partial_trace += current[rz * D + cz];
          }
          next[r * D + c] -= 0.5 * partial_trace;
        }
      }
      current.swap(next);
    }
    return current;
  }

  void orthonormalize_u(std::vector<double>& U, std::vector<double>& V) {
    // Modified Gram--Schmidt U = Q R, followed by V <- V R^T, so UV^T
    // remains unchanged.
    double r00 = 0.0;
    for (int i = 0; i < D; ++i) r00 += U[2 * i] * U[2 * i];
    r00 = std::sqrt(r00);
    if (r00 < 1e-14) r00 = 1e-14;
    for (int i = 0; i < D; ++i) U[2 * i] /= r00;

    double r01 = 0.0;
    for (int i = 0; i < D; ++i) r01 += U[2 * i] * U[2 * i + 1];
    for (int i = 0; i < D; ++i)
      U[2 * i + 1] -= r01 * U[2 * i];

    double r11 = 0.0;
    for (int i = 0; i < D; ++i) r11 += U[2 * i + 1] * U[2 * i + 1];
    r11 = std::sqrt(r11);
    if (r11 < 1e-14) {
      // Deterministic emergency direction orthogonal to column zero.
      int pivot = 0;
      for (int i = 1; i < D; ++i)
        if (std::abs(U[2 * i]) < std::abs(U[2 * pivot])) pivot = i;
      for (int i = 0; i < D; ++i) U[2 * i + 1] = (i == pivot ? 1.0 : 0.0);
      double proj = U[2 * pivot];
      for (int i = 0; i < D; ++i)
        U[2 * i + 1] -= proj * U[2 * i];
      r11 = 0.0;
      for (int i = 0; i < D; ++i)
        r11 += U[2 * i + 1] * U[2 * i + 1];
      r11 = std::sqrt(r11);
      r01 = 0.0;
    }
    for (int i = 0; i < D; ++i) U[2 * i + 1] /= r11;

    for (int i = 0; i < D; ++i) {
      const double v0 = V[2 * i];
      const double v1 = V[2 * i + 1];
      V[2 * i] = r00 * v0 + r01 * v1;
      V[2 * i + 1] = r11 * v1;
    }
  }

  void normalize_v(std::vector<double>& V) {
    double norm = 0.0;
    for (double x : V) norm += x * x;
    norm = std::sqrt(norm);
    for (double& x : V) x /= norm;
  }

  std::vector<double> coefficient(const std::vector<double>& U,
                                  const std::vector<double>& V) const {
    std::vector<double> C(D * D, 0.0);
    for (int i = 0; i < D; ++i)
      for (int j = 0; j < D; ++j)
        C[i * D + j] =
            U[2 * i] * V[2 * j] + U[2 * i + 1] * V[2 * j + 1];
    return C;
  }

  double objective(const std::vector<double>& C,
                   const std::vector<double>& G) const {
    double q = 0.0;
    double norm = 0.0;
    for (int i = 0; i < D * D; ++i) {
      q += C[i] * G[i];
      norm += C[i] * C[i];
    }
    return q / norm;
  }

  double one_start(int iterations, double initial_step,
                   std::vector<double>& best_c) {
    std::vector<double> U(2 * D), V(2 * D);
    for (double& x : U) x = normal(rng);
    for (double& x : V) x = normal(rng);
    orthonormalize_u(U, V);
    normalize_v(V);

    double best = std::numeric_limits<double>::infinity();
    double step = initial_step;
    for (int iter = 0; iter < iterations; ++iter) {
      std::vector<double> C = coefficient(U, V);
      std::vector<double> G = apply_k(C);
      const double q = objective(C, G);
      if (q < best) {
        best = q;
        best_c = C;
      }

      // Since U is orthonormal and ||V||_F=1, ||C||_F=1.
      // The quotient gradient in C is 2(G-qC).
      std::vector<double> grad_c(D * D);
      for (int k = 0; k < D * D; ++k)
        grad_c[k] = 2.0 * (G[k] - q * C[k]);
      std::vector<double> grad_u(2 * D, 0.0), grad_v(2 * D, 0.0);
      for (int i = 0; i < D; ++i) {
        for (int j = 0; j < D; ++j) {
          const double g = grad_c[i * D + j];
          grad_u[2 * i] += g * V[2 * j];
          grad_u[2 * i + 1] += g * V[2 * j + 1];
          grad_v[2 * j] += g * U[2 * i];
          grad_v[2 * j + 1] += g * U[2 * i + 1];
        }
      }

      // Project the U gradient onto the tangent of the Stiefel manifold.
      double gram[2][2] = {{0.0, 0.0}, {0.0, 0.0}};
      for (int i = 0; i < D; ++i)
        for (int a = 0; a < 2; ++a)
          for (int b = 0; b < 2; ++b)
            gram[a][b] += U[2 * i + a] * grad_u[2 * i + b];
      const double sym01 = 0.5 * (gram[0][1] + gram[1][0]);
      gram[0][1] = gram[1][0] = sym01;
      for (int i = 0; i < D; ++i) {
        const double u0 = U[2 * i], u1 = U[2 * i + 1];
        grad_u[2 * i] -= u0 * gram[0][0] + u1 * gram[1][0];
        grad_u[2 * i + 1] -= u0 * gram[0][1] + u1 * gram[1][1];
      }

      // Backtracking projected step.
      bool accepted = false;
      double trial_step = step;
      for (int trial = 0; trial < 16; ++trial) {
        std::vector<double> Ut = U, Vt = V;
        for (int k = 0; k < 2 * D; ++k) {
          Ut[k] -= trial_step * grad_u[k];
          Vt[k] -= trial_step * grad_v[k];
        }
        orthonormalize_u(Ut, Vt);
        normalize_v(Vt);
        const std::vector<double> Ct = coefficient(Ut, Vt);
        const std::vector<double> Gt = apply_k(Ct);
        const double qt = objective(Ct, Gt);
        if (qt <= q + 1e-13) {
          U.swap(Ut);
          V.swap(Vt);
          step = std::min(initial_step, trial_step * 1.05);
          accepted = true;
          break;
        }
        trial_step *= 0.5;
      }
      if (!accepted) break;
    }
    return best;
  }
};

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr << "usage: search_rank2_real d n starts iterations [seed]\\n";
    return 2;
  }
  const int d = std::stoi(argv[1]);
  const int n = std::stoi(argv[2]);
  const int starts = std::stoi(argv[3]);
  const int iterations = std::stoi(argv[4]);
  const std::uint64_t seed =
      argc >= 6 ? std::stoull(argv[5]) : UINT64_C(20260728);
  Search search(d, n, seed);
  double global_best = std::numeric_limits<double>::infinity();
  std::vector<double> global_c;
  for (int s = 0; s < starts; ++s) {
    std::vector<double> candidate;
    const double value = search.one_start(iterations, 0.05, candidate);
    if (value < global_best) {
      global_best = value;
      global_c.swap(candidate);
    }
    std::cout << "start " << s << " value " << std::setprecision(17) << value
              << " global " << global_best << "\n";
  }
  std::cout << "best " << std::setprecision(17) << global_best << "\n";
  std::cout << "matrix\n";
  for (int i = 0; i < search.D; ++i) {
    for (int j = 0; j < search.D; ++j)
      std::cout << std::setprecision(10) << global_c[i * search.D + j]
                << (j + 1 == search.D ? '\n' : ' ');
  }
  return 0;
}
