// Exact full-PAF joins for prime-83 Sidelnikov products:
//   * independently decimated products through degree three;
//   * un-decimated products through degree four.
//
// This independently extends verify_degree3_sidelnikov_fold.py.  A common
// decimation normalizes U, while V,C,D retain arbitrary relative nonzero
// multipliers modulo 83.  The inverse-pair condition is applied before the
// full 41-coordinate integer PAF join.
//
// Build and run:
//   clang++ -O3 -std=c++20 audit_independent_decimations.cpp -o /tmp/d3dec
//   /tmp/d3dec
//   /tmp/d3dec --degree4-undecimated

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kPrime = 167;
constexpr int kOrder = 83;
constexpr int kHalf = 41;
constexpr int kEnergy = 334;

using Sequence = std::array<std::int8_t, kOrder>;
using Paf = std::array<std::int16_t, kHalf>;

struct Bits {
  std::uint64_t low = 0;
  std::uint64_t high = 0;
  auto operator<=>(const Bits&) const = default;
};

struct BinaryTemplate {
  Sequence sequence{};
  Paf paf{};
  int row_sum = 0;
};

struct ZeroRepresentative {
  Sequence sequence{};
  Paf paf{};
  int absolute_row_sum = 0;
};

struct PafHash {
  std::size_t operator()(const Paf& values) const noexcept {
    std::uint64_t state = 1469598103934665603ULL;
    for (std::int16_t value : values) {
      state ^= static_cast<std::uint16_t>(value);
      state *= 1099511628211ULL;
    }
    return static_cast<std::size_t>(state);
  }
};

using PafSet = std::unordered_set<Paf, PafHash>;

int Mod(int value, int modulus) {
  value %= modulus;
  return value < 0 ? value + modulus : value;
}

int PowerMod(int base, int exponent, int modulus) {
  long long result = 1;
  long long factor = Mod(base, modulus);
  while (exponent > 0) {
    if (exponent & 1) {
      result = result * factor % modulus;
    }
    factor = factor * factor % modulus;
    exponent >>= 1;
  }
  return static_cast<int>(result);
}

int Character(int value) {
  value = Mod(value, kPrime);
  if (value == 0) {
    return 0;
  }
  return PowerMod(value, (kPrime - 1) / 2, kPrime) == 1 ? 1 : -1;
}

Sequence Shift(const Sequence& sequence, int amount) {
  Sequence result{};
  for (int index = 0; index < kOrder; ++index) {
    result[index] = sequence[Mod(index - amount, kOrder)];
  }
  return result;
}

Sequence Decimate(const Sequence& sequence, int multiplier) {
  Sequence result{};
  for (int index = 0; index < kOrder; ++index) {
    result[index] = sequence[Mod(multiplier * index, kOrder)];
  }
  return result;
}

Sequence Multiply(const Sequence& left, const Sequence& right) {
  Sequence result{};
  for (int index = 0; index < kOrder; ++index) {
    result[index] = static_cast<std::int8_t>(
        static_cast<int>(left[index]) * static_cast<int>(right[index]));
  }
  return result;
}

int RowSum(const Sequence& sequence) {
  return std::accumulate(sequence.begin(), sequence.end(), 0);
}

Paf PeriodicPaf(const Sequence& sequence) {
  Paf result{};
  for (int lag = 1; lag <= kHalf; ++lag) {
    int value = 0;
    for (int index = 0; index < kOrder; ++index) {
      value += static_cast<int>(sequence[index]) *
               static_cast<int>(sequence[(index + lag) % kOrder]);
    }
    result[lag - 1] = static_cast<std::int16_t>(value);
  }
  return result;
}

bool GetBit(const Bits& bits, int index) {
  if (index < 64) {
    return ((bits.low >> index) & 1U) != 0;
  }
  return ((bits.high >> (index - 64)) & 1U) != 0;
}

void SetBit(Bits& bits, int index) {
  if (index < 64) {
    bits.low |= std::uint64_t{1} << index;
  } else {
    bits.high |= std::uint64_t{1} << (index - 64);
  }
}

int Value(const Bits& bits, int index) {
  return GetBit(bits, index) ? -1 : 1;
}

int RowSum(const Bits& bits) {
  return kOrder -
         2 * (std::popcount(bits.low) + std::popcount(bits.high));
}

Sequence ToSequence(const Bits& bits) {
  Sequence result{};
  for (int index = 0; index < kOrder; ++index) {
    result[index] = static_cast<std::int8_t>(Value(bits, index));
  }
  return result;
}

Bits AffineBits(const Sequence& sequence, int multiplier, int offset) {
  Bits result;
  for (int index = 0; index < kOrder; ++index) {
    const int source = Mod(multiplier * index + offset, kOrder);
    if (sequence[source] < 0) {
      SetBit(result, index);
    }
  }
  return result;
}

Bits ComplementBits(const Bits& bits) {
  constexpr std::uint64_t kHighMask =
      (std::uint64_t{1} << (kOrder - 64)) - 1;
  return Bits{~bits.low, (~bits.high) & kHighMask};
}

std::uint64_t Orientation(const Bits& bits) {
  std::uint64_t result = 0;
  for (int lag = 1; lag <= kHalf; ++lag) {
    if (GetBit(bits, lag) == GetBit(bits, kOrder - lag)) {
      result |= std::uint64_t{1} << (lag - 1);
    }
  }
  return result;
}

std::uint64_t Orientation(const Sequence& sequence) {
  std::uint64_t result = 0;
  for (int lag = 1; lag <= kHalf; ++lag) {
    if (sequence[lag] == sequence[kOrder - lag]) {
      result |= std::uint64_t{1} << (lag - 1);
    }
  }
  return result;
}

std::string Encode(const Sequence& sequence) {
  std::string result;
  result.reserve(kOrder);
  for (int value : sequence) {
    result.push_back(value < 0 ? '0' : value == 0 ? '1' : '2');
  }
  return result;
}

std::vector<int> CanonicalTranslate(const std::vector<int>& indices) {
  if (indices.empty()) {
    return {};
  }
  std::vector<int> best;
  bool initialized = false;
  for (int anchor : indices) {
    std::vector<int> candidate;
    candidate.reserve(indices.size());
    for (int index : indices) {
      candidate.push_back(Mod(index - anchor, kOrder));
    }
    std::sort(candidate.begin(), candidate.end());
    if (!initialized || candidate < best) {
      best = std::move(candidate);
      initialized = true;
    }
  }
  return best;
}

template <class Callback>
void EnumerateSubsets(int size, Callback&& callback) {
  if (size == 0) {
    callback(std::vector<int>{});
  } else if (size == 1) {
    for (int first = 0; first < kOrder; ++first) {
      callback(std::vector<int>{first});
    }
  } else if (size == 2) {
    for (int first = 0; first < kOrder; ++first) {
      for (int second = first + 1; second < kOrder; ++second) {
        callback(std::vector<int>{first, second});
      }
    }
  } else if (size == 3) {
    for (int first = 0; first < kOrder; ++first) {
      for (int second = first + 1; second < kOrder; ++second) {
        for (int third = second + 1; third < kOrder; ++third) {
          callback(std::vector<int>{first, second, third});
        }
      }
    }
  } else if (size == 4) {
    for (int first = 0; first < kOrder; ++first) {
      for (int second = first + 1; second < kOrder; ++second) {
        for (int third = second + 1; third < kOrder; ++third) {
          for (int fourth = third + 1; fourth < kOrder; ++fourth) {
            callback(std::vector<int>{first, second, third, fourth});
          }
        }
      }
    }
  } else {
    throw std::runtime_error("unsupported subset size");
  }
}

Sequence ProductOfPhases(const std::array<Sequence, kOrder>& phases,
                         const std::vector<int>& indices) {
  Sequence result{};
  result.fill(1);
  for (int index : indices) {
    result = Multiply(result, phases[index]);
  }
  return result;
}

std::pair<std::vector<BinaryTemplate>, std::vector<Sequence>>
BuildTemplates(int maximum_degree) {
  Sequence binary_base{};
  Sequence zero_base{};
  int field_value = 1;
  for (int index = 0; index < kOrder; ++index) {
    binary_base[index] =
        static_cast<std::int8_t>(Character(field_value + 1));
    zero_base[index] =
        static_cast<std::int8_t>(Character(field_value - 1));
    field_value = 2 * field_value % kPrime;
  }
  if (field_value != 1 || RowSum(binary_base) != -1 ||
      RowSum(zero_base) != 0 ||
      std::count(zero_base.begin(), zero_base.end(), 0) != 1 ||
      zero_base[0] != 0) {
    throw std::runtime_error("base Sidelnikov data changed");
  }

  std::array<Sequence, kOrder> binary_phases{};
  for (int phase = 0; phase < kOrder; ++phase) {
    binary_phases[phase] = Shift(binary_base, phase);
  }

  std::set<std::vector<int>> canonical_subsets;
  for (int size = 0; size <= maximum_degree; ++size) {
    EnumerateSubsets(size, [&](const std::vector<int>& indices) {
      canonical_subsets.insert(CanonicalTranslate(indices));
    });
  }
  const std::size_t expected_binary =
      maximum_degree == 3 ? 1150 : maximum_degree == 4 ? 23'290 : 0;
  if (expected_binary == 0 ||
      canonical_subsets.size() != expected_binary) {
    throw std::runtime_error("binary translation quotient changed");
  }

  std::set<std::string> binary_sequences;
  std::vector<BinaryTemplate> binary;
  binary.reserve(canonical_subsets.size());
  for (const std::vector<int>& indices : canonical_subsets) {
    const Sequence sequence = ProductOfPhases(binary_phases, indices);
    if (!binary_sequences.insert(Encode(sequence)).second) {
      throw std::runtime_error("binary product collision");
    }
    binary.push_back(
        BinaryTemplate{sequence, PeriodicPaf(sequence), RowSum(sequence)});
  }

  Sequence zero_square = Multiply(zero_base, zero_base);
  std::set<std::string> zero_sequences;
  std::vector<Sequence> zero;
  for (int zero_power : {1, 2}) {
    const Sequence zero_factor =
        zero_power == 1 ? zero_base : zero_square;
    for (int size = 0; size <= maximum_degree - zero_power; ++size) {
      EnumerateSubsets(size, [&](const std::vector<int>& indices) {
        const Sequence sequence =
            Multiply(zero_factor, ProductOfPhases(binary_phases, indices));
        if (sequence[0] != 0 ||
            std::count(sequence.begin(), sequence.end(), 0) != 1) {
          throw std::runtime_error("one-zero product malformed");
        }
        if (!zero_sequences.insert(Encode(sequence)).second) {
          throw std::runtime_error("one-zero product collision");
        }
        zero.push_back(sequence);
      });
    }
  }
  const std::size_t expected_zero =
      maximum_degree == 3 ? 3571 : maximum_degree == 4 ? 98'855 : 0;
  if (zero.size() != expected_zero) {
    throw std::runtime_error("one-zero template count changed");
  }
  return {binary, zero};
}

std::map<int, PafSet> BuildOrdinaryPafCatalog(
    const std::vector<BinaryTemplate>& binary,
    bool independent_decimations) {
  std::map<int, PafSet> result;
  for (const BinaryTemplate& item : binary) {
    const int multiplier_limit =
        independent_decimations ? kOrder : 2;
    for (int multiplier = 1; multiplier < multiplier_limit; ++multiplier) {
      const Sequence sequence = Decimate(item.sequence, multiplier);
      result[std::abs(RowSum(sequence))].insert(PeriodicPaf(sequence));
    }
  }
  return result;
}

std::vector<Bits> BuildAffineStates(
    const std::vector<BinaryTemplate>& binary,
    bool independent_decimations) {
  std::vector<Bits> result;
  result.reserve(static_cast<std::size_t>(binary.size()) *
                 (independent_decimations ? kOrder - 1 : 1) * kOrder);
  for (const BinaryTemplate& item : binary) {
    const int multiplier_limit =
        independent_decimations ? kOrder : 2;
    for (int multiplier = 1; multiplier < multiplier_limit; ++multiplier) {
      for (int offset = 0; offset < kOrder; ++offset) {
        const Bits direct = AffineBits(item.sequence, multiplier, offset);
        const Bits opposite = ComplementBits(direct);
        result.push_back(std::min(direct, opposite));
      }
    }
  }
  std::sort(result.begin(), result.end());
  result.erase(std::unique(result.begin(), result.end()), result.end());
  return result;
}

std::map<std::uint64_t, std::vector<ZeroRepresentative>>
BuildZeroRepresentatives(const std::vector<Sequence>& zero) {
  std::map<std::uint64_t, std::vector<ZeroRepresentative>> result;
  std::set<std::tuple<std::uint64_t, int, Paf>> seen;
  for (const Sequence& sequence : zero) {
    const std::uint64_t orientation = Orientation(sequence);
    const int absolute_row_sum = std::abs(RowSum(sequence));
    const Paf paf = PeriodicPaf(sequence);
    if (seen.emplace(orientation, absolute_row_sum, paf).second) {
      result[orientation].push_back(
          ZeroRepresentative{sequence, paf, absolute_row_sum});
    }
  }
  return result;
}

bool HasPair(const Paf& needed, int residual,
             const std::map<int, PafSet>& ordinary) {
  for (const auto& [left_sum, left_pafs] : ordinary) {
    for (const auto& [right_sum, right_pafs] : ordinary) {
      if (left_sum > right_sum ||
          left_sum * left_sum + right_sum * right_sum != residual) {
        continue;
      }
      const PafSet* iterate = &left_pafs;
      const PafSet* lookup = &right_pafs;
      if (iterate->size() > lookup->size()) {
        std::swap(iterate, lookup);
      }
      for (const Paf& left : *iterate) {
        Paf right{};
        for (int index = 0; index < kHalf; ++index) {
          right[index] = static_cast<std::int16_t>(
              needed[index] - left[index]);
        }
        if (lookup->contains(right)) {
          return true;
        }
      }
    }
  }
  return false;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    bool degree_four_undecimated = false;
    if (argc == 2 && std::string(argv[1]) == "--degree4-undecimated") {
      degree_four_undecimated = true;
    } else if (argc != 1) {
      throw std::runtime_error(
          "usage: audit_independent_decimations "
          "[--degree4-undecimated]");
    }
    const int maximum_degree = degree_four_undecimated ? 4 : 3;
    const bool independent_decimations = !degree_four_undecimated;
    const auto [binary, zero] = BuildTemplates(maximum_degree);
    const std::map<int, PafSet> ordinary =
        BuildOrdinaryPafCatalog(binary, independent_decimations);
    const std::vector<Bits> affine =
        BuildAffineStates(binary, independent_decimations);
    const auto zero_by_orientation = BuildZeroRepresentatives(zero);

    if (!degree_four_undecimated) {
      const std::map<int, std::size_t> expected_paf_counts{
          {1, 4633}, {3, 3321}, {5, 3813}, {7, 3034}, {9, 2378},
          {11, 2706}, {13, 2296}, {15, 1312}, {17, 779}, {19, 533},
          {21, 205}, {23, 164}, {25, 82}, {83, 1}};
      if (ordinary.size() != expected_paf_counts.size()) {
        throw std::runtime_error("ordinary row-sum layer count changed");
      }
      for (const auto& [row_sum, expected] : expected_paf_counts) {
        if (!ordinary.contains(row_sum) ||
            ordinary.at(row_sum).size() != expected) {
          throw std::runtime_error("ordinary PAF catalog count changed");
        }
      }
      if (affine.size() != 3'910'048) {
        throw std::runtime_error(
            "binary affine sequence count changed: observed " +
            std::to_string(affine.size()));
      }
    }

    std::set<int> pair_norms;
    for (const auto& [left_sum, left_pafs] : ordinary) {
      (void)left_pafs;
      for (const auto& [right_sum, right_pafs] : ordinary) {
        (void)right_pafs;
        if (left_sum <= right_sum &&
            left_sum * left_sum + right_sum * right_sum <= kEnergy) {
          pair_norms.insert(
              left_sum * left_sum + right_sum * right_sum);
        }
      }
    }

    std::set<std::uint64_t> intersecting_fingerprints;
    std::uint64_t orientation_sum_states = 0;
    std::uint64_t row_compatible_states = 0;
    std::uint64_t exact_signature_hits = 0;
    std::map<int, std::uint64_t> residual_counts;
    std::map<int, PafSet> needed_by_residual;

    for (const Bits& v_bits : affine) {
      const std::uint64_t fingerprint = Orientation(v_bits);
      const auto found = zero_by_orientation.find(fingerprint);
      if (found == zero_by_orientation.end()) {
        continue;
      }
      intersecting_fingerprints.insert(fingerprint);
      const Sequence underlying = ToSequence(v_bits);
      const Paf underlying_paf = PeriodicPaf(underlying);
      const int underlying_sum = RowSum(v_bits);
      const int underlying_origin = Value(v_bits, 0);

      for (int sign : {-1, 1}) {
        const int origin = sign * underlying_origin;
        const int delta = 2 - origin;
        const int v_sum = sign * underlying_sum + delta;
        Paf v_paf{};
        for (int lag = 1; lag <= kHalf; ++lag) {
          const int correction =
              delta * sign *
              (Value(v_bits, lag) + Value(v_bits, kOrder - lag));
          v_paf[lag - 1] = static_cast<std::int16_t>(
              underlying_paf[lag - 1] + correction);
        }

        for (const ZeroRepresentative& u : found->second) {
          ++orientation_sum_states;
          const int residual =
              kEnergy - u.absolute_row_sum * u.absolute_row_sum -
              v_sum * v_sum;

          if (!pair_norms.contains(residual)) {
            continue;
          }
          ++row_compatible_states;
          ++residual_counts[residual];

          Paf needed{};
          for (int index = 0; index < kHalf; ++index) {
            needed[index] = static_cast<std::int16_t>(
                -u.paf[index] - v_paf[index]);
            if (Mod(needed[index], 4) != 2) {
              throw std::runtime_error(
                  "orientation-compatible state failed modulo four");
            }
          }
          if (degree_four_undecimated) {
            needed_by_residual[residual].insert(needed);
          } else if (HasPair(needed, residual, ordinary)) {
            ++exact_signature_hits;
            std::cout << "unexpected_exact_hit_fingerprint="
                      << fingerprint << '\n';
          }
        }
      }
    }

    if (degree_four_undecimated) {
      for (const auto& [residual, needed_set] : needed_by_residual) {
        std::cout << "degree4_needed_signatures_" << residual << '='
                  << needed_set.size() << '\n';
      }
      for (const auto& [residual, needed_set] : needed_by_residual) {
        for (const Paf& needed : needed_set) {
          if (HasPair(needed, residual, ordinary)) {
            ++exact_signature_hits;
            std::cout << "degree4_exact_hit_residual=" << residual
                      << '\n';
          }
        }
      }
    }

    if (degree_four_undecimated) {
      const std::map<int, std::uint64_t> expected_residual_counts{
          {10, 4514},  {74, 27107}, {90, 19444},
          {122, 17746}, {170, 29850}, {218, 38630},
          {234, 69868}, {298, 38324}, {314, 80352}};
      const std::map<int, std::size_t> expected_needed_counts{
          {10, 2257},  {74, 16183}, {90, 10823},
          {122, 9569}, {170, 16260}, {218, 21171},
          {234, 38023}, {298, 20638}, {314, 44297}};
      std::map<int, std::size_t> observed_needed_counts;
      for (const auto& [residual, needed_set] : needed_by_residual) {
        observed_needed_counts[residual] = needed_set.size();
      }
      if (affine.size() != 1'932'988 ||
          intersecting_fingerprints.size() != 862 ||
          orientation_sum_states != 642'560 ||
          row_compatible_states != 325'835 ||
          residual_counts != expected_residual_counts ||
          observed_needed_counts != expected_needed_counts ||
          exact_signature_hits != 0) {
        throw std::runtime_error(
            "undecimated degree-four enumeration fingerprint changed");
      }
    } else {
      const std::map<int, std::uint64_t> expected_residual_counts{
          {10, 182}, {74, 1017}, {234, 686}, {298, 862}, {314, 2687}};
      if (intersecting_fingerprints.size() != 42 ||
          orientation_sum_states != 20'504 ||
          row_compatible_states != 5'434 ||
          residual_counts != expected_residual_counts ||
          exact_signature_hits != 0) {
        throw std::runtime_error(
            "independent-decimation degree-three enumeration fingerprint "
            "changed");
      }
    }

    std::size_t ordinary_paf_states = 0;
    for (const auto& [row_sum, pafs] : ordinary) {
      (void)row_sum;
      ordinary_paf_states += pafs.size();
    }
    if (degree_four_undecimated && ordinary_paf_states != 12'097) {
      throw std::runtime_error(
          "undecimated degree-four ordinary PAF catalog changed");
    }

    std::cout << "family="
              << (degree_four_undecimated
                      ? "undecimated_degree_at_most_four_"
                        "sidelnikov_products"
                      : "independently_decimated_degree_at_most_three_"
                        "sidelnikov_products")
              << '\n';
    std::cout << "binary_translation_templates=" << binary.size() << '\n';
    std::cout << "one_zero_anchored_templates=" << zero.size() << '\n';
    std::cout << "binary_affine_sequences=" << affine.size() << '\n';
    std::cout << "ordinary_norm_paf_states=" << ordinary_paf_states << '\n';
    std::cout << "intersecting_orientation_fingerprints="
              << intersecting_fingerprints.size() << '\n';
    std::cout << "orientation_sum_states=" << orientation_sum_states << '\n';
    std::cout << "row_compatible_uv_states=" << row_compatible_states << '\n';
    std::cout << "exact_cd_signature_hits=" << exact_signature_hits << '\n';
    std::cout << "prime_fold_objects="
              << (exact_signature_hits == 0 ? 0 : -1) << '\n';
    std::cout << "mod84_lifts_tested=0\n";
    std::cout << "hadamard_candidates=0\n";
    std::cout << "residual_norm_distribution=";
    bool first = true;
    for (const auto& [norm, count] : residual_counts) {
      std::cout << (first ? "" : ",") << norm << ':' << count;
      first = false;
    }
    std::cout << '\n';
    if (degree_four_undecimated) {
      std::cout << "PASS exact undecimated degree-four exclusion\n";
    } else {
      std::cout
          << "PASS exact independent-decimation degree-three exclusion\n";
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error=" << error.what() << '\n';
    return 1;
  }
}
