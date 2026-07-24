#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <vector>

using U128 = unsigned __int128;

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int representative_count = 0;
  if (!(std::cin >> representative_count) || representative_count <= 0) {
    throw std::runtime_error("missing representative count");
  }
  std::vector<std::array<unsigned char, 36>> representatives(
      representative_count);
  for (auto& representative : representatives) {
    for (auto& color : representative) {
      int value = -1;
      if (!(std::cin >> value) || value < 0 || value >= 7) {
        throw std::runtime_error("invalid representative color");
      }
      color = static_cast<unsigned char>(value);
    }
  }

  int pair_index[9][9];
  int edge = 0;
  for (int i = 0; i < 9; ++i) {
    for (int j = i + 1; j < 9; ++j) {
      pair_index[i][j] = pair_index[j][i] = edge++;
    }
  }

  constexpr std::uint64_t factorial_nine = 362880;
  std::map<std::uint64_t, std::uint64_t> automorphism_distribution;
  std::map<std::uint64_t, std::uint64_t> orbit_size_distribution;
  std::vector<U128> canonical_codes;
  std::uint64_t labeled_support = 0;
  for (const auto& representative : representatives) {
    std::array<int, 9> permutation{0, 1, 2, 3, 4, 5, 6, 7, 8};
    std::uint64_t automorphisms = 0;
    U128 canonical = ~static_cast<U128>(0);
    do {
      U128 code = 0;
      bool fixed = true;
      int local_edge = 0;
      for (int i = 0; i < 9; ++i) {
        for (int j = i + 1; j < 9; ++j) {
          const unsigned color =
              representative[pair_index[permutation[i]][permutation[j]]];
          code |= static_cast<U128>(color) << (3 * local_edge);
          fixed = fixed && (color == representative[local_edge]);
          ++local_edge;
        }
      }
      if (fixed) ++automorphisms;
      canonical = std::min(canonical, code);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    if (automorphisms == 0 || factorial_nine % automorphisms != 0) {
      throw std::runtime_error("invalid automorphism count");
    }
    const std::uint64_t orbit_size = factorial_nine / automorphisms;
    ++automorphism_distribution[automorphisms];
    ++orbit_size_distribution[orbit_size];
    labeled_support += orbit_size;
    canonical_codes.push_back(canonical);
  }
  std::sort(canonical_codes.begin(), canonical_codes.end());
  if (std::adjacent_find(canonical_codes.begin(), canonical_codes.end()) !=
      canonical_codes.end()) {
    throw std::runtime_error("source representatives have overlapping orbits");
  }

  std::cout << "k9_orbits " << representative_count << '\n';
  std::cout << "labeled_k9_support " << labeled_support << '\n';
  for (const auto& [size, count] : orbit_size_distribution) {
    std::cout << "orbit_size " << size << ' ' << count << '\n';
  }
  for (const auto& [size, count] : automorphism_distribution) {
    std::cout << "automorphism_size " << size << ' ' << count << '\n';
  }
  std::cout << "minimum_k10_color_trials " << 7 * labeled_support << '\n';
  std::cout << "packed_support_bytes_at_16_per_pattern "
            << 16 * labeled_support << '\n';
  return 0;
}
