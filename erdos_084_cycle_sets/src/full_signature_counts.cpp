// Exact full-family and shadow counts for the protected-signature construction.
//
// Compile:
//   c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
//       src/full_signature_counts.cpp -o full_signature_counts
//
// Run:
//   ./full_signature_counts --max-m 8

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint64_t;
using Count = std::uint64_t;

struct Statistics {
  int m;
  Count s;
  Count e0;
  Count e1;
  double seconds;
  std::vector<Count> rank_s;
  std::vector<Count> rank_e;

  Count e() const { return e0 + e1; }
};

struct Options {
  int max_m = 8;
  int rank_table_m = 0;
};

Mask value_bit(const int m, const int value) {
  if (value < -m || value > m) {
    throw std::logic_error("signature value lies outside [-m,m]");
  }
  return Mask{1} << (value + m);
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

Count power_of_eight(const int exponent) {
  Count result = 1;
  for (int i = 0; i < exponent; ++i) {
    result *= 8;
  }
  return result;
}

Statistics compute_statistics(const int m, const bool collect_rank_table) {
  const auto start = std::chrono::steady_clock::now();
  const Mask p_limit = Mask{1} << (2 * m);
  const std::size_t signature_universe =
      std::size_t{1} << (2 * m + 1);

  // Stamps avoid clearing either membership array for each P or shadow.
  std::vector<std::uint32_t> family_marks(signature_universe, 0);
  std::vector<std::uint32_t> shadow_marks(signature_universe, 0);
  std::uint32_t family_stamp = 0;
  std::uint32_t shadow_stamp = 0;

  std::vector<Mask> generators;
  generators.reserve(static_cast<std::size_t>(2 * m));
  std::vector<Mask> family;
  family.reserve(std::size_t{1} << std::min(2 * m, 13));

  Count s_total = 0;
  Count e0_total = 0;
  Count e1_total = 0;
  std::vector<Count> rank_s;
  std::vector<Count> rank_e;
  if (collect_rank_table) {
    rank_s.assign(static_cast<std::size_t>(2 * m + 1), 0);
    rank_e.assign(static_cast<std::size_t>(2 * m + 1), 0);
  }

  for (Mask p_mask = 0; p_mask < p_limit; ++p_mask) {
    ++family_stamp;
    if (family_stamp == 0) {
      std::fill(family_marks.begin(), family_marks.end(), 0);
      ++family_stamp;
    }

    generators.clear();
    for (int b = -m; b <= m; ++b) {
      if (b == 0) {
        continue;
      }
      const Mask generator = generator_mask(m, p_mask, b);
      if (std::find(generators.begin(), generators.end(), generator) ==
          generators.end()) {
        generators.push_back(generator);
      }
    }
    // Large generators tend to create fewer intermediate distinct unions.
    std::sort(generators.begin(), generators.end(),
              [](const Mask left, const Mask right) {
                const int left_size = __builtin_popcountll(left);
                const int right_size = __builtin_popcountll(right);
                if (left_size != right_size) {
                  return left_size > right_size;
                }
                return left > right;
              });

    family.clear();
    family.push_back(0);
    family_marks[0] = family_stamp;
    for (const Mask generator : generators) {
      const std::size_t old_size = family.size();
      for (std::size_t index = 0; index < old_size; ++index) {
        const Mask candidate = family[index] | generator;
        const std::size_t candidate_index =
            static_cast<std::size_t>(candidate);
        if (family_marks[candidate_index] != family_stamp) {
          family_marks[candidate_index] = family_stamp;
          family.push_back(candidate);
        }
      }
    }
    const Count family_size = static_cast<Count>(family.size());
    s_total += family_size;
    const std::size_t rank =
        static_cast<std::size_t>(__builtin_popcountll(p_mask));
    if (collect_rank_table) {
      rank_s[rank] += family_size;
    }

    const Mask v0 = v0_mask(m, p_mask);
    const Mask shadows[2] = {v0, v0 | value_bit(m, -m)};
    for (int alpha = 0; alpha < 2; ++alpha) {
      ++shadow_stamp;
      if (shadow_stamp == 0) {
        std::fill(shadow_marks.begin(), shadow_marks.end(), 0);
        ++shadow_stamp;
      }
      Count shadow_count = 0;
      for (const Mask signature : family) {
        const Mask image = signature | shadows[alpha];
        const std::size_t image_index = static_cast<std::size_t>(image);
        if (family_marks[image_index] != family_stamp &&
            shadow_marks[image_index] != shadow_stamp) {
          shadow_marks[image_index] = shadow_stamp;
          ++shadow_count;
        }
      }
      if (alpha == 0) {
        e0_total += shadow_count;
      } else {
        e1_total += shadow_count;
      }
      if (collect_rank_table) {
        rank_e[rank] += shadow_count;
      }
    }
  }

  if (collect_rank_table) {
    Count reconstructed_s = 0;
    Count reconstructed_e = 0;
    for (const Count value : rank_s) {
      reconstructed_s += value;
    }
    for (const Count value : rank_e) {
      reconstructed_e += value;
    }
    if (reconstructed_s != s_total ||
        reconstructed_e != e0_total + e1_total) {
      throw std::logic_error("rank totals failed to reconstruct S or E");
    }
  }

  const auto stop = std::chrono::steady_clock::now();
  const double seconds =
      std::chrono::duration<double>(stop - start).count();
  return Statistics{m,
                    s_total,
                    e0_total,
                    e1_total,
                    seconds,
                    std::move(rank_s),
                    std::move(rank_e)};
}

int parse_integer(const std::string& value, const std::string& option) {
  std::size_t consumed = 0;
  const int parsed = std::stoi(value, &consumed);
  if (consumed != value.size()) {
    throw std::invalid_argument(option + " requires an integer");
  }
  return parsed;
}

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string argument(argv[i]);
    if (argument == "--help" || argument == "-h") {
      std::cout << "Usage: full_signature_counts [--max-m M] "
                   "[--rank-table-m M]\n";
      std::exit(EXIT_SUCCESS);
    }

    const auto parse_next = [&](const std::string& option) {
      if (++i == argc) {
        throw std::invalid_argument(option + " requires an integer");
      }
      return parse_integer(argv[i], option);
    };

    if (argument == "--max-m") {
      options.max_m = parse_next(argument);
      continue;
    }
    if (argument == "--rank-table-m") {
      options.rank_table_m = parse_next(argument);
      continue;
    }
    constexpr const char max_prefix[] = "--max-m=";
    if (argument.rfind(max_prefix, 0) == 0) {
      options.max_m =
          parse_integer(argument.substr(sizeof(max_prefix) - 1), "--max-m");
      continue;
    }
    constexpr const char rank_prefix[] = "--rank-table-m=";
    if (argument.rfind(rank_prefix, 0) == 0) {
      options.rank_table_m = parse_integer(
          argument.substr(sizeof(rank_prefix) - 1), "--rank-table-m");
      continue;
    }
    throw std::invalid_argument("unknown argument: " + argument);
  }
  if (options.max_m < 1 || options.max_m > 10) {
    throw std::invalid_argument("--max-m must lie between 1 and 10");
  }
  if (options.rank_table_m < 0 || options.rank_table_m > 10) {
    throw std::invalid_argument(
        "--rank-table-m must lie between 1 and 10 when supplied");
  }
  return options;
}

void print_rank_table(const Statistics& row) {
  if (row.rank_s.empty() || row.rank_e.empty()) {
    throw std::logic_error("requested rank table was not collected");
  }
  std::cout << "\nrank table m=" << row.m << '\n';
  std::cout << "k S_mk E_mk paired_k paired_ratio\n";
  for (int k = 0; k <= 2 * row.m; ++k) {
    const int paired_k = 2 * row.m - k;
    const Count paired_s =
        row.rank_s[static_cast<std::size_t>(k)] +
        row.rank_s[static_cast<std::size_t>(paired_k)];
    const Count paired_e =
        row.rank_e[static_cast<std::size_t>(k)] +
        row.rank_e[static_cast<std::size_t>(paired_k)];
    const long double ratio =
        static_cast<long double>(row.m) *
        static_cast<long double>(paired_e) /
        static_cast<long double>(paired_s);
    std::cout << k << ' ' << row.rank_s[static_cast<std::size_t>(k)] << ' '
              << row.rank_e[static_cast<std::size_t>(k)] << ' ' << paired_k
              << ' ' << std::fixed << std::setprecision(9) << ratio << '\n';
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    std::vector<Statistics> rows;
    rows.reserve(static_cast<std::size_t>(options.max_m));
    for (int m = 1; m <= options.max_m; ++m) {
      rows.push_back(
          compute_statistics(m, m == options.rank_table_m));
    }

    std::cout << "m S E0 E1 E E/8^m slack seconds\n";
    for (std::size_t index = 0; index < rows.size(); ++index) {
      const Statistics& row = rows[index];
      const long double normalized_e =
          static_cast<long double>(row.e()) /
          static_cast<long double>(power_of_eight(row.m));
      std::cout << row.m << ' ' << row.s << ' ' << row.e0 << ' ' << row.e1
                << ' ' << row.e() << ' ' << std::fixed
                << std::setprecision(9) << normalized_e << ' ';
      if (index + 1 < rows.size()) {
        const Statistics& next = rows[index + 1];
        const Count baseline = 8 * row.s + 2 * row.e();
        if (next.s < baseline) {
          throw std::logic_error("recurrence lower bound failed");
        }
        std::cout << next.s - baseline << ' ';
      } else {
        std::cout << "- ";
      }
      std::cout << std::setprecision(6) << row.seconds << '\n';
    }

    if (options.rank_table_m != 0) {
      if (options.rank_table_m <= options.max_m) {
        print_rank_table(
            rows[static_cast<std::size_t>(options.rank_table_m - 1)]);
      } else {
        const Statistics rank_row =
            compute_statistics(options.rank_table_m, true);
        print_rank_table(rank_row);
      }
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
