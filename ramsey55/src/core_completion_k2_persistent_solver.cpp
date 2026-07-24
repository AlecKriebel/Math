// Bounded persistent constructive solver for delete-two/add-three completions.
//
// For each selected pair of deleted vertices from a fixed (5,5;42) catalog
// graph, retain the induced 40-vertex core and add vertices A, B, C.
// Variables:
//   0..39    A--core
//   40..79   B--core
//   80..119  C--core
//   120      A--B
//   121      A--C
//   122      B--C
//
// The solver emits one flushed JSON record per selected fixed core.  It
// stops immediately on SAT so the orchestration layer can preserve and
// independently verify the model.  UNSAT statuses carry no proof and must be
// treated only as reproducible computational observations.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;
using Mask = unsigned __int128;

constexpr int kInputOrder = 42;
constexpr int kCoreOrder = 40;
constexpr int kNewVertices = 3;
constexpr int kVariableCount = 123;
constexpr int kAB = 120;
constexpr int kAC = 121;
constexpr int kBC = 122;

struct Clause {
  Mask mask{};
  bool positive{};
};

struct Graph {
  int order{};
  std::vector<uint64_t> adjacency;
};

struct PairSelection {
  uint32_t catalog_line{};
  int deleted_left{};
  int deleted_right{};
};

struct ClauseCounts {
  uint64_t core_k4{};
  uint64_t core_i4{};
  uint64_t core_k3{};
  uint64_t core_i3{};
  uint64_t core_edges{};
  uint64_t core_nonedges{};
  uint64_t one_new_negative{};
  uint64_t one_new_positive{};
  uint64_t two_new_negative{};
  uint64_t two_new_positive{};
  uint64_t three_new_negative{};
  uint64_t three_new_positive{};
  uint64_t negative{};
  uint64_t positive{};
};

struct Options {
  std::string graph_path;
  std::string pairs_path;
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
};

struct SearchResult {
  enum Value { kSat, kUnsat, kLimit } value{kLimit};
  Mask true_mask{};
  Mask false_mask{};
};

uint64_t parse_u64(const char* text, const std::string& label) {
  char* end = nullptr;
  const unsigned long long value = std::strtoull(text, &end, 10);
  if (!end || *end) throw std::runtime_error("invalid " + label);
  return static_cast<uint64_t>(value);
}

double parse_double(const char* text, const std::string& label) {
  char* end = nullptr;
  const double value = std::strtod(text, &end);
  if (!end || *end || value < 0)
    throw std::runtime_error("invalid " + label);
  return value;
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    auto value = [&](const std::string& name) -> const char* {
      if (++i >= argc) throw std::runtime_error(name + " requires a value");
      return argv[i];
    };
    if (arg == "--graph")
      options.graph_path = value(arg);
    else if (arg == "--pairs")
      options.pairs_path = value(arg);
    else if (arg == "--node-limit")
      options.node_limit = parse_u64(value(arg), arg);
    else if (arg == "--seconds-limit")
      options.seconds_limit = parse_double(value(arg), arg);
    else
      throw std::runtime_error("unknown option: " + arg);
  }
  if (options.graph_path.empty() || options.pairs_path.empty())
    throw std::runtime_error("--graph and --pairs are required");
  if (options.node_limit == 0)
    throw std::runtime_error("--node-limit must be positive");
  if (!(options.seconds_limit > 0))
    throw std::runtime_error("--seconds-limit must be positive");
  return options;
}

std::vector<std::string> load_catalog(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph catalog");
  std::vector<std::string> lines;
  std::string line;
  while (std::getline(input, line)) {
    const size_t first = line.find_first_not_of(" \t\r\n");
    if (first == std::string::npos || line[first] == '#') continue;
    const size_t last = line.find_last_not_of(" \t\r\n");
    lines.push_back(line.substr(first, last - first + 1));
  }
  if (lines.empty()) throw std::runtime_error("catalog has no data line");
  return lines;
}

std::vector<PairSelection> load_pairs(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open pair list");
  std::vector<PairSelection> pairs;
  std::set<std::array<uint64_t, 3>> seen;
  std::string line;
  uint64_t physical_line = 0;
  while (std::getline(input, line)) {
    ++physical_line;
    const size_t first = line.find_first_not_of(" \t\r\n");
    if (first == std::string::npos || line[first] == '#') continue;
    std::istringstream parsed(line);
    uint64_t catalog_line = 0;
    int deleted_left = -1;
    int deleted_right = -1;
    std::string extra;
    if (!(parsed >> catalog_line >> deleted_left >> deleted_right) ||
        (parsed >> extra))
      throw std::runtime_error(
          "invalid pair-list record at physical line " +
          std::to_string(physical_line));
    if (catalog_line == 0 ||
        catalog_line > std::numeric_limits<uint32_t>::max())
      throw std::runtime_error("catalog line is outside 1..2^32-1");
    if (deleted_left < 0 || deleted_right >= kInputOrder ||
        deleted_left >= deleted_right)
      throw std::runtime_error(
          "deleted labels must satisfy 0 <= left < right < 42");
    const std::array<uint64_t, 3> key{
        catalog_line, static_cast<uint64_t>(deleted_left),
        static_cast<uint64_t>(deleted_right)};
    if (!seen.insert(key).second)
      throw std::runtime_error("pair list contains a duplicate");
    pairs.push_back(
        {static_cast<uint32_t>(catalog_line), deleted_left, deleted_right});
  }
  if (pairs.empty()) throw std::runtime_error("pair list is empty");
  return pairs;
}

Graph decode_graph6(const std::string& raw) {
  std::string encoded = raw;
  if (encoded.rfind(">>graph6<<", 0) == 0) encoded.erase(0, 10);
  if (encoded.empty()) throw std::runtime_error("empty graph6 record");
  const int order = static_cast<unsigned char>(encoded[0]) - 63;
  if (order < 0 || order > 62)
    throw std::runtime_error("only short graph6 inputs are supported");
  const int required_bits = order * (order - 1) / 2;
  if (6 * static_cast<int>(encoded.size() - 1) < required_bits)
    throw std::runtime_error("truncated graph6 record");
  Graph graph{order, std::vector<uint64_t>(order, 0)};
  int bit_index = 0;
  for (int right = 1; right < order; ++right) {
    for (int left = 0; left < right; ++left) {
      const int chunk =
          static_cast<unsigned char>(encoded[1 + bit_index / 6]) - 63;
      if (chunk < 0 || chunk >= 64)
        throw std::runtime_error("invalid graph6 payload byte");
      if ((chunk >> (5 - bit_index % 6)) & 1) {
        graph.adjacency[left] |= uint64_t{1} << right;
        graph.adjacency[right] |= uint64_t{1} << left;
      }
      ++bit_index;
    }
  }
  return graph;
}

bool edge(const Graph& graph, int left, int right) {
  return (graph.adjacency[left] >> right) & 1;
}

Graph delete_two_vertices(const Graph& input, int deleted_left,
                          int deleted_right) {
  if (input.order != kInputOrder || deleted_left < 0 ||
      deleted_right >= input.order || deleted_left >= deleted_right)
    throw std::runtime_error("invalid delete-two selection");
  std::array<int, kCoreOrder> retained{};
  int cursor = 0;
  for (int vertex = 0; vertex < input.order; ++vertex)
    if (vertex != deleted_left && vertex != deleted_right)
      retained[cursor++] = vertex;
  if (cursor != kCoreOrder)
    throw std::runtime_error("delete-two core order mismatch");
  Graph core{kCoreOrder, std::vector<uint64_t>(kCoreOrder, 0)};
  for (int left = 0; left < kCoreOrder; ++left) {
    for (int right = left + 1; right < kCoreOrder; ++right) {
      if (edge(input, retained[left], retained[right])) {
        core.adjacency[left] |= uint64_t{1} << right;
        core.adjacency[right] |= uint64_t{1} << left;
      }
    }
  }
  return core;
}

std::vector<Clause> build_clauses(const Graph& core, ClauseCounts& counts) {
  if (core.order != kCoreOrder)
    throw std::runtime_error("core order is not 40");
  std::vector<Clause> clauses;

  // One new vertex plus a homogeneous core 4-set.
  for (int a = 0; a < kCoreOrder - 3; ++a)
    for (int b = a + 1; b < kCoreOrder - 2; ++b)
      for (int c = b + 1; c < kCoreOrder - 1; ++c)
        for (int d = c + 1; d < kCoreOrder; ++d) {
          const int edges =
              edge(core, a, b) + edge(core, a, c) + edge(core, a, d) +
              edge(core, b, c) + edge(core, b, d) + edge(core, c, d);
          if (edges != 0 && edges != 6) continue;
          const bool positive = edges == 0;
          for (int added = 0; added < kNewVertices; ++added) {
            const int offset = added * kCoreOrder;
            const Mask mask =
                (Mask{1} << (offset + a)) |
                (Mask{1} << (offset + b)) |
                (Mask{1} << (offset + c)) |
                (Mask{1} << (offset + d));
            clauses.push_back({mask, positive});
          }
          if (positive)
            ++counts.core_i4;
          else
            ++counts.core_k4;
        }

  // Two new vertices plus a homogeneous core triple.
  const std::array<std::array<int, 3>, 3> new_pairs{{
      {{0, 1, kAB}},
      {{0, 2, kAC}},
      {{1, 2, kBC}},
  }};
  for (int a = 0; a < kCoreOrder - 2; ++a)
    for (int b = a + 1; b < kCoreOrder - 1; ++b)
      for (int c = b + 1; c < kCoreOrder; ++c) {
        const int edges =
            edge(core, a, b) + edge(core, a, c) + edge(core, b, c);
        if (edges != 0 && edges != 3) continue;
        const bool positive = edges == 0;
        for (const auto& selected : new_pairs) {
          Mask mask = Mask{1} << selected[2];
          for (int vertex : {a, b, c}) {
            mask |= Mask{1}
                    << (selected[0] * kCoreOrder + vertex);
            mask |= Mask{1}
                    << (selected[1] * kCoreOrder + vertex);
          }
          clauses.push_back({mask, positive});
        }
        if (positive)
          ++counts.core_i3;
        else
          ++counts.core_k3;
      }

  // All three new vertices plus one fixed core pair.
  const Mask new_triangle =
      (Mask{1} << kAB) | (Mask{1} << kAC) | (Mask{1} << kBC);
  for (int left = 0; left < kCoreOrder - 1; ++left) {
    for (int right = left + 1; right < kCoreOrder; ++right) {
      const bool positive = !edge(core, left, right);
      Mask mask = new_triangle;
      for (int added = 0; added < kNewVertices; ++added) {
        const int offset = added * kCoreOrder;
        mask |= Mask{1} << (offset + left);
        mask |= Mask{1} << (offset + right);
      }
      clauses.push_back({mask, positive});
      if (positive)
        ++counts.core_nonedges;
      else
        ++counts.core_edges;
    }
  }

  counts.one_new_negative = 3 * counts.core_k4;
  counts.one_new_positive = 3 * counts.core_i4;
  counts.two_new_negative = 3 * counts.core_k3;
  counts.two_new_positive = 3 * counts.core_i3;
  counts.three_new_negative = counts.core_edges;
  counts.three_new_positive = counts.core_nonedges;
  counts.negative = counts.one_new_negative + counts.two_new_negative +
                    counts.three_new_negative;
  counts.positive = counts.one_new_positive + counts.two_new_positive +
                    counts.three_new_positive;
  if (counts.negative + counts.positive != clauses.size())
    throw std::runtime_error("clause-count accounting mismatch");
  return clauses;
}

int popcount(Mask value) {
  return __builtin_popcountll(static_cast<uint64_t>(value)) +
         __builtin_popcountll(static_cast<uint64_t>(value >> 64));
}

int trailing_zeroes(Mask value) {
  const uint64_t low = static_cast<uint64_t>(value);
  if (low) return __builtin_ctzll(low);
  return 64 + __builtin_ctzll(static_cast<uint64_t>(value >> 64));
}

class Solver {
 public:
  Solver(const std::vector<Clause>& clauses, uint64_t node_limit,
         double seconds_limit)
      : clauses_(clauses),
        node_limit_(node_limit),
        seconds_limit_(seconds_limit),
        started_(Clock::now()),
        all_mask_((Mask{1} << kVariableCount) - 1) {}

  SearchResult run() { return search(0, 0, 0); }
  uint64_t nodes() const { return nodes_; }
  uint64_t branches() const { return branches_; }
  uint64_t leaves() const { return leaves_; }
  uint64_t unit_assignments() const { return unit_assignments_; }
  int max_depth() const { return max_depth_; }
  double elapsed() const {
    return std::chrono::duration<double>(Clock::now() - started_).count();
  }

 private:
  const std::vector<Clause>& clauses_;
  uint64_t node_limit_;
  double seconds_limit_;
  Clock::time_point started_;
  Mask all_mask_;
  uint64_t nodes_{};
  uint64_t branches_{};
  uint64_t leaves_{};
  uint64_t unit_assignments_{};
  int max_depth_{};
  bool limit_hit_{};

  bool over_limit() {
    if (limit_hit_) return true;
    if (nodes_ >= node_limit_ || elapsed() >= seconds_limit_) {
      limit_hit_ = true;
      return true;
    }
    return false;
  }

  bool propagate(Mask& true_mask, Mask& false_mask) {
    while (true) {
      bool changed = false;
      const Mask assigned = true_mask | false_mask;
      for (const Clause& clause : clauses_) {
        const Mask satisfying =
            clause.positive ? clause.mask & true_mask
                            : clause.mask & false_mask;
        if (satisfying) continue;
        const Mask remaining = clause.mask & ~assigned;
        if (!remaining) return false;
        if ((remaining & (remaining - 1)) == 0) {
          if (clause.positive)
            true_mask |= remaining;
          else
            false_mask |= remaining;
          ++unit_assignments_;
          changed = true;
          break;
        }
      }
      if (!changed) return true;
    }
  }

  int choose_variable(Mask true_mask, Mask false_mask,
                      bool& true_first) const {
    const Mask assigned = true_mask | false_mask;
    std::array<uint64_t, kVariableCount> positive{};
    std::array<uint64_t, kVariableCount> negative{};
    for (const Clause& clause : clauses_) {
      const Mask satisfying =
          clause.positive ? clause.mask & true_mask
                          : clause.mask & false_mask;
      if (satisfying) continue;
      Mask remaining = clause.mask & ~assigned;
      const int width = popcount(remaining);
      const uint64_t weight = uint64_t{1} << (14 - width);
      while (remaining) {
        const int variable = trailing_zeroes(remaining);
        remaining &= remaining - 1;
        (clause.positive ? positive[variable] : negative[variable]) +=
            weight;
      }
    }
    int best = -1;
    unsigned __int128 best_product = 0;
    uint64_t best_sum = 0;
    Mask unset = all_mask_ & ~assigned;
    while (unset) {
      const int variable = trailing_zeroes(unset);
      unset &= unset - 1;
      const unsigned __int128 product =
          static_cast<unsigned __int128>(positive[variable] + 1) *
          static_cast<unsigned __int128>(negative[variable] + 1);
      const uint64_t sum = positive[variable] + negative[variable];
      if (best < 0 || product > best_product ||
          (product == best_product && sum > best_sum) ||
          (product == best_product && sum == best_sum &&
           variable < best)) {
        best = variable;
        best_product = product;
        best_sum = sum;
      }
    }
    if (best < 0) throw std::runtime_error("no unset branch variable");
    true_first = positive[best] >= negative[best];
    return best;
  }

  SearchResult search(Mask true_mask, Mask false_mask, int depth) {
    if (over_limit()) return {SearchResult::kLimit, 0, 0};
    ++nodes_;
    max_depth_ = std::max(max_depth_, depth);
    if (!propagate(true_mask, false_mask)) {
      ++leaves_;
      return {SearchResult::kUnsat, 0, 0};
    }
    if ((true_mask | false_mask) == all_mask_)
      return {SearchResult::kSat, true_mask, false_mask};
    bool true_first = false;
    const int variable =
        choose_variable(true_mask, false_mask, true_first);
    ++branches_;
    const Mask selected = Mask{1} << variable;
    if (true_first) {
      SearchResult result =
          search(true_mask | selected, false_mask, depth + 1);
      if (result.value != SearchResult::kUnsat) return result;
      return search(true_mask, false_mask | selected, depth + 1);
    }
    SearchResult result =
        search(true_mask, false_mask | selected, depth + 1);
    if (result.value != SearchResult::kUnsat) return result;
    return search(true_mask | selected, false_mask, depth + 1);
  }
};

void print_true_variables(Mask mask) {
  bool first = true;
  while (mask) {
    const int variable = trailing_zeroes(mask);
    mask &= mask - 1;
    if (!first) std::cout << ',';
    first = false;
    std::cout << variable;
  }
}

void print_result(const PairSelection& selected, const ClauseCounts& counts,
                  const std::vector<Clause>& clauses, const Solver& solver,
                  const SearchResult& result) {
  const char* status = result.value == SearchResult::kSat
                           ? "SAT"
                           : (result.value == SearchResult::kUnsat ? "UNSAT"
                                                                   : "LIMIT");
  std::cout << "{\"record_type\":\"PAIR\",\"status\":\"" << status
            << "\",\"catalog_line\":" << selected.catalog_line
            << ",\"deleted_left\":" << selected.deleted_left
            << ",\"deleted_right\":" << selected.deleted_right
            << ",\"input_n\":" << kInputOrder
            << ",\"core_n\":" << kCoreOrder
            << ",\"added_vertices\":3,\"variables\":" << kVariableCount
            << ",\"core_k4\":" << counts.core_k4
            << ",\"core_i4\":" << counts.core_i4
            << ",\"core_k3\":" << counts.core_k3
            << ",\"core_i3\":" << counts.core_i3
            << ",\"core_edges\":" << counts.core_edges
            << ",\"core_nonedges\":" << counts.core_nonedges
            << ",\"negative_clauses\":" << counts.negative
            << ",\"positive_clauses\":" << counts.positive
            << ",\"clauses\":" << clauses.size()
            << ",\"nodes\":" << solver.nodes()
            << ",\"branches\":" << solver.branches()
            << ",\"leaves\":" << solver.leaves()
            << ",\"unit_assignments\":" << solver.unit_assignments()
            << ",\"max_depth\":" << solver.max_depth()
            << ",\"elapsed_seconds\":" << std::fixed
            << std::setprecision(6) << solver.elapsed();
  if (result.value == SearchResult::kSat) {
    std::cout << ",\"true_variables\":[";
    print_true_variables(result.true_mask);
    std::cout << ']';
  }
  std::cout << "}\n" << std::flush;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const std::vector<std::string> catalog = load_catalog(options.graph_path);
    const std::vector<PairSelection> pairs = load_pairs(options.pairs_path);
    uint64_t unsat_count = 0;
    uint64_t limit_count = 0;
    for (const PairSelection& selected : pairs) {
      if (selected.catalog_line > catalog.size())
        throw std::runtime_error("pair list selects an absent catalog line");
      const Graph input =
          decode_graph6(catalog[selected.catalog_line - 1]);
      const Graph core = delete_two_vertices(
          input, selected.deleted_left, selected.deleted_right);
      ClauseCounts counts;
      const std::vector<Clause> clauses = build_clauses(core, counts);
      Solver solver(clauses, options.node_limit, options.seconds_limit);
      const SearchResult result = solver.run();
      print_result(selected, counts, clauses, solver, result);
      if (result.value == SearchResult::kSat) {
        std::cout << "{\"record_type\":\"RUN\",\"status\":\"SAT_STOP\","
                  << "\"completed_pairs\":" << (unsat_count + limit_count + 1)
                  << ",\"requested_pairs\":" << pairs.size() << "}\n";
        return 10;
      }
      unsat_count += result.value == SearchResult::kUnsat;
      limit_count += result.value == SearchResult::kLimit;
    }
    std::cout << "{\"record_type\":\"RUN\",\"status\":\""
              << (limit_count ? "COMPLETE_WITH_LIMITS" : "COMPLETE")
              << "\",\"requested_pairs\":" << pairs.size()
              << ",\"unsat_count\":" << unsat_count
              << ",\"limit_count\":" << limit_count << "}\n";
    return limit_count ? 2 : 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
