// Compact, atomic shard producer for the full delete-two/add-three screen.
//
// Each promoted K2SCRN01 file has a 64-byte header followed by fixed 48-byte
// records in lexicographic (catalog line, deleted-left, deleted-right) order.
// SAT is never encoded as a negative/status record: the process emits the
// raw model, stops immediately, and leaves only a diagnostic partial shard.

#define main ramsey55_unused_k2_persistent_main
#include "core_completion_k2_persistent_solver.cpp"
#undef main

#include <cmath>
#include <filesystem>

namespace {

constexpr char kCompactMagic[8] = {'K', '2', 'S', 'C', 'R', 'N', '0', '1'};
constexpr uint16_t kHeaderBytes = 64;
constexpr uint16_t kRecordBytes = 48;

struct CompactOptions {
  std::string graph_path;
  std::string records_path;
  uint32_t line_start{};
  uint32_t line_end{};
  std::array<uint8_t, 32> catalog_sha256{};
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t record_byte_cap = std::numeric_limits<uint64_t>::max();
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

std::array<uint8_t, 32> parse_sha256(const std::string& text) {
  if (text.size() != 64)
    throw std::runtime_error("catalog SHA-256 must have 64 hex digits");
  std::array<uint8_t, 32> digest{};
  for (size_t index = 0; index < digest.size(); ++index) {
    digest[index] = static_cast<uint8_t>(
        (hex_nibble(text[2 * index]) << 4) |
        hex_nibble(text[2 * index + 1]));
  }
  return digest;
}

CompactOptions parse_compact_options(int argc, char** argv) {
  CompactOptions options;
  std::string catalog_sha256;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    auto value = [&](const std::string& name) -> const char* {
      if (++i >= argc) throw std::runtime_error(name + " requires a value");
      return argv[i];
    };
    if (arg == "--graph")
      options.graph_path = value(arg);
    else if (arg == "--records")
      options.records_path = value(arg);
    else if (arg == "--line-start")
      options.line_start =
          static_cast<uint32_t>(parse_u64(value(arg), arg));
    else if (arg == "--line-end")
      options.line_end =
          static_cast<uint32_t>(parse_u64(value(arg), arg));
    else if (arg == "--catalog-sha256")
      catalog_sha256 = value(arg);
    else if (arg == "--node-limit")
      options.node_limit = parse_u64(value(arg), arg);
    else if (arg == "--seconds-limit")
      options.seconds_limit = parse_double(value(arg), arg);
    else if (arg == "--record-byte-cap")
      options.record_byte_cap = parse_u64(value(arg), arg);
    else
      throw std::runtime_error("unknown option: " + arg);
  }
  if (options.graph_path.empty() || options.records_path.empty() ||
      catalog_sha256.empty())
    throw std::runtime_error(
        "--graph, --records, and --catalog-sha256 are required");
  if (options.line_start == 0 || options.line_end < options.line_start ||
      options.line_end > std::numeric_limits<uint16_t>::max())
    throw std::runtime_error("invalid catalog line range");
  if (options.node_limit == 0 || !(options.seconds_limit > 0))
    throw std::runtime_error("node and time limits must be positive");
  options.catalog_sha256 = parse_sha256(catalog_sha256);
  return options;
}

void write_u16(std::ostream& output, uint16_t value) {
  output.put(static_cast<char>(value & 0xff));
  output.put(static_cast<char>((value >> 8) & 0xff));
}

void write_u32_compact(std::ostream& output, uint32_t value) {
  for (int shift = 0; shift < 32; shift += 8)
    output.put(static_cast<char>((value >> shift) & 0xff));
}

uint16_t checked_u16(uint64_t value, const std::string& label) {
  if (value > std::numeric_limits<uint16_t>::max())
    throw std::runtime_error(label + " exceeds uint16");
  return static_cast<uint16_t>(value);
}

uint32_t checked_u32(uint64_t value, const std::string& label) {
  if (value > std::numeric_limits<uint32_t>::max())
    throw std::runtime_error(label + " exceeds uint32");
  return static_cast<uint32_t>(value);
}

void write_header(std::ostream& output, const CompactOptions& options,
                  uint32_t record_count) {
  output.write(kCompactMagic, sizeof(kCompactMagic));
  write_u16(output, kHeaderBytes);
  write_u16(output, kRecordBytes);
  write_u16(output, static_cast<uint16_t>(options.line_start));
  write_u16(output, static_cast<uint16_t>(options.line_end));
  write_u32_compact(output, record_count);
  write_u16(output, kVariableCount);
  output.put(static_cast<char>(kCoreOrder));
  output.put(static_cast<char>(kNewVertices));
  output.write(
      reinterpret_cast<const char*>(options.catalog_sha256.data()),
      options.catalog_sha256.size());
  for (int index = 0; index < 8; ++index) output.put('\0');
}

void write_record(std::ostream& output, const PairSelection& selected,
                  uint8_t status, const ClauseCounts& counts,
                  const std::vector<Clause>& clauses, const Solver& solver,
                  uint32_t record_index) {
  write_u16(output, static_cast<uint16_t>(selected.catalog_line));
  output.put(static_cast<char>(selected.deleted_left));
  output.put(static_cast<char>(selected.deleted_right));
  output.put(static_cast<char>(status));
  output.put(static_cast<char>(
      std::min(solver.max_depth(),
               static_cast<int>(std::numeric_limits<uint8_t>::max()))));
  write_u16(output, checked_u16(clauses.size(), "clauses"));
  write_u16(output, checked_u16(counts.negative, "negative clauses"));
  write_u16(output, checked_u16(counts.positive, "positive clauses"));
  write_u16(output, checked_u16(counts.core_k4, "core K4 count"));
  write_u16(output, checked_u16(counts.core_i4, "core I4 count"));
  write_u16(output, checked_u16(counts.core_k3, "core K3 count"));
  write_u16(output, checked_u16(counts.core_i3, "core I3 count"));
  write_u16(output, checked_u16(counts.core_edges, "core edge count"));
  write_u16(output, checked_u16(counts.core_nonedges, "core nonedge count"));
  write_u32_compact(output, checked_u32(solver.nodes(), "nodes"));
  write_u32_compact(output, checked_u32(solver.branches(), "branches"));
  write_u32_compact(output, checked_u32(solver.leaves(), "leaves"));
  write_u32_compact(
      output, checked_u32(solver.unit_assignments(), "unit assignments"));
  const double elapsed_microseconds = std::round(solver.elapsed() * 1e6);
  write_u32_compact(
      output,
      checked_u32(
          static_cast<uint64_t>(std::max(0.0, elapsed_microseconds)),
          "elapsed microseconds"));
  write_u32_compact(output, record_index);
}

void print_sat_result(const PairSelection& selected,
                      const ClauseCounts& counts,
                      const std::vector<Clause>& clauses,
                      const Solver& solver, const SearchResult& result) {
  std::cout << "{\"record_type\":\"SAT\",\"status\":\"SAT\","
            << "\"catalog_line\":" << selected.catalog_line
            << ",\"deleted_left\":" << selected.deleted_left
            << ",\"deleted_right\":" << selected.deleted_right
            << ",\"input_n\":42,\"core_n\":40,"
            << "\"added_vertices\":3,\"variables\":123,"
            << "\"negative_clauses\":" << counts.negative
            << ",\"positive_clauses\":" << counts.positive
            << ",\"clauses\":" << clauses.size()
            << ",\"nodes\":" << solver.nodes()
            << ",\"branches\":" << solver.branches()
            << ",\"leaves\":" << solver.leaves()
            << ",\"unit_assignments\":" << solver.unit_assignments()
            << ",\"max_depth\":" << solver.max_depth()
            << ",\"elapsed_seconds\":" << std::fixed
            << std::setprecision(6) << solver.elapsed()
            << ",\"true_variables\":[";
  print_true_variables(result.true_mask);
  std::cout << "]}\n" << std::flush;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const CompactOptions options = parse_compact_options(argc, argv);
    const std::vector<std::string> catalog = load_catalog(options.graph_path);
    if (options.line_end > catalog.size())
      throw std::runtime_error("requested range exceeds catalog");
    const uint64_t lines = options.line_end - options.line_start + 1;
    const uint64_t record_count_u64 = lines * 861;
    const uint64_t expected_bytes =
        kHeaderBytes + record_count_u64 * kRecordBytes;
    if (expected_bytes > options.record_byte_cap)
      throw std::runtime_error("planned compact shard exceeds byte cap");
    const uint32_t record_count =
        checked_u32(record_count_u64, "record count");

    const std::filesystem::path final_path(options.records_path);
    const std::filesystem::path partial_path(options.records_path + ".partial");
    if (std::filesystem::exists(final_path) ||
        std::filesystem::exists(partial_path))
      throw std::runtime_error(
          "compact output or partial output already exists");
    std::ofstream output(partial_path, std::ios::binary | std::ios::trunc);
    if (!output) throw std::runtime_error("cannot create compact shard");
    write_header(output, options, record_count);

    uint32_t record_index = 0;
    uint64_t unsat_count = 0;
    uint64_t limit_count = 0;
    const Clock::time_point shard_started = Clock::now();
    for (uint32_t line = options.line_start; line <= options.line_end; ++line) {
      const Graph input = decode_graph6(catalog[line - 1]);
      for (int deleted_left = 0; deleted_left < kInputOrder - 1;
           ++deleted_left) {
        for (int deleted_right = deleted_left + 1;
             deleted_right < kInputOrder; ++deleted_right) {
          const PairSelection selected{
              line, deleted_left, deleted_right};
          const Graph core = delete_two_vertices(
              input, deleted_left, deleted_right);
          ClauseCounts counts;
          const std::vector<Clause> clauses = build_clauses(core, counts);
          Solver solver(
              clauses, options.node_limit, options.seconds_limit);
          const SearchResult result = solver.run();
          if (result.value == SearchResult::kSat) {
            output.flush();
            output.close();
            print_sat_result(selected, counts, clauses, solver, result);
            std::cout << "{\"record_type\":\"SHARD\","
                      << "\"status\":\"SAT_STOP\","
                      << "\"completed_records\":" << record_index
                      << ",\"expected_records\":" << record_count
                      << ",\"partial_records\":\""
                      << partial_path.string() << "\"}\n";
            return 10;
          }
          const uint8_t status =
              result.value == SearchResult::kUnsat ? 0 : 1;
          write_record(
              output, selected, status, counts, clauses, solver, record_index);
          if (!output)
            throw std::runtime_error("failed while writing compact record");
          ++record_index;
          unsat_count += result.value == SearchResult::kUnsat;
          limit_count += result.value == SearchResult::kLimit;
        }
      }
      output.flush();
      if (!output)
        throw std::runtime_error("failed while flushing compact shard");
      std::cout << "{\"record_type\":\"LINE\","
                << "\"catalog_line\":" << line
                << ",\"completed_records\":" << record_index
                << ",\"unsat_count\":" << unsat_count
                << ",\"limit_count\":" << limit_count
                << ",\"record_bytes\":"
                << static_cast<uint64_t>(output.tellp()) << "}\n"
                << std::flush;
    }
    if (record_index != record_count)
      throw std::runtime_error("internal compact record-count mismatch");
    const uint64_t actual_bytes = static_cast<uint64_t>(output.tellp());
    output.close();
    if (!output) throw std::runtime_error("failed while closing compact shard");
    if (actual_bytes != expected_bytes)
      throw std::runtime_error("compact shard byte-count mismatch");
    std::filesystem::rename(partial_path, final_path);
    const double runtime =
        std::chrono::duration<double>(Clock::now() - shard_started).count();
    std::cout << "{\"record_type\":\"SHARD\","
              << "\"status\":\"COMPLETE\","
              << "\"line_start\":" << options.line_start
              << ",\"line_end\":" << options.line_end
              << ",\"record_count\":" << record_count
              << ",\"unsat_count\":" << unsat_count
              << ",\"limit_count\":" << limit_count
              << ",\"record_bytes\":" << actual_bytes
              << ",\"runtime_seconds\":" << std::fixed
              << std::setprecision(6) << runtime
              << ",\"records\":\"" << final_path.string() << "\"}\n";
    return limit_count ? 2 : 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
