// Bounded, atomic screen for delete-three/add-three replacements of the two
// frozen order-43 E=2 representatives.
//
// The 40-vertex completion formula is exactly the one used by the existing
// delete-two/add-three core-completion solver.  A triple retaining either
// fixed homogeneous five-set is rejected structurally; all other triples are
// sent to the bounded 123-variable DPLL solver.  Solver UNSAT answers are
// observations, not certificates.  A SAT model is printed and stops the
// process before any negative shard can be promoted.

#define main ramsey55_unused_core_completion_k2_main
#include "core_completion_k2_persistent_solver.cpp"
#undef main

#include <array>
#include <cmath>
#include <filesystem>

namespace {

constexpr int kReplacementInputOrder = 43;
constexpr uint32_t kTriplesPerInput = 12341;
constexpr char kMagic[8] = {'E', '2', 'T', '3', 'R', 'P', '0', '1'};
constexpr uint16_t kHeaderBytes = 64;
constexpr uint16_t kRecordBytes = 64;

enum RecordStatus : uint8_t {
  kStructuralObstruction = 0,
  kObservedUnsat = 1,
  kLimit = 2,
};

struct ReplacementOptions {
  std::string graph_path;
  std::string records_path;
  uint8_t input_index{};
  uint32_t triple_start{};
  uint32_t triple_end{};
  std::array<uint8_t, 32> corpus_sha256{};
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
  uint64_t record_byte_cap = std::numeric_limits<uint64_t>::max();
};

uint8_t hex_nibble_replacement(char value) {
  if (value >= '0' && value <= '9')
    return static_cast<uint8_t>(value - '0');
  if (value >= 'a' && value <= 'f')
    return static_cast<uint8_t>(10 + value - 'a');
  if (value >= 'A' && value <= 'F')
    return static_cast<uint8_t>(10 + value - 'A');
  throw std::runtime_error("invalid SHA-256 hexadecimal digit");
}

std::array<uint8_t, 32> parse_sha256_replacement(
    const std::string& text) {
  if (text.size() != 64)
    throw std::runtime_error("corpus SHA-256 must have 64 hex digits");
  std::array<uint8_t, 32> digest{};
  for (size_t index = 0; index < digest.size(); ++index) {
    digest[index] = static_cast<uint8_t>(
        (hex_nibble_replacement(text[2 * index]) << 4) |
        hex_nibble_replacement(text[2 * index + 1]));
  }
  return digest;
}

ReplacementOptions parse_replacement_options(int argc, char** argv) {
  ReplacementOptions options;
  std::string corpus_sha256;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto value = [&](const std::string& name) -> const char* {
      if (++index >= argc)
        throw std::runtime_error(name + " requires a value");
      return argv[index];
    };
    if (argument == "--graph")
      options.graph_path = value(argument);
    else if (argument == "--records")
      options.records_path = value(argument);
    else if (argument == "--input-index")
      options.input_index =
          static_cast<uint8_t>(parse_u64(value(argument), argument));
    else if (argument == "--triple-start")
      options.triple_start =
          static_cast<uint32_t>(parse_u64(value(argument), argument));
    else if (argument == "--triple-end")
      options.triple_end =
          static_cast<uint32_t>(parse_u64(value(argument), argument));
    else if (argument == "--corpus-sha256")
      corpus_sha256 = value(argument);
    else if (argument == "--node-limit")
      options.node_limit = parse_u64(value(argument), argument);
    else if (argument == "--seconds-limit")
      options.seconds_limit = parse_double(value(argument), argument);
    else if (argument == "--record-byte-cap")
      options.record_byte_cap = parse_u64(value(argument), argument);
    else
      throw std::runtime_error("unknown option: " + argument);
  }
  if (options.graph_path.empty() || options.records_path.empty() ||
      corpus_sha256.empty())
    throw std::runtime_error(
        "--graph, --records, and --corpus-sha256 are required");
  if (options.input_index < 1 || options.input_index > 2)
    throw std::runtime_error("input index must be 1 or 2");
  if (options.triple_start >= options.triple_end ||
      options.triple_end > kTriplesPerInput)
    throw std::runtime_error("invalid half-open triple range");
  if (options.node_limit == 0 || !(options.seconds_limit > 0))
    throw std::runtime_error("node and time limits must be positive");
  options.corpus_sha256 = parse_sha256_replacement(corpus_sha256);
  return options;
}

void write_u16_replacement(std::ostream& output, uint16_t value) {
  output.put(static_cast<char>(value & 0xff));
  output.put(static_cast<char>((value >> 8) & 0xff));
}

void write_u32_replacement(std::ostream& output, uint32_t value) {
  for (int shift = 0; shift < 32; shift += 8)
    output.put(static_cast<char>((value >> shift) & 0xff));
}

uint16_t checked_u16_replacement(
    uint64_t value, const std::string& label) {
  if (value > std::numeric_limits<uint16_t>::max())
    throw std::runtime_error(label + " exceeds uint16");
  return static_cast<uint16_t>(value);
}

uint32_t checked_u32_replacement(
    uint64_t value, const std::string& label) {
  if (value > std::numeric_limits<uint32_t>::max())
    throw std::runtime_error(label + " exceeds uint32");
  return static_cast<uint32_t>(value);
}

std::vector<std::array<int, 3>> all_triples() {
  std::vector<std::array<int, 3>> triples;
  triples.reserve(kTriplesPerInput);
  for (int a = 0; a < kReplacementInputOrder - 2; ++a)
    for (int b = a + 1; b < kReplacementInputOrder - 1; ++b)
      for (int c = b + 1; c < kReplacementInputOrder; ++c)
        triples.push_back({a, b, c});
  if (triples.size() != kTriplesPerInput)
    throw std::runtime_error("internal triple-count mismatch");
  return triples;
}

struct FixedConflict {
  std::array<int, 5> vertices{};
  bool clique{};
};

std::vector<FixedConflict> fixed_conflicts(const Graph& graph) {
  if (graph.order != kReplacementInputOrder)
    throw std::runtime_error("replacement input order is not 43");
  std::vector<FixedConflict> conflicts;
  for (int a = 0; a < graph.order - 4; ++a)
    for (int b = a + 1; b < graph.order - 3; ++b)
      for (int c = b + 1; c < graph.order - 2; ++c)
        for (int d = c + 1; d < graph.order - 1; ++d)
          for (int e = d + 1; e < graph.order; ++e) {
            const std::array<int, 5> vertices{{a, b, c, d, e}};
            int edges = 0;
            for (int left = 0; left < 4; ++left)
              for (int right = left + 1; right < 5; ++right)
                edges += edge(
                    graph, vertices[left], vertices[right]);
            if (edges == 0 || edges == 10)
              conflicts.push_back({vertices, edges == 10});
          }
  if (conflicts.size() != 2 ||
      conflicts[0].clique != conflicts[1].clique)
    throw std::runtime_error(
        "frozen input is not a same-colour exact E=2 graph");
  int overlap = 0;
  for (int left : conflicts[0].vertices)
    for (int right : conflicts[1].vertices)
      overlap += left == right;
  if (overlap != 4)
    throw std::runtime_error("the two input conflicts do not overlap in four");
  return conflicts;
}

bool contains(
    const std::array<int, 3>& triple, int vertex) {
  return triple[0] == vertex || triple[1] == vertex ||
         triple[2] == vertex;
}

uint8_t retained_conflict_count(
    const std::vector<FixedConflict>& conflicts,
    const std::array<int, 3>& deleted) {
  uint8_t retained = 0;
  for (const FixedConflict& conflict : conflicts) {
    bool hit = false;
    for (int vertex : conflict.vertices) hit = hit || contains(deleted, vertex);
    retained += !hit;
  }
  return retained;
}

Graph delete_three_vertices(
    const Graph& input, const std::array<int, 3>& deleted) {
  if (input.order != kReplacementInputOrder ||
      !(deleted[0] < deleted[1] && deleted[1] < deleted[2]) ||
      deleted[0] < 0 || deleted[2] >= input.order)
    throw std::runtime_error("invalid delete-three selection");
  std::array<int, kCoreOrder> retained{};
  int cursor = 0;
  for (int vertex = 0; vertex < input.order; ++vertex)
    if (!contains(deleted, vertex)) retained[cursor++] = vertex;
  if (cursor != kCoreOrder)
    throw std::runtime_error("delete-three core order mismatch");
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

void write_header(
    std::ostream& output, const ReplacementOptions& options,
    uint32_t record_count) {
  output.write(kMagic, sizeof(kMagic));
  write_u16_replacement(output, kHeaderBytes);
  write_u16_replacement(output, kRecordBytes);
  output.put(static_cast<char>(options.input_index));
  output.put('\0');
  write_u16_replacement(output, 0);
  write_u32_replacement(output, options.triple_start);
  write_u32_replacement(output, options.triple_end);
  write_u32_replacement(output, record_count);
  write_u16_replacement(output, kVariableCount);
  output.put(static_cast<char>(kCoreOrder));
  output.put(static_cast<char>(kNewVertices));
  output.write(
      reinterpret_cast<const char*>(options.corpus_sha256.data()),
      options.corpus_sha256.size());
}

void write_record(
    std::ostream& output, uint32_t ordinal,
    const std::array<int, 3>& deleted, RecordStatus status,
    uint8_t retained_conflicts, const ClauseCounts* counts,
    const std::vector<Clause>* clauses, const Solver* solver) {
  write_u32_replacement(output, ordinal);
  output.put(static_cast<char>(deleted[0]));
  output.put(static_cast<char>(deleted[1]));
  output.put(static_cast<char>(deleted[2]));
  output.put(static_cast<char>(status));
  output.put(static_cast<char>(
      solver ? std::min(solver->max_depth(), 255) : 0));
  output.put(static_cast<char>(retained_conflicts));
  const ClauseCounts zero_counts{};
  const ClauseCounts& actual = counts ? *counts : zero_counts;
  const uint64_t clause_count = clauses ? clauses->size() : 0;
  for (uint64_t value : {
           clause_count,
           actual.negative,
           actual.positive,
           actual.core_k4,
           actual.core_i4,
           actual.core_k3,
           actual.core_i3,
           actual.core_edges,
           actual.core_nonedges,
       })
    write_u16_replacement(
        output, checked_u16_replacement(value, "record uint16 field"));
  const double elapsed_microseconds =
      solver ? std::round(solver->elapsed() * 1e6) : 0;
  for (uint64_t value : {
           solver ? solver->nodes() : 0,
           solver ? solver->branches() : 0,
           solver ? solver->leaves() : 0,
           solver ? solver->unit_assignments() : 0,
           static_cast<uint64_t>(std::max(0.0, elapsed_microseconds)),
           static_cast<uint64_t>(ordinal),
       })
    write_u32_replacement(
        output, checked_u32_replacement(value, "record uint32 field"));
  for (int index = 0; index < 12; ++index) output.put('\0');
}

void print_sat(
    uint8_t input_index, uint32_t ordinal,
    const std::array<int, 3>& deleted, const ClauseCounts& counts,
    const std::vector<Clause>& clauses, const Solver& solver,
    const SearchResult& result) {
  std::cout
      << "{\"record_type\":\"SAT\",\"status\":\"SAT\","
      << "\"input_index\":" << static_cast<int>(input_index)
      << ",\"triple_ordinal\":" << ordinal
      << ",\"deleted_vertices\":[" << deleted[0] << ',' << deleted[1]
      << ',' << deleted[2] << "],\"input_n\":43,\"core_n\":40,"
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
    const ReplacementOptions options =
        parse_replacement_options(argc, argv);
    const std::vector<std::string> corpus =
        load_catalog(options.graph_path);
    if (corpus.size() != 2)
      throw std::runtime_error("frozen corpus must have exactly two graphs");
    const Graph input = decode_graph6(corpus[options.input_index - 1]);
    const std::vector<FixedConflict> conflicts =
        fixed_conflicts(input);
    const std::vector<std::array<int, 3>> triples = all_triples();
    const uint32_t record_count =
        options.triple_end - options.triple_start;
    const uint64_t expected_bytes =
        kHeaderBytes + uint64_t{record_count} * kRecordBytes;
    if (expected_bytes > options.record_byte_cap)
      throw std::runtime_error("planned shard exceeds record-byte cap");

    const std::filesystem::path final_path(options.records_path);
    const std::filesystem::path partial_path(
        options.records_path + ".partial");
    if (std::filesystem::exists(final_path) ||
        std::filesystem::exists(partial_path))
      throw std::runtime_error(
          "final or partial output already exists");
    std::ofstream output(
        partial_path, std::ios::binary | std::ios::trunc);
    if (!output) throw std::runtime_error("cannot create partial shard");
    write_header(output, options, record_count);

    uint64_t structural_count = 0;
    uint64_t unsat_count = 0;
    uint64_t limit_count = 0;
    const Clock::time_point started = Clock::now();
    for (uint32_t ordinal = options.triple_start;
         ordinal < options.triple_end; ++ordinal) {
      const std::array<int, 3>& deleted = triples[ordinal];
      const uint8_t retained =
          retained_conflict_count(conflicts, deleted);
      if (retained) {
        write_record(
            output, ordinal, deleted, kStructuralObstruction,
            retained, nullptr, nullptr, nullptr);
        ++structural_count;
        continue;
      }
      const Graph core = delete_three_vertices(input, deleted);
      ClauseCounts counts;
      const std::vector<Clause> clauses = build_clauses(core, counts);
      Solver solver(
          clauses, options.node_limit, options.seconds_limit);
      const SearchResult result = solver.run();
      if (result.value == SearchResult::kSat) {
        output.flush();
        output.close();
        print_sat(
            options.input_index, ordinal, deleted, counts, clauses,
            solver, result);
        std::cout
            << "{\"record_type\":\"SHARD\",\"status\":\"SAT_STOP\","
            << "\"input_index\":" << static_cast<int>(options.input_index)
            << ",\"triple_start\":" << options.triple_start
            << ",\"triple_end\":" << options.triple_end
            << ",\"completed_records\":"
            << (ordinal - options.triple_start)
            << ",\"partial_records\":\"" << partial_path.string()
            << "\"}\n" << std::flush;
        return 10;
      }
      const RecordStatus status =
          result.value == SearchResult::kUnsat
              ? kObservedUnsat
              : kLimit;
      write_record(
          output, ordinal, deleted, status, 0, &counts, &clauses,
          &solver);
      unsat_count += status == kObservedUnsat;
      limit_count += status == kLimit;
    }
    output.flush();
    const uint64_t actual_bytes =
        static_cast<uint64_t>(output.tellp());
    output.close();
    if (!output || actual_bytes != expected_bytes)
      throw std::runtime_error("atomic shard byte-count mismatch");
    std::filesystem::rename(partial_path, final_path);
    const double runtime =
        std::chrono::duration<double>(Clock::now() - started).count();
    std::cout
        << "{\"record_type\":\"SHARD\",\"status\":\"COMPLETE\","
        << "\"input_index\":" << static_cast<int>(options.input_index)
        << ",\"triple_start\":" << options.triple_start
        << ",\"triple_end\":" << options.triple_end
        << ",\"record_count\":" << record_count
        << ",\"structural_count\":" << structural_count
        << ",\"observed_unsat_count\":" << unsat_count
        << ",\"limit_count\":" << limit_count
        << ",\"record_bytes\":" << actual_bytes
        << ",\"runtime_seconds\":" << std::fixed
        << std::setprecision(6) << runtime << "}\n";
    return limit_count ? 2 : 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
