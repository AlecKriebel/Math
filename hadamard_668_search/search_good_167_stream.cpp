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
#include <optional>
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

struct LocalState {
  Bits83 s_mask{};
  Bits83 a_mask{};
  Bits83 b_mask{};
  Bits83 c_mask{};
  Bits83 d_mask{};
  Evaluation metrics{};
};

struct LocalMoveCounts {
  std::array<std::uint64_t, 6> by_kind{};
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

Bits83 random_subset(SplitMix64 &rng, const Bits83 &allowed, int variables,
                     int count) {
  std::array<int, MAX_HALF> indices{};
  int available = 0;
  for (int index = 0; index < variables; ++index)
    if (allowed.test(index)) indices[available++] = index;
  if (count < 0 || count > available)
    throw std::runtime_error("requested subset size is infeasible");
  Bits83 result;
  for (int index = 0; index < count; ++index) {
    const int chosen =
        index + static_cast<int>(rng.bounded(available - index));
    std::swap(indices[index], indices[chosen]);
    result.set(indices[index]);
  }
  return result;
}

LocalState make_local_state(const Bits83 &s_mask, const Bits83 &b_mask,
                            const Bits83 &c_mask, int c_sum, int d_sum,
                            const Instance &instance) {
  const int expected_c_weight = (instance.n - c_sum) / 4;
  const int expected_d_weight = (instance.n - d_sum) / 4;
  const Bits83 d_mask = c_mask ^ s_mask;
  if (b_mask.count() != 38 || c_mask.count() != expected_c_weight ||
      d_mask.count() != expected_d_weight)
    throw std::runtime_error("local state has an incorrect half-weight");
  const Sequence s = symmetric_from_mask(s_mask, instance);
  const Sequence b = symmetric_from_mask(b_mask, instance);
  const Sequence a = derive_a_from_s_b(s, b, instance);
  if (derive_s(a, b, instance) != s)
    throw std::runtime_error("local state failed the product-quotient round trip");
  const Sequence c = symmetric_from_mask(c_mask, instance);
  const Sequence d = symmetric_from_mask(d_mask, instance);
  LocalState state;
  state.s_mask = s_mask;
  state.a_mask = half_negative_mask(a, instance);
  state.b_mask = b_mask;
  state.c_mask = c_mask;
  state.d_mask = d_mask;
  correlation_metrics(a, b, c, d, instance, state.metrics);
  state.metrics.c_mask = c_mask;
  state.metrics.d_mask = d_mask;
  state.metrics.outcome = state.metrics.energy == 0
                              ? Outcome::exact
                              : Outcome::exact_paf_rejection;
  if (state.metrics.energy == 0 &&
      !exact_full_validation(a, b, c, d, 15, c_sum, d_sum, instance))
    throw std::runtime_error("zero-energy local state failed full validation");
  return state;
}

LocalState random_local_state(SplitMix64 &rng, int profile, int s_weight,
                              const Instance &instance) {
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const int c_sum = c_sums[profile];
  const int d_sum = d_sums[profile];
  const int c_weight = (instance.n - c_sum) / 4;
  const int d_weight = (instance.n - d_sum) / 4;
  const Bits83 b_mask = random_mask_with_weight(rng, instance.half, 38);
  if (s_weight < 0) {
    const Bits83 c_mask =
        random_mask_with_weight(rng, instance.half, c_weight);
    const Bits83 d_mask =
        random_mask_with_weight(rng, instance.half, d_weight);
    return make_local_state(c_mask ^ d_mask, b_mask, c_mask, c_sum, d_sum,
                            instance);
  }
  const Bits83 s_mask = canonicalize_doubling_necklace(
      random_mask_with_weight(rng, instance.half, s_weight), instance);
  const int intersection_numerator = c_weight + s_weight - d_weight;
  if (intersection_numerator % 2 != 0)
    throw std::runtime_error("local C/S intersection is nonintegral");
  const int inside_count = intersection_numerator / 2;
  Bits83 all;
  for (int index = 0; index < instance.half; ++index) all.set(index);
  const Bits83 outside = all ^ s_mask;
  const Bits83 c_mask = random_subset(rng, s_mask, instance.half, inside_count) ^
                        random_subset(rng, outside, instance.half,
                                      c_weight - inside_count);
  return make_local_state(s_mask, b_mask, c_mask, c_sum, d_sum, instance);
}

Bits83 exchange_one_bit(SplitMix64 &rng, const Bits83 &mask,
                        const Bits83 &allowed, int variables) {
  std::array<int, MAX_HALF> ones{};
  std::array<int, MAX_HALF> zeros{};
  int one_count = 0;
  int zero_count = 0;
  for (int index = 0; index < variables; ++index) {
    if (!allowed.test(index)) continue;
    if (mask.test(index))
      ones[one_count++] = index;
    else
      zeros[zero_count++] = index;
  }
  if (one_count == 0 || zero_count == 0)
    throw std::runtime_error("exchange domain has only one bit value");
  Bits83 result = mask;
  result.toggle(ones[rng.bounded(one_count)]);
  result.toggle(zeros[rng.bounded(zero_count)]);
  return result;
}

Bits83 coupled_exchange_toggle(SplitMix64 &rng, const Bits83 &left,
                               const Bits83 &right, int variables) {
  for (int attempt = 0; attempt < 256; ++attempt) {
    const int first = static_cast<int>(rng.bounded(variables));
    int second = static_cast<int>(rng.bounded(variables - 1));
    if (second >= first) ++second;
    if (left.test(first) != left.test(second) &&
        right.test(first) != right.test(second)) {
      Bits83 toggle;
      toggle.set(first);
      toggle.set(second);
      return toggle;
    }
  }
  for (int first = 0; first < variables; ++first) {
    for (int second = first + 1; second < variables; ++second) {
      if (left.test(first) != left.test(second) &&
          right.test(first) != right.test(second)) {
        Bits83 toggle;
        toggle.set(first);
        toggle.set(second);
        return toggle;
      }
    }
  }
  throw std::runtime_error("coupled exchange has no feasible endpoint pair");
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

std::string json_field_value(const std::string &document,
                             std::string_view field, bool quoted) {
  const std::string needle = "\"" + std::string(field) + "\"";
  const std::size_t key = document.find(needle);
  if (key == std::string::npos)
    throw std::runtime_error("missing JSON field: " + std::string(field));
  const std::size_t colon = document.find(':', key + needle.size());
  if (colon == std::string::npos)
    throw std::runtime_error("malformed JSON field: " + std::string(field));
  if (quoted) {
    const std::size_t begin = document.find('"', colon + 1);
    const std::size_t end =
        begin == std::string::npos ? begin : document.find('"', begin + 1);
    if (begin == std::string::npos || end == std::string::npos)
      throw std::runtime_error("malformed quoted JSON field: " +
                               std::string(field));
    return document.substr(begin + 1, end - begin - 1);
  }
  const std::size_t begin = document.find_first_of("-0123456789", colon + 1);
  if (begin == std::string::npos)
    throw std::runtime_error("malformed integer JSON field: " +
                             std::string(field));
  const std::size_t end = document.find_first_not_of("0123456789", begin + 1);
  return document.substr(begin, end - begin);
}

Bits83 parse_mask_hex(std::string_view encoded) {
  if (!encoded.starts_with("0x"))
    throw std::runtime_error("mask must begin with 0x");
  const std::string digits(encoded.substr(2));
  if (digits.empty() || digits.size() > 21)
    throw std::runtime_error("mask hexadecimal width is invalid");
  const std::size_t split = digits.size() > 16 ? digits.size() - 16 : 0;
  std::size_t consumed = 0;
  Bits83 result;
  if (split != 0) {
    result.high = std::stoull(digits.substr(0, split), &consumed, 16);
    if (consumed != split)
      throw std::runtime_error("mask high limb is not hexadecimal");
  }
  consumed = 0;
  result.low = std::stoull(digits.substr(split), &consumed, 16);
  if (consumed != digits.size() - split)
    throw std::runtime_error("mask low limb is not hexadecimal");
  const Bits83 original = result;
  result.trim(MAX_HALF);
  if (result != original)
    throw std::runtime_error("mask has bits above position 82");
  return result;
}

LocalState load_local_state(const std::filesystem::path &path, int profile,
                            const Instance &instance) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("could not open initial checkpoint");
  std::ostringstream buffer;
  buffer << input.rdbuf();
  if (!input.good() && !input.eof())
    throw std::runtime_error("could not read initial checkpoint");
  const std::string document = buffer.str();
  if (std::stoi(json_field_value(document, "order", false)) != ORDER ||
      std::stoi(json_field_value(document, "profile", false)) != profile)
    throw std::runtime_error("initial checkpoint order/profile mismatch");
  const Bits83 s_mask =
      parse_mask_hex(json_field_value(document, "s_mask", true));
  const Bits83 a_mask =
      parse_mask_hex(json_field_value(document, "a_mask", true));
  const Bits83 b_mask =
      parse_mask_hex(json_field_value(document, "b_mask", true));
  const Bits83 c_mask =
      parse_mask_hex(json_field_value(document, "c_mask", true));
  const Bits83 d_mask =
      parse_mask_hex(json_field_value(document, "d_mask", true));
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const LocalState state = make_local_state(
      s_mask, b_mask, c_mask, c_sums[profile], d_sums[profile], instance);
  if (state.a_mask != a_mask || state.d_mask != d_mask)
    throw std::runtime_error("initial checkpoint masks are inconsistent");
  if (state.metrics.energy !=
      std::stoll(json_field_value(document, "energy", false)))
    throw std::runtime_error("initial checkpoint energy is incorrect");
  return state;
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

void write_local_checkpoint(const std::filesystem::path &path,
                            const LocalState &state, int profile,
                            int c_sum, int d_sum, std::uint64_t move,
                            std::uint64_t seed, std::uint64_t rng_state,
                            const Instance &instance) {
  write_atomically(path, [&](std::ostream &output) {
    output << "{\n  \"schema\": "
              "\"hadamard668.good167-local-checkpoint.v1\",\n"
           << "  \"kind\": \"good_matrix_local_checkpoint\",\n"
           << "  \"status\": \"near_miss\",\n"
           << "  \"exact\": false,\n"
           << "  \"order\": " << instance.n << ",\n"
           << "  \"hadamard_order\": " << 4 * instance.n << ",\n"
           << "  \"profile\": " << profile << ",\n"
           << "  \"parameterization\": \"local_sbc\",\n"
           << "  \"row_sums\": [15," << c_sum << ',' << d_sum << "],\n"
           << "  \"move\": " << move << ",\n"
           << "  \"random_seed\": " << seed << ",\n"
           << "  \"rng_state\": \"0x" << std::hex << rng_state << std::dec
           << "\",\n"
           << "  \"energy\": " << state.metrics.energy << ",\n"
           << "  \"bad_lags\": " << state.metrics.bad_lags << ",\n"
           << "  \"max_abs_quarter\": "
           << state.metrics.max_abs_quarter << ",\n"
           << "  \"s_mask\": \"" << mask_hex(state.s_mask) << "\",\n"
           << "  \"a_mask\": \"" << mask_hex(state.a_mask) << "\",\n"
           << "  \"b_mask\": \"" << mask_hex(state.b_mask) << "\",\n"
           << "  \"c_mask\": \"" << mask_hex(state.c_mask) << "\",\n"
           << "  \"d_mask\": \"" << mask_hex(state.d_mask) << "\",\n"
           << "  \"quarter_residuals\": [";
    for (int lag = 1; lag <= instance.half; ++lag) {
      if (lag != 1) output << ',';
      output << state.metrics.residual[lag] / 4;
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

  Bits83 all;
  for (int index = 0; index < production.half; ++index) all.set(index);
  LocalState walk = random_local_state(cross_rng, 0, -1, production);
  for (int move = 0; move < 96; ++move) {
    if (move % 3 == 0) {
      const Bits83 b_mask = exchange_one_bit(
          cross_rng, walk.b_mask, all, production.half);
      walk = make_local_state(walk.s_mask, b_mask, walk.c_mask, -1, -21,
                              production);
    } else if (move % 3 == 1) {
      const Bits83 c_mask = exchange_one_bit(
          cross_rng, walk.c_mask, all, production.half);
      walk = make_local_state(c_mask ^ walk.d_mask, walk.b_mask, c_mask, -1,
                              -21, production);
    } else {
      const Bits83 d_mask = exchange_one_bit(
          cross_rng, walk.d_mask, all, production.half);
      walk = make_local_state(walk.c_mask ^ d_mask, walk.b_mask, walk.c_mask,
                              -1, -21, production);
      if (walk.d_mask != d_mask)
        throw std::runtime_error("local D walk lost its proposed mask");
    }
    if (walk.s_mask != (walk.c_mask ^ walk.d_mask) ||
        walk.b_mask.count() != 38 || walk.c_mask.count() != 42 ||
        walk.d_mask.count() != 47 || walk.s_mask.count() % 2 != 1 ||
        walk.metrics.energy % 2 != 0)
      throw std::runtime_error("structured local walk broke an invariant");
  }
  for (int move = 0; move < 96; ++move) {
    const Bits83 old_a = walk.a_mask;
    if (move % 3 == 0) {
      const Bits83 toggle = coupled_exchange_toggle(
          cross_rng, walk.b_mask, walk.c_mask, production.half);
      const Bits83 b_mask = walk.b_mask ^ toggle;
      const Bits83 c_mask = walk.c_mask ^ toggle;
      walk = make_local_state(c_mask ^ walk.d_mask, b_mask, c_mask, -1, -21,
                              production);
    } else if (move % 3 == 1) {
      const Bits83 toggle = coupled_exchange_toggle(
          cross_rng, walk.b_mask, walk.d_mask, production.half);
      const Bits83 b_mask = walk.b_mask ^ toggle;
      const Bits83 d_mask = walk.d_mask ^ toggle;
      walk = make_local_state(walk.c_mask ^ d_mask, b_mask, walk.c_mask, -1,
                              -21, production);
      if (walk.d_mask != d_mask)
        throw std::runtime_error("coupled BD walk lost D");
    } else {
      const Bits83 toggle = coupled_exchange_toggle(
          cross_rng, walk.c_mask, walk.d_mask, production.half);
      const Bits83 c_mask = walk.c_mask ^ toggle;
      const Bits83 d_mask = walk.d_mask ^ toggle;
      walk = make_local_state(c_mask ^ d_mask, walk.b_mask, c_mask, -1, -21,
                              production);
      if (walk.d_mask != d_mask)
        throw std::runtime_error("coupled CD walk lost D");
    }
    if (walk.a_mask != old_a || walk.b_mask.count() != 38 ||
        walk.c_mask.count() != 42 || walk.d_mask.count() != 47 ||
        walk.s_mask != (walk.c_mask ^ walk.d_mask))
      throw std::runtime_error("A-invariant coupled walk broke an invariant");
  }

  std::cout << "PASS: exhaustive order-7 reducer/brute-force equivalence ("
            << brute_exact_pairs << " exact A,B pairs)\n";
  std::cout << "PASS: SplitMix64 deterministic fixture\n";
  std::cout << "PASS: 16 direct/factored order-167 reducer fixtures\n";
  std::cout << "PASS: 96 atomic and 96 coupled structured local moves\n";
}

struct Options {
  int profile = 0;
  std::string parameterization = "ab";
  std::uint64_t inner_batch = 256;
  int s_weight = -1;
  std::uint64_t moves_per_restart = 100'000;
  double start_temperature = 512.0;
  double end_temperature = 0.25;
  double b_move_probability = 0.25;
  double coupled_move_probability = 0.5;
  std::filesystem::path initial;
  bool restart_from_best = false;
  bool steepest_polish = false;
  bool gf_steepest_polish = false;
  std::int64_t shadow_weight = 0;
  double compound_probability = 0.0;
  int compound_arity = 2;
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
    else if (argument == "--moves-per-restart")
      options.moves_per_restart = std::stoull(std::string(value()));
    else if (argument == "--start-temperature")
      options.start_temperature = std::stod(std::string(value()));
    else if (argument == "--end-temperature")
      options.end_temperature = std::stod(std::string(value()));
    else if (argument == "--b-move-probability")
      options.b_move_probability = std::stod(std::string(value()));
    else if (argument == "--coupled-move-probability")
      options.coupled_move_probability = std::stod(std::string(value()));
    else if (argument == "--initial")
      options.initial = value();
    else if (argument == "--restart-from-best")
      options.restart_from_best = true;
    else if (argument == "--steepest-polish")
      options.steepest_polish = true;
    else if (argument == "--gf-steepest-polish")
      options.gf_steepest_polish = true;
    else if (argument == "--shadow-weight")
      options.shadow_weight = std::stoll(std::string(value()));
    else if (argument == "--compound-probability")
      options.compound_probability = std::stod(std::string(value()));
    else if (argument == "--compound-arity")
      options.compound_arity = std::stoi(std::string(value()));
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
  if (options.parameterization != "ab" && options.parameterization != "sb" &&
      options.parameterization != "local")
    throw std::runtime_error("parameterization must be ab, sb, or local");
  if (options.inner_batch == 0)
    throw std::runtime_error("inner batch must be positive");
  if (options.moves_per_restart == 0 || options.start_temperature <= 0 ||
      options.end_temperature <= 0 ||
      options.end_temperature > options.start_temperature)
    throw std::runtime_error("local-search parameters are invalid");
  if (options.parameterization == "local" &&
      (options.b_move_probability <= 0 ||
       options.b_move_probability >= 1 ||
       options.coupled_move_probability < 0 ||
       options.coupled_move_probability >= 1))
    throw std::runtime_error(
        "local move probabilities do not retain every atomic move type");
  if (options.shadow_weight < 0)
    throw std::runtime_error("shadow weight must be nonnegative");
  if (options.compound_probability < 0 ||
      options.compound_probability >= 1 || options.compound_arity < 2)
    throw std::runtime_error("compound move parameters are invalid");
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

int run_gf_steepest(const Options &options);

int run_sb(const Options &options) {
  if (options.gf_steepest_polish) return run_gf_steepest(options);
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

std::optional<LocalState> recover_gf_state(
    const Bits83 &s_mask, const Bits83 &b_mask, int c_sum, int d_sum,
    std::uint64_t max_affine_candidates, const Instance &instance) {
  if (s_mask.count() % 2 != 1 || b_mask.count() != 38) return std::nullopt;
  const Sequence s = symmetric_from_mask(s_mask, instance);
  const Sequence b = symmetric_from_mask(b_mask, instance);
  const Sequence a = derive_a_from_s_b(s, b, instance);
  const CoefficientMatrix matrix = build_coefficient_matrix(s, instance);
  const MatrixFactorization factor = factor_matrix(matrix);
  const Evaluation evaluation = evaluate_factored_pair(
      a, b, matrix, factor, c_sum, d_sum, max_affine_candidates, instance);
  if (evaluation.outcome != Outcome::exact_paf_rejection &&
      evaluation.outcome != Outcome::exact)
    return std::nullopt;
  const LocalState state = make_local_state(
      s_mask, b_mask, evaluation.c_mask, c_sum, d_sum, instance);
  if (state.metrics.energy != evaluation.energy ||
      state.d_mask != evaluation.d_mask)
    throw std::runtime_error("GF recovery and local state disagree");
  return state;
}

int run_gf_steepest(const Options &options) {
  if (options.initial.empty())
    throw std::runtime_error("GF steepest polish requires --initial");
  const Instance instance(ORDER);
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const std::array<int, 2> minimum_s_weights{{5, 7}};
  const std::array<int, 2> maximum_s_weights{{77, 81}};
  const int c_sum = c_sums[options.profile];
  const int d_sum = d_sums[options.profile];
  const LocalState loaded =
      load_local_state(options.initial, options.profile, instance);
  const std::optional<LocalState> recovered = recover_gf_state(
      loaded.s_mask, loaded.b_mask, c_sum, d_sum,
      options.max_affine_candidates, instance);
  if (!recovered || recovered->metrics.energy != loaded.metrics.energy)
    throw std::runtime_error("initial state is not the recovered GF survivor");
  LocalState current = *recovered;
  LocalState best = current;
  std::uint64_t evaluations = 0;
  std::uint64_t survivors = 1;
  std::uint64_t rounds = 0;
  bool complete_neighborhood = false;
  const auto start = std::chrono::steady_clock::now();
  auto next_report = start + std::chrono::duration<double>(options.report_every);
  SplitMix64 metadata_rng(options.random_seed);

  auto record = [&]() {
    write_local_checkpoint(options.checkpoint, best, options.profile, c_sum,
                           d_sum, evaluations, options.random_seed,
                           metadata_rng.state, instance);
    std::cout << "best evaluation=" << evaluations
              << " energy=" << best.metrics.energy
              << " bad_lags=" << best.metrics.bad_lags
              << " max_abs_quarter=" << best.metrics.max_abs_quarter
              << " s_weight=" << best.s_mask.count() << '\n';
  };
  auto exact = [&](const LocalState &candidate) {
    if (candidate.metrics.energy != 0) return false;
    write_exact_candidate(options.output, candidate.a_mask, candidate.b_mask,
                          candidate.metrics, options.profile, c_sum, d_sum,
                          evaluations, options.random_seed, "sb_gf_steepest",
                          candidate.s_mask, instance);
    std::cout << "FOUND evaluation=" << evaluations
              << " output=" << options.output << '\n';
    return true;
  };

  std::cout << "order=167 profile=" << options.profile
            << " parameterization=sb gf_steepest_polish=1 seed="
            << options.random_seed << " workers=1\n";
  if (exact(best)) return 0;
  record();
  bool stopped = false;
  while (!stopped) {
    LocalState round_best = current;
    complete_neighborhood = true;
    for (int family = 0; family < 2 && !stopped; ++family) {
      for (int first = 0; first < instance.half && !stopped; ++first) {
        for (int second = first + 1; second < instance.half; ++second) {
          if (family == 0 &&
              current.b_mask.test(first) == current.b_mask.test(second))
            continue;
          Bits83 toggle;
          toggle.set(first);
          toggle.set(second);
          const Bits83 s_mask =
              family == 0 ? current.s_mask : current.s_mask ^ toggle;
          const Bits83 b_mask =
              family == 0 ? current.b_mask ^ toggle : current.b_mask;
          const int s_weight = s_mask.count();
          if (s_weight < minimum_s_weights[options.profile] ||
              s_weight > maximum_s_weights[options.profile] ||
              s_weight % 2 != 1)
            continue;
          const double elapsed = std::chrono::duration<double>(
                                     std::chrono::steady_clock::now() - start)
                                     .count();
          if ((options.trials != 0 && evaluations >= options.trials) ||
              (options.seconds > 0 && elapsed >= options.seconds)) {
            complete_neighborhood = false;
            stopped = true;
            break;
          }
          ++evaluations;
          const std::optional<LocalState> candidate = recover_gf_state(
              s_mask, b_mask, c_sum, d_sum,
              options.max_affine_candidates, instance);
          if (candidate) {
            ++survivors;
            if (exact(*candidate)) return 0;
            if (candidate->metrics.energy < best.metrics.energy) {
              best = *candidate;
              record();
            }
            if (candidate->metrics.energy < round_best.metrics.energy)
              round_best = *candidate;
          }
          if (std::chrono::steady_clock::now() >= next_report) {
            const double report_elapsed = std::chrono::duration<double>(
                                              std::chrono::steady_clock::now() -
                                              start)
                                              .count();
            std::cout << "evaluations=" << evaluations
                      << " survivors=" << survivors << " elapsed="
                      << std::fixed << std::setprecision(3) << report_elapsed
                      << " rate=" << evaluations / report_elapsed
                      << " rounds=" << rounds
                      << " current_energy=" << current.metrics.energy
                      << " best_energy=" << best.metrics.energy << '\n';
            next_report = std::chrono::steady_clock::now() +
                          std::chrono::duration<double>(options.report_every);
          }
        }
      }
    }
    if (!complete_neighborhood) break;
    if (round_best.metrics.energy >= current.metrics.energy) {
      stopped = true;
      break;
    }
    current = round_best;
    ++rounds;
    std::cout << "descent_round=" << rounds
              << " energy=" << current.metrics.energy << '\n';
  }
  const double elapsed =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
          .count();
  std::cout << "evaluations=" << evaluations << " survivors=" << survivors
            << " elapsed=" << std::fixed << std::setprecision(3) << elapsed
            << " rate=" << (elapsed > 0 ? evaluations / elapsed : 0.0)
            << " descent_rounds=" << rounds
            << " complete_neighborhood=" << complete_neighborhood
            << " local_minimum="
            << (complete_neighborhood &&
                current.metrics.energy == best.metrics.energy)
            << " best_energy=" << best.metrics.energy << '\n'
            << "FOUND=0\n";
  return 0;
}

LocalState local_pair_move(const LocalState &current, const Bits83 &toggle,
                           int kind, int c_sum, int d_sum,
                           const Instance &instance) {
  if (toggle.count() != 2 || kind < 0 || kind >= 6)
    throw std::runtime_error("local pair move arguments are invalid");
  LocalState proposal;
  if (kind == 0) {
    proposal = make_local_state(current.s_mask, current.b_mask ^ toggle,
                                current.c_mask, c_sum, d_sum, instance);
  } else if (kind == 1) {
    const Bits83 c_mask = current.c_mask ^ toggle;
    proposal = make_local_state(c_mask ^ current.d_mask, current.b_mask,
                                c_mask, c_sum, d_sum, instance);
  } else if (kind == 2) {
    const Bits83 d_mask = current.d_mask ^ toggle;
    proposal = make_local_state(current.c_mask ^ d_mask, current.b_mask,
                                current.c_mask, c_sum, d_sum, instance);
    if (proposal.d_mask != d_mask)
      throw std::runtime_error("atomic D move lost D");
  } else if (kind == 3) {
    const Bits83 b_mask = current.b_mask ^ toggle;
    const Bits83 c_mask = current.c_mask ^ toggle;
    proposal = make_local_state(c_mask ^ current.d_mask, b_mask, c_mask,
                                c_sum, d_sum, instance);
  } else if (kind == 4) {
    const Bits83 b_mask = current.b_mask ^ toggle;
    const Bits83 d_mask = current.d_mask ^ toggle;
    proposal = make_local_state(current.c_mask ^ d_mask, b_mask,
                                current.c_mask, c_sum, d_sum, instance);
    if (proposal.d_mask != d_mask)
      throw std::runtime_error("coupled BD move lost D");
  } else {
    const Bits83 c_mask = current.c_mask ^ toggle;
    const Bits83 d_mask = current.d_mask ^ toggle;
    proposal = make_local_state(c_mask ^ d_mask, current.b_mask, c_mask,
                                c_sum, d_sum, instance);
    if (proposal.d_mask != d_mask)
      throw std::runtime_error("coupled CD move lost D");
  }
  if (kind >= 3 && proposal.a_mask != current.a_mask)
    throw std::runtime_error("coupled pair move unexpectedly changed A");
  return proposal;
}

double uniform_unit(SplitMix64 &rng);

LocalState random_local_pair_move(SplitMix64 &rng, const LocalState &current,
                                  double b_move_probability,
                                  double coupled_move_probability,
                                  int c_sum, int d_sum,
                                  const Instance &instance,
                                  LocalMoveCounts &counts) {
  int kind = 0;
  Bits83 toggle;
  const double choice = uniform_unit(rng);
  if (choice < coupled_move_probability) {
    kind = 3 + static_cast<int>(rng.bounded(3));
    if (kind == 3)
      toggle = coupled_exchange_toggle(rng, current.b_mask, current.c_mask,
                                       instance.half);
    else if (kind == 4)
      toggle = coupled_exchange_toggle(rng, current.b_mask, current.d_mask,
                                       instance.half);
    else
      toggle = coupled_exchange_toggle(rng, current.c_mask, current.d_mask,
                                       instance.half);
  } else {
    const double atomic_choice =
        (choice - coupled_move_probability) / (1.0 - coupled_move_probability);
    if (atomic_choice < b_move_probability)
      kind = 0;
    else if (atomic_choice <
             b_move_probability + (1.0 - b_move_probability) / 2.0)
      kind = 1;
    else
      kind = 2;
    Bits83 all;
    for (int index = 0; index < instance.half; ++index) all.set(index);
    const Bits83 &mask =
        kind == 0 ? current.b_mask
                  : (kind == 1 ? current.c_mask : current.d_mask);
    toggle = mask ^ exchange_one_bit(rng, mask, all, instance.half);
  }
  ++counts.by_kind[kind];
  return local_pair_move(current, toggle, kind, c_sum, d_sum, instance);
}

double uniform_unit(SplitMix64 &rng) {
  return static_cast<double>(rng.next() >> 11) *
         (1.0 / 9007199254740992.0);
}

std::int64_t shadow_penalty(const Evaluation &metrics) {
  std::int64_t result = 0;
  for (int lag = 1; lag <= MAX_HALF; ++lag) {
    const int quarter = metrics.residual[lag] / 4;
    const int residue = normalize(quarter, 4);
    const int distance = std::min(residue, 4 - residue);
    result += distance * distance;
  }
  return result;
}

std::int64_t local_score(const LocalState &state, std::int64_t shadow_weight) {
  const std::int64_t penalty = shadow_penalty(state.metrics);
  if (shadow_weight != 0 &&
      penalty > (std::numeric_limits<std::int64_t>::max() -
                 state.metrics.energy) /
                    shadow_weight)
    throw std::runtime_error("local objective overflow");
  return state.metrics.energy + shadow_weight * penalty;
}

int run_local_steepest(const Options &options) {
  const Instance instance(ORDER);
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const int c_sum = c_sums[options.profile];
  const int d_sum = d_sums[options.profile];
  SplitMix64 rng(options.random_seed);
  LocalState current = options.initial.empty()
                           ? random_local_state(rng, options.profile,
                                                options.s_weight, instance)
                           : load_local_state(options.initial, options.profile,
                                              instance);
  LocalState best = current;
  std::int64_t best_score = local_score(best, options.shadow_weight);
  std::uint64_t evaluations = 0;
  std::uint64_t rounds = 0;
  bool complete_neighborhood = false;
  const auto start = std::chrono::steady_clock::now();
  auto next_report = start + std::chrono::duration<double>(options.report_every);

  auto write_best = [&]() {
    write_local_checkpoint(options.checkpoint, best, options.profile, c_sum,
                           d_sum, evaluations, options.random_seed, rng.state,
                           instance);
    std::cout << "best evaluation=" << evaluations
              << " energy=" << best.metrics.energy
              << " bad_lags=" << best.metrics.bad_lags
              << " max_abs_quarter=" << best.metrics.max_abs_quarter
              << " shadow_penalty=" << shadow_penalty(best.metrics)
              << " score=" << best_score
              << " s_weight=" << best.s_mask.count() << '\n';
  };
  auto exact = [&](const LocalState &candidate) {
    if (candidate.metrics.energy != 0) return false;
    write_exact_candidate(options.output, candidate.a_mask, candidate.b_mask,
                          candidate.metrics, options.profile, c_sum, d_sum,
                          evaluations, options.random_seed, "local_sbc",
                          candidate.s_mask, instance);
    std::cout << "FOUND evaluation=" << evaluations
              << " output=" << options.output << '\n';
    return true;
  };

  std::cout << "order=167 profile=" << options.profile
            << " parameterization=local_sbc steepest_polish=1 seed="
            << options.random_seed << " shadow_weight="
            << options.shadow_weight << " workers=1\n";
  if (exact(best)) return 0;
  write_best();

  bool stopped = false;
  while (!stopped) {
    LocalState round_best = current;
    std::int64_t round_best_score =
        local_score(round_best, options.shadow_weight);
    complete_neighborhood = true;
    for (int kind = 0; kind < 6 && !stopped; ++kind) {
      for (int first = 0; first < instance.half && !stopped; ++first) {
        for (int second = first + 1; second < instance.half; ++second) {
          bool eligible = false;
          if (kind == 0)
            eligible = current.b_mask.test(first) !=
                       current.b_mask.test(second);
          else if (kind == 1)
            eligible = current.c_mask.test(first) !=
                       current.c_mask.test(second);
          else if (kind == 2)
            eligible = current.d_mask.test(first) !=
                       current.d_mask.test(second);
          else if (kind == 3)
            eligible = current.b_mask.test(first) !=
                           current.b_mask.test(second) &&
                       current.c_mask.test(first) !=
                           current.c_mask.test(second);
          else if (kind == 4)
            eligible = current.b_mask.test(first) !=
                           current.b_mask.test(second) &&
                       current.d_mask.test(first) !=
                           current.d_mask.test(second);
          else
            eligible = current.c_mask.test(first) !=
                           current.c_mask.test(second) &&
                       current.d_mask.test(first) !=
                           current.d_mask.test(second);
          if (!eligible) continue;
          const double elapsed = std::chrono::duration<double>(
                                     std::chrono::steady_clock::now() - start)
                                     .count();
          if ((options.trials != 0 && evaluations >= options.trials) ||
              (options.seconds > 0 && elapsed >= options.seconds)) {
            complete_neighborhood = false;
            stopped = true;
            break;
          }
          Bits83 toggle;
          toggle.set(first);
          toggle.set(second);
          const LocalState proposal = local_pair_move(
              current, toggle, kind, c_sum, d_sum, instance);
          ++evaluations;
          if (exact(proposal)) return 0;
          const std::int64_t proposal_score =
              local_score(proposal, options.shadow_weight);
          if (proposal_score < best_score) {
            best = proposal;
            best_score = proposal_score;
            write_best();
          }
          if (proposal_score < round_best_score) {
            round_best = proposal;
            round_best_score = proposal_score;
          }

          if (std::chrono::steady_clock::now() >= next_report) {
            const double report_elapsed = std::chrono::duration<double>(
                                              std::chrono::steady_clock::now() -
                                              start)
                                              .count();
            std::cout << "evaluations=" << evaluations
                      << " elapsed=" << std::fixed << std::setprecision(3)
                      << report_elapsed << " rate="
                      << evaluations / report_elapsed << " rounds=" << rounds
                      << " current_score="
                      << local_score(current, options.shadow_weight)
                      << " best_score=" << best_score << '\n';
            next_report = std::chrono::steady_clock::now() +
                          std::chrono::duration<double>(options.report_every);
          }
        }
      }
    }
    if (!complete_neighborhood) break;
    if (round_best_score >= local_score(current, options.shadow_weight)) {
      stopped = true;
      break;
    }
    current = round_best;
    ++rounds;
    std::cout << "descent_round=" << rounds
              << " energy=" << current.metrics.energy
              << " shadow_penalty=" << shadow_penalty(current.metrics)
              << " score=" << round_best_score << '\n';
  }
  const double elapsed =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
          .count();
  std::cout << "evaluations=" << evaluations << " elapsed=" << std::fixed
            << std::setprecision(3) << elapsed << " rate="
            << (elapsed > 0 ? evaluations / elapsed : 0.0)
            << " descent_rounds=" << rounds
            << " complete_neighborhood=" << complete_neighborhood
            << " local_minimum="
            << (complete_neighborhood &&
                local_score(current, options.shadow_weight) == best_score)
            << " best_energy=" << best.metrics.energy
            << " best_shadow_penalty=" << shadow_penalty(best.metrics)
            << " best_score=" << best_score << '\n'
            << "FOUND=0\n";
  return 0;
}

int run_local(const Options &options) {
  if (options.steepest_polish) return run_local_steepest(options);
  const Instance instance(ORDER);
  const std::array<int, 2> c_sums{{-1, -9}};
  const std::array<int, 2> d_sums{{-21, 19}};
  const std::array<int, 2> minimum_s_weights{{5, 7}};
  const std::array<int, 2> maximum_s_weights{{77, 81}};
  const int c_sum = c_sums[options.profile];
  const int d_sum = d_sums[options.profile];
  if (options.s_weight != -1 &&
      (options.s_weight < minimum_s_weights[options.profile] ||
       options.s_weight > maximum_s_weights[options.profile] ||
       options.s_weight % 2 == 0))
    throw std::runtime_error("initial S weight is infeasible for this profile");

  SplitMix64 rng(options.random_seed);
  std::uint64_t completed = 0;
  std::uint64_t restarts = 0;
  std::uint64_t accepted = 0;
  LocalMoveCounts move_counts;
  bool used_initial = false;
  bool have_best = false;
  LocalState best;
  std::int64_t best_score = std::numeric_limits<std::int64_t>::max();
  const auto start = std::chrono::steady_clock::now();
  auto next_report = start + std::chrono::duration<double>(options.report_every);

  std::cout << "order=167 profile=" << options.profile
            << " row_sums=(15," << c_sum << ',' << d_sum << ")\n"
            << "parameterization=local_sbc moves_per_restart="
            << options.moves_per_restart << " temperatures=("
            << options.start_temperature << ',' << options.end_temperature
            << ") b_move_probability=" << options.b_move_probability
            << " coupled_move_probability="
            << options.coupled_move_probability
            << " restart_from_best=" << options.restart_from_best
            << " shadow_weight=" << options.shadow_weight
            << " compound_probability=" << options.compound_probability
            << " compound_arity=" << options.compound_arity
            << " seed=" << options.random_seed << " workers=1\n";

  auto record = [&](const LocalState &candidate,
                    std::uint64_t move) -> bool {
    if (candidate.metrics.energy == 0) {
      write_exact_candidate(options.output, candidate.a_mask,
                            candidate.b_mask, candidate.metrics,
                            options.profile, c_sum, d_sum, move,
                            options.random_seed, "local_sbc", candidate.s_mask,
                            instance);
      std::cout << "FOUND move=" << move << " output=" << options.output
                << '\n';
      return true;
    }
    const std::int64_t candidate_score =
        local_score(candidate, options.shadow_weight);
    if (!have_best || candidate_score < best_score) {
      best = candidate;
      best_score = candidate_score;
      have_best = true;
      write_local_checkpoint(options.checkpoint, best, options.profile, c_sum,
                             d_sum, move, options.random_seed, rng.state,
                             instance);
      std::cout << "best move=" << move << " energy=" << best.metrics.energy
                << " bad_lags=" << best.metrics.bad_lags
                << " max_abs_quarter=" << best.metrics.max_abs_quarter
                << " shadow_penalty=" << shadow_penalty(best.metrics)
                << " score=" << best_score
                << " s_weight=" << best.s_mask.count() << '\n';
    }
    return false;
  };

  bool stop = false;
  while (!stop && (options.trials == 0 || completed < options.trials)) {
    const double elapsed = std::chrono::duration<double>(
                               std::chrono::steady_clock::now() - start)
                               .count();
    if (options.seconds > 0 && elapsed >= options.seconds) break;
    LocalState current;
    if (!used_initial && !options.initial.empty()) {
      current = load_local_state(options.initial, options.profile, instance);
      used_initial = true;
    } else if (options.restart_from_best && have_best) {
      current = best;
    } else {
      current = random_local_state(rng, options.profile, options.s_weight,
                                   instance);
    }
    ++restarts;
    if (record(current, completed)) return 0;

    for (std::uint64_t step = 0; step < options.moves_per_restart; ++step) {
      if (options.trials != 0 && completed >= options.trials) {
        stop = true;
        break;
      }
      const double move_elapsed = std::chrono::duration<double>(
                                      std::chrono::steady_clock::now() - start)
                                      .count();
      if (options.seconds > 0 && move_elapsed >= options.seconds) {
        stop = true;
        break;
      }
      const double fraction =
          options.moves_per_restart == 1
              ? 1.0
              : static_cast<double>(step) /
                    static_cast<double>(options.moves_per_restart - 1);
      const double temperature =
          options.start_temperature *
          std::pow(options.end_temperature / options.start_temperature,
                   fraction);

      LocalState proposal = random_local_pair_move(
          rng, current, options.b_move_probability,
          options.coupled_move_probability, c_sum, d_sum, instance,
          move_counts);
      if (options.compound_probability > 0 &&
          uniform_unit(rng) < options.compound_probability) {
        for (int arity = 1; arity < options.compound_arity; ++arity)
          proposal = random_local_pair_move(
              rng, proposal, options.b_move_probability,
              options.coupled_move_probability, c_sum, d_sum, instance,
              move_counts);
      }
      ++completed;
      if (record(proposal, completed)) return 0;
      const std::int64_t delta =
          local_score(proposal, options.shadow_weight) -
          local_score(current, options.shadow_weight);
      if (delta <= 0 ||
          uniform_unit(rng) <
              std::exp(-static_cast<double>(delta) / temperature)) {
        current = proposal;
        ++accepted;
      }

      if (std::chrono::steady_clock::now() >= next_report) {
        const double report_elapsed = std::chrono::duration<double>(
                                          std::chrono::steady_clock::now() -
                                          start)
                                          .count();
        std::cout << "moves=" << completed << " elapsed=" << std::fixed
                  << std::setprecision(3) << report_elapsed << " rate="
                  << completed / report_elapsed << " restarts=" << restarts
                  << " accepted=" << accepted << " current_score="
                  << local_score(current, options.shadow_weight)
                  << " best_score=" << best_score << '\n';
        next_report = std::chrono::steady_clock::now() +
                      std::chrono::duration<double>(options.report_every);
      }
    }
  }
  const double elapsed =
      std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
          .count();
  std::cout << "moves=" << completed << " elapsed=" << std::fixed
            << std::setprecision(3) << elapsed << " rate="
            << (elapsed > 0 ? completed / elapsed : 0.0)
            << " restarts=" << restarts << " accepted=" << accepted
            << " atomic_moves=(" << move_counts.by_kind[0] << ','
            << move_counts.by_kind[1] << ',' << move_counts.by_kind[2]
            << ") coupled_moves=(" << move_counts.by_kind[3] << ','
            << move_counts.by_kind[4] << ',' << move_counts.by_kind[5]
            << ")";
  if (have_best) {
    std::cout << " best_energy=" << best.metrics.energy
              << " best_shadow_penalty=" << shadow_penalty(best.metrics)
              << " best_score=" << best_score << '\n';
  } else {
    std::cout << "none\n";
  }
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
    if (options.parameterization == "ab") return run_ab(options);
    if (options.parameterization == "sb") return run_sb(options);
    return run_local(options);
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
