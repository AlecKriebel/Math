// Complete characteristic-two census for the order-three LP(333) profiles.
//
// This program independently derives the twelve Boolean quadratic output
// bits from direct F_4 autocorrelation values, then evaluates all 2^24 class
// words by a Gray walk.  It stores counts only; no candidate list is
// materialized.

#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string_view>
#include <vector>

namespace {

constexpr int kPrime = 37;
constexpr int kClasses = 12;
constexpr int kLags = 6;
constexpr int kBits = 24;
constexpr int kSignatures = 4096;
constexpr std::uint32_t kWords = 1u << kBits;

int multiply_f4(int left, int right) {
  const int a = left & 1;
  const int b = left >> 1;
  const int c = right & 1;
  const int d = right >> 1;
  return (a * c ^ b * d) | ((a * d ^ b * c ^ b * d) << 1);
}

int square_f4(int value) { return multiply_f4(value, value); }

struct Geometry {
  std::array<std::array<int, 3>, kClasses> orbit{};
  std::array<int, kPrime> index{};
};

Geometry make_geometry() {
  Geometry geometry;
  geometry.index.fill(-1);
  constexpr std::array<int, 3> subgroup = {1, 10, 26};
  int representative = 1;
  for (int block = 0; block < kClasses; ++block) {
    for (int offset = 0; offset < 3; ++offset) {
      const int position = representative * subgroup[offset] % kPrime;
      geometry.orbit[block][offset] = position;
      if (geometry.index[position] != -1) {
        throw std::runtime_error("overlapping H-orbits");
      }
      geometry.index[position] = block;
    }
    representative = 2 * representative % kPrime;
  }
  for (int position = 1; position < kPrime; ++position) {
    if (geometry.index[position] < 0) {
      throw std::runtime_error("incomplete H-orbit cover");
    }
  }
  return geometry;
}

std::array<std::uint8_t, kClasses> unpack(std::uint32_t bits) {
  std::array<std::uint8_t, kClasses> coefficients{};
  for (int index = 0; index < kClasses; ++index) {
    coefficients[index] =
        static_cast<std::uint8_t>((bits >> (2 * index)) & 3u);
  }
  return coefficients;
}

std::uint16_t direct_output(
    const Geometry& geometry,
    int origin,
    const std::array<std::uint8_t, kClasses>& coefficients) {
  std::array<int, kPrime> word{};
  word[0] = origin;
  for (int position = 1; position < kPrime; ++position) {
    word[position] = coefficients[geometry.index[position]];
  }
  std::uint16_t packed = 0;
  for (int lag_index = 0; lag_index < kLags; ++lag_index) {
    const int lag = geometry.orbit[lag_index][0];
    int correlation = 0;
    for (int source = 0; source < kPrime; ++source) {
      correlation ^= multiply_f4(
          word[(source + lag) % kPrime],
          square_f4(word[source]));
    }
    packed |= static_cast<std::uint16_t>(correlation << (2 * lag_index));
  }
  return packed;
}

struct QuadraticMap {
  std::uint16_t constant = 0;
  std::array<std::uint16_t, kBits> first{};
  std::array<std::array<std::uint16_t, kBits>, kBits> second{};
};

QuadraticMap derive_map(const Geometry& geometry, int origin) {
  QuadraticMap map;
  map.constant = direct_output(geometry, origin, {});
  for (int bit = 0; bit < kBits; ++bit) {
    map.first[bit] =
        direct_output(geometry, origin, unpack(1u << bit)) ^ map.constant;
  }
  for (int left = 0; left < kBits; ++left) {
    for (int right = left + 1; right < kBits; ++right) {
      const auto value = direct_output(
          geometry, origin, unpack((1u << left) | (1u << right)));
      map.second[left][right] = map.second[right][left] =
          value ^ map.constant ^ map.first[left] ^ map.first[right];
    }
  }
  return map;
}

std::uint16_t evaluate(const QuadraticMap& map, std::uint32_t bits) {
  std::uint16_t value = map.constant;
  for (int left = 0; left < kBits; ++left) {
    if (!(bits & (1u << left))) continue;
    value ^= map.first[left];
    for (int right = left + 1; right < kBits; ++right) {
      if (bits & (1u << right)) value ^= map.second[left][right];
    }
  }
  return value;
}

class Census {
 public:
  Census() : counts_(4 * 13 * kSignatures) {}

  std::uint32_t& at(int aggregate, int support, int signature) {
    return counts_.at((aggregate * 13 + support) * kSignatures + signature);
  }
  std::uint32_t at(int aggregate, int support, int signature) const {
    return counts_.at((aggregate * 13 + support) * kSignatures + signature);
  }

  std::uint64_t total() const {
    std::uint64_t result = 0;
    for (const auto value : counts_) result += value;
    return result;
  }

 private:
  std::vector<std::uint32_t> counts_;
};

Census enumerate(const Geometry& geometry, const QuadraticMap& map, int origin) {
  Census census;
  std::array<std::uint16_t, kBits> derivative = map.first;
  std::array<std::uint8_t, kClasses> coefficients{};
  std::uint32_t gray = 0;
  std::uint16_t signature = map.constant;
  int aggregate = 0;
  int support = 0;
  ++census.at(aggregate, support, signature);

  for (std::uint32_t step = 1; step < kWords; ++step) {
    const int bit = std::countr_zero(step);
    const int coordinate = bit / 2;
    const int basis = 1 << (bit % 2);
    const int old_value = coefficients[coordinate];
    const int new_value = old_value ^ basis;

    signature ^= derivative[bit];
    for (int other = 0; other < kBits; ++other) {
      if (other != bit) derivative[other] ^= map.second[bit][other];
    }
    coefficients[coordinate] = static_cast<std::uint8_t>(new_value);
    gray ^= 1u << bit;
    aggregate ^= basis;
    support += (new_value != 0) - (old_value != 0);
    auto& bucket = census.at(aggregate, support, signature);
    if (bucket == std::numeric_limits<std::uint32_t>::max()) {
      throw std::overflow_error("a census bucket overflowed");
    }
    ++bucket;

    if ((step & ((1u << 20) - 1)) == 0) {
      if (unpack(gray) != coefficients ||
          evaluate(map, gray) != signature ||
          direct_output(geometry, origin, coefficients) != signature) {
        throw std::runtime_error("the incremental census drifted");
      }
    }
  }
  return census;
}

std::uint64_t join(
    const Census& left,
    const Census& right,
    int aggregate_left,
    int aggregate_right,
    int total_support) {
  std::uint64_t result = 0;
  for (int left_support = 0; left_support <= 12; ++left_support) {
    const int right_support = total_support - left_support;
    if (right_support < 0 || right_support > 12) continue;
    for (int signature = 0; signature < kSignatures; ++signature) {
      result += static_cast<std::uint64_t>(
          left.at(aggregate_left, left_support, signature))
          * right.at(aggregate_right, right_support, signature);
    }
  }
  return result;
}

struct Target {
  std::string_view name;
  int aggregate_a;
  int aggregate_b;
  int multiplicity;
  std::array<std::uint64_t, 3> expected;
};

constexpr std::array<Target, 5> kTargets = {{
    {"1+w,0", 3, 0, 5, {1591338552, 966197016, 286163712}},
    {"1,1+w", 1, 3, 4, {1591301760, 966296568, 286154784}},
    {"1,w", 1, 2, 4, {1591301760, 966296568, 286154784}},
    {"w,0", 2, 0, 5, {1591338552, 966197016, 286163712}},
    {"0,0", 0, 0, 4, {1591802496, 966019275, 286244568}},
}};

}  // namespace

int main() {
  const Geometry geometry = make_geometry();
  const auto map_a = derive_map(geometry, 1);
  const auto map_b = derive_map(geometry, 0);
  const Census census_a = enumerate(geometry, map_a, 1);
  const Census census_b = enumerate(geometry, map_b, 0);
  if (census_a.total() != kWords || census_b.total() != kWords) {
    throw std::runtime_error("a complete channel census lost words");
  }

  std::array<std::array<std::uint64_t, 3>, 5> observed{};
  for (std::size_t target = 0; target < kTargets.size(); ++target) {
    for (int high = 0; high <= 2; ++high) {
      observed[target][high] = join(
          census_a, census_b,
          kTargets[target].aggregate_a,
          kTargets[target].aggregate_b,
          18 - 2 * high);
      if (observed[target][high] != kTargets[target].expected[high]) {
        throw std::runtime_error("the exact characteristic-two census changed");
      }
    }
  }

  std::cout << "{\n"
            << "  \"schema\":\"lp333-order3-char2-census-output-v1\",\n"
            << "  \"channel_words\":" << kWords << ",\n"
            << "  \"targets\":[\n";
  for (std::size_t target = 0; target < kTargets.size(); ++target) {
    if (target) std::cout << ",\n";
    std::cout << "    {\"name\":\"" << kTargets[target].name
              << "\",\"aggregate\":[" << kTargets[target].aggregate_a
              << "," << kTargets[target].aggregate_b
              << "],\"multiplicity\":" << kTargets[target].multiplicity
              << ",\"matches\":{\"h0\":" << observed[target][0]
              << ",\"h1\":" << observed[target][1]
              << ",\"h2\":" << observed[target][2] << "}}";
  }
  std::cout << "\n  ],\n"
            << "  \"status\":\"PASS\"\n"
            << "}\n";
}
