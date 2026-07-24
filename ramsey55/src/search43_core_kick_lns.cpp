// Deterministic local search beyond the certified radius-six core barrier.
//
// This translation unit reuses the audited incremental objective kernel from
// search43_incident_lns.cpp while replacing its fixed-boundary search policy.
#define main search43_incident_lns_embedded_main
#include "search43_incident_lns.cpp"
#undef main

#include <set>
#include <sstream>

namespace {

struct CoreKickOptions {
  std::string seed_graph;
  std::string metadata;
  std::string ranking;
  std::string output = "core_kick_best.g6";
  std::string json_output;
  uint64_t seed = 20260731;
  long long steps = 50000;
  int restarts = 3;
  int tabu_tenure = 11;
  double random_walk = 0.04;
  int breakout_interval = 250;
  int boundary_perturbation = 12;
  int initial_core_distance = 7;
  int min_core_distance = 7;
  int max_core_distance = 12;
  int guided_initial_edges = 4;
  int guided_pool = 64;
  int swap_samples = 4;
  int global_swap_interval = 8;
  bool self_check = false;
  int self_check_random_swaps = 100;
};

struct RankedCore {
  std::vector<int> edges;
  std::vector<std::pair<int, int>> pairs;
  std::vector<int> scores;
};

struct Move {
  int first{-1};
  int second{-1};
  int delta{};
  long long weighted_delta{};
};

CoreKickOptions parse_core_kick_options(int argc, char** argv) {
  CoreKickOptions options;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto value = [&]() -> std::string {
      if (index + 1 >= argc)
        throw std::runtime_error("missing value for " + option);
      return argv[++index];
    };
    if (option == "--seed-graph")
      options.seed_graph = value();
    else if (option == "--metadata")
      options.metadata = value();
    else if (option == "--ranking")
      options.ranking = value();
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
    else if (option == "--tabu")
      options.tabu_tenure = std::stoi(value());
    else if (option == "--random-walk")
      options.random_walk = std::stod(value());
    else if (option == "--breakout-interval")
      options.breakout_interval = std::stoi(value());
    else if (option == "--boundary-perturbation")
      options.boundary_perturbation = std::stoi(value());
    else if (option == "--initial-core-distance")
      options.initial_core_distance = std::stoi(value());
    else if (option == "--min-core-distance")
      options.min_core_distance = std::stoi(value());
    else if (option == "--max-core-distance")
      options.max_core_distance = std::stoi(value());
    else if (option == "--guided-initial-edges")
      options.guided_initial_edges = std::stoi(value());
    else if (option == "--guided-pool")
      options.guided_pool = std::stoi(value());
    else if (option == "--swap-samples")
      options.swap_samples = std::stoi(value());
    else if (option == "--global-swap-interval")
      options.global_swap_interval = std::stoi(value());
    else if (option == "--self-check-random-swaps")
      options.self_check_random_swaps = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.seed_graph.empty() || options.metadata.empty() ||
      options.ranking.empty())
    throw std::runtime_error(
        "--seed-graph, --metadata, and --ranking are required");
  if (options.steps < 0 || options.restarts < 1 ||
      options.tabu_tenure < 0 || options.random_walk < 0 ||
      options.random_walk > 1 || options.breakout_interval < 0 ||
      options.boundary_perturbation < 0 ||
      options.min_core_distance < 7 ||
      options.initial_core_distance < options.min_core_distance ||
      options.max_core_distance < options.initial_core_distance ||
      options.max_core_distance > 666 || options.guided_initial_edges < 0 ||
      options.guided_initial_edges > options.initial_core_distance ||
      options.guided_pool < options.guided_initial_edges ||
      options.guided_pool > 666 || options.swap_samples < 0 ||
      options.global_swap_interval < 0 ||
      options.self_check_random_swaps < 0)
    throw std::runtime_error("invalid core-kick search option");
  return options;
}

RankedCore read_ranked_core(const std::string& path, const SearchState& state,
                            const Boundary& boundary) {
  const std::string json = read_text(path);
  const std::vector<int> flat =
      integers_in_array(json, "full_occurrence_order_ranking");
  if (flat.size() != 666 * 4)
    throw std::runtime_error("ranking must contain 666 pair/rank/score records");
  RankedCore result;
  std::set<int> seen_edges;
  for (int index = 0; index < 666; ++index) {
    const int left = flat[4 * index];
    const int right = flat[4 * index + 1];
    const int rank = flat[4 * index + 2];
    const int score = flat[4 * index + 3];
    if (rank != index + 1 || !(0 <= left && left < right && right < kOrder) ||
        score <= 0)
      throw std::runtime_error("malformed proof-core ranking record");
    const int edge = state.edge_for_pair(left, right);
    if (boundary.free_mask[edge] || !seen_edges.insert(edge).second)
      throw std::runtime_error("ranking is not a permutation of core edges");
    result.edges.push_back(edge);
    result.pairs.emplace_back(left, right);
    result.scores.push_back(score);
  }
  if (seen_edges.size() != 666)
    throw std::runtime_error("ranking does not cover all 666 core edges");
  return result;
}

std::vector<int> core_edges_from_boundary(const Boundary& boundary) {
  std::vector<int> result;
  for (int edge = 0; edge < 903; ++edge)
    if (!boundary.free_mask[edge]) result.push_back(edge);
  if (result.size() != 666)
    throw std::runtime_error("core edge count is not 666");
  return result;
}

int core_distance(const SearchState& state, const GraphSeed& graph,
                  const std::vector<int>& core_edges) {
  int result = 0;
  for (int edge : core_edges)
    result += state.values()[edge] != graph.edges[edge];
  return result;
}

int boundary_distance(const SearchState& state, const GraphSeed& graph,
                      const Boundary& boundary) {
  int result = 0;
  for (int edge : boundary.free_edges)
    result += state.values()[edge] != graph.edges[edge];
  return result;
}

bool core_changed(const SearchState& state, const GraphSeed& graph, int edge) {
  return state.values()[edge] != graph.edges[edge];
}

int choose_changed_core(const SearchState& state, const GraphSeed& graph,
                        const std::vector<int>& core_edges,
                        std::mt19937_64& rng) {
  for (int attempt = 0; attempt < 4096; ++attempt) {
    const int edge =
        core_edges[static_cast<size_t>(rng() % core_edges.size())];
    if (core_changed(state, graph, edge)) return edge;
  }
  for (int edge : core_edges)
    if (core_changed(state, graph, edge)) return edge;
  throw std::runtime_error("no changed core edge is available");
}

int choose_unchanged_core(const SearchState& state, const GraphSeed& graph,
                          const RankedCore& ranking, int guided_pool,
                          std::mt19937_64& rng) {
  const bool guided = rng() % 100 < 75;
  const int limit = guided ? guided_pool : static_cast<int>(ranking.edges.size());
  for (int attempt = 0; attempt < 4096; ++attempt) {
    const int edge = ranking.edges[static_cast<size_t>(rng() % limit)];
    if (!core_changed(state, graph, edge)) return edge;
  }
  for (int edge : ranking.edges)
    if (!core_changed(state, graph, edge)) return edge;
  throw std::runtime_error("no unchanged core edge is available");
}

std::vector<int> initial_core_kick(const CoreKickOptions& options, int restart,
                                   const RankedCore& ranking,
                                   std::mt19937_64& rng) {
  std::vector<int> result;
  std::set<int> selected;
  if (restart == 0) {
    for (int index = 0; index < options.initial_core_distance; ++index) {
      result.push_back(ranking.edges[index]);
      selected.insert(ranking.edges[index]);
    }
    return result;
  }
  while (static_cast<int>(result.size()) < options.guided_initial_edges) {
    const int edge =
        ranking.edges[static_cast<size_t>(rng() % options.guided_pool)];
    if (selected.insert(edge).second) result.push_back(edge);
  }
  while (static_cast<int>(result.size()) < options.initial_core_distance) {
    const int edge =
        ranking.edges[static_cast<size_t>(rng() % ranking.edges.size())];
    if (selected.insert(edge).second) result.push_back(edge);
  }
  return result;
}

Move evaluate_single(SearchState& state, int edge,
                     const std::vector<uint32_t>& weights) {
  return {edge, -1, state.flip_delta(edge),
          state.weighted_flip_delta(edge, weights)};
}

Move evaluate_pair(SearchState& state, int first, int second,
                   const std::vector<uint32_t>& weights) {
  const int first_delta = state.flip_delta(first);
  const long long first_weighted = state.weighted_flip_delta(first, weights);
  state.flip(first);
  const int second_delta = state.flip_delta(second);
  const long long second_weighted = state.weighted_flip_delta(second, weights);
  state.flip(first);
  return {first, second, first_delta + second_delta,
          first_weighted + second_weighted};
}

void add_unique_move(std::vector<Move>& moves, const Move& move) {
  int first = move.first;
  int second = move.second;
  if (second >= 0 && first > second) std::swap(first, second);
  for (const Move& existing : moves) {
    int old_first = existing.first;
    int old_second = existing.second;
    if (old_second >= 0 && old_first > old_second)
      std::swap(old_first, old_second);
    if (first == old_first && second == old_second) return;
  }
  moves.push_back(move);
}

std::vector<Move> candidate_moves(
    SearchState& state, const GraphSeed& graph, const Boundary& boundary,
    const RankedCore& ranking, const std::vector<int>& core_edges,
    const std::vector<uint32_t>& weights, int distance, long long step,
    const CoreKickOptions& options, std::mt19937_64& rng) {
  std::vector<uint8_t> all_edges(903, 1);
  const std::vector<int> bad_edges =
      state.free_edges_of_random_bad(all_edges, rng);
  std::vector<Move> moves;
  for (int edge : bad_edges) {
    if (boundary.free_mask[edge]) {
      add_unique_move(moves, evaluate_single(state, edge, weights));
      continue;
    }
    const bool changed = core_changed(state, graph, edge);
    if ((!changed && distance < options.max_core_distance) ||
        (changed && distance > options.min_core_distance))
      add_unique_move(moves, evaluate_single(state, edge, weights));
    for (int sample = 0; sample < options.swap_samples; ++sample) {
      const int partner =
          changed ? choose_unchanged_core(state, graph, ranking,
                                          options.guided_pool, rng)
                  : choose_changed_core(state, graph, core_edges, rng);
      if (partner != edge)
        add_unique_move(
            moves, evaluate_pair(state, edge, partner, weights));
    }
  }
  if (options.global_swap_interval > 0 &&
      step % options.global_swap_interval == 0) {
    const int removed = choose_changed_core(state, graph, core_edges, rng);
    const int added = choose_unchanged_core(
        state, graph, ranking, options.guided_pool, rng);
    add_unique_move(moves, evaluate_pair(state, removed, added, weights));
  }
  if (moves.empty()) {
    const int removed = choose_changed_core(state, graph, core_edges, rng);
    const int added = choose_unchanged_core(
        state, graph, ranking, options.guided_pool, rng);
    moves.push_back(evaluate_pair(state, removed, added, weights));
  }
  return moves;
}

void apply_move(SearchState& state, const GraphSeed& graph,
                const Boundary& boundary, const Move& move, int& distance) {
  if (move.second < 0) {
    if (boundary.free_mask[move.first]) {
      state.flip(move.first);
      return;
    }
    const bool was_changed = core_changed(state, graph, move.first);
    state.flip(move.first);
    const bool is_changed = core_changed(state, graph, move.first);
    distance += static_cast<int>(is_changed) - static_cast<int>(was_changed);
    return;
  }
  const bool first_was = core_changed(state, graph, move.first);
  const bool second_was = core_changed(state, graph, move.second);
  state.flip(move.first);
  state.flip(move.second);
  const bool first_is = core_changed(state, graph, move.first);
  const bool second_is = core_changed(state, graph, move.second);
  distance += static_cast<int>(first_is) + static_cast<int>(second_is) -
              static_cast<int>(first_was) - static_cast<int>(second_was);
}

int run_core_kick_self_check(const CoreKickOptions& options,
                             const GraphSeed& graph,
                             const Boundary& boundary,
                             const RankedCore& ranking) {
  const auto started = Clock::now();
  SearchState state;
  const std::vector<int> core_edges = core_edges_from_boundary(boundary);
  state.set_values(graph.edges);
  std::mt19937_64 rng(options.seed);
  for (int edge :
       initial_core_kick(options, 0, ranking, rng))
    state.flip(edge);
  int distance = core_distance(state, graph, core_edges);
  if (distance != options.initial_core_distance)
    throw std::runtime_error("initial core kick has wrong distance");
  const auto [initial_cliques, initial_independent] = state.full_counts();
  if (state.objective() != initial_cliques + initial_independent)
    throw std::runtime_error("initial full objective mismatch");

  std::vector<uint32_t> weights(state.subset_count());
  for (size_t subset = 0; subset < weights.size(); ++subset)
    weights[subset] =
        1 + static_cast<uint32_t>((subset * uint64_t{11400714819323198485ull} +
                                   options.seed) %
                                  23);
  int single_checks = 0;
  for (int edge = 0; edge < 903; ++edge) {
    const int before = state.objective();
    const long long weighted_before = state.full_weighted_objective(weights);
    const Move move = evaluate_single(state, edge, weights);
    state.flip(edge);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + move.delta ||
        state.objective() != cliques + independent ||
        state.full_weighted_objective(weights) !=
            weighted_before + move.weighted_delta)
      throw std::runtime_error("single-edge exact delta check failed");
    state.flip(edge);
    ++single_checks;
  }

  int swap_checks = 0;
  for (int check = 0; check < options.self_check_random_swaps; ++check) {
    const int removed = choose_changed_core(state, graph, core_edges, rng);
    const int added = choose_unchanged_core(
        state, graph, ranking, options.guided_pool, rng);
    const int before = state.objective();
    const long long weighted_before = state.full_weighted_objective(weights);
    const Move move = evaluate_pair(state, removed, added, weights);
    int tracked_distance = distance;
    apply_move(state, graph, boundary, move, tracked_distance);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + move.delta ||
        state.objective() != cliques + independent ||
        state.full_weighted_objective(weights) !=
            weighted_before + move.weighted_delta ||
        tracked_distance != distance ||
        core_distance(state, graph, core_edges) != distance)
      throw std::runtime_error("core-swap exact delta check failed");
    apply_move(state, graph, boundary, move, tracked_distance);
    if (tracked_distance != distance)
      throw std::runtime_error("core-swap rollback distance failed");
    ++swap_checks;
  }
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"self_check\","
            << "\"algorithm\":\"core_kick_dynamic_swap_lns_v1\","
            << "\"seed\":" << options.seed << ","
            << "\"boundary_edge_count\":" << boundary.free_edges.size() << ","
            << "\"ranked_core_edge_count\":" << ranking.edges.size() << ","
            << "\"initial_core_distance\":" << distance << ","
            << "\"single_unweighted_and_weighted_checks\":" << single_checks
            << ",\"pair_unweighted_weighted_distance_checks\":" << swap_checks
            << ",\"status\":\"PASS\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

int run_core_kick_search(const CoreKickOptions& options,
                         const GraphSeed& graph, const Boundary& boundary,
                         const RankedCore& ranking) {
  const auto started = Clock::now();
  SearchState state;
  const std::vector<int> core_edges = core_edges_from_boundary(boundary);
  std::mt19937_64 rng(options.seed);
  std::uniform_real_distribution<double> unit(0.0, 1.0);
  int global_best = std::numeric_limits<int>::max();
  int global_core_distance = -1;
  int global_boundary_distance = -1;
  std::vector<uint8_t> global_values;
  long long completed_steps = 0;
  long long evaluated_moves = 0;
  long long evaluated_pair_moves = 0;
  long long penalty_updates = 0;
  int strict_improvements = 0;
  int equal_best_diversity_updates = 0;

  for (int restart = 0; restart < options.restarts && global_best > 0;
       ++restart) {
    state.set_values(graph.edges);
    const std::vector<int> kick =
        initial_core_kick(options, restart, ranking, rng);
    for (int edge : kick) state.flip(edge);
    int distance = core_distance(state, graph, core_edges);
    for (int flip = 0; flip < options.boundary_perturbation; ++flip) {
      const int edge = boundary.free_edges[
          static_cast<size_t>(rng() % boundary.free_edges.size())];
      state.flip(edge);
    }
    if (distance < options.min_core_distance ||
        distance > options.max_core_distance)
      throw std::runtime_error("restart violates core-distance bounds");

    std::vector<long long> tabu(903, 0);
    std::vector<uint32_t> weights(state.subset_count(), 1);
    int restart_best = state.objective();
    long long next_breakout = options.breakout_interval;
    const int start_boundary = boundary_distance(state, graph, boundary);
    if (state.objective() < global_best) {
      global_best = state.objective();
      global_core_distance = distance;
      global_boundary_distance = start_boundary;
      global_values = state.values();
      ++strict_improvements;
      std::cerr << "best restart=" << restart << " step=0 E=" << global_best
                << " core_distance=" << distance << '\n';
    }

    for (long long step = 0;
         step < options.steps && state.objective() > 0; ++step) {
      std::vector<Move> moves = candidate_moves(
          state, graph, boundary, ranking, core_edges, weights, distance, step,
          options, rng);
      evaluated_moves += moves.size();
      evaluated_pair_moves += std::count_if(
          moves.begin(), moves.end(),
          [](const Move& move) { return move.second >= 0; });
      std::vector<size_t> allowed;
      for (size_t index = 0; index < moves.size(); ++index) {
        const Move& move = moves[index];
        const bool blocked =
            tabu[move.first] > step ||
            (move.second >= 0 && tabu[move.second] > step);
        const bool aspiration =
            state.objective() + move.delta < global_best;
        if (!blocked || aspiration) allowed.push_back(index);
      }
      if (allowed.empty()) {
        for (size_t index = 0; index < moves.size(); ++index)
          allowed.push_back(index);
      }
      size_t selected_index = allowed[0];
      if (unit(rng) < options.random_walk) {
        selected_index =
            allowed[static_cast<size_t>(rng() % allowed.size())];
      } else {
        for (size_t index : allowed) {
          const Move& candidate = moves[index];
          const Move& selected = moves[selected_index];
          if (candidate.weighted_delta < selected.weighted_delta ||
              (candidate.weighted_delta == selected.weighted_delta &&
               candidate.delta < selected.delta) ||
              (candidate.weighted_delta == selected.weighted_delta &&
               candidate.delta == selected.delta && unit(rng) < 0.5))
            selected_index = index;
        }
      }
      const Move selected = moves[selected_index];
      apply_move(state, graph, boundary, selected, distance);
      if (distance < options.min_core_distance ||
          distance > options.max_core_distance)
        throw std::runtime_error("move violated core-distance bounds");
      tabu[selected.first] = step + options.tabu_tenure + 1;
      if (selected.second >= 0)
        tabu[selected.second] = step + options.tabu_tenure + 1;
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

      const int boundary_changed =
          boundary_distance(state, graph, boundary);
      if (state.objective() < global_best) {
        global_best = state.objective();
        global_core_distance = distance;
        global_boundary_distance = boundary_changed;
        global_values = state.values();
        ++strict_improvements;
        std::cerr << "best restart=" << restart << " step=" << step + 1
                  << " E=" << global_best
                  << " core_distance=" << distance << '\n';
      } else if (state.objective() == global_best &&
                 (distance > global_core_distance ||
                  (distance == global_core_distance &&
                   boundary_changed > global_boundary_distance))) {
        global_core_distance = distance;
        global_boundary_distance = boundary_changed;
        global_values = state.values();
        ++equal_best_diversity_updates;
      }
    }
  }

  if (global_values.empty())
    throw std::runtime_error("search did not retain an admissible state");
  state.set_values(global_values);
  const auto [cliques, independent] = state.full_counts();
  const int final_core_distance = core_distance(state, graph, core_edges);
  const int final_boundary_distance =
      boundary_distance(state, graph, boundary);
  if (cliques + independent != global_best ||
      final_core_distance != global_core_distance ||
      final_boundary_distance != global_boundary_distance ||
      final_core_distance < options.min_core_distance ||
      final_core_distance > options.max_core_distance)
    throw std::runtime_error("retained state failed final audit");
  write_graph6(options.output, state.graph6());

  std::vector<std::pair<int, int>> pair_by_edge(903);
  for (int left = 0; left < kOrder; ++left)
    for (int right = left + 1; right < kOrder; ++right)
      pair_by_edge[state.edge_for_pair(left, right)] = {left, right};
  std::ostringstream changed_core_json;
  changed_core_json << '[';
  bool first_pair = true;
  for (int edge : core_edges) {
    if (!core_changed(state, graph, edge)) continue;
    if (!first_pair) changed_core_json << ',';
    first_pair = false;
    changed_core_json << '[' << pair_by_edge[edge].first << ','
                      << pair_by_edge[edge].second << ']';
  }
  changed_core_json << ']';

  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  const std::vector<int> degrees = state.sorted_degrees();
  std::ostringstream output;
  output << std::fixed << std::setprecision(6)
         << "{\"mode\":\"search\","
         << "\"algorithm\":\"core_kick_dynamic_swap_lns_v1\","
         << "\"seed\":" << options.seed << ","
         << "\"steps_requested_per_restart\":" << options.steps << ","
         << "\"restarts\":" << options.restarts << ","
         << "\"steps_executed\":" << completed_steps << ","
         << "\"evaluated_moves\":" << evaluated_moves << ","
         << "\"evaluated_pair_moves\":" << evaluated_pair_moves << ","
         << "\"tabu_tenure\":" << options.tabu_tenure << ","
         << "\"random_walk\":" << options.random_walk << ","
         << "\"breakout_interval\":" << options.breakout_interval << ","
         << "\"boundary_perturbation\":" << options.boundary_perturbation
         << ",\"initial_core_distance\":" << options.initial_core_distance
         << ",\"min_core_distance\":" << options.min_core_distance << ","
         << "\"max_core_distance\":" << options.max_core_distance << ","
         << "\"guided_initial_edges\":" << options.guided_initial_edges << ","
         << "\"guided_pool\":" << options.guided_pool << ","
         << "\"swap_samples\":" << options.swap_samples << ","
         << "\"global_swap_interval\":" << options.global_swap_interval << ","
         << "\"penalty_updates\":" << penalty_updates << ","
         << "\"strict_improvements\":" << strict_improvements << ","
         << "\"equal_best_diversity_updates\":"
         << equal_best_diversity_updates << ","
         << "\"boundary_edge_count\":237,\"core_edge_count\":666,"
         << "\"changed_boundary_edges\":" << final_boundary_distance << ","
         << "\"changed_core_edge_count\":" << final_core_distance << ","
         << "\"changed_core_edges\":" << changed_core_json.str() << ","
         << "\"C5\":" << cliques << ",\"I5\":" << independent << ","
         << "\"E\":" << global_best << ","
         << "\"edge_count\":" << state.edge_count() << ","
         << "\"degree_sequence\":[";
  for (size_t index = 0; index < degrees.size(); ++index) {
    if (index) output << ',';
    output << degrees[index];
  }
  output << "],\"graph6\":" << json_quote(state.graph6()) << ","
         << "\"seed_graph\":" << json_quote(options.seed_graph) << ","
         << "\"metadata\":" << json_quote(options.metadata) << ","
         << "\"ranking\":" << json_quote(options.ranking) << ","
         << "\"runtime_seconds\":" << elapsed << ","
         << "\"output\":" << json_quote(options.output) << "}\n";
  const std::string payload = output.str();
  std::cout << payload;
  if (!options.json_output.empty()) {
    std::ofstream stream(options.json_output, std::ios::trunc);
    if (!stream)
      throw std::runtime_error("cannot write " + options.json_output);
    stream << payload;
  }
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const CoreKickOptions options = parse_core_kick_options(argc, argv);
    SearchState validation_state;
    const GraphSeed graph = decode_graph6(first_data_line(options.seed_graph));
    const Boundary boundary =
        validate_boundary(validation_state, graph, options.metadata);
    const RankedCore ranking =
        read_ranked_core(options.ranking, validation_state, boundary);
    if (options.self_check)
      return run_core_kick_self_check(options, graph, boundary, ranking);
    return run_core_kick_search(options, graph, boundary, ranking);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
