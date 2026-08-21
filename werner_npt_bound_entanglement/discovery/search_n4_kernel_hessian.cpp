// Discovery-only test of the local balanced-kernel Hessian from
// notes/agent_n4_qubit_reference.md, Proposition 20.1.
//
// For a complex Stiefel frame U : C^2 -> (C^3)^tensor4, a physical site i,
// and
//   K_i = {A=A^* in M_3 : U^*(A_i tensor I)U=0},
// this program computes the real quadratic form
//   N_i(A)=Tr[(P tensor P)(A tensor A)_i K_4],
//   K_4=product_j(F_j-I/2), P=UU^*,
// restricted to K_i.  It reports its least eigenvalue and trace, as well as
// the proposed scalar separator trace(N_i|K_i)-F(P)/8.
//
// All calculations are floating point and are discovery evidence only.

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
constexpr int kRest = 27;

int popcount4(int x) {
  int out = 0;
  for (; x; x >>= 1) out += x & 1;
  return out;
}

int digit(int index, int site) {
  for (int s = 0; s < site; ++s) index /= kLocal;
  return index % kLocal;
}

int ket(int a, int b, int c, int d) {
  return a + 3 * b + 9 * c + 27 * d;
}

std::array<std::array<Complex, 9>, 9> hermitian_basis() {
  std::array<std::array<Complex, 9>, 9> G{};
  for (int a = 0; a < 3; ++a) G[a][3 * a + a] = 1.0;
  int mu = 3;
  const double z = 1.0 / std::sqrt(2.0);
  for (int a = 0; a < 3; ++a) {
    for (int b = a + 1; b < 3; ++b) {
      G[mu][3 * a + b] = z;
      G[mu][3 * b + a] = z;
      ++mu;
      G[mu][3 * a + b] = Complex(0.0, -z);
      G[mu][3 * b + a] = Complex(0.0, z);
      ++mu;
    }
  }
  return G;
}

// Jacobi diagonalization of a real symmetric matrix.  On return A is
// diagonal, and the columns of V are the corresponding eigenvectors.
void jacobi(std::vector<double>& A, int n, std::vector<double>& V) {
  V.assign(n * n, 0.0);
  for (int i = 0; i < n; ++i) V[i * n + i] = 1.0;
  for (int sweep = 0; sweep < 100 * n * n; ++sweep) {
    int p = 0, q = 1;
    double largest = 0.0;
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        const double value = std::abs(A[i * n + j]);
        if (value > largest) {
          largest = value;
          p = i;
          q = j;
        }
      }
    }
    if (largest < 1e-13) break;
    const double app = A[p * n + p];
    const double aqq = A[q * n + q];
    const double apq = A[p * n + q];
    const double angle = 0.5 * std::atan2(2.0 * apq, aqq - app);
    const double c = std::cos(angle), s = std::sin(angle);
    for (int k = 0; k < n; ++k) {
      if (k == p || k == q) continue;
      const double akp = A[k * n + p];
      const double akq = A[k * n + q];
      A[k * n + p] = A[p * n + k] = c * akp - s * akq;
      A[k * n + q] = A[q * n + k] = s * akp + c * akq;
    }
    A[p * n + p] =
        c * c * app - 2.0 * s * c * apq + s * s * aqq;
    A[q * n + q] =
        s * s * app + 2.0 * s * c * apq + c * c * aqq;
    A[p * n + q] = A[q * n + p] = 0.0;
    for (int k = 0; k < n; ++k) {
      const double vkp = V[k * n + p];
      const double vkq = V[k * n + q];
      V[k * n + p] = c * vkp - s * vkq;
      V[k * n + q] = s * vkp + c * vkq;
    }
  }
}

struct Result {
  int kernel_dimension = 0;
  double f = 0.0;
  double lambda_min = 0.0;
  double lambda_max = 0.0;
  double trace_kernel = 0.0;
  double trace_full = 0.0;
  double trace_range = 0.0;
  double trace_gap = 0.0;
  int full_positive = 0;
  int full_negative = 0;
  double compression_small = 0.0;
  double compression_large = 0.0;
  double local_determinant = 0.0;
};

struct Search {
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};
  const std::array<std::array<Complex, 9>, 9> G = hermitian_basis();

  explicit Search(std::uint64_t seed) : rng(seed) {}

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

  Vec random_sparse_frame() {
    Vec U(2 * kD, 0.0);
    std::array<int, kD> permutation{};
    for (int i = 0; i < kD; ++i) permutation[i] = i;
    std::shuffle(permutation.begin(), permutation.end(), rng);
    std::uniform_int_distribution<int> support_size(2, 10);
    const int n0 = support_size(rng);
    const int n1 = support_size(rng);
    for (int j = 0; j < n0; ++j)
      U[2 * permutation[j]] = Complex(normal(rng), normal(rng));
    for (int j = 0; j < n1; ++j)
      U[2 * permutation[n0 + j] + 1] =
          Complex(normal(rng), normal(rng));
    orthonormalize(U);
    return U;
  }

  // Frames with a balanced local orthonormal basis:
  //
  //   U = sum_i sqrt(r_i) |i> V_i,       V_i^* V_i = I_2.
  //
  // In the `rank_three` family, V_2 is orthogonal to both V_0 and V_1.
  // Consequently the only nonscalar logical compression comes from
  // V_0^* V_1, so the real compression rank is at most three.  The
  // `rank_one` family makes all three ranges mutually orthogonal.
  Vec random_balanced_frame(int site, bool rank_three) {
    // A random orthonormal six-frame in the three-site complement.
    std::vector<Complex> Q(6 * kRest);
    for (Complex& z : Q) z = Complex(normal(rng), normal(rng));
    for (int a = 0; a < 6; ++a) {
      for (int b = 0; b < a; ++b) {
        Complex overlap = 0.0;
        for (int z = 0; z < kRest; ++z)
          overlap += std::conj(Q[6 * z + b]) * Q[6 * z + a];
        for (int z = 0; z < kRest; ++z)
          Q[6 * z + a] -= overlap * Q[6 * z + b];
      }
      double length = 0.0;
      for (int z = 0; z < kRest; ++z)
        length += std::norm(Q[6 * z + a]);
      length = std::sqrt(std::max(length, 1e-300));
      for (int z = 0; z < kRest; ++z) Q[6 * z + a] /= length;
    }

    std::array<std::array<std::vector<Complex>, 2>, 3> V;
    for (auto& pair : V)
      for (auto& column : pair) column.assign(kRest, 0.0);
    for (int r = 0; r < 2; ++r)
      for (int z = 0; z < kRest; ++z)
        V[0][r][z] = Q[6 * z + r];

    if (!rank_three) {
      for (int i = 1; i < 3; ++i)
        for (int r = 0; r < 2; ++r)
          for (int z = 0; z < kRest; ++z)
            V[i][r][z] = Q[6 * z + 2 * i + r];
    } else {
      std::uniform_real_distribution<double> uniform(0.0, 1.0);
      const double c0 = uniform(rng);
      const double c1 = uniform(rng);
      const double s0 = std::sqrt(1.0 - c0 * c0);
      const double s1 = std::sqrt(1.0 - c1 * c1);
      std::array<std::vector<Complex>, 2> base;
      for (auto& column : base) column.assign(kRest, 0.0);
      for (int z = 0; z < kRest; ++z) {
        base[0][z] = c0 * Q[6 * z] + s0 * Q[6 * z + 2];
        base[1][z] = c1 * Q[6 * z + 1] + s1 * Q[6 * z + 3];
      }

      // Haar-distributed right logical unitary for V_1.
      std::array<Complex, 4> R;
      for (Complex& value : R) value = Complex(normal(rng), normal(rng));
      double length0 = std::sqrt(std::norm(R[0]) + std::norm(R[2]));
      R[0] /= length0;
      R[2] /= length0;
      const Complex overlap = std::conj(R[0]) * R[1] +
                              std::conj(R[2]) * R[3];
      R[1] -= overlap * R[0];
      R[3] -= overlap * R[2];
      const double length1 =
          std::sqrt(std::norm(R[1]) + std::norm(R[3]));
      R[1] /= length1;
      R[3] /= length1;
      for (int r = 0; r < 2; ++r)
        for (int z = 0; z < kRest; ++z)
          V[1][r][z] = base[0][z] * R[r] + base[1][z] * R[2 + r];
      for (int r = 0; r < 2; ++r)
        for (int z = 0; z < kRest; ++z)
          V[2][r][z] = Q[6 * z + 4 + r];
    }

    std::array<double, 3> weights{};
    double weight_sum = 0.0;
    for (double& weight : weights) {
      weight = std::norm(Complex(normal(rng), normal(rng)));
      weight_sum += weight;
    }
    for (double& weight : weights) weight /= weight_sum;

    Vec U(2 * kD, 0.0);
    for (int local = 0; local < 3; ++local) {
      for (int rest = 0; rest < kRest; ++rest) {
        int rr = rest, global = 0, stride = 1;
        for (int s = 0; s < 4; ++s) {
          const int value = s == site ? local : rr % 3;
          if (s != site) rr /= 3;
          global += value * stride;
          stride *= 3;
        }
        for (int logical = 0; logical < 2; ++logical)
          U[2 * global + logical] =
              std::sqrt(weights[local]) * V[local][logical][rest];
      }
    }
    return U;
  }

  int global_index(int local, int rest, int site) const {
    int rr = rest, global = 0, stride = 1;
    for (int s = 0; s < 4; ++s) {
      const int value = s == site ? local : rr % 3;
      if (s != site) rr /= 3;
      global += value * stride;
      stride *= 3;
    }
    return global;
  }

  void orthonormalize_rest_pair(
      std::array<std::vector<Complex>, 2>& pair) const {
    for (int a = 0; a < 2; ++a) {
      for (int b = 0; b < a; ++b) {
        Complex overlap = 0.0;
        for (int z = 0; z < kRest; ++z)
          overlap += std::conj(pair[b][z]) * pair[a][z];
        for (int z = 0; z < kRest; ++z)
          pair[a][z] -= overlap * pair[b][z];
      }
      double length = 0.0;
      for (int z = 0; z < kRest; ++z)
        length += std::norm(pair[a][z]);
      length = std::sqrt(std::max(length, 1e-300));
      for (int z = 0; z < kRest; ++z) pair[a][z] /= length;
    }
  }

  // Local proposal within the rank-at-most-three balanced-ONB stratum.
  // V_0 and V_1 are arbitrary isometries; V_2 is kept orthogonal to their
  // joint range.  Therefore V_2^*V_0=V_2^*V_1=0 and the traceless
  // compression range is generated by Re(V_0^*V_1) and Im(V_0^*V_1).
  void perturb_balanced(Vec& U, int site, double scale,
                        double weight_floor = 0.0) {
    std::array<double, 3> weights{};
    std::array<std::array<std::vector<Complex>, 2>, 3> V;
    for (auto& pair : V)
      for (auto& column : pair) column.assign(kRest, 0.0);
    for (int local = 0; local < 3; ++local) {
      for (int logical = 0; logical < 2; ++logical)
        for (int rest = 0; rest < kRest; ++rest)
          weights[local] +=
              0.5 * std::norm(U[2 * global_index(local, rest, site) +
                                logical]);
      const double inverse = 1.0 / std::sqrt(std::max(weights[local], 1e-15));
      for (int logical = 0; logical < 2; ++logical)
        for (int rest = 0; rest < kRest; ++rest)
          V[local][logical][rest] =
              inverse * U[2 * global_index(local, rest, site) + logical];
    }

    const double entry_scale = scale / std::sqrt(2.0 * kRest);
    for (int local = 0; local < 2; ++local) {
      for (int logical = 0; logical < 2; ++logical)
        for (int rest = 0; rest < kRest; ++rest)
          V[local][logical][rest] +=
              entry_scale * Complex(normal(rng), normal(rng));
      orthonormalize_rest_pair(V[local]);
    }

    // Build an orthonormal basis of ran(V_0)+ran(V_1).
    std::vector<std::vector<Complex>> span;
    for (int local = 0; local < 2; ++local) {
      for (int logical = 0; logical < 2; ++logical) {
        std::vector<Complex> q = V[local][logical];
        for (const auto& prior : span) {
          Complex overlap = 0.0;
          for (int rest = 0; rest < kRest; ++rest)
            overlap += std::conj(prior[rest]) * q[rest];
          for (int rest = 0; rest < kRest; ++rest)
            q[rest] -= overlap * prior[rest];
        }
        double length = 0.0;
        for (Complex value : q) length += std::norm(value);
        if (length > 1e-18) {
          length = std::sqrt(length);
          for (Complex& value : q) value /= length;
          span.push_back(q);
        }
      }
    }

    for (int logical = 0; logical < 2; ++logical) {
      for (int rest = 0; rest < kRest; ++rest)
        V[2][logical][rest] +=
            entry_scale * Complex(normal(rng), normal(rng));
      for (const auto& prior : span) {
        Complex overlap = 0.0;
        for (int rest = 0; rest < kRest; ++rest)
          overlap += std::conj(prior[rest]) * V[2][logical][rest];
        for (int rest = 0; rest < kRest; ++rest)
          V[2][logical][rest] -= overlap * prior[rest];
      }
      for (int prior_logical = 0; prior_logical < logical;
           ++prior_logical) {
        Complex overlap = 0.0;
        for (int rest = 0; rest < kRest; ++rest)
          overlap += std::conj(V[2][prior_logical][rest]) *
                     V[2][logical][rest];
        for (int rest = 0; rest < kRest; ++rest)
          V[2][logical][rest] -=
              overlap * V[2][prior_logical][rest];
      }
      double length = 0.0;
      for (Complex value : V[2][logical]) length += std::norm(value);
      length = std::sqrt(std::max(length, 1e-300));
      for (Complex& value : V[2][logical]) value /= length;
    }

    if (weight_floor == 0.0) {
      double maximum_log = -std::numeric_limits<double>::infinity();
      std::array<double, 3> log_weights{};
      for (int local = 0; local < 3; ++local) {
        log_weights[local] =
            std::log(std::max(weights[local], 1e-15)) +
            scale * normal(rng);
        maximum_log = std::max(maximum_log, log_weights[local]);
      }
      double weight_sum = 0.0;
      for (int local = 0; local < 3; ++local) {
        weights[local] = std::exp(log_weights[local] - maximum_log);
        weight_sum += weights[local];
      }
      for (double& weight : weights) weight /= weight_sum;
    } else {
      // Euclidean projection of a noisy proposal onto
      // {r_i >= weight_floor, sum r_i=1}.
      std::array<double, 3> shifted{};
      for (int local = 0; local < 3; ++local)
        shifted[local] =
            weights[local] + 0.25 * scale * normal(rng) - weight_floor;
      std::array<double, 3> sorted = shifted;
      std::sort(sorted.begin(), sorted.end(), std::greater<double>());
      const double target = 1.0 - 3.0 * weight_floor;
      double partial = 0.0, theta = 0.0;
      for (int j = 0; j < 3; ++j) {
        partial += sorted[j];
        const double candidate = (partial - target) / (j + 1);
        if (sorted[j] - candidate > 0.0) theta = candidate;
      }
      for (int local = 0; local < 3; ++local)
        weights[local] =
            weight_floor + std::max(0.0, shifted[local] - theta);
    }

    std::fill(U.begin(), U.end(), Complex(0.0));
    for (int local = 0; local < 3; ++local)
      for (int rest = 0; rest < kRest; ++rest)
        for (int logical = 0; logical < 2; ++logical)
          U[2 * global_index(local, rest, site) + logical] =
              std::sqrt(weights[local]) * V[local][logical][rest];
  }

  void perturb(Vec& U, double scale) {
    for (Complex& z : U)
      z += scale * Complex(normal(rng), normal(rng));
    orthonormalize(U);
  }

  // Moment A_T=||Tr_{T^c}(WW^*)||_2^2 for a not-necessarily-isometric
  // 81-by-2 frame W.
  double moment(const Vec& W, int T) const {
    std::array<int, 4> kept{}, lost{};
    int nk = 0, nl = 0;
    for (int s = 0; s < 4; ++s) {
      if ((T >> s) & 1)
        kept[nk++] = s;
      else
        lost[nl++] = s;
    }
    int dk = 1, dl = 1;
    for (int j = 0; j < nk; ++j) dk *= 3;
    for (int j = 0; j < nl; ++j) dl *= 3;
    std::vector<int> index(dk * dl);
    for (int x = 0; x < dk; ++x) {
      for (int z = 0; z < dl; ++z) {
        int xx = x, zz = z, global = 0, stride = 1;
        for (int s = 0; s < 4; ++s) {
          int value = 0;
          bool is_kept = false;
          for (int j = 0; j < nk; ++j) {
            if (kept[j] == s) {
              is_kept = true;
              break;
            }
          }
          if (is_kept) {
            value = xx % 3;
            xx /= 3;
          } else {
            value = zz % 3;
            zz /= 3;
          }
          global += value * stride;
          stride *= 3;
        }
        index[x * dl + z] = global;
      }
    }
    double out = 0.0;
    for (int x = 0; x < dk; ++x) {
      for (int y = 0; y < dk; ++y) {
        Complex entry = 0.0;
        for (int z = 0; z < dl; ++z) {
          const int ix = index[x * dl + z];
          const int iy = index[y * dl + z];
          for (int a = 0; a < 2; ++a)
            entry += W[2 * ix + a] * std::conj(W[2 * iy + a]);
        }
        out += std::norm(entry);
      }
    }
    return out;
  }

  double endpoint(const Vec& W) const {
    double out = 0.0;
    for (int T = 0; T < 16; ++T)
      out += std::pow(-0.5, 4 - popcount4(T)) * moment(W, T);
    return out;
  }

  // Complex Cholesky E=L L^*.  The caller supplies a positive definite E.
  std::array<Complex, 9> cholesky(
      const std::array<Complex, 9>& E) const {
    std::array<Complex, 9> L{};
    for (int i = 0; i < 3; ++i) {
      for (int j = 0; j <= i; ++j) {
        Complex value = E[3 * i + j];
        for (int k = 0; k < j; ++k)
          value -= L[3 * i + k] * std::conj(L[3 * j + k]);
        if (i == j) {
          L[3 * i + j] = std::sqrt(std::max(0.0, std::real(value)));
        } else {
          L[3 * i + j] = value / L[3 * j + j];
        }
      }
    }
    return L;
  }

  // If E=L L^*, use S=L^* so S^*S=E.  Local-unitary invariance makes
  // endpoint(S P S^*) equal to the effect insertion polynomial q(E).
  Vec filter(const Vec& U, int site,
             const std::array<Complex, 9>& E) const {
    const auto L = cholesky(E);
    Vec W(2 * kD, 0.0);
    const int stride = static_cast<int>(std::pow(3, site));
    for (int global = 0; global < kD; ++global) {
      const int a = digit(global, site);
      for (int b = 0; b < 3; ++b) {
        const int source = global + (b - a) * stride;
        // S=L^*: S_ab=conj(L_ba).
        const Complex Sab = std::conj(L[3 * b + a]);
        for (int r = 0; r < 2; ++r)
          W[2 * global + r] += Sab * U[2 * source + r];
      }
    }
    return W;
  }

  std::array<Complex, 9> effect(
      const std::array<double, 9>& coefficients, double t) const {
    std::array<Complex, 9> E{};
    for (int a = 0; a < 3; ++a) E[3 * a + a] = 1.0;
    for (int mu = 0; mu < 9; ++mu)
      for (int k = 0; k < 9; ++k)
        E[k] += t * coefficients[mu] * G[mu][k];
    return E;
  }

  double effect_endpoint(const Vec& U, int site,
                         const std::array<double, 9>& coefficients,
                         double t) const {
    return endpoint(filter(U, site, effect(coefficients, t)));
  }

  Result evaluate(const Vec& U, int site) const {
    Result out;
    out.f = endpoint(U);

    std::array<Complex, 9> local_reduction{};
    const int local_stride = static_cast<int>(std::pow(3, site));
    for (int i = 0; i < kD; ++i) {
      const int a = digit(i, site);
      for (int b = 0; b < 3; ++b) {
        const int j = i + (b - a) * local_stride;
        for (int r = 0; r < 2; ++r)
          local_reduction[3 * a + b] +=
              U[2 * i + r] * std::conj(U[2 * j + r]);
      }
    }
    out.local_determinant = std::real(
        local_reduction[0] *
            (local_reduction[4] * local_reduction[8] -
             local_reduction[5] * local_reduction[7]) -
        local_reduction[1] *
            (local_reduction[3] * local_reduction[8] -
             local_reduction[5] * local_reduction[6]) +
        local_reduction[2] *
            (local_reduction[3] * local_reduction[7] -
             local_reduction[4] * local_reduction[6]));

    // Compression map from Herm(3) to Herm(2), in orthonormal real
    // Hermitian bases.  The codomain basis is diagonal, symmetric, and
    // antisymmetric, exactly as the first four entries below.
    std::array<std::array<double, 9>, 4> C{};
    for (int mu = 0; mu < 9; ++mu) {
      Complex M[2][2] = {};
      for (int i = 0; i < kD; ++i) {
        const int a = digit(i, site);
        const int stride = static_cast<int>(std::pow(3, site));
        for (int b = 0; b < 3; ++b) {
          const int j = i + (b - a) * stride;
          const Complex Gab = G[mu][3 * a + b];
          for (int r = 0; r < 2; ++r)
            for (int s = 0; s < 2; ++s)
              M[r][s] +=
                  std::conj(U[2 * i + r]) * Gab * U[2 * j + s];
        }
      }
      C[0][mu] = std::real(M[0][0]);
      C[1][mu] = std::real(M[1][1]);
      C[2][mu] = std::sqrt(2.0) * std::real(M[0][1]);
      C[3][mu] = -std::sqrt(2.0) * std::imag(M[0][1]);
    }

    std::vector<double> gram(81, 0.0), vectors;
    for (int mu = 0; mu < 9; ++mu)
      for (int nu = 0; nu < 9; ++nu)
        for (int r = 0; r < 4; ++r)
          gram[9 * mu + nu] += C[r][mu] * C[r][nu];
    jacobi(gram, 9, vectors);
    std::vector<int> order(9);
    for (int i = 0; i < 9; ++i) order[i] = i;
    std::sort(order.begin(), order.end(),
              [&](int a, int b) { return gram[9 * a + a] <
                                         gram[9 * b + b]; });
    const double threshold = 1e-10;
    int kernel_dimension = 0;
    while (kernel_dimension < 9 &&
           gram[9 * order[kernel_dimension] + order[kernel_dimension]] <
               threshold)
      ++kernel_dimension;
    out.kernel_dimension = kernel_dimension;
    out.compression_small = gram[9 * order[std::max(0, kernel_dimension - 1)] +
                                 order[std::max(0, kernel_dimension - 1)]];
    out.compression_large =
        kernel_dimension < 9
            ? gram[9 * order[kernel_dimension] + order[kernel_dimension]]
            : 0.0;

    // Recover the 9-by-9 Hessian from the exactly quadratic effect
    // polynomial.  The symmetric +/- samples determine linear and diagonal
    // terms; one positive sample for each pair determines its cross term.
    constexpr double t = 0.2;
    std::array<double, 9> linear{}, diagonal{};
    std::vector<double> N(81, 0.0);
    for (int mu = 0; mu < 9; ++mu) {
      std::array<double, 9> c{};
      c[mu] = 1.0;
      const double plus = effect_endpoint(U, site, c, t);
      const double minus = effect_endpoint(U, site, c, -t);
      linear[mu] = (plus - minus) / (2.0 * t);
      diagonal[mu] = (plus + minus - 2.0 * out.f) / (2.0 * t * t);
      N[9 * mu + mu] = diagonal[mu];
      out.trace_full += diagonal[mu];
    }
    for (int mu = 0; mu < 9; ++mu) {
      for (int nu = mu + 1; nu < 9; ++nu) {
        std::array<double, 9> c{};
        c[mu] = c[nu] = 1.0;
        const double together = effect_endpoint(U, site, c, t);
        const double cross =
            (together - out.f - t * (linear[mu] + linear[nu]) -
             t * t * (diagonal[mu] + diagonal[nu])) /
            (2.0 * t * t);
        N[9 * mu + nu] = N[9 * nu + mu] = cross;
      }
    }
    {
      std::vector<double> full_spectrum = N;
      std::vector<double> full_vectors;
      jacobi(full_spectrum, 9, full_vectors);
      for (int mu = 0; mu < 9; ++mu) {
        const double eigenvalue = full_spectrum[9 * mu + mu];
        if (eigenvalue > 1e-10) ++out.full_positive;
        if (eigenvalue < -1e-10) ++out.full_negative;
      }
    }

    // Kernel basis Z consists of the eigenvectors of C^T C with zero
    // eigenvalue.  Restrict N by Z^T N Z.
    if (kernel_dimension == 0) {
      out.lambda_min = std::numeric_limits<double>::infinity();
      out.trace_kernel = 0.0;
      out.trace_gap = -out.f / 8.0;
      return out;
    }
    std::vector<double> restricted(kernel_dimension * kernel_dimension, 0.0);
    for (int a = 0; a < kernel_dimension; ++a) {
      const int ca = order[a];
      for (int b = 0; b < kernel_dimension; ++b) {
        const int cb = order[b];
        double value = 0.0;
        for (int mu = 0; mu < 9; ++mu)
          for (int nu = 0; nu < 9; ++nu)
            value += vectors[9 * mu + ca] * N[9 * mu + nu] *
                     vectors[9 * nu + cb];
        restricted[kernel_dimension * a + b] = value;
      }
    }
    std::vector<double> restricted_vectors;
    jacobi(restricted, kernel_dimension, restricted_vectors);
    out.lambda_min = restricted[0];
    out.lambda_max = restricted[0];
    out.trace_kernel = 0.0;
    for (int a = 0; a < kernel_dimension; ++a) {
      out.lambda_min =
          std::min(out.lambda_min,
                   restricted[kernel_dimension * a + a]);
      out.lambda_max =
          std::max(out.lambda_max,
                   restricted[kernel_dimension * a + a]);
      out.trace_kernel += restricted[kernel_dimension * a + a];
    }
    out.trace_gap = out.trace_kernel - out.f / 8.0;
    out.trace_range = out.trace_full - out.trace_kernel;
    return out;
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
    double ar, ai, br, bi;
    while (in >> i >> ar >> ai >> br >> bi) {
      U[2 * i] = Complex(ar, ai);
      U[2 * i + 1] = Complex(br, bi);
    }
    return U;
  }
};

void print_result(int sample, int site, const Result& r) {
  std::cout << std::setprecision(17)
            << "sample " << sample << " site " << site
            << " F " << r.f
            << " kdim " << r.kernel_dimension
            << " csmall " << r.compression_small
            << " clarge " << r.compression_large
            << " localdet " << r.local_determinant
            << " lambda " << r.lambda_min
            << " lambdaMax " << r.lambda_max
            << " trAll " << r.trace_full
            << " inertia " << r.full_positive << "/" << r.full_negative
            << " trRan " << r.trace_range
            << " trK " << r.trace_kernel
            << " gap " << r.trace_gap << "\n";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 3 || argc > 7) {
    std::cerr << "usage: search_n4_kernel_hessian"
              << " {random|sparse|balanced1|balanced3|file|examples|"
              << "hill-lambda|hill-trace|hillbalanced-f|"
              << "hillbalanced-floor|hillbalanced-lambda|"
              << "hillfile-lambda|hillfile-trace} count_or_path site"
              << " [seed] [steps] [output]\n";
    return 2;
  }
  const std::string mode = argv[1];
  const std::string arg = argv[2];
  const int site = argc >= 4 ? std::stoi(argv[3]) : 0;
  const std::uint64_t seed =
      argc >= 5 ? std::stoull(argv[4]) : UINT64_C(20260728);
  const int steps = argc >= 6 ? std::stoi(argv[5]) : 500;
  const std::string output =
      argc >= 7 ? argv[6] : "discovery/n4_kernel_hessian_best.txt";
  if (site < 0 || site > 3) return 2;
  Search search(seed);

  if (mode == "examples") {
    // Exact sparse stress tests from notes/agent_n4_crossed_kernel.md.
    Vec U(2 * kD, 0.0);
    U[2 * ket(1, 0, 0, 1)] = 1.0 / std::sqrt(6.0);
    U[2 * ket(1, 0, 2, 2)] = 1.0 / std::sqrt(6.0);
    U[2 * ket(2, 2, 0, 2)] = 2.0 / std::sqrt(6.0);
    U[2 * ket(0, 0, 2, 2) + 1] = 2.0 / std::sqrt(5.0);
    U[2 * ket(0, 2, 2, 0) + 1] = 1.0 / std::sqrt(5.0);
    std::cout << "trace-counterexample\n";
    print_result(0, 0, search.evaluate(U, 0));
    search.save(U, "/tmp/n4_kernel_trace_counterexample.txt");

    std::fill(U.begin(), U.end(), Complex(0.0));
    U[2 * ket(1, 2, 2, 1)] = -1.0 / std::sqrt(3.0);
    U[2 * ket(2, 0, 2, 2)] = 1.0 / std::sqrt(3.0);
    U[2 * ket(1, 2, 0, 2)] = 1.0 / std::sqrt(3.0);
    U[2 * ket(1, 1, 2, 2) + 1] = 1.0 / std::sqrt(3.0);
    U[2 * ket(1, 0, 2, 2) + 1] = -1.0 / std::sqrt(3.0);
    U[2 * ket(0, 2, 0, 2) + 1] = 1.0 / std::sqrt(3.0);
    std::cout << "full-inertia-counterexample\n";
    print_result(1, 0, search.evaluate(U, 0));
    search.save(U, "/tmp/n4_kernel_inertia_counterexample.txt");
    return 0;
  }

  if (mode == "file") {
    Vec U = search.load(arg);
    for (int s = 0; s < 4; ++s) print_result(0, s, search.evaluate(U, s));
    return 0;
  }

  if (mode == "random" || mode == "sparse" ||
      mode == "balanced1" || mode == "balanced3") {
    const int count = std::stoi(arg);
    double best_lambda = -std::numeric_limits<double>::infinity();
    double best_gap = -std::numeric_limits<double>::infinity();
    Vec best;
    for (int sample = 0; sample < count; ++sample) {
      Vec U;
      if (mode == "sparse")
        U = search.random_sparse_frame();
      else if (mode == "balanced1")
        U = search.random_balanced_frame(site, false);
      else if (mode == "balanced3")
        U = search.random_balanced_frame(site, true);
      else
        U = search.random_frame();
      const Result r = search.evaluate(U, site);
      print_result(sample, site, r);
      if (r.lambda_min > best_lambda || r.trace_gap > best_gap) {
        if (r.lambda_min > best_lambda) best_lambda = r.lambda_min;
        if (r.trace_gap > best_gap) best_gap = r.trace_gap;
        best = U;
        search.save(best, output);
      }
    }
    std::cout << "best_lambda " << best_lambda
              << " best_gap " << best_gap << "\n";
    return 0;
  }

  if (mode == "hillbalanced-f" || mode == "hillbalanced-floor") {
    const double weight_floor = mode == "hillbalanced-floor" ? 0.05 : 0.0;
    const int starts = std::stoi(arg);
    double global = std::numeric_limits<double>::infinity();
    for (int start = 0; start < starts; ++start) {
      Vec U = search.random_balanced_frame(site, true);
      if (weight_floor > 0.0)
        search.perturb_balanced(U, site, 0.0, weight_floor);
      double score = search.endpoint(U);
      double scale = 0.12;
      for (int step = 0; step < steps; ++step) {
        Vec V = U;
        search.perturb_balanced(V, site, scale, weight_floor);
        const double trial_score = search.endpoint(V);
        if (trial_score < score) {
          U.swap(V);
          score = trial_score;
          scale = std::min(0.25, 1.02 * scale);
        } else {
          scale = std::max(2e-4, 0.997 * scale);
        }
        if ((step + 1) % 100 == 0)
          std::cout << "progress start " << start << " step " << (step + 1)
                    << " F " << score << " scale " << scale << "\n";
      }
      print_result(start, site, search.evaluate(U, site));
      if (score < global) {
        global = score;
        search.save(U, output);
      }
    }
    std::cout << "best_F " << std::setprecision(17) << global << "\n";
    return 0;
  }

  if (mode == "hillbalanced-lambda") {
    const int starts = std::stoi(arg);
    constexpr double weight_floor = 0.05;
    double global = -std::numeric_limits<double>::infinity();
    for (int start = 0; start < starts; ++start) {
      Vec U = search.random_balanced_frame(site, true);
      search.perturb_balanced(U, site, 0.0, weight_floor);
      Result current = search.evaluate(U, site);
      double score = current.lambda_min;
      double scale = 0.08;
      for (int step = 0; step < steps; ++step) {
        Vec V = U;
        search.perturb_balanced(V, site, scale, weight_floor);
        const Result trial = search.evaluate(V, site);
        if (trial.lambda_min > score) {
          U.swap(V);
          current = trial;
          score = trial.lambda_min;
          scale = std::min(0.18, 1.02 * scale);
        } else {
          scale = std::max(2e-4, 0.997 * scale);
        }
        if ((step + 1) % 100 == 0)
          std::cout << "progress start " << start << " step " << (step + 1)
                    << " lambda " << score << " scale " << scale << "\n";
      }
      print_result(start, site, current);
      if (score > global) {
        global = score;
        search.save(U, output);
      }
    }
    std::cout << "best_lambda " << std::setprecision(17) << global << "\n";
    return 0;
  }

  if (mode != "hill-lambda" && mode != "hill-trace" &&
      mode != "hillfile-lambda" && mode != "hillfile-trace")
    return 2;
  const bool trace_objective =
      mode == "hill-trace" || mode == "hillfile-trace";
  const bool from_file =
      mode == "hillfile-lambda" || mode == "hillfile-trace";
  const int starts = from_file ? 1 : std::stoi(arg);
  double global = -std::numeric_limits<double>::infinity();
  for (int start = 0; start < starts; ++start) {
    Vec U = from_file ? search.load(arg) : search.random_frame();
    Result current = search.evaluate(U, site);
    double score = trace_objective ? current.trace_gap : current.lambda_min;
    double scale = 0.08;
    for (int step = 0; step < steps; ++step) {
      Vec V = U;
      search.perturb(V, scale);
      const Result trial = search.evaluate(V, site);
      const double trial_score =
          trace_objective ? trial.trace_gap : trial.lambda_min;
      if (trial_score > score) {
        U.swap(V);
        current = trial;
        score = trial_score;
        scale = std::min(0.15, 1.03 * scale);
      } else {
        scale = std::max(1e-4, 0.995 * scale);
      }
      if ((step + 1) % 25 == 0)
        std::cout << "progress start " << start << " step " << (step + 1)
                  << " score " << score << " scale " << scale << "\n";
    }
    print_result(start, site, current);
    if (score > global) {
      global = score;
      search.save(U, output);
    }
  }
  std::cout << "best_score " << std::setprecision(17) << global << "\n";
  return 0;
}
