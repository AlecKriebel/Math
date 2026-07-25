// Exact trace and e_0 diagnostics for the protected-signature construction.
//
// Compile:
//   c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
//       src/trace_diagnostics.cpp -o trace_diagnostics
//
// Run full e_0 diagnostics through m=8 and trace-only diagnostics thereafter:
//   ./trace_diagnostics --max-m 10 --e0-max-m 8

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint64_t;
using Count = std::uint64_t;

struct Closure {
  std::vector<Mask> elements;
  std::unordered_set<Mask> lookup;
};

struct Statistics {
  int m;
  Count trace_total;
  bool computed_e0;
  Count e0_total;
  Count bad_pointwise_count;
  std::int64_t minimum_gap;
  double seconds;
};

struct Options {
  int max_m = 8;
  int e0_max_m = 8;
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
  for (int p = 1; p <= 2 * m; ++p) {
    if ((p_mask & (Mask{1} << (p - 1))) == 0) {
      continue;
    }
    const int value = b - p;
    if (-m <= value && value <= m) {
      result |= value_bit(m, value);
    }
  }
  return result;
}

bool is_safe(const int m, const Mask p_mask, const int b) {
  if (b == 0 || std::abs(b) >= m) {
    return false;
  }
  const int p = m + b;
  return (p_mask & (Mask{1} << (p - 1))) == 0;
}

Mask v0_mask(const int m, const Mask p_mask) {
  Mask result = 0;
  for (int p = 1; p <= 2 * m; ++p) {
    if ((p_mask & (Mask{1} << (p - 1))) != 0) {
      result |= value_bit(m, m + 1 - p);
    }
  }
  return result;
}

Closure union_closure(const std::vector<Mask>& raw_generators) {
  std::vector<Mask> generators;
  generators.reserve(raw_generators.size());
  std::unordered_set<Mask> seen_generators;
  seen_generators.reserve(2 * raw_generators.size() + 1);
  for (const Mask generator : raw_generators) {
    if (seen_generators.insert(generator).second) {
      generators.push_back(generator);
    }
  }

  Closure closure;
  closure.elements.push_back(0);
  closure.lookup.insert(0);
  // There are at most 2^(number of distinct generators) unions. Cap the
  // initial reservation: most closures are far smaller than that worst case.
  const std::size_t reserve_exponent =
      std::min<std::size_t>(generators.size(), 12);
  const std::size_t reserve_hint = std::size_t{1} << reserve_exponent;
  closure.elements.reserve(reserve_hint);
  closure.lookup.reserve(2 * reserve_hint + 1);

  for (const Mask generator : generators) {
    const std::size_t old_size = closure.elements.size();
    for (std::size_t index = 0; index < old_size; ++index) {
      const Mask candidate = closure.elements[index] | generator;
      if (closure.lookup.insert(candidate).second) {
        closure.elements.push_back(candidate);
      }
    }
  }
  return closure;
}

std::vector<Mask> all_generators(const int m, const Mask p_mask) {
  std::vector<Mask> generators;
  generators.reserve(static_cast<std::size_t>(2 * m));
  for (int b = -m; b <= m; ++b) {
    if (b != 0) {
      generators.push_back(generator_mask(m, p_mask, b));
    }
  }
  return generators;
}

std::vector<Mask> safe_generators(const int m, const Mask p_mask) {
  std::vector<Mask> generators;
  generators.reserve(static_cast<std::size_t>(2 * m - 2));
  for (int b = -m + 1; b < m; ++b) {
    if (b != 0 && is_safe(m, p_mask, b)) {
      generators.push_back(generator_mask(m, p_mask, b));
    }
  }
  return generators;
}

Count e0_from_family(const int m,
                     const Mask p_mask,
                     const Closure& family) {
  const Mask v0 = v0_mask(m, p_mask);
  std::unordered_set<Mask> new_outputs;
  new_outputs.reserve(2 * family.elements.size() + 1);
  for (const Mask signature : family.elements) {
    const Mask image = signature | v0;
    if (family.lookup.find(image) == family.lookup.end()) {
      new_outputs.insert(image);
    }
  }
  return static_cast<Count>(new_outputs.size());
}

Statistics compute_statistics(const int m, const bool compute_e0) {
  const auto start = std::chrono::steady_clock::now();
  const Mask p_limit = Mask{1} << (2 * m);

  Count trace_total = 0;
  Count e0_total = 0;
  Count bad_pointwise_count = 0;
  std::int64_t minimum_gap = std::numeric_limits<std::int64_t>::max();

  // Odd masks are exactly the subsets P of [2m] containing 1.
  for (Mask p_mask = 1; p_mask < p_limit; p_mask += 2) {
    const Closure trace = union_closure(safe_generators(m, p_mask));
    const Count trace_size = static_cast<Count>(trace.elements.size());
    trace_total += trace_size;

    if (compute_e0) {
      const Closure family = union_closure(all_generators(m, p_mask));
      const Count e0 = e0_from_family(m, p_mask, family);
      e0_total += e0;

      const std::int64_t gap =
          static_cast<std::int64_t>(e0) -
          static_cast<std::int64_t>(trace_size);
      minimum_gap = std::min(minimum_gap, gap);
      if (gap < 0) {
        ++bad_pointwise_count;
      }
    }
  }

  if (!compute_e0) {
    minimum_gap = 0;
  }
  const auto stop = std::chrono::steady_clock::now();
  const double seconds =
      std::chrono::duration<double>(stop - start).count();
  return Statistics{m,
                    trace_total,
                    compute_e0,
                    e0_total,
                    bad_pointwise_count,
                    minimum_gap,
                    seconds};
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
      std::cout
          << "Usage: trace_diagnostics [--max-m M] [--e0-max-m M]\n";
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
    if (argument == "--e0-max-m") {
      options.e0_max_m = parse_next(argument);
      continue;
    }
    constexpr const char max_prefix[] = "--max-m=";
    if (argument.rfind(max_prefix, 0) == 0) {
      options.max_m =
          parse_integer(argument.substr(sizeof(max_prefix) - 1), "--max-m");
      continue;
    }
    constexpr const char e0_prefix[] = "--e0-max-m=";
    if (argument.rfind(e0_prefix, 0) == 0) {
      options.e0_max_m =
          parse_integer(argument.substr(sizeof(e0_prefix) - 1), "--e0-max-m");
      continue;
    }
    throw std::invalid_argument("unknown argument: " + argument);
  }

  if (options.max_m < 1 || options.max_m > 12) {
    throw std::invalid_argument("--max-m must lie between 1 and 12");
  }
  if (options.e0_max_m < 0 || options.e0_max_m > options.max_m) {
    throw std::invalid_argument(
        "--e0-max-m must lie between 0 and --max-m");
  }
  return options;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    std::cout << "m trace e0(P:1inP) bad_pointwise min(e0-R) seconds\n";
    for (int m = 1; m <= options.max_m; ++m) {
      const Statistics result =
          compute_statistics(m, m <= options.e0_max_m);
      std::cout << result.m << ' ' << result.trace_total << ' ';
      if (result.computed_e0) {
        std::cout << result.e0_total << ' ' << result.bad_pointwise_count
                  << ' ' << result.minimum_gap << ' ';
      } else {
        std::cout << "- - - ";
      }
      std::cout << std::fixed << std::setprecision(6) << result.seconds
                << '\n';
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
