// Exact row-sum projection enumerator for the viable order-three LP(333) lane.
//
// If a QPSK quotient is invariant under the order-three multiplier that fixes
// the Z/9 row coordinate, its full row sums have the form
//
//     s_r = x_r + 3 t_r,
//
// where x is the zero-column word and t_r is a sum of twelve fourth roots of
// unity.  The fixed Legendre compression gives sum(t_r)=0.  Any exact
// Legendre pair must also satisfy
//
//     Re PAF_s(0) = 297,   Re PAF_s(a) = -37  (a=1,2,3,4).
//
// This program enumerates that finite projection exactly.  It is not a search
// for a Legendre pair: surviving row-sum words still have to lift through the
// twelve cyclotomic class words and every mixed quotient equation.

#include <array>
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kRows = 9;
constexpr int kTargetEnergy = 297;

struct Gaussian {
  int real;
  int imag;
};

struct Option {
  Gaussian s;
  Gaussian t;
  int energy;
};

struct State {
  int energy;
  int real;
  int imag;

  bool operator==(const State& other) const {
    return energy == other.energy && real == other.real && imag == other.imag;
  }
};

struct StateHash {
  std::size_t operator()(const State& value) const {
    std::uint64_t result = static_cast<std::uint32_t>(value.energy);
    result = result * 257U + static_cast<std::uint32_t>(value.real + 512);
    result = result * 257U + static_cast<std::uint32_t>(value.imag + 512);
    return static_cast<std::size_t>(result);
  }
};

using StateSet = std::unordered_set<State, StateHash>;

constexpr std::array<Gaussian, 4> kRoots = {
    Gaussian{1, 0}, Gaussian{0, 1}, Gaussian{-1, 0}, Gaussian{0, -1}};

constexpr std::array<int, kRows> kCanonicalZeroExponents =
    {0, 0, 0, 1, 2, 3, 1, 3, 2};

int SquaredNorm(const Gaussian value) {
  return value.real * value.real + value.imag * value.imag;
}

int Dot(const Gaussian left, const Gaussian right) {
  return left.real * right.real + left.imag * right.imag;
}

std::vector<Gaussian> SumAlphabet(const int summands) {
  std::vector<Gaussian> result;
  for (int real = -summands; real <= summands; ++real) {
    for (int imag = -summands; imag <= summands; ++imag) {
      const int l1 = std::abs(real) + std::abs(imag);
      if (l1 <= summands && (summands - l1) % 2 == 0) {
        result.push_back({real, imag});
      }
    }
  }
  return result;
}

std::array<std::vector<Option>, kRows> BuildOptions() {
  const std::vector<Gaussian> alphabet = SumAlphabet(12);
  if (alphabet.size() != 169U) {
    std::cerr << "unexpected twelve-root alphabet size\n";
    std::exit(2);
  }

  std::array<std::vector<Option>, kRows> result;
  for (int row = 0; row < kRows; ++row) {
    const Gaussian x = kRoots[kCanonicalZeroExponents[row]];
    for (const Gaussian t : alphabet) {
      const Gaussian s{x.real + 3 * t.real, x.imag + 3 * t.imag};
      const int energy = SquaredNorm(s);
      if (energy <= kTargetEnergy) {
        result[row].push_back({s, t, energy});
      }
    }
    if (result[row].size() != 52U) {
      std::cerr << "unexpected row option count at row " << row << '\n';
      std::exit(2);
    }
  }
  return result;
}

std::array<StateSet, kRows + 1> BuildSuffixStates(
    const std::array<std::vector<Option>, kRows>& options) {
  std::array<StateSet, kRows + 1> suffix;
  suffix[kRows].insert({0, 0, 0});
  for (int row = kRows - 1; row >= 0; --row) {
    StateSet& current = suffix[row];
    for (const Option& option : options[row]) {
      for (const State& rest : suffix[row + 1]) {
        const int energy = option.energy + rest.energy;
        if (energy <= kTargetEnergy) {
          current.insert(
              {energy, option.s.real + rest.real, option.s.imag + rest.imag});
        }
      }
    }
  }
  return suffix;
}

struct Enumeration {
  const std::array<std::vector<Option>, kRows>& options;
  const std::array<StateSet, kRows + 1>& suffix;
  const std::map<std::pair<int, int>, int>& minimum_pair_splits;
  std::array<Gaussian, kRows> word{};
  std::array<Gaussian, kRows> t_word{};
  std::uint64_t energy_sum_words = 0;
  std::uint64_t exact_paf_words = 0;
  std::uint64_t margin_liftable_words = 0;
  std::array<Gaussian, kRows> first_exact{};
  std::map<int, std::uint64_t> split_lower_bound_histogram;
  std::map<int, std::uint64_t> liftable_split_lower_bound_histogram;
  std::ostream* catalog = nullptr;

  Enumeration(const std::array<std::vector<Option>, kRows>& options_in,
              const std::array<StateSet, kRows + 1>& suffix_in,
              const std::map<std::pair<int, int>, int>&
                  minimum_pair_splits_in,
              std::ostream* catalog_in)
      : options(options_in),
        suffix(suffix_in),
        minimum_pair_splits(minimum_pair_splits_in),
        catalog(catalog_in) {}

  static bool BipartiteMarginsAreGraphical(std::array<int, kRows> rows) {
    std::sort(rows.begin(), rows.end(), std::greater<int>());
    int left_sum = 0;
    for (int k = 1; k <= kRows; ++k) {
      left_sum += rows[k - 1];
      const int right_sum = 6 * std::min(6, k) + 6 * std::min(3, k);
      if (left_sum > right_sum) {
        return false;
      }
    }
    return left_sum == 54;
  }

  void Visit(const int row, const int energy, const int real, const int imag) {
    if (row == kRows) {
      ++energy_sum_words;
      std::array<int, 4> paf{};
      for (int lag = 1; lag <= 4; ++lag) {
        for (int index = 0; index < kRows; ++index) {
          paf[lag - 1] += Dot(word[index], word[(index + lag) % kRows]);
        }
      }
      if (paf == std::array<int, 4>{-37, -37, -37, -37}) {
        if (catalog != nullptr) {
          for (int row = 0; row < kRows; ++row) {
            if (row != 0) {
              *catalog << ',';
            }
            *catalog << word[row].real << ',' << word[row].imag;
          }
          *catalog << '\n';
        }
        if (exact_paf_words == 0) {
          first_exact = word;
        }
        int split_lower_bound = 0;
        for (const Gaussian t : t_word) {
          split_lower_bound += minimum_pair_splits.at({t.real, t.imag});
        }
        ++split_lower_bound_histogram[split_lower_bound];
        std::array<int, kRows> a_plus_counts{};
        std::array<int, kRows> b_plus_counts{};
        for (int row = 0; row < kRows; ++row) {
          a_plus_counts[row] =
              (12 + t_word[row].real - t_word[row].imag) / 2;
          b_plus_counts[row] =
              (12 + t_word[row].real + t_word[row].imag) / 2;
        }
        if (BipartiteMarginsAreGraphical(a_plus_counts) &&
            BipartiteMarginsAreGraphical(b_plus_counts)) {
          ++margin_liftable_words;
          ++liftable_split_lower_bound_histogram[split_lower_bound];
        }
        ++exact_paf_words;
      }
      return;
    }

    for (const Option& option : options[row]) {
      const int next_energy = energy + option.energy;
      if (next_energy > kTargetEnergy) {
        continue;
      }
      const int next_real = real + option.s.real;
      const int next_imag = imag + option.s.imag;
      const State required{kTargetEnergy - next_energy, 1 - next_real,
                           -next_imag};
      if (!suffix[row + 1].contains(required)) {
        continue;
      }
      word[row] = option.s;
      t_word[row] = option.t;
      Visit(row + 1, next_energy, next_real, next_imag);
    }
  }
};

std::map<std::pair<int, int>, int> MinimumSexticPairSplits() {
  constexpr int kInfinity = std::numeric_limits<int>::max() / 4;
  std::map<std::pair<int, int>, int> current;
  current[{0, 0}] = 0;
  for (int pair_index = 0; pair_index < 6; ++pair_index) {
    std::map<std::pair<int, int>, int> next;
    for (const auto& [sum, cost] : current) {
      for (int left = 0; left < 4; ++left) {
        for (int right = 0; right < 4; ++right) {
          const std::pair<int, int> new_sum{
              sum.first + kRoots[left].real + kRoots[right].real,
              sum.second + kRoots[left].imag + kRoots[right].imag};
          const int new_cost = cost + static_cast<int>(left != right);
          auto [where, inserted] = next.emplace(new_sum, kInfinity);
          where->second = std::min(where->second, new_cost);
        }
      }
    }
    current = std::move(next);
  }
  if (current.size() != 169U) {
    std::cerr << "unexpected paired twelve-root alphabet size\n";
    std::exit(2);
  }
  return current;
}

}  // namespace

int main(const int argc, char** argv) {
  std::ofstream catalog_file;
  if (argc == 3 && std::string(argv[1]) == "--emit-words") {
    catalog_file.open(argv[2]);
    if (!catalog_file) {
      std::cerr << "could not open row-sum catalog output\n";
      return 2;
    }
    for (int row = 0; row < kRows; ++row) {
      if (row != 0) {
        catalog_file << ',';
      }
      catalog_file << "s" << row << "_real,s" << row << "_imag";
    }
    catalog_file << '\n';
  } else if (argc != 1) {
    std::cerr << "usage: " << argv[0] << " [--emit-words PATH]\n";
    return 2;
  }

  const auto options = BuildOptions();
  const auto suffix = BuildSuffixStates(options);
  const auto minimum_pair_splits = MinimumSexticPairSplits();
  Enumeration enumeration(options, suffix, minimum_pair_splits,
                          catalog_file.is_open() ? &catalog_file : nullptr);
  enumeration.Visit(0, 0, 0, 0);

  std::cout << "order_three_t_alphabet=169\n";
  std::cout << "energy_bounded_row_options=52\n";
  std::cout << "suffix_root_states=" << suffix[0].size() << '\n';
  std::cout << "energy_and_sum_words=" << enumeration.energy_sum_words << '\n';
  std::cout << "exact_row_sum_paf_words=" << enumeration.exact_paf_words << '\n';
  std::cout << "fixed_class_margin_liftable_words="
            << enumeration.margin_liftable_words << '\n';
  std::cout << "sextic_pair_split_lower_bound_histogram=";
  bool first = true;
  for (const auto& [splits, count] :
       enumeration.split_lower_bound_histogram) {
    if (!first) {
      std::cout << ',';
    }
    first = false;
    std::cout << splits << ':' << count;
  }
  std::cout << '\n';
  std::cout << "liftable_sextic_pair_split_lower_bound_histogram=";
  first = true;
  for (const auto& [splits, count] :
       enumeration.liftable_split_lower_bound_histogram) {
    if (!first) {
      std::cout << ',';
    }
    first = false;
    std::cout << splits << ':' << count;
  }
  std::cout << '\n';
  if (enumeration.exact_paf_words != 0) {
    std::cout << "first_exact_row_sum_word=";
    for (int row = 0; row < kRows; ++row) {
      if (row != 0) {
        std::cout << ',';
      }
      std::cout << '(' << enumeration.first_exact[row].real << ','
                << enumeration.first_exact[row].imag << ')';
    }
    std::cout << '\n';
  }
  return 0;
}
