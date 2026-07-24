#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <unordered_map>
#include <utility>
#include <vector>

using U128 = unsigned __int128;

struct U128Hash {
  std::size_t operator()(U128 value) const noexcept {
    const std::uint64_t low = static_cast<std::uint64_t>(value);
    const std::uint64_t high = static_cast<std::uint64_t>(value >> 64);
    std::uint64_t mixed =
        low ^ (high + 0x9e3779b97f4a7c15ULL + (low << 6) + (low >> 2));
    mixed ^= mixed >> 30;
    mixed *= 0xbf58476d1ce4e5b9ULL;
    mixed ^= mixed >> 27;
    mixed *= 0x94d049bb133111ebULL;
    mixed ^= mixed >> 31;
    return static_cast<std::size_t>(mixed);
  }
};

struct Record {
  std::uint64_t common;
  std::uint32_t tail;
};

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int representative_count = 0;
  if (!(std::cin >> representative_count) || representative_count <= 0) {
    throw std::runtime_error("missing representative count");
  }
  std::vector<std::array<unsigned char, 28>> representatives(
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

  int pair_index_8[8][8];
  int edge = 0;
  for (int i = 0; i < 8; ++i) {
    for (int j = i + 1; j < 8; ++j) {
      pair_index_8[i][j] = pair_index_8[j][i] = edge++;
    }
  }
  int pair_index_7[7][7];
  edge = 0;
  for (int i = 0; i < 7; ++i) {
    for (int j = i + 1; j < 7; ++j) {
      pair_index_7[i][j] = pair_index_7[j][i] = edge++;
    }
  }

  std::vector<U128> support;
  support.reserve(static_cast<std::size_t>(representative_count) * 40320);
  std::map<std::size_t, std::uint64_t> orbit_size_distribution;
  std::uint64_t orbit_size_sum = 0;
  for (const auto& representative : representatives) {
    std::array<int, 8> permutation{0, 1, 2, 3, 4, 5, 6, 7};
    std::vector<U128> orbit;
    orbit.reserve(40320);
    do {
      U128 code = 0;
      int local_edge = 0;
      for (int i = 0; i < 8; ++i) {
        for (int j = i + 1; j < 8; ++j) {
          const int old_i = permutation[i];
          const int old_j = permutation[j];
          const unsigned color =
              representative[pair_index_8[old_i][old_j]];
          code |= static_cast<U128>(color) << (3 * local_edge++);
        }
      }
      orbit.push_back(code);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    std::sort(orbit.begin(), orbit.end());
    orbit.erase(std::unique(orbit.begin(), orbit.end()), orbit.end());
    orbit_size_distribution[orbit.size()] += 1;
    orbit_size_sum += orbit.size();
    support.insert(support.end(), orbit.begin(), orbit.end());
  }
  std::sort(support.begin(), support.end());
  support.erase(std::unique(support.begin(), support.end()), support.end());
  if (support.size() != orbit_size_sum) {
    throw std::runtime_error("source orbits overlap");
  }

  const U128 low_81_mask = (static_cast<U128>(1) << 81) - 1;
  std::unordered_map<U128, unsigned char, U128Hash> prefix_masks;
  prefix_masks.reserve(support.size() * 5 / 4);
  std::vector<Record> records;
  records.reserve(support.size());
  for (const U128 code : support) {
    const U128 prefix = code & low_81_mask;
    const unsigned last_color = static_cast<unsigned>((code >> 81) & 7);
    prefix_masks[prefix] |= static_cast<unsigned char>(1U << last_color);

    std::uint64_t common = 0;
    int common_edge = 0;
    for (int i = 0; i < 7; ++i) {
      for (int j = i + 1; j < 7; ++j) {
        const unsigned color =
            static_cast<unsigned>((code >> (3 * pair_index_8[i][j])) & 7);
        common |= static_cast<std::uint64_t>(color) << (3 * common_edge++);
      }
    }
    std::uint32_t tail = 0;
    for (int i = 0; i < 7; ++i) {
      const unsigned color =
          static_cast<unsigned>((code >> (3 * pair_index_8[i][7])) & 7);
      tail |= static_cast<std::uint32_t>(color) << (3 * i);
    }
    records.push_back({common, tail});
  }
  std::sort(records.begin(), records.end(), [](const Record& first,
                                                const Record& second) {
    return first.common < second.common ||
           (first.common == second.common && first.tail < second.tail);
  });
  for (std::size_t index = 1; index < records.size(); ++index) {
    if (records[index - 1].common == records[index].common &&
        records[index - 1].tail == records[index].tail) {
      throw std::runtime_error("duplicate common/tail record");
    }
  }

  std::map<std::size_t, std::uint64_t> group_size_distribution;
  std::uint64_t overlap_keys = 0;
  std::uint64_t ordered_pairs = 0;
  std::uint64_t compatible = 0;
  for (std::size_t begin = 0; begin < records.size();) {
    std::size_t end = begin + 1;
    while (end < records.size() &&
           records[end].common == records[begin].common) {
      ++end;
    }
    const std::size_t group_size = end - begin;
    ++overlap_keys;
    ++group_size_distribution[group_size];
    ordered_pairs += static_cast<std::uint64_t>(group_size) * group_size;

    std::array<U128, 7> common_parts{};
    std::array<std::array<int, 6>, 7> remaining{};
    for (int deleted = 0; deleted < 7; ++deleted) {
      int position = 0;
      for (int vertex = 0; vertex < 7; ++vertex) {
        if (vertex != deleted) remaining[deleted][position++] = vertex;
      }
      for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j) {
          const int global_i = remaining[deleted][i];
          const int global_j = remaining[deleted][j];
          const int source_position = pair_index_7[global_i][global_j];
          const unsigned color = static_cast<unsigned>(
              (records[begin].common >> (3 * source_position)) & 7);
          const int target_position = pair_index_8[i][j];
          common_parts[deleted] |=
              static_cast<U128>(color) << (3 * target_position);
        }
      }
    }

    std::vector<std::array<U128, 7>> role_seven(group_size);
    std::vector<std::array<U128, 7>> role_eight(group_size);
    for (std::size_t item = 0; item < group_size; ++item) {
      const std::uint32_t tail = records[begin + item].tail;
      for (int deleted = 0; deleted < 7; ++deleted) {
        for (int local = 0; local < 6; ++local) {
          const int global = remaining[deleted][local];
          const unsigned color =
              static_cast<unsigned>((tail >> (3 * global)) & 7);
          role_seven[item][deleted] |=
              static_cast<U128>(color)
              << (3 * pair_index_8[local][6]);
          role_eight[item][deleted] |=
              static_cast<U128>(color)
              << (3 * pair_index_8[local][7]);
        }
      }
    }

    for (std::size_t first = 0; first < group_size; ++first) {
      for (std::size_t second = 0; second < group_size; ++second) {
        unsigned mask = 0x7f;
        for (int deleted = 0; deleted < 7; ++deleted) {
          const U128 prefix = common_parts[deleted] |
                              role_seven[first][deleted] |
                              role_eight[second][deleted];
          const auto found = prefix_masks.find(prefix);
          if (found == prefix_masks.end()) {
            mask = 0;
            break;
          }
          mask &= found->second;
          if (mask == 0) break;
        }
        compatible += static_cast<std::uint64_t>(
            __builtin_popcount(static_cast<unsigned>(mask)));
      }
    }
    begin = end;
  }

  std::cout << "k8_orbits " << representative_count << '\n';
  std::cout << "labeled_k8_support " << support.size() << '\n';
  for (const auto& [size, count] : orbit_size_distribution) {
    std::cout << "orbit_size " << size << ' ' << count << '\n';
  }
  std::cout << "k7_overlap_keys " << overlap_keys << '\n';
  for (const auto& [size, count] : group_size_distribution) {
    std::cout << "group_size " << size << ' ' << count << '\n';
  }
  std::cout << "compatible_ordered_k8_face_pairs " << ordered_pairs << '\n';
  std::cout << "pre_support_k9_color_trials " << 7 * ordered_pairs << '\n';
  std::cout << "support_compatible_labeled_k9 " << compatible << '\n';
  return 0;
}
