// Constant-memory A,B -> GF(2) -> C,D search for circulant good matrices.
//
// A normalized skew A and symmetric B determine the symmetric quotient
// D/C through the good-matrix product theorem.  The mod-four shadows of the
// remaining correlation equations form an 83-variable GF(2) system for C.
// This program streams random (A,B) pairs, solves that exact necessary
// system, applies the exact C,D weights, and checks every survivor in the
// original integer PAF equations.  It is deliberately single-threaded and
// uses fixed-size arrays.  Only an exact candidate is written in the format
// accepted by verify_good_167.py.

#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>

namespace {

constexpr int ORDER = 167;
constexpr int MAX_HALF = (ORDER - 1) / 2;
constexpr int MAX_ORDER = ORDER;

struct Bits83 {
  std::uint64_t low = 0;
  std::uint64_t high = 0;

  bool test(int index) const {
    if (index < 0 || index >= MAX_HALF)
      throw std::runtime_error("bit index is out of range");
    return index < 64 ? ((low >> index) & 1U) != 0
                      : ((high >> (index - 64)) & 1U) != 0;
  }

  void set(int index) {
    if (index < 0 || index >= MAX_HALF)
      throw std::runtime_error("bit index is out of range");
    if (index < 64)
      low |= std::uint64_t{1} << index;
    else
      high |= std::uint64_t{1} << (index - 64);
  }

  void clear(int index) {
    if (index < 0 || index >= MAX_HALF)
      throw std::runtime_error("bit index is out of range");
    if (index < 64)
      low &= ~(std::uint64_t{1} << index);
    else
      high &= ~(std::uint64_t{1} << (index - 64));
  }

  void toggle(int index) {
    if (index < 0 || index >= MAX_HALF)
      throw std::runtime_error("bit index is out of range");
    if (index < 64)
      low ^= std::uint64_t{1} << index;
    else
      high ^= std::uint64_t{1} << (index - 64);
  }

  void trim(int variables) {
    if (variables < 0 || variables > MAX_HALF)
      throw std::runtime_error("bit width is out of range");
    if (variables < 64) {
      low &= variables == 0 ? 0 : (std::uint64_t{1} << variables) - 1;
      high = 0;
    } else {
      const int high_bits = variables - 64;
      high &= high_bits == 0
                  ? 0
                  : (std::uint64_t{1} << high_bits) - 1;
    }
  }

  int count() const {
    return std::popcount(low) + std::popcount(high);
  }

  bool empty() const { return low == 0 && high == 0; }

  friend Bits83 operator^(Bits83 left, const Bits83 &right) {
    left.low ^= right.low;
    left.high ^= right.high;
    return left;
  }

  Bits83 &operator^=(const Bits83 &right) {
    low ^= right.low;
    high ^= right.high;
    return *this;
  }

  friend bool operator==(const Bits83 &, const Bits83 &) = default;
};

int dot_parity(const Bits83 &left, const Bits83 &right) {
  return (std::popcount(left.low & right.low) +
          std::popcount(left.high & right.high)) &
         1;
}

using Sequence = std::array<std::int8_t, MAX_ORDER>;
using Residuals = std::array<int, MAX_HALF + 1>;

struct Instance {
  int n = ORDER;
  int half = MAX_HALF;
  int inverse_two = (ORDER + 1) / 2;

  explicit Instance(int requested_n) : n(requested_n) {
    if (n <= 1 || n > MAX_ORDER || n % 2 == 0)
      throw std::runtime_error("order must be odd and between 3 and 167");
    half = (n - 1) / 2;
    inverse_two = (n + 1) / 2;
  }
};

struct Equation {
  Bits83 coefficients{};
  bool rhs = false;
};

enum class EarlyReason {
  none,
  q_nonintegral,
  fixed_edge_parity,
  edge_parity,
  edge_count_bound,
};

struct LinearSystem {
  std::array<Equation, MAX_HALF> rows{};
  int row_count = 0;
  int variables = 0;
  EarlyReason early_reason = EarlyReason::none;
  int early_lag = 0;
};

struct LinearSolution {
  int rank = 0;
  bool inconsistent = false;
  Bits83 particular{};
  std::array<Bits83, MAX_HALF> nullspace{};
  int nullity = 0;
};

struct CoefficientMatrix {
  std::array<Bits83, MAX_HALF> rows{};
  std::array<int, MAX_HALF> representative_counts{};
  int row_count = 0;
  int variables = 0;
  Bits83 s_mask{};
};

struct MatrixFactorization {
  std::array<Bits83, MAX_HALF> rref_rows{};
  std::array<Bits83, MAX_HALF> transforms{};
  std::array<int, MAX_HALF> pivot_columns{};
  std::array<Bits83, MAX_HALF> nullspace{};
  int rows = 0;
  int variables = 0;
  int rank = 0;
  int nullity = 0;
};

struct FactoredSolution {
  bool inconsistent = false;
  Bits83 particular{};
};

enum class Outcome {
  early_rejection,
  inconsistent,
  deferred_nullity,
  weight_rejection,
  exact_paf_rejection,
  exact,
};

constexpr int OUTCOME_COUNT = 6;

struct Evaluation {
  Outcome outcome = Outcome::early_rejection;
  EarlyReason early_reason = EarlyReason::none;
  int early_lag = 0;
  int rank = 0;
  int nullity = 0;
  std::uint64_t weight_survivors = 0;
  std::int64_t energy = std::numeric_limits<std::int64_t>::max();
  int bad_lags = 0;
  int max_abs_quarter = 0;
  Bits83 c_mask{};
  Bits83 d_mask{};
  Residuals residual{};
};

struct SplitMix64 {
  std::uint64_t state;

  explicit SplitMix64(std::uint64_t seed) : state(seed) {}

  std::uint64_t next() {
    std::uint64_t value = (state += 0x9e3779b97f4a7c15ULL);
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
  }

  std::uint64_t bounded(std::uint64_t bound) {
    if (bound == 0) throw std::runtime_error("bounded RNG received zero");
    const std::uint64_t threshold = -bound % bound;
    for (;;) {
      const std::uint64_t value = next();
      if (value >= threshold) return value % bound;
    }
  }
};

int normalize(int value, int n) {
  value %= n;
  return value < 0 ? value + n : value;
}

int pair_variable(int index, const Instance &instance) {
  index = normalize(index, instance.n);
  if (index == 0) return -1;
  return std::min(index, instance.n - index) - 1;
}

Sequence symmetric_from_mask(const Bits83 &mask, const Instance &instance) {
  Sequence result{};
  result[0] = 1;
  for (int index = 1; index <= instance.half; ++index) {
    const std::int8_t sign = mask.test(index - 1) ? -1 : 1;
    result[index] = sign;
    result[instance.n - index] = sign;
  }
  return result;
}

Sequence skew_from_mask(const Bits83 &mask, const Instance &instance) {
  Sequence result{};
  result[0] = 1;
  for (int index = 1; index <= instance.half; ++index) {
    const std::int8_t sign = mask.test(index - 1) ? -1 : 1;
    result[index] = sign;
    result[instance.n - index] = -sign;
  }
  return result;
}

int row_sum(const Sequence &sequence, const Instance &instance) {
  int result = 0;
  for (int index = 0; index < instance.n; ++index) result += sequence[index];
  return result;
}

int periodic_correlation(const Sequence &sequence, int lag,
                         const Instance &instance) {
  int result = 0;
  for (int index = 0; index < instance.n; ++index)
    result += sequence[index] * sequence[(index + lag) % instance.n];
  return result;
}

Sequence derive_s(const Sequence &a, const Sequence &b,
                  const Instance &instance) {
  Sequence result{};
  result[0] = 1;
  for (int index = 1; index < instance.n; ++index)
    result[index] = -a[index] * a[(2 * index) % instance.n] * b[index];
  for (int index = 1; index <= instance.half; ++index)
    if (result[index] != result[instance.n - index])
      throw std::runtime_error("derived quotient S is not symmetric");
  return result;
}

Sequence derive_a_from_s_b(const Sequence &s, const Sequence &b,
                           const Instance &instance) {
  if (instance.n != ORDER)
    throw std::runtime_error("S,B parameterization is implemented at order 167");
  Sequence result{};
  result[0] = 1;
  result[1] = 1;  // A[1]=+1.
  int index = 1;
  for (int step = 0; step < instance.half; ++step) {
    const int next = (2 * index) % instance.n;
    const std::int8_t next_sign = -s[index] * result[index] * b[index];
    if (step + 1 == instance.half) {
      if (next != 1 || next_sign != 1)
        throw std::runtime_error("S,B doubling recurrence does not close");
    } else {
      if (next == 1 || result[next] != 0)
        throw std::runtime_error("doubling cycle repeated before closure");
      result[next] = next_sign;
    }
    index = next;
  }
  for (int position = 1; position < instance.n; ++position) {
    if (result[position] == 0 && result[instance.n - position] != 0)
      result[position] = -result[instance.n - position];
  }
  for (int position = 1; position <= instance.half; ++position)
    if (result[position] == 0 ||
        result[position] != -result[instance.n - position])
      throw std::runtime_error("recovered A is not skew");
  return result;
}

Bits83 half_negative_mask(const Sequence &sequence,
                          const Instance &instance) {
  Bits83 result;
  for (int index = 1; index <= instance.half; ++index)
    if (sequence[index] == -1) result.set(index - 1);
  return result;
}

LinearSystem build_linear_system(const Sequence &a, const Sequence &b,
                                 const Sequence &s,
                                 const Instance &instance) {
  LinearSystem system;
  system.variables = instance.half;
  const Bits83 s_mask = half_negative_mask(s, instance);

  for (int lag = 1; lag <= instance.half; ++lag) {
    const int q_numerator =
        -(periodic_correlation(a, lag, instance) +
          periodic_correlation(b, lag, instance));
    if (q_numerator % 2 != 0) {
      system.early_reason = EarlyReason::q_nonintegral;
      system.early_lag = lag;
      return system;
    }
    const int q = q_numerator / 2;
    const int fixed = normalize(-lag * instance.inverse_two, instance.n);
    if (s[fixed] != s[(fixed + lag) % instance.n])
      throw std::runtime_error("reflection-fixed edge is not selected");

    Equation equation;
    int representatives = 0;
    for (int index = 0; index < instance.n; ++index) {
      const int endpoint = (index + lag) % instance.n;
      if (s[index] != s[endpoint] || index == fixed) continue;
      const int mate = normalize(-index - lag, instance.n);
      if (mate == index || s[mate] != s[(mate + lag) % instance.n])
        throw std::runtime_error("edge-reflection orbit mismatch");
      if (index > mate) continue;
      ++representatives;
      for (int vertex : {index, endpoint}) {
        const int variable = pair_variable(vertex, instance);
        if (variable >= 0) equation.coefficients.toggle(variable);
      }
    }

    if ((q - 1) % 2 != 0) {
      system.early_reason = EarlyReason::fixed_edge_parity;
      system.early_lag = lag;
      return system;
    }
    const int sign_sum_target = (q - 1) / 2;
    const int negative_edge_numerator = representatives - sign_sum_target;
    if (negative_edge_numerator % 2 != 0) {
      system.early_reason = EarlyReason::edge_parity;
      system.early_lag = lag;
      return system;
    }
    const int negative_edges = negative_edge_numerator / 2;
    if (negative_edges < 0 || negative_edges > representatives) {
      system.early_reason = EarlyReason::edge_count_bound;
      system.early_lag = lag;
      return system;
    }
    equation.rhs = (negative_edges & 1) != 0;
    if (dot_parity(equation.coefficients, s_mask) != 0)
      throw std::runtime_error("C/D swap mask is not homogeneous");
    system.rows[system.row_count++] = equation;
  }
  return system;
}

CoefficientMatrix build_coefficient_matrix(const Sequence &s,
                                           const Instance &instance) {
  CoefficientMatrix matrix;
  matrix.variables = instance.half;
  matrix.s_mask = half_negative_mask(s, instance);
  for (int lag = 1; lag <= instance.half; ++lag) {
    const int fixed = normalize(-lag * instance.inverse_two, instance.n);
    if (s[fixed] != s[(fixed + lag) % instance.n])
      throw std::runtime_error("reflection-fixed edge is not selected");
    Bits83 coefficients;
    int representatives = 0;
    for (int index = 0; index < instance.n; ++index) {
      const int endpoint = (index + lag) % instance.n;
      if (s[index] != s[endpoint] || index == fixed) continue;
      const int mate = normalize(-index - lag, instance.n);
      if (mate == index || s[mate] != s[(mate + lag) % instance.n])
        throw std::runtime_error("edge-reflection orbit mismatch");
      if (index > mate) continue;
      ++representatives;
      for (int vertex : {index, endpoint}) {
        const int variable = pair_variable(vertex, instance);
        if (variable >= 0) coefficients.toggle(variable);
      }
    }
    if (dot_parity(coefficients, matrix.s_mask) != 0)
      throw std::runtime_error("C/D swap mask is not homogeneous");
    matrix.rows[matrix.row_count] = coefficients;
    matrix.representative_counts[matrix.row_count] = representatives;
    ++matrix.row_count;
  }
  return matrix;
}

bool build_rhs(const Sequence &a, const Sequence &b,
               const CoefficientMatrix &matrix, const Instance &instance,
               Bits83 &rhs, EarlyReason &reason, int &rejection_lag) {
  rhs = {};
  reason = EarlyReason::none;
  rejection_lag = 0;
  for (int row = 0; row < matrix.row_count; ++row) {
    const int lag = row + 1;
    const int q_numerator =
        -(periodic_correlation(a, lag, instance) +
          periodic_correlation(b, lag, instance));
    if (q_numerator % 2 != 0) {
      reason = EarlyReason::q_nonintegral;
      rejection_lag = lag;
      return false;
    }
    const int q = q_numerator / 2;
    if ((q - 1) % 2 != 0) {
      reason = EarlyReason::fixed_edge_parity;
      rejection_lag = lag;
      return false;
    }
    const int sign_sum_target = (q - 1) / 2;
    const int negative_edge_numerator =
        matrix.representative_counts[row] - sign_sum_target;
    if (negative_edge_numerator % 2 != 0) {
      reason = EarlyReason::edge_parity;
      rejection_lag = lag;
      return false;
    }
    const int negative_edges = negative_edge_numerator / 2;
    if (negative_edges < 0 ||
        negative_edges > matrix.representative_counts[row]) {
      reason = EarlyReason::edge_count_bound;
      rejection_lag = lag;
      return false;
    }
    if ((negative_edges & 1) != 0) rhs.set(row);
  }
  return true;
}

MatrixFactorization factor_matrix(const CoefficientMatrix &matrix) {
  MatrixFactorization factor;
  factor.rows = matrix.row_count;
  factor.variables = matrix.variables;
  factor.rref_rows = matrix.rows;
  for (int row = 0; row < matrix.row_count; ++row)
    factor.transforms[row].set(row);

  int pivot_row = 0;
  for (int column = 0; column < matrix.variables; ++column) {
    int found = -1;
    for (int row = pivot_row; row < matrix.row_count; ++row) {
      if (factor.rref_rows[row].test(column)) {
        found = row;
        break;
      }
    }
    if (found < 0) continue;
    std::swap(factor.rref_rows[pivot_row], factor.rref_rows[found]);
    std::swap(factor.transforms[pivot_row], factor.transforms[found]);
    for (int row = 0; row < matrix.row_count; ++row) {
      if (row != pivot_row && factor.rref_rows[row].test(column)) {
        factor.rref_rows[row] ^= factor.rref_rows[pivot_row];
        factor.transforms[row] ^= factor.transforms[pivot_row];
      }
    }
    factor.pivot_columns[pivot_row] = column;
    ++pivot_row;
  }
  factor.rank = pivot_row;

  std::array<bool, MAX_HALF> is_pivot{};
  for (int row = 0; row < factor.rank; ++row)
    is_pivot[factor.pivot_columns[row]] = true;
  for (int free_column = 0; free_column < factor.variables; ++free_column) {
    if (is_pivot[free_column]) continue;
    Bits83 vector;
    vector.set(free_column);
    for (int row = 0; row < factor.rank; ++row)
      if (factor.rref_rows[row].test(free_column))
        vector.set(factor.pivot_columns[row]);
    factor.nullspace[factor.nullity++] = vector;
  }

  for (int row = 0; row < matrix.row_count; ++row) {
    Bits83 reconstructed;
    for (int source = 0; source < matrix.row_count; ++source)
      if (factor.transforms[row].test(source))
        reconstructed ^= matrix.rows[source];
    if (reconstructed != factor.rref_rows[row])
      throw std::runtime_error("GF(2) row transform failed reconstruction");
  }
  for (int basis = 0; basis < factor.nullity; ++basis)
    for (int row = 0; row < matrix.row_count; ++row)
      if (dot_parity(matrix.rows[row], factor.nullspace[basis]) != 0)
        throw std::runtime_error("factored null vector failed an equation");
  if (!matrix.s_mask.empty() && factor.rank >= matrix.variables)
    throw std::runtime_error("nonzero C/D swap mask did not lower matrix rank");
  return factor;
}

FactoredSolution solve_factored(const MatrixFactorization &factor,
                                const Bits83 &rhs) {
  FactoredSolution solution;
  for (int row = 0; row < factor.rows; ++row) {
    const bool transformed_rhs = dot_parity(factor.transforms[row], rhs) != 0;
    if (row >= factor.rank) {
      if (transformed_rhs) {
        solution.inconsistent = true;
        return solution;
      }
    } else if (transformed_rhs) {
      solution.particular.set(factor.pivot_columns[row]);
    }
  }
  return solution;
}

bool equation_holds(const Equation &equation, const Bits83 &vector) {
  return dot_parity(equation.coefficients, vector) == equation.rhs;
}

LinearSolution solve_linear_system(const LinearSystem &system) {
  if (system.early_reason != EarlyReason::none)
    throw std::runtime_error("cannot solve an early-rejected system");
  std::array<Equation, MAX_HALF> rows = system.rows;
  std::array<int, MAX_HALF> pivot_columns{};
  int pivot_row = 0;
  for (int column = 0; column < system.variables; ++column) {
    int found = -1;
    for (int index = pivot_row; index < system.row_count; ++index) {
      if (rows[index].coefficients.test(column)) {
        found = index;
        break;
      }
    }
    if (found < 0) continue;
    std::swap(rows[pivot_row], rows[found]);
    for (int index = 0; index < system.row_count; ++index) {
      if (index != pivot_row && rows[index].coefficients.test(column)) {
        rows[index].coefficients ^= rows[pivot_row].coefficients;
        rows[index].rhs = rows[index].rhs != rows[pivot_row].rhs;
      }
    }
    pivot_columns[pivot_row] = column;
    ++pivot_row;
  }

  LinearSolution solution;
  solution.rank = pivot_row;
  for (int index = 0; index < system.row_count; ++index) {
    if (rows[index].coefficients.empty() && rows[index].rhs) {
      solution.inconsistent = true;
      return solution;
    }
  }

  for (int index = 0; index < pivot_row; ++index)
    if (rows[index].rhs) solution.particular.set(pivot_columns[index]);

  std::array<bool, MAX_HALF> is_pivot{};
  for (int index = 0; index < pivot_row; ++index)
    is_pivot[pivot_columns[index]] = true;
  for (int free_column = 0; free_column < system.variables; ++free_column) {
    if (is_pivot[free_column]) continue;
    Bits83 vector;
    vector.set(free_column);
    for (int index = 0; index < pivot_row; ++index)
      if (rows[index].coefficients.test(free_column))
        vector.set(pivot_columns[index]);
    solution.nullspace[solution.nullity++] = vector;
  }

  for (int index = 0; index < system.row_count; ++index) {
    if (!equation_holds(system.rows[index], solution.particular))
      throw std::runtime_error("RREF particular vector failed an equation");
    for (int basis = 0; basis < solution.nullity; ++basis)
      if (dot_parity(system.rows[index].coefficients,
                     solution.nullspace[basis]) != 0)
        throw std::runtime_error("RREF null vector failed an equation");
  }
  return solution;
}

void correlation_metrics(const Sequence &a, const Sequence &b,
                         const Sequence &c, const Sequence &d,
                         const Instance &instance, Evaluation &evaluation) {
  evaluation.energy = 0;
  evaluation.bad_lags = 0;
  evaluation.max_abs_quarter = 0;
  evaluation.residual.fill(0);
  evaluation.residual[0] = 4 * instance.n;
  for (int lag = 1; lag <= instance.half; ++lag) {
    const int residual = periodic_correlation(a, lag, instance) +
                         periodic_correlation(b, lag, instance) +
                         periodic_correlation(c, lag, instance) +
                         periodic_correlation(d, lag, instance);
    if (residual % 4 != 0)
      throw std::runtime_error("good-matrix residual is not divisible by four");
    evaluation.residual[lag] = residual;
    const int quarter = residual / 4;
    evaluation.energy += static_cast<std::int64_t>(quarter) * quarter;
    if (quarter != 0) ++evaluation.bad_lags;
    evaluation.max_abs_quarter =
        std::max(evaluation.max_abs_quarter, std::abs(quarter));
  }
}

bool exact_full_validation(const Sequence &a, const Sequence &b,
                           const Sequence &c, const Sequence &d,
                           int b_sum, int c_sum, int d_sum,
                           const Instance &instance) {
  if (a[0] != 1 || b[0] != 1 || c[0] != 1 || d[0] != 1) return false;
  for (int index = 1; index <= instance.half; ++index) {
    if (a[index] != -a[instance.n - index] ||
        b[index] != b[instance.n - index] ||
        c[index] != c[instance.n - index] ||
        d[index] != d[instance.n - index])
      return false;
  }
  if (row_sum(a, instance) != 1 || row_sum(b, instance) != b_sum ||
      row_sum(c, instance) != c_sum || row_sum(d, instance) != d_sum)
    return false;
  for (int index = 1; index < instance.n; ++index)
    if (a[index] * b[index] * c[index] * d[index] !=
        -a[(2 * index) % instance.n])
      return false;
  for (int lag = 0; lag < instance.n; ++lag) {
    const int expected = lag == 0 ? 4 * instance.n : 0;
    const int actual = periodic_correlation(a, lag, instance) +
                       periodic_correlation(b, lag, instance) +
                       periodic_correlation(c, lag, instance) +
                       periodic_correlation(d, lag, instance);
    if (actual != expected) return false;
  }
  return true;
}

Evaluation evaluate_pair(const Bits83 &a_mask, const Bits83 &b_mask,
                         int c_sum, int d_sum,
                         std::uint64_t max_affine_candidates,
                         const Instance &instance) {
  if ((instance.n - c_sum) % 4 != 0 || (instance.n - d_sum) % 4 != 0)
    throw std::runtime_error("requested row sum has the wrong congruence");
  const int c_weight = (instance.n - c_sum) / 4;
  const int d_weight = (instance.n - d_sum) / 4;
  const Sequence a = skew_from_mask(a_mask, instance);
  const Sequence b = symmetric_from_mask(b_mask, instance);
  const Sequence s = derive_s(a, b, instance);
  const Bits83 s_mask = half_negative_mask(s, instance);
  const LinearSystem system = build_linear_system(a, b, s, instance);

  Evaluation evaluation;
  if (system.early_reason != EarlyReason::none) {
    evaluation.outcome = Outcome::early_rejection;
    evaluation.early_reason = system.early_reason;
    evaluation.early_lag = system.early_lag;
    return evaluation;
  }

  const LinearSolution solution = solve_linear_system(system);
  evaluation.rank = solution.rank;
  evaluation.nullity = solution.nullity;
  if (solution.inconsistent) {
    evaluation.outcome = Outcome::inconsistent;
    return evaluation;
  }
  if (!s_mask.empty() && solution.rank >= instance.half)
    throw std::runtime_error("nonzero C/D swap mask did not lower the rank");

  if (solution.nullity >= 63 ||
      (std::uint64_t{1} << solution.nullity) > max_affine_candidates) {
    evaluation.outcome = Outcome::deferred_nullity;
    return evaluation;
  }
  const std::uint64_t affine_count = std::uint64_t{1} << solution.nullity;
  Bits83 vector = solution.particular;
  std::uint64_t previous_gray = 0;
  for (std::uint64_t selector = 0; selector < affine_count; ++selector) {
    if (selector != 0) {
      const std::uint64_t gray = selector ^ (selector >> 1);
      const std::uint64_t changed = gray ^ previous_gray;
      vector ^= solution.nullspace[std::countr_zero(changed)];
      previous_gray = gray;
    }
    const Bits83 d_mask = vector ^ s_mask;
    if (vector.count() != c_weight || d_mask.count() != d_weight) continue;
    ++evaluation.weight_survivors;
    const Sequence c = symmetric_from_mask(vector, instance);
    const Sequence d = symmetric_from_mask(d_mask, instance);
    Evaluation candidate;
    correlation_metrics(a, b, c, d, instance, candidate);
    if (candidate.energy < evaluation.energy) {
      evaluation.energy = candidate.energy;
      evaluation.bad_lags = candidate.bad_lags;
      evaluation.max_abs_quarter = candidate.max_abs_quarter;
      evaluation.residual = candidate.residual;
      evaluation.c_mask = vector;
      evaluation.d_mask = d_mask;
    }
    if (candidate.energy == 0) {
      if (!exact_full_validation(a, b, c, d,
                                 instance.n - 4 * b_mask.count(), c_sum,
                                 d_sum, instance))
        throw std::runtime_error("zero-energy candidate failed full validation");
      evaluation.outcome = Outcome::exact;
      return evaluation;
    }
  }
  evaluation.outcome = evaluation.weight_survivors == 0
                           ? Outcome::weight_rejection
                           : Outcome::exact_paf_rejection;
  return evaluation;
}

Evaluation evaluate_factored_pair(const Sequence &a, const Sequence &b,
                                  const CoefficientMatrix &matrix,
                                  const MatrixFactorization &factor,
                                  int c_sum, int d_sum,
                                  std::uint64_t max_affine_candidates,
                                  const Instance &instance) {
  if ((instance.n - c_sum) % 4 != 0 || (instance.n - d_sum) % 4 != 0)
    throw std::runtime_error("requested row sum has the wrong congruence");
  const int c_weight = (instance.n - c_sum) / 4;
  const int d_weight = (instance.n - d_sum) / 4;
  Evaluation evaluation;
  Bits83 rhs;
  if (!build_rhs(a, b, matrix, instance, rhs, evaluation.early_reason,
                 evaluation.early_lag)) {
    evaluation.outcome = Outcome::early_rejection;
    return evaluation;
  }

  const FactoredSolution solution = solve_factored(factor, rhs);
  evaluation.rank = factor.rank;
  if (solution.inconsistent) {
    evaluation.outcome = Outcome::inconsistent;
    return evaluation;
  }
  evaluation.nullity = factor.nullity;
  for (int row = 0; row < matrix.row_count; ++row)
    if (dot_parity(matrix.rows[row], solution.particular) != rhs.test(row))
      throw std::runtime_error("factored particular vector failed an equation");
  if (factor.nullity >= 63 ||
      (std::uint64_t{1} << factor.nullity) > max_affine_candidates) {
    evaluation.outcome = Outcome::deferred_nullity;
    return evaluation;
  }

  const Sequence s = symmetric_from_mask(matrix.s_mask, instance);
  const std::uint64_t affine_count = std::uint64_t{1} << factor.nullity;
  Bits83 vector = solution.particular;
  std::uint64_t previous_gray = 0;
  for (std::uint64_t selector = 0; selector < affine_count; ++selector) {
    if (selector != 0) {
      const std::uint64_t gray = selector ^ (selector >> 1);
      const std::uint64_t changed = gray ^ previous_gray;
      vector ^= factor.nullspace[std::countr_zero(changed)];
      previous_gray = gray;
    }
    const Bits83 d_mask = vector ^ matrix.s_mask;
    if (vector.count() != c_weight || d_mask.count() != d_weight) continue;
    ++evaluation.weight_survivors;
    const Sequence c = symmetric_from_mask(vector, instance);
    const Sequence d = symmetric_from_mask(d_mask, instance);
    Evaluation candidate;
    correlation_metrics(a, b, c, d, instance, candidate);
    if (candidate.energy < evaluation.energy) {
      evaluation.energy = candidate.energy;
      evaluation.bad_lags = candidate.bad_lags;
      evaluation.max_abs_quarter = candidate.max_abs_quarter;
      evaluation.residual = candidate.residual;
      evaluation.c_mask = vector;
      evaluation.d_mask = d_mask;
    }
    if (candidate.energy == 0) {
      if (derive_s(a, b, instance) != s)
        throw std::runtime_error("factored S differs from product quotient");
      if (!exact_full_validation(a, b, c, d, 15, c_sum, d_sum, instance))
        throw std::runtime_error("zero-energy candidate failed full validation");
      evaluation.outcome = Outcome::exact;
      return evaluation;
    }
  }
  evaluation.outcome = evaluation.weight_survivors == 0
                           ? Outcome::weight_rejection
                           : Outcome::exact_paf_rejection;
  return evaluation;
}

Bits83 random_a_mask(SplitMix64 &rng, const Instance &instance) {
  Bits83 result{rng.next(), rng.next()};
  result.trim(instance.half);
  result.clear(0);  // exact i -> -i normalization: A[1]=+1.
  return result;
}

Bits83 random_mask_with_weight(SplitMix64 &rng, int variables, int weight) {
  if (variables < 0 || variables > MAX_HALF || weight < 0 || weight > variables)
    throw std::runtime_error("random fixed-weight mask arguments are invalid");
  std::array<int, MAX_HALF> indices{};
  for (int index = 0; index < variables; ++index) indices[index] = index;
  Bits83 result;
  for (int index = 0; index < weight; ++index) {
    const int chosen = index + static_cast<int>(
                                   rng.bounded(variables - index));
    std::swap(indices[index], indices[chosen]);
    result.set(indices[index]);
  }
  return result;
}

std::array<int, MAX_HALF> doubling_cycle_variables(
    const Instance &instance) {
  if (instance.n != ORDER)
    throw std::runtime_error("doubling necklace is implemented at order 167");
  std::array<int, MAX_HALF> result{};
  std::array<bool, MAX_HALF> seen{};
  int value = 1;
  for (int index = 0; index < instance.half; ++index) {
    const int variable = pair_variable(value, instance);
    if (variable < 0 || seen[variable])
      throw std::runtime_error("doubling failed to traverse the quotient");
    seen[variable] = true;
    result[index] = variable;
    value = (2 * value) % instance.n;
  }
  if (value != 1)
    throw std::runtime_error("doubling does not have order 83");
  return result;
}

Bits83 canonicalize_doubling_necklace(const Bits83 &mask,
                                      const Instance &instance) {
  const auto cycle = doubling_cycle_variables(instance);
  std::array<bool, MAX_HALF> word{};
  for (int index = 0; index < instance.half; ++index)
    word[index] = mask.test(cycle[index]);
  int best_shift = 0;
  for (int shift = 1; shift < instance.half; ++shift) {
    for (int offset = 0; offset < instance.half; ++offset) {
      const bool candidate = word[(shift + offset) % instance.half];
      const bool incumbent = word[(best_shift + offset) % instance.half];
      if (candidate == incumbent) continue;
      if (candidate) best_shift = shift;
      break;
    }
  }
  Bits83 result;
  for (int offset = 0; offset < instance.half; ++offset)
    if (word[(best_shift + offset) % instance.half])
      result.set(cycle[offset]);
  return result;
}

std::string outcome_name(Outcome outcome) {
  switch (outcome) {
    case Outcome::early_rejection:
      return "early_rejection";
    case Outcome::inconsistent:
      return "linear_inconsistent";
    case Outcome::deferred_nullity:
      return "deferred_nullity";
    case Outcome::weight_rejection:
      return "weight_rejection";
    case Outcome::exact_paf_rejection:
      return "exact_paf_rejection";
    case Outcome::exact:
      return "exact";
  }
  throw std::runtime_error("unknown outcome");
}

int outcome_index(Outcome outcome) { return static_cast<int>(outcome); }

void write_sequence(std::ostream &output, const Sequence &sequence,
                    const Instance &instance) {
  output << '[';
  for (int index = 0; index < instance.n; ++index) {
    if (index != 0) output << ',';
    output << static_cast<int>(sequence[index]);
  }
  output << ']';
}

std::string mask_hex(const Bits83 &mask) {
  std::ostringstream output;
  output << "0x" << std::hex << std::setfill('0') << std::setw(5)
         << mask.high << std::setw(16) << mask.low;
  return output.str();
}

void prepare_parent(const std::filesystem::path &path) {
  const std::filesystem::path parent = path.parent_path();
  if (!parent.empty()) std::filesystem::create_directories(parent);
}

template <typename Writer>
void write_atomically(const std::filesystem::path &path, Writer writer) {
  prepare_parent(path);
  std::filesystem::path temporary = path;
  temporary += ".tmp";
  {
    std::ofstream output(temporary, std::ios::trunc);
    if (!output) throw std::runtime_error("could not open temporary output");
    writer(output);
    output.flush();
    if (!output) {
      output.close();
      std::filesystem::remove(temporary);
      throw std::runtime_error("could not flush temporary output");
    }
    output.close();
    if (output.fail()) {
      std::filesystem::remove(temporary);
      throw std::runtime_error("could not close temporary output");
    }
  }
  std::error_code error;
  std::filesystem::rename(temporary, path, error);
  if (error) {
    std::filesystem::remove(temporary);
    throw std::runtime_error("could not atomically replace output: " +
                             error.message());
  }
}

void write_exact_candidate(const std::filesystem::path &path,
                           const Bits83 &a_mask, const Bits83 &b_mask,
                           const Evaluation &evaluation, int profile,
                           int c_sum, int d_sum, std::uint64_t trial,
                           std::uint64_t seed,
                           std::string_view parameterization,
                           const Bits83 &s_mask,
                           const Instance &instance) {
  const Sequence a = skew_from_mask(a_mask, instance);
  const Sequence b = symmetric_from_mask(b_mask, instance);
  const Sequence c = symmetric_from_mask(evaluation.c_mask, instance);
  const Sequence d = symmetric_from_mask(evaluation.d_mask, instance);
  write_atomically(path, [&](std::ostream &output) {
    output << "{\n  \"kind\": \"circulant_good_matrices\",\n"
           << "  \"order\": " << instance.n << ",\n"
           << "  \"hadamard_order\": " << 4 * instance.n << ",\n"
           << "  \"profile\": " << profile << ",\n"
           << "  \"parameterization\": \"" << parameterization << "\",\n"
           << "  \"row_sums\": [15," << c_sum << ',' << d_sum << "],\n"
           << "  \"trial\": " << trial << ",\n"
           << "  \"random_seed\": " << seed << ",\n"
           << "  \"s_mask\": \"" << mask_hex(s_mask) << "\",\n"
           << "  \"sequences\": [\n    ";
    write_sequence(output, a, instance);
    output << ",\n    ";
    write_sequence(output, b, instance);
    output << ",\n    ";
    write_sequence(output, c, instance);
    output << ",\n    ";
    write_sequence(output, d, instance);
    output << "\n  ]\n}\n";
  });
}

void write_checkpoint(const std::filesystem::path &path,
                      const Bits83 &a_mask, const Bits83 &b_mask,
                      const Evaluation &evaluation, int profile, int c_sum,
                      int d_sum, std::uint64_t trial, std::uint64_t seed,
                      std::uint64_t trial_rng_state,
                      std::uint64_t next_rng_state,
                      std::string_view parameterization,
                      const Bits83 &s_mask,
                      const Instance &instance) {
  write_atomically(path, [&](std::ostream &output) {
    output << "{\n  \"kind\": \"good_matrix_stream_checkpoint\",\n"
           << "  \"order\": " << instance.n << ",\n"
           << "  \"profile\": " << profile << ",\n"
           << "  \"parameterization\": \"" << parameterization << "\",\n"
           << "  \"row_sums\": [15," << c_sum << ',' << d_sum << "],\n"
           << "  \"trial\": " << trial << ",\n"
           << "  \"random_seed\": " << seed << ",\n"
           << "  \"trial_rng_state\": \"0x" << std::hex
           << trial_rng_state << std::dec << "\",\n"
           << "  \"next_rng_state\": \"0x" << std::hex << next_rng_state
           << std::dec << "\",\n"
           << "  \"energy\": " << evaluation.energy << ",\n"
           << "  \"bad_lags\": " << evaluation.bad_lags << ",\n"
           << "  \"max_abs_quarter\": " << evaluation.max_abs_quarter
           << ",\n"
           << "  \"rank\": " << evaluation.rank << ",\n"
           << "  \"s_mask\": \"" << mask_hex(s_mask) << "\",\n"
           << "  \"a_mask\": \"" << mask_hex(a_mask) << "\",\n"
           << "  \"b_mask\": \"" << mask_hex(b_mask) << "\",\n"
           << "  \"c_mask\": \"" << mask_hex(evaluation.c_mask)
           << "\",\n"
           << "  \"d_mask\": \"" << mask_hex(evaluation.d_mask)
           << "\",\n"
           << "  \"quarter_residuals\": [";
    for (int lag = 1; lag <= instance.half; ++lag) {
      if (lag != 1) output << ',';
      output << evaluation.residual[lag] / 4;
    }
    output << "]\n}\n";
  });
}

bool brute_pair_has_exact(const Bits83 &a_mask, const Bits83 &b_mask,
                          int c_sum, int d_sum,
                          const Instance &instance) {
  const Sequence a = skew_from_mask(a_mask, instance);
  const Sequence b = symmetric_from_mask(b_mask, instance);
  const Sequence s = derive_s(a, b, instance);
  const Bits83 s_mask = half_negative_mask(s, instance);
  const int c_weight = (instance.n - c_sum) / 4;
  const int d_weight = (instance.n - d_sum) / 4;
  const std::uint64_t masks = std::uint64_t{1} << instance.half;
  for (std::uint64_t raw = 0; raw < masks; ++raw) {
    Bits83 c_mask{raw, 0};
    if (c_mask.count() != c_weight) continue;
    const Bits83 d_mask = c_mask ^ s_mask;
    if (d_mask.count() != d_weight) continue;
    const Sequence c = symmetric_from_mask(c_mask, instance);
    const Sequence d = symmetric_from_mask(d_mask, instance);
    if (exact_full_validation(a, b, c, d, row_sum(b, instance), c_sum,
                              d_sum, instance))
      return true;
  }
  return false;
}

void self_test() {
  const Instance small(7);
  int brute_exact_pairs = 0;
  int reducer_exact_pairs = 0;
  for (std::uint64_t raw_a = 0; raw_a < 8; ++raw_a) {
    if ((raw_a & 1U) != 0) continue;
    const Bits83 a_mask{raw_a, 0};
    for (std::uint64_t raw_b = 0; raw_b < 8; ++raw_b) {
      if (std::popcount(raw_b) != 1) continue;
      const Bits83 b_mask{raw_b, 0};
      const bool brute = brute_pair_has_exact(a_mask, b_mask, 3, 3, small);
      const Evaluation reduced = evaluate_pair(a_mask, b_mask, 3, 3, 256, small);
      const bool found = reduced.outcome == Outcome::exact;
      if (brute) ++brute_exact_pairs;
      if (found) ++reducer_exact_pairs;
      if (brute != found)
        throw std::runtime_error("order-7 reducer disagrees with brute force");
    }
  }
  if (brute_exact_pairs == 0 || brute_exact_pairs != reducer_exact_pairs)
    throw std::runtime_error("order-7 exact fixture count mismatch");

  SplitMix64 first(668);
  const std::array<std::uint64_t, 4> expected{{
      0xc33416aae473d238ULL,
      0x3b8136e0ff77e131ULL,
      0x60589b6ae8406f3fULL,
      0x58edd5f5ed8cb9c0ULL,
  }};
  for (std::uint64_t value : expected)
    if (first.next() != value)
      throw std::runtime_error("SplitMix64 reproducibility fixture failed");

  const Instance production(ORDER);
  SplitMix64 cross_rng(0x668167ULL);
  for (int trial = 0; trial < 16; ++trial) {
    const Bits83 a_mask = random_a_mask(cross_rng, production);
    const Bits83 b_mask = random_mask_with_weight(cross_rng, MAX_HALF, 38);
    const Sequence a = skew_from_mask(a_mask, production);
    const Sequence b = symmetric_from_mask(b_mask, production);
    const Sequence s = derive_s(a, b, production);
    const Bits83 s_mask = half_negative_mask(s, production);
    if (s_mask.count() % 2 != 1)
      throw std::runtime_error("derived S should have odd half-weight");
    if (derive_a_from_s_b(s, b, production) != a)
      throw std::runtime_error("S,B parameterization did not recover A");
    const Bits83 canonical =
        canonicalize_doubling_necklace(s_mask, production);
    if (canonical.count() != s_mask.count() ||
        canonicalize_doubling_necklace(canonical, production) != canonical)
      throw std::runtime_error("doubling necklace is not idempotent");
    const CoefficientMatrix matrix = build_coefficient_matrix(s, production);
    const MatrixFactorization factor = factor_matrix(matrix);
    const Evaluation original =
        evaluate_pair(a_mask, b_mask, -1, -21, 4096, production);
    const Evaluation factored = evaluate_factored_pair(
        a, b, matrix, factor, -1, -21, 4096, production);
    if (original.outcome != factored.outcome ||
        original.early_reason != factored.early_reason ||
        original.early_lag != factored.early_lag ||
        original.rank != factored.rank ||
        original.nullity != factored.nullity ||
        original.weight_survivors != factored.weight_survivors ||
        original.energy != factored.energy ||
        original.c_mask != factored.c_mask ||
        original.d_mask != factored.d_mask)
      throw std::runtime_error("factored reducer differs from direct reducer");
  }

  std::cout << "PASS: exhaustive order-7 reducer/brute-force equivalence ("
            << brute_exact_pairs << " exact A,B pairs)\n";
  std::cout << "PASS: SplitMix64 deterministic fixture\n";
  std::cout << "PASS: 16 direct/factored order-167 reducer fixtures\n";
}

struct Options {
  int profile = 0;
  std::string parameterization = "ab";
  std::uint64_t inner_batch = 256;
  int s_weight = -1;
  std::uint64_t trials = 1'000'000;
  double seconds = 60.0;
  std::uint64_t random_seed = 668;
  std::uint64_t max_affine_candidates = 4096;
  double report_every = 10.0;
  std::filesystem::path output = "output/good_167_stream_candidate.json";
  std::filesystem::path checkpoint = "output/good_167_stream_best.json";
  bool self_test = false;
};

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string_view argument(argv[index]);
    auto value = [&]() -> std::string_view {
      if (++index >= argc)
        throw std::runtime_error("missing value after " + std::string(argument));
      return argv[index];
    };
    if (argument == "--profile")
      options.profile = std::stoi(std::string(value()));
    else if (argument == "--parameterization")
      options.parameterization = value();
    else if (argument == "--inner-batch")
      options.inner_batch = std::stoull(std::string(value()));
    else if (argument == "--s-weight")
      options.s_weight = std::stoi(std::string(value()));
    else if (argument == "--trials")
      options.trials = std::stoull(std::string(value()));
    else if (argument == "--seconds")
      options.seconds = std::stod(std::string(value()));
    else if (argument == "--random-seed")
      options.random_seed = std::stoull(std::string(value()));
    else if (argument == "--max-affine-candidates")
      options.max_affine_candidates = std::stoull(std::string(value()));
    else if (argument == "--report-every")
      options.report_every = std::stod(std::string(value()));
    else if (argument == "--output")
      options.output = value();
    else if (argument == "--checkpoint")
      options.checkpoint = value();
    else if (argument == "--self-test")
      options.self_test = true;
    else
      throw std::runtime_error("unknown option: " + std::string(argument));
  }
  if (options.profile < 0 || options.profile > 1)
    throw std::runtime_error("profile must be 0 or 1");
  if (options.parameterization != "ab" && options.parameterization != "sb")
    throw std::runtime_error("parameterization must be ab or sb");
  if (options.inner_batch == 0)
    throw std::runtime_error("inner batch must be positive");
  if (options.trials == 0 && options.seconds <= 0)
    throw std::runtime_error("trials and seconds cannot both be disabled");
  if (options.seconds < 0 || options.report_every <= 0 ||
      options.max_affine_candidates == 0)
    throw std::runtime_error("time and affine limits must be positive");
  return options;
}

void mix_checksum(std::uint64_t &checksum, std::uint64_t value) {
  checksum ^= value;
  checksum *= 0x100000001b3ULL;
}

void print_summary(std::uint64_t completed,
                   const std::array<std::uint64_t, OUTCOME_COUNT> &counters,
                   const std::array<std::uint64_t, MAX_HALF + 1> &ranks,
                   std::uint64_t checksum, double elapsed) {
  std::cout << "trials=" << completed << " elapsed=" << std::fixed
            << std::setprecision(3) << elapsed << " rate="
            << (elapsed > 0 ? completed / elapsed : 0.0) << '\n';
  std::cout << "outcomes={";
  bool first = true;
  for (int raw = 0; raw < OUTCOME_COUNT; ++raw) {
    if (counters[raw] == 0) continue;
    if (!first) std::cout << ',';
    first = false;
    std::cout << outcome_name(static_cast<Outcome>(raw)) << ':' << counters[raw];
  }
  std::cout << "}\nrank_histogram={";
  first = true;
  for (int rank = 0; rank <= MAX_HALF; ++rank) {
    if (ranks[rank] == 0) continue;
    if (!first) std::cout << ',';
    first = false;
    std::cout << rank << ':' << ranks[rank];
  }
  std::cout << "}\nchecksum=0x" << std::hex << checksum << std::dec << '\n';
}

int run_ab(const Options &options) {
  const Instance instance(ORDER);
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const int c_sum = c_sums[options.profile];
  const int d_sum = d_sums[options.profile];
  const int b_weight = (ORDER - 15) / 4;
  SplitMix64 rng(options.random_seed);
  std::array<std::uint64_t, OUTCOME_COUNT> counters{};
  std::array<std::uint64_t, MAX_HALF + 1> ranks{};
  std::uint64_t checksum = 0xcbf29ce484222325ULL;
  std::uint64_t completed = 0;
  std::int64_t best_energy = std::numeric_limits<std::int64_t>::max();
  const auto start = std::chrono::steady_clock::now();
  auto next_report = start + std::chrono::duration<double>(options.report_every);

  std::cout << "order=167 profile=" << options.profile
            << " row_sums=(15," << c_sum << ',' << d_sum << ")\n"
            << "seed=" << options.random_seed << " max_affine_candidates="
            << options.max_affine_candidates << " workers=1\n";

  while (options.trials == 0 || completed < options.trials) {
    const auto now = std::chrono::steady_clock::now();
    const double elapsed = std::chrono::duration<double>(now - start).count();
    if (options.seconds > 0 && elapsed >= options.seconds) break;

    const std::uint64_t trial_rng_state = rng.state;
    const Bits83 a_mask = random_a_mask(rng, instance);
    const Bits83 b_mask =
        random_mask_with_weight(rng, instance.half, b_weight);
    const Evaluation evaluation = evaluate_pair(
        a_mask, b_mask, c_sum, d_sum, options.max_affine_candidates, instance);
    ++completed;
    ++counters[outcome_index(evaluation.outcome)];
    if (evaluation.early_reason == EarlyReason::none && evaluation.rank >= 0 &&
        evaluation.rank <= MAX_HALF)
      ++ranks[evaluation.rank];
    mix_checksum(checksum, a_mask.low);
    mix_checksum(checksum, a_mask.high);
    mix_checksum(checksum, b_mask.low);
    mix_checksum(checksum, b_mask.high);
    mix_checksum(checksum, static_cast<std::uint64_t>(evaluation.outcome));
    mix_checksum(checksum, static_cast<std::uint64_t>(evaluation.rank));
    if (evaluation.outcome == Outcome::exact_paf_rejection &&
        evaluation.energy < best_energy) {
      best_energy = evaluation.energy;
      const Bits83 s_mask = half_negative_mask(
          derive_s(skew_from_mask(a_mask, instance),
                   symmetric_from_mask(b_mask, instance), instance),
          instance);
      write_checkpoint(options.checkpoint, a_mask, b_mask, evaluation,
                       options.profile, c_sum, d_sum, completed - 1,
                       options.random_seed, trial_rng_state, rng.state,
                       "ab", s_mask, instance);
      std::cout << "best trial=" << completed - 1
                << " energy=" << evaluation.energy
                << " bad_lags=" << evaluation.bad_lags
                << " max_abs_quarter=" << evaluation.max_abs_quarter << '\n';
    }
    if (evaluation.outcome == Outcome::exact) {
      const Bits83 s_mask = half_negative_mask(
          derive_s(skew_from_mask(a_mask, instance),
                   symmetric_from_mask(b_mask, instance), instance),
          instance);
      write_exact_candidate(options.output, a_mask, b_mask, evaluation,
                            options.profile, c_sum, d_sum, completed - 1,
                            options.random_seed, "ab", s_mask, instance);
      std::cout << "FOUND trial=" << completed - 1
                << " output=" << options.output << '\n';
      return 0;
    }
    if (std::chrono::steady_clock::now() >= next_report) {
      const double report_elapsed = std::chrono::duration<double>(
                                        std::chrono::steady_clock::now() - start)
                                        .count();
      print_summary(completed, counters, ranks, checksum, report_elapsed);
      next_report = std::chrono::steady_clock::now() +
                    std::chrono::duration<double>(options.report_every);
    }
  }
  const double elapsed =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
          .count();
  print_summary(completed, counters, ranks, checksum, elapsed);
  std::cout << "best_energy=";
  if (best_energy == std::numeric_limits<std::int64_t>::max())
    std::cout << "none\n";
  else
    std::cout << best_energy << '\n';
  std::cout << "FOUND=0\n";
  return 0;
}

int run_sb(const Options &options) {
  const Instance instance(ORDER);
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const std::array<int, 2> minimum_s_weights{{5, 7}};
  const std::array<int, 2> maximum_s_weights{{77, 81}};
  const int c_sum = c_sums[options.profile];
  const int d_sum = d_sums[options.profile];
  const int minimum_s_weight = minimum_s_weights[options.profile];
  const int maximum_s_weight = maximum_s_weights[options.profile];
  if (options.s_weight != -1 &&
      (options.s_weight < minimum_s_weight ||
       options.s_weight > maximum_s_weight || options.s_weight % 2 == 0))
    throw std::runtime_error("fixed S weight is infeasible for this profile");
  const int s_weight_count =
      (maximum_s_weight - minimum_s_weight) / 2 + 1;
  const int b_weight = (ORDER - 15) / 4;
  SplitMix64 rng(options.random_seed);
  std::array<std::uint64_t, OUTCOME_COUNT> counters{};
  std::array<std::uint64_t, MAX_HALF + 1> ranks{};
  std::uint64_t checksum = 0xcbf29ce484222325ULL;
  std::uint64_t completed = 0;
  std::uint64_t factorizations = 0;
  std::int64_t best_energy = std::numeric_limits<std::int64_t>::max();
  const auto start = std::chrono::steady_clock::now();
  auto next_report = start + std::chrono::duration<double>(options.report_every);

  std::cout << "order=167 profile=" << options.profile
            << " row_sums=(15," << c_sum << ',' << d_sum << ")\n"
            << "parameterization=sb inner_batch=" << options.inner_batch
            << " s_weight=";
  if (options.s_weight < 0)
    std::cout << "mixed";
  else
    std::cout << options.s_weight;
  std::cout << " seed=" << options.random_seed
            << " max_affine_candidates=" << options.max_affine_candidates
            << " workers=1\n";

  bool stop = false;
  while (!stop && (options.trials == 0 || completed < options.trials)) {
    const double outer_elapsed = std::chrono::duration<double>(
                                     std::chrono::steady_clock::now() - start)
                                     .count();
    if (options.seconds > 0 && outer_elapsed >= options.seconds) break;
    const int s_weight =
        options.s_weight >= 0
            ? options.s_weight
            : minimum_s_weight +
                  2 * static_cast<int>(rng.bounded(s_weight_count));
    const Bits83 raw_s_mask =
        random_mask_with_weight(rng, instance.half, s_weight);
    const Bits83 s_mask =
        canonicalize_doubling_necklace(raw_s_mask, instance);
    if (s_mask.count() != s_weight || s_weight % 2 == 0)
      throw std::runtime_error("canonical S has the wrong weight or parity");
    const Sequence s = symmetric_from_mask(s_mask, instance);
    const CoefficientMatrix matrix = build_coefficient_matrix(s, instance);
    const MatrixFactorization factor = factor_matrix(matrix);
    ++factorizations;

    for (std::uint64_t inner = 0; inner < options.inner_batch; ++inner) {
      if (options.trials != 0 && completed >= options.trials) {
        stop = true;
        break;
      }
      const double elapsed = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - start)
                                 .count();
      if (options.seconds > 0 && elapsed >= options.seconds) {
        stop = true;
        break;
      }
      const std::uint64_t trial_rng_state = rng.state;
      const Bits83 b_mask =
          random_mask_with_weight(rng, instance.half, b_weight);
      const Sequence b = symmetric_from_mask(b_mask, instance);
      const Sequence a = derive_a_from_s_b(s, b, instance);
      if (derive_s(a, b, instance) != s)
        throw std::runtime_error("S,B parameterization failed round trip");
      const Bits83 a_mask = half_negative_mask(a, instance);
      const Evaluation evaluation = evaluate_factored_pair(
          a, b, matrix, factor, c_sum, d_sum,
          options.max_affine_candidates, instance);
      ++completed;
      ++counters[outcome_index(evaluation.outcome)];
      if (evaluation.early_reason == EarlyReason::none &&
          evaluation.rank >= 0 && evaluation.rank <= MAX_HALF)
        ++ranks[evaluation.rank];
      mix_checksum(checksum, s_mask.low);
      mix_checksum(checksum, s_mask.high);
      mix_checksum(checksum, a_mask.low);
      mix_checksum(checksum, a_mask.high);
      mix_checksum(checksum, b_mask.low);
      mix_checksum(checksum, b_mask.high);
      mix_checksum(checksum, static_cast<std::uint64_t>(evaluation.outcome));
      mix_checksum(checksum, static_cast<std::uint64_t>(evaluation.rank));
      if (evaluation.outcome == Outcome::exact_paf_rejection &&
          evaluation.energy < best_energy) {
        best_energy = evaluation.energy;
        write_checkpoint(options.checkpoint, a_mask, b_mask, evaluation,
                         options.profile, c_sum, d_sum, completed - 1,
                         options.random_seed, trial_rng_state, rng.state,
                         "sb", s_mask, instance);
        std::cout << "best trial=" << completed - 1
                  << " energy=" << evaluation.energy
                  << " bad_lags=" << evaluation.bad_lags
                  << " max_abs_quarter=" << evaluation.max_abs_quarter
                  << " s_weight=" << s_weight << '\n';
      }
      if (evaluation.outcome == Outcome::exact) {
        write_exact_candidate(options.output, a_mask, b_mask, evaluation,
                              options.profile, c_sum, d_sum, completed - 1,
                              options.random_seed, "sb", s_mask, instance);
        std::cout << "FOUND trial=" << completed - 1
                  << " output=" << options.output << '\n';
        return 0;
      }
      if (std::chrono::steady_clock::now() >= next_report) {
        const double report_elapsed = std::chrono::duration<double>(
                                          std::chrono::steady_clock::now() -
                                          start)
                                          .count();
        print_summary(completed, counters, ranks, checksum, report_elapsed);
        std::cout << "factorizations=" << factorizations << '\n';
        next_report = std::chrono::steady_clock::now() +
                      std::chrono::duration<double>(options.report_every);
      }
    }
  }
  const double elapsed =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
          .count();
  print_summary(completed, counters, ranks, checksum, elapsed);
  std::cout << "factorizations=" << factorizations << " best_energy=";
  if (best_energy == std::numeric_limits<std::int64_t>::max())
    std::cout << "none\n";
  else
    std::cout << best_energy << '\n';
  std::cout << "FOUND=0\n";
  return 0;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    if (options.self_test) {
      self_test();
      return 0;
    }
    return options.parameterization == "ab" ? run_ab(options) : run_sb(options);
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
