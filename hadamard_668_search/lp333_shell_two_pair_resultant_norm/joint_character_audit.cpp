#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int P = 167;
constexpr int D = 12;
constexpr int FACTORS = 6;
constexpr int CLASSES = 12;
using U128 = unsigned __int128;

struct E {
  std::array<uint8_t, D> a{};
  bool operator==(const E &other) const { return a == other.a; }
  bool operator!=(const E &other) const { return !(*this == other); }
};

std::array<int, D> theta_relation{};

int reduce(int value) {
  value %= P;
  if (value < 0) value += P;
  return value;
}

E one() {
  E result;
  result.a[0] = 1;
  return result;
}

E add(const E &left, const E &right) {
  E result;
  for (int i = 0; i < D; ++i) {
    result.a[i] = static_cast<uint8_t>((left.a[i] + right.a[i]) % P);
  }
  return result;
}

E multiply(const E &left, const E &right) {
  std::array<int, 2 * D - 1> work{};
  for (int i = 0; i < D; ++i) {
    if (!left.a[i]) continue;
    for (int j = 0; j < D; ++j) {
      work[i + j] += static_cast<int>(left.a[i]) * right.a[j];
      work[i + j] %= P;
    }
  }
  for (int degree = 2 * D - 2; degree >= D; --degree) {
    int coefficient = reduce(work[degree]);
    if (!coefficient) continue;
    for (int i = 0; i < D; ++i) {
      work[degree - D + i] += coefficient * theta_relation[i];
      work[degree - D + i] %= P;
    }
  }
  E result;
  for (int i = 0; i < D; ++i) {
    result.a[i] = static_cast<uint8_t>(reduce(work[i]));
  }
  return result;
}

E power(E base, U128 exponent) {
  E result = one();
  while (exponent) {
    if (exponent & 1) result = multiply(result, base);
    base = multiply(base, base);
    exponent >>= 1;
  }
  return result;
}

bool is_zero(const E &value) {
  return std::all_of(value.a.begin(), value.a.end(),
                     [](uint8_t entry) { return entry == 0; });
}

uint32_t read_u32(std::ifstream &input) {
  std::array<unsigned char, 4> bytes{};
  input.read(reinterpret_cast<char *>(bytes.data()), bytes.size());
  if (!input) throw std::runtime_error("truncated u32");
  return static_cast<uint32_t>(bytes[0])
       | (static_cast<uint32_t>(bytes[1]) << 8)
       | (static_cast<uint32_t>(bytes[2]) << 16)
       | (static_cast<uint32_t>(bytes[3]) << 24);
}

E read_e(std::ifstream &input) {
  E result;
  input.read(reinterpret_cast<char *>(result.a.data()), D);
  if (!input) throw std::runtime_error("truncated field element");
  for (auto value : result.a) {
    if (value >= P) throw std::runtime_error("noncanonical field coordinate");
  }
  return result;
}

struct Factor {
  E constant;
  std::array<std::vector<E>, CLASSES> options;
};

struct Case {
  std::string label;
  uint8_t channel = 0;
  std::array<uint8_t, CLASSES> profile_ids{};
  std::array<Factor, FACTORS> factors;
};

std::vector<Case> read_input(const std::string &path) {
  std::ifstream input(path, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open input");
  std::array<char, 9> magic{};
  input.read(magic.data(), magic.size());
  if (std::string(magic.data(), magic.size()) != "H668CHAR1") {
    throw std::runtime_error("wrong input magic");
  }
  for (int i = 0; i < D; ++i) {
    unsigned char value;
    input.read(reinterpret_cast<char *>(&value), 1);
    if (!input || value >= P) throw std::runtime_error("bad field relation");
    theta_relation[i] = value;
  }
  uint32_t count = read_u32(input);
  std::vector<Case> result(count);
  for (auto &item : result) {
    uint32_t label_length = read_u32(input);
    item.label.resize(label_length);
    input.read(item.label.data(), label_length);
    input.read(reinterpret_cast<char *>(&item.channel), 1);
    input.read(reinterpret_cast<char *>(item.profile_ids.data()), CLASSES);
    if (!input || item.channel > 1) throw std::runtime_error("bad case header");
    for (auto &factor : item.factors) {
      factor.constant = read_e(input);
      for (auto &options : factor.options) {
        uint32_t option_count = read_u32(input);
        if (option_count == 0 || option_count > 27) {
          throw std::runtime_error("bad option count");
        }
        options.resize(option_count);
        for (auto &value : options) value = read_e(input);
      }
    }
    for (int factor = 1; factor < FACTORS; ++factor) {
      for (int cls = 0; cls < CLASSES; ++cls) {
        if (item.factors[factor].options[cls].size()
            != item.factors[0].options[cls].size()) {
          throw std::runtime_error("factor option counts disagree");
        }
      }
    }
  }
  char trailing;
  if (input.read(&trailing, 1)) throw std::runtime_error("trailing input");
  return result;
}

struct XorShift64 {
  uint64_t state;
  explicit XorShift64(uint64_t seed) : state(seed ? seed : 1) {}
  uint64_t next() {
    uint64_t x = state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    state = x;
    return x;
  }
};

std::vector<int> prime_divisors(int value) {
  std::vector<int> result;
  for (int divisor = 2; divisor * divisor <= value; ++divisor) {
    if (value % divisor) continue;
    result.push_back(divisor);
    while (value % divisor == 0) value /= divisor;
  }
  if (value > 1) result.push_back(value);
  return result;
}

E root_generator(int order, U128 group_order) {
  U128 exponent = group_order / static_cast<unsigned>(order);
  E unity = one();
  for (int seed = 1; seed < 10000; ++seed) {
    E candidate;
    candidate.a[0] = static_cast<uint8_t>(seed % P);
    candidate.a[1] = static_cast<uint8_t>((seed / P + 1) % P);
    E root = power(candidate, exponent);
    if (is_zero(root) || power(root, order) != unity) continue;
    bool exact = true;
    for (int prime : prime_divisors(order)) {
      if (power(root, order / prime) == unity) {
        exact = false;
        break;
      }
    }
    if (exact) return root;
  }
  throw std::runtime_error("failed to find a character root generator");
}

uint64_t integer_power(uint64_t base, int exponent) {
  uint64_t result = 1;
  while (exponent--) {
    if (result > std::numeric_limits<uint64_t>::max() / base) {
      throw std::runtime_error("signature space overflow");
    }
    result *= base;
  }
  return result;
}

struct AuditResult {
  uint64_t samples = 0;
  uint64_t signatures = 0;
  uint64_t target = 0;
  bool complete = false;
  std::vector<std::array<uint8_t, CLASSES>> witnesses;
};

AuditResult audit_product_case(const Case &item, int order, U128 group_order,
                               uint64_t max_samples, uint64_t seed) {
  E generator = root_generator(order, group_order);
  std::vector<E> roots(order);
  roots[0] = one();
  for (int i = 1; i < order; ++i) {
    roots[i] = multiply(roots[i - 1], generator);
  }
  if (multiply(roots.back(), generator) != roots[0]) {
    throw std::runtime_error("character roots do not close");
  }
  U128 exponent = group_order / static_cast<unsigned>(order);
  uint64_t target = static_cast<uint64_t>(order);
  std::vector<uint8_t> seen(target, 0);
  std::vector<std::array<uint8_t, CLASSES>> witnesses(target);
  XorShift64 rng(seed);
  uint64_t found = 0;
  uint64_t samples = 0;
  for (; samples < max_samples && found < target; ++samples) {
    std::array<uint8_t, CLASSES> choices{};
    for (int cls = 0; cls < CLASSES; ++cls) {
      choices[cls] = static_cast<uint8_t>(
          rng.next() % item.factors[0].options[cls].size());
    }
    E product = one();
    for (int factor = 0; factor < FACTORS; ++factor) {
      E value = item.factors[factor].constant;
      for (int cls = 0; cls < CLASSES; ++cls) {
        value = add(value,
                    item.factors[factor].options[cls][choices[cls]]);
      }
      if (is_zero(value)) {
        throw std::runtime_error("primitive-unit theorem replay failed");
      }
      product = multiply(product, value);
    }
    E character = power(product, exponent);
    auto position = std::find(roots.begin(), roots.end(), character);
    if (position == roots.end()) {
      throw std::runtime_error("product character left root group");
    }
    uint64_t index = static_cast<uint64_t>(position - roots.begin());
    if (!seen[index]) {
      seen[index] = 1;
      witnesses[index] = choices;
      ++found;
    }
  }
  // Exact deterministic replay of every retained image witness.
  for (uint64_t expected = 0; expected < target; ++expected) {
    if (!seen[expected]) continue;
    E product = one();
    const auto &choices = witnesses[expected];
    for (int factor = 0; factor < FACTORS; ++factor) {
      E value = item.factors[factor].constant;
      for (int cls = 0; cls < CLASSES; ++cls) {
        value = add(value,
                    item.factors[factor].options[cls][choices[cls]]);
      }
      product = multiply(product, value);
    }
    E character = power(product, exponent);
    if (character != roots[expected]) {
      throw std::runtime_error("product witness replay failed");
    }
  }
  return {samples, found, target, found == target, std::move(witnesses)};
}

AuditResult audit_case(const Case &item, int order, U128 group_order,
                       uint64_t max_samples, uint64_t seed) {
  E generator = root_generator(order, group_order);
  std::vector<E> roots(order);
  roots[0] = one();
  for (int i = 1; i < order; ++i) {
    roots[i] = multiply(roots[i - 1], generator);
  }
  if (multiply(roots.back(), generator) != roots[0]) {
    throw std::runtime_error("character roots do not close");
  }
  U128 exponent = group_order / static_cast<unsigned>(order);
  uint64_t target = integer_power(order, FACTORS);
  std::vector<uint8_t> seen(target, 0);
  std::vector<std::array<uint8_t, CLASSES>> witnesses(target);
  XorShift64 rng(seed);
  uint64_t found = 0;
  uint64_t samples = 0;
  for (; samples < max_samples && found < target; ++samples) {
    std::array<uint8_t, CLASSES> choices{};
    for (int cls = 0; cls < CLASSES; ++cls) {
      choices[cls] = static_cast<uint8_t>(
          rng.next() % item.factors[0].options[cls].size());
    }
    uint64_t signature = 0;
    uint64_t multiplier = 1;
    for (int factor = 0; factor < FACTORS; ++factor) {
      E value = item.factors[factor].constant;
      for (int cls = 0; cls < CLASSES; ++cls) {
        value = add(value,
                    item.factors[factor].options[cls][choices[cls]]);
      }
      if (is_zero(value)) {
        throw std::runtime_error("primitive-unit theorem replay failed");
      }
      E character = power(value, exponent);
      int index = -1;
      for (int candidate = 0; candidate < order; ++candidate) {
        if (character == roots[candidate]) {
          index = candidate;
          break;
        }
      }
      if (index < 0) throw std::runtime_error("character left root group");
      signature += multiplier * static_cast<uint64_t>(index);
      multiplier *= order;
    }
    if (!seen[signature]) {
      seen[signature] = 1;
      witnesses[signature] = choices;
      ++found;
    }
  }
  // Replay every retained witness through a fresh exact evaluation.
  for (uint64_t expected = 0; expected < target; ++expected) {
    if (!seen[expected]) continue;
    const auto &choices = witnesses[expected];
    uint64_t signature = 0;
    uint64_t multiplier = 1;
    for (int factor = 0; factor < FACTORS; ++factor) {
      E value = item.factors[factor].constant;
      for (int cls = 0; cls < CLASSES; ++cls) {
        value = add(value,
                    item.factors[factor].options[cls][choices[cls]]);
      }
      E character = power(value, exponent);
      auto position = std::find(roots.begin(), roots.end(), character);
      if (position == roots.end()) {
        throw std::runtime_error("witness character left root group");
      }
      signature += multiplier
                 * static_cast<uint64_t>(position - roots.begin());
      multiplier *= order;
    }
    if (signature != expected) {
      throw std::runtime_error("witness signature replay failed");
    }
  }
  return {samples, found, target, found == target, std::move(witnesses)};
}

std::string u128_string(U128 value) {
  if (!value) return "0";
  std::string result;
  while (value) {
    result.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  }
  std::reverse(result.begin(), result.end());
  return result;
}

std::string e_string(const E &value) {
  std::string result;
  for (int i = 0; i < D; ++i) {
    if (i) result.push_back(',');
    result += std::to_string(static_cast<unsigned>(value.a[i]));
  }
  return result;
}

int modular_inverse(int value, int prime) {
  int64_t old_r = value;
  int64_t r = prime;
  int64_t old_s = 1;
  int64_t s = 0;
  while (r) {
    int64_t quotient = old_r / r;
    int64_t next_r = old_r - quotient * r;
    old_r = r;
    r = next_r;
    int64_t next_s = old_s - quotient * s;
    old_s = s;
    s = next_s;
  }
  if (old_r != 1) throw std::runtime_error("noninvertible modular pivot");
  int result = static_cast<int>(old_s % prime);
  if (result < 0) result += prime;
  return result;
}

int affine_rank(
    const std::vector<std::array<int, 3>> &points, int prime) {
  if (points.size() <= 1) return 0;
  std::vector<std::array<int, 3>> matrix;
  for (size_t i = 1; i < points.size(); ++i) {
    std::array<int, 3> row{};
    for (int column = 0; column < 3; ++column) {
      row[column] = points[i][column] - points[0][column];
      row[column] %= prime;
      if (row[column] < 0) row[column] += prime;
    }
    matrix.push_back(row);
  }
  int rank = 0;
  for (int column = 0; column < 3; ++column) {
    int pivot = -1;
    for (int row = rank; row < static_cast<int>(matrix.size()); ++row) {
      if (matrix[row][column]) {
        pivot = row;
        break;
      }
    }
    if (pivot < 0) continue;
    std::swap(matrix[rank], matrix[pivot]);
    int scale = modular_inverse(matrix[rank][column], prime);
    for (int entry = 0; entry < 3; ++entry) {
      matrix[rank][entry] =
          static_cast<int>(
              static_cast<int64_t>(matrix[rank][entry]) * scale % prime);
    }
    for (int row = 0; row < static_cast<int>(matrix.size()); ++row) {
      if (row == rank || !matrix[row][column]) continue;
      int factor = matrix[row][column];
      for (int entry = 0; entry < 3; ++entry) {
        matrix[row][entry] = static_cast<int>(
            (matrix[row][entry]
             - static_cast<int64_t>(factor) * matrix[rank][entry])
            % prime);
        if (matrix[row][entry] < 0) matrix[row][entry] += prime;
      }
    }
    ++rank;
    if (rank == 3) break;
  }
  return rank;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc < 3 || argc > 5) {
      std::cerr
          << "usage: joint_character_audit INPUT ORDER [MAX_SAMPLES]"
          << " [joint|product|pairspan|pairmargins|probe]\n";
      return 2;
    }
    std::string input_path = argv[1];
    int order = std::stoi(argv[2]);
    uint64_t max_samples = argc == 4
        ? std::stoull(argv[3])
        : 1000000;
    if (argc >= 4) max_samples = std::stoull(argv[3]);
    std::string mode = argc >= 5 ? argv[4] : "joint";
    if (mode != "joint" && mode != "product"
        && mode != "pairspan" && mode != "pairmargins"
        && mode != "probe") {
      throw std::runtime_error(
          "mode must be joint, product, pairspan, pairmargins, or probe");
    }
    U128 field_size = 1;
    for (int i = 0; i < D; ++i) field_size *= P;
    U128 group_order = field_size - 1;
    if (order < 2 || group_order % static_cast<unsigned>(order)) {
      throw std::runtime_error("order does not divide 167^12-1");
    }
    auto cases = read_input(input_path);
    auto started = std::chrono::steady_clock::now();
    uint64_t total_samples = 0;
    uint64_t complete_cases = 0;
    std::cout << "schema=h668-joint-character-audit-v1\n";
    std::cout << "field_size=" << u128_string(field_size) << "\n";
    std::cout << "character_order=" << order << "\n";
    std::cout << "mode=" << mode << "\n";
    std::cout << "cases=" << cases.size() << "\n";
    if (mode == "probe") {
      E root = root_generator(order, group_order);
      U128 exponent = group_order / static_cast<unsigned>(order);
      std::vector<E> roots(order);
      roots[0] = one();
      for (int i = 1; i < order; ++i) {
        roots[i] = multiply(roots[i - 1], root);
      }
      for (size_t index = 0; index < cases.size(); ++index) {
        E product = one();
        for (int factor = 0; factor < FACTORS; ++factor) {
          E value = cases[index].factors[factor].constant;
          for (int cls = 0; cls < CLASSES; ++cls) {
            size_t count =
                cases[index].factors[factor].options[cls].size();
            size_t choice =
                ((index + 1) * static_cast<size_t>(cls + 3) + 7) % count;
            value = add(
                value,
                cases[index].factors[factor].options[cls][choice]);
          }
          product = multiply(product, value);
        }
        E character = power(product, exponent);
        auto position = std::find(roots.begin(), roots.end(), character);
        if (position == roots.end()) {
          throw std::runtime_error("probe character left root group");
        }
        std::cout << "probe=" << index
                  << " product=" << e_string(product)
                  << " character=" << e_string(character)
                  << " character_index=" << (position - roots.begin())
                  << "\n";
      }
      return 0;
    }
    if (mode == "pairspan") {
      if (!prime_divisors(order).empty()
          && (prime_divisors(order).size() != 1
              || prime_divisors(order)[0] != order)) {
        throw std::runtime_error("pairspan requires prime character order");
      }
      E root = root_generator(order, group_order);
      U128 exponent = group_order / static_cast<unsigned>(order);
      std::vector<E> roots(order);
      roots[0] = one();
      for (int i = 1; i < order; ++i) {
        roots[i] = multiply(roots[i - 1], root);
      }
      uint64_t complete_cases = 0;
      uint64_t total_samples = 0;
      auto started = std::chrono::steady_clock::now();
      for (size_t index = 0; index < cases.size(); ++index) {
        XorShift64 rng(
            UINT64_C(0x6a09e667f3bcc909)
            ^ (static_cast<uint64_t>(order) << 32)
            ^ (index * UINT64_C(0x94d049bb133111eb)));
        std::vector<std::array<int, 3>> points;
        int rank = 0;
        uint64_t samples = 0;
        for (; samples < max_samples && rank < 3; ++samples) {
          std::array<uint8_t, CLASSES> choices{};
          for (int cls = 0; cls < CLASSES; ++cls) {
            choices[cls] = static_cast<uint8_t>(
                rng.next() % cases[index].factors[0].options[cls].size());
          }
          std::array<E, FACTORS> values;
          for (int factor = 0; factor < FACTORS; ++factor) {
            values[factor] = cases[index].factors[factor].constant;
            for (int cls = 0; cls < CLASSES; ++cls) {
              values[factor] = add(
                  values[factor],
                  cases[index].factors[factor].options[cls][choices[cls]]);
            }
          }
          std::array<int, 3> point{};
          for (int pair = 0; pair < 3; ++pair) {
            E pair_product = multiply(values[pair], values[pair + 3]);
            E character = power(pair_product, exponent);
            auto position = std::find(roots.begin(), roots.end(), character);
            if (position == roots.end()) {
              throw std::runtime_error("pair character left root group");
            }
            point[pair] = static_cast<int>(position - roots.begin());
          }
          points.push_back(point);
          rank = affine_rank(points, order);
        }
        total_samples += samples;
        complete_cases += rank == 3;
        std::cout << "case=" << index
                  << " label=" << cases[index].label
                  << " affine_rank=" << rank
                  << "/3 samples=" << samples
                  << " complete=" << (rank == 3 ? "true" : "false")
                  << "\n";
      }
      auto stopped = std::chrono::steady_clock::now();
      std::chrono::duration<double> elapsed = stopped - started;
      std::cout << "complete_cases=" << complete_cases
                << "/" << cases.size() << "\n";
      std::cout << "total_samples=" << total_samples << "\n";
      std::cout << std::fixed << std::setprecision(6)
                << "wall_seconds=" << elapsed.count() << "\n";
      return complete_cases == cases.size() ? 0 : 1;
    }
    if (mode == "pairmargins") {
      E root = root_generator(order, group_order);
      U128 exponent = group_order / static_cast<unsigned>(order);
      std::vector<E> roots(order);
      roots[0] = one();
      for (int i = 1; i < order; ++i) {
        roots[i] = multiply(roots[i - 1], root);
      }
      uint64_t complete_cases = 0;
      uint64_t total_samples = 0;
      auto started = std::chrono::steady_clock::now();
      for (size_t index = 0; index < cases.size(); ++index) {
        XorShift64 rng(
            UINT64_C(0x510e527fade682d1)
            ^ (static_cast<uint64_t>(order) << 32)
            ^ (index * UINT64_C(0x9e3779b97f4a7c15)));
        std::array<std::vector<uint8_t>, 3> seen;
        std::array<std::vector<std::array<uint8_t, CLASSES>>, 3> witnesses;
        for (int pair = 0; pair < 3; ++pair) {
          seen[pair].assign(order, 0);
          witnesses[pair].resize(order);
        }
        uint64_t found = 0;
        uint64_t target = 3 * static_cast<uint64_t>(order);
        uint64_t samples = 0;
        for (; samples < max_samples && found < target; ++samples) {
          std::array<uint8_t, CLASSES> choices{};
          for (int cls = 0; cls < CLASSES; ++cls) {
            choices[cls] = static_cast<uint8_t>(
                rng.next() % cases[index].factors[0].options[cls].size());
          }
          std::array<E, FACTORS> values;
          for (int factor = 0; factor < FACTORS; ++factor) {
            values[factor] = cases[index].factors[factor].constant;
            for (int cls = 0; cls < CLASSES; ++cls) {
              values[factor] = add(
                  values[factor],
                  cases[index].factors[factor].options[cls][choices[cls]]);
            }
          }
          for (int pair = 0; pair < 3; ++pair) {
            E character = power(
                multiply(values[pair], values[pair + 3]), exponent);
            auto position = std::find(roots.begin(), roots.end(), character);
            if (position == roots.end()) {
              throw std::runtime_error("pair character left root group");
            }
            int value = static_cast<int>(position - roots.begin());
            if (!seen[pair][value]) {
              seen[pair][value] = 1;
              witnesses[pair][value] = choices;
              ++found;
            }
          }
        }
        // Exact replay of one retained physical assignment for each value in
        // each of the three pair-coordinate images.
        for (int pair = 0; pair < 3; ++pair) {
          for (int expected = 0; expected < order; ++expected) {
            if (!seen[pair][expected]) continue;
            const auto &choices = witnesses[pair][expected];
            E left = cases[index].factors[pair].constant;
            E right = cases[index].factors[pair + 3].constant;
            for (int cls = 0; cls < CLASSES; ++cls) {
              left = add(
                  left,
                  cases[index].factors[pair].options[cls][choices[cls]]);
              right = add(
                  right,
                  cases[index].factors[pair + 3].options[cls][choices[cls]]);
            }
            E character = power(multiply(left, right), exponent);
            if (character != roots[expected]) {
              throw std::runtime_error("pair-margin witness replay failed");
            }
          }
        }
        total_samples += samples;
        complete_cases += found == target;
        std::cout << "case=" << index
                  << " label=" << cases[index].label
                  << " marginal_values=" << found
                  << "/" << target
                  << " samples=" << samples
                  << " complete=" << (found == target ? "true" : "false")
                  << "\n";
      }
      auto stopped = std::chrono::steady_clock::now();
      std::chrono::duration<double> elapsed = stopped - started;
      std::cout << "complete_cases=" << complete_cases
                << "/" << cases.size() << "\n";
      std::cout << "total_samples=" << total_samples << "\n";
      std::cout << std::fixed << std::setprecision(6)
                << "wall_seconds=" << elapsed.count() << "\n";
      return complete_cases == cases.size() ? 0 : 1;
    }
    for (size_t index = 0; index < cases.size(); ++index) {
      uint64_t seed = UINT64_C(0x9e3779b97f4a7c15)
                    ^ (static_cast<uint64_t>(order) << 48)
                    ^ (index * UINT64_C(0xbf58476d1ce4e5b9));
      auto result = mode == "joint"
          ? audit_case(cases[index], order, group_order, max_samples, seed)
          : audit_product_case(
                cases[index], order, group_order, max_samples, seed);
      total_samples += result.samples;
      complete_cases += result.complete;
      std::cout << "case=" << index
                << " label=" << cases[index].label
                << " signatures=" << result.signatures
                << "/" << result.target
                << " samples=" << result.samples
                << " complete=" << (result.complete ? "true" : "false")
                << "\n";
    }
    auto stopped = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = stopped - started;
    std::cout << "complete_cases=" << complete_cases
              << "/" << cases.size() << "\n";
    std::cout << "total_samples=" << total_samples << "\n";
    std::cout << std::fixed << std::setprecision(6)
              << "wall_seconds=" << elapsed.count() << "\n";
    return complete_cases == cases.size() ? 0 : 1;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 2;
  }
}
