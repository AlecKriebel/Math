// Deterministic degree-preserving 2-switch and compound-2-switch search.
//
// This translation unit reuses the audited incremental five-set objective
// kernel from search43_incident_lns.cpp.  Every accepted primitive replaces
// two disjoint present edges by the opposite matching of the same four
// vertices, so the labeled degree vector is invariant.
#define main search43_incident_lns_embedded_main
#include "search43_incident_lns.cpp"
#undef main

#include <array>
#include <set>
#include <sstream>

namespace {

struct DegreeSwitchOptions {
  std::string seed_graph;
  std::string output = "degree_switch_best.g6";
  std::string json_output;
  std::string improvement_prefix;
  uint64_t seed = 20260801;
  long long steps = 6000;
  int restarts = 3;
  int tabu_tenure = 13;
  int random_walk_per_million = 40000;
  int breakout_interval = 300;
  int restart_switches = 24;
  int targeted_samples = 8;
  int global_samples = 3;
  int compound_samples = 2;
  int full_audit_interval = 250;
  bool self_check = false;
  int self_check_single = 100;
  int self_check_compound = 50;
};

struct EdgeMap {
  std::array<int, 903> left{};
  std::array<int, 903> right{};
};

struct SwitchMove {
  std::vector<int> flips;
  int switch_count{};
  int delta{};
  long long weighted_delta{};
};

struct Improvement {
  int ordinal{};
  int restart{};
  long long step{};
  int objective{};
  int cliques{};
  int independent{};
  int hamming_distance{};
  std::string path;
  std::string graph6;
};

DegreeSwitchOptions parse_degree_switch_options(int argc, char** argv) {
  DegreeSwitchOptions options;
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
    else if (option == "--improvement-prefix")
      options.improvement_prefix = value();
    else if (option == "--seed")
      options.seed = std::stoull(value());
    else if (option == "--steps")
      options.steps = std::stoll(value());
    else if (option == "--restarts")
      options.restarts = std::stoi(value());
    else if (option == "--tabu")
      options.tabu_tenure = std::stoi(value());
    else if (option == "--random-walk-per-million")
      options.random_walk_per_million = std::stoi(value());
    else if (option == "--breakout-interval")
      options.breakout_interval = std::stoi(value());
    else if (option == "--restart-switches")
      options.restart_switches = std::stoi(value());
    else if (option == "--targeted-samples")
      options.targeted_samples = std::stoi(value());
    else if (option == "--global-samples")
      options.global_samples = std::stoi(value());
    else if (option == "--compound-samples")
      options.compound_samples = std::stoi(value());
    else if (option == "--full-audit-interval")
      options.full_audit_interval = std::stoi(value());
    else if (option == "--self-check-single")
      options.self_check_single = std::stoi(value());
    else if (option == "--self-check-compound")
      options.self_check_compound = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.seed_graph.empty())
    throw std::runtime_error("--seed-graph is required");
  if (!options.self_check &&
      (options.json_output.empty() || options.improvement_prefix.empty()))
    throw std::runtime_error(
        "--json-output and --improvement-prefix are required for search");
  if (options.steps < 0 || options.restarts < 1 ||
      options.tabu_tenure < 0 || options.random_walk_per_million < 0 ||
      options.random_walk_per_million > 1000000 ||
      options.breakout_interval < 0 || options.restart_switches < 0 ||
      options.targeted_samples < 0 || options.global_samples < 0 ||
      options.compound_samples < 0 || options.full_audit_interval < 1 ||
      options.self_check_single < 0 || options.self_check_compound < 0)
    throw std::runtime_error("invalid degree-switch option");
  return options;
}

EdgeMap build_edge_map(const SearchState& state) {
  EdgeMap result;
  for (int left = 0; left < kOrder; ++left) {
    for (int right = left + 1; right < kOrder; ++right) {
      const int edge = state.edge_for_pair(left, right);
      result.left[edge] = left;
      result.right[edge] = right;
    }
  }
  return result;
}

std::vector<int> labeled_degrees(const SearchState& state,
                                 const EdgeMap& edge_map) {
  std::vector<int> result(kOrder, 0);
  for (int edge = 0; edge < 903; ++edge) {
    if (!state.values()[edge]) continue;
    ++result[edge_map.left[edge]];
    ++result[edge_map.right[edge]];
  }
  return result;
}

int edge_hamming_distance(const SearchState& state,
                          const GraphSeed& base) {
  int result = 0;
  for (int edge = 0; edge < 903; ++edge)
    result += state.values()[edge] != base.edges[edge];
  return result;
}

bool four_distinct(int a, int b, int c, int d) {
  std::array<int, 4> vertices{a, b, c, d};
  std::sort(vertices.begin(), vertices.end());
  return std::adjacent_find(vertices.begin(), vertices.end()) ==
         vertices.end();
}

std::vector<int> switch_from_present_edges(
    const SearchState& state, const EdgeMap& edge_map, int first, int second,
    int orientation) {
  if (!state.values()[first] || !state.values()[second])
    return {};
  const int a = edge_map.left[first];
  const int b = edge_map.right[first];
  const int c = edge_map.left[second];
  const int d = edge_map.right[second];
  if (!four_distinct(a, b, c, d)) return {};
  const int add_first = orientation == 0
                            ? state.edge_for_pair(a, c)
                            : state.edge_for_pair(a, d);
  const int add_second = orientation == 0
                             ? state.edge_for_pair(b, d)
                             : state.edge_for_pair(b, c);
  if (state.values()[add_first] || state.values()[add_second] ||
      add_first == add_second || add_first == first ||
      add_first == second || add_second == first || add_second == second)
    return {};
  return {first, second, add_first, add_second};
}

std::vector<int> random_global_switch(const SearchState& state,
                                      const EdgeMap& edge_map,
                                      std::mt19937_64& rng) {
  for (int attempt = 0; attempt < 2048; ++attempt) {
    const int first = static_cast<int>(rng() % 903);
    const int second = static_cast<int>(rng() % 903);
    if (first == second) continue;
    const int initial_orientation = static_cast<int>(rng() & 1);
    std::vector<int> result = switch_from_present_edges(
        state, edge_map, first, second, initial_orientation);
    if (!result.empty()) return result;
    result = switch_from_present_edges(
        state, edge_map, first, second, 1 - initial_orientation);
    if (!result.empty()) return result;
  }
  return {};
}

std::vector<int> targeted_switch(const SearchState& state,
                                 const EdgeMap& edge_map,
                                 const std::vector<uint8_t>& all_edges,
                                 std::mt19937_64& rng) {
  if (state.objective() == 0) return {};
  const std::vector<int> bad_edges =
      state.free_edges_of_random_bad(all_edges, rng);
  if (bad_edges.size() != 10)
    throw std::runtime_error("a forbidden five-set does not have ten pairs");
  const bool clique = state.values()[bad_edges.front()] != 0;
  for (int attempt = 0; attempt < 2048; ++attempt) {
    const int target =
        bad_edges[static_cast<size_t>(rng() % bad_edges.size())];
    if (clique) {
      const int partner = static_cast<int>(rng() % 903);
      const int initial_orientation = static_cast<int>(rng() & 1);
      std::vector<int> result = switch_from_present_edges(
          state, edge_map, target, partner, initial_orientation);
      if (!result.empty()) return result;
      result = switch_from_present_edges(
          state, edge_map, target, partner, 1 - initial_orientation);
      if (!result.empty()) return result;
      continue;
    }

    const int a = edge_map.left[target];
    const int c = edge_map.right[target];
    const int b = static_cast<int>(rng() % kOrder);
    const int d = static_cast<int>(rng() % kOrder);
    if (!four_distinct(a, b, c, d)) continue;
    const int remove_first = state.edge_for_pair(a, b);
    const int remove_second = state.edge_for_pair(c, d);
    const int add_second = state.edge_for_pair(b, d);
    if (!state.values()[remove_first] || !state.values()[remove_second] ||
        state.values()[target] || state.values()[add_second] ||
        remove_first == remove_second || target == add_second)
      continue;
    return {remove_first, remove_second, target, add_second};
  }
  return {};
}

void apply_sequence(SearchState& state, const std::vector<int>& flips) {
  for (int edge : flips) state.flip(edge);
}

void rollback_sequence(SearchState& state, const std::vector<int>& flips) {
  for (auto iterator = flips.rbegin(); iterator != flips.rend(); ++iterator)
    state.flip(*iterator);
}

SwitchMove evaluate_sequence(SearchState& state, std::vector<int> flips,
                             int switch_count,
                             const std::vector<uint32_t>& weights) {
  int delta = 0;
  long long weighted_delta = 0;
  for (int edge : flips) {
    delta += state.flip_delta(edge);
    weighted_delta += state.weighted_flip_delta(edge, weights);
    state.flip(edge);
  }
  rollback_sequence(state, flips);
  return {std::move(flips), switch_count, delta, weighted_delta};
}

std::vector<int> parity_signature(const std::vector<int>& flips) {
  std::array<int, 903> parity{};
  for (int edge : flips) parity[edge] ^= 1;
  std::vector<int> result;
  for (int edge = 0; edge < 903; ++edge)
    if (parity[edge]) result.push_back(edge);
  return result;
}

void add_unique_move(std::vector<SwitchMove>& moves, SwitchMove move) {
  const std::vector<int> signature = parity_signature(move.flips);
  if (signature.empty()) return;
  for (const SwitchMove& old : moves)
    if (parity_signature(old.flips) == signature) return;
  moves.push_back(std::move(move));
}

bool disjoint_flips(const std::vector<int>& first,
                    const std::vector<int>& second) {
  std::set<int> seen(first.begin(), first.end());
  return std::all_of(second.begin(), second.end(),
                     [&](int edge) { return !seen.count(edge); });
}

std::vector<SwitchMove> candidate_moves(
    SearchState& state, const EdgeMap& edge_map,
    const std::vector<uint8_t>& all_edges,
    const std::vector<uint32_t>& weights,
    const DegreeSwitchOptions& options, std::mt19937_64& rng) {
  std::vector<SwitchMove> moves;
  for (int sample = 0; sample < options.targeted_samples; ++sample) {
    std::vector<int> flips =
        targeted_switch(state, edge_map, all_edges, rng);
    if (!flips.empty())
      add_unique_move(
          moves, evaluate_sequence(state, std::move(flips), 1, weights));
  }
  for (int sample = 0; sample < options.global_samples; ++sample) {
    std::vector<int> flips = random_global_switch(state, edge_map, rng);
    if (!flips.empty())
      add_unique_move(
          moves, evaluate_sequence(state, std::move(flips), 1, weights));
  }
  for (int sample = 0; sample < options.compound_samples; ++sample) {
    std::vector<int> first =
        targeted_switch(state, edge_map, all_edges, rng);
    if (first.empty()) continue;
    apply_sequence(state, first);
    std::vector<int> second;
    if (state.objective() > 0)
      second = targeted_switch(state, edge_map, all_edges, rng);
    if (second.empty())
      second = random_global_switch(state, edge_map, rng);
    rollback_sequence(state, first);
    if (second.empty() || !disjoint_flips(first, second)) continue;
    first.insert(first.end(), second.begin(), second.end());
    add_unique_move(
        moves, evaluate_sequence(state, std::move(first), 2, weights));
  }
  if (moves.empty()) {
    std::vector<int> flips = random_global_switch(state, edge_map, rng);
    if (flips.empty())
      throw std::runtime_error("could not construct a legal 2-switch");
    moves.push_back(
        evaluate_sequence(state, std::move(flips), 1, weights));
  }
  return moves;
}

void require_exact_state(const SearchState& state,
                         const std::vector<int>& base_degrees) {
  if (labeled_degrees(state, build_edge_map(state)) != base_degrees)
    throw std::runtime_error("degree-preserving invariant failed");
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != cliques + independent)
    throw std::runtime_error("incremental objective disagrees with full count");
}

Improvement preserve_improvement(const DegreeSwitchOptions& options,
                                 SearchState& state, const GraphSeed& base,
                                 int ordinal, int restart, long long step) {
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != cliques + independent)
    throw std::runtime_error("improvement objective failed full audit");
  std::ostringstream path;
  path << options.improvement_prefix << '_' << ordinal << "_E"
       << state.objective() << ".g6";
  write_graph6(path.str(), state.graph6());
  return {
      ordinal,
      restart,
      step,
      state.objective(),
      cliques,
      independent,
      edge_hamming_distance(state, base),
      path.str(),
      state.graph6(),
  };
}

int run_degree_switch_self_check(const DegreeSwitchOptions& options,
                                 const GraphSeed& base) {
  const auto started = Clock::now();
  SearchState state;
  state.set_values(base.edges);
  const EdgeMap edge_map = build_edge_map(state);
  const std::vector<int> base_degrees = labeled_degrees(state, edge_map);
  const std::string base_graph6 = state.graph6();
  std::vector<uint8_t> all_edges(903, 1);
  std::vector<uint32_t> weights(state.subset_count());
  for (size_t subset = 0; subset < weights.size(); ++subset)
    weights[subset] =
        1 + static_cast<uint32_t>(
                (subset * uint64_t{11400714819323198485ull} + options.seed) %
                29);
  std::mt19937_64 rng(options.seed);

  auto check_move = [&](const std::vector<int>& flips, int switch_count) {
    const int before = state.objective();
    const long long weighted_before =
        state.full_weighted_objective(weights);
    const SwitchMove move =
        evaluate_sequence(state, flips, switch_count, weights);
    apply_sequence(state, move.flips);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + move.delta ||
        state.objective() != cliques + independent ||
        state.full_weighted_objective(weights) !=
            weighted_before + move.weighted_delta ||
        labeled_degrees(state, edge_map) != base_degrees)
      throw std::runtime_error("degree-switch exact delta check failed");
    rollback_sequence(state, move.flips);
    if (state.graph6() != base_graph6 ||
        labeled_degrees(state, edge_map) != base_degrees)
      throw std::runtime_error("degree-switch rollback failed");
  };

  int single_checks = 0;
  for (int check = 0; check < options.self_check_single; ++check) {
    std::vector<int> flips =
        check % 2 == 0
            ? targeted_switch(state, edge_map, all_edges, rng)
            : random_global_switch(state, edge_map, rng);
    if (flips.empty()) {
      --check;
      continue;
    }
    check_move(flips, 1);
    ++single_checks;
  }

  int compound_checks = 0;
  for (int check = 0; check < options.self_check_compound; ++check) {
    std::vector<int> first =
        targeted_switch(state, edge_map, all_edges, rng);
    if (first.empty()) {
      --check;
      continue;
    }
    apply_sequence(state, first);
    std::vector<int> second =
        random_global_switch(state, edge_map, rng);
    rollback_sequence(state, first);
    if (second.empty() || !disjoint_flips(first, second)) {
      --check;
      continue;
    }
    first.insert(first.end(), second.begin(), second.end());
    check_move(first, 2);
    ++compound_checks;
  }

  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"self_check\","
            << "\"algorithm\":\"degree_preserving_2switch_compound_lns_v1\","
            << "\"seed\":" << options.seed << ','
            << "\"initial_objective\":" << state.objective() << ','
            << "\"single_switch_checks\":" << single_checks << ','
            << "\"compound_switch_checks\":" << compound_checks << ','
            << "\"degree_vector_preserved\":true,"
            << "\"unweighted_weighted_full_count_checks\":true,"
            << "\"rollback_checks\":true,"
            << "\"status\":\"PASS\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

int run_degree_switch_search(const DegreeSwitchOptions& options,
                             const GraphSeed& base) {
  const auto started = Clock::now();
  SearchState state;
  state.set_values(base.edges);
  const EdgeMap edge_map = build_edge_map(state);
  const std::vector<int> base_degrees = labeled_degrees(state, edge_map);
  const auto [base_cliques, base_independent] = state.full_counts();
  if (base_cliques + base_independent != 2 ||
      state.objective() != base_cliques + base_independent)
    throw std::runtime_error("production seed is not independently E=2");

  std::mt19937_64 rng(options.seed);
  std::vector<uint8_t> all_edges(903, 1);
  int global_best = state.objective();
  int global_hamming = 0;
  std::vector<uint8_t> global_values = state.values();
  std::vector<Improvement> improvements;
  long long completed_steps = 0;
  long long evaluated_moves = 0;
  long long evaluated_single_switch_moves = 0;
  long long evaluated_compound_moves = 0;
  long long penalty_updates = 0;
  long long full_audits = 0;
  int equal_best_diversity_updates = 0;

  for (int restart = 0;
       restart < options.restarts && global_best > 0; ++restart) {
    state.set_values(base.edges);
    const int perturbation_count =
        restart == 0 ? 0 : options.restart_switches;
    for (int move = 0; move < perturbation_count; ++move) {
      std::vector<int> flips =
          random_global_switch(state, edge_map, rng);
      if (flips.empty())
        throw std::runtime_error("restart perturbation has no legal switch");
      apply_sequence(state, flips);
    }
    if (labeled_degrees(state, edge_map) != base_degrees)
      throw std::runtime_error("restart changed the labeled degree vector");

    std::vector<long long> tabu(903, 0);
    std::vector<uint32_t> weights(state.subset_count(), 1);
    int restart_best = state.objective();
    long long next_breakout = options.breakout_interval;
    const int restart_hamming = edge_hamming_distance(state, base);
    if (state.objective() < global_best) {
      global_best = state.objective();
      global_hamming = restart_hamming;
      global_values = state.values();
      improvements.push_back(preserve_improvement(
          options, state, base,
          static_cast<int>(improvements.size()) + 1, restart, 0));
      std::cerr << "best restart=" << restart << " step=0 E="
                << global_best << " edge_hamming=" << restart_hamming
                << '\n';
    } else if (state.objective() == global_best &&
               restart_hamming > global_hamming) {
      global_hamming = restart_hamming;
      global_values = state.values();
      ++equal_best_diversity_updates;
    }

    for (long long step = 0;
         step < options.steps && state.objective() > 0; ++step) {
      std::vector<SwitchMove> moves = candidate_moves(
          state, edge_map, all_edges, weights, options, rng);
      evaluated_moves += static_cast<long long>(moves.size());
      for (const SwitchMove& move : moves) {
        if (move.switch_count == 1)
          ++evaluated_single_switch_moves;
        else
          ++evaluated_compound_moves;
      }

      std::vector<size_t> allowed;
      for (size_t index = 0; index < moves.size(); ++index) {
        bool blocked = false;
        for (int edge : parity_signature(moves[index].flips))
          blocked = blocked || tabu[edge] > completed_steps;
        const bool aspiration =
            state.objective() + moves[index].delta < global_best;
        if (!blocked || aspiration) allowed.push_back(index);
      }
      if (allowed.empty()) {
        for (size_t index = 0; index < moves.size(); ++index)
          allowed.push_back(index);
      }
      size_t selected_index = allowed.front();
      if (static_cast<int>(rng() % 1000000) <
          options.random_walk_per_million) {
        selected_index =
            allowed[static_cast<size_t>(rng() % allowed.size())];
      } else {
        for (size_t index : allowed) {
          const SwitchMove& candidate = moves[index];
          const SwitchMove& selected = moves[selected_index];
          if (candidate.weighted_delta < selected.weighted_delta ||
              (candidate.weighted_delta == selected.weighted_delta &&
               candidate.delta < selected.delta) ||
              (candidate.weighted_delta == selected.weighted_delta &&
               candidate.delta == selected.delta &&
               candidate.switch_count < selected.switch_count) ||
              (candidate.weighted_delta == selected.weighted_delta &&
               candidate.delta == selected.delta &&
               candidate.switch_count == selected.switch_count &&
               (rng() & 1)))
            selected_index = index;
        }
      }

      const SwitchMove selected = moves[selected_index];
      apply_sequence(state, selected.flips);
      if (labeled_degrees(state, edge_map) != base_degrees)
        throw std::runtime_error("selected move changed a vertex degree");
      for (int edge : parity_signature(selected.flips))
        tabu[edge] =
            completed_steps + options.tabu_tenure + 1;
      ++completed_steps;

      if (state.objective() < restart_best) {
        restart_best = state.objective();
        if (options.breakout_interval > 0)
          next_breakout = step + 1 + options.breakout_interval;
      } else if (options.breakout_interval > 0 &&
                 step + 1 >= next_breakout) {
        state.increment_bad_weights(weights);
        ++penalty_updates;
        next_breakout += options.breakout_interval;
      }

      if (completed_steps % options.full_audit_interval == 0) {
        require_exact_state(state, base_degrees);
        ++full_audits;
      }

      const int hamming = edge_hamming_distance(state, base);
      if (state.objective() < global_best) {
        global_best = state.objective();
        global_hamming = hamming;
        global_values = state.values();
        improvements.push_back(preserve_improvement(
            options, state, base,
            static_cast<int>(improvements.size()) + 1, restart,
            step + 1));
        std::cerr << "best restart=" << restart << " step=" << step + 1
                  << " E=" << global_best
                  << " edge_hamming=" << hamming << '\n';
      } else if (state.objective() == global_best &&
                 hamming > global_hamming) {
        global_hamming = hamming;
        global_values = state.values();
        ++equal_best_diversity_updates;
      }
    }
  }

  state.set_values(global_values);
  require_exact_state(state, base_degrees);
  ++full_audits;
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != global_best ||
      edge_hamming_distance(state, base) != global_hamming)
    throw std::runtime_error("retained state disagrees with search record");
  write_graph6(options.output, state.graph6());

  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  const std::vector<int> final_degrees = labeled_degrees(state, edge_map);
  const std::vector<int> sorted_degrees = state.sorted_degrees();
  std::ostringstream output;
  output << std::fixed << std::setprecision(6)
         << "{\"mode\":\"search\","
         << "\"algorithm\":\"degree_preserving_2switch_compound_lns_v1\","
         << "\"seed\":" << options.seed << ','
         << "\"steps_requested_per_restart\":" << options.steps << ','
         << "\"restarts\":" << options.restarts << ','
         << "\"steps_executed\":" << completed_steps << ','
         << "\"evaluated_moves\":" << evaluated_moves << ','
         << "\"evaluated_single_switch_moves\":"
         << evaluated_single_switch_moves << ','
         << "\"evaluated_compound_moves\":" << evaluated_compound_moves << ','
         << "\"tabu_tenure\":" << options.tabu_tenure << ','
         << "\"random_walk_per_million\":"
         << options.random_walk_per_million << ','
         << "\"breakout_interval\":" << options.breakout_interval << ','
         << "\"restart_switches\":" << options.restart_switches << ','
         << "\"targeted_samples\":" << options.targeted_samples << ','
         << "\"global_samples\":" << options.global_samples << ','
         << "\"compound_samples\":" << options.compound_samples << ','
         << "\"full_audit_interval\":" << options.full_audit_interval << ','
         << "\"penalty_updates\":" << penalty_updates << ','
         << "\"full_incremental_objective_audits\":" << full_audits << ','
         << "\"strict_improvements\":" << improvements.size() << ','
         << "\"equal_best_diversity_updates\":"
         << equal_best_diversity_updates << ','
         << "\"initial_C5\":" << base_cliques << ','
         << "\"initial_I5\":" << base_independent << ','
         << "\"initial_E\":2,"
         << "\"C5\":" << cliques << ','
         << "\"I5\":" << independent << ','
         << "\"E\":" << global_best << ','
         << "\"edge_count\":" << state.edge_count() << ','
         << "\"edge_hamming_distance\":" << global_hamming << ','
         << "\"degree_vector_preserved\":true,"
         << "\"stopped_on_E0\":" << (global_best == 0 ? "true" : "false")
         << ",\"degree_vector\":[";
  for (size_t index = 0; index < final_degrees.size(); ++index) {
    if (index) output << ',';
    output << final_degrees[index];
  }
  output << "],\"degree_sequence\":[";
  for (size_t index = 0; index < sorted_degrees.size(); ++index) {
    if (index) output << ',';
    output << sorted_degrees[index];
  }
  output << "],\"graph6\":" << json_quote(state.graph6()) << ','
         << "\"seed_graph\":" << json_quote(options.seed_graph) << ','
         << "\"output\":" << json_quote(options.output) << ','
         << "\"improvements\":[";
  for (size_t index = 0; index < improvements.size(); ++index) {
    if (index) output << ',';
    const Improvement& item = improvements[index];
    output << "{\"ordinal\":" << item.ordinal << ','
           << "\"restart\":" << item.restart << ','
           << "\"step\":" << item.step << ','
           << "\"E\":" << item.objective << ','
           << "\"C5\":" << item.cliques << ','
           << "\"I5\":" << item.independent << ','
           << "\"edge_hamming_distance\":" << item.hamming_distance << ','
           << "\"path\":" << json_quote(item.path) << ','
           << "\"graph6\":" << json_quote(item.graph6) << '}';
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
    const DegreeSwitchOptions options =
        parse_degree_switch_options(argc, argv);
    const GraphSeed base =
        decode_graph6(first_data_line(options.seed_graph));
    if (options.self_check)
      return run_degree_switch_self_check(options, base);
    return run_degree_switch_search(options, base);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
