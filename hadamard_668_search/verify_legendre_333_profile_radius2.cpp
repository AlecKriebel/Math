// Independent exact radius-two audit for an exact-profile LP(333) checkpoint.
//
// This verifier does not use search-engine caches or trust recorded energies.
// It parses the two sign vectors, checks every fixed CRT row/column margin,
// recomputes all 166 independent PAF residuals, and then enumerates:
//
//   * every legal checkerboard switch in A and B;
//   * every pair of cell-disjoint switches in one sequence;
//   * every alternating six-cycle in one sequence; and
//   * every Cartesian pair of one A switch and one B switch.
//
// Eight-cell outcomes are deduplicated with an exact combinatorial rank in
// C(333,8), which fits in uint64_t.  The process is single-threaded and keeps
// only one sequence's rank vector in memory at a time.  Exit status zero means
// that no enumerated state has energy below the recomputed checkpoint energy.

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
using Delta = std::array<int8_t, LAST_LAG + 1>;
using SingleDeltas = std::array<std::array<int8_t, LAST_LAG + 1>, N>;
using RowSums = std::array<std::array<int, ROWS>, 2>;

struct Move {
  std::array<uint16_t, 4> positions{};
  std::array<int, 4> coordinates{};  // row1,row2,column1,column2
  Delta delta{};
  int energy_change = 0;
};

struct NeighborhoodResult {
  uint64_t representations = 0;
  uint64_t unique_states = 0;
  uint64_t improving_representations = 0;
  int best_energy = std::numeric_limits<int>::max();
  size_t first = 0;
  size_t second = 0;
  bool found = false;
};

struct CycleResult {
  uint64_t raw_patterns = 0;
  uint64_t alternating_cycles = 0;
  uint64_t improving_cycles = 0;
  int best_energy = std::numeric_limits<int>::max();
  std::array<uint16_t, 6> best_positions{};
  bool found = false;
};

std::array<std::array<int, COLS>, ROWS> make_crt_table() {
  std::array<std::array<int, COLS>, ROWS> result{};
  for (int row = 0; row < ROWS; ++row)
    for (int column = 0; column < COLS; ++column)
      result[row][column] =
          column + COLS * (((row - column) % ROWS + ROWS) % ROWS);
  return result;
}

std::array<std::array<uint64_t, 9>, N + 1> make_binomial_table() {
  std::array<std::array<uint64_t, 9>, N + 1> result{};
  result[0][0] = 1;
  for (int n = 1; n <= N; ++n) {
    result[n][0] = 1;
    for (int k = 1; k <= 8; ++k)
      result[n][k] = result[n - 1][k - 1] + result[n - 1][k];
  }
  return result;
}

const auto CRT = make_crt_table();
const auto BINOMIAL = make_binomial_table();

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

std::vector<int> extract_array(const std::string &document,
                               const std::string &key) {
  const std::string needle = "\"" + key + "\"";
  const size_t key_at = document.find(needle);
  if (key_at == std::string::npos)
    throw std::runtime_error("checkpoint has no " + key);
  const size_t begin = document.find('[', key_at + needle.size());
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

int extract_integer(const std::string &document, const std::string &key) {
  const std::string needle = "\"" + key + "\"";
  const size_t key_at = document.find(needle);
  if (key_at == std::string::npos)
    throw std::runtime_error("checkpoint has no " + key);
  const size_t colon = document.find(':', key_at + needle.size());
  if (colon == std::string::npos)
    throw std::runtime_error("malformed checkpoint integer " + key);
  size_t at = colon + 1;
  while (at < document.size() && std::isspace(
             static_cast<unsigned char>(document[at])))
    ++at;
  size_t consumed = 0;
  return std::stoi(document.substr(at), &consumed);
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

uint64_t checkpoint_fingerprint(const Sequences &sequences) {
  uint64_t result = 14'695'981'039'346'656'037ULL;
  for (const Signs &sequence : sequences)
    for (int8_t sign : sequence) {
      result ^= sign == -1 ? 1ULL : 3ULL;
      result *= 1'099'511'628'211ULL;
    }
  return result;
}

RowSums verify_exact_profile_margins(const Sequences &sequences) {
  RowSums row_sums{};
  for (int which = 0; which < 2; ++which) {
    int total = 0;
    for (int row = 0; row < ROWS; ++row) {
      int row_sum = 0;
      for (int column = 0; column < COLS; ++column)
        row_sum += sequences[which][CRT[row][column]];
      row_sums[which][row] = row_sum;
      total += row_sum;
    }
    if (total != 1) throw std::runtime_error("sequence sum is not one");
    for (int column = 0; column < COLS; ++column) {
      int column_sum = 0;
      for (int row = 0; row < ROWS; ++row)
        column_sum += sequences[which][CRT[row][column]];
      const int expected =
          column == 0 ? 1 : (which == 0 ? 3 : -3) *
                                   legendre_symbol_37(column);
      if (column_sum != expected)
        throw std::runtime_error("fixed Legendre column-margin mismatch");
    }
  }

  for (int lag = 0; lag < ROWS; ++lag) {
    int combined_paf = 0;
    for (int which = 0; which < 2; ++which)
      for (int row = 0; row < ROWS; ++row)
        combined_paf +=
            row_sums[which][row] * row_sums[which][(row + lag) % ROWS];
    const int expected = lag == 0 ? 594 : -74;
    if (combined_paf != expected)
      throw std::runtime_error("combined mod-9 PAF profile mismatch");
  }
  return row_sums;
}

void verify_recorded_profile(const std::string &document,
                             const RowSums &row_sums) {
  for (int which = 0; which < 2; ++which) {
    const auto recorded =
        extract_array(document, which == 0 ? "row_sums_a" : "row_sums_b");
    if (recorded.size() != ROWS)
      throw std::runtime_error("recorded row-sum vector length mismatch");
    for (int row = 0; row < ROWS; ++row)
      if (recorded[row] != row_sums[which][row])
        throw std::runtime_error("recorded row sums disagree with signs");
  }

  const auto recorded_paf =
      extract_array(document, "mod9_combined_paf_0_through_8");
  if (recorded_paf.size() != ROWS)
    throw std::runtime_error("recorded mod-9 PAF length mismatch");
  for (int lag = 0; lag < ROWS; ++lag) {
    const int expected = lag == 0 ? 594 : -74;
    if (recorded_paf[lag] != expected)
      throw std::runtime_error("recorded mod-9 PAF disagrees with recomputation");
  }
}

Residuals recompute_residuals(const Sequences &sequences) {
  Residuals residual{};
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int paf_sum = 0;
    for (const Signs &sequence : sequences)
      for (int index = 0; index < N; ++index)
        paf_sum += sequence[index] * sequence[(index + lag) % N];
    if ((paf_sum + 2) % 4 != 0)
      throw std::runtime_error("combined PAF violates mod-four parity");
    residual[lag] = static_cast<int16_t>((paf_sum + 2) / 2);
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
  std::array<int, LAST_LAG + 1> work{};
  for (uint16_t position : positions)
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      work[lag] += single[position][lag];
  for (size_t left = 0; left < Size; ++left)
    for (size_t right = left + 1; right < Size; ++right) {
      const int lag = cyclic_distance(positions[left], positions[right]);
      work[lag] += 2 * sequence[positions[left]] * sequence[positions[right]];
    }
  Delta result{};
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    if (work[lag] < -128 || work[lag] > 127)
      throw std::runtime_error("residual delta does not fit int8");
    result[lag] = static_cast<int8_t>(work[lag]);
  }
  return result;
}

int energy_after(const Residuals &residual, const Delta &delta) {
  int result = 0;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int value = residual[lag] + delta[lag];
    result += value * value;
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

std::vector<Move> enumerate_moves(const Signs &sequence,
                                  const SingleDeltas &single,
                                  const Residuals &residual) {
  const int base_energy = energy(residual);
  std::vector<Move> moves;
  moves.reserve(3200);
  for (int row1 = 0; row1 < ROWS; ++row1)
    for (int row2 = row1 + 1; row2 < ROWS; ++row2)
      for (int column1 = 0; column1 < COLS; ++column1)
        for (int column2 = column1 + 1; column2 < COLS; ++column2) {
          if (!checkerboard(sequence, row1, row2, column1, column2)) continue;
          Move move;
          move.positions = {{static_cast<uint16_t>(CRT[row1][column1]),
                             static_cast<uint16_t>(CRT[row1][column2]),
                             static_cast<uint16_t>(CRT[row2][column1]),
                             static_cast<uint16_t>(CRT[row2][column2])}};
          move.coordinates = {{row1, row2, column1, column2}};
          move.delta = exact_delta(sequence, single, move.positions);
          move.energy_change = energy_after(residual, move.delta) - base_energy;
          moves.push_back(move);
        }
  return moves;
}

bool disjoint(const Move &left, const Move &right) {
  for (uint16_t first : left.positions)
    for (uint16_t second : right.positions)
      if (first == second) return false;
  return true;
}

template <size_t Size>
uint64_t combinatorial_rank(std::array<uint16_t, Size> positions) {
  static_assert(Size <= 8);
  std::sort(positions.begin(), positions.end());
  if (std::adjacent_find(positions.begin(), positions.end()) != positions.end())
    throw std::runtime_error("cannot rank a repeated flip position");
  uint64_t result = 0;
  for (size_t index = 0; index < Size; ++index)
    result += BINOMIAL[positions[index]][index + 1];
  return result;
}

int replay_moves(const Sequences &source, int first_sequence,
                 const std::array<uint16_t, 4> &first,
                 int second_sequence,
                 const std::array<uint16_t, 4> &second) {
  const RowSums source_rows = verify_exact_profile_margins(source);
  Sequences changed = source;
  for (uint16_t position : first)
    changed[first_sequence][position] = -changed[first_sequence][position];
  for (uint16_t position : second)
    changed[second_sequence][position] = -changed[second_sequence][position];
  if (verify_exact_profile_margins(changed) != source_rows)
    throw std::runtime_error("move replay changed a row margin");
  return energy(recompute_residuals(changed));
}

template <size_t Size>
int replay_cycle(const Sequences &source, int which,
                 const std::array<uint16_t, Size> &positions) {
  const RowSums source_rows = verify_exact_profile_margins(source);
  Sequences changed = source;
  for (uint16_t position : positions)
    changed[which][position] = -changed[which][position];
  if (verify_exact_profile_margins(changed) != source_rows)
    throw std::runtime_error("cycle replay changed a row margin");
  return energy(recompute_residuals(changed));
}

NeighborhoodResult audit_single_moves(const std::vector<Move> &moves,
                                      int base_energy) {
  NeighborhoodResult result;
  result.representations = moves.size();
  result.unique_states = moves.size();
  for (size_t index = 0; index < moves.size(); ++index) {
    const int proposed = base_energy + moves[index].energy_change;
    result.improving_representations += proposed < base_energy;
    if (!result.found || proposed < result.best_energy) {
      result.best_energy = proposed;
      result.first = index;
      result.found = true;
    }
  }
  return result;
}

NeighborhoodResult audit_same_sequence_pairs(
    const Sequences &sequences, int which, const Residuals &residual,
    const std::vector<Move> &moves) {
  const int base_energy = energy(residual);
  NeighborhoodResult result;
  std::vector<uint64_t> state_ranks;
  state_ranks.reserve(moves.size() * (moves.size() - 1) / 2);
  std::array<uint32_t, LAST_LAG + 1> stamps{};
  std::array<int16_t, LAST_LAG + 1> cross{};
  uint32_t serial = 0;

  for (size_t left = 0; left < moves.size(); ++left) {
    for (size_t right = left + 1; right < moves.size(); ++right) {
      if (!disjoint(moves[left], moves[right])) continue;
      ++result.representations;
      std::array<uint16_t, 8> positions{};
      std::copy(moves[left].positions.begin(), moves[left].positions.end(),
                positions.begin());
      std::copy(moves[right].positions.begin(), moves[right].positions.end(),
                positions.begin() + 4);
      state_ranks.push_back(combinatorial_rank(positions));

      int dot_product = 0;
      for (int lag = 1; lag <= LAST_LAG; ++lag)
        dot_product += moves[left].delta[lag] * moves[right].delta[lag];
      int proposed = base_energy + moves[left].energy_change +
                     moves[right].energy_change + 2 * dot_product;

      ++serial;
      std::array<uint8_t, 16> touched{};
      int touched_count = 0;
      for (uint16_t first : moves[left].positions)
        for (uint16_t second : moves[right].positions) {
          const int lag = cyclic_distance(first, second);
          if (stamps[lag] != serial) {
            stamps[lag] = serial;
            cross[lag] = 0;
            touched[touched_count++] = static_cast<uint8_t>(lag);
          }
          cross[lag] += static_cast<int16_t>(
              2 * sequences[which][first] * sequences[which][second]);
        }
      for (int index = 0; index < touched_count; ++index) {
        const int lag = touched[index];
        const int before = residual[lag] + moves[left].delta[lag] +
                           moves[right].delta[lag];
        proposed += 2 * before * cross[lag] + cross[lag] * cross[lag];
      }

      result.improving_representations += proposed < base_energy;
      if (!result.found || proposed < result.best_energy) {
        result.best_energy = proposed;
        result.first = left;
        result.second = right;
        result.found = true;
      }
    }
  }
  std::sort(state_ranks.begin(), state_ranks.end());
  result.unique_states = static_cast<uint64_t>(std::distance(
      state_ranks.begin(), std::unique(state_ranks.begin(), state_ranks.end())));
  if (result.found) {
    const int replayed = replay_moves(
        sequences, which, moves[result.first].positions, which,
        moves[result.second].positions);
    if (replayed != result.best_energy)
      throw std::runtime_error("same-sequence pair replay mismatch");
  }
  return result;
}

std::vector<std::array<int, 3>> permutations_of_three() {
  std::array<int, 3> permutation{{0, 1, 2}};
  std::vector<std::array<int, 3>> result;
  do {
    result.push_back(permutation);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return result;
}

CycleResult audit_six_cycles(const Sequences &sequences, int which,
                             const SingleDeltas &single,
                             const Residuals &residual) {
  const int base_energy = energy(residual);
  const Signs &sequence = sequences[which];
  const auto permutations = permutations_of_three();
  CycleResult result;
  std::vector<uint64_t> ranks;
  ranks.reserve(130000);
  for (int row0 = 0; row0 < ROWS; ++row0)
    for (int row1 = row0 + 1; row1 < ROWS; ++row1)
      for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
        const std::array<int, 3> rows{{row0, row1, row2}};
        for (int column0 = 0; column0 < COLS; ++column0)
          for (int column1 = column0 + 1; column1 < COLS; ++column1)
            for (int column2 = column1 + 1; column2 < COLS; ++column2) {
              const std::array<int, 3> columns{{column0, column1, column2}};
              for (size_t first = 0; first < permutations.size(); ++first)
                for (size_t second = first + 1;
                     second < permutations.size(); ++second) {
                  bool deranged = true;
                  for (int row = 0; row < 3; ++row)
                    deranged &= permutations[first][row] !=
                                permutations[second][row];
                  if (!deranged) continue;
                  ++result.raw_patterns;
                  std::array<uint16_t, 6> positions{};
                  for (int row = 0; row < 3; ++row) {
                    positions[row] = static_cast<uint16_t>(
                        CRT[rows[row]][columns[permutations[first][row]]]);
                    positions[3 + row] = static_cast<uint16_t>(
                        CRT[rows[row]][columns[permutations[second][row]]]);
                  }
                  const int sign = sequence[positions[0]];
                  bool alternating = true;
                  for (int row = 0; row < 3; ++row) {
                    alternating &= sequence[positions[row]] == sign;
                    alternating &= sequence[positions[3 + row]] == -sign;
                  }
                  if (!alternating) continue;
                  ++result.alternating_cycles;
                  ranks.push_back(combinatorial_rank(positions));
                  const Delta delta = exact_delta(sequence, single, positions);
                  const int proposed = energy_after(residual, delta);
                  result.improving_cycles += proposed < base_energy;
                  if (!result.found || proposed < result.best_energy) {
                    result.best_energy = proposed;
                    result.best_positions = positions;
                    result.found = true;
                  }
                }
            }
      }
  std::sort(ranks.begin(), ranks.end());
  if (std::unique(ranks.begin(), ranks.end()) != ranks.end())
    throw std::runtime_error("six-cycle generator produced a duplicate state");
  if (result.found) {
    const int replayed = replay_cycle(sequences, which, result.best_positions);
    if (replayed != result.best_energy)
      throw std::runtime_error("six-cycle replay mismatch");
  }
  return result;
}

NeighborhoodResult audit_cross_pairs(const Sequences &sequences,
                                     const Residuals &residual,
                                     const std::vector<Move> &a_moves,
                                     const std::vector<Move> &b_moves) {
  const int base_energy = energy(residual);
  NeighborhoodResult result;
  result.representations = a_moves.size() * b_moves.size();
  result.unique_states = result.representations;
  for (size_t left = 0; left < a_moves.size(); ++left) {
    for (size_t right = 0; right < b_moves.size(); ++right) {
      int dot_product = 0;
      for (int lag = 1; lag <= LAST_LAG; ++lag)
        dot_product += a_moves[left].delta[lag] * b_moves[right].delta[lag];
      const int proposed = base_energy + a_moves[left].energy_change +
                           b_moves[right].energy_change + 2 * dot_product;
      result.improving_representations += proposed < base_energy;
      if (!result.found || proposed < result.best_energy) {
        result.best_energy = proposed;
        result.first = left;
        result.second = right;
        result.found = true;
      }
    }
  }
  if (result.found) {
    const int replayed = replay_moves(
        sequences, 0, a_moves[result.first].positions, 1,
        b_moves[result.second].positions);
    if (replayed != result.best_energy)
      throw std::runtime_error("cross-sequence pair replay mismatch");
  }
  return result;
}

void print_move(const Move &move) {
  std::cout << '(';
  for (int index = 0; index < 4; ++index)
    std::cout << (index ? "," : "") << move.coordinates[index];
  std::cout << ')';
}

void print_neighborhood(const std::string &label,
                        const NeighborhoodResult &result) {
  std::cout << label << " representations=" << result.representations
            << " unique_states=" << result.unique_states
            << " duplicates=" << result.representations - result.unique_states
            << " improving=" << result.improving_representations
            << " best_energy=" << result.best_energy << '\n';
}

void verify_profile6_regression(
    int profile, uint64_t fingerprint, int base_energy,
    const std::array<NeighborhoodResult, 2> &single_results,
    const std::array<NeighborhoodResult, 2> &pair_results,
    const std::array<CycleResult, 2> &cycle_results,
    const NeighborhoodResult &cross, uint64_t total_unique_nontrivial) {
  // The fingerprint only selects the checked-in fixture; all other valid
  // checkpoints, including other profile-6 states, remain generic audits.
  constexpr uint64_t PROFILE6_FIXTURE_FINGERPRINT =
      0x75c76421460e76dfULL;
  if (profile != 6 || fingerprint != PROFILE6_FIXTURE_FINGERPRINT) return;

  const bool exact_counts =
      base_energy == 2320 &&
      single_results[0].representations == 2'939 &&
      single_results[0].unique_states == 2'939 &&
      single_results[0].improving_representations == 0 &&
      single_results[0].best_energy == 2400 &&
      pair_results[0].representations == 4'109'262 &&
      pair_results[0].unique_states == 4'056'465 &&
      pair_results[0].improving_representations == 0 &&
      pair_results[0].best_energy == 2584 &&
      cycle_results[0].raw_patterns == 3'916'080 &&
      cycle_results[0].alternating_cycles == 120'553 &&
      cycle_results[0].improving_cycles == 0 &&
      cycle_results[0].best_energy == 2496 &&
      single_results[1].representations == 3'053 &&
      single_results[1].unique_states == 3'053 &&
      single_results[1].improving_representations == 0 &&
      single_results[1].best_energy == 2496 &&
      pair_results[1].representations == 4'438'151 &&
      pair_results[1].unique_states == 4'378'922 &&
      pair_results[1].improving_representations == 0 &&
      pair_results[1].best_energy == 2688 &&
      cycle_results[1].raw_patterns == 3'916'080 &&
      cycle_results[1].alternating_cycles == 126'980 &&
      cycle_results[1].improving_cycles == 0 &&
      cycle_results[1].best_energy == 2616 &&
      cross.representations == 8'972'767 &&
      cross.unique_states == 8'972'767 &&
      cross.improving_representations == 0 &&
      cross.best_energy == 2560 &&
      total_unique_nontrivial == 17'661'679;
  if (!exact_counts)
    throw std::runtime_error("profile-6 exact-count regression failed");
  std::cout << "PASS profile-6 exact-count regression\n";
}

void self_test() {
  std::vector<uint64_t> ranks;
  for (uint16_t a = 0; a < 12; ++a)
    for (uint16_t b = a + 1; b < 12; ++b)
      for (uint16_t c = b + 1; c < 12; ++c)
        for (uint16_t d = c + 1; d < 12; ++d)
          ranks.push_back(combinatorial_rank(std::array<uint16_t, 4>{{a,b,c,d}}));
  std::sort(ranks.begin(), ranks.end());
  if (std::unique(ranks.begin(), ranks.end()) != ranks.end() ||
      ranks.size() != 495)
    throw std::runtime_error("combinatorial-rank self-test failed");

  Signs sequence{};
  for (int index = 0; index < N; ++index)
    sequence[index] = ((index * index + 3 * index + 7) % 11 < 5) ? 1 : -1;
  const auto single = make_single_deltas(sequence);
  const std::array<uint16_t, 6> positions{{0, 5, 41, 100, 221, 332}};
  const Delta delta = exact_delta(sequence, single, positions);
  Signs changed = sequence;
  for (uint16_t position : positions) changed[position] = -changed[position];
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int before = 0;
    int after = 0;
    for (int index = 0; index < N; ++index) {
      before += sequence[index] * sequence[(index + lag) % N];
      after += changed[index] * changed[(index + lag) % N];
    }
    if ((after - before) / 2 != delta[lag])
      throw std::runtime_error("delta self-test failed");
  }
  std::cout << "PASS radius-two arithmetic self-test\n";
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
      self_test();
      return 0;
    }
    if (argc != 2) {
      std::cerr << "usage: verify_legendre_333_profile_radius2 CHECKPOINT.json\n"
                   "       verify_legendre_333_profile_radius2 --self-test\n";
      return 2;
    }

    std::ifstream input(argv[1]);
    if (!input) throw std::runtime_error("could not open checkpoint");
    const std::string document((std::istreambuf_iterator<char>(input)),
                               std::istreambuf_iterator<char>());
    const int profile = extract_integer(document, "profile");
    if (profile < 0)
      throw std::runtime_error("checkpoint profile index is negative");
    if (extract_integer(document, "length") != N)
      throw std::runtime_error("checkpoint length is not 333");
    const Sequences sequences = parse_sequences(document);
    const RowSums row_sums = verify_exact_profile_margins(sequences);
    verify_recorded_profile(document, row_sums);
    const Residuals residual = recompute_residuals(sequences);
    const int base_energy = energy(residual);
    std::cout << "checkpoint profile=" << profile
              << " length=" << N
              << " recomputed_baseline_energy=" << base_energy << '\n';

    const auto recorded_residuals =
        extract_array(document, "half_paf_residuals_1_through_166");
    if (recorded_residuals.size() != LAST_LAG)
      throw std::runtime_error("recorded residual-vector length mismatch");
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      if (recorded_residuals[lag - 1] != residual[lag])
        throw std::runtime_error("recorded residual disagrees with recomputation");
    if (extract_integer(document, "energy_half_paf") != base_energy)
      throw std::runtime_error("recorded energy disagrees with recomputation");

    std::array<SingleDeltas, 2> singles{{
        make_single_deltas(sequences[0]), make_single_deltas(sequences[1])}};
    std::array<std::vector<Move>, 2> moves{{
        enumerate_moves(sequences[0], singles[0], residual),
        enumerate_moves(sequences[1], singles[1], residual)}};

    bool improving_state_exists = false;
    std::array<NeighborhoodResult, 2> single_results;
    std::array<NeighborhoodResult, 2> pair_results;
    std::array<CycleResult, 2> cycle_results;
    uint64_t total_unique_nontrivial = 0;
    for (int which = 0; which < 2; ++which) {
      single_results[which] = audit_single_moves(moves[which], base_energy);
      print_neighborhood(which == 0 ? "A single" : "B single",
                         single_results[which]);
      improving_state_exists |=
          single_results[which].improving_representations != 0;

      pair_results[which] = audit_same_sequence_pairs(
          sequences, which, residual, moves[which]);
      print_neighborhood(which == 0 ? "A disjoint-pair" : "B disjoint-pair",
                         pair_results[which]);
      if (pair_results[which].found) {
        std::cout << "  best moves=";
        print_move(moves[which][pair_results[which].first]);
        std::cout << ',';
        print_move(moves[which][pair_results[which].second]);
        std::cout << '\n';
      }
      improving_state_exists |=
          pair_results[which].improving_representations != 0;

      cycle_results[which] =
          audit_six_cycles(sequences, which, singles[which], residual);
      std::cout << (which == 0 ? "A six-cycle" : "B six-cycle")
                << " raw_patterns=" << cycle_results[which].raw_patterns
                << " unique_alternating="
                << cycle_results[which].alternating_cycles
                << " improving=" << cycle_results[which].improving_cycles
                << " best_energy=" << cycle_results[which].best_energy << '\n';
      improving_state_exists |= cycle_results[which].improving_cycles != 0;

      const uint64_t unique_nontrivial_radius_two =
          single_results[which].unique_states + pair_results[which].unique_states +
          cycle_results[which].alternating_cycles;
      total_unique_nontrivial += unique_nontrivial_radius_two;
      std::cout << (which == 0 ? "A" : "B")
                << " unique_nontrivial_radius2_states="
                << unique_nontrivial_radius_two << '\n';
    }

    const NeighborhoodResult cross =
        audit_cross_pairs(sequences, residual, moves[0], moves[1]);
    print_neighborhood("A-cross-B pair", cross);
    if (cross.found) {
      std::cout << "  best moves=";
      print_move(moves[0][cross.first]);
      std::cout << ',';
      print_move(moves[1][cross.second]);
      std::cout << '\n';
    }
    improving_state_exists |= cross.improving_representations != 0;
    total_unique_nontrivial += cross.unique_states;
    std::cout << "total_unique_nontrivial_radius2_states="
              << total_unique_nontrivial
              << " radius2_ball_including_center="
              << total_unique_nontrivial + 1 << '\n';

    verify_profile6_regression(profile, checkpoint_fingerprint(sequences),
                               base_energy, single_results, pair_results,
                               cycle_results, cross,
                               total_unique_nontrivial);

    if (improving_state_exists) {
      std::cout << "FAIL found an exact radius-two state below baseline="
                << base_energy << '\n';
      return 1;
    }
    std::cout << "PASS no enumerated radius-two state has energy below "
              << "baseline=" << base_energy << '\n';
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
