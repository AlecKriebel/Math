// Discovery-only search for the quantitative endpoint inequality on
// real positive-semidefinite rank-two matrices.
//
// Parametrize H = U diag(cos(theta), sin(theta)) U^T, U^T U = I_2.
// The optimized objective is
//   <H,K^{tensor n}(H)> - 2^{-n}(cos(theta)-sin(theta))^2.
// Floating-point output is conjecture-generation data only.

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
  enum class Mode { kPsdQuantitative, kProjection, kSignedNormal };
  Mode mode;

  Search(int d_, int n_, std::uint64_t seed, Mode mode_)
      : d(d_), n(n_), D(1), rng(seed), mode(mode_) {
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

  void orthonormalize(std::vector<double>& U) const {
    double r00 = 0.0;
    for (int i = 0; i < D; ++i) r00 += U[2 * i] * U[2 * i];
    r00 = std::sqrt(std::max(r00, 1e-30));
    for (int i = 0; i < D; ++i) U[2 * i] /= r00;

    double r01 = 0.0;
    for (int i = 0; i < D; ++i) r01 += U[2 * i] * U[2 * i + 1];
    for (int i = 0; i < D; ++i) U[2 * i + 1] -= r01 * U[2 * i];

    double r11 = 0.0;
    for (int i = 0; i < D; ++i) r11 += U[2 * i + 1] * U[2 * i + 1];
    r11 = std::sqrt(std::max(r11, 1e-30));
    for (int i = 0; i < D; ++i) U[2 * i + 1] /= r11;
  }

  std::vector<double> matrix(const std::vector<double>& U,
                             double lambda, double mu) const {
    std::vector<double> H(D * D);
    for (int i = 0; i < D; ++i) {
      for (int j = 0; j < D; ++j) {
        H[i * D + j] = lambda * U[2 * i] * U[2 * j]
                     + mu * U[2 * i + 1] * U[2 * j + 1];
      }
    }
    return H;
  }

  double objective(const std::vector<double>& U, double theta,
                   std::vector<double>* gradient_u,
                   double* gradient_theta) const {
    const double lambda = std::cos(theta);
    const double mu = std::sin(theta);
    const std::vector<double> H = matrix(U, lambda, mu);
    const std::vector<double> G = apply_k(H);
    double q = 0.0;
    for (int k = 0; k < D * D; ++k) q += H[k] * G[k];
    const double m = std::ldexp(1.0, -n);
    const double value =
        mode == Mode::kPsdQuantitative
            ? q - m * (lambda - mu) * (lambda - mu)
            : q;

    if (gradient_u != nullptr) {
      gradient_u->assign(2 * D, 0.0);
      for (int i = 0; i < D; ++i) {
        for (int j = 0; j < D; ++j) {
          const double sym_g = G[i * D + j] + G[j * D + i];
          (*gradient_u)[2 * i] +=
              2.0 * lambda * sym_g * U[2 * j];
          (*gradient_u)[2 * i + 1] +=
              2.0 * mu * sym_g * U[2 * j + 1];
        }
      }
      // G is symmetric here, and q's C-gradient is 2G.  The displayed
      // symmetrization therefore gives the U-gradient.
      double gram[2][2] = {{0.0, 0.0}, {0.0, 0.0}};
      for (int i = 0; i < D; ++i) {
        for (int a = 0; a < 2; ++a) {
          for (int b = 0; b < 2; ++b) {
            gram[a][b] += U[2 * i + a] * (*gradient_u)[2 * i + b];
          }
        }
      }
      const double off = 0.5 * (gram[0][1] + gram[1][0]);
      gram[0][1] = gram[1][0] = off;
      for (int i = 0; i < D; ++i) {
        const double u0 = U[2 * i], u1 = U[2 * i + 1];
        (*gradient_u)[2 * i] -= u0 * gram[0][0] + u1 * gram[1][0];
        (*gradient_u)[2 * i + 1] -=
            u0 * gram[0][1] + u1 * gram[1][1];
      }

      double q_lambda = 0.0, q_mu = 0.0;
      for (int i = 0; i < D; ++i) {
        for (int j = 0; j < D; ++j) {
          q_lambda += 2.0 * G[i * D + j] * U[2 * i] * U[2 * j];
          q_mu +=
              2.0 * G[i * D + j] * U[2 * i + 1] * U[2 * j + 1];
        }
      }
      *gradient_theta =
          -std::sin(theta) * q_lambda + std::cos(theta) * q_mu;
      if (mode == Mode::kPsdQuantitative) {
        *gradient_theta +=
            2.0 * m * (lambda - mu)
            * (std::sin(theta) + std::cos(theta));
      }
      if (mode == Mode::kProjection) *gradient_theta = 0.0;
    }
    return value;
  }

  double one_start(int iterations, double initial_step,
                   std::vector<double>& best_u, double& best_theta) {
    std::vector<double> U(2 * D);
    for (double& x : U) x = normal(rng);
    orthonormalize(U);
    std::uniform_real_distribution<double> positive_angle(
        0.0, 0.5 * std::acos(-1.0));
    std::uniform_real_distribution<double> signed_angle(
        -std::acos(-1.0), std::acos(-1.0));
    double theta =
        mode == Mode::kProjection
            ? 0.25 * std::acos(-1.0)
            : (mode == Mode::kSignedNormal ? signed_angle(rng)
                                           : positive_angle(rng));
    double best = std::numeric_limits<double>::infinity();
    double step = initial_step;

    for (int iter = 0; iter < iterations; ++iter) {
      std::vector<double> grad;
      double grad_theta = 0.0;
      const double value = objective(U, theta, &grad, &grad_theta);
      if (value < best) {
        best = value;
        best_u = U;
        best_theta = theta;
      }

      bool accepted = false;
      double trial_step = step;
      for (int trial = 0; trial < 18; ++trial) {
        std::vector<double> Ut = U;
        for (int k = 0; k < 2 * D; ++k)
          Ut[k] -= trial_step * grad[k];
        orthonormalize(Ut);
        double thetat =
            mode == Mode::kProjection
                ? 0.25 * std::acos(-1.0)
                : theta - trial_step * grad_theta;
        if (mode == Mode::kPsdQuantitative) {
          // Reflect into [0,pi/2].
          const double half_pi = 0.5 * std::acos(-1.0);
          while (thetat < 0.0 || thetat > half_pi) {
            if (thetat < 0.0) thetat = -thetat;
            if (thetat > half_pi) thetat = std::acos(-1.0) - thetat;
          }
        } else if (mode == Mode::kSignedNormal) {
          const double pi = std::acos(-1.0);
          while (thetat < -pi) thetat += 2.0 * pi;
          while (thetat > pi) thetat -= 2.0 * pi;
        }
        const double trial_value =
            objective(Ut, thetat, nullptr, nullptr);
        if (trial_value <= value + 1e-13) {
          U.swap(Ut);
          theta = thetat;
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
    std::cerr
        << "usage: agent_exterior_psd_search d n starts iterations"
        << " [seed] [psd|projection|signed]\n";
    return 2;
  }
  const int d = std::stoi(argv[1]);
  const int n = std::stoi(argv[2]);
  const int starts = std::stoi(argv[3]);
  const int iterations = std::stoi(argv[4]);
  const std::uint64_t seed =
      argc >= 6 ? std::stoull(argv[5]) : UINT64_C(20260728);
  const std::string mode_name = argc >= 7 ? argv[6] : "psd";
  Search::Mode mode = Search::Mode::kPsdQuantitative;
  if (mode_name == "projection") mode = Search::Mode::kProjection;
  if (mode_name == "signed") mode = Search::Mode::kSignedNormal;
  Search search(d, n, seed, mode);
  double global = std::numeric_limits<double>::infinity();
  std::vector<double> global_u;
  double global_theta = 0.0;
  for (int s = 0; s < starts; ++s) {
    std::vector<double> candidate_u;
    double candidate_theta = 0.0;
    const double value =
        search.one_start(iterations, 0.03, candidate_u, candidate_theta);
    if (value < global) {
      global = value;
      global_u.swap(candidate_u);
      global_theta = candidate_theta;
    }
    std::cout << "start " << s << " value " << std::setprecision(17)
              << value << " global " << global << "\n";
  }
  std::cout << "best " << std::setprecision(17) << global << "\n";
  std::cout << "theta " << global_theta << " lambda "
            << std::cos(global_theta) << " mu " << std::sin(global_theta)
            << "\n";
  return 0;
}
