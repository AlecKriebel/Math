// Discovery-only search for a violation of
//
//   6 Tr(rho_K^2) + sum_{i<j} Tr(rho_ij^2)
//       - 3 sum_i Tr(rho_Ki^2) >= 0
//
// on a pure state of K x A1 x ... x A4, where dim(K)=2 and dim(Ai)=d.
// This is a deliberately broader domain than the rank-two code problem:
// the latter additionally requires rho_K=I/2.  Floating-point output from
// this program is not a certificate.

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
  int kdim, d, D;
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};

  Search(int kdim_, int d_, std::uint64_t seed)
      : kdim(kdim_), d(d_), D(kdim_), rng(seed) {
    for (int i = 0; i < 4; ++i) D *= d;
  }

  std::vector<int> digits(int index) const {
    std::vector<int> out(5);
    for (int i = 4; i >= 1; --i) {
      out[i] = index % d;
      index /= d;
    }
      out[0] = index;
    return out;
  }

  // Return purity of the reduction to the factors selected by mask.  If
  // grad is nonnull, add coefficient times its Euclidean gradient.
  double purity(const Vec& x, int mask, double coefficient, Vec* grad) const {
    std::vector<int> row_of(D), col_of(D);
    int row_dim = 1;
    for (int site = 0; site < 5; ++site) {
      const int dim = site == 0 ? kdim : d;
      if (mask & (1 << site))
        row_dim *= dim;
    }
    for (int k = 0; k < D; ++k) {
      const auto q = digits(k);
      int row = 0, col = 0;
      for (int site = 0; site < 5; ++site) {
        const int dim = site == 0 ? kdim : d;
        if (mask & (1 << site))
          row = row * dim + q[site];
        else
          col = col * dim + q[site];
      }
      row_of[k] = row;
      col_of[k] = col;
    }

    Vec rho(row_dim * row_dim, 0.0);
    for (int k = 0; k < D; ++k)
      for (int l = 0; l < D; ++l)
        if (col_of[k] == col_of[l])
          rho[row_of[k] * row_dim + row_of[l]] += x[k] * std::conj(x[l]);

    double p = 0.0;
    for (const Complex& z : rho) p += std::norm(z);

    if (grad) {
      // The real Euclidean gradient is 4 rho*x in this flattening.
      for (int k = 0; k < D; ++k)
        for (int l = 0; l < D; ++l)
          if (col_of[k] == col_of[l])
            (*grad)[k] +=
                4.0 * coefficient *
                rho[row_of[k] * row_dim + row_of[l]] * x[l];
    }
    return p;
  }

  double one_site_determinant(const Vec& x, int site) const {
    const int dim = site == 0 ? kdim : d;
    Vec rho(dim * dim, 0.0);
    for (int k = 0; k < D; ++k) {
      const auto qk = digits(k);
      for (int l = 0; l < D; ++l) {
        const auto ql = digits(l);
        bool same = true;
        for (int s = 0; s < 5; ++s)
          if (s != site && qk[s] != ql[s]) same = false;
        if (same) rho[qk[site] * dim + ql[site]] += x[k] * std::conj(x[l]);
      }
    }
    Complex det = 1.0;
    for (int col = 0; col < dim; ++col) {
      int pivot = col;
      for (int row = col + 1; row < dim; ++row)
        if (std::abs(rho[row * dim + col]) >
            std::abs(rho[pivot * dim + col]))
          pivot = row;
      if (std::abs(rho[pivot * dim + col]) < 1e-14) return 0.0;
      if (pivot != col) {
        for (int j = 0; j < dim; ++j)
          std::swap(rho[pivot * dim + j], rho[col * dim + j]);
        det = -det;
      }
      const Complex z = rho[col * dim + col];
      det *= z;
      for (int row = col + 1; row < dim; ++row) {
        const Complex ratio = rho[row * dim + col] / z;
        for (int j = col; j < dim; ++j)
          rho[row * dim + j] -= ratio * rho[col * dim + j];
      }
    }
    return std::real(det);
  }

  double value_and_gradient(const Vec& x, Vec* grad) const {
    if (grad) grad->assign(D, 0.0);
    double value = 0.0;
    value += 6.0 * purity(x, 1, 6.0, grad);
    for (int i = 1; i <= 4; ++i)
      for (int j = i + 1; j <= 4; ++j) {
        const int mask = (1 << i) | (1 << j);
        value += purity(x, mask, 1.0, grad);
      }
    for (int i = 1; i <= 4; ++i) {
      const int mask = 1 | (1 << i);
      value -= 3.0 * purity(x, mask, -3.0, grad);
    }
    if (grad) {
      Complex radial = 0.0;
      for (int k = 0; k < D; ++k) radial += std::conj(x[k]) * (*grad)[k];
      radial = std::real(radial);
      for (int k = 0; k < D; ++k) (*grad)[k] -= radial * x[k];
    }
    return value;
  }

  void normalize(Vec& x) const {
    double norm2 = 0.0;
    for (const Complex& z : x) norm2 += std::norm(z);
    const double norm = std::sqrt(std::max(norm2, 1e-300));
    for (Complex& z : x) z /= norm;
  }

  double one_start(int iterations, Vec* output) {
    Vec x(D);
    for (Complex& z : x) z = Complex(normal(rng), normal(rng));
    normalize(x);
    double step = 0.1;
    double best = std::numeric_limits<double>::infinity();
    for (int iter = 0; iter < iterations; ++iter) {
      Vec grad;
      const double value = value_and_gradient(x, &grad);
      best = std::min(best, value);
      double norm2 = 0.0;
      for (const Complex& z : grad) norm2 += std::norm(z);
      if (norm2 < 1e-24) break;
      bool accepted = false;
      double trial = step;
      for (int bt = 0; bt < 30; ++bt) {
        Vec y = x;
        for (int k = 0; k < D; ++k) y[k] -= trial * grad[k];
        normalize(y);
        const double next = value_and_gradient(y, nullptr);
        if (next <= value - 1e-4 * trial * norm2) {
          x.swap(y);
          step = std::min(0.2, 1.1 * trial);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    if (output) *output = x;
    return best;
  }

  void run(int starts, int iterations) {
    double best = std::numeric_limits<double>::infinity();
    Vec best_x;
    for (int s = 0; s < starts; ++s) {
      Vec x;
      const double value = one_start(iterations, &x);
      if (value < best) {
        best = value;
        best_x = x;
      }
      std::cout << "start " << s << " value " << std::setprecision(17)
                << value << " global " << best << "\n";
    }
    if (!best_x.empty()) {
      std::cout << "best diagnostics pK "
                << purity(best_x, 1, 0.0, nullptr);
      for (int i = 1; i <= 4; ++i)
        std::cout << " pK" << i << " "
                  << purity(best_x, 1 | (1 << i), 0.0, nullptr);
      for (int i = 1; i <= 4; ++i)
        std::cout << " p" << i << " "
                  << purity(best_x, 1 << i, 0.0, nullptr);
      for (int i = 1; i <= 4; ++i)
        for (int j = i + 1; j <= 4; ++j)
          std::cout << " p" << i << j << " "
                    << purity(best_x, (1 << i) | (1 << j), 0.0, nullptr);
      for (int i = 1; i <= 4; ++i)
        std::cout << " det" << i << " " << one_site_determinant(best_x, i);
      std::cout << "\n";
    }
  }
};

int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr << "usage: search_n4_homogeneous_purity kdim d starts "
                 "iterations [seed]\n";
    return 2;
  }
  const int kdim = std::stoi(argv[1]);
  const int d = std::stoi(argv[2]);
  const int starts = std::stoi(argv[3]);
  const int iterations = std::stoi(argv[4]);
  const std::uint64_t seed =
      argc >= 6 ? std::stoull(argv[5]) : UINT64_C(20260728);
  Search(kdim, d, seed).run(starts, iterations);
  return 0;
}
