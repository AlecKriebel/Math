// Discovery-only unrestricted complex search for a negative qutrit
// four-copy rank-two projection.
//
// The variable U is an 81-by-2 complex isometry and P=U U^*.  We compute
// all sixteen exact two-replica swap-sector masses p_R through the sixteen
// partial-trace moments A_T.  Three search modes are supported:
//
//   q       minimize the true endpoint Q_4(P);
//   target  minimize squared distance to the first formal negative table;
//   target2 do the same for the second formal table;
//   target3 uses the symmetric filter-resistant point (106) from
//           notes/agent_n4_qubit_reference.md;
//   homotopy / homotopy2 / homotopy3 approach the chosen table, then release
//           the penalty and minimize Q;
//   oddhomotopy3 constrains only the eight odd sectors of target3 and then
//           follows the Q-versus-constraint penalty curve.
//
// Floating-point output is only discovery evidence.  If a robust negative Q
// is found, the two codewords are written as text for exact reconstruction.

#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <vector>

using Complex = std::complex<double>;
using Vec = std::vector<Complex>;

namespace {

constexpr int kD = 81;
constexpr int kLocal = 3;

int popcount4(int x) {
  int out = 0;
  for (; x; x >>= 1) out += x & 1;
  return out;
}

double real_dot(const Vec& x, const Vec& y) {
  Complex z = 0.0;
  for (std::size_t i = 0; i < x.size(); ++i) z += std::conj(x[i]) * y[i];
  return std::real(z);
}

double norm_squared(const Vec& x) {
  double out = 0.0;
  for (const Complex z : x) out += std::norm(z);
  return out;
}

struct Evaluation {
  double q = 0.0;
  double h1 = 0.0;
  double target_loss = 0.0;
  double objective = 0.0;
  std::array<double, 16> moment{};
  std::array<double, 16> sector{};
};

struct Search {
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};
  std::array<double, 16> target{};
  bool minimize_h1;
  bool minimize_e4;
  bool maximize_e4;
  bool odd_target_only;
  bool feasibility_only;

  explicit Search(std::uint64_t seed, int target_id, bool minimize_h1_,
                  bool minimize_e4_, bool maximize_e4_,
                  bool odd_target_only_, bool feasibility_only_ = false)
      : rng(seed),
        minimize_h1(minimize_h1_),
        minimize_e4(minimize_e4_),
        maximize_e4(maximize_e4_),
        odd_target_only(odd_target_only_),
        feasibility_only(feasibility_only_) {
    // Formal tables (31) and (33a) in
    // notes/agent_four_copy_attack.md.  Bits 0,1,2,3 correspond to the
    // displayed sites 1,2,3,4.
    target.fill(0.0);
    if (target_id == 1) {
      target[0] = 21.0 / 16.0;
      target[2] = 1.0 / 16.0;
      target[3] = target[6] = target[10] = 1.0 / 4.0;
      target[5] = target[9] = target[12] = 5.0 / 16.0;
      target[7] = target[11] = target[14] = 11.0 / 48.0;
      target[13] = 1.0 / 4.0;
    } else if (target_id == 2) {
      target[0] = 9.0 / 4.0;
      target[1] = 7.0 / 12.0;
      target[6] = target[10] = target[12] = 1.0 / 4.0;
      target[7] = target[11] = target[13] = 1.0 / 12.0;
      target[14] = 1.0 / 6.0;
    } else {
      // The normalized purification masses are
      // (79/160,1/8,39/160,1/8,1/80) by Hamming layer.  Multiplication
      // by four converts them to the unnormalized code-projector sectors.
      const std::array<double, 5> per_subset = {
          79.0 / 40.0, 1.0 / 8.0, 13.0 / 80.0,
          1.0 / 8.0, 1.0 / 20.0};
      for (int R = 0; R < 16; ++R) target[R] = per_subset[popcount4(R)];
    }
  }

  void orthonormalize(Vec& U) const {
    for (int a = 0; a < 2; ++a) {
      for (int b = 0; b < a; ++b) {
        Complex overlap = 0.0;
        for (int i = 0; i < kD; ++i)
          overlap += std::conj(U[2 * i + b]) * U[2 * i + a];
        for (int i = 0; i < kD; ++i)
          U[2 * i + a] -= overlap * U[2 * i + b];
      }
      double length = 0.0;
      for (int i = 0; i < kD; ++i) length += std::norm(U[2 * i + a]);
      length = std::sqrt(std::max(length, 1e-300));
      for (int i = 0; i < kD; ++i) U[2 * i + a] /= length;
    }
  }

  Vec random_frame() {
    Vec U(2 * kD);
    for (Complex& z : U) z = Complex(normal(rng), normal(rng));
    orthonormalize(U);
    return U;
  }

  Vec projection(const Vec& U) const {
    Vec P(kD * kD);
    for (int i = 0; i < kD; ++i)
      for (int j = 0; j < kD; ++j)
        P[i * kD + j] =
            U[2 * i] * std::conj(U[2 * j]) +
            U[2 * i + 1] * std::conj(U[2 * j + 1]);
    return P;
  }

  Vec column_projection(const Vec& U, int logical) const {
    Vec P(kD * kD);
    for (int i = 0; i < kD; ++i)
      for (int j = 0; j < kD; ++j)
        P[i * kD + j] =
            U[2 * i + logical] * std::conj(U[2 * j + logical]);
    return P;
  }

  Vec trace_replace_site(const Vec& C, int site) const {
    Vec out(kD * kD, 0.0);
    int stride = 1;
    for (int s = 0; s < site; ++s) stride *= kLocal;
    for (int i = 0; i < kD; ++i) {
      const int ii = (i / stride) % kLocal;
      for (int j = 0; j < kD; ++j) {
        if ((j / stride) % kLocal != ii) continue;
        Complex tr = 0.0;
        for (int z = 0; z < kLocal; ++z) {
          const int iz = i + (z - ii) * stride;
          const int jz = j + (z - ii) * stride;
          tr += C[iz * kD + jz];
        }
        out[i * kD + j] = tr;
      }
    }
    return out;
  }

  // maps[R] = (tensor product of trace-and-replace maps at sites in R)(P).
  std::array<Vec, 16> trace_maps(const Vec& P) const {
    std::array<Vec, 16> maps;
    maps[0] = P;
    for (int mask = 1; mask < 16; ++mask) {
      int site = 0;
      while (((mask >> site) & 1) == 0) ++site;
      maps[mask] = trace_replace_site(maps[mask ^ (1 << site)], site);
    }
    return maps;
  }

  std::array<double, 16> cross_sectors(const Vec& U) const {
    const Vec Pu = column_projection(U, 0);
    const Vec Pv = column_projection(U, 1);
    const auto maps_v = trace_maps(Pv);
    std::array<double, 16> g{}, c{};
    for (int T = 0; T < 16; ++T)
      g[T] = real_dot(Pu, maps_v[15 ^ T]);
    for (int R = 0; R < 16; ++R)
      for (int T = 0; T < 16; ++T)
        c[R] += (popcount4(R & T) & 1 ? -1.0 : 1.0) * g[T] / 16.0;
    return c;
  }

  void project_tangent(const Vec& U, Vec& G) const {
    Complex gram[2][2] = {};
    for (int a = 0; a < 2; ++a)
      for (int b = 0; b < 2; ++b)
        for (int i = 0; i < kD; ++i)
          gram[a][b] += std::conj(U[2 * i + a]) * G[2 * i + b];
    const Complex off =
        0.5 * (gram[0][1] + std::conj(gram[1][0]));
    gram[0][0] = std::real(gram[0][0]);
    gram[1][1] = std::real(gram[1][1]);
    gram[0][1] = off;
    gram[1][0] = std::conj(off);
    for (int i = 0; i < kD; ++i)
      for (int a = 0; a < 2; ++a)
        for (int b = 0; b < 2; ++b)
          G[2 * i + a] -= U[2 * i + b] * gram[b][a];
  }

  Evaluation evaluate(const Vec& U, double penalty, Vec* gradient) const {
    const Vec P = projection(U);
    const auto maps = trace_maps(P);
    Evaluation out;

    // A_T = <P, (Tr_{T^c} P) tensor I_{T^c}>.
    for (int T = 0; T < 16; ++T)
      out.moment[T] = real_dot(P, maps[15 ^ T]);

    for (int R = 0; R < 16; ++R) {
      double value = 0.0;
      for (int T = 0; T < 16; ++T) {
        const double sign = popcount4(R & T) & 1 ? -1.0 : 1.0;
        value += sign * out.moment[T];
      }
      out.sector[R] = value / 16.0;
      const double residual = out.sector[R] - target[R];
      if (!odd_target_only || (popcount4(R) & 1))
        out.target_loss += 0.5 * residual * residual;
      out.q += std::ldexp(1.0, -4) *
               (popcount4(R) & 1 ? -1.0 : 1.0) *
               std::pow(3.0, popcount4(R)) * out.sector[R];
      const int weight = popcount4(R);
      if (weight == 2) out.h1 += out.sector[R];
      if (weight == 3) out.h1 -= 3.0 * out.sector[R];
      if (weight == 4) out.h1 += 6.0 * out.sector[R];
    }
    const double base_objective =
        feasibility_only
            ? 0.0
            : (minimize_e4
            ? out.sector[15]
            : (maximize_e4 ? -out.sector[15]
                           : (minimize_h1 ? out.h1 : out.q)));
    out.objective = base_objective + penalty * out.target_loss;

    if (!gradient) return out;

    // Coefficient of each moment A_T in Q + penalty*target_loss.
    std::array<double, 16> coefficient{};
    for (int T = 0; T < 16; ++T) {
      for (int R = 0; R < 16; ++R) {
        const int weight = popcount4(R);
        double sector_coefficient = 0.0;
        if (feasibility_only) {
          sector_coefficient = 0.0;
        } else if (minimize_e4 || maximize_e4) {
          if (R == 15)
            sector_coefficient = maximize_e4 ? -1.0 : 1.0;
        } else if (minimize_h1) {
          if (weight == 2) sector_coefficient = 1.0;
          if (weight == 3) sector_coefficient = -3.0;
          if (weight == 4) sector_coefficient = 6.0;
        } else {
          sector_coefficient =
              std::ldexp(1.0, -4) *
              (weight & 1 ? -1.0 : 1.0) * std::pow(3.0, weight);
        }
        const double sign = popcount4(R & T) & 1 ? -1.0 : 1.0;
        coefficient[T] += sector_coefficient * sign / 16.0;
      }
    }
    if (penalty != 0.0) {
      for (int T = 0; T < 16; ++T) {
        double derivative = 0.0;
        for (int R = 0; R < 16; ++R) {
          if (odd_target_only && !(popcount4(R) & 1)) continue;
          const double sign = popcount4(R & T) & 1 ? -1.0 : 1.0;
          derivative += (out.sector[R] - target[R]) * sign / 16.0;
        }
        coefficient[T] += penalty * derivative;
      }
    }

    Vec operator_sum(kD * kD, 0.0);
    for (int T = 0; T < 16; ++T) {
      const Vec& M = maps[15 ^ T];
      for (int k = 0; k < kD * kD; ++k)
        operator_sum[k] += coefficient[T] * M[k];
    }
    gradient->assign(2 * kD, 0.0);
    for (int i = 0; i < kD; ++i)
      for (int j = 0; j < kD; ++j)
        for (int a = 0; a < 2; ++a)
          (*gradient)[2 * i + a] +=
              4.0 * operator_sum[i * kD + j] * U[2 * j + a];
    project_tangent(U, *gradient);
    return out;
  }

  // Riemannian steepest descent with QR retraction and Armijo backtracking.
  Evaluation descend(Vec& U, double penalty, int iterations,
                     double initial_step) const {
    Evaluation best = evaluate(U, penalty, nullptr);
    Vec best_U = U;
    double step = initial_step;
    for (int iteration = 0; iteration < iterations; ++iteration) {
      Vec gradient;
      const Evaluation current = evaluate(U, penalty, &gradient);
      const double grad2 = norm_squared(gradient);
      if (current.objective < best.objective) {
        best = current;
        best_U = U;
      }
      if (grad2 < 1e-24) break;

      bool accepted = false;
      double trial = step;
      for (int backtrack = 0; backtrack < 30; ++backtrack) {
        Vec V = U;
        for (int k = 0; k < 2 * kD; ++k) V[k] -= trial * gradient[k];
        orthonormalize(V);
        const Evaluation candidate = evaluate(V, penalty, nullptr);
        if (candidate.objective <=
            current.objective - 1e-4 * trial * grad2) {
          U.swap(V);
          step = std::min(initial_step, 1.25 * trial);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    U = best_U;
    return best;
  }

  void perturb(Vec& U, double scale) {
    for (Complex& z : U)
      z += scale * Complex(normal(rng), normal(rng));
    orthonormalize(U);
  }

  void print(const Vec& U, const Evaluation& value) const {
    double even = 0.0, odd = 0.0, e2 = 0.0, o3 = 0.0;
    for (int R = 0; R < 16; ++R) {
      if (popcount4(R) & 1) odd += value.sector[R];
      else even += value.sector[R];
      if (popcount4(R) == 2) e2 += value.sector[R];
      if (popcount4(R) == 3) o3 += value.sector[R];
    }
    const double e4 = value.sector[15];
    std::cout << std::setprecision(17)
              << "Q " << value.q << " target_loss " << value.target_loss
              << " H1 " << value.h1 << " e2 " << e2 << " o3 " << o3
              << " e4 " << e4 << " parity " << even << " " << odd
              << "\nsector";
    for (double x : value.sector) std::cout << " " << x;
    std::cout << "\nmoment";
    for (double x : value.moment) std::cout << " " << x;
    const auto cross = cross_sectors(U);
    std::cout << "\ncross";
    for (double x : cross) std::cout << " " << x;
    std::cout << "\n";
  }

  void save(const Vec& U, const std::string& path) const {
    std::ofstream out(path);
    out << std::setprecision(17);
    for (int i = 0; i < kD; ++i)
      out << i << " " << std::real(U[2 * i]) << " "
          << std::imag(U[2 * i]) << " "
          << std::real(U[2 * i + 1]) << " "
          << std::imag(U[2 * i + 1]) << "\n";
  }

  Vec load(const std::string& path) const {
    std::ifstream in(path);
    Vec U(2 * kD, 0.0);
    int i;
    double ur, ui, vr, vi;
    while (in >> i >> ur >> ui >> vr >> vi) {
      U[2 * i] = Complex(ur, ui);
      U[2 * i + 1] = Complex(vr, vi);
    }
    return U;
  }
};

}  // namespace

int main(int argc, char** argv) {
  if (argc < 3 || argc > 7) {
    std::cerr
        << "usage: search_n4_complex_sector_target"
        << " {q|h1|target|target2|target3|homotopy|homotopy2|homotopy3"
        << "|homotopy3h1|odd3|oddhomotopy3|odde4|odde4max|oddwalk"
        << "|oddfeasible}"
        << " starts iterations"
        << " [seed] [perturbations] [output]\n";
    return 2;
  }
  const std::string mode = argv[1];
  if (mode == "inspect") {
    Search search(0, 3, false, false, false, true);
    Vec U = search.load(argv[2]);
    search.orthonormalize(U);
    search.print(U, search.evaluate(U, 0.0, nullptr));
    return 0;
  }
  if (argc < 4) return 2;
  const int starts = std::stoi(argv[2]);
  const int iterations = std::stoi(argv[3]);
  const std::uint64_t seed =
      argc >= 5 ? std::stoull(argv[4]) : UINT64_C(20260728);
  const int perturbations = argc >= 6 ? std::stoi(argv[5]) : 0;
  const std::string output =
      argc >= 7 ? argv[6] : "discovery/n4_complex_best_frame.txt";
  if (mode != "q" && mode != "h1" &&
      mode != "target" && mode != "homotopy" &&
      mode != "target2" && mode != "homotopy2" &&
      mode != "target3" && mode != "homotopy3" &&
      mode != "homotopy3h1" && mode != "odd3" &&
      mode != "oddhomotopy3" && mode != "odde4" &&
      mode != "odde4max" && mode != "oddwalk" &&
      mode != "oddfeasible")
    return 2;
  if (starts < 1 || iterations < 1 || perturbations < 0) return 2;

  const int target_id =
      (mode == "target2" || mode == "homotopy2")
          ? 2
          : ((mode == "target3" || mode == "homotopy3" ||
              mode == "homotopy3h1")
              || mode == "odd3" || mode == "oddhomotopy3" ||
              mode == "odde4" || mode == "odde4max" ||
              mode == "oddwalk" || mode == "oddfeasible"
                 ? 3
                 : 1);
  const bool target_only =
      mode == "target" || mode == "target2" || mode == "target3" ||
      mode == "odd3" || mode == "oddwalk" || mode == "oddfeasible";
  const bool constrained_e4 = mode == "odde4" || mode == "odde4max";
  const bool homotopy =
      mode == "homotopy" || mode == "homotopy2" ||
      mode == "homotopy3" || mode == "homotopy3h1" ||
      mode == "oddhomotopy3";
  const bool minimize_h1 = mode == "h1" || mode == "homotopy3h1";
  const bool minimize_e4 = mode == "odde4";
  const bool maximize_e4 = mode == "odde4max";
  const bool odd_target_only =
      mode == "odd3" || mode == "oddhomotopy3" ||
      mode == "odde4" || mode == "odde4max" || mode == "oddwalk" ||
      mode == "oddfeasible";
  const bool feasibility_only = mode == "oddfeasible";
  Search search(seed, target_id, minimize_h1, minimize_e4, maximize_e4,
                odd_target_only, feasibility_only);
  double global_score = std::numeric_limits<double>::infinity();
  Evaluation global_value;
  Vec global_U;
  for (int start = 0; start < starts; ++start) {
    Vec U = mode == "oddwalk" ? search.load(output) : search.random_frame();
    if (mode == "oddwalk") {
      search.orthonormalize(U);
      search.perturb(U, 0.15);
    }
    Evaluation value;
    if (mode == "q" || mode == "h1") {
      value = search.descend(U, 0.0, iterations, 0.1);
    } else if (target_only || constrained_e4) {
      // Subtracting Q is not part of the target loss.  A huge penalty makes
      // its contribution negligible while retaining the common evaluator.
      value = search.descend(U, 1.0e6, iterations, 0.03);
    } else if (homotopy) {
      // Approach the formal table, then release its influence continuously.
      value = search.descend(U, 1.0e4, iterations, 0.03);
      const std::array<double, 9> schedule =
          {1.0e3, 1.0e2, 30.0, 10.0, 3.0, 1.0, 0.3, 0.03, 0.0};
      const int stage_iterations = std::max(50, iterations / 3);
      for (double penalty : schedule) {
        value = search.descend(U, penalty, stage_iterations, 0.05);
        if (start == 0)
          std::cout << "stage penalty " << std::setprecision(10) << penalty
                    << " Q " << value.q << " H1 " << value.h1
                    << " loss " << value.target_loss << "\n";
      }
    }

    for (int p = 0; p < perturbations; ++p) {
      Vec V = U;
      search.perturb(V, std::pow(0.35, 1 + (p % 5)));
      Evaluation trial =
          search.descend(V, (target_only || constrained_e4) ? 1.0e6 : 0.0,
                         std::max(100, iterations / 2), 0.08);
      const double lhs = target_only
                             ? trial.target_loss
                             : (minimize_e4
                                    ? trial.sector[15]
                                    : (maximize_e4
                                           ? -trial.sector[15]
                                           : (minimize_h1 ? trial.h1
                                                          : trial.q)));
      const double rhs = target_only
                             ? value.target_loss
                             : (minimize_e4
                                    ? value.sector[15]
                                    : (maximize_e4
                                           ? -value.sector[15]
                                           : (minimize_h1 ? value.h1
                                                          : value.q)));
      if (lhs < rhs) {
        U.swap(V);
        value = trial;
      }
    }

    value = search.evaluate(U, 0.0, nullptr);
    const double score =
        target_only
            ? value.target_loss
            : (minimize_e4 ? value.sector[15]
                           : (maximize_e4
                                  ? -value.sector[15]
                                  : (minimize_h1 ? value.h1 : value.q)));
    if (score < global_score) {
      global_score = score;
      global_value = value;
      global_U = U;
      search.save(global_U, output);
    }
    std::cout << "start " << start << " score " << std::setprecision(17)
              << score << " global " << global_score << "\n";
    search.print(U, value);
  }
  std::cout << "BEST\n";
  search.print(global_U, global_value);
  search.save(global_U, output);
  return 0;
}
