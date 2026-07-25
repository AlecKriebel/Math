// Connected end-to-end oracle for one real dense-shell production prefix.
//
// This audit deliberately includes the production classifier and the
// support-factorized 729-character kernel in one translation unit.  It
// uses the genuine h0-p01-p13 support, a genuine canonical signed skeleton,
// and a genuine exact aggregate target.  The complete affine cube is
// enumerated independently to check every one of the 729 Gauss sums and to
// recover a profile witness for detached all-37-lag replay.

#define main dense_classifier_reference_main
#include "../dense_shell_classifier_pilot/dense_shell_classifier_pilot.cpp"
#undef main

#define main dense_character_benchmark_reference_main
#include "../scratch_dense_shell_benchmark/benchmark_dense_shell_characters.cpp"
#undef main

#include <chrono>
#include <sstream>

namespace {

using AuditClock = std::chrono::steady_clock;
using AuditQ = std::array<std::uint8_t, QUARTETS>;

double audit_seconds(AuditClock::time_point start) {
  return std::chrono::duration<double>(AuditClock::now() - start).count();
}

int audit_encode(const AuditQ& value) {
  int code = 0;
  int power = 1;
  for (std::uint8_t coordinate : value) {
    code += power * coordinate;
    power *= FIELD;
  }
  return code;
}

std::pair<int, int> audit_decode_medium_id(int id) {
  switch (id) {
    case 7:
      return {1, 0};
    case 6:
      return {1, 1};
    case 1:
      return {1, 2};
    case 2:
      return {-1, 0};
    case 4:
      return {-1, 1};
    case 8:
      return {-1, 2};
    default:
      throw std::runtime_error("audit assignment contains a non-medium ID");
  }
}

Assignment audit_expected_assignment() {
  Assignment result = {
      8, 5, 8, 7, 4, 1, 4, 5, 7, 2, 2, 7,
      5, 5, 4, 6, 8, 4, 5, 5, 1, 8, 2, 2,
  };
  return result;
}

Decoration audit_selected_decoration(
    const std::vector<Local>& local) {
  std::array<Local, PAIRS> selected = {
      local.at(1),
      local.at(13),
      local.at(6),
      local.at(20),
      local.at(0),
      local.at(24),
  };
  return {selected_to_skeleton(selected), -1};
}

AmbientVector audit_x_from_assignment(
    const Decoration& decor, const Assignment& assignment) {
  AmbientVector result{};
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int skeleton_sign = decor.skeleton[channel][class_index];
    if (!skeleton_sign) {
      if (assignment[slot] != ZERO_ID) {
        throw std::runtime_error("expected assignment changed support");
      }
      continue;
    }
    const auto [decoded_sign, phase] =
        audit_decode_medium_id(assignment[slot]);
    if (decoded_sign != skeleton_sign) {
      throw std::runtime_error("expected assignment changed skeleton sign");
    }
    const int sigma =
        actual_factor(channel, class_index) * skeleton_sign;
    result[slot] =
        static_cast<std::uint8_t>(mod3(-sigma * phase));
  }
  return result;
}

Assignment audit_assignment_from_x(
    const Decoration& decor, const AmbientVector& x) {
  std::array<std::uint8_t, SLOTS> phases{};
  for (int slot = 0; slot < SLOTS; ++slot) {
    const auto [channel, class_index] = decode_slot(slot);
    const int skeleton_sign = decor.skeleton[channel][class_index];
    if (!skeleton_sign) {
      if (x[slot]) {
        throw std::runtime_error("affine point left the selected support");
      }
      continue;
    }
    const int sigma =
        actual_factor(channel, class_index) * skeleton_sign;
    phases[slot] =
        static_cast<std::uint8_t>(mod3(-sigma * x[slot]));
  }
  return assignment_ids(decor, phases, 0);
}

AuditQ audit_q_from_assignment(
    const Geometry& geometry, const Assignment& assignment,
    std::array<E, PAIRS>* exact_output = nullptr) {
  const Values values = values_from_assignment(assignment);
  const std::array<E, PAIRS> exact =
      exact_correlations(geometry, values);
  const Signature signature = reduced_signature(exact);
  AuditQ result{};
  for (int lag = 0; lag < PAIRS; ++lag) {
    if (signature[2 * lag] % 3 ||
        signature[2 * lag + 1] % 3 ||
        primitive_flag(signature, lag) != 0) {
      throw std::runtime_error("affine cube left the primitive-flag rows");
    }
    result[lag] =
        static_cast<std::uint8_t>(signature[2 * lag] / 3);
  }
  if (exact_output != nullptr) *exact_output = exact;
  return result;
}

AuditQ audit_q_from_x(
    const Geometry& geometry, const Decoration& decor,
    const AmbientVector& x, Assignment* assignment_output = nullptr,
    std::array<E, PAIRS>* exact_output = nullptr) {
  const Assignment assignment = audit_assignment_from_x(decor, x);
  if (assignment_output != nullptr) *assignment_output = assignment;
  return audit_q_from_assignment(geometry, assignment, exact_output);
}

AuditQ audit_quadratic_prediction(
    const SupportFixture& support, const Batch& batch,
    const std::array<std::uint8_t, MAX_DIM>& coordinates) {
  AuditQ result{};
  for (int lag = 0; lag < QUARTETS; ++lag) {
    int homogeneous = 0;
    for (int left = 0; left < support.cell.d; ++left) {
      for (int right = 0; right < support.cell.d; ++right) {
        homogeneous +=
            coordinates[left] *
            support.restricted[lag][left][right] *
            coordinates[right];
      }
    }
    int value = batch.offset[lag] + 2 * homogeneous;
    for (int index = 0; index < support.cell.d; ++index) {
      value += batch.linear[lag][index] * coordinates[index];
    }
    result[lag] = static_cast<std::uint8_t>(mod3(value));
  }
  return result;
}

Eisenstein audit_direct_character(
    const std::array<std::uint64_t, CHARACTERS>& histogram,
    const Coefficients& coefficients) {
  Eisenstein result{};
  for (int output_code = 0; output_code < CHARACTERS; ++output_code) {
    int work = output_code;
    int phase = 0;
    for (int lag = 0; lag < QUARTETS; ++lag) {
      phase += coefficients[lag] * (work % FIELD);
      work /= FIELD;
    }
    const Eisenstein term =
        e_rotate({static_cast<std::int64_t>(histogram[output_code]), 0},
                 phase);
    result.a += term.a;
    result.b += term.b;
  }
  return result;
}

bool audit_equal(Eisenstein left, Eisenstein right) {
  return left.a == right.a && left.b == right.b;
}

std::uint64_t audit_prefix_skeletons(
    const std::vector<Local>& local,
    std::uint64_t* canonical,
    std::uint64_t* weighted) {
  std::array<Local, PAIRS> selected{};
  selected[0] = local.at(1);
  selected[1] = local.at(13);
  std::uint64_t raw = 0;
  *canonical = 0;
  *weighted = 0;
  const auto recurse = [&](auto&& self, int pair, int used) -> void {
    if (pair == PAIRS) {
      if (used != 18) return;
      ++raw;
      const Decoration decor = {
          selected_to_skeleton(selected), -1};
      const OrbitInfo orbit = decoration_orbit_info(decor);
      if (orbit.canonical) {
        ++*canonical;
        *weighted += orbit.orbit_size;
      }
      return;
    }
    const int remaining = PAIRS - pair - 1;
    for (const Local& state : local) {
      const int next = used + medium_count(state);
      if (next > 18 || next + 4 * remaining < 18) continue;
      selected[pair] = state;
      self(self, pair + 1, next);
    }
  };
  recurse(recurse, 2, medium_count(selected[0]));
  return raw;
}

}  // namespace

int main() {
  try {
    const auto total_start = AuditClock::now();
    initialize_geometry();
    const Geometry geometry = build_geometry();
    const std::vector<Local> local = local_states();
    if (local.size() != 27) {
      throw std::runtime_error("legal local alphabet changed");
    }

    const auto skeleton_start = AuditClock::now();
    std::uint64_t canonical_skeletons = 0;
    std::uint64_t weighted_skeletons = 0;
    const std::uint64_t raw_skeletons = audit_prefix_skeletons(
        local, &canonical_skeletons, &weighted_skeletons);
    const double skeleton_seconds = audit_seconds(skeleton_start);
    if (raw_skeletons != 1296 || canonical_skeletons != 42 ||
        weighted_skeletons != 600) {
      throw std::runtime_error("representative prefix census changed");
    }

    const Decoration decor = audit_selected_decoration(local);
    const OrbitInfo decoration_orbit = decoration_orbit_info(decor);
    if (!decoration_orbit.canonical) {
      throw std::runtime_error("selected decoration is not canonical");
    }
    const Assignment expected = audit_expected_assignment();
    const Values expected_values = values_from_assignment(expected);
    constexpr int selected_target = 2;
    if (exact_target_index(aggregate(expected_values)) != selected_target) {
      throw std::runtime_error("selected witness target changed");
    }
    std::array<E, PAIRS> expected_exact{};
    const AuditQ expected_q =
        audit_q_from_assignment(geometry, expected, &expected_exact);
    if (audit_encode(expected_q) != 0 ||
        !post_mod9_lambda_zero(expected_exact) ||
        assignment_digest(
            expected, expected_exact, selected_target) !=
            0xc8ac157d026d3025ULL) {
      throw std::runtime_error("selected modulo-nine witness changed");
    }
    detached_replay(
        geometry, expected_values, expected_exact,
        TARGETS[selected_target]);

    std::uint32_t mask = 0;
    for (int slot = 0; slot < SLOTS; ++slot) {
      const auto [channel, class_index] = decode_slot(slot);
      if (decor.skeleton[channel][class_index]) mask |= 1u << slot;
    }
    const Cell cell = support_cell(mask, 18);
    if (cell != Cell{5, 12, 12, 0}) {
      throw std::runtime_error("selected support cell changed");
    }
    const SupportFixture support =
        make_support_fixture(18, cell, mask);
    const AmbientVector x0 = audit_x_from_assignment(decor, expected);

    // Fit the genuine modulo-nine map on this actual affine target fiber.
    // The earlier throughput benchmark factors a different, later polar
    // family.  We retain its exact Gauss-sum implementation but replace the
    // synthetic/theoretical matrices with the polynomial recovered from
    // exact classifier correlations.
    SupportFixture actual_support = support;
    Batch batch;
    const AuditQ constant = audit_q_from_x(geometry, decor, x0);
    std::array<AuditQ, MAX_DIM> basis_values{};
    for (int basis = 0; basis < actual_support.cell.d; ++basis) {
      AmbientVector point = x0;
      AmbientVector twice = x0;
      for (int ambient = 0; ambient < AMBIENT; ++ambient) {
        point[ambient] = static_cast<std::uint8_t>(mod3(
            point[ambient] +
            actual_support.kernel[basis][ambient]));
        twice[ambient] = static_cast<std::uint8_t>(mod3(
            twice[ambient] +
            2 * actual_support.kernel[basis][ambient]));
      }
      basis_values[basis] = audit_q_from_x(geometry, decor, point);
      const AuditQ twice_value = audit_q_from_x(geometry, decor, twice);
      for (int lag = 0; lag < QUARTETS; ++lag) {
        const int actual_diagonal = mod3(
            basis_values[basis][lag] + twice_value[lag] +
            constant[lag]);
        actual_support.restricted[lag][basis][basis] =
            static_cast<std::uint8_t>(actual_diagonal);
        batch.linear[lag][basis] = static_cast<std::uint8_t>(mod3(
            basis_values[basis][lag] - constant[lag] -
            2 * actual_diagonal));
      }
    }
    for (int left = 0; left < actual_support.cell.d; ++left) {
      for (int right = left + 1; right < actual_support.cell.d;
           ++right) {
        AmbientVector point = x0;
        for (int ambient = 0; ambient < AMBIENT; ++ambient) {
          point[ambient] = static_cast<std::uint8_t>(mod3(
              point[ambient] +
              actual_support.kernel[left][ambient] +
              actual_support.kernel[right][ambient]));
        }
        const AuditQ pair_value = audit_q_from_x(geometry, decor, point);
        for (int lag = 0; lag < QUARTETS; ++lag) {
          const int actual_off_diagonal = mod3(
              pair_value[lag] - basis_values[left][lag] -
              basis_values[right][lag] + constant[lag]);
          actual_support.restricted[lag][left][right] =
              static_cast<std::uint8_t>(actual_off_diagonal);
          actual_support.restricted[lag][right][left] =
              static_cast<std::uint8_t>(actual_off_diagonal);
        }
      }
    }
    for (int lag = 0; lag < QUARTETS; ++lag) {
      batch.offset[lag] = constant[lag];
    }

    std::uint64_t benchmark_polar_differences = 0;
    for (int lag = 0; lag < QUARTETS; ++lag) {
      for (int left = 0; left < actual_support.cell.d; ++left) {
        for (int right = 0; right < actual_support.cell.d; ++right) {
          benchmark_polar_differences +=
              actual_support.restricted[lag][left][right] !=
              support.restricted[lag][left][right];
        }
      }
    }

    const auto factor_start = AuditClock::now();
    const auto factors = factor_support(actual_support);
    const double factor_seconds = audit_seconds(factor_start);

    const auto enumerate_start = AuditClock::now();
    std::array<std::uint64_t, CHARACTERS> histogram{};
    std::uint64_t exact_target_points = 0;
    std::uint64_t exact_target_mod9_points = 0;
    std::uint64_t exact_target_post_mod9_points = 0;
    Assignment recovered{};
    std::array<E, PAIRS> recovered_exact{};
    bool recovered_present = false;
    const std::uint64_t affine_points = static_cast<std::uint64_t>(
        power3(actual_support.cell.d));
    for (std::uint64_t code = 0; code < affine_points; ++code) {
      std::uint64_t work = code;
      AmbientVector point = x0;
      std::array<std::uint8_t, MAX_DIM> coordinates{};
      for (int basis = 0; basis < actual_support.cell.d; ++basis) {
        const int trit = static_cast<int>(work % FIELD);
        work /= FIELD;
        coordinates[basis] = static_cast<std::uint8_t>(trit);
        for (int ambient = 0; ambient < AMBIENT; ++ambient) {
          point[ambient] = static_cast<std::uint8_t>(mod3(
              point[ambient] +
              trit * actual_support.kernel[basis][ambient]));
        }
      }
      Assignment assignment{};
      std::array<E, PAIRS> exact{};
      const AuditQ value = audit_q_from_x(
          geometry, decor, point, &assignment, &exact);
      const AuditQ predicted = audit_quadratic_prediction(
          actual_support, batch, coordinates);
      if (value != predicted) {
        throw std::runtime_error(
            "actual modulo-nine polynomial is not quadratic");
      }
      ++histogram[audit_encode(value)];
      const Values values = values_from_assignment(assignment);
      const Aggregate value_aggregate = aggregate(values);
      if (lambda3_residue(
              {value_aggregate[0], value_aggregate[1]}) !=
              lambda3_residue(
                  {TARGETS[selected_target][0],
                   TARGETS[selected_target][1]}) ||
          lambda3_residue(
              {value_aggregate[2], value_aggregate[3]}) !=
              lambda3_residue(
                  {TARGETS[selected_target][2],
                   TARGETS[selected_target][3]})) {
        throw std::runtime_error("affine cube left the target residue");
      }
      if (exact_target_index(value_aggregate) == selected_target) {
        ++exact_target_points;
        if (audit_encode(value) == 0) {
          ++exact_target_mod9_points;
          if (post_mod9_lambda_zero(exact)) {
            ++exact_target_post_mod9_points;
            if (!recovered_present) {
              recovered = assignment;
              recovered_exact = exact;
              recovered_present = true;
            }
          }
        }
      }
    }
    const double enumerate_seconds = audit_seconds(enumerate_start);
    if (std::accumulate(histogram.begin(), histogram.end(), 0ULL) !=
        affine_points) {
      throw std::runtime_error("affine histogram lost points");
    }
    if (!recovered_present) {
      throw std::runtime_error("positive exact-target fiber lost witness");
    }

    const auto character_start = AuditClock::now();
    std::array<Eisenstein, CHARACTERS> character_sums{};
    for (int code = 0; code < CHARACTERS; ++code) {
      character_sums[code] =
          evaluate_character(
              factors[code], batch, character_trits[code]);
    }
    const double character_seconds = audit_seconds(character_start);

    const auto histogram_check_start = AuditClock::now();
    for (int code = 0; code < CHARACTERS; ++code) {
      const Eisenstein direct =
          audit_direct_character(histogram, character_trits[code]);
      if (!audit_equal(character_sums[code], direct)) {
        throw std::runtime_error(
            "factorized character sum disagrees with exact histogram");
      }
    }
    const double histogram_check_seconds =
        audit_seconds(histogram_check_start);

    const auto inversion_start = AuditClock::now();
    for (int output_code = 0; output_code < CHARACTERS; ++output_code) {
      int work = output_code;
      AuditQ output{};
      for (int lag = 0; lag < QUARTETS; ++lag) {
        output[lag] = static_cast<std::uint8_t>(work % FIELD);
        work /= FIELD;
      }
      Eisenstein total{};
      for (int code = 0; code < CHARACTERS; ++code) {
        int phase = 0;
        for (int lag = 0; lag < QUARTETS; ++lag) {
          phase -= character_trits[code][lag] * output[lag];
        }
        const Eisenstein term =
            e_rotate(character_sums[code], phase);
        total.a += term.a;
        total.b += term.b;
      }
      if (total.b != 0 || total.a % CHARACTERS != 0 ||
          static_cast<std::uint64_t>(total.a / CHARACTERS) !=
              histogram[output_code]) {
        throw std::runtime_error("729-character inversion changed a fiber");
      }
    }
    const double inversion_seconds = audit_seconds(inversion_start);

    constexpr int benchmark_rounds = 16384;
    std::uint64_t benchmark_checksum = 0x243f6a8885a308d3ULL;
    const auto benchmark_start = AuditClock::now();
    for (int round = 0; round < benchmark_rounds; ++round) {
      for (int code = 0; code < CHARACTERS; ++code) {
        const Eisenstein value = evaluate_character(
            factors[code], batch, character_trits[code]);
        benchmark_checksum = checksum_mix(
            benchmark_checksum, value,
            static_cast<std::uint64_t>(round) * CHARACTERS + code);
      }
    }
    const double benchmark_seconds = audit_seconds(benchmark_start);
    const std::uint64_t benchmark_evaluations =
        static_cast<std::uint64_t>(benchmark_rounds) * CHARACTERS;

    const Values recovered_values = values_from_assignment(recovered);
    if (!post_mod9_lambda_zero(recovered_exact)) {
      throw std::runtime_error("recovered witness lost the post-mod9 gate");
    }
    detached_replay(
        geometry, recovered_values, recovered_exact,
        TARGETS[selected_target]);
    const AssignmentOrbitInfo recovered_orbit =
        assignment_orbit_info(recovered);
    const Values canonical_values =
        values_from_assignment(recovered_orbit.canonical);
    const std::array<E, PAIRS> canonical_exact =
        exact_correlations(geometry, canonical_values);
    const int canonical_target =
        exact_target_index(aggregate(canonical_values));
    if (canonical_target < 0) {
      throw std::runtime_error("canonical witness lost its target");
    }
    detached_replay(
        geometry, canonical_values, canonical_exact,
        TARGETS[canonical_target]);

    std::cout << "schema=dense-shell-e2e-audit-v1\n";
    std::cout << "status=PASS\n";
    std::cout << "shell=h0\n";
    std::cout << "prefix_first=1\n";
    std::cout << "prefix_second=13\n";
    std::cout << "legal_local_states=" << local.size() << "\n";
    std::cout << "raw_skeletons=" << raw_skeletons << "\n";
    std::cout << "canonical_decorations="
              << canonical_skeletons << "\n";
    std::cout << "weighted_canonical_decorations="
              << weighted_skeletons << "\n";
    std::cout << "selected_decoration_orbit="
              << decoration_orbit.orbit_size << "\n";
    std::cout << "support_mask=" << mask << "\n";
    std::cout << "support_cell=5,12,12,0\n";
    std::cout << "lower_affine_dimension=" << support.cell.d << "\n";
    std::cout << "lower_affine_points=" << affine_points << "\n";
    std::cout << "actual_mod9_zero_fiber=" << histogram[0] << "\n";
    std::cout << "benchmark_polar_differences="
              << benchmark_polar_differences << "\n";
    std::cout << "exact_target_points=" << exact_target_points << "\n";
    std::cout << "exact_target_mod9_points="
              << exact_target_mod9_points << "\n";
    std::cout << "exact_target_post_mod9_points="
              << exact_target_post_mod9_points << "\n";
    std::cout << "character_evaluations=" << CHARACTERS << "\n";
    std::cout << "character_inversion_fibers=" << CHARACTERS << "\n";
    std::cout << "actual_family_benchmark_evaluations="
              << benchmark_evaluations << "\n";
    std::cout << "actual_family_benchmark_checksum=0x" << std::hex
              << benchmark_checksum << std::dec << "\n";
    std::cout << "recovered_target=" << selected_target << "\n";
    std::cout << "recovered_digest=0x" << std::hex
              << assignment_digest(
                     recovered, recovered_exact, selected_target)
              << std::dec << "\n";
    std::cout << "recovered_assignment_orbit="
              << recovered_orbit.orbit_size << "\n";
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "skeleton_seconds=" << skeleton_seconds << "\n";
    std::cout << "factor_seconds=" << factor_seconds << "\n";
    std::cout << "affine_exact_enumeration_seconds="
              << enumerate_seconds << "\n";
    std::cout << "character_seconds=" << character_seconds << "\n";
    std::cout << "histogram_character_check_seconds="
              << histogram_check_seconds << "\n";
    std::cout << "character_inversion_seconds="
              << inversion_seconds << "\n";
    std::cout << "actual_family_benchmark_seconds="
              << benchmark_seconds << "\n";
    std::cout << "actual_family_characters_per_second="
              << static_cast<double>(benchmark_evaluations) /
                     benchmark_seconds
              << "\n";
    std::cout << "wall_seconds=" << audit_seconds(total_start) << "\n";
    std::cout
        << "PASS: legal skeletons, symmetry, actual 729-character count, "
           "witness recovery, and detached exact replay\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << "\n";
    return 1;
  }
}
