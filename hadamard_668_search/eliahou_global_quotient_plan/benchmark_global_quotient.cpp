// Single-core prototype for the complete case-26 parity-quotient census.
//
// This is a measured kernel, not a completed whole-case census.  It consumes
// the derived binary model emitted by verify_global_quotient_plan.py.  The
// known pinned quotient must reproduce 62 joint mod-6 supports.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Sig = std::uint64_t;

constexpr int EQUATIONS = 20;
constexpr int VARIABLES = 78;
constexpr int PAIRS = 39;
constexpr int QUOTIENT_DIMENSION = 18;
constexpr Sig LOW_BITS = 0x5555555555ULL;
constexpr Sig SIGNATURE_MASK = 0xffffffffffULL;

struct Model {
  std::array<std::int16_t, EQUATIONS> constant{};
  std::array<std::int16_t, EQUATIONS * VARIABLES> linear{};
  std::array<std::int16_t, EQUATIONS * VARIABLES * VARIABLES> quadratic{};
  std::array<std::uint8_t, PAIRS * 2> pairs{};
  std::array<std::uint8_t, PAIRS> pair_blocks{};
  std::array<std::uint8_t, PAIRS> pair_phases{};
  std::array<std::uint8_t, PAIRS> particular{};
  std::array<std::uint8_t, QUOTIENT_DIMENSION * PAIRS> basis{};
  std::array<std::uint8_t, PAIRS> pinned{};
  std::array<std::int8_t, 4 * 42> physical_rows{};
  std::array<std::uint8_t, VARIABLES> variable_blocks{};
  std::array<std::uint8_t, VARIABLES> variable_cells{};
  std::uint32_t central = 0;
};

struct ComponentTable {
  std::vector<Sig> signatures;
  std::vector<std::uint8_t> weights;
};

struct SurvivorState {
  std::uint8_t central_value = 0;
  std::uint64_t pair_state = 0;

  bool operator<(const SurvivorState& other) const {
    if (central_value != other.central_value) {
      return central_value < other.central_value;
    }
    return pair_state < other.pair_state;
  }
};

struct Kernel {
  Model model;
  Sig constant = 0;
  std::array<Sig, PAIRS> base_linear{};
  std::array<std::array<Sig, PAIRS>, PAIRS> base_quadratic{};
  std::array<std::array<Sig, PAIRS>, 2> direct_linear{};
  std::array<std::array<std::array<Sig, PAIRS>, PAIRS>, 2>
      base_interaction{};
  std::array<
      std::array<std::array<std::array<Sig, PAIRS>, PAIRS>, 2>, 2>
      pair_quadratic{};

  std::vector<std::int32_t> heads;
  std::vector<std::uint32_t> stamps;
  std::vector<std::uint64_t> entry_keys;
  std::vector<std::int32_t> next;
  std::vector<std::uint32_t> entry_states;
  std::uint32_t generation = 0;

  explicit Kernel(Model input)
      : model(std::move(input)),
        heads(1U << 20, -1),
        stamps(1U << 20, 0),
        entry_keys(1U << 18),
        next(1U << 18),
        entry_states(1U << 18) {
    precompute();
  }

  static Sig add3(Sig left, Sig right) {
    const Sig left_one = left & LOW_BITS;
    const Sig left_two = (left >> 1) & LOW_BITS;
    const Sig left_zero = LOW_BITS ^ left_one ^ left_two;
    const Sig right_one = right & LOW_BITS;
    const Sig right_two = (right >> 1) & LOW_BITS;
    const Sig right_zero = LOW_BITS ^ right_one ^ right_two;
    const Sig result_one =
        (left_zero & right_one) | (left_one & right_zero) |
        (left_two & right_two);
    const Sig result_two =
        (left_zero & right_two) | (left_two & right_zero) |
        (left_one & right_one);
    return (result_one | (result_two << 1)) & SIGNATURE_MASK;
  }

  static Sig negate3(Sig value) {
    const Sig one = value & LOW_BITS;
    const Sig two = (value >> 1) & LOW_BITS;
    return (two | (one << 1)) & SIGNATURE_MASK;
  }

  static Sig scale3(Sig value, int scalar) {
    if (scalar % 3 == 0) return 0;
    return scalar % 3 == 1 ? value : negate3(value);
  }

  static std::uint8_t residue3(std::int16_t value) {
    int residue = value % 3;
    if (residue < 0) residue += 3;
    return static_cast<std::uint8_t>(residue);
  }

  Sig raw_linear(int variable) const {
    Sig result = 0;
    for (int equation = 0; equation < EQUATIONS; ++equation) {
      result |= Sig(residue3(
                    model.linear[equation * VARIABLES + variable]))
                << (2 * equation);
    }
    return result;
  }

  Sig raw_quadratic(int left, int right) const {
    Sig result = 0;
    for (int equation = 0; equation < EQUATIONS; ++equation) {
      const auto offset =
          (equation * VARIABLES + left) * VARIABLES + right;
      result |= Sig(residue3(model.quadratic[offset]))
                << (2 * equation);
    }
    return result;
  }

  void precompute() {
    for (int equation = 0; equation < EQUATIONS; ++equation) {
      constant |= Sig(residue3(model.constant[equation]))
                  << (2 * equation);
    }
    for (int i = 0; i < PAIRS; ++i) {
      const int a = model.pairs[2 * i];
      const int b = model.pairs[2 * i + 1];
      base_linear[i] = raw_linear(a);
      for (int j = 0; j < PAIRS; ++j) {
        const int aj = model.pairs[2 * j];
        base_quadratic[i][j] = raw_quadratic(a, aj);
      }
      for (int parity = 0; parity < 2; ++parity) {
        const int sign = parity == 0 ? 1 : 2;
        direct_linear[parity][i] =
            add3(scale3(raw_linear(a), sign), raw_linear(b));
        if (parity == 0) {
          direct_linear[parity][i] =
              add3(direct_linear[parity][i], raw_quadratic(a, b));
        }
        for (int k = 0; k < PAIRS; ++k) {
          if (i == k) continue;
          const int ak = model.pairs[2 * k];
          base_interaction[parity][i][k] =
              add3(scale3(raw_quadratic(a, ak), sign),
                   raw_quadratic(b, ak));
        }
      }
    }
    for (int left = 0; left < PAIRS; ++left) {
      const int a = model.pairs[2 * left];
      const int b = model.pairs[2 * left + 1];
      for (int right = 0; right < PAIRS; ++right) {
        if (left == right) continue;
        const int c = model.pairs[2 * right];
        const int d = model.pairs[2 * right + 1];
        for (int left_parity = 0; left_parity < 2; ++left_parity) {
          const int left_sign = left_parity == 0 ? 1 : 2;
          for (int right_parity = 0; right_parity < 2;
               ++right_parity) {
            const int right_sign = right_parity == 0 ? 1 : 2;
            Sig value = scale3(raw_quadratic(a, c),
                               (left_sign * right_sign) % 3);
            value = add3(
                value, scale3(raw_quadratic(a, d), left_sign));
            value = add3(
                value, scale3(raw_quadratic(b, c), right_sign));
            value = add3(value, raw_quadratic(b, d));
            pair_quadratic[left_parity][right_parity][left][right] =
                value;
          }
        }
      }
    }

    // Exhaustively self-test packed arithmetic on constant trit vectors.
    for (int left = 0; left < 3; ++left) {
      for (int right = 0; right < 3; ++right) {
        Sig a = 0;
        Sig b = 0;
        for (int equation = 0; equation < EQUATIONS; ++equation) {
          a |= Sig(left) << (2 * equation);
          b |= Sig(right) << (2 * equation);
        }
        const Sig sum = add3(a, b);
        for (int equation = 0; equation < EQUATIONS; ++equation) {
          if (((sum >> (2 * equation)) & 3) !=
              std::uint64_t((left + right) % 3)) {
            throw std::runtime_error("packed trit addition failed");
          }
        }
      }
    }
  }

  ComponentTable component_table(
      const std::vector<int>& variables,
      const std::array<std::uint8_t, PAIRS>& parity,
      const std::array<Sig, PAIRS>& reduced_linear) const {
    const std::size_t count = std::size_t{1} << variables.size();
    ComponentTable table;
    table.signatures.resize(count);
    table.weights.resize(count);
    for (std::size_t mask = 1; mask < count; ++mask) {
      const int local = __builtin_ctzll(mask);
      const std::size_t rest = mask & (mask - 1);
      const int variable = variables[local];
      Sig delta = reduced_linear[variable];
      std::size_t remaining = rest;
      while (remaining) {
        const int other_local = __builtin_ctzll(remaining);
        const int other = variables[other_local];
        delta = add3(
            delta,
            pair_quadratic[parity[variable]][parity[other]]
                            [variable][other]);
        remaining &= remaining - 1;
      }
      table.signatures[mask] = add3(table.signatures[rest], delta);
      table.weights[mask] = static_cast<std::uint8_t>(
          table.weights[rest] + (parity[variable] == 0));
    }
    return table;
  }

  static std::uint64_t hash_key(std::uint64_t value) {
    value ^= value >> 30;
    value *= 0xbf58476d1ce4e5b9ULL;
    value ^= value >> 27;
    value *= 0x94d049bb133111ebULL;
    value ^= value >> 31;
    return value;
  }

  std::uint64_t census_one(
      const std::array<std::uint8_t, PAIRS>& parity,
      std::vector<SurvivorState>* survivor_states = nullptr,
      int fixed_zero_pair = -1) {
    Sig reduced_constant = constant;
    for (int i = 0; i < PAIRS; ++i) {
      if (!parity[i]) continue;
      reduced_constant = add3(reduced_constant, base_linear[i]);
      for (int j = 0; j < i; ++j) {
        if (parity[j]) {
          reduced_constant =
              add3(reduced_constant, base_quadratic[i][j]);
        }
      }
    }

    std::array<Sig, PAIRS> reduced_linear{};
    for (int i = 0; i < PAIRS; ++i) {
      reduced_linear[i] = direct_linear[parity[i]][i];
      for (int k = 0; k < PAIRS; ++k) {
        if (k != i && parity[k]) {
          reduced_linear[i] = add3(
              reduced_linear[i],
              base_interaction[parity[i]][i][k]);
        }
      }
    }

    std::array<std::vector<int>, 4> components;
    int odd_pairs = 0;
    for (int i = 0; i < PAIRS; ++i) {
      odd_pairs += parity[i];
      if (i == static_cast<int>(model.central)) continue;
      if (model.pair_blocks[i] > 1) {
        throw std::runtime_error("noncentral pair has invalid block");
      }
      const int component =
          2 * model.pair_blocks[i] +
          (parity[i] ^ model.pair_phases[i]);
      components[component].push_back(i);
    }
    if (fixed_zero_pair >= 0) {
      if (
          fixed_zero_pair >= PAIRS ||
          fixed_zero_pair == static_cast<int>(model.central) ||
          model.pair_blocks[fixed_zero_pair] != 0 ||
          parity[fixed_zero_pair] != 1) {
        throw std::runtime_error(
            "reflection gauge pair is not an odd noncentral L pair");
      }
      bool removed = false;
      for (auto& component : components) {
        const auto place = std::find(
            component.begin(), component.end(), fixed_zero_pair);
        if (place != component.end()) {
          component.erase(place);
          removed = true;
          break;
        }
      }
      if (!removed) {
        throw std::runtime_error(
            "reflection gauge pair was absent from the components");
      }
    }
    if ((odd_pairs & 1) == 0) {
      throw std::runtime_error("quotient point has even parity");
    }
    const int full_even_total = (39 - odd_pairs) / 2;
    std::uint64_t survivors = 0;

    for (int central_value = 0; central_value < 2; ++central_value) {
      auto effective_linear = reduced_linear;
      if (central_value) {
        for (int i = 0; i < PAIRS; ++i) {
          if (i == static_cast<int>(model.central)) continue;
          effective_linear[i] = add3(
              effective_linear[i],
              pair_quadratic[parity[i]][parity[model.central]]
                              [i][model.central]);
        }
      }
      Sig target = reduced_constant;
      if (central_value) {
        target = add3(target, reduced_linear[model.central]);
      }
      target = negate3(target);
      const int remaining_full =
          full_even_total -
          (parity[model.central] == 0 ? central_value : 0);
      if (remaining_full < 0) continue;

      // Component order is L-color-0, L-color-1, S-color-0, S-color-1.
      // Each may contain both even and odd raw pair parities, so every table
      // tracks its own number of selected full-even pairs.
      const auto left_zero = component_table(
          components[0], parity, effective_linear);
      const auto left_one = component_table(
          components[1], parity, effective_linear);
      const auto right_zero = component_table(
          components[2], parity, effective_linear);
      const auto right_one = component_table(
          components[3], parity, effective_linear);

      ++generation;
      std::size_t entry = 0;
      for (std::size_t zero_state = 0;
           zero_state < right_zero.signatures.size(); ++zero_state) {
        for (std::size_t one_state = 0;
             one_state < right_one.signatures.size(); ++one_state) {
          const int weight =
              right_zero.weights[zero_state] +
              right_one.weights[one_state];
          const Sig signature =
              add3(right_zero.signatures[zero_state],
                   right_one.signatures[one_state]);
          const std::uint64_t key =
              signature | (std::uint64_t(weight) << 40);
          const std::uint32_t bucket =
              hash_key(key) & ((1U << 20) - 1);
          if (stamps[bucket] != generation) {
            stamps[bucket] = generation;
            heads[bucket] = -1;
          }
          entry_keys[entry] = key;
          next[entry] = heads[bucket];
          entry_states[entry] = static_cast<std::uint32_t>(
              zero_state |
              (one_state << components[2].size()));
          heads[bucket] = static_cast<std::int32_t>(entry);
          ++entry;
        }
      }
      if (entry != (1U << 18)) {
        throw std::runtime_error("right table lost its fixed cardinality");
      }

      for (std::size_t zero_state = 0;
           zero_state < left_zero.signatures.size(); ++zero_state) {
        for (std::size_t one_state = 0;
             one_state < left_one.signatures.size(); ++one_state) {
          const int left_weight =
              left_zero.weights[zero_state] +
              left_one.weights[one_state];
          const int needed_weight = remaining_full - left_weight;
          if (needed_weight < 0 || needed_weight > 18) continue;
          const Sig left_signature =
              add3(left_zero.signatures[zero_state],
                   left_one.signatures[one_state]);
          const Sig needed_signature =
              add3(target, negate3(left_signature));
          const std::uint64_t key =
              needed_signature |
              (std::uint64_t(needed_weight) << 40);
          const std::uint32_t bucket =
              hash_key(key) & ((1U << 20) - 1);
          if (stamps[bucket] != generation) continue;
          for (std::int32_t candidate = heads[bucket]; candidate >= 0;
               candidate = next[candidate]) {
            if (entry_keys[candidate] != key) continue;
            ++survivors;
            if (survivor_states != nullptr) {
              std::uint64_t pair_state =
                  std::uint64_t(central_value) << model.central;
              const auto place_component =
                  [&](int component_index, std::uint64_t state) {
                    const auto& variables = components[component_index];
                    for (std::size_t local = 0;
                         local < variables.size(); ++local) {
                      if ((state >> local) & 1ULL) {
                        pair_state |=
                            1ULL << variables[local];
                      }
                    }
                  };
              place_component(0, zero_state);
              place_component(1, one_state);
              const std::uint32_t encoded =
                  entry_states[candidate];
              const std::size_t right_zero_size =
                  components[2].size();
              const std::uint64_t right_zero_mask =
                  right_zero_size == 64
                      ? std::numeric_limits<std::uint64_t>::max()
                      : ((1ULL << right_zero_size) - 1);
              place_component(2, encoded & right_zero_mask);
              place_component(3, encoded >> right_zero_size);
              survivor_states->push_back(
                  SurvivorState{
                      static_cast<std::uint8_t>(central_value),
                      pair_state});
            }
          }
        }
      }
    }
    return survivors;
  }
};

template <typename T>
void read_exact(std::ifstream& stream, T* destination, std::size_t count) {
  stream.read(reinterpret_cast<char*>(destination),
              static_cast<std::streamsize>(sizeof(T) * count));
  if (!stream) throw std::runtime_error("truncated benchmark model");
}

Model read_model(const std::string& path) {
  std::ifstream stream(path, std::ios::binary);
  if (!stream) throw std::runtime_error("cannot open benchmark model");
  char magic[8]{};
  read_exact(stream, magic, 8);
  if (std::memcmp(magic, "H668GQ2", 7) != 0) {
    throw std::runtime_error("invalid benchmark-model magic");
  }
  std::array<std::uint32_t, 5> dimensions{};
  read_exact(stream, dimensions.data(), dimensions.size());
  if (dimensions[0] != EQUATIONS || dimensions[1] != VARIABLES ||
      dimensions[2] != PAIRS || dimensions[3] != QUOTIENT_DIMENSION ||
      dimensions[4] >= PAIRS) {
    throw std::runtime_error("benchmark-model dimensions changed");
  }
  Model model;
  model.central = dimensions[4];
  read_exact(stream, model.constant.data(), model.constant.size());
  read_exact(stream, model.linear.data(), model.linear.size());
  read_exact(stream, model.quadratic.data(), model.quadratic.size());
  read_exact(stream, model.pairs.data(), model.pairs.size());
  read_exact(stream, model.pair_blocks.data(), model.pair_blocks.size());
  read_exact(stream, model.pair_phases.data(), model.pair_phases.size());
  read_exact(stream, model.particular.data(), model.particular.size());
  read_exact(stream, model.basis.data(), model.basis.size());
  read_exact(stream, model.pinned.data(), model.pinned.size());
  read_exact(
      stream, model.physical_rows.data(), model.physical_rows.size());
  read_exact(
      stream, model.variable_blocks.data(), model.variable_blocks.size());
  read_exact(
      stream, model.variable_cells.data(), model.variable_cells.size());
  char trailing;
  if (stream.read(&trailing, 1)) {
    throw std::runtime_error("benchmark model has trailing bytes");
  }
  return model;
}

std::array<std::uint8_t, PAIRS> quotient_point(
    const Model& model, std::uint32_t index) {
  auto point = model.particular;
  for (int bit = 0; bit < QUOTIENT_DIMENSION; ++bit) {
    if ((index >> bit) & 1U) {
      for (int pair = 0; pair < PAIRS; ++pair) {
        point[pair] ^= model.basis[bit * PAIRS + pair];
      }
    }
  }
  return point;
}

}  // namespace

#ifndef H668_GQ_NO_MAIN
int main(int argc, char** argv) {
  try {
    if (argc < 3) {
      std::cerr << "usage: " << argv[0]
                << " MODEL (--pinned | --states N [--start I])\n";
      return 2;
    }
    const std::string model_path = argv[1];
    Model model = read_model(model_path);
    bool pinned = false;
    std::uint32_t states = 0;
    std::uint32_t start = 0;
    for (int argument = 2; argument < argc; ++argument) {
      const std::string option = argv[argument];
      if (option == "--pinned") {
        pinned = true;
      } else if (option == "--states" && argument + 1 < argc) {
        states = static_cast<std::uint32_t>(
            std::stoul(argv[++argument]));
      } else if (option == "--start" && argument + 1 < argc) {
        start = static_cast<std::uint32_t>(
            std::stoul(argv[++argument]));
      } else {
        throw std::runtime_error("invalid command-line argument");
      }
    }
    if (pinned == (states != 0)) {
      throw std::runtime_error(
          "choose exactly one of --pinned and --states");
    }
    if (!pinned &&
        (start >= (1U << QUOTIENT_DIMENSION) ||
         states > (1U << QUOTIENT_DIMENSION) - start)) {
      throw std::runtime_error("requested quotient range is invalid");
    }

    Kernel kernel(model);
    const auto started = std::chrono::steady_clock::now();
    std::uint64_t survivors = 0;
    if (pinned) {
      survivors = kernel.census_one(model.pinned);
      states = 1;
    } else {
      for (std::uint32_t offset = 0; offset < states; ++offset) {
        survivors +=
            kernel.census_one(quotient_point(model, start + offset));
      }
    }
    const double seconds =
        std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started)
            .count();
    const std::uint64_t join_rows =
        std::uint64_t(states) * ((1U << 20) + (1U << 18)) * 2;
    // Each quotient is conditioned on both values of the central pair.  The
    // Python prototype's 3.4 s timing likewise includes both values.
    std::cout << "{\n"
              << "  \"mode\": \"" << (pinned ? "pinned" : "range")
              << "\",\n"
              << "  \"start\": " << start << ",\n"
              << "  \"quotient_states\": " << states << ",\n"
              << "  \"central_values_per_state\": 2,\n"
              << "  \"join_rows\": " << join_rows << ",\n"
              << "  \"joint_mod6_supports\": " << survivors << ",\n"
              << "  \"seconds\": " << seconds << ",\n"
              << "  \"join_rows_per_second\": "
              << (join_rows / seconds) << "\n"
              << "}\n";
    if (pinned && survivors != 62) {
      throw std::runtime_error(
          "pinned quotient did not reproduce 62 survivors");
    }
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
  return 0;
}
#endif
