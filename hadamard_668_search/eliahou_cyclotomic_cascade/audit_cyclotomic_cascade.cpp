#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <map>
#include <memory>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

using WideUnsigned = unsigned __int128;

constexpr int kLong = 84;
constexpr int kShort = 83;
constexpr int kFold = 42;
constexpr int kSupportWeight = 39;
constexpr int kTarget = 167;
constexpr int kMaximumTargetEnergy = 166;

using Row = std::array<int, kFold>;
using Rows = std::array<Row, 4>;

struct Case {
  char block;
  int index;
  int signature_plus;
  int signature_minus;
};

struct LocalOption {
  int weight;
  int value;
  std::uint64_t multiplicity;
  std::uint64_t representative_mask;
};

struct BlockSpecification {
  int modulus;
  std::vector<int> baseline;
  std::vector<std::vector<LocalOption>> options;

  std::string Fingerprint() const {
    std::ostringstream out;
    out << modulus << ':';
    for (int value : baseline) out << value << ',';
    out << '|';
    for (const auto& group : options) {
      for (const auto& option : group) {
        out << option.weight << '/' << option.value << '/'
            << option.multiplicity << '/'
            << option.representative_mask << ',';
      }
      out << ';';
    }
    return out.str();
  }

  std::string ArithmeticFingerprint() const {
    std::ostringstream out;
    out << modulus << ':';
    for (int value : baseline) out << value << ',';
    out << '|';
    for (const auto& group : options) {
      for (const auto& option : group) {
        out << option.weight << '/' << option.value << '/'
            << option.multiplicity << ',';
      }
      out << ';';
    }
    return out.str();
  }
};

struct Histogram {
  // Packed (weight,c0,c1,c2), where absent higher coefficients are zero.
  struct Value {
    std::uint64_t count = 0;
    std::uint64_t representative_mask = 0;
  };
  std::unordered_map<std::uint64_t, Value> counts;
  std::uint64_t vector_tuples = 0;
};

struct CaseResult {
  int case_number;
  Case item;
  std::array<int, 3> target_signature;
  WideUnsigned support_count;
  std::uint64_t joined_signature_count;
  std::size_t p_histogram_entries;
  std::size_t q_histogram_entries;
  std::uint64_t long_support_mask;
  std::uint64_t short_support_mask;
};

struct GrowthResult {
  std::uint64_t raw_vector_tuples;
  std::uint64_t energy_admissible_vector_tuples;
};

std::vector<int> DecodeRuns(const std::vector<int>& runs) {
  std::vector<int> result;
  int sign = 1;
  for (int run : runs) {
    result.insert(result.end(), run, sign);
    sign = -sign;
  }
  return result;
}

std::vector<int> SeedSRuns() {
  std::vector<int> runs;
  auto append = [&](std::initializer_list<int> pattern, int repeats) {
    for (int repeat = 0; repeat < repeats; ++repeat) {
      runs.insert(runs.end(), pattern.begin(), pattern.end());
    }
  };
  append({4}, 5);
  append({2, 1, 1}, 5);
  append({1, 5}, 1);
  append({4}, 4);
  append({2, 1, 1}, 6);
  append({4}, 4);
  append({3}, 1);
  append({1, 2, 1}, 5);
  append({3}, 1);
  append({4}, 4);
  append({3}, 1);
  append({1, 2, 1}, 5);
  return runs;
}

std::array<std::vector<int>, 4> BaseRows() {
  const std::vector<int> s = DecodeRuns(SeedSRuns());
  const std::vector<int> q = DecodeRuns({83, 2, 81, 1});
  if (s.size() != 167 || q.size() != 167) {
    throw std::runtime_error("seed run data has the wrong length");
  }
  std::vector<int> product(167);
  for (int index = 0; index < 167; ++index) {
    product[index] = s[index] * q[index];
  }
  return {
      std::vector<int>(s.begin(), s.begin() + kLong),
      std::vector<int>(product.begin(), product.begin() + kLong),
      std::vector<int>(s.begin() + kLong, s.end()),
      std::vector<int>(product.begin() + kLong, product.end()),
  };
}

Row Antifold(const std::vector<int>& row) {
  if (row.size() != kLong && row.size() != kShort) {
    throw std::runtime_error("anti-fold row has the wrong length");
  }
  Row result{};
  for (int index = 0; index < kFold; ++index) {
    result[index] =
        row[index] -
        (index + kFold < static_cast<int>(row.size())
             ? row[index + kFold]
             : 0);
  }
  return result;
}

Rows SeedAntifold() {
  const auto base = BaseRows();
  Rows result{};
  for (int row = 0; row < 4; ++row) result[row] = Antifold(base[row]);
  return result;
}

std::pair<int, int> QCells(char block, int first_index) {
  const int length = block == 'L' ? kLong : kShort;
  return {first_index % kFold, (length - 1 - first_index) % kFold};
}

std::pair<int, int> QPairFoldSignature(const std::vector<int>& row,
                                       int first_index) {
  const int reflected = static_cast<int>(row.size()) - 1 - first_index;
  const std::array<int, 2> coordinates{first_index, reflected};
  if (coordinates[0] % kFold == coordinates[1] % kFold) {
    return {999, 999};
  }
  for (int index : coordinates) {
    const int mate = index < kFold ? index + kFold : index - kFold;
    if (mate >= static_cast<int>(row.size()) || row[index] == row[mate]) {
      return {999, 999};
    }
  }
  std::array<int, kFold> delta{};
  for (int index : coordinates) delta[index % kFold] -= row[index];
  int ordinary = 0;
  int alternating = 0;
  for (int index = 0; index < kFold; ++index) {
    ordinary += delta[index];
    alternating += (index % 2 == 0 ? 1 : -1) * delta[index];
  }
  return {ordinary, alternating};
}

std::vector<Case> CanonicalCases() {
  const auto base = BaseRows();
  std::vector<Case> result;
  for (const auto wanted :
       {std::pair<int, int>{-2, 0}, std::pair<int, int>{0, 2}}) {
    for (int index = 0; index < 42; ++index) {
      if (QPairFoldSignature(base[1], index) == wanted) {
        result.push_back({'L', index, wanted.first, wanted.second});
      }
    }
  }
  std::set<std::pair<int, int>> seen_short_cells;
  for (int index = 0; index < 41; ++index) {
    if (QPairFoldSignature(base[3], index) != std::pair<int, int>{0, 0}) {
      continue;
    }
    auto cells = QCells('S', index);
    if (cells.first > cells.second) std::swap(cells.first, cells.second);
    if (seen_short_cells.insert(cells).second) {
      result.push_back({'S', index, 0, 0});
    }
  }
  if (result.size() != 30) {
    throw std::runtime_error("canonical anti-fold case count changed");
  }
  return result;
}

std::array<Row, 4> NormalizedPairRows(const Rows& rows) {
  std::array<Row, 4> result{};
  for (int index = 0; index < kFold; ++index) {
    if ((rows[0][index] + rows[1][index]) % 2 ||
        (rows[2][index] + rows[3][index]) % 2 ||
        (rows[0][index] - rows[1][index]) % 2 ||
        (rows[2][index] - rows[3][index]) % 2) {
      throw std::runtime_error("pair normalization is not integral");
    }
    result[0][index] = (rows[0][index] + rows[1][index]) / 2;
    result[1][index] = (rows[2][index] + rows[3][index]) / 2;
    result[2][index] = (rows[0][index] - rows[1][index]) / 2;
    result[3][index] = (rows[2][index] - rows[3][index]) / 2;
  }
  return result;
}

std::pair<std::vector<int>, std::vector<int>> AvailableCells(
    const Case& item) {
  const auto q_cells = QCells(item.block, item.index);
  const std::set<int> removed{q_cells.first, q_cells.second};
  std::vector<int> long_cells;
  std::vector<int> short_cells;
  for (int cell = 0; cell < 41; ++cell) {
    if (item.block != 'L' || !removed.count(cell)) {
      long_cells.push_back(cell);
    }
  }
  for (int cell = 1; cell < 40; ++cell) {
    if (item.block != 'S' || !removed.count(cell)) {
      short_cells.push_back(cell);
    }
  }
  return {long_cells, short_cells};
}

Rows QAdjustedRows(const Case& item) {
  Rows rows = SeedAntifold();
  const int active_row = item.block == 'L' ? 1 : 3;
  const auto cells = QCells(item.block, item.index);
  rows[active_row][cells.first] = 0;
  rows[active_row][cells.second] = 0;
  return rows;
}

std::vector<int> ReducePolynomial(const Row& row, int modulus) {
  if (kFold % modulus != 0 || modulus % 2 != 0) {
    throw std::runtime_error("invalid negacyclic divisor");
  }
  std::vector<int> result(modulus);
  for (int index = 0; index < kFold; ++index) {
    const int quotient = index / modulus;
    result[index % modulus] +=
        (quotient % 2 == 0 ? 1 : -1) * row[index];
  }
  return result;
}

std::vector<int> NegacyclicNorm(const std::vector<int>& row) {
  const int modulus = static_cast<int>(row.size());
  std::vector<int> result(modulus);
  for (int left = 0; left < modulus; ++left) {
    for (int right = 0; right < modulus; ++right) {
      int exponent = left - right;
      int sign = 1;
      if (exponent < 0) {
        exponent += modulus;
        sign = -1;
      }
      result[exponent] += sign * row[left] * row[right];
    }
  }
  return result;
}

std::array<int, 3> IndependentNormSignature(
    const std::vector<int>& row) {
  const auto norm = NegacyclicNorm(row);
  std::array<int, 3> result{};
  const int independent = static_cast<int>(row.size()) / 2;
  if (independent != 1 && independent != 3) {
    throw std::runtime_error("only Phi4 and Phi4*Phi12 are implemented");
  }
  for (int index = 0; index < independent; ++index) {
    result[index] = norm[index];
  }
  if (norm[independent] != 0) {
    throw std::runtime_error("middle negacyclic norm coefficient is nonzero");
  }
  for (int index = 1; index < independent; ++index) {
    if (norm[row.size() - index] != -norm[index]) {
      throw std::runtime_error("negacyclic norm reflection failed");
    }
  }
  return result;
}

BlockSpecification MakeBlockSpecification(const Row& row,
                                          const std::vector<int>& cells,
                                          int modulus) {
  BlockSpecification result;
  result.modulus = modulus;
  result.baseline = ReducePolynomial(row, modulus);
  std::vector<std::vector<std::pair<int, int>>> contributions(modulus);
  for (int cell : cells) {
    const int quotient = cell / modulus;
    contributions[cell % modulus].push_back(
        {(quotient % 2 == 0 ? 1 : -1) * row[cell], cell});
  }
  for (int residue = 0; residue < modulus; ++residue) {
    struct LocalValue {
      std::uint64_t multiplicity;
      std::uint64_t representative_mask;
    };
    std::map<std::pair<int, int>, LocalValue> states;
    states[{0, result.baseline[residue]}] = {1, 0};
    for (const auto& [contribution, cell] : contributions[residue]) {
      auto next = states;
      for (const auto& [key, value] : states) {
        auto& target = next[{key.first + 1, key.second - contribution}];
        if (target.multiplicity == 0) {
          target.representative_mask =
              value.representative_mask | (1ULL << cell);
        }
        target.multiplicity += value.multiplicity;
      }
      states.swap(next);
    }
    std::vector<LocalOption> options;
    for (const auto& [key, value] : states) {
      options.push_back({key.first, key.second, value.multiplicity,
                         value.representative_mask});
    }
    result.options.push_back(std::move(options));
  }
  return result;
}

constexpr std::uint64_t kFieldMask = (1ULL << 13) - 1;
constexpr int kFieldBias = 4096;

std::uint64_t PackKey(int weight, int c0, int c1, int c2) {
  if (weight < 0 || weight >= 64 || c0 < 0 || c0 > 8191 ||
      c1 <= -4096 || c1 >= 4096 || c2 <= -4096 || c2 >= 4096) {
    throw std::runtime_error("histogram key exceeded packing range");
  }
  return static_cast<std::uint64_t>(weight) |
         (static_cast<std::uint64_t>(c0) << 6) |
         (static_cast<std::uint64_t>(c1 + kFieldBias) << 19) |
         (static_cast<std::uint64_t>(c2 + kFieldBias) << 32);
}

std::array<int, 4> UnpackKey(std::uint64_t key) {
  return {
      static_cast<int>(key & 63),
      static_cast<int>((key >> 6) & kFieldMask),
      static_cast<int>((key >> 19) & kFieldMask) - kFieldBias,
      static_cast<int>((key >> 32) & kFieldMask) - kFieldBias,
  };
}

std::array<int, 3> FastSignature(const std::vector<int>& values) {
  if (values.size() == 2) {
    return {values[0] * values[0] + values[1] * values[1], 0, 0};
  }
  if (values.size() != 6) {
    throw std::runtime_error("unexpected signature modulus");
  }
  const int a0 = values[0];
  const int a1 = values[1];
  const int a2 = values[2];
  const int a3 = values[3];
  const int a4 = values[4];
  const int a5 = values[5];
  return {
      a0 * a0 + a1 * a1 + a2 * a2 + a3 * a3 + a4 * a4 + a5 * a5,
      a1 * a0 + a2 * a1 + a3 * a2 + a4 * a3 + a5 * a4 - a0 * a5,
      a2 * a0 + a3 * a1 + a4 * a2 + a5 * a3 - a0 * a4 - a1 * a5,
  };
}

void EnumerateHistogram(const BlockSpecification& specification, int residue,
                        int weight, std::uint64_t multiplicity,
                        std::uint64_t representative_mask,
                        std::vector<int>* values, Histogram* histogram) {
  if (weight > kSupportWeight) return;
  if (residue == specification.modulus) {
    const auto signature = FastSignature(*values);
    if (signature[0] > kMaximumTargetEnergy) return;
    const auto key =
        PackKey(weight, signature[0], signature[1], signature[2]);
    auto& target = histogram->counts[key];
    if (target.count == 0) {
      target.representative_mask = representative_mask;
    }
    target.count += multiplicity;
    ++histogram->vector_tuples;
    return;
  }
  for (const auto& option : specification.options[residue]) {
    (*values)[residue] = option.value;
    EnumerateHistogram(specification, residue + 1,
                       weight + option.weight,
                       multiplicity * option.multiplicity,
                       representative_mask | option.representative_mask,
                       values, histogram);
  }
}

std::shared_ptr<Histogram> BuildHistogram(
    const BlockSpecification& specification) {
  auto result = std::make_shared<Histogram>();
  std::vector<int> values(specification.modulus);
  EnumerateHistogram(specification, 0, 0, 1, 0, &values, result.get());
  return result;
}

GrowthResult MeasureGrowth(const BlockSpecification& specification) {
  std::uint64_t raw = 1;
  for (const auto& group : specification.options) {
    raw *= group.size();
  }
  std::map<std::pair<int, int>, std::uint64_t> states;
  states[{0, 0}] = 1;
  for (const auto& group : specification.options) {
    std::map<std::pair<int, int>, std::uint64_t> next;
    for (const auto& [state, count] : states) {
      for (const auto& option : group) {
        const int weight = state.first + option.weight;
        const int energy = state.second + option.value * option.value;
        if (weight > kSupportWeight ||
            energy > kMaximumTargetEnergy) {
          continue;
        }
        next[{weight, energy}] += count;
      }
    }
    states.swap(next);
  }
  std::uint64_t admissible = 0;
  for (const auto& [state, count] : states) {
    static_cast<void>(state);
    admissible += count;
  }
  return {raw, admissible};
}

std::array<int, 3> TargetSignature(const std::array<Row, 4>& pair_rows,
                                   int modulus) {
  const auto r_signature =
      IndependentNormSignature(ReducePolynomial(pair_rows[2], modulus));
  const auto s_signature =
      IndependentNormSignature(ReducePolynomial(pair_rows[3], modulus));
  return {
      kTarget - r_signature[0] - s_signature[0],
      -r_signature[1] - s_signature[1],
      -r_signature[2] - s_signature[2],
  };
}

CaseResult JoinCase(
    int case_number, const Case& item, int modulus,
    std::map<std::string, std::shared_ptr<Histogram>>* cache) {
  const Rows adjusted = QAdjustedRows(item);
  const auto pair_rows = NormalizedPairRows(adjusted);
  const auto [long_cells, short_cells] = AvailableCells(item);
  const auto p_spec =
      MakeBlockSpecification(pair_rows[0], long_cells, modulus);
  const auto q_spec =
      MakeBlockSpecification(pair_rows[1], short_cells, modulus);

  auto get_histogram = [&](const BlockSpecification& specification) {
    const std::string fingerprint = specification.Fingerprint();
    auto found = cache->find(fingerprint);
    if (found != cache->end()) return found->second;
    const auto started = std::chrono::steady_clock::now();
    auto histogram = BuildHistogram(specification);
    const double seconds =
        std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                     started)
            .count();
    std::cerr << "built modulus=" << modulus
              << " histogram entries=" << histogram->counts.size()
              << " vectors=" << histogram->vector_tuples
              << " seconds=" << seconds << '\n';
    (*cache)[fingerprint] = histogram;
    return histogram;
  };

  const auto p_histogram = get_histogram(p_spec);
  const auto q_histogram = get_histogram(q_spec);
  const auto target = TargetSignature(pair_rows, modulus);
  WideUnsigned support_count = 0;
  std::uint64_t joined_signatures = 0;
  std::uint64_t long_support_mask = 0;
  std::uint64_t short_support_mask = 0;
  for (const auto& [packed, p_value] : p_histogram->counts) {
    const auto key = UnpackKey(packed);
    const int q_weight = kSupportWeight - key[0];
    if (q_weight < 0) continue;
    const int q_c0 = target[0] - key[1];
    const int q_c1 = target[1] - key[2];
    const int q_c2 = target[2] - key[3];
    if (q_c0 < 0 || q_c0 > kMaximumTargetEnergy ||
        q_c1 <= -4096 || q_c1 >= 4096 ||
        q_c2 <= -4096 || q_c2 >= 4096) {
      continue;
    }
    const auto wanted = PackKey(q_weight, q_c0, q_c1, q_c2);
    const auto found = q_histogram->counts.find(wanted);
    if (found == q_histogram->counts.end()) continue;
    support_count +=
        static_cast<WideUnsigned>(p_value.count) * found->second.count;
    if (joined_signatures == 0) {
      long_support_mask = p_value.representative_mask;
      short_support_mask = found->second.representative_mask;
    }
    ++joined_signatures;
  }
  return {
      case_number,
      item,
      target,
      support_count,
      joined_signatures,
      p_histogram->counts.size(),
      q_histogram->counts.size(),
      long_support_mask,
      short_support_mask,
  };
}

void SelfTest() {
  const auto cases = CanonicalCases();
  if (cases.front().block != 'L' || cases.front().index != 0 ||
      cases[1].index != 2 || cases[20].index != 36 ||
      cases[21].block != 'S' || cases[21].index != 2 ||
      cases.back().index != 18) {
    throw std::runtime_error("canonical case ordering changed");
  }
  const Rows seed = SeedAntifold();
  std::array<int, kFold> total_norm{};
  for (const Row& row : seed) {
    std::vector<int> values(row.begin(), row.end());
    const auto norm = NegacyclicNorm(values);
    for (int index = 0; index < kFold; ++index) {
      total_norm[index] += norm[index];
    }
  }
  const std::map<int, int> expected{
      {0, 654},   {4, -512}, {8, 384},  {12, -256}, {16, 128},
      {26, -128}, {30, 256}, {34, -384}, {38, 512},
  };
  std::map<int, int> actual;
  for (int index = 0; index < kFold; ++index) {
    if (total_norm[index] != 0) actual[index] = total_norm[index];
  }
  if (actual != expected) {
    throw std::runtime_error("seed anti-fold norm changed");
  }
  for (const int modulus : {2, 6}) {
    for (const Row& row : seed) {
      const auto direct =
          IndependentNormSignature(ReducePolynomial(row, modulus));
      const auto full = NegacyclicNorm(
          std::vector<int>(row.begin(), row.end()));
      Row full_row{};
      for (int index = 0; index < kFold; ++index) full_row[index] = full[index];
      const auto reduced_norm = ReducePolynomial(full_row, modulus);
      for (int index = 0; index < modulus / 2; ++index) {
        if (direct[index] != reduced_norm[index]) {
          throw std::runtime_error("norm reduction failed");
        }
      }
    }
  }
  for (const auto& values :
       {std::vector<int>{3, -4}, std::vector<int>{1, 2, -3, 4, -5, 6}}) {
    if (FastSignature(values) != IndependentNormSignature(values)) {
      throw std::runtime_error("fast norm signature failed");
    }
  }
}

void PrintJson(int modulus, const std::vector<CaseResult>& results,
               std::size_t unique_histograms, double seconds) {
  auto decimal = [](WideUnsigned value) {
    if (value == 0) return std::string("0");
    std::string result;
    while (value != 0) {
      result.push_back(static_cast<char>('0' + value % 10));
      value /= 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
  };
  auto support_json = [](std::uint64_t mask) {
    std::ostringstream out;
    out << '[';
    bool first = true;
    for (int cell = 0; cell < kFold; ++cell) {
      if ((mask & (1ULL << cell)) == 0) continue;
      if (!first) out << ", ";
      out << cell;
      first = false;
    }
    out << ']';
    return out.str();
  };
  std::cout << "{\n";
  std::cout << "  \"schema\": \"eliahou-cyclotomic-cascade-v1\",\n";
  std::cout << "  \"modulus\": " << modulus << ",\n";
  std::cout << "  \"factor\": \""
            << (modulus == 2 ? "Phi4" : "Phi4*Phi12") << "\",\n";
  std::cout << "  \"cases\": [\n";
  for (std::size_t index = 0; index < results.size(); ++index) {
    const auto& result = results[index];
    std::cout << "    {\"case\": " << result.case_number
              << ", \"block\": \"" << result.item.block
              << "\", \"q_index\": " << result.item.index
              << ", \"target_signature\": ["
              << result.target_signature[0] << ", "
              << result.target_signature[1] << ", "
              << result.target_signature[2] << "]"
              << ", \"support_count\": \""
              << decimal(result.support_count) << "\""
              << ", \"joined_signature_count\": "
              << result.joined_signature_count
              << ", \"p_histogram_entries\": "
              << result.p_histogram_entries
              << ", \"q_histogram_entries\": "
              << result.q_histogram_entries
              << ", \"representative_long_support\": "
              << support_json(result.long_support_mask)
              << ", \"representative_short_support\": "
              << support_json(result.short_support_mask) << "}";
    if (index + 1 != results.size()) std::cout << ',';
    std::cout << '\n';
  }
  std::cout << "  ],\n";
  std::cout << "  \"unique_histograms\": " << unique_histograms << ",\n";
  std::cout << "  \"seconds\": " << seconds << "\n";
  std::cout << "}\n";
}

void PrintGrowthJson(const std::vector<Case>& cases) {
  struct Record {
    char side;
    std::vector<int> cases;
    GrowthResult growth;
    std::vector<std::size_t> local_option_counts;
  };
  std::map<std::string, Record> records;
  for (int case_number = 0;
       case_number < static_cast<int>(cases.size()); ++case_number) {
    const auto& item = cases[case_number];
    const auto pair_rows = NormalizedPairRows(QAdjustedRows(item));
    const auto [long_cells, short_cells] = AvailableCells(item);
    const std::array<std::pair<char, BlockSpecification>, 2> specifications{
        std::pair<char, BlockSpecification>{
            'P', MakeBlockSpecification(pair_rows[0], long_cells, 14)},
        std::pair<char, BlockSpecification>{
            'Q', MakeBlockSpecification(pair_rows[1], short_cells, 14)},
    };
    for (const auto& [side, specification] : specifications) {
      const std::string key =
          std::string(1, side) + specification.ArithmeticFingerprint();
      auto found = records.find(key);
      if (found == records.end()) {
        std::vector<std::size_t> sizes;
        for (const auto& group : specification.options) {
          sizes.push_back(group.size());
        }
        found =
            records
                .emplace(key,
                         Record{side, {}, MeasureGrowth(specification), sizes})
                .first;
      }
      found->second.cases.push_back(case_number);
    }
  }

  auto decimal = [](WideUnsigned value) {
    if (value == 0) return std::string("0");
    std::string result;
    while (value != 0) {
      result.push_back(static_cast<char>('0' + value % 10));
      value /= 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
  };
  WideUnsigned total_raw = 0;
  WideUnsigned total_admissible = 0;
  std::uint64_t maximum_raw = 0;
  std::cout << "{\n";
  std::cout << "  \"schema\": \"eliahou-cyclotomic-growth-v1\",\n";
  std::cout << "  \"modulus\": 14,\n";
  std::cout << "  \"factor\": \"Phi4*Phi28\",\n";
  std::cout << "  \"specifications\": [\n";
  std::size_t record_number = 0;
  for (const auto& [key, record] : records) {
    static_cast<void>(key);
    total_raw += record.growth.raw_vector_tuples;
    total_admissible += record.growth.energy_admissible_vector_tuples;
    maximum_raw =
        std::max(maximum_raw, record.growth.raw_vector_tuples);
    std::cout << "    {\"side\": \"" << record.side << "\", \"cases\": [";
    for (std::size_t index = 0; index < record.cases.size(); ++index) {
      if (index) std::cout << ", ";
      std::cout << record.cases[index];
    }
    std::cout << "], \"local_option_counts\": [";
    for (std::size_t index = 0;
         index < record.local_option_counts.size(); ++index) {
      if (index) std::cout << ", ";
      std::cout << record.local_option_counts[index];
    }
    std::cout << "], \"raw_vector_tuples\": "
              << record.growth.raw_vector_tuples
              << ", \"energy_admissible_vector_tuples\": "
              << record.growth.energy_admissible_vector_tuples << "}";
    if (++record_number != records.size()) std::cout << ',';
    std::cout << '\n';
  }
  std::cout << "  ],\n";
  std::cout << "  \"unique_specifications\": " << records.size() << ",\n";
  std::cout << "  \"total_raw_vector_tuples\": \""
            << decimal(total_raw) << "\",\n";
  std::cout << "  \"total_energy_admissible_vector_tuples\": \""
            << decimal(total_admissible) << "\",\n";
  std::cout << "  \"maximum_raw_vector_tuples\": "
            << maximum_raw << "\n";
  std::cout << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
  try {
    SelfTest();
    int modulus = 0;
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
      std::cout << "PASS: cyclotomic cascade algebra self-test\n";
      return 0;
    }
    if (argc == 3 && std::string(argv[1]) == "--growth" &&
        std::string(argv[2]) == "14") {
      PrintGrowthJson(CanonicalCases());
      return 0;
    }
    if (argc == 3 && std::string(argv[1]) == "--modulus") {
      modulus = std::stoi(argv[2]);
    } else {
      throw std::runtime_error(
          "usage: audit_cyclotomic_cascade --self-test | "
          "--modulus 2|6 | --growth 14");
    }
    if (modulus != 2 && modulus != 6) {
      throw std::runtime_error("implemented moduli are 2 and 6");
    }
    const auto started = std::chrono::steady_clock::now();
    const auto cases = CanonicalCases();
    std::map<std::string, std::shared_ptr<Histogram>> cache;
    std::vector<CaseResult> results;
    for (int index = 0; index < static_cast<int>(cases.size()); ++index) {
      results.push_back(JoinCase(index, cases[index], modulus, &cache));
    }
    const double seconds =
        std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                     started)
            .count();
    PrintJson(modulus, results, cache.size(), seconds);
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
