// Independent rank audit for the lambda-adic quadratic pencil on the two dense
// order-three profile shells.
//
// The six reversal-independent quadratic correlation coordinates have
// symmetric polar matrices over F_3.  This program forms every projective
// nonzero linear combination of the six matrices (364 combinations),
// restricts it to every legal medium-support mask of size 18 or 15, and
// records the maximum attainable rank.  It does not enumerate any phase
// assignment.

#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace {

constexpr int P = 37;
constexpr int CLASSES = 12;
constexpr int LAGS = 6;
constexpr int MASKS = 1 << CLASSES;

using Matrix = std::array<std::array<std::uint8_t, CLASSES>, CLASSES>;
using Coefficients = std::array<std::uint8_t, LAGS>;

int mod3(int value) {
  value %= 3;
  return value < 0 ? value + 3 : value;
}

std::array<std::array<int, 3>, CLASSES> classes;
std::array<int, P> class_of;
std::array<Matrix, LAGS> polar;

void initialize_geometry() {
  constexpr std::array<int, 3> subgroup = {1, 26, 10};
  class_of.fill(-1);
  int power = 1;
  for (int j = 0; j < CLASSES; ++j) {
    for (int k = 0; k < 3; ++k) {
      int value = power * subgroup[k] % P;
      classes[j][k] = value;
      if (class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      class_of[value] = j;
    }
    power = power * 2 % P;
  }
  for (int lag_class = 0; lag_class < LAGS; ++lag_class) {
    std::array<std::array<int, CLASSES>, CLASSES> transition{};
    int lag = classes[lag_class][0];
    for (int source = 1; source < P; ++source) {
      int target = (source + lag) % P;
      if (target == 0) continue;
      ++transition[class_of[source]][class_of[target]];
    }
    for (int left = 0; left < CLASSES; ++left) {
      for (int right = 0; right < CLASSES; ++right) {
        polar[lag_class][left][right] = static_cast<std::uint8_t>(
            mod3(transition[left][right] + transition[right][left]));
      }
    }
  }
}

std::vector<Coefficients> projective_coefficients() {
  std::vector<Coefficients> result;
  for (int code = 1; code < 729; ++code) {
    int work = code;
    Coefficients value{};
    int first_nonzero = -1;
    for (int index = 0; index < LAGS; ++index) {
      value[index] = static_cast<std::uint8_t>(work % 3);
      work /= 3;
      if (first_nonzero < 0 && value[index]) first_nonzero = index;
    }
    if (value[first_nonzero] != 1) continue;
    result.push_back(value);
  }
  if (result.size() != 364) {
    throw std::runtime_error("the projective pencil must have 364 members");
  }
  return result;
}

Matrix combine(const Coefficients& coefficients) {
  Matrix result{};
  for (int left = 0; left < CLASSES; ++left) {
    for (int right = 0; right < CLASSES; ++right) {
      int value = 0;
      for (int lag = 0; lag < LAGS; ++lag) {
        value += coefficients[lag] * polar[lag][left][right];
      }
      result[left][right] =
          static_cast<std::uint8_t>(mod3(value));
    }
  }
  return result;
}

int principal_rank(const Matrix& matrix, std::uint16_t mask) {
  std::array<int, CLASSES> positions{};
  int size = 0;
  for (int index = 0; index < CLASSES; ++index) {
    if (mask & (1u << index)) positions[size++] = index;
  }
  std::array<std::array<std::uint8_t, CLASSES>, CLASSES> work{};
  for (int row = 0; row < size; ++row) {
    for (int column = 0; column < size; ++column) {
      work[row][column] = matrix[positions[row]][positions[column]];
    }
  }
  int rank = 0;
  for (int column = 0; column < size; ++column) {
    int pivot = -1;
    for (int row = rank; row < size; ++row) {
      if (work[row][column]) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(work[rank], work[pivot]);
    if (work[rank][column] == 2) {
      for (int c = column; c < size; ++c) {
        work[rank][c] =
            static_cast<std::uint8_t>(2 * work[rank][c] % 3);
      }
    }
    for (int row = 0; row < size; ++row) {
      if (row == rank || !work[row][column]) continue;
      int factor = work[row][column];
      for (int c = column; c < size; ++c) {
        work[row][c] = static_cast<std::uint8_t>(
            mod3(work[row][c] - factor * work[rank][c]));
      }
    }
    ++rank;
  }
  return rank;
}

struct ShellStats {
  std::uint64_t support_masks = 0;
  std::map<int, std::uint64_t> maximum_rank_histogram;
  std::map<int, std::uint64_t> nonsingular_pencil_histogram;
  std::array<int, 364> minimum_rank_by_pencil{};
  std::array<std::uint64_t, 13> channel_size_histogram{};
  std::vector<std::pair<std::uint32_t, int>> deficient_examples;

  ShellStats() { minimum_rank_by_pencil.fill(100); }
};

class SupportEnumerator {
 public:
  SupportEnumerator(
      int target,
      const std::vector<Coefficients>& coefficients,
      const std::vector<std::array<std::uint8_t, MASKS>>& ranks)
      : target_(target), coefficients_(coefficients), ranks_(ranks) {}

  ShellStats run() {
    enumerate(0, 0, 0, 0);
    return stats_;
  }

 private:
  void enumerate(
      int quartet,
      int total,
      std::uint16_t a_mask,
      std::uint16_t b_mask) {
    if (quartet == LAGS) {
      if (total == target_) record(a_mask, b_mask);
      return;
    }
    int remaining = LAGS - quartet - 1;
    for (int local = 0; local < 16; ++local) {
      int count = __builtin_popcount(static_cast<unsigned>(local));
      if (count == 1) continue;
      int next = total + count;
      if (next > target_ || next + 4 * remaining < target_) continue;
      std::uint16_t next_a = a_mask;
      std::uint16_t next_b = b_mask;
      if (local & 1) next_a |= 1u << quartet;
      if (local & 2) next_a |= 1u << (quartet + 6);
      if (local & 4) next_b |= 1u << quartet;
      if (local & 8) next_b |= 1u << (quartet + 6);
      enumerate(quartet + 1, next, next_a, next_b);
    }
  }

  void record(std::uint16_t a_mask, std::uint16_t b_mask) {
    ++stats_.support_masks;
    int a_size = __builtin_popcount(static_cast<unsigned>(a_mask));
    ++stats_.channel_size_histogram[a_size];
    int maximum_rank = 0;
    int nonsingular = 0;
    for (std::size_t pencil = 0; pencil < coefficients_.size(); ++pencil) {
      int rank = ranks_[pencil][a_mask] + ranks_[pencil][b_mask];
      maximum_rank = std::max(maximum_rank, rank);
      if (rank == target_) ++nonsingular;
      stats_.minimum_rank_by_pencil[pencil] =
          std::min(stats_.minimum_rank_by_pencil[pencil], rank);
    }
    ++stats_.maximum_rank_histogram[maximum_rank];
    ++stats_.nonsingular_pencil_histogram[nonsingular];
    if (maximum_rank < target_ && stats_.deficient_examples.size() < 32) {
      std::uint32_t packed =
          static_cast<std::uint32_t>(a_mask)
          | (static_cast<std::uint32_t>(b_mask) << 12);
      stats_.deficient_examples.push_back({packed, maximum_rank});
    }
  }

  int target_;
  const std::vector<Coefficients>& coefficients_;
  const std::vector<std::array<std::uint8_t, MASKS>>& ranks_;
  ShellStats stats_;
};

void print_coefficients(const Coefficients& coefficients) {
  for (int index = 0; index < LAGS; ++index) {
    if (index) std::cout << ",";
    std::cout << static_cast<int>(coefficients[index]);
  }
}

void print_shell(
    int target,
    const ShellStats& stats,
    const std::vector<Coefficients>& coefficients) {
  std::cout << "shell_medium_count=" << target << "\n";
  std::cout << "support_masks=" << stats.support_masks << "\n";
  for (int size = 0; size <= 12; ++size) {
    if (stats.channel_size_histogram[size]) {
      std::cout << "channel_A_size[" << size
                << "]=" << stats.channel_size_histogram[size] << "\n";
    }
  }
  for (const auto& [rank, count] : stats.maximum_rank_histogram) {
    std::cout << "maximum_pencil_rank[" << rank << "]=" << count << "\n";
  }
  std::cout << "distinct_nonsingular_pencil_counts="
            << stats.nonsingular_pencil_histogram.size() << "\n";
  std::cout << "nonsingular_pencil_count_range="
            << stats.nonsingular_pencil_histogram.begin()->first << ","
            << stats.nonsingular_pencil_histogram.rbegin()->first << "\n";
  int universal_best = 0;
  for (int rank : stats.minimum_rank_by_pencil) {
    universal_best = std::max(universal_best, rank);
  }
  std::cout << "best_universal_rank=" << universal_best << "\n";
  for (std::size_t pencil = 0; pencil < coefficients.size(); ++pencil) {
    if (stats.minimum_rank_by_pencil[pencil] == universal_best) {
      std::cout << "best_universal_coefficients=";
      print_coefficients(coefficients[pencil]);
      std::cout << "\n";
    }
  }
  for (const auto& [packed, rank] : stats.deficient_examples) {
    std::cout << "deficient_mask=" << (packed & 0xfffu)
              << "," << (packed >> 12)
              << " rank=" << rank << "\n";
  }
}

}  // namespace

int main() {
  initialize_geometry();
  auto coefficients = projective_coefficients();
  std::vector<std::array<std::uint8_t, MASKS>> ranks(
      coefficients.size());
  for (std::size_t pencil = 0; pencil < coefficients.size(); ++pencil) {
    Matrix matrix = combine(coefficients[pencil]);
    for (int mask = 0; mask < MASKS; ++mask) {
      ranks[pencil][mask] = static_cast<std::uint8_t>(
          principal_rank(matrix, static_cast<std::uint16_t>(mask)));
    }
  }
  std::cout << "projective_pencils=" << coefficients.size() << "\n";
  for (int target : {15, 18}) {
    ShellStats stats =
        SupportEnumerator(target, coefficients, ranks).run();
    print_shell(target, stats, coefficients);
  }
}
