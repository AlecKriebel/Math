// Discovery-only probe for the normalized one-plane marginal operators
//
//   A(Psi) = 3 I + 2 sum_{i<j} rho_{Kij} - 3 sum_i rho_{Ki}.
//
// It tests A >= c |Psi><Psi| for c = 0, 1, 3/2, 2 on unrestricted
// complex qutrit codes.  Floating-point output is not a certificate.

#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

using C = std::complex<double>;

extern "C" void zheev_(char*, char*, int*, C*, int*, double*, C*, int*,
                        double*, int*);

constexpr int dH = 27;
constexpr int dK = 2;
constexpr int D = dK * dH;

struct Probe {
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};
  std::vector<C> frame = std::vector<C>(dH * dK);
  std::vector<C> psi = std::vector<C>(D);

  explicit Probe(std::uint64_t seed) : rng(seed) {}

  static int hidx(int a, int b, int c) { return (a * 3 + b) * 3 + c; }

  static int idx(int k, int a, int b, int c) {
    return ((k * 3 + a) * 3 + b) * 3 + c;
  }

  void random_code() {
    for (C& z : frame) z = C(normal(rng), normal(rng));
    for (int col = 0; col < 2; ++col) {
      for (int prev = 0; prev < col; ++prev) {
        C overlap = 0.0;
        for (int h = 0; h < dH; ++h)
          overlap += std::conj(frame[2 * h + prev]) *
                     frame[2 * h + col];
        for (int h = 0; h < dH; ++h)
          frame[2 * h + col] -= overlap * frame[2 * h + prev];
      }
      double n2 = 0.0;
      for (int h = 0; h < dH; ++h) n2 += std::norm(frame[2 * h + col]);
      for (int h = 0; h < dH; ++h) frame[2 * h + col] /= std::sqrt(n2);
    }
    for (int k = 0; k < 2; ++k)
      for (int a = 0; a < 3; ++a)
        for (int b = 0; b < 3; ++b)
          for (int c = 0; c < 3; ++c)
            psi[idx(k, a, b, c)] =
                frame[2 * hidx(a, b, c) + k] / std::sqrt(2.0);
  }

  void clear_code() {
    std::fill(frame.begin(), frame.end(), C(0.0));
  }

  void finish_code() {
    for (int k = 0; k < 2; ++k)
      for (int a = 0; a < 3; ++a)
        for (int b = 0; b < 3; ++b)
          for (int c = 0; c < 3; ++c)
            psi[idx(k, a, b, c)] =
                frame[2 * hidx(a, b, c) + k] / std::sqrt(2.0);
  }

  void ghz_code() {
    clear_code();
    frame[2 * hidx(0, 0, 0)] = 1.0;
    frame[2 * hidx(1, 1, 1) + 1] = 1.0;
    finish_code();
  }

  void bell_spectator_code() {
    clear_code();
    for (int a = 0; a < 3; ++a) {
      frame[2 * hidx(a, a, 0)] = 1.0 / std::sqrt(3.0);
      frame[2 * hidx(a, a, 1) + 1] = 1.0 / std::sqrt(3.0);
    }
    finish_code();
  }

  void qutrit_ghz_phase_code() {
    clear_code();
    const C omega(-0.5, std::sqrt(3.0) / 2.0);
    for (int a = 0; a < 3; ++a) {
      frame[2 * hidx(a, a, a)] = 1.0 / std::sqrt(3.0);
      frame[2 * hidx(a, a, a) + 1] =
          std::pow(omega, a) / std::sqrt(3.0);
    }
    finish_code();
  }

  C marginal_entry(int keep_mask, const std::array<int, 4>& row,
                   const std::array<int, 4>& col) const {
    // K is always kept.  keep_mask uses physical bits 0,1,2.
    for (int site = 0; site < 3; ++site)
      if (!(keep_mask & (1 << site)) && row[site + 1] != col[site + 1])
        return 0.0;

    C answer = 0.0;
    for (int a = 0; a < 3; ++a)
      for (int b = 0; b < 3; ++b)
        for (int c = 0; c < 3; ++c) {
          const int q[3] = {a, b, c};
          std::array<int, 4> rr = row, cc = col;
          for (int site = 0; site < 3; ++site)
            if (!(keep_mask & (1 << site)))
              rr[site + 1] = cc[site + 1] = q[site];
          // Avoid repeated terms: the loop variables at kept sites are ignored.
          bool canonical = true;
          for (int site = 0; site < 3; ++site)
            if ((keep_mask & (1 << site)) && q[site] != 0) canonical = false;
          if (!canonical) continue;
          answer += psi[idx(rr[0], rr[1], rr[2], rr[3])] *
                    std::conj(psi[idx(cc[0], cc[1], cc[2], cc[3])]);
        }
    return answer;
  }

  std::vector<C> build(double rank_one_coefficient) const {
    // Column-major storage for LAPACK.
    std::vector<C> matrix(D * D);
    for (int r = 0; r < D; ++r) {
      int z = r;
      std::array<int, 4> rr{};
      for (int site = 3; site >= 0; --site) {
        const int base = site == 0 ? 2 : 3;
        rr[site] = z % base;
        z /= base;
      }
      for (int c = 0; c < D; ++c) {
        int w = c;
        std::array<int, 4> cc{};
        for (int site = 3; site >= 0; --site) {
          const int base = site == 0 ? 2 : 3;
          cc[site] = w % base;
          w /= base;
        }
        C value = r == c ? 3.0 : 0.0;
        value += 2.0 * (marginal_entry(3, rr, cc) +
                       marginal_entry(5, rr, cc) +
                       marginal_entry(6, rr, cc));
        value -= 3.0 * (marginal_entry(1, rr, cc) +
                       marginal_entry(2, rr, cc) +
                       marginal_entry(4, rr, cc));
        value -= rank_one_coefficient * psi[r] * std::conj(psi[c]);
        matrix[r + D * c] = value;
      }
    }
    return matrix;
  }

  static double min_eigenpair(std::vector<C> matrix,
                              std::vector<C>* eigenvector = nullptr) {
    char job = eigenvector ? 'V' : 'N', uplo = 'U';
    int n = D, lda = D, info = 0, lwork = -1;
    std::vector<double> eigenvalues(D), rwork(3 * D - 2);
    C query = 0.0;
    zheev_(&job, &uplo, &n, matrix.data(), &lda, eigenvalues.data(), &query,
           &lwork, rwork.data(), &info);
    lwork = std::max(2 * D, static_cast<int>(std::real(query)));
    std::vector<C> work(lwork);
    zheev_(&job, &uplo, &n, matrix.data(), &lda, eigenvalues.data(),
           work.data(), &lwork, rwork.data(), &info);
    if (info != 0) {
      std::cerr << "zheev failed: " << info << "\n";
      std::exit(2);
    }
    if (eigenvector)
      eigenvector->assign(matrix.begin(), matrix.begin() + D);
    return eigenvalues.front();
  }

  static double min_eigenvalue(std::vector<C> matrix) {
    return min_eigenpair(std::move(matrix), nullptr);
  }

  static C inner(const std::vector<C>& left, const std::vector<C>& right) {
    C value = 0.0;
    for (int i = 0; i < D; ++i) value += std::conj(left[i]) * right[i];
    return value;
  }

  static std::vector<C> multiply(const std::vector<C>& matrix,
                                 const std::vector<C>& vector) {
    std::vector<C> result(D);
    for (int col = 0; col < D; ++col)
      for (int row = 0; row < D; ++row)
        result[row] += matrix[row + D * col] * vector[col];
    return result;
  }

  void frame_from_psi_gradient(const std::vector<C>& state_gradient,
                               std::vector<C>& gradient) const {
    gradient.assign(dH * 2, 0.0);
    for (int k = 0; k < 2; ++k)
      for (int a = 0; a < 3; ++a)
        for (int b = 0; b < 3; ++b)
          for (int c = 0; c < 3; ++c)
            gradient[2 * hidx(a, b, c) + k] =
                std::sqrt(2.0) * state_gradient[idx(k, a, b, c)];
    C gram[2][2] = {};
    for (int i = 0; i < 2; ++i)
      for (int j = 0; j < 2; ++j)
        for (int h = 0; h < dH; ++h)
          gram[i][j] += std::conj(frame[2 * h + i]) *
                        gradient[2 * h + j];
    const C off = 0.5 * (gram[0][1] + std::conj(gram[1][0]));
    gram[0][0] = std::real(gram[0][0]);
    gram[1][1] = std::real(gram[1][1]);
    gram[0][1] = off;
    gram[1][0] = std::conj(off);
    for (int h = 0; h < dH; ++h) {
      const C v0 = frame[2 * h], v1 = frame[2 * h + 1];
      gradient[2 * h] -= v0 * gram[0][0] + v1 * gram[1][0];
      gradient[2 * h + 1] -= v0 * gram[0][1] + v1 * gram[1][1];
    }
  }

  void orthonormalize_frame() {
    for (int col = 0; col < 2; ++col) {
      for (int prev = 0; prev < col; ++prev) {
        C overlap = 0.0;
        for (int h = 0; h < dH; ++h)
          overlap += std::conj(frame[2 * h + prev]) *
                     frame[2 * h + col];
        for (int h = 0; h < dH; ++h)
          frame[2 * h + col] -= overlap * frame[2 * h + prev];
      }
      double norm2 = 0.0;
      for (int h = 0; h < dH; ++h) norm2 += std::norm(frame[2 * h + col]);
      for (int h = 0; h < dH; ++h) frame[2 * h + col] /= std::sqrt(norm2);
    }
    finish_code();
  }

  double optimize(double coefficient, int iterations) {
    random_code();
    double best = 1e100;
    double step = 0.2;
    for (int iteration = 0; iteration < iterations; ++iteration) {
      const std::vector<C> code_state = psi;
      std::vector<C> x;
      const double value = min_eigenpair(build(coefficient), &x);
      best = std::min(best, value);

      // By the swap identity, with x fixed the same biform is obtained by
      // building the marginal operator from x and evaluating it on Psi.
      psi = x;
      const std::vector<C> operator_from_x = build(coefficient);
      psi = code_state;
      const std::vector<C> image = multiply(operator_from_x, code_state);
      std::vector<C> gradient;
      frame_from_psi_gradient(image, gradient);
      double gradient2 = 0.0;
      for (const C& z : gradient) gradient2 += std::norm(z);
      if (gradient2 < 1e-24) break;

      const std::vector<C> old_frame = frame;
      bool accepted = false;
      double trial_step = step;
      for (int backtrack = 0; backtrack < 30; ++backtrack) {
        frame = old_frame;
        for (int i = 0; i < dH * 2; ++i)
          frame[i] -= trial_step * gradient[i];
        orthonormalize_frame();
        const std::vector<C> trial_image = multiply(operator_from_x, psi);
        const double fixed_value = std::real(inner(psi, trial_image));
        if (fixed_value <= value - 1e-5 * trial_step * gradient2) {
          step = std::min(0.2, 1.2 * trial_step);
          accepted = true;
          break;
        }
        trial_step *= 0.5;
      }
      if (!accepted) {
        frame = old_frame;
        finish_code();
        break;
      }
    }
    return best;
  }
};

int main(int argc, char** argv) {
  const int trials = argc > 1 ? std::stoi(argv[1]) : 100;
  Probe probe(0x5c4f7a9ULL);
  const std::array<double, 5> coefficients{0.0, 1.0, 4.0 / 3.0, 1.5,
                                            2.0};
  std::array<double, 5> minima{1e100, 1e100, 1e100, 1e100, 1e100};
  probe.ghz_code();
  std::cout << std::setprecision(16) << "GHZ:";
  for (double coefficient : coefficients)
    std::cout << " " << Probe::min_eigenvalue(probe.build(coefficient));
  std::cout << "\n";
  probe.bell_spectator_code();
  std::cout << "Bell spectator:";
  for (double coefficient : coefficients)
    std::cout << " " << Probe::min_eigenvalue(probe.build(coefficient));
  std::cout << "\n";
  probe.qutrit_ghz_phase_code();
  std::cout << "Qutrit GHZ phase:";
  for (double coefficient : coefficients)
    std::cout << " " << Probe::min_eigenvalue(probe.build(coefficient));
  std::cout << "\n";
  for (int trial = 0; trial < trials; ++trial) {
    probe.random_code();
    for (int j = 0; j < 5; ++j)
      minima[j] =
          std::min(minima[j], Probe::min_eigenvalue(probe.build(coefficients[j])));
  }
  std::cout << std::setprecision(16);
  for (int j = 0; j < 5; ++j)
    std::cout << "c=" << coefficients[j] << " min=" << minima[j] << "\n";
  for (double coefficient : {0.0, 1.0, 4.0 / 3.0}) {
    double optimized = 1e100;
    for (int trial = 0; trial < std::max(1, trials / 10); ++trial)
      optimized = std::min(optimized, probe.optimize(coefficient, 250));
    std::cout << "optimized c=" << coefficient << " min=" << optimized
              << "\n";
  }
}
