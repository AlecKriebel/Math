// Exact down-set diagnostics for the protected-signature construction.
//
// For every P containing 1, compute
//
//   g(P) = e_0(P) + e_1(P) - R_m(P),
//
// followed by its Boolean zeta transform
//
//   H(P_0) = sum_{1 in P subseteq P_0} g(P).
//
// The program reports the minimum H and the minimum first difference
// H(P_0)-H(P_0\{p}), thereby testing the down-set conjecture (D) and its
// coordinatewise strengthening (D+).

#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

using Mask = std::uint64_t;
using SignedCount = std::int64_t;
using UnsignedCount = std::uint64_t;

struct Options {
  int m = 9;
  unsigned threads = 0;
};

struct LocalTotals {
  UnsignedCount trace = 0;
  UnsignedCount e0 = 0;
  UnsignedCount e1 = 0;
};

Mask value_bit(const int m, const int value) {
  return Mask{1} << (value + m);
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

std::string decode_p(const int m, const Mask p_mask) {
  std::string result = "{";
  bool first = true;
  for (int p = 1; p <= 2 * m; ++p) {
    if ((p_mask & (Mask{1} << (p - 1))) == 0) {
      continue;
    }
    if (!first) {
      result += ",";
    }
    result += std::to_string(p);
    first = false;
  }
  result += "}";
  return result;
}

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string argument(argv[i]);
    const auto next_integer = [&](const std::string& name) {
      if (++i == argc) {
        throw std::invalid_argument(name + " requires an integer");
      }
      return std::stoi(argv[i]);
    };
    if (argument == "--m") {
      options.m = next_integer(argument);
    } else if (argument == "--threads") {
      const int value = next_integer(argument);
      if (value < 1) {
        throw std::invalid_argument("--threads must be positive");
      }
      options.threads = static_cast<unsigned>(value);
    } else if (argument == "--help" || argument == "-h") {
      std::cout << "Usage: downset_diagnostics [--m M] [--threads T]\n";
      std::exit(EXIT_SUCCESS);
    } else {
      throw std::invalid_argument("unknown argument: " + argument);
    }
  }
  if (options.m < 1 || options.m > 10) {
    throw std::invalid_argument("--m must lie between 1 and 10");
  }
  if (options.threads == 0) {
    options.threads = std::max(1u, std::thread::hardware_concurrency());
  }
  return options;
}

void compute_worker(const int m,
                    const unsigned worker_index,
                    const unsigned worker_count,
                    std::vector<SignedCount>& g,
                    LocalTotals& totals) {
  const Mask p_limit = Mask{1} << (2 * m);
  const std::size_t signature_limit =
      std::size_t{1} << (2 * m + 1);
  std::vector<std::uint32_t> family_marks(signature_limit, 0);
  std::vector<std::uint32_t> shadow_marks(signature_limit, 0);
  std::uint32_t family_stamp = 0;
  std::uint32_t shadow_stamp = 0;
  std::vector<Mask> generators;
  std::vector<Mask> family;
  generators.reserve(static_cast<std::size_t>(2 * m));
  family.reserve(std::size_t{1} << std::min(2 * m, 15));

  for (Mask p_mask = 1 + 2 * worker_index; p_mask < p_limit;
       p_mask += 2 * worker_count) {
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
        if (family_marks[static_cast<std::size_t>(candidate)] !=
            family_stamp) {
          family_marks[static_cast<std::size_t>(candidate)] = family_stamp;
          family.push_back(candidate);
        }
      }
    }

    UnsignedCount trace = 0;
    for (const Mask signature : family) {
      if ((signature & Mask{1}) == 0) {
        ++trace;
      }
    }

    const Mask v0 = v0_mask(m, p_mask);
    const Mask shadows[2] = {v0, v0 | Mask{1}};
    UnsignedCount excess[2] = {0, 0};
    for (int alpha = 0; alpha < 2; ++alpha) {
      ++shadow_stamp;
      if (shadow_stamp == 0) {
        std::fill(shadow_marks.begin(), shadow_marks.end(), 0);
        ++shadow_stamp;
      }
      for (const Mask signature : family) {
        const Mask image = signature | shadows[alpha];
        const std::size_t image_index =
            static_cast<std::size_t>(image);
        if (family_marks[image_index] != family_stamp &&
            shadow_marks[image_index] != shadow_stamp) {
          shadow_marks[image_index] = shadow_stamp;
          ++excess[alpha];
        }
      }
    }

    g[static_cast<std::size_t>(p_mask)] =
        static_cast<SignedCount>(excess[0] + excess[1]) -
        static_cast<SignedCount>(trace);
    totals.trace += trace;
    totals.e0 += excess[0];
    totals.e1 += excess[1];
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const int m = options.m;
    const std::size_t p_limit = std::size_t{1} << (2 * m);
    std::vector<SignedCount> h(p_limit, 0);
    std::vector<LocalTotals> local(options.threads);
    std::vector<std::thread> workers;
    workers.reserve(options.threads);

    const auto start = std::chrono::steady_clock::now();
    for (unsigned index = 0; index < options.threads; ++index) {
      workers.emplace_back(compute_worker, m, index, options.threads,
                           std::ref(h), std::ref(local[index]));
    }
    for (std::thread& worker : workers) {
      worker.join();
    }
    const auto family_stop = std::chrono::steady_clock::now();

    LocalTotals totals;
    for (const LocalTotals& value : local) {
      totals.trace += value.trace;
      totals.e0 += value.e0;
      totals.e1 += value.e1;
    }

    // Bit zero is forced throughout. Zeta-transform only the optional bits.
    for (int bit = 1; bit < 2 * m; ++bit) {
      const std::size_t bit_mask = std::size_t{1} << bit;
      for (std::size_t mask = 1; mask < p_limit; mask += 2) {
        if ((mask & bit_mask) != 0) {
          h[mask] += h[mask ^ bit_mask];
        }
      }
    }

    SignedCount minimum_h = std::numeric_limits<SignedCount>::max();
    Mask minimum_h_mask = 0;
    SignedCount minimum_difference =
        std::numeric_limits<SignedCount>::max();
    Mask minimum_difference_mask = 0;
    int minimum_difference_bit = 0;
    UnsignedCount zero_h_count = 0;
    UnsignedCount negative_h_count = 0;
    UnsignedCount negative_difference_count = 0;

    for (Mask mask = 1; mask < p_limit; mask += 2) {
      if (h[static_cast<std::size_t>(mask)] < minimum_h) {
        minimum_h = h[static_cast<std::size_t>(mask)];
        minimum_h_mask = mask;
      }
      if (h[static_cast<std::size_t>(mask)] == 0) {
        ++zero_h_count;
      }
      if (h[static_cast<std::size_t>(mask)] < 0) {
        ++negative_h_count;
      }
      for (int bit = 1; bit < 2 * m; ++bit) {
        const Mask bit_mask = Mask{1} << bit;
        if ((mask & bit_mask) == 0) {
          continue;
        }
        const SignedCount difference =
            h[static_cast<std::size_t>(mask)] -
            h[static_cast<std::size_t>(mask ^ bit_mask)];
        if (difference < minimum_difference) {
          minimum_difference = difference;
          minimum_difference_mask = mask;
          minimum_difference_bit = bit;
        }
        if (difference < 0) {
          ++negative_difference_count;
        }
      }
    }

    const auto stop = std::chrono::steady_clock::now();
    const double family_seconds =
        std::chrono::duration<double>(family_stop - start).count();
    const double total_seconds =
        std::chrono::duration<double>(stop - start).count();
    const Mask full_mask = (Mask{1} << (2 * m)) - 1;

    std::cout << "m=" << m << " threads=" << options.threads << '\n';
    std::cout << "trace_total=" << totals.trace
              << " e0_total=" << totals.e0
              << " e1_total=" << totals.e1
              << " g_total=" << h[static_cast<std::size_t>(full_mask)]
              << '\n';
    std::cout << "min_H=" << minimum_h
              << " at=" << decode_p(m, minimum_h_mask)
              << " zeros=" << zero_h_count
              << " negatives=" << negative_h_count << '\n';
    std::cout << "min_first_difference=" << minimum_difference
              << " at=" << decode_p(m, minimum_difference_mask)
              << " deleting=" << (minimum_difference_bit + 1)
              << " negative_first_differences="
              << negative_difference_count << '\n';
    std::cout << std::fixed << std::setprecision(6)
              << "family_seconds=" << family_seconds
              << " total_seconds=" << total_seconds << '\n';
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
