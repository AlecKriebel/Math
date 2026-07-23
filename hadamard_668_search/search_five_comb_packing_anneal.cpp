// Structured annealer for the 32-carrier / 14-hole five-comb packing.
//
// The default carrier family is the exact spectral escape certified by
// verify_five_comb_secant.py.  There are sixteen carrier types
//
//   P_j(z^4) + eps*z^42*P_j(z^4),  j=0,...,7, eps in {-1,+1},
//
// and exactly two copies of every type.  Four sequences have eight fixed
// disjoint carrier slots each; their remaining 14 coefficients are binary
// holes.  Thus every state is automatically a binary quadruple of lengths
// (84,84,83,83), and the multiset of carrier self-norms is already the
// constant 320.  Only packing cross terms and hole terms are searched.
//
// The alternating word is needed to connect that octet to Eliahou's defect,
// but it is not needed for a direct construction.  There are 48 normalized
// complementary four-word multisets of length five.  With --quartet-index,
// one of these quartets is polarized and every resulting type is repeated
// four times, again giving exactly 32 carriers of total energy 320.
//
// This is a constructor, not a verifier.  Any zero is printed as four full
// sign words and must be replayed by the dependency-free BS/Hadamard checker.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kSequenceCount = 4;
constexpr int kSlotsPerSequence = 8;
constexpr int kSlotCount = kSequenceCount * kSlotsPerSequence;
constexpr int kMaxTypeCount = 16;
constexpr int kMaxLength = 84;
constexpr int kCarrierWeight = 10;

constexpr std::array<int, kSequenceCount> kLengths{84, 84, 83, 83};
constexpr std::array<int, kSlotsPerSequence> kShifts{0, 1, 2, 3, 20, 21, 22, 23};
constexpr std::array<std::array<int, 5>, 8> kOctet{{
    {{1, -1, 1, -1, 1}},
    {{-1, -1, -1, -1, -1}},
    {{-1, -1, -1, -1, 1}},
    {{-1, -1, -1, 1, 1}},
    {{-1, -1, 1, -1, 1}},
    {{-1, -1, 1, 1, -1}},
    {{-1, -1, 1, 1, -1}},
    {{-1, 1, -1, -1, 1}},
}};

std::array<std::array<int, 5>, 8> gFamily = kOctet;
int gFamilySize = 8;
int gTypeCount = 16;
int gTypeCopies = 2;
int gQuartetIndex = -1;

using Word = std::array<std::int8_t, kMaxLength>;
using Quadruple = std::array<Word, kSequenceCount>;
using Residuals = std::array<int, kMaxLength>;

struct State {
  std::array<std::uint8_t, kSlotCount> type{};
  std::array<std::int8_t, kSlotCount> slot_sign{};
  std::array<std::array<std::int8_t, 4>, kSequenceCount> hole_sign{};
  Quadruple sequence{};
  Residuals residual{};
  std::int64_t energy = 0;
};

struct Options {
  double seconds = 60.0;
  std::uint64_t seed = 66832014;
  std::uint64_t moves_per_restart = 500'000;
  double start_temperature = 20'000.0;
  double end_temperature = 0.25;
  int quartet_index = -1;
  bool mub_checkpoint = false;
  bool self_test = false;
};

constexpr std::array<std::array<int, 4>, kSequenceCount> kHolePositions{{
    {{40, 41, 82, 83}},
    {{40, 41, 82, 83}},
    {{40, 41, 82, -1}},
    {{40, 41, 82, -1}},
}};

std::array<int, 4> word_signature(const std::array<int, 5>& word) {
  std::array<int, 4> result{};
  for (int lag = 1; lag < 5; ++lag)
    for (int index = 0; index + lag < 5; ++index)
      result[lag - 1] += word[index] * word[index + lag];
  return result;
}

std::vector<std::array<std::array<int, 5>, 4>> complementary_quartets() {
  std::array<std::array<int, 5>, 16> words{};
  for (int mask = 0; mask < 16; ++mask) {
    words[mask][0] = 1;
    for (int index = 1; index < 5; ++index)
      words[mask][index] = ((mask >> (4 - index)) & 1) ? 1 : -1;
  }
  std::array<std::array<int, 4>, 16> signatures{};
  for (int index = 0; index < 16; ++index)
    signatures[index] = word_signature(words[index]);

  std::vector<std::array<std::array<int, 5>, 4>> result;
  for (int first = 0; first < 16; ++first)
    for (int second = first; second < 16; ++second)
      for (int third = second; third < 16; ++third)
        for (int fourth = third; fourth < 16; ++fourth) {
          bool complementary = true;
          for (int lag = 0; lag < 4; ++lag)
            complementary &=
                signatures[first][lag] + signatures[second][lag] +
                    signatures[third][lag] + signatures[fourth][lag] ==
                0;
          if (complementary)
            result.push_back(
                {{words[first], words[second], words[third], words[fourth]}});
        }
  return result;
}

void configure_family(int quartet_index) {
  if (quartet_index < 0) {
    gFamily = kOctet;
    gFamilySize = 8;
    gTypeCount = 16;
    gTypeCopies = 2;
    gQuartetIndex = -1;
    return;
  }
  const auto quartets = complementary_quartets();
  if (quartets.size() != 48)
    throw std::runtime_error("complementary-quartet classification changed");
  if (quartet_index >= static_cast<int>(quartets.size()))
    throw std::runtime_error("quartet index must lie in 0,...,47");
  gFamily.fill({});
  for (int index = 0; index < 4; ++index)
    gFamily[index] = quartets[quartet_index][index];
  gFamilySize = 4;
  gTypeCount = 8;
  gTypeCopies = 4;
  gQuartetIndex = quartet_index;
}

int carrier_value(int type, int offset) {
  if (type < 0 || type >= gTypeCount || offset < 0 ||
      offset >= kCarrierWeight)
    throw std::runtime_error("carrier lookup out of range");
  const int word = type / 2;
  const int separation_sign = type % 2 == 0 ? -1 : 1;
  const int tooth = offset % 5;
  return (offset < 5 ? 1 : separation_sign) * gFamily[word][tooth];
}

int carrier_position(int slot, int offset) {
  const int shift = kShifts[slot % kSlotsPerSequence];
  return shift + 4 * (offset % 5) + (offset < 5 ? 0 : 42);
}

Residuals full_residual(const Quadruple& sequences) {
  Residuals result{};
  for (int which = 0; which < kSequenceCount; ++which) {
    const int length = kLengths[which];
    for (int lag = 0; lag < length; ++lag)
      for (int index = 0; index + lag < length; ++index)
        result[lag] +=
            sequences[which][index] * sequences[which][index + lag];
  }
  return result;
}

std::int64_t residual_energy(const Residuals& residual) {
  std::int64_t result = 0;
  for (int lag = 1; lag < kMaxLength; ++lag)
    result += static_cast<std::int64_t>(residual[lag]) * residual[lag];
  return result;
}

void rebuild(State& state) {
  for (Word& word : state.sequence) word.fill(0);
  for (int slot = 0; slot < kSlotCount; ++slot) {
    const int which = slot / kSlotsPerSequence;
    for (int offset = 0; offset < kCarrierWeight; ++offset) {
      const int position = carrier_position(slot, offset);
      if (state.sequence[which][position] != 0)
        throw std::runtime_error("carrier supports overlap");
      state.sequence[which][position] =
          state.slot_sign[slot] * carrier_value(state.type[slot], offset);
    }
  }
  for (int which = 0; which < kSequenceCount; ++which) {
    for (int hole = 0; hole < 4; ++hole) {
      const int position = kHolePositions[which][hole];
      if (position < 0) continue;
      if (state.sequence[which][position] != 0)
        throw std::runtime_error("hole overlaps a carrier");
      state.sequence[which][position] = state.hole_sign[which][hole];
    }
    for (int index = 0; index < kLengths[which]; ++index)
      if (state.sequence[which][index] != -1 &&
          state.sequence[which][index] != 1)
        throw std::runtime_error("packing left a nonbinary coefficient");
  }
  state.residual = full_residual(state.sequence);
  state.energy = residual_energy(state.residual);
}

void validate(const State& state) {
  std::array<int, kMaxTypeCount> counts{};
  for (int slot = 0; slot < kSlotCount; ++slot) {
    if (state.type[slot] >= gTypeCount)
      throw std::runtime_error("invalid carrier type");
    ++counts[state.type[slot]];
    if (state.slot_sign[slot] != -1 && state.slot_sign[slot] != 1)
      throw std::runtime_error("invalid carrier sign");
  }
  for (int type = 0; type < kMaxTypeCount; ++type) {
    const int wanted = type < gTypeCount ? gTypeCopies : 0;
    if (counts[type] != wanted)
      throw std::runtime_error("carrier multiset changed");
  }
  for (int which = 0; which < kSequenceCount; ++which)
    for (int hole = 0; hole < 4; ++hole) {
      if (kHolePositions[which][hole] < 0) continue;
      if (state.hole_sign[which][hole] != -1 &&
          state.hole_sign[which][hole] != 1)
        throw std::runtime_error("invalid hole sign");
    }
  State rebuilt = state;
  rebuild(rebuilt);
  if (rebuilt.sequence != state.sequence ||
      rebuilt.residual != state.residual ||
      rebuilt.energy != state.energy)
    throw std::runtime_error("incremental packing state is inconsistent");
  if (state.residual[0] != 334)
    throw std::runtime_error("packing has the wrong zero-lag energy");
}

State random_state(std::mt19937_64& generator) {
  State state;
  int slot = 0;
  for (int type = 0; type < gTypeCount; ++type)
    for (int copy = 0; copy < gTypeCopies; ++copy)
      state.type[slot++] = static_cast<std::uint8_t>(type);
  if (slot != kSlotCount)
    throw std::runtime_error("carrier family does not fill 32 slots");
  std::shuffle(state.type.begin(), state.type.end(), generator);
  std::uniform_int_distribution<int> bit(0, 1);
  for (std::int8_t& sign : state.slot_sign) sign = bit(generator) ? 1 : -1;
  for (int which = 0; which < kSequenceCount; ++which)
    for (int hole = 0; hole < 4; ++hole)
      state.hole_sign[which][hole] = bit(generator) ? 1 : -1;
  rebuild(state);
  validate(state);
  return state;
}

State quartet_39_mub_checkpoint() {
  if (gQuartetIndex != 39)
    throw std::runtime_error("the row-compatible MUB checkpoint belongs to quartet 39");
  State state;
  state.type = {
      5, 0, 4, 1, 7, 2, 6, 3, 5, 0, 4, 1, 7, 2, 6, 3,
      5, 0, 4, 1, 7, 2, 6, 3, 5, 0, 4, 1, 7, 2, 6, 3,
  };
  state.slot_sign = {
      -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1,  1,  1, -1, -1,  1,  1,
      -1, -1, -1, -1,  1,  1,  1,  1,
      -1,  1, -1,  1,  1, -1,  1, -1,
  };
  constexpr std::array<int, 14> holes{
      1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1,
  };
  int next_hole = 0;
  for (int which = 0; which < kSequenceCount; ++which)
    for (int hole = 0; hole < 4; ++hole)
      if (kHolePositions[which][hole] >= 0)
        state.hole_sign[which][hole] = holes[next_hole++];
  rebuild(state);
  validate(state);
  if (state.energy != 1'248)
    throw std::runtime_error("the row-compatible MUB checkpoint energy changed");
  int row_square_norm = 0;
  for (int which = 0; which < kSequenceCount; ++which) {
    int row_sum = 0;
    for (int index = 0; index < kLengths[which]; ++index)
      row_sum += state.sequence[which][index];
    row_square_norm += row_sum * row_sum;
  }
  if (row_square_norm != 334)
    throw std::runtime_error("the MUB checkpoint left the z=1 sphere");
  return state;
}

struct Change {
  std::array<std::array<bool, kMaxLength>, kSequenceCount> flip{};
  Residuals delta{};
  std::int64_t new_energy = 0;
};

void mark_slot_change(Change& change, const State& state, int slot,
                      int new_type, int new_sign) {
  const int which = slot / kSlotsPerSequence;
  for (int offset = 0; offset < kCarrierWeight; ++offset) {
    const int old_value =
        state.slot_sign[slot] * carrier_value(state.type[slot], offset);
    const int new_value = new_sign * carrier_value(new_type, offset);
    if (old_value != new_value)
      change.flip[which][carrier_position(slot, offset)] = true;
  }
}

void finish_change(Change& change, const State& state) {
  change.delta.fill(0);
  for (int which = 0; which < kSequenceCount; ++which) {
    const int length = kLengths[which];
    for (int left = 0; left < length; ++left) {
      for (int right = left + 1; right < length; ++right) {
        if (change.flip[which][left] == change.flip[which][right]) continue;
        change.delta[right - left] -=
            2 * state.sequence[which][left] * state.sequence[which][right];
      }
    }
  }
  change.new_energy = 0;
  for (int lag = 1; lag < kMaxLength; ++lag) {
    const std::int64_t updated = state.residual[lag] + change.delta[lag];
    change.new_energy += updated * updated;
  }
}

void apply_change(State& state, const Change& change) {
  for (int which = 0; which < kSequenceCount; ++which)
    for (int position = 0; position < kLengths[which]; ++position)
      if (change.flip[which][position])
        state.sequence[which][position] *= -1;
  for (int lag = 1; lag < kMaxLength; ++lag)
    state.residual[lag] += change.delta[lag];
  state.energy = change.new_energy;
}

void emit(const State& state, std::uint64_t proposals, double elapsed) {
  int bad = 0;
  int maximum = 0;
  for (int lag = 1; lag < kMaxLength; ++lag) {
    bad += state.residual[lag] != 0;
    maximum = std::max(maximum, std::abs(state.residual[lag]));
  }
  std::cout << "BEST family="
            << (gQuartetIndex < 0 ? "octet" : "quartet")
            << " family_index=" << gQuartetIndex << " energy=" << state.energy
            << " bad=" << bad
            << " max_abs=" << maximum << " proposals=" << proposals
            << " seconds=" << std::fixed << std::setprecision(3) << elapsed
            << '\n';
  std::cout << "family_words:";
  for (int word = 0; word < gFamilySize; ++word) {
    std::cout << ' ';
    for (int value : gFamily[word]) std::cout << (value > 0 ? '+' : '-');
  }
  std::cout << "\ntypes:";
  for (int value : state.type) std::cout << ' ' << value;
  std::cout << "\nslot_signs:";
  for (int value : state.slot_sign) std::cout << ' ' << value;
  std::cout << "\nholes:";
  for (int which = 0; which < kSequenceCount; ++which)
    for (int hole = 0; hole < 4; ++hole)
      if (kHolePositions[which][hole] >= 0)
        std::cout << ' ' << static_cast<int>(state.hole_sign[which][hole]);
  std::cout << "\nresiduals:";
  for (int lag = 1; lag < kMaxLength; ++lag)
    std::cout << ' ' << state.residual[lag];
  std::cout << '\n';
  if (state.energy == 0) {
    std::cout << "EXACT SIGN WORDS\n";
    for (int which = 0; which < kSequenceCount; ++which) {
      for (int index = 0; index < kLengths[which]; ++index)
        std::cout << (state.sequence[which][index] > 0 ? '+' : '-');
      std::cout << '\n';
    }
  }
  std::cout.flush();
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto value = [&]() -> std::string {
      if (++index >= argc) throw std::runtime_error("missing option value");
      return argv[index];
    };
    if (argument == "--seconds")
      options.seconds = std::stod(value());
    else if (argument == "--seed")
      options.seed = std::stoull(value());
    else if (argument == "--moves-per-restart")
      options.moves_per_restart = std::stoull(value());
    else if (argument == "--temperature-start")
      options.start_temperature = std::stod(value());
    else if (argument == "--temperature-end")
      options.end_temperature = std::stod(value());
    else if (argument == "--quartet-index")
      options.quartet_index = std::stoi(value());
    else if (argument == "--mub-checkpoint")
      options.mub_checkpoint = true;
    else if (argument == "--self-test")
      options.self_test = true;
    else
      throw std::runtime_error("unknown option: " + argument);
  }
  if (!(options.seconds > 0.0) || options.moves_per_restart == 0 ||
      !(options.start_temperature > 0.0) ||
      !(options.end_temperature > 0.0))
    throw std::runtime_error("invalid search option");
  return options;
}

void self_test() {
  std::mt19937_64 generator(668);
  State state = random_state(generator);
  std::uniform_int_distribution<int> slot_distribution(0, kSlotCount - 1);
  for (int round = 0; round < 1000; ++round) {
    int first = slot_distribution(generator);
    int second = slot_distribution(generator);
    while (second == first) second = slot_distribution(generator);
    Change change;
    mark_slot_change(change, state, first, state.type[second],
                     state.slot_sign[first]);
    mark_slot_change(change, state, second, state.type[first],
                     state.slot_sign[second]);
    finish_change(change, state);
    std::swap(state.type[first], state.type[second]);
    apply_change(state, change);
    validate(state);
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    configure_family(options.mub_checkpoint ? 39 : options.quartet_index);
    if (options.self_test) {
      self_test();
      std::cout << "self_test=passed\n";
      return 0;
    }
    std::mt19937_64 generator(options.seed);
    std::uniform_int_distribution<int> slot_distribution(0, kSlotCount - 1);
    std::uniform_int_distribution<int> sequence_distribution(
        0, kSequenceCount - 1);
    std::uniform_int_distribution<int> geometric_slot_distribution(
        0, kSlotsPerSequence - 1);
    std::uniform_int_distribution<int> hole_distribution(0, 3);
    std::uniform_real_distribution<double> unit(0.0, 1.0);
    std::uniform_int_distribution<int> move_kind(0, 11);

    const auto start = std::chrono::steady_clock::now();
    const auto deadline =
        start + std::chrono::duration<double>(options.seconds);
    State best;
    best.energy = std::numeric_limits<std::int64_t>::max();
    std::uint64_t proposals = 0;
    bool first_restart = true;

    while (std::chrono::steady_clock::now() < deadline) {
      State state =
          options.mub_checkpoint && first_restart
              ? quartet_39_mub_checkpoint()
              : random_state(generator);
      first_restart = false;
      if (state.energy < best.energy) {
        best = state;
        emit(best, proposals, 0.0);
      }
      for (std::uint64_t step = 0; step < options.moves_per_restart; ++step) {
        if ((step & 4095ULL) == 0 &&
            std::chrono::steady_clock::now() >= deadline)
          break;
        const double fraction =
            static_cast<double>(step) / options.moves_per_restart;
        const double temperature =
            options.start_temperature *
            std::pow(options.end_temperature / options.start_temperature,
                     fraction);
        const int kind = move_kind(generator);
        Change change;
        auto proposed_type = state.type;
        auto proposed_sign = state.slot_sign;
        bool carrier_move = false;
        int hole_sequence = -1;
        int hole_index = -1;

        if (kind <= 5) {
          carrier_move = true;
          int first = slot_distribution(generator);
          int second = slot_distribution(generator);
          while (second == first) second = slot_distribution(generator);
          std::swap(proposed_type[first], proposed_type[second]);
          if (kind == 2 || kind == 4 || kind == 5)
            proposed_sign[first] *= -1;
          if (kind == 3 || kind == 4 || kind == 5)
            proposed_sign[second] *= -1;
        } else if (kind <= 7) {
          hole_sequence = sequence_distribution(generator);
          hole_index = hole_distribution(generator);
          while (kHolePositions[hole_sequence][hole_index] < 0) {
            hole_sequence = sequence_distribution(generator);
            hole_index = hole_distribution(generator);
          }
          change.flip[hole_sequence]
                     [kHolePositions[hole_sequence][hole_index]] = true;
        } else if (kind <= 9) {
          // Exchange two entire geometric columns across all four rows.
          // This traverses non-affine type and projective assignments while
          // preserving the carrier histogram in one algebraic move.
          carrier_move = true;
          int first_geometric = geometric_slot_distribution(generator);
          int second_geometric = geometric_slot_distribution(generator);
          while (second_geometric == first_geometric)
            second_geometric = geometric_slot_distribution(generator);
          for (int which = 0; which < kSequenceCount; ++which) {
            const int first = which * kSlotsPerSequence + first_geometric;
            const int second = which * kSlotsPerSequence + second_geometric;
            std::swap(proposed_type[first], proposed_type[second]);
            if (kind == 8)
              std::swap(proposed_sign[first], proposed_sign[second]);
          }
        } else if (kind == 10) {
          // A three-cycle can cross barriers that contain no descending
          // transposition while retaining the exact carrier inventory.
          carrier_move = true;
          int first = slot_distribution(generator);
          int second = slot_distribution(generator);
          int third = slot_distribution(generator);
          while (second == first) second = slot_distribution(generator);
          while (third == first || third == second)
            third = slot_distribution(generator);
          const auto saved_type = proposed_type[first];
          proposed_type[first] = proposed_type[second];
          proposed_type[second] = proposed_type[third];
          proposed_type[third] = saved_type;
        } else {
          // Flip a whole four-row sign column, the natural move between the
          // two projective-Hadamard packing geometries.
          carrier_move = true;
          const int geometric = geometric_slot_distribution(generator);
          for (int which = 0; which < kSequenceCount; ++which)
            proposed_sign[which * kSlotsPerSequence + geometric] *= -1;
        }
        if (carrier_move) {
          for (int slot = 0; slot < kSlotCount; ++slot)
            if (proposed_type[slot] != state.type[slot] ||
                proposed_sign[slot] != state.slot_sign[slot])
              mark_slot_change(change, state, slot, proposed_type[slot],
                               proposed_sign[slot]);
        }
        finish_change(change, state);
        ++proposals;
        const std::int64_t difference = change.new_energy - state.energy;
        if (difference <= 0 ||
            unit(generator) <
                std::exp(-static_cast<double>(difference) / temperature)) {
          if (carrier_move) {
            state.type = proposed_type;
            state.slot_sign = proposed_sign;
          } else {
            state.hole_sign[hole_sequence][hole_index] *= -1;
          }
          apply_change(state, change);
        }
        if (state.energy < best.energy) {
          best = state;
          validate(best);
          const double elapsed =
              std::chrono::duration<double>(
                  std::chrono::steady_clock::now() - start)
                  .count();
          emit(best, proposals, elapsed);
          if (best.energy == 0) return 0;
        }
      }
    }
    return best.energy == 0 ? 0 : 2;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
