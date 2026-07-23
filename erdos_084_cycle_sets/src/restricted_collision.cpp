// Independent exact verifier for the restricted-witness collision statistics.
//
// Compile:
//   c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
//       src/restricted_collision.cpp -o restricted_collision
//
// Run:
//   ./restricted_collision --max-m 8

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

using Mask = std::uint64_t;
using Count = std::uint64_t;

struct Statistics {
  int m;
  Count witnesses;
  Count collision_energy;
  Count distinct_outputs;
  Count max_fiber;
  double seconds;
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

Count expected_witness_total(const int m) {
  if (m == 1) {
    return 2;
  }
  Count result = 12;
  for (int exponent = 0; exponent < m - 2; ++exponent) {
    result *= 8;
  }
  return result;
}

Statistics compute_statistics(const int m) {
  const auto start = std::chrono::steady_clock::now();
  const Mask p_limit = Mask{1} << (2 * m);

  Count total_witnesses = 0;
  Count total_collision_energy = 0;
  Count total_distinct_outputs = 0;
  Count global_max_fiber = 0;

  // Odd masks are exactly the P subsets of [2m] that contain 1.
  for (Mask p_mask = 1; p_mask < p_limit; p_mask += 2) {
    // choices[t-1] contains the nonempty generators that may be selected
    // at coordinate t. The empty choice is handled separately. Keeping both
    // equal masks, if equality occurs, is essential: they are distinct B's.
    std::vector<std::vector<Mask>> choices(static_cast<std::size_t>(m - 1));
    Count witness_count_for_p = 1;

    for (int t = 1; t < m; ++t) {
      auto& coordinate_choices = choices[static_cast<std::size_t>(t - 1)];
      if (is_safe(m, p_mask, t)) {
        coordinate_choices.push_back(generator_mask(m, p_mask, t));
      }
      if (is_safe(m, p_mask, -t)) {
        coordinate_choices.push_back(generator_mask(m, p_mask, -t));
      }
      witness_count_for_p *=
          static_cast<Count>(1 + coordinate_choices.size());
    }

    std::unordered_map<Mask, Count> fibers;
    fibers.reserve(static_cast<std::size_t>(2 * witness_count_for_p + 1));

    std::function<void(int, Mask)> enumerate =
        [&](const int coordinate, const Mask signature) {
          if (coordinate == m - 1) {
            ++fibers[signature];
            return;
          }

          enumerate(coordinate + 1, signature);
          for (const Mask generator :
               choices[static_cast<std::size_t>(coordinate)]) {
            enumerate(coordinate + 1, signature | generator);
          }
        };
    enumerate(0, 0);

    Count reconstructed_witness_count = 0;
    for (const auto& [signature, multiplicity] : fibers) {
      (void)signature;
      reconstructed_witness_count += multiplicity;
      total_collision_energy += multiplicity * multiplicity;
      global_max_fiber = std::max(global_max_fiber, multiplicity);
    }

    if (reconstructed_witness_count != witness_count_for_p) {
      throw std::logic_error("fiber multiplicities failed to count witnesses");
    }
    total_witnesses += reconstructed_witness_count;
    total_distinct_outputs += static_cast<Count>(fibers.size());
  }

  if (total_witnesses != expected_witness_total(m)) {
    throw std::logic_error(
        "computed witness total disagrees with 12*8^(m-2)");
  }

  const auto stop = std::chrono::steady_clock::now();
  const double seconds =
      std::chrono::duration<double>(stop - start).count();
  return Statistics{m,
                    total_witnesses,
                    total_collision_energy,
                    total_distinct_outputs,
                    global_max_fiber,
                    seconds};
}

int parse_max_m(const int argc, char** argv) {
  int max_m = 8;
  for (int i = 1; i < argc; ++i) {
    const std::string argument(argv[i]);
    if (argument == "--help" || argument == "-h") {
      std::cout << "Usage: restricted_collision [--max-m M]\n";
      std::exit(EXIT_SUCCESS);
    }
    if (argument == "--max-m") {
      if (++i == argc) {
        throw std::invalid_argument("--max-m requires an integer");
      }
      max_m = std::stoi(argv[i]);
      continue;
    }
    constexpr const char prefix[] = "--max-m=";
    if (argument.rfind(prefix, 0) == 0) {
      max_m = std::stoi(argument.substr(sizeof(prefix) - 1));
      continue;
    }
    throw std::invalid_argument("unknown argument: " + argument);
  }
  if (max_m < 1 || max_m > 12) {
    throw std::invalid_argument("--max-m must lie between 1 and 12");
  }
  return max_m;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const int max_m = parse_max_m(argc, argv);
    std::cout << "m W Q D max_fiber Q/W seconds\n";
    for (int m = 1; m <= max_m; ++m) {
      const Statistics result = compute_statistics(m);
      const long double ratio =
          static_cast<long double>(result.collision_energy) /
          static_cast<long double>(result.witnesses);
      std::cout << result.m << ' ' << result.witnesses << ' '
                << result.collision_energy << ' ' << result.distinct_outputs
                << ' ' << result.max_fiber << ' ' << std::fixed
                << std::setprecision(9) << ratio << ' '
                << std::setprecision(6) << result.seconds << '\n';
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
