#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using Row = std::array<int, 9>;

struct Candidate {
  std::array<int8_t, 8> off{};
  int8_t diagonal = 0;
  bool operator<(const Candidate& other) const {
    if (off != other.off) return off < other.off;
    return diagonal < other.diagonal;
  }
};

static std::vector<Candidate> candidates;
static std::array<Row, 9> matrix_rows{};
static unsigned long long rooted_solutions = 0;
static std::set<std::array<int8_t, 45>> orderly_solutions;
static std::map<std::array<int8_t, 45>, unsigned long long> canonical_counts;
static std::map<std::array<int8_t, 45>, std::array<Row, 9>>
    canonical_representatives;
static unsigned long long nodes[10]{};
static unsigned long long candidate_visits[10]{};
static bool stop_after_first = false;
static bool verbose = false;
static bool dump_diagonals = false;
static bool dump_canonical = false;

static int rank_mod(std::array<Row, 9> rows, int prime);

[[noreturn]] static void fail(const std::string& message) {
  std::cerr << "ERROR: " << message << "\n";
  std::exit(1);
}

static void require_or_fail(bool condition, const std::string& message) {
  if (!condition) fail(message);
}

static void generate_multisets_rec(int position, int minimum, int sum,
                                   int square_sum, std::array<int, 8>& values) {
  if (position == 8) {
    int diagonal = -sum;
    if ((diagonal & 1) != 0 || diagonal < -16 || diagonal > 16) return;
    if (square_sum + diagonal * diagonal != 296) return;
    std::array<int, 8> permutation = values;
    do {
      Candidate candidate;
      for (int i = 0; i < 8; ++i) {
        candidate.off[i] = static_cast<int8_t>(permutation[i]);
      }
      candidate.diagonal = static_cast<int8_t>(diagonal);
      candidates.push_back(candidate);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return;
  }
  const int remaining = 8 - position;
  for (int value = minimum; value <= 17; value += 2) {
    int new_square_sum = square_sum + value * value;
    if (new_square_sum > 296) continue;
    values[position] = value;
    generate_multisets_rec(position + 1, value, sum + value,
                           new_square_sum, values);
  }
}

static std::pair<size_t, size_t> prefix_range(const std::vector<int>& prefix) {
  auto lower = std::lower_bound(
      candidates.begin(), candidates.end(), prefix,
      [](const Candidate& candidate, const std::vector<int>& value) {
        for (size_t i = 0; i < value.size(); ++i) {
          if (candidate.off[i] != value[i])
            return candidate.off[i] < value[i];
        }
        return false;
      });
  auto upper = std::upper_bound(
      candidates.begin(), candidates.end(), prefix,
      [](const std::vector<int>& value, const Candidate& candidate) {
        for (size_t i = 0; i < value.size(); ++i) {
          if (value[i] != candidate.off[i])
            return value[i] < candidate.off[i];
        }
        return false;
      });
  return {static_cast<size_t>(lower - candidates.begin()),
          static_cast<size_t>(upper - candidates.begin())};
}

static Row materialize_row(const Candidate& candidate, int diagonal_position) {
  Row row{};
  int off_index = 0;
  for (int j = 0; j < 9; ++j) {
    if (j == diagonal_position) {
      row[j] = candidate.diagonal;
    } else {
      row[j] = candidate.off[off_index++];
    }
  }
  return row;
}

static bool canonical_future_order(const Row& row, int current) {
  // Future vertices having identical columns against all already processed
  // rows are interchangeable.  Retain their nondecreasing order in this row.
  for (int first = current + 1; first < 9; ++first) {
    for (int second = first + 1; second < 9; ++second) {
      bool same_signature = true;
      for (int h = 0; h < current; ++h) {
        if (matrix_rows[h][first] != matrix_rows[h][second]) {
          same_signature = false;
          break;
        }
      }
      if (same_signature && row[first] > row[second]) return false;
    }
  }
  return true;
}

static std::array<int8_t, 45> upper_triangle(
    const std::array<Row, 9>& rows) {
  std::array<int8_t, 45> result{};
  int index = 0;
  for (int i = 0; i < 9; ++i)
    for (int j = i; j < 9; ++j)
      result[index++] = static_cast<int8_t>(rows[i][j]);
  return result;
}

static std::array<Row, 9> from_upper_triangle(
    const std::array<int8_t, 45>& upper) {
  std::array<Row, 9> rows{};
  int index = 0;
  for (int i = 0; i < 9; ++i) {
    for (int j = i; j < 9; ++j) {
      rows[i][j] = rows[j][i] = upper[index++];
    }
  }
  return rows;
}

static std::array<int8_t, 45> permuted_upper(
    const std::array<Row, 9>& rows, const std::array<int, 9>& p) {
  std::array<int8_t, 45> result{};
  int index = 0;
  for (int i = 0; i < 9; ++i)
    for (int j = i; j < 9; ++j)
      result[index++] = static_cast<int8_t>(rows[p[i]][p[j]]);
  return result;
}

static std::array<int8_t, 45> canonical_form(
    const std::array<Row, 9>& rows) {
  std::array<int, 9> p{0, 1, 2, 3, 4, 5, 6, 7, 8};
  auto best = permuted_upper(rows, p);
  while (std::next_permutation(p.begin(), p.end())) {
    auto image = permuted_upper(rows, p);
    if (image < best) best = image;
  }
  return best;
}

static int rank_mod(std::array<Row, 9> rows, int prime) {
  int rank = 0;
  for (int column = 0; column < 9 && rank < 9; ++column) {
    int pivot = rank;
    while (pivot < 9 && ((rows[pivot][column] % prime) + prime) % prime == 0)
      ++pivot;
    if (pivot == 9) continue;
    std::swap(rows[rank], rows[pivot]);
    int value = ((rows[rank][column] % prime) + prime) % prime;
    int inverse = 1;
    while ((value * inverse) % prime != 1) ++inverse;
    for (int j = column; j < 9; ++j)
      rows[rank][j] = (((rows[rank][j] % prime) + prime) % prime * inverse) %
                      prime;
    for (int i = 0; i < 9; ++i) {
      if (i == rank) continue;
      int factor = ((rows[i][column] % prime) + prime) % prime;
      for (int j = column; j < 9; ++j) {
        rows[i][j] = ((rows[i][j] - factor * rows[rank][j]) % prime + prime) %
                     prime;
      }
    }
    ++rank;
  }
  return rank;
}

static long double log2_binomial(int n, int k) {
  return (std::lgammal(n + 1.0L) - std::lgammal(k + 1.0L) -
          std::lgammal(n - k + 1.0L)) /
         std::log(2.0L);
}

static long double raw_binary_lift_log2(const std::array<Row, 9>& rows) {
  long double result = 0.0L;
  for (int i = 0; i < 9; ++i) {
    const int inverse_pairs = (36 - rows[i][i]) / 4;
    result += log2_binomial(18, inverse_pairs);
    for (int j = i + 1; j < 9; ++j) {
      const int block_degree = (37 - rows[i][j]) / 2;
      result += log2_binomial(37, block_degree);
    }
  }
  return result;
}

static void print_matrix(const std::array<Row, 9>& rows,
                         const std::string& prefix) {
  std::cerr << prefix << "\n";
  for (int i = 0; i < 9; ++i) {
    for (int j = 0; j < 9; ++j) {
      std::cerr << (j ? " " : "") << rows[i][j];
    }
    std::cerr << "\n";
  }
}

static void verify_terminal_matrix(const std::array<Row, 9>& rows) {
  for (int i = 0; i < 9; ++i) {
    int row_sum = 0;
    for (int j = 0; j < 9; ++j) {
      require_or_fail(rows[i][j] == rows[j][i],
                      "terminal matrix is not symmetric");
      row_sum += rows[i][j];
      if (i == j) {
        require_or_fail(rows[i][j] % 2 == 0,
                        "terminal diagonal parity failed");
        require_or_fail(std::abs(rows[i][j]) <= 36,
                        "terminal diagonal block bound failed");
      } else {
        require_or_fail(rows[i][j] % 2 != 0,
                        "terminal off-diagonal parity failed");
        require_or_fail(std::abs(rows[i][j]) <= 37,
                        "terminal off-diagonal block bound failed");
      }
    }
    require_or_fail(row_sum == 0, "terminal row sum failed");
  }
  for (int i = 0; i < 9; ++i) {
    for (int j = 0; j < 9; ++j) {
      int product = 0;
      for (int k = 0; k < 9; ++k)
        product += rows[i][k] * rows[k][j];
      const int expected = i == j ? 296 : -37;
      require_or_fail(product == expected,
                      "terminal square equation failed");
    }
  }
  require_or_fail(rank_mod(rows, 37) == 4,
                  "terminal rank modulo 37 is not four");
}

static void recurse(int current) {
  ++nodes[current];
  if (current == 9) {
    verify_terminal_matrix(matrix_rows);
    ++rooted_solutions;
    auto labelled = upper_triangle(matrix_rows);
    if (!orderly_solutions.insert(labelled).second) return;
    auto canonical = canonical_form(matrix_rows);
    auto [it, inserted] = canonical_counts.emplace(canonical, 0);
    ++it->second;
    if (inserted) canonical_representatives.emplace(canonical, matrix_rows);
    if (inserted && verbose) {
      print_matrix(matrix_rows, "NEW_CLASS " +
          std::to_string(canonical_counts.size()));
      std::cerr << "rooted=" << rooted_solutions
                << " orderly=" << orderly_solutions.size()
                << " classes=" << canonical_counts.size() << "\n";
    }
    return;
  }

  std::vector<int> prefix;
  prefix.reserve(current);
  for (int h = 0; h < current; ++h)
    prefix.push_back(matrix_rows[h][current]);
  auto [begin, end] = prefix_range(prefix);
  candidate_visits[current] += end - begin;

  for (size_t index = begin; index < end; ++index) {
    Row row = materialize_row(candidates[index], current);
    bool compatible = true;
    for (int h = 0; h < current; ++h) {
      int dot = 0;
      for (int j = 0; j < 9; ++j) dot += row[j] * matrix_rows[h][j];
      if (dot != -37) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    if (!canonical_future_order(row, current)) continue;
    matrix_rows[current] = row;
    recurse(current + 1);
    if (stop_after_first && rooted_solutions) return;
  }
}

int main(int argc, char** argv) {
  for (int i = 1; i < argc; ++i) {
    if (std::string(argv[i]) == "--first") stop_after_first = true;
    if (std::string(argv[i]) == "--verbose") verbose = true;
    if (std::string(argv[i]) == "--dump-diagonals") dump_diagonals = true;
    if (std::string(argv[i]) == "--dump-canonical") dump_canonical = true;
  }
  std::array<int, 8> values{};
  generate_multisets_rec(0, -17, 0, 0, values);
  std::sort(candidates.begin(), candidates.end());
  candidates.erase(std::unique(
      candidates.begin(), candidates.end(),
      [](const Candidate& a, const Candidate& b) {
        return a.off == b.off && a.diagonal == b.diagonal;
      }), candidates.end());
  std::cerr << "ordered_row_candidates=" << candidates.size() << "\n";

  // At the root all eight other vertices are interchangeable, so require the
  // first row's off-diagonal entries to be nondecreasing.
  for (const Candidate& candidate : candidates) {
    if (!std::is_sorted(candidate.off.begin(), candidate.off.end())) continue;
    matrix_rows[0] = materialize_row(candidate, 0);
    recurse(1);
    if (stop_after_first && rooted_solutions) break;
  }

  std::cout << "rooted_solutions " << rooted_solutions << "\n";
  std::cout << "orderly_terminal_matrices " << orderly_solutions.size()
            << "\n";
  std::cout << "equivalence_classes " << canonical_counts.size() << "\n";
  if (!stop_after_first) {
    require_or_fail(rooted_solutions == 7016,
                    "orderly terminal count changed");
    require_or_fail(orderly_solutions.size() == 7016,
                    "distinct orderly terminal count changed");
    require_or_fail(canonical_counts.size() == 625,
                    "permutation-class count changed");
  }
  if (dump_canonical) {
    size_t class_index = 0;
    for (const auto& [canonical, count] : canonical_counts) {
      std::cout << "canonical_upper " << ++class_index;
      for (int8_t entry : canonical)
        std::cout << " " << static_cast<int>(entry);
      std::cout << "\n";
    }
  }
  size_t self_negative_classes = 0;
  for (const auto& [canonical, representative] : canonical_representatives) {
    std::array<Row, 9> negative = representative;
    for (Row& row : negative)
      for (int& entry : row) entry = -entry;
    if (canonical_form(negative) == canonical) ++self_negative_classes;
  }
  std::cout << "self_negative_classes " << self_negative_classes << "\n";
  std::cout << "sign_permutation_classes "
            << (canonical_counts.size() + self_negative_classes) / 2 << "\n";
  if (!stop_after_first) {
    require_or_fail(self_negative_classes == 3,
                    "self-negative class count changed");
    require_or_fail(
        (canonical_counts.size() + self_negative_classes) / 2 == 314,
        "sign-permutation class count changed");
  }

  std::map<int, size_t> automorphism_distribution;
  std::map<std::array<int8_t, 45>, int> automorphism_orders;
  std::map<int, size_t> rank_mod_3_distribution;
  std::map<int, size_t> maximum_absolute_entry_distribution;
  std::map<std::array<int8_t, 45>, long double> raw_lift_logs;
  std::map<std::array<int, 9>, size_t> diagonal_multiset_distribution;
  size_t zero_diagonal_classes = 0;
  size_t central_diagonal_classes = 0;
  for (const auto& [canonical, representative] : canonical_representatives) {
    std::array<int, 9> p{0, 1, 2, 3, 4, 5, 6, 7, 8};
    int automorphisms = 0;
    do {
      if (permuted_upper(representative, p) == canonical) ++automorphisms;
    } while (std::next_permutation(p.begin(), p.end()));
    ++automorphism_distribution[automorphisms];
    automorphism_orders.emplace(canonical, automorphisms);

    std::array<int, 9> diagonal{};
    for (int i = 0; i < 9; ++i) diagonal[i] = representative[i][i];
    std::sort(diagonal.begin(), diagonal.end());
    ++diagonal_multiset_distribution[diagonal];
    if (diagonal == std::array<int, 9>{}) ++zero_diagonal_classes;
    if (std::all_of(diagonal.begin(), diagonal.end(),
                    [](int entry) {
                      return entry == -4 || entry == 0 || entry == 4;
                    }))
      ++central_diagonal_classes;
    ++rank_mod_3_distribution[rank_mod(representative, 3)];
    int maximum_absolute_entry = 0;
    for (const Row& row : representative)
      for (int entry : row)
        maximum_absolute_entry =
            std::max(maximum_absolute_entry, std::abs(entry));
    ++maximum_absolute_entry_distribution[maximum_absolute_entry];
    raw_lift_logs.emplace(canonical, raw_binary_lift_log2(representative));
  }
  std::cout << "automorphism_distribution";
  for (const auto& [order, count] : automorphism_distribution)
    std::cout << " " << order << ":" << count;
  std::cout << "\n";
  if (!stop_after_first) {
    const std::map<int, size_t> expected{
        {1, 480}, {2, 100}, {3, 24}, {4, 5}, {6, 14}, {24, 2}};
    require_or_fail(automorphism_distribution == expected,
                    "automorphism distribution changed");
  }
  unsigned long long all_labelled_matrices = 0;
  constexpr unsigned long long factorial_nine = 362880;
  for (const auto& [order, count] : automorphism_distribution)
    all_labelled_matrices += factorial_nine / order * count;
  std::cout << "all_labelled_matrices " << all_labelled_matrices << "\n";
  if (!stop_after_first)
    require_or_fail(all_labelled_matrices == 196560000,
                    "labeled matrix count changed");
  std::cout << "diagonal_multisets "
            << diagonal_multiset_distribution.size() << "\n";
  if (dump_diagonals) {
    for (const auto& [diagonal, count] : diagonal_multiset_distribution) {
      std::cout << "diagonal_multiset";
      for (int entry : diagonal) std::cout << " " << entry;
      std::cout << " classes " << count << "\n";
    }
  }
  std::cout << "zero_diagonal_classes " << zero_diagonal_classes << "\n";
  std::cout << "diagonal_entries_all_in_minus4_0_4_classes "
            << central_diagonal_classes << "\n";
  std::cout << "rank_mod_3_distribution";
  for (const auto& [rank, count] : rank_mod_3_distribution)
    std::cout << " " << rank << ":" << count;
  std::cout << "\n";
  std::cout << "maximum_absolute_entry_distribution";
  for (const auto& [maximum, count] : maximum_absolute_entry_distribution)
    std::cout << " " << maximum << ":" << count;
  std::cout << "\n";
  if (!stop_after_first) {
    require_or_fail(diagonal_multiset_distribution.size() == 111,
                    "diagonal-multiset count changed");
    require_or_fail(zero_diagonal_classes == 0,
                    "an all-zero diagonal class appeared");
    require_or_fail(central_diagonal_classes == 2,
                    "central diagonal class count changed");
    require_or_fail(rank_mod_3_distribution ==
                        std::map<int, size_t>{{2, 39}, {4, 586}},
                    "rank-modulo-3 distribution changed");
    require_or_fail(
        maximum_absolute_entry_distribution ==
            std::map<int, size_t>{
                {9, 3}, {11, 52}, {12, 231},
                {13, 231}, {15, 28}, {16, 80}},
        "maximum-entry distribution changed");
  }
  auto raw_minimum = std::min_element(
      raw_lift_logs.begin(), raw_lift_logs.end(),
      [](const auto& first, const auto& second) {
        return first.second < second.second;
      });
  auto raw_maximum = std::max_element(
      raw_lift_logs.begin(), raw_lift_logs.end(),
      [](const auto& first, const auto& second) {
        return first.second < second.second;
      });
  std::cout.precision(15);
  std::cout << "raw_binary_lift_log2_min "
            << static_cast<double>(raw_minimum->second) << "\n";
  std::cout << "raw_binary_lift_log2_max "
            << static_cast<double>(raw_maximum->second) << "\n";
  if (!stop_after_first) {
    require_or_fail(
        std::abs(raw_minimum->second - 1340.52392808143L) < 1e-10L,
        "minimum raw-lift exponent changed");
    require_or_fail(
        std::abs(raw_maximum->second - 1340.83193919044L) < 1e-10L,
        "maximum raw-lift exponent changed");
  }
  int balanced_index = 0;
  for (const auto& [canonical, representative] : canonical_representatives) {
    int maximum_absolute_entry = 0;
    for (int8_t entry : canonical)
      maximum_absolute_entry =
          std::max(maximum_absolute_entry, std::abs(static_cast<int>(entry)));
    if (maximum_absolute_entry != 9) continue;
    ++balanced_index;
    auto canonical_rows = from_upper_triangle(canonical);
    std::array<Row, 9> negative = canonical_rows;
    for (Row& row : negative)
      for (int& entry : row) entry = -entry;
    std::cout << "balanced_class " << balanced_index
              << " automorphisms " << automorphism_orders.at(canonical)
              << " rank_mod_3 " << rank_mod(canonical_rows, 3)
              << " self_negative "
              << (canonical_form(negative) == canonical ? 1 : 0) << "\n";
    for (const Row& row : canonical_rows) {
      for (int j = 0; j < 9; ++j)
        std::cout << (j ? " " : "") << row[j];
      std::cout << "\n";
    }
  }

  const std::array<Row, 9> certified{{
      {{0, -11, -3, 7, -3, 7, -3, 7, -1}},
      {{-11, -4, 7, -1, 7, -1, 7, -1, -3}},
      {{-3, 7, 0, -11, -3, 7, -3, 7, -1}},
      {{7, -1, -11, -4, 7, -1, 7, -1, -3}},
      {{-3, 7, -3, 7, 0, -11, -3, 7, -1}},
      {{7, -1, 7, -1, -11, -4, 7, -1, -3}},
      {{-3, 7, -3, 7, -3, 7, 0, -11, -1}},
      {{7, -1, 7, -1, 7, -1, -11, -4, -3}},
      {{-1, -3, -1, -3, -1, -3, -1, -3, 16}},
  }};
  auto certified_canonical = canonical_form(certified);
  auto certified_iterator = canonical_counts.find(certified_canonical);
  if (certified_iterator == canonical_counts.end()) {
    fail("certified quotient absent from census");
  }
  size_t certified_index =
      1 + static_cast<size_t>(std::distance(canonical_counts.begin(),
                                            certified_iterator));
  int certified_automorphisms = 0;
  std::array<int, 9> certified_permutation{0, 1, 2, 3, 4, 5, 6, 7, 8};
  do {
    if (permuted_upper(certified, certified_permutation) ==
        upper_triangle(certified))
      ++certified_automorphisms;
  } while (std::next_permutation(certified_permutation.begin(),
                                 certified_permutation.end()));
  std::cout << "certified_class_lexicographic_index " << certified_index
            << "\n";
  std::cout << "certified_automorphism_order " << certified_automorphisms
            << "\n";
  const long double certified_raw_log = raw_lift_logs.at(certified_canonical);
  size_t certified_raw_rank = 1;
  for (const auto& [canonical, raw_log] : raw_lift_logs)
    if (raw_log < certified_raw_log - 1e-12L) ++certified_raw_rank;
  std::cout << "certified_raw_binary_lift_log2 "
            << static_cast<double>(certified_raw_log) << "\n";
  std::cout << "certified_raw_binary_lift_rank "
            << certified_raw_rank << "_of_" << raw_lift_logs.size() << "\n";
  if (!stop_after_first) {
    require_or_fail(certified_automorphisms == 24,
                    "certified automorphism order changed");
    require_or_fail(
        std::abs(certified_raw_log - 1340.72177608771L) < 1e-10L,
        "certified raw-lift exponent changed");
    require_or_fail(certified_raw_rank == 106,
                    "certified raw-lift rank changed");
  }

  const std::array<Row, 9> rank_two_exception{{
      {{-4, -11, -7, 1, 1, 3, 5, 5, 7}},
      {{-11, 0, 11, 1, 1, -5, 3, 3, -3}},
      {{-7, 11, -4, -3, -3, 5, -3, -3, 7}},
      {{1, 1, -3, 4, 1, 5, -9, 9, -9}},
      {{1, 1, -3, 1, 4, 5, 9, -9, -9}},
      {{3, -5, 5, 5, 5, 0, -9, -9, 5}},
      {{5, 3, -3, -9, 9, -9, 0, 3, 1}},
      {{5, 3, -3, 9, -9, -9, 3, 0, 1}},
      {{7, -3, 7, -9, -9, 5, 1, 1, 0}},
  }};
  verify_terminal_matrix(rank_two_exception);
  const auto exception_canonical = canonical_form(rank_two_exception);
  require_or_fail(canonical_counts.count(exception_canonical) == 1,
                  "rank-two exceptional quotient is absent");
  std::array<Row, 9> negative_exception = rank_two_exception;
  for (Row& row : negative_exception)
    for (int& entry : row) entry = -entry;
  const auto negative_exception_canonical =
      canonical_form(negative_exception);
  require_or_fail(negative_exception_canonical != exception_canonical,
                  "rank-two exceptional quotient became self-negative");
  require_or_fail(canonical_counts.count(negative_exception_canonical) == 1,
                  "negative rank-two exceptional quotient is absent");
  const std::array<int, 9> exception_generator{
      0, 1, 2, 4, 3, 5, 7, 6, 8};
  require_or_fail(
      permuted_upper(rank_two_exception, exception_generator) ==
          upper_triangle(rank_two_exception),
      "rank-two exceptional automorphism generator failed");
  require_or_fail(automorphism_orders.at(exception_canonical) == 2,
                  "rank-two exceptional automorphism order changed");
  std::cout << "rank_two_exception_profile "
            << "-4 -4 0 0 0 0 0 4 4\n";
  std::cout << "rank_two_exception_sign_classes 1\n";
  std::cout << "rank_two_exception_automorphism_generator_one_based "
            << "(4 5)(7 8)\n";
  std::cout << "rank_two_exception_representative\n";
  for (const Row& row : rank_two_exception) {
    for (int j = 0; j < 9; ++j)
      std::cout << (j ? " " : "") << row[j];
    std::cout << "\n";
  }
  std::cout << "rank_two_exception_adjacency_quotient\n";
  for (int i = 0; i < 9; ++i) {
    for (int j = 0; j < 9; ++j) {
      const int degree =
          (37 - (i == j ? 1 : 0) - rank_two_exception[i][j]) / 2;
      std::cout << (j ? " " : "") << degree;
    }
    std::cout << "\n";
  }
  for (int i = 1; i <= 9; ++i) {
    std::cout << "depth " << i << " nodes " << nodes[i]
              << " candidate_visits " << candidate_visits[i] << "\n";
  }
  return 0;
}
