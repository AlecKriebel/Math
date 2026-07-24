// Honest single-core throughput benchmark for the dense LP(333) quadratic
// character front end.
//
// This program:
//   * reconstructs the F_37/H quadratic polar matrices over F_3;
//   * reproduces the legal local-support and signed-skeleton counts;
//   * enumerates all legal h=1 and h=0 supports and their affine-rank census;
//   * selects one real support from every census cell;
//   * factors all 729 restricted quadratic pencils once per support;
//   * reuses those factorizations across batches built from legal sign
//     skeletons, consistent affine right-hand sides, and decorated targets;
//   * evaluates exact Eisenstein quadratic Gauss sums and pins a streaming
//     checksum so the timed loop cannot be optimized away.
//
// It is deliberately single threaded.  Rates are therefore per core.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int FIELD = 3;
constexpr int PRIME = 37;
constexpr int CLASS_COUNT = 12;
constexpr int QUARTETS = 6;
constexpr int AMBIENT = 24;
constexpr int MAX_DIM = 12;
constexpr int CHARACTERS = 729;

using SmallRow = std::array<std::uint8_t, MAX_DIM>;
using SmallMatrix = std::array<SmallRow, MAX_DIM>;
using AmbientVector = std::array<std::uint8_t, AMBIENT>;
using AmbientRow = std::array<std::uint8_t, AMBIENT>;
using AmbientMatrix = std::array<AmbientRow, AMBIENT>;
using Coefficients = std::array<std::uint8_t, QUARTETS>;

struct Eisenstein {
  std::int64_t a = 0;
  std::int64_t b = 0;
};

struct CpuTimer {
  std::chrono::steady_clock::time_point wall_start =
      std::chrono::steady_clock::now();
  std::clock_t cpu_start = std::clock();

  double wall_seconds() const {
    return std::chrono::duration<double>(
               std::chrono::steady_clock::now() - wall_start)
        .count();
  }

  double cpu_seconds() const {
    return static_cast<double>(std::clock() - cpu_start) / CLOCKS_PER_SEC;
  }
};

int mod3(int value) {
  value %= FIELD;
  return value < 0 ? value + FIELD : value;
}

std::uint8_t inverse3(std::uint8_t value) {
  if (value == 1) return 1;
  if (value == 2) return 2;
  throw std::runtime_error("attempted to invert zero in F_3");
}

Eisenstein e_multiply(Eisenstein left, Eisenstein right) {
  return {
      left.a * right.a - left.b * right.b,
      left.a * right.b + left.b * right.a - left.b * right.b,
  };
}

Eisenstein e_scale(std::int64_t scalar, Eisenstein value) {
  return {scalar * value.a, scalar * value.b};
}

Eisenstein e_rotate(Eisenstein value, int exponent) {
  static constexpr std::array<Eisenstein, 3> roots = {
      Eisenstein{1, 0},
      Eisenstein{0, 1},
      Eisenstein{-1, -1},
  };
  return e_multiply(value, roots[mod3(exponent)]);
}

std::int64_t power3(int exponent) {
  std::int64_t value = 1;
  for (int index = 0; index < exponent; ++index) value *= 3;
  return value;
}

std::array<std::array<int, 3>, CLASS_COUNT> classes;
std::array<int, PRIME> class_of;
std::array<AmbientMatrix, QUARTETS> ambient_polar;
std::array<Coefficients, CHARACTERS> character_trits;

int ambient_index(int quartet, int local) {
  switch (local) {
    case 0:
      return quartet;
    case 1:
      return quartet + 6;
    case 2:
      return quartet + 12;
    case 3:
      return quartet + 18;
    default:
      throw std::runtime_error("invalid local quartet index");
  }
}

void initialize_geometry() {
  constexpr std::array<int, 3> subgroup = {1, 26, 10};
  class_of.fill(-1);
  int power = 1;
  for (int class_index = 0; class_index < CLASS_COUNT; ++class_index) {
    for (int member = 0; member < 3; ++member) {
      const int value = power * subgroup[member] % PRIME;
      classes[class_index][member] = value;
      if (class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      class_of[value] = class_index;
    }
    power = power * 2 % PRIME;
  }

  for (int lag_class = 0; lag_class < QUARTETS; ++lag_class) {
    std::array<std::array<int, CLASS_COUNT>, CLASS_COUNT> transition{};
    const int lag = classes[lag_class][0];
    for (int source = 1; source < PRIME; ++source) {
      const int target = (source + lag) % PRIME;
      if (target == 0) continue;
      ++transition[class_of[source]][class_of[target]];
    }
    for (int channel = 0; channel < 2; ++channel) {
      const int offset = channel * CLASS_COUNT;
      for (int left = 0; left < CLASS_COUNT; ++left) {
        for (int right = 0; right < CLASS_COUNT; ++right) {
          ambient_polar[lag_class][offset + left][offset + right] =
              static_cast<std::uint8_t>(mod3(
                  transition[left][right] + transition[right][left]));
        }
      }
    }
  }

  for (int code = 0; code < CHARACTERS; ++code) {
    int work = code;
    for (int coordinate = 0; coordinate < QUARTETS; ++coordinate) {
      character_trits[code][coordinate] =
          static_cast<std::uint8_t>(work % FIELD);
      work /= FIELD;
    }
  }

  AmbientMatrix sum{};
  for (int lag = 0; lag < QUARTETS; ++lag) {
    for (int left = 0; left < AMBIENT; ++left) {
      for (int right = 0; right < AMBIENT; ++right) {
        sum[left][right] = static_cast<std::uint8_t>(
            mod3(sum[left][right] + ambient_polar[lag][left][right]));
      }
    }
  }
  for (int left = 0; left < AMBIENT; ++left) {
    for (int right = 0; right < AMBIENT; ++right) {
      const int expected = left == right ? 2 : 0;
      if (sum[left][right] != expected) {
        throw std::runtime_error("the universal sum is not 2I");
      }
    }
  }
}

int matrix_rank(std::vector<std::vector<std::uint8_t>> matrix) {
  if (matrix.empty()) return 0;
  const int rows = static_cast<int>(matrix.size());
  const int columns = static_cast<int>(matrix.front().size());
  int rank = 0;
  for (int column = 0; column < columns && rank < rows; ++column) {
    int pivot = -1;
    for (int row = rank; row < rows; ++row) {
      if (matrix[row][column]) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(matrix[rank], matrix[pivot]);
    if (matrix[rank][column] == 2) {
      for (int entry = column; entry < columns; ++entry) {
        matrix[rank][entry] =
            static_cast<std::uint8_t>(2 * matrix[rank][entry] % FIELD);
      }
    }
    for (int row = 0; row < rows; ++row) {
      if (row == rank || matrix[row][column] == 0) continue;
      const int factor = matrix[row][column];
      for (int entry = column; entry < columns; ++entry) {
        matrix[row][entry] = static_cast<std::uint8_t>(
            mod3(matrix[row][entry] - factor * matrix[rank][entry]));
      }
    }
    ++rank;
  }
  return rank;
}

struct LocalCounts {
  std::array<std::uint64_t, 5> supports{};
  std::array<std::uint64_t, 5> signed_states{};
};

LocalCounts enumerate_local_counts() {
  LocalCounts result;
  constexpr std::array<int, 4> equation = {-1, 1, 1, -1};
  for (int mask = 0; mask < 16; ++mask) {
    const int occupancy = __builtin_popcount(static_cast<unsigned>(mask));
    std::vector<int> active;
    for (int local = 0; local < 4; ++local) {
      if (mask & (1 << local)) active.push_back(local);
    }
    std::uint64_t legal = 0;
    for (int sign_code = 0; sign_code < (1 << active.size()); ++sign_code) {
      int sum = 0;
      for (std::size_t index = 0; index < active.size(); ++index) {
        const int sign = sign_code & (1 << index) ? -1 : 1;
        sum += equation[active[index]] * sign;
      }
      if (mod3(sum) == 0) ++legal;
    }
    if (legal) ++result.supports[occupancy];
    result.signed_states[occupancy] += legal;
  }
  const std::array<std::uint64_t, 5> expected_supports = {1, 0, 6, 4, 1};
  const std::array<std::uint64_t, 5> expected_signed = {1, 0, 12, 8, 6};
  if (result.supports != expected_supports ||
      result.signed_states != expected_signed) {
    throw std::runtime_error("the local support/sign census changed");
  }
  return result;
}

using CountTable =
    std::array<std::array<std::array<std::uint64_t, 7>, 25>, 7>;

CountTable polynomial_counts(const std::array<std::uint64_t, 5>& local) {
  CountTable dp{};
  dp[0][0][0] = 1;
  for (int used = 0; used < QUARTETS; ++used) {
    for (int total = 0; total <= AMBIENT; ++total) {
      for (int nonempty = 0; nonempty <= used; ++nonempty) {
        const std::uint64_t current = dp[used][total][nonempty];
        if (!current) continue;
        for (int occupancy = 0; occupancy <= 4; ++occupancy) {
          if (!local[occupancy]) continue;
          dp[used + 1][total + occupancy]
            [nonempty + (occupancy != 0)] += current * local[occupancy];
        }
      }
    }
  }
  return dp;
}

struct Cell {
  int r = 0;
  int d = 0;
  int rho = 0;
  int nu = 0;

  auto operator<=>(const Cell&) const = default;
};

struct SupportCensus {
  std::uint64_t total = 0;
  std::map<Cell, std::uint64_t> histogram;
  std::map<Cell, std::uint32_t> representative_masks;
};

std::vector<int> support_positions(std::uint32_t mask) {
  std::vector<int> positions;
  for (int ambient = 0; ambient < AMBIENT; ++ambient) {
    if (mask & (1u << ambient)) positions.push_back(ambient);
  }
  return positions;
}

std::vector<std::vector<std::uint8_t>> independent_constraint_rows(
    const std::vector<int>& positions) {
  std::vector<std::vector<std::uint8_t>> rows;
  for (int quartet = 0; quartet < QUARTETS; ++quartet) {
    std::vector<std::uint8_t> row(positions.size());
    bool nonempty = false;
    for (std::size_t index = 0; index < positions.size(); ++index) {
      const int position = positions[index];
      for (int local = 0; local < 4; ++local) {
        if (position == ambient_index(quartet, local)) {
          row[index] = 1;
          nonempty = true;
        }
      }
    }
    if (nonempty) rows.push_back(std::move(row));
  }
  std::vector<std::uint8_t> channel_a(positions.size());
  for (std::size_t index = 0; index < positions.size(); ++index) {
    if (positions[index] < CLASS_COUNT) channel_a[index] = 1;
  }
  rows.push_back(std::move(channel_a));
  if (matrix_rank(rows) != static_cast<int>(rows.size())) {
    throw std::runtime_error("selected local plus channel-A rows lost rank");
  }
  return rows;
}

Cell support_cell(std::uint32_t mask, int medium_count) {
  const auto positions = support_positions(mask);
  const auto rows = independent_constraint_rows(positions);
  const int rank = static_cast<int>(rows.size());
  std::vector<std::vector<std::uint8_t>> gram(
      rank, std::vector<std::uint8_t>(rank));
  for (int left = 0; left < rank; ++left) {
    for (int right = 0; right < rank; ++right) {
      int value = 0;
      for (int column = 0; column < medium_count; ++column) {
        value += rows[left][column] * rows[right][column];
      }
      gram[left][right] = static_cast<std::uint8_t>(mod3(value));
    }
  }
  const int r = rank - 1;
  const int d = medium_count - rank;
  const int nu = rank - matrix_rank(gram);
  return {r, d, d - nu, nu};
}

SupportCensus enumerate_support_census(int target) {
  SupportCensus result;
  std::array<int, QUARTETS> local_masks{};
  const auto recurse = [&](auto&& self, int quartet, int total) -> void {
    if (quartet == QUARTETS) {
      if (total != target) return;
      std::uint32_t mask = 0;
      for (int q = 0; q < QUARTETS; ++q) {
        for (int local = 0; local < 4; ++local) {
          if (local_masks[q] & (1 << local)) {
            mask |= 1u << ambient_index(q, local);
          }
        }
      }
      const Cell cell = support_cell(mask, target);
      ++result.total;
      ++result.histogram[cell];
      result.representative_masks.try_emplace(cell, mask);
      return;
    }
    const int remaining = QUARTETS - quartet - 1;
    for (int local = 0; local < 16; ++local) {
      const int occupancy =
          __builtin_popcount(static_cast<unsigned>(local));
      if (occupancy == 1) continue;
      const int next = total + occupancy;
      if (next > target || next + 4 * remaining < target) continue;
      local_masks[quartet] = local;
      self(self, quartet + 1, next);
    }
  };
  recurse(recurse, 0, 0);
  return result;
}

std::vector<AmbientVector> nullspace_basis(
    const std::vector<int>& positions,
    std::vector<std::vector<std::uint8_t>> rows) {
  const int row_count = static_cast<int>(rows.size());
  const int columns = static_cast<int>(positions.size());
  int rank = 0;
  std::vector<int> pivots;
  for (int column = 0; column < columns && rank < row_count; ++column) {
    int pivot = -1;
    for (int row = rank; row < row_count; ++row) {
      if (rows[row][column]) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(rows[rank], rows[pivot]);
    if (rows[rank][column] == 2) {
      for (int entry = 0; entry < columns; ++entry) {
        rows[rank][entry] =
            static_cast<std::uint8_t>(2 * rows[rank][entry] % FIELD);
      }
    }
    for (int row = 0; row < row_count; ++row) {
      if (row == rank || rows[row][column] == 0) continue;
      const int factor = rows[row][column];
      for (int entry = 0; entry < columns; ++entry) {
        rows[row][entry] = static_cast<std::uint8_t>(
            mod3(rows[row][entry] - factor * rows[rank][entry]));
      }
    }
    pivots.push_back(column);
    ++rank;
  }
  if (rank != row_count) {
    throw std::runtime_error("constraint rows unexpectedly dependent");
  }

  std::vector<bool> is_pivot(columns, false);
  for (int pivot : pivots) is_pivot[pivot] = true;
  std::vector<AmbientVector> basis;
  for (int free = 0; free < columns; ++free) {
    if (is_pivot[free]) continue;
    AmbientVector vector{};
    vector[positions[free]] = 1;
    for (int row = 0; row < rank; ++row) {
      vector[positions[pivots[row]]] =
          static_cast<std::uint8_t>(mod3(-rows[row][free]));
    }
    basis.push_back(vector);
  }

  for (const auto& vector : basis) {
    for (const auto& row : rows) {
      int value = 0;
      for (int column = 0; column < columns; ++column) {
        value += row[column] * vector[positions[column]];
      }
      if (mod3(value) != 0) {
        throw std::runtime_error("constructed vector left the kernel");
      }
    }
  }
  return basis;
}

struct SupportFixture {
  int shell = 0;
  Cell cell;
  std::uint32_t mask = 0;
  std::vector<int> positions;
  std::vector<AmbientVector> kernel;
  std::array<SmallMatrix, QUARTETS> restricted{};
};

SupportFixture make_support_fixture(
    int shell, Cell cell, std::uint32_t mask) {
  SupportFixture fixture;
  fixture.shell = shell;
  fixture.cell = cell;
  fixture.mask = mask;
  fixture.positions = support_positions(mask);
  const auto rows = independent_constraint_rows(fixture.positions);
  fixture.kernel = nullspace_basis(fixture.positions, rows);
  if (static_cast<int>(fixture.kernel.size()) != cell.d) {
    throw std::runtime_error("kernel dimension disagrees with census cell");
  }

  for (int lag = 0; lag < QUARTETS; ++lag) {
    for (int left = 0; left < cell.d; ++left) {
      for (int right = 0; right < cell.d; ++right) {
        int value = 0;
        for (int ambient_left = 0; ambient_left < AMBIENT; ++ambient_left) {
          if (!fixture.kernel[left][ambient_left]) continue;
          for (int ambient_right = 0; ambient_right < AMBIENT;
               ++ambient_right) {
            value += fixture.kernel[left][ambient_left] *
                     ambient_polar[lag][ambient_left][ambient_right] *
                     fixture.kernel[right][ambient_right];
          }
        }
        fixture.restricted[lag][left][right] =
            static_cast<std::uint8_t>(mod3(value));
      }
    }
  }
  return fixture;
}

void swap_basis(
    SmallMatrix& matrix,
    SmallMatrix& transform,
    int dimension,
    int left,
    int right) {
  if (left == right) return;
  for (int column = 0; column < dimension; ++column) {
    std::swap(matrix[left][column], matrix[right][column]);
  }
  for (int row = 0; row < dimension; ++row) {
    std::swap(matrix[row][left], matrix[row][right]);
    std::swap(transform[row][left], transform[row][right]);
  }
}

void add_basis_vector(
    SmallMatrix& matrix,
    SmallMatrix& transform,
    int dimension,
    int destination,
    int source,
    int coefficient) {
  coefficient = mod3(coefficient);
  if (coefficient == 0 || destination == source) return;
  const int old_dd = matrix[destination][destination];
  const int old_ds = matrix[destination][source];
  const int old_ss = matrix[source][source];
  std::array<std::uint8_t, MAX_DIM> old_column{};
  for (int row = 0; row < dimension; ++row) {
    old_column[row] = matrix[row][destination];
  }
  for (int row = 0; row < dimension; ++row) {
    if (row == destination) continue;
    const std::uint8_t value = static_cast<std::uint8_t>(
        mod3(old_column[row] + coefficient * matrix[row][source]));
    matrix[row][destination] = value;
    matrix[destination][row] = value;
  }
  matrix[destination][destination] = static_cast<std::uint8_t>(mod3(
      old_dd + 2 * coefficient * old_ds +
      coefficient * coefficient * old_ss));
  for (int row = 0; row < dimension; ++row) {
    transform[row][destination] = static_cast<std::uint8_t>(mod3(
        transform[row][destination] +
        coefficient * transform[row][source]));
  }
}

struct Factor {
  std::uint8_t dimension = 0;
  std::uint8_t rank = 0;
  SmallMatrix transform{};
  SmallRow diagonal{};
  Eisenstein phase_zero;
};

Factor factor_symmetric(SmallMatrix input, int dimension) {
  Factor result;
  result.dimension = static_cast<std::uint8_t>(dimension);
  for (int index = 0; index < dimension; ++index) {
    result.transform[index][index] = 1;
  }

  int pivot_index = 0;
  while (pivot_index < dimension) {
    int diagonal_pivot = -1;
    for (int index = pivot_index; index < dimension; ++index) {
      if (input[index][index]) {
        diagonal_pivot = index;
        break;
      }
    }
    if (diagonal_pivot < 0) {
      int left = -1;
      int right = -1;
      for (int row = pivot_index; row < dimension && left < 0; ++row) {
        for (int column = row + 1; column < dimension; ++column) {
          if (input[row][column]) {
            left = row;
            right = column;
            break;
          }
        }
      }
      if (left < 0) break;
      swap_basis(input, result.transform, dimension, pivot_index, left);
      if (right == pivot_index) right = left;
      add_basis_vector(
          input, result.transform, dimension, pivot_index, right, 1);
      diagonal_pivot = pivot_index;
    }
    swap_basis(
        input, result.transform, dimension, pivot_index, diagonal_pivot);
    const std::uint8_t diagonal = input[pivot_index][pivot_index];
    if (!diagonal) {
      throw std::runtime_error("failed to create a symmetric pivot");
    }
    for (int column = pivot_index + 1; column < dimension; ++column) {
      if (!input[pivot_index][column]) continue;
      const int coefficient = mod3(
          -input[pivot_index][column] * inverse3(diagonal));
      add_basis_vector(
          input, result.transform, dimension, column, pivot_index,
          coefficient);
      if (input[pivot_index][column] != 0) {
        throw std::runtime_error("congruence elimination failed");
      }
    }
    result.diagonal[pivot_index] = diagonal;
    ++pivot_index;
  }
  result.rank = static_cast<std::uint8_t>(pivot_index);

  for (int left = 0; left < dimension; ++left) {
    for (int right = 0; right < dimension; ++right) {
      const int expected =
          left == right && left < pivot_index ? result.diagonal[left] : 0;
      if (input[left][right] != expected) {
        throw std::runtime_error("factor did not diagonalize by congruence");
      }
    }
  }

  Eisenstein gauss{1, 0};
  for (int index = 0; index < pivot_index; ++index) {
    // sum_z omega^((diagonal/2) z^2) = 1+2 omega^(2 diagonal).
    const Eisenstein one_dimensional =
        result.diagonal[index] == 1 ? Eisenstein{-1, -2}
                                    : Eisenstein{1, 2};
    gauss = e_multiply(gauss, one_dimensional);
  }
  result.phase_zero =
      e_scale(power3(dimension - pivot_index), gauss);
  return result;
}

std::array<Factor, CHARACTERS> factor_support(
    const SupportFixture& support) {
  std::array<Factor, CHARACTERS> factors;
  for (int code = 0; code < CHARACTERS; ++code) {
    SmallMatrix pencil{};
    for (int left = 0; left < support.cell.d; ++left) {
      for (int right = 0; right < support.cell.d; ++right) {
        int value = 0;
        for (int lag = 0; lag < QUARTETS; ++lag) {
          value += character_trits[code][lag] *
                   support.restricted[lag][left][right];
        }
        pencil[left][right] = static_cast<std::uint8_t>(mod3(value));
      }
    }
    factors[code] = factor_symmetric(pencil, support.cell.d);
  }
  return factors;
}

std::vector<std::array<std::uint8_t, 4>> legal_local_signs(int local_mask) {
  std::vector<int> active;
  for (int local = 0; local < 4; ++local) {
    if (local_mask & (1 << local)) active.push_back(local);
  }
  constexpr std::array<int, 4> equation = {-1, 1, 1, -1};
  std::vector<std::array<std::uint8_t, 4>> result;
  for (int code = 0; code < (1 << active.size()); ++code) {
    std::array<std::uint8_t, 4> signs{};
    int sum = 0;
    for (std::size_t index = 0; index < active.size(); ++index) {
      const int integer_sign = code & (1 << index) ? -1 : 1;
      signs[active[index]] =
          static_cast<std::uint8_t>(integer_sign == 1 ? 1 : 2);
      sum += equation[active[index]] * integer_sign;
    }
    if (mod3(sum) == 0) result.push_back(signs);
  }
  if (result.empty()) {
    throw std::runtime_error("representative support has an illegal local mask");
  }
  return result;
}

struct Batch {
  AmbientVector x0{};
  std::array<std::uint8_t, QUARTETS> target{};
  std::array<std::uint8_t, 7> affine_rhs{};
  int affine_rhs_size = 0;
  std::array<SmallRow, QUARTETS> linear{};
  std::array<std::uint8_t, QUARTETS> offset{};
  std::uint32_t sign_code = 0;
  int high_position = -1;
};

int ambient_quadratic(
    const AmbientVector& vector, const AmbientMatrix& polar) {
  int value = 0;
  for (int left = 0; left < AMBIENT; ++left) {
    if (!vector[left]) continue;
    for (int right = 0; right < AMBIENT; ++right) {
      value += vector[left] * polar[left][right] * vector[right];
    }
  }
  return mod3(2 * value);
}

Batch make_batch(const SupportFixture& support, std::uint64_t batch_index) {
  Batch batch;
  std::uint64_t sign_selector = batch_index;
  std::array<std::uint8_t, AMBIENT> signs{};
  std::uint32_t packed_signs = 0;
  for (int quartet = 0; quartet < QUARTETS; ++quartet) {
    int local_mask = 0;
    for (int local = 0; local < 4; ++local) {
      if (support.mask & (1u << ambient_index(quartet, local))) {
        local_mask |= 1 << local;
      }
    }
    const auto options = legal_local_signs(local_mask);
    const auto& chosen = options[sign_selector % options.size()];
    sign_selector /= options.size();
    for (int local = 0; local < 4; ++local) {
      const int ambient = ambient_index(quartet, local);
      signs[ambient] = chosen[local];
      if (chosen[local] == 2) packed_signs ^= 1u << ambient;
    }
  }
  batch.sign_code = packed_signs;

  std::vector<int> inactive;
  for (int ambient = 0; ambient < AMBIENT; ++ambient) {
    if (!(support.mask & (1u << ambient))) inactive.push_back(ambient);
  }
  if (support.shell == 15) {
    if (inactive.size() != 9) {
      throw std::runtime_error("the h=1 support did not leave nine positions");
    }
    batch.high_position = inactive[batch_index % inactive.size()];
  }

  for (int ambient : support.positions) {
    const int phase = mod3(
        static_cast<int>(batch_index % 27) +
        2 * ambient +
        (ambient / 6 + 1) * static_cast<int>((batch_index / 7) % 3) +
        (batch.high_position < 0 ? 0 : batch.high_position));
    // x=-sigma*u, with signs represented by 1 and -1=2 in F_3.
    batch.x0[ambient] =
        static_cast<std::uint8_t>(mod3(-signs[ambient] * phase));
  }

  const auto constraint_rows =
      independent_constraint_rows(support.positions);
  batch.affine_rhs_size = static_cast<int>(constraint_rows.size());
  for (int row = 0; row < batch.affine_rhs_size; ++row) {
    int value = 0;
    for (std::size_t column = 0; column < support.positions.size(); ++column) {
      value += constraint_rows[row][column] *
               batch.x0[support.positions[column]];
    }
    batch.affine_rhs[row] = static_cast<std::uint8_t>(mod3(value));
  }

  for (int lag = 0; lag < QUARTETS; ++lag) {
    const int constant =
        ambient_quadratic(batch.x0, ambient_polar[lag]);
    int decoration = static_cast<int>(batch_index % 3) * (lag + 1);
    decoration += (batch.high_position + 1) * (2 * lag + 1);
    for (int ambient : support.positions) {
      const int integer_sign = signs[ambient] == 1 ? 1 : -1;
      decoration += integer_sign * ((ambient + lag) % 3);
    }
    batch.target[lag] =
        static_cast<std::uint8_t>(mod3(constant + decoration));
    batch.offset[lag] =
        static_cast<std::uint8_t>(mod3(constant - batch.target[lag]));

    std::array<std::uint8_t, AMBIENT> matrix_times_x0{};
    for (int left = 0; left < AMBIENT; ++left) {
      int value = 0;
      for (int right = 0; right < AMBIENT; ++right) {
        value += ambient_polar[lag][left][right] * batch.x0[right];
      }
      matrix_times_x0[left] =
          static_cast<std::uint8_t>(mod3(value));
    }
    for (int basis = 0; basis < support.cell.d; ++basis) {
      int value = 0;
      for (int ambient = 0; ambient < AMBIENT; ++ambient) {
        value += support.kernel[basis][ambient] *
                 matrix_times_x0[ambient];
      }
      batch.linear[lag][basis] =
          static_cast<std::uint8_t>(mod3(value));
    }
  }
  return batch;
}

Eisenstein evaluate_character(
    const Factor& factor,
    const Batch& batch,
    const Coefficients& coefficients) {
  SmallRow linear{};
  int phase = 0;
  const int dimension = factor.dimension;
  for (int lag = 0; lag < QUARTETS; ++lag) {
    const int coefficient = coefficients[lag];
    if (!coefficient) continue;
    phase += coefficient * batch.offset[lag];
    for (int index = 0; index < dimension; ++index) {
      linear[index] = static_cast<std::uint8_t>(
          mod3(linear[index] + coefficient * batch.linear[lag][index]));
    }
  }
  phase = mod3(phase);

  for (int diagonal = 0; diagonal < dimension; ++diagonal) {
    int transformed = 0;
    for (int row = 0; row < dimension; ++row) {
      transformed += factor.transform[row][diagonal] * linear[row];
    }
    transformed = mod3(transformed);
    if (diagonal >= factor.rank) {
      if (transformed) return {0, 0};
      continue;
    }
    // Completing the square adds l'^2 / diagonal to the constant in F_3.
    phase += transformed * transformed *
             inverse3(factor.diagonal[diagonal]);
  }
  return e_rotate(factor.phase_zero, phase);
}

std::uint64_t checksum_mix(
    std::uint64_t state,
    Eisenstein value,
    std::uint64_t label) {
  auto mix_word = [](std::uint64_t word) {
    word ^= word >> 30;
    word *= 0xbf58476d1ce4e5b9ULL;
    word ^= word >> 27;
    word *= 0x94d049bb133111ebULL;
    return word ^ (word >> 31);
  };
  state ^= mix_word(static_cast<std::uint64_t>(value.a) +
                    0x9e3779b97f4a7c15ULL * (label + 1));
  state = (state << 17) | (state >> 47);
  state ^= mix_word(static_cast<std::uint64_t>(value.b) +
                    0xd1b54a32d192ed03ULL * (label + 3));
  return state;
}

struct BenchmarkResult {
  std::uint64_t evaluations = 0;
  std::uint64_t checksum = 0;
  double wall_seconds = 0;
  double cpu_seconds = 0;
};

BenchmarkResult benchmark_evaluations(
    const std::vector<SupportFixture>& supports,
    const std::vector<std::array<Factor, CHARACTERS>>& factors,
    int batch_size,
    int rounds) {
  std::vector<std::vector<Batch>> batches;
  for (std::size_t support = 0; support < supports.size(); ++support) {
    std::vector<Batch> support_batches;
    support_batches.reserve(batch_size);
    for (int batch = 0; batch < batch_size; ++batch) {
      support_batches.push_back(make_batch(
          supports[support],
          static_cast<std::uint64_t>(batch) +
              104729ULL * static_cast<std::uint64_t>(support)));
    }
    batches.push_back(std::move(support_batches));
  }

  std::uint64_t checksum = 0x243f6a8885a308d3ULL;
  std::uint64_t evaluations = 0;
  CpuTimer timer;
  for (int round = 0; round < rounds; ++round) {
    for (std::size_t support = 0; support < supports.size(); ++support) {
      for (int code = 0; code < CHARACTERS; ++code) {
        const Factor& factor = factors[support][code];
        for (int batch = 0; batch < batch_size; ++batch) {
          const Eisenstein value = evaluate_character(
              factor, batches[support][batch], character_trits[code]);
          const std::uint64_t label =
              static_cast<std::uint64_t>(round) * 1000000007ULL +
              support * 1000003ULL + code * 1009ULL + batch;
          checksum = checksum_mix(checksum, value, label);
          ++evaluations;
        }
      }
    }
  }
  return {
      evaluations,
      checksum,
      timer.wall_seconds(),
      timer.cpu_seconds(),
  };
}

struct FactorBenchmarkResult {
  std::uint64_t reductions = 0;
  std::uint64_t checksum = 0;
  double wall_seconds = 0;
  double cpu_seconds = 0;
};

FactorBenchmarkResult benchmark_factorization(
    const std::vector<SupportFixture>& supports,
    int repeats) {
  std::uint64_t checksum = 0x13198a2e03707344ULL;
  std::uint64_t reductions = 0;
  CpuTimer timer;
  for (int repeat = 0; repeat < repeats; ++repeat) {
    for (std::size_t support = 0; support < supports.size(); ++support) {
      const auto factors = factor_support(supports[support]);
      for (int code = 0; code < CHARACTERS; ++code) {
        const Factor& factor = factors[code];
        const Eisenstein value = factor.phase_zero;
        checksum = checksum_mix(
            checksum, value,
            repeat * 1000003ULL + support * CHARACTERS + code + factor.rank);
        ++reductions;
      }
    }
  }
  return {
      reductions,
      checksum,
      timer.wall_seconds(),
      timer.cpu_seconds(),
  };
}

std::string trit_string(const std::uint8_t* values, int length) {
  std::string result;
  result.reserve(length);
  for (int index = 0; index < length; ++index) {
    result.push_back(static_cast<char>('0' + values[index]));
  }
  return result;
}

void emit_reference_fixture(
    const SupportFixture& support,
    const std::array<Factor, CHARACTERS>& factors,
    std::uint64_t batch_index) {
  const Batch batch = make_batch(support, batch_index);
  std::cout << "REFERENCE_META"
            << " shell=" << support.shell
            << " mask=" << support.mask
            << " r=" << support.cell.r
            << " d=" << support.cell.d
            << " rho=" << support.cell.rho
            << " nu=" << support.cell.nu
            << " x0=" << trit_string(batch.x0.data(), AMBIENT)
            << " target=" << trit_string(batch.target.data(), QUARTETS)
            << " rhs="
            << trit_string(batch.affine_rhs.data(), batch.affine_rhs_size)
            << " sign_code=" << batch.sign_code
            << " high_position=" << batch.high_position << "\n";
  for (int code = 0; code < CHARACTERS; ++code) {
    const Eisenstein value =
        evaluate_character(factors[code], batch, character_trits[code]);
    std::cout << "REFERENCE_VALUE"
              << " shell=" << support.shell
              << " code=" << code
              << " a=" << value.a
              << " b=" << value.b << "\n";
  }
}

void print_cell(Cell cell, std::uint64_t count) {
  std::cout << "  cell=(r=" << cell.r
            << ",d=" << cell.d
            << ",rho=" << cell.rho
            << ",nu=" << cell.nu
            << ") count=" << count << "\n";
}

std::vector<Cell> expected_cells(int shell) {
  if (shell == 15) {
    return {
        {4, 10, 10, 0},
        {5, 9, 5, 4},
        {5, 9, 7, 2},
        {5, 9, 9, 0},
        {6, 8, 6, 2},
        {6, 8, 8, 0},
    };
  }
  return {
      {5, 12, 11, 1},
      {5, 12, 12, 0},
      {6, 11, 6, 5},
      {6, 11, 8, 3},
      {6, 11, 10, 1},
      {6, 11, 11, 0},
  };
}

std::map<Cell, std::uint64_t> expected_histogram(int shell) {
  if (shell == 15) {
    return {
        {{4, 10, 10, 0}, 240},
        {{5, 9, 5, 4}, 6144},
        {{5, 9, 7, 2}, 46080},
        {{5, 9, 9, 0}, 25920},
        {{6, 8, 6, 2}, 276480},
        {{6, 8, 8, 0}, 155520},
    };
  }
  return {
      {{5, 12, 11, 1}, 1080},
      {{5, 12, 12, 0}, 60},
      {{6, 11, 6, 5}, 4096},
      {{6, 11, 8, 3}, 46080},
      {{6, 11, 10, 1}, 53280},
      {{6, 11, 11, 0}, 2880},
  };
}

void assert_global_counts(
    const LocalCounts& local,
    const CountTable& supports,
    const CountTable& signed_states,
    const SupportCensus& h1,
    const SupportCensus& h0) {
  (void)local;
  if (supports[6][15][4] != 240 ||
      supports[6][15][5] != 78144 ||
      supports[6][15][6] != 432000 ||
      supports[6][18][5] != 1140 ||
      supports[6][18][6] != 106336) {
    throw std::runtime_error("unsigned support counts by r changed");
  }
  if (signed_states[6][15][4] != 103680 ||
      signed_states[6][15][5] != 12085248 ||
      signed_states[6][15][6] != 47554560 ||
      signed_states[6][18][5] != 1296000 ||
      signed_states[6][18][6] != 46434304) {
    throw std::runtime_error("signed skeleton counts by r changed");
  }
  if (h1.total != 510384 || h0.total != 107476 ||
      h1.histogram != expected_histogram(15) ||
      h0.histogram != expected_histogram(18)) {
    throw std::runtime_error("dense support census changed");
  }
  const std::uint64_t signed_h1 =
      signed_states[6][15][4] + signed_states[6][15][5] +
      signed_states[6][15][6];
  const std::uint64_t signed_h0 =
      signed_states[6][18][5] + signed_states[6][18][6];
  if (signed_h1 != 59743488 || signed_h0 != 47730304) {
    throw std::runtime_error("signed shell totals changed");
  }
}

double rate(std::uint64_t work, double seconds) {
  return static_cast<double>(work) / seconds;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    int batch_size = 96;
    int rounds = 48;
    int factor_repeats = 8;
    bool emit_reference = false;
    for (int index = 1; index < argc; ++index) {
      const std::string option = argv[index];
      if (option == "--batch" && index + 1 < argc) {
        batch_size = std::stoi(argv[++index]);
      } else if (option == "--rounds" && index + 1 < argc) {
        rounds = std::stoi(argv[++index]);
      } else if (option == "--factor-repeats" && index + 1 < argc) {
        factor_repeats = std::stoi(argv[++index]);
      } else if (option == "--emit-reference") {
        emit_reference = true;
      } else {
        throw std::runtime_error("unknown or incomplete command-line option");
      }
    }
    if (batch_size <= 0 || rounds <= 0 || factor_repeats <= 0) {
      throw std::runtime_error("benchmark sizes must be positive");
    }

    initialize_geometry();
    const LocalCounts local = enumerate_local_counts();
    const CountTable support_polynomial = polynomial_counts(local.supports);
    const CountTable signed_polynomial =
        polynomial_counts(local.signed_states);
    const SupportCensus h1_census = enumerate_support_census(15);
    const SupportCensus h0_census = enumerate_support_census(18);
    assert_global_counts(
        local, support_polynomial, signed_polynomial, h1_census, h0_census);

    std::cout << "status=PASS\n";
    std::cout << "local_support_histogram=1,0,6,4,1\n";
    std::cout << "local_signed_histogram=1,0,12,8,6\n";
    std::cout << "h1_unsigned_supports=" << h1_census.total << "\n";
    std::cout << "h0_unsigned_supports=" << h0_census.total << "\n";
    std::cout << "h1_signed_skeletons="
              << signed_polynomial[6][15][4] +
                     signed_polynomial[6][15][5] +
                     signed_polynomial[6][15][6]
              << "\n";
    std::cout << "h0_signed_skeletons="
              << signed_polynomial[6][18][5] +
                     signed_polynomial[6][18][6]
              << "\n";
    for (const auto& [cell, count] : h1_census.histogram) {
      std::cout << "h1";
      print_cell(cell, count);
    }
    for (const auto& [cell, count] : h0_census.histogram) {
      std::cout << "h0";
      print_cell(cell, count);
    }

    std::vector<SupportFixture> h1_supports;
    std::vector<SupportFixture> h0_supports;
    for (Cell cell : expected_cells(15)) {
      h1_supports.push_back(make_support_fixture(
          15, cell, h1_census.representative_masks.at(cell)));
    }
    for (Cell cell : expected_cells(18)) {
      h0_supports.push_back(make_support_fixture(
          18, cell, h0_census.representative_masks.at(cell)));
    }

    std::vector<std::array<Factor, CHARACTERS>> h1_factors;
    std::vector<std::array<Factor, CHARACTERS>> h0_factors;
    for (const auto& support : h1_supports) {
      h1_factors.push_back(factor_support(support));
    }
    for (const auto& support : h0_supports) {
      h0_factors.push_back(factor_support(support));
    }

    if (emit_reference) {
      // Use the d=8 h=1 cell and the d=11 h=0 cell.  The accompanying
      // Python verifier independently enumerates their full affine cubes.
      emit_reference_fixture(
          h1_supports.back(), h1_factors.back(), 20260724);
      emit_reference_fixture(
          h0_supports.back(), h0_factors.back(), 20260725);
      return 0;
    }

    std::vector<SupportFixture> all_supports = h1_supports;
    all_supports.insert(
        all_supports.end(), h0_supports.begin(), h0_supports.end());
    const FactorBenchmarkResult factor_result =
        benchmark_factorization(all_supports, factor_repeats);
    const BenchmarkResult h1_result = benchmark_evaluations(
        h1_supports, h1_factors, batch_size, rounds);
    const BenchmarkResult h0_result = benchmark_evaluations(
        h0_supports, h0_factors, batch_size, rounds);

    if (batch_size == 96 && rounds == 48 && factor_repeats == 8) {
      constexpr std::uint64_t expected_factor_checksum =
          0xdcdab09cb31d00b6ULL;
      constexpr std::uint64_t expected_h1_checksum =
          0xf21613ddea2e0b16ULL;
      constexpr std::uint64_t expected_h0_checksum =
          0xa9ee3c575158e4d6ULL;
      if (factor_result.checksum != expected_factor_checksum ||
          h1_result.checksum != expected_h1_checksum ||
          h0_result.checksum != expected_h0_checksum) {
        throw std::runtime_error("the pinned default-workload checksum changed");
      }
    }

    const double factor_rate =
        rate(factor_result.reductions, factor_result.cpu_seconds);
    const double h1_rate =
        rate(h1_result.evaluations, h1_result.cpu_seconds);
    const double h0_rate =
        rate(h0_result.evaluations, h0_result.cpu_seconds);
    const double combined_rate =
        rate(h1_result.evaluations + h0_result.evaluations,
             h1_result.cpu_seconds + h0_result.cpu_seconds);

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "benchmark_batch_size=" << batch_size << "\n";
    std::cout << "benchmark_rounds=" << rounds << "\n";
    std::cout << "factor_reductions=" << factor_result.reductions << "\n";
    std::cout << "factor_cpu_seconds=" << factor_result.cpu_seconds << "\n";
    std::cout << "factor_wall_seconds=" << factor_result.wall_seconds << "\n";
    std::cout << "factor_reductions_per_core_second=" << factor_rate << "\n";
    std::cout << "factor_checksum=0x" << std::hex << factor_result.checksum
              << std::dec << "\n";
    std::cout << "h1_character_evaluations=" << h1_result.evaluations << "\n";
    std::cout << "h1_cpu_seconds=" << h1_result.cpu_seconds << "\n";
    std::cout << "h1_wall_seconds=" << h1_result.wall_seconds << "\n";
    std::cout << "h1_evaluations_per_core_second=" << h1_rate << "\n";
    std::cout << "h1_checksum=0x" << std::hex << h1_result.checksum
              << std::dec << "\n";
    std::cout << "h0_character_evaluations=" << h0_result.evaluations << "\n";
    std::cout << "h0_cpu_seconds=" << h0_result.cpu_seconds << "\n";
    std::cout << "h0_wall_seconds=" << h0_result.wall_seconds << "\n";
    std::cout << "h0_evaluations_per_core_second=" << h0_rate << "\n";
    std::cout << "h0_checksum=0x" << std::hex << h0_result.checksum
              << std::dec << "\n";
    std::cout << "combined_evaluations_per_core_second=" << combined_rate
              << "\n";
    std::cout << "ratio_to_17641=" << combined_rate / 17641.0 << "\n";
    std::cout << "ratio_to_164650=" << combined_rate / 164650.0 << "\n";

    constexpr double reuse_total = 78348394368.0;
    constexpr double unbatched_total = 426772416384.0;
    constexpr double support_reductions = 450419940.0;
    const double reuse_single_core =
        reuse_total / combined_rate + support_reductions / factor_rate;
    const double unbatched_single_core =
        unbatched_total / combined_rate + support_reductions / factor_rate;
    std::cout << "projected_reuse_single_core_hours="
              << reuse_single_core / 3600.0 << "\n";
    std::cout << "projected_reuse_ideal_10_core_hours="
              << reuse_single_core / 36000.0 << "\n";
    std::cout << "projected_unbatched_single_core_hours="
              << unbatched_single_core / 3600.0 << "\n";
    std::cout << "projected_unbatched_ideal_10_core_hours="
              << unbatched_single_core / 36000.0 << "\n";
    std::cout << "scope=quadratic_character_front_end_only\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << "\n";
    return 1;
  }
}
