// Independent checker for C2DPB001 fixed-core proof bundles.
//
// This source does not include or call the producer.  It has its own graph6
// decoder, fixed-graph validation, clause representation, formula builder,
// unit propagation, bundle parser, and exhaustive-tree traversal.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
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

constexpr char kBundleMagic[8] = {'C', '2', 'D', 'P', 'B', '0', '0', '1'};
constexpr char kProofMagic[8] = {'C', 'O', 'R', 'E', '2', 'D', 'P', '2'};
constexpr int kInputOrder = 42;
constexpr int kCoreOrder = 41;
constexpr int kVariables = 83;
constexpr uint8_t kLeaf = 0xff;

struct Bits {
  uint64_t low{};
  uint64_t high{};
};

Bits bit_at(int index) {
  if (index < 0 || index >= kVariables)
    throw std::runtime_error("bit index is out of range");
  return index < 64 ? Bits{uint64_t{1} << index, 0}
                    : Bits{0, uint64_t{1} << (index - 64)};
}

Bits bit_or(Bits left, Bits right) {
  return {left.low | right.low, left.high | right.high};
}

Bits bit_and(Bits left, Bits right) {
  return {left.low & right.low, left.high & right.high};
}

Bits bit_and_not(Bits left, Bits right) {
  return {left.low & ~right.low, left.high & ~right.high};
}

bool any(Bits value) { return value.low || value.high; }

int popcount(Bits value) {
  return __builtin_popcountll(value.low) +
         __builtin_popcountll(value.high);
}

void add_bit(Bits& value, int index) {
  const Bits selected = bit_at(index);
  value = bit_or(value, selected);
}

struct Clause {
  Bits variables;
  bool positive{};
};

struct Graph {
  int order{};
  std::vector<uint64_t> adjacency;
};

struct PairSelection {
  uint32_t catalog_line{};
  int deleted_vertex{};
};

struct FormulaStats {
  uint64_t core_k4{};
  uint64_t core_i4{};
  uint64_t core_k3{};
  uint64_t core_i3{};
  uint64_t negative{};
  uint64_t positive{};
};

struct TreeStats {
  uint64_t nodes{};
  uint64_t branches{};
  uint64_t leaves{};
  uint64_t unit_assignments{};
  int max_depth{};
};

struct CheckerOptions {
  std::string graph_path;
  std::string pairs_path;
  std::string bundle_path;
  std::string transcript_path;
  std::string catalog_sha256;
  std::string pairs_sha256;
};

CheckerOptions parse_options(int argc, char** argv) {
  CheckerOptions options;
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
    else if (arg == "--bundle")
      options.bundle_path = value(arg);
    else if (arg == "--transcript")
      options.transcript_path = value(arg);
    else if (arg == "--catalog-sha256")
      options.catalog_sha256 = value(arg);
    else if (arg == "--pairs-sha256")
      options.pairs_sha256 = value(arg);
    else
      throw std::runtime_error("unknown option: " + arg);
  }
  if (options.graph_path.empty() || options.pairs_path.empty() ||
      options.bundle_path.empty() || options.transcript_path.empty() ||
      options.catalog_sha256.empty() || options.pairs_sha256.empty())
    throw std::runtime_error(
        "--graph, --pairs, --bundle, --transcript, --catalog-sha256, and "
        "--pairs-sha256 are required");
  if (options.catalog_sha256.size() != 64 ||
      options.pairs_sha256.size() != 64)
    throw std::runtime_error("SHA-256 values must contain 64 hex digits");
  return options;
}

uint8_t hex_nibble(char value) {
  if (value >= '0' && value <= '9')
    return static_cast<uint8_t>(value - '0');
  if (value >= 'a' && value <= 'f')
    return static_cast<uint8_t>(10 + value - 'a');
  if (value >= 'A' && value <= 'F')
    return static_cast<uint8_t>(10 + value - 'A');
  throw std::runtime_error("invalid SHA-256 hexadecimal digit");
}

std::array<uint8_t, 32> parse_sha256(const std::string& text) {
  std::array<uint8_t, 32> digest{};
  for (size_t index = 0; index < digest.size(); ++index) {
    digest[index] = static_cast<uint8_t>(
        (hex_nibble(text[2 * index]) << 4) |
        hex_nibble(text[2 * index + 1]));
  }
  return digest;
}

std::vector<std::string> load_catalog(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
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
  std::set<std::pair<uint32_t, int>> seen;
  std::string line;
  uint64_t physical_line = 0;
  while (std::getline(input, line)) {
    ++physical_line;
    const size_t first = line.find_first_not_of(" \t\r\n");
    if (first == std::string::npos || line[first] == '#') continue;
    std::istringstream parsed(line);
    uint64_t catalog_line = 0;
    int deleted_vertex = -1;
    std::string extra;
    if (!(parsed >> catalog_line >> deleted_vertex) || (parsed >> extra))
      throw std::runtime_error(
          "invalid pair-list record at physical line " +
          std::to_string(physical_line));
    if (catalog_line == 0 ||
        catalog_line > std::numeric_limits<uint32_t>::max())
      throw std::runtime_error("catalog line is outside 1..2^32-1");
    if (deleted_vertex < 0 || deleted_vertex >= kInputOrder)
      throw std::runtime_error("deleted vertex is outside 0..41");
    const PairSelection selected{
        static_cast<uint32_t>(catalog_line), deleted_vertex};
    if (!seen.emplace(selected.catalog_line, selected.deleted_vertex).second)
      throw std::runtime_error("pair list contains a duplicate");
    pairs.push_back(selected);
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
    throw std::runtime_error("checker supports short graph6 only");
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

void check_input_graph(const Graph& graph) {
  if (graph.order != kInputOrder)
    throw std::runtime_error("catalog graph order is not 42");
  for (int a = 0; a < graph.order - 4; ++a)
    for (int b = a + 1; b < graph.order - 3; ++b)
      for (int c = b + 1; c < graph.order - 2; ++c)
        for (int d = c + 1; d < graph.order - 1; ++d)
          for (int e = d + 1; e < graph.order; ++e) {
            const int edges =
                edge(graph, a, b) + edge(graph, a, c) +
                edge(graph, a, d) + edge(graph, a, e) +
                edge(graph, b, c) + edge(graph, b, d) +
                edge(graph, b, e) + edge(graph, c, d) +
                edge(graph, c, e) + edge(graph, d, e);
            if (edges == 0 || edges == 10)
              throw std::runtime_error(
                  "catalog graph contains a forbidden homogeneous 5-set");
          }
}

Graph delete_vertex(const Graph& input, int deleted) {
  if (input.order != kInputOrder || deleted < 0 || deleted >= input.order)
    throw std::runtime_error("invalid fixed-core deletion");
  std::array<int, kCoreOrder> retained{};
  int cursor = 0;
  for (int vertex = 0; vertex < input.order; ++vertex)
    if (vertex != deleted) retained[cursor++] = vertex;
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

std::vector<Clause> build_formula(const Graph& core, FormulaStats& stats) {
  if (core.order != kCoreOrder)
    throw std::runtime_error("core order is not 41");
  std::vector<Clause> clauses;
  for (int a = 0; a < kCoreOrder - 3; ++a)
    for (int b = a + 1; b < kCoreOrder - 2; ++b)
      for (int c = b + 1; c < kCoreOrder - 1; ++c)
        for (int d = c + 1; d < kCoreOrder; ++d) {
          const int edges =
              edge(core, a, b) + edge(core, a, c) + edge(core, a, d) +
              edge(core, b, c) + edge(core, b, d) + edge(core, c, d);
          if (edges != 0 && edges != 6) continue;
          Bits first{};
          add_bit(first, a);
          add_bit(first, b);
          add_bit(first, c);
          add_bit(first, d);
          Bits second{};
          add_bit(second, kCoreOrder + a);
          add_bit(second, kCoreOrder + b);
          add_bit(second, kCoreOrder + c);
          add_bit(second, kCoreOrder + d);
          const bool positive = edges == 0;
          clauses.push_back({first, positive});
          clauses.push_back({second, positive});
          if (positive)
            ++stats.core_i4;
          else
            ++stats.core_k4;
        }
  for (int a = 0; a < kCoreOrder - 2; ++a)
    for (int b = a + 1; b < kCoreOrder - 1; ++b)
      for (int c = b + 1; c < kCoreOrder; ++c) {
        const int edges =
            edge(core, a, b) + edge(core, a, c) + edge(core, b, c);
        if (edges != 0 && edges != 3) continue;
        Bits variables{};
        for (int vertex : {a, b, c}) {
          add_bit(variables, vertex);
          add_bit(variables, kCoreOrder + vertex);
        }
        add_bit(variables, 2 * kCoreOrder);
        const bool positive = edges == 0;
        clauses.push_back({variables, positive});
        if (positive)
          ++stats.core_i3;
        else
          ++stats.core_k3;
      }
  stats.negative = 2 * stats.core_k4 + stats.core_k3;
  stats.positive = 2 * stats.core_i4 + stats.core_i3;
  if (stats.negative + stats.positive != clauses.size())
    throw std::runtime_error("independent formula accounting failed");
  return clauses;
}

class TreeChecker {
 public:
  TreeChecker(const std::vector<uint8_t>& proof, size_t payload_begin,
              size_t payload_end, const std::vector<Clause>& clauses)
      : proof_(proof),
        cursor_(payload_begin),
        payload_end_(payload_end),
        clauses_(clauses) {}

  TreeStats run() {
    check_node({}, {}, 0);
    if (cursor_ != payload_end_)
      throw std::runtime_error("proof has trailing tree bytes");
    if (stats_.leaves != stats_.branches + 1)
      throw std::runtime_error("proof tree is not full binary");
    return stats_;
  }

 private:
  const std::vector<uint8_t>& proof_;
  size_t cursor_;
  size_t payload_end_;
  const std::vector<Clause>& clauses_;
  TreeStats stats_;

  bool propagate(Bits& true_bits, Bits& false_bits) {
    while (true) {
      bool changed = false;
      const Bits assigned = bit_or(true_bits, false_bits);
      for (const Clause& clause : clauses_) {
        const Bits satisfying =
            bit_and(clause.variables,
                    clause.positive ? true_bits : false_bits);
        if (any(satisfying)) continue;
        const Bits remaining = bit_and_not(clause.variables, assigned);
        if (!any(remaining)) return false;
        if (popcount(remaining) == 1) {
          if (clause.positive)
            true_bits = bit_or(true_bits, remaining);
          else
            false_bits = bit_or(false_bits, remaining);
          ++stats_.unit_assignments;
          changed = true;
          break;
        }
      }
      if (!changed) return true;
    }
  }

  void check_node(Bits true_bits, Bits false_bits, int depth) {
    ++stats_.nodes;
    stats_.max_depth = std::max(stats_.max_depth, depth);
    const bool consistent = propagate(true_bits, false_bits);
    if (cursor_ >= payload_end_)
      throw std::runtime_error("proof tree is truncated");
    const uint8_t code = proof_[cursor_++];
    if (code == kLeaf) {
      ++stats_.leaves;
      if (consistent)
        throw std::runtime_error(
            "proof leaf has no original-clause conflict");
      return;
    }
    ++stats_.branches;
    if (!consistent)
      throw std::runtime_error("proof branches after a conflict");
    if (code >= kVariables)
      throw std::runtime_error("proof has an invalid branch variable");
    const Bits selected = bit_at(code);
    if (any(bit_and(bit_or(true_bits, false_bits), selected)))
      throw std::runtime_error("proof branches on an assigned variable");
    check_node(true_bits, bit_or(false_bits, selected), depth + 1);
    check_node(bit_or(true_bits, selected), false_bits, depth + 1);
  }
};

std::vector<uint8_t> read_binary(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open proof bundle");
  input.seekg(0, std::ios::end);
  const std::streamoff size = input.tellg();
  if (size < 0) throw std::runtime_error("cannot determine bundle length");
  input.seekg(0);
  std::vector<uint8_t> data(static_cast<size_t>(size));
  if (!data.empty())
    input.read(reinterpret_cast<char*>(data.data()), data.size());
  if (!input) throw std::runtime_error("cannot read proof bundle");
  return data;
}

void require_available(const std::vector<uint8_t>& data, size_t cursor,
                       size_t count, const std::string& label) {
  if (cursor > data.size() || count > data.size() - cursor)
    throw std::runtime_error("truncated " + label);
}

uint32_t read_u32(const std::vector<uint8_t>& data, size_t& cursor,
                  const std::string& label) {
  require_available(data, cursor, 4, label);
  uint32_t value = 0;
  for (int shift = 0; shift < 32; shift += 8)
    value |= static_cast<uint32_t>(data[cursor++]) << shift;
  return value;
}

void require_bytes(const std::vector<uint8_t>& data, size_t& cursor,
                   const uint8_t* expected, size_t count,
                   const std::string& label) {
  require_available(data, cursor, count, label);
  if (!std::equal(expected, expected + count, data.begin() + cursor))
    throw std::runtime_error("wrong " + label);
  cursor += count;
}

void require_digest(const std::vector<uint8_t>& data, size_t& cursor,
                    const std::array<uint8_t, 32>& expected,
                    const std::string& label) {
  require_bytes(data, cursor, expected.data(), expected.size(), label);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Clock::time_point started = Clock::now();
    const CheckerOptions options = parse_options(argc, argv);
    const std::vector<std::string> catalog = load_catalog(options.graph_path);
    const std::vector<PairSelection> pairs = load_pairs(options.pairs_path);
    for (const PairSelection& selected : pairs)
      if (selected.catalog_line > catalog.size())
        throw std::runtime_error("pair list selects an absent catalog line");

    const std::vector<uint8_t> bundle = read_binary(options.bundle_path);
    size_t cursor = 0;
    require_bytes(
        bundle, cursor,
        reinterpret_cast<const uint8_t*>(kBundleMagic),
        sizeof(kBundleMagic), "bundle magic");
    const uint32_t recorded_pair_count =
        read_u32(bundle, cursor, "bundle pair count");
    if (recorded_pair_count != pairs.size())
      throw std::runtime_error("bundle pair count does not match pair list");
    require_digest(bundle, cursor, parse_sha256(options.catalog_sha256),
                   "catalog SHA-256");
    require_digest(bundle, cursor, parse_sha256(options.pairs_sha256),
                   "pair-list SHA-256");

    const std::filesystem::path transcript(options.transcript_path);
    const std::filesystem::path partial(options.transcript_path + ".partial");
    if (std::filesystem::exists(transcript) ||
        std::filesystem::exists(partial))
      throw std::runtime_error(
          "checker transcript or partial transcript already exists");
    std::ofstream output(partial, std::ios::binary | std::ios::trunc);
    if (!output) throw std::runtime_error("cannot create checker transcript");

    std::vector<Graph> decoded(catalog.size());
    std::vector<bool> decoded_ready(catalog.size(), false);
    std::vector<bool> validated(catalog.size(), false);
    uint64_t proof_bytes_total = 0;
    uint64_t tree_nodes_total = 0;
    uint64_t tree_branches_total = 0;
    uint64_t tree_leaves_total = 0;
    uint64_t unit_assignments_total = 0;
    uint64_t catalog_graphs_checked = 0;

    for (size_t pair_index = 0; pair_index < pairs.size(); ++pair_index) {
      const PairSelection expected = pairs[pair_index];
      const uint32_t catalog_line =
          read_u32(bundle, cursor, "record catalog line");
      require_available(bundle, cursor, 1, "record deleted vertex");
      const int deleted_vertex = bundle[cursor++];
      const uint32_t proof_bytes =
          read_u32(bundle, cursor, "record proof length");
      if (catalog_line != expected.catalog_line ||
          deleted_vertex != expected.deleted_vertex)
        throw std::runtime_error(
            "bundle record order does not match pair list");
      require_available(bundle, cursor, proof_bytes, "record proof");
      if (proof_bytes < 19)
        throw std::runtime_error("CORE2DP2 proof is shorter than its header");
      const size_t proof_begin = cursor;
      const size_t proof_end = cursor + proof_bytes;
      size_t proof_cursor = proof_begin;
      require_bytes(
          bundle, proof_cursor,
          reinterpret_cast<const uint8_t*>(kProofMagic),
          sizeof(kProofMagic), "CORE2DP2 magic");
      require_available(bundle, proof_cursor, 1, "proof input order");
      const int proof_input_order = bundle[proof_cursor++];
      const uint32_t proof_catalog_line =
          read_u32(bundle, proof_cursor, "proof catalog line");
      require_available(bundle, proof_cursor, 2, "proof pair fields");
      const int proof_deleted_vertex = bundle[proof_cursor++];
      const int proof_variables = bundle[proof_cursor++];
      const uint32_t proof_clause_count =
          read_u32(bundle, proof_cursor, "proof clause count");
      if (proof_input_order != kInputOrder ||
          proof_catalog_line != catalog_line ||
          proof_deleted_vertex != deleted_vertex ||
          proof_variables != kVariables)
        throw std::runtime_error(
            "CORE2DP2 header does not bind the selected pair");

      const size_t graph_index = catalog_line - 1;
      if (!decoded_ready[graph_index]) {
        decoded[graph_index] = decode_graph6(catalog[graph_index]);
        decoded_ready[graph_index] = true;
      }
      if (!validated[graph_index]) {
        check_input_graph(decoded[graph_index]);
        validated[graph_index] = true;
        ++catalog_graphs_checked;
      }
      const Graph core =
          delete_vertex(decoded[graph_index], deleted_vertex);
      FormulaStats formula_stats;
      const std::vector<Clause> clauses =
          build_formula(core, formula_stats);
      if (proof_clause_count != clauses.size())
        throw std::runtime_error(
            "proof clause count does not match independent formula");

      TreeChecker checker(bundle, proof_cursor, proof_end, clauses);
      const TreeStats tree = checker.run();
      if (proof_bytes != 19 + tree.nodes)
        throw std::runtime_error(
            "proof length is inconsistent with one-byte tree nodes");
      output << "{\"status\":\"VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_"
                "COMPLETION\",\"pair_index\":"
             << pair_index << ",\"catalog_line\":" << catalog_line
             << ",\"deleted_vertex\":" << deleted_vertex
             << ",\"proof_bytes\":" << proof_bytes
             << ",\"variables\":" << kVariables
             << ",\"clauses\":" << clauses.size()
             << ",\"negative_clauses\":" << formula_stats.negative
             << ",\"positive_clauses\":" << formula_stats.positive
             << ",\"core_k4\":" << formula_stats.core_k4
             << ",\"core_i4\":" << formula_stats.core_i4
             << ",\"core_k3\":" << formula_stats.core_k3
             << ",\"core_i3\":" << formula_stats.core_i3
             << ",\"tree_nodes\":" << tree.nodes
             << ",\"tree_branches\":" << tree.branches
             << ",\"tree_leaves\":" << tree.leaves
             << ",\"unit_assignments_replayed\":"
             << tree.unit_assignments
             << ",\"max_branch_depth\":" << tree.max_depth << "}\n";
      if (!output)
        throw std::runtime_error("failed while writing checker transcript");
      cursor = proof_end;
      proof_bytes_total += proof_bytes;
      tree_nodes_total += tree.nodes;
      tree_branches_total += tree.branches;
      tree_leaves_total += tree.leaves;
      unit_assignments_total += tree.unit_assignments;
    }
    if (cursor != bundle.size())
      throw std::runtime_error("bundle has trailing bytes");
    output.close();
    if (!output)
      throw std::runtime_error("failed while closing checker transcript");
    std::filesystem::rename(partial, transcript);

    const double elapsed =
        std::chrono::duration<double>(Clock::now() - started).count();
    std::cout << "{\"status\":\"VERIFIED_UNSAT_FIXED_CORE_BUNDLE\","
              << "\"pair_count\":" << pairs.size()
              << ",\"catalog_graphs_checked\":" << catalog_graphs_checked
              << ",\"bundle_bytes\":" << bundle.size()
              << ",\"proof_bytes_total\":" << proof_bytes_total
              << ",\"tree_nodes_total\":" << tree_nodes_total
              << ",\"tree_branches_total\":" << tree_branches_total
              << ",\"tree_leaves_total\":" << tree_leaves_total
              << ",\"unit_assignments_replayed_total\":"
              << unit_assignments_total
              << ",\"checker_elapsed_seconds\":" << std::fixed
              << std::setprecision(6) << elapsed
              << ",\"transcript\":\"" << transcript.string() << "\"}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
