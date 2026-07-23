// Independent exhaustive verifier for the LP(333) mixed neighborhood.
//
// For each alternating six-cycle in one 9 by 37 CRT sign matrix, this program
// tests every legal 2 by 2 checkerboard switch in the other matrix.  Unlike
// the search engine, it uses neither a kd-tree nor bounding-box pruning: the
// complete Cartesian product is evaluated by a direct exact-integer dot
// product.  Only the roughly 3,000 opposite-sequence checker deltas and one
// work vector are retained, so memory use is small and independent of the
// number of cycles.

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 333;
constexpr int ROWS = 9;
constexpr int COLS = 37;
constexpr int LAST_LAG = 166;

using Signs = std::array<int8_t, N>;
using Sequences = std::array<Signs, 2>;
using Residuals = std::array<int16_t, LAST_LAG + 1>;
using Delta = std::array<int16_t, LAST_LAG + 1>;
using SingleDeltas = std::array<std::array<int8_t, LAST_LAG + 1>, N>;
using RowSums = std::array<std::array<int, ROWS>, 2>;

struct TemporaryChecker {
  std::array<uint16_t, 4> positions{};
  Delta delta{};
};

// Checker deltas are stored coordinate-major.  A query therefore performs
// one contiguous, vectorizable pass over all checkers for each of 166 lags.
struct CheckerSet {
  std::vector<std::array<uint16_t, 4>> positions;
  std::vector<int8_t> delta_by_lag;
  std::vector<int32_t> norm_squared;

  size_t size() const { return positions.size(); }
};

struct QueryResult {
  int minimum_energy = std::numeric_limits<int>::max();
  size_t minimum_index = 0;
  uint64_t minimum_multiplicity = 0;
  uint64_t below_baseline = 0;
  uint64_t at_baseline = 0;
};

struct MixedAudit {
  std::array<uint64_t, 2> raw_patterns{};
  std::array<uint64_t, 2> legal_cycles{};
  uint64_t evaluated_pairs = 0;
  uint64_t below_baseline = 0;
  uint64_t at_baseline = 0;
  uint64_t scalar_cross_checks = 0;
  int minimum_energy = std::numeric_limits<int>::max();
  uint64_t minimum_multiplicity = 0;
  int best_cycle_sequence = -1;
  std::array<uint16_t, 6> best_cycle_positions{};
  std::array<uint16_t, 4> best_checker_positions{};
};

struct EightAudit {
  std::array<uint64_t, 2> raw_assignments{};
  std::array<uint64_t, 2> legal_cycles{};
  std::array<uint64_t, 2> repeated_column_assignments{};
  uint64_t below_baseline = 0;
  uint64_t at_baseline = 0;
  int minimum_energy = std::numeric_limits<int>::max();
  uint64_t minimum_multiplicity = 0;
  int best_sequence = -1;
  std::array<uint16_t, 8> best_positions{};
};

constexpr std::array<std::array<int, 3>, 6> PERMUTATIONS{{
    {{0, 1, 2}}, {{0, 2, 1}}, {{1, 0, 2}},
    {{1, 2, 0}}, {{2, 0, 1}}, {{2, 1, 0}},
}};

constexpr std::array<std::array<int, 4>, 3> ROW_CYCLES_4{{
    {{0, 1, 2, 3}}, {{0, 1, 3, 2}}, {{0, 2, 1, 3}},
}};

std::array<std::array<int, COLS>, ROWS> make_crt_table() {
  std::array<std::array<int, COLS>, ROWS> result{};
  for (int row = 0; row < ROWS; ++row)
    for (int column = 0; column < COLS; ++column)
      result[row][column] =
          column + COLS * (((row - column) % ROWS + ROWS) % ROWS);
  return result;
}

const auto CRT = make_crt_table();

int cyclic_distance(int left, int right) {
  const int raw = std::abs(left - right);
  return std::min(raw, N - raw);
}

int legendre_symbol_37(int value) {
  value %= COLS;
  if (value < 0) value += COLS;
  if (value == 0) return 0;
  int power = 1;
  for (int exponent = 0; exponent < 18; ++exponent)
    power = power * value % COLS;
  if (power == 1) return 1;
  if (power == COLS - 1) return -1;
  throw std::runtime_error("Euler-criterion failure");
}

size_t unique_field(const std::string &document, const std::string &key) {
  const std::string needle = "\"" + key + "\"";
  const size_t found = document.find(needle);
  if (found == std::string::npos)
    throw std::runtime_error("checkpoint has no " + key);
  if (document.find(needle, found + needle.size()) != std::string::npos)
    throw std::runtime_error("checkpoint repeats " + key);
  return found;
}

std::vector<int> extract_array(const std::string &document,
                               const std::string &key) {
  const size_t key_at = unique_field(document, key);
  const size_t begin = document.find('[', key_at + key.size() + 2);
  const size_t end = begin == std::string::npos
                         ? std::string::npos
                         : document.find(']', begin + 1);
  if (begin == std::string::npos || end == std::string::npos)
    throw std::runtime_error("malformed checkpoint array " + key);
  std::vector<int> result;
  size_t at = begin + 1;
  while (at < end) {
    while (at < end &&
           !std::isdigit(static_cast<unsigned char>(document[at])) &&
           document[at] != '-')
      ++at;
    if (at >= end) break;
    size_t consumed = 0;
    result.push_back(std::stoi(document.substr(at, end - at), &consumed));
    at += consumed;
  }
  return result;
}

int64_t extract_integer(const std::string &document, const std::string &key) {
  const size_t key_at = unique_field(document, key);
  const size_t colon = document.find(':', key_at + key.size() + 2);
  if (colon == std::string::npos)
    throw std::runtime_error("malformed checkpoint integer " + key);
  size_t at = colon + 1;
  while (at < document.size() &&
         std::isspace(static_cast<unsigned char>(document[at])))
    ++at;
  size_t consumed = 0;
  const int64_t result = std::stoll(document.substr(at), &consumed);
  const size_t after = at + consumed;
  if (after >= document.size() ||
      (document[after] != ',' && document[after] != '}' &&
       !std::isspace(static_cast<unsigned char>(document[after]))))
    throw std::runtime_error("checkpoint field is not an integer: " + key);
  return result;
}

bool extract_boolean(const std::string &document, const std::string &key) {
  const size_t key_at = unique_field(document, key);
  const size_t colon = document.find(':', key_at + key.size() + 2);
  if (colon == std::string::npos)
    throw std::runtime_error("malformed checkpoint Boolean " + key);
  size_t at = colon + 1;
  while (at < document.size() &&
         std::isspace(static_cast<unsigned char>(document[at])))
    ++at;
  if (document.compare(at, 4, "true") == 0) return true;
  if (document.compare(at, 5, "false") == 0) return false;
  throw std::runtime_error("checkpoint field is not Boolean: " + key);
}

Sequences parse_sequences(const std::string &document) {
  const auto raw_a = extract_array(document, "a");
  const auto raw_b = extract_array(document, "b");
  if (raw_a.size() != N || raw_b.size() != N)
    throw std::runtime_error("checkpoint sign-vector length mismatch");
  Sequences sequences{};
  for (int index = 0; index < N; ++index) {
    if ((raw_a[index] != -1 && raw_a[index] != 1) ||
        (raw_b[index] != -1 && raw_b[index] != 1))
      throw std::runtime_error("checkpoint contains a non-sign entry");
    sequences[0][index] = static_cast<int8_t>(raw_a[index]);
    sequences[1][index] = static_cast<int8_t>(raw_b[index]);
  }
  return sequences;
}

RowSums verify_exact_profile_margins(const Sequences &sequences) {
  RowSums row_sums{};
  for (int which = 0; which < 2; ++which) {
    int total = 0;
    for (int row = 0; row < ROWS; ++row) {
      for (int column = 0; column < COLS; ++column)
        row_sums[which][row] += sequences[which][CRT[row][column]];
      total += row_sums[which][row];
    }
    if (total != 1) throw std::runtime_error("sequence sum is not one");
    for (int column = 0; column < COLS; ++column) {
      int column_sum = 0;
      for (int row = 0; row < ROWS; ++row)
        column_sum += sequences[which][CRT[row][column]];
      const int expected = column == 0
          ? 1
          : (which == 0 ? 3 : -3) * legendre_symbol_37(column);
      if (column_sum != expected)
        throw std::runtime_error("fixed Legendre column-margin mismatch");
    }
  }

  for (int lag = 0; lag < ROWS; ++lag) {
    int paf = 0;
    for (int which = 0; which < 2; ++which)
      for (int row = 0; row < ROWS; ++row)
        paf += row_sums[which][row] *
               row_sums[which][(row + lag) % ROWS];
    if (paf != (lag == 0 ? 594 : -74))
      throw std::runtime_error("combined mod-9 PAF profile mismatch");
  }
  return row_sums;
}

Residuals recompute_residuals(const Sequences &sequences) {
  Residuals residual{};
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int paf = 0;
    for (const Signs &sequence : sequences)
      for (int position = 0; position < N; ++position)
        paf += sequence[position] * sequence[(position + lag) % N];
    if ((paf + 2) % 4 != 0)
      throw std::runtime_error("combined PAF violates mod-four parity");
    residual[lag] = static_cast<int16_t>((paf + 2) / 2);
  }
  return residual;
}

int energy(const Residuals &residual) {
  int result = 0;
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    result += residual[lag] * residual[lag];
  return result;
}

SingleDeltas make_single_deltas(const Signs &sequence) {
  SingleDeltas result{};
  for (int position = 0; position < N; ++position)
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      result[position][lag] = static_cast<int8_t>(
          -sequence[position] *
          (sequence[(position + lag) % N] +
           sequence[(position - lag + N) % N]));
  return result;
}

template <size_t Size>
Delta exact_delta(const Signs &sequence, const SingleDeltas &single,
                  const std::array<uint16_t, Size> &positions) {
  Delta result{};
  for (uint16_t position : positions)
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      result[lag] += single[position][lag];
  for (size_t left = 0; left < Size; ++left)
    for (size_t right = left + 1; right < Size; ++right) {
      const int lag = cyclic_distance(positions[left], positions[right]);
      if (lag <= 0 || lag > LAST_LAG)
        throw std::runtime_error("flip support repeats a position");
      result[lag] += static_cast<int16_t>(
          2 * sequence[positions[left]] * sequence[positions[right]]);
    }
  return result;
}

bool checkerboard(const Signs &sequence, int row1, int row2,
                  int column1, int column2) {
  const int a = sequence[CRT[row1][column1]];
  const int b = sequence[CRT[row1][column2]];
  const int c = sequence[CRT[row2][column1]];
  const int d = sequence[CRT[row2][column2]];
  return a == d && b == c && a != b;
}

CheckerSet enumerate_checkers(const Signs &sequence,
                              const SingleDeltas &single) {
  std::vector<TemporaryChecker> temporary;
  temporary.reserve(3200);
  for (int row1 = 0; row1 < ROWS; ++row1)
    for (int row2 = row1 + 1; row2 < ROWS; ++row2)
      for (int column1 = 0; column1 < COLS; ++column1)
        for (int column2 = column1 + 1; column2 < COLS; ++column2) {
          if (!checkerboard(sequence, row1, row2, column1, column2)) continue;
          TemporaryChecker checker;
          checker.positions = {{
              static_cast<uint16_t>(CRT[row1][column1]),
              static_cast<uint16_t>(CRT[row1][column2]),
              static_cast<uint16_t>(CRT[row2][column1]),
              static_cast<uint16_t>(CRT[row2][column2]),
          }};
          checker.delta = exact_delta(sequence, single, checker.positions);
          temporary.push_back(checker);
        }

  CheckerSet result;
  const size_t count = temporary.size();
  result.positions.resize(count);
  result.norm_squared.resize(count);
  result.delta_by_lag.resize(LAST_LAG * count);
  for (size_t index = 0; index < count; ++index) {
    result.positions[index] = temporary[index].positions;
    int norm = 0;
    for (int lag = 1; lag <= LAST_LAG; ++lag) {
      const int value = temporary[index].delta[lag];
      if (value < -128 || value > 127)
        throw std::runtime_error("checker delta does not fit int8");
      result.delta_by_lag[(lag - 1) * count + index] =
          static_cast<int8_t>(value);
      norm += value * value;
    }
    result.norm_squared[index] = norm;
  }
  return result;
}

QueryResult direct_query(const std::array<int16_t, LAST_LAG> &target,
                         const CheckerSet &checkers, int baseline,
                         std::vector<int32_t> &dot_products) {
  const size_t count = checkers.size();
  if (count == 0) throw std::runtime_error("opposite checker set is empty");
  dot_products.assign(count, 0);
  int target_norm = 0;
  for (int coordinate = 0; coordinate < LAST_LAG; ++coordinate) {
    const int multiplier = target[coordinate];
    target_norm += multiplier * multiplier;
    const int8_t *row =
        checkers.delta_by_lag.data() + coordinate * count;
#if defined(__clang__) && defined(NDEBUG)
#pragma clang loop vectorize(enable) interleave(enable)
#endif
    for (size_t index = 0; index < count; ++index)
      dot_products[index] += multiplier * row[index];
  }

  QueryResult result;
  for (size_t index = 0; index < count; ++index) {
    const int proposed = target_norm + 2 * dot_products[index] +
                         checkers.norm_squared[index];
    result.below_baseline += proposed < baseline;
    result.at_baseline += proposed == baseline;
    if (proposed < result.minimum_energy) {
      result.minimum_energy = proposed;
      result.minimum_index = index;
      result.minimum_multiplicity = 1;
    } else if (proposed == result.minimum_energy) {
      ++result.minimum_multiplicity;
    }
  }
  return result;
}

QueryResult scalar_query(const std::array<int16_t, LAST_LAG> &target,
                         const CheckerSet &checkers, int baseline) {
  QueryResult result;
  for (size_t index = 0; index < checkers.size(); ++index) {
    int proposed = 0;
    for (int coordinate = 0; coordinate < LAST_LAG; ++coordinate) {
      const int value = target[coordinate] +
          checkers.delta_by_lag[coordinate * checkers.size() + index];
      proposed += value * value;
    }
    result.below_baseline += proposed < baseline;
    result.at_baseline += proposed == baseline;
    if (proposed < result.minimum_energy) {
      result.minimum_energy = proposed;
      result.minimum_index = index;
      result.minimum_multiplicity = 1;
    } else if (proposed == result.minimum_energy) {
      ++result.minimum_multiplicity;
    }
  }
  return result;
}

void require_same_query(const QueryResult &linear,
                        const QueryResult &scalar) {
  if (linear.minimum_energy != scalar.minimum_energy ||
      linear.minimum_index != scalar.minimum_index ||
      linear.minimum_multiplicity != scalar.minimum_multiplicity ||
      linear.below_baseline != scalar.below_baseline ||
      linear.at_baseline != scalar.at_baseline)
    throw std::runtime_error("dot-product and scalar query kernels disagree");
}

bool disjoint_matchings(const std::array<int, 3> &left,
                        const std::array<int, 3> &right) {
  for (int row = 0; row < 3; ++row)
    if (left[row] == right[row]) return false;
  return true;
}

MixedAudit audit_mixed_neighborhood(
    const Sequences &sequences, const Residuals &residual,
    const std::array<SingleDeltas, 2> &singles,
    const std::array<CheckerSet, 2> &checkers) {
  const int baseline = energy(residual);
  MixedAudit audit;
  std::vector<int32_t> dot_products;
  dot_products.reserve(std::max(checkers[0].size(), checkers[1].size()));

  for (int cycle_sequence = 0; cycle_sequence < 2; ++cycle_sequence) {
    const CheckerSet &opposite = checkers[1 - cycle_sequence];
    for (int row0 = 0; row0 < ROWS; ++row0)
      for (int row1 = row0 + 1; row1 < ROWS; ++row1)
        for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
          const std::array<int, 3> rows{{row0, row1, row2}};
          for (int column0 = 0; column0 < COLS; ++column0)
            for (int column1 = column0 + 1; column1 < COLS; ++column1)
              for (int column2 = column1 + 1; column2 < COLS; ++column2) {
                const std::array<int, 3> columns{{
                    column0, column1, column2}};
                for (size_t first = 0; first < PERMUTATIONS.size(); ++first)
                  for (size_t second = first + 1;
                       second < PERMUTATIONS.size(); ++second) {
                    if (!disjoint_matchings(PERMUTATIONS[first],
                                            PERMUTATIONS[second]))
                      continue;
                    ++audit.raw_patterns[cycle_sequence];
                    std::array<uint16_t, 6> positions{};
                    for (int row = 0; row < 3; ++row) {
                      positions[row] = static_cast<uint16_t>(
                          CRT[rows[row]][columns[PERMUTATIONS[first][row]]]);
                      positions[3 + row] = static_cast<uint16_t>(
                          CRT[rows[row]][columns[PERMUTATIONS[second][row]]]);
                    }
                    const int sign =
                        sequences[cycle_sequence][positions[0]];
                    bool alternating = true;
                    for (int row = 0; row < 3; ++row) {
                      alternating &=
                          sequences[cycle_sequence][positions[row]] == sign;
                      alternating &=
                          sequences[cycle_sequence][positions[3 + row]] ==
                          -sign;
                    }
                    if (!alternating) continue;
                    ++audit.legal_cycles[cycle_sequence];

                    const Delta cycle_delta = exact_delta(
                        sequences[cycle_sequence], singles[cycle_sequence],
                        positions);
                    std::array<int16_t, LAST_LAG> target{};
                    for (int lag = 1; lag <= LAST_LAG; ++lag)
                      target[lag - 1] =
                          residual[lag] + cycle_delta[lag];
                    const QueryResult query = direct_query(
                        target, opposite, baseline, dot_products);
                    if ((audit.legal_cycles[cycle_sequence] & 8191ULL) == 1) {
                      require_same_query(
                          query, scalar_query(target, opposite, baseline));
                      ++audit.scalar_cross_checks;
                    }
                    audit.evaluated_pairs += opposite.size();
                    audit.below_baseline += query.below_baseline;
                    audit.at_baseline += query.at_baseline;
                    if (query.minimum_energy < audit.minimum_energy) {
                      audit.minimum_energy = query.minimum_energy;
                      audit.minimum_multiplicity =
                          query.minimum_multiplicity;
                      audit.best_cycle_sequence = cycle_sequence;
                      audit.best_cycle_positions = positions;
                      audit.best_checker_positions =
                          opposite.positions[query.minimum_index];
                    } else if (query.minimum_energy == audit.minimum_energy) {
                      audit.minimum_multiplicity +=
                          query.minimum_multiplicity;
                    }

                    if (audit.legal_cycles[cycle_sequence] % 25000 == 0) {
                      std::cerr << (cycle_sequence == 0 ? "A" : "B")
                                << " cycles_checked="
                                << audit.legal_cycles[cycle_sequence]
                                << " pairs_checked=" << audit.evaluated_pairs
                                << " current_min=" << audit.minimum_energy
                                << '\n';
                    }
                  }
              }
        }
  }
  return audit;
}

uint64_t count_canonical_eight_assignments(const Signs &sequence) {
  uint64_t result = 0;
  for (int row0 = 0; row0 < ROWS; ++row0)
    for (int row1 = row0 + 1; row1 < ROWS; ++row1)
      for (int row2 = row1 + 1; row2 < ROWS; ++row2)
        for (int row3 = row2 + 1; row3 < ROWS; ++row3) {
          const std::array<int, 4> row_set{{row0, row1, row2, row3}};
          for (const auto &cycle : ROW_CYCLES_4) {
            std::array<int, 4> rows{};
            for (int index = 0; index < 4; ++index)
              rows[index] = row_set[cycle[index]];
            for (const int sign : {-1, 1}) {
              uint64_t assignments = 1;
              for (int edge = 0; edge < 4; ++edge) {
                const int next = (edge + 1) % 4;
                int columns = 0;
                for (int column = 0; column < COLS; ++column)
                  columns +=
                      sequence[CRT[rows[edge]][column]] == sign &&
                      sequence[CRT[rows[next]][column]] == -sign;
                assignments *= static_cast<uint64_t>(columns);
              }
              result += assignments;
            }
          }
        }
  return result;
}

EightAudit audit_eight_neighborhood(
    const Sequences &sequences, const Residuals &residual,
    const std::array<SingleDeltas, 2> &singles) {
  const int baseline = energy(residual);
  EightAudit audit;
  for (int which = 0; which < 2; ++which) {
    audit.raw_assignments[which] =
        count_canonical_eight_assignments(sequences[which]);

    // Independent canonical traversal: begin at the least row of the cycle,
    // and take its unique plus edge first.  The signs then force the direction
    // around the cycle.  This enumerates every alternating C8 exactly once
    // without using the engine's row-cycle/sign-bucket generator.
    for (int row0 = 0; row0 < ROWS; ++row0)
      for (int column0 = 0; column0 < COLS; ++column0) {
        if (sequences[which][CRT[row0][column0]] != 1) continue;
        for (int row1 = row0 + 1; row1 < ROWS; ++row1) {
          if (sequences[which][CRT[row1][column0]] != -1) continue;
          for (int column1 = 0; column1 < COLS; ++column1) {
            if (column1 == column0 ||
                sequences[which][CRT[row1][column1]] != 1)
              continue;
            for (int row2 = row0 + 1; row2 < ROWS; ++row2) {
              if (row2 == row1 ||
                  sequences[which][CRT[row2][column1]] != -1)
                continue;
              for (int column2 = 0; column2 < COLS; ++column2) {
                if (column2 == column0 || column2 == column1 ||
                    sequences[which][CRT[row2][column2]] != 1)
                  continue;
                for (int row3 = row0 + 1; row3 < ROWS; ++row3) {
                  if (row3 == row1 || row3 == row2 ||
                      sequences[which][CRT[row3][column2]] != -1)
                    continue;
                  for (int column3 = 0; column3 < COLS; ++column3) {
                    if (column3 == column0 || column3 == column1 ||
                        column3 == column2 ||
                        sequences[which][CRT[row3][column3]] != 1 ||
                        sequences[which][CRT[row0][column3]] != -1)
                      continue;
                    const std::array<uint16_t, 8> positions{{
                        static_cast<uint16_t>(CRT[row0][column0]),
                        static_cast<uint16_t>(CRT[row1][column0]),
                        static_cast<uint16_t>(CRT[row1][column1]),
                        static_cast<uint16_t>(CRT[row2][column1]),
                        static_cast<uint16_t>(CRT[row2][column2]),
                        static_cast<uint16_t>(CRT[row3][column2]),
                        static_cast<uint16_t>(CRT[row3][column3]),
                        static_cast<uint16_t>(CRT[row0][column3]),
                    }};
                    ++audit.legal_cycles[which];
                    const Delta delta = exact_delta(
                        sequences[which], singles[which], positions);
                    int proposed = 0;
                    for (int lag = 1; lag <= LAST_LAG; ++lag) {
                      const int value = residual[lag] + delta[lag];
                      proposed += value * value;
                    }
                    audit.below_baseline += proposed < baseline;
                    audit.at_baseline += proposed == baseline;
                    if (proposed < audit.minimum_energy) {
                      audit.minimum_energy = proposed;
                      audit.minimum_multiplicity = 1;
                      audit.best_sequence = which;
                      audit.best_positions = positions;
                    } else if (proposed == audit.minimum_energy) {
                      ++audit.minimum_multiplicity;
                    }
                    if (audit.legal_cycles[which] % 1'000'000 == 0)
                      std::cerr << (which == 0 ? "A" : "B")
                                << " eight_cycles_checked="
                                << audit.legal_cycles[which]
                                << " current_min=" << audit.minimum_energy
                                << '\n';
                  }
                }
              }
            }
          }
        }
      }
    if (audit.raw_assignments[which] < audit.legal_cycles[which])
      throw std::runtime_error("eight-cycle raw count is too small");
    audit.repeated_column_assignments[which] =
        audit.raw_assignments[which] - audit.legal_cycles[which];
  }
  return audit;
}

void require_array(const std::string &document, const std::string &key,
                   const std::vector<int> &expected) {
  if (extract_array(document, key) != expected)
    throw std::runtime_error("recorded array disagrees with recomputation: " +
                             key);
}

void require_integer(const std::string &document, const std::string &key,
                     int64_t expected) {
  if (extract_integer(document, key) != expected)
    throw std::runtime_error("recorded integer disagrees with recomputation: " +
                             key);
}

void verify_checkpoint_metadata(const std::string &document,
                                const Sequences &sequences,
                                const RowSums &row_sums,
                                const Residuals &residual) {
  require_integer(document, "length", N);
  require_integer(document, "hadamard_order", 2 * (N + 1));

  for (int which = 0; which < 2; ++which) {
    std::vector<int> rows(ROWS), row_plus(ROWS);
    std::vector<int> columns(COLS), column_plus(COLS);
    for (int row = 0; row < ROWS; ++row) {
      rows[row] = row_sums[which][row];
      row_plus[row] = (COLS + rows[row]) / 2;
    }
    for (int column = 0; column < COLS; ++column) {
      for (int row = 0; row < ROWS; ++row)
        columns[column] += sequences[which][CRT[row][column]];
      column_plus[column] = (ROWS + columns[column]) / 2;
    }
    require_array(document, which == 0 ? "row_sums_a" : "row_sums_b",
                  rows);
    require_array(document,
                  which == 0 ? "row_plus_counts_a" : "row_plus_counts_b",
                  row_plus);
    require_array(document,
                  which == 0 ? "column_sums_a" : "column_sums_b", columns);
    require_array(document, which == 0 ? "column_plus_counts_a"
                                       : "column_plus_counts_b",
                  column_plus);
  }

  std::vector<int> compressed_paf(ROWS, -74);
  compressed_paf[0] = 594;
  require_array(document, "mod9_combined_paf_0_through_8", compressed_paf);

  std::vector<int> recorded_residual(LAST_LAG);
  std::vector<int> recorded_paf(LAST_LAG);
  int nonzero = 0;
  int maximum = 0;
  int l1 = 0;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    recorded_residual[lag - 1] = residual[lag];
    recorded_paf[lag - 1] = 2 * residual[lag] - 2;
    nonzero += residual[lag] != 0;
    maximum = std::max(maximum, std::abs(static_cast<int>(residual[lag])));
    l1 += std::abs(static_cast<int>(residual[lag]));
  }
  require_array(document, "half_paf_residuals_1_through_166",
                recorded_residual);
  require_array(document, "periodic_correlation_sums_1_through_166",
                recorded_paf);
  const int baseline = energy(residual);
  require_integer(document, "energy_half_paf", baseline);
  require_integer(document, "energy_paf", 4LL * baseline);
  require_integer(document, "bad_lag_count", nonzero);
  require_integer(document, "max_abs_paf_residual", 2 * maximum);
  require_integer(document, "l1_paf_residual", 2 * l1);
}

void verify_recorded_mixed_certificate(
    const std::string &document, const std::array<CheckerSet, 2> &checkers,
    const MixedAudit &audit) {
  if (!extract_boolean(document, "mixed_six_cycle_polish"))
    throw std::runtime_error("checkpoint does not claim mixed polish");
  require_integer(document, "mixed_six_cycle_polish_moves",
                  audit.below_baseline == 0 ? 0 : -1);
  require_integer(document, "mixed_six_cycle_scans", 1);
  require_integer(document, "complete_mixed_six_cycle_scans", 1);
  require_integer(document, "incomplete_mixed_six_cycle_scans", 0);
  require_integer(document, "mixed_six_cycle_raw_patterns",
                  audit.raw_patterns[0] + audit.raw_patterns[1]);
  require_integer(document, "mixed_six_cycle_legal_cycles",
                  audit.legal_cycles[0] + audit.legal_cycles[1]);
  require_integer(document, "mixed_six_cycle_queries",
                  audit.legal_cycles[0] + audit.legal_cycles[1]);
  require_integer(document, "mixed_six_cycle_possible_pair_distances",
                  audit.evaluated_pairs);
  require_integer(document, "last_mixed_six_cycle_a_raw_patterns",
                  audit.raw_patterns[0]);
  require_integer(document, "last_mixed_six_cycle_b_raw_patterns",
                  audit.raw_patterns[1]);
  require_integer(document, "last_mixed_six_cycle_a_legal_cycles",
                  audit.legal_cycles[0]);
  require_integer(document, "last_mixed_six_cycle_b_legal_cycles",
                  audit.legal_cycles[1]);
  require_integer(document, "last_mixed_six_cycle_a_queries",
                  audit.legal_cycles[0]);
  require_integer(document, "last_mixed_six_cycle_b_queries",
                  audit.legal_cycles[1]);
  require_integer(document, "last_mixed_six_cycle_a_checker_components",
                  checkers[0].size());
  require_integer(document, "last_mixed_six_cycle_b_checker_components",
                  checkers[1].size());

  const int64_t point_distances =
      extract_integer(document, "mixed_six_cycle_pair_distances");
  const int64_t pruned_points =
      extract_integer(document, "mixed_six_cycle_pruned_points");
  if (point_distances + pruned_points !=
      static_cast<int64_t>(audit.evaluated_pairs))
    throw std::runtime_error("recorded kd-tree coverage arithmetic is invalid");
  require_integer(document, "mixed_six_cycle_tree_node_visits",
                  point_distances);
  require_integer(document, "mixed_six_cycle_tree_nodes",
                  checkers[0].size() + checkers[1].size());
}

void verify_recorded_eight_certificate(const std::string &document,
                                       const EightAudit &audit) {
  if (!extract_boolean(document, "eight_cycle_polish"))
    throw std::runtime_error("checkpoint does not claim eight-cycle polish");
  require_integer(document, "eight_cycle_polish_moves", 0);
  require_integer(document, "eight_cycle_scans", 1);
  require_integer(document, "complete_eight_cycle_scans", 1);
  require_integer(document, "incomplete_eight_cycle_scans", 0);
  require_integer(document, "eight_cycle_row_cycles", 2 * 378);
  require_integer(document, "eight_cycle_sign_orientations", 2 * 756);
  require_integer(document, "eight_cycle_raw_assignments",
                  audit.raw_assignments[0] + audit.raw_assignments[1]);
  require_integer(document, "eight_cycle_repeated_column_skips",
                  audit.repeated_column_assignments[0] +
                      audit.repeated_column_assignments[1]);
  require_integer(document, "eight_cycle_legal_cycles",
                  audit.legal_cycles[0] + audit.legal_cycles[1]);
  require_integer(document, "eight_cycle_evaluations",
                  audit.legal_cycles[0] + audit.legal_cycles[1]);
  for (int which = 0; which < 2; ++which) {
    const std::string prefix = which == 0 ? "last_eight_cycle_a_"
                                          : "last_eight_cycle_b_";
    require_integer(document, prefix + "row_cycles", 378);
    require_integer(document, prefix + "sign_orientations", 756);
    require_integer(document, prefix + "raw_assignments",
                    audit.raw_assignments[which]);
    require_integer(document, prefix + "repeated_column_skips",
                    audit.repeated_column_assignments[which]);
    require_integer(document, prefix + "legal_cycles",
                    audit.legal_cycles[which]);
    require_integer(document, prefix + "evaluations",
                    audit.legal_cycles[which]);
  }
}

void replay_minimum(const Sequences &source, const RowSums &source_rows,
                    const MixedAudit &audit) {
  if (audit.best_cycle_sequence < 0)
    throw std::runtime_error("mixed neighborhood is empty");
  Sequences changed = source;
  for (uint16_t position : audit.best_cycle_positions)
    changed[audit.best_cycle_sequence][position] =
        -changed[audit.best_cycle_sequence][position];
  for (uint16_t position : audit.best_checker_positions)
    changed[1 - audit.best_cycle_sequence][position] =
        -changed[1 - audit.best_cycle_sequence][position];
  if (verify_exact_profile_margins(changed) != source_rows)
    throw std::runtime_error("best mixed replay changed a margin");
  if (energy(recompute_residuals(changed)) != audit.minimum_energy)
    throw std::runtime_error("best mixed replay energy mismatch");
}

void replay_eight_minimum(const Sequences &source,
                          const RowSums &source_rows,
                          const EightAudit &audit) {
  if (audit.best_sequence < 0)
    throw std::runtime_error("eight-cycle neighborhood is empty");
  Sequences changed = source;
  for (uint16_t position : audit.best_positions)
    changed[audit.best_sequence][position] =
        -changed[audit.best_sequence][position];
  if (verify_exact_profile_margins(changed) != source_rows)
    throw std::runtime_error("best eight-cycle replay changed a margin");
  if (energy(recompute_residuals(changed)) != audit.minimum_energy)
    throw std::runtime_error("best eight-cycle replay energy mismatch");
}

void self_test() {
  int disjoint_pairs = 0;
  for (size_t left = 0; left < PERMUTATIONS.size(); ++left)
    for (size_t right = left + 1; right < PERMUTATIONS.size(); ++right)
      disjoint_pairs += disjoint_matchings(PERMUTATIONS[left],
                                           PERMUTATIONS[right]);
  if (disjoint_pairs != 6)
    throw std::runtime_error("six-cycle matching self-test failed");

  Signs sequence{};
  for (int position = 0; position < N; ++position)
    sequence[position] =
        ((position * position + 5 * position + 1) % 13 < 6) ? 1 : -1;
  const SingleDeltas single = make_single_deltas(sequence);
  const std::array<uint16_t, 6> positions{{0, 7, 51, 129, 230, 332}};
  const Delta delta = exact_delta(sequence, single, positions);
  Signs changed = sequence;
  for (uint16_t position : positions) changed[position] = -changed[position];
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int before = 0;
    int after = 0;
    for (int position = 0; position < N; ++position) {
      before += sequence[position] * sequence[(position + lag) % N];
      after += changed[position] * changed[(position + lag) % N];
    }
    if (after - before != 2 * delta[lag])
      throw std::runtime_error("exact delta self-test failed");
  }

  CheckerSet checkers;
  checkers.positions.resize(3);
  checkers.norm_squared = {5, 10, 1};
  checkers.delta_by_lag.assign(3 * LAST_LAG, 0);
  checkers.delta_by_lag[0] = 1;
  checkers.delta_by_lag[1] = -1;
  checkers.delta_by_lag[2] = 0;
  checkers.delta_by_lag[3] = 2;
  checkers.delta_by_lag[4] = 3;
  checkers.delta_by_lag[5] = 1;
  std::array<int16_t, LAST_LAG> target{};
  target[0] = 2;
  target[1] = -1;
  std::vector<int32_t> work;
  const QueryResult query = direct_query(target, checkers, 9, work);
  int scalar_minimum = std::numeric_limits<int>::max();
  for (size_t index = 0; index < checkers.size(); ++index) {
    int direct = 0;
    for (int coordinate = 0; coordinate < LAST_LAG; ++coordinate) {
      const int value = target[coordinate] +
          checkers.delta_by_lag[coordinate * checkers.size() + index];
      direct += value * value;
    }
    scalar_minimum = std::min(scalar_minimum, direct);
  }
  if (query.minimum_energy != scalar_minimum)
    throw std::runtime_error("direct query kernel self-test failed");
  require_same_query(query, scalar_query(target, checkers, 9));
  std::cout << "PASS mixed-neighborhood arithmetic self-test\n";
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
      self_test();
      return 0;
    }
    const bool eight_mode =
        argc == 3 && std::string(argv[1]) == "--eight";
    if (argc != 2 && !eight_mode) {
      std::cerr << "usage: verify_legendre_333_profile_mixed CHECKPOINT.json\n"
                   "       verify_legendre_333_profile_mixed --eight CHECKPOINT.json\n"
                   "       verify_legendre_333_profile_mixed --self-test\n";
      return 2;
    }

    std::ifstream input(argv[eight_mode ? 2 : 1]);
    if (!input) throw std::runtime_error("could not open checkpoint");
    const std::string document((std::istreambuf_iterator<char>(input)),
                               std::istreambuf_iterator<char>());
    const int profile = static_cast<int>(extract_integer(document, "profile"));
    if (profile < 0) throw std::runtime_error("negative profile index");
    const Sequences sequences = parse_sequences(document);
    const RowSums row_sums = verify_exact_profile_margins(sequences);
    const Residuals residual = recompute_residuals(sequences);
    verify_checkpoint_metadata(document, sequences, row_sums, residual);
    const int baseline = energy(residual);

    const std::array<SingleDeltas, 2> singles{{
        make_single_deltas(sequences[0]), make_single_deltas(sequences[1])}};
    std::cout << "checkpoint profile=" << profile
              << " recomputed_baseline_energy=" << baseline << '\n';

    if (eight_mode) {
      const EightAudit audit =
          audit_eight_neighborhood(sequences, residual, singles);
      replay_eight_minimum(sequences, row_sums, audit);
      verify_recorded_eight_certificate(document, audit);
      std::cout << "eight_raw_assignments A=" << audit.raw_assignments[0]
                << " B=" << audit.raw_assignments[1] << '\n'
                << "eight_repeated_column_assignments A="
                << audit.repeated_column_assignments[0] << " B="
                << audit.repeated_column_assignments[1] << '\n'
                << "legal_eight_cycles A=" << audit.legal_cycles[0]
                << " B=" << audit.legal_cycles[1] << '\n'
                << "minimum_eight_energy=" << audit.minimum_energy
                << " minimum_multiplicity=" << audit.minimum_multiplicity
                << " below_baseline=" << audit.below_baseline
                << " at_baseline=" << audit.at_baseline << '\n'
                << "best_sequence=" << (audit.best_sequence == 0 ? "A" : "B")
                << '\n' << "best_positions=";
      for (size_t index = 0; index < audit.best_positions.size(); ++index)
        std::cout << (index ? "," : "") << audit.best_positions[index];
      std::cout << '\n';
      if (audit.below_baseline != 0 || audit.minimum_energy < baseline) {
        std::cout << "FAIL found an eight-cycle state below baseline="
                  << baseline << '\n';
        return 1;
      }
      std::cout << "PASS all alternating eight-cycle states have energy "
                   ">= baseline=" << baseline << '\n';
      return 0;
    }

    const std::array<CheckerSet, 2> checkers{{
        enumerate_checkers(sequences[0], singles[0]),
        enumerate_checkers(sequences[1], singles[1])}};
    std::cout << "checker_components A=" << checkers[0].size()
              << " B=" << checkers[1].size() << '\n';

    const MixedAudit audit = audit_mixed_neighborhood(
        sequences, residual, singles, checkers);
    replay_minimum(sequences, row_sums, audit);
    verify_recorded_mixed_certificate(document, checkers, audit);

    std::cout << "raw_six_cycle_patterns A=" << audit.raw_patterns[0]
              << " B=" << audit.raw_patterns[1] << '\n'
              << "legal_six_cycles A=" << audit.legal_cycles[0]
              << " B=" << audit.legal_cycles[1] << '\n'
              << "mixed_pairs_evaluated=" << audit.evaluated_pairs << '\n'
              << "minimum_mixed_energy=" << audit.minimum_energy
              << " minimum_multiplicity=" << audit.minimum_multiplicity
              << " below_baseline=" << audit.below_baseline
              << " at_baseline=" << audit.at_baseline
              << " scalar_cross_checks=" << audit.scalar_cross_checks << '\n'
              << "best_orientation="
              << (audit.best_cycle_sequence == 0 ? "A-cycle/B-checker"
                                                  : "B-cycle/A-checker")
              << '\n' << "best_cycle_positions=";
    for (size_t index = 0; index < audit.best_cycle_positions.size(); ++index)
      std::cout << (index ? "," : "")
                << audit.best_cycle_positions[index];
    std::cout << '\n' << "best_checker_positions=";
    for (size_t index = 0; index < audit.best_checker_positions.size(); ++index)
      std::cout << (index ? "," : "")
                << audit.best_checker_positions[index];
    std::cout << '\n';
    if (audit.below_baseline != 0 || audit.minimum_energy < baseline) {
      std::cout << "FAIL found a mixed state below baseline=" << baseline
                << '\n';
      return 1;
    }
    std::cout << "PASS all mixed cycle/opposite-checker states have energy "
                 ">= baseline=" << baseline << '\n';
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
