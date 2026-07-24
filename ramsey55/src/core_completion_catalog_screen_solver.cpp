// Persistent-worker variant of the fixed-core exact solver.
//
// This translation unit deliberately reuses the already tested formula and
// DPLL implementation by including it under a renamed single-instance main.
// It then loads a contiguous catalog line range once and emits one flushed
// JSON record for each (line, deleted vertex) pair.  No proof is generated:
// UNSAT output from this screening binary is an observation, not a
// certificate.

#define main ramsey55_unused_single_instance_main
#include "core_completion_proof_solver.cpp"
#undef main

namespace {

struct CatalogScreenOptions {
  std::string graph_path;
  uint32_t line_start = 0;
  uint32_t line_end = 0;
  uint64_t node_limit = std::numeric_limits<uint64_t>::max();
  double seconds_limit = std::numeric_limits<double>::infinity();
};

CatalogScreenOptions parse_catalog_screen_options(int argc, char** argv) {
  CatalogScreenOptions options;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    auto value = [&](const std::string& name) -> const char* {
      if (++i >= argc) throw std::runtime_error(name + " requires a value");
      return argv[i];
    };
    if (arg == "--graph") {
      options.graph_path = value(arg);
    } else if (arg == "--line-start") {
      const uint64_t parsed = parse_u64(value(arg), arg);
      if (parsed == 0 || parsed > std::numeric_limits<uint32_t>::max())
        throw std::runtime_error("--line-start is outside 1..2^32-1");
      options.line_start = static_cast<uint32_t>(parsed);
    } else if (arg == "--line-end") {
      const uint64_t parsed = parse_u64(value(arg), arg);
      if (parsed == 0 || parsed > std::numeric_limits<uint32_t>::max())
        throw std::runtime_error("--line-end is outside 1..2^32-1");
      options.line_end = static_cast<uint32_t>(parsed);
    } else if (arg == "--node-limit") {
      options.node_limit = parse_u64(value(arg), arg);
    } else if (arg == "--seconds-limit") {
      options.seconds_limit = parse_double(value(arg), arg);
    } else {
      throw std::runtime_error("unknown option: " + arg);
    }
  }
  if (options.graph_path.empty())
    throw std::runtime_error("--graph is required");
  if (options.line_start == 0 || options.line_end == 0)
    throw std::runtime_error("--line-start and --line-end are required");
  if (options.line_start > options.line_end)
    throw std::runtime_error("line range is descending");
  if (options.node_limit == 0)
    throw std::runtime_error("--node-limit must be positive");
  if (!(options.seconds_limit > 0))
    throw std::runtime_error("--seconds-limit must be positive");
  return options;
}

std::vector<std::string> load_catalog_data_lines(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open graph: " + path);
  std::vector<std::string> lines;
  std::string line;
  while (std::getline(input, line)) {
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n'))
      line.pop_back();
    const size_t first = line.find_first_not_of(" \t");
    if (first == std::string::npos || line[first] == '#') continue;
    lines.push_back(line.substr(first));
  }
  if (lines.empty()) throw std::runtime_error("catalog has no data line");
  return lines;
}

void print_screen_result(uint32_t catalog_line, int deleted_vertex,
                         const Graph& input, const Graph& core,
                         const ClauseCounts& counts,
                         const std::vector<Clause>& clauses,
                         const Solver& solver, const SearchResult& result) {
  const char* status = result.value == SearchResult::kSat
                           ? "SAT"
                           : (result.value == SearchResult::kUnsat ? "UNSAT"
                                                                   : "LIMIT");
  std::cout << "{\"status\":\"" << status << "\",\"input_n\":" << input.n
            << ",\"catalog_line\":" << catalog_line
            << ",\"deleted_vertex\":" << deleted_vertex
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
  std::cout << "}\n" << std::flush;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const CatalogScreenOptions options =
        parse_catalog_screen_options(argc, argv);
    const std::vector<std::string> catalog =
        load_catalog_data_lines(options.graph_path);
    if (options.line_end > catalog.size())
      throw std::runtime_error("requested line range exceeds catalog");

    bool saw_sat = false;
    bool saw_limit = false;
    for (uint32_t catalog_line = options.line_start;
         catalog_line <= options.line_end; ++catalog_line) {
      const Graph input = decode_graph6(catalog[catalog_line - 1]);
      for (int deleted_vertex = 0; deleted_vertex < input.n;
           ++deleted_vertex) {
        const Graph core = delete_vertex(input, deleted_vertex);
        ClauseCounts counts;
        check_fixed_core(core, counts);
        const std::vector<Clause> clauses = build_clauses(core, counts);
        if (counts.negative + counts.positive != clauses.size())
          throw std::runtime_error("internal clause-count mismatch");

        Options solver_options;
        solver_options.node_limit = options.node_limit;
        solver_options.seconds_limit = options.seconds_limit;
        solver_options.progress_interval = 0;
        Solver solver(clauses, solver_options, nullptr);
        const SearchResult result = solver.run();
        saw_sat |= result.value == SearchResult::kSat;
        saw_limit |= result.value == SearchResult::kLimit;
        print_screen_result(catalog_line, deleted_vertex, input, core, counts,
                            clauses, solver, result);
      }
    }
    return saw_sat ? 10 : (saw_limit ? 2 : 0);
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
