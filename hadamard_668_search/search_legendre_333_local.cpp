// Parallel integer local search for the prescribed-compression LP(333) route.
//
// A move swaps a +1 and a -1 in one CRT column, so all 74 prescribed
// length-37 compression entries remain exact.  For lag k=1,...,166 we store
//
//   residual[k] = (PAF_A(k) + PAF_B(k) + 2) / 2
//
// and hence the unique zero of every implemented objective is an exact
// Legendre pair.  Single-flip correlation deltas are cached; a two-sign
// column swap is scored in O(166), then the cache is updated exactly.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

namespace {

constexpr int N = 333;
constexpr int ROWS = 9;
constexpr int COLS = 37;
constexpr int LAST_LAG = 166;
constexpr int MAX_FLIPS = 6;

using Clock = std::chrono::steady_clock;
using Signs = std::array<int8_t, N>;
using Residuals = std::array<int16_t, LAST_LAG + 1>;
using Delta = std::array<int16_t, LAST_LAG + 1>;
// Keep the 111 KiB two-sequence cache on the heap.  Besides making worker
// stacks small, this lets sanitizer/debug builds use the same validation path
// as optimized runs on platforms whose std::thread stacks are modest.
using SingleDeltas = std::vector<std::array<int8_t, LAST_LAG + 1>>;

struct Options {
  double seconds = 30.0;
  uint64_t iterations = 0;  // Per worker.  Zero selects the wall clock.
  int threads = 1;
  uint64_t seed = 668;
  uint64_t epoch = 250000;
  int polish_steps = 24;
  int compound_polish_samples = 4096;
  int objective = -1;  // -1 diversifies workers over exact objectives.
  std::string mode = "auto";  // auto, anneal, or late.
  double temperature_start = 0.0;
  double temperature_end = 0.0;
  int late_window = 2048;
  int validate_every = 1000000;
  std::string output = "output/legendre_333_local_best.json";
  bool quiet = false;
};

struct State {
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
  int64_t fourth = 0;

  auto key() const { return std::tie(energy, nonzero, max_abs, l1, fourth); }
};

struct Candidate {
  std::array<Signs, 2> sequence{};
  Residuals residual{};
  Metrics metrics{};
  uint64_t worker_seed = 0;
  uint64_t moves = 0;
  uint64_t accepted = 0;
  uint64_t restarts = 0;
  bool initialized = false;
};

struct Move {
  std::array<int, MAX_FLIPS> position{};  // 0..332=A, 333..665=B.
  int size = 0;
};

struct WorkerResult {
  Candidate best{};
  uint64_t moves = 0;
  uint64_t accepted = 0;
  uint64_t restarts = 0;
};

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
      int d = std::abs(i - j);
      table[i][j] = static_cast<uint16_t>(std::min(d, N - d));
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

std::array<std::array<int, COLS>, 2> make_plus_counts() {
  std::array<std::array<int, COLS>, 2> counts{};
  counts[0][0] = counts[1][0] = 5;
  for (int column = 1; column < COLS; ++column) {
    const int character = legendre_symbol_37(column);
    counts[0][column] = character == 1 ? 6 : 3;
    counts[1][column] = character == 1 ? 3 : 6;
  }
  return counts;
}

const auto PLUS_COUNTS = make_plus_counts();

uint64_t splitmix64(uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

Metrics metrics(const Residuals &residual) {
  Metrics result;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int64_t value = residual[lag];
    const int64_t square = value * value;
    result.energy += square;
    result.nonzero += value != 0;
    result.max_abs = std::max(result.max_abs, std::abs(static_cast<int>(value)));
    result.l1 += std::abs(value);
    result.fourth += square * square;
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

int64_t search_cost(const Residuals &residual, int kind) {
  int64_t energy = 0, l1 = 0, nonzero = 0, fourth = 0;
  std::array<int64_t, ROWS> row_compression_residual{};
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int64_t value = residual[lag];
    const int64_t square = value * value;
    energy += square;
    l1 += std::abs(value);
    nonzero += value != 0;
    fourth += square * square;
    const int residue = lag % ROWS;
    row_compression_residual[residue] += value;
    row_compression_residual[(ROWS - residue) % ROWS] += value;
  }
  int64_t row_penalty = 0;
  for (const int64_t value : row_compression_residual)
    row_penalty += value * value;
  switch (kind & 3) {
    case 0: return energy;
    case 1: return energy + 4 * row_penalty;
    case 2: return energy + 4 * l1 + 16 * nonzero;
    default: return fourth + 8 * energy;
  }
}

int64_t search_cost_after(const State &state, const Delta &delta, int kind) {
  int64_t energy = 0, l1 = 0, nonzero = 0, fourth = 0;
  std::array<int64_t, ROWS> row_compression_residual{};
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int64_t value = state.residual[lag] + delta[lag];
    const int64_t square = value * value;
    energy += square;
    l1 += std::abs(value);
    nonzero += value != 0;
    fourth += square * square;
    const int residue = lag % ROWS;
    row_compression_residual[residue] += value;
    row_compression_residual[(ROWS - residue) % ROWS] += value;
  }
  int64_t row_penalty = 0;
  for (const int64_t value : row_compression_residual)
    row_penalty += value * value;
  switch (kind & 3) {
    case 0: return energy;
    case 1: return energy + 4 * row_penalty;
    case 2: return energy + 4 * l1 + 16 * nonzero;
    default: return fourth + 8 * energy;
  }
}

void recompute(State &state) {
  state.residual.fill(0);
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int paf_sum = 0;
    for (int which = 0; which < 2; ++which) {
      const auto &s = state.sequence[which];
      for (int i = 0; i < N; ++i) paf_sum += s[i] * s[(i + lag) % N];
    }
    if ((paf_sum + 2) & 1) throw std::runtime_error("PAF parity failure");
    state.residual[lag] = static_cast<int16_t>((paf_sum + 2) / 2);
  }
  state.energy = metrics(state.residual).energy;

  for (int which = 0; which < 2; ++which) {
    state.single[which].resize(N);
    const auto &s = state.sequence[which];
    for (int position = 0; position < N; ++position) {
      state.single[which][position][0] = 0;
      for (int lag = 1; lag <= LAST_LAG; ++lag) {
        const int neighbors = s[(position + lag) % N] +
                              s[(position - lag + N) % N];
        state.single[which][position][lag] =
            static_cast<int8_t>(-s[position] * neighbors);
      }
    }
  }
}

template <typename Rng>
State random_state(Rng &rng) {
  State state;
  for (int which = 0; which < 2; ++which) {
    state.sequence[which].fill(-1);
    for (int column = 0; column < COLS; ++column) {
      std::array<int, ROWS> rows{};
      std::iota(rows.begin(), rows.end(), 0);
      std::shuffle(rows.begin(), rows.end(), rng);
      for (int j = 0; j < PLUS_COUNTS[which][column]; ++j)
        state.sequence[which][CRT[rows[j]][column]] = 1;
    }
  }
  recompute(state);
  return state;
}

State state_from_candidate(const Candidate &candidate) {
  State state;
  state.sequence = candidate.sequence;
  recompute(state);
  return state;
}

bool contains(const Move &move, int global_position) {
  for (int i = 0; i < move.size; ++i)
    if (move.position[i] == global_position) return true;
  return false;
}

template <typename Rng>
void add_random_column_swap(const State &state, Move &move, Rng &rng) {
  if (move.size + 2 > MAX_FLIPS) throw std::runtime_error("move overflow");
  for (;;) {
    const int which = static_cast<int>(rng() & 1ULL);
    const int column = static_cast<int>(rng() % COLS);
    int positive = -1, negative = -1;
    for (int attempts = 0; attempts < 64 && (positive < 0 || negative < 0);
         ++attempts) {
      const int position = CRT[rng() % ROWS][column];
      const int global = which * N + position;
      if (contains(move, global)) continue;
      if (state.sequence[which][position] == 1)
        positive = global;
      else
        negative = global;
    }
    if (positive >= 0 && negative >= 0 && positive != negative) {
      move.position[move.size++] = positive;
      move.position[move.size++] = negative;
      return;
    }
  }
}

template <typename Rng>
Move random_move(const State &state, Rng &rng) {
  Move move;
  const uint64_t selector = rng() % 100;
  const int swaps = selector < 2 ? 3 : (selector < 18 ? 2 : 1);
  for (int i = 0; i < swaps; ++i) add_random_column_swap(state, move, rng);
  return move;
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

  // The cached single-flip deltas count a flipped/flipped pair twice, even
  // though its product is unchanged when both signs flip.
  for (int left = 0; left < move.size; ++left) {
    const int global_left = move.position[left];
    const int which = global_left / N;
    const int p = global_left % N;
    for (int right = left + 1; right < move.size; ++right) {
      const int global_right = move.position[right];
      if (global_right / N != which) continue;
      const int q = global_right % N;
      const int lag = DISTANCE[p][q];
      if (lag == 0 || lag > LAST_LAG)
        throw std::runtime_error("invalid distinct flip positions");
      delta[lag] += static_cast<int16_t>(
          2 * state.sequence[which][p] * state.sequence[which][q]);
    }
  }
  return delta;
}

void apply_move(State &state, const Move &move, const Delta &delta) {
  int64_t energy_delta = 0;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    energy_delta += 2LL * state.residual[lag] * delta[lag] +
                    1LL * delta[lag] * delta[lag];
    state.residual[lag] += delta[lag];
  }
  state.energy += energy_delta;

  for (int which = 0; which < 2; ++which) {
    std::array<int, MAX_FLIPS> positions{};
    std::array<int8_t, MAX_FLIPS> old_signs{};
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

    // Update cached rows belonging to unflipped positions.  A changed
    // neighbor contributes +2*s[p]*old_s[f] to its single-flip delta.
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

    // Flipped positions have a changed central sign as well as possibly
    // changed neighbors, so their complete cached rows are cheapest to redo.
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

void validate(const State &state) {
  for (int which = 0; which < 2; ++which) {
    int total_plus = 0;
    for (int column = 0; column < COLS; ++column) {
      int plus = 0;
      for (int row = 0; row < ROWS; ++row)
        plus += state.sequence[which][CRT[row][column]] == 1;
      if (plus != PLUS_COUNTS[which][column])
        throw std::runtime_error("fixed compression invariant failure");
      total_plus += plus;
    }
    if (total_plus != 167)
      throw std::runtime_error("sequence normalization failure");
  }

  State exact;
  exact.sequence = state.sequence;
  recompute(exact);
  if (exact.residual != state.residual || exact.energy != state.energy ||
      exact.single != state.single)
    throw std::runtime_error("incremental correlation cache failure");
}

Candidate make_candidate(const State &state, uint64_t worker_seed,
                         uint64_t moves, uint64_t accepted,
                         uint64_t restarts) {
  Candidate result;
  result.sequence = state.sequence;
  result.residual = state.residual;
  result.metrics = metrics(state.residual);
  result.worker_seed = worker_seed;
  result.moves = moves;
  result.accepted = accepted;
  result.restarts = restarts;
  result.initialized = true;
  return result;
}

std::mutex global_mutex;
Candidate global_best;
std::atomic<bool> exact_found{false};

void publish(const Candidate &candidate, bool quiet) {
  bool changed = false;
  {
    std::lock_guard<std::mutex> lock(global_mutex);
    if (better(candidate, global_best)) {
      global_best = candidate;
      changed = true;
    }
  }
  if (changed && !quiet) {
    std::cerr << "best energy=" << candidate.metrics.energy
              << " bad=" << candidate.metrics.nonzero
              << " max_abs_paf_residual=" << 2 * candidate.metrics.max_abs
              << " l1_paf_residual=" << 2 * candidate.metrics.l1 << '\n';
  }
  if (candidate.metrics.energy == 0) exact_found.store(true);
}

Candidate snapshot_global_best() {
  std::lock_guard<std::mutex> lock(global_mutex);
  return global_best;
}

struct ImprovingMove {
  Move move{};
  Delta delta{};
  int64_t cost = std::numeric_limits<int64_t>::max();
  bool found = false;
};

// Exact steepest descent over every one-column two-sign swap.  It is used at
// epoch boundaries; the O(166) cached scoring makes this affordable.
ImprovingMove best_basic_improvement(const State &state) {
  ImprovingMove best;
  best.cost = state.energy;
  for (int which = 0; which < 2; ++which) {
    for (int column = 0; column < COLS; ++column) {
      for (int positive_row = 0; positive_row < ROWS; ++positive_row) {
        const int positive = CRT[positive_row][column];
        if (state.sequence[which][positive] != 1) continue;
        for (int negative_row = 0; negative_row < ROWS; ++negative_row) {
          const int negative = CRT[negative_row][column];
          if (state.sequence[which][negative] != -1) continue;
          Move move;
          move.position[0] = which * N + positive;
          move.position[1] = which * N + negative;
          move.size = 2;
          Delta delta = correlation_delta(state, move);
          const int64_t cost = search_cost_after(state, delta, 0);
          if (cost < best.cost) {
            best.move = move;
            best.delta = delta;
            best.cost = cost;
            best.found = true;
          }
        }
      }
    }
  }
  return best;
}

template <typename Rng>
ImprovingMove best_sampled_compound_improvement(const State &state, Rng &rng,
                                                int samples) {
  ImprovingMove best;
  best.cost = state.energy;
  for (int sample = 0; sample < samples; ++sample) {
    Move move;
    add_random_column_swap(state, move, rng);
    add_random_column_swap(state, move, rng);
    // A small fraction of samples crosses a three-swap barrier.
    if (sample % 17 == 0) add_random_column_swap(state, move, rng);
    Delta delta = correlation_delta(state, move);
    const int64_t cost = search_cost_after(state, delta, 0);
    if (cost < best.cost) {
      best.move = move;
      best.delta = delta;
      best.cost = cost;
      best.found = true;
    }
  }
  return best;
}

template <typename Rng>
void perturb(State &state, Rng &rng, int swaps) {
  for (int i = 0; i < swaps; ++i) {
    Move move;
    add_random_column_swap(state, move, rng);
    const Delta delta = correlation_delta(state, move);
    apply_move(state, move, delta);
  }
}

double default_temperature_start(int kind) {
  switch (kind & 3) {
    case 0: return 64.0;
    case 1: return 128.0;
    case 2: return 96.0;
    default: return 12000.0;
  }
}

double default_temperature_end(int kind) {
  switch (kind & 3) {
    case 0: return 0.35;
    case 1: return 0.75;
    case 2: return 0.5;
    default: return 12.0;
  }
}

WorkerResult run_worker(int worker, const Options &options,
                        Clock::time_point deadline) {
  WorkerResult result;
  const uint64_t worker_seed =
      splitmix64(options.seed + 0x9e3779b97f4a7c15ULL * (worker + 1));
  std::mt19937_64 rng(worker_seed);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  const int kind = options.objective >= 0 ? options.objective : worker & 3;
  std::string mode = options.mode;
  if (mode == "auto") mode = (worker % 3 == 2) ? "late" : "anneal";
  const double start_temperature = options.temperature_start > 0
      ? options.temperature_start : default_temperature_start(kind);
  const double end_temperature = options.temperature_end > 0
      ? options.temperature_end : default_temperature_end(kind);

  State state = random_state(rng);
  Candidate worker_best = make_candidate(state, worker_seed, 0, 0, 0);
  publish(worker_best, options.quiet);
  std::vector<int64_t> late_history(
      static_cast<size_t>(std::max(1, options.late_window)),
      search_cost(state.residual, kind));
  uint64_t epoch_position = 0;

  auto within_budget = [&]() {
    if (exact_found.load()) return false;
    if (options.iterations) return result.moves < options.iterations;
    return Clock::now() < deadline;
  };

  while (within_budget()) {
    const uint64_t epoch_length = std::max<uint64_t>(1, options.epoch);
    const double fraction = static_cast<double>(epoch_position) /
                            static_cast<double>(epoch_length);
    const double temperature = start_temperature *
        std::pow(end_temperature / start_temperature, fraction);

    Move move = random_move(state, rng);
    Delta delta = correlation_delta(state, move);
    const int64_t current_cost = search_cost(state.residual, kind);
    const int64_t proposed_cost = search_cost_after(state, delta, kind);
    const int64_t change = proposed_cost - current_cost;
    bool accept = false;
    if (mode == "late") {
      const size_t slot = static_cast<size_t>(result.moves % late_history.size());
      accept = proposed_cost <= current_cost || proposed_cost <= late_history[slot];
      late_history[slot] = current_cost;
    } else {
      accept = change <= 0 ||
               uniform(rng) < std::exp(-static_cast<double>(change) / temperature);
    }

    ++result.moves;
    ++epoch_position;
    if (accept) {
      apply_move(state, move, delta);
      ++result.accepted;
      Candidate candidate = make_candidate(
          state, worker_seed, result.moves, result.accepted, result.restarts);
      if (better(candidate, worker_best)) {
        worker_best = candidate;
        publish(candidate, options.quiet);
      }
    }

    if (options.validate_every > 0 &&
        result.moves % static_cast<uint64_t>(options.validate_every) == 0)
      validate(state);

    if (epoch_position >= epoch_length && !exact_found.load()) {
      for (int step = 0; step < options.polish_steps; ++step) {
        ImprovingMove best_move = best_basic_improvement(state);
        if (!best_move.found && options.compound_polish_samples > 0)
          best_move = best_sampled_compound_improvement(
              state, rng, options.compound_polish_samples);
        if (!best_move.found) break;
        apply_move(state, best_move.move, best_move.delta);
        ++result.moves;
        ++result.accepted;
        Candidate candidate = make_candidate(
            state, worker_seed, result.moves, result.accepted, result.restarts);
        if (better(candidate, worker_best)) {
          worker_best = candidate;
          publish(candidate, options.quiet);
        }
        if (candidate.metrics.energy == 0) break;
      }
      validate(state);
      if (exact_found.load()) break;

      // Alternate fully independent restarts with kicks from the best state
      // seen by this worker and, occasionally, from the global incumbent.
      ++result.restarts;
      if (result.restarts % 3 == 0) {
        const Candidate incumbent = snapshot_global_best();
        state = incumbent.initialized ? state_from_candidate(incumbent)
                                      : random_state(rng);
        perturb(state, rng, 16 + static_cast<int>(rng() % 49));
      } else if (result.restarts & 1ULL) {
        state = state_from_candidate(worker_best);
        perturb(state, rng, 24 + static_cast<int>(rng() % 73));
      } else {
        state = random_state(rng);
      }
      epoch_position = 0;
      std::fill(late_history.begin(), late_history.end(),
                search_cost(state.residual, kind));
    }
  }

  validate(state);
  result.best = worker_best;
  result.best.moves = result.moves;
  result.best.accepted = result.accepted;
  result.best.restarts = result.restarts;
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

void write_int_array(std::ostream &out, const std::vector<int> &values) {
  out << '[';
  for (size_t i = 0; i < values.size(); ++i) {
    if (i) out << ',';
    out << values[i];
  }
  out << ']';
}

std::vector<int> compression(const Signs &sequence) {
  std::vector<int> result(COLS, 0);
  for (int column = 0; column < COLS; ++column)
    for (int row = 0; row < ROWS; ++row)
      result[column] += sequence[CRT[row][column]];
  return result;
}

void write_candidate(const std::string &path, const Candidate &candidate,
                     const Options &options, double elapsed,
                     const std::vector<WorkerResult> &workers) {
  const std::filesystem::path output(path);
  if (output.has_parent_path())
    std::filesystem::create_directories(output.parent_path());
  std::ofstream out(path);
  if (!out) throw std::runtime_error("could not open output file: " + path);

  uint64_t moves = 0, accepted = 0, restarts = 0;
  for (const auto &worker : workers) {
    moves += worker.moves;
    accepted += worker.accepted;
    restarts += worker.restarts;
  }

  out << "{\n";
  out << "  \"kind\": \"fixed-compression-legendre-local-search-candidate\",\n";
  out << "  \"exact\": " << (candidate.metrics.energy == 0 ? "true" : "false")
      << ",\n";
  out << "  \"length\": 333,\n";
  out << "  \"hadamard_order\": 668,\n";
  out << "  \"base_seed\": " << options.seed << ",\n";
  out << "  \"worker_seed\": " << candidate.worker_seed << ",\n";
  out << "  \"threads\": " << options.threads << ",\n";
  out << "  \"seconds\": " << std::fixed << std::setprecision(6) << elapsed
      << ",\n";
  out << "  \"energy_half_paf\": " << candidate.metrics.energy << ",\n";
  out << "  \"energy_paf\": " << 4 * candidate.metrics.energy << ",\n";
  out << "  \"bad_lag_count\": " << candidate.metrics.nonzero << ",\n";
  out << "  \"max_abs_paf_residual\": " << 2 * candidate.metrics.max_abs
      << ",\n";
  out << "  \"l1_paf_residual\": " << 2 * candidate.metrics.l1 << ",\n";
  out << "  \"compression_a\": ";
  write_int_array(out, compression(candidate.sequence[0]));
  out << ",\n  \"compression_b\": ";
  write_int_array(out, compression(candidate.sequence[1]));
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
  out << "  \"search\": {\"moves\":" << moves
      << ",\"accepted\":" << accepted << ",\"restarts\":" << restarts
      << ",\"epoch\":" << options.epoch
      << ",\"polish_steps\":" << options.polish_steps
      << ",\"compound_polish_samples\":" << options.compound_polish_samples
      << ",\"objective\":" << options.objective
      << ",\"mode\":\"" << options.mode << "\"}\n";
  out << "}\n";
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
  options.threads = std::max(1u, std::thread::hardware_concurrency());
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
    else if (argument == "--threads")
      options.threads = parse_int(require_value(i), "threads");
    else if (argument == "--seed")
      options.seed = parse_u64(require_value(i), "seed");
    else if (argument == "--epoch")
      options.epoch = parse_u64(require_value(i), "epoch");
    else if (argument == "--polish-steps")
      options.polish_steps = parse_int(require_value(i), "polish-steps");
    else if (argument == "--compound-polish-samples")
      options.compound_polish_samples =
          parse_int(require_value(i), "compound-polish-samples");
    else if (argument == "--objective")
      options.objective = parse_int(require_value(i), "objective");
    else if (argument == "--mode")
      options.mode = require_value(i);
    else if (argument == "--temperature-start")
      options.temperature_start = parse_double(require_value(i), "temperature-start");
    else if (argument == "--temperature-end")
      options.temperature_end = parse_double(require_value(i), "temperature-end");
    else if (argument == "--late-window")
      options.late_window = parse_int(require_value(i), "late-window");
    else if (argument == "--validate-every")
      options.validate_every = parse_int(require_value(i), "validate-every");
    else if (argument == "--output")
      options.output = require_value(i);
    else if (argument == "--quiet")
      options.quiet = true;
    else if (argument == "--help") {
      std::cout
          << "Usage: search_legendre_333_local [options]\n"
          << "  --seconds S             wall-clock budget (default 30)\n"
          << "  --iterations N          deterministic per-worker move budget\n"
          << "  --threads N             parallel independent workers\n"
          << "  --seed N                reproducible base seed\n"
          << "  --epoch N               moves between polish/restart phases\n"
          << "  --polish-steps N        exact steepest-descent steps per epoch\n"
          << "  --compound-polish-samples N sampled 4/6-flip moves at local minima\n"
          << "  --mode auto|anneal|late search acceptance rule\n"
          << "  --objective -1|0|1|2|3 exact-zero loss (-1 diversifies)\n"
          << "  --output PATH           JSON checkpoint path\n";
      std::exit(0);
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  if (!(options.seconds > 0) || options.threads <= 0 || options.epoch == 0 ||
      options.polish_steps < 0 || options.late_window <= 0 ||
      options.compound_polish_samples < 0 ||
      options.validate_every < 0 || options.objective < -1 ||
      options.objective > 3 ||
      (options.mode != "auto" && options.mode != "anneal" &&
       options.mode != "late") || options.temperature_start < 0 ||
      options.temperature_end < 0)
    throw std::runtime_error("invalid option value");
  return options;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    const auto started = Clock::now();
    const auto deadline = started + std::chrono::duration_cast<Clock::duration>(
        std::chrono::duration<double>(options.seconds));
    std::vector<WorkerResult> results(static_cast<size_t>(options.threads));
    std::vector<std::thread> threads;
    threads.reserve(static_cast<size_t>(options.threads));
    for (int worker = 0; worker < options.threads; ++worker) {
      threads.emplace_back([&, worker] {
        results[worker] = run_worker(worker, options, deadline);
      });
    }
    for (auto &thread : threads) thread.join();

    const double elapsed =
        std::chrono::duration<double>(Clock::now() - started).count();
    const Candidate best = snapshot_global_best();
    if (!best.initialized) throw std::runtime_error("search produced no state");
    State checked = state_from_candidate(best);
    validate(checked);
    if (checked.residual != best.residual)
      throw std::runtime_error("output candidate residual mismatch");
    write_candidate(options.output, best, options, elapsed, results);

    std::cout << "output=" << options.output << '\n';
    std::cout << "exact=" << (best.metrics.energy == 0 ? "true" : "false") << '\n';
    std::cout << "energy_half_paf=" << best.metrics.energy << '\n';
    std::cout << "energy_paf=" << 4 * best.metrics.energy << '\n';
    std::cout << "bad_lag_count=" << best.metrics.nonzero << '\n';
    std::cout << "max_abs_paf_residual=" << 2 * best.metrics.max_abs << '\n';
    std::cout << "l1_paf_residual=" << 2 * best.metrics.l1 << '\n';
    std::cout << "seconds=" << std::fixed << std::setprecision(3) << elapsed << '\n';
    if (best.metrics.energy == 0)
      std::cout << "verification_required=python3 verify_legendre_333.py "
                << options.output << '\n';
    return best.metrics.energy == 0 ? 0 : 2;
  } catch (const std::exception &error) {
    std::cerr << "error=" << error.what() << '\n';
    return 3;
  }
}
