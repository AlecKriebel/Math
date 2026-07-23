// Algebraic two-MUB packing search for the five-comb carrier system.
//
// Four binary length-five words form a complementary quartet.  Polarizing
// them across distance 42 gives eight carrier types; four copies of every
// type provide the required 32 channels.  One carrier type is assigned to
// each of the eight disjoint shifts, and all four copies occupy that slot
// across the four target rows.
//
// The four signs in a slot are one projective {+1,-1}^4 column.  The eight
// projective columns split into two mutually unbiased H4 bases.  This program
// derives every bijection of those eight columns to the eight slots that
// survives the exact modulo-four hole quotient.  It then exhausts affine
// carrier-type bijections, affine slot signs, and every hole assignment in
// each surviving modulo-four fiber.
//
// This is a finite group-labeling construction, not a search over the 334
// unconstrained signs.
//
// Build:
//   c++ -O3 -std=c++20 -o search_five_comb_mub_quartet \
//       search_five_comb_mub_quartet.cpp
//
// By default quartet 0 is searched.  Pass an integer 0..47 to select another
// normalized complementary-quartet multiset.

#include <algorithm>
#include <array>
#include <bit>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int kRows = 4;
constexpr int kSlots = 8;
constexpr int kLengthLong = 84;
constexpr int kLengthShort = 83;
constexpr int kLags = 83;
constexpr int kHoleVariables = 14;

using Word = std::array<std::int8_t, 5>;
using Quartet = std::array<int, 4>;
using Vector4 = std::array<std::int8_t, 4>;
using ProjectiveLabels = std::array<int, kSlots>;
using Syndrome = std::bitset<kLags>;

struct Bits {
  std::uint64_t low = 0;
  std::uint64_t high = 0;
};

struct LinearMap {
  int image0 = 0;
  int image1 = 0;
  int image2 = 0;
};

struct ProjectiveMap {
  ProjectiveLabels labels{};
  bool affine = false;
  std::vector<std::uint16_t> hole_masks;
};

int Parity(int value) {
  return std::popcount(static_cast<unsigned int>(value)) & 1;
}

int Apply(const LinearMap& map, int value) {
  return ((value & 1) ? map.image0 : 0) ^
         ((value & 2) ? map.image1 : 0) ^
         ((value & 4) ? map.image2 : 0);
}

int AffineBit(int mask, int value) {
  return Parity((mask & 7) & value);
}

void SetBit(Bits& bits, int position) {
  if (position < 64) {
    bits.low |= std::uint64_t{1} << position;
  } else {
    bits.high |= std::uint64_t{1} << (position - 64);
  }
}

Bits ShiftRight(Bits bits, int amount) {
  if (amount == 0) {
    return bits;
  }
  if (amount < 64) {
    return Bits{(bits.low >> amount) | (bits.high << (64 - amount)),
                bits.high >> amount};
  }
  return Bits{bits.high >> (amount - 64), 0};
}

Bits Xor(Bits left, Bits right) {
  return Bits{left.low ^ right.low, left.high ^ right.high};
}

int PopcountPrefix(Bits bits, int length) {
  if (length <= 0) {
    return 0;
  }
  if (length < 64) {
    return std::popcount(bits.low & ((std::uint64_t{1} << length) - 1));
  }
  if (length == 64) {
    return std::popcount(bits.low);
  }
  const int high_length = length - 64;
  const std::uint64_t high_mask =
      high_length == 64
          ? ~std::uint64_t{0}
          : ((std::uint64_t{1} << high_length) - 1);
  return std::popcount(bits.low) + std::popcount(bits.high & high_mask);
}

int Correlation(const std::array<Bits, kRows>& rows, int lag) {
  int distance = 0;
  int term_count = 0;
  for (int row = 0; row < kRows; ++row) {
    const int length = row < 2 ? kLengthLong : kLengthShort;
    if (lag >= length) {
      continue;
    }
    const int terms = length - lag;
    distance +=
        PopcountPrefix(Xor(rows[row], ShiftRight(rows[row], lag)), terms);
    term_count += terms;
  }
  return term_count - 2 * distance;
}

int SquaredRowSumNorm(const std::array<Bits, kRows>& rows) {
  int result = 0;
  for (int row = 0; row < kRows; ++row) {
    const int length = row < 2 ? kLengthLong : kLengthShort;
    const int negatives = PopcountPrefix(rows[row], length);
    const int row_sum = length - 2 * negatives;
    result += row_sum * row_sum;
  }
  return result;
}

std::vector<LinearMap> GeneralLinear3() {
  std::vector<LinearMap> result;
  for (int first = 1; first < 8; ++first) {
    for (int second = 1; second < 8; ++second) {
      if (second == first) {
        continue;
      }
      for (int third = 1; third < 8; ++third) {
        if (third == first || third == second ||
            third == (first ^ second)) {
          continue;
        }
        result.push_back(LinearMap{first, second, third});
      }
    }
  }
  if (result.size() != 168) {
    throw std::runtime_error("GL(3,2) size changed");
  }
  return result;
}

std::array<Vector4, 8> ProjectiveVectors() {
  constexpr int hadamard[4][4] = {
      {1, 1, 1, 1},
      {1, -1, 1, -1},
      {1, 1, -1, -1},
      {1, -1, -1, 1},
  };
  constexpr int twist[4] = {1, 1, 1, -1};
  std::array<Vector4, 8> result{};
  for (int basis = 0; basis < 2; ++basis) {
    for (int column = 0; column < 4; ++column) {
      for (int row = 0; row < 4; ++row) {
        result[4 * basis + column][row] = static_cast<std::int8_t>(
            hadamard[row][column] * (basis ? twist[row] : 1));
      }
    }
  }
  for (int left = 0; left < 8; ++left) {
    for (int right = 0; right < 8; ++right) {
      int inner = 0;
      for (int row = 0; row < 4; ++row) {
        inner += result[left][row] * result[right][row];
      }
      if ((left / 4 == right / 4 && left != right && inner != 0) ||
          (left / 4 != right / 4 && std::abs(inner) != 2)) {
        throw std::runtime_error("two-MUB vector geometry failed");
      }
    }
  }
  return result;
}

std::vector<Word> NormalizedWords() {
  std::vector<Word> result;
  for (int mask = 0; mask < 16; ++mask) {
    Word word{};
    word[0] = 1;
    for (int index = 1; index < 5; ++index) {
      // Match itertools.product((-1, 1), repeat=4): the last coordinate
      // changes fastest.
      word[index] = ((mask >> (4 - index)) & 1) ? 1 : -1;
    }
    result.push_back(word);
  }
  return result;
}

std::array<int, 4> WordSignature(const Word& word) {
  std::array<int, 4> result{};
  for (int lag = 1; lag < 5; ++lag) {
    for (int index = 0; index + lag < 5; ++index) {
      result[lag - 1] += word[index] * word[index + lag];
    }
  }
  return result;
}

std::vector<Quartet> ComplementaryQuartets(
    const std::vector<Word>& words) {
  std::array<std::array<int, 4>, 16> signatures{};
  for (int index = 0; index < 16; ++index) {
    signatures[index] = WordSignature(words[index]);
  }
  std::vector<Quartet> result;
  for (int a = 0; a < 16; ++a) {
    for (int b = a; b < 16; ++b) {
      for (int c = b; c < 16; ++c) {
        for (int d = c; d < 16; ++d) {
          bool flat = true;
          for (int lag = 0; lag < 4; ++lag) {
            flat &= signatures[a][lag] + signatures[b][lag] +
                        signatures[c][lag] + signatures[d][lag] ==
                    0;
          }
          if (flat) {
            result.push_back(Quartet{a, b, c, d});
          }
        }
      }
    }
  }
  if (result.size() != 48) {
    throw std::runtime_error("normalized complementary-quartet count changed");
  }
  return result;
}

constexpr std::array<int, 8> kSlotShifts = {0, 1, 2, 3, 20, 21, 22, 23};

constexpr std::array<std::pair<int, int>, kHoleVariables> kHolePositions = {
    std::pair{0, 40}, std::pair{0, 41}, std::pair{0, 82},
    std::pair{0, 83}, std::pair{1, 40}, std::pair{1, 41},
    std::pair{1, 82}, std::pair{1, 83}, std::pair{2, 40},
    std::pair{2, 41}, std::pair{2, 82}, std::pair{3, 40},
    std::pair{3, 41}, std::pair{3, 82}};

std::array<Bits, kRows> AddHoles(std::array<Bits, kRows> rows,
                                std::uint16_t hole_mask) {
  for (int variable = 0; variable < kHoleVariables; ++variable) {
    if ((hole_mask >> variable) & 1) {
      SetBit(rows[kHolePositions[variable].first],
             kHolePositions[variable].second);
    }
  }
  return rows;
}

std::array<Bits, kRows> ProjectiveCarrierRows(
    const ProjectiveLabels& labels,
    const std::array<Vector4, 8>& vectors) {
  std::array<Bits, kRows> rows{};
  for (int slot = 0; slot < kSlots; ++slot) {
    const Vector4& vector = vectors[labels[slot]];
    const int shift = kSlotShifts[slot];
    for (int tooth = 0; tooth < 5; ++tooth) {
      for (int row = 0; row < kRows; ++row) {
        if (vector[row] < 0) {
          SetBit(rows[row], shift + 4 * tooth);
          SetBit(rows[row], shift + 42 + 4 * tooth);
        }
      }
    }
  }
  return rows;
}

Syndrome HoleIncidence(int row, int position) {
  Syndrome result;
  const int length = row < 2 ? kLengthLong : kLengthShort;
  for (int lag = 1; lag <= kLags; ++lag) {
    if ((position + lag < length) != (position >= lag)) {
      result.set(lag - 1);
    }
  }
  return result;
}

std::pair<std::array<Syndrome, kLags>, int> HoleSyndromeBasis() {
  std::array<Syndrome, kLags> basis{};
  int rank = 0;
  for (const auto [row, position] : kHolePositions) {
    Syndrome vector = HoleIncidence(row, position);
    for (int pivot = kLags - 1; pivot >= 0; --pivot) {
      if (!vector.test(pivot)) {
        continue;
      }
      if (basis[pivot].none()) {
        basis[pivot] = vector;
        ++rank;
        break;
      }
      vector ^= basis[pivot];
    }
  }
  return {basis, rank};
}

Syndrome ReduceSyndrome(
    Syndrome vector, const std::array<Syndrome, kLags>& basis) {
  for (int pivot = kLags - 1; pivot >= 0; --pivot) {
    if (vector.test(pivot) && basis[pivot].any()) {
      vector ^= basis[pivot];
    }
  }
  return vector;
}

Syndrome Mod4Defect(const std::array<Bits, kRows>& rows) {
  Syndrome result;
  for (int lag = 1; lag <= kLags; ++lag) {
    // Every correlation is even.  Its residue is 2 exactly when one hole
    // parity toggle is required at this lag.
    if (Correlation(rows, lag) % 4 != 0) {
      result.set(lag - 1);
    }
  }
  return result;
}

std::vector<std::uint16_t> Mod4HoleFiber(
    const std::array<Bits, kRows>& projective_rows) {
  std::vector<std::uint16_t> result;
  for (int mask = 0; mask < (1 << kHoleVariables); ++mask) {
    const auto rows =
        AddHoles(projective_rows, static_cast<std::uint16_t>(mask));
    bool valid = true;
    for (int lag = 1; lag <= kLags; ++lag) {
      if (Correlation(rows, lag) % 4 != 0) {
        valid = false;
        break;
      }
    }
    if (valid) {
      result.push_back(static_cast<std::uint16_t>(mask));
    }
  }
  return result;
}

bool IsAffineLabeling(const ProjectiveLabels& labels) {
  const int translation = labels[0];
  const LinearMap linear{labels[1] ^ translation,
                         labels[2] ^ translation,
                         labels[4] ^ translation};
  for (int slot = 0; slot < kSlots; ++slot) {
    if ((Apply(linear, slot) ^ translation) != labels[slot]) {
      return false;
    }
  }
  return true;
}

ProjectiveLabels CanonicalRowSignRepresentative(
    const ProjectiveLabels& labels) {
  ProjectiveLabels canonical = labels;
  for (int translation = 1; translation < 8; ++translation) {
    ProjectiveLabels candidate{};
    for (int slot = 0; slot < kSlots; ++slot) {
      candidate[slot] = labels[slot] ^ translation;
    }
    canonical = std::min(canonical, candidate);
  }
  return canonical;
}

std::vector<ProjectiveMap> AdmissibleProjectiveMaps(
    const std::array<Vector4, 8>& vectors) {
  const auto [hole_basis, hole_rank] = HoleSyndromeBasis();
  if (hole_rank != 6) {
    throw std::runtime_error("hole syndrome rank changed");
  }

  // Enumerate all 8! bijections, then divide by the free action that XORs
  // every label by one fixed vector.  Since projective vectors multiply
  // according to label XOR, this action is exactly independent row
  // negation, with the corresponding hole signs carried by the full fiber.
  ProjectiveLabels labels{0, 1, 2, 3, 4, 5, 6, 7};
  std::set<ProjectiveLabels> representatives;
  int survivors = 0;
  int affine_survivors = 0;
  do {
    const auto rows = ProjectiveCarrierRows(labels, vectors);
    if (ReduceSyndrome(Mod4Defect(rows), hole_basis).any()) {
      continue;
    }
    ++survivors;
    affine_survivors += IsAffineLabeling(labels);
    representatives.insert(CanonicalRowSignRepresentative(labels));
  } while (std::next_permutation(labels.begin(), labels.end()));

  if (survivors != 64 || affine_survivors != 32 ||
      representatives.size() != 8) {
    throw std::runtime_error("projective modulo-four bijection count changed");
  }

  std::vector<ProjectiveMap> result;
  int affine_representatives = 0;
  for (const ProjectiveLabels& representative : representatives) {
    const bool affine = IsAffineLabeling(representative);
    affine_representatives += affine;
    const auto rows = ProjectiveCarrierRows(representative, vectors);
    auto fiber = Mod4HoleFiber(rows);
    if (fiber.size() != 256) {
      throw std::runtime_error("projective modulo-four fiber changed");
    }
    result.push_back(
        ProjectiveMap{representative, affine, std::move(fiber)});
  }
  if (result.size() != 8 || affine_representatives != 4) {
    throw std::runtime_error("admissible projective-map count changed");
  }
  return result;
}

std::array<Bits, kRows> BuildCarrierRows(
    const Quartet& quartet, const std::vector<Word>& words,
    const ProjectiveMap& projective, const LinearMap& type_map,
    int type_translation, int sign_character,
    const std::array<Vector4, 8>& vectors) {
  std::array<Bits, kRows> rows{};
  for (int slot = 0; slot < kSlots; ++slot) {
    const int type = Apply(type_map, slot) ^ type_translation;
    const int word_index = quartet[type & 3];
    const int polarization = (type & 4) ? -1 : 1;
    const int projective_label = projective.labels[slot];
    const Vector4& vector = vectors[projective_label];
    const int scalar = AffineBit(sign_character, slot) ? -1 : 1;
    const int shift = kSlotShifts[slot];
    for (int tooth = 0; tooth < 5; ++tooth) {
      const int first = scalar * words[word_index][tooth];
      const int second = polarization * first;
      for (int row = 0; row < kRows; ++row) {
        if (first * vector[row] < 0) {
          SetBit(rows[row], shift + 4 * tooth);
        }
        if (second * vector[row] < 0) {
          SetBit(rows[row], shift + 42 + 4 * tooth);
        }
      }
    }
  }
  return rows;
}

std::string SignString(Bits bits, int length) {
  std::string result;
  result.reserve(length);
  for (int index = 0; index < length; ++index) {
    const bool negative =
        index < 64 ? ((bits.low >> index) & 1)
                   : ((bits.high >> (index - 64)) & 1);
    result.push_back(negative ? '-' : '+');
  }
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    int quartet_index = 0;
    if (argc == 2) {
      quartet_index = std::stoi(argv[1]);
    } else if (argc > 2) {
      throw std::runtime_error("usage: search_five_comb_mub_quartet [0..47]");
    }
    if (quartet_index < 0 || quartet_index >= 48) {
      throw std::runtime_error("quartet index must lie in 0..47");
    }

    const auto words = NormalizedWords();
    const auto quartets = ComplementaryQuartets(words);
    const auto vectors = ProjectiveVectors();
    const auto linear_maps = GeneralLinear3();
    const auto projective_maps = AdmissibleProjectiveMaps(vectors);
    const Quartet& quartet = quartets[quartet_index];

    std::uint64_t carrier_states = 0;
    std::uint64_t hole_states = 0;
    std::uint64_t row_compatible_states = 0;
    std::uint64_t exact_matches = 0;
    std::array<std::uint64_t, 2> carrier_states_by_affineness{};
    std::array<std::uint64_t, 2> hole_states_by_affineness{};
    std::array<std::uint64_t, 2> row_states_by_affineness{};
    std::array<std::uint64_t, 2> exact_matches_by_affineness{};
    std::array<Bits, kRows> first_match{};
    std::array<Bits, kRows> best_rows{};
    int best_bad_lags = kLags + 1;
    std::uint64_t best_energy = ~std::uint64_t{0};
    int best_projective_index = -1;
    int best_type_map_index = -1;
    int best_type_translation = -1;
    int best_sign_character = -1;
    int best_hole_mask = -1;

    for (int projective_index = 0;
         projective_index < static_cast<int>(projective_maps.size());
         ++projective_index) {
      const ProjectiveMap& projective = projective_maps[projective_index];
      const int affine_index = projective.affine ? 1 : 0;
      for (int type_map_index = 0;
           type_map_index < static_cast<int>(linear_maps.size());
           ++type_map_index) {
        const LinearMap& type_map = linear_maps[type_map_index];
        for (int type_translation = 0; type_translation < 8;
             ++type_translation) {
          // The omitted affine constant negates all 320 carrier positions.
          // Complementing all fourteen holes gives a globally negated
          // quadruple with identical correlations, so masks 0..7 are exact.
          for (int sign_character = 0; sign_character < 8;
               ++sign_character) {
            ++carrier_states;
            ++carrier_states_by_affineness[affine_index];
            const auto carrier =
                BuildCarrierRows(quartet, words, projective, type_map,
                                 type_translation, sign_character, vectors);
            for (const std::uint16_t holes : projective.hole_masks) {
              ++hole_states;
              ++hole_states_by_affineness[affine_index];
              const auto rows = AddHoles(carrier, holes);
              if (SquaredRowSumNorm(rows) != 334) {
                continue;
              }
              ++row_compatible_states;
              ++row_states_by_affineness[affine_index];
              bool exact = true;
              int bad_lags = 0;
              std::uint64_t energy = 0;
              // Long lags are cheapest and reject most hole assignments.
              for (int lag = kLags; lag >= 1; --lag) {
                const int value = Correlation(rows, lag);
                if (value != 0) {
                  exact = false;
                  ++bad_lags;
                  energy += static_cast<std::uint64_t>(value * value);
                  if (bad_lags > best_bad_lags ||
                      (bad_lags == best_bad_lags &&
                       energy >= best_energy)) {
                    break;
                  }
                }
              }
              if (exact) {
                ++exact_matches;
                ++exact_matches_by_affineness[affine_index];
                if (exact_matches == 1) {
                  first_match = rows;
                }
              }
              if (bad_lags < best_bad_lags ||
                  (bad_lags == best_bad_lags && energy < best_energy)) {
                best_bad_lags = bad_lags;
                best_energy = energy;
                best_rows = rows;
                best_projective_index = projective_index;
                best_type_map_index = type_map_index;
                best_type_translation = type_translation;
                best_sign_character = sign_character;
                best_hole_mask = holes;
              }
            }
          }
        }
      }
    }

    const std::uint64_t expected_carriers =
        8ULL * 168 * 8 * 8;
    const std::uint64_t expected_holes = expected_carriers * 256;
    if (carrier_states != expected_carriers ||
        hole_states != expected_holes ||
        carrier_states_by_affineness[0] != expected_carriers / 2 ||
        carrier_states_by_affineness[1] != expected_carriers / 2 ||
        hole_states_by_affineness[0] != expected_holes / 2 ||
        hole_states_by_affineness[1] != expected_holes / 2) {
      throw std::runtime_error("packing state count changed");
    }

    std::cout << "quartet_index=" << quartet_index << '\n';
    std::cout << "quartet_words=" << quartet[0] << ',' << quartet[1] << ','
              << quartet[2] << ',' << quartet[3] << '\n';
    std::cout << "projective_permutations=40320\n";
    std::cout
        << "projective_mod4_survivors_before_row_sign_quotient=64\n";
    std::cout << "projective_affine_survivors=32\n";
    std::cout << "projective_nonaffine_survivors=32\n";
    std::cout << "projective_maps_after_row_sign_quotient="
              << projective_maps.size() << '\n';
    std::cout << "projective_affine_reps_after_quotient=4\n";
    std::cout << "projective_nonaffine_reps_after_quotient=4\n";
    std::cout << "hole_fiber_size=256\n";
    std::cout << "carrier_states=" << carrier_states << '\n';
    std::cout << "affine_carrier_states="
              << carrier_states_by_affineness[1] << '\n';
    std::cout << "nonaffine_carrier_states="
              << carrier_states_by_affineness[0] << '\n';
    std::cout << "hole_completions=" << hole_states << '\n';
    std::cout << "affine_hole_completions="
              << hole_states_by_affineness[1] << '\n';
    std::cout << "nonaffine_hole_completions="
              << hole_states_by_affineness[0] << '\n';
    std::cout << "row_compatible_completions=" << row_compatible_states
              << '\n';
    std::cout << "affine_row_compatible_completions="
              << row_states_by_affineness[1] << '\n';
    std::cout << "nonaffine_row_compatible_completions="
              << row_states_by_affineness[0] << '\n';
    std::cout << "exact_bs84_83=" << exact_matches << '\n';
    std::cout << "affine_exact_bs84_83="
              << exact_matches_by_affineness[1] << '\n';
    std::cout << "nonaffine_exact_bs84_83="
              << exact_matches_by_affineness[0] << '\n';
    std::cout << "best_bad_lags=" << best_bad_lags << '\n';
    std::cout << "best_partial_energy=" << best_energy << '\n';
    std::cout << "best_projective_index=" << best_projective_index << '\n';
    std::cout << "best_projective_affine="
              << (projective_maps[best_projective_index].affine ? 1 : 0)
              << '\n';
    std::cout << "best_projective_labels=";
    for (int slot = 0; slot < kSlots; ++slot) {
      if (slot) {
        std::cout << ',';
      }
      std::cout
          << projective_maps[best_projective_index].labels[slot];
    }
    std::cout << '\n';
    std::cout << "best_type_map_index=" << best_type_map_index << '\n';
    std::cout << "best_type_translation=" << best_type_translation << '\n';
    std::cout << "best_sign_character=" << best_sign_character << '\n';
    std::cout << "best_hole_mask=" << best_hole_mask << '\n';
    for (int row = 0; row < kRows; ++row) {
      const int length = row < 2 ? kLengthLong : kLengthShort;
      std::cout << "best_sequence_" << row << '='
                << SignString(best_rows[row], length) << '\n';
    }
    if (exact_matches > 0) {
      for (int row = 0; row < kRows; ++row) {
        const int length = row < 2 ? kLengthLong : kLengthShort;
        std::cout << "sequence_" << row << '='
                  << SignString(first_match[row], length) << '\n';
      }
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error=" << error.what() << '\n';
    return 1;
  }
}
