// Sparse exact diagnostics for one rotation/complement orbit.
//
// Compile:
//   c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
//       src/targeted_orbit.cpp -o targeted_orbit
//
// Run:
//   ./targeted_orbit --word 0000001111001111
//   ./targeted_orbit --word 0000001111001111 --members

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint64_t;
using Count = std::uint64_t;

constexpr Mask empty_slot = std::numeric_limits<Mask>::max();

class FlatSet {
 public:
  explicit FlatSet(const std::size_t initial_capacity = 1024) {
    std::size_t capacity = 1;
    while (capacity < initial_capacity) {
      capacity *= 2;
    }
    table_.assign(capacity, empty_slot);
  }

  void clear() {
    std::fill(table_.begin(), table_.end(), empty_slot);
    size_ = 0;
  }

  void reserve(const std::size_t requested_size) {
    std::size_t capacity = table_.size();
    while (requested_size * 10 >= capacity * 7) {
      capacity *= 2;
    }
    if (capacity != table_.size()) {
      rehash(capacity);
    }
  }

  bool contains(const Mask value) const {
    std::size_t index = bucket(value);
    while (table_[index] != empty_slot) {
      if (table_[index] == value) {
        return true;
      }
      index = (index + 1) & (table_.size() - 1);
    }
    return false;
  }

  bool insert(const Mask value) {
    if ((size_ + 1) * 10 >= table_.size() * 7) {
      rehash(2 * table_.size());
    }
    return insert_without_growth(value);
  }

 private:
  static Mask mix(Mask value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
  }

  std::size_t bucket(const Mask value) const {
    return static_cast<std::size_t>(mix(value)) & (table_.size() - 1);
  }

  bool insert_without_growth(const Mask value) {
    std::size_t index = bucket(value);
    while (table_[index] != empty_slot) {
      if (table_[index] == value) {
        return false;
      }
      index = (index + 1) & (table_.size() - 1);
    }
    table_[index] = value;
    ++size_;
    return true;
  }

  void rehash(const std::size_t capacity) {
    std::vector<Mask> old_table = std::move(table_);
    table_.assign(capacity, empty_slot);
    size_ = 0;
    for (const Mask value : old_table) {
      if (value != empty_slot) {
        insert_without_growth(value);
      }
    }
  }

  std::vector<Mask> table_;
  std::size_t size_ = 0;
};

struct Options {
  std::string word;
  bool members = false;
};

struct PerPCounts {
  Count q;
  Count e;
};

Mask value_bit(const int m, const int value) {
  if (value < -m || value > m) {
    throw std::logic_error("signature value lies outside [-m,m]");
  }
  return Mask{1} << (value + m);
}

Mask rotate_one(const Mask word, const int length, const Mask word_mask) {
  return ((word << 1) & word_mask) | (word >> (length - 1));
}

int equal_adjacencies(const Mask word,
                      const int length,
                      const Mask word_mask) {
  return length -
         __builtin_popcountll(word ^ rotate_one(word, length, word_mask));
}

Mask parse_word(const std::string& word) {
  Mask result = 0;
  for (std::size_t index = 0; index < word.size(); ++index) {
    if (word[index] == '1') {
      result |= Mask{1} << index;
    } else if (word[index] != '0') {
      throw std::invalid_argument("the word must contain only 0 and 1");
    }
  }
  return result;
}

std::string word_string(const Mask word, const int length) {
  std::string result;
  result.reserve(static_cast<std::size_t>(length));
  for (int index = 0; index < length; ++index) {
    result.push_back((word & (Mask{1} << index)) != 0 ? '1' : '0');
  }
  return result;
}

bool word_less(const Mask left, const Mask right, const int length) {
  for (int index = 0; index < length; ++index) {
    const bool left_bit = (left & (Mask{1} << index)) != 0;
    const bool right_bit = (right & (Mask{1} << index)) != 0;
    if (left_bit != right_bit) {
      return !left_bit;
    }
  }
  return false;
}

std::vector<Mask> orbit_elements(const Mask word,
                                 const int length,
                                 const Mask word_mask) {
  std::vector<Mask> elements;
  elements.reserve(static_cast<std::size_t>(2 * length));
  Mask rotated = word;
  for (int step = 0; step < length; ++step) {
    elements.push_back(rotated);
    elements.push_back(rotated ^ word_mask);
    rotated = rotate_one(rotated, length, word_mask);
  }
  std::sort(elements.begin(), elements.end());
  elements.erase(std::unique(elements.begin(), elements.end()),
                 elements.end());
  return elements;
}

Mask generator_mask(const int m, const Mask p_mask, const int b) {
  Mask result = value_bit(m, b) | value_bit(m, -b);
  Mask remaining = p_mask;
  while (remaining != 0) {
    const unsigned index =
        static_cast<unsigned>(__builtin_ctzll(remaining));
    const int p = static_cast<int>(index) + 1;
    const int value = b - p;
    if (-m <= value && value <= m) {
      result |= value_bit(m, value);
    }
    remaining &= remaining - 1;
  }
  return result;
}

Mask v0_mask(const int m, const Mask p_mask) {
  Mask result = 0;
  Mask remaining = p_mask;
  while (remaining != 0) {
    const unsigned index =
        static_cast<unsigned>(__builtin_ctzll(remaining));
    const int p = static_cast<int>(index) + 1;
    result |= value_bit(m, m + 1 - p);
    remaining &= remaining - 1;
  }
  return result;
}

class SignatureCounter {
 public:
  explicit SignatureCounter(const int m) : m_(m) {
    generators_.reserve(static_cast<std::size_t>(2 * m));
    family_.reserve(4096);
  }

  PerPCounts compute(const Mask p_mask) {
    generators_.clear();
    for (int b = -m_; b <= m_; ++b) {
      if (b == 0) {
        continue;
      }
      const Mask generator = generator_mask(m_, p_mask, b);
      if (std::find(generators_.begin(), generators_.end(), generator) ==
          generators_.end()) {
        generators_.push_back(generator);
      }
    }
    std::sort(generators_.begin(), generators_.end(),
              [](const Mask left, const Mask right) {
                const int left_size = __builtin_popcountll(left);
                const int right_size = __builtin_popcountll(right);
                if (left_size != right_size) {
                  return left_size > right_size;
                }
                return left > right;
              });

    family_lookup_.clear();
    family_.clear();
    family_lookup_.insert(0);
    family_.push_back(0);
    for (const Mask generator : generators_) {
      const std::size_t old_size = family_.size();
      family_lookup_.reserve(2 * old_size);
      for (std::size_t index = 0; index < old_size; ++index) {
        const Mask candidate = family_[index] | generator;
        if (family_lookup_.insert(candidate)) {
          family_.push_back(candidate);
        }
      }
    }

    Count e = 0;
    const Mask v0 = v0_mask(m_, p_mask);
    const Mask shadows[2] = {v0, v0 | value_bit(m_, -m_)};
    for (const Mask shadow : shadows) {
      new_outputs_.clear();
      new_outputs_.reserve(family_.size());
      for (const Mask signature : family_) {
        const Mask image = signature | shadow;
        if (!family_lookup_.contains(image) && new_outputs_.insert(image)) {
          ++e;
        }
      }
    }
    return PerPCounts{static_cast<Count>(family_.size()), e};
  }

 private:
  int m_;
  FlatSet family_lookup_;
  FlatSet new_outputs_;
  std::vector<Mask> generators_;
  std::vector<Mask> family_;
};

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string argument(argv[i]);
    if (argument == "--help" || argument == "-h") {
      std::cout << "Usage: targeted_orbit --word BINARY [--members]\n";
      std::exit(EXIT_SUCCESS);
    }
    if (argument == "--members") {
      options.members = true;
      continue;
    }
    if (argument == "--word") {
      if (++i == argc) {
        throw std::invalid_argument("--word requires a binary word");
      }
      options.word = argv[i];
      continue;
    }
    constexpr const char prefix[] = "--word=";
    if (argument.rfind(prefix, 0) == 0) {
      options.word = argument.substr(sizeof(prefix) - 1);
      continue;
    }
    throw std::invalid_argument("unknown argument: " + argument);
  }
  if (options.word.empty() || options.word.size() % 2 != 0 ||
      options.word.size() > 60) {
    throw std::invalid_argument(
        "--word must have positive even length at most 60");
  }
  return options;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const int length = static_cast<int>(options.word.size());
    const int m = length / 2;
    const Mask word_mask = (Mask{1} << length) - 1;
    const Mask input_word = parse_word(options.word);
    const std::vector<Mask> orbit =
        orbit_elements(input_word, length, word_mask);
    const Mask representative =
        *std::min_element(orbit.begin(), orbit.end(),
                          [length](const Mask left, const Mask right) {
                            return word_less(left, right, length);
                          });
    const int a = equal_adjacencies(input_word, length, word_mask);
    for (const Mask member : orbit) {
      if (equal_adjacencies(member, length, word_mask) != a) {
        throw std::logic_error("equal-adjacency count is not orbit invariant");
      }
    }
    if (a == 0) {
      throw std::invalid_argument("Lambda is undefined for an alternating word");
    }

    const auto start = std::chrono::steady_clock::now();
    SignatureCounter counter(m);
    Count sum_q = 0;
    Count sum_e = 0;
    Count maximum_q = 0;
    std::vector<PerPCounts> member_counts;
    member_counts.reserve(orbit.size());
    for (const Mask member : orbit) {
      const PerPCounts counts = counter.compute(member);
      member_counts.push_back(counts);
      sum_q += counts.q;
      sum_e += counts.e;
      maximum_q = std::max(maximum_q, counts.q);
    }
    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration<double>(stop - start).count();
    const long double lambda =
        static_cast<long double>(m) * static_cast<long double>(m) *
        static_cast<long double>(sum_e) /
        (static_cast<long double>(a) * static_cast<long double>(sum_q));

    std::cout << "m " << m << '\n';
    std::cout << "input " << options.word << '\n';
    std::cout << "representative " << word_string(representative, length)
              << '\n';
    std::cout << "a " << a << '\n';
    std::cout << "orbit_size " << orbit.size() << '\n';
    std::cout << "sum_q " << sum_q << '\n';
    std::cout << "sum_e " << sum_e << '\n';
    std::cout << "lambda " << std::fixed << std::setprecision(12) << lambda
              << '\n';
    std::cout << "maximum_member_q " << maximum_q << '\n';
    std::cout << "seconds " << std::setprecision(6) << seconds << '\n';

    if (options.members) {
      std::cout << "\nmembers\n";
      std::cout << "word q e\n";
      for (std::size_t index = 0; index < orbit.size(); ++index) {
        std::cout << word_string(orbit[index], length) << ' '
                  << member_counts[index].q << ' ' << member_counts[index].e
                  << '\n';
      }
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
