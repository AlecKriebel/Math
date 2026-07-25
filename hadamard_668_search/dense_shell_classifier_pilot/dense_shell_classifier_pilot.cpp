// Bounded, exact end-to-end pilot for the two dense order-three LP(333)
// profile shells.
//
// This is deliberately a streaming classifier, not a microbenchmark.  For
// each selected canonical signed skeleton (and, in h=1, high position), it:
//
//   * restores every medium phase satisfying the exact primitive flag;
//   * imposes one of the 22 exact Eisenstein aggregate targets;
//   * tests the real modulo-9 and following lambda-adic correlation digits;
//   * tests the independent characteristic-two unitary quotient;
//   * canonicalizes complete assignments with exact stabilizers; and
//   * replays every modulo-9 hit directly on all 37 physical positions.
//
// --skip and --limit count canonical decorated skeletons in deterministic
// lexicographic enumeration order.  The default limit is intentionally one.
// Production mode instead fixes the first two legal local-state indices
// before canonicalization, giving 27^2 disjoint, independently resumable
// prefix shards per shell.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int P = 37;
constexpr int CHANNELS = 2;
constexpr int CLASSES = 12;
constexpr int PAIRS = 6;
constexpr int SLOTS = 24;
constexpr int ZERO_ID = 5;

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
  return {
      x.a * y.a - x.b * y.b,
      x.a * y.b + x.b * y.a - x.b * y.b,
  };
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
using Assignment = std::array<std::uint8_t, SLOTS>;
using Physical = std::array<std::array<E, P>, CHANNELS>;

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
    {1, 0},
    {0, 1},
    {-1, -1},
}};
constexpr E LAMBDA = {1, -1};

// The ten exact length-three compression profiles.  The corresponding
// Eisenstein value is p0-p2 + (p1-p2) omega.
constexpr std::array<std::array<int, 3>, 10> PROFILES = {{
    {{0, 0, 3}},
    {{0, 1, 2}},
    {{0, 2, 1}},
    {{0, 3, 0}},
    {{1, 0, 2}},
    {{1, 1, 1}},
    {{1, 2, 0}},
    {{2, 0, 1}},
    {{2, 1, 0}},
    {{3, 0, 0}},
}};

E raw_profile(int id) {
  const auto& p = PROFILES.at(static_cast<std::size_t>(id));
  return {p[0] - p[2], p[1] - p[2]};
}

int conjugate_profile_id(int id) {
  const E wanted = conjugate(raw_profile(id));
  for (int candidate = 0; candidate < 10; ++candidate) {
    if (raw_profile(candidate) == wanted) return candidate;
  }
  throw std::runtime_error("profile alphabet is not conjugation-stable");
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

E coefficient(int slot, int id) {
  const auto [channel, class_index] = decode_slot(slot);
  return scale(actual_factor(channel, class_index), raw_profile(id));
}

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
      const int value = power * subgroup[offset] % P;
      result.classes[index][offset] = value;
      if (result.class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      result.class_of[value] = index;
    }
    power = 2 * power % P;
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
          if (mod(-a0 + a1 + b0 - b1, 3) == 0) {
            result.push_back({a0, a1, b0, b1});
          }
        }
      }
    }
  }
  return result;
}

int medium_count(const Local& local) {
  int result = 0;
  for (int value : local) result += value != 0;
  return result;
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
    const int offset = (2 * rotation + (stars[channel] ? 6 : 0)) % CLASSES;
    const int sign = stars[channel] ? -1 : 1;
    for (int index = 0; index < CLASSES; ++index) {
      result[channel][index] = static_cast<std::int8_t>(
          sign * input[channel][(index + offset) % CLASSES]);
    }
  }
  return result;
}

struct Decoration {
  Skeleton skeleton{};
  int high_slot = -1;
};

Decoration transform_decoration(const Decoration& input, int group) {
  Decoration result;
  result.skeleton = transform_skeleton(input.skeleton, group);
  if (input.high_slot >= 0) {
    const auto [channel, class_index] = decode_slot(input.high_slot);
    const int rotation = group / 4;
    const bool star =
        channel == 0 ? static_cast<bool>((group / 2) % 2)
                     : static_cast<bool>(group % 2);
    const int offset = (2 * rotation + (star ? 6 : 0)) % CLASSES;
    const int output_index = mod(class_index - offset, CLASSES);
    result.high_slot = slot_index(channel, output_index);
  }
  return result;
}

std::array<std::int8_t, SLOTS> decoration_key(const Decoration& decor) {
  std::array<std::int8_t, SLOTS> result{};
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = decor.skeleton[channel][class_index];
    result[slot] = static_cast<std::int8_t>(sign + 1);
  }
  if (decor.high_slot >= 0) {
    if (result[decor.high_slot] != 1) {
      throw std::runtime_error("high position is not a skeleton zero");
    }
    result[decor.high_slot] = 3;
  }
  return result;
}

struct OrbitInfo {
  bool canonical = false;
  int stabilizer = 0;
  int orbit_size = 0;
};

OrbitInfo decoration_orbit_info(const Decoration& decor) {
  const auto raw = decoration_key(decor);
  auto canonical = raw;
  int stabilizer = 0;
  for (int group = 0; group < 24; ++group) {
    const auto image = decoration_key(transform_decoration(decor, group));
    canonical = std::min(canonical, image);
    stabilizer += image == raw;
  }
  if (stabilizer <= 0 || 24 % stabilizer != 0) {
    throw std::runtime_error("invalid decoration stabilizer");
  }
  return {raw == canonical, stabilizer, 24 / stabilizer};
}

E raw_medium(int sign, int phase) {
  return scale(sign, multiply(LAMBDA, OMEGA_POWERS.at(phase)));
}

int medium_id(int sign, int phase) {
  constexpr std::array<int, 3> positive = {7, 6, 1};
  constexpr std::array<int, 3> negative = {2, 4, 8};
  if (sign == 1) return positive.at(phase);
  if (sign == -1) return negative.at(phase);
  throw std::runtime_error("medium sign must be nonzero");
}

int high_id(int phase) {
  constexpr std::array<int, 3> values = {9, 3, 0};
  return values.at(phase);
}

Values values_from_assignment(const Assignment& ids) {
  Values result{};
  result[0][0] = {-1, 0};
  result[1][0] = {2, 0};
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    result[channel][class_index + 1] = coefficient(slot, ids[slot]);
  }
  return result;
}

Assignment assignment_ids(const Decoration& decor,
                          const std::array<std::uint8_t, SLOTS>& phases,
                          int high_phase) {
  Assignment result{};
  result.fill(ZERO_ID);
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = decor.skeleton[channel][class_index];
    if (sign) result[slot] = static_cast<std::uint8_t>(
        medium_id(sign, phases[slot]));
  }
  if (decor.high_slot >= 0) {
    result[decor.high_slot] =
        static_cast<std::uint8_t>(high_id(high_phase));
  }
  return result;
}

Assignment transform_assignment(const Assignment& raw, int group) {
  const int rotation = group / 4;
  const bool stars[2] = {
      static_cast<bool>((group / 2) % 2),
      static_cast<bool>(group % 2),
  };
  Assignment result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    const int offset = (2 * rotation + (stars[channel] ? 6 : 0)) % CLASSES;
    for (int index = 0; index < CLASSES; ++index) {
      int id = raw[slot_index(channel, (index + offset) % CLASSES)];
      if (stars[channel]) id = conjugate_profile_id(id);
      result[slot_index(channel, index)] = static_cast<std::uint8_t>(id);
    }
  }
  return result;
}

struct AssignmentOrbitInfo {
  Assignment canonical{};
  int stabilizer = 0;
  int orbit_size = 0;
};

AssignmentOrbitInfo assignment_orbit_info(const Assignment& raw) {
  Assignment canonical{};
  canonical.fill(10);
  int stabilizer = 0;
  for (int group = 0; group < 24; ++group) {
    const Assignment image = transform_assignment(raw, group);
    canonical = std::min(canonical, image);
    stabilizer += image == raw;
  }
  if (stabilizer <= 0 || 24 % stabilizer != 0) {
    throw std::runtime_error("invalid assignment stabilizer");
  }
  return {canonical, stabilizer, 24 / stabilizer};
}

Values base_values(const Decoration& decor, int high_phase) {
  Assignment ids{};
  ids.fill(ZERO_ID);
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = decor.skeleton[channel][class_index];
    if (sign) ids[slot] = static_cast<std::uint8_t>(medium_id(sign, 0));
  }
  if (decor.high_slot >= 0) {
    ids[decor.high_slot] = static_cast<std::uint8_t>(high_id(high_phase));
  }
  return values_from_assignment(ids);
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
    result[2 * lag] =
        static_cast<std::uint8_t>(mod(exact[lag].a, 9));
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
        total = add(
            total,
            scale(count,
                  multiply(delta, conjugate(base[channel][source]))));
      }
    }
    for (int target = 0; target < 13; ++target) {
      const int count = geometry.transition[lag][part][target];
      if (count) {
        total = add(
            total,
            scale(count,
                  multiply(base[channel][target], conjugate(delta))));
      }
    }
    const int diagonal = geometry.transition[lag][part][part];
    if (diagonal) {
      total = add(
          total,
          scale(diagonal, multiply(delta, conjugate(delta))));
    }
    result[lag] = total;
  }
  return reduced_signature(result);
}

Aggregate aggregate(const Values& values) {
  Aggregate result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    E total{};
    for (int part = 1; part < 13; ++part) {
      total = add(total, values[channel][part]);
    }
    if (total.a < -127 || total.a > 127 ||
        total.b < -127 || total.b > 127) {
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

int exact_target_index(const Aggregate& value) {
  for (int index = 0; index < static_cast<int>(TARGETS.size()); ++index) {
    bool same = true;
    for (int coordinate = 0; coordinate < 4; ++coordinate) {
      same &= static_cast<int>(value[coordinate]) ==
              TARGETS[index][coordinate];
    }
    if (same) return index;
  }
  return -1;
}

int primitive_flag(const Signature& signature, int pair) {
  const int a = signature[2 * pair];
  const int b = signature[2 * pair + 1];
  if (a % 3 || b % 3) {
    throw std::runtime_error(
        "signed skeleton lost divisibility by three");
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
};

Prepared prepare(const Geometry& geometry, const Decoration& decor,
                 int high_phase) {
  Prepared result;
  result.base = base_values(decor, high_phase);
  result.base_signature =
      reduced_signature(exact_correlations(geometry, result.base));
  result.base_aggregate = aggregate(result.base);
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int sign = decor.skeleton[channel][class_index];
    if (!sign) continue;
    const int factor = actual_factor(channel, class_index);
    const E old_value = scale(factor, raw_medium(sign, 0));
    for (int phase = 0; phase < 3; ++phase) {
      const E new_value = scale(factor, raw_medium(sign, phase));
      const E delta = sub(new_value, old_value);
      result.phase_options[slot][phase] = {
          one_slot_delta(
              geometry, result.base, channel, class_index, delta),
          delta,
      };
    }
  }
  return result;
}

struct LocalOption {
  Signature delta_signature{};
  Aggregate delta_aggregate{};
  std::array<std::uint8_t, 4> phases{};
};

using LocalTable = std::vector<LocalOption>;

LocalTable local_options(const Decoration& decor,
                         const Prepared& prepared,
                         int pair) {
  std::array<int, 4> slots = {
      slot_index(0, pair),
      slot_index(0, pair + 6),
      slot_index(1, pair),
      slot_index(1, pair + 6),
  };
  std::vector<int> active;
  for (int local = 0; local < 4; ++local) {
    const auto [channel, class_index] = decode_slot(slots[local]);
    if (decor.skeleton[channel][class_index]) active.push_back(local);
  }
  int combinations = 1;
  for (std::size_t ignored = 0; ignored < active.size(); ++ignored) {
    (void)ignored;
    combinations *= 3;
  }
  LocalTable result;
  for (int code = 0; code < combinations; ++code) {
    int remaining = code;
    LocalOption option;
    for (int local : active) {
      const int phase = remaining % 3;
      remaining /= 3;
      option.phases[local] = static_cast<std::uint8_t>(phase);
      const int slot = slots[local];
      option.delta_signature = add_signature(
          option.delta_signature,
          prepared.phase_options[slot][phase].signature);
      const int channel = decode_slot(slot).first;
      option.delta_aggregate = add_aggregate(
          option.delta_aggregate,
          channel,
          prepared.phase_options[slot][phase].aggregate);
    }
    const Signature flag_signature = add_signature(
        prepared.base_signature, option.delta_signature);
    if (primitive_flag(flag_signature, pair) == 0) {
      result.push_back(option);
    }
  }
  return result;
}

bool signature_zero(const Signature& signature) {
  for (std::uint8_t value : signature) {
    if (value) return false;
  }
  return true;
}

int lambda3_residue(E value) {
  return mod(value.a, 3) +
         3 * mod(value.b, 3) +
         9 * mod(2 * value.a - value.b, 9);
}

bool affine_aggregate_compatible(const Aggregate& value) {
  static const auto target_residues = [] {
    std::array<std::pair<int, int>, TARGETS.size()> result{};
    for (std::size_t index = 0; index < TARGETS.size(); ++index) {
      result[index] = {
          lambda3_residue({TARGETS[index][0], TARGETS[index][1]}),
          lambda3_residue({TARGETS[index][2], TARGETS[index][3]}),
      };
    }
    return result;
  }();
  const std::pair<int, int> residue = {
      lambda3_residue({value[0], value[1]}),
      lambda3_residue({value[2], value[3]}),
  };
  for (const auto& target : target_residues) {
    if (target == residue) return true;
  }
  return false;
}

bool post_mod9_lambda_zero(const std::array<E, PAIRS>& exact) {
  for (E value : exact) {
    if (value.a % 9 || value.b % 9) return false;
    if (mod(value.a / 9 + value.b / 9, 3) != 0) return false;
  }
  return true;
}

bool mod27_zero(const std::array<E, PAIRS>& exact) {
  for (E value : exact) {
    if (value.a % 27 || value.b % 27) return false;
  }
  return true;
}

bool exact_zero(const std::array<E, PAIRS>& exact) {
  for (E value : exact) {
    if (value != E{}) return false;
  }
  return true;
}

Physical expand_physical(const Geometry& geometry, const Values& values) {
  Physical result{};
  for (int channel = 0; channel < CHANNELS; ++channel) {
    result[channel][0] = values[channel][0];
    for (int position = 1; position < P; ++position) {
      result[channel][position] =
          values[channel][geometry.class_of[position] + 1];
    }
  }
  return result;
}

std::array<E, P> direct_physical_correlations(const Physical& physical) {
  std::array<E, P> result{};
  for (int lag = 0; lag < P; ++lag) {
    E total{};
    for (int channel = 0; channel < CHANNELS; ++channel) {
      for (int source = 0; source < P; ++source) {
        total = add(
            total,
            multiply(
                physical[channel][(source + lag) % P],
                conjugate(physical[channel][source])));
      }
    }
    result[lag] = total;
  }
  return result;
}

void detached_replay(const Geometry& geometry, const Values& values,
                     const std::array<E, PAIRS>& compact,
                     const Target& target) {
  const Aggregate exact_aggregate = aggregate(values);
  for (int coordinate = 0; coordinate < 4; ++coordinate) {
    if (exact_aggregate[coordinate] != target[coordinate]) {
      throw std::runtime_error("detached replay lost aggregate target");
    }
  }
  const Physical physical = expand_physical(geometry, values);
  const auto direct = direct_physical_correlations(physical);
  for (int class_index = 0; class_index < CLASSES; ++class_index) {
    const int lag = geometry.classes[class_index][0];
    const E expected =
        class_index < PAIRS
            ? compact[class_index]
            : conjugate(compact[class_index - PAIRS]);
    if (direct[lag] != expected) {
      throw std::runtime_error(
          "detached 37-point replay disagrees with quotient replay");
    }
  }
}

int f4_multiply(int x, int y) {
  const int a = x & 1;
  const int b = (x >> 1) & 1;
  const int c = y & 1;
  const int d = (y >> 1) & 1;
  return (a * c ^ b * d) |
         ((a * d ^ b * c ^ b * d) << 1);
}

int f4_square(int x) { return f4_multiply(x, x); }

int f4_value(E value) {
  return mod(value.a, 2) | (mod(value.b, 2) << 1);
}

// Independent necessary quotient:
// A A* + B B* = e in F_4[C_37]^H.
bool characteristic_two_unitary(const Geometry& geometry,
                                const Values& values) {
  const Physical physical = expand_physical(geometry, values);
  for (int lag_class = 0; lag_class < PAIRS; ++lag_class) {
    const int lag = geometry.classes[lag_class][0];
    int total = 0;
    for (int channel = 0; channel < CHANNELS; ++channel) {
      for (int source = 0; source < P; ++source) {
        total ^= f4_multiply(
            f4_value(physical[channel][(source + lag) % P]),
            f4_square(f4_value(physical[channel][source])));
      }
    }
    if (total != 0) return false;
  }
  return true;
}

std::uint64_t mix64(std::uint64_t value) {
  value ^= value >> 30;
  value *= 0xbf58476d1ce4e5b9ULL;
  value ^= value >> 27;
  value *= 0x94d049bb133111ebULL;
  return value ^ (value >> 31);
}

std::uint64_t assignment_digest(const Assignment& ids,
                                const std::array<E, PAIRS>& exact,
                                int target_index) {
  std::uint64_t digest = 0x66833337ULL;
  for (int slot = 0; slot < SLOTS; ++slot) {
    digest ^= mix64(
        static_cast<std::uint64_t>(ids[slot]) +
        17ULL * static_cast<std::uint64_t>(slot + 1));
  }
  for (int lag = 0; lag < PAIRS; ++lag) {
    const std::uint64_t a =
        static_cast<std::uint64_t>(
            static_cast<std::int64_t>(exact[lag].a));
    const std::uint64_t b =
        static_cast<std::uint64_t>(
            static_cast<std::int64_t>(exact[lag].b));
    digest ^= mix64(a + 257ULL * static_cast<std::uint64_t>(lag + 1));
    digest ^= mix64(b + 65537ULL * static_cast<std::uint64_t>(lag + 1));
  }
  digest ^= mix64(static_cast<std::uint64_t>(target_index + 1));
  return digest;
}

struct Witness {
  bool present = false;
  Assignment ids{};
  int target_index = -1;
  std::array<E, PAIRS> exact{};
  bool canonical = false;
  bool char2 = false;
  bool mod9 = false;
  bool post_lambda = false;
  bool mod27 = false;
  bool zero = false;
};

struct Stats {
  std::uint64_t raw_skeletons_seen = 0;
  std::uint64_t raw_decorations_seen = 0;
  std::uint64_t canonical_decorations_seen = 0;
  std::uint64_t canonical_decorations_processed = 0;
  std::uint64_t weighted_decorations_processed = 0;
  std::uint64_t high_phase_cases = 0;
  std::uint64_t rejected_local_phase_cases = 0;
  std::uint64_t primitive_flag_phase_leaves = 0;
  std::uint64_t weighted_primitive_flag_phase_leaves = 0;
  std::uint64_t affine_aggregate_hits = 0;
  std::uint64_t weighted_affine_aggregate_hits = 0;
  std::uint64_t exact_target_hits = 0;
  std::uint64_t char2_hits = 0;
  std::uint64_t mod9_hits = 0;
  std::uint64_t char2_mod9_hits = 0;
  std::uint64_t post_mod9_lambda_hits = 0;
  std::uint64_t char2_post_mod9_lambda_hits = 0;
  std::uint64_t mod27_hits = 0;
  std::uint64_t exact_zero_hits = 0;
  std::uint64_t diagnostic_assignment_idlex_mod9_hits = 0;
  std::uint64_t diagnostic_weighted_assignment_idlex_mod9_hits = 0;
  std::uint64_t detached_replays = 0;
  std::uint64_t weighted_exact_target_hits = 0;
  std::uint64_t weighted_char2_hits = 0;
  std::uint64_t weighted_mod9_hits = 0;
  std::uint64_t weighted_post_mod9_lambda_hits = 0;
  std::uint64_t weighted_exact_zero_hits = 0;
  std::uint64_t checksum = 0x243f6a8885a308d3ULL;
};

struct Config {
  int medium_total = 15;
  std::uint64_t skip = 0;
  std::uint64_t limit = 1;
  bool count_decorations = false;
  bool complete_shard = false;
  bool enumerate_exact_orbits = false;
  int prefix_first = -1;
  int prefix_second = -1;
};

bool skeleton_fixed_by_group(const Skeleton& skeleton, int group) {
  const int rotation = group / 4;
  const bool stars[2] = {
      static_cast<bool>((group / 2) % 2),
      static_cast<bool>(group % 2),
  };
  for (int channel = 0; channel < CHANNELS; ++channel) {
    const int offset = (2 * rotation + (stars[channel] ? 6 : 0)) % CLASSES;
    const int sign = stars[channel] ? -1 : 1;
    for (int index = 0; index < CLASSES; ++index) {
      if (skeleton[channel][index] !=
          sign * skeleton[channel][(index + offset) % CLASSES]) {
        return false;
      }
    }
  }
  return true;
}

int fixed_zero_positions(const Skeleton& skeleton, int group) {
  const int rotation = group / 4;
  const bool stars[2] = {
      static_cast<bool>((group / 2) % 2),
      static_cast<bool>(group % 2),
  };
  int fixed = 0;
  for (int channel = 0; channel < CHANNELS; ++channel) {
    const int offset = (2 * rotation + (stars[channel] ? 6 : 0)) % CLASSES;
    if (offset != 0) continue;
    for (int index = 0; index < CLASSES; ++index) {
      fixed += skeleton[channel][index] == 0;
    }
  }
  return fixed;
}

struct DecorationCount {
  std::uint64_t raw_skeletons = 0;
  std::uint64_t raw_decorations = 0;
  std::uint64_t canonical_decorations = 0;
  std::array<std::uint64_t, 24> fixed_decorations{};
};

class DecorationCounter {
 public:
  explicit DecorationCounter(int medium_total)
      : medium_total_(medium_total), local_(local_states()) {}

  DecorationCount run() {
    enumerate(0, 0);
    const std::uint64_t expected_skeletons =
        medium_total_ == 15 ? 59'743'488ULL : 47'730'304ULL;
    if (result_.raw_skeletons != expected_skeletons) {
      throw std::runtime_error(
          "complete signed-skeleton count changed");
    }
    result_.raw_decorations =
        result_.fixed_decorations[0];
    const std::uint64_t fixed_sum = [&] {
      std::uint64_t value = 0;
      for (std::uint64_t count : result_.fixed_decorations) {
        if (value > std::numeric_limits<std::uint64_t>::max() - count) {
          throw std::overflow_error("Burnside sum overflow");
        }
        value += count;
      }
      return value;
    }();
    if (fixed_sum % 24 != 0) {
      throw std::runtime_error("Burnside decoration sum is not integral");
    }
    result_.canonical_decorations = fixed_sum / 24;
    const std::uint64_t expected_raw =
        medium_total_ == 15
            ? 537'691'392ULL
            : 47'730'304ULL;
    if (result_.raw_decorations != expected_raw) {
      throw std::runtime_error("raw decorated count changed");
    }
    return result_;
  }

 private:
  void enumerate(int pair, int used) {
    if (pair == PAIRS) {
      if (used == medium_total_) record();
      return;
    }
    const int remaining = PAIRS - pair - 1;
    for (const Local& state : local_) {
      const int count = medium_count(state);
      const int next = used + count;
      if (next > medium_total_ ||
          next + 4 * remaining < medium_total_) {
        continue;
      }
      selected_[pair] = state;
      enumerate(pair + 1, next);
    }
  }

  void record() {
    ++result_.raw_skeletons;
    const Skeleton skeleton = selected_to_skeleton(selected_);
    for (int group = 0; group < 24; ++group) {
      if (!skeleton_fixed_by_group(skeleton, group)) continue;
      if (medium_total_ == 15) {
        result_.fixed_decorations[group] +=
            fixed_zero_positions(skeleton, group);
      } else {
        ++result_.fixed_decorations[group];
      }
    }
  }

  int medium_total_;
  std::vector<Local> local_;
  std::array<Local, PAIRS> selected_{};
  DecorationCount result_;
};

class Search {
 public:
  explicit Search(Config config)
      : config_(config),
        geometry_(build_geometry()),
        local_(local_states()) {}

  void run() {
    if (config_.prefix_first >= 0) {
      selected_[0] = local_.at(
          static_cast<std::size_t>(config_.prefix_first));
      selected_[1] = local_.at(
          static_cast<std::size_t>(config_.prefix_second));
      const int used =
          medium_count(selected_[0]) + medium_count(selected_[1]);
      if (used <= config_.medium_total &&
          used + 4 * (PAIRS - 2) >= config_.medium_total) {
        enumerate_skeleton(2, used);
      }
    } else {
      enumerate_skeleton(0, 0);
    }
  }

  const Stats& stats() const { return stats_; }
  const std::array<Witness, 6>& witnesses() const { return witnesses_; }
  using ExactOrbitKey = std::pair<Assignment, int>;
  const std::map<ExactOrbitKey, Witness>& exact_orbits() const {
    return exact_orbits_;
  }
  bool candidate_found() const { return candidate_found_; }

 private:
  void enumerate_skeleton(int pair, int used) {
    if (stopped_) return;
    if (pair == PAIRS) {
      if (used == config_.medium_total) process_skeleton();
      return;
    }
    const int remaining = PAIRS - pair - 1;
    for (const Local& state : local_) {
      const int count = medium_count(state);
      const int next = used + count;
      if (next > config_.medium_total ||
          next + 4 * remaining < config_.medium_total) {
        continue;
      }
      selected_[pair] = state;
      enumerate_skeleton(pair + 1, next);
      if (stopped_) return;
    }
  }

  void process_skeleton() {
    ++stats_.raw_skeletons_seen;
    const Skeleton skeleton = selected_to_skeleton(selected_);
    if (config_.medium_total == 18) {
      process_decoration({skeleton, -1});
      return;
    }
    for (int slot = 0; slot < SLOTS; ++slot) {
      const auto [channel, class_index] = decode_slot(slot);
      if (skeleton[channel][class_index]) continue;
      process_decoration({skeleton, slot});
      if (stopped_) return;
    }
  }

  void process_decoration(const Decoration& decor) {
    ++stats_.raw_decorations_seen;
    const OrbitInfo orbit = decoration_orbit_info(decor);
    if (!orbit.canonical) return;
    ++stats_.canonical_decorations_seen;
    if (!config_.complete_shard &&
        stats_.canonical_decorations_seen <= config_.skip) {
      return;
    }
    if (stats_.canonical_decorations_processed >= config_.limit) {
      stopped_ = true;
      return;
    }
    ++stats_.canonical_decorations_processed;
    stats_.weighted_decorations_processed += orbit.orbit_size;
    const int high_phases = decor.high_slot < 0 ? 1 : 3;
    for (int high_phase = 0; high_phase < high_phases; ++high_phase) {
      ++stats_.high_phase_cases;
      process_high_phase(decor, orbit, high_phase);
      if (stopped_) return;
    }
  }

  void process_high_phase(const Decoration& decor,
                          const OrbitInfo& decor_orbit,
                          int high_phase) {
    const Prepared prepared =
        prepare(geometry_, decor, high_phase);
    std::array<LocalTable, PAIRS> tables;
    for (int pair = 0; pair < PAIRS; ++pair) {
      tables[pair] = local_options(decor, prepared, pair);
      if (tables[pair].empty()) {
        ++stats_.rejected_local_phase_cases;
        return;
      }
    }
    std::array<std::uint8_t, SLOTS> phases{};
    recurse_phases(
        decor, decor_orbit, high_phase, prepared, tables, 0,
        prepared.base_signature, prepared.base_aggregate, phases);
  }

  void recurse_phases(
      const Decoration& decor,
      const OrbitInfo& decor_orbit,
      int high_phase,
      const Prepared& prepared,
      const std::array<LocalTable, PAIRS>& tables,
      int pair,
      Signature signature,
      Aggregate aggregate_value,
      std::array<std::uint8_t, SLOTS>& phases) {
    (void)prepared;
    if (pair == PAIRS) {
      process_phase_leaf(
          decor, decor_orbit, high_phase, signature,
          aggregate_value, phases);
      return;
    }
    const std::array<int, 4> slots = {
        slot_index(0, pair),
        slot_index(0, pair + 6),
        slot_index(1, pair),
        slot_index(1, pair + 6),
    };
    for (const LocalOption& option : tables[pair]) {
      for (int local = 0; local < 4; ++local) {
        const auto [channel, class_index] = decode_slot(slots[local]);
        if (decor.skeleton[channel][class_index]) {
          phases[slots[local]] = option.phases[local];
        }
      }
      Signature next_signature =
          add_signature(signature, option.delta_signature);
      Aggregate next_aggregate = aggregate_value;
      for (int channel = 0; channel < CHANNELS; ++channel) {
        next_aggregate = add_aggregate(
            next_aggregate, channel,
            {option.delta_aggregate[2 * channel],
             option.delta_aggregate[2 * channel + 1]});
      }
      recurse_phases(
          decor, decor_orbit, high_phase, prepared, tables, pair + 1,
          next_signature, next_aggregate, phases);
      if (stopped_) return;
    }
  }

  void save_witness(int index, const Assignment& ids, int target_index,
                    const std::array<E, PAIRS>& exact, bool char2,
                    bool mod9, bool post_lambda, bool mod27, bool zero,
                    bool canonical = false) {
    if (witnesses_[index].present) return;
    witnesses_[index] = {
        true, ids, target_index, exact, canonical, char2,
        mod9, post_lambda, mod27, zero,
    };
  }

  void process_phase_leaf(
      const Decoration& decor,
      const OrbitInfo& decor_orbit,
      int high_phase,
      const Signature& signature,
      const Aggregate& aggregate_value,
      const std::array<std::uint8_t, SLOTS>& phases) {
    ++stats_.primitive_flag_phase_leaves;
    stats_.weighted_primitive_flag_phase_leaves +=
        decor_orbit.orbit_size;
    const bool affine_aggregate =
        affine_aggregate_compatible(aggregate_value);
    stats_.affine_aggregate_hits += affine_aggregate;
    stats_.weighted_affine_aggregate_hits +=
        affine_aggregate ? decor_orbit.orbit_size : 0;
    const int target_index = exact_target_index(aggregate_value);
    if (target_index < 0) return;
    ++stats_.exact_target_hits;
    stats_.weighted_exact_target_hits += decor_orbit.orbit_size;

    const Assignment ids =
        assignment_ids(decor, phases, high_phase);
    const Values values = values_from_assignment(ids);
    if (aggregate(values) != aggregate_value) {
      throw std::runtime_error("incremental aggregate drift");
    }
    const bool char2 = characteristic_two_unitary(geometry_, values);
    stats_.char2_hits += char2;
    stats_.weighted_char2_hits +=
        char2 ? decor_orbit.orbit_size : 0;

    const bool mod9 = signature_zero(signature);
    stats_.mod9_hits += mod9;
    stats_.char2_mod9_hits += char2 && mod9;
    stats_.weighted_mod9_hits +=
        mod9 ? decor_orbit.orbit_size : 0;

    std::array<E, PAIRS> exact{};
    bool post_lambda = false;
    bool zero_mod27 = false;
    bool zero = false;
    const bool run_upper_exact =
        mod9 && (!config_.complete_shard || char2);
    if (run_upper_exact) {
      exact = exact_correlations(geometry_, values);
      if (reduced_signature(exact) != signature) {
        throw std::runtime_error("incremental modulo-9 signature drift");
      }
      detached_replay(
          geometry_, values, exact, TARGETS[target_index]);
      ++stats_.detached_replays;
      post_lambda = post_mod9_lambda_zero(exact);
      zero_mod27 = mod27_zero(exact);
      zero = exact_zero(exact);
      stats_.post_mod9_lambda_hits += post_lambda;
      stats_.char2_post_mod9_lambda_hits += char2 && post_lambda;
      stats_.mod27_hits += zero_mod27;
      stats_.exact_zero_hits += zero;
      stats_.weighted_post_mod9_lambda_hits +=
          post_lambda ? decor_orbit.orbit_size : 0;
      stats_.weighted_exact_zero_hits +=
          zero ? decor_orbit.orbit_size : 0;

      if (zero && !char2) {
        throw std::runtime_error(
            "exact zero failed characteristic-two quotient");
      }
    }

    Assignment canonical_ids = ids;
    if (mod9) {
      const AssignmentOrbitInfo assignment_orbit =
          assignment_orbit_info(ids);
      canonical_ids = assignment_orbit.canonical;
      if (ids == assignment_orbit.canonical) {
        ++stats_.diagnostic_assignment_idlex_mod9_hits;
        stats_.diagnostic_weighted_assignment_idlex_mod9_hits +=
            assignment_orbit.orbit_size;
      }
    }

    std::array<E, PAIRS> recovered_exact = exact;
    // This fallback exists only to materialize the first bounded-pilot
    // target/char2 witnesses.  Production never emits those two marginal
    // witnesses.  Its mathematically sufficient exact-replay trigger is
    // run_upper_exact above: exact zero necessarily implies both mod9 and
    // the characteristic-two unitary quotient.
    const bool needs_recovered_exact =
        !config_.complete_shard && !mod9 &&
        (!witnesses_[0].present ||
         (char2 && !witnesses_[1].present));
    if (needs_recovered_exact) {
      recovered_exact = exact_correlations(geometry_, values);
      if (reduced_signature(recovered_exact) != signature) {
        throw std::runtime_error(
            "recovered witness modulo-9 signature drift");
      }
      detached_replay(
          geometry_, values, recovered_exact, TARGETS[target_index]);
      ++stats_.detached_replays;
    }

    const auto& digest_exact =
        (mod9 || needs_recovered_exact) ? recovered_exact : exact;
    const std::uint64_t digest =
        assignment_digest(ids, digest_exact, target_index);
    stats_.checksum ^= mix64(
        digest + stats_.exact_target_hits * 0x9e3779b97f4a7c15ULL);

    if (!config_.complete_shard) {
      save_witness(
          0, ids, target_index, recovered_exact, char2, mod9,
          post_lambda, zero_mod27, zero);
      if (char2) {
        save_witness(
            1, ids, target_index, recovered_exact, char2, mod9,
            post_lambda, zero_mod27, zero);
      }
      if (mod9) {
        save_witness(
            2, ids, target_index, exact, char2, mod9,
            post_lambda, zero_mod27, zero);
      }
    }
    if (char2 && mod9) {
      save_witness(
          3, ids, target_index, exact, char2, mod9,
          post_lambda, zero_mod27, zero);
    }
    if (post_lambda) {
      save_witness(
          4, ids, target_index, exact, char2, mod9,
          post_lambda, zero_mod27, zero);
    }
    if (zero) {
      auto canonical_witness = [&]() {
        const Values canonical_values =
            values_from_assignment(canonical_ids);
        const auto canonical_exact =
            exact_correlations(geometry_, canonical_values);
        const int canonical_target =
            exact_target_index(aggregate(canonical_values));
        const bool canonical_char2 =
            characteristic_two_unitary(geometry_, canonical_values);
        if (!exact_zero(canonical_exact) ||
            canonical_target < 0 || !canonical_char2) {
          throw std::runtime_error(
              "canonical exact-zero orbit representative failed replay");
        }
        detached_replay(
            geometry_, canonical_values, canonical_exact,
            TARGETS[canonical_target]);
        ++stats_.detached_replays;
        return Witness{
            true, canonical_ids, canonical_target, canonical_exact,
            true, true, true, true, true, true,
        };
      };

      if (config_.enumerate_exact_orbits) {
        const Witness candidate = canonical_witness();
        const ExactOrbitKey key{
            candidate.ids, candidate.target_index,
        };
        const auto [stored, inserted] =
            exact_orbits_.try_emplace(key, candidate);
        if (!inserted &&
            assignment_digest(
                stored->second.ids, stored->second.exact,
                stored->second.target_index) !=
                assignment_digest(
                    candidate.ids, candidate.exact,
                    candidate.target_index)) {
          throw std::runtime_error(
              "canonical exact-orbit deduplication collision");
        }
        save_witness(
            5, candidate.ids, candidate.target_index, candidate.exact,
            true, true, true, true, true, true);
        return;
      }

      Assignment candidate_ids = ids;
      std::array<E, PAIRS> candidate_exact = exact;
      int candidate_target = target_index;
      bool candidate_canonical = false;
      try {
        const Witness candidate = canonical_witness();
        candidate_ids = candidate.ids;
        candidate_exact = candidate.exact;
        candidate_target = candidate.target_index;
        candidate_canonical = true;
      } catch (const std::exception&) {
        // The already detached-replayed raw exact witness remains valid.
        // Preserve it rather than allowing a canonicalization defect to
        // erase a stop-on-first discovery.
      }
      save_witness(5, candidate_ids, candidate_target, candidate_exact,
                   true, true, true, true, true, candidate_canonical);
      candidate_found_ = true;
      stopped_ = true;
    }
  }

  Config config_;
  Geometry geometry_;
  std::vector<Local> local_;
  std::array<Local, PAIRS> selected_{};
  bool stopped_ = false;
  bool candidate_found_ = false;
  Stats stats_;
  std::array<Witness, 6> witnesses_{};
  std::map<ExactOrbitKey, Witness> exact_orbits_;
};

void print_assignment(const char* prefix, const Witness& witness) {
  std::cout << prefix << "_present=" << witness.present << '\n';
  if (!witness.present) return;
  std::cout << prefix << "_target_index=" << witness.target_index << '\n';
  std::cout << prefix << "_target=";
  for (int coordinate = 0; coordinate < 4; ++coordinate) {
    if (coordinate) std::cout << ",";
    std::cout << TARGETS[witness.target_index][coordinate];
  }
  std::cout << '\n';
  std::cout << prefix << "_ids_a=";
  for (int index = 0; index < CLASSES; ++index) {
    if (index) std::cout << ",";
    std::cout << static_cast<int>(witness.ids[index]);
  }
  std::cout << '\n';
  std::cout << prefix << "_ids_b=";
  for (int index = 0; index < CLASSES; ++index) {
    if (index) std::cout << ",";
    std::cout << static_cast<int>(witness.ids[CLASSES + index]);
  }
  std::cout << '\n';
  std::cout << prefix << "_exact=";
  for (int lag = 0; lag < PAIRS; ++lag) {
    if (lag) std::cout << ";";
    std::cout << witness.exact[lag].a << "," << witness.exact[lag].b;
  }
  std::cout << '\n';
  std::cout << prefix << "_canonical=" << witness.canonical << '\n';
  std::cout << prefix << "_char2=" << witness.char2 << '\n';
  std::cout << prefix << "_mod9=" << witness.mod9 << '\n';
  std::cout << prefix << "_post_mod9_lambda="
            << witness.post_lambda << '\n';
  std::cout << prefix << "_mod27=" << witness.mod27 << '\n';
  std::cout << prefix << "_exact_zero=" << witness.zero << '\n';
  std::cout << prefix << "_digest=0x" << std::hex
            << assignment_digest(
                   witness.ids, witness.exact, witness.target_index)
            << std::dec << '\n';
}

std::uint64_t parse_u64(const std::string& text, const char* label) {
  std::size_t used = 0;
  const unsigned long long value = std::stoull(text, &used);
  if (used != text.size()) {
    throw std::runtime_error(std::string("invalid ") + label);
  }
  return static_cast<std::uint64_t>(value);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    Config config;
    bool skip_requested = false;
    bool limit_requested = false;
    bool prefix_requested = false;
    for (int index = 1; index < argc; ++index) {
      const std::string option = argv[index];
      if (option == "--shell" && index + 1 < argc) {
        const std::string shell = argv[++index];
        if (shell == "h1") {
          config.medium_total = 15;
        } else if (shell == "h0") {
          config.medium_total = 18;
        } else {
          throw std::runtime_error("--shell must be h1 or h0");
        }
      } else if (option == "--skip" && index + 1 < argc) {
        skip_requested = true;
        config.skip = parse_u64(argv[++index], "skip");
      } else if (option == "--limit" && index + 1 < argc) {
        limit_requested = true;
        config.limit = parse_u64(argv[++index], "limit");
      } else if (option == "--prefix" && index + 2 < argc) {
        prefix_requested = true;
        const std::uint64_t first =
            parse_u64(argv[++index], "prefix first");
        const std::uint64_t second =
            parse_u64(argv[++index], "prefix second");
        if (first >= 27 || second >= 27) {
          throw std::runtime_error(
              "--prefix indices must both lie in [0,26]");
        }
        config.prefix_first = static_cast<int>(first);
        config.prefix_second = static_cast<int>(second);
      } else if (option == "--complete-shard") {
        config.complete_shard = true;
      } else if (option == "--enumerate-exact-orbits") {
        config.enumerate_exact_orbits = true;
      } else if (option == "--count-decorations") {
        config.count_decorations = true;
      } else {
        throw std::runtime_error("unknown or incomplete option: " + option);
      }
    }
    if (config.complete_shard) {
      if (!prefix_requested) {
        throw std::runtime_error(
            "--complete-shard requires --prefix FIRST SECOND");
      }
      if (skip_requested || limit_requested ||
          config.count_decorations) {
        throw std::runtime_error(
            "--complete-shard cannot be combined with --skip, --limit, "
            "or --count-decorations");
      }
      config.skip = 0;
      config.limit = std::numeric_limits<std::uint64_t>::max();
    }
    if (config.count_decorations &&
        (prefix_requested || skip_requested || limit_requested)) {
      throw std::runtime_error(
          "--count-decorations is a global census and cannot be "
          "combined with prefix/bounded-search options");
    }
    if (config.count_decorations && config.enumerate_exact_orbits) {
      throw std::runtime_error(
          "--enumerate-exact-orbits cannot be combined with "
          "--count-decorations");
    }
    if (!config.count_decorations && config.limit == 0) {
      throw std::runtime_error("--limit must be positive");
    }

    const auto start = std::chrono::steady_clock::now();
    if (config.count_decorations) {
      const DecorationCount count =
          DecorationCounter(config.medium_total).run();
      const double seconds = std::chrono::duration<double>(
          std::chrono::steady_clock::now() - start).count();
      std::cout << "schema=dense-shell-decoration-burnside-v1\n";
      std::cout << "shell="
                << (config.medium_total == 15 ? "h1" : "h0") << '\n';
      std::cout << "raw_skeletons=" << count.raw_skeletons << '\n';
      std::cout << "raw_decorations=" << count.raw_decorations << '\n';
      std::cout << "canonical_decorations="
                << count.canonical_decorations << '\n';
      std::cout << "fixed_decorations=";
      for (int group = 0; group < 24; ++group) {
        if (group) std::cout << ",";
        std::cout << count.fixed_decorations[group];
      }
      std::cout << '\n';
      std::cout << std::fixed << std::setprecision(6);
      std::cout << "wall_seconds=" << seconds << '\n';
      std::cout << "PASS: exact Burnside decoration census\n";
      return 0;
    }

    Search search(config);
    search.run();
    const double seconds = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - start).count();
    const Stats& stats = search.stats();

    const std::string shell =
        config.medium_total == 15 ? "h1" : "h0";
    if (config.complete_shard) {
      const auto local = local_states();
      std::cout << "schema=dense-shell-production-shard-v2\n";
      std::cout << "mode=complete_shard\n";
      std::cout << "shell=" << shell << '\n';
      std::cout << "shard_id=" << shell << "-p"
                << std::setw(2) << std::setfill('0')
                << config.prefix_first << "-p"
                << std::setw(2) << config.prefix_second
                << std::setfill(' ') << '\n';
      std::cout << "prefix_first=" << config.prefix_first << '\n';
      std::cout << "prefix_second=" << config.prefix_second << '\n';
      std::cout << "prefix_first_weight="
                << medium_count(local.at(
                       static_cast<std::size_t>(
                           config.prefix_first)))
                << '\n';
      std::cout << "prefix_second_weight="
                << medium_count(local.at(
                       static_cast<std::size_t>(
                           config.prefix_second)))
                << '\n';
      std::cout
          << "upper_exact_scope=char2_mod9_intersection\n";
    } else {
      std::cout << "schema=dense-shell-classifier-pilot-v1\n";
      std::cout << "shell=" << shell << '\n';
    }
    std::cout << "skip=" << config.skip << '\n';
    std::cout << "limit=" << config.limit << '\n';
    std::cout << "raw_skeletons_seen="
              << stats.raw_skeletons_seen << '\n';
    std::cout << "raw_decorations_seen="
              << stats.raw_decorations_seen << '\n';
    std::cout << "canonical_decorations_seen="
              << stats.canonical_decorations_seen << '\n';
    std::cout << "canonical_decorations_processed="
              << stats.canonical_decorations_processed << '\n';
    std::cout << "weighted_decorations_processed="
              << stats.weighted_decorations_processed << '\n';
    std::cout << "high_phase_cases=" << stats.high_phase_cases << '\n';
    std::cout << "rejected_local_phase_cases="
              << stats.rejected_local_phase_cases << '\n';
    std::cout << "primitive_flag_phase_leaves="
              << stats.primitive_flag_phase_leaves << '\n';
    std::cout << "weighted_primitive_flag_phase_leaves="
              << stats.weighted_primitive_flag_phase_leaves << '\n';
    std::cout << "affine_aggregate_hits="
              << stats.affine_aggregate_hits << '\n';
    std::cout << "weighted_affine_aggregate_hits="
              << stats.weighted_affine_aggregate_hits << '\n';
    std::cout << "exact_target_hits=" << stats.exact_target_hits << '\n';
    std::cout << "char2_hits=" << stats.char2_hits << '\n';
    std::cout << "mod9_hits=" << stats.mod9_hits << '\n';
    std::cout << "char2_mod9_hits=" << stats.char2_mod9_hits << '\n';
    std::cout << "post_mod9_lambda_hits="
              << stats.post_mod9_lambda_hits << '\n';
    std::cout << "char2_post_mod9_lambda_hits="
              << stats.char2_post_mod9_lambda_hits << '\n';
    std::cout << "mod27_hits=" << stats.mod27_hits << '\n';
    std::cout << "exact_zero_hits=" << stats.exact_zero_hits << '\n';
    std::cout << "diagnostic_assignment_idlex_mod9_hits="
              << stats.diagnostic_assignment_idlex_mod9_hits << '\n';
    std::cout << "diagnostic_weighted_assignment_idlex_mod9_hits="
              << stats.diagnostic_weighted_assignment_idlex_mod9_hits
              << '\n';
    std::cout << "detached_replays=" << stats.detached_replays << '\n';
    std::cout << "weighted_exact_target_hits="
              << stats.weighted_exact_target_hits << '\n';
    std::cout << "weighted_char2_hits="
              << stats.weighted_char2_hits << '\n';
    std::cout << "weighted_mod9_hits="
              << stats.weighted_mod9_hits << '\n';
    std::cout << "weighted_post_mod9_lambda_hits="
              << stats.weighted_post_mod9_lambda_hits << '\n';
    std::cout << "weighted_exact_zero_hits="
              << stats.weighted_exact_zero_hits << '\n';
    std::cout << "checksum=0x" << std::hex << stats.checksum
              << std::dec << '\n';
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "wall_seconds=" << seconds << '\n';
    if (seconds > 0.0) {
      std::cout << "phase_leaves_per_second="
                << static_cast<double>(
                       stats.primitive_flag_phase_leaves) / seconds
                << '\n';
      std::cout << "raw_equivalent_phase_leaves_per_second="
                << static_cast<double>(
                       stats.weighted_primitive_flag_phase_leaves) / seconds
                << '\n';
      std::cout << "raw_equivalent_affine_points_per_second="
                << static_cast<double>(
                       stats.weighted_affine_aggregate_hits) / seconds
                << '\n';
      std::cout << "raw_equivalent_exact_target_hits_per_second="
                << static_cast<double>(
                       stats.weighted_exact_target_hits) / seconds
                << '\n';
    }

    constexpr std::array<const char*, 6> names = {
        "witness_target",
        "witness_char2",
        "witness_mod9",
        "witness_char2_mod9",
        "witness_post_mod9_lambda",
        "witness_exact",
    };
    for (int index = 0; index < 5; ++index) {
      print_assignment(names[index], search.witnesses()[index]);
    }
    if (config.enumerate_exact_orbits &&
        !search.exact_orbits().empty()) {
      print_assignment(
          names[5], search.exact_orbits().begin()->second);
    } else {
      print_assignment(names[5], search.witnesses()[5]);
    }
    std::cout << "exact_orbit_mode="
              << (config.enumerate_exact_orbits
                      ? "enumerate"
                      : "stop_on_first")
              << '\n';
    std::cout << "exact_orbit_collection="
              << (config.enumerate_exact_orbits
                      ? (config.complete_shard
                             ? "complete_shard"
                             : "bounded_stream")
                      : "disabled")
              << '\n';
    std::cout << "exact_orbit_count="
              << search.exact_orbits().size() << '\n';
    std::size_t exact_orbit_index = 0;
    for (const auto& [key, witness] : search.exact_orbits()) {
      (void)key;
      std::ostringstream name;
      name << "exact_orbit_" << std::setw(6) << std::setfill('0')
           << exact_orbit_index++;
      const std::string prefix = name.str();
      print_assignment(prefix.c_str(), witness);
    }
    if (config.complete_shard) {
      if (search.candidate_found()) {
        std::cout << "shard_complete=0\n";
        std::cout
            << "CANDIDATE: canonical exact-zero witness; shard stopped\n";
        return 2;
      }
      std::cout << "shard_complete=1\n";
      std::cout << "PASS: complete production prefix shard\n";
      return 0;
    }
    std::cout
        << "PASS: bounded exact dense-shell stream and detached replay\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
