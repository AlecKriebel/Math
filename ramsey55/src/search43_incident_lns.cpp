// Deterministic constructive local search restricted to the exact 237-edge
// incident-six neighborhood recorded in residual_lns_incident_six.metadata.json.
#include <algorithm>
#include <array>
#include <chrono>
#include <cctype>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;
constexpr int kOrder = 43;
constexpr std::array<int, 6> kResidualVertices{3, 4, 7, 38, 41, 42};

struct FiveSet {
  std::array<uint16_t, 10> edges{};
};

struct GraphSeed {
  int order{};
  std::vector<uint8_t> edges;
  std::string graph6;
};

struct Options {
  std::string seed_graph;
  std::string metadata;
  std::string output = "incident_lns_best.g6";
  uint64_t seed = 20260726;
  long long steps = 250000;
  int restarts = 4;
  int tabu_tenure = 9;
  double random_walk = 0.04;
  int breakout_interval = 250;
  int restart_perturbation = 12;
  bool self_check = false;
  int self_check_random_flips = 100;
};

std::string read_text(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open " + path);
  return std::string(std::istreambuf_iterator<char>(input),
                     std::istreambuf_iterator<char>());
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
  throw std::runtime_error("graph has no data line");
}

GraphSeed decode_graph6(const std::string& raw) {
  std::string line = raw;
  if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
  if (line.empty()) throw std::runtime_error("empty graph6 input");
  const int order = static_cast<unsigned char>(line[0]) - 63;
  if (order != kOrder)
    throw std::runtime_error("incident LNS requires graph order 43");
  const int edge_count = order * (order - 1) / 2;
  std::vector<uint8_t> matrix(order * order, 0);
  int bit_index = 0;
  for (int right = 1; right < order; ++right) {
    for (int left = 0; left < right; ++left) {
      if (1 + bit_index / 6 >= static_cast<int>(line.size()))
        throw std::runtime_error("truncated graph6 input");
      const int value =
          static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64)
        throw std::runtime_error("invalid graph6 byte");
      const uint8_t present = (value >> (5 - bit_index % 6)) & 1;
      ++bit_index;
      matrix[left * order + right] = matrix[right * order + left] = present;
    }
  }
  std::vector<uint8_t> edges;
  edges.reserve(edge_count);
  for (int left = 0; left < order; ++left)
    for (int right = left + 1; right < order; ++right)
      edges.push_back(matrix[left * order + right]);
  return {order, std::move(edges), line};
}

std::pair<size_t, size_t> array_span(const std::string& json,
                                     const std::string& key) {
  const std::string needle = "\"" + key + "\"";
  const size_t key_position = json.find(needle);
  if (key_position == std::string::npos)
    throw std::runtime_error("metadata is missing " + key);
  const size_t colon = json.find(':', key_position + needle.size());
  const size_t start = json.find('[', colon);
  if (colon == std::string::npos || start == std::string::npos)
    throw std::runtime_error("metadata has malformed array " + key);
  int depth = 0;
  for (size_t position = start; position < json.size(); ++position) {
    if (json[position] == '[') ++depth;
    if (json[position] == ']') {
      --depth;
      if (depth == 0) return {start, position + 1};
    }
  }
  throw std::runtime_error("metadata has unterminated array " + key);
}

std::vector<int> integers_in_array(const std::string& json,
                                   const std::string& key) {
  const auto [start, end] = array_span(json, key);
  std::vector<int> result;
  size_t position = start;
  while (position < end) {
    if (json[position] == '-' || std::isdigit(
                                       static_cast<unsigned char>(json[position]))) {
      char* parsed_end = nullptr;
      const long value = std::strtol(json.c_str() + position, &parsed_end, 10);
      if (parsed_end == json.c_str() + position)
        throw std::runtime_error("failed to parse metadata integer");
      result.push_back(static_cast<int>(value));
      position = static_cast<size_t>(parsed_end - json.c_str());
    } else {
      ++position;
    }
  }
  return result;
}

int integer_field(const std::string& json, const std::string& key) {
  const std::string needle = "\"" + key + "\"";
  const size_t key_position = json.find(needle);
  if (key_position == std::string::npos)
    throw std::runtime_error("metadata is missing " + key);
  const size_t colon = json.find(':', key_position + needle.size());
  if (colon == std::string::npos)
    throw std::runtime_error("metadata has malformed field " + key);
  size_t position = colon + 1;
  while (position < json.size() &&
         std::isspace(static_cast<unsigned char>(json[position])))
    ++position;
  char* parsed_end = nullptr;
  const long value = std::strtol(json.c_str() + position, &parsed_end, 10);
  if (parsed_end == json.c_str() + position)
    throw std::runtime_error("metadata field is not an integer: " + key);
  return static_cast<int>(value);
}

std::string string_field(const std::string& json, const std::string& key) {
  const std::string needle = "\"" + key + "\"";
  const size_t key_position = json.find(needle);
  if (key_position == std::string::npos)
    throw std::runtime_error("metadata is missing " + key);
  const size_t colon = json.find(':', key_position + needle.size());
  if (colon == std::string::npos)
    throw std::runtime_error("metadata has malformed field " + key);
  size_t position = colon + 1;
  while (position < json.size() &&
         std::isspace(static_cast<unsigned char>(json[position])))
    ++position;
  if (position >= json.size() || json[position] != '"')
    throw std::runtime_error("metadata field is not a string: " + key);
  ++position;
  std::string result;
  while (position < json.size()) {
    const char value = json[position++];
    if (value == '"') return result;
    if (value != '\\') {
      result.push_back(value);
      continue;
    }
    if (position >= json.size())
      throw std::runtime_error("unterminated JSON escape in " + key);
    const char escaped = json[position++];
    if (escaped == '"' || escaped == '\\' || escaped == '/')
      result.push_back(escaped);
    else if (escaped == 'b')
      result.push_back('\b');
    else if (escaped == 'f')
      result.push_back('\f');
    else if (escaped == 'n')
      result.push_back('\n');
    else if (escaped == 'r')
      result.push_back('\r');
    else if (escaped == 't')
      result.push_back('\t');
    else
      throw std::runtime_error("unsupported JSON escape in " + key);
  }
  throw std::runtime_error("unterminated JSON string " + key);
}

std::string json_quote(const std::string& value) {
  static constexpr char hex[] = "0123456789abcdef";
  std::string result = "\"";
  for (unsigned char character : value) {
    if (character == '"' || character == '\\') {
      result.push_back('\\');
      result.push_back(static_cast<char>(character));
    } else if (character == '\b') {
      result += "\\b";
    } else if (character == '\f') {
      result += "\\f";
    } else if (character == '\n') {
      result += "\\n";
    } else if (character == '\r') {
      result += "\\r";
    } else if (character == '\t') {
      result += "\\t";
    } else if (character < 0x20) {
      result += "\\u00";
      result.push_back(hex[character >> 4]);
      result.push_back(hex[character & 0x0f]);
    } else {
      result.push_back(static_cast<char>(character));
    }
  }
  result.push_back('"');
  return result;
}

bool is_residual_vertex(int vertex) {
  return std::find(kResidualVertices.begin(), kResidualVertices.end(), vertex) !=
         kResidualVertices.end();
}

std::vector<std::pair<int, int>> expected_free_pairs() {
  std::vector<std::pair<int, int>> result;
  for (int left = 0; left < kOrder; ++left) {
    for (int right = left + 1; right < kOrder; ++right) {
      if (is_residual_vertex(left) || is_residual_vertex(right))
        result.emplace_back(left, right);
    }
  }
  if (result.size() != 237)
    throw std::runtime_error("internal incident-edge count is not 237");
  return result;
}

std::vector<std::pair<int, int>> metadata_free_pairs(
    const std::string& json) {
  const std::vector<int> flat = integers_in_array(json, "free_edges");
  if (flat.size() % 2 != 0)
    throw std::runtime_error("metadata free_edges contains an incomplete pair");
  std::vector<std::pair<int, int>> result;
  for (size_t index = 0; index < flat.size(); index += 2)
    result.emplace_back(flat[index], flat[index + 1]);
  return result;
}

class SearchState {
 public:
  SearchState()
      : edge_index(kOrder * kOrder, uint16_t{0}),
        edge_left(kEdgeCount),
        edge_right(kEdgeCount),
        incidence(kEdgeCount),
        edge_value(kEdgeCount, 0),
        degree(kOrder, 0) {
    int edge = 0;
    for (int left = 0; left < kOrder; ++left) {
      for (int right = left + 1; right < kOrder; ++right) {
        edge_index[left * kOrder + right] =
            edge_index[right * kOrder + left] = edge;
        edge_left[edge] = left;
        edge_right[edge] = right;
        ++edge;
      }
    }
    const size_t per_edge =
        static_cast<size_t>(kOrder - 2) * (kOrder - 3) * (kOrder - 4) / 6;
    for (auto& list : incidence) list.reserve(per_edge);
    build_five_sets();
    counts.assign(five_sets.size(), 0);
    bad_position.assign(five_sets.size(), -1);
  }

  int edge_for_pair(int left, int right) const {
    if (left > right) std::swap(left, right);
    if (!(0 <= left && left < right && right < kOrder))
      throw std::runtime_error("invalid edge pair");
    return edge_index[left * kOrder + right];
  }

  void set_values(const std::vector<uint8_t>& values) {
    if (values.size() != edge_value.size())
      throw std::runtime_error("graph edge-vector size mismatch");
    edge_value = values;
    std::fill(degree.begin(), degree.end(), 0);
    for (int edge = 0; edge < kEdgeCount; ++edge) {
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
        if (count == 1) ++delta;
        if (count == 10) --delta;
      }
    } else {
      for (uint32_t subset : incidence[edge]) {
        const uint8_t count = counts[subset];
        if (count == 0) --delta;
        if (count == 9) ++delta;
      }
    }
    return delta;
  }

  long long weighted_flip_delta(
      int edge, const std::vector<uint32_t>& weights) const {
    if (weights.size() != five_sets.size())
      throw std::runtime_error("weight-vector size mismatch");
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

  long long full_weighted_objective(
      const std::vector<uint32_t>& weights) const {
    if (weights.size() != five_sets.size())
      throw std::runtime_error("weight-vector size mismatch");
    long long result = 0;
    for (uint32_t subset : bad) result += weights[subset];
    return result;
  }

  void flip(int edge) {
    const bool old_value = edge_value[edge];
    for (uint32_t subset : incidence[edge]) {
      const uint8_t old_count = counts[subset];
      const uint8_t new_count = old_value ? old_count - 1 : old_count + 1;
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
      int edge_count = 0;
      for (uint16_t edge : subset.edges) edge_count += edge_value[edge];
      cliques += edge_count == 10;
      independent += edge_count == 0;
    }
    return {cliques, independent};
  }

  std::vector<int> free_edges_of_random_bad(
      const std::vector<uint8_t>& free_mask, std::mt19937_64& rng) const {
    if (bad.empty()) throw std::runtime_error("no violating subset remains");
    std::uniform_int_distribution<size_t> choose(0, bad.size() - 1);
    const FiveSet& subset = five_sets[bad[choose(rng)]];
    std::vector<int> result;
    for (uint16_t edge : subset.edges)
      if (free_mask[edge]) result.push_back(edge);
    if (result.empty())
      throw std::runtime_error(
          "encountered a fixed-only forbidden set; seed boundary is invalid");
    return result;
  }

  void increment_bad_weights(std::vector<uint32_t>& weights) const {
    if (weights.size() != five_sets.size())
      throw std::runtime_error("weight-vector size mismatch");
    for (uint32_t subset : bad) ++weights[subset];
  }

  int degree_penalty_after_flip(int edge) const {
    constexpr int lower = kOrder - 25;
    constexpr int upper = 24;
    const int change = edge_value[edge] ? -1 : 1;
    int penalty = 0;
    for (int vertex = 0; vertex < kOrder; ++vertex) {
      int value = degree[vertex];
      if (vertex == edge_left[edge] || vertex == edge_right[edge])
        value += change;
      if (value < lower) penalty += lower - value;
      if (value > upper) penalty += value - upper;
    }
    return penalty;
  }

  int objective() const { return static_cast<int>(bad.size()); }
  size_t subset_count() const { return five_sets.size(); }
  const std::vector<uint8_t>& values() const { return edge_value; }

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
    bits.reserve(kEdgeCount);
    for (int right = 1; right < kOrder; ++right)
      for (int left = 0; left < right; ++left)
        bits.push_back(edge_value[edge_index[left * kOrder + right]]);
    while (bits.size() % 6) bits.push_back(0);
    std::string result(1, static_cast<char>(kOrder + 63));
    for (size_t start = 0; start < bits.size(); start += 6) {
      int value = 0;
      for (size_t offset = 0; offset < 6; ++offset)
        value = (value << 1) | bits[start + offset];
      result.push_back(static_cast<char>(value + 63));
    }
    return result;
  }

 private:
  static constexpr int kEdgeCount = kOrder * (kOrder - 1) / 2;
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
    for (int a = 0; a < kOrder - 4; ++a) {
      for (int b = a + 1; b < kOrder - 3; ++b) {
        for (int c = b + 1; c < kOrder - 2; ++c) {
          for (int d = c + 1; d < kOrder - 1; ++d) {
            for (int e = d + 1; e < kOrder; ++e) {
              const std::array<int, 5> vertices{a, b, c, d, e};
              FiveSet subset;
              int cursor = 0;
              for (int left = 0; left < 5; ++left) {
                for (int right = left + 1; right < 5; ++right) {
                  subset.edges[cursor++] = edge_index[
                      vertices[left] * kOrder + vertices[right]];
                }
              }
              const uint32_t index = five_sets.size();
              five_sets.push_back(subset);
              for (uint16_t edge : subset.edges)
                incidence[edge].push_back(index);
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
      for (uint16_t edge : five_sets[index].edges)
        count += edge_value[edge];
      counts[index] = count;
      if (count == 0 || count == 10) add_bad(index);
    }
  }

  void add_bad(uint32_t subset) {
    if (bad_position[subset] != -1)
      throw std::runtime_error("duplicate bad subset");
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

struct Boundary {
  std::vector<int> free_edges;
  std::vector<uint8_t> free_mask;
};

Boundary validate_boundary(const SearchState& state, const GraphSeed& graph,
                           const std::string& metadata_path) {
  const std::string json = read_text(metadata_path);
  if (string_field(json, "base_graph6") != graph.graph6)
    throw std::runtime_error(
        "seed graph does not equal metadata base_graph6");
  const auto expected = expected_free_pairs();
  const auto recorded = metadata_free_pairs(json);
  if (recorded != expected)
    throw std::runtime_error(
        "metadata free_edges does not equal the incident-six edge set");
  if (integer_field(json, "variable_count") != 237)
    throw std::runtime_error("metadata variable_count is not 237");
  const std::vector<int> recorded_incident =
      integers_in_array(json, "incident_free_vertices");
  if (!std::equal(recorded_incident.begin(), recorded_incident.end(),
                  kResidualVertices.begin(), kResidualVertices.end()))
    throw std::runtime_error("metadata incident vertex list disagrees");

  std::vector<int> free_edges;
  std::vector<uint8_t> free_mask(kOrder * (kOrder - 1) / 2, 0);
  for (const auto& [left, right] : recorded) {
    const int edge = state.edge_for_pair(left, right);
    free_edges.push_back(edge);
    free_mask[edge] = 1;
  }
  const std::vector<int> true_variables =
      integers_in_array(json, "base_true_variables");
  std::vector<uint8_t> true_mask(238, 0);
  for (int variable : true_variables) {
    if (!(1 <= variable && variable <= 237) || true_mask[variable])
      throw std::runtime_error("metadata has invalid base_true_variables");
    true_mask[variable] = 1;
  }
  for (int variable = 1; variable <= 237; ++variable) {
    if (graph.edges[free_edges[variable - 1]] != true_mask[variable])
      throw std::runtime_error(
          "seed graph free-edge assignment disagrees with metadata");
  }
  return {std::move(free_edges), std::move(free_mask)};
}

bool fixed_edges_preserved(const std::vector<uint8_t>& candidate,
                           const std::vector<uint8_t>& base,
                           const std::vector<uint8_t>& free_mask) {
  for (size_t edge = 0; edge < candidate.size(); ++edge)
    if (!free_mask[edge] && candidate[edge] != base[edge]) return false;
  return true;
}

int changed_free_edge_count(const std::vector<uint8_t>& candidate,
                            const std::vector<uint8_t>& base,
                            const std::vector<int>& free_edges) {
  int changed = 0;
  for (int edge : free_edges) changed += candidate[edge] != base[edge];
  return changed;
}

void write_graph6(const std::string& path, const std::string& graph6) {
  std::ofstream output(path, std::ios::trunc);
  if (!output) throw std::runtime_error("cannot write " + path);
  output << graph6 << '\n';
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
      options.seed_graph = value();
    else if (option == "--metadata")
      options.metadata = value();
    else if (option == "--output")
      options.output = value();
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
    else if (option == "--restart-perturbation")
      options.restart_perturbation = std::stoi(value());
    else if (option == "--self-check-random-flips")
      options.self_check_random_flips = std::stoi(value());
    else if (option == "--self-check")
      options.self_check = true;
    else
      throw std::runtime_error("unknown option: " + option);
  }
  if (options.seed_graph.empty() || options.metadata.empty())
    throw std::runtime_error("--seed-graph and --metadata are required");
  if (options.steps < 0 || options.restarts < 1 ||
      options.tabu_tenure < 0 || options.random_walk < 0 ||
      options.random_walk > 1 || options.breakout_interval < 0 ||
      options.restart_perturbation < 0 ||
      options.self_check_random_flips < 0)
    throw std::runtime_error("invalid nonnegative search option");
  return options;
}

int run_self_check(const Options& options, const GraphSeed& graph,
                   const Boundary& boundary) {
  const auto started = Clock::now();
  SearchState state;
  state.set_values(graph.edges);
  const auto [base_cliques, base_independent] = state.full_counts();
  if (state.objective() != base_cliques + base_independent)
    throw std::runtime_error("base incremental objective mismatch");
  std::vector<uint32_t> weights(state.subset_count());
  for (size_t subset = 0; subset < weights.size(); ++subset)
    weights[subset] =
        1 + static_cast<uint32_t>((subset * uint64_t{2654435761} +
                                   options.seed) %
                                  17);

  int exhaustive_checks = 0;
  for (int edge : boundary.free_edges) {
    const int before = state.objective();
    const int predicted = state.flip_delta(edge);
    const long long weighted_before = state.full_weighted_objective(weights);
    const long long weighted_predicted =
        state.weighted_flip_delta(edge, weights);
    state.flip(edge);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + predicted ||
        state.objective() != cliques + independent)
      throw std::runtime_error("exhaustive free-edge delta check failed");
    if (state.full_weighted_objective(weights) !=
        weighted_before + weighted_predicted)
      throw std::runtime_error(
          "exhaustive weighted free-edge delta check failed");
    state.flip(edge);
    if (state.objective() != before)
      throw std::runtime_error("free-edge delta rollback failed");
    ++exhaustive_checks;
  }

  std::mt19937_64 rng(options.seed);
  for (int check = 0; check < options.self_check_random_flips; ++check) {
    const int edge =
        boundary.free_edges[static_cast<size_t>(rng() % boundary.free_edges.size())];
    const int before = state.objective();
    const int predicted = state.flip_delta(edge);
    const long long weighted_before = state.full_weighted_objective(weights);
    const long long weighted_predicted =
        state.weighted_flip_delta(edge, weights);
    state.flip(edge);
    const auto [cliques, independent] = state.full_counts();
    if (state.objective() != before + predicted ||
        state.objective() != cliques + independent)
      throw std::runtime_error("random-sequence free-edge delta check failed");
    if (state.full_weighted_objective(weights) !=
        weighted_before + weighted_predicted)
      throw std::runtime_error(
          "random-sequence weighted free-edge delta check failed");
  }
  if (!fixed_edges_preserved(state.values(), graph.edges, boundary.free_mask))
    throw std::runtime_error("self-check changed a fixed edge");
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"self_check\","
            << "\"algorithm\":\"incident_six_lns_v1\","
            << "\"seed\":" << options.seed << ","
            << "\"metadata_free_edges\":" << boundary.free_edges.size() << ","
            << "\"expected_free_edges\":237,"
            << "\"base_C5\":" << base_cliques << ","
            << "\"base_I5\":" << base_independent << ","
            << "\"exhaustive_base_delta_checks\":" << exhaustive_checks << ","
            << "\"exhaustive_weighted_delta_checks\":" << exhaustive_checks
            << ","
            << "\"random_sequence_delta_checks\":"
            << options.self_check_random_flips << ","
            << "\"random_sequence_weighted_delta_checks\":"
            << options.self_check_random_flips << ","
            << "\"fixed_edges_preserved\":true,"
            << "\"runtime_seconds\":" << elapsed << ","
            << "\"status\":\"PASS\"}\n";
  return 0;
}

int run_search(const Options& options, const GraphSeed& graph,
               const Boundary& boundary) {
  const auto started = Clock::now();
  SearchState state;
  std::mt19937_64 rng(options.seed);
  std::uniform_real_distribution<double> unit(0.0, 1.0);
  int global_best = std::numeric_limits<int>::max();
  std::vector<uint8_t> global_values = graph.edges;
  int global_changed_free = -1;
  long long completed_steps = 0;
  long long delta_evaluations = 0;
  long long penalty_updates = 0;
  int improvement_count = 0;
  int equal_best_diversity_updates = 0;

  for (int restart = 0; restart < options.restarts && global_best > 0;
       ++restart) {
    state.set_values(graph.edges);
    if (restart > 0) {
      for (int flip = 0; flip < options.restart_perturbation; ++flip) {
        const int edge = boundary.free_edges[
            static_cast<size_t>(rng() % boundary.free_edges.size())];
        state.flip(edge);
      }
    }
    std::vector<long long> tabu(kOrder * (kOrder - 1) / 2, 0);
    std::vector<uint32_t> weights(state.subset_count(), 1);
    int restart_best = state.objective();
    long long next_breakout = options.breakout_interval;
    if (state.objective() < global_best) {
      global_best = state.objective();
      global_values = state.values();
      global_changed_free = changed_free_edge_count(
          state.values(), graph.edges, boundary.free_edges);
      ++improvement_count;
      std::cerr << "best restart=" << restart << " step=0 E=" << global_best
                << '\n';
    } else if (state.objective() == global_best) {
      const int changed = changed_free_edge_count(
          state.values(), graph.edges, boundary.free_edges);
      if (changed > global_changed_free) {
        global_values = state.values();
        global_changed_free = changed;
        ++equal_best_diversity_updates;
      }
    }

    for (long long step = 0;
         step < options.steps && state.objective() > 0; ++step) {
      const std::vector<int> choices =
          state.free_edges_of_random_bad(boundary.free_mask, rng);
      int selected = -1;
      int selected_delta = std::numeric_limits<int>::max();
      long long selected_weighted = std::numeric_limits<long long>::max();
      int selected_degree_penalty = std::numeric_limits<int>::max();

      if (unit(rng) < options.random_walk) {
        std::vector<int> allowed;
        for (int edge : choices)
          if (tabu[edge] <= step) allowed.push_back(edge);
        const std::vector<int>& pool = allowed.empty() ? choices : allowed;
        selected = pool[static_cast<size_t>(rng() % pool.size())];
        selected_delta = state.flip_delta(selected);
        ++delta_evaluations;
      } else {
        for (int edge : choices) {
          const int delta = state.flip_delta(edge);
          const long long weighted =
              options.breakout_interval > 0
                  ? state.weighted_flip_delta(edge, weights)
                  : delta;
          ++delta_evaluations;
          const bool aspiration = state.objective() + delta < global_best;
          if (tabu[edge] > step && !aspiration) continue;
          const int degree_penalty = state.degree_penalty_after_flip(edge);
          if (weighted < selected_weighted ||
              (weighted == selected_weighted && delta < selected_delta) ||
              (weighted == selected_weighted && delta == selected_delta &&
               degree_penalty < selected_degree_penalty) ||
              (weighted == selected_weighted && delta == selected_delta &&
               degree_penalty == selected_degree_penalty && unit(rng) < 0.5)) {
            selected = edge;
            selected_delta = delta;
            selected_weighted = weighted;
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
      } else if (options.breakout_interval > 0 &&
                 step + 1 >= next_breakout) {
        state.increment_bad_weights(weights);
        ++penalty_updates;
        next_breakout += options.breakout_interval;
      }

      if (state.objective() < global_best) {
        global_best = state.objective();
        global_values = state.values();
        global_changed_free = changed_free_edge_count(
            state.values(), graph.edges, boundary.free_edges);
        ++improvement_count;
        std::cerr << "best restart=" << restart << " step=" << step + 1
                  << " E=" << global_best << '\n';
      } else if (state.objective() == global_best) {
        const int changed = changed_free_edge_count(
            state.values(), graph.edges, boundary.free_edges);
        if (changed > global_changed_free) {
          global_values = state.values();
          global_changed_free = changed;
          ++equal_best_diversity_updates;
        }
      }
    }
  }

  state.set_values(global_values);
  const auto [cliques, independent] = state.full_counts();
  if (cliques + independent != global_best)
    throw std::runtime_error("final full objective mismatch");
  if (!fixed_edges_preserved(state.values(), graph.edges, boundary.free_mask))
    throw std::runtime_error("search changed a fixed edge");
  write_graph6(options.output, state.graph6());
  const int changed_free =
      changed_free_edge_count(state.values(), graph.edges, boundary.free_edges);
  const double elapsed =
      std::chrono::duration<double>(Clock::now() - started).count();
  const std::vector<int> degrees = state.sorted_degrees();

  std::cout << std::fixed << std::setprecision(6)
            << "{\"mode\":\"search\","
            << "\"algorithm\":\"incident_six_lns_v1\","
            << "\"seed\":" << options.seed << ","
            << "\"steps_requested_per_restart\":" << options.steps << ","
            << "\"restarts\":" << options.restarts << ","
            << "\"steps_executed\":" << completed_steps << ","
            << "\"delta_evaluations\":" << delta_evaluations << ","
            << "\"tabu_tenure\":" << options.tabu_tenure << ","
            << "\"random_walk\":" << options.random_walk << ","
            << "\"breakout_interval\":" << options.breakout_interval << ","
            << "\"restart_perturbation\":" << options.restart_perturbation
            << ",\"penalty_updates\":" << penalty_updates << ","
            << "\"free_edge_count\":" << boundary.free_edges.size() << ","
            << "\"fixed_edge_count\":666,"
            << "\"fixed_edges_preserved\":true,"
            << "\"changed_free_edges\":" << changed_free << ","
            << "\"runtime_seconds\":" << elapsed << ","
            << "\"improvements\":" << improvement_count << ","
            << "\"equal_best_diversity_updates\":"
            << equal_best_diversity_updates << ","
            << "\"C5\":" << cliques << ",\"I5\":" << independent << ","
            << "\"E\":" << global_best << ","
            << "\"edge_count\":" << state.edge_count() << ","
            << "\"degree_sequence\":[";
  for (size_t index = 0; index < degrees.size(); ++index) {
    if (index) std::cout << ',';
    std::cout << degrees[index];
  }
  std::cout << "],\"graph6\":" << json_quote(state.graph6()) << ","
            << "\"seed_graph\":" << json_quote(options.seed_graph) << ","
            << "\"metadata\":" << json_quote(options.metadata) << ","
            << "\"output\":" << json_quote(options.output) << "}\n";
  return 0;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    SearchState state;
    const GraphSeed graph = decode_graph6(first_data_line(options.seed_graph));
    const Boundary boundary =
        validate_boundary(state, graph, options.metadata);
    if (options.self_check)
      return run_self_check(options, graph, boundary);
    return run_search(options, graph, boundary);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
