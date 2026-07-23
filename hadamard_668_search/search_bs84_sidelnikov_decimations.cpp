// Exact independent-decimation join for the prime-83 Sidelnikov fold.
//
// This is a finite character construction, not a search over arbitrary signs.
// It extends check_bs84_sidelnikov_fold.py by allowing each degree-at-most-two
// character template to have its own multiplier in (Z/83Z)^*.  A common
// multiplier is a symmetry of every equation, so the multiplier of U is
// normalized to one.  Reversal identifies d and -d for the remaining PAFs.
//
// Build:
//   c++ -O3 -std=c++20 -o search_bs84_sidelnikov_decimations \
//       search_bs84_sidelnikov_decimations.cpp
//
// The program stores full 41-coordinate signatures and uses lexicographic
// comparison.  Hash collisions therefore play no role in the result.

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
#include <utility>
#include <vector>

namespace {

constexpr int kFieldPrime = 167;
constexpr int kOrder = 83;
constexpr int kHalf = 41;
constexpr int kEnergy = 334;

using Sequence = std::array<std::int8_t, kOrder>;
using Paf = std::array<std::int16_t, kHalf>;

struct Template {
  std::string kind;
  int parameter = -1;
  Sequence sequence{};
  Paf paf{};
  int row_sum = 0;
};

struct Signature {
  int row_norm = 0;
  Paf paf{};

  auto operator<=>(const Signature&) const = default;
};

struct DecimatedTemplate {
  Template base;
  int multiplier = 1;
  Sequence sequence{};
  Paf paf{};
  int row_sum = 0;
  int row_norm = 0;
};

struct PairRecord {
  std::uint16_t row_norm = 0;
  Paf paf{};
  std::uint16_t left = 0;
  std::uint16_t right = 0;
};

struct PairKey {
  int row_norm = 0;
  Paf paf{};
};

bool KeyLess(int left_norm, const Paf& left_paf, int right_norm,
             const Paf& right_paf) {
  if (left_norm != right_norm) {
    return left_norm < right_norm;
  }
  return left_paf < right_paf;
}

struct PairRecordLess {
  bool operator()(const PairRecord& left, const PairRecord& right) const {
    return KeyLess(left.row_norm, left.paf, right.row_norm, right.paf);
  }
  bool operator()(const PairRecord& left, const PairKey& right) const {
    return KeyLess(left.row_norm, left.paf, right.row_norm, right.paf);
  }
  bool operator()(const PairKey& left, const PairRecord& right) const {
    return KeyLess(left.row_norm, left.paf, right.row_norm, right.paf);
  }
};

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
  value = Mod(value, kFieldPrime);
  if (value == 0) {
    return 0;
  }
  return PowerMod(value, (kFieldPrime - 1) / 2, kFieldPrime) == 1 ? 1 : -1;
}

Sequence Sidelnikov(int parameter) {
  Sequence result{};
  int value = 1;
  for (int index = 0; index < kOrder; ++index) {
    result[index] = static_cast<std::int8_t>(Character(value + parameter));
    value = 2 * value % kFieldPrime;
  }
  return result;
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

Paf DecimatePaf(const Paf& paf, int multiplier) {
  Paf result{};
  for (int lag = 1; lag <= kHalf; ++lag) {
    int oriented = Mod(multiplier * lag, kOrder);
    int unoriented = std::min(oriented, kOrder - oriented);
    result[lag - 1] = paf[unoriented - 1];
  }
  return result;
}

int RowSum(const Sequence& sequence) {
  return std::accumulate(sequence.begin(), sequence.end(), 0);
}

std::uint64_t OrientationSignature(const Sequence& sequence) {
  if (sequence[0] == 0) {
    for (int index = 1; index < kOrder; ++index) {
      if (sequence[index] == 0) {
        throw std::runtime_error("one-zero orientation sequence malformed");
      }
    }
  }
  std::uint64_t result = 0;
  for (int lag = 1; lag <= kHalf; ++lag) {
    if (sequence[lag] == sequence[kOrder - lag]) {
      result |= std::uint64_t{1} << (lag - 1);
    }
  }
  return result;
}

Template MakeTemplate(std::string kind, int parameter,
                      const Sequence& sequence) {
  return Template{std::move(kind), parameter, sequence, PeriodicPaf(sequence),
                  RowSum(sequence)};
}

std::pair<std::vector<Template>, std::vector<Template>> RawLibraries() {
  const Sequence binary_base = Sidelnikov(1);
  const Sequence zero_base = Sidelnikov(-1);
  std::vector<Template> binary;
  std::vector<Template> zero;
  binary.push_back(MakeTemplate("B", -1, binary_base));
  zero.push_back(MakeTemplate("Z", -1, zero_base));

  Sequence zero_squared{};
  for (int index = 0; index < kOrder; ++index) {
    zero_squared[index] =
        static_cast<std::int8_t>(zero_base[index] * zero_base[index]);
  }
  zero.push_back(MakeTemplate("Z2", -1, zero_squared));

  for (int phase = 0; phase < kOrder; ++phase) {
    const Sequence translated = Shift(binary_base, phase);
    Sequence binary_product{};
    Sequence zero_product{};
    for (int index = 0; index < kOrder; ++index) {
      binary_product[index] = static_cast<std::int8_t>(
          binary_base[index] * translated[index]);
      zero_product[index] =
          static_cast<std::int8_t>(zero_base[index] * translated[index]);
    }
    binary.push_back(MakeTemplate("BB", phase, binary_product));
    zero.push_back(MakeTemplate("ZB", phase, zero_product));
  }
  if (binary.size() != 84 || zero.size() != 85) {
    throw std::runtime_error("raw library size changed");
  }
  return {binary, zero};
}

std::vector<Template> SignatureRepresentatives(
    const std::vector<Template>& raw) {
  std::map<Signature, Template> representatives;
  for (const Template& item : raw) {
    const Signature key{item.row_sum * item.row_sum, item.paf};
    representatives.try_emplace(key, item);
  }
  std::vector<Template> result;
  result.reserve(representatives.size());
  for (const auto& [key, item] : representatives) {
    (void)key;
    result.push_back(item);
  }
  return result;
}

std::vector<DecimatedTemplate> DecimatedCatalog(
    const std::vector<Template>& bases) {
  std::map<Signature, DecimatedTemplate> catalog;
  for (const Template& base : bases) {
    for (int multiplier = 1; multiplier <= kHalf; ++multiplier) {
      const Sequence sequence = Decimate(base.sequence, multiplier);
      const Paf paf = DecimatePaf(base.paf, multiplier);
      if (PeriodicPaf(sequence) != paf) {
        throw std::runtime_error("decimated PAF permutation failed");
      }
      const int row_sum = RowSum(sequence);
      const Signature key{row_sum * row_sum, paf};
      catalog.try_emplace(
          key, DecimatedTemplate{base, multiplier, sequence, paf, row_sum,
                                 row_sum * row_sum});
    }
  }
  std::vector<DecimatedTemplate> result;
  result.reserve(catalog.size());
  for (const auto& [key, item] : catalog) {
    (void)key;
    result.push_back(item);
  }
  return result;
}

std::vector<PairRecord> BuildPairRecords(
    const std::vector<DecimatedTemplate>& binary) {
  std::vector<PairRecord> records;
  const std::size_t count = binary.size();
  records.reserve(count * (count + 1) / 2);
  for (std::size_t left = 0; left < count; ++left) {
    for (std::size_t right = left; right < count; ++right) {
      const int row_norm = binary[left].row_norm + binary[right].row_norm;
      if (row_norm > kEnergy) {
        continue;
      }
      PairRecord record;
      record.row_norm = static_cast<std::uint16_t>(row_norm);
      record.left = static_cast<std::uint16_t>(left);
      record.right = static_cast<std::uint16_t>(right);
      for (int index = 0; index < kHalf; ++index) {
        record.paf[index] = static_cast<std::int16_t>(
            binary[left].paf[index] + binary[right].paf[index]);
      }
      records.push_back(record);
    }
  }
  std::sort(records.begin(), records.end(), PairRecordLess{});
  return records;
}

struct Match {
  int u_index = 0;
  int v_index = 0;
  int phase = 0;
  int sign = 1;
  int c_index = 0;
  int d_index = 0;
};

void PrintTemplate(const char* label, const DecimatedTemplate& item) {
  std::cout << label << "_kind=" << item.base.kind << '\n';
  std::cout << label << "_parameter=" << item.base.parameter << '\n';
  std::cout << label << "_multiplier=" << item.multiplier << '\n';
  std::cout << label << "_row_sum=" << item.row_sum << '\n';
}

}  // namespace

int main() {
  try {
    const auto [binary_raw, zero_raw] = RawLibraries();
    const std::vector<Template> binary_bases =
        SignatureRepresentatives(binary_raw);
    const std::vector<Template> zero_bases =
        SignatureRepresentatives(zero_raw);
    if (binary_bases.size() != 43 || zero_bases.size() != 44) {
      throw std::runtime_error("base signature count changed");
    }

    const std::vector<DecimatedTemplate> binary =
        DecimatedCatalog(binary_bases);
    const std::vector<DecimatedTemplate> zero =
        DecimatedCatalog(zero_bases);
    if (binary.size() != 1723 || zero.size() != 1723) {
      throw std::runtime_error("decimated signature count changed");
    }

    std::set<std::uint64_t> u_orientation_signatures;
    std::set<std::uint64_t> v_orientation_signatures;
    std::map<std::uint64_t, std::uint64_t> u_orientation_counts;
    std::map<std::uint64_t, std::uint64_t> v_orientation_counts;
    for (const Template& u : zero_bases) {
      const std::uint64_t signature = OrientationSignature(u.sequence);
      u_orientation_signatures.insert(signature);
      ++u_orientation_counts[signature];
    }
    for (const DecimatedTemplate& v : binary) {
      for (int phase = 0; phase < kOrder; ++phase) {
        const std::uint64_t signature =
            OrientationSignature(Shift(v.sequence, phase));
        v_orientation_signatures.insert(signature);
        ++v_orientation_counts[signature];
      }
    }
    std::size_t orientation_intersection = 0;
    std::uint64_t oriented_uv_states = 0;
    int minimum_orientation_distance = kHalf + 1;
    std::uint64_t minimum_orientation_pairs = 0;
    for (const std::uint64_t u : u_orientation_signatures) {
      orientation_intersection += v_orientation_signatures.contains(u);
      oriented_uv_states +=
          2 * u_orientation_counts[u] * v_orientation_counts[u];
      for (const std::uint64_t v : v_orientation_signatures) {
        const int distance = std::popcount(u ^ v);
        if (distance < minimum_orientation_distance) {
          minimum_orientation_distance = distance;
          minimum_orientation_pairs = 1;
        } else if (distance == minimum_orientation_distance) {
          ++minimum_orientation_pairs;
        }
      }
    }

    const std::vector<PairRecord> pairs = BuildPairRecords(binary);
    const std::uint64_t all_pair_states =
        static_cast<std::uint64_t>(binary.size()) * (binary.size() + 1) / 2;
    std::size_t distinct_pair_keys = 0;
    std::set<int> pair_norms;
    for (std::size_t index = 0; index < pairs.size();) {
      ++distinct_pair_keys;
      pair_norms.insert(pairs[index].row_norm);
      std::size_t next = index + 1;
      while (next < pairs.size() &&
             !PairRecordLess{}(pairs[index], pairs[next]) &&
             !PairRecordLess{}(pairs[next], pairs[index])) {
        ++next;
      }
      index = next;
    }

    std::uint64_t uv_states = 0;
    std::uint64_t row_compatible = 0;
    std::uint64_t parity_compatible = 0;
    std::uint64_t uv_signature_hits = 0;
    std::uint64_t matches = 0;
    std::map<int, std::uint64_t> remainder_distribution;
    std::vector<Match> first_matches;

    // A common decimation normalizes U's multiplier to one.  U therefore
    // ranges over the 44 base signatures, while V,C,D use their complete
    // independent relative-decimation catalogs.
    for (std::size_t u_index = 0; u_index < zero_bases.size(); ++u_index) {
      const Template& u = zero_bases[u_index];
      const int u_norm = u.row_sum * u.row_sum;
      for (std::size_t v_index = 0; v_index < binary.size(); ++v_index) {
        const DecimatedTemplate& v_base = binary[v_index];
        for (int phase = 0; phase < kOrder; ++phase) {
          const Sequence translated = Shift(v_base.sequence, phase);
          for (int sign : {-1, 1}) {
            ++uv_states;
            const int origin = sign * static_cast<int>(translated[0]);
            const int delta = 2 - origin;
            const int v_sum = sign * v_base.row_sum + delta;
            const int remaining_norm =
                kEnergy - u_norm - v_sum * v_sum;
            if (!pair_norms.contains(remaining_norm)) {
              continue;
            }
            ++row_compatible;
            remainder_distribution[remaining_norm] += 1;

            Paf needed{};
            bool parity_ok = true;
            for (int lag = 1; lag <= kHalf; ++lag) {
              const int correction =
                  delta * sign *
                  (static_cast<int>(translated[lag]) +
                   static_cast<int>(translated[kOrder - lag]));
              const int v_paf = v_base.paf[lag - 1] + correction;
              needed[lag - 1] =
                  static_cast<std::int16_t>(-u.paf[lag - 1] - v_paf);
              if (Mod(needed[lag - 1], 4) != 2) {
                parity_ok = false;
              }
            }
            if (parity_ok) {
              ++parity_compatible;
            }
            const PairKey key{remaining_norm, needed};
            const auto lower =
                std::lower_bound(pairs.begin(), pairs.end(), key,
                                 PairRecordLess{});
            const auto upper =
                std::upper_bound(lower, pairs.end(), key, PairRecordLess{});
            if (lower == upper) {
              continue;
            }
            ++uv_signature_hits;
            const std::uint64_t multiplicity =
                static_cast<std::uint64_t>(upper - lower);
            matches += multiplicity;
            for (auto iterator = lower;
                 iterator != upper && first_matches.size() < 32; ++iterator) {
              first_matches.push_back(
                  Match{static_cast<int>(u_index),
                        static_cast<int>(v_index), phase, sign, iterator->left,
                        iterator->right});
            }
          }
        }
      }
    }

    const std::uint64_t expected_uv =
        static_cast<std::uint64_t>(zero_bases.size()) * binary.size() *
        kOrder * 2;
    if (uv_states != expected_uv) {
      throw std::runtime_error("U/V state count changed");
    }
    const std::uint64_t all_symmetric =
        (std::uint64_t{1} << kHalf) - 1;
    int all_symmetric_u_templates = 0;
    for (const Template& u : zero_bases) {
      if (OrientationSignature(u.sequence) == all_symmetric) {
        ++all_symmetric_u_templates;
        if (u.kind != "Z2" || u.row_sum != 82) {
          throw std::runtime_error(
              "the common orientation fingerprint changed");
        }
      }
    }
    const std::map<int, std::uint64_t> expected_remainders{
        {74, 64'575},  {90, 135'669}, {122, 72'324},
        {170, 239'112}, {218, 351'657}};
    if (u_orientation_signatures.size() != 43 ||
        v_orientation_signatures.size() != 35'302 ||
        orientation_intersection != 1 || all_symmetric_u_templates != 1 ||
        oriented_uv_states != 3'610 || all_pair_states != 1'485'226 ||
        pairs.size() != 1'475'877 ||
        distinct_pair_keys != 1'475'877 ||
        row_compatible != 863'337 || parity_compatible != 0 ||
        uv_signature_hits != 0 || matches != 0 ||
        remainder_distribution != expected_remainders) {
      throw std::runtime_error(
          "independent-decimation enumeration fingerprint changed");
    }

    std::cout << "binary_base_signatures=" << binary_bases.size() << '\n';
    std::cout << "zero_base_signatures=" << zero_bases.size() << '\n';
    std::cout << "binary_decimated_signatures=" << binary.size() << '\n';
    std::cout << "zero_decimated_signatures=" << zero.size() << '\n';
    std::cout << "u_orientation_signatures="
              << u_orientation_signatures.size() << '\n';
    std::cout << "v_orientation_signatures="
              << v_orientation_signatures.size() << '\n';
    std::cout << "orientation_signature_intersection="
              << orientation_intersection << '\n';
    std::cout << "minimum_orientation_distance="
              << minimum_orientation_distance << '\n';
    std::cout << "minimum_orientation_pairs="
              << minimum_orientation_pairs << '\n';
    std::cout << "uv_states_mod4_compatible_before_row_norm="
              << oriented_uv_states << '\n';
    std::cout << "cd_pair_states_all=" << all_pair_states << '\n';
    std::cout << "cd_pair_states_norm_admissible=" << pairs.size() << '\n';
    std::cout << "cd_distinct_pair_keys=" << distinct_pair_keys << '\n';
    std::cout << "uv_states_common_decimation_quotient=" << uv_states << '\n';
    std::cout << "uv_states_row_compatible=" << row_compatible << '\n';
    std::cout << "uv_states_mod4_compatible=" << parity_compatible << '\n';
    std::cout << "uv_states_with_signature_join=" << uv_signature_hits << '\n';
    std::cout << "prime_fold_objects=" << matches << '\n';
    std::cout << "mod84_lifts_tested=0\n";
    std::cout << "hadamard_candidates=0\n";
    std::cout << "remainder_norm_distribution=";
    bool first = true;
    for (const auto& [norm, count] : remainder_distribution) {
      if (!first) {
        std::cout << ',';
      }
      first = false;
      std::cout << norm << ':' << count;
    }
    std::cout << '\n';

    for (std::size_t index = 0; index < first_matches.size(); ++index) {
      const Match& match = first_matches[index];
      std::cout << "match_index=" << index << '\n';
      const DecimatedTemplate u{
          zero_bases[match.u_index], 1, zero_bases[match.u_index].sequence,
          zero_bases[match.u_index].paf, zero_bases[match.u_index].row_sum,
          zero_bases[match.u_index].row_sum *
              zero_bases[match.u_index].row_sum};
      PrintTemplate("u", u);
      PrintTemplate("v", binary[match.v_index]);
      std::cout << "v_phase=" << match.phase << '\n';
      std::cout << "v_sign=" << match.sign << '\n';
      PrintTemplate("c", binary[match.c_index]);
      PrintTemplate("d", binary[match.d_index]);
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error=" << error.what() << '\n';
    return 1;
  }
}
