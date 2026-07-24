// Exhaustive targeted Hamming-distance-three scan around an E=2 candidate.
//
// Any valid graph obtained by exactly three flips must flip an edge in each
// original forbidden five-set.  We enumerate every unordered edge triple
// satisfying that necessary condition, evaluate it with the audited
// incremental kernel, and directly recount every new incumbent.

#define main search43_embedded_main
#include "search43.cpp"
#undef main

#include <set>
#include <sstream>

namespace {

struct Hamming3Options {
  std::string graph;
  std::array<int, 5> first_conflict{};
  std::array<int, 5> second_conflict{};
  bool first_supplied{false};
  bool second_supplied{false};
  std::string output = "targeted_hamming3_best.g6";
};

std::array<int, 5> parse_five_vertices(const std::string& text) {
  std::array<int, 5> result{};
  std::stringstream stream(text);
  std::string field;
  int cursor = 0;
  while (std::getline(stream, field, ',')) {
    if (cursor >= 5) throw std::runtime_error("conflict must have five vertices");
    result[cursor++] = std::stoi(field);
  }
  if (cursor != 5) throw std::runtime_error("conflict must have five vertices");
  std::sort(result.begin(), result.end());
  if (std::adjacent_find(result.begin(), result.end()) != result.end() ||
      result.front() < 0 || result.back() >= 43)
    throw std::runtime_error("invalid conflict vertex set");
  return result;
}

Hamming3Options parse_hamming3_options(int argc, char** argv) {
  Hamming3Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto value = [&]() {
      if (index + 1 >= argc)
        throw std::runtime_error("missing value for " + option);
      return std::string(argv[++index]);
    };
    if (option == "--graph")
      options.graph = value();
    else if (option == "--first-conflict") {
      options.first_conflict = parse_five_vertices(value());
      options.first_supplied = true;
    } else if (option == "--second-conflict") {
      options.second_conflict = parse_five_vertices(value());
      options.second_supplied = true;
    } else if (option == "--output")
      options.output = value();
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.graph.empty() || !options.first_supplied ||
      !options.second_supplied)
    throw std::runtime_error(
        "--graph, --first-conflict, and --second-conflict are required");
  if (options.first_conflict == options.second_conflict)
    throw std::runtime_error("the two conflicts must differ");
  return options;
}

int edge_index_for_pair(int left, int right) {
  if (left > right) std::swap(left, right);
  if (!(0 <= left && left < right && right < 43))
    throw std::runtime_error("invalid edge pair");
  return left * (2 * 43 - left - 1) / 2 + (right - left - 1);
}

std::array<int, 10> conflict_edges(const std::array<int, 5>& vertices) {
  std::array<int, 10> result{};
  int cursor = 0;
  for (int left = 0; left < 5; ++left)
    for (int right = left + 1; right < 5; ++right)
      result[cursor++] =
          edge_index_for_pair(vertices[left], vertices[right]);
  std::sort(result.begin(), result.end());
  return result;
}

bool homogeneous_conflict(const GraphSeed& graph,
                          const std::array<int, 5>& vertices) {
  int edges = 0;
  for (int left = 0; left < 5; ++left)
    for (int right = left + 1; right < 5; ++right)
      edges += graph.edges[edge_index_for_pair(vertices[left], vertices[right])];
  return edges == 0 || edges == 10;
}

struct Triple {
  uint16_t first{};
  uint16_t second{};
  uint16_t third{};
};

int run_hamming3(const Hamming3Options& options) {
  const auto started = Clock::now();
  const GraphSeed graph = decode_graph6(first_line(options.graph, 1));
  if (graph.n != 43)
    throw std::runtime_error("targeted Hamming-three scan requires order 43");
  if (!homogeneous_conflict(graph, options.first_conflict) ||
      !homogeneous_conflict(graph, options.second_conflict))
    throw std::runtime_error("a supplied five-set is not homogeneous");

  SearchState state(43);
  std::mt19937_64 initialization_rng(0);
  state.initialize_from_seed(graph, initialization_rng);
  const auto [base_cliques, base_independent] = state.full_counts();
  const int base_objective = base_cliques + base_independent;
  if (base_objective != 2)
    throw std::runtime_error("base graph must have exactly two conflicts");

  const auto first_edges = conflict_edges(options.first_conflict);
  const auto second_edges = conflict_edges(options.second_conflict);
  std::array<uint8_t, 903> hits_first{};
  std::array<uint8_t, 903> hits_second{};
  for (int edge : first_edges) hits_first[edge] = 1;
  for (int edge : second_edges) hits_second[edge] = 1;

  std::vector<Triple> triples;
  triples.reserve(2500000);
  for (int first = 0; first < 901; ++first) {
    for (int second = first + 1; second < 902; ++second) {
      const bool prefix_first = hits_first[first] || hits_first[second];
      const bool prefix_second = hits_second[first] || hits_second[second];
      for (int third = second + 1; third < 903; ++third) {
        if ((prefix_first || hits_first[third]) &&
            (prefix_second || hits_second[third]))
          triples.push_back(
              {static_cast<uint16_t>(first),
               static_cast<uint16_t>(second),
               static_cast<uint16_t>(third)});
      }
    }
  }
  if (triples.empty()) throw std::runtime_error("targeted triple set is empty");

  int best_objective = base_objective;
  Triple best{};
  bool has_best = false;
  uint64_t delta_evaluations = 0;
  uint64_t incumbent_recounts = 0;
  size_t cursor = 0;
  while (cursor < triples.size() && best_objective > 0) {
    const int first = triples[cursor].first;
    const int first_delta = state.flip_delta(first);
    ++delta_evaluations;
    state.flip(first);
    while (cursor < triples.size() && triples[cursor].first == first &&
           best_objective > 0) {
      const int second = triples[cursor].second;
      const int second_delta = state.flip_delta(second);
      ++delta_evaluations;
      state.flip(second);
      while (cursor < triples.size() && triples[cursor].first == first &&
             triples[cursor].second == second) {
        const int third = triples[cursor].third;
        const int objective =
            base_objective + first_delta + second_delta +
            state.flip_delta(third);
        ++delta_evaluations;
        if (objective < best_objective) {
          state.flip(third);
          const auto [cliques, independent] = state.full_counts();
          ++incumbent_recounts;
          if (cliques + independent != objective)
            throw std::runtime_error(
                "incremental triple objective failed a full recount");
          state.flip(third);
          best_objective = objective;
          best = triples[cursor];
          has_best = true;
          if (best_objective == 0) {
            ++cursor;
            break;
          }
        }
        ++cursor;
      }
      state.flip(second);
    }
    state.flip(first);
  }

  if (has_best) {
    state.flip(best.first);
    state.flip(best.second);
    state.flip(best.third);
  }
  const auto [best_cliques, best_independent] = state.full_counts();
  if (best_cliques + best_independent != best_objective)
    throw std::runtime_error("retained Hamming-three graph failed recount");
  write_graph6(options.output, state.graph6());
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();

  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"targeted_exhaustive_hamming_distance_3\""
            << ",\"order\":43,\"base_C5\":" << base_cliques
            << ",\"base_I5\":" << base_independent
            << ",\"base_E\":" << base_objective
            << ",\"necessary_condition\":\"triple intersects both original conflict edge sets\""
            << ",\"targeted_triple_count\":" << triples.size()
            << ",\"coverage_complete\":"
            << (cursor == triples.size() || best_objective == 0 ? "true" : "false")
            << ",\"delta_evaluations\":" << delta_evaluations
            << ",\"incumbent_full_recounts\":" << incumbent_recounts
            << ",\"best_first_edge_index\":"
            << (has_best ? static_cast<int>(best.first) : -1)
            << ",\"best_second_edge_index\":"
            << (has_best ? static_cast<int>(best.second) : -1)
            << ",\"best_third_edge_index\":"
            << (has_best ? static_cast<int>(best.third) : -1)
            << ",\"best_C5\":" << best_cliques
            << ",\"best_I5\":" << best_independent
            << ",\"best_E\":" << best_objective
            << ",\"graph6\":\"" << state.graph6() << "\""
            << ",\"output\":\"" << options.output << "\""
            << ",\"runtime_seconds\":" << elapsed << "}\n";
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    return run_hamming3(parse_hamming3_options(argc, argv));
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
