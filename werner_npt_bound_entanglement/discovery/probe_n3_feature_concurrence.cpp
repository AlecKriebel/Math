// Discovery-only probe for the coherent Takagi/Hodge sufficient bound.
//
// Given two unrestricted complex Stiefel frames U,V in (C^3)^tensor3,
// this program constructs the exact logical feature state
//
//   K_f = ((2/3) I - G)^Gamma - (2/9) I,
//
// where G is the four-by-four compression of the exact-weight-two
// operator projection to the dyads |u_a><v_b|.  It then evaluates the
// unnormalized two-qubit concurrence
//
//   max(0,s1-s2-s3-s4).
//
// Floating-point output is discovery evidence only.

#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

using C = std::complex<double>;
using Vec = std::vector<C>;
using M4 = std::array<std::array<C, 4>, 4>;

constexpr int d = 3;
constexpr int n = 3;
constexpr int D = 27;

double norm_squared(const Vec& x) {
  double out = 0.0;
  for (C z : x) out += std::norm(z);
  return out;
}

C inner(const Vec& x, const Vec& y) {
  C out = 0.0;
  for (std::size_t i = 0; i < x.size(); ++i)
    out += std::conj(x[i]) * y[i];
  return out;
}

void orthonormalize(Vec& frame) {
  for (int column = 0; column < 2; ++column) {
    for (int earlier = 0; earlier < column; ++earlier) {
      C overlap = 0.0;
      for (int row = 0; row < D; ++row)
        overlap += std::conj(frame[2 * row + earlier])
                   * frame[2 * row + column];
      for (int row = 0; row < D; ++row)
        frame[2 * row + column] -=
            overlap * frame[2 * row + earlier];
    }
    double length = 0.0;
    for (int row = 0; row < D; ++row)
      length += std::norm(frame[2 * row + column]);
    length = std::sqrt(length);
    for (int row = 0; row < D; ++row)
      frame[2 * row + column] /= length;
  }
}

Vec scalar_part(const Vec& matrix, int site) {
  Vec out(D * D, 0.0);
  int place = 1;
  for (int i = 0; i < site; ++i) place *= d;
  for (int row = 0; row < D; ++row) {
    const int digit = (row / place) % d;
    const int base_row = row - digit * place;
    for (int column = 0; column < D; ++column) {
      if ((column / place) % d != digit) continue;
      const int base_column = column - digit * place;
      C trace = 0.0;
      for (int value = 0; value < d; ++value)
        trace += matrix[(base_row + value * place) * D
                        + base_column + value * place];
      out[row * D + column] = trace / 3.0;
    }
  }
  return out;
}

Vec exact_sector(Vec matrix, int traceless_mask) {
  for (int site = 0; site < n; ++site) {
    Vec scalar = scalar_part(matrix, site);
    if ((traceless_mask >> site) & 1)
      for (int i = 0; i < D * D; ++i) matrix[i] -= scalar[i];
    else
      matrix.swap(scalar);
  }
  return matrix;
}

Vec pair_projection(const Vec& matrix) {
  Vec out(D * D, 0.0);
  for (int mask : {3, 5, 6}) {
    Vec part = exact_sector(matrix, mask);
    for (int i = 0; i < D * D; ++i) out[i] += part[i];
  }
  return out;
}

// Diagonalize a small Hermitian matrix by exact two-by-two rotations.
// Eigenvectors are returned as columns of vectors.
std::array<double, 4> hermitian_eigen(
    M4 matrix, M4* vectors_out = nullptr) {
  M4 vectors{};
  for (int i = 0; i < 4; ++i) vectors[i][i] = 1.0;
  for (int sweep = 0; sweep < 100; ++sweep) {
    int p = 0, q = 1;
    double largest = 0.0;
    for (int i = 0; i < 4; ++i)
      for (int j = i + 1; j < 4; ++j)
        if (std::abs(matrix[i][j]) > largest) {
          largest = std::abs(matrix[i][j]);
          p = i;
          q = j;
        }
    if (largest < 1e-14) break;

    const double a = std::real(matrix[p][p]);
    const double e = std::real(matrix[q][q]);
    const C z = matrix[p][q];
    const double midpoint = 0.5 * (a + e);
    const double radius =
        std::hypot(0.5 * (a - e), std::abs(z));
    const double lambda = midpoint - radius;
    C x = z;
    C y = lambda - a;
    double length = std::sqrt(std::norm(x) + std::norm(y));
    if (length < 1e-15) {
      x = 1.0;
      y = 0.0;
      length = 1.0;
    }
    x /= length;
    y /= length;
    // Columns (x,y) and (-conj(y),conj(x)) form a unitary.
    const C u00 = x, u10 = y;
    const C u01 = -std::conj(y), u11 = std::conj(x);

    M4 next = matrix;
    for (int i = 0; i < 4; ++i) {
      const C aip = matrix[i][p], aiq = matrix[i][q];
      next[i][p] = aip * u00 + aiq * u10;
      next[i][q] = aip * u01 + aiq * u11;
    }
    matrix = next;
    for (int j = 0; j < 4; ++j) {
      const C apj = matrix[p][j], aqj = matrix[q][j];
      next[p][j] = std::conj(u00) * apj + std::conj(u10) * aqj;
      next[q][j] = std::conj(u01) * apj + std::conj(u11) * aqj;
    }
    matrix = next;
    matrix[p][q] = matrix[q][p] = 0.0;
    matrix[p][p] = std::real(matrix[p][p]);
    matrix[q][q] = std::real(matrix[q][q]);

    for (int i = 0; i < 4; ++i) {
      const C vip = vectors[i][p], viq = vectors[i][q];
      vectors[i][p] = vip * u00 + viq * u10;
      vectors[i][q] = vip * u01 + viq * u11;
    }
  }
  std::array<double, 4> eigenvalues{};
  for (int i = 0; i < 4; ++i)
    eigenvalues[i] = std::real(matrix[i][i]);
  if (vectors_out) *vectors_out = vectors;
  return eigenvalues;
}

M4 multiply(const M4& a, const M4& b) {
  M4 out{};
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j)
      for (int k = 0; k < 4; ++k) out[i][j] += a[i][k] * b[k][j];
  return out;
}

M4 adjoint(const M4& a) {
  M4 out{};
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j) out[i][j] = std::conj(a[j][i]);
  return out;
}

M4 transpose(const M4& a) {
  M4 out{};
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j) out[i][j] = a[j][i];
  return out;
}

struct Evaluation {
  double concurrence = 0.0;
  double minimum_ppt = 0.0;
  M4 feature{};
  std::array<double, 4> takagi{};
};

std::array<double, 4> takagi_values(const M4& feature) {
  M4 eigenvectors{};
  auto eigenvalues = hermitian_eigen(feature, &eigenvectors);
  M4 diagonal{};
  for (int i = 0; i < 4; ++i)
    diagonal[i][i] = std::sqrt(std::max(0.0, eigenvalues[i]));
  const M4 square_root =
      multiply(multiply(eigenvectors, diagonal), adjoint(eigenvectors));
  M4 j{};
  j[0][3] = j[3][0] = 1.0;
  j[1][2] = j[2][1] = -1.0;
  const M4 tau =
      multiply(multiply(transpose(square_root), j), square_root);
  const M4 tau_square = multiply(tau, adjoint(tau));
  auto squared = hermitian_eigen(tau_square);
  std::array<double, 4> singular{};
  for (int i = 0; i < 4; ++i)
    singular[i] = std::sqrt(std::max(0.0, squared[i]));
  std::sort(singular.begin(), singular.end(), std::greater<double>());
  return singular;
}

double concurrence(const M4& feature) {
  const auto singular = takagi_values(feature);
  return std::max(
      0.0, singular[0] - singular[1] - singular[2] - singular[3]);
}

Evaluation evaluate(const Vec& left, const Vec& right) {
  std::array<Vec, 4> dyads;
  std::array<Vec, 4> images;
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b) {
      const int label = 2 * a + b;
      dyads[label].assign(D * D, 0.0);
      for (int i = 0; i < D; ++i)
        for (int j = 0; j < D; ++j)
          dyads[label][i * D + j] =
              left[2 * i + a] * std::conj(right[2 * j + b]);
      images[label] = pair_projection(dyads[label]);
    }

  M4 gram{};
  for (int a = 0; a < 4; ++a)
    for (int b = 0; b < 4; ++b)
      gram[a][b] = inner(dyads[a], images[b]);

  M4 feature{};
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b)
      for (int c = 0; c < 2; ++c)
        for (int e = 0; e < 2; ++e) {
          const int row = 2 * a + b, column = 2 * c + e;
          const int crossed_row = 2 * a + e;
          const int crossed_column = 2 * c + b;
          const C w = (crossed_row == crossed_column ? 2.0 / 3.0 : 0.0)
                      - gram[crossed_row][crossed_column];
          feature[row][column] =
              w - (row == column ? 2.0 / 9.0 : 0.0);
        }

  const auto singular = takagi_values(feature);

  M4 full_ppt{};
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b)
      for (int c = 0; c < 2; ++c)
        for (int e = 0; e < 2; ++e)
          full_ppt[2 * a + b][2 * c + e] =
              feature[2 * a + e][2 * c + b]
              + ((a == c && b == e) ? 2.0 / 9.0 : 0.0);
  auto ppt_eigen = hermitian_eigen(full_ppt);

  Evaluation out;
  out.concurrence = std::max(
      0.0, singular[0] - singular[1] - singular[2] - singular[3]);
  out.minimum_ppt =
      *std::min_element(ppt_eigen.begin(), ppt_eigen.end());
  out.feature = feature;
  out.takagi = singular;
  return out;
}

int swap_site_index(int pair_index, int site) {
  const int left_index = pair_index / D;
  const int right_index = pair_index % D;
  int place = 1;
  for (int i = 0; i < site; ++i) place *= 3;
  const int a = (left_index / place) % 3;
  const int b = (right_index / place) % 3;
  return (left_index + (b - a) * place) * D
         + right_index + (a - b) * place;
}

Vec apply_antisymmetrizers(Vec vector, int mask) {
  for (int site = 0; site < 3; ++site) {
    if (!((mask >> site) & 1)) continue;
    Vec next(vector.size());
    for (int index = 0; index < D * D; ++index)
      next[index] =
          0.5 * (vector[index] - vector[swap_site_index(index, site)]);
    vector.swap(next);
  }
  return vector;
}

M4 parity_feature(
    const Vec& left, const Vec& right, int mask, double weight) {
  std::array<Vec, 4> logical;
  std::array<Vec, 4> images;
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b) {
      const int label = 2 * a + b;
      logical[label].resize(D * D);
      for (int i = 0; i < D; ++i)
        for (int j = 0; j < D; ++j)
          logical[label][i * D + j] =
              std::conj(left[2 * i + a]) * right[2 * j + b];
      images[label] = apply_antisymmetrizers(logical[label], mask);
    }
  M4 out{};
  for (int a = 0; a < 4; ++a)
    for (int b = 0; b < 4; ++b)
      out[a][b] = weight * inner(logical[a], images[b]);
  return out;
}

double partition_concurrence_sum(
    const Vec& left, const Vec& right, int subset) {
  const std::array<int, 4> masks{3, 5, 6, 7};
  const std::array<double, 4> weights{
      4.0 / 9.0, 4.0 / 9.0, 4.0 / 9.0, 8.0 / 9.0};
  M4 first{}, second{};
  for (int g = 0; g < 4; ++g) {
    const M4 part =
        parity_feature(left, right, masks[g], weights[g]);
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j)
        ((subset >> g) & 1 ? first : second)[i][j] += part[i][j];
  }
  return concurrence(first) + concurrence(second);
}

double common_plane_floor_objective(const Vec& left, const Vec& right) {
  M4 q2{};
  for (int mask : {3, 5, 6}) {
    const M4 part = parity_feature(left, right, mask, 4.0 / 9.0);
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j) q2[i][j] += part[i][j];
  }
  const M4 q3 = parity_feature(left, right, 7, 8.0 / 9.0);
  M4 q2_ppt{};
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b)
      for (int c = 0; c < 2; ++c)
        for (int e = 0; e < 2; ++e)
          q2_ppt[2 * a + b][2 * c + e] =
              q2[2 * a + e][2 * c + b];
  const auto eigen = hermitian_eigen(q2_ppt);
  const double minimum =
      *std::min_element(eigen.begin(), eigen.end());
  double trace_q3 = 0.0;
  for (int i = 0; i < 4; ++i) trace_q3 += std::real(q3[i][i]);
  return -minimum + 0.5 * trace_q3;
}

double q2_concurrence_objective(const Vec& left, const Vec& right) {
  M4 q2{};
  for (int mask : {3, 5, 6}) {
    const M4 part = parity_feature(left, right, mask, 4.0 / 9.0);
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j) q2[i][j] += part[i][j];
  }
  return concurrence(q2);
}

double shifted_pair_violation(const Vec& left, const Vec& right) {
  std::array<Vec, 4> dyads;
  std::array<Vec, 4> images;
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b) {
      const int label = 2 * a + b;
      dyads[label].assign(D * D, 0.0);
      for (int i = 0; i < D; ++i)
        for (int j = 0; j < D; ++j)
          dyads[label][i * D + j] =
              left[2 * i + a] * std::conj(right[2 * j + b]);
      images[label] = pair_projection(dyads[label]);
    }
  const double g00 = std::real(inner(dyads[0], images[0]));
  const double g11 = std::real(inner(dyads[3], images[3]));
  const C g01 = inner(dyads[0], images[3]);
  const double p = std::max(0.0, 4.0 / 9.0 - g00);
  const double q = std::max(0.0, 4.0 / 9.0 - g11);
  return std::abs(g01) - 2.0 / 9.0 - std::sqrt(p * q);
}

double conjugate_plane_determinant_overlap(
    const Vec& left, const Vec& right) {
  C overlap[2][2]{};
  for (int a = 0; a < 2; ++a)
    for (int b = 0; b < 2; ++b)
      for (int row = 0; row < D; ++row)
        overlap[a][b] +=
            left[2 * row + a] * right[2 * row + b];
  return std::abs(
      overlap[0][0] * overlap[1][1]
      - overlap[0][1] * overlap[1][0]);
}

Vec canonical_left() {
  Vec frame(2 * D, 0.0);
  frame[2 * 0] = 1.0;      // |000>
  frame[2 * 1 + 1] = 1.0;  // |001>, least-significant site
  return frame;
}

Vec canonical_right() {
  Vec frame(2 * D, 0.0);
  frame[2 * (3 * 3)] = 1.0;          // |100> in this indexing
  frame[2 * (3 * 3 + 1) + 1] = 1.0;  // |101>
  // The choice |100>,|101> is locally equivalent to |110>,|111>
  // for the purpose of this test only if the middle dyad is traceless.
  // Use |110>,|111> explicitly.
  frame.assign(2 * D, 0.0);
  frame[2 * (3 * 3 + 3)] = 1.0;
  frame[2 * (3 * 3 + 3 + 1) + 1] = 1.0;
  return frame;
}

Vec graph_frame(
    const std::array<int, 3>& first,
    const std::array<int, 3>& second) {
  Vec frame(2 * D);
  const C omega(-0.5, std::sqrt(3.0) / 2.0);
  for (int index = 0; index < D; ++index) {
    int value = index;
    std::array<int, 3> x{};
    for (int site = 0; site < 3; ++site) {
      x[site] = value % 3;
      value /= 3;
    }
    const int graph_phase = 2 * x[1] * x[2];
    const int phase0 =
        (graph_phase + first[0] * x[0] + first[1] * x[1]
         + first[2] * x[2]) % 3;
    const int phase1 =
        (graph_phase + second[0] * x[0] + second[1] * x[1]
         + second[2] * x[2]) % 3;
    frame[2 * index] = std::pow(omega, phase0) / std::sqrt(27.0);
    frame[2 * index + 1] =
        std::pow(omega, phase1) / std::sqrt(27.0);
  }
  return frame;
}

int main(int argc, char** argv) {
  const int samples = argc > 1 ? std::stoi(argv[1]) : 1000;
  const std::uint64_t seed =
      argc > 2 ? std::stoull(argv[2]) : UINT64_C(20260729);
  const int optimize_steps = argc > 3 ? std::stoi(argv[3]) : 0;
  const int objective_mode = argc > 4 ? std::stoi(argv[4]) : 0;
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;

  const Evaluation canonical =
      evaluate(canonical_left(), canonical_right());
  std::cout << std::setprecision(15)
            << "canonical concurrence " << canonical.concurrence
            << " ppt_min " << canonical.minimum_ppt << " takagi";
  for (double x : canonical.takagi) std::cout << " " << x;
  std::cout << "\n";
  double canonical_group_sum = 0.0;
  std::array<M4, 4> canonical_groups{};
  int canonical_group_index = 0;
  for (int mask : {3, 5, 6}) {
    const M4 group = parity_feature(
        canonical_left(), canonical_right(), mask, 4.0 / 9.0);
    canonical_groups[canonical_group_index++] = group;
    const double group_c = concurrence(group);
    canonical_group_sum += group_c;
    std::cout << "canonical group " << mask
              << " concurrence " << group_c << "\n";
  }
  {
    const M4 group = parity_feature(
        canonical_left(), canonical_right(), 7, 8.0 / 9.0);
    canonical_groups[3] = group;
    const double group_c = concurrence(group);
    canonical_group_sum += group_c;
    std::cout << "canonical residual triple concurrence "
              << group_c << " group sum " << canonical_group_sum << "\n";
  }
  for (int subset = 1; subset < 15; ++subset) {
    M4 group{};
    M4 complement{};
    for (int g = 0; g < 4; ++g)
      for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 4; ++j)
          ((subset >> g) & 1 ? group : complement)[i][j]
              += canonical_groups[g][i][j];
    std::cout << "canonical partition " << subset << "/"
              << (15 ^ subset) << " concurrence sum "
              << concurrence(group) + concurrence(complement) << "\n";
  }
  {
    const Vec graph_left = graph_frame({2, 2, 0}, {0, 1, 1});
    const Vec graph_right = graph_frame({0, 2, 0}, {0, 2, 2});
    const Evaluation graph = evaluate(graph_left, graph_right);
    std::cout << "graph concurrence " << graph.concurrence << " takagi";
    for (double x : graph.takagi) std::cout << " " << x;
    std::cout << "\n";
    for (int subset = 1; subset < 8; ++subset)
      std::cout << "graph partition " << subset << " sum "
                << partition_concurrence_sum(
                       graph_left, graph_right, subset)
                << "\n";
  }

  double maximum = -1.0;
  double maximum_qubit = -1.0;
  double maximum_one_site = -1.0;
  Evaluation best_qubit{};
  double minimum_ppt = std::numeric_limits<double>::infinity();
  for (int sample = 0; sample < samples; ++sample) {
    Vec left(2 * D), right(2 * D);
    for (C& z : left) z = C(normal(rng), normal(rng));
    for (C& z : right) z = C(normal(rng), normal(rng));
    orthonormalize(left);
    orthonormalize(right);
    const Evaluation value = evaluate(left, right);
    maximum = std::max(maximum, value.concurrence);
    minimum_ppt = std::min(minimum_ppt, value.minimum_ppt);
    if (sample == 0) {
      double group_sum = 0.0;
      for (int mask : {3, 5, 6})
        group_sum += concurrence(
            parity_feature(left, right, mask, 4.0 / 9.0));
      group_sum += concurrence(
          parity_feature(left, right, 7, 8.0 / 9.0));
      std::cout << "first random group concurrence sum "
                << group_sum << "\n";
    }

    Vec qubit_left(2 * D, 0.0), qubit_right(2 * D, 0.0);
    Vec one_left(2 * D, 0.0), one_right(2 * D, 0.0);
    for (int index = 0; index < D; ++index) {
      int word = index;
      bool qubit_allowed = true;
      bool first_site_allowed = true;
      for (int site = 0; site < 3; ++site) {
        const int digit = word % 3;
        word /= 3;
        qubit_allowed &= digit < 2;
        if (site == 0) first_site_allowed &= digit < 2;
      }
      for (int a = 0; a < 2; ++a) {
        if (qubit_allowed) {
          qubit_left[2 * index + a] = C(normal(rng), normal(rng));
          qubit_right[2 * index + a] = C(normal(rng), normal(rng));
        }
        if (first_site_allowed) {
          one_left[2 * index + a] = C(normal(rng), normal(rng));
          one_right[2 * index + a] = C(normal(rng), normal(rng));
        }
      }
    }
    orthonormalize(qubit_left);
    orthonormalize(qubit_right);
    orthonormalize(one_left);
    orthonormalize(one_right);
    const Evaluation qubit_value = evaluate(qubit_left, qubit_right);
    if (qubit_value.concurrence > maximum_qubit) {
      maximum_qubit = qubit_value.concurrence;
      best_qubit = qubit_value;
    }
    maximum_one_site = std::max(
        maximum_one_site, evaluate(one_left, one_right).concurrence);
  }
  std::cout << "random maximum concurrence " << maximum
            << " qubit-support maximum " << maximum_qubit
            << " one-site-support maximum " << maximum_one_site
            << " minimum ppt eigenvalue " << minimum_ppt << "\n";
  if (samples > 0) {
    std::cout << "best qubit takagi";
    for (double x : best_qubit.takagi) std::cout << " " << x;
    std::cout << " feature\n";
    for (const auto& row : best_qubit.feature) {
      for (C x : row)
        std::cout << "(" << std::real(x) << "," << std::imag(x) << ") ";
      std::cout << "\n";
    }
  }

  // Finite-difference ascent near the sharp code.  This is intentionally
  // slow and is only an adversarial check of the sufficient inequality.
  for (int start = 0; start < (optimize_steps ? 12 : 0); ++start) {
    Vec left(2 * D), right(2 * D);
    if (start < 4) {
      left = canonical_left();
      right = canonical_right();
      const double noise = 1e-2 * (start + 1);
      for (C& z : left) z += noise * C(normal(rng), normal(rng));
      for (C& z : right) z += noise * C(normal(rng), normal(rng));
    } else {
      for (C& z : left) z = C(normal(rng), normal(rng));
      for (C& z : right) z = C(normal(rng), normal(rng));
    }
    orthonormalize(left);
    orthonormalize(right);
    auto objective = [&](const Vec& a, const Vec& b) {
      if (objective_mode == 1) return evaluate(a, b).concurrence;
      if (objective_mode == 2)
        return common_plane_floor_objective(a, b);
      if (objective_mode == 3)
        return shifted_pair_violation(a, b);
      return q2_concurrence_objective(a, b)
             + (2.0 / 9.0)
                   * conjugate_plane_determinant_overlap(a, b);
    };
    double value = objective(left, right);
    double step = 0.1;
    for (int iteration = 0; iteration < optimize_steps; ++iteration) {
      Vec gradient_left(2 * D), gradient_right(2 * D);
      const double h = 2e-5;
      for (int which = 0; which < 2; ++which) {
        Vec* frame = which ? &right : &left;
        Vec* gradient = which ? &gradient_right : &gradient_left;
        for (int index = 0; index < 2 * D; ++index)
          for (int component = 0; component < 2; ++component) {
            Vec plus = *frame, minus = *frame;
            const C direction = component ? C(0.0, h) : C(h, 0.0);
            plus[index] += direction;
            minus[index] -= direction;
            orthonormalize(plus);
            orthonormalize(minus);
            const double up =
                which ? objective(left, plus) : objective(plus, right);
            const double down =
                which ? objective(left, minus) : objective(minus, right);
            const double derivative = (up - down) / (2.0 * h);
            (*gradient)[index] +=
                component ? C(0.0, derivative) : C(derivative, 0.0);
          }
      }
      const double gradient_norm =
          norm_squared(gradient_left) + norm_squared(gradient_right);
      bool accepted = false;
      double trial_step = step;
      for (int backtrack = 0; backtrack < 20; ++backtrack) {
        Vec trial_left = left, trial_right = right;
        for (int i = 0; i < 2 * D; ++i) {
          trial_left[i] += trial_step * gradient_left[i];
          trial_right[i] += trial_step * gradient_right[i];
        }
        orthonormalize(trial_left);
        orthonormalize(trial_right);
        const double trial = objective(trial_left, trial_right);
        if (trial >= value + 1e-5 * trial_step * gradient_norm) {
          left.swap(trial_left);
          right.swap(trial_right);
          value = trial;
          step = std::min(0.1, 1.25 * trial_step);
          accepted = true;
          break;
        }
        trial_step *= 0.5;
      }
      if (!accepted || gradient_norm < 1e-18) break;
    }
    const Evaluation optimized = evaluate(left, right);
    std::cout << "optimized " << start << " concurrence "
              << optimized.concurrence << " ppt_min "
              << optimized.minimum_ppt << " partition1 "
              << partition_concurrence_sum(left, right, 1)
              << " q2_concurrence "
              << q2_concurrence_objective(left, right)
              << " plane_det "
              << conjugate_plane_determinant_overlap(left, right)
              << " floor_objective "
              << common_plane_floor_objective(left, right)
              << " shifted_violation "
              << shifted_pair_violation(left, right)
              << " takagi";
    for (double x : optimized.takagi) std::cout << " " << x;
    std::cout << "\n";
  }
}
