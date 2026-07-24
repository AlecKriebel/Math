// Bounded exact solver and compact exhaustive-tree proof producer for the
// following fixed-core Ramsey completion problem.
//
// Delete one specified vertex from a fixed (5,5;42) graph, retain all edges
// on the resulting 41-vertex labeled core, and add two vertices A and B.
// Variables 0..40 encode A--core edges, 41..81 encode B--core edges, and
// variable 82 encodes A--B.  Clauses forbid every K5 and independent 5-set
// involving at least one of A,B.  (The fixed core is checked separately.)
//
// A proof is a preorder binary DPLL tree.  A byte in 0..82 branches on that
// variable, with the false child followed by the true child.  Byte 255 is a
// leaf where repeated unit propagation on the original clauses conflicts.
// No learned or derived clause is trusted by the independent checker.

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
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;
using Mask = unsigned __int128;

constexpr int kCoreOrder = 41;
constexpr int kVariableCount = 83;
constexpr uint8_t kLeaf = 0xff;

struct Clause {
  Mask mask{};
  bool positive{};  // true is OR x_i; false is OR !x_i.
};

struct Graph {
  int n{};
  std::vector<uint64_t> adjacency;
};

struct ClauseCounts {
  uint64_t core_k5{};
  uint64_t core_i5{};
  uint64_t core_k4{};
  uint64_t core_i4{};
  uint64_t core_k3{};
  uint64_t core_i3{};
  uint64_t negative{};
  uint64_t positive{};
};

struct Options {
  std::string graph_path;
  std::string proof_path;
  uint32_t catalog_line = 1;
  int deleted_vertex = 0;
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t progress_interval = 1000000;
};

struct SearchResult {
  enum Value { kSat, kUnsat, kLimit } value{kLimit};
  Mask true_mask{};
  Mask false_mask{};
};

std::string selected_data_line(const std::string& path,
                               uint32_t requested_line) {
  if (requested_line == 0)
    throw std::runtime_error("catalog line numbers are one-based");
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph: " + path);
  std::string line;
  uint32_t data_line = 0;
  while (std::getline(input, line)) {
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n'))
      line.pop_back();
    const size_t first = line.find_first_not_of(" \t");
    if (first == std::string::npos || line[first] == '#') continue;
    ++data_line;
    if (data_line == requested_line)
      return line.substr(first);
  }
  throw std::runtime_error("requested catalog line is absent");
}

Graph decode_graph6(const std::string& raw) {
  std::string line = raw;
  if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
  if (line.empty()) throw std::runtime_error("empty graph6 input");
  const int n = static_cast<unsigned char>(line[0]) - 63;
  if (n < 0 || n > 62)
    throw std::runtime_error("only short graph6 inputs are supported");
  const int needed = n * (n - 1) / 2;
  if (static_cast<int>(line.size() - 1) * 6 < needed)
    throw std::runtime_error("truncated graph6 input");
  std::vector<uint64_t> adjacency(n, 0);
  int bit_index = 0;
  for (int right = 1; right < n; ++right) {
    for (int left = 0; left < right; ++left) {
      const int value =
          static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64)
        throw std::runtime_error("invalid graph6 byte");
      const bool edge = (value >> (5 - bit_index % 6)) & 1;
      ++bit_index;
      if (edge) {
        adjacency[left] |= uint64_t{1} << right;
        adjacency[right] |= uint64_t{1} << left;
      }
    }
  }
  return {n, std::move(adjacency)};
}

Graph delete_vertex(const Graph& graph, int deleted) {
  if (graph.n != 42)
    throw std::runtime_error("this experiment requires a 42-vertex input");
  if (deleted < 0 || deleted >= graph.n)
    throw std::runtime_error("deleted vertex is out of range");
  std::vector<int> old_vertices;
  old_vertices.reserve(graph.n - 1);
  for (int vertex = 0; vertex < graph.n; ++vertex)
    if (vertex != deleted) old_vertices.push_back(vertex);
  std::vector<uint64_t> adjacency(old_vertices.size(), 0);
  for (int left = 0; left < static_cast<int>(old_vertices.size()); ++left) {
    for (int right = left + 1; right < static_cast<int>(old_vertices.size());
         ++right) {
      if ((graph.adjacency[old_vertices[left]] >> old_vertices[right]) & 1) {
        adjacency[left] |= uint64_t{1} << right;
        adjacency[right] |= uint64_t{1} << left;
      }
    }
  }
  return {static_cast<int>(adjacency.size()), std::move(adjacency)};
}

bool edge(const Graph& graph, int left, int right) {
  return (graph.adjacency[left] >> right) & 1;
}

void check_fixed_core(const Graph& core, ClauseCounts& counts) {
  for (int a = 0; a < core.n - 4; ++a)
    for (int b = a + 1; b < core.n - 3; ++b)
      for (int c = b + 1; c < core.n - 2; ++c)
        for (int d = c + 1; d < core.n - 1; ++d)
          for (int e = d + 1; e < core.n; ++e) {
            const std::array<int, 5> vertices{a, b, c, d, e};
            int edges = 0;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j)
                edges += edge(core, vertices[i], vertices[j]);
            counts.core_i5 += edges == 0;
            counts.core_k5 += edges == 10;
          }
  if (counts.core_k5 || counts.core_i5)
    throw std::runtime_error("fixed 41-vertex core already violates (5,5)");
}

std::vector<Clause> build_clauses(const Graph& core, ClauseCounts& counts) {
  if (core.n != kCoreOrder)
    throw std::runtime_error("internal core order is not 41");
  std::vector<Clause> clauses;

  // A or B together with a homogeneous core 4-set.
  for (int a = 0; a < core.n - 3; ++a)
    for (int b = a + 1; b < core.n - 2; ++b)
      for (int c = b + 1; c < core.n - 1; ++c)
        for (int d = c + 1; d < core.n; ++d) {
          const std::array<int, 4> vertices{a, b, c, d};
          int edges = 0;
          for (int i = 0; i < 4; ++i)
            for (int j = i + 1; j < 4; ++j)
              edges += edge(core, vertices[i], vertices[j]);
          if (edges != 0 && edges != 6) continue;
          const Mask a_mask = (Mask{1} << a) | (Mask{1} << b) |
                              (Mask{1} << c) | (Mask{1} << d);
          const Mask b_mask = a_mask << kCoreOrder;
          const bool positive = edges == 0;
          clauses.push_back({a_mask, positive});
          clauses.push_back({b_mask, positive});
          if (positive)
            ++counts.core_i4;
          else
            ++counts.core_k4;
        }

  // A,B together with a homogeneous core triple.  All seven relevant edges
  // must be present for a K5 and absent for an independent 5-set.
  const Mask ab_bit = Mask{1} << (2 * kCoreOrder);
  for (int a = 0; a < core.n - 2; ++a)
    for (int b = a + 1; b < core.n - 1; ++b)
      for (int c = b + 1; c < core.n; ++c) {
        const int edges =
            edge(core, a, b) + edge(core, a, c) + edge(core, b, c);
        if (edges != 0 && edges != 3) continue;
        const Mask a_mask =
            (Mask{1} << a) | (Mask{1} << b) | (Mask{1} << c);
        const Mask both_mask = a_mask | (a_mask << kCoreOrder) | ab_bit;
        const bool positive = edges == 0;
        clauses.push_back({both_mask, positive});
        if (positive)
          ++counts.core_i3;
        else
          ++counts.core_k3;
      }

  counts.negative = 2 * counts.core_k4 + counts.core_k3;
  counts.positive = 2 * counts.core_i4 + counts.core_i3;
  return clauses;
}

int popcount(Mask value) {
  const uint64_t low = static_cast<uint64_t>(value);
  const uint64_t high = static_cast<uint64_t>(value >> 64);
  return __builtin_popcountll(low) + __builtin_popcountll(high);
}

int trailing_zeroes(Mask value) {
  const uint64_t low = static_cast<uint64_t>(value);
  if (low) return __builtin_ctzll(low);
  return 64 + __builtin_ctzll(static_cast<uint64_t>(value >> 64));
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
  uint64_t leaves() const { return leaves_; }
  uint64_t branches() const { return branches_; }
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
  uint64_t leaves_ = 0;
  uint64_t branches_ = 0;
  uint64_t unit_assignments_ = 0;
  int max_depth_ = 0;
  bool limit_hit_ = false;

  bool over_limit() {
    if (limit_hit_) return true;
    if (nodes_ >= options_.node_limit) {
      limit_hit_ = true;
      return true;
    }
    if (elapsed() >= options_.seconds_limit) {
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
        (clause.positive ? positive[variable] : negative[variable]) += weight;
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
          (product == best_product && sum == best_sum && variable < best)) {
        best = variable;
        best_product = product;
        best_sum = sum;
      }
    }
    if (best < 0) throw std::runtime_error("no unset branch variable");
    true_first = positive[best] >= negative[best];
    return best;
  }

  void emit(uint8_t byte) {
    if (!proof_) return;
    proof_->put(static_cast<char>(byte));
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
    if ((true_mask | false_mask) == all_mask_)
      return {SearchResult::kSat, true_mask, false_mask};

    bool true_first = false;
    const int variable = choose_variable(true_mask, false_mask, true_first);
    ++branches_;
    emit(static_cast<uint8_t>(variable));
    const Mask bit = Mask{1} << variable;

    // Proof syntax fixes false-child then true-child.  Without a proof, use
    // the heuristic polarity so a satisfying model is found sooner.
    if (proof_ || !true_first) {
      SearchResult left = search(true_mask, false_mask | bit, depth + 1);
      if (left.value != SearchResult::kUnsat) return left;
      SearchResult right = search(true_mask | bit, false_mask, depth + 1);
      if (right.value != SearchResult::kUnsat) return right;
    } else {
      SearchResult right = search(true_mask | bit, false_mask, depth + 1);
      if (right.value != SearchResult::kUnsat) return right;
      SearchResult left = search(true_mask, false_mask | bit, depth + 1);
      if (left.value != SearchResult::kUnsat) return left;
    }
    return {SearchResult::kUnsat, 0, 0};
  }
};

uint64_t parse_u64(const char* text, const std::string& label) {
  char* end = nullptr;
  const unsigned long long value = std::strtoull(text, &end, 10);
  if (!end || *end) throw std::runtime_error("invalid " + label);
  return static_cast<uint64_t>(value);
}

int parse_int(const char* text, const std::string& label) {
  char* end = nullptr;
  const long value = std::strtol(text, &end, 10);
  if (!end || *end || value < 0 || value > 255)
    throw std::runtime_error("invalid " + label);
  return static_cast<int>(value);
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
    else if (arg == "--line") {
      const uint64_t line = parse_u64(value(arg), arg);
      if (line == 0 || line > std::numeric_limits<uint32_t>::max())
        throw std::runtime_error("--line is outside 1..2^32-1");
      options.catalog_line = static_cast<uint32_t>(line);
    }
    else if (arg == "--delete")
      options.deleted_vertex = parse_int(value(arg), arg);
    else if (arg == "--proof")
      options.proof_path = value(arg);
    else if (arg == "--node-limit")
      options.node_limit = parse_u64(value(arg), arg);
    else if (arg == "--seconds-limit")
      options.seconds_limit = parse_double(value(arg), arg);
    else if (arg == "--progress")
      options.progress_interval = parse_u64(value(arg), arg);
    else
      throw std::runtime_error("unknown option: " + arg);
  }
  if (options.graph_path.empty())
    throw std::runtime_error("--graph is required");
  return options;
}

void write_u32(std::ostream& output, uint32_t value) {
  for (int shift = 0; shift < 32; shift += 8)
    output.put(static_cast<char>((value >> shift) & 0xff));
}

void write_header(std::ostream& output, int input_n, uint32_t catalog_line,
                  int deleted, uint32_t clauses) {
  const char magic[8] = {'C', 'O', 'R', 'E', '2', 'D', 'P', '2'};
  output.write(magic, sizeof(magic));
  output.put(static_cast<char>(input_n));
  write_u32(output, catalog_line);
  output.put(static_cast<char>(deleted));
  output.put(static_cast<char>(kVariableCount));
  write_u32(output, clauses);
}

void print_mask_indices(Mask mask) {
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
    const Graph input = decode_graph6(
        selected_data_line(options.graph_path, options.catalog_line));
    const Graph core = delete_vertex(input, options.deleted_vertex);
    ClauseCounts counts;
    check_fixed_core(core, counts);
    const std::vector<Clause> clauses = build_clauses(core, counts);
    if (counts.negative + counts.positive != clauses.size())
      throw std::runtime_error("internal clause-count mismatch");

    const std::string temporary =
        options.proof_path.empty() ? "" : options.proof_path + ".partial";
    std::ofstream proof;
    if (!temporary.empty()) {
      proof.open(temporary, std::ios::binary | std::ios::trunc);
      if (!proof) throw std::runtime_error("cannot open proof output");
      write_header(proof, input.n, options.catalog_line,
                   options.deleted_vertex,
                   static_cast<uint32_t>(clauses.size()));
    }

    Solver solver(clauses, options, temporary.empty() ? nullptr : &proof);
    const SearchResult result = solver.run();
    if (proof.is_open()) proof.close();
    const char* status = result.value == SearchResult::kSat
                             ? "SAT"
                             : (result.value == SearchResult::kUnsat ? "UNSAT"
                                                                     : "LIMIT");
    std::cout << "{\"status\":\"" << status << "\",\"input_n\":" << input.n
              << ",\"catalog_line\":" << options.catalog_line
              << ",\"deleted_vertex\":" << options.deleted_vertex
              << ",\"core_n\":" << core.n
              << ",\"variables\":" << kVariableCount
              << ",\"core_k5\":" << counts.core_k5
              << ",\"core_i5\":" << counts.core_i5
              << ",\"core_k4\":" << counts.core_k4
              << ",\"core_i4\":" << counts.core_i4
              << ",\"core_k3\":" << counts.core_k3
              << ",\"core_i3\":" << counts.core_i3
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
      print_mask_indices(result.true_mask);
      std::cout << ']';
    }
    std::cout << "}\n";

    // Only a fully exhausted UNSAT tree is promoted to the requested name.
    if (result.value == SearchResult::kUnsat && !temporary.empty()) {
      if (std::rename(temporary.c_str(), options.proof_path.c_str()) != 0)
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
