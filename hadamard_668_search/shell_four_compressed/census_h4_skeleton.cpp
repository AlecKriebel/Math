// Valuation-skeleton census for the LP(333) order-three shell
// (n_9,n_3,n_0)=(4,6,14).
//
// This scratch verifier deliberately reuses only the audited exact alphabet,
// cyclotomic classes, and direct Eisenstein correlation implementation from
// the production shell-four verifier.  Its enumeration is different: every
// medium letter is reduced to sigma*(1-omega), sigma in {+1,-1}, before any
// phase is restored.

#define main production_shell_four_main
#include "../verify_lp333_order3_profile_shell_four.cpp"
#undef main

#include <numeric>

namespace {

using LocalSkeleton = std::array<std::int8_t, 4>;

int medium_id(int sign, int phase) {
  // lambda=1-omega.  The IDs are checked against raw_profile below.
  constexpr std::array<int, 3> positive = {7, 6, 1};
  constexpr std::array<int, 3> negative = {2, 4, 8};
  if (sign == 1) return positive.at(phase);
  if (sign == -1) return negative.at(phase);
  throw std::runtime_error("medium sign must be nonzero");
}

int local_weight(const LocalSkeleton &state) {
  return std::count_if(state.begin(), state.end(),
                       [](int value) { return value != 0; });
}

std::vector<LocalSkeleton> make_local_skeletons() {
  std::vector<LocalSkeleton> result;
  for (int a0 = -1; a0 <= 1; ++a0)
    for (int a1 = -1; a1 <= 1; ++a1)
      for (int b0 = -1; b0 <= 1; ++b0)
        for (int b1 = -1; b1 <= 1; ++b1) {
          // This is the residue of the audited pair-signature equality.
          if (mod3(-a0 + a1 + b0 - b1) == 0) {
            result.push_back(
                {static_cast<std::int8_t>(a0),
                 static_cast<std::int8_t>(a1),
                 static_cast<std::int8_t>(b0),
                 static_cast<std::int8_t>(b1)});
          }
        }
  return result;
}

struct Result {
  std::array<std::uint64_t, 3> patterns{};
  std::map<int, std::uint64_t> support_histogram;
  std::uint64_t skeletons = 0;
  std::uint64_t extendible_supports = 0;
  std::uint64_t primitive_assignments = 0;
  std::array<std::array<std::uint64_t, 3>, 3> aggregate_residues{};
  std::set<std::array<std::int8_t, 24>> orbit_representatives;
};

class SkeletonEnumerator {
 public:
  explicit SkeletonEnumerator(std::vector<LocalSkeleton> local)
      : local_(std::move(local)) {}

  Result run() {
    enumerate(0, 0);
    return result_;
  }

 private:
  void enumerate(int quartet, int used) {
    if (quartet == 6) {
      if (used == 6) record();
      return;
    }
    int remaining = 5 - quartet;
    for (const LocalSkeleton &state : local_) {
      int weight = local_weight(state);
      int next = used + weight;
      if (next > 6 || next + 4 * remaining < 6) continue;
      selected_[quartet] = state;
      enumerate(quartet + 1, next);
    }
  }

  int pattern_index() const {
    std::array<int, 6> weights{};
    for (int j = 0; j < 6; ++j) {
      weights[j] = local_weight(selected_[j]);
    }
    std::sort(weights.begin(), weights.end());
    if (weights == std::array<int, 6>{0, 0, 0, 2, 2, 2}) return 0;
    if (weights == std::array<int, 6>{0, 0, 0, 0, 3, 3}) return 1;
    if (weights == std::array<int, 6>{0, 0, 0, 0, 2, 4}) return 2;
    throw std::runtime_error("unexpected six-medium partition");
  }

  Assignment baseline_assignment() const {
    Assignment assignment = zero_assignment();
    for (int quartet = 0; quartet < 6; ++quartet) {
      for (int slot = 0; slot < 4; ++slot) {
        int sign = selected_[quartet][slot];
        if (sign != 0) {
          assignment[position(quartet, slot)] =
              static_cast<std::uint8_t>(medium_id(sign, 0));
        }
      }
    }
    return assignment;
  }

  std::array<int, 2> aggregate_residue(
      const Assignment &assignment) const {
    std::array<int, 2> result{};
    for (int pos = 0; pos < POSITION_COUNT; ++pos) {
      if (assignment[pos] == ZERO_ID) continue;
      E value = coefficient(pos, assignment[pos]);
      int channel = pos / CLASS_COUNT;
      result[channel] = mod3(result[channel] + value.a);
      if (mod3(value.a + value.b) != 0) {
        throw std::runtime_error(
            "a medium residue left its scalar lambda line");
      }
    }
    return result;
  }

  int extendible_support_count(const Assignment &baseline,
                               const Sig &signature) const {
    // The coefficient of x^k after processing some quartets counts high
    // supports of size k whose empty-medium flag equations are satisfied.
    std::array<std::uint64_t, 5> polynomial = {1, 0, 0, 0, 0};
    for (int quartet = 0; quartet < 6; ++quartet) {
      int medium = local_weight(selected_[quartet]);
      std::array<std::uint64_t, 5> local{};
      int available_mask = 0;
      for (int slot = 0; slot < 4; ++slot) {
        int pos = position(quartet, slot);
        if (baseline[pos] == ZERO_ID) available_mask |= 1 << slot;
      }
      for (int subset = available_mask;; subset = (subset - 1) & available_mask) {
        int count = std::popcount(static_cast<unsigned>(subset));
        bool admitted = medium > 0;
        if (!admitted) {
          auto base = sig_part(signature, quartet);
          int flag = (base.first + base.second) % 3;
          for (int slot = 0; slot < 4; ++slot) {
            if (subset >> slot & 1) {
              flag += high_flag[position(quartet, slot)];
            }
          }
          admitted = flag % 3 == 0;
        }
        if (admitted) ++local[count];
        if (subset == 0) break;
      }
      std::array<std::uint64_t, 5> next{};
      for (int left = 0; left <= 4; ++left)
        for (int right = 0; left + right <= 4; ++right)
          next[left + right] += polynomial[left] * local[right];
      polynomial = next;
    }
    return static_cast<int>(polynomial[4]);
  }

  void record() {
    ++result_.skeletons;
    int pattern = pattern_index();
    ++result_.patterns[pattern];
    Assignment baseline = baseline_assignment();
    Sig signature =
        divided_signature(direct_six(baseline), "skeleton baseline");
    int supports = extendible_support_count(baseline, signature);
    ++result_.support_histogram[supports];
    result_.extendible_supports += supports;

    int nonempty = 0;
    for (const LocalSkeleton &state : selected_) {
      nonempty += local_weight(state) > 0;
    }
    std::uint64_t medium_phase_solutions = 1;
    for (int exponent = 0; exponent < 6 - nonempty; ++exponent) {
      medium_phase_solutions *= 3;
    }
    constexpr std::uint64_t high_phases = 81;  // 3^4
    result_.primitive_assignments +=
        static_cast<std::uint64_t>(supports) *
        medium_phase_solutions * high_phases;

    auto residue = aggregate_residue(baseline);
    ++result_.aggregate_residues[residue[0]][residue[1]];

    std::array<std::int8_t, 24> raw{};
    for (int quartet = 0; quartet < 6; ++quartet) {
      raw[quartet] = selected_[quartet][0];
      raw[quartet + 6] = selected_[quartet][1];
      raw[12 + quartet] = selected_[quartet][2];
      raw[12 + quartet + 6] = selected_[quartet][3];
    }
    std::array<std::int8_t, 24> canonical{};
    canonical.fill(2);
    for (int rotation = 0; rotation < 6; ++rotation) {
      int offset = 2 * rotation;
      for (int star_a = 0; star_a < 2; ++star_a) {
        for (int star_b = 0; star_b < 2; ++star_b) {
          std::array<std::int8_t, 24> image{};
          for (int channel = 0; channel < 2; ++channel) {
            int star = channel == 0 ? star_a : star_b;
            int sign = star ? -1 : 1;
            int shift = (offset + (star ? 6 : 0)) % 12;
            for (int index = 0; index < 12; ++index) {
              image[12 * channel + index] =
                  static_cast<std::int8_t>(
                      sign * raw[12 * channel + (index + shift) % 12]);
            }
          }
          canonical = std::min(canonical, image);
        }
      }
    }
    result_.orbit_representatives.insert(canonical);
  }

  std::vector<LocalSkeleton> local_;
  std::array<LocalSkeleton, 6> selected_{};
  Result result_;
};

void audit_medium_coordinates() {
  E lambda{1, -1};
  E omega{0, 1};
  E power{1, 0};
  for (int phase = 0; phase < 3; ++phase) {
    E expected = multiply(lambda, power);
    if (raw_profile(medium_id(1, phase)) != expected ||
        raw_profile(medium_id(-1, phase)) != -1 * expected) {
      throw std::runtime_error("medium sign/phase coordinates changed");
    }
    power = multiply(power, omega);
  }
}

}  // namespace

#ifndef H4_CENSUS_LIBRARY
int main() {
  initialize_classes();
  initialize_signature_arithmetic();
  audit_alphabet();
  initialize_variable_tables();
  audit_medium_coordinates();

  auto local = make_local_skeletons();
  std::array<int, 5> local_histogram{};
  for (const LocalSkeleton &state : local) {
    ++local_histogram[local_weight(state)];
  }
  if (local_histogram != std::array<int, 5>{1, 0, 12, 8, 6}) {
    throw std::runtime_error("signed local quartet census changed");
  }

  Result result = SkeletonEnumerator(std::move(local)).run();
  std::cout << "local_skeletons=27\n";
  for (int weight = 0; weight <= 4; ++weight) {
    std::cout << "local_weight[" << weight << "]="
              << local_histogram[weight] << "\n";
  }
  std::cout << "skeletons=" << result.skeletons << "\n";
  std::cout << "pattern_222000=" << result.patterns[0] << "\n";
  std::cout << "pattern_330000=" << result.patterns[1] << "\n";
  std::cout << "pattern_420000=" << result.patterns[2] << "\n";
  for (const auto &[supports, skeletons] : result.support_histogram) {
    std::cout << "supports[" << supports << "]=" << skeletons << "\n";
  }
  std::cout << "extendible_supports=" << result.extendible_supports << "\n";
  std::cout << "primitive_assignments="
            << result.primitive_assignments << "\n";
  std::cout << "skeleton_orbits="
            << result.orbit_representatives.size() << "\n";
  for (int a = 0; a < 3; ++a)
    for (int b = 0; b < 3; ++b)
      std::cout << "aggregate[" << a << "," << b << "]="
                << result.aggregate_residues[a][b] << "\n";
}
#endif
