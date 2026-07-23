// Exact cyclic-rotation/complement orbit diagnostics.
//
// Compile:
//   c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
//       src/orbit_diagnostics.cpp -o orbit_diagnostics
//
// Run:
//   ./orbit_diagnostics --m 8
//   ./orbit_diagnostics --m 8 --all-orbits

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

struct Options {
  int m = 0;
  bool all_orbits = false;
};

struct Orbit {
  Mask representative;
  int equal_adjacencies;
  Count sum_q = 0;
  Count sum_e = 0;
  std::uint32_t size;
};

struct PerPCounts {
  Count q;
  Count e;
};

struct ReferenceCounts {
  Count s;
  Count e;
};

constexpr ReferenceCounts references[] = {
    {0, 0},
    {10, 7},
    {102, 67},
    {1020, 508},
    {9906, 4082},
    {93198, 30527},
    {854156, 234374},
    {7674138, 1698857},
    {67615730, 12335479},
    {586193940, 89453245},
    {5021202766, 626972078},
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
  const Mask transitions = word ^ rotate_one(word, length, word_mask);
  return length - __builtin_popcountll(transitions);
}

std::string word_string(const Mask word, const int length) {
  std::string result;
  result.reserve(static_cast<std::size_t>(length));
  // Position p in P is printed at character p-1.
  for (int index = 0; index < length; ++index) {
    result.push_back((word & (Mask{1} << index)) != 0 ? '1' : '0');
  }
  return result;
}

bool word_lexicographically_less(const Mask left,
                                 const Mask right,
                                 const int length) {
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

std::vector<Orbit> build_orbits(const int m,
                                std::vector<std::uint32_t>& orbit_ids) {
  const int length = 2 * m;
  const Mask p_limit = Mask{1} << length;
  const Mask word_mask = p_limit - 1;
  constexpr std::uint32_t unassigned =
      std::numeric_limits<std::uint32_t>::max();
  orbit_ids.assign(static_cast<std::size_t>(p_limit), unassigned);

  std::vector<Orbit> orbits;
  orbits.reserve(static_cast<std::size_t>(p_limit / (2 * length) + length));
  for (Mask word = 0; word < p_limit; ++word) {
    if (orbit_ids[static_cast<std::size_t>(word)] != unassigned) {
      continue;
    }
    const std::vector<Mask> elements =
        orbit_elements(word, length, word_mask);
    const Mask representative =
        *std::min_element(elements.begin(), elements.end(),
                          [length](const Mask left, const Mask right) {
                            return word_lexicographically_less(
                                left, right, length);
                          });
    const int adjacency =
        equal_adjacencies(representative, length, word_mask);
    const std::uint32_t id =
        static_cast<std::uint32_t>(orbits.size());
    for (const Mask element : elements) {
      if (equal_adjacencies(element, length, word_mask) != adjacency) {
        throw std::logic_error("equal-adjacency count is not orbit invariant");
      }
      if (orbit_ids[static_cast<std::size_t>(element)] != unassigned) {
        throw std::logic_error("rotation/complement orbits overlap");
      }
      orbit_ids[static_cast<std::size_t>(element)] = id;
    }
    orbits.push_back(Orbit{representative,
                           adjacency,
                           0,
                           0,
                           static_cast<std::uint32_t>(elements.size())});
  }
  return orbits;
}

// P is encoded by bits 0,...,2m-1, with bit p-1 indicating p in P.
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
  explicit SignatureCounter(const int m)
      : m_(m),
        family_marks_(std::size_t{1} << (2 * m + 1), 0),
        shadow_marks_(std::size_t{1} << (2 * m + 1), 0) {
    generators_.reserve(static_cast<std::size_t>(2 * m));
    family_.reserve(std::size_t{1} << std::min(2 * m, 13));
  }

  PerPCounts compute(const Mask p_mask) {
    advance_family_stamp();
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

    family_.clear();
    family_.push_back(0);
    family_marks_[0] = family_stamp_;
    for (const Mask generator : generators_) {
      const std::size_t old_size = family_.size();
      for (std::size_t index = 0; index < old_size; ++index) {
        const Mask candidate = family_[index] | generator;
        const std::size_t candidate_index =
            static_cast<std::size_t>(candidate);
        if (family_marks_[candidate_index] != family_stamp_) {
          family_marks_[candidate_index] = family_stamp_;
          family_.push_back(candidate);
        }
      }
    }

    Count e = 0;
    const Mask v0 = v0_mask(m_, p_mask);
    const Mask shadows[2] = {v0, v0 | value_bit(m_, -m_)};
    for (const Mask shadow : shadows) {
      advance_shadow_stamp();
      for (const Mask signature : family_) {
        const Mask image = signature | shadow;
        const std::size_t image_index = static_cast<std::size_t>(image);
        if (family_marks_[image_index] != family_stamp_ &&
            shadow_marks_[image_index] != shadow_stamp_) {
          shadow_marks_[image_index] = shadow_stamp_;
          ++e;
        }
      }
    }
    return PerPCounts{static_cast<Count>(family_.size()), e};
  }

 private:
  void advance_family_stamp() {
    ++family_stamp_;
    if (family_stamp_ == 0) {
      std::fill(family_marks_.begin(), family_marks_.end(), 0);
      ++family_stamp_;
    }
  }

  void advance_shadow_stamp() {
    ++shadow_stamp_;
    if (shadow_stamp_ == 0) {
      std::fill(shadow_marks_.begin(), shadow_marks_.end(), 0);
      ++shadow_stamp_;
    }
  }

  int m_;
  std::vector<std::uint32_t> family_marks_;
  std::vector<std::uint32_t> shadow_marks_;
  std::uint32_t family_stamp_ = 0;
  std::uint32_t shadow_stamp_ = 0;
  std::vector<Mask> generators_;
  std::vector<Mask> family_;
};

long double lambda(const int m, const Orbit& orbit) {
  if (orbit.equal_adjacencies <= 0 || orbit.sum_q == 0) {
    throw std::logic_error("Lambda requested for an invalid orbit");
  }
  return static_cast<long double>(m) * static_cast<long double>(m) *
         static_cast<long double>(orbit.sum_e) /
         (static_cast<long double>(orbit.equal_adjacencies) *
          static_cast<long double>(orbit.sum_q));
}

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string argument(argv[i]);
    if (argument == "--help" || argument == "-h") {
      std::cout << "Usage: orbit_diagnostics --m M [--all-orbits]\n";
      std::exit(EXIT_SUCCESS);
    }
    if (argument == "--all-orbits") {
      options.all_orbits = true;
      continue;
    }
    if (argument == "--m") {
      if (++i == argc) {
        throw std::invalid_argument("--m requires an integer");
      }
      options.m = std::stoi(argv[i]);
      continue;
    }
    constexpr const char prefix[] = "--m=";
    if (argument.rfind(prefix, 0) == 0) {
      options.m = std::stoi(argument.substr(sizeof(prefix) - 1));
      continue;
    }
    throw std::invalid_argument("unknown argument: " + argument);
  }
  if (options.m < 1 || options.m > 10) {
    throw std::invalid_argument("--m must lie between 1 and 10");
  }
  return options;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const int m = options.m;
    const int length = 2 * m;
    const Mask p_limit = Mask{1} << length;
    const auto start = std::chrono::steady_clock::now();

    std::vector<std::uint32_t> orbit_ids;
    std::vector<Orbit> orbits = build_orbits(m, orbit_ids);
    SignatureCounter counter(m);
    Count total_q = 0;
    Count total_e = 0;
    for (Mask p_mask = 0; p_mask < p_limit; ++p_mask) {
      const PerPCounts counts = counter.compute(p_mask);
      Orbit& orbit =
          orbits[orbit_ids[static_cast<std::size_t>(p_mask)]];
      orbit.sum_q += counts.q;
      orbit.sum_e += counts.e;
      total_q += counts.q;
      total_e += counts.e;
    }

    const ReferenceCounts expected = references[m];
    if (total_q != expected.s || total_e != expected.e) {
      throw std::logic_error(
          "global q/e totals disagree with the independent reference");
    }

    std::size_t nonalternating_count = 0;
    std::size_t alternating_count = 0;
    std::size_t global_minimum_id =
        std::numeric_limits<std::size_t>::max();
    std::vector<std::size_t> by_a_minimum(
        static_cast<std::size_t>(length + 1),
        std::numeric_limits<std::size_t>::max());
    std::vector<std::size_t> by_a_count(
        static_cast<std::size_t>(length + 1), 0);

    for (std::size_t id = 0; id < orbits.size(); ++id) {
      const Orbit& orbit = orbits[id];
      if (orbit.equal_adjacencies == 0) {
        ++alternating_count;
        continue;
      }
      ++nonalternating_count;
      const std::size_t a =
          static_cast<std::size_t>(orbit.equal_adjacencies);
      ++by_a_count[a];
      if (global_minimum_id ==
              std::numeric_limits<std::size_t>::max() ||
          lambda(m, orbit) < lambda(m, orbits[global_minimum_id])) {
        global_minimum_id = id;
      }
      if (by_a_minimum[a] == std::numeric_limits<std::size_t>::max() ||
          lambda(m, orbit) < lambda(m, orbits[by_a_minimum[a]])) {
        by_a_minimum[a] = id;
      }
    }
    if (global_minimum_id == std::numeric_limits<std::size_t>::max()) {
      throw std::logic_error("no nonalternating orbit was found");
    }
    if (alternating_count != 1 ||
        nonalternating_count + alternating_count != orbits.size()) {
      throw std::logic_error("unexpected alternating-orbit count");
    }

    const auto stop = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration<double>(stop - start).count();
    const Orbit& global_minimum = orbits[global_minimum_id];

    std::cout << "m " << m << '\n';
    std::cout << "S " << total_q << '\n';
    std::cout << "E " << total_e << '\n';
    std::cout << "reference_check OK\n";
    std::cout << "orbit_count " << orbits.size() << '\n';
    std::cout << "nonalternating_orbit_count "
              << nonalternating_count << '\n';
    std::cout << "alternating_orbit_count " << alternating_count << '\n';
    std::cout << "global_min_lambda " << std::fixed
              << std::setprecision(12) << lambda(m, global_minimum)
              << '\n';
    std::cout << "global_min_a "
              << global_minimum.equal_adjacencies << '\n';
    std::cout << "global_min_representative "
              << word_string(global_minimum.representative, length) << '\n';
    std::cout << "global_min_orbit_size " << global_minimum.size << '\n';
    std::cout << "global_min_sum_q " << global_minimum.sum_q << '\n';
    std::cout << "global_min_sum_e " << global_minimum.sum_e << '\n';
    std::cout << "seconds " << std::setprecision(6) << seconds << '\n';

    std::cout << "\nby_a\n";
    std::cout << "a orbit_count min_lambda representative orbit_size "
                 "sum_q sum_e\n";
    for (int a = 1; a <= length; ++a) {
      const std::size_t id = by_a_minimum[static_cast<std::size_t>(a)];
      if (id == std::numeric_limits<std::size_t>::max()) {
        continue;
      }
      const Orbit& orbit = orbits[id];
      std::cout << a << ' ' << by_a_count[static_cast<std::size_t>(a)]
                << ' ' << std::setprecision(12) << lambda(m, orbit) << ' '
                << word_string(orbit.representative, length) << ' '
                << orbit.size << ' ' << orbit.sum_q << ' ' << orbit.sum_e
                << '\n';
    }

    if (options.all_orbits) {
      std::cout << "\nall_nonalternating_orbits\n";
      std::cout << "id a lambda representative orbit_size sum_q sum_e\n";
      for (std::size_t id = 0; id < orbits.size(); ++id) {
        const Orbit& orbit = orbits[id];
        if (orbit.equal_adjacencies == 0) {
          continue;
        }
        std::cout << id << ' ' << orbit.equal_adjacencies << ' '
                  << std::setprecision(12) << lambda(m, orbit) << ' '
                  << word_string(orbit.representative, length) << ' '
                  << orbit.size << ' ' << orbit.sum_q << ' ' << orbit.sum_e
                  << '\n';
      }
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
