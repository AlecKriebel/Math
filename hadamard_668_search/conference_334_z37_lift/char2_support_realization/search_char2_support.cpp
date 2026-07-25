// Exploratory exact characteristic-two support realization for the
// semiregular C37 conference-matrix route to H(668).
//
// The exact construction works in
//
//   K = F_2[x]/(1+x+...+x^36) = F_(2^36),
//
// where star is x -> x^-1 and the fixed field has order q=2^18.
// A rank-four Hermitian projection E gives
//
//   D = E + eta I,   D^2 + D = I,
//
// with eta the nonresidue quadratic period.  The CRT inverse of each
// (trivial-factor bit, K element) is the exact 37-bit block support.
//
// The program:
//   1. constructs the dense projection attached to a binary quotient;
//   2. uses exact 2x2 unitary rotations to prescribe all nine diagonal
//      supports, including the full 6/3 trace law and quotient margins;
//   3. solves the remaining off-diagonal weight constraints under the
//      diagonal unitary torus as a difference-CSP on the cyclic unit
//      circle of order 2^18+1.
//
// No floating-point arithmetic is used in any certificate check.

#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <optional>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int N = 9;
constexpr int P = 37;
constexpr int DEGREE = 36;
constexpr std::uint64_t FIELD_MASK = (std::uint64_t{1} << DEGREE) - 1;
constexpr std::uint32_t Q = std::uint32_t{1} << 18;
constexpr std::uint32_t CIRCLE_ORDER = Q + 1;

struct Field {
  std::uint64_t value = 0;

  friend bool operator==(Field a, Field b) { return a.value == b.value; }
  friend bool operator!=(Field a, Field b) { return !(a == b); }
  friend Field operator+(Field a, Field b) {
    return Field{a.value ^ b.value};
  }
  Field& operator+=(Field other) {
    value ^= other.value;
    return *this;
  }
};

Field multiply(Field left, Field right) {
  __uint128_t product = 0;
  std::uint64_t bits = left.value;
  while (bits) {
    const int shift = std::countr_zero(bits);
    product ^= static_cast<__uint128_t>(right.value) << shift;
    bits &= bits - 1;
  }
  // Phi_37(x)=x^36+...+x+1, so x^k is replaced by the 36
  // consecutive powers x^(k-36),...,x^(k-1).
  const __uint128_t low_mask =
      (static_cast<__uint128_t>(1) << DEGREE) - 1;
  for (int degree = 2 * DEGREE - 2; degree >= DEGREE; --degree) {
    if ((product >> degree) & 1) {
      product ^= static_cast<__uint128_t>(1) << degree;
      product ^= low_mask << (degree - DEGREE);
    }
  }
  return Field{static_cast<std::uint64_t>(product) & FIELD_MASK};
}

Field square(Field value) { return multiply(value, value); }

Field power(Field base, std::uint64_t exponent) {
  Field result{1};
  while (exponent) {
    if (exponent & 1) result = multiply(result, base);
    base = square(base);
    exponent >>= 1;
  }
  return result;
}

Field inverse(Field value) {
  if (value.value == 0) throw std::runtime_error("inverse of zero");
  return power(value, (std::uint64_t{1} << DEGREE) - 2);
}

Field star(Field value) {
  std::uint64_t result = (value.value & 1);
  if ((value.value >> 1) & 1) result ^= FIELD_MASK;
  for (int degree = 2; degree < DEGREE; ++degree) {
    if ((value.value >> degree) & 1) {
      result ^= std::uint64_t{1} << (P - degree);
    }
  }
  return Field{result};
}

Field relative_trace(Field value) { return value + star(value); }
Field norm(Field value) { return multiply(value, star(value)); }

Field fixed_field_square_root(Field value) {
  // In F_(2^18), sqrt(a)=a^(2^17).
  for (int index = 0; index < 17; ++index) value = square(value);
  return value;
}

bool is_fixed(Field value) { return star(value) == value; }

int absolute_trace_fixed(Field value) {
  if (!is_fixed(value)) {
    throw std::runtime_error("absolute trace input left the fixed field");
  }
  Field trace{};
  Field conjugate = value;
  for (int index = 0; index < 18; ++index) {
    trace += conjugate;
    conjugate = square(conjugate);
  }
  if (trace.value != 0 && trace.value != 1) {
    throw std::runtime_error("absolute trace did not land in F2");
  }
  return static_cast<int>(trace.value);
}

std::uint64_t word_to_bits(Field value, int trivial_bit) {
  const int correction =
      trivial_bit ^ (std::popcount(value.value) & 1);
  const std::uint64_t low =
      value.value ^ (correction ? FIELD_MASK : 0);
  return low | (std::uint64_t(correction) << DEGREE);
}

Field bits_to_field(std::uint64_t bits) {
  Field result{bits & FIELD_MASK};
  if ((bits >> DEGREE) & 1) result.value ^= FIELD_MASK;
  return result;
}

int support_weight(Field value, int trivial_bit) {
  return std::popcount(word_to_bits(value, trivial_bit));
}

bool quadratic_residue(int value) {
  value %= P;
  if (value < 0) value += P;
  if (value == 0) return false;
  int result = 1;
  for (int index = 0; index < 18; ++index) result = result * value % P;
  return result == 1;
}

Field class_indicator(bool residues) {
  std::uint64_t bits = 0;
  for (int value = 1; value < P; ++value) {
    if (quadratic_residue(value) == residues) {
      bits |= std::uint64_t{1} << value;
    }
  }
  return bits_to_field(bits);
}

using Matrix = std::array<std::array<Field, N>, N>;
using IntegerMatrix = std::array<std::array<int, N>, N>;

Matrix multiply_matrix(const Matrix& left, const Matrix& right) {
  Matrix result{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      for (int k = 0; k < N; ++k) {
        result[i][j] += multiply(left[i][k], right[k][j]);
      }
    }
  }
  return result;
}

bool is_hermitian(const Matrix& matrix) {
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      if (matrix[i][j] != star(matrix[j][i])) return false;
    }
  }
  return true;
}

void require(bool condition, const std::string& message) {
  if (!condition) throw std::runtime_error(message);
}

IntegerMatrix quotient_target(int type) {
  if (type == 1) {
    return {{
        {{16, 18, 18, 18, 22, 22, 22, 13, 17}},
        {{18, 16, 18, 18, 22, 22, 13, 22, 17}},
        {{18, 18, 16, 18, 22, 13, 22, 22, 17}},
        {{18, 18, 18, 16, 13, 22, 22, 22, 17}},
        {{22, 22, 22, 13, 18, 17, 17, 17, 18}},
        {{22, 22, 13, 22, 17, 18, 17, 17, 18}},
        {{22, 13, 22, 22, 17, 17, 18, 17, 18}},
        {{13, 22, 22, 22, 17, 17, 17, 18, 18}},
        {{17, 17, 17, 17, 18, 18, 18, 18, 26}},
    }};
  }
  if (type == 2) {
    return {{
        {{24, 20, 20, 20, 18, 18, 16, 15, 15}},
        {{20, 22, 14, 14, 19, 19, 17, 22, 19}},
        {{20, 14, 18, 17, 24, 15, 19, 18, 21}},
        {{20, 14, 17, 18, 15, 24, 19, 18, 21}},
        {{18, 19, 24, 15, 14, 16, 21, 20, 19}},
        {{18, 19, 15, 24, 16, 14, 21, 20, 19}},
        {{16, 17, 19, 19, 21, 21, 20, 21, 12}},
        {{15, 22, 18, 18, 20, 20, 21, 12, 20}},
        {{15, 19, 21, 21, 19, 19, 12, 20, 20}},
    }};
  }
  throw std::runtime_error("unknown quotient target");
}

IntegerMatrix parity_quotient(const IntegerMatrix& quotient) {
  IntegerMatrix result{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) result[i][j] = quotient[i][j] & 1;
  }
  return result;
}

void verify_quotient(const IntegerMatrix& quotient,
                     const IntegerMatrix& parity) {
  for (int i = 0; i < N; ++i) {
    require(parity[i][i] == 0, "binary quotient acquired a loop");
    int row_sum = 0;
    for (int j = 0; j < N; ++j) row_sum += quotient[i][j];
    require(row_sum == 166, "integer quotient row sum changed");
  }
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      int square_plus = parity[i][j];
      for (int k = 0; k < N; ++k) {
        square_plus ^= parity[i][k] & parity[k][j];
      }
      require(square_plus == (1 ^ (i == j)),
              "binary quotient equation changed");
    }
  }
}

// Small integral max flow used only to choose a 9x18 diagonal incidence
// matrix with prescribed row sums and QR/NR column sums.
struct FlowEdge {
  int to;
  int reverse;
  int capacity;
};

void add_flow_edge(std::vector<std::vector<FlowEdge>>& graph,
                   int from, int to, int capacity) {
  FlowEdge forward{to, static_cast<int>(graph[to].size()), capacity};
  FlowEdge reverse{from, static_cast<int>(graph[from].size()), 0};
  graph[from].push_back(forward);
  graph[to].push_back(reverse);
}

std::array<std::uint64_t, N> choose_diagonal_words(
    const IntegerMatrix& quotient) {
  constexpr int column_count = 18;
  const int source = 0;
  const int row_base = 1;
  const int column_base = row_base + N;
  const int sink = column_base + column_count;
  std::vector<std::vector<FlowEdge>> graph(sink + 1);
  int required_flow = 0;
  for (int row = 0; row < N; ++row) {
    require(quotient[row][row] % 2 == 0,
            "diagonal quotient degree is odd");
    const int pair_weight = quotient[row][row] / 2;
    required_flow += pair_weight;
    add_flow_edge(graph, source, row_base + row, pair_weight);
    for (int column = 0; column < column_count; ++column) {
      add_flow_edge(graph, row_base + row, column_base + column, 1);
    }
  }
  for (int column = 0; column < column_count; ++column) {
    const int representative = column + 1;
    const int column_sum =
        quadratic_residue(representative) ? 6 : 3;
    add_flow_edge(graph, column_base + column, sink, column_sum);
  }

  int flow = 0;
  while (true) {
    std::vector<int> parent_vertex(graph.size(), -1);
    std::vector<int> parent_edge(graph.size(), -1);
    std::queue<int> queue;
    queue.push(source);
    parent_vertex[source] = source;
    while (!queue.empty() && parent_vertex[sink] < 0) {
      const int vertex = queue.front();
      queue.pop();
      for (int edge_index = 0;
           edge_index < static_cast<int>(graph[vertex].size());
           ++edge_index) {
        const auto& edge = graph[vertex][edge_index];
        if (edge.capacity > 0 && parent_vertex[edge.to] < 0) {
          parent_vertex[edge.to] = vertex;
          parent_edge[edge.to] = edge_index;
          queue.push(edge.to);
        }
      }
    }
    if (parent_vertex[sink] < 0) break;
    int vertex = sink;
    while (vertex != source) {
      const int previous = parent_vertex[vertex];
      const int edge_index = parent_edge[vertex];
      auto& edge = graph[previous][edge_index];
      --edge.capacity;
      ++graph[vertex][edge.reverse].capacity;
      vertex = previous;
    }
    ++flow;
  }
  require(flow == required_flow && flow == 81,
          "diagonal trace/margin flow is infeasible");

  std::array<std::uint64_t, N> words{};
  for (int row = 0; row < N; ++row) {
    for (int column = 0; column < column_count; ++column) {
      // The row->column forward edge is saturated exactly when selected.
      // Edge zero is the reverse of source->row.
      const auto& edge = graph[row_base + row][column + 1];
      require(edge.to == column_base + column,
              "flow edge order changed");
      if (edge.capacity == 0) {
        const int representative = column + 1;
        words[row] |= std::uint64_t{1} << representative;
        words[row] |= std::uint64_t{1} << (P - representative);
      }
    }
  }
  for (int row = 0; row < N; ++row) {
    require(std::popcount(words[row]) == quotient[row][row],
            "diagonal support has wrong margin");
  }
  for (int value = 1; value < P; ++value) {
    int incidence = 0;
    for (int row = 0; row < N; ++row) {
      incidence += (words[row] >> value) & 1;
    }
    require(incidence == (quadratic_residue(value) ? 6 : 3),
            "diagonal support lost the 6/3 trace law");
  }
  return words;
}

std::array<std::uint64_t, N> randomize_diagonal_words(
    std::array<std::uint64_t, N> words, std::uint64_t seed,
    int switch_attempts = 20000) {
  std::mt19937_64 random(seed);
  for (int attempt = 0; attempt < switch_attempts; ++attempt) {
    int first_row = random() % N;
    int second_row = random() % (N - 1);
    if (second_row >= first_row) ++second_row;
    int first_column = 1 + random() % 18;
    int second_column = 1 + random() % 17;
    if (second_column >= first_column) ++second_column;
    const int a = (words[first_row] >> first_column) & 1;
    const int b = (words[first_row] >> second_column) & 1;
    const int c = (words[second_row] >> first_column) & 1;
    const int d = (words[second_row] >> second_column) & 1;
    if (a == d && b == c && a != b) {
      for (int row : {first_row, second_row}) {
        for (int column : {first_column, second_column}) {
          words[row] ^= std::uint64_t{1} << column;
          words[row] ^= std::uint64_t{1} << (P - column);
        }
      }
    }
  }
  return words;
}

Matrix central_projection(const IntegerMatrix& parity, Field eta) {
  Matrix result{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      result[i][j] = Field{static_cast<std::uint64_t>(parity[i][j])};
      if (i != j) result[i][j] += eta;
    }
  }
  require(is_hermitian(result), "central projection is not Hermitian");
  require(multiply_matrix(result, result) == result,
          "central projection is not idempotent");
  return result;
}

struct Circle {
  std::vector<Field> powers;
  std::unordered_map<std::uint64_t, std::uint32_t> exponent;
  std::unordered_map<std::uint64_t, Field> trace_preimage;
};

Circle build_circle() {
  constexpr std::array<std::uint32_t, 4> prime_divisors =
      {5, 13, 37, 109};
  std::mt19937_64 random(0x66833337ULL);
  Field generator{};
  for (int trial = 0; trial < 10000; ++trial) {
    Field candidate{random() & FIELD_MASK};
    if (candidate.value == 0) continue;
    candidate = power(candidate, Q - 1);
    if (candidate.value == 1) continue;
    bool primitive = true;
    for (std::uint32_t divisor : prime_divisors) {
      if (power(candidate, CIRCLE_ORDER / divisor).value == 1) {
        primitive = false;
        break;
      }
    }
    if (primitive) {
      generator = candidate;
      break;
    }
  }
  require(generator.value != 0, "failed to find unit-circle generator");
  require(norm(generator).value == 1,
          "circle generator has nonunit norm");

  Circle result;
  result.powers.resize(CIRCLE_ORDER);
  result.exponent.reserve(CIRCLE_ORDER * 2);
  result.trace_preimage.reserve(CIRCLE_ORDER);
  Field current{1};
  for (std::uint32_t index = 0; index < CIRCLE_ORDER; ++index) {
    result.powers[index] = current;
    result.exponent.emplace(current.value, index);
    const Field trace = current + star(current);
    result.trace_preimage.emplace(trace.value, current);
    current = multiply(current, generator);
  }
  require(current.value == 1 &&
              result.exponent.size() == CIRCLE_ORDER,
          "unit-circle enumeration changed");
  require(result.trace_preimage.size() == (Q + 2) / 2,
          "unit-circle trace image has wrong size");
  return result;
}

void rotate_projection(Matrix& matrix, int first, int second,
                       Field c, Field u) {
  require(first != second && is_fixed(c) && norm(u).value == 1,
          "invalid unitary rotation parameters");
  const Field s = multiply(u, Field{1} + c);
  require(square(c) + norm(s) == Field{1},
          "2x2 rotation is not unitary");

  Matrix left = matrix;
  for (int column = 0; column < N; ++column) {
    left[first][column] =
        multiply(c, matrix[first][column]) +
        multiply(s, matrix[second][column]);
    left[second][column] =
        multiply(star(s), matrix[first][column]) +
        multiply(c, matrix[second][column]);
  }
  Matrix result = left;
  for (int row = 0; row < N; ++row) {
    result[row][first] =
        multiply(left[row][first], c) +
        multiply(left[row][second], star(s));
    result[row][second] =
        multiply(left[row][first], s) +
        multiply(left[row][second], c);
  }
  matrix = result;
}

Field random_fixed(std::mt19937_64& random) {
  return relative_trace(Field{random() & FIELD_MASK});
}

// Set one diagonal entry exactly by a unitary rotation with a pivot
// coordinate.  The trace-image lookup replaces a 2^36 search by a handful
// of fixed-field trials.
bool set_diagonal_entry(Matrix& matrix, int index, int pivot, Field target,
                        const Circle& circle,
                        std::mt19937_64& random) {
  const Field a = matrix[index][index];
  const Field d = matrix[pivot][pivot];
  const Field b = matrix[index][pivot];
  require(is_fixed(a) && is_fixed(d) && is_fixed(target),
          "diagonal entry left the fixed field");

  if (b.value == 0) {
    const Field sum = a + d;
    if (sum.value == 0) return target == a;
    const Field ratio = multiply(target + d, inverse(sum));
    const Field c = fixed_field_square_root(ratio);
    rotate_projection(matrix, index, pivot, c, Field{1});
    return matrix[index][index] == target;
  }

  const Field n = fixed_field_square_root(norm(b));
  require(n.value != 0 && is_fixed(n), "off-diagonal norm vanished");
  const Field n_inverse = inverse(n);
  const Field v = multiply(b, n_inverse);
  require(norm(v).value == 1, "normalized off-diagonal is not unitary");

  for (int trial = 0; trial < 10000; ++trial) {
    const Field c = random_fixed(random);
    if (c.value == 0 || c.value == 1) continue;
    const Field one_plus_c = Field{1} + c;
    const Field denominator = multiply(c, one_plus_c);
    const Field numerator =
        target + multiply(square(c), a) +
        multiply(square(one_plus_c), d);
    const Field required_trace =
        multiply(numerator, inverse(denominator));
    const Field normalized_trace =
        multiply(required_trace, n_inverse);
    const auto found =
        circle.trace_preimage.find(normalized_trace.value);
    if (found == circle.trace_preimage.end()) continue;
    const Field w = found->second;
    const Field u = multiply(star(w), v);
    require(norm(u).value == 1,
            "recovered rotation phase is not unitary");
    Matrix candidate = matrix;
    rotate_projection(candidate, index, pivot, c, u);
    if (candidate[index][index] == target) {
      matrix = candidate;
      return true;
    }
  }
  return false;
}

void prescribe_diagonal(Matrix& projection,
                        const std::array<Field, N>& target,
                        const Circle& circle,
                        std::uint64_t seed) {
  Field target_sum{};
  for (Field entry : target) target_sum += entry;
  require(target_sum.value == 0,
          "target diagonal has wrong projection trace");

  std::mt19937_64 random(seed);
  for (int index = 0; index < N - 1; ++index) {
    int pivot = N - 1;
    if (!set_diagonal_entry(
            projection, index, pivot, target[index], circle, random)) {
      bool recovered = false;
      for (int alternate = index + 1; alternate < N; ++alternate) {
        if (set_diagonal_entry(
                projection, index, alternate, target[index],
                circle, random)) {
          recovered = true;
          break;
        }
      }
      require(recovered, "failed to prescribe a diagonal coordinate");
    }
    require(projection[index][index] == target[index],
            "diagonal prescription drifted");
  }
  for (int index = 0; index < N; ++index) {
    require(projection[index][index] == target[index],
            "terminal diagonal prescription failed");
  }
  require(is_hermitian(projection),
          "diagonalized projection is not Hermitian");
  require(multiply_matrix(projection, projection) == projection,
          "diagonalized projection is not idempotent");
}

int required_norm_trace(int support_size) {
  return (support_size * (support_size - 1) / 2) & 1;
}

int norm_trace_score(Field value, int target_weight) {
  if (value.value == 0) {
    // Norm zero is itself trace zero.
    return required_norm_trace(target_weight);
  }
  return absolute_trace_fixed(norm(value)) ^
         required_norm_trace(target_weight);
}

int norm_trace_projection_score(const Matrix& projection,
                                const IntegerMatrix& quotient) {
  int score = 0;
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      score += norm_trace_score(projection[i][j], quotient[i][j]);
    }
  }
  return score;
}

Matrix improve_norm_weight_compatibility(
    Matrix projection, const IntegerMatrix& quotient,
    const IntegerMatrix&, const Circle& circle,
    std::uint64_t seed, int* final_score) {
  std::mt19937_64 random(seed);
  std::array<std::array<int, N>, N> edge_score{};
  int score = 0;
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      edge_score[i][j] =
          norm_trace_score(projection[i][j], quotient[i][j]);
      score += edge_score[i][j];
    }
  }
  Matrix best = projection;
  int best_score = score;
  constexpr int iteration_count = 30000;
  for (int iteration = 0; iteration < iteration_count; ++iteration) {
    int first = random() % N;
    int second = random() % (N - 1);
    if (second >= first) ++second;
    if (first > second) std::swap(first, second);
    Matrix candidate = projection;
    if (!set_diagonal_entry(
            candidate, first, second, projection[first][first],
            circle, random)) {
      continue;
    }
    int candidate_score = score;
    std::array<std::array<int, N>, N> changed_score{};
    for (int i = 0; i < N; ++i) {
      for (int j = i + 1; j < N; ++j) {
        if (i != first && i != second &&
            j != first && j != second) {
          continue;
        }
        changed_score[i][j] =
            norm_trace_score(candidate[i][j], quotient[i][j]);
        candidate_score += changed_score[i][j] - edge_score[i][j];
      }
    }
    bool accept = candidate_score <= score;
    if (!accept) {
      // A small, integer simulated-annealing tail prevents immediate
      // trapping without introducing floating-point certificate logic.
      const int temperature =
          1 + 12 * (iteration_count - iteration) / iteration_count;
      const int difference = candidate_score - score;
      accept = static_cast<int>(random() % (temperature + difference)) <
               temperature;
    }
    if (accept) {
      projection = candidate;
      score = candidate_score;
      for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
          if (i == first || i == second ||
              j == first || j == second) {
            edge_score[i][j] = changed_score[i][j];
          }
        }
      }
    }
    if (candidate_score < best_score) {
      best = candidate;
      best_score = candidate_score;
      if (best_score == 0) break;
    }
  }
  // At a nonzero local minimum the mismatch edges form an even cycle.
  // Search individual diagonal-preserving rotations more intensively to
  // realize a cycle cancellation.
  for (int sweep = 0; sweep < 8 && best_score != 0; ++sweep) {
    bool improved = false;
    for (int first = 0; first < N && !improved; ++first) {
      for (int second = first + 1; second < N && !improved; ++second) {
        for (int trial = 0; trial < 4000; ++trial) {
          Matrix candidate = best;
          if (!set_diagonal_entry(
                  candidate, first, second, best[first][first],
                  circle, random)) {
            continue;
          }
          const int candidate_score =
              norm_trace_projection_score(candidate, quotient);
          if (candidate_score < best_score) {
            best = candidate;
            best_score = candidate_score;
            improved = true;
            break;
          }
        }
      }
    }
    if (!improved) break;
  }
  *final_score = best_score;
  require(is_hermitian(best) &&
              multiply_matrix(best, best) == best,
          "norm-compatible walk left the projection variety");
  return best;
}

using Allowed = std::array<std::array<std::vector<std::uint8_t>, N>, N>;

Allowed build_allowed_differences(const Matrix& projection,
                                  const IntegerMatrix& quotient,
                                  const IntegerMatrix& parity,
                                  const Circle& circle) {
  Allowed allowed;
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      allowed[i][j].assign(CIRCLE_ORDER, 0);
    }
  }
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      require(projection[i][j].value != 0,
              "phase CSP encountered a zero off-diagonal");
      for (std::uint32_t difference = 0;
           difference < CIRCLE_ORDER; ++difference) {
        const Field value =
            multiply(circle.powers[difference], projection[i][j]);
        if (support_weight(value, parity[i][j]) == quotient[i][j]) {
          allowed[i][j][difference] = 1;
          allowed[j][i][
              difference == 0 ? 0 : CIRCLE_ORDER - difference] = 1;
        }
      }
    }
  }
  return allowed;
}

struct PhaseSearch {
  const Allowed& allowed;
  std::array<std::uint32_t, N> exponent{};
  std::array<bool, N> assigned{};
  std::uint64_t nodes = 0;
  std::uint64_t node_limit = 100000000;
  std::mt19937_64 random{0x668C37F2ULL};

  bool search(int depth) {
    if (++nodes > node_limit) return false;
    if (depth == N) return true;

    int vertex = -1;
    std::vector<std::uint32_t> candidates;
    std::size_t best_size = std::numeric_limits<std::size_t>::max();
    for (int trial_vertex = 1; trial_vertex < N; ++trial_vertex) {
      if (assigned[trial_vertex]) continue;
      std::vector<std::uint32_t> trial;
      trial.reserve(CIRCLE_ORDER / 8);
      for (std::uint32_t value = 0; value < CIRCLE_ORDER; ++value) {
        bool valid = true;
        for (int previous = 0; previous < N; ++previous) {
          if (!assigned[previous]) continue;
          const std::uint32_t difference =
              (exponent[previous] + CIRCLE_ORDER - value) %
              CIRCLE_ORDER;
          if (!allowed[previous][trial_vertex][difference]) {
            valid = false;
            break;
          }
        }
        if (valid) trial.push_back(value);
      }
      if (trial.size() < best_size) {
        best_size = trial.size();
        vertex = trial_vertex;
        candidates = std::move(trial);
      }
      if (best_size == 0) break;
    }
    if (vertex < 0 || candidates.empty()) return false;
    std::shuffle(candidates.begin(), candidates.end(), random);
    assigned[vertex] = true;
    for (std::uint32_t value : candidates) {
      exponent[vertex] = value;
      if (search(depth + 1)) return true;
    }
    assigned[vertex] = false;
    return false;
  }
};

Matrix apply_phases(const Matrix& projection,
                    const std::array<std::uint32_t, N>& exponents,
                    const Circle& circle) {
  Matrix result{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      result[i][j] = multiply(
          multiply(circle.powers[exponents[i]], projection[i][j]),
          star(circle.powers[exponents[j]]));
    }
  }
  return result;
}

using WordMatrix =
    std::array<std::array<std::uint64_t, N>, N>;

WordMatrix support_words(
    const Matrix& projection,
    const std::array<std::uint32_t, N>& exponents,
    const IntegerMatrix& parity, Field eta, const Circle& circle) {
  Matrix phased = apply_phases(projection, exponents, circle);
  for (int i = 0; i < N; ++i) phased[i][i] += eta;
  WordMatrix words{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      words[i][j] = word_to_bits(phased[i][j], parity[i][j]);
    }
  }
  return words;
}

int integer_convolution_coefficient(std::uint64_t left,
                                    std::uint64_t right, int lag) {
  int result = 0;
  for (int source = 0; source < P; ++source) {
    result += ((left >> source) & 1) *
              ((right >> ((lag - source + P) % P)) & 1);
  }
  return result;
}

int mod4_carry_defects(
    const Matrix& projection,
    const std::array<std::uint32_t, N>& exponents,
    const IntegerMatrix& parity, Field eta, const Circle& circle) {
  const WordMatrix words =
      support_words(projection, exponents, parity, eta, circle);
  int defects = 0;
  int constraints = 0;
  for (int i = 0; i < N; ++i) {
    for (int j = i; j < N; ++j) {
      const int lag_limit = i == j ? 19 : P;
      for (int lag = 0; lag < lag_limit; ++lag) {
        int value = (words[i][j] >> lag) & 1;
        for (int middle = 0; middle < N; ++middle) {
          value += integer_convolution_coefficient(
              words[i][middle], words[middle][j], lag);
        }
        const int target =
            83 * (1 + ((i == j && lag == 0) ? 1 : 0));
        const int residue = (value - target) & 3;
        require((residue & 1) == 0,
                "phase assignment lost the mod-two equation");
        defects += residue != 0;
        ++constraints;
      }
    }
  }
  require(constraints == 1503, "mod-four carry shape changed");
  return defects;
}

bool phase_assignment_valid(
    const std::array<std::uint32_t, N>& exponents,
    const Allowed& allowed) {
  for (int i = 0; i < N; ++i) {
    for (int j = i + 1; j < N; ++j) {
      const std::uint32_t difference =
          (exponents[i] + CIRCLE_ORDER - exponents[j]) %
          CIRCLE_ORDER;
      if (!allowed[i][j][difference]) return false;
    }
  }
  return true;
}

struct PhaseOptimization {
  std::array<std::uint32_t, N> exponents{};
  int initial_defects = -1;
  int best_defects = -1;
  std::uint64_t proposals = 0;
  std::uint64_t conditional_trials = 0;
};

PhaseOptimization optimize_mod4_carry(
    const Matrix& projection,
    std::array<std::uint32_t, N> exponents,
    const Allowed& allowed, const IntegerMatrix& parity,
    Field eta, const Circle& circle, int iterations) {
  require(phase_assignment_valid(exponents, allowed),
          "initial phase assignment is invalid");
  PhaseOptimization report;
  report.exponents = exponents;
  int current_defects =
      mod4_carry_defects(projection, exponents, parity, eta, circle);
  report.initial_defects = report.best_defects = current_defects;
  std::mt19937_64 random(0xC344668ULL);

  for (int iteration = 0; iteration < iterations; ++iteration) {
    const int vertex = 1 + random() % (N - 1);
    std::optional<std::uint32_t> replacement;
    for (int trial = 0; trial < 500000; ++trial) {
      ++report.conditional_trials;
      const std::uint32_t value = random() % CIRCLE_ORDER;
      if (value == exponents[vertex]) continue;
      bool valid = true;
      for (int other = 0; other < N; ++other) {
        if (other == vertex) continue;
        const int first = std::min(vertex, other);
        const int second = std::max(vertex, other);
        const std::uint32_t difference =
            first == vertex
                ? (value + CIRCLE_ORDER - exponents[other]) %
                      CIRCLE_ORDER
                : (exponents[other] + CIRCLE_ORDER - value) %
                      CIRCLE_ORDER;
        if (!allowed[first][second][difference]) {
          valid = false;
          break;
        }
      }
      if (valid) {
        replacement = value;
        break;
      }
    }
    if (!replacement) continue;
    auto candidate = exponents;
    candidate[vertex] = *replacement;
    ++report.proposals;
    const int candidate_defects =
        mod4_carry_defects(projection, candidate, parity, eta, circle);

    bool accept = candidate_defects <= current_defects;
    if (!accept) {
      const int temperature =
          1 + 24 * (iterations - iteration) / std::max(1, iterations);
      const int increase = candidate_defects - current_defects;
      accept = static_cast<int>(random() % (temperature + 4 * increase)) <
               temperature;
    }
    if (accept) {
      exponents = candidate;
      current_defects = candidate_defects;
    }
    if (candidate_defects < report.best_defects) {
      report.best_defects = candidate_defects;
      report.exponents = candidate;
      std::cerr << "carry_improvement iteration " << iteration
                << " defects " << report.best_defects << "\n";
    }
  }
  require(phase_assignment_valid(report.exponents, allowed),
          "optimized phase assignment is invalid");
  return report;
}

void verify_full_support(const Matrix& projection,
                         const IntegerMatrix& quotient,
                         const IntegerMatrix& parity, Field eta,
                         const std::array<std::uint64_t, N>& diagonal_words) {
  require(is_hermitian(projection), "final projection is not Hermitian");
  require(multiply_matrix(projection, projection) == projection,
          "final projection is not idempotent");
  Matrix d = projection;
  for (int i = 0; i < N; ++i) d[i][i] += eta;

  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      require(support_weight(d[i][j], parity[i][j]) == quotient[i][j],
              "final support has a wrong quotient margin");
      const std::uint64_t word =
          word_to_bits(d[i][j], parity[i][j]);
      const std::uint64_t reverse =
          word_to_bits(d[j][i], parity[j][i]);
      for (int value = 0; value < P; ++value) {
        require(((word >> value) & 1) ==
                    ((reverse >> ((P - value) % P)) & 1),
                "final support lost star symmetry");
      }
    }
    require(word_to_bits(d[i][i], 0) == diagonal_words[i],
            "final diagonal word changed");
  }

  // Verify D^2+D=I directly in K and in every one of the 37 binary
  // coefficient positions via cyclic convolution.
  Matrix residual = multiply_matrix(d, d);
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      residual[i][j] += d[i][j];
      require(residual[i][j] == Field{static_cast<std::uint64_t>(i == j)},
              "final D factor equation failed");
    }
  }

  std::array<std::array<std::uint64_t, N>, N> words{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      words[i][j] = word_to_bits(d[i][j], parity[i][j]);
    }
  }
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      for (int lag = 0; lag < P; ++lag) {
        int coefficient = (words[i][j] >> lag) & 1;
        for (int k = 0; k < N; ++k) {
          for (int source = 0; source < P; ++source) {
            const int target = (lag - source + P) % P;
            coefficient ^=
                ((words[i][k] >> source) & 1) &
                ((words[k][j] >> target) & 1);
          }
        }
        // In the full group algebra the adjacency equation is
        // D^2+D=delta*I+all_ones_group*J.  Thus every coefficient has
        // J, and lag zero additionally has I.
        const int rhs = 1 ^ ((i == j) && lag == 0);
        require(coefficient == rhs,
                "binary cyclic-convolution equation failed");
      }
    }
  }
}

void emit_certificate(const Matrix& projection,
                      const IntegerMatrix& quotient,
                      const IntegerMatrix& parity, Field eta,
                      const std::array<std::uint64_t, N>& diagonal_words,
                      const PhaseSearch& search) {
  Matrix d = projection;
  for (int i = 0; i < N; ++i) d[i][i] += eta;
  std::cout << "status PASS\n";
  std::cout << "phase_search_nodes " << search.nodes << "\n";
  std::cout << "phase_exponents";
  for (std::uint32_t exponent : search.exponent)
    std::cout << " " << exponent;
  std::cout << "\n";
  std::cout << "diagonal_words_hex";
  for (std::uint64_t word : diagonal_words)
    std::cout << " " << std::hex << word << std::dec;
  std::cout << "\n";
  for (int i = 0; i < N; ++i) {
    for (int j = i; j < N; ++j) {
      const std::uint64_t word =
          word_to_bits(d[i][j], parity[i][j]);
      std::cout << "block " << i << " " << j << " "
                << std::hex << word << std::dec << " "
                << std::popcount(word) << " " << quotient[i][j] << "\n";
    }
  }
}

void verify_field_model(Field eta) {
  require(power(Field{2}, P).value == 1,
          "the polynomial generator is not a 37th root");
  require(power(Field{2}, 1).value != 1,
          "the polynomial generator is trivial");
  std::mt19937_64 random(0xF23637ULL);
  for (int trial = 0; trial < 10000; ++trial) {
    const Field a{random() & FIELD_MASK};
    const Field b{random() & FIELD_MASK};
    require(star(star(a)) == a, "star is not an involution");
    require(star(multiply(a, b)) == multiply(star(a), star(b)),
            "star is not multiplicative");
    require(is_fixed(norm(a)), "norm left the fixed field");
    const int q = random() & 1;
    require(bits_to_field(word_to_bits(a, q)) == a,
            "CRT word round trip failed");
    require((std::popcount(word_to_bits(a, q)) & 1) == q,
            "CRT trivial factor changed");
  }
  const Field residues = class_indicator(true);
  require(eta == class_indicator(false),
          "nonresidue period changed");
  require(residues + eta == Field{1},
          "quadratic periods no longer sum to one");
  require(square(eta) + eta == Field{1},
          "quadratic period polynomial changed");
}

}  // namespace

int main(int argc, char** argv) {
  const int quotient_type = argc >= 2 ? std::stoi(argv[1]) : 1;
  const int carry_iterations = argc >= 3 ? std::stoi(argv[2]) : 0;
  require(quotient_type == 1 || quotient_type == 2,
          "usage: search_char2_support [1|2] [carry_iterations]");
  require(carry_iterations >= 0,
          "carry iteration count must be nonnegative");
  const auto started = std::chrono::steady_clock::now();
  const Field eta = class_indicator(false);
  verify_field_model(eta);

  const IntegerMatrix quotient = quotient_target(quotient_type);
  const IntegerMatrix parity = parity_quotient(quotient);
  verify_quotient(quotient, parity);

  const auto base_diagonal_words = choose_diagonal_words(quotient);

  const Circle circle = build_circle();
  Matrix projection{};
  std::array<std::uint64_t, N> solved_diagonal_words{};
  std::optional<Allowed> solved_allowed;
  std::optional<PhaseSearch> solved_search;
  for (int attempt = 0; attempt < 100; ++attempt) {
    const auto diagonal_words = randomize_diagonal_words(
        base_diagonal_words,
        0xD1A637668ULL +
            0x94d049bb133111ebULL * static_cast<std::uint64_t>(attempt));
    std::array<Field, N> target_diagonal{};
    for (int i = 0; i < N; ++i) {
      target_diagonal[i] = bits_to_field(diagonal_words[i]) + eta;
      require(word_to_bits(target_diagonal[i] + eta, 0) ==
                  diagonal_words[i],
              "target diagonal CRT conversion failed");
    }
    Matrix candidate = central_projection(parity, eta);
    prescribe_diagonal(
        candidate, target_diagonal, circle,
        0xC372668333ULL +
            0x9e3779b97f4a7c15ULL * static_cast<std::uint64_t>(attempt));
    int norm_trace_mismatch_score = -1;
    candidate = improve_norm_weight_compatibility(
        candidate, quotient, parity, circle,
        0xA11F236668ULL +
            0xd1b54a32d192ed03ULL * static_cast<std::uint64_t>(attempt),
        &norm_trace_mismatch_score);
    std::cerr << "diagonal_attempt " << attempt
              << " norm_trace_mismatch_score "
              << norm_trace_mismatch_score << "\n";
    Allowed allowed =
        build_allowed_differences(candidate, quotient, parity, circle);
    bool nonempty = true;
    long double expected_log2 = 8.0L * 18.0L;
    std::array<std::array<std::size_t, N>, N> counts{};
    for (int i = 0; i < N; ++i) {
      for (int j = i + 1; j < N; ++j) {
        counts[i][j] = std::count(
            allowed[i][j].begin(), allowed[i][j].end(),
            std::uint8_t{1});
        if (counts[i][j] == 0) {
          nonempty = false;
          if (attempt < 3) {
            std::cerr << "empty_edge " << i << " " << j
                      << " target " << quotient[i][j]
                      << " parity " << parity[i][j]
                      << " value " << candidate[i][j].value
                      << " norm " << norm(candidate[i][j]).value
                      << "\n";
          }
        } else {
          expected_log2 +=
              std::log2(static_cast<long double>(counts[i][j]) /
                        static_cast<long double>(CIRCLE_ORDER));
        }
      }
    }
    std::cerr << "diagonal_attempt " << attempt
              << " all_edge_domains_nonempty " << nonempty
              << " independent_log2 " << static_cast<double>(expected_log2)
              << "\n";
    if (!nonempty) continue;

    PhaseSearch search{allowed};
    search.assigned[0] = true;
    search.exponent[0] = 0;
    if (!search.search(1)) {
      std::cerr << "phase_nodes " << search.nodes << " unsolved\n";
      continue;
    }
    std::cerr << "phase_nodes " << search.nodes << " solved\n";
    for (int i = 0; i < N; ++i) {
      for (int j = i + 1; j < N; ++j) {
        std::cerr << "allowed " << i << " " << j << " "
                  << counts[i][j] << " / " << CIRCLE_ORDER << "\n";
      }
    }
    projection = candidate;
    solved_diagonal_words = diagonal_words;
    solved_allowed.emplace(std::move(allowed));
    solved_search.emplace(*solved_allowed);
    solved_search->exponent = search.exponent;
    solved_search->assigned = search.assigned;
    solved_search->nodes = search.nodes;
    break;
  }
  require(solved_search.has_value(),
          "no diagonal realization yielded a solved phase CSP");
  std::optional<PhaseOptimization> carry_report;
  if (carry_iterations > 0) {
    carry_report = optimize_mod4_carry(
        projection, solved_search->exponent, *solved_allowed,
        parity, eta, circle, carry_iterations);
    solved_search->exponent = carry_report->exponents;
  }
  projection =
      apply_phases(projection, solved_search->exponent, circle);
  verify_full_support(
      projection, quotient, parity, eta, solved_diagonal_words);
  emit_certificate(
      projection, quotient, parity, eta, solved_diagonal_words,
      *solved_search);
  std::cout << "quotient_type " << quotient_type << "\n";
  if (carry_report) {
    std::cout << "carry_optimization_iterations "
              << carry_iterations << "\n";
    std::cout << "carry_initial_defects "
              << carry_report->initial_defects << "\n";
    std::cout << "carry_best_defects "
              << carry_report->best_defects << "\n";
    std::cout << "carry_proposals " << carry_report->proposals << "\n";
    std::cout << "carry_conditional_trials "
              << carry_report->conditional_trials << "\n";
  }

  const double seconds =
      std::chrono::duration<double>(
          std::chrono::steady_clock::now() - started)
          .count();
  std::cerr << "elapsed_seconds " << seconds << "\n";
  return 0;
}
