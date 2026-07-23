// Verifier 2: independent graph6 parser and recursive bitset clique search.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

struct Graph {
  int n{};
  std::vector<uint64_t> adj;
};

Graph parse_graph6(std::string line) {
  while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) line.pop_back();
  constexpr const char* header = ">>graph6<<";
  if (line.rfind(header, 0) == 0) line.erase(0, 10);
  if (line.empty()) throw std::runtime_error("empty graph6 input");
  const int n = static_cast<unsigned char>(line[0]) - 63;
  if (n < 0 || n > 62) throw std::runtime_error("only short graph6 is supported");
  const int required_bits = n * (n - 1) / 2;
  if (static_cast<int>(line.size() - 1) * 6 < required_bits)
    throw std::runtime_error("truncated graph6 input");
  Graph graph{n, std::vector<uint64_t>(n, 0)};
  int bit_index = 0;
  for (int j = 1; j < n; ++j) {
    for (int i = 0; i < j; ++i) {
      const int value = static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64) throw std::runtime_error("invalid graph6 byte");
      const bool edge = (value >> (5 - bit_index % 6)) & 1;
      ++bit_index;
      if (edge) {
        graph.adj[i] |= uint64_t{1} << j;
        graph.adj[j] |= uint64_t{1} << i;
      }
    }
  }
  return graph;
}

bool contains_clique(const Graph& graph, uint64_t candidates, int needed) {
  if (needed == 0) return true;
  if (__builtin_popcountll(candidates) < needed) return false;
  while (candidates) {
    if (__builtin_popcountll(candidates) < needed) return false;
    const int vertex = __builtin_ctzll(candidates);
    const uint64_t bit = uint64_t{1} << vertex;
    candidates &= ~bit;
    if (contains_clique(graph, candidates & graph.adj[vertex], needed - 1)) return true;
  }
  return false;
}

Graph complement(const Graph& graph) {
  const uint64_t mask = (uint64_t{1} << graph.n) - 1;
  Graph result{graph.n, std::vector<uint64_t>(graph.n)};
  for (int i = 0; i < graph.n; ++i)
    result.adj[i] = mask & ~(graph.adj[i] | (uint64_t{1} << i));
  return result;
}

int main_impl(int argc, char** argv) {
  if (argc < 2) {
    std::cerr << "usage: bitset_verify GRAPH [--line N] [--k K]\n";
    return 2;
  }
  std::string path = argv[1];
  int line_number = 1;
  int k = 5;
  for (int i = 2; i < argc; ++i) {
    const std::string option = argv[i];
    if (option == "--line" && i + 1 < argc) line_number = std::stoi(argv[++i]);
    else if (option == "--k" && i + 1 < argc) k = std::stoi(argv[++i]);
    else throw std::runtime_error("unknown or incomplete option: " + option);
  }
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open input");
  std::string line;
  for (int current = 1; current <= line_number; ++current) {
    if (!std::getline(input, line)) throw std::runtime_error("requested line is absent");
  }
  const Graph graph = parse_graph6(line);
  const Graph dual = complement(graph);
  const uint64_t all = (uint64_t{1} << graph.n) - 1;
  const bool clique = contains_clique(graph, all, k);
  const bool independent = contains_clique(dual, all, k);
  const bool lower_clique = k > 1 && contains_clique(graph, all, k - 1);
  const bool lower_independent = k > 1 && contains_clique(dual, all, k - 1);
  long edges = 0;
  std::vector<int> degrees;
  for (uint64_t row : graph.adj) {
    const int degree = __builtin_popcountll(row);
    degrees.push_back(degree);
    edges += degree;
  }
  std::sort(degrees.begin(), degrees.end());
  std::cout << "{\"verifier\":\"cpp_recursive_bitset_clique_v1\",\"n\":" << graph.n
            << ",\"k\":" << k << ",\"edge_count\":" << edges / 2
            << ",\"clique_k_found\":" << (clique ? "true" : "false")
            << ",\"independent_k_found\":" << (independent ? "true" : "false")
            << ",\"clique_k_minus_1_found\":" << (lower_clique ? "true" : "false")
            << ",\"independent_k_minus_1_found\":"
            << (lower_independent ? "true" : "false") << ",\"degree_sequence\":[";
  for (size_t i = 0; i < degrees.size(); ++i) {
    if (i) std::cout << ',';
    std::cout << degrees[i];
  }
  std::cout << "],\"valid\":" << (!clique && !independent ? "true" : "false") << "}\n";
  return !clique && !independent ? 0 : 1;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    return main_impl(argc, argv);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
