// Discovery-only search over permutation-symmetric real qutrit codes.
//
// A normalized occupation vector |N0,N1,N2> is decomposed across k traced
// sites and n-k retained sites by the exact hypergeometric Schmidt
// coefficients.  This makes all 2^n partial traces collapse to n+1 small
// matrices.  The program minimizes the endpoint form on real orthonormal
// pairs in Sym^n(C^3).  Floating-point output is conjecture-generation data,
// never a certificate.
//
// Build:
//   c++ -O3 -std=c++17 search_symmetric_code.cpp -o search_symmetric_code
// Run:
//   ./search_symmetric_code n restarts iterations seed

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

using Vec = std::vector<double>;

struct Occupation {
  int a, b, c;
};

struct Search {
  int n;
  std::vector<std::vector<Occupation>> occ;
  std::vector<std::vector<int>> index;
  std::vector<double> log_fact;

  explicit Search(int n_) : n(n_), occ(n + 1), index(n + 1), log_fact(n + 1) {
    for (int k = 1; k <= n; ++k) log_fact[k] = log_fact[k - 1] + std::log(k);
    for (int m = 0; m <= n; ++m) {
      index[m].assign((m + 1) * (m + 1), -1);
      for (int a = 0; a <= m; ++a) {
        for (int b = 0; b <= m - a; ++b) {
          int j = static_cast<int>(occ[m].size());
          occ[m].push_back({a, b, m - a - b});
          index[m][a * (m + 1) + b] = j;
        }
      }
    }
  }

  int idx(int m, int a, int b) const {
    return index[m][a * (m + 1) + b];
  }

  double log_multinomial(const Occupation& x) const {
    int m = x.a + x.b + x.c;
    return log_fact[m] - log_fact[x.a] - log_fact[x.b] - log_fact[x.c];
  }

  double choose(int nn, int k) const {
    return std::exp(log_fact[nn] - log_fact[k] - log_fact[nn - k]);
  }

  double evaluate(const Vec& X, Vec* gradient) const {
    const int dim = static_cast<int>(occ[n].size());
    if (gradient) gradient->assign(2 * dim, 0.0);
    double value = 0.0;
    for (int k = 0; k <= n; ++k) {
      const int r = n - k;
      const int nr = static_cast<int>(occ[r].size());
      const int nk = static_cast<int>(occ[k].size());
      Vec M0(nr * nk), M1(nr * nk);
      for (int ir = 0; ir < nr; ++ir) {
        const Occupation& R = occ[r][ir];
        for (int ik = 0; ik < nk; ++ik) {
          const Occupation& K = occ[k][ik];
          Occupation N{R.a + K.a, R.b + K.b, R.c + K.c};
          const int in = idx(n, N.a, N.b);
          const double factor = std::exp(0.5 * (
              log_multinomial(R) + log_multinomial(K) -
              log_multinomial(N)));
          M0[ir * nk + ik] = factor * X[2 * in];
          M1[ir * nk + ik] = factor * X[2 * in + 1];
        }
      }
      Vec rho(nr * nr, 0.0);
      for (int i = 0; i < nr; ++i) {
        for (int j = 0; j < nr; ++j) {
          double z = 0.0;
          for (int q = 0; q < nk; ++q)
            z += M0[i * nk + q] * M0[j * nk + q]
               + M1[i * nk + q] * M1[j * nk + q];
          rho[i * nr + j] = z;
        }
      }
      const double weight = choose(n, k) * std::pow(-0.5, k);
      for (double z : rho) value += weight * z * z;
      if (gradient) {
        Vec G0(nr * nk, 0.0), G1(nr * nk, 0.0);
        for (int i = 0; i < nr; ++i) {
          for (int q = 0; q < nk; ++q) {
            for (int j = 0; j < nr; ++j) {
              G0[i * nk + q] +=
                  4.0 * weight * rho[i * nr + j] * M0[j * nk + q];
              G1[i * nk + q] +=
                  4.0 * weight * rho[i * nr + j] * M1[j * nk + q];
            }
          }
        }
        for (int ir = 0; ir < nr; ++ir) {
          const Occupation& R = occ[r][ir];
          for (int ik = 0; ik < nk; ++ik) {
            const Occupation& K = occ[k][ik];
            Occupation N{R.a + K.a, R.b + K.b, R.c + K.c};
            const int in = idx(n, N.a, N.b);
            const double factor = std::exp(0.5 * (
                log_multinomial(R) + log_multinomial(K) -
                log_multinomial(N)));
            (*gradient)[2 * in] += factor * G0[ir * nk + ik];
            (*gradient)[2 * in + 1] += factor * G1[ir * nk + ik];
          }
        }
      }
    }
    return value;
  }

  static void orthonormalize(Vec& X) {
    const int dim = static_cast<int>(X.size() / 2);
    double n0 = 0.0;
    for (int i = 0; i < dim; ++i) n0 += X[2 * i] * X[2 * i];
    n0 = std::sqrt(n0);
    for (int i = 0; i < dim; ++i) X[2 * i] /= n0;
    double p = 0.0;
    for (int i = 0; i < dim; ++i) p += X[2 * i] * X[2 * i + 1];
    for (int i = 0; i < dim; ++i) X[2 * i + 1] -= p * X[2 * i];
    double n1 = 0.0;
    for (int i = 0; i < dim; ++i) n1 += X[2 * i + 1] * X[2 * i + 1];
    n1 = std::sqrt(n1);
    if (n1 < 1e-13) {
      int pivot = 0;
      for (int i = 1; i < dim; ++i)
        if (std::abs(X[2 * i]) < std::abs(X[2 * pivot])) pivot = i;
      for (int i = 0; i < dim; ++i) X[2 * i + 1] = 0.0;
      X[2 * pivot + 1] = 1.0;
      p = X[2 * pivot];
      for (int i = 0; i < dim; ++i) X[2 * i + 1] -= p * X[2 * i];
      n1 = 0.0;
      for (int i = 0; i < dim; ++i) n1 += X[2 * i + 1] * X[2 * i + 1];
      n1 = std::sqrt(n1);
    }
    for (int i = 0; i < dim; ++i) X[2 * i + 1] /= n1;
  }
};

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: " << argv[0]
              << " n restarts iterations seed\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  const int restarts = std::stoi(argv[2]);
  const int iterations = std::stoi(argv[3]);
  const std::uint64_t seed = std::stoull(argv[4]);
  Search search(n);
  const int dim = static_cast<int>(search.occ[n].size());
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  double global_best = 1e100;
  Vec global_X;

  std::cout << std::setprecision(17);
  for (int restart = 0; restart < restarts; ++restart) {
    Vec X(2 * dim);
    for (int i = 0; i < dim; ++i)
      for (int j = 0; j < 2; ++j) X[2 * i + j] = normal(rng);
    Search::orthonormalize(X);

    double step = 0.05;
    double value = search.evaluate(X, nullptr);
    for (int iter = 0; iter < iterations; ++iter) {
      Vec G;
      search.evaluate(X, &G);
      double gram[2][2] = {{0.0, 0.0}, {0.0, 0.0}};
      for (int i = 0; i < dim; ++i)
        for (int a = 0; a < 2; ++a)
          for (int b = 0; b < 2; ++b)
            gram[a][b] += X[2 * i + a] * G[2 * i + b];
      const double sym01 = 0.5 * (gram[0][1] + gram[1][0]);
      gram[0][1] = gram[1][0] = sym01;
      double grad_norm_sq = 0.0;
      for (int i = 0; i < dim; ++i) {
        const double x0 = X[2 * i], x1 = X[2 * i + 1];
        G[2 * i] -= x0 * gram[0][0] + x1 * gram[1][0];
        G[2 * i + 1] -= x0 * gram[0][1] + x1 * gram[1][1];
        grad_norm_sq += G[2 * i] * G[2 * i]
                      + G[2 * i + 1] * G[2 * i + 1];
      }
      if (grad_norm_sq < 1e-22) break;

      bool accepted = false;
      double trial = step;
      for (int bt = 0; bt < 24; ++bt) {
        Vec Y = X;
        for (int i = 0; i < 2 * dim; ++i) Y[i] -= trial * G[i];
        Search::orthonormalize(Y);
        double next = search.evaluate(Y, nullptr);
        if (next <= value - 1e-5 * trial * grad_norm_sq) {
          X.swap(Y);
          value = next;
          step = std::min(0.2, trial * 1.1);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }

    if (value < global_best) {
      global_best = value;
      global_X = X;
    }
    std::cout << "restart " << restart << " value " << value
              << " best " << global_best << "\n";
  }

  std::cout << "best " << global_best << "\n";
  std::cout << "columns in occupation order (a,b,n-a-b)\n";
  for (int i = 0; i < dim; ++i) {
    const Occupation& o = search.occ[n][i];
    std::cout << o.a << " " << o.b << " " << o.c << " "
              << global_X[2 * i] << " " << global_X[2 * i + 1] << "\n";
  }
}
