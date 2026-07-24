// Exact DPLL solver and compact tree-proof producer for a fixed one-vertex
// extension of a (5,5;n) graph.
//
// A variable x_v is true when the new vertex is adjacent to v.  Every K4 in
// the input graph gives the clause OR_{v in K4} !x_v, and every independent
// 4-set gives OR_{v in I4} x_v.  The binary proof is a preorder DPLL tree:
//   0..n-1 : branch on that (currently unset) variable, false child first
//   0xff   : unit propagation reaches a conflicting original clause
// Thus an independent checker only needs the graph, unit propagation, and a
// recursive traversal that confirms both children of every branch.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

struct Clause {
  uint64_t mask{};
  bool positive{};  // true: OR x_v; false: OR !x_v
};

struct Graph {
  int n{};
  std::vector<uint64_t> adjacency;
};

struct Options {
  std::string graph_path;
  std::string proof_path;
  uint64_t line_number = 1;
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t progress_interval = 10000000;
};

struct SearchResult {
  enum Value { kSat, kUnsat, kLimit } value{kLimit};
  uint64_t true_mask{};
  uint64_t false_mask{};
};

std::string data_line(const std::string& path, uint64_t requested_line) {
  if (requested_line == 0)
    throw std::runtime_error("--line must be at least 1");
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph: " + path);
  std::string line;
  uint64_t data_index = 0;
  while (std::getline(input, line)) {
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n'))
      line.pop_back();
    if (!line.empty() && line[0] != '#') {
      ++data_index;
      if (data_index == requested_line) return line;
    }
  }
  throw std::runtime_error(
      "requested graph data line is outside the input catalog");
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
  for (int j = 1; j < n; ++j) {
    for (int i = 0; i < j; ++i) {
      const int value =
          static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
      if (value < 0 || value >= 64)
        throw std::runtime_error("invalid graph6 byte");
      const bool edge = (value >> (5 - bit_index % 6)) & 1;
      ++bit_index;
      if (edge) {
        adjacency[i] |= uint64_t{1} << j;
        adjacency[j] |= uint64_t{1} << i;
      }
    }
  }
  return {n, std::move(adjacency)};
}

std::vector<Clause> build_clauses(const Graph& graph, uint64_t& clique4_count,
                                  uint64_t& independent4_count) {
  std::vector<Clause> clauses;
  clique4_count = independent4_count = 0;
  for (int a = 0; a < graph.n - 3; ++a) {
    for (int b = a + 1; b < graph.n - 2; ++b) {
      for (int c = b + 1; c < graph.n - 1; ++c) {
        for (int d = c + 1; d < graph.n; ++d) {
          const std::array<int, 4> vertices{a, b, c, d};
          int edges = 0;
          for (int i = 0; i < 4; ++i)
            for (int j = i + 1; j < 4; ++j)
              edges += (graph.adjacency[vertices[i]] >> vertices[j]) & 1;
          const uint64_t mask = (uint64_t{1} << a) | (uint64_t{1} << b) |
                                (uint64_t{1} << c) | (uint64_t{1} << d);
          if (edges == 0) {
            clauses.push_back({mask, true});
            ++independent4_count;
          } else if (edges == 6) {
            clauses.push_back({mask, false});
            ++clique4_count;
          }
        }
      }
    }
  }
  return clauses;
}

class Solver {
 public:
  Solver(int n, const std::vector<Clause>& clauses, const Options& options,
         std::ostream* proof)
      : clauses_(clauses),
        options_(options),
        proof_(proof),
        start_(Clock::now()),
        all_mask_((uint64_t{1} << n) - 1) {}

  SearchResult run() { return search(0, 0, 0); }

  uint64_t nodes() const { return nodes_; }
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
  uint64_t all_mask_;
  uint64_t nodes_ = 0;
  uint64_t leaves_ = 0;
  uint64_t unit_assignments_ = 0;
  int max_depth_ = 0;
  bool limit_hit_ = false;

  bool over_limit() {
    if (limit_hit_) return true;
    if (nodes_ >= options_.node_limit) {
      limit_hit_ = true;
      return true;
    }
    // Avoid a clock call at every node.
    if ((nodes_ & 0xffff) == 0 && elapsed() >= options_.seconds_limit) {
      limit_hit_ = true;
      return true;
    }
    return false;
  }

  // Repeatedly scan original clauses to a fixed point.  This deliberately
  // simple rule is duplicated independently in the Python proof checker.
  bool propagate(uint64_t& true_mask, uint64_t& false_mask) {
    while (true) {
      bool changed = false;
      const uint64_t assigned = true_mask | false_mask;
      for (const Clause& clause : clauses_) {
        const uint64_t satisfying =
            clause.positive ? (clause.mask & true_mask)
                            : (clause.mask & false_mask);
        if (satisfying) continue;
        const uint64_t remaining = clause.mask & ~assigned;
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

  int choose_variable(uint64_t true_mask, uint64_t false_mask,
                      bool& true_first) const {
    const uint64_t assigned = true_mask | false_mask;
    std::array<uint64_t, 62> positive{};
    std::array<uint64_t, 62> negative{};
    for (const Clause& clause : clauses_) {
      const uint64_t satisfying =
          clause.positive ? (clause.mask & true_mask)
                          : (clause.mask & false_mask);
      if (satisfying) continue;
      uint64_t remaining = clause.mask & ~assigned;
      const int width = __builtin_popcountll(remaining);
      // At a propagation fixed point width >= 2.  Short clauses receive
      // exponentially more weight (MOMS/Jeroslow-Wang hybrid).
      const uint64_t weight = uint64_t{1} << (12 - width);
      while (remaining) {
        const int variable = __builtin_ctzll(remaining);
        remaining &= remaining - 1;
        (clause.positive ? positive[variable] : negative[variable]) += weight;
      }
    }
    int best = -1;
    unsigned __int128 best_product = 0;
    uint64_t best_sum = 0;
    uint64_t unset = all_mask_ & ~assigned;
    while (unset) {
      const int variable = __builtin_ctzll(unset);
      unset &= unset - 1;
      // Product rewards variables that constrain both polarities.  Adding one
      // prevents a zero-polarity variable from disappearing entirely.
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
    if (best < 0) throw std::runtime_error("no unassigned branch variable");
    true_first = positive[best] >= negative[best];
    return best;
  }

  void emit(uint8_t byte) {
    if (!proof_) return;
    proof_->put(static_cast<char>(byte));
    if (!*proof_) throw std::runtime_error("failed while writing proof");
  }

  SearchResult search(uint64_t true_mask, uint64_t false_mask, int depth) {
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
      emit(0xff);
      return {SearchResult::kUnsat, 0, 0};
    }
    if ((true_mask | false_mask) == all_mask_)
      return {SearchResult::kSat, true_mask, false_mask};

    bool true_first = false;
    const int variable = choose_variable(true_mask, false_mask, true_first);
    emit(static_cast<uint8_t>(variable));
    const uint64_t bit = uint64_t{1} << variable;

    // The tree format fixes false-child then true-child order.  Search-order
    // preference is implemented only when no proof is requested.
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

double parse_double(const char* text, const std::string& label) {
  char* end = nullptr;
  const double value = std::strtod(text, &end);
  if (!end || *end || value < 0) throw std::runtime_error("invalid " + label);
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
    else if (arg == "--proof")
      options.proof_path = value(arg);
    else if (arg == "--line")
      options.line_number = parse_u64(value(arg), arg);
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

void write_header(std::ostream& output, int n, uint32_t clauses) {
  const char magic[8] = {'E', 'X', 'T', 'D', 'P', 'L', 'L', '1'};
  output.write(magic, sizeof(magic));
  output.put(static_cast<char>(n));
  for (int shift = 0; shift < 32; shift += 8)
    output.put(static_cast<char>((clauses >> shift) & 0xff));
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const Graph graph =
        decode_graph6(data_line(options.graph_path, options.line_number));
    uint64_t clique4_count = 0;
    uint64_t independent4_count = 0;
    const std::vector<Clause> clauses =
        build_clauses(graph, clique4_count, independent4_count);

    const std::string temporary =
        options.proof_path.empty() ? "" : options.proof_path + ".partial";
    std::ofstream proof;
    if (!temporary.empty()) {
      proof.open(temporary, std::ios::binary | std::ios::trunc);
      if (!proof) throw std::runtime_error("cannot open proof output");
      write_header(proof, graph.n, static_cast<uint32_t>(clauses.size()));
    }

    Solver solver(graph.n, clauses, options,
                  temporary.empty() ? nullptr : &proof);
    const SearchResult result = solver.run();
    if (proof.is_open()) proof.close();

    std::string status;
    if (result.value == SearchResult::kSat)
      status = "SAT";
    else if (result.value == SearchResult::kUnsat)
      status = "UNSAT";
    else
      status = "LIMIT";

    std::cout << "{\"status\":\"" << status << "\",\"n\":" << graph.n
              << ",\"graph_line\":" << options.line_number
              << ",\"k4_clauses\":" << clique4_count
              << ",\"i4_clauses\":" << independent4_count
              << ",\"clauses\":" << clauses.size()
              << ",\"nodes\":" << solver.nodes()
              << ",\"leaves\":" << solver.leaves()
              << ",\"unit_assignments\":" << solver.unit_assignments()
              << ",\"max_depth\":" << solver.max_depth()
              << ",\"elapsed_seconds\":" << std::fixed
              << std::setprecision(6) << solver.elapsed();
    if (result.value == SearchResult::kSat) {
      std::cout << ",\"true_vertices\":[";
      bool first = true;
      for (int v = 0; v < graph.n; ++v) {
        if ((result.true_mask >> v) & 1) {
          if (!first) std::cout << ',';
          first = false;
          std::cout << v;
        }
      }
      std::cout << ']';
    }
    std::cout << "}\n";

    // Leave partial traces clearly marked on SAT/LIMIT.  Only a complete
    // UNSAT traversal is promoted to the requested proof filename.
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
