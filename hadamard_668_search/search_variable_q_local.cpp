// Parallel local search for the variable-q special Golay lane BS(84,83).
//
// A selected one of the 288 nominal ordinary/alternating margin shards is
// preserved exactly: every move exchanges a +1 and a -1 inside one
// sequence/parity class.  Global coordinate alternation reduces the default
// schedule to 156 representatives; an explicit shard list may still select
// any nominal shard.  For k=1,...,83 the state stores exactly
//
//   residual[k] = (C_A(k)+C_B(k)+C_C(k)+C_D(k)) / 2.
//
// The division is exact because every correlation row has even length.  The
// primary energy sum residual[k]^2 is nonnegative and has the unique zero
// BS(84,83).  Correlation changes are maintained incrementally with integer
// arithmetic and periodically checked by a full recomputation.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <limits>
#include <map>
#include <mutex>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

namespace {

constexpr int LONG = 84;
constexpr int SHORT = 83;
constexpr int SEQUENCES = 4;
constexpr int MAX_LENGTH = LONG;
constexpr int LAST_LAG = 83;
constexpr int GROUPS = 8;
constexpr int MAX_SWAPS = 3;
constexpr int MAX_FLIPS = 2 * MAX_SWAPS;

using Clock = std::chrono::steady_clock;
using Signs = std::array<int8_t, MAX_LENGTH>;
using Residuals = std::array<int16_t, LAST_LAG + 1>;
using Margin = std::array<int, SEQUENCES>;

struct Shard {
  Margin ordinary{};
  Margin alternating{};
  std::array<int, GROUPS> plus_count{};
  std::array<std::vector<int>, GROUPS> positions{};  // local coordinates
  std::vector<int> movable_groups{};
};

struct Options {
  double seconds = 30.0;
  uint64_t iterations = 0;  // Per worker; zero uses the shared wall clock.
  int threads = 1;
  uint64_t seed = 668;
  uint64_t epoch = 120000;
  int polish_steps = 5;
  int parity_polish_samples = 4096;
  int objective = -1;  // -1 diversifies workers over four unique-zero costs.
  std::string mode = "auto";  // auto, anneal, or late.
  double temperature_start = 0.0;
  double temperature_end = 0.0;
  int late_window = 2048;
  uint64_t validate_every = 1000000;
  int sample_shards = 0;
  std::string shard_spec;
  std::string output = "output/variable_q_local_best.json";
  std::string initial;
  bool preserve_endpoint_parity = false;
  bool quiet = false;
  bool list_shards = false;
};

struct State {
  std::array<Signs, SEQUENCES> sequence{};
  Residuals residual{};
  int64_t energy = 0;
  int shard = -1;
};

struct Metrics {
  int64_t energy = 0;
  int odd_residuals = 0;
  int nonzero = 0;
  int max_abs = 0;
  int64_t l1 = 0;
  int64_t fourth = 0;

  auto key() const {
    return std::tie(energy, odd_residuals, nonzero, max_abs, l1, fourth);
  }
};

struct Candidate {
  std::array<Signs, SEQUENCES> sequence{};
  Residuals residual{};
  Metrics metrics{};
  int shard = -1;
  uint64_t worker_seed = 0;
  uint64_t job = 0;
  bool initialized = false;
};

struct Move {
  // Encoded as sequence*MAX_LENGTH + local position.
  std::array<int, MAX_FLIPS> position{};
  int size = 0;
};

struct Syndrome {
  uint64_t low = 0;
  uint64_t high = 0;

  Syndrome &operator^=(const Syndrome &other) {
    low ^= other.low;
    high ^= other.high;
    return *this;
  }
  friend bool operator<(const Syndrome &left, const Syndrome &right) {
    return std::tie(left.high, left.low) < std::tie(right.high, right.low);
  }
};

struct SwapPattern {
  int group = 0;
  int first = 0;
  int second = 0;
};

using Delta = std::array<int16_t, LAST_LAG + 1>;

struct WorkerResult {
  Candidate best{};
  uint64_t moves = 0;
  uint64_t accepted = 0;
  uint64_t restarts = 0;
  uint64_t jobs = 0;
};

int length_of(int which) { return which < 2 ? LONG : SHORT; }

uint64_t splitmix64(uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

std::vector<Margin> row_sum_profiles() {
  std::vector<Margin> result;
  for (int a = 0; a <= LONG; a += 2)
    for (int b = 0; b <= a; b += 2)
      for (int c = 1; c <= SHORT; c += 2)
        for (int d = 1; d <= c; d += 2)
          if (a * a + b * b + c * c + d * d == 334)
            result.push_back({a, b, c, d});
  return result;
}

std::vector<Margin> compatible_alternating_profiles(
    const Margin &ordinary, const std::vector<Margin> &profiles) {
  std::set<Margin> values;
  for (const Margin &magnitudes : profiles) {
    for (int swap_even = 0; swap_even < 2; ++swap_even) {
      const int e0 = magnitudes[swap_even ? 1 : 0];
      const int e1 = magnitudes[swap_even ? 0 : 1];
      if ((ordinary[0] - e0) % 4 || (ordinary[1] - e1) % 4) continue;
      for (int swap_odd = 0; swap_odd < 2; ++swap_odd) {
        const int o0 = magnitudes[swap_odd ? 3 : 2];
        const int o1 = magnitudes[swap_odd ? 2 : 3];
        for (int sign0 : {-1, 1})
          for (int sign1 : {-1, 1}) {
            const int t0 = sign0 * o0;
            const int t1 = sign1 * o1;
            if ((ordinary[2] + t0) % 4 || (ordinary[3] + t1) % 4) continue;
            values.insert({e0, e1, t0, t1});
          }
      }
    }
  }
  return {values.begin(), values.end()};
}

std::vector<Shard> make_shards() {
  const auto profiles = row_sum_profiles();
  if (profiles.size() != 12) throw std::runtime_error("profile enumeration failure");
  std::vector<Shard> result;
  for (const Margin &ordinary : profiles) {
    const auto alternatives = compatible_alternating_profiles(ordinary, profiles);
    if (alternatives.size() != 24)
      throw std::runtime_error("alternating-profile enumeration failure");
    for (const Margin &alternating : alternatives) {
      Shard shard;
      shard.ordinary = ordinary;
      shard.alternating = alternating;
      for (int which = 0; which < SEQUENCES; ++which) {
        const int length = length_of(which);
        for (int parity = 0; parity < 2; ++parity) {
          const int group = 2 * which + parity;
          for (int position = parity; position < length; position += 2)
            shard.positions[group].push_back(position);
          const int parity_sum = parity == 0
              ? (ordinary[which] + alternating[which]) / 2
              : (ordinary[which] - alternating[which]) / 2;
          const int size = static_cast<int>(shard.positions[group].size());
          if ((size + parity_sum) % 2)
            throw std::runtime_error("parity-class margin failure");
          shard.plus_count[group] = (size + parity_sum) / 2;
          if (shard.plus_count[group] < 0 || shard.plus_count[group] > size)
            throw std::runtime_error("impossible parity-class margin");
          if (shard.plus_count[group] > 0 && shard.plus_count[group] < size)
            shard.movable_groups.push_back(group);
        }
      }
      if (shard.movable_groups.empty())
        throw std::runtime_error("shard has no legal swaps");
      result.push_back(std::move(shard));
    }
  }
  if (result.size() != 288) throw std::runtime_error("shard enumeration failure");
  return result;
}

const std::vector<Shard> SHARDS = make_shards();

Syndrome coordinate_syndrome(int which, int position) {
  Syndrome result;
  const int length = length_of(which);
  for (int lag = 0; lag < LAST_LAG; ++lag) {
    const bool active = (position == lag) != (position == length - 1 - lag);
    if (!active) continue;
    if (lag < 64)
      result.low ^= uint64_t{1} << lag;
    else
      result.high ^= uint64_t{1} << (lag - 64);
  }
  return result;
}

Syndrome swap_syndrome(int group, int first, int second) {
  const int which = group / 2;
  Syndrome result = coordinate_syndrome(which, first);
  result ^= coordinate_syndrome(which, second);
  return result;
}

std::map<Syndrome, std::vector<SwapPattern>> make_swap_buckets() {
  std::map<Syndrome, std::vector<SwapPattern>> result;
  for (int group = 0; group < GROUPS; ++group) {
    const int which = group / 2;
    const int parity = group % 2;
    const int length = length_of(which);
    for (int first = parity; first < length; first += 2)
      for (int second = first + 2; second < length; second += 2)
        result[swap_syndrome(group, first, second)].push_back(
            {group, first, second});
  }
  return result;
}

const auto SWAP_BUCKETS = make_swap_buckets();

int ordinary_sum(const Signs &sequence, int length) {
  int result = 0;
  for (int i = 0; i < length; ++i) result += sequence[i];
  return result;
}

int alternating_sum(const Signs &sequence, int length) {
  int result = 0;
  for (int i = 0; i < length; ++i)
    result += (i & 1) ? -sequence[i] : sequence[i];
  return result;
}

Metrics metrics(const Residuals &residual) {
  Metrics result;
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    const int64_t value = residual[lag];
    const int64_t square = value * value;
    result.energy += square;
    result.odd_residuals += std::abs(static_cast<int>(value)) & 1;
    result.nonzero += value != 0;
    result.max_abs = std::max(result.max_abs, std::abs(static_cast<int>(value)));
    result.l1 += std::abs(value);
    result.fourth += square * square;
  }
  return result;
}

bool better(const Candidate &left, const Candidate &right) {
  if (!left.initialized) return false;
  if (!right.initialized) return true;
  if (left.metrics.key() != right.metrics.key())
    return left.metrics.key() < right.metrics.key();
  if (left.shard != right.shard) return left.shard < right.shard;
  return left.sequence < right.sequence;
}

void recompute(State &state) {
  state.residual.fill(0);
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    int correlation = 0;
    for (int which = 0; which < SEQUENCES; ++which) {
      const int length = length_of(which);
      for (int i = 0; i + lag < length; ++i)
        correlation += state.sequence[which][i] * state.sequence[which][i + lag];
    }
    if (correlation & 1) throw std::runtime_error("odd base correlation");
    state.residual[lag] = static_cast<int16_t>(correlation / 2);
  }
  state.energy = metrics(state.residual).energy;
}

template <typename Rng>
State random_state(int shard_index, Rng &rng) {
  State state;
  state.shard = shard_index;
  for (auto &sequence : state.sequence) sequence.fill(0);
  const Shard &shard = SHARDS[shard_index];
  for (int group = 0; group < GROUPS; ++group) {
    const int which = group / 2;
    std::vector<int> positions = shard.positions[group];
    std::shuffle(positions.begin(), positions.end(), rng);
    for (int position : positions) state.sequence[which][position] = -1;
    for (int j = 0; j < shard.plus_count[group]; ++j)
      state.sequence[which][positions[j]] = 1;
  }
  recompute(state);
  return state;
}

State state_from_candidate(const Candidate &candidate) {
  State state;
  state.sequence = candidate.sequence;
  state.shard = candidate.shard;
  recompute(state);
  return state;
}

bool contains(const Move &move, int global_position) {
  for (int i = 0; i < move.size; ++i)
    if (move.position[i] == global_position) return true;
  return false;
}

template <typename Rng>
void add_group_swap(const State &state, int group, Move &move, Rng &rng) {
  if (move.size + 2 > MAX_FLIPS) throw std::runtime_error("move overflow");
  const int which = group / 2;
  const auto &positions = SHARDS[state.shard].positions[group];
  int positive = -1, negative = -1;
  while (positive < 0 || negative < 0) {
    const int position = positions[rng() % positions.size()];
    const int global = which * MAX_LENGTH + position;
    if (contains(move, global)) continue;
    if (state.sequence[which][position] == 1)
      positive = global;
    else
      negative = global;
  }
  move.position[move.size++] = positive;
  move.position[move.size++] = negative;
}

template <typename Rng>
Move random_move(const State &state, Rng &rng) {
  Move move;
  const auto &groups = SHARDS[state.shard].movable_groups;
  const uint64_t selector = rng() % 1000;
  const int swaps = selector < 18 ? 3 : (selector < 180 ? 2 : 1);
  std::array<int, MAX_SWAPS> selected{};
  int selected_count = 0;
  while (selected_count < swaps) {
    const int group = groups[rng() % groups.size()];
    bool used = false;
    for (int i = 0; i < selected_count; ++i) used |= selected[i] == group;
    if (used) continue;
    selected[selected_count++] = group;
    add_group_swap(state, group, move, rng);
  }
  return move;
}

template <typename Rng>
Move random_endpoint_preserving_move(const State &state, Rng &rng) {
  const auto &groups = SHARDS[state.shard].movable_groups;
  for (int outer = 0; outer < 1000; ++outer) {
    Move first;
    const int group = groups[rng() % groups.size()];
    add_group_swap(state, group, first, rng);
    const int first_local = first.position[0] % MAX_LENGTH;
    const int second_local = first.position[1] % MAX_LENGTH;
    const Syndrome key = swap_syndrome(group, first_local, second_local);
    // A reversal-paired swap in an odd-length sequence has zero endpoint
    // syndrome by itself.  It is already a complete parity-preserving move;
    // forcing a second zero-syndrome swap needlessly removes these edges from
    // the search graph.
    if (key.low == 0 && key.high == 0) return first;
    const auto found = SWAP_BUCKETS.find(key);
    if (found == SWAP_BUCKETS.end()) continue;
    const auto &bucket = found->second;
    for (int attempt = 0; attempt < 64; ++attempt) {
      const SwapPattern &pattern = bucket[rng() % bucket.size()];
      const int which = pattern.group / 2;
      const int left = which * MAX_LENGTH + pattern.first;
      const int right = which * MAX_LENGTH + pattern.second;
      if (contains(first, left) || contains(first, right)) continue;
      if (state.sequence[which][pattern.first] ==
          state.sequence[which][pattern.second])
        continue;
      Move result = first;
      result.position[result.size++] = left;
      result.position[result.size++] = right;
      return result;
    }
  }
  throw std::runtime_error("could not sample an endpoint-preserving move");
}

Delta correlation_delta(const State &state, const Move &move) {
  Delta delta{};
  for (int which = 0; which < SEQUENCES; ++which) {
    std::array<int, MAX_FLIPS> flipped{};
    int count = 0;
    for (int entry = 0; entry < move.size; ++entry) {
      if (move.position[entry] / MAX_LENGTH == which)
        flipped[count++] = move.position[entry] % MAX_LENGTH;
    }
    if (!count) continue;
    const int length = length_of(which);
    for (int j = 0; j < count; ++j) {
      const int p = flipped[j];
      const int sp = state.sequence[which][p];
      for (int q = 0; q < length; ++q) {
        bool q_flipped = false;
        for (int t = 0; t < count; ++t) q_flipped |= q == flipped[t];
        if (q_flipped) continue;
        const int lag = std::abs(p - q);
        if (lag)
          delta[lag] -= static_cast<int16_t>(sp * state.sequence[which][q]);
      }
    }
  }
  return delta;
}

int64_t energy_delta(const State &state, const Delta &delta) {
  int64_t result = 0;
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    result += 2LL * state.residual[lag] * delta[lag] +
              1LL * delta[lag] * delta[lag];
  return result;
}

int64_t search_cost(const Residuals &residual, int kind) {
  const Metrics value = metrics(residual);
  switch (kind & 3) {
    case 0: return value.energy;
    case 1: return value.energy + 4 * value.l1;
    // The endpoint-product telescope is equivalent to every half-residual
    // being even.  Expose that sparse necessary condition to one worker class.
    case 2: return value.energy + 32 * value.odd_residuals + 4 * value.nonzero;
    default: return value.fourth + 8 * value.energy;
  }
}

int64_t search_cost_after(const State &state, const Delta &delta, int kind) {
  Residuals proposed = state.residual;
  for (int lag = 1; lag <= LAST_LAG; ++lag) proposed[lag] += delta[lag];
  return search_cost(proposed, kind);
}

void apply_move(State &state, const Move &move, const Delta &delta) {
  state.energy += energy_delta(state, delta);
  for (int lag = 1; lag <= LAST_LAG; ++lag) state.residual[lag] += delta[lag];
  for (int entry = 0; entry < move.size; ++entry) {
    const int which = move.position[entry] / MAX_LENGTH;
    const int position = move.position[entry] % MAX_LENGTH;
    state.sequence[which][position] = -state.sequence[which][position];
  }
}

void validate(const State &state) {
  if (state.shard < 0 || state.shard >= static_cast<int>(SHARDS.size()))
    throw std::runtime_error("invalid shard in state");
  const Shard &shard = SHARDS[state.shard];
  for (int which = 0; which < SEQUENCES; ++which) {
    const int length = length_of(which);
    for (int i = 0; i < length; ++i)
      if (state.sequence[which][i] != 1 && state.sequence[which][i] != -1)
        throw std::runtime_error("non-sign coordinate");
    if (ordinary_sum(state.sequence[which], length) != shard.ordinary[which] ||
        alternating_sum(state.sequence[which], length) != shard.alternating[which])
      throw std::runtime_error("margin invariant failure");
  }
  State exact = state;
  recompute(exact);
  if (exact.residual != state.residual || exact.energy != state.energy)
    throw std::runtime_error("incremental correlation failure");
}

bool endpoint_parities_hold(const State &state) {
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    if (state.residual[lag] & 1) return false;
  return true;
}

Candidate make_candidate(const State &state, uint64_t worker_seed,
                         uint64_t job) {
  Candidate result;
  result.sequence = state.sequence;
  result.residual = state.residual;
  result.metrics = metrics(state.residual);
  result.shard = state.shard;
  result.worker_seed = worker_seed;
  result.job = job;
  result.initialized = true;
  return result;
}

std::mutex best_mutex;
Candidate global_best;
std::array<Candidate, 288> shard_best;
std::atomic<bool> exact_found{false};
std::atomic<uint64_t> next_job{0};

void publish(const Candidate &candidate, bool quiet) {
  bool global_changed = false;
  {
    std::lock_guard<std::mutex> lock(best_mutex);
    if (better(candidate, shard_best[candidate.shard]))
      shard_best[candidate.shard] = candidate;
    if (better(candidate, global_best)) {
      global_best = candidate;
      global_changed = true;
    }
  }
  if (global_changed && !quiet) {
    std::cerr << "best shard=" << candidate.shard
              << " energy_half=" << candidate.metrics.energy
              << " bad=" << candidate.metrics.nonzero
              << " max_abs_base=" << 2 * candidate.metrics.max_abs
              << " l1_base=" << 2 * candidate.metrics.l1 << '\n';
  }
  if (candidate.metrics.energy == 0)
    exact_found.store(true, std::memory_order_relaxed);
}

Candidate shard_incumbent(int shard) {
  std::lock_guard<std::mutex> lock(best_mutex);
  return shard_best[shard];
}

std::vector<int> parse_json_sign_array(const std::string &text,
                                       const std::string &label,
                                       int expected_length) {
  const std::string key = "\"" + label + "\"";
  size_t position = text.find(key);
  if (position == std::string::npos)
    throw std::runtime_error("initial JSON is missing " + label);
  position = text.find('[', position + key.size());
  if (position == std::string::npos)
    throw std::runtime_error("initial JSON has malformed " + label);
  ++position;
  std::vector<int> result;
  while (position < text.size()) {
    while (position < text.size() &&
           (text[position] == ' ' || text[position] == '\n' ||
            text[position] == '\r' || text[position] == '\t' ||
            text[position] == ','))
      ++position;
    if (position >= text.size()) break;
    if (text[position] == ']') {
      ++position;
      break;
    }
    int sign = 1;
    if (text[position] == '-') {
      sign = -1;
      ++position;
    }
    if (position >= text.size() || text[position] != '1')
      throw std::runtime_error("initial JSON contains a non-sign value");
    ++position;
    result.push_back(sign);
  }
  if (static_cast<int>(result.size()) != expected_length)
    throw std::runtime_error("initial JSON has wrong length for " + label);
  return result;
}

Candidate load_initial_candidate(const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("could not open initial JSON: " + path);
  const std::string text((std::istreambuf_iterator<char>(input)),
                         std::istreambuf_iterator<char>());
  State state;
  for (auto &sequence : state.sequence) sequence.fill(0);
  for (int which = 0; which < SEQUENCES; ++which) {
    const int length = length_of(which);
    const auto values = parse_json_sign_array(
        text, std::string(1, "abcd"[which]), length);
    for (int index = 0; index < length; ++index)
      state.sequence[which][index] = static_cast<int8_t>(values[index]);
  }

  for (int shard = 0; shard < static_cast<int>(SHARDS.size()); ++shard) {
    bool matches = true;
    for (int which = 0; which < SEQUENCES; ++which) {
      const int length = length_of(which);
      matches &= ordinary_sum(state.sequence[which], length) ==
                 SHARDS[shard].ordinary[which];
      matches &= alternating_sum(state.sequence[which], length) ==
                 SHARDS[shard].alternating[which];
    }
    if (matches) {
      state.shard = shard;
      break;
    }
  }
  if (state.shard < 0)
    throw std::runtime_error("initial JSON does not belong to a margin shard");
  recompute(state);
  validate(state);
  return make_candidate(state, 0, 0);
}

struct ImprovingMove {
  Move move{};
  Delta delta{};
  int64_t energy_change = 0;
  bool found = false;
};

ImprovingMove best_basic_improvement(const State &state) {
  ImprovingMove best;
  const Shard &shard = SHARDS[state.shard];
  for (int group : shard.movable_groups) {
    const int which = group / 2;
    const auto &positions = shard.positions[group];
    for (int positive : positions) {
      if (state.sequence[which][positive] != 1) continue;
      for (int negative : positions) {
        if (state.sequence[which][negative] != -1) continue;
        Move move;
        move.position[0] = which * MAX_LENGTH + positive;
        move.position[1] = which * MAX_LENGTH + negative;
        move.size = 2;
        const Delta delta = correlation_delta(state, move);
        const int64_t change = energy_delta(state, delta);
        if (!best.found || change < best.energy_change) {
          best.move = move;
          best.delta = delta;
          best.energy_change = change;
          best.found = change < 0;
        }
      }
    }
  }
  return best;
}

template <typename Rng>
ImprovingMove best_sampled_endpoint_improvement(const State &state, Rng &rng,
                                                int samples) {
  ImprovingMove best;
  for (int sample = 0; sample < samples; ++sample) {
    const Move move = random_endpoint_preserving_move(state, rng);
    const Delta delta = correlation_delta(state, move);
    const int64_t change = energy_delta(state, delta);
    if (!best.found || change < best.energy_change) {
      best.move = move;
      best.delta = delta;
      best.energy_change = change;
      best.found = change < 0;
    }
  }
  return best;
}

template <typename Rng>
void perturb(State &state, Rng &rng, int swaps, bool preserve_endpoint_parity) {
  for (int step = 0; step < swaps; ++step) {
    Move move;
    if (preserve_endpoint_parity) {
      move = random_endpoint_preserving_move(state, rng);
    } else {
      const auto &groups = SHARDS[state.shard].movable_groups;
      add_group_swap(state, groups[rng() % groups.size()], move, rng);
    }
    const Delta delta = correlation_delta(state, move);
    apply_move(state, move, delta);
  }
}

double default_temperature_start(int kind) {
  switch (kind & 3) {
    case 0: return 110.0;
    case 1: return 170.0;
    case 2: return 220.0;
    default: return 12000.0;
  }
}

double default_temperature_end(int kind) {
  switch (kind & 3) {
    case 0: return 0.4;
    case 1: return 0.7;
    case 2: return 0.8;
    default: return 14.0;
  }
}

WorkerResult run_worker(int worker, const Options &options,
                        const std::vector<int> &schedule,
                        Clock::time_point deadline,
                        const Candidate *initial) {
  WorkerResult result;
  const uint64_t worker_seed = splitmix64(
      options.seed + 0x9e3779b97f4a7c15ULL * static_cast<uint64_t>(worker + 1));
  std::mt19937_64 rng(worker_seed);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  const int kind = options.objective >= 0 ? options.objective : worker & 3;
  std::string mode = options.mode;
  if (mode == "auto") mode = worker % 3 == 2 ? "late" : "anneal";
  const double start_temperature = options.temperature_start > 0
      ? options.temperature_start : default_temperature_start(kind);
  const double end_temperature = options.temperature_end > 0
      ? options.temperature_end : default_temperature_end(kind);

  auto within_budget = [&]() {
    if (exact_found.load(std::memory_order_relaxed)) return false;
    if (options.iterations) return result.moves < options.iterations;
    return Clock::now() < deadline;
  };

  while (within_budget()) {
    const uint64_t job = next_job.fetch_add(1, std::memory_order_relaxed);
    const int shard = schedule[job % schedule.size()];
    const Candidate incumbent = shard_incumbent(shard);
    State state;
    if (options.preserve_endpoint_parity) {
      const Candidate &start = incumbent.initialized ? incumbent : *initial;
      state = state_from_candidate(start);
      perturb(state, rng, 12 + static_cast<int>(rng() % 37), true);
    } else if (incumbent.initialized && (job / schedule.size()) % 3 == 2) {
      state = state_from_candidate(incumbent);
      perturb(state, rng, 12 + static_cast<int>(rng() % 37), false);
    } else {
      state = random_state(shard, rng);
    }
    Candidate epoch_best = make_candidate(state, worker_seed, job);
    if (better(epoch_best, result.best)) result.best = epoch_best;
    publish(epoch_best, options.quiet);
    int64_t current_cost = search_cost(state.residual, kind);
    std::vector<int64_t> late_history(
        static_cast<size_t>(std::max(1, options.late_window)), current_cost);

    for (uint64_t step = 0; step < options.epoch && within_budget(); ++step) {
      if ((step & 4095ULL) == 0 && !options.iterations && Clock::now() >= deadline)
        break;
      const double phase = static_cast<double>(step) /
                           static_cast<double>(std::max<uint64_t>(1, options.epoch - 1));
      const double temperature = start_temperature *
          std::pow(end_temperature / start_temperature, phase);
      const Move move = options.preserve_endpoint_parity
          ? random_endpoint_preserving_move(state, rng)
          : random_move(state, rng);
      const Delta delta = correlation_delta(state, move);
      const int64_t proposed_cost = search_cost_after(state, delta, kind);
      const int64_t change = proposed_cost - current_cost;
      bool accept;
      if (mode == "late") {
        const size_t slot = static_cast<size_t>(result.moves % late_history.size());
        accept = proposed_cost <= current_cost || proposed_cost <= late_history[slot];
        late_history[slot] = current_cost;
      } else {
        accept = change <= 0 ||
                 uniform(rng) < std::exp(-static_cast<double>(change) / temperature);
      }
      ++result.moves;
      if (accept) {
        apply_move(state, move, delta);
        current_cost = proposed_cost;
        ++result.accepted;
        const Candidate candidate = make_candidate(state, worker_seed, job);
        if (better(candidate, epoch_best)) epoch_best = candidate;
        if (better(candidate, result.best)) result.best = candidate;
        publish(candidate, options.quiet);
      }
      if (options.validate_every &&
          result.moves % options.validate_every == 0) {
        validate(state);
        if (options.preserve_endpoint_parity && !endpoint_parities_hold(state))
          throw std::runtime_error("endpoint parity invariant failure");
      }
    }

    state = state_from_candidate(epoch_best);
    for (int step = 0; step < options.polish_steps && within_budget(); ++step) {
      const ImprovingMove best = options.preserve_endpoint_parity
          ? best_sampled_endpoint_improvement(
                state, rng, options.parity_polish_samples)
          : best_basic_improvement(state);
      if (!best.found) break;
      apply_move(state, best.move, best.delta);
      ++result.accepted;
      const Candidate candidate = make_candidate(state, worker_seed, job);
      if (better(candidate, result.best)) result.best = candidate;
      publish(candidate, options.quiet);
    }
    validate(state);
    if (options.preserve_endpoint_parity && !endpoint_parities_hold(state))
      throw std::runtime_error("endpoint parity invariant failure");
    ++result.restarts;
    ++result.jobs;
  }
  if (result.best.initialized) {
    State best_state = state_from_candidate(result.best);
    validate(best_state);
  }
  return result;
}

void write_sign_array(std::ostream &out, const Signs &sequence, int length) {
  out << '[';
  for (int i = 0; i < length; ++i) {
    if (i) out << ',';
    out << static_cast<int>(sequence[i]);
  }
  out << ']';
}

void write_margin(std::ostream &out, const Margin &margin) {
  out << '[';
  for (int i = 0; i < SEQUENCES; ++i) {
    if (i) out << ',';
    out << margin[i];
  }
  out << ']';
}

void write_special_s(std::ostream &out, const Candidate &candidate) {
  out << '[';
  bool first = true;
  for (int which : {0, 2}) {
    const int length = length_of(which);
    for (int i = 0; i < length; ++i) {
      if (!first) out << ',';
      first = false;
      out << static_cast<int>(candidate.sequence[which][i]);
    }
  }
  out << ']';
}

void write_special_q(std::ostream &out, const Candidate &candidate) {
  out << '[';
  bool first = true;
  for (const auto [left, right] : {std::pair{0, 1}, std::pair{2, 3}}) {
    const int length = length_of(left);
    for (int i = 0; i < length; ++i) {
      if (!first) out << ',';
      first = false;
      out << static_cast<int>(candidate.sequence[left][i] *
                              candidate.sequence[right][i]);
    }
  }
  out << ']';
}

void write_candidate(const std::string &path, const Candidate &candidate,
                     const Options &options, const std::vector<int> &schedule,
                     double elapsed, const std::vector<WorkerResult> &workers) {
  const std::filesystem::path output(path);
  if (output.has_parent_path())
    std::filesystem::create_directories(output.parent_path());
  const std::string temporary = path + ".tmp";
  std::ofstream out(temporary);
  if (!out) throw std::runtime_error("could not open output file: " + temporary);
  uint64_t moves = 0, accepted = 0, restarts = 0, jobs = 0;
  for (const auto &worker : workers) {
    moves += worker.moves;
    accepted += worker.accepted;
    restarts += worker.restarts;
    jobs += worker.jobs;
  }
  const Shard &shard = SHARDS[candidate.shard];
  out << "{\n";
  out << "  \"kind\": \"variable-q-bs-84-83-local-search-candidate\",\n";
  out << "  \"exact\": " << (candidate.metrics.energy == 0 ? "true" : "false") << ",\n";
  // C++ only certifies the base correlations.  This flag remains false even
  // at energy zero until verify_variable_q.py expands and checks H H^T.
  out << "  \"hadamard_verified\": false,\n";
  out << "  \"length\": 167,\n";
  out << "  \"hadamard_order\": 668,\n";
  out << "  \"shard\": " << candidate.shard << ",\n";
  out << "  \"ordinary_sums\": "; write_margin(out, shard.ordinary); out << ",\n";
  out << "  \"alternating_sums\": "; write_margin(out, shard.alternating); out << ",\n";
  out << "  \"base_seed\": " << options.seed << ",\n";
  out << "  \"worker_seed\": " << candidate.worker_seed << ",\n";
  out << "  \"job\": " << candidate.job << ",\n";
  out << "  \"threads\": " << options.threads << ",\n";
  out << "  \"seconds\": " << std::fixed << std::setprecision(6) << elapsed << ",\n";
  out << "  \"energy_half_base\": " << candidate.metrics.energy << ",\n";
  out << "  \"energy_base\": " << 4 * candidate.metrics.energy << ",\n";
  out << "  \"bad_lag_count\": " << candidate.metrics.nonzero << ",\n";
  out << "  \"odd_half_residual_count\": "
      << candidate.metrics.odd_residuals << ",\n";
  out << "  \"max_abs_base_residual\": " << 2 * candidate.metrics.max_abs << ",\n";
  out << "  \"l1_base_residual\": " << 2 * candidate.metrics.l1 << ",\n";
  for (int which = 0; which < SEQUENCES; ++which) {
    out << "  \"" << "abcd"[which] << "\": ";
    write_sign_array(out, candidate.sequence[which], length_of(which));
    out << ",\n";
  }
  out << "  \"s\": "; write_special_s(out, candidate); out << ",\n";
  out << "  \"q\": "; write_special_q(out, candidate); out << ",\n";
  out << "  \"base_correlations\": [334";
  for (int lag = 1; lag <= LAST_LAG; ++lag)
    out << ',' << 2 * candidate.residual[lag];
  out << "],\n";
  out << "  \"half_base_residuals_1_through_83\": [";
  for (int lag = 1; lag <= LAST_LAG; ++lag) {
    if (lag > 1) out << ',';
    out << candidate.residual[lag];
  }
  out << "],\n";
  out << "  \"search\": {\"moves\":" << moves
      << ",\"accepted\":" << accepted << ",\"restarts\":" << restarts
      << ",\"jobs\":" << jobs << ",\"scheduled_shards\":" << schedule.size()
      << ",\"epoch\":" << options.epoch
      << ",\"polish_steps\":" << options.polish_steps
      << ",\"parity_polish_samples\":" << options.parity_polish_samples
      << ",\"objective\":" << options.objective
      << ",\"mode\":\"" << options.mode << "\""
      << ",\"preserve_endpoint_parity\":"
      << (options.preserve_endpoint_parity ? "true" : "false") << "}\n";
  out << "}\n";
  out.close();
  if (std::rename(temporary.c_str(), path.c_str()) != 0)
    throw std::runtime_error("could not atomically replace output file");
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

void add_shard_token(std::vector<int> &result, const std::string &token) {
  const size_t dash = token.find('-');
  if (dash == std::string::npos) {
    result.push_back(parse_int(token, "shard"));
    return;
  }
  const int first = parse_int(token.substr(0, dash), "shard range");
  const int last = parse_int(token.substr(dash + 1), "shard range");
  if (first > last) throw std::runtime_error("descending shard range");
  for (int shard = first; shard <= last; ++shard) result.push_back(shard);
}

std::vector<int> parse_shard_spec(const std::string &specification) {
  std::vector<int> result;
  std::stringstream stream(specification);
  std::string token;
  while (std::getline(stream, token, ',')) {
    if (token.empty()) throw std::runtime_error("empty shard-list token");
    add_shard_token(result, token);
  }
  std::sort(result.begin(), result.end());
  result.erase(std::unique(result.begin(), result.end()), result.end());
  for (int shard : result)
    if (shard < 0 || shard >= static_cast<int>(SHARDS.size()))
      throw std::runtime_error("shard must be in 0..287");
  if (result.empty()) throw std::runtime_error("empty shard schedule");
  return result;
}

int global_alternation_partner(int shard_index) {
  Margin ordinary = SHARDS[shard_index].alternating;
  Margin alternating = SHARDS[shard_index].ordinary;
  for (int which = 0; which < SEQUENCES; ++which) {
    if (ordinary[which] < 0) {
      ordinary[which] = -ordinary[which];
      alternating[which] = -alternating[which];
    }
  }
  for (int which : {0, 1})
    if (alternating[which] < 0)
      alternating[which] = -alternating[which];
  for (const auto [left, right] : {std::pair{0, 1}, std::pair{2, 3}}) {
    if (ordinary[left] < ordinary[right]) {
      std::swap(ordinary[left], ordinary[right]);
      std::swap(alternating[left], alternating[right]);
    }
  }
  for (int candidate = 0; candidate < static_cast<int>(SHARDS.size()); ++candidate)
    if (SHARDS[candidate].ordinary == ordinary &&
        SHARDS[candidate].alternating == alternating)
      return candidate;
  throw std::runtime_error("global alternation produced an unknown shard");
}

std::vector<int> make_schedule(const Options &options) {
  std::vector<int> result;
  if (!options.shard_spec.empty())
    result = parse_shard_spec(options.shard_spec);
  else {
    // Coordinate alternation x_i -> (-1)^i*x_i pairs 264 normalized margin
    // shards and fixes 24.  Search one representative from each orbit.
    for (int shard = 0; shard < static_cast<int>(SHARDS.size()); ++shard)
      if (shard <= global_alternation_partner(shard))
        result.push_back(shard);
    if (result.size() != 156)
      throw std::runtime_error("global alternation representative failure");
  }
  if (options.sample_shards > 0) {
    if (options.sample_shards > static_cast<int>(result.size()))
      throw std::runtime_error("sample-shards exceeds selected shard count");
    std::mt19937_64 rng(splitmix64(options.seed ^ 0x425338343833ULL));
    std::shuffle(result.begin(), result.end(), rng);
    result.resize(options.sample_shards);
  }
  return result;
}

void usage(const char *program) {
  std::cerr << "Usage: " << program << " [options]\n"
      "  --seconds N              wall-clock budget (default 30)\n"
      "  --iterations N           move budget per worker; overrides wall clock\n"
      "  --threads N              parallel workers\n"
      "  --seed N                 deterministic base seed\n"
      "  --shard N                select one shard\n"
      "  --shards LIST            comma/range list, e.g. 0,96,192,280-287\n"
      "  --sample-shards N        deterministically sample from selected shards\n"
      "  --epoch N                moves before the next scheduled shard\n"
      "  --polish-steps N         exact best-swap steps at epoch end\n"
      "  --parity-polish-samples N  sampled paired moves per polish step\n"
      "  --objective -1..3        -1 diversifies unique-zero objectives\n"
      "  --mode auto|anneal|late  acceptance scheme\n"
      "  --temperature-start N    annealing start temperature\n"
      "  --temperature-end N      annealing end temperature\n"
      "  --late-window N          late-acceptance history size\n"
      "  --validate-every N       full incremental-state check interval\n"
      "  --initial PATH           start from a,b,c,d candidate JSON\n"
      "  --preserve-endpoint-parity  use only paired-syndrome moves\n"
      "  --output PATH            checkpoint JSON\n"
      "  --list-shards            print the exact 288-shard enumeration\n"
      "  --quiet                   suppress progress\n";
}

Options parse_options(int argc, char **argv) {
  Options options;
  options.threads = std::max(1u, std::thread::hardware_concurrency());
  auto value = [&](int &index) -> std::string {
    if (++index >= argc) throw std::runtime_error("missing option value");
    return argv[index];
  };
  for (int i = 1; i < argc; ++i) {
    const std::string argument = argv[i];
    if (argument == "--seconds")
      options.seconds = parse_double(value(i), "seconds");
    else if (argument == "--iterations")
      options.iterations = parse_u64(value(i), "iterations");
    else if (argument == "--threads")
      options.threads = parse_int(value(i), "threads");
    else if (argument == "--seed")
      options.seed = parse_u64(value(i), "seed");
    else if (argument == "--shard")
      options.shard_spec = value(i);
    else if (argument == "--shards")
      options.shard_spec = value(i);
    else if (argument == "--sample-shards")
      options.sample_shards = parse_int(value(i), "sample-shards");
    else if (argument == "--epoch")
      options.epoch = parse_u64(value(i), "epoch");
    else if (argument == "--polish-steps")
      options.polish_steps = parse_int(value(i), "polish-steps");
    else if (argument == "--parity-polish-samples")
      options.parity_polish_samples =
          parse_int(value(i), "parity-polish-samples");
    else if (argument == "--objective")
      options.objective = parse_int(value(i), "objective");
    else if (argument == "--mode")
      options.mode = value(i);
    else if (argument == "--temperature-start")
      options.temperature_start = parse_double(value(i), "temperature-start");
    else if (argument == "--temperature-end")
      options.temperature_end = parse_double(value(i), "temperature-end");
    else if (argument == "--late-window")
      options.late_window = parse_int(value(i), "late-window");
    else if (argument == "--validate-every")
      options.validate_every = parse_u64(value(i), "validate-every");
    else if (argument == "--initial")
      options.initial = value(i);
    else if (argument == "--preserve-endpoint-parity")
      options.preserve_endpoint_parity = true;
    else if (argument == "--output")
      options.output = value(i);
    else if (argument == "--quiet")
      options.quiet = true;
    else if (argument == "--list-shards")
      options.list_shards = true;
    else if (argument == "--help" || argument == "-h") {
      usage(argv[0]);
      std::exit(0);
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  if (options.seconds <= 0 || options.threads <= 0 || options.epoch == 0 ||
      options.polish_steps < 0 || options.late_window <= 0 ||
      options.parity_polish_samples < 0 || options.sample_shards < 0)
    throw std::runtime_error("invalid nonpositive numeric option");
  if (options.objective < -1 || options.objective > 3)
    throw std::runtime_error("objective must be -1, 0, 1, 2, or 3");
  if (options.mode != "auto" && options.mode != "anneal" &&
      options.mode != "late")
    throw std::runtime_error("mode must be auto, anneal, or late");
  return options;
}

void print_margin(const Margin &margin) {
  std::cout << '(' << margin[0] << ',' << margin[1] << ','
            << margin[2] << ',' << margin[3] << ')';
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    if (options.list_shards) {
      for (size_t index = 0; index < SHARDS.size(); ++index) {
        std::cout << index << " ordinary=";
        print_margin(SHARDS[index].ordinary);
        std::cout << " alternating=";
        print_margin(SHARDS[index].alternating);
        std::cout << '\n';
      }
      return 0;
    }
    const std::vector<int> schedule = make_schedule(options);
    Candidate initial;
    const Candidate *initial_pointer = nullptr;
    if (!options.initial.empty()) {
      initial = load_initial_candidate(options.initial);
      initial_pointer = &initial;
      if (std::find(schedule.begin(), schedule.end(), initial.shard) ==
          schedule.end())
        throw std::runtime_error("initial candidate shard is not scheduled");
      // Record the exact checkpoint before any worker perturbs it.  This
      // makes continuation monotone even for a one-move or expired budget.
      publish(initial, options.quiet);
    }
    if (options.preserve_endpoint_parity) {
      if (!initial_pointer)
        throw std::runtime_error(
            "--preserve-endpoint-parity requires --initial");
      if (!endpoint_parities_hold(state_from_candidate(initial)))
        throw std::runtime_error("initial state violates endpoint parities");
      if (schedule.size() != 1 || schedule.front() != initial.shard)
        throw std::runtime_error(
            "parity-preserving search schedule must equal the initial shard");
    }
    const auto start = Clock::now();
    const auto deadline = start + std::chrono::duration_cast<Clock::duration>(
        std::chrono::duration<double>(options.seconds));
    std::vector<WorkerResult> workers(options.threads);
    std::vector<std::thread> threads;
    threads.reserve(options.threads);
    for (int worker = 0; worker < options.threads; ++worker) {
      threads.emplace_back([&, worker] {
        workers[worker] =
            run_worker(worker, options, schedule, deadline, initial_pointer);
      });
    }
    for (auto &thread : threads) thread.join();
    const double elapsed =
        std::chrono::duration<double>(Clock::now() - start).count();

    Candidate winner;
    for (const auto &worker : workers)
      if (better(worker.best, winner)) winner = worker.best;
    {
      std::lock_guard<std::mutex> lock(best_mutex);
      if (better(global_best, winner)) winner = global_best;
    }
    if (!winner.initialized) throw std::runtime_error("search produced no state");
    State exact = state_from_candidate(winner);
    validate(exact);
    write_candidate(options.output, winner, options, schedule, elapsed, workers);

    uint64_t moves = 0, accepted = 0, restarts = 0, jobs = 0;
    for (const auto &worker : workers) {
      moves += worker.moves;
      accepted += worker.accepted;
      restarts += worker.restarts;
      jobs += worker.jobs;
    }
    if (!options.quiet) {
      std::cout << "shard=" << winner.shard
                << " energy_half=" << winner.metrics.energy
                << " energy_base=" << 4 * winner.metrics.energy
                << " nonzero=" << winner.metrics.nonzero
                << " max_abs_base=" << 2 * winner.metrics.max_abs
                << " l1_base=" << 2 * winner.metrics.l1 << '\n';
      std::cout << "elapsed=" << std::fixed << std::setprecision(3) << elapsed
                << " moves=" << moves << " accepted=" << accepted
                << " restarts=" << restarts << " jobs=" << jobs
                << " scheduled_shards=" << schedule.size() << '\n';
      std::cout << "output=" << options.output << '\n';
    }
    return winner.metrics.energy == 0 ? 0 : 2;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
