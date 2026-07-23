// Fixed-row-and-column-margin local search for the prescribed LP(333) route.
//
// The two 9 by 37 CRT sign matrices have both their column plus-counts (the
// fixed Legendre length-37 compression) and the following exact length-9
// profile fixed.  Every proposal is one checkerboard 2 by 2 switch, so both
// sets of margins are invariants.  An optional escape proposal coordinates
// one legal switch in A with one legal switch in B and scores the resulting
// eight flips atomically; it is disabled by default.  Default-off exact polish
// modes additionally cover the Cartesian product of A/B switches and
// unordered disjoint switch pairs within A or B, alternating six-cycles on
// 3 by 3 CRT supports, mixed alternating-six-cycle/opposite-checker moves,
// and alternating eight-cycles on 4 by 4 CRT supports.  For lag k=1,...,166
// we store
//
//   residual[k] = (PAF_A(k) + PAF_B(k) + 2) / 2.
//
// Thus energy=sum(residual[k]^2) is an exact integer objective whose unique
// zero is a Legendre pair.  A nonzero output is explicitly a non-certificate
// checkpoint.  A zero output contains top-level `a` and `b` arrays accepted
// by verify_legendre_333.py, which must still be run independently.
//
// The implementation is deliberately single-threaded and fixed-memory for a
// 16 GiB workstation.  Cached single-flip PAF deltas make each four-cell
// checkerboard proposal O(166), and accepted moves update the cache exactly.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int N = 333;
constexpr int ROWS = 9;
constexpr int COLS = 37;
constexpr int LAST_LAG = 166;
constexpr int BASIC_MOVE_SIZE = 4;
constexpr int MAX_MOVE_SIZE = 10;

using Clock = std::chrono::steady_clock;
using Signs = std::array<int8_t, N>;
using Residuals = std::array<int16_t, LAST_LAG + 1>;
using Delta = std::array<int16_t, LAST_LAG + 1>;
using SingleDeltas = std::vector<std::array<int8_t, LAST_LAG + 1>>;

struct Options {
  double seconds = 30.0;
  uint64_t iterations = 0;
  uint64_t seed = 668;
  int profile = 0;
  bool profile_explicit = false;
  uint64_t epoch = 250000;
  int polish_steps = 16;
  int initial_mix_switches = 4096;
  int late_window = 4096;
  int validate_every = 500000;
  std::string mode = "anneal";  // late or anneal.
  double temperature_start = 64.0;
  double temperature_end = 0.2;
  double compound_probability = 0.0;
  bool cross_pair_polish = false;
  int cross_pair_max_rounds = 16;
  bool same_sequence_pair_polish = false;
  int same_sequence_pair_max_rounds = 16;
  bool six_cycle_polish = false;
  int six_cycle_max_rounds = 16;
  bool eight_cycle_polish = false;
  int eight_cycle_max_rounds = 16;
  bool mixed_six_cycle_polish = false;
  int mixed_six_cycle_max_rounds = 16;
  bool polish_only = false;
  std::string initial_checkpoint;
  std::string output = "output/legendre_333_profile_local_best.json";
  bool quiet = false;
  bool self_test = false;
};

struct State {
  int profile = 0;
  std::array<Signs, 2> sequence{};
  std::array<SingleDeltas, 2> single{};
  Residuals residual{};
  int64_t energy = 0;
};

struct Metrics {
  int64_t energy = 0;
  int nonzero = 0;
  int max_abs = 0;
  int64_t l1 = 0;

  auto key() const { return std::tie(energy, nonzero, max_abs, l1); }
};

struct Candidate {
  int profile = 0;
  std::array<Signs, 2> sequence{};
  Residuals residual{};
  Metrics metrics{};
  uint64_t proposals = 0;
  uint64_t accepted = 0;
  uint64_t restarts = 0;
  uint64_t polish_moves = 0;
  uint64_t neighborhood_evaluations = 0;
  bool initialized = false;
};

struct Move {
  std::array<int, MAX_MOVE_SIZE> position{};  // 0..332=A, 333..665=B.
  int size = 0;
};

struct SearchResult {
  Candidate best{};
  uint64_t proposals = 0;
  uint64_t accepted = 0;
  uint64_t compound_proposals = 0;
  uint64_t compound_accepted = 0;
  uint64_t restarts = 0;
  uint64_t polish_moves = 0;
  uint64_t cross_pair_polish_moves = 0;
  uint64_t cross_pair_scans = 0;
  uint64_t complete_cross_pair_scans = 0;
  uint64_t cross_pair_evaluations = 0;
  uint64_t incomplete_cross_pair_scans = 0;
  uint64_t last_cross_pair_evaluations = 0;
  size_t last_cross_pair_a_components = 0;
  size_t last_cross_pair_b_components = 0;
  uint64_t same_sequence_pair_polish_moves = 0;
  uint64_t same_sequence_pair_scans = 0;
  uint64_t complete_same_sequence_pair_scans = 0;
  uint64_t same_sequence_pair_evaluations = 0;
  uint64_t same_sequence_pair_overlap_skips = 0;
  uint64_t incomplete_same_sequence_pair_scans = 0;
  uint64_t last_same_sequence_pair_evaluations = 0;
  uint64_t last_same_sequence_pair_overlap_skips = 0;
  std::array<size_t, 2> last_same_sequence_pair_components{};
  std::array<uint64_t, 2> last_same_sequence_pair_evaluations_by_sequence{};
  std::array<uint64_t, 2> last_same_sequence_pair_overlap_skips_by_sequence{};
  uint64_t six_cycle_polish_moves = 0;
  uint64_t six_cycle_scans = 0;
  uint64_t complete_six_cycle_scans = 0;
  uint64_t six_cycle_raw_patterns = 0;
  uint64_t six_cycle_valid_cycles = 0;
  uint64_t six_cycle_evaluations = 0;
  uint64_t incomplete_six_cycle_scans = 0;
  std::array<uint64_t, 2> last_six_cycle_raw_patterns{};
  std::array<uint64_t, 2> last_six_cycle_valid_cycles{};
  std::array<uint64_t, 2> last_six_cycle_evaluations{};
  uint64_t eight_cycle_polish_moves = 0;
  uint64_t eight_cycle_scans = 0;
  uint64_t complete_eight_cycle_scans = 0;
  uint64_t incomplete_eight_cycle_scans = 0;
  uint64_t eight_cycle_row_cycles = 0;
  uint64_t eight_cycle_sign_orientations = 0;
  uint64_t eight_cycle_raw_assignments = 0;
  uint64_t eight_cycle_repeated_column_skips = 0;
  uint64_t eight_cycle_legal_cycles = 0;
  uint64_t eight_cycle_evaluations = 0;
  std::array<uint64_t, 2> last_eight_cycle_row_cycles{};
  std::array<uint64_t, 2> last_eight_cycle_sign_orientations{};
  std::array<uint64_t, 2> last_eight_cycle_raw_assignments{};
  std::array<uint64_t, 2> last_eight_cycle_repeated_column_skips{};
  std::array<uint64_t, 2> last_eight_cycle_legal_cycles{};
  std::array<uint64_t, 2> last_eight_cycle_evaluations{};
  uint64_t mixed_six_cycle_polish_moves = 0;
  uint64_t mixed_six_cycle_scans = 0;
  uint64_t complete_mixed_six_cycle_scans = 0;
  uint64_t incomplete_mixed_six_cycle_scans = 0;
  uint64_t mixed_six_cycle_raw_patterns = 0;
  uint64_t mixed_six_cycle_legal_cycles = 0;
  uint64_t mixed_six_cycle_queries = 0;
  uint64_t mixed_six_cycle_possible_pair_distances = 0;
  uint64_t mixed_six_cycle_pair_distances = 0;
  uint64_t mixed_six_cycle_tree_nodes = 0;
  uint64_t mixed_six_cycle_tree_node_visits = 0;
  uint64_t mixed_six_cycle_box_tests = 0;
  uint64_t mixed_six_cycle_pruned_subtrees = 0;
  uint64_t mixed_six_cycle_pruned_points = 0;
  std::array<uint64_t, 2> last_mixed_six_cycle_raw_patterns{};
  std::array<uint64_t, 2> last_mixed_six_cycle_legal_cycles{};
  std::array<uint64_t, 2> last_mixed_six_cycle_queries{};
  std::array<size_t, 2> last_mixed_six_cycle_checker_components{};
  uint64_t neighborhood_evaluations = 0;
};

using RowVector = std::array<int, ROWS>;
using RowProfile = std::array<RowVector, 2>;
constexpr int PROFILE_COUNT = 21;

constexpr std::array<RowProfile, PROFILE_COUNT> ROW_SUM_PROFILES{{
    RowProfile{{
        RowVector{{-21, 3, 5, 5, 1, 5, 1, -1, 3}},
        RowVector{{-3, 3, 3, -3, -3, 1, 1, 3, -1}},
    }},
    RowProfile{{
        RowVector{{15, 5, -9, 3, -5, 1, -7, 1, -3}},
        RowVector{{11, 3, -3, 1, -1, -3, -1, -3, -3}},
    }},
    RowProfile{{
        RowVector{{9, 5, 5, 5, -5, 1, -3, -1, -15}},
        RowVector{{7, 3, -3, 3, -1, 1, 3, -9, -3}},
    }},
    RowProfile{{
        RowVector{{11, 9, -13, 1, -5, 1, -1, -3, 1}},
        RowVector{{5, 5, 1, -5, 5, -9, -1, 1, -1}},
    }},
    RowProfile{{
        RowVector{{9, 7, 1, 3, 1, -1, 3, -9, -13}},
        RowVector{{7, 1, -3, 5, -5, 1, -7, 5, -3}},
    }},
    RowProfile{{
        RowVector{{9, 7, -3, -3, -13, -1, 5, 5, -5}},
        RowVector{{7, -1, -5, 5, -5, 5, 1, 1, -7}},
    }},
    RowProfile{{
        RowVector{{11, 7, -9, 5, 3, -7, -5, -5, 1}},
        RowVector{{7, -1, 5, -3, 7, -5, -5, 1, -5}},
    }},
    RowProfile{{
        RowVector{{17, 3, 1, -3, -5, -3, -1, -3, -5}},
        RowVector{{11, -3, -3, -3, 3, 1, 3, -1, -7}},
    }},
    RowProfile{{
        RowVector{{9, 5, -5, 1, -3, -7, 1, -5, 5}},
        RowVector{{7, 3, 3, -13, 1, 7, -7, 3, -3}},
    }},
    RowProfile{{
        RowVector{{15, 3, -5, -5, 1, -7, 1, 1, -3}},
        RowVector{{7, 5, 1, -7, 1, -5, 7, -7, -1}},
    }},
    RowProfile{{
        RowVector{{13, 5, -9, -3, -5, 1, 1, -1, -1}},
        RowVector{{11, -1, 1, 1, -9, -1, 1, 5, -7}},
    }},
    RowProfile{{
        RowVector{{9, 9, 1, -1, -9, 1, -3, 1, -7}},
        RowVector{{9, -5, -5, -1, 5, 1, 7, -1, -9}},
    }},
    RowProfile{{
        RowVector{{11, 5, -3, 5, -11, 1, -3, -1, -3}},
        RowVector{{7, 3, 7, -3, -7, -3, 7, -5, -5}},
    }},
    RowProfile{{
        RowVector{{13, 9, -7, 3, -11, -1, -1, 1, -5}},
        RowVector{{7, -1, -3, -3, 5, 3, 1, -3, -5}},
    }},
    RowProfile{{
        RowVector{{13, 11, -7, -1, -1, 1, -9, 3, -9}},
        RowVector{{5, 3, 3, -1, -3, -1, -1, -5, 1}},
    }},
    RowProfile{{
        RowVector{{11, 7, -5, -1, -3, -5, 7, -15, 5}},
        RowVector{{5, 1, 3, -1, -1, -1, -5, -1, 1}},
    }},
    RowProfile{{
        RowVector{{11, 7, -1, -1, -5, -3, 1, 3, -11}},
        RowVector{{11, 3, 3, -3, -9, 1, -1, 1, -5}},
    }},
    RowProfile{{
        RowVector{{11, 7, 1, -1, -1, -5, 1, -11, -1}},
        RowVector{{9, 1, -7, 3, 3, 1, -7, 5, -7}},
    }},
    RowProfile{{
        RowVector{{11, 9, -3, 3, 3, -3, -1, -9, -9}},
        RowVector{{7, -3, 1, 1, 3, 3, -5, 3, -9}},
    }},
    RowProfile{{
        RowVector{{13, 1, 1, -3, -1, -13, 7, -5, 1}},
        RowVector{{7, 5, -1, -5, -3, 5, 1, -3, -5}},
    }},
    RowProfile{{
        RowVector{{7, 1, 1, -1, -1, -5, 1, -1, -1}},
        RowVector{{5, 3, 1, 3, 3, 1, 3, -21, 3}},
    }},
}};

std::array<RowProfile, PROFILE_COUNT> ROW_PLUS_COUNTS{};

std::array<std::array<int, COLS>, ROWS> make_crt_table() {
  std::array<std::array<int, COLS>, ROWS> table{};
  for (int row = 0; row < ROWS; ++row) {
    for (int column = 0; column < COLS; ++column) {
      const int multiplier = ((row - column) % ROWS + ROWS) % ROWS;
      table[row][column] = column + COLS * multiplier;
    }
  }
  return table;
}

std::array<std::array<uint16_t, N>, N> make_distance_table() {
  std::array<std::array<uint16_t, N>, N> table{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      const int raw = std::abs(i - j);
      table[i][j] = static_cast<uint16_t>(std::min(raw, N - raw));
    }
  }
  return table;
}

const auto CRT = make_crt_table();
const auto DISTANCE = make_distance_table();

int legendre_symbol_37(int value) {
  value %= COLS;
  if (value < 0) value += COLS;
  if (value == 0) return 0;
  int power = 1;
  for (int i = 0; i < (COLS - 1) / 2; ++i) power = power * value % COLS;
  if (power == 1) return 1;
  if (power == COLS - 1) return -1;
  throw std::runtime_error("Euler criterion failure");
}

std::array<std::array<int, COLS>, 2> make_column_plus_counts() {
  std::array<std::array<int, COLS>, 2> result{};
  result[0][0] = result[1][0] = 5;
  for (int column = 1; column < COLS; ++column) {
    const int character = legendre_symbol_37(column);
    result[0][column] = character == 1 ? 6 : 3;
    result[1][column] = character == 1 ? 3 : 6;
  }
  return result;
}

const auto COLUMN_PLUS_COUNTS = make_column_plus_counts();

uint64_t splitmix64(uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

Metrics compute_metrics(const Residuals &residual) {
  Metrics result;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int64_t value = residual[lag];
    result.energy += value * value;
    result.nonzero += value != 0;
    result.max_abs = std::max(result.max_abs, std::abs(static_cast<int>(value)));
    result.l1 += std::abs(value);
  }
  return result;
}

bool better(const Candidate &left, const Candidate &right) {
  if (!right.initialized) return true;
  if (left.metrics.key() != right.metrics.key())
    return left.metrics.key() < right.metrics.key();
  if (left.sequence[0] != right.sequence[0])
    return left.sequence[0] < right.sequence[0];
  return left.sequence[1] < right.sequence[1];
}

void initialize_and_verify_profiles() {
  for (int profile = 0; profile < PROFILE_COUNT; ++profile) {
    for (int which = 0; which < 2; ++which) {
      for (int row = 0; row < ROWS; ++row) {
        const int row_sum = ROW_SUM_PROFILES[profile][which][row];
        if (row_sum < -COLS || row_sum > COLS || row_sum % 2 == 0)
          throw std::runtime_error("catalog row sum is outside the odd range");
        ROW_PLUS_COUNTS[profile][which][row] = (COLS + row_sum) / 2;
      }
      const int row_total = std::accumulate(
          ROW_PLUS_COUNTS[profile][which].begin(),
          ROW_PLUS_COUNTS[profile][which].end(), 0);
      const int column_total =
          std::accumulate(COLUMN_PLUS_COUNTS[which].begin(),
                          COLUMN_PLUS_COUNTS[which].end(), 0);
      if (row_total != 167 || column_total != 167 ||
          row_total != column_total)
        throw std::runtime_error("catalog margin totals are inconsistent");
      if (std::accumulate(ROW_SUM_PROFILES[profile][which].begin(),
                          ROW_SUM_PROFILES[profile][which].end(), 0) != 1)
        throw std::runtime_error("catalog row sums do not normalize to one");
    }

    int zero_lag = 0;
    for (int which = 0; which < 2; ++which)
      for (const int value : ROW_SUM_PROFILES[profile][which])
        zero_lag += value * value;
    if (zero_lag != 594)
      throw std::runtime_error("catalog profile has the wrong zero-lag norm");
    for (int lag = 1; lag < ROWS; ++lag) {
      int paf_sum = 0;
      for (int which = 0; which < 2; ++which)
        for (int row = 0; row < ROWS; ++row)
          paf_sum += ROW_SUM_PROFILES[profile][which][row] *
                     ROW_SUM_PROFILES[profile][which][(row + lag) % ROWS];
      if (paf_sum != -74)
        throw std::runtime_error("catalog profile PAF identity failure");
    }
  }
}

void recompute(State &state) {
  state.residual.fill(0);
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int paf_sum = 0;
    for (int which = 0; which < 2; ++which) {
      const auto &sequence = state.sequence[which];
      for (int i = 0; i < N; ++i)
        paf_sum += sequence[i] * sequence[(i + lag) % N];
    }
    if ((paf_sum + 2) % 4 != 0)
      throw std::runtime_error("periodic-correlation mod-four parity failure");
    state.residual[lag] = static_cast<int16_t>((paf_sum + 2) / 2);
  }
  state.energy = compute_metrics(state.residual).energy;

  for (int which = 0; which < 2; ++which) {
    state.single[which].resize(N);
    const auto &sequence = state.sequence[which];
    for (int position = 0; position < N; ++position) {
      state.single[which][position][0] = 0;
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        const int neighbors = sequence[(position + lag) % N] +
                              sequence[(position - lag + N) % N];
        state.single[which][position][lag] = static_cast<int8_t>(
            -sequence[position] * neighbors);
      }
    }
  }
}

template <typename Rng>
Signs realize_margins(int profile, int which, Rng &rng) {
  Signs sequence{};
  sequence.fill(-1);
  std::array<int, ROWS> remaining = ROW_PLUS_COUNTS[profile][which];

  // Bipartite Havel-Hakimi: process column degrees in descending order and
  // attach each column to rows with largest residual degree.  Randomized tie
  // order gives independent realizations without changing correctness.
  std::array<int, COLS> columns{};
  std::iota(columns.begin(), columns.end(), 0);
  std::shuffle(columns.begin(), columns.end(), rng);
  std::stable_sort(columns.begin(), columns.end(), [&](int left, int right) {
    return COLUMN_PLUS_COUNTS[which][left] >
           COLUMN_PLUS_COUNTS[which][right];
  });

  for (const int column : columns) {
    std::array<int, ROWS> rows{};
    std::iota(rows.begin(), rows.end(), 0);
    std::shuffle(rows.begin(), rows.end(), rng);
    std::stable_sort(rows.begin(), rows.end(), [&](int left, int right) {
      return remaining[left] > remaining[right];
    });
    const int degree = COLUMN_PLUS_COUNTS[which][column];
    for (int j = 0; j < degree; ++j) {
      const int row = rows[j];
      if (remaining[row] <= 0)
        throw std::runtime_error("profile margins are not bipartite graphical");
      sequence[CRT[row][column]] = 1;
      --remaining[row];
    }
  }
  if (std::any_of(remaining.begin(), remaining.end(),
                  [](int value) { return value != 0; }))
    throw std::runtime_error("Havel-Hakimi realization left a row deficit");
  return sequence;
}

bool checkerboard(const Signs &sequence, int row1, int row2,
                  int column1, int column2) {
  const int a = sequence[CRT[row1][column1]];
  const int b = sequence[CRT[row1][column2]];
  const int c = sequence[CRT[row2][column1]];
  const int d = sequence[CRT[row2][column2]];
  return a == d && b == c && a != b;
}

Move make_checkerboard_move(int which, int row1, int row2,
                            int column1, int column2) {
  Move move;
  move.size = BASIC_MOVE_SIZE;
  move.position = {{
      which * N + CRT[row1][column1],
      which * N + CRT[row1][column2],
      which * N + CRT[row2][column1],
      which * N + CRT[row2][column2],
  }};
  return move;
}

template <typename Rng>
bool random_checkerboard_move(const Signs &sequence, int which, Rng &rng,
                              Move &move) {
  for (int attempt = 0; attempt < 256; ++attempt) {
    int row1 = static_cast<int>(rng() % ROWS);
    int row2 = static_cast<int>(rng() % (ROWS - 1));
    if (row2 >= row1) ++row2;
    int column1 = static_cast<int>(rng() % COLS);
    int column2 = static_cast<int>(rng() % (COLS - 1));
    if (column2 >= column1) ++column2;
    if (!checkerboard(sequence, row1, row2, column1, column2)) continue;
    move = make_checkerboard_move(which, row1, row2, column1, column2);
    return true;
  }

  // A deterministic scan with reservoir sampling makes failure exact rather
  // than an unlucky random event.
  uint64_t seen = 0;
  for (int row1 = 0; row1 < ROWS; ++row1) {
    for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
      for (int column1 = 0; column1 < COLS; ++column1) {
        for (int column2 = column1 + 1; column2 < COLS; ++column2) {
          if (!checkerboard(sequence, row1, row2, column1, column2)) continue;
          ++seen;
          if (rng() % seen == 0)
            move = make_checkerboard_move(
                which, row1, row2, column1, column2);
        }
      }
    }
  }
  return seen != 0;
}

void flip_direct(Signs &sequence, const Move &move, int which) {
  if (move.size != BASIC_MOVE_SIZE)
    throw std::runtime_error("checkerboard move has the wrong size");
  for (int entry = 0; entry < move.size; ++entry) {
    if (move.position[entry] / N != which)
      throw std::runtime_error("checkerboard move crosses sequences");
    const int position = move.position[entry] % N;
    sequence[position] = -sequence[position];
  }
}

void flip_direct_all(std::array<Signs, 2> &sequences, const Move &move) {
  if (move.size <= 0 || move.size > MAX_MOVE_SIZE)
    throw std::runtime_error("direct move size is out of range");
  for (int entry = 0; entry < move.size; ++entry) {
    const int global = move.position[entry];
    if (global < 0 || global >= 2 * N)
      throw std::runtime_error("direct move position is out of range");
    for (int earlier = 0; earlier < entry; ++earlier)
      if (move.position[earlier] == global)
        throw std::runtime_error("direct move repeats a position");
    sequences[global / N][global % N] =
        -sequences[global / N][global % N];
  }
}

template <typename Rng>
State random_state(int profile, Rng &rng, int mix_switches) {
  State state;
  state.profile = profile;
  for (int which = 0; which < 2; ++which) {
    state.sequence[which] = realize_margins(profile, which, rng);
    for (int step = 0; step < mix_switches; ++step) {
      Move move;
      if (!random_checkerboard_move(state.sequence[which], which, rng, move))
        throw std::runtime_error("margin fiber has no checkerboard switch");
      flip_direct(state.sequence[which], move, which);
    }
  }
  recompute(state);
  return state;
}

template <typename Rng>
Move random_move(const State &state, Rng &rng) {
  const int first = static_cast<int>(rng() & 1ULL);
  Move move;
  if (random_checkerboard_move(state.sequence[first], first, rng, move))
    return move;
  if (random_checkerboard_move(state.sequence[1 - first], 1 - first, rng,
                               move))
    return move;
  throw std::runtime_error("both fixed-margin fibers have no legal switch");
}

template <typename Rng>
Move coordinated_compound_move(const State &state, Rng &rng) {
  Move left, right;
  if (!random_checkerboard_move(state.sequence[0], 0, rng, left) ||
      !random_checkerboard_move(state.sequence[1], 1, rng, right))
    throw std::runtime_error(
        "coordinated compound move requires a switch in both fibers");
  if (left.size != BASIC_MOVE_SIZE || right.size != BASIC_MOVE_SIZE)
    throw std::runtime_error("compound component has the wrong size");

  Move result;
  result.size = 2 * BASIC_MOVE_SIZE;
  for (int entry = 0; entry < BASIC_MOVE_SIZE; ++entry) {
    result.position[entry] = left.position[entry];
    result.position[BASIC_MOVE_SIZE + entry] = right.position[entry];
  }
  return result;
}

Delta correlation_delta(const State &state, const Move &move) {
  Delta delta{};
  for (int entry = 0; entry < move.size; ++entry) {
    const int global = move.position[entry];
    const int which = global / N;
    const int position = global % N;
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      delta[lag] += state.single[which][position][lag];
  }

  // The cached single-flip deltas count a flipped/flipped product twice,
  // while flipping both endpoints leaves that product unchanged.
  for (int left = 0; left < move.size; ++left) {
    const int global_left = move.position[left];
    const int which = global_left / N;
    const int position_left = global_left % N;
    for (int right = left + 1; right < move.size; ++right) {
      const int global_right = move.position[right];
      if (global_right / N != which) continue;
      const int position_right = global_right % N;
      const int lag = DISTANCE[position_left][position_right];
      if (lag <= 0 || lag > LAST_LAG)
        throw std::runtime_error("checkerboard move repeats a position");
      delta[lag] += static_cast<int16_t>(
          2 * state.sequence[which][position_left] *
          state.sequence[which][position_right]);
    }
  }
  return delta;
}

int64_t energy_after(const State &state, const Delta &delta) {
  int64_t result = state.energy;
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    result += 2LL * state.residual[lag] * delta[lag] +
              1LL * delta[lag] * delta[lag];
  return result;
}

void apply_move(State &state, const Move &move, const Delta &delta) {
  state.energy = energy_after(state, delta);
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    state.residual[lag] += delta[lag];

  for (int which = 0; which < 2; ++which) {
    std::array<int, MAX_MOVE_SIZE> positions{};
    std::array<int8_t, MAX_MOVE_SIZE> old_signs{};
    int count = 0;
    for (int entry = 0; entry < move.size; ++entry) {
      if (move.position[entry] / N != which) continue;
      positions[count] = move.position[entry] % N;
      old_signs[count] = state.sequence[which][positions[count]];
      ++count;
    }
    if (count == 0) continue;

    for (int j = 0; j < count; ++j)
      state.sequence[which][positions[j]] = -old_signs[j];

    for (int j = 0; j < count; ++j) {
      const int flipped = positions[j];
      for (int position = 0; position < N; ++position) {
        bool is_flipped = false;
        for (int q = 0; q < count; ++q)
          is_flipped |= position == positions[q];
        if (is_flipped) continue;
        const int lag = DISTANCE[position][flipped];
        state.single[which][position][lag] += static_cast<int8_t>(
            2 * state.sequence[which][position] * old_signs[j]);
      }
    }

    for (int j = 0; j < count; ++j) {
      const int position = positions[j];
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        const int neighbors =
            state.sequence[which][(position + lag) % N] +
            state.sequence[which][(position - lag + N) % N];
        state.single[which][position][lag] = static_cast<int8_t>(
            -state.sequence[which][position] * neighbors);
      }
    }
  }
}

void validate_margins(const State &state) {
  if (state.profile < 0 || state.profile >= PROFILE_COUNT)
    throw std::runtime_error("state profile index is out of range");
  for (int which = 0; which < 2; ++which) {
    int total_plus = 0;
    for (int row = 0; row < ROWS; ++row) {
      int plus = 0;
      for (int column = 0; column < COLS; ++column)
        plus += state.sequence[which][CRT[row][column]] == 1;
      if (plus != ROW_PLUS_COUNTS[state.profile][which][row])
        throw std::runtime_error("fixed row-margin invariant failure");
      total_plus += plus;
    }
    for (int column = 0; column < COLS; ++column) {
      int plus = 0;
      for (int row = 0; row < ROWS; ++row)
        plus += state.sequence[which][CRT[row][column]] == 1;
      if (plus != COLUMN_PLUS_COUNTS[which][column])
        throw std::runtime_error("fixed column-margin invariant failure");
    }
    if (total_plus != 167)
      throw std::runtime_error("sequence normalization failure");
  }
}

void validate(const State &state) {
  validate_margins(state);
  State exact;
  exact.profile = state.profile;
  exact.sequence = state.sequence;
  recompute(exact);
  if (exact.residual != state.residual || exact.energy != state.energy ||
      exact.single != state.single)
    throw std::runtime_error("incremental periodic-correlation cache failure");
}

struct ParsedCheckpoint {
  int profile = 0;
  std::array<Signs, 2> sequence{};
};

void skip_json_space(const std::string &text, size_t &position) {
  while (position < text.size() &&
         (text[position] == ' ' || text[position] == '\n' ||
          text[position] == '\r' || text[position] == '\t'))
    ++position;
}

size_t unique_json_field_value(const std::string &text,
                               const std::string &field) {
  const std::string needle = "\"" + field + "\"";
  const size_t found = text.find(needle);
  if (found == std::string::npos)
    throw std::runtime_error("initial checkpoint is missing field: " + field);
  if (text.find(needle, found + needle.size()) != std::string::npos)
    throw std::runtime_error("initial checkpoint repeats field: " + field);
  size_t position = found + needle.size();
  skip_json_space(text, position);
  if (position >= text.size() || text[position++] != ':')
    throw std::runtime_error("initial checkpoint field has no colon: " + field);
  skip_json_space(text, position);
  return position;
}

int parse_json_integer(const std::string &text, size_t &position,
                       const std::string &field) {
  skip_json_space(text, position);
  bool negative = false;
  if (position < text.size() && text[position] == '-') {
    negative = true;
    ++position;
  }
  if (position >= text.size() || text[position] < '0' || text[position] > '9')
    throw std::runtime_error("initial checkpoint has a noninteger " + field);
  const size_t first_digit = position;
  int64_t magnitude = 0;
  while (position < text.size() && text[position] >= '0' &&
         text[position] <= '9') {
    magnitude = 10 * magnitude + (text[position] - '0');
    if (magnitude > static_cast<int64_t>(std::numeric_limits<int>::max()) + 1)
      throw std::runtime_error("initial checkpoint integer is out of range");
    ++position;
  }
  if (text[first_digit] == '0' && position > first_digit + 1)
    throw std::runtime_error("initial checkpoint integer has a leading zero");
  const int64_t value = negative ? -magnitude : magnitude;
  if (value < std::numeric_limits<int>::min() ||
      value > std::numeric_limits<int>::max())
    throw std::runtime_error("initial checkpoint integer is out of range");
  return static_cast<int>(value);
}

Signs parse_checkpoint_signs(const std::string &text,
                             const std::string &field) {
  size_t position = unique_json_field_value(text, field);
  if (position >= text.size() || text[position++] != '[')
    throw std::runtime_error("initial checkpoint field is not an array: " + field);
  Signs result{};
  for (int index = 0; index < N; ++index) {
    const int value = parse_json_integer(text, position, field);
    if (value != -1 && value != 1)
      throw std::runtime_error("initial checkpoint sequence is not a sign vector");
    result[index] = static_cast<int8_t>(value);
    skip_json_space(text, position);
    const char expected = index + 1 == N ? ']' : ',';
    if (position >= text.size() || text[position++] != expected)
      throw std::runtime_error(
          "initial checkpoint sequence has the wrong length or delimiter");
  }
  skip_json_space(text, position);
  if (position >= text.size() ||
      (text[position] != ',' && text[position] != '}'))
    throw std::runtime_error("initial checkpoint array has trailing garbage");
  return result;
}

ParsedCheckpoint parse_checkpoint_text(const std::string &text) {
  size_t beginning = 0;
  skip_json_space(text, beginning);
  size_t ending = text.size();
  while (ending > beginning &&
         (text[ending - 1] == ' ' || text[ending - 1] == '\n' ||
          text[ending - 1] == '\r' || text[ending - 1] == '\t'))
    --ending;
  if (beginning >= ending || text[beginning] != '{' || text[ending - 1] != '}')
    throw std::runtime_error("initial checkpoint is not a JSON object");

  ParsedCheckpoint result;
  size_t profile_position = unique_json_field_value(text, "profile");
  result.profile = parse_json_integer(text, profile_position, "profile");
  skip_json_space(text, profile_position);
  if (profile_position >= text.size() ||
      (text[profile_position] != ',' && text[profile_position] != '}'))
    throw std::runtime_error("initial checkpoint profile is malformed");
  if (result.profile < 0 || result.profile >= PROFILE_COUNT)
    throw std::runtime_error("initial checkpoint profile is out of range");
  result.sequence[0] = parse_checkpoint_signs(text, "a");
  result.sequence[1] = parse_checkpoint_signs(text, "b");
  return result;
}

State state_from_checkpoint_text(const std::string &text) {
  const ParsedCheckpoint parsed = parse_checkpoint_text(text);
  State state;
  state.profile = parsed.profile;
  state.sequence = parsed.sequence;
  recompute(state);
  validate(state);
  return state;
}

State load_initial_checkpoint(const std::string &path) {
  constexpr std::streamoff MAX_CHECKPOINT_BYTES = 1 << 20;
  std::ifstream input(path, std::ios::binary);
  if (!input)
    throw std::runtime_error("could not open initial checkpoint: " + path);
  input.seekg(0, std::ios::end);
  const std::streamoff length = input.tellg();
  if (length < 0 || length > MAX_CHECKPOINT_BYTES)
    throw std::runtime_error("initial checkpoint exceeds the 1 MiB limit");
  input.seekg(0, std::ios::beg);
  std::string text(static_cast<size_t>(length), '\0');
  if (length > 0)
    input.read(text.data(), length);
  if (!input && length > 0)
    throw std::runtime_error("could not read complete initial checkpoint");
  return state_from_checkpoint_text(text);
}

Candidate make_candidate(const State &state, const SearchResult &counters) {
  Candidate result;
  result.profile = state.profile;
  result.sequence = state.sequence;
  result.residual = state.residual;
  result.metrics = compute_metrics(state.residual);
  result.proposals = counters.proposals;
  result.accepted = counters.accepted;
  result.restarts = counters.restarts;
  result.polish_moves = counters.polish_moves;
  result.neighborhood_evaluations = counters.neighborhood_evaluations;
  result.initialized = true;
  return result;
}

State state_from_candidate(const Candidate &candidate) {
  State state;
  state.profile = candidate.profile;
  state.sequence = candidate.sequence;
  recompute(state);
  return state;
}

void consider_best(const State &state, SearchResult &result,
                   const Options &options) {
  if (result.best.initialized && state.energy > result.best.metrics.energy)
    return;
  const Candidate candidate = make_candidate(state, result);
  if (!better(candidate, result.best)) return;
  result.best = candidate;
  if (!options.quiet) {
    std::cerr << "best energy_half_paf=" << candidate.metrics.energy
              << " bad=" << candidate.metrics.nonzero
              << " max_abs_paf_residual=" << 2 * candidate.metrics.max_abs
              << " l1_paf_residual=" << 2 * candidate.metrics.l1 << '\n';
  }
}

struct ImprovingMove {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  bool found = false;
};

struct CheckerboardComponent {
  std::array<int, BASIC_MOVE_SIZE> position{};
  Delta delta{};
  int64_t linear_energy_change = 0;
};

using KdTarget = std::array<int32_t, LAST_LAG + 1>;

struct KdSearchStats {
  uint64_t node_visits = 0;
  uint64_t point_distances = 0;
  uint64_t box_tests = 0;
  uint64_t pruned_subtrees = 0;
  uint64_t pruned_points = 0;
};

struct KdQueryResult {
  int point_index = -1;
  int64_t distance = std::numeric_limits<int64_t>::max();
  KdSearchStats stats{};
  bool complete = false;
};

struct DeltaKdNode {
  std::array<int16_t, LAST_LAG + 1> lower{};
  std::array<int16_t, LAST_LAG + 1> upper{};
  int point_index = -1;
  int left = -1;
  int right = -1;
  int split_dimension = 1;
  int subtree_size = 1;
};

class ExactDeltaKdTree {
 public:
  ExactDeltaKdTree(const std::vector<CheckerboardComponent> &points,
                   Clock::time_point deadline, bool use_deadline)
      : points_(points), deadline_(deadline), use_deadline_(use_deadline) {
    order_.resize(points_.size());
    std::iota(order_.begin(), order_.end(), 0);
    nodes_.reserve(points_.size());
    root_ = build(0, static_cast<int>(order_.size()));
    if (build_complete_ && nodes_.size() != points_.size())
      throw std::runtime_error("kd-tree node count mismatch");
  }

  bool complete() const { return build_complete_; }
  size_t point_count() const { return points_.size(); }
  size_t node_count() const { return nodes_.size(); }

  KdQueryResult nearest(const KdTarget &target) const {
    KdQueryResult result;
    if (!build_complete_) return result;
    result.complete = true;
    if (root_ >= 0) search_node(root_, target, result);
    if (!result.complete) {
      result.point_index = -1;
      result.distance = std::numeric_limits<int64_t>::max();
      return result;
    }
    if (result.stats.point_distances + result.stats.pruned_points !=
        points_.size())
      throw std::runtime_error("kd-tree exact coverage count mismatch");
    return result;
  }

 private:
  int build(int begin, int end) {
    if (begin >= end || !build_complete_) return -1;
    if (use_deadline_ && Clock::now() >= deadline_) {
      build_complete_ = false;
      return -1;
    }

    std::array<int16_t, LAST_LAG + 1> lower{}, upper{};
    const Delta &first = points_[order_[begin]].delta;
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      lower[lag] = upper[lag] = first[lag];
    for (int offset = begin + 1; offset < end; ++offset) {
      const Delta &delta = points_[order_[offset]].delta;
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        lower[lag] = std::min(lower[lag], delta[lag]);
        upper[lag] = std::max(upper[lag], delta[lag]);
      }
    }
    int split_dimension = 1;
    int widest = upper[1] - lower[1];
    for (int lag = 2; lag <= LAST_LAG; ++lag) {
      const int width = upper[lag] - lower[lag];
      if (width > widest) {
        widest = width;
        split_dimension = lag;
      }
    }

    const int middle = begin + (end - begin) / 2;
    std::nth_element(
        order_.begin() + begin, order_.begin() + middle,
        order_.begin() + end, [&](int left, int right) {
          const int left_value = points_[left].delta[split_dimension];
          const int right_value = points_[right].delta[split_dimension];
          return left_value != right_value ? left_value < right_value
                                           : left < right;
        });
    const int node_index = static_cast<int>(nodes_.size());
    nodes_.emplace_back();
    nodes_[node_index].point_index = order_[middle];
    nodes_[node_index].split_dimension = split_dimension;
    nodes_[node_index].left = build(begin, middle);
    nodes_[node_index].right = build(middle + 1, end);
    if (!build_complete_) return node_index;

    DeltaKdNode &node = nodes_[node_index];
    const Delta &point = points_[node.point_index].delta;
    for (int lag = 1; lag <= LAST_LAG; ++lag)
      node.lower[lag] = node.upper[lag] = point[lag];
    for (const int child : {node.left, node.right}) {
      if (child < 0) continue;
      node.subtree_size += nodes_[child].subtree_size;
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        node.lower[lag] = std::min(node.lower[lag], nodes_[child].lower[lag]);
        node.upper[lag] = std::max(node.upper[lag], nodes_[child].upper[lag]);
      }
    }
    return node_index;
  }

  int64_t point_distance(int point_index, const KdTarget &target) const {
    int64_t result = 0;
    for (int lag = 1; lag <= LAST_LAG; ++lag) {
      const int64_t difference =
          static_cast<int64_t>(points_[point_index].delta[lag]) - target[lag];
      result += difference * difference;
    }
    return result;
  }

  int64_t box_lower_bound(int node_index, const KdTarget &target) const {
    int64_t result = 0;
    const DeltaKdNode &node = nodes_[node_index];
    for (int lag = 1; lag <= LAST_LAG; ++lag) {
      int64_t difference = 0;
      if (target[lag] < node.lower[lag])
        difference = static_cast<int64_t>(node.lower[lag]) - target[lag];
      else if (target[lag] > node.upper[lag])
        difference = static_cast<int64_t>(target[lag]) - node.upper[lag];
      result += difference * difference;
    }
    return result;
  }

  void search_node(int node_index, const KdTarget &target,
                   KdQueryResult &result) const {
    if (!result.complete) return;
    if ((result.stats.node_visits & 1023ULL) == 0 && use_deadline_ &&
        Clock::now() >= deadline_) {
      result.complete = false;
      return;
    }
    const DeltaKdNode &node = nodes_[node_index];
    ++result.stats.node_visits;
    ++result.stats.point_distances;
    const int64_t distance = point_distance(node.point_index, target);
    if (distance < result.distance ||
        (distance == result.distance &&
         (result.point_index < 0 || node.point_index < result.point_index))) {
      result.distance = distance;
      result.point_index = node.point_index;
    }

    std::array<std::pair<int64_t, int>, 2> children{};
    int child_count = 0;
    for (const int child : {node.left, node.right}) {
      if (child < 0) continue;
      ++result.stats.box_tests;
      children[child_count++] = {box_lower_bound(child, target), child};
    }
    if (child_count == 2 && children[1] < children[0])
      std::swap(children[0], children[1]);
    for (int index = 0; index < child_count; ++index) {
      if (!result.complete) return;
      const auto [bound, child] = children[index];
      // Equality is visited so deterministic smallest-index tie-breaking is
      // exact as well as the nearest squared distance.
      if (bound <= result.distance) {
        search_node(child, target, result);
      } else {
        ++result.stats.pruned_subtrees;
        result.stats.pruned_points += nodes_[child].subtree_size;
      }
    }
  }

  const std::vector<CheckerboardComponent> &points_;
  Clock::time_point deadline_;
  bool use_deadline_ = false;
  bool build_complete_ = true;
  std::vector<int> order_;
  std::vector<DeltaKdNode> nodes_;
  int root_ = -1;
};

// Reference implementation used only by bounded self-tests.  It has the
// same exact nearest-neighbor contract as the kd-tree but evaluates every
// stored point.
class ExactDeltaLinearIndex {
 public:
  explicit ExactDeltaLinearIndex(
      const std::vector<CheckerboardComponent> &points) : points_(points) {}

  size_t point_count() const { return points_.size(); }

  KdQueryResult nearest(const KdTarget &target) const {
    KdQueryResult result;
    result.complete = true;
    for (size_t point_index = 0; point_index < points_.size(); ++point_index) {
      int64_t distance = 0;
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        const int64_t difference =
            static_cast<int64_t>(points_[point_index].delta[lag]) -
            target[lag];
        distance += difference * difference;
      }
      ++result.stats.node_visits;
      ++result.stats.point_distances;
      if (distance < result.distance ||
          (distance == result.distance &&
           (result.point_index < 0 ||
            static_cast<int>(point_index) < result.point_index))) {
        result.distance = distance;
        result.point_index = static_cast<int>(point_index);
      }
    }
    return result;
  }

 private:
  const std::vector<CheckerboardComponent> &points_;
};

struct CrossPairImprovement {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  uint64_t evaluations = 0;
  size_t a_components = 0;
  size_t b_components = 0;
  bool found = false;
  bool complete = false;
};

struct SameSequencePairImprovement {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  std::array<size_t, 2> components{};
  std::array<uint64_t, 2> evaluations_by_sequence{};
  std::array<uint64_t, 2> overlap_skips_by_sequence{};
  uint64_t evaluations = 0;
  uint64_t overlap_skips = 0;
  bool found = false;
  bool complete = false;
};

struct SixCycleImprovement {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  std::array<uint64_t, 2> raw_patterns{};
  std::array<uint64_t, 2> valid_cycles{};
  std::array<uint64_t, 2> evaluations{};
  bool found = false;
  bool complete = false;
};

struct EightCycleImprovement {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  std::array<uint64_t, 2> row_cycles{};
  std::array<uint64_t, 2> sign_orientations{};
  std::array<uint64_t, 2> raw_assignments{};
  std::array<uint64_t, 2> repeated_column_skips{};
  std::array<uint64_t, 2> legal_cycles{};
  std::array<uint64_t, 2> evaluations{};
  bool found = false;
  bool complete = false;
};

struct MixedSixCycleImprovement {
  Move move{};
  Delta delta{};
  int64_t energy = std::numeric_limits<int64_t>::max();
  std::array<uint64_t, 2> raw_patterns{};
  std::array<uint64_t, 2> legal_cycles{};
  std::array<uint64_t, 2> queries{};
  std::array<size_t, 2> checker_components{};
  uint64_t possible_pair_distances = 0;
  KdSearchStats kd_stats{};
  uint64_t tree_nodes = 0;
  bool found = false;
  bool complete = false;
};

constexpr std::array<std::array<int, 3>, 6> PERMUTATIONS_3{{
    {{0, 1, 2}}, {{0, 2, 1}}, {{1, 0, 2}},
    {{1, 2, 0}}, {{2, 0, 1}}, {{2, 1, 0}},
}};

// With the least row fixed first, these are the three undirected Hamiltonian
// cycles on four ordered row vertices.  Reversal would duplicate a support.
constexpr std::array<std::array<int, 4>, 3> ROW_CYCLES_4{{
    {{0, 1, 2, 3}}, {{0, 1, 3, 2}}, {{0, 2, 1, 3}},
}};

constexpr uint64_t choose_three(int value) {
  return static_cast<uint64_t>(value) * (value - 1) * (value - 2) / 6;
}

constexpr uint64_t choose_four(int value) {
  return static_cast<uint64_t>(value) * (value - 1) * (value - 2) *
         (value - 3) / 24;
}

constexpr uint64_t SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE =
    choose_three(ROWS) * choose_three(COLS) * PERMUTATIONS_3.size();

constexpr uint64_t EIGHT_CYCLE_ROW_CYCLES_PER_SEQUENCE =
    choose_four(ROWS) * ROW_CYCLES_4.size();

constexpr size_t MAX_LEGAL_CHECKERBOARDS =
    (ROWS * (ROWS - 1) / 2) * (COLS * (COLS - 1) / 2);

std::vector<CheckerboardComponent> collect_checkerboard_components(
    const State &state, int which, Clock::time_point deadline,
    bool use_deadline, bool &complete) {
  std::vector<CheckerboardComponent> result;
  result.reserve(MAX_LEGAL_CHECKERBOARDS);
  complete = false;
  for (int row1 = 0; row1 < ROWS; ++row1) {
    for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
      if (use_deadline && Clock::now() >= deadline) return result;
      for (int column1 = 0; column1 < COLS; ++column1) {
        for (int column2 = column1 + 1; column2 < COLS; ++column2) {
          if (!checkerboard(state.sequence[which], row1, row2,
                            column1, column2))
            continue;
          const Move move = make_checkerboard_move(
              which, row1, row2, column1, column2);
          CheckerboardComponent component;
          for (int entry = 0; entry < BASIC_MOVE_SIZE; ++entry)
            component.position[entry] = move.position[entry];
          component.delta = correlation_delta(state, move);
          component.linear_energy_change = energy_after(state, component.delta) -
                                           state.energy;
          result.push_back(component);
          if (result.size() > MAX_LEGAL_CHECKERBOARDS)
            throw std::runtime_error("checkerboard component bound exceeded");
        }
      }
    }
  }
  complete = true;
  return result;
}

CrossPairImprovement best_cross_pair_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline) {
  CrossPairImprovement best;
  bool a_complete = false, b_complete = false;
  auto a_components = collect_checkerboard_components(
      state, 0, deadline, use_deadline, a_complete);
  if (!a_complete) return best;
  auto b_components = collect_checkerboard_components(
      state, 1, deadline, use_deadline, b_complete);
  if (!b_complete) return best;
  best.a_components = a_components.size();
  best.b_components = b_components.size();
  int64_t best_change = 0;
  uint64_t until_clock_check = 0;
  for (const auto &left : a_components) {
    for (const auto &right : b_components) {
      int64_t change = left.linear_energy_change + right.linear_energy_change;
      for (int lag = 1; lag <= LAST_LAG; ++lag)
        change += 2LL * left.delta[lag] * right.delta[lag];
      ++best.evaluations;
      if (change < best_change) {
        best_change = change;
        best.move.size = 2 * BASIC_MOVE_SIZE;
        for (int entry = 0; entry < BASIC_MOVE_SIZE; ++entry) {
          best.move.position[entry] = left.position[entry];
          best.move.position[BASIC_MOVE_SIZE + entry] = right.position[entry];
        }
        for (int lag = 1; lag <= LAST_LAG; ++lag)
          best.delta[lag] = left.delta[lag] + right.delta[lag];
        best.energy = state.energy + change;
        best.found = true;
      }
      if (++until_clock_check == 4096) {
        until_clock_check = 0;
        if (use_deadline && Clock::now() >= deadline) {
          // A partial Cartesian-product scan is never used as an exhaustive
          // polish result.
          best.found = false;
          return best;
        }
      }
    }
  }
  if (best.evaluations !=
      static_cast<uint64_t>(best.a_components) * best.b_components)
    throw std::runtime_error("cross-pair evaluation count mismatch");
  best.complete = true;
  return best;
}

bool disjoint_components(const CheckerboardComponent &left,
                         const CheckerboardComponent &right) {
  for (const int left_position : left.position)
    for (const int right_position : right.position)
      if (left_position == right_position) return false;
  return true;
}

Delta same_sequence_union_delta(const State &state,
                                const CheckerboardComponent &left,
                                const CheckerboardComponent &right) {
  if (!disjoint_components(left, right))
    throw std::runtime_error("same-sequence union components overlap");
  const int which = left.position[0] / N;
  for (const int position : left.position)
    if (position / N != which)
      throw std::runtime_error("left checkerboard component crosses sequences");
  for (const int position : right.position)
    if (position / N != which)
      throw std::runtime_error("paired checkerboards lie in different sequences");

  Delta result{};
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    result[lag] = left.delta[lag] + right.delta[lag];
  // Each component delta already contains its six internal quadratic pair
  // corrections.  Add the sixteen corrections between the two disjoint
  // four-flip components to obtain the exact eight-flip union delta.
  for (const int left_global : left.position) {
    const int left_position = left_global % N;
    for (const int right_global : right.position) {
      const int right_position = right_global % N;
      const int lag = DISTANCE[left_position][right_position];
      if (lag <= 0 || lag > LAST_LAG)
        throw std::runtime_error("same-sequence union repeats a position");
      result[lag] += static_cast<int16_t>(
          2 * state.sequence[which][left_position] *
          state.sequence[which][right_position]);
    }
  }
  return result;
}

SameSequencePairImprovement best_same_sequence_pair_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline) {
  SameSequencePairImprovement best;
  best.energy = state.energy;
  uint64_t until_clock_check = 0;
  for (int which = 0; which < 2; ++which) {
    bool components_complete = false;
    auto components = collect_checkerboard_components(
        state, which, deadline, use_deadline, components_complete);
    if (!components_complete) {
      best.found = false;
      return best;
    }
    best.components[which] = components.size();
    for (size_t left_index = 0; left_index < components.size(); ++left_index) {
      for (size_t right_index = left_index + 1;
           right_index < components.size(); ++right_index) {
        const auto &left = components[left_index];
        const auto &right = components[right_index];
        if (!disjoint_components(left, right)) {
          ++best.overlap_skips;
          ++best.overlap_skips_by_sequence[which];
        } else {
          const Delta delta = same_sequence_union_delta(state, left, right);
          const int64_t proposed = energy_after(state, delta);
          ++best.evaluations;
          ++best.evaluations_by_sequence[which];
          if (proposed < best.energy) {
            best.energy = proposed;
            best.delta = delta;
            best.move.size = 2 * BASIC_MOVE_SIZE;
            for (int entry = 0; entry < BASIC_MOVE_SIZE; ++entry) {
              best.move.position[entry] = left.position[entry];
              best.move.position[BASIC_MOVE_SIZE + entry] =
                  right.position[entry];
            }
            best.found = true;
          }
        }
        if (++until_clock_check == 4096) {
          until_clock_check = 0;
          if (use_deadline && Clock::now() >= deadline) {
            best.found = false;
            return best;
          }
        }
      }
    }
    const uint64_t unordered_pairs =
        static_cast<uint64_t>(components.size()) *
        (components.size() - (components.empty() ? 0 : 1)) / 2;
    if (best.evaluations_by_sequence[which] +
            best.overlap_skips_by_sequence[which] !=
        unordered_pairs)
      throw std::runtime_error("same-sequence pair count mismatch");
  }
  best.complete = true;
  return best;
}

Move make_six_cycle_move(int which, const std::array<int, 3> &rows,
                         const std::array<int, 3> &columns,
                         const std::array<int, 3> &omitted_matching) {
  Move move;
  for (int row_index = 0; row_index < 3; ++row_index) {
    for (int column_index = 0; column_index < 3; ++column_index) {
      if (column_index == omitted_matching[row_index]) continue;
      move.position[move.size++] =
          which * N + CRT[rows[row_index]][columns[column_index]];
    }
  }
  if (move.size != 6)
    throw std::runtime_error("K3,3 complement is not a six-cycle");
  return move;
}

bool alternating_six_cycle(const State &state, int which,
                           const std::array<int, 3> &rows,
                           const std::array<int, 3> &columns,
                           const std::array<int, 3> &omitted_matching) {
  // K3,3 minus one perfect matching is a six-cycle.  Alternation is
  // equivalent to the two retained signs summing to zero at every row and
  // every column vertex.
  for (int row_index = 0; row_index < 3; ++row_index) {
    int sum = 0;
    for (int column_index = 0; column_index < 3; ++column_index)
      if (column_index != omitted_matching[row_index])
        sum += state.sequence[which]
            [CRT[rows[row_index]][columns[column_index]]];
    if (sum != 0) return false;
  }
  for (int column_index = 0; column_index < 3; ++column_index) {
    int sum = 0;
    for (int row_index = 0; row_index < 3; ++row_index)
      if (column_index != omitted_matching[row_index])
        sum += state.sequence[which]
            [CRT[rows[row_index]][columns[column_index]]];
    if (sum != 0) return false;
  }
  return true;
}

SixCycleImprovement best_six_cycle_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline) {
  SixCycleImprovement best;
  best.energy = state.energy;
  uint64_t until_clock_check = 0;
  for (int which = 0; which < 2; ++which) {
    for (int row0 = 0; row0 < ROWS; ++row0) {
      for (int row1 = row0 + 1; row1 < ROWS; ++row1) {
        for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
          const std::array<int, 3> rows{{row0, row1, row2}};
          for (int column0 = 0; column0 < COLS; ++column0) {
            for (int column1 = column0 + 1; column1 < COLS; ++column1) {
              for (int column2 = column1 + 1; column2 < COLS; ++column2) {
                const std::array<int, 3> columns{{
                    column0, column1, column2}};
                for (const auto &omitted_matching : PERMUTATIONS_3) {
                  ++best.raw_patterns[which];
                  if (alternating_six_cycle(
                          state, which, rows, columns, omitted_matching)) {
                    ++best.valid_cycles[which];
                    const Move move = make_six_cycle_move(
                        which, rows, columns, omitted_matching);
                    const Delta delta = correlation_delta(state, move);
                    const int64_t proposed = energy_after(state, delta);
                    ++best.evaluations[which];
                    if (proposed < best.energy) {
                      best.move = move;
                      best.delta = delta;
                      best.energy = proposed;
                      best.found = true;
                    }
                  }
                  if (++until_clock_check == 4096) {
                    until_clock_check = 0;
                    if (use_deadline && Clock::now() >= deadline) {
                      best.found = false;
                      return best;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    if (best.raw_patterns[which] != SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE ||
        best.valid_cycles[which] != best.evaluations[which])
      throw std::runtime_error("six-cycle enumeration count mismatch");
  }
  best.complete = true;
  return best;
}

Move make_eight_cycle_move(int which, const std::array<int, 4> &rows,
                           const std::array<int, 4> &columns) {
  // This connected C8 is a genuine switch-graph radius-three support: every
  // row and column vertex has one plus and one minus edge, while no union of
  // at most two checkerboard supports can be a connected simple eight-cycle.
  Move move;
  for (int edge = 0; edge < 4; ++edge) {
    const int next = (edge + 1) % 4;
    move.position[move.size++] =
        which * N + CRT[rows[edge]][columns[edge]];
    move.position[move.size++] =
        which * N + CRT[rows[next]][columns[edge]];
  }
  if (move.size != 8)
    throw std::runtime_error("4 by 4 support is not an eight-cycle");
  return move;
}

bool scan_eight_cycles_one_sequence(
    const State &state, int which, Clock::time_point deadline,
    bool use_deadline, uint64_t raw_limit,
    EightCycleImprovement &best) {
  uint64_t until_clock_check = 0;
  for (int row0 = 0; row0 < ROWS; ++row0) {
    for (int row1 = row0 + 1; row1 < ROWS; ++row1) {
      for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
        for (int row3 = row2 + 1; row3 < ROWS; ++row3) {
          const std::array<int, 4> row_set{{row0, row1, row2, row3}};
          for (const auto &row_cycle : ROW_CYCLES_4) {
            ++best.row_cycles[which];
            std::array<int, 4> rows{};
            for (int index = 0; index < 4; ++index)
              rows[index] = row_set[row_cycle[index]];
            for (const int sign : {-1, 1}) {
              ++best.sign_orientations[which];
              if (use_deadline && Clock::now() >= deadline) {
                best.found = false;
                return false;
              }
              std::array<std::array<int, COLS>, 4> columns_by_edge{};
              std::array<int, 4> column_counts{};
              for (int edge = 0; edge < 4; ++edge) {
                const int next = (edge + 1) % 4;
                for (int column = 0; column < COLS; ++column) {
                  if (state.sequence[which][CRT[rows[edge]][column]] == sign &&
                      state.sequence[which][CRT[rows[next]][column]] == -sign)
                    columns_by_edge[edge][column_counts[edge]++] = column;
                }
              }

              for (int index0 = 0; index0 < column_counts[0]; ++index0) {
                const int column0 = columns_by_edge[0][index0];
                for (int index1 = 0; index1 < column_counts[1]; ++index1) {
                  const int column1 = columns_by_edge[1][index1];
                  for (int index2 = 0; index2 < column_counts[2]; ++index2) {
                    const int column2 = columns_by_edge[2][index2];
                    for (int index3 = 0; index3 < column_counts[3]; ++index3) {
                      if (raw_limit != 0 &&
                          best.raw_assignments[which] >= raw_limit)
                        return true;
                      const int column3 = columns_by_edge[3][index3];
                      ++best.raw_assignments[which];
                      if (column0 == column1 || column0 == column2 ||
                          column0 == column3 || column1 == column2 ||
                          column1 == column3 || column2 == column3) {
                        ++best.repeated_column_skips[which];
                      } else {
                        ++best.legal_cycles[which];
                        ++best.evaluations[which];
                        const std::array<int, 4> columns{{
                            column0, column1, column2, column3}};
                        const Move move =
                            make_eight_cycle_move(which, rows, columns);
                        const Delta delta = correlation_delta(state, move);
                        const int64_t proposed = energy_after(state, delta);
                        if (proposed < best.energy) {
                          best.move = move;
                          best.delta = delta;
                          best.energy = proposed;
                          best.found = true;
                        }
                      }
                      if (++until_clock_check == 4096) {
                        until_clock_check = 0;
                        if (use_deadline && Clock::now() >= deadline) {
                          best.found = false;
                          return false;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return true;
}

EightCycleImprovement best_eight_cycle_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline,
    uint64_t raw_limit_per_sequence = 0) {
  EightCycleImprovement best;
  best.energy = state.energy;
  for (int which = 0; which < 2; ++which) {
    if (!scan_eight_cycles_one_sequence(
            state, which, deadline, use_deadline, raw_limit_per_sequence,
            best))
      return best;
    if (raw_limit_per_sequence != 0 &&
        best.raw_assignments[which] != raw_limit_per_sequence)
      throw std::runtime_error("eight-cycle bounded scan is too short");
    if (raw_limit_per_sequence == 0 &&
        (best.row_cycles[which] !=
             EIGHT_CYCLE_ROW_CYCLES_PER_SEQUENCE ||
         best.sign_orientations[which] !=
             2 * EIGHT_CYCLE_ROW_CYCLES_PER_SEQUENCE))
      throw std::runtime_error("eight-cycle row enumeration count mismatch");
    if (best.raw_assignments[which] !=
            best.repeated_column_skips[which] + best.legal_cycles[which] ||
        best.legal_cycles[which] != best.evaluations[which])
      throw std::runtime_error("eight-cycle assignment count mismatch");
  }
  best.complete = true;
  return best;
}

void add_kd_stats(KdSearchStats &target, const KdSearchStats &source) {
  target.node_visits += source.node_visits;
  target.point_distances += source.point_distances;
  target.box_tests += source.box_tests;
  target.pruned_subtrees += source.pruned_subtrees;
  target.pruned_points += source.pruned_points;
}

template <typename DeltaIndex>
bool scan_mixed_six_cycles_one_orientation(
    const State &state, int cycle_sequence,
    const std::vector<CheckerboardComponent> &opposite_components,
    const DeltaIndex &opposite_tree, Clock::time_point deadline,
    bool use_deadline, uint64_t raw_limit,
    MixedSixCycleImprovement &best) {
  uint64_t until_clock_check = 0;
  for (int row0 = 0; row0 < ROWS; ++row0) {
    for (int row1 = row0 + 1; row1 < ROWS; ++row1) {
      for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
        const std::array<int, 3> rows{{row0, row1, row2}};
        for (int column0 = 0; column0 < COLS; ++column0) {
          for (int column1 = column0 + 1; column1 < COLS; ++column1) {
            for (int column2 = column1 + 1; column2 < COLS; ++column2) {
              const std::array<int, 3> columns{{
                  column0, column1, column2}};
              for (const auto &omitted_matching : PERMUTATIONS_3) {
                ++best.raw_patterns[cycle_sequence];
                if (alternating_six_cycle(
                        state, cycle_sequence, rows, columns,
                        omitted_matching)) {
                  ++best.legal_cycles[cycle_sequence];
                  ++best.queries[cycle_sequence];
                  const Move cycle_move = make_six_cycle_move(
                      cycle_sequence, rows, columns, omitted_matching);
                  const Delta cycle_delta =
                      correlation_delta(state, cycle_move);
                  KdTarget target{};
                  for (int lag = 1; lag <= LAST_LAG; ++lag)
                    target[lag] = -static_cast<int32_t>(
                        state.residual[lag] + cycle_delta[lag]);
                  best.possible_pair_distances += opposite_tree.point_count();
                  const KdQueryResult query = opposite_tree.nearest(target);
                  add_kd_stats(best.kd_stats, query.stats);
                  if (!query.complete) {
                    best.found = false;
                    return false;
                  }
                  if (query.point_index >= 0 && query.distance < best.energy) {
                    const CheckerboardComponent &checker =
                        opposite_components[query.point_index];
                    best.move.size = 6 + BASIC_MOVE_SIZE;
                    for (int entry = 0; entry < 6; ++entry)
                      best.move.position[entry] = cycle_move.position[entry];
                    for (int entry = 0; entry < BASIC_MOVE_SIZE; ++entry)
                      best.move.position[6 + entry] = checker.position[entry];
                    for (int lag = 1; lag <= LAST_LAG; ++lag)
                      best.delta[lag] =
                          cycle_delta[lag] + checker.delta[lag];
                    best.energy = query.distance;
                    best.found = true;
                  }
                }
                if (raw_limit != 0 &&
                    best.raw_patterns[cycle_sequence] >= raw_limit)
                  return true;
                if (++until_clock_check == 4096) {
                  until_clock_check = 0;
                  if (use_deadline && Clock::now() >= deadline) {
                    best.found = false;
                    return false;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return true;
}

MixedSixCycleImprovement best_mixed_six_cycle_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline,
    uint64_t raw_limit_per_sequence = 0, size_t checker_limit = 0) {
  MixedSixCycleImprovement best;
  best.energy = state.energy;
  bool a_complete = false, b_complete = false;
  auto a_components = collect_checkerboard_components(
      state, 0, deadline, use_deadline, a_complete);
  best.checker_components[0] = a_components.size();
  if (!a_complete) return best;
  auto b_components = collect_checkerboard_components(
      state, 1, deadline, use_deadline, b_complete);
  best.checker_components[1] = b_components.size();
  if (!b_complete) return best;
  if (checker_limit != 0) {
    if (a_components.size() > checker_limit) a_components.resize(checker_limit);
    if (b_components.size() > checker_limit) b_components.resize(checker_limit);
  }
  best.checker_components = {{a_components.size(), b_components.size()}};

  const ExactDeltaKdTree a_tree(
      a_components, deadline, use_deadline);
  best.tree_nodes += a_tree.node_count();
  if (!a_tree.complete()) return best;
  const ExactDeltaKdTree b_tree(
      b_components, deadline, use_deadline);
  best.tree_nodes += b_tree.node_count();
  if (!b_tree.complete()) return best;

  if (!scan_mixed_six_cycles_one_orientation(
          state, 0, b_components, b_tree, deadline, use_deadline,
          raw_limit_per_sequence, best))
    return best;
  if (!scan_mixed_six_cycles_one_orientation(
          state, 1, a_components, a_tree, deadline, use_deadline,
          raw_limit_per_sequence, best))
    return best;

  const uint64_t expected_raw = raw_limit_per_sequence == 0
      ? SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE
      : std::min(raw_limit_per_sequence,
                 SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE);
  for (int which = 0; which < 2; ++which)
    if (best.raw_patterns[which] != expected_raw ||
        best.legal_cycles[which] != best.queries[which])
      throw std::runtime_error("mixed six-cycle enumeration count mismatch");
  const uint64_t expected_possible =
      best.queries[0] * b_components.size() +
      best.queries[1] * a_components.size();
  if (best.possible_pair_distances != expected_possible ||
      best.kd_stats.point_distances + best.kd_stats.pruned_points !=
          expected_possible ||
      best.kd_stats.node_visits != best.kd_stats.point_distances)
    throw std::runtime_error("mixed six-cycle kd-tree coverage mismatch");
  best.complete = true;
  return best;
}

ImprovingMove best_checkerboard_improvement(
    const State &state, Clock::time_point deadline, bool use_deadline,
    uint64_t &evaluations) {
  ImprovingMove best;
  best.energy = state.energy;
  uint64_t since_clock_check = 0;
  for (int which = 0; which < 2; ++which) {
    for (int row1 = 0; row1 < ROWS; ++row1) {
      for (int row2 = row1 + 1; row2 < ROWS; ++row2) {
        for (int column1 = 0; column1 < COLS; ++column1) {
          for (int column2 = column1 + 1; column2 < COLS; ++column2) {
            if (!checkerboard(state.sequence[which], row1, row2,
                              column1, column2))
              continue;
            const Move move = make_checkerboard_move(
                which, row1, row2, column1, column2);
            const Delta delta = correlation_delta(state, move);
            const int64_t proposed = energy_after(state, delta);
            ++evaluations;
            if (proposed < best.energy) {
              best.move = move;
              best.delta = delta;
              best.energy = proposed;
              best.found = true;
            }
            if (++since_clock_check == 1024) {
              since_clock_check = 0;
              if (use_deadline && Clock::now() >= deadline) return best;
            }
          }
        }
      }
    }
  }
  return best;
}

void polish_state(State &state, SearchResult &result, const Options &options,
                  Clock::time_point deadline, bool use_deadline) {
  const bool any_extended_polish = options.cross_pair_polish ||
                                   options.same_sequence_pair_polish ||
                                   options.six_cycle_polish ||
                                   options.eight_cycle_polish ||
                                   options.mixed_six_cycle_polish;
  if (!any_extended_polish) {
    for (int step = 0; step < options.polish_steps; ++step) {
      if (use_deadline && Clock::now() >= deadline) break;
      ImprovingMove improvement = best_checkerboard_improvement(
          state, deadline, use_deadline, result.neighborhood_evaluations);
      if (!improvement.found) break;
      apply_move(state, improvement.move, improvement.delta);
      ++result.accepted;
      ++result.polish_moves;
      consider_best(state, result, options);
      if (result.best.metrics.energy == 0) break;
    }
    return;
  }

  int cross_rounds = 0;
  int same_sequence_rounds = 0;
  int six_cycle_rounds = 0;
  int eight_cycle_rounds = 0;
  int mixed_six_cycle_rounds = 0;
  for (;;) {
    bool single_local = options.polish_steps == 0;
    for (int step = 0; step < options.polish_steps; ++step) {
      if (use_deadline && Clock::now() >= deadline) return;
      ImprovingMove improvement = best_checkerboard_improvement(
          state, deadline, use_deadline, result.neighborhood_evaluations);
      if (!improvement.found) {
        single_local = true;
        break;
      }
      apply_move(state, improvement.move, improvement.delta);
      ++result.accepted;
      ++result.polish_moves;
      consider_best(state, result, options);
      if (result.best.metrics.energy == 0) return;
    }
    // In extended-polish modes, ordinary descent continues in bounded batches
    // until a complete scan proves the current state single-switch local.
    if (!single_local) continue;
    if (use_deadline && Clock::now() >= deadline) return;

    const bool scan_cross = options.cross_pair_polish &&
                            cross_rounds < options.cross_pair_max_rounds;
    const bool scan_same = options.same_sequence_pair_polish &&
                           same_sequence_rounds <
                               options.same_sequence_pair_max_rounds;
    const bool scan_six = options.six_cycle_polish &&
                          six_cycle_rounds < options.six_cycle_max_rounds;
    const bool scan_eight = options.eight_cycle_polish &&
        eight_cycle_rounds < options.eight_cycle_max_rounds;
    const bool scan_mixed_six = options.mixed_six_cycle_polish &&
        mixed_six_cycle_rounds < options.mixed_six_cycle_max_rounds;
    if (!scan_cross && !scan_same && !scan_six && !scan_eight &&
        !scan_mixed_six)
      return;

    CrossPairImprovement cross_pair;
    if (scan_cross) {
      cross_pair = best_cross_pair_improvement(state, deadline, use_deadline);
      ++result.cross_pair_scans;
      result.cross_pair_evaluations += cross_pair.evaluations;
      result.last_cross_pair_evaluations = cross_pair.evaluations;
      result.last_cross_pair_a_components = cross_pair.a_components;
      result.last_cross_pair_b_components = cross_pair.b_components;
      if (!cross_pair.complete) {
        ++result.incomplete_cross_pair_scans;
        return;
      }
      ++result.complete_cross_pair_scans;
    }

    SameSequencePairImprovement same_pair;
    if (scan_same) {
      same_pair = best_same_sequence_pair_improvement(
          state, deadline, use_deadline);
      ++result.same_sequence_pair_scans;
      result.same_sequence_pair_evaluations += same_pair.evaluations;
      result.same_sequence_pair_overlap_skips += same_pair.overlap_skips;
      result.last_same_sequence_pair_evaluations = same_pair.evaluations;
      result.last_same_sequence_pair_overlap_skips = same_pair.overlap_skips;
      result.last_same_sequence_pair_components = same_pair.components;
      result.last_same_sequence_pair_evaluations_by_sequence =
          same_pair.evaluations_by_sequence;
      result.last_same_sequence_pair_overlap_skips_by_sequence =
          same_pair.overlap_skips_by_sequence;
      if (!same_pair.complete) {
        ++result.incomplete_same_sequence_pair_scans;
        return;
      }
      ++result.complete_same_sequence_pair_scans;
    }

    SixCycleImprovement six_cycle;
    if (scan_six) {
      six_cycle = best_six_cycle_improvement(state, deadline, use_deadline);
      ++result.six_cycle_scans;
      for (int which = 0; which < 2; ++which) {
        result.six_cycle_raw_patterns += six_cycle.raw_patterns[which];
        result.six_cycle_valid_cycles += six_cycle.valid_cycles[which];
        result.six_cycle_evaluations += six_cycle.evaluations[which];
      }
      result.last_six_cycle_raw_patterns = six_cycle.raw_patterns;
      result.last_six_cycle_valid_cycles = six_cycle.valid_cycles;
      result.last_six_cycle_evaluations = six_cycle.evaluations;
      if (!six_cycle.complete) {
        ++result.incomplete_six_cycle_scans;
        return;
      }
      ++result.complete_six_cycle_scans;
    }

    EightCycleImprovement eight_cycle;
    if (scan_eight) {
      eight_cycle = best_eight_cycle_improvement(
          state, deadline, use_deadline);
      ++result.eight_cycle_scans;
      for (int which = 0; which < 2; ++which) {
        result.eight_cycle_row_cycles += eight_cycle.row_cycles[which];
        result.eight_cycle_sign_orientations +=
            eight_cycle.sign_orientations[which];
        result.eight_cycle_raw_assignments +=
            eight_cycle.raw_assignments[which];
        result.eight_cycle_repeated_column_skips +=
            eight_cycle.repeated_column_skips[which];
        result.eight_cycle_legal_cycles += eight_cycle.legal_cycles[which];
        result.eight_cycle_evaluations += eight_cycle.evaluations[which];
      }
      result.last_eight_cycle_row_cycles = eight_cycle.row_cycles;
      result.last_eight_cycle_sign_orientations =
          eight_cycle.sign_orientations;
      result.last_eight_cycle_raw_assignments =
          eight_cycle.raw_assignments;
      result.last_eight_cycle_repeated_column_skips =
          eight_cycle.repeated_column_skips;
      result.last_eight_cycle_legal_cycles = eight_cycle.legal_cycles;
      result.last_eight_cycle_evaluations = eight_cycle.evaluations;
      if (!eight_cycle.complete) {
        ++result.incomplete_eight_cycle_scans;
        return;
      }
      ++result.complete_eight_cycle_scans;
    }

    MixedSixCycleImprovement mixed_six_cycle;
    if (scan_mixed_six) {
      mixed_six_cycle = best_mixed_six_cycle_improvement(
          state, deadline, use_deadline);
      ++result.mixed_six_cycle_scans;
      for (int which = 0; which < 2; ++which) {
        result.mixed_six_cycle_raw_patterns +=
            mixed_six_cycle.raw_patterns[which];
        result.mixed_six_cycle_legal_cycles +=
            mixed_six_cycle.legal_cycles[which];
        result.mixed_six_cycle_queries += mixed_six_cycle.queries[which];
      }
      result.mixed_six_cycle_possible_pair_distances +=
          mixed_six_cycle.possible_pair_distances;
      result.mixed_six_cycle_pair_distances +=
          mixed_six_cycle.kd_stats.point_distances;
      result.mixed_six_cycle_tree_nodes += mixed_six_cycle.tree_nodes;
      result.mixed_six_cycle_tree_node_visits +=
          mixed_six_cycle.kd_stats.node_visits;
      result.mixed_six_cycle_box_tests +=
          mixed_six_cycle.kd_stats.box_tests;
      result.mixed_six_cycle_pruned_subtrees +=
          mixed_six_cycle.kd_stats.pruned_subtrees;
      result.mixed_six_cycle_pruned_points +=
          mixed_six_cycle.kd_stats.pruned_points;
      result.last_mixed_six_cycle_raw_patterns =
          mixed_six_cycle.raw_patterns;
      result.last_mixed_six_cycle_legal_cycles =
          mixed_six_cycle.legal_cycles;
      result.last_mixed_six_cycle_queries = mixed_six_cycle.queries;
      result.last_mixed_six_cycle_checker_components =
          mixed_six_cycle.checker_components;
      if (!mixed_six_cycle.complete) {
        ++result.incomplete_mixed_six_cycle_scans;
        return;
      }
      ++result.complete_mixed_six_cycle_scans;
    }

    enum class PolishChoice {
      none,
      cross,
      same_sequence,
      six_cycle,
      eight_cycle,
      mixed_six_cycle
    };
    PolishChoice choice = PolishChoice::none;
    int64_t energy = state.energy;
    const Move *move = nullptr;
    const Delta *delta = nullptr;
    if (cross_pair.found && cross_pair.energy < energy) {
      choice = PolishChoice::cross;
      energy = cross_pair.energy;
      move = &cross_pair.move;
      delta = &cross_pair.delta;
    }
    if (same_pair.found && same_pair.energy < energy) {
      choice = PolishChoice::same_sequence;
      energy = same_pair.energy;
      move = &same_pair.move;
      delta = &same_pair.delta;
    }
    if (six_cycle.found && six_cycle.energy < energy) {
      choice = PolishChoice::six_cycle;
      energy = six_cycle.energy;
      move = &six_cycle.move;
      delta = &six_cycle.delta;
    }
    if (eight_cycle.found && eight_cycle.energy < energy) {
      choice = PolishChoice::eight_cycle;
      energy = eight_cycle.energy;
      move = &eight_cycle.move;
      delta = &eight_cycle.delta;
    }
    if (mixed_six_cycle.found && mixed_six_cycle.energy < energy) {
      choice = PolishChoice::mixed_six_cycle;
      energy = mixed_six_cycle.energy;
      move = &mixed_six_cycle.move;
      delta = &mixed_six_cycle.delta;
    }
    if (choice == PolishChoice::none) return;
    if (energy >= state.energy || energy_after(state, *delta) != energy ||
        correlation_delta(state, *move) != *delta)
      throw std::runtime_error("extended-polish scoring inconsistency");
    apply_move(state, *move, *delta);
    ++result.accepted;
    ++result.polish_moves;
    if (choice == PolishChoice::cross) {
      ++result.cross_pair_polish_moves;
      ++cross_rounds;
    } else if (choice == PolishChoice::same_sequence) {
      ++result.same_sequence_pair_polish_moves;
      ++same_sequence_rounds;
    } else if (choice == PolishChoice::six_cycle) {
      ++result.six_cycle_polish_moves;
      ++six_cycle_rounds;
    } else if (choice == PolishChoice::eight_cycle) {
      ++result.eight_cycle_polish_moves;
      ++eight_cycle_rounds;
    } else {
      ++result.mixed_six_cycle_polish_moves;
      ++mixed_six_cycle_rounds;
    }
    consider_best(state, result, options);
    if (result.best.metrics.energy == 0) return;
  }
}

template <typename Rng>
void perturb_from_candidate(State &state, const Candidate &candidate,
                            Rng &rng, int switches) {
  state.profile = candidate.profile;
  state.sequence = candidate.sequence;
  for (int step = 0; step < switches; ++step) {
    const int first = static_cast<int>(rng() & 1ULL);
    Move move;
    int which = first;
    if (!random_checkerboard_move(state.sequence[which], which, rng, move)) {
      which = 1 - which;
      if (!random_checkerboard_move(state.sequence[which], which, rng, move))
        throw std::runtime_error("cannot perturb isolated margin fiber");
    }
    flip_direct(state.sequence[which], move, which);
  }
  recompute(state);
}

SearchResult search(const Options &options, const State *initial_state) {
  SearchResult result;
  std::mt19937_64 rng(splitmix64(options.seed));
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  State state = initial_state != nullptr
                    ? *initial_state
                    : random_state(options.profile, rng,
                                   options.initial_mix_switches);
  validate(state);
  consider_best(state, result, options);

  std::vector<int64_t> late_history(
      static_cast<size_t>(options.late_window), state.energy);
  uint64_t epoch_position = 0;
  const auto started = Clock::now();
  const auto deadline = started + std::chrono::duration_cast<Clock::duration>(
      std::chrono::duration<double>(options.seconds));
  const bool use_deadline = options.iterations == 0;

  auto within_budget = [&]() {
    if (result.best.initialized && result.best.metrics.energy == 0) return false;
    if (options.iterations) return result.proposals < options.iterations;
    return Clock::now() < deadline;
  };

  if (options.cross_pair_polish || options.same_sequence_pair_polish ||
      options.six_cycle_polish || options.eight_cycle_polish ||
      options.mixed_six_cycle_polish || options.polish_only) {
    polish_state(state, result, options, deadline, use_deadline);
    validate(state);
    std::fill(late_history.begin(), late_history.end(), state.energy);
  }

  while (!options.polish_only && within_budget()) {
    const bool compound = options.compound_probability > 0.0 &&
                          uniform(rng) < options.compound_probability;
    const Move move = compound ? coordinated_compound_move(state, rng)
                               : random_move(state, rng);
    if (compound) ++result.compound_proposals;
    const Delta delta = correlation_delta(state, move);
    const int64_t proposed = energy_after(state, delta);
    bool accept = false;
    if (options.mode == "late") {
      const size_t slot = static_cast<size_t>(
          result.proposals % late_history.size());
      accept = proposed <= state.energy || proposed <= late_history[slot];
      late_history[slot] = state.energy;
    } else {
      const double fraction = static_cast<double>(epoch_position) /
                              static_cast<double>(options.epoch);
      const double temperature = options.temperature_start * std::pow(
          options.temperature_end / options.temperature_start, fraction);
      const int64_t change = proposed - state.energy;
      accept = change <= 0 ||
               uniform(rng) < std::exp(-static_cast<double>(change) /
                                        temperature);
    }

    ++result.proposals;
    ++epoch_position;
    if (accept) {
      apply_move(state, move, delta);
      ++result.accepted;
      if (compound) ++result.compound_accepted;
      consider_best(state, result, options);
    }

    if (options.validate_every > 0 &&
        result.proposals % static_cast<uint64_t>(options.validate_every) == 0)
      validate(state);

    if (epoch_position < options.epoch ||
        (result.best.initialized && result.best.metrics.energy == 0))
      continue;

    polish_state(state, result, options, deadline, use_deadline);
    validate(state);
    if (!within_budget()) break;

    ++result.restarts;
    if (result.restarts % 3 == 0) {
      state = random_state(options.profile, rng, options.initial_mix_switches);
    } else {
      const int switches = 48 + static_cast<int>(rng() % 145);
      perturb_from_candidate(state, result.best, rng, switches);
    }
    epoch_position = 0;
    std::fill(late_history.begin(), late_history.end(), state.energy);
  }

  validate(state);
  // Store total counters even if the best state was found earlier.
  result.best.proposals = result.proposals;
  result.best.accepted = result.accepted;
  result.best.restarts = result.restarts;
  result.best.polish_moves = result.polish_moves;
  result.best.neighborhood_evaluations = result.neighborhood_evaluations;
  return result;
}

void write_sign_array(std::ostream &out, const Signs &sequence) {
  out << '[';
  for (int i = 0; i < N; ++i) {
    if (i) out << ',';
    out << static_cast<int>(sequence[i]);
  }
  out << ']';
}

template <size_t Size>
void write_int_array(std::ostream &out, const std::array<int, Size> &values) {
  out << '[';
  for (size_t i = 0; i < Size; ++i) {
    if (i) out << ',';
    out << values[i];
  }
  out << ']';
}

std::array<int, COLS> column_compression(const Signs &sequence) {
  std::array<int, COLS> result{};
  for (int column = 0; column < COLS; ++column)
    for (int row = 0; row < ROWS; ++row)
      result[column] += sequence[CRT[row][column]];
  return result;
}

std::array<int, ROWS> row_compression(const Signs &sequence) {
  std::array<int, ROWS> result{};
  for (int row = 0; row < ROWS; ++row)
    for (int column = 0; column < COLS; ++column)
      result[row] += sequence[CRT[row][column]];
  return result;
}

void write_checkpoint(const std::string &path, const SearchResult &result,
                      const Options &options, double elapsed) {
  const Candidate &candidate = result.best;
  if (candidate.profile != options.profile)
    throw std::runtime_error("checkpoint profile disagrees with search options");
  const bool exact = candidate.metrics.energy == 0;
  const std::filesystem::path output(path);
  if (output.has_parent_path())
    std::filesystem::create_directories(output.parent_path());
  std::filesystem::path temporary = output;
  temporary += ".tmp";
  std::ofstream out(temporary);
  if (!out)
    throw std::runtime_error("could not open checkpoint: " + temporary.string());

  out << "{\n";
  out << "  \"schema\": \""
      << (exact ? "hadamard668.legendre333-exact-search-candidate.v1"
                : "hadamard668.legendre333-row-column-local-checkpoint.v1")
      << "\",\n";
  out << "  \"kind\": \""
      << (exact ? "fixed-compression-legendre-profile-search-candidate"
                : "legendre333_row_column_local_checkpoint")
      << "\",\n";
  out << "  \"status\": \""
      << (exact ? "exact_candidate_pending_independent_verification"
                : "near_miss")
      << "\",\n";
  out << "  \"exact\": " << (exact ? "true" : "false") << ",\n";
  out << "  \"independent_verification_required\": true,\n";
  out << "  \"parameterization\": \"crt_row_column_margins\",\n";
  out << "  \"profile\": " << candidate.profile << ",\n";
  out << "  \"length\": 333,\n";
  out << "  \"hadamard_order\": 668,\n";
  out << "  \"base_seed\": " << options.seed << ",\n";
  out << "  \"seconds\": " << std::fixed << std::setprecision(6) << elapsed
      << ",\n";
  out << "  \"energy_half_paf\": " << candidate.metrics.energy << ",\n";
  out << "  \"energy_paf\": " << 4 * candidate.metrics.energy << ",\n";
  out << "  \"bad_lag_count\": " << candidate.metrics.nonzero << ",\n";
  out << "  \"max_abs_paf_residual\": "
      << 2 * candidate.metrics.max_abs << ",\n";
  out << "  \"l1_paf_residual\": " << 2 * candidate.metrics.l1 << ",\n";
  out << "  \"row_plus_counts_a\": ";
  write_int_array(out, ROW_PLUS_COUNTS[candidate.profile][0]);
  out << ",\n  \"row_plus_counts_b\": ";
  write_int_array(out, ROW_PLUS_COUNTS[candidate.profile][1]);
  out << ",\n  \"column_plus_counts_a\": ";
  write_int_array(out, COLUMN_PLUS_COUNTS[0]);
  out << ",\n  \"column_plus_counts_b\": ";
  write_int_array(out, COLUMN_PLUS_COUNTS[1]);
  out << ",\n  \"row_sums_a\": ";
  write_int_array(out, row_compression(candidate.sequence[0]));
  out << ",\n  \"row_sums_b\": ";
  write_int_array(out, row_compression(candidate.sequence[1]));
  out << ",\n  \"column_sums_a\": ";
  write_int_array(out, column_compression(candidate.sequence[0]));
  out << ",\n  \"column_sums_b\": ";
  write_int_array(out, column_compression(candidate.sequence[1]));
  out << ",\n  \"mod9_combined_paf_0_through_8\": [594,-74,-74,-74,-74,-74,-74,-74,-74]";
  out << ",\n  \"a\": ";
  write_sign_array(out, candidate.sequence[0]);
  out << ",\n  \"b\": ";
  write_sign_array(out, candidate.sequence[1]);
  out << ",\n  \"periodic_correlation_sums_1_through_166\": [";
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    if (lag > 1) out << ',';
    out << 2 * candidate.residual[lag] - 2;
  }
  out << "],\n  \"half_paf_residuals_1_through_166\": [";
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    if (lag > 1) out << ',';
    out << candidate.residual[lag];
  }
  out << "],\n";
  out << "  \"search\": {\"proposals\":" << result.proposals
      << ",\"accepted\":" << result.accepted
      << ",\"compound_proposals\":" << result.compound_proposals
      << ",\"compound_accepted\":" << result.compound_accepted
      << ",\"compound_probability\":" << options.compound_probability
      << ",\"restarts\":" << result.restarts
      << ",\"polish_moves\":" << result.polish_moves
      << ",\"cross_pair_polish\":"
      << (options.cross_pair_polish ? "true" : "false")
      << ",\"cross_pair_max_rounds\":" << options.cross_pair_max_rounds
      << ",\"cross_pair_polish_moves\":" << result.cross_pair_polish_moves
      << ",\"cross_pair_scans\":" << result.cross_pair_scans
      << ",\"complete_cross_pair_scans\":"
      << result.complete_cross_pair_scans
      << ",\"cross_pair_evaluations\":" << result.cross_pair_evaluations
      << ",\"incomplete_cross_pair_scans\":"
      << result.incomplete_cross_pair_scans
      << ",\"last_cross_pair_evaluations\":"
      << result.last_cross_pair_evaluations
      << ",\"last_cross_pair_a_components\":"
      << result.last_cross_pair_a_components
      << ",\"last_cross_pair_b_components\":"
      << result.last_cross_pair_b_components
      << ",\"same_sequence_pair_polish\":"
      << (options.same_sequence_pair_polish ? "true" : "false")
      << ",\"same_sequence_pair_max_rounds\":"
      << options.same_sequence_pair_max_rounds
      << ",\"same_sequence_pair_polish_moves\":"
      << result.same_sequence_pair_polish_moves
      << ",\"same_sequence_pair_scans\":"
      << result.same_sequence_pair_scans
      << ",\"complete_same_sequence_pair_scans\":"
      << result.complete_same_sequence_pair_scans
      << ",\"same_sequence_pair_evaluations\":"
      << result.same_sequence_pair_evaluations
      << ",\"same_sequence_pair_overlap_skips\":"
      << result.same_sequence_pair_overlap_skips
      << ",\"incomplete_same_sequence_pair_scans\":"
      << result.incomplete_same_sequence_pair_scans
      << ",\"last_same_sequence_pair_evaluations\":"
      << result.last_same_sequence_pair_evaluations
      << ",\"last_same_sequence_pair_overlap_skips\":"
      << result.last_same_sequence_pair_overlap_skips
      << ",\"last_same_sequence_pair_a_components\":"
      << result.last_same_sequence_pair_components[0]
      << ",\"last_same_sequence_pair_b_components\":"
      << result.last_same_sequence_pair_components[1]
      << ",\"last_same_sequence_pair_a_evaluations\":"
      << result.last_same_sequence_pair_evaluations_by_sequence[0]
      << ",\"last_same_sequence_pair_b_evaluations\":"
      << result.last_same_sequence_pair_evaluations_by_sequence[1]
      << ",\"last_same_sequence_pair_a_overlap_skips\":"
      << result.last_same_sequence_pair_overlap_skips_by_sequence[0]
      << ",\"last_same_sequence_pair_b_overlap_skips\":"
      << result.last_same_sequence_pair_overlap_skips_by_sequence[1]
      << ",\"six_cycle_polish\":"
      << (options.six_cycle_polish ? "true" : "false")
      << ",\"six_cycle_max_rounds\":" << options.six_cycle_max_rounds
      << ",\"six_cycle_polish_moves\":" << result.six_cycle_polish_moves
      << ",\"six_cycle_scans\":" << result.six_cycle_scans
      << ",\"complete_six_cycle_scans\":"
      << result.complete_six_cycle_scans
      << ",\"six_cycle_raw_patterns\":" << result.six_cycle_raw_patterns
      << ",\"six_cycle_valid_cycles\":" << result.six_cycle_valid_cycles
      << ",\"six_cycle_evaluations\":" << result.six_cycle_evaluations
      << ",\"incomplete_six_cycle_scans\":"
      << result.incomplete_six_cycle_scans
      << ",\"last_six_cycle_a_raw_patterns\":"
      << result.last_six_cycle_raw_patterns[0]
      << ",\"last_six_cycle_b_raw_patterns\":"
      << result.last_six_cycle_raw_patterns[1]
      << ",\"last_six_cycle_a_valid_cycles\":"
      << result.last_six_cycle_valid_cycles[0]
      << ",\"last_six_cycle_b_valid_cycles\":"
      << result.last_six_cycle_valid_cycles[1]
      << ",\"last_six_cycle_a_evaluations\":"
      << result.last_six_cycle_evaluations[0]
      << ",\"last_six_cycle_b_evaluations\":"
      << result.last_six_cycle_evaluations[1]
      << ",\"eight_cycle_polish\":"
      << (options.eight_cycle_polish ? "true" : "false")
      << ",\"eight_cycle_max_rounds\":"
      << options.eight_cycle_max_rounds
      << ",\"eight_cycle_polish_moves\":"
      << result.eight_cycle_polish_moves
      << ",\"eight_cycle_scans\":" << result.eight_cycle_scans
      << ",\"complete_eight_cycle_scans\":"
      << result.complete_eight_cycle_scans
      << ",\"incomplete_eight_cycle_scans\":"
      << result.incomplete_eight_cycle_scans
      << ",\"eight_cycle_row_cycles\":"
      << result.eight_cycle_row_cycles
      << ",\"eight_cycle_sign_orientations\":"
      << result.eight_cycle_sign_orientations
      << ",\"eight_cycle_raw_assignments\":"
      << result.eight_cycle_raw_assignments
      << ",\"eight_cycle_repeated_column_skips\":"
      << result.eight_cycle_repeated_column_skips
      << ",\"eight_cycle_legal_cycles\":"
      << result.eight_cycle_legal_cycles
      << ",\"eight_cycle_evaluations\":"
      << result.eight_cycle_evaluations
      << ",\"last_eight_cycle_a_row_cycles\":"
      << result.last_eight_cycle_row_cycles[0]
      << ",\"last_eight_cycle_b_row_cycles\":"
      << result.last_eight_cycle_row_cycles[1]
      << ",\"last_eight_cycle_a_sign_orientations\":"
      << result.last_eight_cycle_sign_orientations[0]
      << ",\"last_eight_cycle_b_sign_orientations\":"
      << result.last_eight_cycle_sign_orientations[1]
      << ",\"last_eight_cycle_a_raw_assignments\":"
      << result.last_eight_cycle_raw_assignments[0]
      << ",\"last_eight_cycle_b_raw_assignments\":"
      << result.last_eight_cycle_raw_assignments[1]
      << ",\"last_eight_cycle_a_repeated_column_skips\":"
      << result.last_eight_cycle_repeated_column_skips[0]
      << ",\"last_eight_cycle_b_repeated_column_skips\":"
      << result.last_eight_cycle_repeated_column_skips[1]
      << ",\"last_eight_cycle_a_legal_cycles\":"
      << result.last_eight_cycle_legal_cycles[0]
      << ",\"last_eight_cycle_b_legal_cycles\":"
      << result.last_eight_cycle_legal_cycles[1]
      << ",\"last_eight_cycle_a_evaluations\":"
      << result.last_eight_cycle_evaluations[0]
      << ",\"last_eight_cycle_b_evaluations\":"
      << result.last_eight_cycle_evaluations[1]
      << ",\"mixed_six_cycle_polish\":"
      << (options.mixed_six_cycle_polish ? "true" : "false")
      << ",\"mixed_six_cycle_max_rounds\":"
      << options.mixed_six_cycle_max_rounds
      << ",\"mixed_six_cycle_polish_moves\":"
      << result.mixed_six_cycle_polish_moves
      << ",\"mixed_six_cycle_scans\":"
      << result.mixed_six_cycle_scans
      << ",\"complete_mixed_six_cycle_scans\":"
      << result.complete_mixed_six_cycle_scans
      << ",\"incomplete_mixed_six_cycle_scans\":"
      << result.incomplete_mixed_six_cycle_scans
      << ",\"mixed_six_cycle_raw_patterns\":"
      << result.mixed_six_cycle_raw_patterns
      << ",\"mixed_six_cycle_legal_cycles\":"
      << result.mixed_six_cycle_legal_cycles
      << ",\"mixed_six_cycle_queries\":"
      << result.mixed_six_cycle_queries
      << ",\"mixed_six_cycle_possible_pair_distances\":"
      << result.mixed_six_cycle_possible_pair_distances
      << ",\"mixed_six_cycle_pair_distances\":"
      << result.mixed_six_cycle_pair_distances
      << ",\"mixed_six_cycle_tree_nodes\":"
      << result.mixed_six_cycle_tree_nodes
      << ",\"mixed_six_cycle_tree_node_visits\":"
      << result.mixed_six_cycle_tree_node_visits
      << ",\"mixed_six_cycle_box_tests\":"
      << result.mixed_six_cycle_box_tests
      << ",\"mixed_six_cycle_pruned_subtrees\":"
      << result.mixed_six_cycle_pruned_subtrees
      << ",\"mixed_six_cycle_pruned_points\":"
      << result.mixed_six_cycle_pruned_points
      << ",\"last_mixed_six_cycle_a_raw_patterns\":"
      << result.last_mixed_six_cycle_raw_patterns[0]
      << ",\"last_mixed_six_cycle_b_raw_patterns\":"
      << result.last_mixed_six_cycle_raw_patterns[1]
      << ",\"last_mixed_six_cycle_a_legal_cycles\":"
      << result.last_mixed_six_cycle_legal_cycles[0]
      << ",\"last_mixed_six_cycle_b_legal_cycles\":"
      << result.last_mixed_six_cycle_legal_cycles[1]
      << ",\"last_mixed_six_cycle_a_queries\":"
      << result.last_mixed_six_cycle_queries[0]
      << ",\"last_mixed_six_cycle_b_queries\":"
      << result.last_mixed_six_cycle_queries[1]
      << ",\"last_mixed_six_cycle_a_checker_components\":"
      << result.last_mixed_six_cycle_checker_components[0]
      << ",\"last_mixed_six_cycle_b_checker_components\":"
      << result.last_mixed_six_cycle_checker_components[1]
      << ",\"initial_checkpoint_used\":"
      << (!options.initial_checkpoint.empty() ? "true" : "false")
      << ",\"polish_only\":" << (options.polish_only ? "true" : "false")
      << ",\"neighborhood_evaluations\":"
      << result.neighborhood_evaluations
      << ",\"epoch\":" << options.epoch
      << ",\"polish_steps\":" << options.polish_steps
      << ",\"mode\":\"" << options.mode << "\"}\n";
  out << "}\n";
  out.close();
  if (!out)
    throw std::runtime_error("failed while writing checkpoint: " +
                             temporary.string());
  std::filesystem::rename(temporary, output);
}

std::string self_test_checkpoint_text(const State &state, int profile,
                                      int bad_sequence, int bad_index) {
  std::array<Signs, 2> sequences = state.sequence;
  if (bad_sequence >= 0) sequences[bad_sequence][bad_index] = 0;
  std::ostringstream out;
  out << "{\"profile\":" << profile
      << ",\"energy_half_paf\":0,\"a\":";
  write_sign_array(out, sequences[0]);
  out << ",\"b\":";
  write_sign_array(out, sequences[1]);
  out << '}';
  return out.str();
}

void expect_checkpoint_rejection(const std::string &text) {
  try {
    (void)state_from_checkpoint_text(text);
  } catch (const std::exception &) {
    return;
  }
  throw std::runtime_error("self-test malformed checkpoint was accepted");
}

void run_self_test() {
  std::mt19937_64 rng(0x668333ULL);
  for (int profile = 0; profile < PROFILE_COUNT; ++profile) {
    State state = random_state(profile, rng, 32);
    validate(state);
  }

  uint64_t delta_trials = 0;
  uint64_t compound_delta_trials = 0;
  State parser_fixture;
  for (const int profile : {0, PROFILE_COUNT - 1}) {
    for (int fixture = 0; fixture < 2; ++fixture) {
      State state = random_state(profile, rng, 128);
      validate(state);
      for (int trial = 0; trial < 64; ++trial) {
        const bool compound = trial % 2 != 0;
        const Move move = compound ? coordinated_compound_move(state, rng)
                                   : random_move(state, rng);
        if (compound) {
          if (move.size != 2 * BASIC_MOVE_SIZE)
            throw std::runtime_error("self-test compound size mismatch");
          int a_flips = 0, b_flips = 0;
          for (int entry = 0; entry < move.size; ++entry) {
            a_flips += move.position[entry] / N == 0;
            b_flips += move.position[entry] / N == 1;
          }
          if (a_flips != BASIC_MOVE_SIZE || b_flips != BASIC_MOVE_SIZE)
            throw std::runtime_error("self-test compound balance mismatch");
          ++compound_delta_trials;
        }
        const Delta delta = correlation_delta(state, move);
        const int64_t predicted_energy = energy_after(state, delta);

        State exact;
        exact.profile = state.profile;
        exact.sequence = state.sequence;
        flip_direct_all(exact.sequence, move);
        validate_margins(exact);
        recompute(exact);
        for (int lag = 1; lag <= LAST_LAG; ++lag) {
          if (exact.residual[lag] != state.residual[lag] + delta[lag])
            throw std::runtime_error("self-test delta/recompute mismatch");
        }
        if (exact.energy != predicted_energy)
          throw std::runtime_error("self-test energy delta mismatch");

        apply_move(state, move, delta);
        if (state.residual != exact.residual || state.energy != exact.energy ||
            state.single != exact.single)
          throw std::runtime_error("self-test incremental apply mismatch");
        if (trial % 16 == 15) validate(state);
        ++delta_trials;
      }
      validate(state);
      if (profile == PROFILE_COUNT - 1 && fixture == 1)
        parser_fixture = state;
    }
  }

  const std::string valid_checkpoint = self_test_checkpoint_text(
      parser_fixture, parser_fixture.profile, -1, 0);
  const State reparsed = state_from_checkpoint_text(valid_checkpoint);
  if (reparsed.profile != parser_fixture.profile ||
      reparsed.sequence != parser_fixture.sequence ||
      reparsed.residual != parser_fixture.residual ||
      reparsed.energy != parser_fixture.energy ||
      reparsed.single != parser_fixture.single)
    throw std::runtime_error("self-test checkpoint recomputation mismatch");
  std::string duplicate_profile = valid_checkpoint;
  duplicate_profile.insert(1, "\"profile\":11,");
  expect_checkpoint_rejection(duplicate_profile);
  expect_checkpoint_rejection("{\"profile\":0,\"a\":[],\"b\":[]}");
  expect_checkpoint_rejection("{\"profile\":false,\"a\":[],\"b\":[]}");
  expect_checkpoint_rejection(self_test_checkpoint_text(
      parser_fixture, PROFILE_COUNT, -1, 0));
  expect_checkpoint_rejection(self_test_checkpoint_text(
      parser_fixture, parser_fixture.profile, 0, 0));
  State wrong_margin = parser_fixture;
  wrong_margin.sequence[0][0] = -wrong_margin.sequence[0][0];
  expect_checkpoint_rejection(self_test_checkpoint_text(
      wrong_margin, wrong_margin.profile, -1, 0));

  State cross_state = random_state(0, rng, 64);
  const CrossPairImprovement cross = best_cross_pair_improvement(
      cross_state, Clock::time_point::max(), false);
  if (!cross.complete || cross.evaluations == 0 ||
      cross.evaluations !=
          static_cast<uint64_t>(cross.a_components) * cross.b_components ||
      !cross.found || cross.energy >= cross_state.energy)
    throw std::runtime_error("self-test exhaustive cross-pair scan failure");
  if (correlation_delta(cross_state, cross.move) != cross.delta ||
      energy_after(cross_state, cross.delta) != cross.energy)
    throw std::runtime_error("self-test cross-pair score mismatch");
  State cross_exact;
  cross_exact.profile = cross_state.profile;
  cross_exact.sequence = cross_state.sequence;
  flip_direct_all(cross_exact.sequence, cross.move);
  validate_margins(cross_exact);
  recompute(cross_exact);
  apply_move(cross_state, cross.move, cross.delta);
  if (cross_state.sequence != cross_exact.sequence ||
      cross_state.residual != cross_exact.residual ||
      cross_state.energy != cross_exact.energy ||
      cross_state.single != cross_exact.single)
    throw std::runtime_error("self-test cross-pair apply mismatch");
  validate(cross_state);

  State same_state = random_state(PROFILE_COUNT - 1, rng, 64);
  const SameSequencePairImprovement same =
      best_same_sequence_pair_improvement(
          same_state, Clock::time_point::max(), false);
  if (!same.complete || same.evaluations == 0 || !same.found ||
      same.energy >= same_state.energy)
    throw std::runtime_error(
        "self-test exhaustive same-sequence pair scan failure");
  for (int which = 0; which < 2; ++which) {
    const uint64_t unordered_pairs =
        static_cast<uint64_t>(same.components[which]) *
        (same.components[which] -
         (same.components[which] == 0 ? 0 : 1)) / 2;
    if (same.evaluations_by_sequence[which] +
            same.overlap_skips_by_sequence[which] !=
        unordered_pairs)
      throw std::runtime_error(
          "self-test same-sequence complete count mismatch");
  }
  if (correlation_delta(same_state, same.move) != same.delta ||
      energy_after(same_state, same.delta) != same.energy)
    throw std::runtime_error("self-test same-sequence pair score mismatch");
  State same_exact;
  same_exact.profile = same_state.profile;
  same_exact.sequence = same_state.sequence;
  flip_direct_all(same_exact.sequence, same.move);
  validate_margins(same_exact);
  recompute(same_exact);
  apply_move(same_state, same.move, same.delta);
  if (same_state.sequence != same_exact.sequence ||
      same_state.residual != same_exact.residual ||
      same_state.energy != same_exact.energy ||
      same_state.single != same_exact.single)
    throw std::runtime_error("self-test same-sequence pair apply mismatch");
  validate(same_state);
  const SameSequencePairImprovement interrupted_same =
      best_same_sequence_pair_improvement(
          same_state, Clock::now(), true);
  if (interrupted_same.complete || interrupted_same.found)
    throw std::runtime_error(
        "self-test partial same-sequence scan was treated as complete");

  if (SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE != 3'916'080)
    throw std::runtime_error("self-test six-cycle raw count constant mismatch");
  const std::array<int, 3> test_rows{{0, 1, 2}};
  const std::array<int, 3> test_columns{{0, 1, 2}};
  std::array<std::array<int, 6>, 6> cycle_supports{};
  for (size_t permutation = 0; permutation < PERMUTATIONS_3.size();
       ++permutation) {
    const Move move = make_six_cycle_move(
        0, test_rows, test_columns, PERMUTATIONS_3[permutation]);
    if (move.size != 6)
      throw std::runtime_error("self-test six-cycle has the wrong size");
    std::array<int, 3> row_degrees{}, column_degrees{};
    for (int entry = 0; entry < move.size; ++entry) {
      const int position = move.position[entry];
      cycle_supports[permutation][entry] = position;
      ++row_degrees[position % ROWS];
      ++column_degrees[position % COLS];
    }
    std::sort(cycle_supports[permutation].begin(),
              cycle_supports[permutation].end());
    if (row_degrees != std::array<int, 3>{{2, 2, 2}} ||
        column_degrees != std::array<int, 3>{{2, 2, 2}})
      throw std::runtime_error("self-test six-cycle degree mismatch");
    for (size_t earlier = 0; earlier < permutation; ++earlier)
      if (cycle_supports[earlier] == cycle_supports[permutation])
        throw std::runtime_error("self-test duplicate K3,3 six-cycle");

    int alternating_assignments = 0;
    for (int mask = 0; mask < (1 << 6); ++mask) {
      State alternating_fixture;
      alternating_fixture.sequence[0].fill(-1);
      for (int entry = 0; entry < move.size; ++entry)
        alternating_fixture.sequence[0][move.position[entry]] =
            (mask >> entry) & 1 ? 1 : -1;
      alternating_assignments += alternating_six_cycle(
          alternating_fixture, 0, test_rows, test_columns,
          PERMUTATIONS_3[permutation]);
    }
    if (alternating_assignments != 2)
      throw std::runtime_error(
          "self-test six-cycle does not have two alternating signings");
  }

  State cycle_state = random_state(0, rng, 64);
  const SixCycleImprovement cycle = best_six_cycle_improvement(
      cycle_state, Clock::time_point::max(), false);
  if (!cycle.complete || !cycle.found || cycle.move.size != 6 ||
      cycle.energy >= cycle_state.energy)
    throw std::runtime_error("self-test exhaustive six-cycle scan failure");
  for (int which = 0; which < 2; ++which) {
    if (cycle.raw_patterns[which] != SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE ||
        cycle.valid_cycles[which] == 0 ||
        cycle.valid_cycles[which] != cycle.evaluations[which])
      throw std::runtime_error("self-test six-cycle count mismatch");
  }
  if (correlation_delta(cycle_state, cycle.move) != cycle.delta ||
      energy_after(cycle_state, cycle.delta) != cycle.energy)
    throw std::runtime_error("self-test six-cycle score mismatch");
  State cycle_exact;
  cycle_exact.profile = cycle_state.profile;
  cycle_exact.sequence = cycle_state.sequence;
  flip_direct_all(cycle_exact.sequence, cycle.move);
  validate_margins(cycle_exact);
  recompute(cycle_exact);
  apply_move(cycle_state, cycle.move, cycle.delta);
  if (cycle_state.sequence != cycle_exact.sequence ||
      cycle_state.residual != cycle_exact.residual ||
      cycle_state.energy != cycle_exact.energy ||
      cycle_state.single != cycle_exact.single)
    throw std::runtime_error("self-test six-cycle apply mismatch");
  validate(cycle_state);
  const SixCycleImprovement interrupted_cycle =
      best_six_cycle_improvement(cycle_state, Clock::now(), true);
  if (interrupted_cycle.complete || interrupted_cycle.found)
    throw std::runtime_error(
        "self-test partial six-cycle scan was treated as complete");

  if (EIGHT_CYCLE_ROW_CYCLES_PER_SEQUENCE != 378)
    throw std::runtime_error("self-test eight-cycle row count mismatch");
  using LocalEightSupport = std::array<int, 8>;
  struct LocalEightDescriptor {
    LocalEightSupport support{};
    std::array<int, 4> rows{};
    std::array<int, 4> columns{};
  };
  std::vector<LocalEightDescriptor> canonical_eight_descriptors;
  std::array<int, 4> local_columns{{0, 1, 2, 3}};
  for (const auto &row_cycle : ROW_CYCLES_4) {
    local_columns = {{0, 1, 2, 3}};
    do {
      LocalEightDescriptor descriptor;
      descriptor.rows = row_cycle;
      descriptor.columns = local_columns;
      int entry = 0;
      for (int edge = 0; edge < 4; ++edge) {
        const int next = (edge + 1) % 4;
        descriptor.support[entry++] =
            4 * row_cycle[edge] + local_columns[edge];
        descriptor.support[entry++] =
            4 * row_cycle[next] + local_columns[edge];
      }
      std::sort(descriptor.support.begin(), descriptor.support.end());
      canonical_eight_descriptors.push_back(descriptor);
    } while (std::next_permutation(
        local_columns.begin(), local_columns.end()));
  }
  std::vector<LocalEightSupport> canonical_eight_supports;
  for (const auto &descriptor : canonical_eight_descriptors)
    canonical_eight_supports.push_back(descriptor.support);
  std::sort(canonical_eight_supports.begin(),
            canonical_eight_supports.end());
  if (canonical_eight_supports.size() != 72 ||
      std::adjacent_find(canonical_eight_supports.begin(),
                         canonical_eight_supports.end()) !=
          canonical_eight_supports.end())
    throw std::runtime_error(
        "self-test canonical eight-cycle support duplication");

  std::vector<LocalEightSupport> brute_eight_supports;
  std::array<int, 3> local_row_tail{{1, 2, 3}};
  do {
    const std::array<int, 4> rows{{
        0, local_row_tail[0], local_row_tail[1], local_row_tail[2]}};
    local_columns = {{0, 1, 2, 3}};
    do {
      LocalEightSupport support{};
      int entry = 0;
      for (int edge = 0; edge < 4; ++edge) {
        const int next = (edge + 1) % 4;
        support[entry++] = 4 * rows[edge] + local_columns[edge];
        support[entry++] = 4 * rows[next] + local_columns[edge];
      }
      std::sort(support.begin(), support.end());
      brute_eight_supports.push_back(support);
    } while (std::next_permutation(
        local_columns.begin(), local_columns.end()));
  } while (std::next_permutation(
      local_row_tail.begin(), local_row_tail.end()));
  std::sort(brute_eight_supports.begin(), brute_eight_supports.end());
  brute_eight_supports.erase(
      std::unique(brute_eight_supports.begin(), brute_eight_supports.end()),
      brute_eight_supports.end());
  if (brute_eight_supports.size() != 72 ||
      brute_eight_supports != canonical_eight_supports)
    throw std::runtime_error(
        "self-test canonical/brute eight-cycle supports disagree");

  for (int fixture = 0; fixture < 260; ++fixture) {
    const uint16_t bits = fixture == 0
        ? 0
        : fixture == 1 ? std::numeric_limits<uint16_t>::max()
                       : static_cast<uint16_t>(
                             0x9e37U * fixture + 0x5a3cU);
    std::array<int8_t, 16> local_signs{};
    for (int cell = 0; cell < 16; ++cell)
      local_signs[cell] = (bits >> cell) & 1U ? 1 : -1;
    for (const auto &descriptor : canonical_eight_descriptors) {
      std::array<int, 4> row_sums{}, column_sums{};
      for (const int cell : descriptor.support) {
        row_sums[cell / 4] += local_signs[cell];
        column_sums[cell % 4] += local_signs[cell];
      }
      const bool alternating =
          std::all_of(row_sums.begin(), row_sums.end(),
                      [](int value) { return value == 0; }) &&
          std::all_of(column_sums.begin(), column_sums.end(),
                      [](int value) { return value == 0; });
      int bucket_orientations = 0;
      for (const int sign : {-1, 1}) {
        bool accepted = true;
        for (int edge = 0; edge < 4; ++edge) {
          const int next = (edge + 1) % 4;
          accepted = accepted &&
              local_signs[4 * descriptor.rows[edge] +
                          descriptor.columns[edge]] == sign &&
              local_signs[4 * descriptor.rows[next] +
                          descriptor.columns[edge]] == -sign;
        }
        bucket_orientations += accepted;
      }
      if (bucket_orientations != (alternating ? 1 : 0))
        throw std::runtime_error(
            "self-test eight-cycle sign buckets are incomplete");
    }
  }

  constexpr uint64_t EIGHT_SELF_TEST_RAW_LIMIT = 32'768;
  State eight_state = random_state(4, rng, 64);
  const EightCycleImprovement eight = best_eight_cycle_improvement(
      eight_state, Clock::time_point::max(), false,
      EIGHT_SELF_TEST_RAW_LIMIT);
  if (!eight.complete || !eight.found || eight.move.size != 8 ||
      eight.energy >= eight_state.energy)
    throw std::runtime_error("self-test bounded eight-cycle scan failure");
  for (int which = 0; which < 2; ++which) {
    if (eight.raw_assignments[which] != EIGHT_SELF_TEST_RAW_LIMIT ||
        eight.raw_assignments[which] !=
            eight.repeated_column_skips[which] +
                eight.legal_cycles[which] ||
        eight.legal_cycles[which] == 0 ||
        eight.legal_cycles[which] != eight.evaluations[which] ||
        eight.row_cycles[which] == 0 ||
        eight.sign_orientations[which] == 0)
      throw std::runtime_error(
          "self-test bounded eight-cycle counts mismatch");
  }
  const int eight_sequence = eight.move.position[0] / N;
  std::array<int, ROWS> eight_row_degrees{}, eight_row_sign_sums{};
  std::array<int, COLS> eight_column_degrees{}, eight_column_sign_sums{};
  for (int entry = 0; entry < eight.move.size; ++entry) {
    const int global = eight.move.position[entry];
    if (global / N != eight_sequence)
      throw std::runtime_error("self-test eight-cycle crosses sequences");
    const int position = global % N;
    const int row = position % ROWS;
    const int column = position % COLS;
    ++eight_row_degrees[row];
    ++eight_column_degrees[column];
    eight_row_sign_sums[row] += eight_state.sequence[eight_sequence][position];
    eight_column_sign_sums[column] +=
        eight_state.sequence[eight_sequence][position];
  }
  int used_eight_rows = 0, used_eight_columns = 0;
  for (int row = 0; row < ROWS; ++row) {
    used_eight_rows += eight_row_degrees[row] != 0;
    if (eight_row_degrees[row] != 0 &&
        (eight_row_degrees[row] != 2 || eight_row_sign_sums[row] != 0))
      throw std::runtime_error("self-test eight-cycle row imbalance");
  }
  for (int column = 0; column < COLS; ++column) {
    used_eight_columns += eight_column_degrees[column] != 0;
    if (eight_column_degrees[column] != 0 &&
        (eight_column_degrees[column] != 2 ||
         eight_column_sign_sums[column] != 0))
      throw std::runtime_error("self-test eight-cycle column imbalance");
  }
  if (used_eight_rows != 4 || used_eight_columns != 4 ||
      correlation_delta(eight_state, eight.move) != eight.delta ||
      energy_after(eight_state, eight.delta) != eight.energy)
    throw std::runtime_error("self-test eight-cycle score mismatch");
  State eight_exact;
  eight_exact.profile = eight_state.profile;
  eight_exact.sequence = eight_state.sequence;
  flip_direct_all(eight_exact.sequence, eight.move);
  validate_margins(eight_exact);
  recompute(eight_exact);
  apply_move(eight_state, eight.move, eight.delta);
  if (eight_state.sequence != eight_exact.sequence ||
      eight_state.residual != eight_exact.residual ||
      eight_state.energy != eight_exact.energy ||
      eight_state.single != eight_exact.single)
    throw std::runtime_error("self-test eight-cycle apply/cache mismatch");
  validate(eight_state);
  const EightCycleImprovement interrupted_eight =
      best_eight_cycle_improvement(
          eight_state, Clock::now(), true, EIGHT_SELF_TEST_RAW_LIMIT);
  if (interrupted_eight.complete || interrupted_eight.found)
    throw std::runtime_error(
        "self-test partial eight-cycle scan was treated as complete");

  constexpr uint64_t MIXED_SELF_TEST_RAW_LIMIT = 16'384;
  constexpr size_t MIXED_SELF_TEST_CHECKER_LIMIT = 96;
  State mixed_state = random_state(PROFILE_COUNT - 1, rng, 64);
  const MixedSixCycleImprovement mixed =
      best_mixed_six_cycle_improvement(
          mixed_state, Clock::time_point::max(), false,
          MIXED_SELF_TEST_RAW_LIMIT, MIXED_SELF_TEST_CHECKER_LIMIT);
  if (!mixed.complete || !mixed.found || mixed.move.size != 10 ||
      mixed.energy >= mixed_state.energy ||
      mixed.checker_components !=
          std::array<size_t, 2>{{MIXED_SELF_TEST_CHECKER_LIMIT,
                                MIXED_SELF_TEST_CHECKER_LIMIT}} ||
      mixed.tree_nodes != 2 * MIXED_SELF_TEST_CHECKER_LIMIT)
    throw std::runtime_error("self-test bounded mixed scan failure");
  for (int which = 0; which < 2; ++which) {
    if (mixed.raw_patterns[which] != MIXED_SELF_TEST_RAW_LIMIT ||
        mixed.legal_cycles[which] == 0 ||
        mixed.legal_cycles[which] != mixed.queries[which])
      throw std::runtime_error("self-test mixed enumeration count mismatch");
  }
  if (mixed.kd_stats.point_distances + mixed.kd_stats.pruned_points !=
          mixed.possible_pair_distances ||
      mixed.kd_stats.node_visits != mixed.kd_stats.point_distances ||
      mixed.kd_stats.box_tests == 0 ||
      mixed.kd_stats.pruned_subtrees == 0 ||
      mixed.kd_stats.pruned_points == 0)
    throw std::runtime_error("self-test mixed kd accounting mismatch");

  bool mixed_a_complete = false, mixed_b_complete = false;
  auto all_mixed_a = collect_checkerboard_components(
      mixed_state, 0, Clock::time_point::max(), false, mixed_a_complete);
  auto all_mixed_b = collect_checkerboard_components(
      mixed_state, 1, Clock::time_point::max(), false, mixed_b_complete);
  if (!mixed_a_complete || !mixed_b_complete ||
      all_mixed_a.size() < MIXED_SELF_TEST_CHECKER_LIMIT ||
      all_mixed_b.size() < MIXED_SELF_TEST_CHECKER_LIMIT)
    throw std::runtime_error("self-test mixed checker collection failure");
  std::vector<CheckerboardComponent> mixed_a(
      all_mixed_a.begin(),
      all_mixed_a.begin() + MIXED_SELF_TEST_CHECKER_LIMIT);
  std::vector<CheckerboardComponent> mixed_b(
      all_mixed_b.begin(),
      all_mixed_b.begin() + MIXED_SELF_TEST_CHECKER_LIMIT);
  std::vector<CheckerboardComponent>().swap(all_mixed_a);
  std::vector<CheckerboardComponent>().swap(all_mixed_b);

  const ExactDeltaKdTree self_test_tree(
      mixed_a, Clock::time_point::max(), false);
  const ExactDeltaLinearIndex self_test_linear(mixed_a);
  if (!self_test_tree.complete() ||
      self_test_tree.node_count() != mixed_a.size())
    throw std::runtime_error("self-test kd-tree build failure");
  KdSearchStats direct_kd_stats;
  for (int target_index = 0; target_index < 32; ++target_index) {
    KdTarget target{};
    for (int lag = 1; lag <= LAST_LAG; ++lag) {
      target[lag] = target_index < 16
          ? mixed_a[target_index].delta[lag]
          : ((target_index * 97 + lag * 53) % 129) - 64;
    }
    const KdQueryResult indexed = self_test_tree.nearest(target);
    const KdQueryResult brute = self_test_linear.nearest(target);
    if (!indexed.complete || !brute.complete ||
        indexed.point_index != brute.point_index ||
        indexed.distance != brute.distance ||
        indexed.stats.point_distances + indexed.stats.pruned_points !=
            mixed_a.size() ||
        brute.stats.point_distances != mixed_a.size())
      throw std::runtime_error("self-test kd-tree/brute query mismatch");
    add_kd_stats(direct_kd_stats, indexed.stats);
  }
  if (direct_kd_stats.pruned_points == 0 ||
      direct_kd_stats.pruned_subtrees == 0)
    throw std::runtime_error("self-test kd-tree did not exercise pruning");

  const ExactDeltaLinearIndex linear_a(mixed_a);
  const ExactDeltaLinearIndex linear_b(mixed_b);
  MixedSixCycleImprovement brute_mixed;
  brute_mixed.energy = mixed_state.energy;
  brute_mixed.checker_components = {{mixed_a.size(), mixed_b.size()}};
  if (!scan_mixed_six_cycles_one_orientation(
          mixed_state, 0, mixed_b, linear_b, Clock::time_point::max(), false,
          MIXED_SELF_TEST_RAW_LIMIT, brute_mixed) ||
      !scan_mixed_six_cycles_one_orientation(
          mixed_state, 1, mixed_a, linear_a, Clock::time_point::max(), false,
          MIXED_SELF_TEST_RAW_LIMIT, brute_mixed))
    throw std::runtime_error("self-test bounded brute mixed scan interrupted");
  brute_mixed.complete = true;
  bool same_mixed_move = mixed.move.size == brute_mixed.move.size;
  for (int entry = 0; same_mixed_move && entry < mixed.move.size; ++entry)
    same_mixed_move =
        mixed.move.position[entry] == brute_mixed.move.position[entry];
  if (!brute_mixed.found || !same_mixed_move ||
      mixed.energy != brute_mixed.energy || mixed.delta != brute_mixed.delta ||
      mixed.raw_patterns != brute_mixed.raw_patterns ||
      mixed.legal_cycles != brute_mixed.legal_cycles ||
      mixed.queries != brute_mixed.queries ||
      mixed.possible_pair_distances !=
          brute_mixed.possible_pair_distances ||
      brute_mixed.kd_stats.point_distances !=
          brute_mixed.possible_pair_distances ||
      brute_mixed.kd_stats.pruned_points != 0)
    throw std::runtime_error("self-test indexed/brute mixed scan mismatch");

  int mixed_a_flips = 0, mixed_b_flips = 0;
  for (int entry = 0; entry < mixed.move.size; ++entry) {
    mixed_a_flips += mixed.move.position[entry] / N == 0;
    mixed_b_flips += mixed.move.position[entry] / N == 1;
  }
  if (!((mixed_a_flips == 6 && mixed_b_flips == BASIC_MOVE_SIZE) ||
        (mixed_a_flips == BASIC_MOVE_SIZE && mixed_b_flips == 6)) ||
      correlation_delta(mixed_state, mixed.move) != mixed.delta ||
      energy_after(mixed_state, mixed.delta) != mixed.energy)
    throw std::runtime_error("self-test mixed move score mismatch");
  State mixed_exact;
  mixed_exact.profile = mixed_state.profile;
  mixed_exact.sequence = mixed_state.sequence;
  flip_direct_all(mixed_exact.sequence, mixed.move);
  validate_margins(mixed_exact);
  recompute(mixed_exact);
  apply_move(mixed_state, mixed.move, mixed.delta);
  if (mixed_state.sequence != mixed_exact.sequence ||
      mixed_state.residual != mixed_exact.residual ||
      mixed_state.energy != mixed_exact.energy ||
      mixed_state.single != mixed_exact.single)
    throw std::runtime_error("self-test mixed apply/cache mismatch");
  validate(mixed_state);
  const MixedSixCycleImprovement interrupted_mixed =
      best_mixed_six_cycle_improvement(
          mixed_state, Clock::now(), true,
          MIXED_SELF_TEST_RAW_LIMIT, MIXED_SELF_TEST_CHECKER_LIMIT);
  if (interrupted_mixed.complete || interrupted_mixed.found)
    throw std::runtime_error(
        "self-test partial mixed scan was treated as complete");

  std::cout << "self_test=passed\n";
  std::cout << "static_profiles=" << PROFILE_COUNT << '\n';
  std::cout << "margin_fixtures=" << PROFILE_COUNT << '\n';
  std::cout << "profile_zero_lag_norm=594\n";
  std::cout << "profile_nonzero_paf_sum=-74\n";
  std::cout << "delta_profiles=0," << PROFILE_COUNT - 1 << '\n';
  std::cout << "delta_trials=" << delta_trials << '\n';
  std::cout << "compound_delta_trials=" << compound_delta_trials << '\n';
  std::cout << "checkpoint_parser_rejections=6\n";
  std::cout << "cross_pair_components=" << cross.a_components << 'x'
            << cross.b_components << '\n';
  std::cout << "cross_pair_evaluations=" << cross.evaluations << '\n';
  std::cout << "same_sequence_pair_components=" << same.components[0] << 'x'
            << same.components[1] << '\n';
  std::cout << "same_sequence_pair_evaluations=" << same.evaluations << '\n';
  std::cout << "same_sequence_pair_overlap_skips=" << same.overlap_skips
            << '\n';
  std::cout << "same_sequence_deadline_firewall=passed\n";
  std::cout << "six_cycle_unique_supports=6\n";
  std::cout << "six_cycle_raw_patterns_per_sequence="
            << SIX_CYCLE_RAW_PATTERNS_PER_SEQUENCE << '\n';
  std::cout << "six_cycle_valid_cycles="
            << cycle.valid_cycles[0] + cycle.valid_cycles[1] << '\n';
  std::cout << "six_cycle_evaluations="
            << cycle.evaluations[0] + cycle.evaluations[1] << '\n';
  std::cout << "six_cycle_deadline_firewall=passed\n";
  std::cout << "eight_cycle_canonical_supports=72\n";
  std::cout << "eight_cycle_sign_fixtures=260\n";
  std::cout << "eight_cycle_bounded_raw_assignments="
            << eight.raw_assignments[0] + eight.raw_assignments[1] << '\n';
  std::cout << "eight_cycle_bounded_legal_cycles="
            << eight.legal_cycles[0] + eight.legal_cycles[1] << '\n';
  std::cout << "eight_cycle_bounded_evaluations="
            << eight.evaluations[0] + eight.evaluations[1] << '\n';
  std::cout << "eight_cycle_deadline_firewall=passed\n";
  std::cout << "mixed_six_cycle_bounded_raw_patterns="
            << mixed.raw_patterns[0] + mixed.raw_patterns[1] << '\n';
  std::cout << "mixed_six_cycle_bounded_legal_cycles="
            << mixed.legal_cycles[0] + mixed.legal_cycles[1] << '\n';
  std::cout << "mixed_six_cycle_bounded_queries="
            << mixed.queries[0] + mixed.queries[1] << '\n';
  std::cout << "mixed_six_cycle_possible_pair_distances="
            << mixed.possible_pair_distances << '\n';
  std::cout << "mixed_six_cycle_indexed_pair_distances="
            << mixed.kd_stats.point_distances << '\n';
  std::cout << "mixed_six_cycle_pruned_points="
            << mixed.kd_stats.pruned_points << '\n';
  std::cout << "mixed_six_cycle_brute_force_match=passed\n";
  std::cout << "mixed_six_cycle_direct_kd_queries=32\n";
  std::cout << "mixed_six_cycle_deadline_firewall=passed\n";
}

uint64_t parse_u64(const std::string &text, const char *name) {
  size_t used = 0;
  const uint64_t value = std::stoull(text, &used);
  if (used != text.size()) throw std::runtime_error(std::string("bad ") + name);
  return value;
}

int parse_int(const std::string &text, const char *name) {
  size_t used = 0;
  const int value = std::stoi(text, &used);
  if (used != text.size()) throw std::runtime_error(std::string("bad ") + name);
  return value;
}

double parse_double(const std::string &text, const char *name) {
  size_t used = 0;
  const double value = std::stod(text, &used);
  if (used != text.size()) throw std::runtime_error(std::string("bad ") + name);
  return value;
}

Options parse_options(int argc, char **argv) {
  Options options;
  auto require_value = [&](int &index) -> std::string {
    if (++index >= argc) throw std::runtime_error("missing option value");
    return argv[index];
  };
  for (int i = 1; i < argc; ++i) {
    const std::string argument = argv[i];
    if (argument == "--seconds")
      options.seconds = parse_double(require_value(i), "seconds");
    else if (argument == "--iterations")
      options.iterations = parse_u64(require_value(i), "iterations");
    else if (argument == "--seed")
      options.seed = parse_u64(require_value(i), "seed");
    else if (argument == "--profile") {
      options.profile = parse_int(require_value(i), "profile");
      options.profile_explicit = true;
    }
    else if (argument == "--epoch")
      options.epoch = parse_u64(require_value(i), "epoch");
    else if (argument == "--polish-steps")
      options.polish_steps = parse_int(require_value(i), "polish-steps");
    else if (argument == "--initial-mix-switches")
      options.initial_mix_switches =
          parse_int(require_value(i), "initial-mix-switches");
    else if (argument == "--late-window")
      options.late_window = parse_int(require_value(i), "late-window");
    else if (argument == "--validate-every")
      options.validate_every = parse_int(require_value(i), "validate-every");
    else if (argument == "--mode")
      options.mode = require_value(i);
    else if (argument == "--temperature-start")
      options.temperature_start =
          parse_double(require_value(i), "temperature-start");
    else if (argument == "--temperature-end")
      options.temperature_end =
          parse_double(require_value(i), "temperature-end");
    else if (argument == "--compound-probability")
      options.compound_probability =
          parse_double(require_value(i), "compound-probability");
    else if (argument == "--cross-pair-polish")
      options.cross_pair_polish = true;
    else if (argument == "--cross-pair-max-rounds")
      options.cross_pair_max_rounds =
          parse_int(require_value(i), "cross-pair-max-rounds");
    else if (argument == "--same-sequence-pair-polish")
      options.same_sequence_pair_polish = true;
    else if (argument == "--same-sequence-pair-max-rounds")
      options.same_sequence_pair_max_rounds =
          parse_int(require_value(i), "same-sequence-pair-max-rounds");
    else if (argument == "--six-cycle-polish")
      options.six_cycle_polish = true;
    else if (argument == "--six-cycle-max-rounds")
      options.six_cycle_max_rounds =
          parse_int(require_value(i), "six-cycle-max-rounds");
    else if (argument == "--eight-cycle-polish")
      options.eight_cycle_polish = true;
    else if (argument == "--eight-cycle-max-rounds")
      options.eight_cycle_max_rounds =
          parse_int(require_value(i), "eight-cycle-max-rounds");
    else if (argument == "--mixed-six-cycle-polish")
      options.mixed_six_cycle_polish = true;
    else if (argument == "--mixed-six-cycle-max-rounds")
      options.mixed_six_cycle_max_rounds =
          parse_int(require_value(i), "mixed-six-cycle-max-rounds");
    else if (argument == "--polish-only")
      options.polish_only = true;
    else if (argument == "--initial-checkpoint")
      options.initial_checkpoint = require_value(i);
    else if (argument == "--output")
      options.output = require_value(i);
    else if (argument == "--quiet")
      options.quiet = true;
    else if (argument == "--self-test")
      options.self_test = true;
    else if (argument == "--help") {
      std::cout
          << "Usage: search_legendre_333_profile_local [options]\n"
          << "  --seconds S                 wall-clock budget (default 30)\n"
          << "  --iterations N              deterministic proposal budget\n"
          << "  --seed N                    reproducible seed\n"
          << "  --profile N                 compressed profile 0..20 (default 0)\n"
          << "  --epoch N                   proposals between polish/restarts\n"
          << "  --polish-steps N            exact checkerboard descent steps\n"
          << "  --initial-mix-switches N    random switches per new sequence\n"
          << "  --mode late|anneal          acceptance rule (default anneal)\n"
          << "  --late-window N             late-acceptance history length\n"
          << "  --temperature-start X       annealing start temperature\n"
          << "  --temperature-end X         annealing end temperature\n"
          << "  --compound-probability P    simultaneous A/B switches (default 0)\n"
          << "  --cross-pair-polish          exhaustive A-switch x B-switch polish\n"
          << "  --cross-pair-max-rounds N    strict pair improvements per polish (16)\n"
          << "  --same-sequence-pair-polish  exhaustive disjoint switch pairs in A/B\n"
          << "  --same-sequence-pair-max-rounds N strict improvements per polish (16)\n"
          << "  --six-cycle-polish           exhaustive alternating K3,3 six-cycles\n"
          << "  --six-cycle-max-rounds N     strict cycle improvements per polish (16)\n"
          << "  --eight-cycle-polish         exact alternating 4x4 eight-cycles\n"
          << "  --eight-cycle-max-rounds N   strict cycle improvements per polish (16)\n"
          << "  --mixed-six-cycle-polish     exact six-cycle/opposite-switch polish\n"
          << "  --mixed-six-cycle-max-rounds N strict mixed improvements (16)\n"
          << "  --polish-only                polish initial state without random search\n"
          << "  --initial-checkpoint PATH    load profile,a,b and recompute all data\n"
          << "  --validate-every N          exact cache-validation interval\n"
          << "  --output PATH               JSON checkpoint path\n"
          << "  --quiet                     suppress incumbent messages\n"
          << "  --self-test                 margins and delta regression\n";
      std::exit(0);
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  if (!(options.seconds > 0) || options.profile < 0 ||
      options.profile >= PROFILE_COUNT || options.epoch == 0 ||
      options.polish_steps < 0 || options.initial_mix_switches < 0 ||
      options.late_window <= 0 || options.validate_every < 0 ||
      (options.mode != "late" && options.mode != "anneal") ||
      !(options.temperature_start > 0) ||
      !(options.temperature_end > 0) ||
      !(options.compound_probability >= 0.0 &&
        options.compound_probability <= 1.0) ||
      options.cross_pair_max_rounds <= 0 ||
      options.same_sequence_pair_max_rounds <= 0 ||
      options.six_cycle_max_rounds <= 0 ||
      options.eight_cycle_max_rounds <= 0 ||
      options.mixed_six_cycle_max_rounds <= 0)
    throw std::runtime_error("invalid option value");
  return options;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    Options options = parse_options(argc, argv);
    initialize_and_verify_profiles();
    if (options.self_test) {
      run_self_test();
      return 0;
    }

    State initial_state;
    const State *initial_pointer = nullptr;
    if (!options.initial_checkpoint.empty()) {
      initial_state = load_initial_checkpoint(options.initial_checkpoint);
      if (options.profile_explicit && options.profile != initial_state.profile)
        throw std::runtime_error(
            "--profile disagrees with the initial checkpoint profile");
      options.profile = initial_state.profile;
      initial_pointer = &initial_state;
    }

    const auto started = Clock::now();
    const SearchResult result = search(options, initial_pointer);
    const double elapsed =
        std::chrono::duration<double>(Clock::now() - started).count();
    if (!result.best.initialized)
      throw std::runtime_error("search produced no checkpoint");
    State checked = state_from_candidate(result.best);
    validate(checked);
    if (checked.residual != result.best.residual)
      throw std::runtime_error("output residuals fail recomputation");
    write_checkpoint(options.output, result, options, elapsed);

    const Metrics &metrics = result.best.metrics;
    std::cout << "output=" << options.output << '\n';
    std::cout << "exact=" << (metrics.energy == 0 ? "true" : "false") << '\n';
    std::cout << "certificate="
              << (metrics.energy == 0
                      ? "pending_independent_verification"
                      : "none_near_miss_only")
              << '\n';
    std::cout << "energy_half_paf=" << metrics.energy << '\n';
    std::cout << "energy_paf=" << 4 * metrics.energy << '\n';
    std::cout << "bad_lag_count=" << metrics.nonzero << '\n';
    std::cout << "max_abs_paf_residual=" << 2 * metrics.max_abs << '\n';
    std::cout << "l1_paf_residual=" << 2 * metrics.l1 << '\n';
    std::cout << "proposals=" << result.proposals << '\n';
    std::cout << "accepted=" << result.accepted << '\n';
    std::cout << "restarts=" << result.restarts << '\n';
    std::cout << "cross_pair_polish_moves="
              << result.cross_pair_polish_moves << '\n';
    std::cout << "cross_pair_scans=" << result.cross_pair_scans << '\n';
    std::cout << "complete_cross_pair_scans="
              << result.complete_cross_pair_scans << '\n';
    std::cout << "cross_pair_evaluations="
              << result.cross_pair_evaluations << '\n';
    std::cout << "incomplete_cross_pair_scans="
              << result.incomplete_cross_pair_scans << '\n';
    std::cout << "last_cross_pair_components="
              << result.last_cross_pair_a_components << 'x'
              << result.last_cross_pair_b_components << '\n';
    std::cout << "last_cross_pair_evaluations="
              << result.last_cross_pair_evaluations << '\n';
    std::cout << "same_sequence_pair_polish_moves="
              << result.same_sequence_pair_polish_moves << '\n';
    std::cout << "same_sequence_pair_scans="
              << result.same_sequence_pair_scans << '\n';
    std::cout << "complete_same_sequence_pair_scans="
              << result.complete_same_sequence_pair_scans << '\n';
    std::cout << "same_sequence_pair_evaluations="
              << result.same_sequence_pair_evaluations << '\n';
    std::cout << "same_sequence_pair_overlap_skips="
              << result.same_sequence_pair_overlap_skips << '\n';
    std::cout << "incomplete_same_sequence_pair_scans="
              << result.incomplete_same_sequence_pair_scans << '\n';
    std::cout << "last_same_sequence_pair_components="
              << result.last_same_sequence_pair_components[0] << 'x'
              << result.last_same_sequence_pair_components[1] << '\n';
    std::cout << "six_cycle_polish_moves="
              << result.six_cycle_polish_moves << '\n';
    std::cout << "six_cycle_scans=" << result.six_cycle_scans << '\n';
    std::cout << "complete_six_cycle_scans="
              << result.complete_six_cycle_scans << '\n';
    std::cout << "six_cycle_raw_patterns="
              << result.six_cycle_raw_patterns << '\n';
    std::cout << "six_cycle_valid_cycles="
              << result.six_cycle_valid_cycles << '\n';
    std::cout << "six_cycle_evaluations="
              << result.six_cycle_evaluations << '\n';
    std::cout << "incomplete_six_cycle_scans="
              << result.incomplete_six_cycle_scans << '\n';
    std::cout << "eight_cycle_polish_moves="
              << result.eight_cycle_polish_moves << '\n';
    std::cout << "eight_cycle_scans=" << result.eight_cycle_scans << '\n';
    std::cout << "complete_eight_cycle_scans="
              << result.complete_eight_cycle_scans << '\n';
    std::cout << "incomplete_eight_cycle_scans="
              << result.incomplete_eight_cycle_scans << '\n';
    std::cout << "eight_cycle_row_cycles="
              << result.eight_cycle_row_cycles << '\n';
    std::cout << "eight_cycle_sign_orientations="
              << result.eight_cycle_sign_orientations << '\n';
    std::cout << "eight_cycle_raw_assignments="
              << result.eight_cycle_raw_assignments << '\n';
    std::cout << "eight_cycle_repeated_column_skips="
              << result.eight_cycle_repeated_column_skips << '\n';
    std::cout << "eight_cycle_legal_cycles="
              << result.eight_cycle_legal_cycles << '\n';
    std::cout << "eight_cycle_evaluations="
              << result.eight_cycle_evaluations << '\n';
    std::cout << "mixed_six_cycle_polish_moves="
              << result.mixed_six_cycle_polish_moves << '\n';
    std::cout << "mixed_six_cycle_scans="
              << result.mixed_six_cycle_scans << '\n';
    std::cout << "complete_mixed_six_cycle_scans="
              << result.complete_mixed_six_cycle_scans << '\n';
    std::cout << "incomplete_mixed_six_cycle_scans="
              << result.incomplete_mixed_six_cycle_scans << '\n';
    std::cout << "mixed_six_cycle_raw_patterns="
              << result.mixed_six_cycle_raw_patterns << '\n';
    std::cout << "mixed_six_cycle_legal_cycles="
              << result.mixed_six_cycle_legal_cycles << '\n';
    std::cout << "mixed_six_cycle_queries="
              << result.mixed_six_cycle_queries << '\n';
    std::cout << "mixed_six_cycle_possible_pair_distances="
              << result.mixed_six_cycle_possible_pair_distances << '\n';
    std::cout << "mixed_six_cycle_pair_distances="
              << result.mixed_six_cycle_pair_distances << '\n';
    std::cout << "mixed_six_cycle_tree_nodes="
              << result.mixed_six_cycle_tree_nodes << '\n';
    std::cout << "mixed_six_cycle_tree_node_visits="
              << result.mixed_six_cycle_tree_node_visits << '\n';
    std::cout << "mixed_six_cycle_box_tests="
              << result.mixed_six_cycle_box_tests << '\n';
    std::cout << "mixed_six_cycle_pruned_subtrees="
              << result.mixed_six_cycle_pruned_subtrees << '\n';
    std::cout << "mixed_six_cycle_pruned_points="
              << result.mixed_six_cycle_pruned_points << '\n';
    std::cout << "last_mixed_six_cycle_checker_components="
              << result.last_mixed_six_cycle_checker_components[0] << 'x'
              << result.last_mixed_six_cycle_checker_components[1] << '\n';
    std::cout << "neighborhood_evaluations="
              << result.neighborhood_evaluations << '\n';
    std::cout << "seconds=" << std::fixed << std::setprecision(3) << elapsed
              << '\n';
    if (metrics.energy == 0)
      std::cout << "verification_required=python3 verify_legendre_333.py "
                << options.output << '\n';
    return metrics.energy == 0 ? 0 : 2;
  } catch (const std::exception &error) {
    std::cerr << "error=" << error.what() << '\n';
    return 3;
  }
}
