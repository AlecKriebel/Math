// Discovery-only search for the shifted degree-two exterior inequality
//
//   ||Pi_2 C||_2^2 <= 4/9 (||C||_2^2 + s_1(C)s_2(C))
//
// on qutrit three-copy rank-two matrices.  The parameterization is
// C=U diag(s_0,s_1)V^*, with U,V complex Stiefel frames and
// s_0^2+s_1^2=1.  Floating-point output is not a certificate.

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

constexpr int d = 3;
constexpr int n = 3;
constexpr int D = 27;

double norm_squared(const Vec& vector) {
  double answer = 0.0;
  for (Complex entry : vector) answer += std::norm(entry);
  return answer;
}

void orthonormalize(Vec& frame) {
  for (int column = 0; column < 2; ++column) {
    for (int earlier = 0; earlier < column; ++earlier) {
      Complex overlap = 0.0;
      for (int row = 0; row < D; ++row)
        overlap += std::conj(frame[2 * row + earlier])
                   * frame[2 * row + column];
      for (int row = 0; row < D; ++row)
        frame[2 * row + column] -=
            overlap * frame[2 * row + earlier];
    }
    double square = 0.0;
    for (int row = 0; row < D; ++row)
      square += std::norm(frame[2 * row + column]);
    const double inverse = 1.0 / std::sqrt(std::max(square, 1e-300));
    for (int row = 0; row < D; ++row)
      frame[2 * row + column] *= inverse;
  }
}

void tangent_project(const Vec& frame, Vec& gradient) {
  Complex gram[2][2] = {};
  for (int first = 0; first < 2; ++first)
    for (int second = 0; second < 2; ++second)
      for (int row = 0; row < D; ++row)
        gram[first][second] +=
            std::conj(frame[2 * row + first])
            * gradient[2 * row + second];
  gram[0][0] = std::real(gram[0][0]);
  gram[1][1] = std::real(gram[1][1]);
  const Complex off =
      0.5 * (gram[0][1] + std::conj(gram[1][0]));
  gram[0][1] = off;
  gram[1][0] = std::conj(off);
  for (int row = 0; row < D; ++row) {
    const Complex x0 = frame[2 * row];
    const Complex x1 = frame[2 * row + 1];
    gradient[2 * row] -=
        x0 * gram[0][0] + x1 * gram[1][0];
    gradient[2 * row + 1] -=
        x0 * gram[0][1] + x1 * gram[1][1];
  }
}

Vec scalar_part(const Vec& matrix, int site) {
  Vec answer(D * D, 0.0);
  int place = 1;
  for (int index = 0; index < site; ++index) place *= d;
  for (int row = 0; row < D; ++row) {
    const int row_digit = (row / place) % d;
    const int row_base = row - row_digit * place;
    for (int column = 0; column < D; ++column) {
      const int column_digit = (column / place) % d;
      if (column_digit != row_digit) continue;
      const int column_base = column - column_digit * place;
      Complex trace = 0.0;
      for (int value = 0; value < d; ++value)
        trace += matrix[
            (row_base + value * place) * D
            + column_base + value * place];
      answer[row * D + column] = trace / 3.0;
    }
  }
  return answer;
}

Vec degree_two(Vec matrix) {
  Vec answer(D * D, 0.0);
  for (int scalar_site = 0; scalar_site < n; ++scalar_site) {
    Vec component = matrix;
    for (int site = 0; site < n; ++site) {
      Vec scalar = scalar_part(component, site);
      if (site == scalar_site)
        component.swap(scalar);
      else
        for (int index = 0; index < D * D; ++index)
          component[index] -= scalar[index];
    }
    for (int index = 0; index < D * D; ++index)
      answer[index] += component[index];
  }
  return answer;
}

Vec matrix_from(
    const Vec& left, const Vec& right,
    const std::vector<double>& singular) {
  Vec answer(D * D, 0.0);
  for (int row = 0; row < D; ++row)
    for (int column = 0; column < D; ++column)
      for (int index = 0; index < 2; ++index)
        answer[row * D + column] +=
            singular[index] * left[2 * row + index]
            * std::conj(right[2 * column + index]);
  return answer;
}

struct Value {
  double defect;
  double mass;
  Vec image;
};

Value evaluate(
    const Vec& left, const Vec& right,
    const std::vector<double>& singular) {
  const Vec matrix = matrix_from(left, right, singular);
  Vec projected = degree_two(matrix);
  const double mass = norm_squared(projected);
  Vec image(D * D);
  for (int index = 0; index < D * D; ++index)
    image[index] = matrix[index] - 2.25 * projected[index];
  return {
      1.0 - 2.25 * mass + singular[0] * singular[1],
      mass,
      std::move(image)};
}

int main(int argc, char** argv) {
  const int starts = argc >= 2 ? std::stoi(argv[1]) : 20;
  const int iterations = argc >= 3 ? std::stoi(argv[2]) : 500;
  const std::uint64_t seed =
      argc >= 4 ? std::stoull(argv[3]) : UINT64_C(20260729);
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  double global = std::numeric_limits<double>::infinity();

  for (int start = 0; start < starts; ++start) {
    Vec left(2 * D), right(2 * D);
    for (Complex& entry : left)
      entry = Complex(normal(rng), normal(rng));
    for (Complex& entry : right)
      entry = Complex(normal(rng), normal(rng));
    orthonormalize(left);
    orthonormalize(right);
    std::vector<double> singular = {
        std::abs(normal(rng)), std::abs(normal(rng))};
    const double scale = std::hypot(singular[0], singular[1]);
    singular[0] /= scale;
    singular[1] /= scale;
    double step = 0.08;
    double best = std::numeric_limits<double>::infinity();
    double best_mass = 0.0;

    for (int iteration = 0; iteration < iterations; ++iteration) {
      const Value current = evaluate(left, right, singular);
      if (current.defect < best) {
        best = current.defect;
        best_mass = current.mass;
      }
      Vec matrix_gradient(D * D);
      for (int index = 0; index < D * D; ++index)
        matrix_gradient[index] = 2.0 * current.image[index];
      Vec left_gradient(2 * D, 0.0), right_gradient(2 * D, 0.0);
      std::vector<double> singular_gradient = {
          singular[1], singular[0]};
      for (int row = 0; row < D; ++row)
        for (int column = 0; column < D; ++column) {
          const Complex gradient =
              matrix_gradient[row * D + column];
          for (int index = 0; index < 2; ++index) {
            left_gradient[2 * row + index] +=
                singular[index] * gradient
                * right[2 * column + index];
            right_gradient[2 * column + index] +=
                singular[index] * std::conj(gradient)
                * left[2 * row + index];
            singular_gradient[index] += std::real(
                std::conj(left[2 * row + index])
                * gradient * right[2 * column + index]);
          }
        }
      tangent_project(left, left_gradient);
      tangent_project(right, right_gradient);
      const double radial =
          singular[0] * singular_gradient[0]
          + singular[1] * singular_gradient[1];
      for (int index = 0; index < 2; ++index)
        singular_gradient[index] -= radial * singular[index];
      const double gradient_square =
          norm_squared(left_gradient) + norm_squared(right_gradient)
          + singular_gradient[0] * singular_gradient[0]
          + singular_gradient[1] * singular_gradient[1];
      if (gradient_square < 1e-24) break;

      bool accepted = false;
      double trial_step = step;
      for (int trial = 0; trial < 25; ++trial) {
        Vec next_left = left, next_right = right;
        std::vector<double> next_singular = singular;
        for (int index = 0; index < 2 * D; ++index) {
          next_left[index] -= trial_step * left_gradient[index];
          next_right[index] -= trial_step * right_gradient[index];
        }
        for (int index = 0; index < 2; ++index)
          next_singular[index] -=
              trial_step * singular_gradient[index];
        orthonormalize(next_left);
        orthonormalize(next_right);
        const double next_scale =
            std::hypot(next_singular[0], next_singular[1]);
        for (double& value : next_singular)
          value = std::abs(value / next_scale);
        const Value next =
            evaluate(next_left, next_right, next_singular);
        if (next.defect <=
            current.defect - 1e-6 * trial_step * gradient_square) {
          left.swap(next_left);
          right.swap(next_right);
          singular.swap(next_singular);
          step = std::min(0.2, 1.2 * trial_step);
          accepted = true;
          break;
        }
        trial_step *= 0.5;
      }
      if (!accepted) break;
    }
    global = std::min(global, best);
    std::cout << std::setprecision(17)
              << "start " << start
              << " defect " << best
              << " degree_two_mass " << best_mass
              << " singular_product "
              << singular[0] * singular[1]
              << " global " << global << "\n";
  }
}
