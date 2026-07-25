#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>

using Matrix = std::array<std::array<int, 9>, 9>;
using Upper = std::array<int8_t, 45>;

static Upper permuted_upper(const Matrix& matrix,
                            const std::array<int, 9>& permutation) {
  Upper result{};
  int index = 0;
  for (int i = 0; i < 9; ++i)
    for (int j = i; j < 9; ++j)
      result[index++] = matrix[permutation[i]][permutation[j]];
  return result;
}

static Upper canonical_form(const Matrix& matrix) {
  std::array<int, 9> permutation{0, 1, 2, 3, 4, 5, 6, 7, 8};
  Upper best = permuted_upper(matrix, permutation);
  while (std::next_permutation(permutation.begin(), permutation.end()))
    best = std::min(best, permuted_upper(matrix, permutation));
  return best;
}

static Matrix from_upper(const Upper& upper) {
  Matrix matrix{};
  int index = 0;
  for (int i = 0; i < 9; ++i)
    for (int j = i; j < 9; ++j)
      matrix[i][j] = matrix[j][i] = upper[index++];
  return matrix;
}

static Matrix binary_adjacency_quotient(const Matrix& orbit_sum) {
  Matrix result{};
  for (int i = 0; i < 9; ++i) {
    for (int j = 0; j < 9; ++j) {
      result[i][j] =
          ((37 - (i == j ? 1 : 0) - orbit_sum[i][j]) / 2) & 1;
    }
  }
  return result;
}

static Matrix off_diagonal_complement(Matrix matrix) {
  for (int i = 0; i < 9; ++i)
    for (int j = 0; j < 9; ++j)
      if (i != j) matrix[i][j] ^= 1;
  return matrix;
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: audit_z37_quotient_parity CENSUS_OUTPUT\n";
    return 1;
  }
  std::ifstream input(argv[1]);
  std::string line;
  std::map<Upper, size_t> parity_class_preimages;
  size_t quotient_classes = 0;
  while (std::getline(input, line)) {
    std::istringstream fields(line);
    std::string label;
    fields >> label;
    if (label != "canonical_upper") continue;
    int index;
    fields >> index;
    Upper upper{};
    for (int i = 0; i < 45; ++i) {
      int entry;
      fields >> entry;
      upper[i] = static_cast<int8_t>(entry);
    }
    Matrix orbit_sum = from_upper(upper);
    Upper parity =
        canonical_form(binary_adjacency_quotient(orbit_sum));
    ++parity_class_preimages[parity];
    ++quotient_classes;
  }
  if (quotient_classes != 625) {
    std::cerr << "expected 625 quotient classes\n";
    return 1;
  }

  std::map<int, size_t> automorphism_distribution;
  std::map<Upper, int> automorphism_orders;
  std::map<size_t, size_t> preimage_distribution;
  unsigned long long raw_labelled_patterns = 0;
  size_t self_complementary_classes = 0;
  constexpr unsigned long long factorial_nine = 362880;
  for (const auto& [canonical, preimages] : parity_class_preimages) {
    Matrix matrix = from_upper(canonical);
    std::array<int, 9> permutation{0, 1, 2, 3, 4, 5, 6, 7, 8};
    int automorphisms = 0;
    do {
      if (permuted_upper(matrix, permutation) == canonical)
        ++automorphisms;
    } while (std::next_permutation(permutation.begin(),
                                   permutation.end()));
    ++automorphism_distribution[automorphisms];
    automorphism_orders.emplace(canonical, automorphisms);
    ++preimage_distribution[preimages];
    raw_labelled_patterns += factorial_nine / automorphisms;
    if (canonical_form(off_diagonal_complement(matrix)) == canonical)
      ++self_complementary_classes;
  }

  std::cout << "quotient_classes " << quotient_classes << "\n";
  std::cout << "binary_permutation_classes "
            << parity_class_preimages.size() << "\n";
  std::cout << "binary_raw_labelled_patterns "
            << raw_labelled_patterns << "\n";
  std::cout << "binary_raw_labelled_patterns_mod_complement "
            << raw_labelled_patterns / 2 << "\n";
  std::cout << "binary_self_complementary_permutation_classes "
            << self_complementary_classes << "\n";
  std::cout << "binary_permutation_complement_classes "
            << (parity_class_preimages.size() +
                self_complementary_classes) /
                   2
            << "\n";
  std::cout << "binary_automorphism_distribution";
  for (const auto& [order, count] : automorphism_distribution)
    std::cout << " " << order << ":" << count;
  std::cout << "\n";
  std::cout << "quotient_class_preimage_distribution";
  for (const auto& [preimages, count] : preimage_distribution)
    std::cout << " " << preimages << ":" << count;
  std::cout << "\n";
  std::map<Upper, int> parity_class_indices;
  int parity_class_index = 0;
  for (const auto& [canonical, preimages] : parity_class_preimages)
    parity_class_indices.emplace(canonical, ++parity_class_index);
  for (const auto& [canonical, preimages] : parity_class_preimages) {
    Matrix matrix = from_upper(canonical);
    const int index = parity_class_indices.at(canonical);
    const Upper complement =
        canonical_form(off_diagonal_complement(matrix));
    std::array<int, 9> row_weights{};
    for (int i = 0; i < 9; ++i)
      for (int j = 0; j < 9; ++j)
        row_weights[i] += matrix[i][j];
    std::sort(row_weights.begin(), row_weights.end());
    std::cout << "binary_class " << index
              << " quotient_preimages " << preimages
              << " automorphisms " << automorphism_orders.at(canonical)
              << " complement_class " << parity_class_indices.at(complement)
              << "\n";
    std::cout << "loops";
    for (int i = 0; i < 9; ++i)
      if (matrix[i][i]) std::cout << " " << i + 1;
    std::cout << "\n";
    std::cout << "off_edges";
    for (int i = 0; i < 9; ++i)
      for (int j = i + 1; j < 9; ++j)
        if (matrix[i][j])
          std::cout << " (" << i + 1 << "," << j + 1 << ")";
    std::cout << "\n";
    std::cout << "row_weight_sequence";
    for (int weight : row_weights) std::cout << " " << weight;
    std::cout << "\n";
  }
  if (parity_class_preimages.size() != 3 ||
      raw_labelled_patterns != 48384 ||
      self_complementary_classes != 1 ||
      (parity_class_preimages.size() + self_complementary_classes) / 2 != 2 ||
      automorphism_distribution !=
          std::map<int, size_t>{{20, 1}, {24, 2}} ||
      preimage_distribution !=
          std::map<size_t, size_t>{{206, 2}, {213, 1}}) {
    std::cerr << "binary quotient census changed\n";
    return 1;
  }
  return 0;
}
