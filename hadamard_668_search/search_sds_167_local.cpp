// Low-memory simulated annealing for unrestricted cyclic SDS at order 167.
//
// The engine keeps four row sums fixed and updates all 83 independent
// periodic-correlation residuals in O(83) per two-coordinate exchange.  It is
// deliberately single-threaded and uses only fixed-size arrays.  A zero is
// accepted only after a full recomputation; Python independently expands any
// exact output to the 668x668 Goethals-Seidel matrix.

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
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <string_view>

namespace {

constexpr int N = 167;
constexpr int HALF = 83;
constexpr int SEQUENCES = 4;

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

std::array<int, HALF + 1> exchange_deltas(
    const Sequence &sequence, int left, int right) {
  if (left == right || sequence[left] == sequence[right])
    throw std::runtime_error("exchange endpoints must have opposite signs");
  std::array<int, HALF + 1> result{};
  const int left_sign = sequence[left];
  const int right_sign = sequence[right];
  for (int lag = 1; lag <= HALF; ++lag) {
    int delta =
        -2 * left_sign *
            (sequence[wrap(left + lag)] + sequence[wrap(left - lag)])
        -2 * right_sign *
            (sequence[wrap(right + lag)] + sequence[wrap(right - lag)]);
    if (wrap(left + lag) == right || wrap(right + lag) == left)
      delta += 4 * left_sign * right_sign;
    result[lag] = delta;
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
    const State &state, const std::array<int, HALF + 1> &delta) {
  std::int64_t result = 0;
  for (int lag = 1; lag <= HALF; ++lag) {
    const int updated = state.residual[lag] + delta[lag];
    if (updated % 4 != 0)
      throw std::runtime_error("exchange broke quarter-residual integrality");
    const std::int64_t value = updated / 4;
    result += value * value;
  }
  return result;
}

void apply_exchange(State &state, int which, int left, int right,
                    const std::array<int, HALF + 1> &delta,
                    std::int64_t new_energy) {
  std::swap(state.sequence[which][left], state.sequence[which][right]);
  for (int lag = 1; lag <= HALF; ++lag) state.residual[lag] += delta[lag];
  state.energy = new_energy;
}

int bad_lags(const State &state) {
  int result = 0;
  for (int lag = 1; lag <= HALF; ++lag)
    result += state.residual[lag] != 0;
  return result;
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
                      bool exact) {
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
  stream << "  \"bad_lags\": " << bad_lags(state) << ",\n";
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
          << "  --self-test              validate incremental deltas\n";
      std::exit(0);
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  if (!(options.seconds > 0.0) || options.moves_per_restart == 0 ||
      !(options.start_temperature > 0.0) ||
      !(options.end_temperature > 0.0) || options.validate_every == 0 ||
      !(options.report_every > 0.0))
    throw std::runtime_error("time, move, temperature, and interval values must be positive");
  if (options.profile < -1 || options.profile >= static_cast<int>(PROFILES.size()))
    throw std::runtime_error("profile must be -1 or lie in 0..9");
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
      const std::int64_t new_energy = exchanged_energy(state, delta);
      apply_exchange(state, which, left, right, delta, new_energy);
      validate(state);
    }
  }
  std::cout << "PASS: 10000 exact cyclic exchange-delta checks\n";
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
  std::uint64_t moves = 0;
  std::uint64_t accepted = 0;
  std::uint64_t restarts = 0;

  while (std::chrono::steady_clock::now() < deadline) {
    const int profile = options.profile >= 0
                            ? options.profile
                            : static_cast<int>(restarts % PROFILES.size());
    State state = random_state(profile, rng);
    ++restarts;
    if (state.energy < best.energy) {
      best = state;
      write_checkpoint(options.output, best, options.seed, moves, false);
    }

    for (std::uint64_t phase = 0;
         phase < options.moves_per_restart &&
         std::chrono::steady_clock::now() < deadline;
         ++phase) {
      const int which = sequence_choice(rng);
      const auto [left, right] = random_exchange(state.sequence[which], rng);
      const auto delta = exchange_deltas(state.sequence[which], left, right);
      const std::int64_t candidate_energy = exchanged_energy(state, delta);
      const double fraction = options.moves_per_restart <= 1
                                  ? 1.0
                                  : static_cast<double>(phase) /
                                        static_cast<double>(options.moves_per_restart - 1);
      const double temperature =
          options.start_temperature *
          std::pow(options.end_temperature / options.start_temperature, fraction);
      const std::int64_t increase = candidate_energy - state.energy;
      const bool accept =
          increase <= 0 || uniform(rng) < std::exp(-static_cast<double>(increase) /
                                                   temperature);
      if (accept) {
        apply_exchange(state, which, left, right, delta, candidate_energy);
        ++accepted;
      }
      ++moves;

      if (state.energy < best.energy) {
        best = state;
        validate(best);
        const bool exact = best.energy == 0;
        write_checkpoint(options.output, best, options.seed, moves, exact);
        if (exact) {
          std::cout << "FOUND exact cyclic SDS at profile=" << best.profile
                    << " moves=" << moves << " output=" << options.output << '\n';
          return 0;
        }
      }
      if (moves % options.validate_every == 0) validate(state);

      const auto now = std::chrono::steady_clock::now();
      if (now >= next_report) {
        const double elapsed = std::chrono::duration<double>(now - started).count();
        std::cout << std::fixed << std::setprecision(3)
                  << "elapsed=" << elapsed << " moves=" << moves
                  << " restarts=" << restarts << " accepted=" << accepted
                  << " best_energy=" << best.energy
                  << " best_bad_lags=" << bad_lags(best)
                  << " best_profile=" << best.profile << '\n';
        std::cout.flush();
        next_report = now + std::chrono::duration<double>(options.report_every);
      }
    }
  }
  validate(best);
  write_checkpoint(options.output, best, options.seed, moves, false);
  std::cout << "DONE moves=" << moves << " restarts=" << restarts
            << " best_energy=" << best.energy
            << " bad_lags=" << bad_lags(best)
            << " profile=" << best.profile << " output=" << options.output << '\n';
  return 1;
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
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
