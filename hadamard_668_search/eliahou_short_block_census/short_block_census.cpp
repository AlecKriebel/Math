// Parameterized production kernel for canonical short-block cases 21..29.
//
// The proven packed arithmetic, binary model reader, SHA-256, and exact
// physical replay are compiled from the already audited case-26 sources.
// This translation unit replaces only the quotient join driver so that the
// free reflection gauge is chosen dynamically: first an odd noncentral L
// pair, and (only when none exists) an odd noncentral S pair.

#define main h668_disabled_case26_main
#include "../eliahou_global_quotient_plan/global_quotient_census.cpp"
#undef main

namespace {

std::uint64_t dynamic_census_one(
    Kernel& kernel,
    const std::array<std::uint8_t, PAIRS>& parity,
    std::vector<SurvivorState>* survivor_states,
    int fixed_zero_pair) {
  Sig reduced_constant = kernel.constant;
  for (int i = 0; i < PAIRS; ++i) {
    if (!parity[i]) continue;
    reduced_constant =
        Kernel::add3(reduced_constant, kernel.base_linear[i]);
    for (int j = 0; j < i; ++j) {
      if (parity[j]) {
        reduced_constant = Kernel::add3(
            reduced_constant, kernel.base_quadratic[i][j]);
      }
    }
  }

  std::array<Sig, PAIRS> reduced_linear{};
  for (int i = 0; i < PAIRS; ++i) {
    reduced_linear[i] = kernel.direct_linear[parity[i]][i];
    for (int k = 0; k < PAIRS; ++k) {
      if (k != i && parity[k]) {
        reduced_linear[i] = Kernel::add3(
            reduced_linear[i],
            kernel.base_interaction[parity[i]][i][k]);
      }
    }
  }

  std::array<std::vector<int>, 4> components;
  int odd_pairs = 0;
  for (int pair = 0; pair < PAIRS; ++pair) {
    odd_pairs += parity[pair];
    if (pair == static_cast<int>(kernel.model.central)) continue;
    if (kernel.model.pair_blocks[pair] > 1) {
      throw std::runtime_error("noncentral pair has invalid block");
    }
    const int component =
        2 * kernel.model.pair_blocks[pair] +
        (parity[pair] ^ kernel.model.pair_phases[pair]);
    components[component].push_back(pair);
  }
  if ((odd_pairs & 1) == 0) {
    throw std::runtime_error("quotient point has even parity");
  }
  if (
      fixed_zero_pair < 0 || fixed_zero_pair >= PAIRS ||
      fixed_zero_pair == static_cast<int>(kernel.model.central) ||
      kernel.model.pair_blocks[fixed_zero_pair] > 1 ||
      parity[fixed_zero_pair] != 1) {
    throw std::runtime_error(
        "dynamic reflection gauge is not an odd noncentral pair");
  }
  const int gauge_block = kernel.model.pair_blocks[fixed_zero_pair];
  const int gauge_component =
      2 * gauge_block +
      (parity[fixed_zero_pair] ^
       kernel.model.pair_phases[fixed_zero_pair]);
  auto place = std::find(
      components[gauge_component].begin(),
      components[gauge_component].end(),
      fixed_zero_pair);
  if (place == components[gauge_component].end()) {
    throw std::runtime_error(
        "dynamic reflection gauge was absent from its component");
  }
  components[gauge_component].erase(place);

  const int full_even_total = (39 - odd_pairs) / 2;
  const int right_pair_count =
      static_cast<int>(components[2].size() + components[3].size());
  const std::size_t expected_right_entries =
      std::size_t{1} << right_pair_count;
  std::uint64_t survivors = 0;

  for (int central_value = 0; central_value < 2; ++central_value) {
    auto effective_linear = reduced_linear;
    if (central_value) {
      for (int pair = 0; pair < PAIRS; ++pair) {
        if (pair == static_cast<int>(kernel.model.central)) continue;
        effective_linear[pair] = Kernel::add3(
            effective_linear[pair],
            kernel.pair_quadratic
                [parity[pair]][parity[kernel.model.central]]
                [pair][kernel.model.central]);
      }
    }
    Sig target = reduced_constant;
    if (central_value) {
      target = Kernel::add3(
          target, reduced_linear[kernel.model.central]);
    }
    target = Kernel::negate3(target);
    const int remaining_full =
        full_even_total -
        (parity[kernel.model.central] == 0 ? central_value : 0);
    if (remaining_full < 0) continue;

    const auto left_zero = kernel.component_table(
        components[0], parity, effective_linear);
    const auto left_one = kernel.component_table(
        components[1], parity, effective_linear);
    const auto right_zero = kernel.component_table(
        components[2], parity, effective_linear);
    const auto right_one = kernel.component_table(
        components[3], parity, effective_linear);

    ++kernel.generation;
    std::size_t entry = 0;
    for (std::size_t zero_state = 0;
         zero_state < right_zero.signatures.size(); ++zero_state) {
      for (std::size_t one_state = 0;
           one_state < right_one.signatures.size(); ++one_state) {
        const int weight =
            right_zero.weights[zero_state] +
            right_one.weights[one_state];
        const Sig signature = Kernel::add3(
            right_zero.signatures[zero_state],
            right_one.signatures[one_state]);
        const std::uint64_t key =
            signature | (std::uint64_t(weight) << 40);
        const std::uint32_t bucket =
            Kernel::hash_key(key) & ((1U << 20) - 1);
        if (kernel.stamps[bucket] != kernel.generation) {
          kernel.stamps[bucket] = kernel.generation;
          kernel.heads[bucket] = -1;
        }
        if (entry >= kernel.entry_keys.size()) {
          throw std::runtime_error(
              "dynamic right table exceeded its fixed capacity");
        }
        kernel.entry_keys[entry] = key;
        kernel.next[entry] = kernel.heads[bucket];
        kernel.entry_states[entry] = static_cast<std::uint32_t>(
            zero_state |
            (one_state << components[2].size()));
        kernel.heads[bucket] = static_cast<std::int32_t>(entry);
        ++entry;
      }
    }
    if (entry != expected_right_entries) {
      throw std::runtime_error(
          "dynamic right table lost its exact cardinality");
    }

    for (std::size_t zero_state = 0;
         zero_state < left_zero.signatures.size(); ++zero_state) {
      for (std::size_t one_state = 0;
           one_state < left_one.signatures.size(); ++one_state) {
        const int left_weight =
            left_zero.weights[zero_state] +
            left_one.weights[one_state];
        const int needed_weight = remaining_full - left_weight;
        if (needed_weight < 0 || needed_weight > right_pair_count) {
          continue;
        }
        const Sig left_signature = Kernel::add3(
            left_zero.signatures[zero_state],
            left_one.signatures[one_state]);
        const Sig needed_signature = Kernel::add3(
            target, Kernel::negate3(left_signature));
        const std::uint64_t key =
            needed_signature |
            (std::uint64_t(needed_weight) << 40);
        const std::uint32_t bucket =
            Kernel::hash_key(key) & ((1U << 20) - 1);
        if (kernel.stamps[bucket] != kernel.generation) continue;
        for (std::int32_t candidate = kernel.heads[bucket];
             candidate >= 0;
             candidate = kernel.next[candidate]) {
          if (kernel.entry_keys[candidate] != key) continue;
          ++survivors;
          if (survivor_states == nullptr) continue;
          std::uint64_t pair_state =
              std::uint64_t(central_value) << kernel.model.central;
          const auto place_component =
              [&](int component_index, std::uint64_t state) {
                const auto& variables = components[component_index];
                for (std::size_t local_index = 0;
                     local_index < variables.size(); ++local_index) {
                  if ((state >> local_index) & 1ULL) {
                    pair_state |=
                        1ULL << variables[local_index];
                  }
                }
              };
          place_component(0, zero_state);
          place_component(1, one_state);
          const std::uint32_t encoded =
              kernel.entry_states[candidate];
          const std::size_t right_zero_size = components[2].size();
          const std::uint64_t right_zero_mask =
              (1ULL << right_zero_size) - 1;
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
  return survivors;
}

std::uint64_t rows_for_gauge_block(int block) {
  if (block == 0) {
    return 2 * ((1ULL << 19) + (1ULL << 18));
  }
  if (block == 1) {
    return 2 * ((1ULL << 20) + (1ULL << 17));
  }
  throw std::runtime_error("invalid dynamic gauge block");
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 16) {
      std::cerr
          << "usage: " << argv[0]
          << " MODEL --case N --q-index Q --start I --states N"
             " --source-sha HEX --model-sha HEX"
             " --mode gauged|ungauged\n";
      return 2;
    }
    const std::string model_path = argv[1];
    int case_number = -1;
    int q_index = -1;
    std::uint32_t start = 0;
    std::uint32_t states = 0;
    std::string source_sha;
    std::string model_sha;
    std::string mode;
    for (int argument = 2; argument < argc; argument += 2) {
      const std::string option = argv[argument];
      if (option == "--case") {
        case_number = std::stoi(argv[argument + 1]);
      } else if (option == "--q-index") {
        q_index = std::stoi(argv[argument + 1]);
      } else if (option == "--start") {
        start = static_cast<std::uint32_t>(
            std::stoul(argv[argument + 1]));
      } else if (option == "--states") {
        states = static_cast<std::uint32_t>(
            std::stoul(argv[argument + 1]));
      } else if (option == "--source-sha") {
        source_sha = argv[argument + 1];
      } else if (option == "--model-sha") {
        model_sha = argv[argument + 1];
      } else if (option == "--mode") {
        mode = argv[argument + 1];
      } else {
        throw std::runtime_error("invalid command-line option");
      }
    }
    if (
        case_number < 21 || case_number > 29 ||
        q_index != 2 * (case_number - 20)) {
      throw std::runtime_error("case and short-block index disagree");
    }
    if (
        states == 0 || start >= (1U << QUOTIENT_DIMENSION) ||
        states > (1U << QUOTIENT_DIMENSION) - start) {
      throw std::runtime_error("requested quotient range is invalid");
    }
    if (!valid_hash(source_sha) || !valid_hash(model_sha)) {
      throw std::runtime_error("source/model hash is malformed");
    }
    if (mode != "gauged" && mode != "ungauged") {
      throw std::runtime_error("mode must be gauged or ungauged");
    }
    const bool reflection_gauge = mode == "gauged";

    {
      Sha256 self_test;
      const std::string abc = "abc";
      self_test.update(abc.data(), abc.size());
      if (
          self_test.hex_digest() !=
          "ba7816bf8f01cfea414140de5dae2223"
          "b00361a396177a9cb410ff61f20015ad") {
        throw std::runtime_error("SHA-256 self-test failed");
      }
    }

    Model model = read_model(model_path);
    Kernel kernel(model);
    ExactReplay replay(model);
    Sha256 survivor_digest;
    std::uint64_t survivor_count = 0;
    std::uint64_t representative_count = 0;
    std::uint64_t exact_count = 0;
    std::uint64_t join_rows = 0;
    std::uint32_t l_gauge_states = 0;
    std::uint32_t s_gauge_states = 0;
    std::vector<DetailedRecord> exact_records;
    DetailedRecord best;
    bool have_best = false;

    const auto started = std::chrono::steady_clock::now();
    for (std::uint32_t offset = 0; offset < states; ++offset) {
      const std::uint32_t quotient_index = start + offset;
      const auto parity = quotient_point(model, quotient_index);
      int gauge_pair = -1;
      int gauge_block = -1;
      if (reflection_gauge) {
        for (int wanted_block : {0, 1}) {
          for (int pair = 0; pair < PAIRS; ++pair) {
            if (
                pair != static_cast<int>(model.central) &&
                model.pair_blocks[pair] == wanted_block &&
                parity[pair] == 1) {
              gauge_pair = pair;
              gauge_block = wanted_block;
              break;
            }
          }
          if (gauge_pair >= 0) break;
        }
        if (gauge_pair < 0) {
          throw std::runtime_error(
              "quotient has no odd noncentral reflection gauge pair");
        }
        if (gauge_block == 0) {
          ++l_gauge_states;
        } else {
          ++s_gauge_states;
        }
        join_rows += rows_for_gauge_block(gauge_block);
      } else {
        join_rows += 2 * ((1ULL << 20) + (1ULL << 18));
      }

      std::vector<SurvivorState> representatives;
      const std::uint64_t joined =
          reflection_gauge
              ? dynamic_census_one(
                    kernel, parity, &representatives, gauge_pair)
              : kernel.census_one(parity, &representatives);
      if (joined != representatives.size()) {
        throw std::runtime_error(
            "survivor reconstruction changed the join count");
      }
      representative_count += representatives.size();
      std::vector<SurvivorState> survivors;
      if (reflection_gauge) {
        std::uint64_t reflection_mask = 0;
        for (int pair = 0; pair < PAIRS; ++pair) {
          if (
              pair != static_cast<int>(model.central) &&
              parity[pair]) {
            reflection_mask |= 1ULL << pair;
          }
        }
        survivors.reserve(2 * representatives.size());
        for (const SurvivorState& representative : representatives) {
          if ((representative.pair_state >> gauge_pair) & 1ULL) {
            throw std::runtime_error(
                "dynamic-gauge representative violates y_g=0");
          }
          survivors.push_back(representative);
          survivors.push_back(
              SurvivorState{
                  representative.central_value,
                  representative.pair_state ^ reflection_mask});
        }
      } else {
        survivors = std::move(representatives);
      }
      std::sort(survivors.begin(), survivors.end());
      if (
          std::adjacent_find(
              survivors.begin(), survivors.end(),
              [](const SurvivorState& left,
                 const SurvivorState& right) {
                return left.central_value == right.central_value &&
                       left.pair_state == right.pair_state;
              }) != survivors.end()) {
        throw std::runtime_error("the join emitted a duplicate support");
      }
      for (const SurvivorState& survivor : survivors) {
        DetailedRecord record =
            replay.evaluate(quotient_index, parity, survivor);
        digest_record(survivor_digest, record);
        ++survivor_count;
        if (record.nonzero_lags == 0) {
          ++exact_count;
          exact_records.push_back(record);
        }
        if (!have_best || record.score_less(best)) {
          best = record;
          have_best = true;
        }
      }
    }
    const double seconds =
        std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started)
            .count();

    std::cout
        << "{\n"
        << "  \"schema\": "
           "\"h668-eliahou-short-block-range-v1\",\n"
        << "  \"status\": \"complete\",\n"
        << "  \"case\": " << case_number << ",\n"
        << "  \"block\": \"S\",\n"
        << "  \"q_index\": " << q_index << ",\n"
        << "  \"start\": " << start << ",\n"
        << "  \"states\": " << states << ",\n"
        << "  \"stop\": " << (start + states) << ",\n"
        << "  \"central_values_per_state\": 2,\n"
        << "  \"reflection_gauge\": "
        << (reflection_gauge ? "true" : "false") << ",\n"
        << "  \"reflection_gauge_rule\": "
           "\"lowest odd noncentral L pair, else S pair, has y=0\",\n"
        << "  \"L_gauge_states\": " << l_gauge_states << ",\n"
        << "  \"S_fallback_gauge_states\": "
        << s_gauge_states << ",\n"
        << "  \"joined_representatives\": "
        << representative_count << ",\n"
        << "  \"reconstructed_reflection_mates\": "
        << (reflection_gauge ? representative_count : 0) << ",\n"
        << "  \"join_rows\": " << join_rows << ",\n"
        << "  \"joint_mod6_supports\": " << survivor_count << ",\n"
        << "  \"exact_integer_supports\": " << exact_count << ",\n"
        << "  \"integer_polynomial_checks\": "
        << survivor_count << ",\n"
        << "  \"bitpacked_physical_replays\": "
        << survivor_count << ",\n"
        << "  \"survivor_stream_sha256\": \""
        << survivor_digest.hex_digest() << "\",\n"
        << "  \"producer_sources_sha256\": \""
        << source_sha << "\",\n"
        << "  \"model_sha256\": \"" << model_sha << "\",\n"
        << "  \"kernel_seconds\": " << std::setprecision(12)
        << seconds << ",\n"
        << "  \"join_rows_per_second\": "
        << (join_rows / seconds) << ",\n"
        << "  \"best_witness\": "
        << (have_best ? record_json(best) : "null") << ",\n"
        << "  \"exact_candidates\": [";
    for (std::size_t index = 0; index < exact_records.size(); ++index) {
      if (index) std::cout << ",";
      std::cout << record_json(exact_records[index]);
    }
    std::cout << "]\n}\n";
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
  return 0;
}
