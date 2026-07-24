// Complement-normalized aligned near-parent crossover with path relinking and
// exact incremental conflict repair.
#define main search43_incident_lns_embedded_main
#include "search43_incident_lns.cpp"
#undef main

#include <cmath>
#include <set>
#include <sstream>
#include <tuple>

namespace {

struct RelinkOptions {
  std::string parent_a;
  std::string parent_b;
  bool complement_a = false;
  bool complement_b = false;
  std::vector<int> mapping;
  std::string direction = "a_to_b";
  std::string output = "path_relink_best.g6";
  std::string child_output = "path_relink_child.g6";
  std::string json_output;
  uint64_t seed = 2026083001;
  long long steps = 10000;
  int path_sample = 24;
  int path_flips = 48;
  int tabu_tenure = 11;
  int random_walk_per_million = 50000;
  int breakout_interval = 300;
  int agreement_penalty = 4;
  int corridor_penalty = 1;
  int full_audit_interval = 250;
  bool self_check = false;
  int self_check_moves = 100;
};

struct RelinkImprovement {
  int ordinal{};
  long long step{};
  int objective{};
  int cliques{};
  int independent{};
  int distance_a{};
  int distance_b{};
  int agreement_breaks{};
};

std::vector<int> comma_integers(const std::string& text) {
  std::vector<int> result;
  size_t start = 0;
  while (start <= text.size()) {
    const size_t comma = text.find(',', start);
    const std::string token =
        text.substr(start, comma == std::string::npos
                               ? std::string::npos
                               : comma - start);
    if (token.empty())
      throw std::runtime_error("mapping contains an empty item");
    result.push_back(std::stoi(token));
    if (comma == std::string::npos) break;
    start = comma + 1;
  }
  return result;
}

RelinkOptions parse_relink_options(int argc, char** argv) {
  RelinkOptions options;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto value = [&]() -> std::string {
      if (index + 1 >= argc)
        throw std::runtime_error("missing value for " + option);
      return argv[++index];
    };
    if (option == "--parent-a")
      options.parent_a = value();
    else if (option == "--parent-b")
      options.parent_b = value();
    else if (option == "--complement-a")
      options.complement_a = std::stoi(value()) != 0;
    else if (option == "--complement-b")
      options.complement_b = std::stoi(value()) != 0;
    else if (option == "--mapping")
      options.mapping = comma_integers(value());
    else if (option == "--direction")
      options.direction = value();
    else if (option == "--output")
      options.output = value();
    else if (option == "--child-output")
      options.child_output = value();
    else if (option == "--json-output")
      options.json_output = value();
    else if (option == "--seed")
      options.seed = std::stoull(value());
    else if (option == "--steps")
      options.steps = std::stoll(value());
    else if (option == "--path-sample")
      options.path_sample = std::stoi(value());
    else if (option == "--path-flips")
      options.path_flips = std::stoi(value());
    else if (option == "--tabu-tenure")
      options.tabu_tenure = std::stoi(value());
    else if (option == "--random-walk-per-million")
      options.random_walk_per_million = std::stoi(value());
    else if (option == "--breakout-interval")
      options.breakout_interval = std::stoi(value());
    else if (option == "--agreement-penalty")
      options.agreement_penalty = std::stoi(value());
    else if (option == "--corridor-penalty")
      options.corridor_penalty = std::stoi(value());
    else if (option == "--full-audit-interval")
      options.full_audit_interval = std::stoi(value());
    else if (option == "--self-check-moves")
      options.self_check_moves = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.parent_a.empty() || options.parent_b.empty())
    throw std::runtime_error("--parent-a and --parent-b are required");
  if (options.mapping.size() != kOrder)
    throw std::runtime_error("--mapping must contain 43 vertices");
  std::vector<int> sorted = options.mapping;
  std::sort(sorted.begin(), sorted.end());
  for (int vertex = 0; vertex < kOrder; ++vertex)
    if (sorted[vertex] != vertex)
      throw std::runtime_error("--mapping is not a permutation");
  if (options.direction != "a_to_b" && options.direction != "b_to_a")
    throw std::runtime_error("--direction must be a_to_b or b_to_a");
  if (!options.self_check &&
      (options.json_output.empty() || options.child_output.empty()))
    throw std::runtime_error(
        "--json-output and --child-output are required");
  if (options.steps < 0 || options.path_sample < 1 ||
      options.path_flips < 1 ||
      options.tabu_tenure < 0 || options.random_walk_per_million < 0 ||
      options.random_walk_per_million > 1000000 ||
      options.breakout_interval < 0 || options.agreement_penalty < 0 ||
      options.corridor_penalty < 0 || options.full_audit_interval < 1 ||
      options.self_check_moves < 0)
    throw std::runtime_error("invalid path-relink option");
  return options;
}

std::vector<uint8_t> oriented_values(const GraphSeed& graph,
                                     bool use_complement) {
  std::vector<uint8_t> result = graph.edges;
  if (use_complement)
    for (uint8_t& value : result) value ^= 1;
  return result;
}

std::vector<uint8_t> align_values(const std::vector<uint8_t>& values,
                                  const std::vector<int>& mapping) {
  SearchState index;
  std::vector<uint8_t> result(values.size(), 0);
  for (int left = 0; left < kOrder; ++left)
    for (int right = left + 1; right < kOrder; ++right)
      result[index.edge_for_pair(left, right)] =
          values[index.edge_for_pair(mapping[left], mapping[right])];
  return result;
}

int hamming(const std::vector<uint8_t>& left,
            const std::vector<uint8_t>& right) {
  if (left.size() != right.size())
    throw std::runtime_error("Hamming vectors have different lengths");
  int result = 0;
  for (size_t index = 0; index < left.size(); ++index)
    result += left[index] != right[index];
  return result;
}

int agreement_break_count(const std::vector<uint8_t>& values,
                          const std::vector<uint8_t>& parent_a,
                          const std::vector<uint8_t>& parent_b) {
  int result = 0;
  for (size_t edge = 0; edge < values.size(); ++edge)
    result += parent_a[edge] == parent_b[edge] &&
              values[edge] != parent_a[edge];
  return result;
}

int distance_delta(int edge, const std::vector<uint8_t>& values,
                   const std::vector<uint8_t>& parent) {
  return values[edge] == parent[edge] ? 1 : -1;
}

int agreement_delta(int edge, const std::vector<uint8_t>& values,
                    const std::vector<uint8_t>& parent_a,
                    const std::vector<uint8_t>& parent_b) {
  if (parent_a[edge] != parent_b[edge]) return 0;
  return values[edge] == parent_a[edge] ? 1 : -1;
}

void require_full_objective(const SearchState& state) {
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != cliques + independent)
    throw std::runtime_error(
        "incremental objective disagrees with full recomputation");
}

struct Midpoint {
  std::vector<uint8_t> values;
  int disagreement_count{};
  int source_distance{};
  int target_distance{};
  int sampled_delta_evaluations{};
};

Midpoint build_midpoint(const std::vector<uint8_t>& source,
                        const std::vector<uint8_t>& target,
                        const RelinkOptions& options,
                        std::mt19937_64& rng) {
  SearchState state;
  state.set_values(source);
  std::vector<int> remaining;
  for (int edge = 0; edge < static_cast<int>(source.size()); ++edge)
    if (source[edge] != target[edge]) remaining.push_back(edge);
  const int disagreement_count = remaining.size();
  const int flips_requested =
      std::min(options.path_flips, disagreement_count / 2);
  int delta_evaluations = 0;
  for (int path_step = 0; path_step < flips_requested; ++path_step) {
    std::vector<int> positions;
    if (static_cast<int>(remaining.size()) <= options.path_sample) {
      for (int position = 0;
           position < static_cast<int>(remaining.size()); ++position)
        positions.push_back(position);
    } else {
      std::set<int> seen;
      while (static_cast<int>(positions.size()) < options.path_sample) {
        const int position =
            static_cast<int>(rng() % remaining.size());
        if (seen.insert(position).second) positions.push_back(position);
      }
    }
    int selected_position = positions.front();
    int selected_edge = remaining[selected_position];
    int selected_delta = state.flip_delta(selected_edge);
    ++delta_evaluations;
    for (size_t index = 1; index < positions.size(); ++index) {
      const int position = positions[index];
      const int edge = remaining[position];
      const int delta = state.flip_delta(edge);
      ++delta_evaluations;
      if (std::pair<int, int>{delta, edge} <
          std::pair<int, int>{selected_delta, selected_edge}) {
        selected_position = position;
        selected_edge = edge;
        selected_delta = delta;
      }
    }
    state.flip(selected_edge);
    remaining[selected_position] = remaining.back();
    remaining.pop_back();
  }
  require_full_objective(state);
  return {
      state.values(),
      disagreement_count,
      hamming(state.values(), source),
      hamming(state.values(), target),
      delta_evaluations,
  };
}

int run_relink_self_check(const RelinkOptions& options,
                          const std::vector<uint8_t>& parent_a,
                          const std::vector<uint8_t>& parent_b) {
  const auto started = Clock::now();
  SearchState parent_state;
  parent_state.set_values(parent_a);
  require_full_objective(parent_state);
  const int parent_a_objective = parent_state.objective();
  parent_state.set_values(parent_b);
  require_full_objective(parent_state);
  const int parent_b_objective = parent_state.objective();
  std::mt19937_64 rng(options.seed);
  const std::vector<uint8_t>& source =
      options.direction == "a_to_b" ? parent_a : parent_b;
  const std::vector<uint8_t>& target =
      options.direction == "a_to_b" ? parent_b : parent_a;
  const Midpoint midpoint =
      build_midpoint(source, target, options, rng);
  if (midpoint.source_distance + midpoint.target_distance !=
          midpoint.disagreement_count ||
      midpoint.source_distance !=
          std::min(options.path_flips, midpoint.disagreement_count / 2) ||
      agreement_break_count(midpoint.values, parent_a, parent_b) != 0)
    throw std::runtime_error("midpoint path invariant failed");

  SearchState state;
  state.set_values(midpoint.values);
  const std::string midpoint_graph6 = state.graph6();
  std::vector<uint32_t> weights(state.subset_count());
  for (size_t subset = 0; subset < weights.size(); ++subset)
    weights[subset] =
        1 + static_cast<uint32_t>(
                (subset * uint64_t{11400714819323198485ull} + options.seed) %
                29);
  int checks = 0;
  for (int trial = 0; trial < options.self_check_moves; ++trial) {
    const int edge = static_cast<int>(rng() % state.values().size());
    const int before = state.objective();
    const long long weighted_before =
        state.full_weighted_objective(weights);
    const int predicted = state.flip_delta(edge);
    const long long weighted_predicted =
        state.weighted_flip_delta(edge, weights);
    state.flip(edge);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + predicted ||
        state.objective() != cliques + independent ||
        state.full_weighted_objective(weights) !=
            weighted_before + weighted_predicted)
      throw std::runtime_error("path-relink exact delta check failed");
    state.flip(edge);
    if (state.graph6() != midpoint_graph6)
      throw std::runtime_error("path-relink rollback check failed");
    ++checks;
  }
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"self_check\","
            << "\"algorithm\":\"aligned_path_relink_minconflicts_v1\","
            << "\"seed\":" << options.seed << ','
            << "\"parent_a_E\":" << parent_a_objective << ','
            << "\"parent_b_E\":" << parent_b_objective << ','
            << "\"parent_disagreement\":" << midpoint.disagreement_count << ','
            << "\"path_flips_requested\":" << options.path_flips << ','
            << "\"child_source_distance\":" << midpoint.source_distance
            << ','
            << "\"child_target_distance\":" << midpoint.target_distance
            << ','
            << "\"child_agreement_breaks\":0,"
            << "\"move_delta_full_recomputation_checks\":" << checks << ','
            << "\"weighted_delta_checks\":true,"
            << "\"rollback_checks\":true,"
            << "\"status\":\"PASS\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

int run_relink_search(const RelinkOptions& options,
                      const std::vector<uint8_t>& parent_a,
                      const std::vector<uint8_t>& parent_b) {
  const auto started = Clock::now();
  SearchState parent_state;
  parent_state.set_values(parent_a);
  require_full_objective(parent_state);
  const auto [parent_a_cliques, parent_a_independent] =
      parent_state.full_counts();
  parent_state.set_values(parent_b);
  require_full_objective(parent_state);
  const auto [parent_b_cliques, parent_b_independent] =
      parent_state.full_counts();

  std::mt19937_64 rng(options.seed);
  const std::vector<uint8_t>& source =
      options.direction == "a_to_b" ? parent_a : parent_b;
  const std::vector<uint8_t>& target =
      options.direction == "a_to_b" ? parent_b : parent_a;
  const Midpoint midpoint =
      build_midpoint(source, target, options, rng);
  SearchState state;
  state.set_values(midpoint.values);
  require_full_objective(state);
  const auto [midpoint_cliques, midpoint_independent] = state.full_counts();
  const int midpoint_objective = state.objective();
  const int midpoint_distance_a = hamming(midpoint.values, parent_a);
  const int midpoint_distance_b = hamming(midpoint.values, parent_b);
  const int midpoint_agreement_breaks =
      agreement_break_count(midpoint.values, parent_a, parent_b);
  if (midpoint.source_distance + midpoint.target_distance !=
          midpoint.disagreement_count ||
      midpoint.source_distance !=
          std::min(options.path_flips, midpoint.disagreement_count / 2) ||
      midpoint_agreement_breaks != 0)
    throw std::runtime_error("retained midpoint violates path invariants");
  write_graph6(options.child_output, state.graph6());

  int global_best = midpoint_objective;
  int global_distance_a = midpoint_distance_a;
  int global_distance_b = midpoint_distance_b;
  int global_agreement_breaks = midpoint_agreement_breaks;
  std::vector<uint8_t> global_values = state.values();
  std::vector<RelinkImprovement> improvements;
  std::vector<uint32_t> weights(state.subset_count(), 1);
  std::vector<long long> tabu_until(state.values().size(), 0);
  std::vector<uint8_t> all_edges(state.values().size(), 1);
  long long completed_steps = 0;
  long long delta_evaluations = midpoint.sampled_delta_evaluations;
  long long penalty_updates = 0;
  long long full_audits = 1;
  long long last_strict_step = 0;
  long long last_breakout = 0;
  int equal_best_updates = 0;

  auto retain = [&](long long step) {
    const int objective = state.objective();
    const int distance_a = hamming(state.values(), parent_a);
    const int distance_b = hamming(state.values(), parent_b);
    const int breaks =
        agreement_break_count(state.values(), parent_a, parent_b);
    if (objective < global_best) {
      require_full_objective(state);
      ++full_audits;
      global_best = objective;
      global_distance_a = distance_a;
      global_distance_b = distance_b;
      global_agreement_breaks = breaks;
      global_values = state.values();
      const auto [cliques, independent] = state.full_counts();
      improvements.push_back({
          static_cast<int>(improvements.size()) + 1,
          step,
          objective,
          cliques,
          independent,
          distance_a,
          distance_b,
          breaks,
      });
      std::cerr << "best step=" << step << " E=" << objective << '\n';
      if (objective == 0) write_graph6(options.output, state.graph6());
    } else if (objective == global_best) {
      const auto old_key =
          std::tuple<int, int, int>{
              global_agreement_breaks,
              -std::min(global_distance_a, global_distance_b),
              std::abs(global_distance_a - global_distance_b),
          };
      const auto new_key =
          std::tuple<int, int, int>{
              breaks,
              -std::min(distance_a, distance_b),
              std::abs(distance_a - distance_b),
          };
      if (new_key < old_key) {
        global_distance_a = distance_a;
        global_distance_b = distance_b;
        global_agreement_breaks = breaks;
        global_values = state.values();
        ++equal_best_updates;
      }
    }
  };

  if (global_best == 0) write_graph6(options.output, state.graph6());
  for (long long step = 0;
       step < options.steps && state.objective() > 0 && global_best > 0;
       ++step) {
    const int before_best = global_best;
    const std::vector<int> candidates =
        state.free_edges_of_random_bad(all_edges, rng);
    std::vector<int> allowed;
    for (int edge : candidates) {
      const bool aspiration =
          state.objective() + state.flip_delta(edge) < global_best;
      ++delta_evaluations;
      if (tabu_until[edge] <= step || aspiration) allowed.push_back(edge);
    }
    if (allowed.empty()) allowed = candidates;

    int selected = allowed[static_cast<size_t>(rng() % allowed.size())];
    if (static_cast<int>(rng() % 1000000) >=
        options.random_walk_per_million) {
      auto score = [&](int edge) {
        const long long weighted_delta =
            state.weighted_flip_delta(edge, weights);
        const int delta_a =
            distance_delta(edge, state.values(), parent_a);
        const int delta_b =
            distance_delta(edge, state.values(), parent_b);
        const int current_a = hamming(state.values(), parent_a);
        const int current_b = hamming(state.values(), parent_b);
        const int corridor_delta =
            std::abs(current_a + delta_a - current_b - delta_b) -
            std::abs(current_a - current_b);
        const int breaks_delta =
            agreement_delta(edge, state.values(), parent_a, parent_b);
        return std::tuple<long long, int, int>{
            weighted_delta * 1000 +
                static_cast<long long>(options.agreement_penalty) *
                    breaks_delta +
                static_cast<long long>(options.corridor_penalty) *
                    corridor_delta,
            state.flip_delta(edge),
            edge,
        };
      };
      auto selected_score = score(selected);
      for (int edge : allowed) {
        const auto candidate_score = score(edge);
        if (candidate_score < selected_score) {
          selected = edge;
          selected_score = candidate_score;
        }
      }
    }

    state.flip(selected);
    tabu_until[selected] = step + options.tabu_tenure + 1;
    ++completed_steps;
    retain(step + 1);
    if (global_best < before_best) last_strict_step = step + 1;
    if (global_best == 0) break;

    if (options.breakout_interval > 0 &&
        step + 1 - last_strict_step >= options.breakout_interval &&
        step + 1 - last_breakout >= options.breakout_interval) {
      state.increment_bad_weights(weights);
      ++penalty_updates;
      last_breakout = step + 1;
    }
    if (completed_steps % options.full_audit_interval == 0) {
      require_full_objective(state);
      ++full_audits;
    }
  }

  state.set_values(global_values);
  require_full_objective(state);
  ++full_audits;
  const auto [cliques, independent] = state.full_counts();
  if (state.objective() != global_best ||
      hamming(state.values(), parent_a) != global_distance_a ||
      hamming(state.values(), parent_b) != global_distance_b ||
      agreement_break_count(state.values(), parent_a, parent_b) !=
          global_agreement_breaks)
    throw std::runtime_error("retained path-relink state is inconsistent");
  write_graph6(options.output, state.graph6());

  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::ostringstream output;
  output << std::fixed << std::setprecision(6)
         << "{\"mode\":\"search\","
         << "\"algorithm\":\"aligned_path_relink_minconflicts_v1\","
         << "\"seed\":" << options.seed << ','
         << "\"direction\":" << json_quote(options.direction) << ','
         << "\"parent_a\":" << json_quote(options.parent_a) << ','
         << "\"parent_b\":" << json_quote(options.parent_b) << ','
         << "\"complement_a\":"
         << (options.complement_a ? "true" : "false") << ','
         << "\"complement_b\":"
         << (options.complement_b ? "true" : "false") << ','
         << "\"mapping\":[";
  for (size_t index = 0; index < options.mapping.size(); ++index) {
    if (index) output << ',';
    output << options.mapping[index];
  }
  output << "],\"parent_a_C5\":" << parent_a_cliques << ','
         << "\"parent_a_I5\":" << parent_a_independent << ','
         << "\"parent_a_E\":" << parent_a_cliques + parent_a_independent
         << ','
         << "\"parent_b_C5\":" << parent_b_cliques << ','
         << "\"parent_b_I5\":" << parent_b_independent << ','
         << "\"parent_b_E\":" << parent_b_cliques + parent_b_independent
         << ','
         << "\"parent_disagreement\":" << midpoint.disagreement_count << ','
         << "\"path_sample\":" << options.path_sample << ','
         << "\"path_flips_requested\":" << options.path_flips << ','
         << "\"child_C5\":" << midpoint_cliques << ','
         << "\"child_I5\":" << midpoint_independent << ','
         << "\"child_E\":" << midpoint_objective << ','
         << "\"child_distance_a\":" << midpoint_distance_a << ','
         << "\"child_distance_b\":" << midpoint_distance_b << ','
         << "\"child_agreement_breaks\":"
         << midpoint_agreement_breaks << ','
         << "\"child_graph6\":" << json_quote(
                [&]() {
                  SearchState midpoint_state;
                  midpoint_state.set_values(midpoint.values);
                  return midpoint_state.graph6();
                }())
         << ','
         << "\"child_output\":" << json_quote(options.child_output)
         << ','
         << "\"steps_requested\":" << options.steps << ','
         << "\"steps_executed\":" << completed_steps << ','
         << "\"tabu_tenure\":" << options.tabu_tenure << ','
         << "\"random_walk_per_million\":"
         << options.random_walk_per_million << ','
         << "\"breakout_interval\":" << options.breakout_interval << ','
         << "\"agreement_penalty\":" << options.agreement_penalty << ','
         << "\"corridor_penalty\":" << options.corridor_penalty << ','
         << "\"delta_evaluations\":" << delta_evaluations << ','
         << "\"penalty_updates\":" << penalty_updates << ','
         << "\"full_incremental_objective_audits\":" << full_audits << ','
         << "\"strict_improvements\":" << improvements.size() << ','
         << "\"equal_best_updates\":" << equal_best_updates << ','
         << "\"C5\":" << cliques << ','
         << "\"I5\":" << independent << ','
         << "\"E\":" << global_best << ','
         << "\"distance_a\":" << global_distance_a << ','
         << "\"distance_b\":" << global_distance_b << ','
         << "\"agreement_breaks\":" << global_agreement_breaks << ','
         << "\"edge_count\":" << state.edge_count() << ','
         << "\"stopped_on_E0\":" << (global_best == 0 ? "true" : "false")
         << ",\"degree_sequence\":[";
  const std::vector<int> degrees = state.sorted_degrees();
  for (size_t index = 0; index < degrees.size(); ++index) {
    if (index) output << ',';
    output << degrees[index];
  }
  output << "],\"graph6\":" << json_quote(state.graph6()) << ','
         << "\"output\":" << json_quote(options.output)
         << ",\"improvements\":[";
  for (size_t index = 0; index < improvements.size(); ++index) {
    if (index) output << ',';
    const RelinkImprovement& item = improvements[index];
    output << "{\"ordinal\":" << item.ordinal << ','
           << "\"step\":" << item.step << ','
           << "\"E\":" << item.objective << ','
           << "\"C5\":" << item.cliques << ','
           << "\"I5\":" << item.independent << ','
           << "\"distance_a\":" << item.distance_a << ','
           << "\"distance_b\":" << item.distance_b << ','
           << "\"agreement_breaks\":" << item.agreement_breaks << '}';
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
    const RelinkOptions options = parse_relink_options(argc, argv);
    const GraphSeed graph_a =
        decode_graph6(first_data_line(options.parent_a));
    const GraphSeed graph_b =
        decode_graph6(first_data_line(options.parent_b));
    const std::vector<uint8_t> parent_a =
        oriented_values(graph_a, options.complement_a);
    const std::vector<uint8_t> parent_b = align_values(
        oriented_values(graph_b, options.complement_b), options.mapping);
    if (options.self_check)
      return run_relink_self_check(options, parent_a, parent_b);
    return run_relink_search(options, parent_a, parent_b);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
