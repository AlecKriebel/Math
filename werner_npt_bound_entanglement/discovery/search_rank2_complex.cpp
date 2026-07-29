// Discovery-only unrestricted complex rank-two search for Q_n(C).
//
// General mode parameterizes a Frobenius-normalized rank-two matrix by
//
//     C = U diag(s_0,s_1) V^*
//
// with complex Stiefel frames U,V and real singular values on the unit
// circle.  Normal mode sets V=U and allows two arbitrary complex
// eigenvalues of unit Euclidean norm.  Floating-point output is never a
// certificate.

#include <algorithm>
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

struct Search {
  int d, n, D;
  bool use_even_reduction = false;
  std::mt19937_64 rng;
  std::normal_distribution<double> normal{0.0, 1.0};

  Search(int d_, int n_, std::uint64_t seed)
      : d(d_), n(n_), D(1), rng(seed) {
    for (int i = 0; i < n; ++i) D *= d;
  }

  void orthonormalize(Vec& frame) const {
    for (int column = 0; column < 2; ++column) {
      for (int earlier = 0; earlier < column; ++earlier) {
        Complex overlap = 0.0;
        for (int row = 0; row < D; ++row)
          overlap +=
              std::conj(frame[2 * row + earlier]) *
              frame[2 * row + column];
        for (int row = 0; row < D; ++row)
          frame[2 * row + column] -=
              overlap * frame[2 * row + earlier];
      }
      double norm_squared = 0.0;
      for (int row = 0; row < D; ++row)
        norm_squared += std::norm(frame[2 * row + column]);
      const double inverse =
          1.0 / std::sqrt(std::max(norm_squared, 1e-300));
      for (int row = 0; row < D; ++row)
        frame[2 * row + column] *= inverse;
    }
  }

  void tangent_project(const Vec& frame, Vec& gradient) const {
    Complex gram[2][2] = {};
    for (int a = 0; a < 2; ++a)
      for (int b = 0; b < 2; ++b)
        for (int row = 0; row < D; ++row)
          gram[a][b] +=
              std::conj(frame[2 * row + a]) *
              gradient[2 * row + b];
    const Complex off =
        0.5 * (gram[0][1] + std::conj(gram[1][0]));
    gram[0][0] = std::real(gram[0][0]);
    gram[1][1] = std::real(gram[1][1]);
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

  Vec apply_l(Vec matrix) const {
    Vec next(D * D);
    int power = 1;
    for (int site = 0; site < n; ++site) {
      next = matrix;
      for (int row = 0; row < D; ++row) {
        const int digit = (row / power) % d;
        for (int column = 0; column < D; ++column) {
          if ((column / power) % d != digit) continue;
          Complex trace = 0.0;
          for (int value = 0; value < d; ++value) {
            const int changed_row =
                row + (value - digit) * power;
            const int changed_column =
                column + (value - digit) * power;
            trace += matrix[changed_row * D + changed_column];
          }
          next[row * D + column] -= 0.5 * trace;
        }
      }
      matrix.swap(next);
      power *= d;
    }
    return matrix;
  }

  Vec apply_d_site(const Vec& matrix, int site) const {
    Vec next(D * D, 0.0);
    int power = 1;
    for (int index = 0; index < site; ++index) power *= d;
    for (int row = 0; row < D; ++row) {
      const int digit = (row / power) % d;
      for (int column = 0; column < D; ++column) {
        if ((column / power) % d != digit) continue;
        Complex trace = 0.0;
        for (int value = 0; value < d; ++value) {
          const int changed_row =
              row + (value - digit) * power;
          const int changed_column =
              column + (value - digit) * power;
          trace += matrix[changed_row * D + changed_column];
        }
        next[row * D + column] = trace;
      }
    }
    return next;
  }

  Vec apply_even_reduction(const Vec& matrix) const {
    Vec result(D * D);
    for (int index = 0; index < D * D; ++index)
      result[index] = 3.0 * matrix[index];
    std::vector<Vec> one_site;
    one_site.reserve(n);
    for (int site = 0; site < n; ++site) {
      one_site.push_back(apply_d_site(matrix, site));
      for (int index = 0; index < D * D; ++index)
        result[index] -= 2.0 * one_site.back()[index];
    }
    for (int first = 0; first < n; ++first)
      for (int second = first + 1; second < n; ++second) {
        const Vec pair =
            apply_d_site(one_site[first], second);
        for (int index = 0; index < D * D; ++index)
          result[index] += pair[index];
      }
    return result;
  }

  Vec general_matrix(
      const Vec& left, const Vec& right,
      const std::vector<double>& singular) const {
    Vec matrix(D * D, 0.0);
    for (int row = 0; row < D; ++row)
      for (int column = 0; column < D; ++column)
        for (int a = 0; a < 2; ++a)
          matrix[row * D + column] +=
              singular[a] * left[2 * row + a] *
              std::conj(right[2 * column + a]);
    return matrix;
  }

  Vec normal_matrix(
      const Vec& frame, const std::vector<Complex>& eigenvalue) const {
    Vec matrix(D * D, 0.0);
    for (int row = 0; row < D; ++row)
      for (int column = 0; column < D; ++column)
        for (int a = 0; a < 2; ++a)
          matrix[row * D + column] +=
              eigenvalue[a] * frame[2 * row + a] *
              std::conj(frame[2 * column + a]);
    return matrix;
  }

  double objective(const Vec& matrix, Vec* image = nullptr) const {
    Vec applied = use_even_reduction
        ? apply_even_reduction(matrix)
        : apply_l(matrix);
    double value = 0.0;
    for (int index = 0; index < D * D; ++index)
      value += std::real(
          std::conj(matrix[index]) * applied[index]);
    if (image) image->swap(applied);
    return value;
  }

  static double norm_squared(const Vec& vector) {
    double value = 0.0;
    for (const Complex& entry : vector) value += std::norm(entry);
    return value;
  }

  static double real_inner(const Vec& left, const Vec& right) {
    double value = 0.0;
    for (std::size_t index = 0; index < left.size(); ++index)
      value += std::real(std::conj(left[index]) * right[index]);
    return value;
  }

  // Sum of log determinants of the combined one-site support matrices
  //
  //   R_i = sum_a Tr_{\bar i}(
  //       |left_a><left_a| + |right_a><right_a|).
  //
  // A common local two-dimensional support has det(R_i)=0.  Subtracting
  // mu times this barrier from Q therefore keeps the discovery search in
  // the genuinely qutrit interior.  The ridge is only a numerical
  // regularizer; this routine is not part of a certificate.
  double support_logdet(
      const Vec& left, const Vec& right,
      Vec* left_gradient = nullptr,
      Vec* right_gradient = nullptr,
      double ridge = 1e-10,
      double* smallest_pivot = nullptr) const {
    if (left_gradient) left_gradient->assign(2 * D, 0.0);
    if (right_gradient) right_gradient->assign(2 * D, 0.0);
    double total = 0.0;
    double minimum = std::numeric_limits<double>::infinity();
    int power = 1;
    for (int site = 0; site < n; ++site) {
      Vec reduced(d * d, 0.0);
      for (int row = 0; row < D; ++row) {
        const int x = (row / power) % d;
        const int base = row - x * power;
        for (int y = 0; y < d; ++y) {
          const int other = base + y * power;
          for (int a = 0; a < 2; ++a) {
            reduced[x * d + y] +=
                left[2 * row + a] *
                    std::conj(left[2 * other + a]) +
                right[2 * row + a] *
                    std::conj(right[2 * other + a]);
          }
        }
      }
      for (int x = 0; x < d; ++x)
        reduced[x * d + x] += ridge;

      // Cholesky factorization reduced = lower * lower^*.  Besides being
      // stable for the positive support matrices, its diagonal supplies
      // log(det) and a useful lower-pivot diagnostic.
      Vec lower(d * d, 0.0);
      for (int x = 0; x < d; ++x) {
        for (int y = 0; y <= x; ++y) {
          Complex entry = reduced[x * d + y];
          for (int k = 0; k < y; ++k)
            entry -=
                lower[x * d + k] *
                std::conj(lower[y * d + k]);
          if (x == y) {
            const double diagonal =
                std::max(std::real(entry), 1e-300);
            lower[x * d + y] = std::sqrt(diagonal);
            total += std::log(diagonal);
            minimum = std::min(minimum, diagonal);
          } else {
            lower[x * d + y] =
                entry / lower[y * d + y];
          }
        }
      }

      // Invert through the Cholesky factors.
      Vec inverse(d * d, 0.0);
      for (int column = 0; column < d; ++column) {
        std::vector<Complex> intermediate(d, 0.0);
        for (int x = 0; x < d; ++x) {
          Complex entry = (x == column ? 1.0 : 0.0);
          for (int k = 0; k < x; ++k)
            entry -= lower[x * d + k] * intermediate[k];
          intermediate[x] = entry / lower[x * d + x];
        }
        for (int x = d - 1; x >= 0; --x) {
          Complex entry = intermediate[x];
          for (int k = x + 1; k < d; ++k)
            entry -=
                std::conj(lower[k * d + x]) *
                inverse[k * d + column];
          inverse[x * d + column] =
              entry / std::conj(lower[x * d + x]);
        }
      }

      // d log(det R)[delta frame]
      //   = 2 Re sum_a <R^{-1} frame_a, delta frame_a>.
      if (left_gradient || right_gradient) {
        for (int row = 0; row < D; ++row) {
          const int x = (row / power) % d;
          const int base = row - x * power;
          for (int a = 0; a < 2; ++a) {
            Complex left_entry = 0.0, right_entry = 0.0;
            for (int y = 0; y < d; ++y) {
              const int other = base + y * power;
              left_entry +=
                  inverse[x * d + y] * left[2 * other + a];
              right_entry +=
                  inverse[x * d + y] * right[2 * other + a];
            }
            if (left_gradient)
              (*left_gradient)[2 * row + a] += 2.0 * left_entry;
            if (right_gradient)
              (*right_gradient)[2 * row + a] += 2.0 * right_entry;
          }
        }
      }
      power *= d;
    }
    if (smallest_pivot) *smallest_pivot = minimum;
    return total;
  }

  double general_start(
      int iterations, Vec& best_matrix,
      double initial_step = 0.08,
      const std::vector<double>* fixed_singular = nullptr,
      Vec* best_left = nullptr, Vec* best_right = nullptr,
      std::vector<double>* best_singular = nullptr) {
    Vec left(2 * D), right(2 * D);
    for (Complex& entry : left)
      entry = Complex(normal(rng), normal(rng));
    for (Complex& entry : right)
      entry = Complex(normal(rng), normal(rng));
    orthonormalize(left);
    orthonormalize(right);
    std::vector<double> singular = {
        std::abs(normal(rng)), std::abs(normal(rng))};
    double singular_norm = std::hypot(singular[0], singular[1]);
    singular[0] /= singular_norm;
    singular[1] /= singular_norm;
    if (fixed_singular) singular = *fixed_singular;

    double best = std::numeric_limits<double>::infinity();
    double step = initial_step;
    for (int iteration = 0; iteration < iterations; ++iteration) {
      const Vec matrix = general_matrix(left, right, singular);
      Vec applied;
      const double value = objective(matrix, &applied);
      if (value < best) {
        best = value;
        best_matrix = matrix;
        if (best_left) *best_left = left;
        if (best_right) *best_right = right;
        if (best_singular) *best_singular = singular;
      }
      Vec matrix_gradient(D * D);
      for (int index = 0; index < D * D; ++index)
        matrix_gradient[index] =
            2.0 * (applied[index] - value * matrix[index]);

      Vec left_gradient(2 * D, 0.0);
      Vec right_gradient(2 * D, 0.0);
      std::vector<double> singular_gradient(2, 0.0);
      for (int row = 0; row < D; ++row) {
        for (int column = 0; column < D; ++column) {
          const Complex gradient =
              matrix_gradient[row * D + column];
          for (int a = 0; a < 2; ++a) {
            left_gradient[2 * row + a] +=
                singular[a] * gradient *
                right[2 * column + a];
            right_gradient[2 * column + a] +=
                singular[a] * std::conj(gradient) *
                left[2 * row + a];
            singular_gradient[a] += std::real(
                std::conj(left[2 * row + a]) * gradient *
                right[2 * column + a]);
          }
        }
      }
      tangent_project(left, left_gradient);
      tangent_project(right, right_gradient);
      const double radial =
          singular[0] * singular_gradient[0] +
          singular[1] * singular_gradient[1];
      for (int a = 0; a < 2; ++a)
        singular_gradient[a] -= radial * singular[a];
      const double gradient_squared =
          norm_squared(left_gradient) +
          norm_squared(right_gradient) +
          (fixed_singular
               ? 0.0
               : singular_gradient[0] * singular_gradient[0] +
                     singular_gradient[1] * singular_gradient[1]);
      if (gradient_squared < 1e-24) break;

      bool accepted = false;
      double trial = step;
      for (int backtrack = 0; backtrack < 25; ++backtrack) {
        Vec trial_left = left, trial_right = right;
        std::vector<double> trial_singular = singular;
        for (int index = 0; index < 2 * D; ++index) {
          trial_left[index] -= trial * left_gradient[index];
          trial_right[index] -= trial * right_gradient[index];
        }
        if (!fixed_singular)
          for (int a = 0; a < 2; ++a)
            trial_singular[a] -= trial * singular_gradient[a];
        orthonormalize(trial_left);
        orthonormalize(trial_right);
        if (!fixed_singular) {
          singular_norm = std::hypot(
              trial_singular[0], trial_singular[1]);
          for (double& entry : trial_singular)
            entry /= std::max(singular_norm, 1e-300);
        }
        const Vec trial_matrix = general_matrix(
            trial_left, trial_right, trial_singular);
        const double trial_value = objective(trial_matrix);
        if (trial_value <=
            value - 1e-5 * trial * gradient_squared) {
          left.swap(trial_left);
          right.swap(trial_right);
          singular.swap(trial_singular);
          step = std::min(initial_step, 1.2 * trial);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    return best;
  }

  double barrier_start(
      int iterations, Vec& final_matrix, double mu,
      double ridge, double initial_step = 0.04,
      double* final_augmented = nullptr,
      double* final_smallest_pivot = nullptr,
      Vec* final_left = nullptr, Vec* final_right = nullptr,
      std::vector<double>* final_singular = nullptr) {
    Vec left(2 * D), right(2 * D);
    for (Complex& entry : left)
      entry = Complex(normal(rng), normal(rng));
    for (Complex& entry : right)
      entry = Complex(normal(rng), normal(rng));
    orthonormalize(left);
    orthonormalize(right);
    std::vector<double> singular = {
        std::abs(normal(rng)), std::abs(normal(rng))};
    double singular_norm = std::hypot(singular[0], singular[1]);
    singular[0] /= singular_norm;
    singular[1] /= singular_norm;

    double step = initial_step;
    for (int iteration = 0; iteration < iterations; ++iteration) {
      const Vec matrix = general_matrix(left, right, singular);
      Vec applied;
      const double q = objective(matrix, &applied);
      Vec barrier_left, barrier_right;
      const double barrier = support_logdet(
          left, right, &barrier_left, &barrier_right, ridge);
      const double value = q - mu * barrier;

      Vec matrix_gradient(D * D);
      for (int index = 0; index < D * D; ++index)
        matrix_gradient[index] =
            2.0 * (applied[index] - q * matrix[index]);

      Vec left_gradient(2 * D, 0.0);
      Vec right_gradient(2 * D, 0.0);
      std::vector<double> singular_gradient(2, 0.0);
      for (int row = 0; row < D; ++row) {
        for (int column = 0; column < D; ++column) {
          const Complex gradient =
              matrix_gradient[row * D + column];
          for (int a = 0; a < 2; ++a) {
            left_gradient[2 * row + a] +=
                singular[a] * gradient *
                right[2 * column + a];
            right_gradient[2 * column + a] +=
                singular[a] * std::conj(gradient) *
                left[2 * row + a];
            singular_gradient[a] += std::real(
                std::conj(left[2 * row + a]) * gradient *
                right[2 * column + a]);
          }
        }
      }
      for (int index = 0; index < 2 * D; ++index) {
        left_gradient[index] -= mu * barrier_left[index];
        right_gradient[index] -= mu * barrier_right[index];
      }
      tangent_project(left, left_gradient);
      tangent_project(right, right_gradient);
      const double radial =
          singular[0] * singular_gradient[0] +
          singular[1] * singular_gradient[1];
      for (int a = 0; a < 2; ++a)
        singular_gradient[a] -= radial * singular[a];
      const double gradient_squared =
          norm_squared(left_gradient) +
          norm_squared(right_gradient) +
          singular_gradient[0] * singular_gradient[0] +
          singular_gradient[1] * singular_gradient[1];
      if (gradient_squared < 1e-22) break;

      bool accepted = false;
      double trial = step;
      for (int backtrack = 0; backtrack < 30; ++backtrack) {
        Vec trial_left = left, trial_right = right;
        std::vector<double> trial_singular = singular;
        for (int index = 0; index < 2 * D; ++index) {
          trial_left[index] -= trial * left_gradient[index];
          trial_right[index] -= trial * right_gradient[index];
        }
        for (int a = 0; a < 2; ++a)
          trial_singular[a] -= trial * singular_gradient[a];
        orthonormalize(trial_left);
        orthonormalize(trial_right);
        singular_norm = std::hypot(
            trial_singular[0], trial_singular[1]);
        for (double& entry : trial_singular)
          entry /= std::max(singular_norm, 1e-300);
        const Vec trial_matrix = general_matrix(
            trial_left, trial_right, trial_singular);
        const double trial_q = objective(trial_matrix);
        const double trial_barrier = support_logdet(
            trial_left, trial_right, nullptr, nullptr, ridge);
        const double trial_value =
            trial_q - mu * trial_barrier;
        if (trial_value <=
            value - 1e-5 * trial * gradient_squared) {
          left.swap(trial_left);
          right.swap(trial_right);
          singular.swap(trial_singular);
          step = std::min(initial_step, 1.2 * trial);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }

    final_matrix = general_matrix(left, right, singular);
    const double q = objective(final_matrix);
    double smallest = 0.0;
    const double barrier = support_logdet(
        left, right, nullptr, nullptr, ridge, &smallest);
    if (final_augmented) *final_augmented = q - mu * barrier;
    if (final_smallest_pivot) *final_smallest_pivot = smallest;
    if (final_left) *final_left = left;
    if (final_right) *final_right = right;
    if (final_singular) *final_singular = singular;
    return q;
  }

  double normal_start(
      int iterations, Vec& best_matrix,
      double initial_step = 0.08) {
    Vec frame(2 * D);
    for (Complex& entry : frame)
      entry = Complex(normal(rng), normal(rng));
    orthonormalize(frame);
    std::vector<Complex> eigenvalue = {
        Complex(normal(rng), normal(rng)),
        Complex(normal(rng), normal(rng))};
    double eigen_norm = std::sqrt(
        std::norm(eigenvalue[0]) + std::norm(eigenvalue[1]));
    for (Complex& entry : eigenvalue) entry /= eigen_norm;

    double best = std::numeric_limits<double>::infinity();
    double step = initial_step;
    for (int iteration = 0; iteration < iterations; ++iteration) {
      const Vec matrix = normal_matrix(frame, eigenvalue);
      Vec applied;
      const double value = objective(matrix, &applied);
      if (value < best) {
        best = value;
        best_matrix = matrix;
      }
      Vec matrix_gradient(D * D);
      for (int index = 0; index < D * D; ++index)
        matrix_gradient[index] =
            2.0 * (applied[index] - value * matrix[index]);

      Vec frame_gradient(2 * D, 0.0);
      std::vector<Complex> eigen_gradient(2, 0.0);
      for (int row = 0; row < D; ++row) {
        for (int column = 0; column < D; ++column) {
          const Complex gradient =
              matrix_gradient[row * D + column];
          for (int a = 0; a < 2; ++a) {
            frame_gradient[2 * row + a] +=
                gradient * frame[2 * column + a] *
                    std::conj(eigenvalue[a]) +
                std::conj(matrix_gradient[column * D + row]) *
                    frame[2 * column + a] * eigenvalue[a];
            eigen_gradient[a] +=
                std::conj(frame[2 * row + a]) * gradient *
                frame[2 * column + a];
          }
        }
      }
      tangent_project(frame, frame_gradient);
      const double radial =
          std::real(
              std::conj(eigenvalue[0]) * eigen_gradient[0] +
              std::conj(eigenvalue[1]) * eigen_gradient[1]);
      for (int a = 0; a < 2; ++a)
        eigen_gradient[a] -= radial * eigenvalue[a];
      const double gradient_squared =
          norm_squared(frame_gradient) +
          std::norm(eigen_gradient[0]) +
          std::norm(eigen_gradient[1]);
      if (gradient_squared < 1e-24) break;

      bool accepted = false;
      double trial = step;
      for (int backtrack = 0; backtrack < 25; ++backtrack) {
        Vec trial_frame = frame;
        std::vector<Complex> trial_eigenvalue = eigenvalue;
        for (int index = 0; index < 2 * D; ++index)
          trial_frame[index] -= trial * frame_gradient[index];
        for (int a = 0; a < 2; ++a)
          trial_eigenvalue[a] -= trial * eigen_gradient[a];
        orthonormalize(trial_frame);
        eigen_norm = std::sqrt(
            std::norm(trial_eigenvalue[0]) +
            std::norm(trial_eigenvalue[1]));
        for (Complex& entry : trial_eigenvalue)
          entry /= std::max(eigen_norm, 1e-300);
        const Vec trial_matrix =
            normal_matrix(trial_frame, trial_eigenvalue);
        const double trial_value = objective(trial_matrix);
        if (trial_value <=
            value - 1e-5 * trial * gradient_squared) {
          frame.swap(trial_frame);
          eigenvalue.swap(trial_eigenvalue);
          step = std::min(initial_step, 1.2 * trial);
          accepted = true;
          break;
        }
        trial *= 0.5;
      }
      if (!accepted) break;
    }
    return best;
  }

  void save_matrix(const std::string& path, const Vec& matrix) const {
    std::ofstream output(path);
    output << std::setprecision(17);
    for (int row = 0; row < D; ++row)
      for (int column = 0; column < D; ++column) {
        const Complex value = matrix[row * D + column];
        output << row << " " << column << " "
               << std::real(value) << " " << std::imag(value) << "\n";
      }
  }

  void save_barrier_state(
      const std::string& path, const Vec& left, const Vec& right,
      const std::vector<double>& singular) const {
    std::ofstream output(path);
    output << std::setprecision(17);
    output << "singular " << singular[0] << " " << singular[1] << "\n";
    for (int row = 0; row < D; ++row)
      for (int a = 0; a < 2; ++a)
        output << "left " << row << " " << a << " "
               << std::real(left[2 * row + a]) << " "
               << std::imag(left[2 * row + a]) << "\n";
    for (int row = 0; row < D; ++row)
      for (int a = 0; a < 2; ++a)
        output << "right " << row << " " << a << " "
               << std::real(right[2 * row + a]) << " "
               << std::imag(right[2 * row + a]) << "\n";
  }
};

int main(int argc, char** argv) {
  if (argc < 6) {
    std::cerr
        << "usage: search_rank2_complex general|fixed|normal|barrier d n "
        << "starts iterations [seed] [output] [mu-or-s0] [ridge]\n";
    return 2;
  }
  const std::string mode = argv[1];
  const int d = std::stoi(argv[2]);
  const int n = std::stoi(argv[3]);
  const int starts = std::stoi(argv[4]);
  const int iterations = std::stoi(argv[5]);
  const std::uint64_t seed =
      argc >= 7 ? std::stoull(argv[6]) : UINT64_C(20260728);
  const std::string output = argc >= 8 ? argv[7] : "";
  const double mu = argc >= 9 ? std::stod(argv[8]) : 1e-3;
  const double ridge = argc >= 10 ? std::stod(argv[9]) : 1e-10;
  Search search(d, n, seed);
  if (mode == "even" || mode == "even_fixed" ||
      mode == "even_crosscheck")
    search.use_even_reduction = true;
  if (mode == "crosscheck" || mode == "even_crosscheck") {
    double minimum_shifted_determinant =
        std::numeric_limits<double>::infinity();
    double minimum_real_determinant =
        std::numeric_limits<double>::infinity();
    double minimum_energy_monge =
        std::numeric_limits<double>::infinity();
    double maximum_exterior_difference = 0.0;
    double maximum_feature_plucker_violation =
        -std::numeric_limits<double>::infinity();
    double maximum_shifted_minor_violation =
        -std::numeric_limits<double>::infinity();
    const double ground = std::pow(0.5, n);
    for (int trial = 0; trial < starts * iterations; ++trial) {
      Vec left(2 * search.D), right(2 * search.D);
      for (Complex& entry : left)
        entry = Complex(search.normal(search.rng), search.normal(search.rng));
      for (Complex& entry : right)
        entry = Complex(search.normal(search.rng), search.normal(search.rng));
      search.orthonormalize(left);
      search.orthonormalize(right);
      std::vector<double> first = {1.0, 0.0};
      std::vector<double> second = {0.0, 1.0};
      const Vec d1 = search.general_matrix(left, right, first);
      const Vec d2 = search.general_matrix(left, right, second);
      const Vec image1 = search.apply_l(d1);
      const Vec image2 = search.apply_l(d2);
      const double a = search.real_inner(d1, image1);
      const double b = search.real_inner(d2, image2);
      Complex c = 0.0;
      for (int index = 0; index < search.D * search.D; ++index)
        c += std::conj(d1[index]) * image2[index];
      const double shifted =
          (a - ground) * (b - ground) -
          std::norm(c + ground);
      const double real_only =
          (a - ground) * (b - ground) -
          std::pow(std::real(c) + ground, 2);
      minimum_shifted_determinant =
          std::min(minimum_shifted_determinant, shifted);
      minimum_real_determinant =
          std::min(minimum_real_determinant, real_only);

      Vec crossed_first(search.D * search.D, 0.0);
      Vec crossed_second(search.D * search.D, 0.0);
      for (int row = 0; row < search.D; ++row)
        for (int column = 0; column < search.D; ++column) {
          crossed_first[row * search.D + column] =
              left[2 * row] *
              std::conj(right[2 * column + 1]);
          crossed_second[row * search.D + column] =
              left[2 * row + 1] *
              std::conj(right[2 * column]);
        }
      const double crossed_a =
          search.objective(crossed_first);
      const double crossed_b =
          search.objective(crossed_second);
      const Vec crossed_second_image =
          search.apply_l(crossed_second);
      Complex crossed_inner = 0.0;
      for (int index = 0; index < search.D * search.D; ++index)
        crossed_inner +=
            std::conj(crossed_first[index]) *
            crossed_second_image[index];
      maximum_exterior_difference = std::max(
          maximum_exterior_difference,
          std::abs(c - crossed_inner));
      if (search.use_even_reduction) {
        Complex trace11 = 0.0, trace22 = 0.0;
        Complex trace12 = 0.0, trace21 = 0.0;
        for (int index = 0; index < search.D; ++index) {
          trace11 += std::conj(right[2 * index]) *
                     left[2 * index];
          trace22 += std::conj(right[2 * index + 1]) *
                     left[2 * index + 1];
          trace12 += std::conj(right[2 * index + 1]) *
                     left[2 * index];
          trace21 += std::conj(right[2 * index]) *
                     left[2 * index + 1];
        }
        const Complex h =
            2.0 * c - std::conj(trace11) * trace22;
        const Complex matched =
            2.0 * crossed_inner -
            std::conj(trace12) * trace21;
        const double g1 =
            2.0 * a + 1.0 - std::norm(trace11);
        const double g2 =
            2.0 * b + 1.0 - std::norm(trace22);
        maximum_feature_plucker_violation = std::max(
            maximum_feature_plucker_violation,
            std::abs(h) - std::abs(matched) - 1.0);
        maximum_shifted_minor_violation = std::max(
            maximum_shifted_minor_violation,
            std::abs(h) -
                1.0 - std::sqrt(std::max(0.0, g1 * g2)));
      }
      const double monge =
          ground +
          std::sqrt(std::max(0.0, (a - ground) * (b - ground))) -
          std::sqrt(std::max(
              0.0, (crossed_a - ground) *
                       (crossed_b - ground)));
      minimum_energy_monge =
          std::min(minimum_energy_monge, monge);
    }
    std::cout << std::setprecision(17)
              << "min_abs_shifted " << minimum_shifted_determinant
              << " min_real_shifted " << minimum_real_determinant
              << " min_energy_monge " << minimum_energy_monge
              << " max_exterior_difference "
              << maximum_exterior_difference
              << " ground " << ground;
    if (search.use_even_reduction)
      std::cout << " max_feature_plucker_violation "
                << maximum_feature_plucker_violation
                << " max_shifted_minor_violation "
                << maximum_shifted_minor_violation;
    std::cout << "\n";
    return 0;
  }
  std::vector<double> fixed_singular;
  if (mode == "fixed" || mode == "even_fixed") {
    if (!(mu >= 0.0 && mu <= 1.0)) {
      std::cerr << "fixed mode requires s0 in [0,1]\n";
      return 2;
    }
    fixed_singular = {mu, std::sqrt(std::max(0.0, 1.0 - mu * mu))};
  }
  double global_best = std::numeric_limits<double>::infinity();
  Vec global_matrix;
  for (int start = 0; start < starts; ++start) {
    Vec matrix;
    Vec barrier_left, barrier_right;
    std::vector<double> barrier_singular;
    double augmented = 0.0;
    double smallest_pivot = 0.0;
    const double value =
        mode == "normal"
            ? search.normal_start(iterations, matrix)
            : (mode == "barrier"
                   ? search.barrier_start(
                         iterations, matrix, mu, ridge, 0.04,
                         &augmented, &smallest_pivot,
                         &barrier_left, &barrier_right,
                         &barrier_singular)
                   : search.general_start(
                         iterations, matrix, 0.08,
                         (mode == "fixed" || mode == "even_fixed")
                             ? &fixed_singular
                             : nullptr,
                         &barrier_left, &barrier_right,
                         &barrier_singular));
    if (value < global_best) {
      global_best = value;
      global_matrix.swap(matrix);
      if (!output.empty()) {
        search.save_matrix(output, global_matrix);
        if (mode == "barrier" || mode == "even" ||
            mode == "even_fixed")
          search.save_barrier_state(
              output + ".state", barrier_left, barrier_right,
              barrier_singular);
      }
    }
    std::cout << "start " << start << " value "
              << std::setprecision(17) << value
              << " global " << global_best;
    if (mode == "barrier")
      std::cout << " augmented " << augmented
                << " smallest_pivot " << smallest_pivot;
    std::cout << "\n";
  }
  std::cout << "best " << std::setprecision(17) << global_best << "\n";
  return 0;
}
