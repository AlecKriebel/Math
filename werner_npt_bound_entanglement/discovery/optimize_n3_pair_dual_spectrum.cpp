// Discovery-only nonlinear power iteration for the dual shifted pair target.
//
// D is constrained to the exact-degree-two qutrit operator sector.  In the
// balanced band s_2 >= s_1/2 the conjectured inequality is
//
//   3(s_1^2-s_1 s_2+s_2^2) <= ||D||_2^2.
//
// The iteration projects the Euclidean gradient back to that linear sector.
// Floating-point output is conjecture-generation evidence only.

#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

using Complex = std::complex<double>;
using Matrix = std::vector<Complex>;

constexpr int local_dimension = 3;
constexpr int sites = 3;
constexpr int dimension = 27;

Complex inner(const Matrix& x, const Matrix& y) {
  Complex value = 0.0;
  for (std::size_t i = 0; i < x.size(); ++i)
    value += std::conj(x[i]) * y[i];
  return value;
}

double norm_squared(const Matrix& x) {
  return std::real(inner(x, x));
}

void normalize(Matrix& x) {
  const double scale = std::sqrt(norm_squared(x));
  for (Complex& z : x) z /= scale;
}

Matrix scalar_part(const Matrix& matrix, int site) {
  Matrix out(dimension * dimension, 0.0);
  int place = 1;
  for (int i = 0; i < site; ++i) place *= local_dimension;
  for (int row = 0; row < dimension; ++row) {
    const int row_digit = (row / place) % local_dimension;
    const int row_base = row - row_digit * place;
    for (int column = 0; column < dimension; ++column) {
      const int column_digit = (column / place) % local_dimension;
      if (column_digit != row_digit) continue;
      const int column_base = column - column_digit * place;
      Complex trace = 0.0;
      for (int value = 0; value < local_dimension; ++value)
        trace += matrix[(row_base + value * place) * dimension
                        + column_base + value * place];
      out[row * dimension + column] =
          trace / static_cast<double>(local_dimension);
    }
  }
  return out;
}

Matrix exact_sector(Matrix matrix, int traceless_mask) {
  for (int site = 0; site < sites; ++site) {
    Matrix scalar = scalar_part(matrix, site);
    if ((traceless_mask >> site) & 1) {
      for (std::size_t i = 0; i < matrix.size(); ++i)
        matrix[i] -= scalar[i];
    } else {
      matrix.swap(scalar);
    }
  }
  return matrix;
}

Matrix pair_projection(const Matrix& matrix) {
  Matrix out(dimension * dimension, 0.0);
  for (int mask : {3, 5, 6}) {
    Matrix part = exact_sector(matrix, mask);
    for (std::size_t i = 0; i < out.size(); ++i) out[i] += part[i];
  }
  return out;
}

Matrix even_projection(const Matrix& matrix) {
  Matrix out = pair_projection(matrix);
  Matrix scalar = exact_sector(matrix, 0);
  for (std::size_t i = 0; i < out.size(); ++i) out[i] += scalar[i];
  return out;
}

// Descending eigensystem of a small complex Hermitian matrix, by Jacobi
// rotations. Eigenvectors are stored as columns.
void hermitian_eigensystem(
    Matrix matrix, std::vector<double>& eigenvalues, Matrix& vectors) {
  const int n = dimension;
  vectors.assign(n * n, 0.0);
  for (int i = 0; i < n; ++i) vectors[i * n + i] = 1.0;
  for (int sweep = 0; sweep < 20000; ++sweep) {
    int p = 0, q = 1;
    double largest = 0.0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j)
        if (std::abs(matrix[i * n + j]) > largest) {
          largest = std::abs(matrix[i * n + j]);
          p = i;
          q = j;
        }
    if (largest < 1e-12) break;
    const double a = std::real(matrix[p * n + p]);
    const double b = std::real(matrix[q * n + q]);
    const Complex z = matrix[p * n + q];
    const double radius = std::hypot(0.5 * (a - b), std::abs(z));
    const double lambda = 0.5 * (a + b) - radius;
    Complex x = z;
    Complex y = lambda - a;
    double length = std::sqrt(std::norm(x) + std::norm(y));
    if (length < 1e-15) {
      x = 1.0;
      y = 0.0;
      length = 1.0;
    }
    x /= length;
    y /= length;
    const Complex u00 = x, u10 = y;
    const Complex u01 = -std::conj(y), u11 = std::conj(x);

    Matrix next = matrix;
    for (int i = 0; i < n; ++i) {
      const Complex aip = matrix[i * n + p];
      const Complex aiq = matrix[i * n + q];
      next[i * n + p] = aip * u00 + aiq * u10;
      next[i * n + q] = aip * u01 + aiq * u11;
    }
    matrix.swap(next);
    next = matrix;
    for (int j = 0; j < n; ++j) {
      const Complex apj = matrix[p * n + j];
      const Complex aqj = matrix[q * n + j];
      next[p * n + j] =
          std::conj(u00) * apj + std::conj(u10) * aqj;
      next[q * n + j] =
          std::conj(u01) * apj + std::conj(u11) * aqj;
    }
    matrix.swap(next);
    matrix[p * n + q] = matrix[q * n + p] = 0.0;
    matrix[p * n + p] = std::real(matrix[p * n + p]);
    matrix[q * n + q] = std::real(matrix[q * n + q]);

    for (int i = 0; i < n; ++i) {
      const Complex vip = vectors[i * n + p];
      const Complex viq = vectors[i * n + q];
      vectors[i * n + p] = vip * u00 + viq * u10;
      vectors[i * n + q] = vip * u01 + viq * u11;
    }
  }
  std::vector<int> order(n);
  for (int i = 0; i < n; ++i) order[i] = i;
  std::sort(order.begin(), order.end(), [&](int i, int j) {
    return std::real(matrix[i * n + i])
           > std::real(matrix[j * n + j]);
  });
  eigenvalues.resize(n);
  Matrix sorted(n * n);
  for (int column = 0; column < n; ++column) {
    eigenvalues[column] =
        std::real(matrix[order[column] * n + order[column]]);
    for (int row = 0; row < n; ++row)
      sorted[row * n + column] =
          vectors[row * n + order[column]];
  }
  vectors.swap(sorted);
}

struct TopPair {
  double s1 = 0.0;
  double s2 = 0.0;
  double s3 = 0.0;
  Matrix u1, u2, v1, v2;
};

TopPair top_pair(const Matrix& d) {
  Matrix gram(dimension * dimension, 0.0);
  for (int i = 0; i < dimension; ++i)
    for (int j = 0; j < dimension; ++j)
      for (int k = 0; k < dimension; ++k)
        gram[i * dimension + j] +=
            std::conj(d[k * dimension + i])
            * d[k * dimension + j];
  std::vector<double> eigenvalues;
  Matrix vectors;
  hermitian_eigensystem(gram, eigenvalues, vectors);
  TopPair out;
  out.s1 = std::sqrt(std::max(0.0, eigenvalues[0]));
  out.s2 = std::sqrt(std::max(0.0, eigenvalues[1]));
  out.s3 = std::sqrt(std::max(0.0, eigenvalues[2]));
  out.v1.resize(dimension);
  out.v2.resize(dimension);
  out.u1.assign(dimension, 0.0);
  out.u2.assign(dimension, 0.0);
  for (int i = 0; i < dimension; ++i) {
    out.v1[i] = vectors[i * dimension];
    out.v2[i] = vectors[i * dimension + 1];
    for (int j = 0; j < dimension; ++j) {
      out.u1[i] += d[i * dimension + j] * out.v1[j];
      out.u2[i] += d[i * dimension + j] * out.v2[j];
    }
    out.u1[i] /= out.s1;
    out.u2[i] /= out.s2;
  }
  return out;
}

Matrix dyad(const Matrix& u, const Matrix& v) {
  Matrix out(dimension * dimension);
  for (int i = 0; i < dimension; ++i)
    for (int j = 0; j < dimension; ++j)
      out[i * dimension + j] = u[i] * std::conj(v[j]);
  return out;
}

double objective(
    const Matrix& d, int mode, TopPair* pair_out = nullptr) {
  TopPair pair = top_pair(d);
  if (pair_out) *pair_out = pair;
  if (mode == 1)
    return (pair.s1 * pair.s1 + pair.s2 * pair.s2)
           / norm_squared(d);
  return 3.0
         * (pair.s1 * pair.s1 - pair.s1 * pair.s2
            + pair.s2 * pair.s2)
         / norm_squared(d);
}

int main(int argc, char** argv) {
  const int starts = argc > 1 ? std::stoi(argv[1]) : 20;
  const int iterations = argc > 2 ? std::stoi(argv[2]) : 1000;
  const std::uint64_t seed =
      argc > 3 ? std::stoull(argv[3]) : UINT64_C(20260729);
  const int mode = argc > 4 ? std::stoi(argv[4]) : 0;
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  std::cout << std::setprecision(15);
  for (int start = 0; start < starts; ++start) {
    Matrix d(dimension * dimension);
    for (Complex& z : d) z = Complex(normal(rng), normal(rng));
    d = mode == 1 ? even_projection(d) : pair_projection(d);
    normalize(d);
    double value = objective(d, mode);
    double step = 0.25;
    int iteration = 0;
    for (; iteration < iterations; ++iteration) {
      TopPair pair;
      value = objective(d, mode, &pair);
      if (mode == 0 && pair.s2 < 0.5 * pair.s1) break;
      Matrix e1 = dyad(pair.u1, pair.v1);
      Matrix e2 = dyad(pair.u2, pair.v2);
      Matrix gradient(dimension * dimension);
      const double c1 =
          mode == 1 ? pair.s1 : 3.0 * (2.0 * pair.s1 - pair.s2);
      const double c2 =
          mode == 1 ? pair.s2 : 3.0 * (2.0 * pair.s2 - pair.s1);
      for (std::size_t i = 0; i < gradient.size(); ++i)
        gradient[i] = c1 * e1[i] + c2 * e2[i];
      gradient =
          mode == 1 ? even_projection(gradient)
                    : pair_projection(gradient);
      normalize(gradient);
      const Complex alignment = inner(d, gradient);
      for (Complex& z : gradient)
        z *= std::exp(Complex(0.0, -std::arg(alignment)));

      bool accepted = false;
      double trial_step = step;
      for (int backtrack = 0; backtrack < 30; ++backtrack) {
        Matrix trial = d;
        for (std::size_t i = 0; i < trial.size(); ++i)
          trial[i] =
              (1.0 - trial_step) * trial[i]
              + trial_step * gradient[i];
        trial =
            mode == 1 ? even_projection(trial)
                      : pair_projection(trial);
        normalize(trial);
        const double trial_value = objective(trial, mode);
        if (trial_value >= value - 1e-12) {
          d.swap(trial);
          value = trial_value;
          step = std::min(0.8, 1.03 * trial_step);
          accepted = true;
          break;
        }
        trial_step *= 0.5;
      }
      if (!accepted || trial_step < 1e-10) break;
    }
    TopPair pair;
    value = objective(d, mode, &pair);
    const double scalar_mass =
        norm_squared(exact_sector(d, 0));
    std::cout << "start " << start << " iterations " << iteration
              << " objective " << value
              << " ratio " << pair.s2 / pair.s1
              << " s1 " << pair.s1 << " s2 " << pair.s2
              << " s3 " << pair.s3
              << " scalar_mass " << scalar_mass
              << " tail "
              << 1.0 - pair.s1 * pair.s1 - pair.s2 * pair.s2
              << "\n";
  }
}
