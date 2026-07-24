// Exact sparse-shell audit for the LP(333) order-three profile zero gate.
//
// This first implementation is intentionally dependency-free.  It reconstructs
// the ten Eisenstein profile values, the six opposite-class quartet conditions,
// the F_37 cyclotomic transition matrices, and the six reversal-independent
// exact correlations.  The h=6 shell is reduced modulo 9 quartet by quartet.
// In the h=5 shell all three norm-3 letters lie in one quartet; after that
// choice, every remaining norm-9 letter contributes linearly modulo 9 because
// products of two norm-9 letters are divisible by 9.

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int P = 37;
constexpr int CLASS_COUNT = 12;
constexpr int PAIR_COUNT = 6;
constexpr int PROFILE_COUNT = 10;
constexpr int TARGET_COUNT = 22;

struct E {
  int a = 0;
  int b = 0;

  friend bool operator==(const E&, const E&) = default;
};

E add(E x, E y) { return {x.a + y.a, x.b + y.b}; }
E scale(int n, E x) { return {n * x.a, n * x.b}; }
E conjugate(E x) { return {x.a - x.b, -x.b}; }
E multiply(E x, E y) {
  return {x.a * y.a - x.b * y.b,
          x.a * y.b + x.b * y.a - x.b * y.b};
}
int norm(E x) { return x.a * x.a - x.a * x.b + x.b * x.b; }
int mod9(int x) {
  x %= 9;
  return x < 0 ? x + 9 : x;
}

std::uint32_t rotate_right(std::uint32_t value, unsigned amount) {
  return (value >> amount) | (value << (32U - amount));
}

std::string sha256(const std::vector<std::uint8_t>& input) {
  static constexpr std::array<std::uint32_t, 64> constants = {{
      0x428a2f98U, 0x71374491U, 0xb5c0fbcfU, 0xe9b5dba5U,
      0x3956c25bU, 0x59f111f1U, 0x923f82a4U, 0xab1c5ed5U,
      0xd807aa98U, 0x12835b01U, 0x243185beU, 0x550c7dc3U,
      0x72be5d74U, 0x80deb1feU, 0x9bdc06a7U, 0xc19bf174U,
      0xe49b69c1U, 0xefbe4786U, 0x0fc19dc6U, 0x240ca1ccU,
      0x2de92c6fU, 0x4a7484aaU, 0x5cb0a9dcU, 0x76f988daU,
      0x983e5152U, 0xa831c66dU, 0xb00327c8U, 0xbf597fc7U,
      0xc6e00bf3U, 0xd5a79147U, 0x06ca6351U, 0x14292967U,
      0x27b70a85U, 0x2e1b2138U, 0x4d2c6dfcU, 0x53380d13U,
      0x650a7354U, 0x766a0abbU, 0x81c2c92eU, 0x92722c85U,
      0xa2bfe8a1U, 0xa81a664bU, 0xc24b8b70U, 0xc76c51a3U,
      0xd192e819U, 0xd6990624U, 0xf40e3585U, 0x106aa070U,
      0x19a4c116U, 0x1e376c08U, 0x2748774cU, 0x34b0bcb5U,
      0x391c0cb3U, 0x4ed8aa4aU, 0x5b9cca4fU, 0x682e6ff3U,
      0x748f82eeU, 0x78a5636fU, 0x84c87814U, 0x8cc70208U,
      0x90befffaU, 0xa4506cebU, 0xbef9a3f7U, 0xc67178f2U,
  }};
  std::vector<std::uint8_t> message = input;
  const std::uint64_t bit_length =
      static_cast<std::uint64_t>(message.size()) * 8U;
  message.push_back(0x80U);
  while (message.size() % 64 != 56) message.push_back(0);
  for (int shift = 56; shift >= 0; shift -= 8) {
    message.push_back(static_cast<std::uint8_t>(bit_length >> shift));
  }

  std::array<std::uint32_t, 8> state = {{
      0x6a09e667U, 0xbb67ae85U, 0x3c6ef372U, 0xa54ff53aU,
      0x510e527fU, 0x9b05688cU, 0x1f83d9abU, 0x5be0cd19U,
  }};
  for (std::size_t offset = 0; offset < message.size(); offset += 64) {
    std::array<std::uint32_t, 64> words{};
    for (int index = 0; index < 16; ++index) {
      const std::size_t base = offset + static_cast<std::size_t>(4 * index);
      words[index] = (static_cast<std::uint32_t>(message[base]) << 24U) |
                     (static_cast<std::uint32_t>(message[base + 1]) << 16U) |
                     (static_cast<std::uint32_t>(message[base + 2]) << 8U) |
                     static_cast<std::uint32_t>(message[base + 3]);
    }
    for (int index = 16; index < 64; ++index) {
      const std::uint32_t x = words[index - 15];
      const std::uint32_t y = words[index - 2];
      const std::uint32_t s0 =
          rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3U);
      const std::uint32_t s1 =
          rotate_right(y, 17) ^ rotate_right(y, 19) ^ (y >> 10U);
      words[index] =
          words[index - 16] + s0 + words[index - 7] + s1;
    }

    std::uint32_t a = state[0];
    std::uint32_t b = state[1];
    std::uint32_t c = state[2];
    std::uint32_t d = state[3];
    std::uint32_t e = state[4];
    std::uint32_t f = state[5];
    std::uint32_t g = state[6];
    std::uint32_t h = state[7];
    for (int index = 0; index < 64; ++index) {
      const std::uint32_t sum1 =
          rotate_right(e, 6) ^ rotate_right(e, 11) ^ rotate_right(e, 25);
      const std::uint32_t choose = (e & f) ^ ((~e) & g);
      const std::uint32_t temporary1 =
          h + sum1 + choose + constants[index] + words[index];
      const std::uint32_t sum0 =
          rotate_right(a, 2) ^ rotate_right(a, 13) ^ rotate_right(a, 22);
      const std::uint32_t majority = (a & b) ^ (a & c) ^ (b & c);
      const std::uint32_t temporary2 = sum0 + majority;
      h = g;
      g = f;
      f = e;
      e = d + temporary1;
      d = c;
      c = b;
      b = a;
      a = temporary1 + temporary2;
    }
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;
    state[5] += f;
    state[6] += g;
    state[7] += h;
  }

  std::ostringstream output;
  output << std::hex << std::setfill('0');
  for (std::uint32_t value : state) output << std::setw(8) << value;
  return output.str();
}

using Target = std::array<int, 4>;
using Signature = std::array<int, 12>;
using IdWord = std::array<int, CLASS_COUNT>;

constexpr std::array<E, PROFILE_COUNT> PROFILE_VALUES = {{
    {-3, -3}, {-2, -1}, {-1, 1}, {0, 3}, {-1, -2},
    {0, 0},   {1, 2},   {1, -1}, {2, 1}, {3, 0},
}};

constexpr std::array<Target, TARGET_COUNT> TARGETS = {{
    {-3, -3, -4, -2}, {-3, -3, -2, 2}, {-3, 0, -3, -3},
    {-3, 0, 0, 3},    {-1, -2, -5, -1}, {-1, -2, -4, 1},
    {0, 3, -4, -2},   {0, 3, -2, 2},    {1, -1, 2, -2},
    {1, -1, 4, 2},    {1, 2, -5, -1},   {1, 2, -4, 1},
    {2, -2, -4, -2},  {2, -2, -2, 2},   {2, 1, 2, -2},
    {2, 1, 4, 2},     {3, 0, 0, -3},    {3, 0, 3, 3},
    {4, -1, 0, 0},    {4, 2, -4, -2},   {4, 2, -2, 2},
    {5, 1, 0, 0},
}};

constexpr std::string_view EXPECTED_H6_REPLAY_SHA256 =
    "981f1a39c7858271e9588b7606dece1c6d408b31506381c71eecc9dbc85d410e";
constexpr std::string_view EXPECTED_H5_REPLAY_SHA256 =
    "e917360e36cbf57b96e5f0a8d842017eaeab9a73c4cdff804bdad719d898090e";

int profile_norm(int id) { return norm(PROFILE_VALUES.at(id)); }

void audit_profile_alphabet_and_targets() {
  std::array<int, 10> norm_histogram{};
  for (E value : PROFILE_VALUES) {
    if (norm(value) < 0 || norm(value) >= static_cast<int>(norm_histogram.size())) {
      throw std::runtime_error("profile norm left the expected alphabet");
    }
    ++norm_histogram[norm(value)];
  }
  if (norm_histogram[0] != 1 || norm_histogram[3] != 6 ||
      norm_histogram[9] != 3) {
    throw std::runtime_error("profile alphabet type census changed");
  }
  for (int id = 0; id < PROFILE_COUNT; ++id) {
    if (profile_norm(id) == 9 &&
        (PROFILE_VALUES[id].a % 3 || PROFILE_VALUES[id].b % 3)) {
      throw std::runtime_error("a norm-9 letter is not divisible by 3");
    }
  }
  for (const Target& target : TARGETS) {
    const E full_a = {-1 + 3 * target[0], 3 * target[1]};
    const E full_b = {2 + 3 * target[2], 3 * target[3]};
    if (norm(full_a) + norm(full_b) != 167) {
      throw std::runtime_error("aggregate target left the norm-167 shell");
    }
  }
}

E signed_profile(int channel, int class_index, int id) {
  const int epsilon = class_index % 2 == 0 ? 1 : -1;
  const int factor = channel == 0 ? -epsilon : epsilon;
  return scale(factor, PROFILE_VALUES.at(id));
}

E pair_signature(int left_id, int right_id) {
  const E left = PROFILE_VALUES.at(left_id);
  const E right = PROFILE_VALUES.at(right_id);
  return {((left.a - left.b + right.a) % 3 + 3) % 3,
          ((-left.b + right.b) % 3 + 3) % 3};
}

struct Geometry {
  std::array<std::array<int, 3>, CLASS_COUNT> classes{};
  std::array<int, P> class_of{};
  // transition[lag_class][source_part][target_part]
  std::array<std::array<std::array<int, 13>, 13>, PAIR_COUNT> transition{};
};

int power_mod(int base, int exponent) {
  int result = 1;
  for (int index = 0; index < exponent; ++index) {
    result = result * base % P;
  }
  return result;
}

Geometry build_geometry() {
  Geometry result;
  result.class_of.fill(-1);
  const std::array<int, 3> subgroup = {1, 26, 10};
  for (int class_index = 0; class_index < CLASS_COUNT; ++class_index) {
    const int multiplier = power_mod(2, class_index);
    for (int local = 0; local < 3; ++local) {
      const int value = multiplier * subgroup[local] % P;
      result.classes[class_index][local] = value;
      if (result.class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      result.class_of[value] = class_index;
    }
  }
  for (int value = 1; value < P; ++value) {
    if (result.class_of[value] < 0) {
      throw std::runtime_error("cyclotomic classes do not cover F_37^*");
    }
  }

  auto part = [&](int value) { return value == 0 ? 0 : result.class_of[value] + 1; };
  for (int lag_class = 0; lag_class < PAIR_COUNT; ++lag_class) {
    const int lag = result.classes[lag_class][0];
    for (int source = 0; source < P; ++source) {
      ++result.transition[lag_class][part(source)][part((source + lag) % P)];
    }
    for (int representative : result.classes[lag_class]) {
      std::array<std::array<int, 13>, 13> direct{};
      for (int source = 0; source < P; ++source) {
        ++direct[part(source)][part((source + representative) % P)];
      }
      if (direct != result.transition[lag_class]) {
        throw std::runtime_error("transition matrix depends on class representative");
      }
    }
  }
  return result;
}

struct BlockRow {
  std::array<std::uint8_t, 4> ids{};
  int high = 0;
  int medium = 0;
  Target aggregate{};
  std::array<std::array<E, 2>, 2> coefficients{};
};

BlockRow make_block_row(int pair_index, const std::array<int, 4>& ids) {
  BlockRow row;
  for (int index = 0; index < 4; ++index) {
    row.ids[index] = static_cast<std::uint8_t>(ids[index]);
    row.high += profile_norm(ids[index]) == 9;
    row.medium += profile_norm(ids[index]) == 3;
  }
  row.coefficients[0][0] = signed_profile(0, pair_index, ids[0]);
  row.coefficients[0][1] = signed_profile(0, pair_index + 6, ids[1]);
  row.coefficients[1][0] = signed_profile(1, pair_index, ids[2]);
  row.coefficients[1][1] = signed_profile(1, pair_index + 6, ids[3]);
  row.aggregate = {
      row.coefficients[0][0].a + row.coefficients[0][1].a,
      row.coefficients[0][0].b + row.coefficients[0][1].b,
      row.coefficients[1][0].a + row.coefficients[1][1].a,
      row.coefficients[1][0].b + row.coefficients[1][1].b,
  };
  return row;
}

std::array<std::vector<BlockRow>, PAIR_COUNT> high_zero_rows() {
  std::array<std::vector<BlockRow>, PAIR_COUNT> result;
  constexpr std::array<int, 4> alphabet = {0, 3, 5, 9};
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    for (int a0 : alphabet) {
      for (int a1 : alphabet) {
        for (int b0 : alphabet) {
          for (int b1 : alphabet) {
            const std::array<int, 4> ids = {a0, a1, b0, b1};
            if (!(pair_signature(a0, a1) == pair_signature(b0, b1))) {
              throw std::runtime_error("high/zero quartet lost its zero signature");
            }
            result[pair].push_back(make_block_row(pair, ids));
          }
        }
      }
    }
    if (result[pair].size() != 256) {
      throw std::runtime_error("high/zero quartet must contain 256 rows");
    }
  }
  return result;
}

std::array<std::vector<BlockRow>, PAIR_COUNT> triple_medium_rows() {
  std::array<std::vector<BlockRow>, PAIR_COUNT> result;
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    for (int a0 = 0; a0 < PROFILE_COUNT; ++a0) {
      for (int a1 = 0; a1 < PROFILE_COUNT; ++a1) {
        for (int b0 = 0; b0 < PROFILE_COUNT; ++b0) {
          for (int b1 = 0; b1 < PROFILE_COUNT; ++b1) {
            const std::array<int, 4> ids = {a0, a1, b0, b1};
            const BlockRow row = make_block_row(pair, ids);
            if (row.medium != 3 || row.high > 1) {
              continue;
            }
            if (pair_signature(a0, a1) != pair_signature(b0, b1)) {
              continue;
            }
            result[pair].push_back(row);
          }
        }
      }
    }
    if (result[pair].size() != 864) {
      throw std::runtime_error("triple-medium quartet must contain 864 rows");
    }
  }
  return result;
}

std::map<std::pair<int, int>, int> audit_quartet_type_census() {
  const std::map<std::pair<int, int>, int> expected = {
      {{0, 0}, 1},   {{0, 2}, 108}, {{0, 3}, 216}, {{0, 4}, 486},
      {{1, 0}, 12},  {{1, 2}, 648}, {{1, 3}, 648}, {{2, 0}, 54},
      {{2, 2}, 972}, {{3, 0}, 108}, {{4, 0}, 81},
  };
  std::map<std::pair<int, int>, int> result;
  for (int a0 = 0; a0 < PROFILE_COUNT; ++a0) {
    for (int a1 = 0; a1 < PROFILE_COUNT; ++a1) {
      for (int b0 = 0; b0 < PROFILE_COUNT; ++b0) {
        for (int b1 = 0; b1 < PROFILE_COUNT; ++b1) {
          if (pair_signature(a0, a1) != pair_signature(b0, b1)) continue;
          const BlockRow row = make_block_row(0, {a0, a1, b0, b1});
          ++result[{row.high, row.medium}];
        }
      }
    }
  }
  if (result != expected) {
    throw std::runtime_error("opposite-quartet type census changed");
  }
  int total_rows = 0;
  for (const auto& [type, count] : result) {
    static_cast<void>(type);
    total_rows += count;
  }
  if (total_rows != 3334 || result.count({0, 1}) || result.count({1, 1})) {
    throw std::runtime_error("opposite-quartet sparse geometry changed");
  }
  return result;
}

std::array<std::array<E, 13>, 2> atoms_for_block(int pair,
                                                 const BlockRow& row) {
  std::array<std::array<E, 13>, 2> values{};
  values[0][pair + 1] = row.coefficients[0][0];
  values[0][pair + 7] = row.coefficients[0][1];
  values[1][pair + 1] = row.coefficients[1][0];
  values[1][pair + 7] = row.coefficients[1][1];
  return values;
}

Signature block_self_signature(const Geometry& geometry, int pair,
                               const BlockRow& row) {
  auto values = atoms_for_block(pair, row);
  values[0][0] = {-1, 0};
  values[1][0] = {2, 0};
  Signature result{};
  for (int lag_class = 0; lag_class < PAIR_COUNT; ++lag_class) {
    E total{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int source = 0; source < 13; ++source) {
        if (values[channel][source] == E{}) continue;
        for (int target = 0; target < 13; ++target) {
          const int count = geometry.transition[lag_class][source][target];
          if (!count || values[channel][target] == E{}) continue;
          total = add(total,
                      scale(count, multiply(values[channel][target],
                                            conjugate(values[channel][source]))));
        }
      }
    }
    result[2 * lag_class] = total.a;
    result[2 * lag_class + 1] = total.b;
  }
  return result;
}

Signature block_cross_signature(const Geometry& geometry, int left_pair,
                                const BlockRow& left, int right_pair,
                                const BlockRow& right) {
  const auto left_values = atoms_for_block(left_pair, left);
  const auto right_values = atoms_for_block(right_pair, right);
  Signature result{};
  for (int lag_class = 0; lag_class < PAIR_COUNT; ++lag_class) {
    E total{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int left_part = 1; left_part < 13; ++left_part) {
        if (left_values[channel][left_part] == E{}) continue;
        for (int right_part = 1; right_part < 13; ++right_part) {
          if (right_values[channel][right_part] == E{}) continue;
          const int left_to_right =
              geometry.transition[lag_class][left_part][right_part];
          const int right_to_left =
              geometry.transition[lag_class][right_part][left_part];
          if (left_to_right) {
            total = add(total,
                        scale(left_to_right,
                              multiply(right_values[channel][right_part],
                                       conjugate(left_values[channel][left_part]))));
          }
          if (right_to_left) {
            total = add(total,
                        scale(right_to_left,
                              multiply(left_values[channel][left_part],
                                       conjugate(right_values[channel][right_part]))));
          }
        }
      }
    }
    result[2 * lag_class] = total.a;
    result[2 * lag_class + 1] = total.b;
  }
  return result;
}

Signature signature_add(Signature left, const Signature& right) {
  for (int index = 0; index < 12; ++index) left[index] += right[index];
  return left;
}

Signature signature_mod9(Signature value) {
  for (int& coordinate : value) coordinate = mod9(coordinate);
  return value;
}

bool signature_zero(const Signature& value) {
  return std::all_of(value.begin(), value.end(), [](int x) { return x == 0; });
}

std::array<E, P> physical_correlations(const Geometry& geometry,
                                       const IdWord& a_ids,
                                       const IdWord& b_ids) {
  std::array<std::array<E, P>, 2> words{};
  words[0][0] = {-1, 0};
  words[1][0] = {2, 0};
  for (int column = 1; column < P; ++column) {
    const int class_index = geometry.class_of[column];
    words[0][column] = signed_profile(0, class_index, a_ids[class_index]);
    words[1][column] = signed_profile(1, class_index, b_ids[class_index]);
  }
  std::array<E, P> result{};
  for (int lag = 0; lag < P; ++lag) {
    E total{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int source = 0; source < P; ++source) {
        total = add(total,
                    multiply(words[channel][(source + lag) % P],
                             conjugate(words[channel][source])));
      }
    }
    if (lag == 0) total.a -= 167;
    result[lag] = total;
  }
  return result;
}

Signature physical_signature(const Geometry& geometry, const IdWord& a_ids,
                             const IdWord& b_ids,
                             bool require_zero_origin = true) {
  const auto physical = physical_correlations(geometry, a_ids, b_ids);
  if (require_zero_origin && !(physical[0] == E{})) {
    throw std::runtime_error("physical replay has nonzero origin residual");
  }
  Signature result{};
  for (int class_index = 0; class_index < CLASS_COUNT; ++class_index) {
    const E representative = physical[geometry.classes[class_index][0]];
    for (int value : geometry.classes[class_index]) {
      if (!(physical[value] == representative)) {
        throw std::runtime_error("physical correlation lost H-invariance");
      }
    }
    if (class_index < PAIR_COUNT) {
      result[2 * class_index] = representative.a;
      result[2 * class_index + 1] = representative.b;
    } else if (!(representative ==
                 conjugate({result[2 * (class_index - 6)],
                            result[2 * (class_index - 6) + 1]}))) {
      throw std::runtime_error("physical correlation lost reversal conjugacy");
    }
  }
  return result;
}

Target assignment_aggregate(const IdWord& a_ids, const IdWord& b_ids) {
  Target result{};
  for (int channel = 0; channel < 2; ++channel) {
    const IdWord& ids = channel == 0 ? a_ids : b_ids;
    E total{};
    for (int class_index = 0; class_index < CLASS_COUNT; ++class_index) {
      total = add(total, signed_profile(channel, class_index, ids[class_index]));
    }
    result[2 * channel] = total.a;
    result[2 * channel + 1] = total.b;
  }
  return result;
}

int assignment_high_count(const IdWord& a_ids, const IdWord& b_ids) {
  int result = 0;
  for (int id : a_ids) result += profile_norm(id) == 9;
  for (int id : b_ids) result += profile_norm(id) == 9;
  return result;
}

int assignment_medium_count(const IdWord& a_ids, const IdWord& b_ids) {
  int result = 0;
  for (int id : a_ids) result += profile_norm(id) == 3;
  for (int id : b_ids) result += profile_norm(id) == 3;
  return result;
}

void install_block(int pair, const BlockRow& row, IdWord& a_ids, IdWord& b_ids) {
  a_ids[pair] = row.ids[0];
  a_ids[pair + 6] = row.ids[1];
  b_ids[pair] = row.ids[2];
  b_ids[pair + 6] = row.ids[3];
}

bool target_is(const Target& left, const Target& right) { return left == right; }

struct ShellResult {
  std::array<std::uint64_t, TARGET_COUNT> aggregate_counts{};
  std::array<std::uint64_t, TARGET_COUNT> mod9_counts{};
  std::array<std::uint64_t, 13> bad_part_histogram{};
  std::uint64_t exact_survivors = 0;
  std::vector<std::uint8_t> replay_certificate;
};

void append_u32(std::vector<std::uint8_t>& output, std::int32_t signed_value) {
  const std::uint32_t value = static_cast<std::uint32_t>(signed_value);
  output.push_back(static_cast<std::uint8_t>(value >> 24U));
  output.push_back(static_cast<std::uint8_t>(value >> 16U));
  output.push_back(static_cast<std::uint8_t>(value >> 8U));
  output.push_back(static_cast<std::uint8_t>(value));
}

void replay_candidate(const Geometry& geometry, int expected_high,
                      int expected_medium, int target_index,
                      const IdWord& a_ids, const IdWord& b_ids,
                      ShellResult& result) {
  const Target& target = TARGETS.at(target_index);
  if (assignment_high_count(a_ids, b_ids) != expected_high ||
      assignment_medium_count(a_ids, b_ids) != expected_medium) {
    throw std::runtime_error("candidate left its declared type shell");
  }
  if (assignment_aggregate(a_ids, b_ids) != target) {
    throw std::runtime_error("candidate aggregate replay failed");
  }
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    if (!(pair_signature(a_ids[pair], a_ids[pair + 6]) ==
          pair_signature(b_ids[pair], b_ids[pair + 6]))) {
      throw std::runtime_error("candidate opposite-pair replay failed");
    }
  }
  const Signature exact = physical_signature(geometry, a_ids, b_ids);
  if (!signature_zero(signature_mod9(exact))) {
    throw std::runtime_error("modulo-9 survivor failed detached physical replay");
  }
  int bad = 0;
  for (int part = 0; part < PAIR_COUNT; ++part) {
    const E value = {exact[2 * part], exact[2 * part + 1]};
    if (!(value == E{})) bad += 2;
  }
  ++result.bad_part_histogram.at(bad);
  if (bad == 0) ++result.exact_survivors;

  result.replay_certificate.push_back(
      static_cast<std::uint8_t>(expected_high));
  result.replay_certificate.push_back(
      static_cast<std::uint8_t>(target_index));
  for (int id : a_ids) result.replay_certificate.push_back(id);
  for (int id : b_ids) result.replay_certificate.push_back(id);
  for (int coordinate : exact) {
    append_u32(result.replay_certificate, coordinate);
  }
}

ShellResult audit_h6(
    const Geometry& geometry,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& high_rows) {
  ShellResult result;

  using CountKey = std::array<int, 5>;
  std::map<CountKey, std::uint64_t> states = {{{0, 0, 0, 0, 0}, 1}};
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    std::map<CountKey, std::uint64_t> next;
    for (const auto& [key, count] : states) {
      for (const BlockRow& row : high_rows[pair]) {
        if (key[0] + row.high > 6) continue;
        CountKey new_key = key;
        new_key[0] += row.high;
        for (int coordinate = 0; coordinate < 4; ++coordinate) {
          new_key[coordinate + 1] += row.aggregate[coordinate];
        }
        next[new_key] += count;
      }
    }
    states = std::move(next);
  }
  for (int target_index = 0; target_index < TARGET_COUNT; ++target_index) {
    const CountKey key = {6, TARGETS[target_index][0], TARGETS[target_index][1],
                          TARGETS[target_index][2], TARGETS[target_index][3]};
    const auto found = states.find(key);
    if (found != states.end()) result.aggregate_counts[target_index] = found->second;
  }

  std::array<std::vector<BlockRow>, PAIR_COUNT> allowed;
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    std::array<int, 5> high_histogram{};
    for (const BlockRow& row : high_rows[pair]) {
      const Signature reduced = signature_mod9(block_self_signature(geometry, pair, row));
      for (int coordinate = 0; coordinate < 12; ++coordinate) {
        if (coordinate / 2 != pair && reduced[coordinate] != 0) {
          throw std::runtime_error(
              "high/zero origin term escaped its opposite-class quartet");
        }
      }
      if (signature_zero(reduced)) {
        allowed[pair].push_back(row);
        ++high_histogram.at(row.high);
      }
    }
    if (allowed[pair].size() != 40 ||
        high_histogram != std::array<int, 5>{1, 0, 12, 0, 27}) {
      throw std::runtime_error("h=6 local modulo-9 quartet count changed");
    }
  }

  IdWord a_ids{};
  IdWord b_ids{};
  a_ids.fill(5);
  b_ids.fill(5);
  Target aggregate{};

  auto recurse = [&](auto&& self, int pair, int high) -> void {
    if (high > 6) return;
    if (pair == PAIR_COUNT) {
      if (high != 6) return;
      for (int target_index = 0; target_index < TARGET_COUNT; ++target_index) {
        if (!target_is(aggregate, TARGETS[target_index])) continue;
        ++result.mod9_counts[target_index];
        replay_candidate(geometry, 6, 0, target_index, a_ids, b_ids, result);
      }
      return;
    }
    const Target saved = aggregate;
    for (const BlockRow& row : allowed[pair]) {
      aggregate = saved;
      for (int coordinate = 0; coordinate < 4; ++coordinate) {
        aggregate[coordinate] += row.aggregate[coordinate];
      }
      install_block(pair, row, a_ids, b_ids);
      self(self, pair + 1, high + row.high);
    }
    aggregate = saved;
    a_ids[pair] = a_ids[pair + 6] = 5;
    b_ids[pair] = b_ids[pair + 6] = 5;
  };
  recurse(recurse, 0, 0);
  return result;
}

struct HighKey {
  std::array<std::int8_t, 5> values{};
  friend bool operator==(const HighKey&, const HighKey&) = default;
};

struct HighKeyHash {
  std::size_t operator()(const HighKey& key) const {
    std::uint64_t value = 1469598103934665603ULL;
    for (std::int8_t coordinate : key.values) {
      value ^= static_cast<std::uint8_t>(coordinate);
      value *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(value);
  }
};

HighKey high_key(int high, const Target& aggregate) {
  HighKey result;
  result.values[0] = static_cast<std::int8_t>(high);
  for (int index = 0; index < 4; ++index) {
    if (aggregate[index] < -120 || aggregate[index] > 120) {
      throw std::runtime_error("packed aggregate left int8 range");
    }
    result.values[index + 1] = static_cast<std::int8_t>(aggregate[index]);
  }
  return result;
}

using HighCatalog =
    std::unordered_map<HighKey, std::vector<std::uint64_t>, HighKeyHash>;

HighCatalog build_high_catalog(
    int missing_pair,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& high_rows,
    std::array<int, 5>& active_pairs) {
  int active_index = 0;
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    if (pair != missing_pair) active_pairs[active_index++] = pair;
  }
  HighCatalog result;
  Target aggregate{};
  auto recurse = [&](auto&& self, int depth, int high,
                     std::uint64_t packed) -> void {
    if (high > 5) return;
    if (depth == 5) {
      if (high == 4 || high == 5) {
        result[high_key(high, aggregate)].push_back(packed);
      }
      return;
    }
    const int pair = active_pairs[depth];
    const Target saved = aggregate;
    for (std::size_t row_index = 0; row_index < high_rows[pair].size();
         ++row_index) {
      const BlockRow& row = high_rows[pair][row_index];
      aggregate = saved;
      for (int coordinate = 0; coordinate < 4; ++coordinate) {
        aggregate[coordinate] += row.aggregate[coordinate];
      }
      self(self, depth + 1, high + row.high,
           packed | (static_cast<std::uint64_t>(row_index) << (8 * depth)));
    }
    aggregate = saved;
  };
  recurse(recurse, 0, 0, 0);
  std::array<std::uint64_t, 6> high_counts{};
  for (const auto& [key, assignments] : result) {
    high_counts.at(static_cast<std::uint8_t>(key.values[0])) += assignments.size();
  }
  if (high_counts[4] != 392445 || high_counts[5] != 3767472) {
    throw std::runtime_error("five-block sparse high catalog changed");
  }
  return result;
}

ShellResult audit_h5(
    const Geometry& geometry,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& high_rows,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& medium_rows) {
  ShellResult result;
  for (int medium_pair = 0; medium_pair < PAIR_COUNT; ++medium_pair) {
    std::array<int, 5> active_pairs{};
    const HighCatalog catalog =
        build_high_catalog(medium_pair, high_rows, active_pairs);

    for (const BlockRow& medium : medium_rows[medium_pair]) {
      const int needed_high = 5 - medium.high;
      const Signature base =
          signature_mod9(block_self_signature(geometry, medium_pair, medium));

      std::array<std::array<Signature, 256>, 5> increments{};
      for (int depth = 0; depth < 5; ++depth) {
        const int pair = active_pairs[depth];
        for (int row_index = 0; row_index < 256; ++row_index) {
          Signature value = block_self_signature(
              geometry, pair, high_rows[pair][row_index]);
          value = signature_add(
              value, block_cross_signature(geometry, medium_pair, medium, pair,
                                           high_rows[pair][row_index]));
          increments[depth][row_index] = signature_mod9(value);
        }
      }

      for (int target_index = 0; target_index < TARGET_COUNT; ++target_index) {
        Target needed_aggregate{};
        for (int coordinate = 0; coordinate < 4; ++coordinate) {
          needed_aggregate[coordinate] =
              TARGETS[target_index][coordinate] - medium.aggregate[coordinate];
        }
        const auto found =
            catalog.find(high_key(needed_high, needed_aggregate));
        if (found == catalog.end()) continue;
        result.aggregate_counts[target_index] += found->second.size();

        for (std::uint64_t packed : found->second) {
          Signature reduced = base;
          for (int depth = 0; depth < 5; ++depth) {
            const int row_index = static_cast<int>((packed >> (8 * depth)) & 255U);
            for (int coordinate = 0; coordinate < 12; ++coordinate) {
              reduced[coordinate] =
                  (reduced[coordinate] + increments[depth][row_index][coordinate]) %
                  9;
            }
          }
          if (!signature_zero(reduced)) continue;
          ++result.mod9_counts[target_index];

          IdWord a_ids{};
          IdWord b_ids{};
          a_ids.fill(5);
          b_ids.fill(5);
          install_block(medium_pair, medium, a_ids, b_ids);
          for (int depth = 0; depth < 5; ++depth) {
            const int pair = active_pairs[depth];
            const int row_index = static_cast<int>((packed >> (8 * depth)) & 255U);
            install_block(pair, high_rows[pair][row_index], a_ids, b_ids);
          }
          replay_candidate(geometry, 5, 3, target_index, a_ids, b_ids, result);
        }
      }
    }
  }
  return result;
}

void require_pinned_results(const ShellResult& h6, const ShellResult& h5) {
  std::array<std::uint64_t, TARGET_COUNT> expected_h6_aggregate{};
  std::array<std::uint64_t, TARGET_COUNT> expected_h6_mod9{};
  for (int index : {2, 3, 16, 17}) {
    expected_h6_aggregate[index] = 413460;
    expected_h6_mod9[index] = 72;
  }
  std::array<std::uint64_t, 13> expected_h6_bad{};
  expected_h6_bad[10] = 24;
  expected_h6_bad[12] = 264;
  if (h6.aggregate_counts != expected_h6_aggregate ||
      h6.mod9_counts != expected_h6_mod9 ||
      h6.bad_part_histogram != expected_h6_bad ||
      h6.exact_survivors != 0 ||
      h6.replay_certificate.size() != 288U * 74U ||
      sha256(h6.replay_certificate) != EXPECTED_H6_REPLAY_SHA256) {
    throw std::runtime_error("pinned h=6 sparse-shell result changed");
  }

  std::array<std::uint64_t, TARGET_COUNT> expected_h5_aggregate{};
  std::array<std::uint64_t, TARGET_COUNT> expected_h5_mod9{};
  for (int index : {0, 1, 6, 7}) {
    expected_h5_aggregate[index] = 5748834;
    expected_h5_mod9[index] = 42;
  }
  for (int index : {18, 21}) {
    expected_h5_aggregate[index] = 5819400;
    expected_h5_mod9[index] = 192;
  }
  std::array<std::uint64_t, 13> expected_h5_bad{};
  expected_h5_bad[6] = 24;
  expected_h5_bad[10] = 144;
  expected_h5_bad[12] = 384;
  if (h5.aggregate_counts != expected_h5_aggregate ||
      h5.mod9_counts != expected_h5_mod9 ||
      h5.bad_part_histogram != expected_h5_bad ||
      h5.exact_survivors != 0 ||
      h5.replay_certificate.size() != 552U * 74U ||
      sha256(h5.replay_certificate) != EXPECTED_H5_REPLAY_SHA256) {
    throw std::runtime_error("pinned h=5 sparse-shell result changed");
  }
}

std::uint64_t total(const std::array<std::uint64_t, TARGET_COUNT>& values) {
  std::uint64_t result = 0;
  for (std::uint64_t value : values) result += value;
  return result;
}

void print_nonzero_counts(
    const std::string& label,
    const std::array<std::uint64_t, TARGET_COUNT>& values) {
  std::cout << label << "=";
  bool first = true;
  for (int index = 0; index < TARGET_COUNT; ++index) {
    if (!values[index]) continue;
    if (!first) std::cout << ";";
    first = false;
    std::cout << "(" << TARGETS[index][0] << "," << TARGETS[index][1] << ","
              << TARGETS[index][2] << "," << TARGETS[index][3] << "):"
              << values[index];
  }
  std::cout << "\n";
}

void print_histogram(const std::string& label,
                     const std::array<std::uint64_t, 13>& values) {
  std::cout << label << "=";
  bool first = true;
  for (int index = 0; index < 13; ++index) {
    if (!values[index]) continue;
    if (!first) std::cout << ";";
    first = false;
    std::cout << index << ":" << values[index];
  }
  std::cout << "\n";
}

void audit_block_decomposition(
    const Geometry& geometry,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& high_rows,
    const std::array<std::vector<BlockRow>, PAIR_COUNT>& medium_rows) {
  IdWord a_ids{};
  IdWord b_ids{};
  a_ids.fill(5);
  b_ids.fill(5);
  std::array<const BlockRow*, PAIR_COUNT> rows{};
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    const BlockRow& row =
        pair == 2 ? medium_rows[pair][137] : high_rows[pair][(37 * pair + 11) % 256];
    rows[pair] = &row;
    install_block(pair, row, a_ids, b_ids);
  }
  Signature decomposed{};
  for (int pair = 0; pair < PAIR_COUNT; ++pair) {
    decomposed =
        signature_add(decomposed, block_self_signature(geometry, pair, *rows[pair]));
    for (int prior = 0; prior < pair; ++prior) {
      decomposed = signature_add(
          decomposed,
          block_cross_signature(geometry, prior, *rows[prior], pair, *rows[pair]));
    }
  }
  if (decomposed != physical_signature(geometry, a_ids, b_ids, false)) {
    throw std::runtime_error("block and physical correlation replays disagree");
  }
}

}  // namespace

int main() {
  try {
    if (sha256({'a', 'b', 'c'}) !=
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad") {
      throw std::runtime_error("internal SHA-256 implementation failed");
    }
    audit_profile_alphabet_and_targets();
    const Geometry geometry = build_geometry();
    const auto quartet_census = audit_quartet_type_census();
    const auto high_rows = high_zero_rows();
    const auto medium_rows = triple_medium_rows();
    audit_block_decomposition(geometry, high_rows, medium_rows);
    std::cout << "quartet_legal_rows=3334\n";
    std::cout << "quartet_medium_count_support=0,2,3,4\n";
    std::cout << "quartet_triple_medium_rows="
              << quartet_census.at({0, 3}) + quartet_census.at({1, 3}) << "\n";

    const ShellResult h6 = audit_h6(geometry, high_rows);
    const ShellResult h5 = audit_h5(geometry, high_rows, medium_rows);
    require_pinned_results(h6, h5);

    std::cout << "h6_aggregate_candidates=" << total(h6.aggregate_counts) << "\n";
    print_nonzero_counts("h6_aggregate_by_target", h6.aggregate_counts);
    std::cout << "h6_mod9_candidates=" << total(h6.mod9_counts) << "\n";
    print_nonzero_counts("h6_mod9_by_target", h6.mod9_counts);
    print_histogram("h6_bad_part_histogram", h6.bad_part_histogram);
    std::cout << "h6_exact_survivors=" << h6.exact_survivors << "\n";
    std::cout << "h6_replay_certificate_sha256="
              << sha256(h6.replay_certificate) << "\n";

    std::cout << "h5_aggregate_candidates=" << total(h5.aggregate_counts) << "\n";
    print_nonzero_counts("h5_aggregate_by_target", h5.aggregate_counts);
    std::cout << "h5_mod9_candidates=" << total(h5.mod9_counts) << "\n";
    print_nonzero_counts("h5_mod9_by_target", h5.mod9_counts);
    print_histogram("h5_bad_part_histogram", h5.bad_part_histogram);
    std::cout << "h5_exact_survivors=" << h5.exact_survivors << "\n";
    std::cout << "h5_replay_certificate_sha256="
              << sha256(h5.replay_certificate) << "\n";
    std::cout << "PASS: exact h=5 and h=6 profile sectors excluded\n";
    std::cout << "STATUS: no profile survivor, LP(333), or H(668) asserted\n";
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << "\n";
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
