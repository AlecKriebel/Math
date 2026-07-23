// Structured local constructor for the prime-83 oriented endpoint fold.
//
// Unlike a BS(84,83) aperiodic sign search, this engine stays inside one of
// the 45 exact row-sum profiles and enforces the X/Y inverse-pair parity law
// after every move.  The 41 periodic residuals are updated in O(41) per
// changed coordinate.  Near states are resumable; an energy-zero state is
// emitted in the strict certificate format consumed by
// verify_bs84_oriented_sds.py.

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
#include <iterator>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <string_view>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace {

constexpr int P = 83;
constexpr int HALF = 41;
constexpr int BLOCKS = 4;
constexpr int ENERGY = 334;
constexpr int MAX_FLIPS = 8;

using Sequence = std::array<std::int8_t, P>;
using Quadruple = std::array<Sequence, BLOCKS>;
using Residuals = std::array<int, HALF + 1>;
using Profile = std::array<int, BLOCKS>;

constexpr std::array<std::array<int, 4>, 8> PAIR_BITS{{
    {{0, 0, 0, 0}},
    {{0, 0, 1, 1}},
    {{0, 1, 0, 1}},
    {{0, 1, 1, 0}},
    {{1, 0, 0, 1}},
    {{1, 0, 1, 0}},
    {{1, 1, 0, 0}},
    {{1, 1, 1, 1}},
}};

struct State {
  Quadruple sequence{};
  std::array<std::uint8_t, HALF> pair_state{};
  Residuals residual{};
  std::int64_t energy = 0;
  int profile_index = -1;
  std::uint64_t recorded_moves = 0;
  bool regular_polish_completed = false;
  std::uint64_t regular_xy_moves = 0;
  std::uint64_t regular_c_moves = 0;
  std::uint64_t regular_d_moves = 0;
  bool deep_polish_completed = false;
  std::uint64_t deep_c_double_moves = 0;
  std::uint64_t deep_d_double_moves = 0;
  std::uint64_t deep_xy_triple_moves = 0;
};

struct Move {
  std::array<std::array<int, MAX_FLIPS>, BLOCKS> flips{};
  std::array<int, BLOCKS> flip_count{};
  std::array<int, 3> pair_index{{-1, -1, -1}};
  std::array<int, 3> new_pair_state{{-1, -1, -1}};
  int pair_count = 0;
  Residuals delta{};
  std::int64_t new_energy = 0;
};

struct Options {
  double seconds = 60.0;
  std::uint64_t seed = 668083;
  int profile = 20;
  std::uint64_t moves_per_restart = 1'000'000;
  double start_temperature = 40.0;
  double end_temperature = 0.05;
  std::uint64_t validate_every = 1'000'000;
  double report_every = 10.0;
  int polish_pool = 512;
  int polish_steps = 12;
  bool deep_polish = false;
  std::filesystem::path output =
      "output/bs84_oriented_sds_local_best.json";
  std::filesystem::path initial;
  bool self_test = false;
};

int wrap(int value) {
  if (value >= P) return value - P;
  if (value < 0) return value + P;
  return value;
}

std::vector<Profile> profiles() {
  std::vector<Profile> result;
  for (int x = 0; x <= HALF; ++x) {
    for (int y = 0; y < P; ++y) {
      for (int z = 0; z <= HALF; ++z) {
        for (int w = z; w <= HALF; ++w) {
          const std::array<int, 4> sums{
              82 - 2 * x, 84 - 2 * y, 83 - 2 * z, 83 - 2 * w};
          int square_sum = 0;
          for (int value : sums) square_sum += value * value;
          if (square_sum == ENERGY) result.push_back({{x, y, z, w}});
        }
      }
    }
  }
  if (result.size() != 45)
    throw std::runtime_error("anchored profile count is not 45");
  return result;
}

int periodic(const Sequence &sequence, int lag) {
  int result = 0;
  for (int index = 0; index < P; ++index)
    result += sequence[index] * sequence[wrap(index + lag)];
  return result;
}

Residuals full_residual(const Quadruple &quadruple) {
  Residuals result{};
  result[0] = 0;
  for (const Sequence &sequence : quadruple)
    for (std::int8_t value : sequence) result[0] += value * value;
  for (int lag = 1; lag <= HALF; ++lag)
    for (const Sequence &sequence : quadruple)
      result[lag] += periodic(sequence, lag);
  return result;
}

std::int64_t residual_energy(const Residuals &residual) {
  std::int64_t result = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    if (residual[lag] % 4 != 0)
      throw std::runtime_error("oriented residual is not divisible by four");
    const std::int64_t value = residual[lag] / 4;
    result += value * value;
  }
  return result;
}

int bad_lags(const State &state) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result += state.residual[lag] != 0;
  return result;
}

int maximum_quarter_residual(const State &state) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result = std::max(result, std::abs(state.residual[lag] / 4));
  return result;
}

std::array<int, 2> pair_counts(int state) {
  return {{PAIR_BITS[state][0] + PAIR_BITS[state][1],
           PAIR_BITS[state][2] + PAIR_BITS[state][3]}};
}

void validate(const State &state) {
  const std::vector<Profile> all_profiles = profiles();
  if (state.profile_index < 0 ||
      state.profile_index >= static_cast<int>(all_profiles.size()))
    throw std::runtime_error("profile index is invalid");
  const Profile expected = all_profiles[state.profile_index];
  if (state.sequence[0][0] != 0 || state.sequence[1][0] != 2)
    throw std::runtime_error("anomalous coordinates changed");
  int negative[BLOCKS]{};
  for (int which = 0; which < BLOCKS; ++which) {
    for (int index = 0; index < P; ++index) {
      const int value = state.sequence[which][index];
      if (which == 0 && index == 0) {
        if (value != 0) throw std::runtime_error("U[0] is not zero");
      } else if (which == 1 && index == 0) {
        if (value != 2) throw std::runtime_error("V[0] is not two");
      } else if (value != -1 && value != 1) {
        throw std::runtime_error("a non-anomalous entry is not binary");
      }
      if (value == -1) ++negative[which];
    }
  }
  for (int which = 0; which < BLOCKS; ++which)
    if (negative[which] != expected[which])
      throw std::runtime_error("a block size changed");
  for (int pair = 0; pair < HALF; ++pair) {
    const int lag = pair + 1;
    const int inverse = P - lag;
    const int pair_state = state.pair_state[pair];
    if (pair_state < 0 || pair_state >= 8)
      throw std::runtime_error("pair state is invalid");
    const auto &bits = PAIR_BITS[pair_state];
    if ((state.sequence[0][lag] == -1) != static_cast<bool>(bits[0]) ||
        (state.sequence[0][inverse] == -1) != static_cast<bool>(bits[1]) ||
        (state.sequence[1][lag] == -1) != static_cast<bool>(bits[2]) ||
        (state.sequence[1][inverse] == -1) != static_cast<bool>(bits[3]))
      throw std::runtime_error("pair state disagrees with X/Y sequences");
  }
  const Residuals expected_residual = full_residual(state.sequence);
  if (expected_residual != state.residual)
    throw std::runtime_error("incremental residual mismatch");
  if (state.residual[0] != ENERGY)
    throw std::runtime_error("folded energy is not 334");
  if (residual_energy(state.residual) != state.energy)
    throw std::runtime_error("incremental energy mismatch");
}

State random_state(int profile_index, std::mt19937_64 &rng) {
  const std::vector<Profile> all_profiles = profiles();
  if (profile_index < 0 ||
      profile_index >= static_cast<int>(all_profiles.size()))
    throw std::runtime_error("profile index lies outside 0..44");
  const Profile target = all_profiles[profile_index];

  // possible[r][x][y] says whether r inverse pairs can supply x X-entries
  // and y Y-entries.  Boolean feasibility is enough for randomized sampling.
  using Plane = std::array<std::array<std::uint8_t, P>, P>;
  std::array<Plane, HALF + 1> possible{};
  possible[0][0][0] = 1;
  for (int remaining = 1; remaining <= HALF; ++remaining) {
    for (int x = 0; x < P; ++x) {
      for (int y = 0; y < P; ++y) {
        for (int pair_state = 0; pair_state < 8; ++pair_state) {
          const auto counts = pair_counts(pair_state);
          if (x >= counts[0] && y >= counts[1] &&
              possible[remaining - 1][x - counts[0]][y - counts[1]]) {
            possible[remaining][x][y] = 1;
            break;
          }
        }
      }
    }
  }
  if (!possible[HALF][target[0]][target[1]])
    throw std::runtime_error("profile has no inverse-pair realization");

  State state;
  state.profile_index = profile_index;
  state.sequence[0].fill(1);
  state.sequence[1].fill(1);
  state.sequence[2].fill(1);
  state.sequence[3].fill(1);
  state.sequence[0][0] = 0;
  state.sequence[1][0] = 2;
  int x_left = target[0];
  int y_left = target[1];
  for (int pair = 0; pair < HALF; ++pair) {
    const int remaining = HALF - pair - 1;
    std::array<int, 8> choices{};
    int choice_count = 0;
    for (int pair_state = 0; pair_state < 8; ++pair_state) {
      const auto counts = pair_counts(pair_state);
      if (x_left >= counts[0] && y_left >= counts[1] &&
          possible[remaining][x_left - counts[0]][y_left - counts[1]])
        choices[choice_count++] = pair_state;
    }
    std::uniform_int_distribution<int> choose(0, choice_count - 1);
    const int selected = choices[choose(rng)];
    state.pair_state[pair] = static_cast<std::uint8_t>(selected);
    const int lag = pair + 1;
    const int inverse = P - lag;
    const auto &bits = PAIR_BITS[selected];
    state.sequence[0][lag] = bits[0] ? -1 : 1;
    state.sequence[0][inverse] = bits[1] ? -1 : 1;
    state.sequence[1][lag] = bits[2] ? -1 : 1;
    state.sequence[1][inverse] = bits[3] ? -1 : 1;
    const auto counts = pair_counts(selected);
    x_left -= counts[0];
    y_left -= counts[1];
  }
  if (x_left != 0 || y_left != 0)
    throw std::runtime_error("inverse-pair sampler missed target sizes");

  std::array<int, P> order{};
  for (int index = 0; index < P; ++index) order[index] = index;
  for (int which = 2; which < 4; ++which) {
    std::shuffle(order.begin(), order.end(), rng);
    for (int count = 0; count < target[which]; ++count)
      state.sequence[which][order[count]] = -1;
  }
  state.residual = full_residual(state.sequence);
  state.energy = residual_energy(state.residual);
  validate(state);
  return state;
}

bool contains_flip(const Move &move, int which, int position) {
  for (int index = 0; index < move.flip_count[which]; ++index)
    if (move.flips[which][index] == position) return true;
  return false;
}

void add_flip(Move &move, int which, int position) {
  if (contains_flip(move, which, position)) return;
  int &count = move.flip_count[which];
  if (count >= MAX_FLIPS)
    throw std::runtime_error("move exceeded the flip buffer");
  move.flips[which][count++] = position;
}

void add_pair_change(Move &move, const State &state, int pair,
                     int new_state) {
  if (move.pair_count >= 3)
    throw std::runtime_error("move exceeded the pair-update buffer");
  const int old_state = state.pair_state[pair];
  move.pair_index[move.pair_count] = pair;
  move.new_pair_state[move.pair_count] = new_state;
  ++move.pair_count;
  const int lag = pair + 1;
  const int inverse = P - lag;
  for (int bit = 0; bit < 4; ++bit) {
    if (PAIR_BITS[old_state][bit] == PAIR_BITS[new_state][bit]) continue;
    const int which = bit < 2 ? 0 : 1;
    const int position = bit % 2 == 0 ? lag : inverse;
    add_flip(move, which, position);
  }
}

bool propose_pair_move(Move &move, const State &state,
                       std::mt19937_64 &rng) {
  std::uniform_int_distribution<int> pair_distribution(0, HALF - 1);
  std::bernoulli_distribution single_move(0.35);
  if (single_move(rng)) {
    const int pair = pair_distribution(rng);
    const int old_state = state.pair_state[pair];
    const auto old_counts = pair_counts(old_state);
    std::array<int, 8> choices{};
    int count = 0;
    for (int candidate = 0; candidate < 8; ++candidate)
      if (candidate != old_state && pair_counts(candidate) == old_counts)
        choices[count++] = candidate;
    if (count == 0) return false;
    std::uniform_int_distribution<int> choose(0, count - 1);
    add_pair_change(move, state, pair, choices[choose(rng)]);
    return true;
  }

  int first = pair_distribution(rng);
  int second = pair_distribution(rng);
  while (second == first) second = pair_distribution(rng);
  const int old_first = state.pair_state[first];
  const int old_second = state.pair_state[second];
  const auto first_counts = pair_counts(old_first);
  const auto second_counts = pair_counts(old_second);
  const std::array<int, 2> target{
      {first_counts[0] + second_counts[0],
       first_counts[1] + second_counts[1]}};
  std::array<std::array<int, 2>, 64> choices{};
  int count = 0;
  for (int new_first = 0; new_first < 8; ++new_first) {
    for (int new_second = 0; new_second < 8; ++new_second) {
      const auto new_first_counts = pair_counts(new_first);
      const auto new_second_counts = pair_counts(new_second);
      if (new_first_counts[0] + new_second_counts[0] != target[0] ||
          new_first_counts[1] + new_second_counts[1] != target[1])
        continue;
      if (new_first == old_first && new_second == old_second) continue;
      choices[count++] = {{new_first, new_second}};
    }
  }
  if (count == 0) return false;
  std::uniform_int_distribution<int> choose(0, count - 1);
  const auto selected = choices[choose(rng)];
  add_pair_change(move, state, first, selected[0]);
  add_pair_change(move, state, second, selected[1]);
  return true;
}

void add_exchange(Move &move, const State &state, int which,
                  std::mt19937_64 &rng) {
  std::uniform_int_distribution<int> position(0, P - 1);
  int first = position(rng);
  int second = position(rng);
  while (state.sequence[which][second] == state.sequence[which][first])
    second = position(rng);
  add_flip(move, which, first);
  add_flip(move, which, second);
}

void compute_delta(const State &state, Move &move) {
  move.delta.fill(0);
  for (int which = 0; which < BLOCKS; ++which) {
    const Sequence &sequence = state.sequence[which];
    for (int flip_index = 0; flip_index < move.flip_count[which];
         ++flip_index) {
      const int position = move.flips[which][flip_index];
      for (int lag = 1; lag <= HALF; ++lag) {
        const int forward = wrap(position + lag);
        const int backward = wrap(position - lag);
        if (!contains_flip(move, which, forward))
          move.delta[lag] -=
              2 * sequence[position] * sequence[forward];
        if (!contains_flip(move, which, backward))
          move.delta[lag] -=
              2 * sequence[position] * sequence[backward];
      }
    }
  }
  move.new_energy = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    const int updated = state.residual[lag] + move.delta[lag];
    if (updated % 4 != 0)
      throw std::runtime_error("a move broke oriented divisibility");
    const std::int64_t quarter = updated / 4;
    move.new_energy += quarter * quarter;
  }
}

Move propose_move(const State &state, std::mt19937_64 &rng) {
  std::uniform_int_distribution<int> kind_distribution(0, 6);
  for (;;) {
    Move move;
    const int kind = kind_distribution(rng);
    bool valid = true;
    if (kind == 0 || kind == 3 || kind == 4 || kind == 6)
      valid = propose_pair_move(move, state, rng);
    if (!valid) continue;
    if (kind == 1 || kind == 3 || kind == 5 || kind == 6)
      add_exchange(move, state, 2, rng);
    if (kind == 2 || kind == 4 || kind == 5 || kind == 6)
      add_exchange(move, state, 3, rng);
    compute_delta(state, move);
    return move;
  }
}

void apply_move(State &state, const Move &move) {
  for (int which = 0; which < BLOCKS; ++which)
    for (int index = 0; index < move.flip_count[which]; ++index)
      state.sequence[which][move.flips[which][index]] *= -1;
  for (int index = 0; index < move.pair_count; ++index)
    state.pair_state[move.pair_index[index]] =
        static_cast<std::uint8_t>(move.new_pair_state[index]);
  for (int lag = 1; lag <= HALF; ++lag)
    state.residual[lag] += move.delta[lag];
  state.energy = move.new_energy;
}

std::vector<Move> xy_moves(const State &state) {
  std::vector<Move> result(1);  // Include the identity move.
  result[0].new_energy = state.energy;
  for (int pair = 0; pair < HALF; ++pair) {
    const int old_state = state.pair_state[pair];
    const auto old_counts = pair_counts(old_state);
    for (int candidate = 0; candidate < 8; ++candidate) {
      if (candidate == old_state || pair_counts(candidate) != old_counts)
        continue;
      Move move;
      add_pair_change(move, state, pair, candidate);
      compute_delta(state, move);
      result.push_back(move);
    }
  }
  for (int first = 0; first < HALF; ++first) {
    for (int second = first + 1; second < HALF; ++second) {
      const int old_first = state.pair_state[first];
      const int old_second = state.pair_state[second];
      const auto first_counts = pair_counts(old_first);
      const auto second_counts = pair_counts(old_second);
      const std::array<int, 2> target{{
          first_counts[0] + second_counts[0],
          first_counts[1] + second_counts[1],
      }};
      for (int new_first = 0; new_first < 8; ++new_first) {
        for (int new_second = 0; new_second < 8; ++new_second) {
          if (new_first == old_first && new_second == old_second) continue;
          const auto new_first_counts = pair_counts(new_first);
          const auto new_second_counts = pair_counts(new_second);
          if (new_first_counts[0] + new_second_counts[0] != target[0] ||
              new_first_counts[1] + new_second_counts[1] != target[1])
            continue;
          Move move;
          add_pair_change(move, state, first, new_first);
          add_pair_change(move, state, second, new_second);
          compute_delta(state, move);
          result.push_back(move);
        }
      }
    }
  }
  return result;
}

std::vector<Move> exchange_moves(const State &state, int which) {
  std::vector<Move> result(1);  // Include the identity move.
  result[0].new_energy = state.energy;
  for (int left = 0; left < P; ++left) {
    for (int right = left + 1; right < P; ++right) {
      if (state.sequence[which][left] == state.sequence[which][right]) continue;
      Move move;
      add_flip(move, which, left);
      add_flip(move, which, right);
      compute_delta(state, move);
      result.push_back(move);
    }
  }
  return result;
}

Move combine_disjoint(const State &state, const Move &xy, const Move &c,
                      const Move &d) {
  Move result;
  for (const Move *source : {&xy, &c, &d}) {
    for (int which = 0; which < BLOCKS; ++which)
      for (int index = 0; index < source->flip_count[which]; ++index)
        add_flip(result, which, source->flips[which][index]);
    for (int index = 0; index < source->pair_count; ++index) {
      result.pair_index[result.pair_count] = source->pair_index[index];
      result.new_pair_state[result.pair_count] =
          source->new_pair_state[index];
      ++result.pair_count;
    }
    for (int lag = 1; lag <= HALF; ++lag)
      result.delta[lag] += source->delta[lag];
  }
  result.new_energy = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    const std::int64_t value =
        (state.residual[lag] + result.delta[lag]) / 4;
    result.new_energy += value * value;
  }
  return result;
}

std::uint64_t mix64(std::uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

struct Fingerprint {
  std::uint64_t first = 0;
  std::uint64_t second = 0;
  bool operator==(const Fingerprint &other) const {
    return first == other.first && second == other.second;
  }
};

struct FingerprintHash {
  std::size_t operator()(const Fingerprint &value) const {
    return static_cast<std::size_t>(
        value.first ^ (value.second + 0x9e3779b97f4a7c15ULL +
                       (value.first << 6) + (value.first >> 2)));
  }
};

Fingerprint fingerprint(const Residuals &values) {
  Fingerprint result;
  for (int lag = 1; lag <= HALF; ++lag) {
    const std::uint64_t coefficient =
        static_cast<std::uint64_t>(static_cast<std::int64_t>(values[lag]));
    result.first += mix64(static_cast<std::uint64_t>(lag)) * coefficient;
    result.second +=
        mix64(static_cast<std::uint64_t>(lag) + 0x668083ULL) * coefficient;
  }
  return result;
}

Fingerprint subtract(Fingerprint left, const Fingerprint &right) {
  left.first -= right.first;
  left.second -= right.second;
  return left;
}

bool exact_triple_polish(State &state, const std::vector<Move> &xy,
                         const std::vector<Move> &c,
                         const std::vector<Move> &d) {
  std::vector<Fingerprint> xy_fingerprints;
  std::vector<Fingerprint> c_fingerprints;
  xy_fingerprints.reserve(xy.size());
  c_fingerprints.reserve(c.size());
  for (const Move &move : xy)
    xy_fingerprints.push_back(fingerprint(move.delta));
  for (const Move &move : c)
    c_fingerprints.push_back(fingerprint(move.delta));
  std::unordered_multimap<Fingerprint, std::size_t, FingerprintHash> d_table;
  d_table.reserve(d.size() * 2);
  for (std::size_t index = 0; index < d.size(); ++index)
    d_table.emplace(fingerprint(d[index].delta), index);
  Residuals negative_residual{};
  for (int lag = 1; lag <= HALF; ++lag)
    negative_residual[lag] = -state.residual[lag];
  const Fingerprint target = fingerprint(negative_residual);
  for (std::size_t xy_index = 0; xy_index < xy.size(); ++xy_index) {
    const Move &xy_move = xy[xy_index];
    const Fingerprint after_xy =
        subtract(target, xy_fingerprints[xy_index]);
    for (std::size_t c_index = 0; c_index < c.size(); ++c_index) {
      const Move &c_move = c[c_index];
      const Fingerprint needed =
          subtract(after_xy, c_fingerprints[c_index]);
      const auto range = d_table.equal_range(needed);
      for (auto iterator = range.first; iterator != range.second; ++iterator) {
        const Move &d_move = d[iterator->second];
        bool exact = true;
        for (int lag = 1; lag <= HALF; ++lag)
          if (state.residual[lag] + xy_move.delta[lag] +
                  c_move.delta[lag] + d_move.delta[lag] !=
              0) {
            exact = false;
            break;
          }
        if (!exact) continue;
        const Move combined =
            combine_disjoint(state, xy_move, c_move, d_move);
        if (combined.new_energy != 0)
          throw std::runtime_error("exact triple hash produced nonzero energy");
        apply_move(state, combined);
        validate(state);
        return true;
      }
    }
  }
  return false;
}

std::vector<Move> double_exchange_moves(const State &state, int which) {
  std::vector<int> negative;
  std::vector<int> positive;
  for (int index = 0; index < P; ++index) {
    if (state.sequence[which][index] == -1)
      negative.push_back(index);
    else
      positive.push_back(index);
  }
  const std::size_t expected =
      1 + negative.size() * (negative.size() - 1) / 2 *
              positive.size() * (positive.size() - 1) / 2;
  std::vector<Move> result;
  result.reserve(expected);
  result.emplace_back();
  result[0].new_energy = state.energy;
  for (std::size_t first_negative = 0; first_negative < negative.size();
       ++first_negative) {
    for (std::size_t second_negative = first_negative + 1;
         second_negative < negative.size(); ++second_negative) {
      for (std::size_t first_positive = 0; first_positive < positive.size();
           ++first_positive) {
        for (std::size_t second_positive = first_positive + 1;
             second_positive < positive.size(); ++second_positive) {
          Move move;
          add_flip(move, which, negative[first_negative]);
          add_flip(move, which, negative[second_negative]);
          add_flip(move, which, positive[first_positive]);
          add_flip(move, which, positive[second_positive]);
          compute_delta(state, move);
          result.push_back(move);
        }
      }
    }
  }
  if (result.size() != expected)
    throw std::runtime_error("double-exchange enumeration count mismatch");
  return result;
}

std::vector<Move> xy_triple_moves(const State &state) {
  std::vector<Move> result(1);
  result[0].new_energy = state.energy;
  for (int first = 0; first < HALF; ++first) {
    for (int second = first + 1; second < HALF; ++second) {
      for (int third = second + 1; third < HALF; ++third) {
        const std::array<int, 3> old{{
            state.pair_state[first],
            state.pair_state[second],
            state.pair_state[third],
        }};
        std::array<int, 2> target{};
        for (int old_state : old) {
          const auto counts = pair_counts(old_state);
          target[0] += counts[0];
          target[1] += counts[1];
        }
        for (int new_first = 0; new_first < 8; ++new_first) {
          for (int new_second = 0; new_second < 8; ++new_second) {
            for (int new_third = 0; new_third < 8; ++new_third) {
              if (new_first == old[0] && new_second == old[1] &&
                  new_third == old[2])
                continue;
              const auto first_counts = pair_counts(new_first);
              const auto second_counts = pair_counts(new_second);
              const auto third_counts = pair_counts(new_third);
              if (first_counts[0] + second_counts[0] + third_counts[0] !=
                      target[0] ||
                  first_counts[1] + second_counts[1] + third_counts[1] !=
                      target[1])
                continue;
              Move move;
              add_pair_change(move, state, first, new_first);
              add_pair_change(move, state, second, new_second);
              add_pair_change(move, state, third, new_third);
              compute_delta(state, move);
              result.push_back(move);
            }
          }
        }
      }
    }
  }
  return result;
}

bool deep_exact_polish(State &state) {
  state.deep_polish_completed = false;
  state.deep_c_double_moves = 0;
  state.deep_d_double_moves = 0;
  state.deep_xy_triple_moves = 0;
  const std::vector<Move> xy = xy_moves(state);
  const std::vector<Move> c_single = exchange_moves(state, 2);
  const std::vector<Move> d_single = exchange_moves(state, 3);
  std::cout << "deep_polish=building_c_double\n";
  std::vector<Move> c_double = double_exchange_moves(state, 2);
  state.deep_c_double_moves = c_double.size();
  std::cout << "deep_polish_c_double_moves=" << c_double.size() << '\n';
  // Put the large double-exchange family in the hash table (the third
  // argument), leaving only |XY|*|D1| probes.
  if (exact_triple_polish(state, xy, d_single, c_double)) return true;
  std::cout << "deep_polish=building_d_double\n";
  std::vector<Move> d_double = double_exchange_moves(state, 3);
  state.deep_d_double_moves = d_double.size();
  std::cout << "deep_polish_d_double_moves=" << d_double.size() << '\n';
  if (exact_triple_polish(state, xy, c_single, d_double)) return true;
  const std::vector<Move> identity(1);
  if (exact_triple_polish(state, identity, c_double, d_double)) return true;
  c_double.clear();
  c_double.shrink_to_fit();
  d_double.clear();
  d_double.shrink_to_fit();
  std::cout << "deep_polish=building_xy_triple\n";
  const std::vector<Move> xy_triple = xy_triple_moves(state);
  state.deep_xy_triple_moves = xy_triple.size();
  std::cout << "deep_polish_xy_triple_moves=" << xy_triple.size() << '\n';
  // Hash the large XY family and probe it with all C1/D1 combinations.
  if (exact_triple_polish(state, c_single, d_single, xy_triple)) return true;
  state.deep_polish_completed = true;
  return false;
}

std::vector<const Move *> best_pool(const std::vector<Move> &moves,
                                    int limit) {
  std::vector<const Move *> result;
  result.reserve(moves.size());
  for (const Move &move : moves) result.push_back(&move);
  std::sort(result.begin(), result.end(), [](const Move *left,
                                             const Move *right) {
    return left->new_energy < right->new_energy;
  });
  if (result.size() > static_cast<std::size_t>(limit))
    result.resize(static_cast<std::size_t>(limit));
  return result;
}

bool pooled_pair_descent(State &state, const std::vector<Move> &xy,
                         const std::vector<Move> &c,
                         const std::vector<Move> &d, int pool_size) {
  const auto xy_pool = best_pool(xy, pool_size);
  const auto c_pool = best_pool(c, pool_size);
  const auto d_pool = best_pool(d, pool_size);
  Move best;
  best.new_energy = state.energy;
  const auto scan = [&](const std::vector<const Move *> &left,
                        const std::vector<const Move *> &right,
                        int left_family, int right_family) {
    for (const Move *left_move : left) {
      for (const Move *right_move : right) {
        const Move zero;
        const Move &xy_move =
            left_family == 0 ? *left_move
                             : (right_family == 0 ? *right_move : zero);
        const Move &c_move =
            left_family == 1 ? *left_move
                             : (right_family == 1 ? *right_move : zero);
        const Move &d_move =
            left_family == 2 ? *left_move
                             : (right_family == 2 ? *right_move : zero);
        Move candidate =
            combine_disjoint(state, xy_move, c_move, d_move);
        if (candidate.new_energy < best.new_energy) best = candidate;
      }
    }
  };
  scan(xy_pool, c_pool, 0, 1);
  scan(xy_pool, d_pool, 0, 2);
  scan(c_pool, d_pool, 1, 2);
  if (best.new_energy >= state.energy) return false;
  apply_move(state, best);
  validate(state);
  return true;
}

bool polish(State &state, int pool_size, int maximum_steps) {
  state.regular_polish_completed = false;
  state.regular_xy_moves = 0;
  state.regular_c_moves = 0;
  state.regular_d_moves = 0;
  for (int step = 0; step < maximum_steps; ++step) {
    const std::vector<Move> xy = xy_moves(state);
    const std::vector<Move> c = exchange_moves(state, 2);
    const std::vector<Move> d = exchange_moves(state, 3);
    state.regular_xy_moves = xy.size();
    state.regular_c_moves = c.size();
    state.regular_d_moves = d.size();
    std::cout << "polish_step=" << step << " energy=" << state.energy
              << " xy_moves=" << xy.size() << " c_moves=" << c.size()
              << " d_moves=" << d.size() << '\n';
    if (exact_triple_polish(state, xy, c, d)) return true;
    state.regular_polish_completed = true;
    if (!pooled_pair_descent(state, xy, c, d, pool_size)) return false;
    state.regular_polish_completed = false;
    state.regular_xy_moves = 0;
    state.regular_c_moves = 0;
    state.regular_d_moves = 0;
    if (state.energy == 0) return true;
  }
  return state.energy == 0;
}

void write_integer_array(std::ostream &stream, const Sequence &sequence) {
  stream << '[';
  for (int index = 0; index < P; ++index) {
    if (index) stream << ',';
    stream << static_cast<int>(sequence[index]);
  }
  stream << ']';
}

void write_set(std::ostream &stream, const Sequence &sequence) {
  stream << '[';
  bool first = true;
  for (int index = 0; index < P; ++index) {
    if (sequence[index] != -1) continue;
    if (!first) stream << ',';
    first = false;
    stream << index;
  }
  stream << ']';
}

void write_checkpoint(const std::filesystem::path &path, const State &state,
                      std::uint64_t seed, std::uint64_t moves) {
  validate(state);
  const bool exact = state.energy == 0;
  const Profile profile = profiles()[state.profile_index];
  const std::filesystem::path parent = path.parent_path();
  if (!parent.empty()) std::filesystem::create_directories(parent);
  const std::filesystem::path temporary = path.string() + ".tmp";
  std::ofstream stream(temporary);
  if (!stream) throw std::runtime_error("could not open checkpoint output");
  stream << "{\n";
  stream << "  \"format\": \""
         << (exact ? "h668-oriented-sds-v1"
                   : "h668-oriented-sds-local-checkpoint-v1")
         << "\",\n";
  stream << "  \"modulus\": 83,\n";
  stream << "  \"profile_index\": " << state.profile_index << ",\n";
  stream << "  \"profile\": {\"x\": " << profile[0]
         << ", \"y\": " << profile[1] << ", \"z\": " << profile[2]
         << ", \"w\": " << profile[3] << "},\n";
  stream << "  \"search\": {\"engine\": \"oriented-local-v1\", "
         << "\"seed\": " << seed << ", \"moves\": " << moves << "},\n";
  stream << "  \"quarter_energy\": " << state.energy << ",\n";
  stream << "  \"bad_independent_lags\": " << bad_lags(state) << ",\n";
  stream << "  \"maximum_absolute_quarter_residual\": "
         << maximum_quarter_residual(state) << ",\n";
  stream << "  \"finite_neighborhood_audit\": {\n";
  stream << "    \"regular_completed\": "
         << (state.regular_polish_completed ? "true" : "false") << ",\n";
  stream << "    \"xy_support_at_most_two_moves\": "
         << state.regular_xy_moves << ",\n";
  stream << "    \"c_single_exchange_moves\": " << state.regular_c_moves
         << ",\n";
  stream << "    \"d_single_exchange_moves\": " << state.regular_d_moves
         << ",\n";
  stream << "    \"deep_completed\": "
         << (state.deep_polish_completed ? "true" : "false") << ",\n";
  stream << "    \"c_double_exchange_moves\": "
         << state.deep_c_double_moves << ",\n";
  stream << "    \"d_double_exchange_moves\": "
         << state.deep_d_double_moves << ",\n";
  stream << "    \"xy_support_at_most_three_moves\": "
         << state.deep_xy_triple_moves << "\n";
  stream << "  },\n";
  for (int which = 0; which < BLOCKS; ++which) {
    stream << "  \"" << "xyzw"[which] << "\": ";
    write_set(stream, state.sequence[which]);
    stream << ",\n";
  }
  for (int which = 0; which < BLOCKS; ++which) {
    stream << "  \"fold_" << "uvcd"[which] << "\": ";
    write_integer_array(stream, state.sequence[which]);
    stream << ",\n";
  }
  stream << "  \"periodic_paf_sum\": [334";
  for (int lag = 1; lag <= HALF; ++lag)
    stream << ',' << state.residual[lag];
  for (int lag = HALF + 1; lag < P; ++lag)
    stream << ',' << state.residual[P - lag];
  stream << "],\n";
  stream << "  \"lift\": null\n";
  stream << "}\n";
  stream.close();
  if (!stream) throw std::runtime_error("failed while writing checkpoint");
  std::filesystem::rename(temporary, path);
}

std::vector<int> parse_array_after(const std::string &text,
                                   const std::string &key) {
  const std::size_t key_position = text.find(key);
  if (key_position == std::string::npos)
    throw std::runtime_error("initial checkpoint is missing " + key);
  const std::size_t left = text.find('[', key_position);
  const std::size_t right = text.find(']', left);
  if (left == std::string::npos || right == std::string::npos)
    throw std::runtime_error("initial checkpoint has a malformed " + key);
  std::vector<int> result;
  const char *cursor = text.c_str() + left + 1;
  const char *finish = text.c_str() + right;
  while (cursor < finish) {
    if (*cursor == '-' || (*cursor >= '0' && *cursor <= '9')) {
      char *end = nullptr;
      result.push_back(static_cast<int>(std::strtol(cursor, &end, 10)));
      cursor = end;
    } else {
      ++cursor;
    }
  }
  return result;
}

int parse_integer_after(const std::string &text, const std::string &key) {
  const std::size_t key_position = text.find(key);
  if (key_position == std::string::npos)
    throw std::runtime_error("initial checkpoint is missing " + key);
  const std::size_t colon = text.find(':', key_position);
  if (colon == std::string::npos)
    throw std::runtime_error("initial checkpoint has a malformed " + key);
  return std::stoi(text.substr(colon + 1));
}

std::uint64_t parse_unsigned_after(const std::string &text,
                                   const std::string &key) {
  const std::size_t key_position = text.find(key);
  if (key_position == std::string::npos)
    throw std::runtime_error("initial checkpoint is missing " + key);
  const std::size_t colon = text.find(':', key_position);
  if (colon == std::string::npos)
    throw std::runtime_error("initial checkpoint has a malformed " + key);
  return std::stoull(text.substr(colon + 1));
}

State read_checkpoint(const std::filesystem::path &path) {
  std::ifstream stream(path);
  if (!stream) throw std::runtime_error("could not open initial checkpoint");
  const std::string text((std::istreambuf_iterator<char>(stream)),
                         std::istreambuf_iterator<char>());
  State state;
  state.profile_index = parse_integer_after(text, "\"profile_index\"");
  state.recorded_moves = parse_unsigned_after(text, "\"moves\"");
  for (int which = 0; which < BLOCKS; ++which) {
    const std::vector<int> values =
        parse_array_after(text, "\"fold_" + std::string(1, "uvcd"[which]) + "\"");
    if (values.size() != P)
      throw std::runtime_error("initial folded sequence has wrong length");
    for (int index = 0; index < P; ++index)
      state.sequence[which][index] = static_cast<std::int8_t>(values[index]);
  }
  for (int pair = 0; pair < HALF; ++pair) {
    const int lag = pair + 1;
    const int inverse = P - lag;
    std::array<int, 4> bits{{
        state.sequence[0][lag] == -1,
        state.sequence[0][inverse] == -1,
        state.sequence[1][lag] == -1,
        state.sequence[1][inverse] == -1,
    }};
    int found = -1;
    for (int candidate = 0; candidate < 8; ++candidate)
      if (PAIR_BITS[candidate] == bits) found = candidate;
    if (found < 0)
      throw std::runtime_error("initial X/Y state violates pair parity");
    state.pair_state[pair] = static_cast<std::uint8_t>(found);
  }
  state.residual = full_residual(state.sequence);
  state.energy = residual_energy(state.residual);
  validate(state);
  return state;
}

std::uint64_t parse_unsigned(std::string_view value, std::string_view name) {
  std::size_t consumed = 0;
  const std::string text(value);
  const unsigned long long result = std::stoull(text, &consumed);
  if (consumed != text.size())
    throw std::runtime_error(std::string(name) + " is not an unsigned integer");
  return static_cast<std::uint64_t>(result);
}

double parse_double(std::string_view value, std::string_view name) {
  std::size_t consumed = 0;
  const std::string text(value);
  const double result = std::stod(text, &consumed);
  if (consumed != text.size() || !std::isfinite(result))
    throw std::runtime_error(std::string(name) + " is not a finite number");
  return result;
}

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string_view argument(argv[index]);
    const auto value = [&](std::string_view name) -> std::string_view {
      if (index + 1 >= argc)
        throw std::runtime_error(std::string(name) + " needs a value");
      return argv[++index];
    };
    if (argument == "--seconds")
      options.seconds = parse_double(value(argument), argument);
    else if (argument == "--seed")
      options.seed = parse_unsigned(value(argument), argument);
    else if (argument == "--profile")
      options.profile =
          static_cast<int>(parse_unsigned(value(argument), argument));
    else if (argument == "--moves-per-restart")
      options.moves_per_restart = parse_unsigned(value(argument), argument);
    else if (argument == "--start-temperature")
      options.start_temperature = parse_double(value(argument), argument);
    else if (argument == "--end-temperature")
      options.end_temperature = parse_double(value(argument), argument);
    else if (argument == "--validate-every")
      options.validate_every = parse_unsigned(value(argument), argument);
    else if (argument == "--report-every")
      options.report_every = parse_double(value(argument), argument);
    else if (argument == "--polish-pool")
      options.polish_pool =
          static_cast<int>(parse_unsigned(value(argument), argument));
    else if (argument == "--polish-steps")
      options.polish_steps =
          static_cast<int>(parse_unsigned(value(argument), argument));
    else if (argument == "--deep-polish")
      options.deep_polish = true;
    else if (argument == "--output")
      options.output = value(argument);
    else if (argument == "--initial")
      options.initial = value(argument);
    else if (argument == "--self-test")
      options.self_test = true;
    else
      throw std::runtime_error("unknown option: " + std::string(argument));
  }
  if (options.seconds <= 0.0)
    throw std::runtime_error("--seconds must be positive");
  if (options.profile < 0 || options.profile >= 45)
    throw std::runtime_error("--profile must lie in 0..44");
  if (options.moves_per_restart == 0)
    throw std::runtime_error("--moves-per-restart must be positive");
  if (options.start_temperature <= 0.0 || options.end_temperature <= 0.0)
    throw std::runtime_error("temperatures must be positive");
  if (options.polish_pool <= 0 || options.polish_steps < 0)
    throw std::runtime_error("polish parameters are out of range");
  return options;
}

void self_test() {
  if (profiles().size() != 45)
    throw std::runtime_error("profile self-test failed");
  std::mt19937_64 rng(668083);
  for (int profile : {0, 9, 20, 44}) {
    State state = random_state(profile, rng);
    for (int iteration = 0; iteration < 1000; ++iteration) {
      Move move = propose_move(state, rng);
      apply_move(state, move);
      validate(state);
    }
  }
  std::cout << "self_test=passed\n";
}

int run(const Options &options) {
  std::mt19937_64 rng(options.seed);
  State current = options.initial.empty()
                      ? random_state(options.profile, rng)
                      : read_checkpoint(options.initial);
  if (!options.initial.empty() && current.profile_index != options.profile)
    throw std::runtime_error("--initial profile disagrees with --profile");
  State best = current;
  const std::uint64_t prior_moves = current.recorded_moves;
  std::uint64_t moves = 0;
  std::uint64_t accepted = 0;
  std::uint64_t restarts = 0;
  const auto started = std::chrono::steady_clock::now();
  auto next_report = started + std::chrono::duration<double>(options.report_every);
  const auto deadline = started + std::chrono::duration<double>(options.seconds);
  std::uniform_real_distribution<double> unit(0.0, 1.0);

  write_checkpoint(options.output, best, options.seed, prior_moves + moves);
  while (std::chrono::steady_clock::now() < deadline) {
    const std::uint64_t phase_move = moves % options.moves_per_restart;
    if (phase_move == 0 && moves != 0) {
      current = random_state(options.profile, rng);
      ++restarts;
    }
    const double fraction =
        static_cast<double>(phase_move) /
        static_cast<double>(std::max<std::uint64_t>(
            1, options.moves_per_restart - 1));
    const double temperature =
        options.start_temperature *
        std::pow(options.end_temperature / options.start_temperature, fraction);
    Move move = propose_move(current, rng);
    const std::int64_t difference = move.new_energy - current.energy;
    if (difference <= 0 ||
        unit(rng) < std::exp(-static_cast<double>(difference) / temperature)) {
      apply_move(current, move);
      ++accepted;
      if (current.energy < best.energy) {
        best = current;
        write_checkpoint(options.output, best, options.seed,
                         prior_moves + moves + 1);
        if (best.energy == 0) {
          validate(best);
          std::cout << "exact=true\n";
          std::cout << "output=" << options.output << '\n';
          std::cout << "moves=" << moves + 1 << '\n';
          return 0;
        }
      }
    }
    ++moves;
    if (options.validate_every != 0 && moves % options.validate_every == 0)
      validate(current);
    const auto now = std::chrono::steady_clock::now();
    if (now >= next_report) {
      const double elapsed =
          std::chrono::duration<double>(now - started).count();
      std::cout << std::fixed << std::setprecision(3)
                << "elapsed=" << elapsed << " moves=" << moves
                << " accepted=" << accepted << " restarts=" << restarts
                << " current_energy=" << current.energy
                << " best_energy=" << best.energy
                << " best_bad_lags=" << bad_lags(best)
                << " best_max_residual=" << maximum_quarter_residual(best)
                << '\n';
      next_report = now + std::chrono::duration<double>(options.report_every);
    }
  }
  validate(best);
  const std::int64_t anneal_energy = best.energy;
  if (options.polish_steps > 0)
    polish(best, options.polish_pool, options.polish_steps);
  if (best.energy != 0 && options.deep_polish) deep_exact_polish(best);
  write_checkpoint(options.output, best, options.seed, prior_moves + moves);
  std::cout << "exact=" << (best.energy == 0 ? "true" : "false") << '\n';
  std::cout << "output=" << options.output << '\n';
  std::cout << "moves=" << moves << '\n';
  std::cout << "anneal_energy=" << anneal_energy << '\n';
  std::cout << "best_energy=" << best.energy << '\n';
  std::cout << "best_bad_lags=" << bad_lags(best) << '\n';
  std::cout << "best_max_residual=" << maximum_quarter_residual(best) << '\n';
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
    return run(options);
  } catch (const std::exception &error) {
    std::cerr << "error=" << error.what() << '\n';
    return 2;
  }
}
