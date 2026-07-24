// Lossless signed-skeleton/MITM verifier for the LP(333) order-three shell
// (n_9,n_3,n_0)=(4,6,14).
//
// Unlike the production shell-four verifier, this program never enumerates
// the 27,468,720 fully phased medium frames.  It works on the 1,704 exact
// signed-skeleton orbits, restores phases additively modulo nine, joins two
// groups of three opposite quartets, then independently replays every
// surviving full-assignment orbit on all 37 physical lags.

#define H4_CENSUS_LIBRARY
#include "census_h4_skeleton.cpp"

#include <bit>
#include <functional>
#include <unordered_map>

namespace {

struct SlotOption {
  std::uint8_t profile_id = ZERO_ID;
  std::uint8_t is_high = 0;
  Sig correction{};
  Target aggregate_delta{};
};

struct LocalLift {
  std::array<std::uint8_t, 4> profile_ids{};
  std::uint8_t high_count = 0;
  std::uint16_t a_signature = 0;
  Target aggregate_delta{};
};

struct HalfRecord {
  std::uint16_t signature = 0;
  std::uint8_t high_count = 0;
  Target aggregate_delta{};
  std::uint32_t path = 0;
};

using RawSkeleton = std::array<std::int8_t, POSITION_COUNT>;
using PackedAssignment = std::array<std::uint8_t, POSITION_COUNT>;

struct H4Counters {
  std::uint64_t skeleton_orbits = 0;
  std::uint64_t half_records_generated = 0;
  std::uint64_t join_hits_with_stabilizer_duplicates = 0;
  std::uint64_t assignment_orbits = 0;
  std::uint64_t raw_mod9_survivors = 0;
  std::array<std::uint64_t, TARGETS.size()> raw_target_survivors{};
  std::map<int, std::uint64_t> raw_bad_class_histogram;
  std::uint64_t exact_profiles = 0;
  std::size_t maximum_right_records = 0;
  std::size_t maximum_right_keys = 0;
};

int conjugate_profile_id(int id) {
  E target = conjugate(raw_profile(id));
  for (int candidate = 0; candidate < 10; ++candidate) {
    if (raw_profile(candidate) == target) return candidate;
  }
  throw std::runtime_error("the profile alphabet is not conjugation-stable");
}

PackedAssignment canonical_assignment(const PackedAssignment &raw) {
  PackedAssignment canonical{};
  canonical.fill(10);
  for (int rotation = 0; rotation < 6; ++rotation) {
    int offset = 2 * rotation;
    for (int star_a = 0; star_a < 2; ++star_a) {
      for (int star_b = 0; star_b < 2; ++star_b) {
        PackedAssignment image{};
        for (int channel = 0; channel < 2; ++channel) {
          bool star = channel == 0 ? star_a : star_b;
          int shift = (offset + (star ? 6 : 0)) % 12;
          for (int index = 0; index < 12; ++index) {
            int id = raw[12 * channel + (index + shift) % 12];
            image[12 * channel + index] =
                static_cast<std::uint8_t>(
                    star ? conjugate_profile_id(id) : id);
          }
        }
        canonical = std::min(canonical, image);
      }
    }
  }
  return canonical;
}

int assignment_stabilizer(const PackedAssignment &raw) {
  int fixed = 0;
  for (int rotation = 0; rotation < 6; ++rotation) {
    int offset = 2 * rotation;
    for (int star_a = 0; star_a < 2; ++star_a) {
      for (int star_b = 0; star_b < 2; ++star_b) {
        bool same = true;
        for (int channel = 0; channel < 2 && same; ++channel) {
          bool star = channel == 0 ? star_a : star_b;
          int shift = (offset + (star ? 6 : 0)) % 12;
          for (int index = 0; index < 12; ++index) {
            int id = raw[12 * channel + (index + shift) % 12];
            if (star) id = conjugate_profile_id(id);
            if (id != raw[12 * channel + index]) {
              same = false;
              break;
            }
          }
        }
        fixed += same;
      }
    }
  }
  if (fixed == 0 || 24 % fixed != 0) {
    throw std::runtime_error("invalid exact-assignment stabilizer");
  }
  return fixed;
}

Target assignment_aggregate(const PackedAssignment &assignment) {
  Target result{};
  for (int pos = 0; pos < POSITION_COUNT; ++pos) {
    E value = coefficient(pos, assignment[pos]);
    int channel = pos / CLASS_COUNT;
    result[2 * channel] += value.a;
    result[2 * channel + 1] += value.b;
  }
  return result;
}

int exact_target_index(const Target &target) {
  for (int index = 0; index < static_cast<int>(TARGETS.size()); ++index) {
    if (TARGETS[index] == target) return index;
  }
  return -1;
}

std::array<E, P> detached_physical(
    const PackedAssignment &assignment) {
  std::array<std::array<E, P>, 2> word{};
  word[0][0] = {-1, 0};
  word[1][0] = {2, 0};
  for (int channel = 0; channel < 2; ++channel) {
    for (int value = 1; value < P; ++value) {
      int cls = class_of[value];
      word[channel][value] =
          coefficient(channel * CLASS_COUNT + cls,
                      assignment[channel * CLASS_COUNT + cls]);
    }
  }
  std::array<E, P> result{};
  for (int lag = 0; lag < P; ++lag) {
    E sum{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int value = 0; value < P; ++value) {
        sum = sum + multiply(word[channel][(value + lag) % P],
                             conjugate(word[channel][value]));
      }
    }
    if (lag == 0) sum.a -= 167;
    result[lag] = sum;
  }
  return result;
}

std::uint64_t pack_key(int high_count, int signature,
                       const Target &aggregate) {
  if (high_count < 0 || high_count > 4 ||
      signature < 0 || signature >= 729) {
    return std::numeric_limits<std::uint64_t>::max();
  }
  std::uint64_t key = static_cast<std::uint64_t>(signature);
  key |= static_cast<std::uint64_t>(high_count) << 10;
  int shift = 13;
  for (int value : aggregate) {
    if (value < -31 || value > 31) {
      return std::numeric_limits<std::uint64_t>::max();
    }
    key |= static_cast<std::uint64_t>(value + 31) << shift;
    shift += 6;
  }
  return key;
}

Target target_subtract(Target left, const Target &right) {
  for (int coordinate = 0; coordinate < 4; ++coordinate) {
    left[coordinate] -= right[coordinate];
  }
  return left;
}

Target target_add(Target left, const Target &right) {
  for (int coordinate = 0; coordinate < 4; ++coordinate) {
    left[coordinate] += right[coordinate];
  }
  return left;
}

class OrbitProcessor {
 public:
  OrbitProcessor(const RawSkeleton &raw, H4Counters &counters,
                 std::set<PackedAssignment> &survivor_orbits)
      : raw_(raw), counters_(counters), survivor_orbits_(survivor_orbits) {
    build_baseline();
    build_slot_options();
    build_local_tables();
  }

  void run() {
    choose_balanced_partition();
    std::vector<HalfRecord> right;
    enumerate_half(right_quartets_, 0, {}, right);
    counters_.half_records_generated += right.size();
    counters_.maximum_right_records =
        std::max(counters_.maximum_right_records, right.size());

    std::unordered_map<std::uint64_t, std::vector<std::uint32_t>> index;
    index.reserve(right.size() * 2 + 1);
    for (const HalfRecord &record : right) {
      std::uint64_t key =
          pack_key(record.high_count, record.signature,
                   record.aggregate_delta);
      if (key == std::numeric_limits<std::uint64_t>::max()) {
        throw std::runtime_error("a right-half aggregate left the packed key");
      }
      index[key].push_back(record.path);
    }
    counters_.maximum_right_keys =
        std::max(counters_.maximum_right_keys, index.size());

    HalfRecord start;
    enumerate_left_and_join(0, start, index);
  }

 private:
  void build_baseline() {
    baseline_.fill(ZERO_ID);
    for (int pos = 0; pos < POSITION_COUNT; ++pos) {
      int sign = raw_[pos];
      if (sign != 0) {
        baseline_[pos] =
            static_cast<std::uint8_t>(medium_id(sign, 0));
      }
    }
    baseline_six_ = direct_six(baseline_);
    baseline_signature_ =
        divided_signature(baseline_six_, "orbit skeleton baseline");
    baseline_aggregate_ = assignment_aggregate(baseline_);
  }

  Sig correction_signature(int pos, int id) const {
    if (baseline_[pos] == id) return {};
    PackedAssignment changed = baseline_;
    changed[pos] = static_cast<std::uint8_t>(id);
    Six difference =
        six_subtract(direct_six(changed), baseline_six_);
    return divided_signature(difference, "one-slot lift correction");
  }

  Target correction_aggregate(int pos, int id) const {
    Target result{};
    E before = coefficient(pos, baseline_[pos]);
    E after = coefficient(pos, id);
    E delta = after - before;
    int channel = pos / CLASS_COUNT;
    result[2 * channel] = delta.a;
    result[2 * channel + 1] = delta.b;
    return result;
  }

  void build_slot_options() {
    std::vector<E> nonzero_corrections;
    for (int pos = 0; pos < POSITION_COUNT; ++pos) {
      std::vector<int> ids;
      if (baseline_[pos] == ZERO_ID) {
        ids = {ZERO_ID, HIGH_IDS[0], HIGH_IDS[1], HIGH_IDS[2]};
      } else {
        int sign = raw_[pos];
        ids = {medium_id(sign, 0), medium_id(sign, 1),
               medium_id(sign, 2)};
      }
      for (int id : ids) {
        SlotOption option;
        option.profile_id = static_cast<std::uint8_t>(id);
        option.is_high =
            static_cast<std::uint8_t>(profile_norm(id) == 9);
        option.correction = correction_signature(pos, id);
        option.aggregate_delta = correction_aggregate(pos, id);
        options_[pos].push_back(option);
        E delta =
            raw_profile(id) - raw_profile(baseline_[pos]);
        if (delta != E{}) {
          if (delta.a % 3 || delta.b % 3) {
            throw std::runtime_error(
                "a lift correction is not coefficientwise divisible by 3");
          }
          nonzero_corrections.push_back(delta);
        }
        for (int part = 0; part < 6; ++part) {
          auto value = sig_part(option.correction, part);
          int flag = (value.first + value.second) % 3;
          if (part != pos % 6 && flag != 0) {
            throw std::runtime_error(
                "a one-slot correction changed a remote flag");
          }
        }
      }
    }
    for (E left : nonzero_corrections) {
      for (E right : nonzero_corrections) {
        E product = multiply(left, conjugate(right));
        if (product.a % 9 || product.b % 9) {
          throw std::runtime_error(
              "two lift corrections have a nonzero cross term modulo 9");
        }
      }
    }
  }

  void enumerate_local(int quartet, int slot, LocalLift state) {
    if (slot == 4) {
      auto base = sig_part(baseline_signature_, quartet);
      int base_flag = (base.first + base.second) % 3;
      int correction_flag = 0;
      int a_code = state.a_signature;
      correction_flag =
          (trits[a_code][quartet] +
           trits[local_b_signature_][quartet]) % 3;
      if ((base_flag + correction_flag) % 3 != 0) return;
      local_tables_[quartet].push_back(state);
      return;
    }
    int pos = position(quartet, slot);
    std::uint16_t saved_b = local_b_signature_;
    for (const SlotOption &option : options_[pos]) {
      if (state.high_count + option.is_high > 4) continue;
      LocalLift next = state;
      next.profile_ids[slot] = option.profile_id;
      next.high_count += option.is_high;
      next.a_signature =
          add_code[next.a_signature * 729 + option.correction.a];
      local_b_signature_ =
          add_code[saved_b * 729 + option.correction.b];
      next.aggregate_delta =
          target_add(next.aggregate_delta, option.aggregate_delta);
      enumerate_local(quartet, slot + 1, next);
    }
    local_b_signature_ = saved_b;
  }

  void build_local_tables() {
    for (int quartet = 0; quartet < 6; ++quartet) {
      local_b_signature_ = 0;
      enumerate_local(quartet, 0, {});
      if (local_tables_[quartet].empty() ||
          local_tables_[quartet].size() > 255) {
        throw std::runtime_error("unexpected local lift-table size");
      }
    }
  }

  void choose_balanced_partition() {
    std::uint64_t best = std::numeric_limits<std::uint64_t>::max();
    for (int a = 0; a < 6; ++a)
      for (int b = a + 1; b < 6; ++b)
        for (int c = b + 1; c < 6; ++c) {
          std::array<int, 3> left = {a, b, c};
          std::array<int, 3> right{};
          int cursor = 0;
          for (int q = 0; q < 6; ++q) {
            if (q != a && q != b && q != c) right[cursor++] = q;
          }
          std::uint64_t left_product = 1;
          std::uint64_t right_product = 1;
          for (int q : left) left_product *= local_tables_[q].size();
          for (int q : right) right_product *= local_tables_[q].size();
          std::uint64_t score = std::max(left_product, right_product);
          if (score < best) {
            best = score;
            left_quartets_ = left;
            right_quartets_ = right;
          }
        }
  }

  void enumerate_half(const std::array<int, 3> &quartets, int depth,
                      HalfRecord state, std::vector<HalfRecord> &output) {
    if (depth == 3) {
      output.push_back(state);
      return;
    }
    int quartet = quartets[depth];
    for (int index = 0;
         index < static_cast<int>(local_tables_[quartet].size());
         ++index) {
      const LocalLift &local = local_tables_[quartet][index];
      if (state.high_count + local.high_count > 4) continue;
      HalfRecord next = state;
      next.signature =
          add_code[next.signature * 729 + local.a_signature];
      next.high_count += local.high_count;
      next.aggregate_delta =
          target_add(next.aggregate_delta, local.aggregate_delta);
      next.path |= static_cast<std::uint32_t>(index) << (8 * depth);
      enumerate_half(quartets, depth + 1, next, output);
    }
  }

  void enumerate_left_and_join(
      int depth, HalfRecord state,
      const std::unordered_map<std::uint64_t,
                               std::vector<std::uint32_t>> &right_index) {
    if (depth < 3) {
      int quartet = left_quartets_[depth];
      for (int index = 0;
           index < static_cast<int>(local_tables_[quartet].size());
           ++index) {
        const LocalLift &local = local_tables_[quartet][index];
        if (state.high_count + local.high_count > 4) continue;
        HalfRecord next = state;
        next.signature =
            add_code[next.signature * 729 + local.a_signature];
        next.high_count += local.high_count;
        next.aggregate_delta =
            target_add(next.aggregate_delta, local.aggregate_delta);
        next.path |= static_cast<std::uint32_t>(index) << (8 * depth);
        enumerate_left_and_join(depth + 1, next, right_index);
      }
      return;
    }

    int high_needed = 4 - state.high_count;
    if (high_needed < 0 || high_needed > 4) return;
    int used_signature =
        add_code[baseline_signature_.a * 729 + state.signature];
    int signature_needed = negate_code[used_signature];
    for (int target = 0; target < static_cast<int>(TARGETS.size());
         ++target) {
      Target needed =
          target_subtract(TARGETS[target], baseline_aggregate_);
      needed = target_subtract(needed, state.aggregate_delta);
      std::uint64_t key =
          pack_key(high_needed, signature_needed, needed);
      if (key == std::numeric_limits<std::uint64_t>::max()) continue;
      auto found = right_index.find(key);
      if (found == right_index.end()) continue;
      for (std::uint32_t right_path : found->second) {
        ++counters_.join_hits_with_stabilizer_duplicates;
        replay_join(state.path, right_path, target);
      }
    }
  }

  void replay_join(std::uint32_t left_path, std::uint32_t right_path,
                   int target_index) {
    PackedAssignment assignment = baseline_;
    for (int depth = 0; depth < 3; ++depth) {
      int left_q = left_quartets_[depth];
      int left_index = (left_path >> (8 * depth)) & 255;
      const LocalLift &left = local_tables_[left_q].at(left_index);
      int right_q = right_quartets_[depth];
      int right_index = (right_path >> (8 * depth)) & 255;
      const LocalLift &right = local_tables_[right_q].at(right_index);
      for (int slot = 0; slot < 4; ++slot) {
        assignment[position(left_q, slot)] = left.profile_ids[slot];
        assignment[position(right_q, slot)] = right.profile_ids[slot];
      }
    }

    if (assignment_aggregate(assignment) != TARGETS[target_index]) {
      throw std::runtime_error("the MITM aggregate join is not exact");
    }
    int medium = 0;
    int high = 0;
    for (int id : assignment) {
      medium += profile_norm(id) == 3;
      high += profile_norm(id) == 9;
    }
    if (medium != 6 || high != 4) {
      throw std::runtime_error("the MITM join left the shell");
    }
    Six six = direct_six(assignment);
    for (E value : six) {
      if (value.a % 9 || value.b % 9) {
        throw std::runtime_error("the MITM join failed modulo nine");
      }
    }

    PackedAssignment canonical = canonical_assignment(assignment);
    auto [iterator, inserted] = survivor_orbits_.insert(canonical);
    if (!inserted) return;
    (void)iterator;

    int stabilizer = assignment_stabilizer(canonical);
    std::uint64_t orbit_size = 24 / stabilizer;
    ++counters_.assignment_orbits;
    counters_.raw_mod9_survivors += orbit_size;

    Target canonical_target = assignment_aggregate(canonical);
    int canonical_target_index = exact_target_index(canonical_target);
    if (canonical_target_index < 0) {
      throw std::runtime_error(
          "the exact symmetry moved a target outside the catalog");
    }
    // Target labels vary around an orbit when a channel is conjugated.
    // Count them explicitly, rather than attributing the whole orbit to
    // the canonical representative's label.
    for (int rotation = 0; rotation < 6; ++rotation) {
      int offset = 2 * rotation;
      for (int star_a = 0; star_a < 2; ++star_a) {
        for (int star_b = 0; star_b < 2; ++star_b) {
          PackedAssignment image{};
          for (int channel = 0; channel < 2; ++channel) {
            bool star = channel == 0 ? star_a : star_b;
            int shift = (offset + (star ? 6 : 0)) % 12;
            for (int index = 0; index < 12; ++index) {
              int id =
                  canonical[12 * channel + (index + shift) % 12];
              image[12 * channel + index] =
                  static_cast<std::uint8_t>(
                      star ? conjugate_profile_id(id) : id);
            }
          }
          // The set removes repeats caused by a stabilizer.
          orbit_images_.insert(image);
        }
      }
    }
    if (orbit_images_.size() != orbit_size) {
      throw std::runtime_error("exact orbit-image census changed");
    }
    for (const PackedAssignment &image : orbit_images_) {
      int index = exact_target_index(assignment_aggregate(image));
      if (index < 0) {
        throw std::runtime_error("an orbit image lost its exact target");
      }
      ++counters_.raw_target_survivors[index];
    }
    orbit_images_.clear();

    auto physical = detached_physical(canonical);
    if (physical[0] != E{}) {
      throw std::runtime_error("detached replay has nonzero origin");
    }
    int bad_classes = 0;
    for (int part = 0; part < CLASS_COUNT; ++part) {
      E representative = physical[classes[part][0]];
      for (int value : classes[part]) {
        if (physical[value] != representative) {
          throw std::runtime_error(
              "detached replay lost H-invariance");
        }
      }
      E expected =
          part < 6 ? representative
                   : conjugate(physical[classes[part - 6][0]]);
      if (representative != expected) {
        throw std::runtime_error(
            "detached replay lost reversal conjugation");
      }
      if (representative.a % 9 || representative.b % 9) {
        throw std::runtime_error(
            "detached replay lost the modulo-nine join");
      }
      bad_classes += representative != E{};
    }
    counters_.raw_bad_class_histogram[bad_classes] += orbit_size;
    if (bad_classes == 0) {
      counters_.exact_profiles += orbit_size;
    }
  }

  RawSkeleton raw_;
  H4Counters &counters_;
  std::set<PackedAssignment> &survivor_orbits_;
  PackedAssignment baseline_{};
  Six baseline_six_{};
  Sig baseline_signature_{};
  Target baseline_aggregate_{};
  std::array<std::vector<SlotOption>, POSITION_COUNT> options_;
  std::array<std::vector<LocalLift>, 6> local_tables_;
  std::uint16_t local_b_signature_ = 0;
  std::array<int, 3> left_quartets_{};
  std::array<int, 3> right_quartets_{};
  std::set<PackedAssignment> orbit_images_;
};

}  // namespace

int main() {
  initialize_classes();
  initialize_signature_arithmetic();
  audit_alphabet();
  initialize_variable_tables();
  audit_medium_coordinates();

  Result skeleton_census =
      SkeletonEnumerator(make_local_skeletons()).run();
  if (skeleton_census.skeletons != 37680 ||
      skeleton_census.orbit_representatives.size() != 1704) {
    throw std::runtime_error("the signed-skeleton census changed");
  }

  H4Counters counters;
  std::set<PackedAssignment> survivor_orbits;
  for (const RawSkeleton &raw :
       skeleton_census.orbit_representatives) {
    ++counters.skeleton_orbits;
    OrbitProcessor(raw, counters, survivor_orbits).run();
    if (counters.skeleton_orbits % 100 == 0) {
      std::cerr << "skeleton_orbits=" << counters.skeleton_orbits
                << " assignment_orbits=" << counters.assignment_orbits
                << " raw_survivors=" << counters.raw_mod9_survivors
                << "\n";
    }
  }

  constexpr std::array<std::uint64_t, 22> expected_targets = {
      15162, 15162, 13518, 13518, 14970, 14970, 15162, 15162,
      19818, 19818, 14970, 14970, 15147, 15147, 19818, 19818,
      14358, 14358, 14922, 15147, 15147, 14922,
  };
  const std::map<int, std::uint64_t> expected_histogram = {
      {4, 204}, {6, 1860}, {8, 16884}, {10, 96192}, {12, 230844}};
  if (counters.raw_mod9_survivors != 345984 ||
      counters.raw_target_survivors != expected_targets ||
      counters.raw_bad_class_histogram != expected_histogram ||
      counters.exact_profiles != 0) {
    throw std::runtime_error(
        "the independent orbit-weighted shell-four census changed");
  }

  std::cout << "signed_skeletons=37680\n";
  std::cout << "signed_skeleton_orbits=" << counters.skeleton_orbits << "\n";
  std::cout << "half_records_generated="
            << counters.half_records_generated << "\n";
  std::cout << "maximum_right_records="
            << counters.maximum_right_records << "\n";
  std::cout << "maximum_right_keys="
            << counters.maximum_right_keys << "\n";
  std::cout << "join_hits_with_stabilizer_duplicates="
            << counters.join_hits_with_stabilizer_duplicates << "\n";
  std::cout << "mod9_assignment_orbits="
            << counters.assignment_orbits << "\n";
  std::cout << "raw_mod9_survivors="
            << counters.raw_mod9_survivors << "\n";
  for (int index = 0; index < 22; ++index) {
    std::cout << "target[" << index << "]="
              << counters.raw_target_survivors[index] << "\n";
  }
  for (const auto &[bad, count] : counters.raw_bad_class_histogram) {
    std::cout << "bad_classes[" << bad << "]=" << count << "\n";
  }
  std::cout << "exact_profiles=" << counters.exact_profiles << "\n";
  std::cout << "PASS: signed-skeleton MITM and detached 37-lag replay\n";
}
