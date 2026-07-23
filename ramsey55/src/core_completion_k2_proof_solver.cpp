// Exact solver and compact exhaustive-tree proof producer for one fixed
// k=2 Ramsey core-completion instance.
//
// Starting with the supplied 42-vertex graph, delete original vertices 0 and
// 1, retain the resulting labeled 40-vertex induced core, and add three
// labeled vertices A, B, C.  The 123 Boolean variables are:
//
//   0..39    A--core edges
//   40..79   B--core edges
//   80..119  C--core edges
//   120      A--B
//   121      A--C
//   122      B--C
//
// A true variable means that the corresponding edge is present.  For every
// five-set containing at least one new vertex, a monotone clause forbids all
// ten pairs from being edges, and another applicable monotone clause forbids
// all ten pairs from being nonedges.  Fixed core pairs make a clause
// applicable exactly when they are homogeneous.
//
// The proof is a preorder full binary DPLL tree.  A payload byte in 0..122
// branches on that variable, false child first and true child second.  Byte
// 255 is a leaf at which repeated unit propagation on the original clauses
// conflicts.  No learned clause is emitted or trusted.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;
using Mask = unsigned __int128;

constexpr int kInputOrder = 42;
constexpr int kDeletedFirst = 0;
constexpr int kDeletedSecond = 1;
constexpr int kCoreOrder = 40;
constexpr int kNewCount = 3;
constexpr int kVariableCount = 123;
constexpr uint8_t kLeaf = 0xff;

struct Graph {
  int order{};
  std::vector<uint64_t> adjacency;
};

struct Clause {
  Mask mask{};
  bool positive{};  // positive: OR x_i; negative: OR !x_i.
};

struct Counts {
  uint64_t core_k5{};
  uint64_t core_i5{};
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
};

struct Options {
  std::string graph_path;
  std::string proof_path;
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t progress_interval = 100000;
};

struct SearchResult {
  enum Value { kSat, kUnsat, kLimit } value{kLimit};
  Mask true_mask{};
  Mask false_mask{};
};

int popcount(Mask value) {
  return __builtin_popcountll(static_cast<uint64_t>(value)) +
         __builtin_popcountll(static_cast<uint64_t>(value >> 64));
}

int trailing_zeroes(Mask value) {
  const uint64_t low = static_cast<uint64_t>(value);
  if (low) return __builtin_ctzll(low);
  return 64 + __builtin_ctzll(static_cast<uint64_t>(value >> 64));
}

std::string first_data_line(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph: " + path);
  std::string line;
  while (std::getline(input, line)) {
    while (!line.empty() && line.back() == '\r') line.pop_back();
    if (!line.empty() && line[0] != '#') return line;
  }
  throw std::runtime_error("graph file has no data line");
}

Graph decode_short_graph6(std::string line) {
  if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
  if (line.empty()) throw std::runtime_error("empty graph6 input");
  const int order = static_cast<unsigned char>(line[0]) - 63;
  if (order < 0 || order > 62)
    throw std::runtime_error("only short graph6 inputs are supported");
  const int required_bits = order * (order - 1) / 2;
  if (6 * static_cast<int>(line.size() - 1) < required_bits)
    throw std::runtime_error("truncated graph6 input");

  std::vector<uint64_t> adjacency(order, 0);
  int bit_index = 0;
  for (int right = 1; right < order; ++right) {
    for (int left = 0; left < right; ++left) {
      const int value =
          static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64)
        throw std::runtime_error("invalid graph6 payload byte");
      if ((value >> (5 - bit_index % 6)) & 1) {
        adjacency[left] |= uint64_t{1} << right;
        adjacency[right] |= uint64_t{1} << left;
      }
      ++bit_index;
    }
  }
  return {order, std::move(adjacency)};
}

Graph fixed_core(const Graph& input) {
  if (input.order != kInputOrder)
    throw std::runtime_error("this experiment requires a 42-vertex input");
  std::vector<int> retained;
  for (int vertex = 0; vertex < input.order; ++vertex)
    if (vertex != kDeletedFirst && vertex != kDeletedSecond)
      retained.push_back(vertex);
  if (static_cast<int>(retained.size()) != kCoreOrder)
    throw std::runtime_error("internal retained-vertex count mismatch");

  std::vector<uint64_t> adjacency(kCoreOrder, 0);
  for (int left = 0; left < kCoreOrder; ++left) {
    for (int right = left + 1; right < kCoreOrder; ++right) {
      if ((input.adjacency[retained[left]] >> retained[right]) & 1) {
        adjacency[left] |= uint64_t{1} << right;
        adjacency[right] |= uint64_t{1} << left;
      }
    }
  }
  return {kCoreOrder, std::move(adjacency)};
}

bool edge(const Graph& graph, int left, int right) {
  return (graph.adjacency[left] >> right) & 1;
}

void check_core(const Graph& core, Counts& counts) {
  for (int a = 0; a < core.order - 4; ++a)
    for (int b = a + 1; b < core.order - 3; ++b)
      for (int c = b + 1; c < core.order - 2; ++c)
        for (int d = c + 1; d < core.order - 1; ++d)
          for (int e = d + 1; e < core.order; ++e) {
            const std::array<int, 5> vertices{a, b, c, d, e};
            int edge_count = 0;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j)
                edge_count += edge(core, vertices[i], vertices[j]);
            counts.core_k5 += edge_count == 10;
            counts.core_i5 += edge_count == 0;
          }
  if (counts.core_k5 || counts.core_i5)
    throw std::runtime_error("the fixed core already violates (5,5)");
}

int new_pair_variable(int first, int second) {
  if (first > second) std::swap(first, second);
  if (first == 0 && second == 1) return 120;
  if (first == 0 && second == 2) return 121;
  if (first == 1 && second == 2) return 122;
  throw std::runtime_error("invalid pair of new vertices");
}

Mask incident_mask(const std::vector<int>& core_vertices,
                   const std::vector<int>& new_vertices) {
  Mask result = 0;
  for (int new_vertex : new_vertices)
    for (int core_vertex : core_vertices)
      result |= Mask{1} << (new_vertex * kCoreOrder + core_vertex);
  for (int left = 0; left < static_cast<int>(new_vertices.size()); ++left)
    for (int right = left + 1;
         right < static_cast<int>(new_vertices.size()); ++right)
      result |= Mask{1}
                << new_pair_variable(new_vertices[left],
                                     new_vertices[right]);
  return result;
}

std::vector<Clause> build_formula(const Graph& core, Counts& counts) {
  std::vector<Clause> clauses;

  // One new vertex plus a homogeneous core 4-set: three width-4 clauses.
  for (int a = 0; a < core.order - 3; ++a)
    for (int b = a + 1; b < core.order - 2; ++b)
      for (int c = b + 1; c < core.order - 1; ++c)
        for (int d = c + 1; d < core.order; ++d) {
          const std::array<int, 4> vertices{a, b, c, d};
          int edge_count = 0;
          for (int i = 0; i < 4; ++i)
            for (int j = i + 1; j < 4; ++j)
              edge_count += edge(core, vertices[i], vertices[j]);
          if (edge_count != 0 && edge_count != 6) continue;
          const bool positive = edge_count == 0;
          for (int new_vertex = 0; new_vertex < kNewCount; ++new_vertex) {
            const Mask mask =
                (Mask{1} << a | Mask{1} << b | Mask{1} << c |
                 Mask{1} << d)
                << (new_vertex * kCoreOrder);
            clauses.push_back({mask, positive});
          }
          if (positive)
            ++counts.core_i4;
          else
            ++counts.core_k4;
        }

  // Two new vertices plus a homogeneous core triple: three width-7 clauses.
  for (int a = 0; a < core.order - 2; ++a)
    for (int b = a + 1; b < core.order - 1; ++b)
      for (int c = b + 1; c < core.order; ++c) {
        const int edge_count =
            edge(core, a, b) + edge(core, a, c) + edge(core, b, c);
        if (edge_count != 0 && edge_count != 3) continue;
        const bool positive = edge_count == 0;
        const std::vector<int> core_vertices{a, b, c};
        for (int first = 0; first < kNewCount - 1; ++first)
          for (int second = first + 1; second < kNewCount; ++second)
            clauses.push_back(
                {incident_mask(core_vertices, {first, second}), positive});
        if (positive)
          ++counts.core_i3;
        else
          ++counts.core_k3;
      }

  // All three new vertices plus a core pair: every fixed core pair is
  // homogeneous, yielding one width-9 clause.
  for (int left = 0; left < core.order - 1; ++left)
    for (int right = left + 1; right < core.order; ++right) {
      const bool fixed_edge = edge(core, left, right);
      clauses.push_back(
          {incident_mask({left, right}, {0, 1, 2}), !fixed_edge});
      if (fixed_edge)
        ++counts.core_edges;
      else
        ++counts.core_nonedges;
    }

  counts.one_new_negative = 3 * counts.core_k4;
  counts.one_new_positive = 3 * counts.core_i4;
  counts.two_new_negative = 3 * counts.core_k3;
  counts.two_new_positive = 3 * counts.core_i3;
  counts.three_new_negative = counts.core_edges;
  counts.three_new_positive = counts.core_nonedges;
  return clauses;
}

class Solver {
 public:
  Solver(const std::vector<Clause>& clauses, const Options& options,
         std::ostream* proof)
      : clauses_(clauses),
        options_(options),
        proof_(proof),
        start_(Clock::now()),
        all_mask_((Mask{1} << kVariableCount) - 1) {}

  SearchResult run() { return search(0, 0, 0); }
  uint64_t nodes() const { return nodes_; }
  uint64_t branches() const { return branches_; }
  uint64_t leaves() const { return leaves_; }
  uint64_t unit_assignments() const { return unit_assignments_; }
  int max_depth() const { return max_depth_; }
  double elapsed() const {
    return std::chrono::duration<double>(Clock::now() - start_).count();
  }

 private:
  const std::vector<Clause>& clauses_;
  const Options& options_;
  std::ostream* proof_;
  Clock::time_point start_;
  Mask all_mask_;
  uint64_t nodes_ = 0;
  uint64_t branches_ = 0;
  uint64_t leaves_ = 0;
  uint64_t unit_assignments_ = 0;
  int max_depth_ = 0;
  bool limit_hit_ = false;

  bool over_limit() {
    if (limit_hit_) return true;
    if (nodes_ >= options_.node_limit || elapsed() >= options_.seconds_limit) {
      limit_hit_ = true;
      return true;
    }
    return false;
  }

  bool propagate(Mask& true_mask, Mask& false_mask) {
    while (true) {
      const Mask assigned = true_mask | false_mask;
      Mask force_true = 0;
      Mask force_false = 0;
      for (const Clause& clause : clauses_) {
        if (clause.mask &
            (clause.positive ? true_mask : false_mask))
          continue;
        const Mask remaining = clause.mask & ~assigned;
        if (!remaining) return false;
        if ((remaining & (remaining - 1)) == 0) {
          if (clause.positive)
            force_true |= remaining;
          else
            force_false |= remaining;
        }
      }
      if (force_true & force_false) return false;
      const Mask newly_forced = force_true | force_false;
      if (!newly_forced) return true;
      unit_assignments_ += popcount(newly_forced);
      true_mask |= force_true;
      false_mask |= force_false;
    }
  }

  int choose_variable(Mask true_mask, Mask false_mask,
                      bool& all_satisfied) const {
    const Mask assigned = true_mask | false_mask;
    std::array<uint64_t, kVariableCount> positive{};
    std::array<uint64_t, kVariableCount> negative{};
    all_satisfied = true;
    for (const Clause& clause : clauses_) {
      if (clause.mask &
          (clause.positive ? true_mask : false_mask))
        continue;
      all_satisfied = false;
      Mask remaining = clause.mask & ~assigned;
      const int width = popcount(remaining);
      // Widths after propagation are at least two and at most nine.
      const uint64_t weight = uint64_t{1} << (14 - width);
      while (remaining) {
        const int variable = trailing_zeroes(remaining);
        remaining &= remaining - 1;
        (clause.positive ? positive[variable] : negative[variable]) += weight;
      }
    }
    if (all_satisfied) return -1;

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
          (product == best_product && sum == best_sum && variable < best)) {
        best = variable;
        best_product = product;
        best_sum = sum;
      }
    }
    if (best < 0) throw std::runtime_error("no unset branch variable");
    return best;
  }

  void emit(uint8_t code) {
    if (!proof_) return;
    proof_->put(static_cast<char>(code));
    if (!*proof_) throw std::runtime_error("failed while writing proof");
  }

  SearchResult search(Mask true_mask, Mask false_mask, int depth) {
    if (over_limit()) return {SearchResult::kLimit, 0, 0};
    ++nodes_;
    max_depth_ = std::max(max_depth_, depth);
    if (options_.progress_interval &&
        nodes_ % options_.progress_interval == 0) {
      std::cerr << "progress nodes=" << nodes_ << " leaves=" << leaves_
                << " depth=" << depth << " elapsed=" << std::fixed
                << std::setprecision(3) << elapsed() << "s\n";
    }

    if (!propagate(true_mask, false_mask)) {
      ++leaves_;
      emit(kLeaf);
      return {SearchResult::kUnsat, 0, 0};
    }

    bool all_satisfied = false;
    const int variable =
        choose_variable(true_mask, false_mask, all_satisfied);
    if (all_satisfied) return {SearchResult::kSat, true_mask, false_mask};

    ++branches_;
    emit(static_cast<uint8_t>(variable));
    const Mask bit = Mask{1} << variable;
    SearchResult left = search(true_mask, false_mask | bit, depth + 1);
    if (left.value != SearchResult::kUnsat) return left;
    SearchResult right = search(true_mask | bit, false_mask, depth + 1);
    if (right.value != SearchResult::kUnsat) return right;
    return {SearchResult::kUnsat, 0, 0};
  }
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
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto value = [&](const std::string& name) -> const char* {
      if (++index >= argc) throw std::runtime_error(name + " needs a value");
      return argv[index];
    };
    if (argument == "--graph")
      options.graph_path = value(argument);
    else if (argument == "--proof")
      options.proof_path = value(argument);
    else if (argument == "--node-limit")
      options.node_limit = parse_u64(value(argument), argument);
    else if (argument == "--seconds-limit")
      options.seconds_limit = parse_double(value(argument), argument);
    else if (argument == "--progress")
      options.progress_interval = parse_u64(value(argument), argument);
    else
      throw std::runtime_error("unknown option: " + argument);
  }
  if (options.graph_path.empty())
    throw std::runtime_error("--graph is required");
  return options;
}

void write_u32(std::ostream& output, uint32_t value) {
  for (int shift = 0; shift < 32; shift += 8)
    output.put(static_cast<char>((value >> shift) & 0xff));
}

void write_header(std::ostream& output, uint32_t clause_count) {
  const char magic[8] = {'K', '2', 'C', '3', 'D', 'P', 'L', '1'};
  output.write(magic, sizeof(magic));
  output.put(static_cast<char>(kInputOrder));
  output.put(static_cast<char>(kDeletedFirst));
  output.put(static_cast<char>(kDeletedSecond));
  output.put(static_cast<char>(kVariableCount));
  write_u32(output, clause_count);
}

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

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const Graph input = decode_short_graph6(first_data_line(options.graph_path));
    const Graph core = fixed_core(input);
    Counts counts;
    check_core(core, counts);
    const std::vector<Clause> clauses = build_formula(core, counts);
    const uint64_t negative = counts.one_new_negative +
                              counts.two_new_negative +
                              counts.three_new_negative;
    const uint64_t positive = counts.one_new_positive +
                              counts.two_new_positive +
                              counts.three_new_positive;
    if (negative + positive != clauses.size())
      throw std::runtime_error("internal clause-count mismatch");

    const std::string partial =
        options.proof_path.empty() ? "" : options.proof_path + ".partial";
    std::ofstream proof;
    if (!partial.empty()) {
      proof.open(partial, std::ios::binary | std::ios::trunc);
      if (!proof) throw std::runtime_error("cannot open proof output");
      write_header(proof, static_cast<uint32_t>(clauses.size()));
    }

    Solver solver(clauses, options, partial.empty() ? nullptr : &proof);
    const SearchResult result = solver.run();
    if (proof.is_open()) proof.close();
    const char* status = result.value == SearchResult::kSat
                             ? "SAT"
                             : (result.value == SearchResult::kUnsat ? "UNSAT"
                                                                     : "LIMIT");
    std::cout << "{\"status\":\"" << status << "\""
              << ",\"input_n\":" << input.order
              << ",\"deleted_vertices\":[0,1]"
              << ",\"core_n\":" << core.order
              << ",\"new_vertices\":3"
              << ",\"variables\":" << kVariableCount
              << ",\"core_k5\":" << counts.core_k5
              << ",\"core_i5\":" << counts.core_i5
              << ",\"core_k4\":" << counts.core_k4
              << ",\"core_i4\":" << counts.core_i4
              << ",\"core_k3\":" << counts.core_k3
              << ",\"core_i3\":" << counts.core_i3
              << ",\"core_edges\":" << counts.core_edges
              << ",\"core_nonedges\":" << counts.core_nonedges
              << ",\"one_new_negative\":" << counts.one_new_negative
              << ",\"one_new_positive\":" << counts.one_new_positive
              << ",\"two_new_negative\":" << counts.two_new_negative
              << ",\"two_new_positive\":" << counts.two_new_positive
              << ",\"three_new_negative\":" << counts.three_new_negative
              << ",\"three_new_positive\":" << counts.three_new_positive
              << ",\"negative_clauses\":" << negative
              << ",\"positive_clauses\":" << positive
              << ",\"clauses\":" << clauses.size()
              << ",\"nodes\":" << solver.nodes()
              << ",\"branches\":" << solver.branches()
              << ",\"leaves\":" << solver.leaves()
              << ",\"unit_assignments\":" << solver.unit_assignments()
              << ",\"max_depth\":" << solver.max_depth()
              << ",\"elapsed_seconds\":" << std::fixed
              << std::setprecision(6) << solver.elapsed();
    if (result.value == SearchResult::kSat) {
      std::cout << ",\"true_variables_zero_based\":[";
      print_true_variables(result.true_mask);
      std::cout << ']';
    }
    std::cout << "}\n";

    if (result.value == SearchResult::kUnsat && !partial.empty()) {
      if (std::rename(partial.c_str(), options.proof_path.c_str()) != 0)
        throw std::runtime_error("cannot promote completed proof");
    }
    return result.value == SearchResult::kSat
               ? 10
               : (result.value == SearchResult::kUnsat ? 20 : 2);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
