// Lossless modulo-27 audit for the LP(333) order-three profile
// shell (n_9,n_3,n_0)=(3,9,12).
//
// It enumerates one representative of every signed skeleton orbit, restores
// the medium phases quartet by quartet subject to the primitive flag, inserts
// exactly three high letters, joins on the exact aggregate and all twelve
// modulo-nine correlation coordinates, evaluates the quadratic modulo-27
// layer and an independent cubic characteristic-37 moment, and replays every
// modulo-nine survivor with exact Eisenstein arithmetic.
//
// The key lossless identity is that, after a signed skeleton is fixed, every
// medium-phase change and every high insertion is divisible by three.
// Products of two changes therefore vanish modulo nine, so their correlation
// signatures add.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int P = 37;
constexpr int CHANNELS = 2;
constexpr int CLASSES = 12;
constexpr int PAIRS = 6;
constexpr int SLOTS = 24;

struct E {
  int a = 0;
  int b = 0;
  friend bool operator==(const E&, const E&) = default;
};

E add(E x, E y) { return {x.a + y.a, x.b + y.b}; }
E sub(E x, E y) { return {x.a - y.a, x.b - y.b}; }
E scale(int n, E x) { return {n * x.a, n * x.b}; }
E conjugate(E x) { return {x.a - x.b, -x.b}; }
E multiply(E x, E y) {
  return {x.a * y.a - x.b * y.b,
          x.a * y.b + x.b * y.a - x.b * y.b};
}

int mod(int value, int modulus) {
  value %= modulus;
  return value < 0 ? value + modulus : value;
}

using Local = std::array<int, 4>;
using Target = std::array<int, 4>;
using Skeleton = std::array<std::array<std::int8_t, CLASSES>, CHANNELS>;
using Values = std::array<std::array<E, 13>, CHANNELS>;
using Signature = std::array<std::uint8_t, 12>;
using Aggregate = std::array<std::int8_t, 4>;

constexpr std::array<Target, 22> TARGETS = {{
    {{-3, -3, -4, -2}}, {{-3, -3, -2, 2}},  {{-3, 0, -3, -3}},
    {{-3, 0, 0, 3}},    {{-1, -2, -5, -1}}, {{-1, -2, -4, 1}},
    {{0, 3, -4, -2}},   {{0, 3, -2, 2}},    {{1, -1, 2, -2}},
    {{1, -1, 4, 2}},    {{1, 2, -5, -1}},   {{1, 2, -4, 1}},
    {{2, -2, -4, -2}},  {{2, -2, -2, 2}},   {{2, 1, 2, -2}},
    {{2, 1, 4, 2}},     {{3, 0, 0, -3}},    {{3, 0, 3, 3}},
    {{4, -1, 0, 0}},    {{4, 2, -4, -2}},   {{4, 2, -2, 2}},
    {{5, 1, 0, 0}},
}};

constexpr std::array<E, 3> OMEGA_POWERS = {{
    {1, 0}, {0, 1}, {-1, -1},
}};
constexpr E LAMBDA = {1, -1};

struct Geometry {
  std::array<std::array<int, 3>, CLASSES> classes{};
  std::array<int, P> class_of{};
  std::array<std::array<std::array<int, 13>, 13>, PAIRS> transition{};
};

Geometry build_geometry() {
  Geometry result;
  result.class_of.fill(-1);
  constexpr std::array<int, 3> subgroup = {1, 26, 10};
  int power = 1;
  for (int index = 0; index < CLASSES; ++index) {
    for (int offset = 0; offset < 3; ++offset) {
      int value = power * subgroup[offset] % P;
      result.classes[index][offset] = value;
      if (result.class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      result.class_of[value] = index;
    }
    power = power * 2 % P;
  }
  auto part = [&](int value) {
    return value == 0 ? 0 : result.class_of[value] + 1;
  };
  for (int lag = 0; lag < PAIRS; ++lag) {
    const int shift = result.classes[lag][0];
    for (int source = 0; source < P; ++source) {
      ++result.transition[lag][part(source)][part((source + shift) % P)];
    }
  }
  return result;
}

std::vector<Local> local_states() {
  std::vector<Local> result;
  for (int a0 = -1; a0 <= 1; ++a0) {
    for (int a1 = -1; a1 <= 1; ++a1) {
      for (int b0 = -1; b0 <= 1; ++b0) {
        for (int b1 = -1; b1 <= 1; ++b1) {
          if (mod(a1 - a0 - b1 + b0, 3) == 0) {
            result.push_back({a0, a1, b0, b1});
          }
        }
      }
    }
  }
  return result;
}

int medium_count(const Local& state) {
  int result = 0;
  for (int value : state) result += value != 0;
  return result;
}

int parity_sign(int class_index) {
  return class_index % 2 == 0 ? 1 : -1;
}

int actual_factor(int channel, int class_index) {
  const int epsilon = parity_sign(class_index);
  return channel == 0 ? -epsilon : epsilon;
}

int slot_index(int channel, int class_index) {
  return channel * CLASSES + class_index;
}

std::pair<int, int> decode_slot(int slot) {
  return {slot / CLASSES, slot % CLASSES};
}

Skeleton selected_to_skeleton(const std::array<Local, PAIRS>& selected) {
  Skeleton result{};
  for (int pair = 0; pair < PAIRS; ++pair) {
    result[0][pair] = static_cast<std::int8_t>(selected[pair][0]);
    result[0][pair + 6] = static_cast<std::int8_t>(selected[pair][1]);
    result[1][pair] = static_cast<std::int8_t>(selected[pair][2]);
    result[1][pair + 6] = static_cast<std::int8_t>(selected[pair][3]);
  }
  return result;
}

Skeleton transform_skeleton(const Skeleton& input, int group) {
  const int rotation = group / 4;
  const bool stars[2] = {
      static_cast<bool>((group / 2) % 2),
      static_cast<bool>(group % 2),
  };
  Skeleton result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    const int offset = (2 * rotation + (stars[channel] ? 6 : 0)) % 12;
    const int sign = stars[channel] ? -1 : 1;
    for (int index = 0; index < CLASSES; ++index) {
      result[channel][index] = static_cast<std::int8_t>(
          sign * input[channel][(index + offset) % CLASSES]);
    }
  }
  return result;
}

bool skeleton_less(const Skeleton& left, const Skeleton& right) {
  return left < right;
}

bool canonical_skeleton(const Skeleton& skeleton) {
  for (int group = 1; group < 24; ++group) {
    if (skeleton_less(transform_skeleton(skeleton, group), skeleton)) {
      return false;
    }
  }
  return true;
}

std::array<int, 2> aggregate_residue(const Skeleton& skeleton) {
  std::array<int, 2> result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    for (int class_index = 0; class_index < CLASSES; ++class_index) {
      result[channel] += actual_factor(channel, class_index) *
                         skeleton[channel][class_index];
    }
    result[channel] = mod(result[channel], 3);
  }
  return result;
}

E raw_medium(int sign, int phase) {
  return scale(sign, multiply(LAMBDA, OMEGA_POWERS.at(phase)));
}

E raw_high(int phase) {
  return scale(3, OMEGA_POWERS.at(phase));
}

Values base_values(const Skeleton& skeleton) {
  Values result{};
  result[0][0] = {-1, 0};
  result[1][0] = {2, 0};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    for (int class_index = 0; class_index < CLASSES; ++class_index) {
      const int sign = skeleton[channel][class_index];
      if (!sign) continue;
      result[channel][class_index + 1] =
          scale(actual_factor(channel, class_index), raw_medium(sign, 0));
    }
  }
  return result;
}

std::array<E, PAIRS> exact_correlations(const Geometry& geometry,
                                        const Values& values) {
  std::array<E, PAIRS> result{};
  for (int lag = 0; lag < PAIRS; ++lag) {
    E total{};
    for (int channel = 0; channel < CHANNELS; ++channel) {
      for (int source = 0; source < 13; ++source) {
        for (int target = 0; target < 13; ++target) {
          const int count = geometry.transition[lag][source][target];
          if (!count) continue;
          total = add(
              total,
              scale(count,
                    multiply(values[channel][target],
                             conjugate(values[channel][source]))));
        }
      }
    }
    result[lag] = total;
  }
  return result;
}

Signature reduced_signature(const std::array<E, PAIRS>& exact) {
  Signature result{};
  for (int lag = 0; lag < PAIRS; ++lag) {
    result[2 * lag] = static_cast<std::uint8_t>(mod(exact[lag].a, 9));
    result[2 * lag + 1] =
        static_cast<std::uint8_t>(mod(exact[lag].b, 9));
  }
  return result;
}

Signature add_signature(Signature left, const Signature& right) {
  for (int index = 0; index < 12; ++index) {
    left[index] =
        static_cast<std::uint8_t>((left[index] + right[index]) % 9);
  }
  return left;
}

Signature one_slot_delta(const Geometry& geometry, const Values& base,
                         int channel, int class_index, E delta) {
  const int part = class_index + 1;
  std::array<E, PAIRS> result{};
  for (int lag = 0; lag < PAIRS; ++lag) {
    E total{};
    for (int source = 0; source < 13; ++source) {
      const int count = geometry.transition[lag][source][part];
      if (count) {
        total = add(total,
                    scale(count,
                          multiply(delta, conjugate(base[channel][source]))));
      }
    }
    for (int target = 0; target < 13; ++target) {
      const int count = geometry.transition[lag][part][target];
      if (count) {
        total = add(total,
                    scale(count,
                          multiply(base[channel][target], conjugate(delta))));
      }
    }
    const int diagonal = geometry.transition[lag][part][part];
    if (diagonal) {
      total = add(total,
                  scale(diagonal, multiply(delta, conjugate(delta))));
    }
    result[lag] = total;
  }
  return reduced_signature(result);
}

Aggregate base_aggregate(const Values& values) {
  Aggregate result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    E total{};
    for (int part = 1; part < 13; ++part) {
      total = add(total, values[channel][part]);
    }
    if (total.a < -127 || total.a > 127 || total.b < -127 ||
        total.b > 127) {
      throw std::runtime_error("aggregate left int8 range");
    }
    result[2 * channel] = static_cast<std::int8_t>(total.a);
    result[2 * channel + 1] = static_cast<std::int8_t>(total.b);
  }
  return result;
}

Aggregate add_aggregate(Aggregate left, int channel, E delta) {
  const int a = static_cast<int>(left[2 * channel]) + delta.a;
  const int b = static_cast<int>(left[2 * channel + 1]) + delta.b;
  if (a < -127 || a > 127 || b < -127 || b > 127) {
    throw std::runtime_error("aggregate delta left int8 range");
  }
  left[2 * channel] = static_cast<std::int8_t>(a);
  left[2 * channel + 1] = static_cast<std::int8_t>(b);
  return left;
}

int primitive_flag(const Signature& signature, int pair) {
  const int a = signature[2 * pair];
  const int b = signature[2 * pair + 1];
  if (a % 3 || b % 3) {
    throw std::runtime_error("signed skeleton lost divisibility by three");
  }
  return (a / 3 + b / 3) % 3;
}

struct SlotOption {
  Signature signature{};
  E aggregate{};
};

struct Prepared {
  Values base{};
  Signature base_signature{};
  Aggregate base_aggregate{};
  std::array<std::array<SlotOption, 3>, SLOTS> phase_options{};
  std::array<int, 9> medium_slots{};
  int medium_count = 0;
  std::array<int, 15> zero_slots{};
  int zero_count = 0;
};

Prepared prepare(const Geometry& geometry, const Skeleton& skeleton) {
  Prepared result;
  result.base = base_values(skeleton);
  result.base_signature =
      reduced_signature(exact_correlations(geometry, result.base));
  result.base_aggregate = base_aggregate(result.base);
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = skeleton[channel][class_index];
    const int factor = actual_factor(channel, class_index);
    if (sign) {
      result.medium_slots[result.medium_count++] = slot;
      const E old_value =
          scale(factor, raw_medium(sign, 0));
      for (int phase = 0; phase < 3; ++phase) {
        const E new_value =
            scale(factor, raw_medium(sign, phase));
        const E delta = sub(new_value, old_value);
        result.phase_options[slot][phase] = {
            one_slot_delta(geometry, result.base, channel, class_index, delta),
            delta,
        };
      }
    } else {
      result.zero_slots[result.zero_count++] = slot;
      for (int phase = 0; phase < 3; ++phase) {
        const E delta = scale(factor, raw_high(phase));
        result.phase_options[slot][phase] = {
            one_slot_delta(geometry, result.base, channel, class_index, delta),
            delta,
        };
      }
    }
  }
  if (result.medium_count != 9 || result.zero_count != 15) {
    throw std::runtime_error("prepared object left the (3,9,12) shell");
  }
  return result;
}

struct RecordKey {
  std::array<std::int8_t, 16> coordinates{};
  friend bool operator==(const RecordKey&, const RecordKey&) = default;
};

struct RecordKeyHash {
  std::size_t operator()(const RecordKey& key) const {
    std::uint64_t value = 1469598103934665603ULL;
    for (std::int8_t coordinate : key.coordinates) {
      value ^= static_cast<std::uint8_t>(coordinate);
      value *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(value);
  }
};

RecordKey record_key(const Aggregate& aggregate,
                     const Signature& signature) {
  RecordKey result;
  for (int index = 0; index < 4; ++index) {
    result.coordinates[index] = aggregate[index];
  }
  for (int index = 0; index < 12; ++index) {
    result.coordinates[index + 4] =
        static_cast<std::int8_t>(signature[index]);
  }
  return result;
}

RecordKey required_key(const Target& target, const Aggregate& high_aggregate,
                       const Signature& high_signature) {
  Aggregate aggregate{};
  Signature signature{};
  for (int index = 0; index < 4; ++index) {
    const int value = target[index] - high_aggregate[index];
    if (value < -127 || value > 127) {
      throw std::runtime_error("required aggregate left int8 range");
    }
    aggregate[index] = static_cast<std::int8_t>(value);
  }
  for (int index = 0; index < 12; ++index) {
    signature[index] =
        static_cast<std::uint8_t>((9 - high_signature[index]) % 9);
  }
  return record_key(aggregate, signature);
}

struct RecordValue {
  std::vector<std::uint32_t> phase_codes;
};

struct LocalMediumOption {
  Signature delta_signature{};
  Aggregate delta_aggregate{};
  std::uint32_t phase_code = 0;
};

using LocalTable = std::vector<LocalMediumOption>;

LocalTable local_medium_options(const Skeleton& skeleton,
                                const Prepared& prepared,
                                const std::array<int, 3>& high_slots,
                                int pair) {
  std::vector<int> slots;
  for (int channel = 0; channel < CHANNELS; ++channel) {
    for (int class_index : {pair, pair + 6}) {
      if (skeleton[channel][class_index]) {
        slots.push_back(slot_index(channel, class_index));
      }
    }
  }
  LocalTable result;
  int combinations = 1;
  for (std::size_t ignored = 0; ignored < slots.size(); ++ignored) {
    (void)ignored;
    combinations *= 3;
  }
  for (int code = 0; code < combinations; ++code) {
    int remaining = code;
    Signature delta{};
    Aggregate aggregate{};
    std::uint32_t global_code = 0;
    std::uint32_t place = 1;
    for (int slot : prepared.medium_slots) {
      int phase = 0;
      auto found = std::find(slots.begin(), slots.end(), slot);
      if (found != slots.end()) {
        const int local_index =
            static_cast<int>(std::distance(slots.begin(), found));
        int local_code = code;
        for (int index = 0; index < local_index; ++index) local_code /= 3;
        phase = local_code % 3;
      }
      global_code += place * static_cast<std::uint32_t>(phase);
      place *= 3;
    }
    remaining = code;
    for (int slot : slots) {
      const int phase = remaining % 3;
      remaining /= 3;
      const auto& option = prepared.phase_options[slot][phase];
      delta = add_signature(delta, option.signature);
      const int channel = decode_slot(slot).first;
      aggregate = add_aggregate(aggregate, channel, option.aggregate);
    }
    Signature flag_signature =
        add_signature(prepared.base_signature, delta);
    for (int high_slot : high_slots) {
      if (decode_slot(high_slot).second % 6 != pair) continue;
      flag_signature = add_signature(
          flag_signature,
          prepared.phase_options[high_slot][0].signature);
    }
    if (primitive_flag(flag_signature, pair) == 0) {
      result.push_back({delta, aggregate, global_code});
    }
  }
  return result;
}

struct SearchStats {
  std::uint64_t raw_skeletons = 0;
  std::uint64_t canonical_skeletons = 0;
  std::uint64_t skeleton_targets = 0;
  std::uint64_t support_trials = 0;
  std::uint64_t extendible_supports = 0;
  std::uint64_t medium_records = 0;
  std::uint64_t high_records = 0;
  std::uint64_t mod9_survivors = 0;
  std::uint64_t mod27_survivors = 0;
  std::uint64_t cubic37_survivors = 0;
  std::uint64_t mod27_cubic37_survivors = 0;
  std::uint64_t exact_survivors = 0;
  std::uint64_t exact_replays = 0;
};

struct Witness {
  std::array<int, CLASSES> ids_a{};
  std::array<int, CLASSES> ids_b{};
  Target target{};
  std::array<E, PAIRS> exact{};
};

struct NearWitness {
  std::array<int, CLASSES> ids_a{};
  std::array<int, CLASSES> ids_b{};
  Target target{};
  int cubic_j = 0;
  std::array<E, PAIRS> exact{};
};

int medium_id(int sign, int phase) {
  constexpr int positive[3] = {7, 6, 1};
  constexpr int negative[3] = {2, 4, 8};
  return sign > 0 ? positive[phase] : negative[phase];
}

int high_id(int phase) {
  constexpr int values[3] = {9, 3, 0};
  return values[phase];
}

Values assignment_values(
    const Skeleton& skeleton, std::uint32_t medium_code,
    const std::array<int, 3>& high_slots, int high_code,
    std::array<int, CLASSES>& ids_a, std::array<int, CLASSES>& ids_b) {
  Values result{};
  result[0][0] = {-1, 0};
  result[1][0] = {2, 0};
  ids_a.fill(5);
  ids_b.fill(5);
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = skeleton[channel][class_index];
    if (!sign) continue;
    const int phase = medium_code % 3;
    medium_code /= 3;
    const int id = medium_id(sign, phase);
    (channel == 0 ? ids_a : ids_b)[class_index] = id;
    result[channel][class_index + 1] =
        scale(actual_factor(channel, class_index), raw_medium(sign, phase));
  }
  for (int high_slot : high_slots) {
    const int phase = high_code % 3;
    high_code /= 3;
    const auto [channel, class_index] = decode_slot(high_slot);
    const int id = high_id(phase);
    (channel == 0 ? ids_a : ids_b)[class_index] = id;
    result[channel][class_index + 1] =
        scale(actual_factor(channel, class_index), raw_high(phase));
  }
  return result;
}

bool exact_target(const Values& values, const Target& target) {
  Aggregate aggregate = base_aggregate(values);
  for (int index = 0; index < 4; ++index) {
    if (aggregate[index] != target[index]) return false;
  }
  return true;
}

int determinant(E left, E right) {
  return left.a * right.b - left.b * right.a;
}

int cubic_character_filter(const Values& values, const Target& target) {
  std::array<E, CHANNELS> moment{};
  int weight = 1;
  for (int class_index = 0; class_index < CLASSES; ++class_index) {
    for (int channel = 0; channel < CHANNELS; ++channel) {
      moment[channel] =
          add(moment[channel],
              scale(weight, values[channel][class_index + 1]));
    }
    weight = weight * 8 % P;
  }
  const E physical_a = {-1 + 3 * target[0], 3 * target[1]};
  const E physical_b = {2 + 3 * target[2], 3 * target[3]};
  return mod(determinant(moment[0], physical_a) +
                 determinant(moment[1], physical_b),
             P);
}

void verify_cubic_identity(const std::array<E, PAIRS>& exact, int cubic_j) {
  E moment{};
  int weight = 1;
  for (int class_index = 0; class_index < CLASSES; ++class_index) {
    const E value =
        class_index < PAIRS ? exact[class_index]
                            : conjugate(exact[class_index - PAIRS]);
    moment = add(moment, scale(3 * weight, value));
    weight = weight * 8 % P;
  }
  const E expected = {-3 * cubic_j, -6 * cubic_j};
  if (mod(moment.a - expected.a, P) != 0 ||
      mod(moment.b - expected.b, P) != 0) {
    throw std::runtime_error("cubic characteristic-37 identity failed");
  }
}

class Search {
 public:
  Search(std::uint64_t canonical_skip, std::uint64_t canonical_limit,
         bool stop_first)
      : geometry_(build_geometry()),
        states_(local_states()),
        canonical_skip_(canonical_skip),
        canonical_limit_(canonical_limit),
        stop_first_(stop_first) {}

  void run() { enumerate_skeleton(0, 0); }

  const SearchStats& stats() const { return stats_; }
  const std::vector<Witness>& witnesses() const { return witnesses_; }
  const std::vector<NearWitness>& near_witnesses() const {
    return near_witnesses_;
  }

 private:
  void enumerate_skeleton(int pair, int total_medium) {
    if (stopped_) return;
    if (pair == PAIRS) {
      if (total_medium == 9) process_skeleton();
      return;
    }
    const int remaining = PAIRS - pair - 1;
    for (const Local& state : states_) {
      const int count = medium_count(state);
      const int next = total_medium + count;
      if (next > 9 || next + 4 * remaining < 9) continue;
      selected_[pair] = state;
      enumerate_skeleton(pair + 1, next);
      if (stopped_) return;
    }
  }

  void process_skeleton() {
    ++stats_.raw_skeletons;
    const Skeleton skeleton = selected_to_skeleton(selected_);
    if (!canonical_skeleton(skeleton)) return;
    if (canonical_seen_++ < canonical_skip_) return;
    if (stats_.canonical_skeletons >= canonical_limit_) {
      stopped_ = true;
      return;
    }
    ++stats_.canonical_skeletons;
    const auto residue = aggregate_residue(skeleton);
    std::vector<Target> targets;
    for (const Target& target : TARGETS) {
      if (mod(target[0], 3) == residue[0] &&
          mod(target[2], 3) == residue[1]) {
        targets.push_back(target);
      }
    }
    stats_.skeleton_targets += targets.size();
    const Prepared prepared = prepare(geometry_, skeleton);

    for (int first = 0; first < prepared.zero_count; ++first) {
      for (int second = first + 1; second < prepared.zero_count; ++second) {
        for (int third = second + 1; third < prepared.zero_count; ++third) {
          ++stats_.support_trials;
          const std::array<int, 3> high_slots = {
              prepared.zero_slots[first],
              prepared.zero_slots[second],
              prepared.zero_slots[third],
          };
          std::array<LocalTable, PAIRS> local_tables;
          bool extendible = true;
          for (int pair = 0; pair < PAIRS; ++pair) {
            local_tables[pair] =
                local_medium_options(skeleton, prepared, high_slots, pair);
            if (local_tables[pair].empty()) {
              extendible = false;
              break;
            }
          }
          if (!extendible) continue;
          ++stats_.extendible_supports;
          process_support_targets(
              skeleton, prepared, high_slots, local_tables, targets);
          if (stopped_) return;
        }
      }
    }
  }

  void process_support_targets(
      const Skeleton& skeleton, const Prepared& prepared,
      const std::array<int, 3>& high_slots,
      const std::array<LocalTable, PAIRS>& local_tables,
      const std::vector<Target>& targets) {
    std::unordered_map<RecordKey, RecordValue, RecordKeyHash> medium;
    std::uint64_t expected = 1;
    for (const auto& table : local_tables) expected *= table.size();
    medium.reserve(static_cast<std::size_t>(expected * 2 + 1));

    auto recurse = [&](auto&& self, int pair, Signature signature,
                       Aggregate aggregate, std::uint32_t phase_code) -> void {
      if (pair == PAIRS) {
        ++stats_.medium_records;
        RecordKey key = record_key(aggregate, signature);
        medium[key].phase_codes.push_back(phase_code);
        return;
      }
      for (const auto& option : local_tables[pair]) {
        Signature next_signature =
            add_signature(signature, option.delta_signature);
        Aggregate next_aggregate = aggregate;
        for (int index = 0; index < 4; ++index) {
          const int value = static_cast<int>(next_aggregate[index]) +
                            option.delta_aggregate[index];
          next_aggregate[index] = static_cast<std::int8_t>(value);
        }
        self(self, pair + 1, next_signature, next_aggregate,
             phase_code + option.phase_code);
      }
    };
    recurse(recurse, 0, prepared.base_signature, prepared.base_aggregate, 0);

    for (int high_code = 0; high_code < 27; ++high_code) {
      ++stats_.high_records;
      int remaining = high_code;
      Signature high_signature{};
      Aggregate high_aggregate{};
      for (int slot : high_slots) {
        const int phase = remaining % 3;
        remaining /= 3;
        const auto& option = prepared.phase_options[slot][phase];
        high_signature = add_signature(high_signature, option.signature);
        const int channel = decode_slot(slot).first;
        high_aggregate =
            add_aggregate(high_aggregate, channel, option.aggregate);
      }
      for (const Target& target : targets) {
        auto found =
            medium.find(required_key(target, high_aggregate, high_signature));
        if (found == medium.end()) continue;
        stats_.mod9_survivors += found->second.phase_codes.size();
        for (std::uint32_t phase_code : found->second.phase_codes) {
          std::array<int, CLASSES> ids_a{}, ids_b{};
          Values values = assignment_values(
              skeleton, phase_code, high_slots, high_code, ids_a, ids_b);
          if (!exact_target(values, target)) {
            throw std::runtime_error("joined aggregate failed exact replay");
          }
          const int cubic_j = cubic_character_filter(values, target);
          const bool cubic37 = cubic_j == 0;
          if (cubic37) {
            ++stats_.cubic37_survivors;
          }
          ++stats_.exact_replays;
          const auto exact = exact_correlations(geometry_, values);
          verify_cubic_identity(exact, cubic_j);
          bool zero_mod27 = true;
          for (E value : exact) {
            zero_mod27 &= value.a % 27 == 0 && value.b % 27 == 0;
          }
          if (zero_mod27) {
            ++stats_.mod27_survivors;
            near_witnesses_.push_back(
                {ids_a, ids_b, target, cubic_j, exact});
            if (cubic37) {
              ++stats_.mod27_cubic37_survivors;
            }
          }
          bool zero = true;
          for (E value : exact) zero &= value == E{};
          if (zero) {
            ++stats_.exact_survivors;
            witnesses_.push_back({ids_a, ids_b, target, exact});
            if (stop_first_) {
              stopped_ = true;
              return;
            }
          }
        }
      }
    }
  }

  Geometry geometry_;
  std::vector<Local> states_;
  std::array<Local, PAIRS> selected_{};
  std::uint64_t canonical_skip_;
  std::uint64_t canonical_limit_;
  std::uint64_t canonical_seen_ = 0;
  bool stop_first_ = false;
  bool stopped_ = false;
  SearchStats stats_;
  std::vector<Witness> witnesses_;
  std::vector<NearWitness> near_witnesses_;
};

void print_ids(const char* label, const std::array<int, CLASSES>& ids) {
  std::cout << label << "=";
  for (int index = 0; index < CLASSES; ++index) {
    if (index) std::cout << ",";
    std::cout << ids[index];
  }
  std::cout << "\n";
}

void print_exact_table(const char* label,
                       const std::array<E, PAIRS>& exact) {
  std::cout << label << "=";
  for (int pair = 0; pair < PAIRS; ++pair) {
    if (pair) std::cout << ";";
    std::cout << exact[pair].a << "," << exact[pair].b;
  }
  std::cout << "\n";
}

void require_full_census(const SearchStats& stats,
                         std::size_t near_witnesses) {
  const SearchStats expected = {
      908800,     38296,     93564,     17424680,
      1817356,    470489796, 49068612,  479850,
      2,          13004,     0,          0,
      479850,
  };
  if (stats.raw_skeletons != expected.raw_skeletons ||
      stats.canonical_skeletons != expected.canonical_skeletons ||
      stats.skeleton_targets != expected.skeleton_targets ||
      stats.support_trials != expected.support_trials ||
      stats.extendible_supports != expected.extendible_supports ||
      stats.medium_records != expected.medium_records ||
      stats.high_records != expected.high_records ||
      stats.mod9_survivors != expected.mod9_survivors ||
      stats.mod27_survivors != expected.mod27_survivors ||
      stats.cubic37_survivors != expected.cubic37_survivors ||
      stats.mod27_cubic37_survivors !=
          expected.mod27_cubic37_survivors ||
      stats.exact_survivors != expected.exact_survivors ||
      stats.exact_replays != expected.exact_replays ||
      near_witnesses != 2) {
    throw std::runtime_error("complete shell-three census changed");
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    std::uint64_t skip = 0;
    std::uint64_t limit = std::numeric_limits<std::uint64_t>::max();
    bool stop_first = false;
    for (int index = 1; index < argc; ++index) {
      std::string argument = argv[index];
      if (argument == "--stop-first") {
        stop_first = true;
      } else if (argument == "--skip" && index + 1 < argc) {
        skip = std::stoull(argv[++index]);
      } else if (argument == "--limit" && index + 1 < argc) {
        limit = std::stoull(argv[++index]);
      } else {
        throw std::runtime_error(
            "usage: search [--skip N] [--limit N] [--stop-first]");
      }
    }
    Search search(skip, limit, stop_first);
    search.run();
    const SearchStats& stats = search.stats();
    const bool complete =
        skip == 0 && limit == std::numeric_limits<std::uint64_t>::max() &&
        !stop_first;
    if (complete) {
      require_full_census(stats, search.near_witnesses().size());
    }
    std::cout << "raw_skeletons_seen=" << stats.raw_skeletons << "\n";
    std::cout << "canonical_skeletons=" << stats.canonical_skeletons << "\n";
    std::cout << "skeleton_targets=" << stats.skeleton_targets << "\n";
    std::cout << "support_trials=" << stats.support_trials << "\n";
    std::cout << "extendible_supports=" << stats.extendible_supports << "\n";
    std::cout << "medium_records=" << stats.medium_records << "\n";
    std::cout << "high_records=" << stats.high_records << "\n";
    std::cout << "mod9_survivors=" << stats.mod9_survivors << "\n";
    std::cout << "mod27_survivors=" << stats.mod27_survivors << "\n";
    std::cout << "cubic37_survivors=" << stats.cubic37_survivors << "\n";
    std::cout << "mod27_cubic37_survivors="
              << stats.mod27_cubic37_survivors << "\n";
    std::cout << "exact_replays=" << stats.exact_replays << "\n";
    std::cout << "exact_survivors=" << stats.exact_survivors << "\n";
    for (std::size_t index = 0; index < search.near_witnesses().size();
         ++index) {
      const NearWitness& witness = search.near_witnesses()[index];
      std::string prefix = "mod27_witness_" + std::to_string(index);
      print_ids((prefix + "_a").c_str(), witness.ids_a);
      print_ids((prefix + "_b").c_str(), witness.ids_b);
      std::cout << prefix << "_target=" << witness.target[0] << ","
                << witness.target[1] << "," << witness.target[2] << ","
                << witness.target[3] << "\n";
      std::cout << prefix << "_cubic_j=" << witness.cubic_j << "\n";
      print_exact_table((prefix + "_exact_c0_to_c5").c_str(),
                        witness.exact);
    }
    if (!search.witnesses().empty()) {
      const Witness& witness = search.witnesses().front();
      print_ids("witness_a", witness.ids_a);
      print_ids("witness_b", witness.ids_b);
      std::cout << "witness_target=" << witness.target[0] << ","
                << witness.target[1] << "," << witness.target[2] << ","
                << witness.target[3] << "\n";
    }
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << "\n";
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
