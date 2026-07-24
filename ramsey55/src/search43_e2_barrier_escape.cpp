// In-memory barrier-crossing search from the two-conflict neutral cycles.
//
// Every move and objective update is exact.  For an edge uv, the change in
// the number of forbidden 5-sets is computed from triangle counts in the
// common-neighbor and common-nonneighbor graphs.  The search first enumerates
// an E=2 neutral cycle exactly, then deliberately takes a shared-core edge
// whose flip worsens E before running a short tabu repair excursion.  Reaching
// an E=2 state outside all known neutral cycles discovers a new component;
// reaching E=0 prints the graph6 construction and stops immediately.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kOrder = 43;
constexpr int kEdgeCount = kOrder * (kOrder - 1) / 2;
constexpr uint64_t kVertexMask = (uint64_t{1} << kOrder) - 1;
using Clock = std::chrono::steady_clock;

struct Edge {
  int left = -1;
  int right = -1;

  bool operator==(const Edge&) const = default;
  bool operator<(const Edge& other) const {
    return std::pair{left, right} < std::pair{other.left, other.right};
  }
};

struct Graph {
  std::array<uint64_t, kOrder> adjacency{};
};

struct Conflict {
  bool clique{};
  std::array<int, 5> vertices{};
};

struct CycleState {
  Graph graph;
  std::vector<Conflict> conflicts;
  std::array<int, 4> core{};
  std::vector<std::pair<Edge, int>> barriers;
};

struct Component {
  std::string canonical_graph6;
  std::string source;
  std::vector<CycleState> states;
};

struct Options {
  std::vector<std::string> seed_graphs;
  uint64_t seed = 20261231;
  int rollouts_per_barrier = 1;
  int steps_per_rollout = 160;
  int tabu_tenure = 11;
  int noise_per_million = 90000;
  int objective_ceiling = 80;
  int component_limit = 256;
  int progress_interval = 500;
  int atomic_pair_retain = 8;
  int closure_state_limit = 250000;
  bool atomic_scan = false;
  bool self_check = false;
  int self_check_flips = 200;
};

std::array<std::array<int, kOrder>, kOrder> edge_index{};
std::array<Edge, kEdgeCount> indexed_edge{};

void initialize_edges() {
  int index = 0;
  for (int left = 0; left < kOrder; ++left) {
    for (int right = left + 1; right < kOrder; ++right) {
      edge_index[left][right] = edge_index[right][left] = index;
      indexed_edge[index] = {left, right};
      ++index;
    }
  }
  if (index != kEdgeCount) throw std::runtime_error("bad edge indexing");
}

std::string first_data_line(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph: " + path);
  std::string line;
  while (std::getline(input, line)) {
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n'))
      line.pop_back();
    if (!line.empty() && line[0] != '#') return line;
  }
  throw std::runtime_error("graph has no data line: " + path);
}

Graph decode_graph6(std::string line) {
  if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
  if (line.empty() ||
      static_cast<unsigned char>(line.front()) - 63 != kOrder)
    throw std::runtime_error("expected a short graph6 graph of order 43");
  Graph graph;
  int bit = 0;
  for (int right = 1; right < kOrder; ++right) {
    for (int left = 0; left < right; ++left) {
      if (1 + bit / 6 >= static_cast<int>(line.size()))
        throw std::runtime_error("truncated graph6 input");
      const int value =
          static_cast<unsigned char>(line[1 + bit / 6]) - 63;
      if (!(0 <= value && value < 64))
        throw std::runtime_error("invalid graph6 byte");
      if ((value >> (5 - bit % 6)) & 1) {
        graph.adjacency[left] |= uint64_t{1} << right;
        graph.adjacency[right] |= uint64_t{1} << left;
      }
      ++bit;
    }
  }
  return graph;
}

std::string graph6(const Graph& graph) {
  std::string bits;
  bits.reserve(kEdgeCount + 5);
  for (int right = 1; right < kOrder; ++right)
    for (int left = 0; left < right; ++left)
      bits.push_back((graph.adjacency[left] >> right) & 1);
  while (bits.size() % 6) bits.push_back(0);
  std::string result(1, static_cast<char>(kOrder + 63));
  for (size_t start = 0; start < bits.size(); start += 6) {
    int value = 0;
    for (int offset = 0; offset < 6; ++offset)
      value = (value << 1) | bits[start + offset];
    result.push_back(static_cast<char>(value + 63));
  }
  return result;
}

bool edge_value(const Graph& graph, Edge edge) {
  return (graph.adjacency[edge.left] >> edge.right) & 1;
}

void flip(Graph& graph, Edge edge) {
  graph.adjacency[edge.left] ^= uint64_t{1} << edge.right;
  graph.adjacency[edge.right] ^= uint64_t{1} << edge.left;
}

uint64_t neighbors(const Graph& graph, int vertex, bool complement) {
  if (!complement) return graph.adjacency[vertex];
  return kVertexMask &
         ~(graph.adjacency[vertex] | (uint64_t{1} << vertex));
}

int triangle_count(const Graph& graph, uint64_t vertices, bool complement) {
  int result = 0;
  uint64_t remaining_a = vertices;
  while (remaining_a) {
    const int a = __builtin_ctzll(remaining_a);
    remaining_a &= remaining_a - 1;
    const uint64_t neighbors_a =
        neighbors(graph, a, complement) & remaining_a;
    uint64_t remaining_b = neighbors_a;
    while (remaining_b) {
      const int b = __builtin_ctzll(remaining_b);
      remaining_b &= remaining_b - 1;
      const uint64_t after_b =
          remaining_a & ~((uint64_t{1} << (b + 1)) - 1);
      result += __builtin_popcountll(
          neighbors_a & neighbors(graph, b, complement) & after_b);
    }
  }
  return result;
}

// Exact objective change from toggling one edge.
int flip_delta(const Graph& graph, Edge edge) {
  const int left = edge.left;
  const int right = edge.right;
  const uint64_t excluded =
      ~((uint64_t{1} << left) | (uint64_t{1} << right));
  const uint64_t common_neighbors =
      graph.adjacency[left] & graph.adjacency[right] & excluded;
  const uint64_t common_nonneighbors =
      neighbors(graph, left, true) & neighbors(graph, right, true) & excluded;
  const int cliques = triangle_count(graph, common_neighbors, false);
  const int independent =
      triangle_count(graph, common_nonneighbors, true);
  return edge_value(graph, edge) ? independent - cliques
                                 : cliques - independent;
}

void enumerate_cliques(const Graph& graph, uint64_t candidates,
                       bool complement, int depth,
                       std::array<int, 5>& selected,
                       std::vector<Conflict>& output) {
  const int needed = 5 - depth;
  if (__builtin_popcountll(candidates) < needed) return;
  if (depth == 5) {
    output.push_back({!complement, selected});
    return;
  }
  while (candidates) {
    if (__builtin_popcountll(candidates) < needed) return;
    const int vertex = __builtin_ctzll(candidates);
    candidates &= candidates - 1;
    selected[depth] = vertex;
    enumerate_cliques(
        graph, candidates & neighbors(graph, vertex, complement),
        complement, depth + 1, selected, output);
  }
}

std::vector<Conflict> all_conflicts(const Graph& graph) {
  std::vector<Conflict> result;
  std::array<int, 5> selected{};
  enumerate_cliques(graph, kVertexMask, false, 0, selected, result);
  enumerate_cliques(graph, kVertexMask, true, 0, selected, result);
  return result;
}

std::array<int, 4> shared_core(const std::vector<Conflict>& conflicts) {
  if (conflicts.size() != 2 ||
      conflicts[0].clique != conflicts[1].clique)
    throw std::runtime_error("E=2 state lacks a same-color conflict pair");
  std::array<int, 4> core{};
  int count = 0;
  for (int left : conflicts[0].vertices) {
    if (std::find(conflicts[1].vertices.begin(),
                  conflicts[1].vertices.end(),
                  left) != conflicts[1].vertices.end()) {
      if (count >= 4)
        throw std::runtime_error("conflict pair intersects in more than four");
      core[count++] = left;
    }
  }
  if (count != 4)
    throw std::runtime_error("E=2 conflict pair does not intersect in four");
  std::sort(core.begin(), core.end());
  return core;
}

std::vector<Edge> core_edges(const std::array<int, 4>& core) {
  std::vector<Edge> result;
  for (int left = 0; left < 4; ++left)
    for (int right = left + 1; right < 4; ++right)
      result.push_back({core[left], core[right]});
  return result;
}

int degree_penalty(const Graph& graph) {
  int result = 0;
  for (uint64_t row : graph.adjacency) {
    const int degree = __builtin_popcountll(row);
    if (degree < 18) result += (18 - degree) * (18 - degree);
    if (degree > 24) result += (degree - 24) * (degree - 24);
  }
  return result;
}

CycleState inspect_cycle_state(const Graph& graph) {
  CycleState result;
  result.graph = graph;
  result.conflicts = all_conflicts(graph);
  if (result.conflicts.size() != 2)
    throw std::runtime_error("cycle state objective is not two");
  result.core = shared_core(result.conflicts);
  for (Edge edge : core_edges(result.core)) {
    const int after = 2 + flip_delta(graph, edge);
    if (after > 2) result.barriers.push_back({edge, after});
  }
  std::sort(result.barriers.begin(), result.barriers.end(),
            [](const auto& left, const auto& right) {
              return std::pair{left.second, left.first} <
                     std::pair{right.second, right.first};
            });
  return result;
}

std::vector<Edge> neutral_edges(const CycleState& state) {
  std::vector<Edge> result;
  for (Edge edge : core_edges(state.core))
    if (2 + flip_delta(state.graph, edge) == 2) result.push_back(edge);
  return result;
}

Component build_component(const Graph& start, const std::string& source) {
  Component component;
  component.source = source;
  Graph current = start;
  Edge previous;
  bool first = true;
  std::unordered_map<std::string, int> seen;
  while (true) {
    const std::string code = graph6(current);
    const auto old = seen.find(code);
    if (old != seen.end()) {
      if (old->second != 0)
        throw std::runtime_error("neutral walk entered a noninitial cycle");
      break;
    }
    if (component.states.size() >= 10000)
      throw std::runtime_error("neutral component exceeded 10,000 states");
    seen.emplace(code, static_cast<int>(component.states.size()));
    CycleState state = inspect_cycle_state(current);
    std::vector<Edge> neutral = neutral_edges(state);
    if (neutral.size() != 2)
      throw std::runtime_error("neutral E=2 state does not have degree two");
    Edge next;
    if (first) {
      next = neutral.front();
      first = false;
    } else if (neutral[0] == previous) {
      next = neutral[1];
    } else if (neutral[1] == previous) {
      next = neutral[0];
    } else {
      throw std::runtime_error("neutral cycle lost its reverse edge");
    }
    component.states.push_back(std::move(state));
    flip(current, next);
    if (2 + flip_delta(component.states.back().graph, next) != 2)
      throw std::runtime_error("neutral transition objective mismatch");
    previous = next;
  }
  component.canonical_graph6 = seen.empty()
                                   ? graph6(start)
                                   : std::min_element(
                                         seen.begin(), seen.end(),
                                         [](const auto& left,
                                            const auto& right) {
                                           return left.first < right.first;
                                         })
                                         ->first;
  return component;
}

std::vector<Edge> conflict_edges(const Conflict& conflict) {
  std::vector<Edge> result;
  for (int left = 0; left < 5; ++left)
    for (int right = left + 1; right < 5; ++right)
      result.push_back(
          {conflict.vertices[left], conflict.vertices[right]});
  return result;
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto value = [&]() -> std::string {
      if (index + 1 >= argc)
        throw std::runtime_error("missing value for " + option);
      return argv[++index];
    };
    if (option == "--seed-graph")
      options.seed_graphs.push_back(value());
    else if (option == "--seed")
      options.seed = std::stoull(value());
    else if (option == "--rollouts-per-barrier")
      options.rollouts_per_barrier = std::stoi(value());
    else if (option == "--steps")
      options.steps_per_rollout = std::stoi(value());
    else if (option == "--tabu")
      options.tabu_tenure = std::stoi(value());
    else if (option == "--noise-per-million")
      options.noise_per_million = std::stoi(value());
    else if (option == "--objective-ceiling")
      options.objective_ceiling = std::stoi(value());
    else if (option == "--component-limit")
      options.component_limit = std::stoi(value());
    else if (option == "--progress-interval")
      options.progress_interval = std::stoi(value());
    else if (option == "--atomic-pair-retain")
      options.atomic_pair_retain = std::stoi(value());
    else if (option == "--closure-state-limit")
      options.closure_state_limit = std::stoi(value());
    else if (option == "--atomic-scan")
      options.atomic_scan = true;
    else if (option == "--self-check-flips")
      options.self_check_flips = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.seed_graphs.empty())
    throw std::runtime_error("at least one --seed-graph is required");
  if (options.rollouts_per_barrier < 1 ||
      options.steps_per_rollout < 1 || options.tabu_tenure < 0 ||
      options.noise_per_million < 0 ||
      options.noise_per_million > 1000000 ||
      options.objective_ceiling < 2 || options.component_limit < 1 ||
      options.progress_interval < 0 || options.atomic_pair_retain < 0 ||
      options.closure_state_limit < 1 ||
      options.self_check_flips < 0)
    throw std::runtime_error("invalid nonnegative search option");
  return options;
}

int run_self_check(const Options& options) {
  Graph graph = decode_graph6(first_data_line(options.seed_graphs.front()));
  std::mt19937_64 rng(options.seed);
  int exhaustive_checks = 0;
  for (int edge = 0; edge < kEdgeCount; ++edge) {
    const int before = static_cast<int>(all_conflicts(graph).size());
    const int delta = flip_delta(graph, indexed_edge[edge]);
    flip(graph, indexed_edge[edge]);
    const int after = static_cast<int>(all_conflicts(graph).size());
    if (after != before + delta)
      throw std::runtime_error("exhaustive base delta check failed");
    flip(graph, indexed_edge[edge]);
    ++exhaustive_checks;
  }
  for (int trial = 0; trial < options.self_check_flips; ++trial) {
    const Edge edge = indexed_edge[rng() % kEdgeCount];
    const int before = static_cast<int>(all_conflicts(graph).size());
    const int delta = flip_delta(graph, edge);
    flip(graph, edge);
    const int after = static_cast<int>(all_conflicts(graph).size());
    if (after != before + delta)
      throw std::runtime_error("random-sequence delta check failed");
  }
  std::cout
      << "{\"mode\":\"self_check\","
      << "\"algorithm\":\"e2_neutral_cycle_barrier_escape_v1\","
      << "\"exhaustive_base_edge_delta_checks\":" << exhaustive_checks << ','
      << "\"random_sequence_delta_checks\":" << options.self_check_flips << ','
      << "\"status\":\"PASS\"}\n";
  return 0;
}

struct SearchCounters {
  long long rollouts{};
  long long steps{};
  long long absorbed_known_cycle{};
  long long known_cycle_visits{};
  long long repeated_barrier_crossings{};
  long long exhausted{};
  long long ceiling_rejections{};
  long long exact_objective_checks{};
  long long e1_visits{};
  long long new_components{};
  int best_objective = std::numeric_limits<int>::max();
  int maximum_objective{};
  std::map<int, long long> barriers_by_height;
  std::map<int, long long> terminal_best_distribution;
};

struct RolloutResult {
  enum Kind { kAbsorbed, kExhausted, kNewE2, kConstruction } kind;
  Graph graph;
  int best{};
  int steps{};
};

RolloutResult rollout(
    Graph graph, int objective, Edge forced_edge, const Options& options,
    std::mt19937_64& rng,
    const std::unordered_map<std::string, int>& known_states,
    const std::unordered_map<std::string,
                             std::vector<std::pair<Edge, int>>>&
        known_barriers,
    SearchCounters& counters) {
  std::array<long long, kEdgeCount> tabu{};
  tabu[edge_index[forced_edge.left][forced_edge.right]] =
      options.tabu_tenure + 1;
  int best = objective;
  int stagnation = 0;
  counters.maximum_objective =
      std::max(counters.maximum_objective, objective);

  for (int step = 0; step < options.steps_per_rollout; ++step) {
    std::vector<Conflict> conflicts = all_conflicts(graph);
    ++counters.exact_objective_checks;
    if (static_cast<int>(conflicts.size()) != objective)
      throw std::runtime_error("incremental objective mismatch in rollout");
    if (objective == 0)
      return {RolloutResult::kConstruction, graph, 0, step};
    if (objective == 1) ++counters.e1_visits;
    if (objective == 2) {
      const std::string code = graph6(graph);
      if (known_states.contains(code)) {
        ++counters.known_cycle_visits;
        const auto barrier_record = known_barriers.find(code);
        if (barrier_record == known_barriers.end())
          throw std::runtime_error("known cycle state lacks barriers");
        std::vector<std::pair<Edge, int>> available;
        for (const auto& item : barrier_record->second) {
          const int index = edge_index[item.first.left][item.first.right];
          if (item.second <= options.objective_ceiling &&
              tabu[index] <= step)
            available.push_back(item);
        }
        if (available.empty()) {
          for (const auto& item : barrier_record->second)
            if (item.second <= options.objective_ceiling)
              available.push_back(item);
        }
        if (available.empty())
          return {RolloutResult::kAbsorbed, graph, best, step};
        const auto& [barrier, expected_height] =
            available[rng() % available.size()];
        const int exact_height = objective + flip_delta(graph, barrier);
        if (exact_height != expected_height)
          throw std::runtime_error("repeated barrier height mismatch");
        flip(graph, barrier);
        objective = exact_height;
        tabu[edge_index[barrier.left][barrier.right]] =
            step + options.tabu_tenure + 1;
        counters.maximum_objective =
            std::max(counters.maximum_objective, objective);
        ++counters.repeated_barrier_crossings;
        continue;
      }
      try {
        (void)shared_core(conflicts);
      } catch (const std::runtime_error&) {
        // It is still a genuinely new E=2 state; return it to the caller,
        // which records that it is not a degree-two neutral-cycle seed.
      }
      return {RolloutResult::kNewE2, graph, best, step};
    }

    const Conflict& selected = conflicts[rng() % conflicts.size()];
    const std::vector<Edge> candidates = conflict_edges(selected);
    struct Choice {
      Edge edge;
      int delta{};
      int penalty{};
      bool tabu{};
    };
    std::vector<Choice> choices;
    choices.reserve(10);
    for (Edge edge : candidates) {
      const int delta = flip_delta(graph, edge);
      const int after = objective + delta;
      if (after > options.objective_ceiling) {
        ++counters.ceiling_rejections;
        continue;
      }
      Graph changed = graph;
      flip(changed, edge);
      const bool is_tabu =
          tabu[edge_index[edge.left][edge.right]] > step;
      choices.push_back({edge, delta, degree_penalty(changed), is_tabu});
    }
    if (choices.empty())
      return {RolloutResult::kExhausted, graph, best, step};

    std::vector<int> allowed;
    for (int index = 0; index < static_cast<int>(choices.size()); ++index) {
      const bool aspiration = objective + choices[index].delta < best;
      if (!choices[index].tabu || aspiration) allowed.push_back(index);
    }
    if (allowed.empty())
      for (int index = 0; index < static_cast<int>(choices.size()); ++index)
        allowed.push_back(index);

    int chosen = allowed.front();
    if (static_cast<int>(rng() % 1000000) <
        options.noise_per_million) {
      chosen = allowed[rng() % allowed.size()];
    } else {
      for (int index : allowed) {
        const auto score =
            std::tuple{choices[index].delta, choices[index].penalty,
                       static_cast<uint64_t>(rng())};
        const auto old_score =
            std::tuple{choices[chosen].delta, choices[chosen].penalty,
                       std::numeric_limits<uint64_t>::max()};
        if (score < old_score) chosen = index;
      }
    }
    flip(graph, choices[chosen].edge);
    objective += choices[chosen].delta;
    counters.maximum_objective =
        std::max(counters.maximum_objective, objective);
    tabu[edge_index[choices[chosen].edge.left]
                   [choices[chosen].edge.right]] =
        step + options.tabu_tenure + 1;
    if (objective < best) {
      best = objective;
      stagnation = 0;
    } else {
      ++stagnation;
    }

    // A deterministic local minimum is deliberately perturbed by making the
    // next choice noisy; the existing noise mechanism supplies that move.
    if (stagnation > 4 * options.tabu_tenure) stagnation = 0;
  }
  return {RolloutResult::kExhausted, graph, best,
          options.steps_per_rollout};
}

std::string json_quote(const std::string& value) {
  std::ostringstream output;
  output << '"';
  for (unsigned char character : value) {
    if (character == '"' || character == '\\')
      output << '\\' << character;
    else if (character >= 0x20 && character < 0x7f)
      output << character;
    else
      output << "\\u00" << std::hex << std::setw(2)
             << std::setfill('0') << static_cast<int>(character)
             << std::dec << std::setfill(' ');
  }
  output << '"';
  return output.str();
}

struct LowState {
  Graph graph;
  int objective{};
  std::vector<Conflict> conflicts;
};

int run_atomic_scan(
    const Options& options, const std::vector<Component>& components,
    const std::unordered_map<std::string, int>& known_states,
    const Clock::time_point started) {
  long long pair_checks = 0;
  long long pair_exact_replays = 0;
  long long triple_checks = 0;
  long long triple_exact_replays = 0;
  long long fourth_checks = 0;
  long long fourth_exact_replays = 0;
  long long fifth_checks = 0;
  long long fifth_exact_replays = 0;
  long long closure_checks = 0;
  long long closure_exact_replays = 0;
  long long closure_e1_hits = 0;
  long long closure_known_e2_hits = 0;
  std::map<int, long long> pair_raw_distribution;
  std::map<int, long long> pair_unique_distribution;
  std::map<int, long long> triple_raw_distribution;
  std::map<int, long long> triple_unique_distribution;
  std::map<int, long long> fourth_raw_distribution;
  std::map<int, long long> fourth_unique_distribution;
  std::map<int, long long> fifth_raw_distribution;
  std::map<int, long long> fifth_unique_distribution;
  std::map<int, long long> closure_state_distribution;
  std::unordered_set<std::string> pair_seen;
  std::unordered_set<std::string> triple_seen;
  std::unordered_set<std::string> fourth_seen;
  std::unordered_set<std::string> fifth_seen;
  std::unordered_set<std::string> offcycle_e2;
  std::vector<LowState> pair_low;
  std::vector<LowState> triple_low;
  std::vector<LowState> fourth_low;
  int minimum_pair_objective = std::numeric_limits<int>::max();
  int minimum_fourth_objective = std::numeric_limits<int>::max();

  for (const Component& component : components) {
    for (const CycleState& state : component.states) {
      for (const auto& [barrier, barrier_height] : state.barriers) {
        Graph once = state.graph;
        flip(once, barrier);
        for (int edge_number = 0; edge_number < kEdgeCount; ++edge_number) {
          const Edge second = indexed_edge[edge_number];
          if (second == barrier) continue;
          ++pair_checks;
          const int objective =
              barrier_height + flip_delta(once, second);
          minimum_pair_objective =
              std::min(minimum_pair_objective, objective);
          if (objective > options.atomic_pair_retain) continue;
          Graph twice = once;
          flip(twice, second);
          std::vector<Conflict> conflicts = all_conflicts(twice);
          ++pair_exact_replays;
          if (static_cast<int>(conflicts.size()) != objective)
            throw std::runtime_error("atomic-pair objective replay failed");
          ++pair_raw_distribution[objective];
          const std::string code = graph6(twice);
          if (pair_seen.insert(code).second) {
            ++pair_unique_distribution[objective];
            pair_low.push_back({twice, objective, std::move(conflicts)});
          }
          if (objective == 0) {
            std::cout
                << "{\"mode\":\"construction\","
                << "\"algorithm\":\"e2_atomic_barrier_pair_scan_v1\","
                << "\"graph6\":" << json_quote(code) << ','
                << "\"objective\":0,"
                << "\"pair_checks\":" << pair_checks << "}\n";
            return 10;
          }
          if (objective == 2 && !known_states.contains(code))
            offcycle_e2.insert(code);
        }
      }
    }
  }

  // A final improving flip must touch at least one current conflict.  Hence
  // the union of conflict edges is a complete target set for all triples
  // whose third flip lowers E from one of the retained E<=4 pair states.
  for (const LowState& pair : pair_low) {
    std::set<Edge> targeted;
    for (const Conflict& conflict : pair.conflicts)
      for (Edge edge : conflict_edges(conflict)) targeted.insert(edge);
    for (Edge third : targeted) {
      ++triple_checks;
      const int objective = pair.objective + flip_delta(pair.graph, third);
      if (objective > 4) continue;
      Graph graph = pair.graph;
      flip(graph, third);
      std::vector<Conflict> conflicts = all_conflicts(graph);
      ++triple_exact_replays;
      if (static_cast<int>(conflicts.size()) != objective)
        throw std::runtime_error("targeted-triple objective replay failed");
      ++triple_raw_distribution[objective];
      const std::string code = graph6(graph);
      if (triple_seen.insert(code).second) {
        ++triple_unique_distribution[objective];
        triple_low.push_back({graph, objective, std::move(conflicts)});
      }
      if (objective == 0) {
        std::cout
            << "{\"mode\":\"construction\","
            << "\"algorithm\":\"e2_atomic_barrier_triple_scan_v1\","
            << "\"graph6\":" << json_quote(code) << ','
            << "\"objective\":0,"
            << "\"pair_checks\":" << pair_checks << ','
            << "\"triple_checks\":" << triple_checks << "}\n";
        return 10;
      }
      if (objective == 2 && !known_states.contains(code))
        offcycle_e2.insert(code);
    }
  }
  pair_low.clear();
  pair_low.shrink_to_fit();
  pair_seen.clear();
  pair_seen.rehash(0);

  // One complete additional layer: from every unique retained triple state,
  // inspect every possible fourth edge, including objective-neutral edges
  // outside the current conflicts.
  for (const LowState& triple : triple_low) {
    for (int edge_number = 0; edge_number < kEdgeCount; ++edge_number) {
      const Edge fourth = indexed_edge[edge_number];
      ++fourth_checks;
      const int objective =
          triple.objective + flip_delta(triple.graph, fourth);
      minimum_fourth_objective =
          std::min(minimum_fourth_objective, objective);
      if (objective > 4) continue;
      Graph graph = triple.graph;
      flip(graph, fourth);
      std::vector<Conflict> conflicts = all_conflicts(graph);
      ++fourth_exact_replays;
      if (static_cast<int>(conflicts.size()) != objective)
        throw std::runtime_error("fourth-edge objective replay failed");
      ++fourth_raw_distribution[objective];
      const std::string code = graph6(graph);
      if (fourth_seen.insert(code).second) {
        ++fourth_unique_distribution[objective];
        if (objective >= 3)
          fourth_low.push_back({graph, objective, std::move(conflicts)});
      }
      if (objective == 0) {
        std::cout
            << "{\"mode\":\"construction\","
            << "\"algorithm\":\"e2_atomic_barrier_four_edge_scan_v1\","
            << "\"graph6\":" << json_quote(code) << ','
            << "\"objective\":0,"
            << "\"pair_checks\":" << pair_checks << ','
            << "\"triple_checks\":" << triple_checks << ','
            << "\"fourth_checks\":" << fourth_checks << "}\n";
        return 10;
      }
      if (objective == 2 && !known_states.contains(code))
        offcycle_e2.insert(code);
    }
  }

  // Targeted fifth flips from every unique E=3/E=4 fourth-layer state.
  // Any fifth flip that improves E must lie in this conflict-edge union.
  for (const LowState& fourth : fourth_low) {
    std::set<Edge> targeted;
    for (const Conflict& conflict : fourth.conflicts)
      for (Edge edge : conflict_edges(conflict)) targeted.insert(edge);
    for (Edge fifth : targeted) {
      ++fifth_checks;
      const int objective =
          fourth.objective + flip_delta(fourth.graph, fifth);
      if (objective > 4) continue;
      Graph graph = fourth.graph;
      flip(graph, fifth);
      std::vector<Conflict> conflicts = all_conflicts(graph);
      ++fifth_exact_replays;
      if (static_cast<int>(conflicts.size()) != objective)
        throw std::runtime_error("fifth-edge objective replay failed");
      ++fifth_raw_distribution[objective];
      const std::string code = graph6(graph);
      if (fifth_seen.insert(code).second)
        ++fifth_unique_distribution[objective];
      if (objective == 0) {
        std::cout
            << "{\"mode\":\"construction\","
            << "\"algorithm\":\"e2_atomic_barrier_five_edge_scan_v1\","
            << "\"graph6\":" << json_quote(code) << ','
            << "\"objective\":0,"
            << "\"pair_checks\":" << pair_checks << ','
            << "\"triple_checks\":" << triple_checks << ','
            << "\"fourth_checks\":" << fourth_checks << ','
            << "\"fifth_checks\":" << fifth_checks << "}\n";
        return 10;
      }
      if (objective == 2 && !known_states.contains(code))
        offcycle_e2.insert(code);
    }
  }
  triple_seen.clear();
  triple_seen.rehash(0);
  fourth_seen.clear();
  fourth_seen.rehash(0);
  fifth_seen.clear();
  fifth_seen.rehash(0);

  // Close the retained E=3/E=4 region under flips that touch a current
  // conflict and keep E<=4.  This is an exact targeted closure, with an
  // explicit state cap; it does not include unrelated zero-delta edges.
  std::unordered_set<std::string> closure_seen;
  std::vector<LowState> closure_queue;
  closure_seen.reserve(
      static_cast<size_t>(options.closure_state_limit));
  closure_queue.reserve(
      static_cast<size_t>(options.closure_state_limit));
  auto seed_closure = [&](std::vector<LowState>& values) {
    for (LowState& value : values) {
      const std::string code = graph6(value.graph);
      if (value.objective >= 3 && closure_seen.insert(code).second)
        closure_queue.push_back(std::move(value));
    }
    values.clear();
    values.shrink_to_fit();
  };
  seed_closure(triple_low);
  seed_closure(fourth_low);
  size_t closure_cursor = 0;
  bool closure_truncated = false;
  while (closure_cursor < closure_queue.size()) {
    if (static_cast<int>(closure_queue.size()) >=
        options.closure_state_limit) {
      closure_truncated = true;
      break;
    }
    const LowState current = closure_queue[closure_cursor++];
    std::set<Edge> targeted;
    for (const Conflict& conflict : current.conflicts)
      for (Edge edge : conflict_edges(conflict)) targeted.insert(edge);
    for (Edge edge : targeted) {
      ++closure_checks;
      const int objective =
          current.objective + flip_delta(current.graph, edge);
      if (objective > 4) continue;
      Graph graph = current.graph;
      flip(graph, edge);
      std::vector<Conflict> conflicts = all_conflicts(graph);
      ++closure_exact_replays;
      if (static_cast<int>(conflicts.size()) != objective)
        throw std::runtime_error("targeted-closure replay failed");
      const std::string code = graph6(graph);
      if (objective == 0) {
        std::cout
            << "{\"mode\":\"construction\","
            << "\"algorithm\":\"e2_targeted_low_closure_v1\","
            << "\"graph6\":" << json_quote(code) << ','
            << "\"objective\":0,"
            << "\"closure_checks\":" << closure_checks << "}\n";
        return 10;
      }
      if (objective == 1) ++closure_e1_hits;
      if (objective == 2) {
        if (!known_states.contains(code))
          offcycle_e2.insert(code);
        else
          ++closure_known_e2_hits;
      }
      if (objective >= 3 && closure_seen.insert(code).second) {
        if (static_cast<int>(closure_queue.size()) >=
            options.closure_state_limit) {
          closure_truncated = true;
          break;
        }
        closure_queue.push_back(
            {graph, objective, std::move(conflicts)});
      }
    }
    if (closure_truncated) break;
  }
  for (const LowState& state : closure_queue)
    ++closure_state_distribution[state.objective];

  auto integer_map = [](const auto& values) {
    std::ostringstream output;
    output << '{';
    bool first = true;
    for (const auto& [key, value] : values) {
      if (!first) output << ',';
      first = false;
      output << '"' << key << "\":" << value;
    }
    output << '}';
    return output.str();
  };
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"atomic_scan\","
            << "\"algorithm\":\"e2_atomic_barrier_pair_triple_scan_v1\","
            << "\"evidence_label\":\"REPRODUCIBLE COMPUTATIONAL "
               "OBSERVATION\","
            << "\"input_seed_count\":" << options.seed_graphs.size() << ','
            << "\"component_count\":" << components.size() << ','
            << "\"neutral_state_count\":" << known_states.size() << ','
            << "\"pair_checks\":" << pair_checks << ','
            << "\"pair_exact_replays\":" << pair_exact_replays << ','
            << "\"minimum_pair_objective\":" << minimum_pair_objective << ','
            << "\"pair_retain_ceiling\":"
            << options.atomic_pair_retain << ','
            << "\"pair_raw_retained_distribution\":"
            << integer_map(pair_raw_distribution) << ','
            << "\"pair_unique_retained_distribution\":"
            << integer_map(pair_unique_distribution) << ','
            << "\"triple_checks\":" << triple_checks << ','
            << "\"triple_exact_replays\":" << triple_exact_replays << ','
            << "\"triple_raw_E_le_4_distribution\":"
            << integer_map(triple_raw_distribution) << ','
            << "\"triple_unique_E_le_4_distribution\":"
            << integer_map(triple_unique_distribution) << ','
            << "\"fourth_checks\":" << fourth_checks << ','
            << "\"fourth_exact_replays\":" << fourth_exact_replays << ','
            << "\"minimum_fourth_objective\":"
            << (minimum_fourth_objective ==
                        std::numeric_limits<int>::max()
                    ? -1
                    : minimum_fourth_objective)
            << ','
            << "\"fourth_raw_E_le_4_distribution\":"
            << integer_map(fourth_raw_distribution) << ','
            << "\"fourth_unique_E_le_4_distribution\":"
            << integer_map(fourth_unique_distribution) << ','
            << "\"fifth_checks\":" << fifth_checks << ','
            << "\"fifth_exact_replays\":" << fifth_exact_replays << ','
            << "\"fifth_raw_E_le_4_distribution\":"
            << integer_map(fifth_raw_distribution) << ','
            << "\"fifth_unique_E_le_4_distribution\":"
            << integer_map(fifth_unique_distribution) << ','
            << "\"closure_checks\":" << closure_checks << ','
            << "\"closure_exact_replays\":" << closure_exact_replays << ','
            << "\"closure_E1_hits\":" << closure_e1_hits << ','
            << "\"closure_known_E2_hits\":"
            << closure_known_e2_hits << ','
            << "\"closure_state_limit\":"
            << options.closure_state_limit << ','
            << "\"closure_state_distribution\":"
            << integer_map(closure_state_distribution) << ','
            << "\"closure_complete\":"
            << (!closure_truncated &&
                        closure_cursor == closure_queue.size()
                    ? "true"
                    : "false")
            << ','
            << "\"offcycle_E2_count\":" << offcycle_e2.size() << ','
            << "\"E0_found\":false,"
            << "\"claim_boundary\":\"The pair scan is exhaustive only "
               "for two-flip paths whose first edge is one of the four "
               "shared-core worsening edges of the 1,892 audited cycle "
               "states. The targeted third-edge scan is exhaustive only "
               "over the conflict-edge union of pair states at or below "
               "the configured retention ceiling. The fourth-edge layer "
               "checks all 903 edges from each retained triple state. "
               "The fifth-edge layer checks the conflict-edge union of "
               "each unique E=3/E=4 fourth-layer state. "
               "The final closure uses only current-conflict edges and "
               "is complete only when closure_complete is true. "
               "Neither is a global nonexistence result.\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

int run_search(const Options& options) {
  const auto started = Clock::now();
  std::mt19937_64 rng(options.seed);
  std::vector<Component> components;
  std::unordered_set<std::string> component_keys;
  std::unordered_map<std::string, int> known_states;
  std::unordered_map<std::string, std::vector<std::pair<Edge, int>>>
      known_barriers;
  std::vector<std::string> noncycle_e2;

  auto add_component = [&](Component component) {
    if (component_keys.contains(component.canonical_graph6)) return false;
    const int index = static_cast<int>(components.size());
    component_keys.insert(component.canonical_graph6);
    for (const CycleState& state : component.states) {
      const std::string code = graph6(state.graph);
      known_states.emplace(code, index);
      known_barriers.emplace(code, state.barriers);
    }
    components.push_back(std::move(component));
    return true;
  };

  for (const std::string& path : options.seed_graphs) {
    Component component =
        build_component(decode_graph6(first_data_line(path)), path);
    add_component(std::move(component));
  }
  const int initial_components = components.size();
  const int initial_neutral_states = known_states.size();
  if (options.atomic_scan)
    return run_atomic_scan(options, components, known_states, started);
  SearchCounters counters;
  counters.best_objective = 2;

  for (size_t component_index = 0;
       component_index < components.size() &&
       static_cast<int>(component_index) < options.component_limit;
       ++component_index) {
    // Copy because discovering a component can reallocate the outer vector.
    const Component component = components[component_index];
    for (const CycleState& state : component.states) {
      for (const auto& [barrier, barrier_height] : state.barriers) {
        ++counters.barriers_by_height[barrier_height];
        for (int repetition = 0;
             repetition < options.rollouts_per_barrier; ++repetition) {
          Graph forced = state.graph;
          const int exact_height = 2 + flip_delta(forced, barrier);
          if (exact_height != barrier_height)
            throw std::runtime_error("barrier height changed");
          flip(forced, barrier);
          RolloutResult result = rollout(
              forced, barrier_height, barrier, options, rng, known_states,
              known_barriers, counters);
          ++counters.rollouts;
          counters.steps += result.steps;
          counters.best_objective =
              std::min(counters.best_objective, result.best);
          ++counters.terminal_best_distribution[result.best];
          if (result.kind == RolloutResult::kConstruction) {
            const std::vector<Conflict> conflicts =
                all_conflicts(result.graph);
            if (!conflicts.empty())
              throw std::runtime_error("E=0 construction replay failed");
            std::cout
                << "{\"mode\":\"construction\","
                << "\"algorithm\":\"e2_neutral_cycle_barrier_escape_v1\","
                << "\"graph6\":" << json_quote(graph6(result.graph)) << ','
                << "\"objective\":0,"
                << "\"rollouts\":" << counters.rollouts << ','
                << "\"steps\":" << counters.steps << "}\n";
            return 10;
          }
          if (result.kind == RolloutResult::kAbsorbed) {
            ++counters.absorbed_known_cycle;
          } else if (result.kind == RolloutResult::kExhausted) {
            ++counters.exhausted;
          } else if (result.kind == RolloutResult::kNewE2) {
            try {
              Component discovered = build_component(
                  result.graph, "barrier_escape");
              if (static_cast<int>(components.size()) <
                      options.component_limit &&
                  add_component(std::move(discovered))) {
                ++counters.new_components;
                std::cerr << "new_component index="
                          << components.size() - 1
                          << " after_rollout=" << counters.rollouts
                          << " total_states=" << known_states.size() << '\n';
              } else {
                ++counters.absorbed_known_cycle;
              }
            } catch (const std::runtime_error&) {
              noncycle_e2.push_back(graph6(result.graph));
            }
          }
          if (options.progress_interval > 0 &&
              counters.rollouts % options.progress_interval == 0) {
            const double elapsed =
                std::chrono::duration<double>(Clock::now() - started).count();
            std::cerr << "progress rollouts=" << counters.rollouts
                      << " steps=" << counters.steps
                      << " components=" << components.size()
                      << " best_E=" << counters.best_objective
                      << " elapsed=" << elapsed << '\n';
          }
        }
      }
    }
  }

  std::map<int, int> cycle_lengths;
  std::map<int, int> barriers_per_state;
  for (const Component& component : components) {
    ++cycle_lengths[component.states.size()];
    for (const CycleState& state : component.states)
      ++barriers_per_state[state.barriers.size()];
  }
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  auto integer_map = [](const auto& values) {
    std::ostringstream output;
    output << '{';
    bool first = true;
    for (const auto& [key, value] : values) {
      if (!first) output << ',';
      first = false;
      output << '"' << key << "\":" << value;
    }
    output << '}';
    return output.str();
  };
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"exploratory_search\","
            << "\"algorithm\":\"e2_neutral_cycle_barrier_escape_v1\","
            << "\"evidence_label\":\"REPRODUCIBLE COMPUTATIONAL "
               "OBSERVATION\","
            << "\"seed\":" << options.seed << ','
            << "\"input_seed_count\":" << options.seed_graphs.size() << ','
            << "\"initial_components\":" << initial_components << ','
            << "\"initial_neutral_states\":" << initial_neutral_states << ','
            << "\"components_discovered\":" << counters.new_components << ','
            << "\"total_components\":" << components.size() << ','
            << "\"total_neutral_states\":" << known_states.size() << ','
            << "\"cycle_length_distribution\":"
            << integer_map(cycle_lengths) << ','
            << "\"barriers_per_state_distribution\":"
            << integer_map(barriers_per_state) << ','
            << "\"barriers_by_height\":"
            << integer_map(counters.barriers_by_height) << ','
            << "\"rollouts\":" << counters.rollouts << ','
            << "\"steps\":" << counters.steps << ','
            << "\"absorbed_known_cycle\":"
            << counters.absorbed_known_cycle << ','
            << "\"known_cycle_visits\":"
            << counters.known_cycle_visits << ','
            << "\"repeated_barrier_crossings\":"
            << counters.repeated_barrier_crossings << ','
            << "\"exhausted\":" << counters.exhausted << ','
            << "\"noncycle_E2_hits\":" << noncycle_e2.size() << ','
            << "\"E1_visits\":" << counters.e1_visits << ','
            << "\"best_E\":" << counters.best_objective << ','
            << "\"maximum_E\":" << counters.maximum_objective << ','
            << "\"terminal_best_distribution\":"
            << integer_map(counters.terminal_best_distribution) << ','
            << "\"exact_objective_checks\":"
            << counters.exact_objective_checks << ','
            << "\"ceiling_rejections\":"
            << counters.ceiling_rejections << ','
            << "\"rollouts_per_barrier\":"
            << options.rollouts_per_barrier << ','
            << "\"steps_per_rollout\":" << options.steps_per_rollout << ','
            << "\"tabu_tenure\":" << options.tabu_tenure << ','
            << "\"noise_per_million\":"
            << options.noise_per_million << ','
            << "\"objective_ceiling\":"
            << options.objective_ceiling << ','
            << "\"stopped_on_E0\":false,"
            << "\"claim_boundary\":\"Heuristic barrier excursions and "
               "finite neutral-cycle enumeration do not certify "
               "nonexistence.\","
            << "\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    initialize_edges();
    const Options options = parse_options(argc, argv);
    if (options.self_check) return run_self_check(options);
    return run_search(options);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
