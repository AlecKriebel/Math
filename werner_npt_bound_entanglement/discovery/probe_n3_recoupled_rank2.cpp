// Discovery-only test of recoupled positivity when the two grouped
// coefficient matrices each have rank at most two.
//
// It uses the exact realignment identity
//
//   <a b, B a b> = 1/2 <W,(Y tensor Y)W>,
//
// W_{(p,q),(r,s)}
//   = conj(A_{p,r}) B_{q,s} - conj(A_{r,p}) B_{s,q},
//
// where a=vec(A), b=vec(B), and Y=2I-3 Pi_2 on M_27.
// Floating-point output is discovery evidence only.

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
using Vec = std::vector<C>;

constexpr int local = 3;
constexpr int copies = 3;
constexpr int physical = 27;
constexpr int operators = physical * physical;

Vec scalar_part(const Vec& matrix, int site) {
  Vec out(operators, 0.0);
  int place = 1;
  for (int i = 0; i < site; ++i) place *= local;
  for (int row = 0; row < physical; ++row) {
    const int digit = (row / place) % local;
    const int base_row = row - digit * place;
    for (int column = 0; column < physical; ++column) {
      if ((column / place) % local != digit) continue;
      const int base_column = column - digit * place;
      C trace = 0.0;
      for (int value = 0; value < local; ++value)
        trace += matrix[
            (base_row + value * place) * physical
            + base_column + value * place];
      out[row * physical + column] = trace / 3.0;
    }
  }
  return out;
}

Vec exact_sector(Vec matrix, int traceless_mask) {
  for (int site = 0; site < copies; ++site) {
    Vec scalar = scalar_part(matrix, site);
    if ((traceless_mask >> site) & 1)
      for (int i = 0; i < operators; ++i) matrix[i] -= scalar[i];
    else
      matrix.swap(scalar);
  }
  return matrix;
}

Vec apply_y(const Vec& matrix) {
  Vec out = matrix;
  for (C& value : out) value *= 2.0;
  for (int mask : {3, 5, 6}) {
    const Vec part = exact_sector(matrix, mask);
    for (int i = 0; i < operators; ++i) out[i] -= 3.0 * part[i];
  }
  return out;
}

double norm_squared(const Vec& matrix) {
  double out = 0.0;
  for (C value : matrix) out += std::norm(value);
  return out;
}

void normalize(Vec& matrix) {
  const double scale = std::sqrt(norm_squared(matrix));
  for (C& value : matrix) value /= scale;
}

double objective(const Vec& a, const Vec& b) {
  Vec wedge(operators * operators);
  for (int p = 0; p < physical; ++p)
    for (int q = 0; q < physical; ++q) {
      const int first = p * physical + q;
      for (int r = 0; r < physical; ++r)
        for (int s = 0; s < physical; ++s) {
          const int second = r * physical + s;
          wedge[first * operators + second] =
              std::conj(a[p * physical + r])
                  * b[q * physical + s]
              - std::conj(a[r * physical + p])
                  * b[s * physical + q];
        }
    }

  Vec first_action(operators * operators);
  Vec fiber(operators);
  for (int second = 0; second < operators; ++second) {
    for (int first = 0; first < operators; ++first)
      fiber[first] = wedge[first * operators + second];
    const Vec image = apply_y(fiber);
    for (int first = 0; first < operators; ++first)
      first_action[first * operators + second] = image[first];
  }
  Vec full_action(operators * operators);
  for (int first = 0; first < operators; ++first) {
    for (int second = 0; second < operators; ++second)
      fiber[second] = first_action[first * operators + second];
    const Vec image = apply_y(fiber);
    for (int second = 0; second < operators; ++second)
      full_action[first * operators + second] = image[second];
  }

  C value = 0.0;
  for (int i = 0; i < operators * operators; ++i)
    value += std::conj(wedge[i]) * full_action[i];
  return 0.5 * std::real(value);
}

Vec rank_two(
    std::mt19937_64& rng, std::normal_distribution<double>& normal) {
  Vec left(2 * physical), right(2 * physical);
  for (C& value : left) value = C(normal(rng), normal(rng));
  for (C& value : right) value = C(normal(rng), normal(rng));
  Vec out(operators, 0.0);
  for (int row = 0; row < physical; ++row)
    for (int column = 0; column < physical; ++column)
      for (int k = 0; k < 2; ++k)
        out[row * physical + column] +=
            left[2 * row + k] * std::conj(right[2 * column + k]);
  normalize(out);
  return out;
}

Vec matrix_unit(int row, int column) {
  Vec out(operators);
  out[row * physical + column] = 1.0;
  return out;
}

Vec site_product_counterexample(bool left_side) {
  Vec out(operators, 0.0);
  // Least-significant digit is site zero.  The local matrices are
  // E_01, then E_00/E_11, then I/sqrt(3).
  for (int value = 0; value < 3; ++value) {
    const int row =
        0 + 3 * (left_side ? 0 : 1) + 9 * value;
    const int column = 1 + 3 * (left_side ? 0 : 1) + 9 * value;
    out[row * physical + column] = 1.0 / std::sqrt(3.0);
  }
  return out;
}

int main(int argc, char** argv) {
  const int samples = argc > 1 ? std::stoi(argv[1]) : 100;
  const std::uint64_t seed =
      argc > 2 ? std::stoull(argv[2]) : UINT64_C(20260729);
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;

  const double exact_probe = objective(
      site_product_counterexample(true),
      site_product_counterexample(false));
  std::cout << std::setprecision(15)
            << "rank3 site-product probe " << exact_probe << "\n";

  double minimum = 1e100;
  for (int sample = 0; sample < samples; ++sample) {
    const Vec a = rank_two(rng, normal);
    const Vec b = rank_two(rng, normal);
    minimum = std::min(minimum, objective(a, b));
  }
  std::cout << "random rank2 minimum " << minimum << "\n";
}
