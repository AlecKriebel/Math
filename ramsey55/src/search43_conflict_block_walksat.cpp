// Conflict-hypergraph ProbSAT/WalkSAT with multi-edge block perturbations.
//
// Unlike the degree-switch search, this algorithm deliberately crosses degree
// fibers.  It samples one-, two-, and three-edge repairs from violated
// five-sets, paired-conflict blocks, and periodic multi-conflict shakes.
#define main search43_incident_lns_embedded_main
#include "search43_incident_lns.cpp"
#undef main

#include <array>
#include <set>
#include <sstream>

namespace {

struct ConflictOptions {
  std::string seed_graph;
  std::string output = "conflict_block_best.g6";
  std::string json_output;
  uint64_t seed = 20260811;
  long long steps = 15000;
  int restarts = 2;
  int block2_samples = 5;
  int block3_samples = 3;
  int pair_samples = 4;
  int global_samples = 2;
  int noise_per_million = 60000;
  int degree_penalty_weight = 2;
  int breakout_interval = 400;
  int shake_interval = 800;
  int shake_conflicts = 5;
  int restart_shakes = 4;
  int full_audit_interval = 250;
  bool self_check = false;
  int self_check_moves = 150;
};

struct ConflictMove {
  std::vector<int> flips;
  int delta{};
  long long weighted_delta{};
  int degree_penalty_after{};
  long long energy_delta{};
  std::string kind;
};

struct ImprovementTrace {
  int ordinal{};
  int restart{};
  long long step{};
  int objective{};
  int cliques{};
  int independent{};
  int degree_penalty{};
  int edge_hamming{};
  std::string cause;
};

ConflictOptions parse_conflict_options(int argc, char** argv) {
  ConflictOptions options;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto value = [&]() -> std::string {
      if (index + 1 >= argc)
        throw std::runtime_error("missing value for " + option);
      return argv[++index];
    };
    if (option == "--seed-graph")
      options.seed_graph = value();
    else if (option == "--output")
      options.output = value();
    else if (option == "--json-output")
      options.json_output = value();
    else if (option == "--seed")
      options.seed = std::stoull(value());
    else if (option == "--steps")
      options.steps = std::stoll(value());
    else if (option == "--restarts")
      options.restarts = std::stoi(value());
    else if (option == "--block2-samples")
      options.block2_samples = std::stoi(value());
    else if (option == "--block3-samples")
      options.block3_samples = std::stoi(value());
    else if (option == "--pair-samples")
      options.pair_samples = std::stoi(value());
    else if (option == "--global-samples")
      options.global_samples = std::stoi(value());
    else if (option == "--noise-per-million")
      options.noise_per_million = std::stoi(value());
    else if (option == "--degree-penalty-weight")
      options.degree_penalty_weight = std::stoi(value());
    else if (option == "--breakout-interval")
      options.breakout_interval = std::stoi(value());
    else if (option == "--shake-interval")
      options.shake_interval = std::stoi(value());
    else if (option == "--shake-conflicts")
      options.shake_conflicts = std::stoi(value());
    else if (option == "--restart-shakes")
      options.restart_shakes = std::stoi(value());
    else if (option == "--full-audit-interval")
      options.full_audit_interval = std::stoi(value());
    else if (option == "--self-check-moves")
      options.self_check_moves = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.seed_graph.empty())
    throw std::runtime_error("--seed-graph is required");
  if (!options.self_check && options.json_output.empty())
    throw std::runtime_error("--json-output is required for search");
  if (options.steps < 0 || options.restarts < 1 ||
      options.block2_samples < 0 || options.block3_samples < 0 ||
      options.pair_samples < 0 || options.global_samples < 0 ||
      options.noise_per_million < 0 ||
      options.noise_per_million > 1000000 ||
      options.degree_penalty_weight < 0 || options.breakout_interval < 0 ||
      options.shake_interval < 0 || options.shake_conflicts < 1 ||
      options.restart_shakes < 0 || options.full_audit_interval < 1 ||
      options.self_check_moves < 0)
    throw std::runtime_error("invalid conflict-block option");
  return options;
}

int degree_penalty(const SearchState& state) {
  const std::vector<int> degrees = state.sorted_degrees();
  int result = 0;
  for (int degree : degrees) {
    if (degree < 18) {
      const int deficit = 18 - degree;
      result += deficit * deficit;
    }
    if (degree > 24) {
      const int excess = degree - 24;
      result += excess * excess;
    }
  }
  return result;
}

int edge_hamming(const SearchState& state, const GraphSeed& base) {
  int result = 0;
  for (int edge = 0; edge < 903; ++edge)
    result += state.values()[edge] != base.edges[edge];
  return result;
}

std::vector<int> canonical_flips(const std::vector<int>& flips) {
  std::array<uint8_t, 903> parity{};
  for (int edge : flips) {
    if (!(0 <= edge && edge < 903))
      throw std::runtime_error("move contains an invalid edge");
    parity[edge] ^= 1;
  }
  std::vector<int> result;
  for (int edge = 0; edge < 903; ++edge)
    if (parity[edge]) result.push_back(edge);
  return result;
}

void apply_flips(SearchState& state, const std::vector<int>& flips) {
  for (int edge : flips) state.flip(edge);
}

void rollback_flips(SearchState& state, const std::vector<int>& flips) {
  for (auto iterator = flips.rbegin(); iterator != flips.rend(); ++iterator)
    state.flip(*iterator);
}

ConflictMove evaluate_move(SearchState& state, std::vector<int> raw_flips,
                           const std::vector<uint32_t>& weights,
                           int degree_weight, std::string kind) {
  std::vector<int> flips = canonical_flips(raw_flips);
  if (flips.empty())
    throw std::runtime_error("attempted to evaluate an empty block");
  const int penalty_before = degree_penalty(state);
  int delta = 0;
  long long weighted_delta = 0;
  for (int edge : flips) {
    delta += state.flip_delta(edge);
    weighted_delta += state.weighted_flip_delta(edge, weights);
    state.flip(edge);
  }
  const int penalty_after = degree_penalty(state);
  rollback_flips(state, flips);
  const long long energy_delta =
      weighted_delta +
      static_cast<long long>(degree_weight) *
          (penalty_after - penalty_before);
  return {
      std::move(flips),
      delta,
      weighted_delta,
      penalty_after,
      energy_delta,
      std::move(kind),
  };
}

void add_unique(std::vector<ConflictMove>& moves, ConflictMove move) {
  for (const ConflictMove& old : moves)
    if (old.flips == move.flips) return;
  moves.push_back(std::move(move));
}

std::vector<int> sample_distinct(const std::vector<int>& values, int count,
                                 std::mt19937_64& rng) {
  if (count > static_cast<int>(values.size()))
    throw std::runtime_error("block sample is larger than its conflict");
  std::vector<int> result;
  std::set<int> seen;
  while (static_cast<int>(result.size()) < count) {
    const int edge = values[static_cast<size_t>(rng() % values.size())];
    if (seen.insert(edge).second) result.push_back(edge);
  }
  return result;
}

std::vector<int> multi_conflict_block(
    const SearchState& state, const std::vector<uint8_t>& all_edges,
    int conflict_count, std::mt19937_64& rng) {
  if (state.objective() == 0) return {};
  std::vector<int> raw;
  for (int conflict = 0; conflict < conflict_count; ++conflict) {
    const std::vector<int> edges =
        state.free_edges_of_random_bad(all_edges, rng);
    raw.push_back(edges[static_cast<size_t>(rng() % edges.size())]);
    if ((rng() % 4) == 0)
      raw.push_back(edges[static_cast<size_t>(rng() % edges.size())]);
  }
  return canonical_flips(raw);
}

std::vector<ConflictMove> conflict_candidates(
    SearchState& state, const std::vector<uint8_t>& all_edges,
    const std::vector<uint32_t>& weights, const ConflictOptions& options,
    std::mt19937_64& rng) {
  if (state.objective() == 0) return {};
  const std::vector<int> primary =
      state.free_edges_of_random_bad(all_edges, rng);
  std::vector<ConflictMove> moves;
  for (int edge : primary)
    add_unique(moves, evaluate_move(
                          state, {edge}, weights,
                          options.degree_penalty_weight, "conflict_single"));
  for (int sample = 0; sample < options.block2_samples; ++sample)
    add_unique(
        moves,
        evaluate_move(state, sample_distinct(primary, 2, rng), weights,
                      options.degree_penalty_weight, "conflict_block2"));
  for (int sample = 0; sample < options.block3_samples; ++sample)
    add_unique(
        moves,
        evaluate_move(state, sample_distinct(primary, 3, rng), weights,
                      options.degree_penalty_weight, "conflict_block3"));
  for (int sample = 0; sample < options.pair_samples; ++sample) {
    const std::vector<int> secondary =
        state.free_edges_of_random_bad(all_edges, rng);
    std::vector<int> pair{
        primary[static_cast<size_t>(rng() % primary.size())],
        secondary[static_cast<size_t>(rng() % secondary.size())],
    };
    pair = canonical_flips(pair);
    if (!pair.empty())
      add_unique(
          moves,
          evaluate_move(state, pair, weights,
                        options.degree_penalty_weight, "conflict_pair"));
  }
  for (int sample = 0; sample < options.global_samples; ++sample) {
    std::vector<int> global{
        static_cast<int>(rng() % 903),
        static_cast<int>(rng() % 903),
    };
    global = canonical_flips(global);
    if (!global.empty())
      add_unique(
          moves,
          evaluate_move(state, global, weights,
                        options.degree_penalty_weight, "global_block"));
  }
  if (moves.empty())
    throw std::runtime_error("conflict candidate set is empty");
  return moves;
}

size_t probsat_choice(const std::vector<ConflictMove>& moves,
                      const ConflictOptions& options,
                      std::mt19937_64& rng) {
  if (static_cast<int>(rng() % 1000000) < options.noise_per_million)
    return static_cast<size_t>(rng() % moves.size());
  long long minimum = moves.front().energy_delta;
  for (const ConflictMove& move : moves)
    minimum = std::min(minimum, move.energy_delta);
  std::vector<uint64_t> probabilities;
  uint64_t total = 0;
  for (const ConflictMove& move : moves) {
    const uint64_t difference = static_cast<uint64_t>(
        std::min<long long>(1000000, move.energy_delta - minimum));
    const uint64_t denominator =
        1 + difference + difference * difference;
    const uint64_t probability =
        std::max<uint64_t>(1, uint64_t{1000000000} / denominator);
    probabilities.push_back(probability);
    total += probability;
  }
  uint64_t target = rng() % total;
  for (size_t index = 0; index < probabilities.size(); ++index) {
    if (target < probabilities[index]) return index;
    target -= probabilities[index];
  }
  return probabilities.size() - 1;
}

void require_full_objective(const SearchState& state) {
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != cliques + independent)
    throw std::runtime_error(
        "incremental conflict objective disagrees with full recomputation");
}

int run_conflict_self_check(const ConflictOptions& options,
                            const GraphSeed& base) {
  const auto started = Clock::now();
  SearchState state;
  state.set_values(base.edges);
  const std::string base_graph6 = state.graph6();
  std::vector<uint8_t> all_edges(903, 1);
  std::vector<uint32_t> weights(state.subset_count());
  for (size_t subset = 0; subset < weights.size(); ++subset)
    weights[subset] =
        1 + static_cast<uint32_t>(
                (subset * uint64_t{11400714819323198485ull} + options.seed) %
                31);
  std::mt19937_64 rng(options.seed);
  int checked = 0;
  for (int trial = 0; trial < options.self_check_moves; ++trial) {
    std::vector<ConflictMove> moves = conflict_candidates(
        state, all_edges, weights, options, rng);
    const ConflictMove& move =
        moves[static_cast<size_t>(rng() % moves.size())];
    const int before = state.objective();
    const long long weighted_before =
        state.full_weighted_objective(weights);
    const int penalty_before = degree_penalty(state);
    apply_flips(state, move.flips);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + move.delta ||
        state.objective() != cliques + independent ||
        state.full_weighted_objective(weights) !=
            weighted_before + move.weighted_delta ||
        degree_penalty(state) != move.degree_penalty_after ||
        move.energy_delta !=
            move.weighted_delta +
                static_cast<long long>(options.degree_penalty_weight) *
                    (degree_penalty(state) - penalty_before))
      throw std::runtime_error("conflict-block exact delta check failed");
    rollback_flips(state, move.flips);
    if (state.graph6() != base_graph6)
      throw std::runtime_error("conflict-block rollback failed");
    ++checked;
  }
  int shake_checks = 0;
  for (int trial = 0; trial < 50; ++trial) {
    std::vector<int> flips = multi_conflict_block(
        state, all_edges, options.shake_conflicts, rng);
    if (flips.empty()) continue;
    const int before = state.objective();
    ConflictMove move = evaluate_move(
        state, flips, weights, options.degree_penalty_weight, "shake");
    apply_flips(state, move.flips);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + move.delta ||
        state.objective() != cliques + independent)
      throw std::runtime_error("multi-conflict shake delta check failed");
    rollback_flips(state, move.flips);
    if (state.graph6() != base_graph6)
      throw std::runtime_error("multi-conflict shake rollback failed");
    ++shake_checks;
  }
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"self_check\","
            << "\"algorithm\":\"conflict_hypergraph_probsat_blocks_v1\","
            << "\"seed\":" << options.seed << ','
            << "\"move_delta_full_recomputation_checks\":" << checked << ','
            << "\"multi_conflict_shake_checks\":" << shake_checks << ','
            << "\"weighted_delta_checks\":true,"
            << "\"degree_energy_checks\":true,"
            << "\"rollback_checks\":true,"
            << "\"status\":\"PASS\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

int run_conflict_search(const ConflictOptions& options,
                        const GraphSeed& base) {
  const auto started = Clock::now();
  SearchState state;
  state.set_values(base.edges);
  require_full_objective(state);
  const auto [initial_cliques, initial_independent] = state.full_counts();
  const int initial_objective = state.objective();
  const int initial_degree_penalty = degree_penalty(state);
  std::vector<uint8_t> all_edges(903, 1);
  std::mt19937_64 rng(options.seed);

  int global_best = initial_objective;
  int global_penalty = initial_degree_penalty;
  int global_hamming = 0;
  std::vector<uint8_t> global_values = state.values();
  std::vector<ImprovementTrace> improvements;
  long long completed_steps = 0;
  long long evaluated_moves = 0;
  long long single_moves = 0;
  long long block2_moves = 0;
  long long block3_moves = 0;
  long long pair_moves = 0;
  long long global_moves = 0;
  long long shake_events = 0;
  long long shake_flips = 0;
  long long penalty_updates = 0;
  long long full_audits = 0;
  int equal_best_updates = 0;

  auto retain_if_better = [&](int restart, long long step,
                              const std::string& cause) {
    const int objective = state.objective();
    const int penalty = degree_penalty(state);
    const int hamming = edge_hamming(state, base);
    if (objective < global_best) {
      require_full_objective(state);
      ++full_audits;
      global_best = objective;
      global_penalty = penalty;
      global_hamming = hamming;
      global_values = state.values();
      const auto [cliques, independent] = state.full_counts();
      improvements.push_back({
          static_cast<int>(improvements.size()) + 1,
          restart,
          step,
          objective,
          cliques,
          independent,
          penalty,
          hamming,
          cause,
      });
      std::cerr << "best restart=" << restart << " step=" << step
                << " E=" << objective << " cause=" << cause << '\n';
      if (objective == 0) write_graph6(options.output, state.graph6());
    } else if (objective == global_best &&
               (penalty < global_penalty ||
                (penalty == global_penalty && hamming > global_hamming))) {
      global_penalty = penalty;
      global_hamming = hamming;
      global_values = state.values();
      ++equal_best_updates;
    }
  };

  for (int restart = 0;
       restart < options.restarts && global_best > 0; ++restart) {
    state.set_values(base.edges);
    for (int shake = 0;
         shake < (restart == 0 ? 0 : options.restart_shakes) &&
         state.objective() > 0;
         ++shake) {
      std::vector<int> flips = multi_conflict_block(
          state, all_edges, options.shake_conflicts, rng);
      if (!flips.empty()) {
        apply_flips(state, flips);
        ++shake_events;
        shake_flips += flips.size();
      }
    }
    retain_if_better(restart, 0, "restart_shake");
    if (global_best == 0) break;

    std::vector<uint32_t> weights(state.subset_count(), 1);
    long long last_strict_step = 0;
    long long last_breakout = 0;
    long long last_shake = 0;
    for (long long step = 0;
         step < options.steps && state.objective() > 0 &&
         global_best > 0;
         ++step) {
      const int before_best = global_best;
      std::vector<ConflictMove> moves = conflict_candidates(
          state, all_edges, weights, options, rng);
      evaluated_moves += moves.size();
      for (const ConflictMove& move : moves) {
        if (move.kind == "conflict_single") ++single_moves;
        if (move.kind == "conflict_block2") ++block2_moves;
        if (move.kind == "conflict_block3") ++block3_moves;
        if (move.kind == "conflict_pair") ++pair_moves;
        if (move.kind == "global_block") ++global_moves;
      }
      const size_t selected = probsat_choice(moves, options, rng);
      apply_flips(state, moves[selected].flips);
      ++completed_steps;
      retain_if_better(restart, step + 1, moves[selected].kind);
      if (global_best < before_best) last_strict_step = step + 1;
      if (global_best == 0) break;

      if (options.breakout_interval > 0 &&
          step + 1 - last_strict_step >= options.breakout_interval &&
          step + 1 - last_breakout >= options.breakout_interval) {
        state.increment_bad_weights(weights);
        last_breakout = step + 1;
        ++penalty_updates;
      }
      if (options.shake_interval > 0 &&
          step + 1 - last_strict_step >= options.shake_interval &&
          step + 1 - last_shake >= options.shake_interval) {
        std::vector<int> flips = multi_conflict_block(
            state, all_edges, options.shake_conflicts, rng);
        if (!flips.empty()) {
          apply_flips(state, flips);
          ++shake_events;
          shake_flips += flips.size();
          retain_if_better(restart, step + 1, "multi_conflict_shake");
          if (global_best == 0) break;
        }
        last_shake = step + 1;
      }
      if (completed_steps % options.full_audit_interval == 0) {
        require_full_objective(state);
        ++full_audits;
      }
    }
  }

  state.set_values(global_values);
  require_full_objective(state);
  ++full_audits;
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != global_best ||
      degree_penalty(state) != global_penalty ||
      edge_hamming(state, base) != global_hamming)
    throw std::runtime_error("retained conflict-block state is inconsistent");
  write_graph6(options.output, state.graph6());

  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  const std::vector<int> degrees = state.sorted_degrees();
  std::ostringstream output;
  output << std::fixed << std::setprecision(6)
         << "{\"mode\":\"search\","
         << "\"algorithm\":\"conflict_hypergraph_probsat_blocks_v1\","
         << "\"hypothesis\":\"degree-fiber barriers require temporary degree "
            "changes and multi-conflict block flips\","
         << "\"seed\":" << options.seed << ','
         << "\"steps_requested_per_restart\":" << options.steps << ','
         << "\"restarts\":" << options.restarts << ','
         << "\"steps_executed\":" << completed_steps << ','
         << "\"evaluated_moves\":" << evaluated_moves << ','
         << "\"evaluated_single_moves\":" << single_moves << ','
         << "\"evaluated_block2_moves\":" << block2_moves << ','
         << "\"evaluated_block3_moves\":" << block3_moves << ','
         << "\"evaluated_pair_moves\":" << pair_moves << ','
         << "\"evaluated_global_moves\":" << global_moves << ','
         << "\"noise_per_million\":" << options.noise_per_million << ','
         << "\"degree_penalty_weight\":" << options.degree_penalty_weight << ','
         << "\"breakout_interval\":" << options.breakout_interval << ','
         << "\"shake_interval\":" << options.shake_interval << ','
         << "\"shake_conflicts\":" << options.shake_conflicts << ','
         << "\"restart_shakes\":" << options.restart_shakes << ','
         << "\"shake_events\":" << shake_events << ','
         << "\"shake_flips\":" << shake_flips << ','
         << "\"penalty_updates\":" << penalty_updates << ','
         << "\"full_incremental_objective_audits\":" << full_audits << ','
         << "\"strict_improvements\":" << improvements.size() << ','
         << "\"equal_best_updates\":" << equal_best_updates << ','
         << "\"initial_C5\":" << initial_cliques << ','
         << "\"initial_I5\":" << initial_independent << ','
         << "\"initial_E\":" << initial_objective << ','
         << "\"initial_degree_penalty\":" << initial_degree_penalty << ','
         << "\"C5\":" << cliques << ','
         << "\"I5\":" << independent << ','
         << "\"E\":" << global_best << ','
         << "\"degree_penalty\":" << global_penalty << ','
         << "\"edge_count\":" << state.edge_count() << ','
         << "\"edge_hamming_distance\":" << global_hamming << ','
         << "\"stopped_on_E0\":" << (global_best == 0 ? "true" : "false")
         << ",\"degree_sequence\":[";
  for (size_t index = 0; index < degrees.size(); ++index) {
    if (index) output << ',';
    output << degrees[index];
  }
  output << "],\"graph6\":" << json_quote(state.graph6()) << ','
         << "\"seed_graph\":" << json_quote(options.seed_graph) << ','
         << "\"output\":" << json_quote(options.output) << ','
         << "\"improvements\":[";
  for (size_t index = 0; index < improvements.size(); ++index) {
    if (index) output << ',';
    const ImprovementTrace& item = improvements[index];
    output << "{\"ordinal\":" << item.ordinal << ','
           << "\"restart\":" << item.restart << ','
           << "\"step\":" << item.step << ','
           << "\"E\":" << item.objective << ','
           << "\"C5\":" << item.cliques << ','
           << "\"I5\":" << item.independent << ','
           << "\"degree_penalty\":" << item.degree_penalty << ','
           << "\"edge_hamming_distance\":" << item.edge_hamming << ','
           << "\"cause\":" << json_quote(item.cause) << '}';
  }
  output << "],\"runtime_seconds\":" << elapsed << "}\n";
  const std::string payload = output.str();
  std::cout << payload;
  std::ofstream stream(options.json_output, std::ios::trunc);
  if (!stream)
    throw std::runtime_error("cannot write " + options.json_output);
  stream << payload;
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const ConflictOptions options = parse_conflict_options(argc, argv);
    const GraphSeed base =
        decode_graph6(first_data_line(options.seed_graph));
    if (options.self_check)
      return run_conflict_self_check(options, base);
    return run_conflict_search(options, base);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
