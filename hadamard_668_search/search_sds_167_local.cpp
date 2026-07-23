// Low-memory simulated annealing for unrestricted cyclic SDS at order 167.
//
// The engine keeps four row sums fixed and updates all 83 independent
// periodic-correlation residuals in O(83) per two-coordinate exchange.  It is
// deliberately single-threaded and uses bounded low-memory move pools.  A
// zero is accepted only after a full recomputation.  Exact bounded scan modes
// also cover independent decimations and the complete fixed-profile Hamming
// radius-four neighborhood.  Python independently expands any exact output
// to the 668x668 Goethals-Seidel matrix.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
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
#include <vector>

namespace {

constexpr int N = 167;
constexpr int HALF = 83;
constexpr int SEQUENCES = 4;
static_assert(static_cast<std::uint64_t>(HALF) * (HALF + 1) < 8192,
              "complete exchange pools must fit below the hard cap");

using Sequence = std::array<std::int8_t, N>;
using Quadruple = std::array<Sequence, SEQUENCES>;
using Profile = std::array<int, SEQUENCES>;
using Residuals = std::array<int, HALF + 1>;

constexpr std::array<Profile, 10> PROFILES{{
    {{1, 1, 15, 21}},
    {{1, 9, 15, 19}},
    {{3, 3, 5, 25}},
    {{3, 3, 11, 23}},
    {{3, 3, 17, 19}},
    {{3, 7, 9, 23}},
    {{3, 7, 13, 21}},
    {{3, 9, 17, 17}},
    {{5, 9, 11, 21}},
    {{7, 13, 15, 15}},
}};

struct State {
  Quadruple sequence{};
  Residuals residual{};
  std::int64_t energy = 0;
  int profile = -1;
};

struct ScoreWeights {
  std::uint64_t energy = 1;
  std::uint64_t quartic = 0;
  std::uint64_t bad_lags = 0;
};

struct Options {
  double seconds = 60.0;
  std::uint64_t seed = 668;
  int profile = -1;
  std::uint64_t moves_per_restart = 1'000'000;
  double start_temperature = 80.0;
  double end_temperature = 0.05;
  std::uint64_t validate_every = 1'000'000;
  double report_every = 10.0;
  std::filesystem::path output = "output/sds_167_local_best.json";
  std::filesystem::path initial;
  bool restart_from_best = false;
  std::uint64_t perturb_exchanges = 8;
  int move_arity = 1;
  double compound_probability = 1.0;
  double same_sequence_probability = 0.0;
  std::uint64_t pair_polish_size = 0;
  std::uint64_t pair_polish_steps = 64;
  int pair_polish_arity = 2;
  ScoreWeights score_weights;
  bool decimation_scan = false;
  bool same_sequence_pair_scan = false;
  bool cross_sequence_pair_scan = false;
  int window_half_size = 0;
  int paired_window_half_size = 0;
  int four_window_mitm_half_size = 0;
  int mixed_window_mitm_half_size = 0;
  int mixed_window_batch_size = 8;
  int mixed_window_batch_start = 0;
  int mixed_window_batch_count = 0;
  int window_family_count = 1;
  std::string scan_objective = "energy";
  bool self_test = false;
};

int wrap(int index) {
  if (index >= N) return index - N;
  if (index < 0) return index + N;
  return index;
}

int periodic_correlation(const Sequence &sequence, int lag) {
  int value = 0;
  for (int index = 0; index < N; ++index)
    value += sequence[index] * sequence[wrap(index + lag)];
  return value;
}

Residuals full_residuals(const Quadruple &quadruple) {
  Residuals result{};
  result[0] = 4 * N;
  for (int lag = 1; lag <= HALF; ++lag) {
    int value = 0;
    for (const Sequence &sequence : quadruple)
      value += periodic_correlation(sequence, lag);
    if (value % 4 != 0)
      throw std::runtime_error("periodic residual is not divisible by four");
    result[lag] = value;
  }
  return result;
}

std::int64_t energy(const Residuals &residual) {
  std::int64_t result = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    if (residual[lag] % 4 != 0)
      throw std::runtime_error("energy received a nonintegral quarter residual");
    const std::int64_t value = residual[lag] / 4;
    result += value * value;
  }
  return result;
}

std::int64_t quartic_energy(const Residuals &residual) {
  std::int64_t result = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    if (residual[lag] % 4 != 0)
      throw std::runtime_error(
          "quartic energy received a nonintegral quarter residual");
    const std::int64_t value = residual[lag] / 4;
    const std::int64_t square = value * value;
    result += square * square;
  }
  return result;
}

int row_sum(const Sequence &sequence) {
  int result = 0;
  for (std::int8_t value : sequence) result += value;
  return result;
}

void validate(const State &state) {
  if (state.profile < 0 || state.profile >= static_cast<int>(PROFILES.size()))
    throw std::runtime_error("state profile is invalid");
  for (int which = 0; which < SEQUENCES; ++which) {
    if (row_sum(state.sequence[which]) != PROFILES[state.profile][which])
      throw std::runtime_error("row sum changed during local search");
    for (std::int8_t value : state.sequence[which])
      if (value != -1 && value != 1)
        throw std::runtime_error("non-sign entry in local state");
  }
  const Residuals expected = full_residuals(state.sequence);
  if (expected != state.residual)
    throw std::runtime_error("incremental periodic residual mismatch");
  if (energy(expected) != state.energy)
    throw std::runtime_error("incremental energy mismatch");
}

State random_state(int profile, std::mt19937_64 &rng) {
  State state;
  state.profile = profile;
  for (int which = 0; which < SEQUENCES; ++which) {
    const int plus = (N + PROFILES[profile][which]) / 2;
    Sequence &sequence = state.sequence[which];
    std::fill(sequence.begin(), sequence.begin() + plus, 1);
    std::fill(sequence.begin() + plus, sequence.end(), -1);
    std::shuffle(sequence.begin(), sequence.end(), rng);
  }
  state.residual = full_residuals(state.sequence);
  state.energy = energy(state.residual);
  return state;
}

std::array<int, HALF + 1> two_flip_deltas(
    const Sequence &sequence, int left, int right) {
  if (left == right)
    throw std::runtime_error("flip endpoints must be distinct");
  std::array<int, HALF + 1> result{};
  const int left_sign = sequence[left];
  const int right_sign = sequence[right];
  for (int lag = 1; lag <= HALF; ++lag) {
    int delta =
        -2 * left_sign *
            (sequence[wrap(left + lag)] + sequence[wrap(left - lag)])
        -2 * right_sign *
            (sequence[wrap(right + lag)] + sequence[wrap(right - lag)]);
    // The two endpoint contributions counted their mutual PAF pair as if
    // only one sign flipped.  Restore that pair when both signs flip.
    if (wrap(left + lag) == right || wrap(right + lag) == left)
      delta += 4 * left_sign * right_sign;
    result[lag] = delta;
  }
  return result;
}

std::array<int, HALF + 1> exchange_deltas(
    const Sequence &sequence, int left, int right) {
  if (sequence[left] == sequence[right])
    throw std::runtime_error("exchange endpoints must have opposite signs");
  return two_flip_deltas(sequence, left, right);
}

Residuals same_sequence_double_exchange_deltas(
    const Sequence &sequence, const std::array<int, 4> &positions) {
  if (sequence[positions[0]] != sequence[positions[1]] ||
      sequence[positions[2]] != sequence[positions[3]] ||
      sequence[positions[0]] == sequence[positions[2]])
    throw std::runtime_error(
        "same-sequence move requires two endpoints of each sign");
  for (int first = 0; first < 4; ++first)
    for (int second = first + 1; second < 4; ++second)
      if (positions[first] == positions[second])
        throw std::runtime_error(
            "same-sequence move endpoints must be distinct");
  Residuals result =
      two_flip_deltas(sequence, positions[0], positions[1]);
  const Residuals second_pair =
      two_flip_deltas(sequence, positions[2], positions[3]);
  for (int lag = 1; lag <= HALF; ++lag)
    result[lag] += second_pair[lag];
  for (int first = 0; first < 2; ++first) {
    for (int second = 2; second < 4; ++second) {
      int lag = std::abs(positions[first] - positions[second]);
      if (lag > HALF) lag = N - lag;
      result[lag] += 4 * sequence[positions[first]] *
                     sequence[positions[second]];
    }
  }
  return result;
}

std::array<int, 4> random_same_sequence_double_exchange(
    const Sequence &sequence, std::mt19937_64 &rng) {
  std::uniform_int_distribution<int> position(0, N - 1);
  std::array<int, 4> result{};
  for (int index = 0; index < 2; ++index) {
    do {
      result[index] = position(rng);
    } while (sequence[result[index]] != 1 ||
             (index == 1 && result[index] == result[0]));
  }
  for (int index = 2; index < 4; ++index) {
    do {
      result[index] = position(rng);
    } while (sequence[result[index]] != -1 ||
             (index == 3 && result[index] == result[2]));
  }
  return result;
}

std::pair<int, int> random_exchange(const Sequence &sequence,
                                    std::mt19937_64 &rng) {
  std::uniform_int_distribution<int> position(0, N - 1);
  const int left = position(rng);
  int right = position(rng);
  while (sequence[right] == sequence[left]) right = position(rng);
  return {left, right};
}

std::int64_t exchanged_energy(
    const State &state, const std::array<int, HALF + 1> &delta,
    int *resulting_bad_lags = nullptr,
    std::int64_t *resulting_quartic = nullptr) {
  std::int64_t result = 0;
  std::int64_t quartic = 0;
  int bad_lag_count = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    const int updated = state.residual[lag] + delta[lag];
    if (updated % 4 != 0)
      throw std::runtime_error("exchange broke quarter-residual integrality");
    const std::int64_t value = updated / 4;
    const std::int64_t square = value * value;
    result += square;
    quartic += square * square;
    bad_lag_count += updated != 0;
  }
  if (resulting_bad_lags != nullptr)
    *resulting_bad_lags = bad_lag_count;
  if (resulting_quartic != nullptr)
    *resulting_quartic = quartic;
  return result;
}

void apply_exchange(State &state, int which, int left, int right,
                    const std::array<int, HALF + 1> &delta,
                    std::int64_t new_energy) {
  std::swap(state.sequence[which][left], state.sequence[which][right]);
  for (int lag = 1; lag <= HALF; ++lag) state.residual[lag] += delta[lag];
  state.energy = new_energy;
}

void apply_compound_exchange(
    State &state, const std::array<int, SEQUENCES> &which,
    const std::array<int, SEQUENCES> &left,
    const std::array<int, SEQUENCES> &right, int arity,
    const std::array<int, HALF + 1> &combined_delta,
    std::int64_t new_energy) {
  for (int move = 0; move < arity; ++move)
    std::swap(state.sequence[which[move]][left[move]],
              state.sequence[which[move]][right[move]]);
  for (int lag = 1; lag <= HALF; ++lag)
    state.residual[lag] += combined_delta[lag];
  state.energy = new_energy;
}

void apply_same_sequence_double_exchange(
    State &state, int which, const std::array<int, 4> &positions,
    const Residuals &delta, std::int64_t new_energy) {
  for (int position : positions)
    state.sequence[which][position] *= -1;
  for (int lag = 1; lag <= HALF; ++lag)
    state.residual[lag] += delta[lag];
  state.energy = new_energy;
}

struct ExchangeMove {
  int which = -1;
  int left = -1;
  int right = -1;
  Residuals delta{};
  std::int64_t energy = 0;
};

std::vector<ExchangeMove> best_exchange_moves(
    const State &state, int which, std::size_t limit) {
  std::vector<ExchangeMove> candidates;
  candidates.reserve(7000);
  for (int left = 0; left < N; ++left) {
    for (int right = left + 1; right < N; ++right) {
      if (state.sequence[which][left] == state.sequence[which][right]) continue;
      ExchangeMove move;
      move.which = which;
      move.left = left;
      move.right = right;
      move.delta = exchange_deltas(state.sequence[which], left, right);
      move.energy = exchanged_energy(state, move.delta);
      candidates.push_back(move);
    }
  }
  const auto less = [](const ExchangeMove &left, const ExchangeMove &right) {
    if (left.energy != right.energy) return left.energy < right.energy;
    if (left.left != right.left) return left.left < right.left;
    return left.right < right.right;
  };
  if (candidates.size() > limit) {
    std::nth_element(
        candidates.begin(), candidates.begin() + static_cast<std::ptrdiff_t>(limit),
        candidates.end(), less);
    candidates.resize(limit);
  }
  std::sort(candidates.begin(), candidates.end(), less);
  return candidates;
}

int best_pair_descent(State &state, std::size_t pool_size, int maximum_steps,
                      int maximum_arity) {
  int improvements = 0;
  for (int step = 0; step < maximum_steps; ++step) {
    std::array<std::vector<ExchangeMove>, SEQUENCES> pools;
    for (int which = 0; which < SEQUENCES; ++which)
      pools[which] = best_exchange_moves(state, which, pool_size);

    std::int64_t best_energy = state.energy;
    const ExchangeMove *best_first = nullptr;
    const ExchangeMove *best_second = nullptr;
    const ExchangeMove *best_third = nullptr;
    Residuals best_delta{};
    for (int first_sequence = 0; first_sequence < SEQUENCES;
         ++first_sequence) {
      for (const ExchangeMove &first : pools[first_sequence]) {
        if (first.energy < best_energy) {
          best_energy = first.energy;
          best_first = &first;
          best_second = nullptr;
          best_third = nullptr;
          best_delta = first.delta;
        }
      }
      for (int second_sequence = first_sequence + 1;
           second_sequence < SEQUENCES; ++second_sequence) {
        for (const ExchangeMove &first : pools[first_sequence]) {
          for (const ExchangeMove &second : pools[second_sequence]) {
            Residuals combined{};
            for (int lag = 1; lag <= HALF; ++lag)
              combined[lag] = first.delta[lag] + second.delta[lag];
            const std::int64_t candidate_energy =
                exchanged_energy(state, combined);
            if (candidate_energy < best_energy) {
              best_energy = candidate_energy;
              best_first = &first;
              best_second = &second;
              best_third = nullptr;
              best_delta = combined;
            }
          }
        }
      }
    }
    if (maximum_arity >= 3) {
      for (int first_sequence = 0; first_sequence < SEQUENCES;
           ++first_sequence) {
        for (int second_sequence = first_sequence + 1;
             second_sequence < SEQUENCES; ++second_sequence) {
          for (int third_sequence = second_sequence + 1;
               third_sequence < SEQUENCES; ++third_sequence) {
            for (const ExchangeMove &first : pools[first_sequence]) {
              for (const ExchangeMove &second : pools[second_sequence]) {
                Residuals pair_delta{};
                for (int lag = 1; lag <= HALF; ++lag)
                  pair_delta[lag] = first.delta[lag] + second.delta[lag];
                for (const ExchangeMove &third : pools[third_sequence]) {
                  Residuals combined{};
                  for (int lag = 1; lag <= HALF; ++lag)
                    combined[lag] = pair_delta[lag] + third.delta[lag];
                  const std::int64_t candidate_energy =
                      exchanged_energy(state, combined);
                  if (candidate_energy < best_energy) {
                    best_energy = candidate_energy;
                    best_first = &first;
                    best_second = &second;
                    best_third = &third;
                    best_delta = combined;
                  }
                }
              }
            }
          }
        }
      }
    }
    if (best_first == nullptr) break;
    if (best_second == nullptr) {
      apply_exchange(state, best_first->which, best_first->left,
                     best_first->right, best_delta, best_energy);
    } else {
      const int arity = best_third == nullptr ? 2 : 3;
      std::array<int, SEQUENCES> which{{best_first->which, best_second->which,
                                       best_third == nullptr ? 0
                                                             : best_third->which}};
      std::array<int, SEQUENCES> left{{best_first->left, best_second->left,
                                      best_third == nullptr ? 0
                                                            : best_third->left}};
      std::array<int, SEQUENCES> right{{best_first->right, best_second->right,
                                       best_third == nullptr ? 0
                                                             : best_third->right}};
      apply_compound_exchange(
          state, which, left, right, arity, best_delta, best_energy);
    }
    ++improvements;
    validate(state);
  }
  return improvements;
}

int bad_lags(const State &state) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result += state.residual[lag] != 0;
  return result;
}

int exchanged_bad_lags(const State &state, const Residuals &delta) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result += state.residual[lag] + delta[lag] != 0;
  return result;
}

std::int64_t search_score(std::int64_t state_energy,
                          std::int64_t state_quartic, int state_bad_lags,
                          const ScoreWeights &weights) {
  return static_cast<std::int64_t>(weights.energy) * state_energy +
         static_cast<std::int64_t>(weights.quartic) * state_quartic +
         static_cast<std::int64_t>(weights.bad_lags) * state_bad_lags;
}

int maximum_residual(const State &state) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result = std::max(result, std::abs(state.residual[lag]));
  return result;
}

void write_sequence(std::ostream &stream, const Sequence &sequence) {
  stream << '[';
  for (int index = 0; index < N; ++index) {
    if (index) stream << ',';
    stream << static_cast<int>(sequence[index]);
  }
  stream << ']';
}

void write_checkpoint(const std::filesystem::path &path, const State &state,
                      std::uint64_t seed, std::uint64_t moves,
                      bool exact, const ScoreWeights &weights) {
  const std::filesystem::path parent = path.parent_path();
  if (!parent.empty()) std::filesystem::create_directories(parent);
  const std::filesystem::path temporary = path.string() + ".tmp";
  std::ofstream stream(temporary);
  if (!stream) throw std::runtime_error("could not open checkpoint output");
  stream << "{\n";
  stream << "  \"kind\": \""
         << (exact ? "cyclic_sds_167" : "cyclic_sds_167_checkpoint")
         << "\",\n";
  stream << "  \"order\": 167,\n";
  stream << "  \"hadamard_order\": 668,\n";
  stream << "  \"profile\": " << state.profile << ",\n";
  stream << "  \"row_sums\": [";
  for (int which = 0; which < SEQUENCES; ++which) {
    if (which) stream << ',';
    stream << row_sum(state.sequence[which]);
  }
  stream << "],\n";
  stream << "  \"quarter_energy\": " << state.energy << ",\n";
  stream << "  \"quarter_quartic\": " << quartic_energy(state.residual)
         << ",\n";
  stream << "  \"bad_lags\": " << bad_lags(state) << ",\n";
  stream << "  \"energy_weight\": " << weights.energy << ",\n";
  stream << "  \"quartic_weight\": " << weights.quartic << ",\n";
  stream << "  \"bad_lag_penalty\": " << weights.bad_lags << ",\n";
  stream << "  \"search_score\": "
         << search_score(state.energy, quartic_energy(state.residual),
                         bad_lags(state), weights)
         << ",\n";
  stream << "  \"maximum_absolute_residual\": " << maximum_residual(state)
         << ",\n";
  stream << "  \"seed\": " << seed << ",\n";
  stream << "  \"moves\": " << moves << ",\n";
  stream << "  \"periodic_correlation_sums\": [";
  stream << 4 * N;
  for (int lag = 1; lag <= HALF; ++lag) stream << ',' << state.residual[lag];
  for (int lag = HALF + 1; lag < N; ++lag)
    stream << ',' << state.residual[N - lag];
  stream << "],\n";
  stream << "  \"sequences\": [\n";
  for (int which = 0; which < SEQUENCES; ++which) {
    stream << "    ";
    write_sequence(stream, state.sequence[which]);
    stream << (which + 1 == SEQUENCES ? "\n" : ",\n");
  }
  stream << "  ]\n";
  stream << "}\n";
  stream.close();
  if (!stream) throw std::runtime_error("failed while writing checkpoint");
  std::filesystem::rename(temporary, path);
}

State read_checkpoint(const std::filesystem::path &path) {
  std::ifstream stream(path);
  if (!stream) throw std::runtime_error("could not open initial checkpoint");
  const std::string text((std::istreambuf_iterator<char>(stream)),
                         std::istreambuf_iterator<char>());
  const std::size_t profile_key = text.find("\"profile\"");
  if (profile_key == std::string::npos)
    throw std::runtime_error("initial checkpoint has no profile");
  const std::size_t profile_colon = text.find(':', profile_key);
  if (profile_colon == std::string::npos)
    throw std::runtime_error("initial checkpoint profile is malformed");

  State state;
  std::size_t consumed = 0;
  state.profile = std::stoi(text.substr(profile_colon + 1), &consumed);
  if (state.profile < 0 || state.profile >= static_cast<int>(PROFILES.size()))
    throw std::runtime_error("initial checkpoint profile is out of range");

  const std::size_t sequence_key = text.find("\"sequences\"");
  if (sequence_key == std::string::npos)
    throw std::runtime_error("initial checkpoint has no sequences");
  const char *cursor = text.c_str() + sequence_key;
  const char *const finish = text.c_str() + text.size();
  int count = 0;
  while (cursor < finish && count < SEQUENCES * N) {
    if (*cursor == '-' || (*cursor >= '0' && *cursor <= '9')) {
      char *end = nullptr;
      const long value = std::strtol(cursor, &end, 10);
      if (end == cursor) throw std::runtime_error("could not parse initial sign");
      if (value != -1 && value != 1)
        throw std::runtime_error("initial checkpoint contains a non-sign");
      state.sequence[count / N][count % N] = static_cast<std::int8_t>(value);
      ++count;
      cursor = end;
    } else {
      ++cursor;
    }
  }
  if (count != SEQUENCES * N)
    throw std::runtime_error("initial checkpoint has too few signs");
  state.residual = full_residuals(state.sequence);
  state.energy = energy(state.residual);
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

int parse_bounded_int(std::string_view value, std::string_view name,
                      std::uint64_t maximum) {
  const std::uint64_t result = parse_unsigned(value, name);
  if (result > maximum)
    throw std::runtime_error(
        std::string(name) + " exceeds its supported bound");
  return static_cast<int>(result);
}

double parse_double(std::string_view value, std::string_view name) {
  std::size_t consumed = 0;
  const std::string text(value);
  const double result = std::stod(text, &consumed);
  if (consumed != text.size() || !std::isfinite(result))
    throw std::runtime_error(std::string(name) + " is not finite");
  return result;
}

Options parse_options(int argc, char **argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto next = [&](std::string_view name) -> std::string_view {
      if (++index >= argc)
        throw std::runtime_error(std::string(name) + " requires a value");
      return argv[index];
    };
    if (argument == "--seconds")
      options.seconds = parse_double(next(argument), argument);
    else if (argument == "--seed")
      options.seed = parse_unsigned(next(argument), argument);
    else if (argument == "--profile")
      options.profile = std::stoi(std::string(next(argument)));
    else if (argument == "--moves-per-restart")
      options.moves_per_restart = parse_unsigned(next(argument), argument);
    else if (argument == "--start-temperature")
      options.start_temperature = parse_double(next(argument), argument);
    else if (argument == "--end-temperature")
      options.end_temperature = parse_double(next(argument), argument);
    else if (argument == "--validate-every")
      options.validate_every = parse_unsigned(next(argument), argument);
    else if (argument == "--report-every")
      options.report_every = parse_double(next(argument), argument);
    else if (argument == "--output")
      options.output = std::string(next(argument));
    else if (argument == "--initial")
      options.initial = std::string(next(argument));
    else if (argument == "--restart-from-best")
      options.restart_from_best = true;
    else if (argument == "--perturb-exchanges")
      options.perturb_exchanges = parse_unsigned(next(argument), argument);
    else if (argument == "--move-arity")
      options.move_arity = parse_bounded_int(next(argument), argument, 4);
    else if (argument == "--compound-probability")
      options.compound_probability = parse_double(next(argument), argument);
    else if (argument == "--same-sequence-probability")
      options.same_sequence_probability =
          parse_double(next(argument), argument);
    else if (argument == "--pair-polish-size")
      options.pair_polish_size = parse_unsigned(next(argument), argument);
    else if (argument == "--pair-polish-steps")
      options.pair_polish_steps = parse_unsigned(next(argument), argument);
    else if (argument == "--pair-polish-arity")
      options.pair_polish_arity =
          parse_bounded_int(next(argument), argument, 3);
    else if (argument == "--energy-weight")
      options.score_weights.energy = parse_unsigned(next(argument), argument);
    else if (argument == "--quartic-weight")
      options.score_weights.quartic = parse_unsigned(next(argument), argument);
    else if (argument == "--bad-lag-penalty")
      options.score_weights.bad_lags = parse_unsigned(next(argument), argument);
    else if (argument == "--decimation-scan")
      options.decimation_scan = true;
    else if (argument == "--same-sequence-pair-scan")
      options.same_sequence_pair_scan = true;
    else if (argument == "--cross-sequence-pair-scan")
      options.cross_sequence_pair_scan = true;
    else if (argument == "--window-scan-half-size")
      options.window_half_size =
          parse_bounded_int(next(argument), argument, 12);
    else if (argument == "--paired-window-half-size")
      options.paired_window_half_size =
          parse_bounded_int(next(argument), argument, 6);
    else if (argument == "--four-window-mitm-half-size")
      options.four_window_mitm_half_size =
          parse_bounded_int(next(argument), argument, 6);
    else if (argument == "--mixed-window-mitm-half-size")
      options.mixed_window_mitm_half_size =
          parse_bounded_int(next(argument), argument, 6);
    else if (argument == "--mixed-window-batch-size")
      options.mixed_window_batch_size =
          parse_bounded_int(next(argument), argument, 8);
    else if (argument == "--mixed-window-batch-start")
      options.mixed_window_batch_start =
          parse_bounded_int(next(argument), argument, 144);
    else if (argument == "--mixed-window-batch-count")
      options.mixed_window_batch_count =
          parse_bounded_int(next(argument), argument, 144);
    else if (argument == "--window-family-count")
      options.window_family_count =
          parse_bounded_int(next(argument), argument, 12);
    else if (argument == "--scan-objective")
      options.scan_objective = std::string(next(argument));
    else if (argument == "--self-test")
      options.self_test = true;
    else if (argument == "--help") {
      std::cout
          << "Usage: search_sds_167_local [options]\n"
          << "  --seconds S              wall-clock limit (default 60)\n"
          << "  --seed N                 RNG seed (default 668)\n"
          << "  --profile P              0..9, or -1 for round-robin\n"
          << "  --moves-per-restart N    annealing schedule length\n"
          << "  --start-temperature T    initial temperature\n"
          << "  --end-temperature T      final temperature\n"
          << "  --validate-every N       full-check interval\n"
          << "  --report-every S         progress interval\n"
          << "  --output PATH            best-checkpoint JSON\n"
          << "  --initial PATH           start from a checkpoint JSON\n"
          << "  --restart-from-best      perturb and re-anneal the incumbent\n"
          << "  --perturb-exchanges N    exchanges before incumbent restart\n"
          << "  --move-arity N           coupled exchanges in 1..4 sequences\n"
          << "  --compound-probability P use arity N with probability P\n"
          << "  --same-sequence-probability P propose a four-flip same-block move\n"
          << "  --pair-polish-size N      top single moves per sequence (0 disables)\n"
          << "  --pair-polish-steps N     improving compound-descent steps\n"
          << "  --pair-polish-arity N     evaluate pairs or triples (2 or 3)\n"
          << "  --energy-weight N         search-score coefficient of sum r^2\n"
          << "  --quartic-weight N        search-score coefficient of sum r^4\n"
          << "  --bad-lag-penalty N      search-score cost per nonzero lag\n"
          << "  --decimation-scan        exhaust the 83^3 relative multiplier orbit\n"
          << "  --same-sequence-pair-scan exhaust every same-block double exchange\n"
          << "  --cross-sequence-pair-scan exhaust every cross-block exchange pair\n"
          << "  --window-scan-half-size H exhaust H-plus/H-minus guided windows\n"
          << "  --paired-window-half-size H exhaust paired H-plus/H-minus windows\n"
          << "  --four-window-mitm-half-size H exact four-block window MITM\n"
          << "  --mixed-window-mitm-half-size H exact all mixed-family windows\n"
          << "  --mixed-window-batch-size N left-family pairs per batch (max 8)\n"
          << "  --mixed-window-batch-start N first mixed-family batch\n"
          << "  --mixed-window-batch-count N number of batches (0 means all)\n"
          << "  --window-family-count N  disjoint guided windows per sequence\n"
          << "  --scan-objective NAME    energy, quartic, or maximum\n"
          << "  --self-test              validate incremental deltas\n";
      std::exit(0);
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  if (!(options.seconds > 0.0) || options.moves_per_restart == 0 ||
      !(options.start_temperature > 0.0) ||
      !(options.end_temperature > 0.0) || options.validate_every == 0 ||
      !(options.report_every > 0.0) || options.perturb_exchanges == 0)
    throw std::runtime_error("time, move, temperature, and interval values must be positive");
  if (options.profile < -1 || options.profile >= static_cast<int>(PROFILES.size()))
    throw std::runtime_error("profile must be -1 or lie in 0..9");
  if (options.move_arity < 1 || options.move_arity > SEQUENCES)
    throw std::runtime_error("move arity must lie in 1..4");
  if (options.compound_probability < 0.0 ||
      options.compound_probability > 1.0)
    throw std::runtime_error("compound probability must lie in [0,1]");
  if (options.same_sequence_probability < 0.0 ||
      options.same_sequence_probability > 1.0)
    throw std::runtime_error(
        "same-sequence probability must lie in [0,1]");
  if (options.pair_polish_size > 8192)
    throw std::runtime_error("pair polish size must not exceed 8192");
  if (options.pair_polish_steps > 10000)
    throw std::runtime_error("pair polish steps must not exceed 10000");
  if (options.pair_polish_size > 0 && options.pair_polish_steps == 0)
    throw std::runtime_error("pair polish steps must be positive when enabled");
  if (options.pair_polish_arity < 2 || options.pair_polish_arity > 3)
    throw std::runtime_error("pair polish arity must be 2 or 3");
  if (options.score_weights.energy > 1'000'000 ||
      options.score_weights.quartic > 1'000'000 ||
      options.score_weights.bad_lags > 1'000'000)
    throw std::runtime_error("search-score weights must not exceed 1000000");
  if (options.score_weights.energy == 0 &&
      options.score_weights.quartic == 0)
    throw std::runtime_error(
        "energy weight and quartic weight cannot both be zero");
  const bool raw_energy_score = options.score_weights.energy == 1 &&
                                options.score_weights.quartic == 0 &&
                                options.score_weights.bad_lags == 0;
  if (!raw_energy_score && options.pair_polish_size > 0)
    throw std::runtime_error(
        "shaped search scores cannot be combined with raw-energy pair polish");
  if (options.decimation_scan && options.initial.empty())
    throw std::runtime_error("decimation scan requires an initial checkpoint");
  if (options.decimation_scan && !raw_energy_score)
    throw std::runtime_error("decimation scan uses exact raw-energy ranking");
  if (options.decimation_scan && options.pair_polish_size > 0)
    throw std::runtime_error("decimation scan cannot be combined with pair polish");
  if (options.same_sequence_pair_scan && options.initial.empty())
    throw std::runtime_error(
        "same-sequence pair scan requires an initial checkpoint");
  if (options.same_sequence_pair_scan && !raw_energy_score)
    throw std::runtime_error(
        "same-sequence pair scan uses invariant residual metrics");
  if (options.same_sequence_pair_scan && options.pair_polish_size > 0)
    throw std::runtime_error(
        "same-sequence pair scan cannot be combined with pair polish");
  if (options.cross_sequence_pair_scan && options.initial.empty())
    throw std::runtime_error(
        "cross-sequence pair scan requires an initial checkpoint");
  if (options.cross_sequence_pair_scan && !raw_energy_score)
    throw std::runtime_error(
        "cross-sequence pair scan uses invariant residual metrics");
  if (options.cross_sequence_pair_scan && options.pair_polish_size > 0)
    throw std::runtime_error(
        "cross-sequence pair scan cannot be combined with pair polish");
  if (options.window_half_size < 0 || options.window_half_size > 12)
    throw std::runtime_error("window scan half-size must lie in 0..12");
  if (options.paired_window_half_size < 0 ||
      options.paired_window_half_size > 6)
    throw std::runtime_error(
        "paired-window half-size must lie in 0..6");
  if (options.four_window_mitm_half_size < 0 ||
      options.four_window_mitm_half_size > 6)
    throw std::runtime_error(
        "four-window MITM half-size must lie in 0..6");
  if (options.mixed_window_mitm_half_size < 0 ||
      options.mixed_window_mitm_half_size > 6)
    throw std::runtime_error(
        "mixed-window MITM half-size must lie in 0..6");
  if (options.mixed_window_batch_size < 1 ||
      options.mixed_window_batch_size > 8)
    throw std::runtime_error("mixed-window batch size must lie in 1..8");
  if (options.window_family_count < 1 || options.window_family_count > 12)
    throw std::runtime_error("window family count must lie in 1..12");
  if (options.window_half_size > 0 && options.initial.empty())
    throw std::runtime_error("window scan requires an initial checkpoint");
  if (options.window_half_size > 0 && !raw_energy_score)
    throw std::runtime_error(
        "window scan tracks invariant metrics from a raw-score launch");
  if (options.window_half_size > 0 && options.pair_polish_size > 0)
    throw std::runtime_error(
        "window scan cannot be combined with pair polish");
  if (options.paired_window_half_size > 0 && options.initial.empty())
    throw std::runtime_error(
        "paired-window scan requires an initial checkpoint");
  if (options.paired_window_half_size > 0 && !raw_energy_score)
    throw std::runtime_error(
        "paired-window scan tracks invariant metrics from a raw-score launch");
  if (options.paired_window_half_size > 0 &&
      options.pair_polish_size > 0)
    throw std::runtime_error(
        "paired-window scan cannot be combined with pair polish");
  if (options.four_window_mitm_half_size > 0 && options.initial.empty())
    throw std::runtime_error(
        "four-window MITM requires an initial checkpoint");
  if (options.four_window_mitm_half_size > 0 && !raw_energy_score)
    throw std::runtime_error(
        "four-window MITM requires a raw-score launch");
  if (options.four_window_mitm_half_size > 0 &&
      options.pair_polish_size > 0)
    throw std::runtime_error(
        "four-window MITM cannot be combined with pair polish");
  if (options.mixed_window_mitm_half_size > 0 && options.initial.empty())
    throw std::runtime_error(
        "mixed-window MITM requires an initial checkpoint");
  if (options.mixed_window_mitm_half_size > 0 && !raw_energy_score)
    throw std::runtime_error(
        "mixed-window MITM requires a raw-score launch");
  if (options.mixed_window_mitm_half_size > 0 &&
      options.pair_polish_size > 0)
    throw std::runtime_error(
        "mixed-window MITM cannot be combined with pair polish");
  if (options.mixed_window_mitm_half_size == 0 &&
      (options.mixed_window_batch_size != 8 ||
       options.mixed_window_batch_start != 0 ||
       options.mixed_window_batch_count != 0))
    throw std::runtime_error(
        "mixed-window batch options require mixed-window MITM");
  const int exact_scan_modes = static_cast<int>(options.decimation_scan) +
                               static_cast<int>(options.same_sequence_pair_scan) +
                               static_cast<int>(options.cross_sequence_pair_scan) +
                               static_cast<int>(options.window_half_size > 0) +
                               static_cast<int>(
                                   options.paired_window_half_size > 0) +
                               static_cast<int>(
                                   options.four_window_mitm_half_size > 0) +
                               static_cast<int>(
                                   options.mixed_window_mitm_half_size > 0);
  if (exact_scan_modes > 1)
    throw std::runtime_error("select only one exact scan mode");
  if (options.scan_objective != "energy" &&
      options.scan_objective != "quartic" &&
      options.scan_objective != "maximum")
    throw std::runtime_error(
        "scan objective must be energy, quartic, or maximum");
  return options;
}

void self_test() {
  std::mt19937_64 rng(668);
  std::uniform_int_distribution<int> sequence_choice(0, SEQUENCES - 1);
  for (int profile = 0; profile < static_cast<int>(PROFILES.size()); ++profile) {
    State state = random_state(profile, rng);
    for (int trial = 0; trial < 1000; ++trial) {
      const int which = sequence_choice(rng);
      const auto [left, right] = random_exchange(state.sequence[which], rng);
      const auto delta = exchange_deltas(state.sequence[which], left, right);
      std::int64_t new_quartic = 0;
      const std::int64_t new_energy =
          exchanged_energy(state, delta, nullptr, &new_quartic);
      const int new_bad_lags = exchanged_bad_lags(state, delta);
      apply_exchange(state, which, left, right, delta, new_energy);
      validate(state);
      if (bad_lags(state) != new_bad_lags)
        throw std::runtime_error("incremental bad-lag mismatch");
      if (search_score(new_energy, new_quartic, new_bad_lags,
                       ScoreWeights{2, 3, 5}) !=
          search_score(state.energy, quartic_energy(state.residual),
                       bad_lags(state), ScoreWeights{2, 3, 5}))
        throw std::runtime_error("incremental search-score mismatch");
    }
    for (int trial = 0; trial < 100; ++trial) {
      std::array<int, SEQUENCES> order{{0, 1, 2, 3}};
      std::shuffle(order.begin(), order.end(), rng);
      std::array<int, SEQUENCES> left{};
      std::array<int, SEQUENCES> right{};
      std::array<int, HALF + 1> combined{};
      for (int move = 0; move < 2; ++move) {
        const auto endpoints = random_exchange(state.sequence[order[move]], rng);
        left[move] = endpoints.first;
        right[move] = endpoints.second;
        const auto delta = exchange_deltas(
            state.sequence[order[move]], left[move], right[move]);
        for (int lag = 1; lag <= HALF; ++lag) combined[lag] += delta[lag];
      }
      std::int64_t new_quartic = 0;
      const std::int64_t new_energy =
          exchanged_energy(state, combined, nullptr, &new_quartic);
      const int new_bad_lags = exchanged_bad_lags(state, combined);
      apply_compound_exchange(
          state, order, left, right, 2, combined, new_energy);
      validate(state);
      if (bad_lags(state) != new_bad_lags)
        throw std::runtime_error("compound bad-lag mismatch");
      if (search_score(new_energy, new_quartic, new_bad_lags,
                       ScoreWeights{2, 3, 5}) !=
          search_score(state.energy, quartic_energy(state.residual),
                       bad_lags(state), ScoreWeights{2, 3, 5}))
        throw std::runtime_error("compound search-score mismatch");
    }
    for (int trial = 0; trial < 10; ++trial) {
      const int which = sequence_choice(rng);
      std::vector<int> plus_positions;
      std::vector<int> minus_positions;
      for (int position = 0; position < N; ++position) {
        if (state.sequence[which][position] == 1)
          plus_positions.push_back(position);
        else
          minus_positions.push_back(position);
      }
      std::shuffle(plus_positions.begin(), plus_positions.end(), rng);
      std::shuffle(minus_positions.begin(), minus_positions.end(), rng);
      const std::array<int, 4> positions{{
          plus_positions[0], plus_positions[1],
          minus_positions[0], minus_positions[1]}};
      Residuals predicted = state.residual;
      const Residuals delta = same_sequence_double_exchange_deltas(
          state.sequence[which], positions);
      for (int lag = 1; lag <= HALF; ++lag)
        predicted[lag] += delta[lag];
      State changed = state;
      const std::int64_t changed_energy = exchanged_energy(state, delta);
      apply_same_sequence_double_exchange(
          changed, which, positions, delta, changed_energy);
      if (predicted != changed.residual)
        throw std::runtime_error(
            "same-sequence compound interaction mismatch");
      validate(changed);
    }
  }
  if (search_score(64, 136, 46, ScoreWeights{1, 0, 2}) != 156)
    throw std::runtime_error("bad-lag search-score self-test failed");
  if (search_score(64, 136, 46, ScoreWeights{1, 0, 0}) != 64)
    throw std::runtime_error("zero-penalty search-score self-test failed");
  if (search_score(64, 136, 46, ScoreWeights{0, 1, 0}) != 136)
    throw std::runtime_error("quartic search-score self-test failed");
  if (search_score(64, 136, 46, ScoreWeights{4, 1, 0}) != 392)
    throw std::runtime_error("mixed search-score self-test failed");
  State polished = random_state(5, rng);
  best_pair_descent(polished, 8, 1, 3);
  validate(polished);
  std::cout << "PASS: 10000 single, 1000 cross-sequence compound, and 100 "
               "same-sequence compound delta checks; pair polish validates\n";
}

using PafTable = std::array<std::array<int, N>, SEQUENCES>;

struct DecimationMetrics {
  std::int64_t energy = 0;
  std::int64_t quartic = 0;
  int bad_lags = 0;
  int maximum_quarter_residual = 0;
  Profile multipliers{{1, 1, 1, 1}};
};

PafTable individual_periodic_correlations(const Quadruple &quadruple) {
  PafTable result{};
  for (int which = 0; which < SEQUENCES; ++which)
    for (int lag = 0; lag < N; ++lag)
      result[which][lag] = periodic_correlation(quadruple[which], lag);
  return result;
}

DecimationMetrics decimation_metrics(const PafTable &paf,
                                      const Profile &multipliers) {
  DecimationMetrics result;
  result.multipliers = multipliers;
  for (int lag = 1; lag <= HALF; ++lag) {
    int residual = 0;
    for (int which = 0; which < SEQUENCES; ++which)
      residual += paf[which][(multipliers[which] * lag) % N];
    if (residual % 4 != 0)
      throw std::runtime_error("decimation residual is not divisible by four");
    const std::int64_t value = residual / 4;
    const std::int64_t square = value * value;
    result.energy += square;
    result.quartic += square * square;
    result.bad_lags += value != 0;
    result.maximum_quarter_residual = std::max(
        result.maximum_quarter_residual,
        static_cast<int>(std::abs(value)));
  }
  return result;
}

State decimated_state(const State &source, const Profile &multipliers) {
  State result;
  result.profile = source.profile;
  for (int which = 0; which < SEQUENCES; ++which)
    for (int index = 0; index < N; ++index)
      result.sequence[which][index] =
          source.sequence[which][(multipliers[which] * index) % N];
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

void print_decimation_metrics(std::string_view label,
                              const DecimationMetrics &metrics) {
  std::cout << label << " energy=" << metrics.energy
            << " quartic=" << metrics.quartic
            << " bad_lags=" << metrics.bad_lags
            << " maximum_quarter_residual="
            << metrics.maximum_quarter_residual << " multipliers=("
            << metrics.multipliers[0] << ',' << metrics.multipliers[1] << ','
            << metrics.multipliers[2] << ',' << metrics.multipliers[3]
            << ")\n";
}

int run_decimation_scan(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const PafTable paf = individual_periodic_correlations(source.sequence);
  const Profile identity{{1, 1, 1, 1}};
  const DecimationMetrics initial = decimation_metrics(paf, identity);
  DecimationMetrics best_energy = initial;
  DecimationMetrics best_quartic = initial;
  DecimationMetrics best_bad_lags = initial;
  DecimationMetrics best_maximum = initial;
  std::uint64_t energy_ties = 0;
  std::uint64_t quartic_ties = 0;
  std::uint64_t maximum_ties = 0;
  std::uint64_t cases = 0;

  // PAF_x(d*k) is unchanged when d is replaced by -d, leaving 83 multiplier
  // classes.  A common multiplier only permutes the 83 lags, so normalize the
  // first multiplier to one and exhaust the remaining 83^3 classes.
  for (int second = 1; second <= HALF; ++second) {
    for (int third = 1; third <= HALF; ++third) {
      for (int fourth = 1; fourth <= HALF; ++fourth) {
        const Profile multipliers{{1, second, third, fourth}};
        const DecimationMetrics candidate =
            decimation_metrics(paf, multipliers);
        ++cases;
        const auto energy_key = std::tie(
            candidate.energy, candidate.quartic,
            candidate.maximum_quarter_residual, candidate.bad_lags);
        const auto best_energy_key = std::tie(
            best_energy.energy, best_energy.quartic,
            best_energy.maximum_quarter_residual, best_energy.bad_lags);
        if (energy_key < best_energy_key) {
          best_energy = candidate;
          energy_ties = 1;
        } else if (energy_key == best_energy_key) {
          ++energy_ties;
        }
        const auto quartic_key = std::tie(
            candidate.quartic, candidate.energy,
            candidate.maximum_quarter_residual, candidate.bad_lags);
        const auto best_quartic_key = std::tie(
            best_quartic.quartic, best_quartic.energy,
            best_quartic.maximum_quarter_residual, best_quartic.bad_lags);
        if (quartic_key < best_quartic_key) {
          best_quartic = candidate;
          quartic_ties = 1;
        } else if (quartic_key == best_quartic_key) {
          ++quartic_ties;
        }
        if (std::tie(candidate.bad_lags, candidate.energy,
                     candidate.quartic,
                     candidate.maximum_quarter_residual) <
            std::tie(best_bad_lags.bad_lags, best_bad_lags.energy,
                     best_bad_lags.quartic,
                     best_bad_lags.maximum_quarter_residual))
          best_bad_lags = candidate;
        const auto maximum_key = std::tie(
            candidate.maximum_quarter_residual, candidate.quartic,
            candidate.energy, candidate.bad_lags);
        const auto best_maximum_key = std::tie(
            best_maximum.maximum_quarter_residual, best_maximum.quartic,
            best_maximum.energy, best_maximum.bad_lags);
        if (maximum_key < best_maximum_key) {
          best_maximum = candidate;
          maximum_ties = 1;
        } else if (maximum_key == best_maximum_key) {
          ++maximum_ties;
        }
      }
    }
  }

  if (cases != static_cast<std::uint64_t>(HALF) * HALF * HALF)
    throw std::runtime_error("decimation scan case-count mismatch");
  const DecimationMetrics *selected = &best_energy;
  if (options.scan_objective == "quartic") selected = &best_quartic;
  if (options.scan_objective == "maximum") selected = &best_maximum;
  const State best = decimated_state(source, selected->multipliers);
  const DecimationMetrics materialized =
      decimation_metrics(individual_periodic_correlations(best.sequence),
                         identity);
  if (materialized.energy != selected->energy ||
      materialized.quartic != selected->quartic ||
      materialized.bad_lags != selected->bad_lags ||
      materialized.maximum_quarter_residual !=
          selected->maximum_quarter_residual)
    throw std::runtime_error("materialized decimation metrics mismatch");

  const bool exact = best.energy == 0;
  write_checkpoint(
      options.output, best, options.seed, cases, exact, ScoreWeights{});
  std::cout << "DECIMATION_SCAN cases=" << cases << '\n';
  print_decimation_metrics("INITIAL", initial);
  print_decimation_metrics("BEST_ENERGY", best_energy);
  print_decimation_metrics("BEST_QUARTIC", best_quartic);
  print_decimation_metrics("BEST_BAD_LAGS", best_bad_lags);
  print_decimation_metrics("BEST_MAXIMUM", best_maximum);
  std::cout << "TIES energy=" << energy_ties
            << " quartic=" << quartic_ties
            << " maximum=" << maximum_ties << '\n';
  std::cout << "SELECTED objective=" << options.scan_objective << '\n';
  std::cout << (exact ? "FOUND" : "DONE")
            << " decimation output=" << options.output << '\n';
  return exact ? 0 : 1;
}

struct ResidualMetrics {
  std::int64_t energy = 0;
  std::int64_t quartic = 0;
  int bad_lags = 0;
  int maximum_quarter_residual = 0;
};

struct SameSequenceMove {
  int which = -1;
  std::array<int, 4> positions{{-1, -1, -1, -1}};
};

struct NeighborhoodChampion {
  ResidualMetrics metrics;
  SameSequenceMove move;
  std::uint64_t ties = 1;
};

struct SameSignFlipPair {
  int first = -1;
  int second = -1;
  Residuals delta{};
};

ResidualMetrics residual_metrics(const Residuals &residual) {
  ResidualMetrics result;
  for (int lag = 1; lag <= HALF; ++lag) {
    if (residual[lag] % 4 != 0)
      throw std::runtime_error("residual metric is not divisible by four");
    const std::int64_t value = residual[lag] / 4;
    const std::int64_t square = value * value;
    result.energy += square;
    result.quartic += square * square;
    result.bad_lags += value != 0;
    result.maximum_quarter_residual = std::max(
        result.maximum_quarter_residual,
        static_cast<int>(std::abs(value)));
  }
  return result;
}

std::vector<SameSignFlipPair> same_sign_flip_pairs(
    const Sequence &sequence, std::int8_t sign) {
  std::vector<int> positions;
  positions.reserve(N);
  for (int index = 0; index < N; ++index)
    if (sequence[index] == sign) positions.push_back(index);
  std::vector<SameSignFlipPair> result;
  result.reserve(positions.size() * (positions.size() - 1) / 2);
  for (std::size_t first = 0; first < positions.size(); ++first) {
    for (std::size_t second = first + 1; second < positions.size(); ++second) {
      SameSignFlipPair pair;
      pair.first = positions[first];
      pair.second = positions[second];
      pair.delta = two_flip_deltas(sequence, pair.first, pair.second);
      result.push_back(pair);
    }
  }
  return result;
}

void update_neighborhood_champions(
    const ResidualMetrics &candidate, const SameSequenceMove &move,
    NeighborhoodChampion &best_energy, NeighborhoodChampion &best_quartic,
    NeighborhoodChampion &best_maximum) {
  const auto energy_key = std::tie(
      candidate.energy, candidate.quartic,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_energy_key = std::tie(
      best_energy.metrics.energy, best_energy.metrics.quartic,
      best_energy.metrics.maximum_quarter_residual,
      best_energy.metrics.bad_lags);
  if (energy_key < best_energy_key) {
    best_energy = {candidate, move, 1};
  } else if (energy_key == best_energy_key) {
    ++best_energy.ties;
  }

  const auto quartic_key = std::tie(
      candidate.quartic, candidate.energy,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_quartic_key = std::tie(
      best_quartic.metrics.quartic, best_quartic.metrics.energy,
      best_quartic.metrics.maximum_quarter_residual,
      best_quartic.metrics.bad_lags);
  if (quartic_key < best_quartic_key) {
    best_quartic = {candidate, move, 1};
  } else if (quartic_key == best_quartic_key) {
    ++best_quartic.ties;
  }

  const auto maximum_key = std::tie(
      candidate.maximum_quarter_residual, candidate.quartic,
      candidate.energy, candidate.bad_lags);
  const auto best_maximum_key = std::tie(
      best_maximum.metrics.maximum_quarter_residual,
      best_maximum.metrics.quartic, best_maximum.metrics.energy,
      best_maximum.metrics.bad_lags);
  if (maximum_key < best_maximum_key) {
    best_maximum = {candidate, move, 1};
  } else if (maximum_key == best_maximum_key) {
    ++best_maximum.ties;
  }
}

void print_neighborhood_champion(std::string_view label,
                                 const NeighborhoodChampion &champion) {
  std::cout << label << " energy=" << champion.metrics.energy
            << " quartic=" << champion.metrics.quartic
            << " bad_lags=" << champion.metrics.bad_lags
            << " maximum_quarter_residual="
            << champion.metrics.maximum_quarter_residual
            << " lexicographic_ties_including_incumbent=" << champion.ties
            << " sequence=" << champion.move.which << " positions=("
            << champion.move.positions[0] << ',' << champion.move.positions[1]
            << ',' << champion.move.positions[2] << ','
            << champion.move.positions[3] << ")\n";
}

State state_after_same_sequence_move(const State &source,
                                     const SameSequenceMove &move) {
  State result = source;
  if (move.which >= 0)
    for (int position : move.positions)
      result.sequence[move.which][position] *= -1;
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

int run_same_sequence_pair_scan(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const ResidualMetrics initial = residual_metrics(source.residual);
  NeighborhoodChampion best_energy{initial, {}, 1};
  NeighborhoodChampion best_quartic{initial, {}, 1};
  NeighborhoodChampion best_maximum{initial, {}, 1};
  std::uint64_t raw_energy_ties = 1;
  std::uint64_t raw_quartic_ties = 1;
  std::uint64_t raw_maximum_ties = 1;
  std::uint64_t cases = 0;

  for (int which = 0; which < SEQUENCES; ++which) {
    const auto plus_pairs =
        same_sign_flip_pairs(source.sequence[which], 1);
    const auto minus_pairs =
        same_sign_flip_pairs(source.sequence[which], -1);
    const std::uint64_t expected =
        static_cast<std::uint64_t>(plus_pairs.size()) * minus_pairs.size();
    std::uint64_t block_cases = 0;
    std::array<std::uint64_t, HALF + 1> correction_stamp{};
    std::array<int, HALF + 1> correction{};
    std::uint64_t stamp = 0;

    for (const SameSignFlipPair &plus : plus_pairs) {
      for (const SameSignFlipPair &minus : minus_pairs) {
        ++stamp;
        const std::array<int, 2> plus_positions{{plus.first, plus.second}};
        const std::array<int, 2> minus_positions{{minus.first, minus.second}};
        for (int plus_position : plus_positions) {
          for (int minus_position : minus_positions) {
            int lag = std::abs(plus_position - minus_position);
            if (lag > HALF) lag = N - lag;
            if (correction_stamp[lag] != stamp) {
              correction_stamp[lag] = stamp;
              correction[lag] = 0;
            }
            // plus.delta + minus.delta treats each cross pair as singly
            // flipped twice.  Adding 4*x_p*x_q restores the unchanged product
            // when all four endpoints flip simultaneously.
            correction[lag] +=
                4 * source.sequence[which][plus_position] *
                source.sequence[which][minus_position];
          }
        }

        ResidualMetrics candidate;
        for (int lag = 1; lag <= HALF; ++lag) {
          int updated = source.residual[lag] + plus.delta[lag] +
                        minus.delta[lag];
          if (correction_stamp[lag] == stamp)
            updated += correction[lag];
          if (updated % 4 != 0)
            throw std::runtime_error(
                "same-sequence compound residual is not divisible by four");
          const std::int64_t value = updated / 4;
          const std::int64_t square = value * value;
          candidate.energy += square;
          candidate.quartic += square * square;
          candidate.bad_lags += value != 0;
          candidate.maximum_quarter_residual = std::max(
              candidate.maximum_quarter_residual,
              static_cast<int>(std::abs(value)));
        }
        const SameSequenceMove move{
            which,
            {{plus.first, plus.second, minus.first, minus.second}}};
        if (candidate.energy < best_energy.metrics.energy)
          raw_energy_ties = 1;
        else if (candidate.energy == best_energy.metrics.energy)
          ++raw_energy_ties;
        if (candidate.quartic < best_quartic.metrics.quartic)
          raw_quartic_ties = 1;
        else if (candidate.quartic == best_quartic.metrics.quartic)
          ++raw_quartic_ties;
        if (candidate.maximum_quarter_residual <
            best_maximum.metrics.maximum_quarter_residual)
          raw_maximum_ties = 1;
        else if (candidate.maximum_quarter_residual ==
                 best_maximum.metrics.maximum_quarter_residual)
          ++raw_maximum_ties;
        update_neighborhood_champions(
            candidate, move, best_energy, best_quartic, best_maximum);
        ++block_cases;
      }
    }
    if (block_cases != expected)
      throw std::runtime_error("same-sequence block case-count mismatch");
    cases += block_cases;
    std::cout << "SAME_SEQUENCE_BLOCK sequence=" << which
              << " plus_pairs=" << plus_pairs.size()
              << " minus_pairs=" << minus_pairs.size()
              << " cases=" << block_cases << '\n';
    std::cout.flush();
  }
  if (source.profile == 5 && cases != 46'884'138)
    throw std::runtime_error(
        "profile-5 same-sequence aggregate count mismatch");

  const NeighborhoodChampion *selected = &best_energy;
  if (options.scan_objective == "quartic") selected = &best_quartic;
  if (options.scan_objective == "maximum") selected = &best_maximum;
  const State best = state_after_same_sequence_move(source, selected->move);
  const ResidualMetrics materialized = residual_metrics(best.residual);
  if (std::tie(materialized.energy, materialized.quartic,
               materialized.bad_lags,
               materialized.maximum_quarter_residual) !=
      std::tie(selected->metrics.energy, selected->metrics.quartic,
               selected->metrics.bad_lags,
               selected->metrics.maximum_quarter_residual))
    throw std::runtime_error(
        "materialized same-sequence scan metrics mismatch");
  const bool exact = best.energy == 0;
  write_checkpoint(
      options.output, best, options.seed, cases, exact, ScoreWeights{});
  std::cout << "SAME_SEQUENCE_PAIR_SCAN cases=" << cases << '\n';
  print_neighborhood_champion("INITIAL",
      NeighborhoodChampion{initial, {}, 1});
  print_neighborhood_champion("BEST_ENERGY", best_energy);
  print_neighborhood_champion("BEST_QUARTIC", best_quartic);
  print_neighborhood_champion("BEST_MAXIMUM", best_maximum);
  std::cout << "PRIMARY_TIES_INCLUDING_INCUMBENT energy=" << raw_energy_ties
            << " quartic=" << raw_quartic_ties
            << " maximum=" << raw_maximum_ties << '\n';
  std::cout << "SELECTED objective=" << options.scan_objective << '\n';
  std::cout << (exact ? "FOUND" : "DONE")
            << " same-sequence-pair output=" << options.output << '\n';
  return exact ? 0 : 1;
}

struct CrossSequenceMove {
  int first_sequence = -1;
  int first_left = -1;
  int first_right = -1;
  int second_sequence = -1;
  int second_left = -1;
  int second_right = -1;
};

struct CrossNeighborhoodChampion {
  ResidualMetrics metrics;
  CrossSequenceMove move;
  std::uint64_t ties = 1;
};

void update_cross_champions(
    const ResidualMetrics &candidate, const CrossSequenceMove &move,
    CrossNeighborhoodChampion &best_energy,
    CrossNeighborhoodChampion &best_quartic,
    CrossNeighborhoodChampion &best_maximum) {
  const auto energy_key = std::tie(
      candidate.energy, candidate.quartic,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_energy_key = std::tie(
      best_energy.metrics.energy, best_energy.metrics.quartic,
      best_energy.metrics.maximum_quarter_residual,
      best_energy.metrics.bad_lags);
  if (energy_key < best_energy_key) {
    best_energy = {candidate, move, 1};
  } else if (energy_key == best_energy_key) {
    ++best_energy.ties;
  }

  const auto quartic_key = std::tie(
      candidate.quartic, candidate.energy,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_quartic_key = std::tie(
      best_quartic.metrics.quartic, best_quartic.metrics.energy,
      best_quartic.metrics.maximum_quarter_residual,
      best_quartic.metrics.bad_lags);
  if (quartic_key < best_quartic_key) {
    best_quartic = {candidate, move, 1};
  } else if (quartic_key == best_quartic_key) {
    ++best_quartic.ties;
  }

  const auto maximum_key = std::tie(
      candidate.maximum_quarter_residual, candidate.quartic,
      candidate.energy, candidate.bad_lags);
  const auto best_maximum_key = std::tie(
      best_maximum.metrics.maximum_quarter_residual,
      best_maximum.metrics.quartic, best_maximum.metrics.energy,
      best_maximum.metrics.bad_lags);
  if (maximum_key < best_maximum_key) {
    best_maximum = {candidate, move, 1};
  } else if (maximum_key == best_maximum_key) {
    ++best_maximum.ties;
  }
}

void print_cross_champion(std::string_view label,
                          const CrossNeighborhoodChampion &champion) {
  std::cout << label << " energy=" << champion.metrics.energy
            << " quartic=" << champion.metrics.quartic
            << " bad_lags=" << champion.metrics.bad_lags
            << " maximum_quarter_residual="
            << champion.metrics.maximum_quarter_residual
            << " lexicographic_ties_including_incumbent=" << champion.ties
            << " first=(" << champion.move.first_sequence << ','
            << champion.move.first_left << ',' << champion.move.first_right
            << ") second=(" << champion.move.second_sequence << ','
            << champion.move.second_left << ','
            << champion.move.second_right << ")\n";
}

State state_after_cross_sequence_move(const State &source,
                                      const CrossSequenceMove &move) {
  State result = source;
  if (move.first_sequence >= 0)
    std::swap(result.sequence[move.first_sequence][move.first_left],
              result.sequence[move.first_sequence][move.first_right]);
  if (move.second_sequence >= 0)
    std::swap(result.sequence[move.second_sequence][move.second_left],
              result.sequence[move.second_sequence][move.second_right]);
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

int run_cross_sequence_pair_scan(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const ResidualMetrics initial = residual_metrics(source.residual);
  CrossNeighborhoodChampion best_energy{initial, {}, 1};
  CrossNeighborhoodChampion best_quartic{initial, {}, 1};
  CrossNeighborhoodChampion best_maximum{initial, {}, 1};
  std::uint64_t raw_energy_ties = 1;
  std::uint64_t raw_quartic_ties = 1;
  std::uint64_t raw_maximum_ties = 1;
  std::array<std::vector<ExchangeMove>, SEQUENCES> pools;
  std::uint64_t single_cases = 0;
  for (int which = 0; which < SEQUENCES; ++which) {
    pools[which] = best_exchange_moves(source, which, 8192);
    const int plus = (N + row_sum(source.sequence[which])) / 2;
    const int minus = N - plus;
    const std::uint64_t expected_exchanges =
        static_cast<std::uint64_t>(plus) * minus;
    if (pools[which].size() != expected_exchanges)
      throw std::runtime_error(
          "cross-sequence exchange pool is not exhaustive");
    single_cases += pools[which].size();
    for (const ExchangeMove &move : pools[which]) {
      Residuals residual = source.residual;
      for (int lag = 1; lag <= HALF; ++lag)
        residual[lag] += move.delta[lag];
      const CrossSequenceMove description{
          which, move.left, move.right, -1, -1, -1};
      const ResidualMetrics candidate = residual_metrics(residual);
      if (candidate.energy < best_energy.metrics.energy)
        raw_energy_ties = 1;
      else if (candidate.energy == best_energy.metrics.energy)
        ++raw_energy_ties;
      if (candidate.quartic < best_quartic.metrics.quartic)
        raw_quartic_ties = 1;
      else if (candidate.quartic == best_quartic.metrics.quartic)
        ++raw_quartic_ties;
      if (candidate.maximum_quarter_residual <
          best_maximum.metrics.maximum_quarter_residual)
        raw_maximum_ties = 1;
      else if (candidate.maximum_quarter_residual ==
               best_maximum.metrics.maximum_quarter_residual)
        ++raw_maximum_ties;
      update_cross_champions(candidate, description,
                             best_energy, best_quartic, best_maximum);
    }
  }

  std::uint64_t pair_cases = 0;
  for (int first_sequence = 0; first_sequence < SEQUENCES;
       ++first_sequence) {
    for (int second_sequence = first_sequence + 1;
         second_sequence < SEQUENCES; ++second_sequence) {
      const std::uint64_t expected =
          static_cast<std::uint64_t>(pools[first_sequence].size()) *
          pools[second_sequence].size();
      std::uint64_t block_cases = 0;
      for (const ExchangeMove &first : pools[first_sequence]) {
        for (const ExchangeMove &second : pools[second_sequence]) {
          ResidualMetrics candidate;
          bool competitive = true;
          for (int lag = 1; lag <= HALF; ++lag) {
            const int updated = source.residual[lag] + first.delta[lag] +
                                second.delta[lag];
            if (updated % 4 != 0)
              throw std::runtime_error(
                  "cross-sequence residual is not divisible by four");
            const std::int64_t value = updated / 4;
            const std::int64_t square = value * value;
            candidate.energy += square;
            candidate.quartic += square * square;
            candidate.bad_lags += value != 0;
            candidate.maximum_quarter_residual = std::max(
                candidate.maximum_quarter_residual,
                static_cast<int>(std::abs(value)));
            const bool energy_possible =
                candidate.energy <= best_energy.metrics.energy;
            const bool quartic_possible =
                candidate.quartic <= best_quartic.metrics.quartic;
            const bool maximum_possible =
                candidate.maximum_quarter_residual <=
                best_maximum.metrics.maximum_quarter_residual;
            // All three partial metrics are monotone in the remaining lags.
            // Once none can tie or improve its incumbent, exact early exit is
            // safe and does not omit a primary tie.
            if (!energy_possible && !quartic_possible &&
                !maximum_possible) {
              competitive = false;
              break;
            }
          }
          if (competitive) {
            const CrossSequenceMove description{
                first_sequence, first.left, first.right,
                second_sequence, second.left, second.right};
            if (candidate.energy < best_energy.metrics.energy)
              raw_energy_ties = 1;
            else if (candidate.energy == best_energy.metrics.energy)
              ++raw_energy_ties;
            if (candidate.quartic < best_quartic.metrics.quartic)
              raw_quartic_ties = 1;
            else if (candidate.quartic == best_quartic.metrics.quartic)
              ++raw_quartic_ties;
            if (candidate.maximum_quarter_residual <
                best_maximum.metrics.maximum_quarter_residual)
              raw_maximum_ties = 1;
            else if (candidate.maximum_quarter_residual ==
                     best_maximum.metrics.maximum_quarter_residual)
              ++raw_maximum_ties;
            update_cross_champions(candidate, description, best_energy,
                                   best_quartic, best_maximum);
          }
          ++block_cases;
        }
      }
      if (block_cases != expected)
        throw std::runtime_error("cross-sequence block case-count mismatch");
      pair_cases += block_cases;
      std::cout << "CROSS_SEQUENCE_BLOCK first=" << first_sequence
                << " second=" << second_sequence
                << " cases=" << block_cases << '\n';
      std::cout.flush();
    }
  }
  if (source.profile == 5 &&
      (single_cases != 27'722 || pair_cases != 288'185'440))
    throw std::runtime_error(
        "profile-5 cross-sequence aggregate count mismatch");

  const CrossNeighborhoodChampion *selected = &best_energy;
  if (options.scan_objective == "quartic") selected = &best_quartic;
  if (options.scan_objective == "maximum") selected = &best_maximum;
  const State best = state_after_cross_sequence_move(source, selected->move);
  const ResidualMetrics materialized = residual_metrics(best.residual);
  if (std::tie(materialized.energy, materialized.quartic,
               materialized.bad_lags,
               materialized.maximum_quarter_residual) !=
      std::tie(selected->metrics.energy, selected->metrics.quartic,
               selected->metrics.bad_lags,
               selected->metrics.maximum_quarter_residual))
    throw std::runtime_error(
        "materialized cross-sequence scan metrics mismatch");
  const bool exact = best.energy == 0;
  write_checkpoint(options.output, best, options.seed,
                   single_cases + pair_cases, exact, ScoreWeights{});
  std::cout << "CROSS_SEQUENCE_PAIR_SCAN singles=" << single_cases
            << " pairs=" << pair_cases << '\n';
  print_cross_champion("INITIAL",
      CrossNeighborhoodChampion{initial, {}, 1});
  print_cross_champion("BEST_ENERGY", best_energy);
  print_cross_champion("BEST_QUARTIC", best_quartic);
  print_cross_champion("BEST_MAXIMUM", best_maximum);
  std::cout << "PRIMARY_TIES_INCLUDING_INCUMBENT energy=" << raw_energy_ties
            << " quartic=" << raw_quartic_ties
            << " maximum=" << raw_maximum_ties << '\n';
  std::cout << "SELECTED objective=" << options.scan_objective << '\n';
  std::cout << (exact ? "FOUND" : "DONE")
            << " cross-sequence-pair output=" << options.output << '\n';
  return exact ? 0 : 1;
}

struct WindowExchange {
  std::int64_t quartic = 0;
  std::int64_t energy = 0;
  int left = -1;
  int right = -1;
};

struct WindowChampion {
  ResidualMetrics metrics;
  State state;
  int changed_sequence = -1;
  int window_family = -1;
  std::uint64_t ties = 1;
};

std::uint64_t binomial(int n, int k) {
  if (k < 0 || k > n) return 0;
  k = std::min(k, n - k);
  std::uint64_t result = 1;
  for (int index = 1; index <= k; ++index)
    result = result * static_cast<std::uint64_t>(n - k + index) /
             static_cast<std::uint64_t>(index);
  return result;
}

std::pair<std::vector<int>, std::vector<int>> guided_window(
    const State &source, int which, int half_size,
    const std::array<bool, N> &excluded) {
  std::vector<WindowExchange> exchanges;
  exchanges.reserve(7000);
  for (int left = 0; left < N; ++left) {
    for (int right = left + 1; right < N; ++right) {
      if (source.sequence[which][left] == source.sequence[which][right])
        continue;
      const Residuals delta =
          exchange_deltas(source.sequence[which], left, right);
      std::int64_t candidate_quartic = 0;
      const std::int64_t candidate_energy =
          exchanged_energy(source, delta, nullptr, &candidate_quartic);
      exchanges.push_back(
          {candidate_quartic, candidate_energy, left, right});
    }
  }
  std::sort(exchanges.begin(), exchanges.end(),
            [](const WindowExchange &left, const WindowExchange &right) {
              return std::tie(left.quartic, left.energy, left.left,
                              left.right) <
                     std::tie(right.quartic, right.energy, right.left,
                              right.right);
            });
  std::array<bool, N> selected{};
  std::vector<int> plus;
  std::vector<int> minus;
  plus.reserve(half_size);
  minus.reserve(half_size);
  for (const WindowExchange &exchange : exchanges) {
    const std::array<int, 2> endpoints{{exchange.left, exchange.right}};
    for (int position : endpoints) {
      if (excluded[position] || selected[position]) continue;
      std::vector<int> &target =
          source.sequence[which][position] == 1 ? plus : minus;
      if (static_cast<int>(target.size()) == half_size) continue;
      target.push_back(position);
      selected[position] = true;
    }
    if (static_cast<int>(plus.size()) == half_size &&
        static_cast<int>(minus.size()) == half_size)
      break;
  }
  if (static_cast<int>(plus.size()) != half_size ||
      static_cast<int>(minus.size()) != half_size)
    throw std::runtime_error("could not fill a guided window");
  std::sort(plus.begin(), plus.end());
  std::sort(minus.begin(), minus.end());
  return {plus, minus};
}

void update_window_champions(
    const ResidualMetrics &candidate, const State &state, int which,
    int family,
    WindowChampion &best_energy, WindowChampion &best_quartic,
    WindowChampion &best_maximum) {
  const auto energy_key = std::tie(
      candidate.energy, candidate.quartic,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_energy_key = std::tie(
      best_energy.metrics.energy, best_energy.metrics.quartic,
      best_energy.metrics.maximum_quarter_residual,
      best_energy.metrics.bad_lags);
  if (energy_key < best_energy_key) {
    best_energy = {candidate, state, which, family, 1};
  } else if (energy_key == best_energy_key) {
    ++best_energy.ties;
  }

  const auto quartic_key = std::tie(
      candidate.quartic, candidate.energy,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_quartic_key = std::tie(
      best_quartic.metrics.quartic, best_quartic.metrics.energy,
      best_quartic.metrics.maximum_quarter_residual,
      best_quartic.metrics.bad_lags);
  if (quartic_key < best_quartic_key) {
    best_quartic = {candidate, state, which, family, 1};
  } else if (quartic_key == best_quartic_key) {
    ++best_quartic.ties;
  }

  const auto maximum_key = std::tie(
      candidate.maximum_quarter_residual, candidate.quartic,
      candidate.energy, candidate.bad_lags);
  const auto best_maximum_key = std::tie(
      best_maximum.metrics.maximum_quarter_residual,
      best_maximum.metrics.quartic, best_maximum.metrics.energy,
      best_maximum.metrics.bad_lags);
  if (maximum_key < best_maximum_key) {
    best_maximum = {candidate, state, which, family, 1};
  } else if (maximum_key == best_maximum_key) {
    ++best_maximum.ties;
  }
}

void print_window_champion(std::string_view label,
                           const WindowChampion &champion) {
  std::cout << label << " energy=" << champion.metrics.energy
            << " quartic=" << champion.metrics.quartic
            << " bad_lags=" << champion.metrics.bad_lags
            << " maximum_quarter_residual="
            << champion.metrics.maximum_quarter_residual
            << " lexicographic_ties=" << champion.ties
            << " changed_sequence=" << champion.changed_sequence
            << " window_family=" << champion.window_family << '\n';
}

int run_window_scan(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const int half_size = options.window_half_size;
  const int window_size = 2 * half_size;
  const std::uint64_t cases_per_block =
      binomial(window_size, half_size);
  const ResidualMetrics initial = residual_metrics(source.residual);
  WindowChampion best_energy{initial, source, -1, -1, 1};
  WindowChampion best_quartic{initial, source, -1, -1, 1};
  WindowChampion best_maximum{initial, source, -1, -1, 1};
  std::uint64_t evaluated = 0;
  std::uint64_t unique_cases = 1;
  std::uint64_t transition_exchanges = 0;
  std::array<std::array<bool, N>, SEQUENCES> excluded{};
  for (int which = 0; which < SEQUENCES; ++which) {
    const int plus = (N + row_sum(source.sequence[which])) / 2;
    const int minus = N - plus;
    const int required = half_size * options.window_family_count;
    if (plus < required || minus < required)
      throw std::runtime_error(
          "window families require more signs than the profile contains");
  }

  for (int family = 0; family < options.window_family_count; ++family) {
    for (int which = 0; which < SEQUENCES; ++which) {
      const auto [plus, minus] =
          guided_window(source, which, half_size, excluded[which]);
      for (int position : plus) excluded[which][position] = true;
      for (int position : minus) excluded[which][position] = true;
      std::vector<int> window = plus;
      window.insert(window.end(), minus.begin(), minus.end());
      std::cout << "WINDOW family=" << family << " sequence=" << which
                << " plus=(";
      for (int index = 0; index < half_size; ++index)
        std::cout << (index == 0 ? "" : ",") << plus[index];
      std::cout << ") minus=(";
      for (int index = 0; index < half_size; ++index)
        std::cout << (index == 0 ? "" : ",") << minus[index];
      std::cout << ")\n";
      std::cout.flush();

      State state = source;
      std::vector<int> combination(half_size);
      for (int index = 0; index < half_size; ++index)
        combination[index] = index;
      std::uint64_t block_cases = 0;
      while (true) {
        const ResidualMetrics candidate = residual_metrics(state.residual);
        if (candidate.energy != state.energy)
          throw std::runtime_error("window scan incremental energy mismatch");
        if (block_cases > 0)
          update_window_champions(candidate, state, which, family, best_energy,
                                  best_quartic, best_maximum);
        ++block_cases;

        int pivot = half_size - 1;
        while (pivot >= 0 &&
               combination[pivot] == window_size - half_size + pivot)
          --pivot;
        if (pivot < 0) break;
        std::vector<int> next = combination;
        ++next[pivot];
        for (int index = pivot + 1; index < half_size; ++index)
          next[index] = next[index - 1] + 1;
        std::array<bool, 24> current_set{};
        std::array<bool, 24> next_set{};
        for (int index : combination) current_set[index] = true;
        for (int index : next) next_set[index] = true;
        std::vector<int> leaving;
        std::vector<int> entering;
        for (int index = 0; index < window_size; ++index) {
          if (current_set[index] && !next_set[index]) leaving.push_back(index);
          if (!current_set[index] && next_set[index]) entering.push_back(index);
        }
        if (leaving.size() != entering.size())
          throw std::runtime_error("window transition cardinality mismatch");
        for (std::size_t exchange = 0; exchange < leaving.size(); ++exchange) {
          const int left = window[leaving[exchange]];
          const int right = window[entering[exchange]];
          const Residuals delta =
              exchange_deltas(state.sequence[which], left, right);
          const std::int64_t new_energy = exchanged_energy(state, delta);
          apply_exchange(state, which, left, right, delta, new_energy);
          ++transition_exchanges;
        }
        combination = std::move(next);
      }
      if (block_cases != cases_per_block)
        throw std::runtime_error("window scan case-count mismatch");
      evaluated += block_cases;
      unique_cases += block_cases - 1;
      validate(state);
      std::cout << "WINDOW_BLOCK family=" << family
                << " sequence=" << which
                << " cases=" << block_cases << '\n';
      std::cout.flush();
    }
  }

  const WindowChampion *selected = &best_energy;
  if (options.scan_objective == "quartic") selected = &best_quartic;
  if (options.scan_objective == "maximum") selected = &best_maximum;
  validate(selected->state);
  const ResidualMetrics materialized = residual_metrics(selected->state.residual);
  if (std::tie(materialized.energy, materialized.quartic,
               materialized.bad_lags,
               materialized.maximum_quarter_residual) !=
      std::tie(selected->metrics.energy, selected->metrics.quartic,
               selected->metrics.bad_lags,
               selected->metrics.maximum_quarter_residual))
    throw std::runtime_error("materialized window metrics mismatch");
  const bool exact = selected->state.energy == 0;
  write_checkpoint(options.output, selected->state, options.seed,
                   unique_cases, exact, ScoreWeights{});
  std::cout << "WINDOW_SCAN half_size=" << half_size
            << " families=" << options.window_family_count
            << " cases_per_block=" << cases_per_block
            << " evaluated=" << evaluated
            << " unique_cases=" << unique_cases
            << " transition_exchanges=" << transition_exchanges << '\n';
  print_window_champion("INITIAL",
      WindowChampion{initial, source, -1, -1, 1});
  print_window_champion("BEST_ENERGY", best_energy);
  print_window_champion("BEST_QUARTIC", best_quartic);
  print_window_champion("BEST_MAXIMUM", best_maximum);
  std::cout << "SELECTED objective=" << options.scan_objective << '\n';
  std::cout << (exact ? "FOUND" : "DONE")
            << " window-scan output=" << options.output << '\n';
  return exact ? 0 : 1;
}

struct WindowAssignment {
  Residuals delta{};
  std::uint16_t plus_mask = 0;
};

struct PairedWindowMove {
  int first_sequence = -1;
  int second_sequence = -1;
  int family = -1;
  int window_size = 0;
  std::array<int, 12> first_window{};
  std::array<int, 12> second_window{};
  std::uint16_t first_mask = 0;
  std::uint16_t second_mask = 0;
};

struct PairedWindowChampion {
  ResidualMetrics metrics;
  PairedWindowMove move;
  std::uint64_t evaluation_ties = 1;
};

std::vector<WindowAssignment> enumerate_window_assignments(
    const State &source, int which, const std::vector<int> &window,
    int half_size) {
  const int window_size = 2 * half_size;
  if (window_size > 12 || static_cast<int>(window.size()) != window_size)
    throw std::runtime_error("paired window has an invalid size");
  std::vector<WindowAssignment> result;
  result.reserve(binomial(window_size, half_size));
  State state = source;
  std::vector<int> combination(half_size);
  for (int index = 0; index < half_size; ++index)
    combination[index] = index;
  while (true) {
    WindowAssignment assignment;
    for (int lag = 1; lag <= HALF; ++lag)
      assignment.delta[lag] = state.residual[lag] - source.residual[lag];
    for (int index : combination)
      assignment.plus_mask |= static_cast<std::uint16_t>(1U << index);
    result.push_back(assignment);

    int pivot = half_size - 1;
    while (pivot >= 0 &&
           combination[pivot] == window_size - half_size + pivot)
      --pivot;
    if (pivot < 0) break;
    std::vector<int> next = combination;
    ++next[pivot];
    for (int index = pivot + 1; index < half_size; ++index)
      next[index] = next[index - 1] + 1;
    std::array<bool, 12> current_set{};
    std::array<bool, 12> next_set{};
    for (int index : combination) current_set[index] = true;
    for (int index : next) next_set[index] = true;
    std::vector<int> leaving;
    std::vector<int> entering;
    for (int index = 0; index < window_size; ++index) {
      if (current_set[index] && !next_set[index]) leaving.push_back(index);
      if (!current_set[index] && next_set[index]) entering.push_back(index);
    }
    if (leaving.size() != entering.size())
      throw std::runtime_error(
          "paired-window transition cardinality mismatch");
    for (std::size_t exchange = 0; exchange < leaving.size(); ++exchange) {
      const int left = window[leaving[exchange]];
      const int right = window[entering[exchange]];
      const Residuals delta =
          exchange_deltas(state.sequence[which], left, right);
      const std::int64_t new_energy = exchanged_energy(state, delta);
      apply_exchange(state, which, left, right, delta, new_energy);
    }
    combination = std::move(next);
  }
  if (result.size() != binomial(window_size, half_size))
    throw std::runtime_error("paired-window assignment count mismatch");
  validate(state);
  return result;
}

void update_paired_window_champions(
    const ResidualMetrics &candidate, const PairedWindowMove &move,
    PairedWindowChampion &best_energy,
    PairedWindowChampion &best_quartic,
    PairedWindowChampion &best_maximum) {
  const auto energy_key = std::tie(
      candidate.energy, candidate.quartic,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_energy_key = std::tie(
      best_energy.metrics.energy, best_energy.metrics.quartic,
      best_energy.metrics.maximum_quarter_residual,
      best_energy.metrics.bad_lags);
  if (energy_key < best_energy_key) {
    best_energy = {candidate, move, 1};
  } else if (energy_key == best_energy_key) {
    ++best_energy.evaluation_ties;
  }

  const auto quartic_key = std::tie(
      candidate.quartic, candidate.energy,
      candidate.maximum_quarter_residual, candidate.bad_lags);
  const auto best_quartic_key = std::tie(
      best_quartic.metrics.quartic, best_quartic.metrics.energy,
      best_quartic.metrics.maximum_quarter_residual,
      best_quartic.metrics.bad_lags);
  if (quartic_key < best_quartic_key) {
    best_quartic = {candidate, move, 1};
  } else if (quartic_key == best_quartic_key) {
    ++best_quartic.evaluation_ties;
  }

  const auto maximum_key = std::tie(
      candidate.maximum_quarter_residual, candidate.quartic,
      candidate.energy, candidate.bad_lags);
  const auto best_maximum_key = std::tie(
      best_maximum.metrics.maximum_quarter_residual,
      best_maximum.metrics.quartic, best_maximum.metrics.energy,
      best_maximum.metrics.bad_lags);
  if (maximum_key < best_maximum_key) {
    best_maximum = {candidate, move, 1};
  } else if (maximum_key == best_maximum_key) {
    ++best_maximum.evaluation_ties;
  }
}

State state_after_paired_window_move(const State &source,
                                     const PairedWindowMove &move) {
  State result = source;
  if (move.first_sequence >= 0) {
    for (int index = 0; index < move.window_size; ++index) {
      result.sequence[move.first_sequence][move.first_window[index]] =
          (move.first_mask & (1U << index)) != 0 ? 1 : -1;
      result.sequence[move.second_sequence][move.second_window[index]] =
          (move.second_mask & (1U << index)) != 0 ? 1 : -1;
    }
  }
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

void print_paired_window_champion(
    std::string_view label, const PairedWindowChampion &champion) {
  std::cout << label << " energy=" << champion.metrics.energy
            << " quartic=" << champion.metrics.quartic
            << " bad_lags=" << champion.metrics.bad_lags
            << " maximum_quarter_residual="
            << champion.metrics.maximum_quarter_residual
            << " lexicographic_evaluation_ties="
            << champion.evaluation_ties
            << " first_sequence=" << champion.move.first_sequence
            << " second_sequence=" << champion.move.second_sequence
            << " family=" << champion.move.family
            << " first_mask=" << champion.move.first_mask
            << " second_mask=" << champion.move.second_mask << '\n';
}

int run_paired_window_scan(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const int half_size = options.paired_window_half_size;
  const int window_size = 2 * half_size;
  const std::uint64_t assignments_per_window =
      binomial(window_size, half_size);
  const std::uint64_t cases_per_pair =
      assignments_per_window * assignments_per_window;
  const std::uint64_t nonidentity_assignments =
      assignments_per_window - 1;
  const std::uint64_t unique_per_family =
      1 + SEQUENCES * nonidentity_assignments +
      6 * nonidentity_assignments * nonidentity_assignments;
  const std::uint64_t unique_states =
      1 + static_cast<std::uint64_t>(options.window_family_count) *
              (unique_per_family - 1);
  const ResidualMetrics initial = residual_metrics(source.residual);
  PairedWindowChampion best_energy{initial, {}, 1};
  PairedWindowChampion best_quartic{initial, {}, 1};
  PairedWindowChampion best_maximum{initial, {}, 1};
  std::array<std::array<bool, N>, SEQUENCES> excluded{};
  std::uint64_t evaluated = 0;
  std::uint64_t competitive = 0;

  for (int which = 0; which < SEQUENCES; ++which) {
    const int plus = (N + row_sum(source.sequence[which])) / 2;
    const int minus = N - plus;
    const int required = half_size * options.window_family_count;
    if (plus < required || minus < required)
      throw std::runtime_error(
          "paired-window families require more signs than the profile contains");
  }

  for (int family = 0; family < options.window_family_count; ++family) {
    std::array<std::vector<int>, SEQUENCES> windows;
    std::array<std::vector<WindowAssignment>, SEQUENCES> assignments;
    for (int which = 0; which < SEQUENCES; ++which) {
      const auto [plus, minus] =
          guided_window(source, which, half_size, excluded[which]);
      for (int position : plus) excluded[which][position] = true;
      for (int position : minus) excluded[which][position] = true;
      windows[which] = plus;
      windows[which].insert(
          windows[which].end(), minus.begin(), minus.end());
      assignments[which] = enumerate_window_assignments(
          source, which, windows[which], half_size);
      std::cout << "PAIRED_WINDOW family=" << family
                << " sequence=" << which << " positions=(";
      for (int index = 0; index < window_size; ++index)
        std::cout << (index == 0 ? "" : ",") << windows[which][index];
      std::cout << ") assignments=" << assignments[which].size() << '\n';
    }
    std::cout.flush();

    for (int first_sequence = 0; first_sequence < SEQUENCES;
         ++first_sequence) {
      for (int second_sequence = first_sequence + 1;
           second_sequence < SEQUENCES; ++second_sequence) {
        std::uint64_t block_cases = 0;
        for (const WindowAssignment &first : assignments[first_sequence]) {
          for (const WindowAssignment &second : assignments[second_sequence]) {
            ResidualMetrics candidate;
            bool can_improve = true;
            for (int lag = 1; lag <= HALF; ++lag) {
              const int updated = source.residual[lag] + first.delta[lag] +
                                  second.delta[lag];
              if (updated % 4 != 0)
                throw std::runtime_error(
                    "paired-window residual is not divisible by four");
              const std::int64_t value = updated / 4;
              const std::int64_t square = value * value;
              candidate.energy += square;
              candidate.quartic += square * square;
              candidate.bad_lags += value != 0;
              candidate.maximum_quarter_residual = std::max(
                  candidate.maximum_quarter_residual,
                  static_cast<int>(std::abs(value)));
              const bool energy_possible =
                  candidate.energy <= best_energy.metrics.energy;
              const bool quartic_possible =
                  candidate.quartic <= best_quartic.metrics.quartic;
              const bool maximum_possible =
                  candidate.maximum_quarter_residual <
                      best_maximum.metrics.maximum_quarter_residual ||
                  (candidate.maximum_quarter_residual ==
                       best_maximum.metrics.maximum_quarter_residual &&
                   candidate.quartic <= best_maximum.metrics.quartic);
              if (!energy_possible && !quartic_possible &&
                  !maximum_possible) {
                can_improve = false;
                break;
              }
            }
            if (can_improve) {
              PairedWindowMove move;
              move.first_sequence = first_sequence;
              move.second_sequence = second_sequence;
              move.family = family;
              move.window_size = window_size;
              for (int index = 0; index < window_size; ++index) {
                move.first_window[index] = windows[first_sequence][index];
                move.second_window[index] = windows[second_sequence][index];
              }
              move.first_mask = first.plus_mask;
              move.second_mask = second.plus_mask;
              update_paired_window_champions(
                  candidate, move, best_energy, best_quartic, best_maximum);
              ++competitive;
            }
            ++block_cases;
          }
        }
        if (block_cases != cases_per_pair)
          throw std::runtime_error("paired-window pair count mismatch");
        evaluated += block_cases;
        std::cout << "PAIRED_WINDOW_BLOCK family=" << family
                  << " first=" << first_sequence
                  << " second=" << second_sequence
                  << " cases=" << block_cases << '\n';
        std::cout.flush();
      }
    }
  }

  const PairedWindowChampion *selected = &best_energy;
  if (options.scan_objective == "quartic") selected = &best_quartic;
  if (options.scan_objective == "maximum") selected = &best_maximum;
  const State best = state_after_paired_window_move(source, selected->move);
  const ResidualMetrics materialized = residual_metrics(best.residual);
  if (std::tie(materialized.energy, materialized.quartic,
               materialized.bad_lags,
               materialized.maximum_quarter_residual) !=
      std::tie(selected->metrics.energy, selected->metrics.quartic,
               selected->metrics.bad_lags,
               selected->metrics.maximum_quarter_residual))
    throw std::runtime_error("materialized paired-window metrics mismatch");
  const bool exact = best.energy == 0;
  write_checkpoint(options.output, best, options.seed, evaluated, exact,
                   ScoreWeights{});
  std::cout << "PAIRED_WINDOW_SCAN half_size=" << half_size
            << " families=" << options.window_family_count
            << " assignments_per_window=" << assignments_per_window
            << " cases_per_pair=" << cases_per_pair
            << " evaluated=" << evaluated
            << " unique_states=" << unique_states
            << " competitive=" << competitive << '\n';
  print_paired_window_champion("INITIAL",
      PairedWindowChampion{initial, {}, 1});
  print_paired_window_champion("BEST_ENERGY", best_energy);
  print_paired_window_champion("BEST_QUARTIC", best_quartic);
  print_paired_window_champion("BEST_MAXIMUM", best_maximum);
  std::cout << "SELECTED objective=" << options.scan_objective << '\n';
  std::cout << (exact ? "FOUND" : "DONE")
            << " paired-window-scan output=" << options.output << '\n';
  return exact ? 0 : 1;
}

struct PairFingerprint {
  std::uint64_t first = 0;
  std::uint64_t second = 0;
  std::uint32_t packed_indices = 0;
};

struct FourWindowMove {
  int family = -1;
  int window_size = 0;
  std::array<std::array<int, 12>, SEQUENCES> windows{};
  std::array<std::uint16_t, SEQUENCES> masks{};
};

std::uint64_t splitmix64(std::uint64_t value) {
  value += 0x9e3779b97f4a7c15ULL;
  value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
  value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

std::pair<std::uint64_t, std::uint64_t> residual_fingerprint(
    const Residuals &residual) {
  std::uint64_t first = 0;
  std::uint64_t second = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    const std::uint64_t value = static_cast<std::uint64_t>(
        static_cast<std::int64_t>(residual[lag]));
    const std::uint64_t first_weight =
        splitmix64(0x66816701ULL + static_cast<std::uint64_t>(lag));
    const std::uint64_t second_weight =
        splitmix64(0x16766802ULL + static_cast<std::uint64_t>(lag));
    first += value * first_weight;
    second += value * second_weight;
  }
  return {first, second};
}

State state_after_four_window_move(const State &source,
                                   const FourWindowMove &move) {
  State result = source;
  if (move.family >= 0) {
    for (int which = 0; which < SEQUENCES; ++which) {
      for (int index = 0; index < move.window_size; ++index) {
        result.sequence[which][move.windows[which][index]] =
            (move.masks[which] & (1U << index)) != 0 ? 1 : -1;
      }
    }
  }
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

int run_four_window_mitm(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const int half_size = options.four_window_mitm_half_size;
  const int window_size = 2 * half_size;
  const std::uint64_t assignment_count = binomial(window_size, half_size);
  const std::uint64_t pair_count = assignment_count * assignment_count;
  const std::uint64_t conceptual_per_family = pair_count * pair_count;
  if (assignment_count > std::numeric_limits<std::uint32_t>::max() ||
      pair_count > std::numeric_limits<std::uint32_t>::max())
    throw std::runtime_error("four-window packed index exceeds 32 bits");
  const std::uint32_t assignment_count_32 =
      static_cast<std::uint32_t>(assignment_count);
  std::array<std::array<bool, N>, SEQUENCES> excluded{};
  FourWindowMove solution;
  bool found = false;
  std::uint64_t right_pair_probes = 0;
  std::uint64_t exact_comparisons = 0;

  for (int which = 0; which < SEQUENCES; ++which) {
    const int plus = (N + row_sum(source.sequence[which])) / 2;
    const int minus = N - plus;
    const int required = half_size * options.window_family_count;
    if (plus < required || minus < required)
      throw std::runtime_error(
          "four-window families require more signs than the profile contains");
  }

  const auto source_hash = residual_fingerprint(source.residual);
  for (int family = 0;
       family < options.window_family_count && !found; ++family) {
    std::array<std::vector<int>, SEQUENCES> windows;
    std::array<std::vector<WindowAssignment>, SEQUENCES> assignments;
    std::array<std::vector<std::pair<std::uint64_t, std::uint64_t>>,
               SEQUENCES> hashes;
    for (int which = 0; which < SEQUENCES; ++which) {
      const auto [plus, minus] =
          guided_window(source, which, half_size, excluded[which]);
      for (int position : plus) excluded[which][position] = true;
      for (int position : minus) excluded[which][position] = true;
      windows[which] = plus;
      windows[which].insert(
          windows[which].end(), minus.begin(), minus.end());
      assignments[which] = enumerate_window_assignments(
          source, which, windows[which], half_size);
      hashes[which].reserve(assignments[which].size());
      for (const WindowAssignment &assignment : assignments[which])
        hashes[which].push_back(residual_fingerprint(assignment.delta));
      std::cout << "FOUR_WINDOW family=" << family
                << " sequence=" << which << " positions=(";
      for (int index = 0; index < window_size; ++index)
        std::cout << (index == 0 ? "" : ",") << windows[which][index];
      std::cout << ") assignments=" << assignments[which].size() << '\n';
    }

    std::uint64_t brute_force_exact = 0;
    if (half_size <= 2) {
      for (std::uint32_t first = 0; first < assignment_count_32; ++first) {
        for (std::uint32_t second = 0; second < assignment_count_32;
             ++second) {
          for (std::uint32_t third = 0; third < assignment_count_32;
               ++third) {
            for (std::uint32_t fourth = 0; fourth < assignment_count_32;
                 ++fourth) {
              bool exact = true;
              for (int lag = 1; lag <= HALF; ++lag) {
                if (source.residual[lag] +
                        assignments[0][first].delta[lag] +
                        assignments[1][second].delta[lag] +
                        assignments[2][third].delta[lag] +
                        assignments[3][fourth].delta[lag] !=
                    0) {
                  exact = false;
                  break;
                }
              }
              brute_force_exact += exact;
            }
          }
        }
      }
    }

    std::vector<PairFingerprint> left_pairs;
    left_pairs.reserve(pair_count);
    for (std::uint32_t first = 0; first < assignment_count_32; ++first) {
      for (std::uint32_t second = 0; second < assignment_count_32; ++second) {
        left_pairs.push_back({
            hashes[0][first].first + hashes[1][second].first,
            hashes[0][first].second + hashes[1][second].second,
            first * assignment_count_32 + second});
      }
    }
    if (left_pairs.size() != pair_count)
      throw std::runtime_error("four-window left-pair count mismatch");
    std::sort(left_pairs.begin(), left_pairs.end(),
              [](const PairFingerprint &left,
                 const PairFingerprint &right) {
                return std::tie(left.first, left.second,
                                left.packed_indices) <
                       std::tie(right.first, right.second,
                                right.packed_indices);
              });

    for (std::uint32_t third = 0;
         third < assignment_count && !found; ++third) {
      for (std::uint32_t fourth = 0;
           fourth < assignment_count && !found; ++fourth) {
        const std::uint64_t target_first =
            0 - source_hash.first - hashes[2][third].first -
            hashes[3][fourth].first;
        const std::uint64_t target_second =
            0 - source_hash.second - hashes[2][third].second -
            hashes[3][fourth].second;
        const auto begin = std::lower_bound(
            left_pairs.begin(), left_pairs.end(),
            std::pair<std::uint64_t, std::uint64_t>{target_first,
                                                    target_second},
            [](const PairFingerprint &record,
               const std::pair<std::uint64_t, std::uint64_t> &target) {
              return record.first < target.first ||
                     (record.first == target.first &&
                      record.second < target.second);
            });
        for (auto match = begin;
             match != left_pairs.end() && match->first == target_first &&
             match->second == target_second;
             ++match) {
          ++exact_comparisons;
          const std::uint32_t first =
              match->packed_indices / assignment_count_32;
          const std::uint32_t second =
              match->packed_indices % assignment_count_32;
          bool exact = true;
          for (int lag = 1; lag <= HALF; ++lag) {
            if (source.residual[lag] + assignments[0][first].delta[lag] +
                    assignments[1][second].delta[lag] +
                    assignments[2][third].delta[lag] +
                    assignments[3][fourth].delta[lag] !=
                0) {
              exact = false;
              break;
            }
          }
          if (exact) {
            solution.family = family;
            solution.window_size = window_size;
            for (int which = 0; which < SEQUENCES; ++which)
              for (int index = 0; index < window_size; ++index)
                solution.windows[which][index] = windows[which][index];
            solution.masks = {{
                assignments[0][first].plus_mask,
                assignments[1][second].plus_mask,
                assignments[2][third].plus_mask,
                assignments[3][fourth].plus_mask}};
            found = true;
            break;
          }
        }
        ++right_pair_probes;
      }
    }
    std::cout << "FOUR_WINDOW_FAMILY family=" << family
              << " pair_records=" << left_pairs.size()
              << " record_bytes="
              << left_pairs.size() * sizeof(PairFingerprint)
              << " cumulative_right_pair_probes=" << right_pair_probes
              << " cumulative_exact_comparisons=" << exact_comparisons
              << " found=" << (found ? 1 : 0) << '\n';
    if (half_size <= 2) {
      const bool mitm_found_in_family = found && solution.family == family;
      if (mitm_found_in_family != (brute_force_exact != 0))
        throw std::runtime_error(
            "four-window MITM disagrees with direct enumeration");
      std::cout << "FOUR_WINDOW_BRUTE_FORCE family=" << family
                << " cases=" << conceptual_per_family
                << " exact_solutions=" << brute_force_exact << '\n';
    }
    std::cout.flush();
  }

  const State result = state_after_four_window_move(source, solution);
  if (found && result.energy != 0)
    throw std::runtime_error(
        "four-window fingerprint match failed exact materialization");
  if (!found &&
      right_pair_probes !=
          static_cast<std::uint64_t>(options.window_family_count) * pair_count)
    throw std::runtime_error("four-window right-pair count mismatch");
  write_checkpoint(options.output, result, options.seed, right_pair_probes,
                   found, ScoreWeights{});
  const std::uint64_t fully_exhausted_families = found
      ? static_cast<std::uint64_t>(solution.family)
      : static_cast<std::uint64_t>(options.window_family_count);
  const std::uint64_t conceptual_exhausted =
      fully_exhausted_families * conceptual_per_family;
  const std::uint64_t unique_exhausted = fully_exhausted_families == 0
      ? 0
      : 1 + fully_exhausted_families * (conceptual_per_family - 1);
  std::cout << "FOUR_WINDOW_MITM half_size=" << half_size
            << " requested_families=" << options.window_family_count
            << " fully_exhausted_families=" << fully_exhausted_families
            << " assignments_per_sequence=" << assignment_count
            << " pair_records=" << pair_count
            << " conceptual_per_family=" << conceptual_per_family
            << " conceptual_exhausted=" << conceptual_exhausted
            << " unique_exhausted=" << unique_exhausted
            << " right_pair_probes=" << right_pair_probes
            << " exact_comparisons=" << exact_comparisons << '\n';
  std::cout << (found ? "FOUND" : "DONE")
            << " four-window-mitm family=" << solution.family
            << " output=" << options.output << '\n';
  return found ? 0 : 1;
}

class PairBloomFilter {
 public:
  explicit PairBloomFilter(std::uint64_t entries) {
    std::uint64_t bits = 1ULL << 16;
    constexpr std::uint64_t maximum_bits = 1ULL << 28;
    while (bits < maximum_bits && bits < 32 * entries) bits <<= 1;
    bit_mask_ = bits - 1;
    words_.assign(static_cast<std::size_t>(bits / 64), 0);
  }

  void insert(std::uint64_t first, std::uint64_t second) {
    for (std::uint64_t hash : hashes(first, second))
      words_[static_cast<std::size_t>((hash & bit_mask_) >> 6)] |=
          1ULL << (hash & 63);
  }

  bool possibly_contains(std::uint64_t first, std::uint64_t second) const {
    for (std::uint64_t hash : hashes(first, second)) {
      if ((words_[static_cast<std::size_t>((hash & bit_mask_) >> 6)] &
           (1ULL << (hash & 63))) == 0)
        return false;
    }
    return true;
  }

  std::uint64_t bytes() const {
    return static_cast<std::uint64_t>(words_.size()) * sizeof(std::uint64_t);
  }

 private:
  static std::array<std::uint64_t, 3> hashes(
      std::uint64_t first, std::uint64_t second) {
    const std::uint64_t base =
        splitmix64(first ^ splitmix64(second ^ 0x66816703ULL));
    const std::uint64_t step =
        splitmix64(second ^ splitmix64(first ^ 0x16766804ULL)) | 1ULL;
    return {{base, base + step, base + 2 * step}};
  }

  std::vector<std::uint64_t> words_;
  std::uint64_t bit_mask_ = 0;
};

void self_test_pair_bloom_filter() {
  PairBloomFilter bloom(4096);
  std::vector<std::pair<std::uint64_t, std::uint64_t>> inserted;
  inserted.reserve(4096);
  for (std::uint64_t index = 0; index < 4096; ++index) {
    const std::pair<std::uint64_t, std::uint64_t> fingerprint{
        splitmix64(0x66800000ULL + index),
        splitmix64(0x16700000ULL + index)};
    inserted.push_back(fingerprint);
    bloom.insert(fingerprint.first, fingerprint.second);
  }
  for (const auto &[first, second] : inserted) {
    if (!bloom.possibly_contains(first, second))
      throw std::runtime_error("Bloom filter produced a false negative");
  }
  std::cout << "PASS: Bloom filter retained 4096 inserted fingerprints\n";
}

struct MixedFourWindowMove {
  std::array<int, SEQUENCES> families{{-1, -1, -1, -1}};
  int window_size = 0;
  std::array<std::array<int, 12>, SEQUENCES> windows{};
  std::array<std::uint16_t, SEQUENCES> masks{};
};

State state_after_mixed_four_window_move(
    const State &source, const MixedFourWindowMove &move) {
  State result = source;
  if (move.families[0] >= 0) {
    for (int which = 0; which < SEQUENCES; ++which) {
      for (int index = 0; index < move.window_size; ++index) {
        result.sequence[which][move.windows[which][index]] =
            (move.masks[which] & (1U << index)) != 0 ? 1 : -1;
      }
    }
  }
  result.residual = full_residuals(result.sequence);
  result.energy = energy(result.residual);
  validate(result);
  return result;
}

int run_mixed_window_mitm(const Options &options) {
  const State source = read_checkpoint(options.initial);
  if (options.profile >= 0 && options.profile != source.profile)
    throw std::runtime_error(
        "requested profile disagrees with initial checkpoint");
  const int half_size = options.mixed_window_mitm_half_size;
  const int window_size = 2 * half_size;
  const int family_count = options.window_family_count;
  const std::uint64_t assignment_count = binomial(window_size, half_size);
  const std::uint64_t pair_count = assignment_count * assignment_count;
  if (assignment_count > std::numeric_limits<std::uint32_t>::max() ||
      pair_count > std::numeric_limits<std::uint32_t>::max())
    throw std::runtime_error("mixed-window packed index exceeds 32 bits");
  const std::uint32_t assignment_count_32 =
      static_cast<std::uint32_t>(assignment_count);
  const std::uint32_t pair_count_32 =
      static_cast<std::uint32_t>(pair_count);
  const int left_family_pair_count = family_count * family_count;
  const int batch_size = options.mixed_window_batch_size;
  const int total_batches =
      (left_family_pair_count + batch_size - 1) / batch_size;
  if (options.mixed_window_batch_start >= total_batches)
    throw std::runtime_error("mixed-window batch start is out of range");
  const int batch_begin = options.mixed_window_batch_start;
  const int batch_end = options.mixed_window_batch_count == 0
      ? total_batches
      : batch_begin + options.mixed_window_batch_count;
  if (batch_end > total_batches)
    throw std::runtime_error("mixed-window batch range is out of range");
  if (static_cast<std::uint64_t>(batch_size) * pair_count >
      std::numeric_limits<std::uint32_t>::max())
    throw std::runtime_error("mixed-window batch packing exceeds 32 bits");

  for (int which = 0; which < SEQUENCES; ++which) {
    const int plus = (N + row_sum(source.sequence[which])) / 2;
    const int minus = N - plus;
    const int required = half_size * family_count;
    if (plus < required || minus < required)
      throw std::runtime_error(
          "mixed-window families require more signs than the profile contains");
  }

  std::array<std::vector<std::vector<int>>, SEQUENCES> windows;
  std::array<std::vector<std::vector<WindowAssignment>>, SEQUENCES>
      assignments;
  std::array<
      std::vector<std::vector<std::pair<std::uint64_t, std::uint64_t>>>,
      SEQUENCES> hashes;
  for (int which = 0; which < SEQUENCES; ++which) {
    windows[which].resize(family_count);
    assignments[which].resize(family_count);
    hashes[which].resize(family_count);
  }
  std::array<std::array<bool, N>, SEQUENCES> excluded{};
  for (int family = 0; family < family_count; ++family) {
    for (int which = 0; which < SEQUENCES; ++which) {
      const auto [plus, minus] =
          guided_window(source, which, half_size, excluded[which]);
      for (int position : plus) excluded[which][position] = true;
      for (int position : minus) excluded[which][position] = true;
      windows[which][family] = plus;
      windows[which][family].insert(
          windows[which][family].end(), minus.begin(), minus.end());
      assignments[which][family] = enumerate_window_assignments(
          source, which, windows[which][family], half_size);
      const std::uint16_t identity_mask = static_cast<std::uint16_t>(
          (1U << half_size) - 1U);
      if (assignments[which][family].empty() ||
          assignments[which][family][0].plus_mask != identity_mask ||
          assignments[which][family][0].delta != Residuals{})
        throw std::runtime_error(
            "mixed-window assignment zero is not the identity");
      hashes[which][family].reserve(assignments[which][family].size());
      for (const WindowAssignment &assignment : assignments[which][family])
        hashes[which][family].push_back(
            residual_fingerprint(assignment.delta));
      std::cout << "MIXED_WINDOW family=" << family
                << " sequence=" << which << " positions=(";
      for (int index = 0; index < window_size; ++index)
        std::cout << (index == 0 ? "" : ",")
                  << windows[which][family][index];
      std::cout << ") assignments="
                << assignments[which][family].size() << '\n';
    }
  }
  std::cout.flush();

  std::uint64_t brute_force_exact = 0;
  const bool small_full_crosscheck =
      half_size <= 2 && family_count <= 2 && batch_begin == 0 &&
      batch_end == total_batches;
  if (small_full_crosscheck) {
    for (int first_family = 0; first_family < family_count; ++first_family) {
      for (int second_family = 0; second_family < family_count;
           ++second_family) {
        for (int third_family = 0; third_family < family_count;
             ++third_family) {
          for (int fourth_family = 0; fourth_family < family_count;
               ++fourth_family) {
            for (const WindowAssignment &first :
                 assignments[0][first_family]) {
              for (const WindowAssignment &second :
                   assignments[1][second_family]) {
                for (const WindowAssignment &third :
                     assignments[2][third_family]) {
                  for (const WindowAssignment &fourth :
                       assignments[3][fourth_family]) {
                    bool exact = true;
                    for (int lag = 1; lag <= HALF; ++lag) {
                      if (source.residual[lag] + first.delta[lag] +
                              second.delta[lag] + third.delta[lag] +
                              fourth.delta[lag] !=
                          0) {
                        exact = false;
                        break;
                      }
                    }
                    brute_force_exact += exact;
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  const auto source_hash = residual_fingerprint(source.residual);
  const std::uint64_t right_pair_records =
      static_cast<std::uint64_t>(left_family_pair_count) * pair_count;
  MixedFourWindowMove solution;
  bool found = false;
  std::uint64_t right_pair_probes = 0;
  std::uint64_t bloom_positive_probes = 0;
  std::uint64_t exact_comparisons = 0;
  std::uint64_t conceptual_exhausted = 0;
  std::uint64_t fully_exhausted_left_family_pairs = 0;
  std::array<bool, 12> exhausted_first_families{};
  std::array<bool, 12> exhausted_second_families{};
  const auto scan_started = std::chrono::steady_clock::now();

  for (int batch = batch_begin; batch < batch_end && !found; ++batch) {
    const auto batch_started = std::chrono::steady_clock::now();
    const int first_left_pair = batch * batch_size;
    const int last_left_pair =
        std::min(first_left_pair + batch_size, left_family_pair_count);
    const int left_pairs_in_batch = last_left_pair - first_left_pair;
    const std::uint64_t left_record_count =
        static_cast<std::uint64_t>(left_pairs_in_batch) * pair_count;
    PairBloomFilter bloom(left_record_count);
    std::vector<PairFingerprint> left_pairs;
    left_pairs.reserve(static_cast<std::size_t>(left_record_count));
    for (int pair_index = first_left_pair;
         pair_index < last_left_pair; ++pair_index) {
      const int local_pair = pair_index - first_left_pair;
      const int first_family = pair_index / family_count;
      const int second_family = pair_index % family_count;
      for (std::uint32_t first = 0; first < assignment_count_32; ++first) {
        for (std::uint32_t second = 0; second < assignment_count_32;
             ++second) {
          const std::uint64_t first_hash =
              hashes[0][first_family][first].first +
              hashes[1][second_family][second].first;
          const std::uint64_t second_hash =
              hashes[0][first_family][first].second +
              hashes[1][second_family][second].second;
          const std::uint32_t packed =
              static_cast<std::uint32_t>(local_pair) * pair_count_32 +
              first * assignment_count_32 + second;
          left_pairs.push_back({first_hash, second_hash, packed});
          bloom.insert(first_hash, second_hash);
        }
      }
    }
    if (left_pairs.size() != left_record_count)
      throw std::runtime_error("mixed-window left-record count mismatch");
    std::sort(left_pairs.begin(), left_pairs.end(),
              [](const PairFingerprint &left,
                 const PairFingerprint &right) {
                return std::tie(left.first, left.second,
                                left.packed_indices) <
                       std::tie(right.first, right.second,
                                right.packed_indices);
              });

    const std::uint64_t probes_before_batch = right_pair_probes;
    for (int third_family = 0;
         third_family < family_count && !found; ++third_family) {
      for (int fourth_family = 0;
           fourth_family < family_count && !found; ++fourth_family) {
        for (std::uint32_t third = 0;
             third < assignment_count_32 && !found; ++third) {
          for (std::uint32_t fourth = 0;
               fourth < assignment_count_32 && !found; ++fourth) {
            const std::uint64_t target_first =
                0 - source_hash.first -
                hashes[2][third_family][third].first -
                hashes[3][fourth_family][fourth].first;
            const std::uint64_t target_second =
                0 - source_hash.second -
                hashes[2][third_family][third].second -
                hashes[3][fourth_family][fourth].second;
            if (bloom.possibly_contains(target_first, target_second)) {
              ++bloom_positive_probes;
              const auto begin = std::lower_bound(
                  left_pairs.begin(), left_pairs.end(),
                  std::pair<std::uint64_t, std::uint64_t>{target_first,
                                                          target_second},
                  [](const PairFingerprint &record,
                     const std::pair<std::uint64_t, std::uint64_t> &target) {
                    return record.first < target.first ||
                           (record.first == target.first &&
                            record.second < target.second);
                  });
              for (auto match = begin;
                   match != left_pairs.end() &&
                   match->first == target_first &&
                   match->second == target_second;
                   ++match) {
                ++exact_comparisons;
                const std::uint32_t local_pair =
                    match->packed_indices / pair_count_32;
                const std::uint32_t within_pair =
                    match->packed_indices % pair_count_32;
                const std::uint32_t first =
                    within_pair / assignment_count_32;
                const std::uint32_t second =
                    within_pair % assignment_count_32;
                const int left_pair =
                    first_left_pair + static_cast<int>(local_pair);
                const int first_family = left_pair / family_count;
                const int second_family = left_pair % family_count;
                bool exact = true;
                for (int lag = 1; lag <= HALF; ++lag) {
                  if (source.residual[lag] +
                          assignments[0][first_family][first].delta[lag] +
                          assignments[1][second_family][second].delta[lag] +
                          assignments[2][third_family][third].delta[lag] +
                          assignments[3][fourth_family][fourth].delta[lag] !=
                      0) {
                    exact = false;
                    break;
                  }
                }
                if (exact) {
                  solution.families = {{first_family, second_family,
                                        third_family, fourth_family}};
                  solution.window_size = window_size;
                  const std::array<int, SEQUENCES> selected_families{{
                      first_family, second_family,
                      third_family, fourth_family}};
                  for (int which = 0; which < SEQUENCES; ++which) {
                    for (int index = 0; index < window_size; ++index) {
                      solution.windows[which][index] =
                          windows[which][selected_families[which]][index];
                    }
                  }
                  solution.masks = {{
                      assignments[0][first_family][first].plus_mask,
                      assignments[1][second_family][second].plus_mask,
                      assignments[2][third_family][third].plus_mask,
                      assignments[3][fourth_family][fourth].plus_mask}};
                  found = true;
                  break;
                }
              }
            }
            ++right_pair_probes;
          }
        }
      }
    }

    if (!found) {
      if (right_pair_probes - probes_before_batch != right_pair_records)
        throw std::runtime_error("mixed-window right-record count mismatch");
      conceptual_exhausted += left_record_count * right_pair_records;
      fully_exhausted_left_family_pairs +=
          static_cast<std::uint64_t>(left_pairs_in_batch);
      for (int pair_index = first_left_pair;
           pair_index < last_left_pair; ++pair_index) {
        exhausted_first_families[pair_index / family_count] = true;
        exhausted_second_families[pair_index % family_count] = true;
      }
    }
    const double batch_seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - batch_started).count();
    std::cout << std::fixed << std::setprecision(3)
              << "MIXED_WINDOW_BATCH batch=" << batch
              << " first_left_pair=" << first_left_pair
              << " left_family_pairs=" << left_pairs_in_batch
              << " left_records=" << left_pairs.size()
              << " record_bytes="
              << left_pairs.size() * sizeof(PairFingerprint)
              << " bloom_bytes=" << bloom.bytes()
              << " cumulative_right_pair_probes=" << right_pair_probes
              << " cumulative_bloom_positive_probes="
              << bloom_positive_probes
              << " cumulative_exact_comparisons=" << exact_comparisons
              << " found=" << (found ? 1 : 0)
              << " seconds=" << batch_seconds << '\n';
    std::cout.flush();
  }

  const State result = state_after_mixed_four_window_move(source, solution);
  if (found && result.energy != 0)
    throw std::runtime_error(
        "mixed-window fingerprint match failed exact materialization");
  if (!found) {
    const std::uint64_t completed_batches =
        static_cast<std::uint64_t>(batch_end - batch_begin);
    if (right_pair_probes != completed_batches * right_pair_records)
      throw std::runtime_error("mixed-window total probe count mismatch");
  }
  if (small_full_crosscheck &&
      found != (brute_force_exact != 0))
    throw std::runtime_error(
        "mixed-window MITM disagrees with direct enumeration");

  write_checkpoint(options.output, result, options.seed, right_pair_probes,
                   found, ScoreWeights{});
  const std::uint64_t nonidentity = assignment_count - 1;
  const std::uint64_t first_family_choices = static_cast<std::uint64_t>(
      std::count(exhausted_first_families.begin(),
                 exhausted_first_families.end(), true));
  const std::uint64_t second_family_choices = static_cast<std::uint64_t>(
      std::count(exhausted_second_families.begin(),
                 exhausted_second_families.end(), true));
  const std::uint64_t unique_left_states =
      fully_exhausted_left_family_pairs == 0
      ? 0
      : 1 + (first_family_choices + second_family_choices) * nonidentity +
            fully_exhausted_left_family_pairs * nonidentity * nonidentity;
  const std::uint64_t unique_per_right_sequence =
      1 + static_cast<std::uint64_t>(family_count) * nonidentity;
  const std::uint64_t unique_exhausted = unique_left_states == 0
      ? 0
      : unique_left_states * unique_per_right_sequence *
            unique_per_right_sequence;
  const std::uint64_t full_unique_domain =
      unique_per_right_sequence * unique_per_right_sequence *
      unique_per_right_sequence * unique_per_right_sequence;
  const double total_seconds = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - scan_started).count();
  std::cout << "MIXED_WINDOW_MITM half_size=" << half_size
            << " families=" << family_count
            << " assignments_per_sequence=" << assignment_count
            << " batch_size=" << batch_size
            << " batch_begin=" << batch_begin
            << " batch_end=" << batch_end
            << " total_batches=" << total_batches
            << " fully_exhausted_left_family_pairs="
            << fully_exhausted_left_family_pairs
            << " conceptual_exhausted=" << conceptual_exhausted
            << " unique_exhausted=" << unique_exhausted
            << " full_unique_domain=" << full_unique_domain
            << " right_pair_probes=" << right_pair_probes
            << " bloom_positive_probes=" << bloom_positive_probes
            << " exact_comparisons=" << exact_comparisons
            << " seconds=" << total_seconds << '\n';
  if (small_full_crosscheck)
    std::cout << "MIXED_WINDOW_BRUTE_FORCE conceptual_cases="
              << static_cast<std::uint64_t>(left_family_pair_count) *
                     pair_count * right_pair_records
              << " exact_representations=" << brute_force_exact << '\n';
  const bool full_scan = batch_begin == 0 && batch_end == total_batches;
  std::cout << (found ? "FOUND" : (full_scan ? "DONE" : "DONE_SUBSET"))
            << " mixed-window-mitm families=("
            << solution.families[0] << ',' << solution.families[1] << ','
            << solution.families[2] << ',' << solution.families[3]
            << ") output=" << options.output << '\n';
  return found ? 0 : 1;
}

int run(const Options &options) {
  std::mt19937_64 rng(options.seed);
  std::uniform_int_distribution<int> sequence_choice(0, SEQUENCES - 1);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  const auto started = std::chrono::steady_clock::now();
  const auto deadline = started + std::chrono::duration<double>(options.seconds);
  auto next_report = started + std::chrono::duration<double>(options.report_every);
  State best;
  best.energy = std::numeric_limits<std::int64_t>::max();
  std::int64_t best_quartic = std::numeric_limits<std::int64_t>::max();
  int best_bad_lags = std::numeric_limits<int>::max();
  std::int64_t best_score = std::numeric_limits<std::int64_t>::max();
  auto improves_best = [&](const State &candidate,
                           std::int64_t candidate_quartic,
                           int candidate_bad_lags,
                           std::int64_t candidate_score) {
    return candidate_score < best_score ||
           (candidate_score == best_score &&
            (candidate.energy < best.energy ||
             (candidate.energy == best.energy &&
              (candidate_quartic < best_quartic ||
               (candidate_quartic == best_quartic &&
                candidate_bad_lags < best_bad_lags)))));
  };
  auto validate_search_metrics = [&](const State &state,
                                     std::int64_t state_quartic,
                                     int state_bad_lags,
                                     std::int64_t state_score) {
    validate(state);
    if (quartic_energy(state.residual) != state_quartic)
      throw std::runtime_error("incremental quartic mismatch");
    if (bad_lags(state) != state_bad_lags)
      throw std::runtime_error("incremental bad-lag count mismatch");
    if (search_score(state.energy, state_quartic, state_bad_lags,
                     options.score_weights) != state_score)
      throw std::runtime_error("incremental weighted score mismatch");
  };
  State initial;
  const bool has_initial = !options.initial.empty();
  if (has_initial) {
    initial = read_checkpoint(options.initial);
    if (options.profile >= 0 && options.profile != initial.profile)
      throw std::runtime_error("requested profile disagrees with initial checkpoint");
    if (options.pair_polish_size > 0) {
      const std::int64_t before = initial.energy;
      const int improvements = best_pair_descent(
          initial, static_cast<std::size_t>(options.pair_polish_size),
          static_cast<int>(options.pair_polish_steps), options.pair_polish_arity);
      std::cout << "PAIR_POLISH source=initial improvements=" << improvements
                << " before=" << before << " after=" << initial.energy << '\n';
    }
    best = initial;
    best_quartic = quartic_energy(best.residual);
    best_bad_lags = bad_lags(best);
    best_score = search_score(
        best.energy, best_quartic, best_bad_lags, options.score_weights);
    validate_search_metrics(best, best_quartic, best_bad_lags, best_score);
    write_checkpoint(options.output, best, options.seed, 0, best.energy == 0,
                     options.score_weights);
    if (best.energy == 0) {
      std::cout << "FOUND exact cyclic SDS in initial checkpoint output="
                << options.output << '\n';
      return 0;
    }
  }
  std::uint64_t moves = 0;
  std::uint64_t accepted = 0;
  std::uint64_t restarts = 0;

  while (std::chrono::steady_clock::now() < deadline) {
    State state;
    if (has_initial && restarts == 0) {
      state = initial;
    } else if (options.restart_from_best &&
               best.energy != std::numeric_limits<std::int64_t>::max()) {
      state = best;
      for (std::uint64_t perturb = 0; perturb < options.perturb_exchanges;
           ++perturb) {
        const int which = sequence_choice(rng);
        const auto [left, right] = random_exchange(state.sequence[which], rng);
        const auto delta = exchange_deltas(state.sequence[which], left, right);
        const std::int64_t new_energy = exchanged_energy(state, delta);
        apply_exchange(state, which, left, right, delta, new_energy);
        ++moves;
      }
      validate(state);
    } else {
      const int profile = options.profile >= 0
                              ? options.profile
                              : static_cast<int>(restarts % PROFILES.size());
      state = random_state(profile, rng);
    }
    ++restarts;
    std::int64_t state_quartic = quartic_energy(state.residual);
    int state_bad_lags = bad_lags(state);
    std::int64_t state_score = search_score(
        state.energy, state_quartic, state_bad_lags, options.score_weights);
    if (improves_best(
            state, state_quartic, state_bad_lags, state_score)) {
      if (options.pair_polish_size > 0)
        best_pair_descent(
            state, static_cast<std::size_t>(options.pair_polish_size),
            static_cast<int>(options.pair_polish_steps),
            options.pair_polish_arity);
      state_quartic = quartic_energy(state.residual);
      state_bad_lags = bad_lags(state);
      state_score = search_score(
          state.energy, state_quartic, state_bad_lags,
          options.score_weights);
      if (improves_best(
              state, state_quartic, state_bad_lags, state_score)) {
        best = state;
        best_quartic = state_quartic;
        best_bad_lags = state_bad_lags;
        best_score = state_score;
        validate_search_metrics(
            best, best_quartic, best_bad_lags, best_score);
        const bool exact = best.energy == 0;
        write_checkpoint(options.output, best, options.seed, moves, exact,
                         options.score_weights);
        if (exact) {
          std::cout << "FOUND exact cyclic SDS at restart profile="
                    << best.profile << " moves=" << moves
                    << " output=" << options.output << '\n';
          return 0;
        }
      }
    }

    for (std::uint64_t phase = 0;
         phase < options.moves_per_restart &&
         std::chrono::steady_clock::now() < deadline;
         ++phase) {
      const bool use_same_sequence_move =
          uniform(rng) < options.same_sequence_probability;
      std::array<int, SEQUENCES> order{{0, 1, 2, 3}};
      int effective_arity = 0;
      std::array<int, SEQUENCES> left{};
      std::array<int, SEQUENCES> right{};
      std::array<int, HALF + 1> combined{};
      int same_sequence = -1;
      std::array<int, 4> same_positions{};
      if (use_same_sequence_move) {
        same_sequence = sequence_choice(rng);
        same_positions = random_same_sequence_double_exchange(
            state.sequence[same_sequence], rng);
        combined = same_sequence_double_exchange_deltas(
            state.sequence[same_sequence], same_positions);
      } else {
        std::shuffle(order.begin(), order.end(), rng);
        effective_arity =
            options.move_arity > 1 &&
                    uniform(rng) < options.compound_probability
                ? options.move_arity
                : 1;
        for (int move = 0; move < effective_arity; ++move) {
          const auto endpoints =
              random_exchange(state.sequence[order[move]], rng);
          left[move] = endpoints.first;
          right[move] = endpoints.second;
          const auto delta = exchange_deltas(
              state.sequence[order[move]], left[move], right[move]);
          for (int lag = 1; lag <= HALF; ++lag)
            combined[lag] += delta[lag];
        }
      }
      int candidate_bad_lags = 0;
      std::int64_t candidate_quartic = 0;
      const std::int64_t candidate_energy = exchanged_energy(
          state, combined, &candidate_bad_lags, &candidate_quartic);
      const std::int64_t candidate_score = search_score(
          candidate_energy, candidate_quartic, candidate_bad_lags,
          options.score_weights);
      const double fraction = options.moves_per_restart <= 1
                                  ? 1.0
                                  : static_cast<double>(phase) /
                                        static_cast<double>(options.moves_per_restart - 1);
      const double temperature =
          options.start_temperature *
          std::pow(options.end_temperature / options.start_temperature, fraction);
      const std::int64_t increase = candidate_score - state_score;
      const bool accept =
          increase <= 0 || uniform(rng) < std::exp(-static_cast<double>(increase) /
                                                   temperature);
      if (accept) {
        if (use_same_sequence_move) {
          apply_same_sequence_double_exchange(
              state, same_sequence, same_positions, combined,
              candidate_energy);
        } else {
          apply_compound_exchange(state, order, left, right, effective_arity,
                                  combined, candidate_energy);
        }
        state_quartic = candidate_quartic;
        state_bad_lags = candidate_bad_lags;
        state_score = candidate_score;
        ++accepted;
      }
      ++moves;

      if (improves_best(
              state, state_quartic, state_bad_lags, state_score)) {
        if (options.pair_polish_size > 0)
          best_pair_descent(
              state, static_cast<std::size_t>(options.pair_polish_size),
              static_cast<int>(options.pair_polish_steps),
              options.pair_polish_arity);
        state_quartic = quartic_energy(state.residual);
        state_bad_lags = bad_lags(state);
        state_score = search_score(
            state.energy, state_quartic, state_bad_lags,
            options.score_weights);
        if (improves_best(
                state, state_quartic, state_bad_lags, state_score)) {
          best = state;
          best_quartic = state_quartic;
          best_bad_lags = state_bad_lags;
          best_score = state_score;
          validate_search_metrics(
              best, best_quartic, best_bad_lags, best_score);
          const bool exact = best.energy == 0;
          write_checkpoint(options.output, best, options.seed, moves, exact,
                           options.score_weights);
          if (exact) {
            std::cout << "FOUND exact cyclic SDS at profile=" << best.profile
                      << " moves=" << moves << " output=" << options.output
                      << '\n';
            return 0;
          }
        }
      }
      if (moves % options.validate_every == 0)
        validate_search_metrics(
            state, state_quartic, state_bad_lags, state_score);

      const auto now = std::chrono::steady_clock::now();
      if (now >= next_report) {
        const double elapsed = std::chrono::duration<double>(now - started).count();
        std::cout << std::fixed << std::setprecision(3)
                  << "elapsed=" << elapsed << " moves=" << moves
                  << " restarts=" << restarts << " accepted=" << accepted
                  << " best_energy=" << best.energy
                  << " best_quartic=" << best_quartic
                  << " best_bad_lags=" << best_bad_lags
                  << " best_score=" << best_score
                  << " energy_weight=" << options.score_weights.energy
                  << " quartic_weight=" << options.score_weights.quartic
                  << " bad_lag_penalty="
                  << options.score_weights.bad_lags
                  << " same_sequence_probability="
                  << options.same_sequence_probability
                  << " best_profile=" << best.profile << '\n';
        std::cout.flush();
        next_report = now + std::chrono::duration<double>(options.report_every);
      }
    }
  }
  validate_search_metrics(best, best_quartic, best_bad_lags, best_score);
  write_checkpoint(options.output, best, options.seed, moves, false,
                   options.score_weights);
  std::cout << "DONE moves=" << moves << " restarts=" << restarts
            << " best_energy=" << best.energy
            << " best_quartic=" << best_quartic
            << " bad_lags=" << best_bad_lags
            << " best_score=" << best_score
            << " energy_weight=" << options.score_weights.energy
            << " quartic_weight=" << options.score_weights.quartic
            << " bad_lag_penalty=" << options.score_weights.bad_lags
            << " same_sequence_probability="
            << options.same_sequence_probability
            << " profile=" << best.profile << " output=" << options.output << '\n';
  return 1;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options options = parse_options(argc, argv);
    if (options.self_test) {
      self_test();
      self_test_pair_bloom_filter();
      return 0;
    }
    if (options.decimation_scan)
      return run_decimation_scan(options);
    if (options.same_sequence_pair_scan)
      return run_same_sequence_pair_scan(options);
    if (options.cross_sequence_pair_scan)
      return run_cross_sequence_pair_scan(options);
    if (options.window_half_size > 0)
      return run_window_scan(options);
    if (options.paired_window_half_size > 0)
      return run_paired_window_scan(options);
    if (options.four_window_mitm_half_size > 0)
      return run_four_window_mitm(options);
    if (options.mixed_window_mitm_half_size > 0)
      return run_mixed_window_mitm(options);
    return run(options);
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
