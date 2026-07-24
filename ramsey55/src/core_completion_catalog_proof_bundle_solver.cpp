// Persistent proof-bundle producer for fixed-core two-vertex completions.
//
// This translation unit reuses the exact formula and DPLL implementation from
// core_completion_proof_solver.cpp.  It loads the catalog once, solves an
// explicitly ordered pair list, and atomically promotes a bundle only when
// every pair has a complete CORE2DP2 UNSAT tree.  SAT and LIMIT leave only a
// diagnostic .partial bundle and are never represented as certified records.

#define main ramsey55_unused_single_core_completion_main
#include "core_completion_proof_solver.cpp"
#undef main

#include <array>
#include <filesystem>
#include <set>
#include <sstream>

namespace {

constexpr char kBundleMagic[8] = {'C', '2', 'D', 'P', 'B', '0', '0', '1'};

struct PairSelection {
  uint32_t catalog_line{};
  int deleted_vertex{};
};

struct BundleOptions {
  std::string graph_path;
  std::string pairs_path;
  std::string bundle_path;
  std::array<uint8_t, 32> catalog_sha256{};
  std::array<uint8_t, 32> pairs_sha256{};
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t bundle_byte_limit = std::numeric_limits<uint64_t>::max();
};

uint8_t hex_nibble(char value) {
  if (value >= '0' && value <= '9')
    return static_cast<uint8_t>(value - '0');
  if (value >= 'a' && value <= 'f')
    return static_cast<uint8_t>(10 + value - 'a');
  if (value >= 'A' && value <= 'F')
    return static_cast<uint8_t>(10 + value - 'A');
  throw std::runtime_error("invalid SHA-256 hexadecimal digit");
}

std::array<uint8_t, 32> parse_sha256(const std::string& text,
                                     const std::string& label) {
  if (text.size() != 64)
    throw std::runtime_error(label + " must contain 64 hexadecimal digits");
  std::array<uint8_t, 32> digest{};
  for (size_t index = 0; index < digest.size(); ++index) {
    digest[index] = static_cast<uint8_t>(
        (hex_nibble(text[2 * index]) << 4) |
        hex_nibble(text[2 * index + 1]));
  }
  return digest;
}

BundleOptions parse_bundle_options(int argc, char** argv) {
  BundleOptions options;
  std::string catalog_sha256;
  std::string pairs_sha256;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    auto value = [&](const std::string& name) -> const char* {
      if (++i >= argc) throw std::runtime_error(name + " requires a value");
      return argv[i];
    };
    if (arg == "--graph") {
      options.graph_path = value(arg);
    } else if (arg == "--pairs") {
      options.pairs_path = value(arg);
    } else if (arg == "--bundle") {
      options.bundle_path = value(arg);
    } else if (arg == "--catalog-sha256") {
      catalog_sha256 = value(arg);
    } else if (arg == "--pairs-sha256") {
      pairs_sha256 = value(arg);
    } else if (arg == "--node-limit") {
      options.node_limit = parse_u64(value(arg), arg);
    } else if (arg == "--seconds-limit") {
      options.seconds_limit = parse_double(value(arg), arg);
    } else if (arg == "--bundle-byte-limit") {
      options.bundle_byte_limit = parse_u64(value(arg), arg);
    } else {
      throw std::runtime_error("unknown option: " + arg);
    }
  }
  if (options.graph_path.empty() || options.pairs_path.empty() ||
      options.bundle_path.empty())
    throw std::runtime_error("--graph, --pairs, and --bundle are required");
  if (catalog_sha256.empty() || pairs_sha256.empty())
    throw std::runtime_error(
        "--catalog-sha256 and --pairs-sha256 are required");
  if (options.node_limit == 0)
    throw std::runtime_error("--node-limit must be positive");
  if (!(options.seconds_limit > 0))
    throw std::runtime_error("--seconds-limit must be positive");
  if (options.bundle_byte_limit < 76)
    throw std::runtime_error("--bundle-byte-limit must be at least 76");
  options.catalog_sha256 = parse_sha256(catalog_sha256, "--catalog-sha256");
  options.pairs_sha256 = parse_sha256(pairs_sha256, "--pairs-sha256");
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
    if (deleted_vertex < 0 || deleted_vertex >= 42)
      throw std::runtime_error("deleted vertex is outside 0..41");
    const PairSelection selected{
        static_cast<uint32_t>(catalog_line), deleted_vertex};
    if (!seen.emplace(selected.catalog_line, selected.deleted_vertex).second)
      throw std::runtime_error("pair list contains a duplicate");
    pairs.push_back(selected);
  }
  if (pairs.empty()) throw std::runtime_error("pair list is empty");
  if (pairs.size() > std::numeric_limits<uint32_t>::max())
    throw std::runtime_error("pair list is too large");
  return pairs;
}

void write_digest(std::ostream& output,
                  const std::array<uint8_t, 32>& digest) {
  output.write(reinterpret_cast<const char*>(digest.data()), digest.size());
}

void print_pair_result(const PairSelection& selected, const Graph& input,
                       const Graph& core, const ClauseCounts& counts,
                       const std::vector<Clause>& clauses,
                       const Solver& solver, const SearchResult& result,
                       uint64_t proof_bytes, uint64_t bundle_record_offset) {
  const char* status = result.value == SearchResult::kSat
                           ? "SAT"
                           : (result.value == SearchResult::kUnsat ? "UNSAT"
                                                                   : "LIMIT");
  std::cout << "{\"record_type\":\"PAIR\",\"status\":\"" << status
            << "\",\"input_n\":" << input.n
            << ",\"catalog_line\":" << selected.catalog_line
            << ",\"deleted_vertex\":" << selected.deleted_vertex
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
            << std::setprecision(6) << solver.elapsed()
            << ",\"proof_bytes\":" << proof_bytes
            << ",\"bundle_record_offset\":" << bundle_record_offset;
  if (result.value == SearchResult::kSat) {
    std::cout << ",\"true_variables\":[";
    print_mask_indices(result.true_mask);
    std::cout << ']';
  }
  std::cout << "}\n" << std::flush;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const BundleOptions options = parse_bundle_options(argc, argv);
    const std::vector<std::string> catalog = load_catalog(options.graph_path);
    const std::vector<PairSelection> pairs = load_pairs(options.pairs_path);
    for (const PairSelection& selected : pairs)
      if (selected.catalog_line > catalog.size())
        throw std::runtime_error("pair list selects an absent catalog line");

    const std::filesystem::path final_path(options.bundle_path);
    const std::filesystem::path partial_path(options.bundle_path + ".partial");
    if (std::filesystem::exists(final_path) ||
        std::filesystem::exists(partial_path))
      throw std::runtime_error("bundle output or partial output already exists");
    std::ofstream bundle(partial_path, std::ios::binary | std::ios::trunc);
    if (!bundle) throw std::runtime_error("cannot create partial bundle");
    bundle.write(kBundleMagic, sizeof(kBundleMagic));
    write_u32(bundle, static_cast<uint32_t>(pairs.size()));
    write_digest(bundle, options.catalog_sha256);
    write_digest(bundle, options.pairs_sha256);

    uint64_t completed = 0;
    uint64_t proof_bytes_total = 0;
    uint64_t tree_nodes_total = 0;
    for (const PairSelection& selected : pairs) {
      const Graph input =
          decode_graph6(catalog[selected.catalog_line - 1]);
      const Graph core = delete_vertex(input, selected.deleted_vertex);
      ClauseCounts counts;
      check_fixed_core(core, counts);
      const std::vector<Clause> clauses = build_clauses(core, counts);
      if (counts.negative + counts.positive != clauses.size())
        throw std::runtime_error("internal clause-count mismatch");

      std::ostringstream proof(std::ios::out | std::ios::binary);
      write_header(proof, input.n, selected.catalog_line,
                   selected.deleted_vertex,
                   static_cast<uint32_t>(clauses.size()));
      Options solver_options;
      solver_options.node_limit = options.node_limit;
      solver_options.seconds_limit = options.seconds_limit;
      solver_options.progress_interval = 0;
      Solver solver(clauses, solver_options, &proof);
      const SearchResult result = solver.run();
      const std::string proof_raw = proof.str();
      const uint64_t record_offset =
          static_cast<uint64_t>(bundle.tellp());

      if (result.value != SearchResult::kUnsat) {
        bundle.flush();
        bundle.close();
        print_pair_result(selected, input, core, counts, clauses, solver,
                          result, 0, record_offset);
        std::cout << "{\"record_type\":\"BUNDLE\",\"status\":\""
                  << (result.value == SearchResult::kSat
                          ? "ABORTED_SAT"
                          : "ABORTED_LIMIT")
                  << "\",\"completed_unsat_pairs\":" << completed
                  << ",\"requested_pairs\":" << pairs.size()
                  << ",\"partial_bundle\":\"" << partial_path.string()
                  << "\"}\n";
        return result.value == SearchResult::kSat ? 10 : 2;
      }
      if (proof_raw.size() > std::numeric_limits<uint32_t>::max())
        throw std::runtime_error("one proof exceeds the bundle length field");
      const uint64_t next_bundle_bytes =
          record_offset + 9 + proof_raw.size();
      if (next_bundle_bytes > options.bundle_byte_limit) {
        bundle.flush();
        bundle.close();
        print_pair_result(selected, input, core, counts, clauses, solver,
                          result, proof_raw.size(), record_offset);
        std::cout << "{\"record_type\":\"BUNDLE\","
                  << "\"status\":\"ABORTED_BUNDLE_BYTE_LIMIT\","
                  << "\"completed_unsat_pairs\":" << completed
                  << ",\"requested_pairs\":" << pairs.size()
                  << ",\"bundle_byte_limit\":"
                  << options.bundle_byte_limit
                  << ",\"next_bundle_bytes\":" << next_bundle_bytes
                  << ",\"partial_bundle\":\"" << partial_path.string()
                  << "\"}\n";
        return 2;
      }
      write_u32(bundle, selected.catalog_line);
      bundle.put(static_cast<char>(selected.deleted_vertex));
      write_u32(bundle, static_cast<uint32_t>(proof_raw.size()));
      bundle.write(proof_raw.data(), proof_raw.size());
      if (!bundle) throw std::runtime_error("failed while writing bundle");
      bundle.flush();
      if (!bundle) throw std::runtime_error("failed while flushing bundle");
      ++completed;
      proof_bytes_total += proof_raw.size();
      tree_nodes_total += solver.nodes();
      print_pair_result(selected, input, core, counts, clauses, solver, result,
                        proof_raw.size(), record_offset);
    }

    const uint64_t bundle_bytes = static_cast<uint64_t>(bundle.tellp());
    bundle.close();
    if (!bundle) throw std::runtime_error("failed while closing bundle");
    std::filesystem::rename(partial_path, final_path);
    std::cout << "{\"record_type\":\"BUNDLE\","
              << "\"status\":\"UNSAT_BUNDLE_COMPLETE\","
              << "\"completed_unsat_pairs\":" << completed
              << ",\"requested_pairs\":" << pairs.size()
              << ",\"proof_bytes_total\":" << proof_bytes_total
              << ",\"tree_nodes_total\":" << tree_nodes_total
              << ",\"bundle_bytes\":" << bundle_bytes
              << ",\"bundle\":\"" << final_path.string() << "\"}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
