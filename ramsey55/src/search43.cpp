// Dependency-free incremental local-search baseline for the (5,5;n) objective.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

struct FiveSet {
  std::array<uint16_t, 10> edges{};
};

struct GraphSeed {
  int n{};
  std::vector<uint8_t> edges;
};

std::string first_line(const std::string& path, int requested_line) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open seed graph: " + path);
  std::string line;
  for (int current = 1; current <= requested_line; ++current) {
    if (!std::getline(input, line)) throw std::runtime_error("seed line is absent");
  }
  while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
  return line;
}

GraphSeed decode_graph6(const std::string& raw) {
  std::string line = raw;
  if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
  if (line.empty()) throw std::runtime_error("empty graph6 seed");
  const int n = static_cast<unsigned char>(line[0]) - 63;
  if (n < 0 || n > 62) throw std::runtime_error("only short graph6 seeds are supported");
  const int m = n * (n - 1) / 2;
  std::vector<uint8_t> matrix(n * n, 0);
  int bit_index = 0;
  for (int j = 1; j < n; ++j) {
    for (int i = 0; i < j; ++i) {
      if (1 + bit_index / 6 >= static_cast<int>(line.size()))
        throw std::runtime_error("truncated graph6 seed");
      const int value = static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64) throw std::runtime_error("invalid graph6 seed");
      const uint8_t edge = (value >> (5 - bit_index % 6)) & 1;
      ++bit_index;
      matrix[i * n + j] = matrix[j * n + i] = edge;
    }
  }
  std::vector<uint8_t> edges;
  edges.reserve(m);
  for (int i = 0; i < n; ++i)
    for (int j = i + 1; j < n; ++j) edges.push_back(matrix[i * n + j]);
  return {n, std::move(edges)};
}

class SearchState {
 public:
  explicit SearchState(int order)
      : n(order),
        m(order * (order - 1) / 2),
        edge_index(order * order, uint16_t{0}),
        edge_left(m),
        edge_right(m),
        incidence(m),
        edge_value(m, 0),
        degree(order, 0) {
    if (n < 5 || n > 62) throw std::runtime_error("n must be in 5..62");
    int edge = 0;
    for (int i = 0; i < n; ++i) {
      for (int j = i + 1; j < n; ++j) {
        edge_index[i * n + j] = edge_index[j * n + i] = edge;
        edge_left[edge] = i;
        edge_right[edge] = j;
        ++edge;
      }
    }
    const size_t per_edge =
        static_cast<size_t>(n - 2) * (n - 3) * (n - 4) / 6;
    for (auto& list : incidence) list.reserve(per_edge);
    build_five_sets();
    counts.assign(five_sets.size(), 0);
    bad_position.assign(five_sets.size(), -1);
  }

  void randomize(std::mt19937_64& rng) {
    std::bernoulli_distribution coin(0.5);
    std::fill(degree.begin(), degree.end(), 0);
    for (int edge = 0; edge < m; ++edge) {
      edge_value[edge] = coin(rng);
      if (edge_value[edge]) {
        ++degree[edge_left[edge]];
        ++degree[edge_right[edge]];
      }
    }
    rebuild_counts();
  }

  void initialize_from_seed(const GraphSeed& seed, std::mt19937_64& rng) {
    if (seed.n != n && seed.n + 1 != n)
      throw std::runtime_error("seed order must equal n or n-1");
    std::bernoulli_distribution coin(0.5);
    std::fill(edge_value.begin(), edge_value.end(), 0);
    std::fill(degree.begin(), degree.end(), 0);
    size_t source = 0;
    for (int i = 0; i < seed.n; ++i) {
      for (int j = i + 1; j < seed.n; ++j) {
        const int edge = edge_index[i * n + j];
        edge_value[edge] = seed.edges.at(source++);
      }
    }
    if (seed.n + 1 == n) {
      for (int i = 0; i < seed.n; ++i) edge_value[edge_index[i * n + seed.n]] = coin(rng);
    }
    for (int edge = 0; edge < m; ++edge) {
      if (edge_value[edge]) {
        ++degree[edge_left[edge]];
        ++degree[edge_right[edge]];
      }
    }
    rebuild_counts();
  }

  int flip_delta(int edge) const {
    int delta = 0;
    if (edge_value[edge]) {
      for (uint32_t subset : incidence[edge]) {
        const uint8_t count = counts[subset];
        if (count == 1) ++delta;   // create an independent five-set
        if (count == 10) --delta;  // destroy a clique
      }
    } else {
      for (uint32_t subset : incidence[edge]) {
        const uint8_t count = counts[subset];
        if (count == 0) --delta;  // destroy an independent five-set
        if (count == 9) ++delta;  // create a clique
      }
    }
    return delta;
  }

  long long weighted_flip_delta(
      int edge, const std::vector<uint32_t>& weights) const {
    if (weights.size() != five_sets.size())
      throw std::runtime_error("weight vector size mismatch");
    long long delta = 0;
    if (edge_value[edge]) {
      for (uint32_t subset : incidence[edge]) {
        const uint8_t count = counts[subset];
        if (count == 1) delta += weights[subset];
        if (count == 10) delta -= weights[subset];
      }
    } else {
      for (uint32_t subset : incidence[edge]) {
        const uint8_t count = counts[subset];
        if (count == 0) delta -= weights[subset];
        if (count == 9) delta += weights[subset];
      }
    }
    return delta;
  }

  void increment_bad_weights(std::vector<uint32_t>& weights) const {
    if (weights.size() != five_sets.size())
      throw std::runtime_error("weight vector size mismatch");
    for (uint32_t subset : bad) ++weights[subset];
  }

  void flip(int edge) {
    const bool old_edge = edge_value[edge];
    for (uint32_t subset : incidence[edge]) {
      const uint8_t old_count = counts[subset];
      const uint8_t new_count = old_edge ? old_count - 1 : old_count + 1;
      const bool old_bad = old_count == 0 || old_count == 10;
      const bool new_bad = new_count == 0 || new_count == 10;
      if (old_bad && !new_bad) remove_bad(subset);
      if (!old_bad && new_bad) add_bad(subset);
      counts[subset] = new_count;
    }
    edge_value[edge] ^= 1;
    const int change = edge_value[edge] ? 1 : -1;
    degree[edge_left[edge]] += change;
    degree[edge_right[edge]] += change;
  }

  std::pair<int, int> full_counts() const {
    int cliques = 0;
    int independent = 0;
    for (const FiveSet& subset : five_sets) {
      int count = 0;
      for (uint16_t edge : subset.edges) count += edge_value[edge];
      cliques += count == 10;
      independent += count == 0;
    }
    return {cliques, independent};
  }

  int objective() const { return static_cast<int>(bad.size()); }

  int degree_violation_after_flip(int edge) const {
    const int lower = n - 25;
    const int upper = 24;
    const int change = edge_value[edge] ? -1 : 1;
    int penalty = 0;
    for (int v = 0; v < n; ++v) {
      int value = degree[v];
      if (v == edge_left[edge] || v == edge_right[edge]) value += change;
      if (value < lower) penalty += lower - value;
      if (value > upper) penalty += value - upper;
    }
    return penalty;
  }

  std::array<uint16_t, 10> random_bad_edges(std::mt19937_64& rng) const {
    if (bad.empty()) throw std::runtime_error("no violating set remains");
    std::uniform_int_distribution<size_t> choice(0, bad.size() - 1);
    return five_sets[bad[choice(rng)]].edges;
  }

  int edge_count() const {
    return std::count(edge_value.begin(), edge_value.end(), uint8_t{1});
  }

  std::vector<int> sorted_degrees() const {
    std::vector<int> result = degree;
    std::sort(result.begin(), result.end());
    return result;
  }

  std::string graph6() const {
    std::string bits;
    bits.reserve(n * (n - 1) / 2);
    for (int j = 1; j < n; ++j)
      for (int i = 0; i < j; ++i) bits.push_back(edge_value[edge_index[i * n + j]]);
    while (bits.size() % 6) bits.push_back(0);
    std::string result(1, static_cast<char>(n + 63));
    for (size_t start = 0; start < bits.size(); start += 6) {
      int value = 0;
      for (size_t offset = 0; offset < 6; ++offset)
        value = (value << 1) | bits[start + offset];
      result.push_back(static_cast<char>(value + 63));
    }
    return result;
  }

  const std::vector<uint8_t>& values() const { return edge_value; }

  void set_values(const std::vector<uint8_t>& values) {
    if (values.size() != edge_value.size()) throw std::runtime_error("state size mismatch");
    edge_value = values;
    std::fill(degree.begin(), degree.end(), 0);
    for (int edge = 0; edge < m; ++edge) {
      if (edge_value[edge]) {
        ++degree[edge_left[edge]];
        ++degree[edge_right[edge]];
      }
    }
    rebuild_counts();
  }

  size_t subset_count() const { return five_sets.size(); }
  int edge_slots() const { return m; }
  size_t incidence_count() const {
    size_t total = 0;
    for (const auto& list : incidence) total += list.size();
    return total;
  }

 private:
  int n;
  int m;
  std::vector<uint16_t> edge_index;
  std::vector<uint8_t> edge_left;
  std::vector<uint8_t> edge_right;
  std::vector<FiveSet> five_sets;
  std::vector<std::vector<uint32_t>> incidence;
  std::vector<uint8_t> edge_value;
  std::vector<uint8_t> counts;
  std::vector<int32_t> bad_position;
  std::vector<uint32_t> bad;
  std::vector<int> degree;

  void build_five_sets() {
    for (int a = 0; a < n - 4; ++a) {
      for (int b = a + 1; b < n - 3; ++b) {
        for (int c = b + 1; c < n - 2; ++c) {
          for (int d = c + 1; d < n - 1; ++d) {
            for (int e = d + 1; e < n; ++e) {
              const std::array<int, 5> vertices{a, b, c, d, e};
              FiveSet subset;
              int cursor = 0;
              for (int i = 0; i < 5; ++i)
                for (int j = i + 1; j < 5; ++j)
                  subset.edges[cursor++] = edge_index[vertices[i] * n + vertices[j]];
              const uint32_t index = five_sets.size();
              five_sets.push_back(subset);
              for (uint16_t edge : subset.edges) incidence[edge].push_back(index);
            }
          }
        }
      }
    }
  }

  void rebuild_counts() {
    bad.clear();
    std::fill(bad_position.begin(), bad_position.end(), -1);
    for (uint32_t index = 0; index < five_sets.size(); ++index) {
      uint8_t count = 0;
      for (uint16_t edge : five_sets[index].edges) count += edge_value[edge];
      counts[index] = count;
      if (count == 0 || count == 10) add_bad(index);
    }
  }

  void add_bad(uint32_t subset) {
    if (bad_position[subset] != -1) throw std::runtime_error("duplicate bad subset");
    bad_position[subset] = static_cast<int32_t>(bad.size());
    bad.push_back(subset);
  }

  void remove_bad(uint32_t subset) {
    const int32_t position = bad_position[subset];
    if (position < 0) throw std::runtime_error("missing bad subset");
    const uint32_t last = bad.back();
    bad[position] = last;
    bad_position[last] = position;
    bad.pop_back();
    bad_position[subset] = -1;
  }
};

struct Options {
  int n = 43;
  uint64_t seed = 1;
  long long steps = 20000;
  int restarts = 1;
  int tabu_tenure = 7;
  double random_walk = 0.03;
  std::string output = "best.g6";
  std::string seed_graph;
  int seed_line = 1;
  bool self_test = false;
  bool benchmark = false;
  bool scan_two_flip = false;
  int trials = 20;
  int breakout_interval = 0;
  int initial_perturbation = 0;
};

Options parse_options(int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string option = argv[i];
    auto value = [&]() -> std::string {
      if (i + 1 >= argc) throw std::runtime_error("missing value for " + option);
      return argv[++i];
    };
    if (option == "--n") options.n = std::stoi(value());
    else if (option == "--seed") options.seed = std::stoull(value());
    else if (option == "--steps") options.steps = std::stoll(value());
    else if (option == "--restarts") options.restarts = std::stoi(value());
    else if (option == "--tabu") options.tabu_tenure = std::stoi(value());
    else if (option == "--random-walk") options.random_walk = std::stod(value());
    else if (option == "--output") options.output = value();
    else if (option == "--seed-graph") options.seed_graph = value();
    else if (option == "--seed-line") options.seed_line = std::stoi(value());
    else if (option == "--trials") options.trials = std::stoi(value());
    else if (option == "--breakout-interval") options.breakout_interval = std::stoi(value());
    else if (option == "--initial-perturbation")
      options.initial_perturbation = std::stoi(value());
    else if (option == "--self-test") options.self_test = true;
    else if (option == "--benchmark") options.benchmark = true;
    else if (option == "--scan-two-flip") options.scan_two_flip = true;
    else throw std::runtime_error("unknown option: " + option);
  }
  return options;
}

void write_graph6(const std::string& path, const std::string& graph6) {
  std::ofstream output(path, std::ios::trunc);
  if (!output) throw std::runtime_error("cannot write " + path);
  output << graph6 << '\n';
}

int run_self_test(const Options& options) {
  std::mt19937_64 rng(options.seed);
  SearchState state(10);
  long long checks = 0;
  for (int trial = 0; trial < options.trials; ++trial) {
    state.randomize(rng);
    for (int flip = 0; flip < 200; ++flip) {
      std::uniform_int_distribution<int> edge_choice(0, 44);
      const int edge = edge_choice(rng);
      const int old_objective = state.objective();
      const int predicted = state.flip_delta(edge);
      state.flip(edge);
      const auto [cliques, independent] = state.full_counts();
      if (state.objective() != old_objective + predicted ||
          state.objective() != cliques + independent) {
        throw std::runtime_error("incremental delta self-test failed");
      }
      ++checks;
    }
  }
  std::cout << "{\"mode\":\"self_test\",\"seed\":" << options.seed
            << ",\"trials\":" << options.trials << ",\"random_flips\":" << checks
            << ",\"status\":\"PASS\"}\n";
  return 0;
}

int run_benchmark(const Options& options) {
  const auto pre_start = Clock::now();
  SearchState state(options.n);
  const double pre_seconds =
      std::chrono::duration<double>(Clock::now() - pre_start).count();
  std::mt19937_64 rng(options.seed);
  state.randomize(rng);
  constexpr int full_iterations = 100;
  auto start = Clock::now();
  int checksum = 0;
  for (int i = 0; i < full_iterations; ++i) {
    const auto [c, d] = state.full_counts();
    checksum += c + d;
  }
  const double full_seconds = std::chrono::duration<double>(Clock::now() - start).count();
  constexpr int delta_iterations = 100000;
  std::uniform_int_distribution<int> edge_choice(0, options.n * (options.n - 1) / 2 - 1);
  start = Clock::now();
  for (int i = 0; i < delta_iterations; ++i) checksum += state.flip_delta(edge_choice(rng));
  const double delta_seconds = std::chrono::duration<double>(Clock::now() - start).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"benchmark\",\"n\":" << options.n << ",\"seed\":"
            << options.seed << ",\"five_subsets\":" << state.subset_count()
            << ",\"incidence_entries\":" << state.incidence_count()
            << ",\"precompute_seconds\":" << pre_seconds
            << ",\"full_recomputations\":" << full_iterations
            << ",\"full_seconds\":" << full_seconds
            << ",\"full_per_second\":" << full_iterations / full_seconds
            << ",\"delta_evaluations\":" << delta_iterations
            << ",\"delta_seconds\":" << delta_seconds
            << ",\"delta_per_second\":" << delta_iterations / delta_seconds
            << ",\"checksum\":" << checksum << "}\n";
  return 0;
}

int run_search(const Options& options) {
  const auto total_start = Clock::now();
  const auto pre_start = Clock::now();
  SearchState state(options.n);
  const double pre_seconds =
      std::chrono::duration<double>(Clock::now() - pre_start).count();
  std::mt19937_64 rng(options.seed);
  GraphSeed seed_graph;
  if (!options.seed_graph.empty())
    seed_graph = decode_graph6(first_line(options.seed_graph, options.seed_line));

  int global_best = std::numeric_limits<int>::max();
  std::vector<uint8_t> global_values;
  long long completed_steps = 0;
  long long delta_evaluations = 0;
  int improvement_count = 0;
  long long penalty_updates = 0;
  std::uniform_real_distribution<double> unit(0.0, 1.0);

  for (int restart = 0; restart < options.restarts && global_best > 0; ++restart) {
    if (options.seed_graph.empty()) state.randomize(rng);
    else state.initialize_from_seed(seed_graph, rng);
    if (options.initial_perturbation > 0) {
      std::uniform_int_distribution<int> edge_choice(0, state.edge_slots() - 1);
      for (int i = 0; i < options.initial_perturbation; ++i)
        state.flip(edge_choice(rng));
    }
    std::vector<long long> tabu(options.n * (options.n - 1) / 2, 0);
    std::vector<uint32_t> weights(state.subset_count(), 1);
    long long next_breakout = options.breakout_interval;
    int restart_best = state.objective();
    if (state.objective() < global_best) {
      global_best = state.objective();
      global_values = state.values();
      ++improvement_count;
      std::cerr << "best restart=" << restart << " step=0 E=" << global_best << '\n';
    }

    for (long long step = 0; step < options.steps && state.objective() > 0; ++step) {
      const auto choices = state.random_bad_edges(rng);
      int selected = -1;
      int selected_delta = std::numeric_limits<int>::max();
      long long selected_weighted_delta = std::numeric_limits<long long>::max();
      int selected_degree_penalty = std::numeric_limits<int>::max();
      const bool walk = unit(rng) < options.random_walk;
      if (walk) {
        std::vector<int> allowed;
        for (uint16_t edge : choices)
          if (tabu[edge] <= step) allowed.push_back(edge);
        if (allowed.empty()) allowed.assign(choices.begin(), choices.end());
        std::uniform_int_distribution<size_t> choice(0, allowed.size() - 1);
        selected = allowed[choice(rng)];
        selected_delta = state.flip_delta(selected);
        ++delta_evaluations;
      } else {
        for (uint16_t edge : choices) {
          const int delta = state.flip_delta(edge);
          const long long weighted_delta =
              options.breakout_interval > 0
                  ? state.weighted_flip_delta(edge, weights)
                  : delta;
          ++delta_evaluations;
          const bool aspiration = state.objective() + delta < global_best;
          if (tabu[edge] > step && !aspiration) continue;
          const int degree_penalty = state.degree_violation_after_flip(edge);
          if (weighted_delta < selected_weighted_delta ||
              (weighted_delta == selected_weighted_delta && delta < selected_delta) ||
              (weighted_delta == selected_weighted_delta && delta == selected_delta &&
               degree_penalty < selected_degree_penalty) ||
              (weighted_delta == selected_weighted_delta && delta == selected_delta &&
               degree_penalty == selected_degree_penalty && unit(rng) < 0.5)) {
            selected = edge;
            selected_delta = delta;
            selected_weighted_delta = weighted_delta;
            selected_degree_penalty = degree_penalty;
          }
        }
        if (selected < 0) {
          selected = choices[static_cast<size_t>(rng() % choices.size())];
          selected_delta = state.flip_delta(selected);
          ++delta_evaluations;
        }
      }
      state.flip(selected);
      tabu[selected] = step + options.tabu_tenure + 1;
      ++completed_steps;

      if (state.objective() < restart_best) {
        restart_best = state.objective();
        if (options.breakout_interval > 0)
          next_breakout = step + 1 + options.breakout_interval;
      } else if (options.breakout_interval > 0 && step + 1 >= next_breakout) {
        state.increment_bad_weights(weights);
        ++penalty_updates;
        next_breakout += options.breakout_interval;
      }

      if (state.objective() < global_best) {
        global_best = state.objective();
        global_values = state.values();
        ++improvement_count;
        std::cerr << "best restart=" << restart << " step=" << step + 1
                  << " E=" << global_best << '\n';
      }
    }
  }

  state.set_values(global_values);
  const auto [cliques, independent] = state.full_counts();
  if (cliques + independent != global_best)
    throw std::runtime_error("final full recomputation disagrees with incremental objective");
  write_graph6(options.output, state.graph6());
  const double total_seconds =
      std::chrono::duration<double>(Clock::now() - total_start).count();
  const std::vector<int> degrees = state.sorted_degrees();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"search\",\"algorithm\":\"violated_set_min_conflicts_tabu_v1\""
            << ",\"n\":" << options.n << ",\"seed\":" << options.seed
            << ",\"steps_requested\":" << options.steps << ",\"restarts\":"
            << options.restarts << ",\"steps_executed\":" << completed_steps
            << ",\"delta_evaluations\":" << delta_evaluations
            << ",\"tabu_tenure\":" << options.tabu_tenure
            << ",\"random_walk\":" << options.random_walk
            << ",\"breakout_interval\":" << options.breakout_interval
            << ",\"initial_perturbation\":" << options.initial_perturbation
            << ",\"penalty_updates\":" << penalty_updates
            << ",\"seed_graph\":\"" << options.seed_graph << "\""
            << ",\"seed_line\":" << options.seed_line
            << ",\"precompute_seconds\":" << pre_seconds
            << ",\"runtime_seconds\":" << total_seconds
            << ",\"improvements\":" << improvement_count << ",\"C5\":" << cliques
            << ",\"I5\":" << independent << ",\"E\":" << global_best
            << ",\"edge_count\":" << state.edge_count() << ",\"degree_sequence\":[";
  for (size_t i = 0; i < degrees.size(); ++i) {
    if (i) std::cout << ',';
    std::cout << degrees[i];
  }
  std::cout << "],\"graph6\":\"" << state.graph6() << "\",\"output\":\""
            << options.output << "\"}\n";
  return 0;
}

int run_two_flip_scan(const Options& options) {
  if (options.seed_graph.empty())
    throw std::runtime_error("--scan-two-flip requires --seed-graph");
  const auto started = Clock::now();
  SearchState state(options.n);
  std::mt19937_64 rng(options.seed);
  const GraphSeed seed_graph =
      decode_graph6(first_line(options.seed_graph, options.seed_line));
  if (seed_graph.n != options.n)
    throw std::runtime_error("two-flip scan requires a seed graph of order n");
  state.initialize_from_seed(seed_graph, rng);
  const auto [base_cliques, base_independent] = state.full_counts();
  const int base_objective = base_cliques + base_independent;
  int best_objective = base_objective;
  int best_first = -1;
  int best_second = -1;
  long long evaluations = 0;
  bool found_zero = false;

  for (int first = 0; first < state.edge_slots() && !found_zero; ++first) {
    const int first_delta = state.flip_delta(first);
    ++evaluations;
    if (base_objective + first_delta < best_objective) {
      best_objective = base_objective + first_delta;
      best_first = first;
      best_second = -1;
      if (best_objective == 0) {
        found_zero = true;
        break;
      }
    }
    state.flip(first);
    for (int second = first + 1; second < state.edge_slots(); ++second) {
      const int second_delta = state.flip_delta(second);
      ++evaluations;
      const int objective = base_objective + first_delta + second_delta;
      if (objective < best_objective) {
        best_objective = objective;
        best_first = first;
        best_second = second;
        if (best_objective == 0) {
          found_zero = true;
          break;
        }
      }
    }
    state.flip(first);
  }

  if (best_first >= 0) state.flip(best_first);
  if (best_second >= 0) state.flip(best_second);
  const auto [best_cliques, best_independent] = state.full_counts();
  if (best_cliques + best_independent != best_objective)
    throw std::runtime_error("two-flip scan result failed full recomputation");
  write_graph6(options.output, state.graph6());
  const double elapsed = std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"exhaustive_hamming_radius_2\",\"n\":" << options.n
            << ",\"seed_graph\":\"" << options.seed_graph << "\""
            << ",\"base_C5\":" << base_cliques << ",\"base_I5\":"
            << base_independent << ",\"base_E\":" << base_objective
            << ",\"flip_delta_evaluations\":" << evaluations
            << ",\"best_first_edge_index\":" << best_first
            << ",\"best_second_edge_index\":" << best_second
            << ",\"best_C5\":" << best_cliques << ",\"best_I5\":"
            << best_independent << ",\"best_E\":" << best_objective
            << ",\"edge_count\":" << state.edge_count()
            << ",\"runtime_seconds\":" << elapsed << ",\"output\":\""
            << options.output << "\"}\n";
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    if (options.self_test) return run_self_test(options);
    if (options.benchmark) return run_benchmark(options);
    if (options.scan_two_flip) return run_two_flip_scan(options);
    return run_search(options);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
