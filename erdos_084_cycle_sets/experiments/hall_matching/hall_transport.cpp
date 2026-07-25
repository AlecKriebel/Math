// Exact Hall-transport experiment for the safe/unsafe decomposition.
//
// For every parameter P containing 1, this program computes
//
//   d(P) = |A_P| - |A_P join V(P)|,
//   b(P) = |(H_P join V(P)) \ H_P|
//        + |((A_P join V(P)) union (H_P join V(P))) \ H_P|.
//
// It then asks whether all integer supply d(P) can be transported to the
// capacities b(Q), allowing Q to be obtained from P by at most r downward
// parameter deletions.  A maximum-flow certificate answers this exactly.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint64_t;
using Count = std::int64_t;

struct Options {
  int m = 6;
  int radius = 1;
  unsigned threads = 1;
  bool print_witness = false;
  bool details = false;
  bool net = false;
  bool reverse_order = false;
};

struct ParameterCounts {
  Count safe = 0;
  Count safe_images = 0;
  Count boundary0 = 0;
  Count boundary1 = 0;

  Count deficit() const { return safe - safe_images; }
  Count capacity() const { return boundary0 + boundary1; }
  Count e0() const { return safe_images + boundary0; }
  Count e1() const { return boundary1; }
  Count g() const { return capacity() - deficit(); }
};

struct Totals {
  Count safe = 0;
  Count safe_images = 0;
  Count boundary0 = 0;
  Count boundary1 = 0;

  void add(const ParameterCounts& value) {
    safe += value.safe;
    safe_images += value.safe_images;
    boundary0 += value.boundary0;
    boundary1 += value.boundary1;
  }

  Count deficit() const { return safe - safe_images; }
  Count capacity() const { return boundary0 + boundary1; }
  Count e0() const { return safe_images + boundary0; }
  Count e1() const { return boundary1; }
  Count g() const { return capacity() - deficit(); }
};

Mask value_bit(const int m, const int value) {
  return Mask{1} << (value + m);
}

Mask parameter_mask(const Mask optional_mask) {
  return (optional_mask << 1) | Mask{1};
}

Mask generator_mask(const int m, const Mask p_mask, const int b) {
  Mask result = value_bit(m, b) | value_bit(m, -b);
  Mask remaining = p_mask;
  while (remaining != 0) {
    const unsigned index =
        static_cast<unsigned>(__builtin_ctzll(remaining));
    const int p = static_cast<int>(index) + 1;
    const int value = b - p;
    if (-m <= value && value <= m) {
      result |= value_bit(m, value);
    }
    remaining &= remaining - 1;
  }
  return result;
}

Mask v_mask(const int m, const Mask p_mask) {
  Mask result = 0;
  Mask remaining = p_mask;
  while (remaining != 0) {
    const unsigned index =
        static_cast<unsigned>(__builtin_ctzll(remaining));
    const int p = static_cast<int>(index) + 1;
    result |= value_bit(m, m + 1 - p);
    remaining &= remaining - 1;
  }
  return result;
}

std::string decode_optional(const int m, const Mask optional_mask) {
  const Mask p_mask = parameter_mask(optional_mask);
  std::string result = "{";
  bool first = true;
  for (int p = 1; p <= 2 * m; ++p) {
    if ((p_mask & (Mask{1} << (p - 1))) == 0) {
      continue;
    }
    if (!first) {
      result += ",";
    }
    result += std::to_string(p);
    first = false;
  }
  result += "}";
  return result;
}

Options parse_options(const int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument(argv[index]);
    const auto next_integer = [&](const std::string& name) {
      if (++index == argc) {
        throw std::invalid_argument(name + " requires an integer");
      }
      return std::stoi(argv[index]);
    };
    if (argument == "--m") {
      options.m = next_integer(argument);
    } else if (argument == "--radius") {
      options.radius = next_integer(argument);
    } else if (argument == "--threads") {
      const int value = next_integer(argument);
      if (value < 1) {
        throw std::invalid_argument("--threads must be positive");
      }
      options.threads = static_cast<unsigned>(value);
    } else if (argument == "--print-witness") {
      options.print_witness = true;
    } else if (argument == "--details") {
      options.details = true;
    } else if (argument == "--net") {
      options.net = true;
    } else if (argument == "--reverse-order") {
      options.reverse_order = true;
    } else if (argument == "--help" || argument == "-h") {
      std::cout
          << "Usage: hall_transport [--m M] [--radius 1|2] "
             "[--threads T] [--print-witness] [--details] [--net] "
             "[--reverse-order]\n";
      std::exit(EXIT_SUCCESS);
    } else {
      throw std::invalid_argument("unknown argument: " + argument);
    }
  }
  if (options.m < 1 || options.m > 7) {
    throw std::invalid_argument("--m must lie between 1 and 7");
  }
  if (options.radius < 1 || options.radius > 2) {
    throw std::invalid_argument("--radius must be 1 or 2");
  }
  return options;
}

class FamilyWorkspace {
 public:
  explicit FamilyWorkspace(const int m)
      : m_(m),
        signature_limit_(std::size_t{1} << (2 * m + 1)),
        family_marks_(signature_limit_, 0),
        unsafe_marks_(signature_limit_, 0),
        safe_image_marks_(signature_limit_, 0),
        unsafe_image_marks_(signature_limit_, 0),
        union_image_marks_(signature_limit_, 0),
        direct_shadow_marks_(signature_limit_, 0) {
    generators_.reserve(static_cast<std::size_t>(2 * m));
    family_.reserve(std::size_t{1} << std::min(2 * m, 15));
    safe_.reserve(family_.capacity());
    unsafe_.reserve(family_.capacity());
  }

  ParameterCounts compute(const Mask optional_mask) {
    const Mask p_mask = parameter_mask(optional_mask);
    advance_stamp();

    generators_.clear();
    for (int b = -m_; b <= m_; ++b) {
      if (b == 0) {
        continue;
      }
      const Mask generator = generator_mask(m_, p_mask, b);
      if (std::find(generators_.begin(), generators_.end(), generator) ==
          generators_.end()) {
        generators_.push_back(generator);
      }
    }
    std::sort(generators_.begin(), generators_.end(),
              [](const Mask left, const Mask right) {
                const int left_size = __builtin_popcountll(left);
                const int right_size = __builtin_popcountll(right);
                if (left_size != right_size) {
                  return left_size > right_size;
                }
                return left > right;
              });

    family_.clear();
    family_.push_back(0);
    family_marks_[0] = stamp_;
    for (const Mask generator : generators_) {
      const std::size_t old_size = family_.size();
      for (std::size_t index = 0; index < old_size; ++index) {
        const Mask candidate = family_[index] | generator;
        if (family_marks_[static_cast<std::size_t>(candidate)] != stamp_) {
          family_marks_[static_cast<std::size_t>(candidate)] = stamp_;
          family_.push_back(candidate);
        }
      }
    }

    const Mask bottom = value_bit(m_, -m_);
    const Mask without_bottom = ~bottom;
    safe_.clear();
    unsafe_.clear();
    for (const Mask signature : family_) {
      if ((signature & bottom) == 0) {
        safe_.push_back(signature);
      } else {
        const Mask trace = signature & without_bottom;
        unsafe_.push_back(trace);
        unsafe_marks_[static_cast<std::size_t>(trace)] = stamp_;
      }
    }

    const Mask u = v_mask(m_, p_mask);
    ParameterCounts result;
    result.safe = static_cast<Count>(safe_.size());

    for (const Mask signature : safe_) {
      const Mask image = signature | u;
      if (safe_image_marks_[static_cast<std::size_t>(image)] != stamp_) {
        safe_image_marks_[static_cast<std::size_t>(image)] = stamp_;
        union_image_marks_[static_cast<std::size_t>(image)] = stamp_;
        ++result.safe_images;
      }
    }

    for (const Mask signature : unsafe_) {
      const Mask image = signature | u;
      if (unsafe_image_marks_[static_cast<std::size_t>(image)] != stamp_) {
        unsafe_image_marks_[static_cast<std::size_t>(image)] = stamp_;
        if (unsafe_marks_[static_cast<std::size_t>(image)] != stamp_) {
          ++result.boundary0;
        }
      }
      union_image_marks_[static_cast<std::size_t>(image)] = stamp_;
    }

    // Count the distinct union of the two image families outside H.
    for (std::size_t index = 0; index < signature_limit_; ++index) {
      if (union_image_marks_[index] == stamp_ &&
          unsafe_marks_[index] != stamp_) {
        ++result.boundary1;
      }
    }

    // Independently recompute e_0 and e_1 from the full union closure.  This
    // catches mistakes in the safe/unsafe partition before any flow is run.
    Count direct[2] = {0, 0};
    const Mask shadows[2] = {u, u | bottom};
    for (int alpha = 0; alpha < 2; ++alpha) {
      advance_shadow_stamp();
      for (const Mask signature : family_) {
        const Mask image = signature | shadows[alpha];
        const std::size_t image_index = static_cast<std::size_t>(image);
        if (family_marks_[image_index] != stamp_ &&
            direct_shadow_marks_[image_index] != shadow_stamp_) {
          direct_shadow_marks_[image_index] = shadow_stamp_;
          ++direct[alpha];
        }
      }
    }
    if (result.e0() != direct[0] || result.e1() != direct[1]) {
      throw std::logic_error("safe/unsafe identity failed at P=" +
                             decode_optional(m_, optional_mask));
    }
    if (result.deficit() < 0) {
      throw std::logic_error("negative collision deficit");
    }
    return result;
  }

 private:
  void advance_stamp() {
    ++stamp_;
    if (stamp_ == 0) {
      std::fill(family_marks_.begin(), family_marks_.end(), 0);
      std::fill(unsafe_marks_.begin(), unsafe_marks_.end(), 0);
      std::fill(safe_image_marks_.begin(), safe_image_marks_.end(), 0);
      std::fill(unsafe_image_marks_.begin(), unsafe_image_marks_.end(), 0);
      std::fill(union_image_marks_.begin(), union_image_marks_.end(), 0);
      ++stamp_;
    }
  }

  void advance_shadow_stamp() {
    ++shadow_stamp_;
    if (shadow_stamp_ == 0) {
      std::fill(direct_shadow_marks_.begin(), direct_shadow_marks_.end(), 0);
      ++shadow_stamp_;
    }
  }

  int m_;
  std::size_t signature_limit_;
  std::uint32_t stamp_ = 0;
  std::uint32_t shadow_stamp_ = 0;
  std::vector<std::uint32_t> family_marks_;
  std::vector<std::uint32_t> unsafe_marks_;
  std::vector<std::uint32_t> safe_image_marks_;
  std::vector<std::uint32_t> unsafe_image_marks_;
  std::vector<std::uint32_t> union_image_marks_;
  std::vector<std::uint32_t> direct_shadow_marks_;
  std::vector<Mask> generators_;
  std::vector<Mask> family_;
  std::vector<Mask> safe_;
  std::vector<Mask> unsafe_;
};

void compute_worker(const int m,
                    const unsigned worker_index,
                    const unsigned worker_count,
                    std::vector<ParameterCounts>& counts,
                    Totals& totals) {
  FamilyWorkspace workspace(m);
  for (Mask optional = worker_index; optional < counts.size();
       optional += worker_count) {
    counts[static_cast<std::size_t>(optional)] =
        workspace.compute(optional);
    totals.add(counts[static_cast<std::size_t>(optional)]);
  }
}

struct Edge {
  int to = 0;
  int reverse = 0;
  Count capacity = 0;
};

struct FlowPhase {
  int sink_level = 0;
  Count flow = 0;
  std::size_t pushes = 0;
};

class Dinic {
 public:
  explicit Dinic(const int node_count)
      : graph_(static_cast<std::size_t>(node_count)),
        level_(static_cast<std::size_t>(node_count)),
        next_(static_cast<std::size_t>(node_count)) {}

  int add_edge(const int from, const int to, const Count capacity) {
    const std::size_t from_index = static_cast<std::size_t>(from);
    const std::size_t to_index = static_cast<std::size_t>(to);
    const int index = static_cast<int>(graph_[from_index].size());
    const int reverse_index = static_cast<int>(graph_[to_index].size());
    graph_[from_index].push_back(Edge{to, reverse_index, capacity});
    graph_[to_index].push_back(Edge{from, index, 0});
    return index;
  }

  Count max_flow(const int source, const int sink) {
    Count result = 0;
    phases_.clear();
    while (build_levels(source, sink)) {
      std::fill(next_.begin(), next_.end(), 0);
      FlowPhase phase;
      phase.sink_level = level_[static_cast<std::size_t>(sink)];
      while (true) {
        const Count pushed =
            send(source, sink, std::numeric_limits<Count>::max() / 4);
        if (pushed == 0) {
          break;
        }
        result += pushed;
        phase.flow += pushed;
        ++phase.pushes;
      }
      phases_.push_back(phase);
    }
    return result;
  }

  const std::vector<FlowPhase>& phases() const { return phases_; }

  std::vector<bool> residual_reachable(const int source) const {
    std::vector<bool> reached(graph_.size(), false);
    std::queue<int> queue;
    reached[static_cast<std::size_t>(source)] = true;
    queue.push(source);
    while (!queue.empty()) {
      const int node = queue.front();
      queue.pop();
      for (const Edge& edge : graph_[static_cast<std::size_t>(node)]) {
        if (edge.capacity <= 0 ||
            reached[static_cast<std::size_t>(edge.to)]) {
          continue;
        }
        reached[static_cast<std::size_t>(edge.to)] = true;
        queue.push(edge.to);
      }
    }
    return reached;
  }

  const Edge& edge(const int from, const int index) const {
    return graph_[static_cast<std::size_t>(from)]
                 [static_cast<std::size_t>(index)];
  }

  const Edge& reverse_edge(const int from, const int index) const {
    const Edge& forward = edge(from, index);
    return graph_[static_cast<std::size_t>(forward.to)]
                 [static_cast<std::size_t>(forward.reverse)];
  }

 private:
  bool build_levels(const int source, const int sink) {
    std::fill(level_.begin(), level_.end(), -1);
    std::queue<int> queue;
    level_[static_cast<std::size_t>(source)] = 0;
    queue.push(source);
    while (!queue.empty()) {
      const int node = queue.front();
      queue.pop();
      for (const Edge& edge : graph_[static_cast<std::size_t>(node)]) {
        if (edge.capacity <= 0 ||
            level_[static_cast<std::size_t>(edge.to)] != -1) {
          continue;
        }
        level_[static_cast<std::size_t>(edge.to)] =
            level_[static_cast<std::size_t>(node)] + 1;
        queue.push(edge.to);
      }
    }
    return level_[static_cast<std::size_t>(sink)] != -1;
  }

  Count send(const int node, const int sink, const Count limit) {
    if (node == sink) {
      return limit;
    }
    for (int& index = next_[static_cast<std::size_t>(node)];
         index < static_cast<int>(graph_[static_cast<std::size_t>(node)].size());
         ++index) {
      Edge& edge = graph_[static_cast<std::size_t>(node)]
                        [static_cast<std::size_t>(index)];
      if (edge.capacity <= 0 ||
          level_[static_cast<std::size_t>(edge.to)] !=
              level_[static_cast<std::size_t>(node)] + 1) {
        continue;
      }
      const Count pushed =
          send(edge.to, sink, std::min(limit, edge.capacity));
      if (pushed == 0) {
        continue;
      }
      edge.capacity -= pushed;
      graph_[static_cast<std::size_t>(edge.to)]
            [static_cast<std::size_t>(edge.reverse)]
                .capacity += pushed;
      return pushed;
    }
    return 0;
  }

  std::vector<std::vector<Edge>> graph_;
  std::vector<int> level_;
  std::vector<int> next_;
  std::vector<FlowPhase> phases_;
};

struct TransportEdge {
  Mask source = 0;
  Mask destination = 0;
  int distance = 0;
  int graph_index = 0;
};

std::uint64_t hash_masks(const std::vector<Mask>& masks) {
  std::uint64_t hash = 1469598103934665603ULL;
  for (const Mask mask : masks) {
    for (int byte = 0; byte < 8; ++byte) {
      hash ^= (mask >> (8 * byte)) & 255ULL;
      hash *= 1099511628211ULL;
    }
  }
  return hash;
}

void print_rank_histogram(const std::string& label,
                          const std::vector<Mask>& masks,
                          const int optional_bits) {
  std::vector<std::size_t> histogram(
      static_cast<std::size_t>(optional_bits + 1), 0);
  for (const Mask mask : masks) {
    ++histogram[static_cast<std::size_t>(__builtin_popcountll(mask))];
  }
  std::cout << label << "_rank_histogram=";
  for (int rank = 0; rank <= optional_bits; ++rank) {
    if (rank != 0) {
      std::cout << ',';
    }
    std::cout << rank << ':' << histogram[static_cast<std::size_t>(rank)];
  }
  std::cout << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    const int optional_bits = 2 * options.m - 1;
    const std::size_t parameter_count =
        std::size_t{1} << optional_bits;
    std::vector<ParameterCounts> counts(parameter_count);
    std::vector<Totals> local_totals(options.threads);
    std::vector<std::thread> workers;
    workers.reserve(options.threads);

    const auto start = std::chrono::steady_clock::now();
    for (unsigned worker = 0; worker < options.threads; ++worker) {
      workers.emplace_back(compute_worker, options.m, worker,
                           options.threads, std::ref(counts),
                           std::ref(local_totals[worker]));
    }
    for (std::thread& worker : workers) {
      worker.join();
    }
    Totals totals;
    for (const Totals& local : local_totals) {
      totals.safe += local.safe;
      totals.safe_images += local.safe_images;
      totals.boundary0 += local.boundary0;
      totals.boundary1 += local.boundary1;
    }
    const auto count_stop = std::chrono::steady_clock::now();

    const int left_offset = 0;
    const int right_offset = static_cast<int>(parameter_count);
    const int source = 2 * static_cast<int>(parameter_count);
    const int sink = source + 1;
    Dinic flow(sink + 1);
    std::vector<Count> supplies(parameter_count, 0);
    std::vector<Count> capacities(parameter_count, 0);
    Count transport_supply = 0;
    Count transport_capacity = 0;
    for (Mask p = 0; p < parameter_count; ++p) {
      const ParameterCounts& profile =
          counts[static_cast<std::size_t>(p)];
      if (options.net) {
        supplies[static_cast<std::size_t>(p)] =
            std::max<Count>(0, -profile.g());
        capacities[static_cast<std::size_t>(p)] =
            std::max<Count>(0, profile.g());
      } else {
        supplies[static_cast<std::size_t>(p)] = profile.deficit();
        capacities[static_cast<std::size_t>(p)] = profile.capacity();
      }
      transport_supply += supplies[static_cast<std::size_t>(p)];
      transport_capacity += capacities[static_cast<std::size_t>(p)];
    }
    const Count infinity = transport_supply + 1;
    std::vector<TransportEdge> transport_edges;
    transport_edges.reserve(
        parameter_count * static_cast<std::size_t>(
                              1 + optional_bits +
                              (options.radius == 2
                                   ? optional_bits * (optional_bits - 1) / 2
                                   : 0)));

    std::vector<Mask> parameter_order(parameter_count);
    std::iota(parameter_order.begin(), parameter_order.end(), Mask{0});
    if (options.reverse_order) {
      std::reverse(parameter_order.begin(), parameter_order.end());
    }
    for (const Mask p : parameter_order) {
      const int left = left_offset + static_cast<int>(p);
      const int right = right_offset + static_cast<int>(p);
      flow.add_edge(source, left, supplies[static_cast<std::size_t>(p)]);
      flow.add_edge(right, sink, capacities[static_cast<std::size_t>(p)]);

      const int diagonal_index = flow.add_edge(left, right, infinity);
      transport_edges.push_back(TransportEdge{p, p, 0, diagonal_index});

      std::vector<int> present;
      Mask remaining = p;
      while (remaining != 0) {
        const int bit = __builtin_ctzll(remaining);
        present.push_back(bit);
        remaining &= remaining - 1;
      }
      if (options.reverse_order) {
        std::reverse(present.begin(), present.end());
      }
      for (const int bit : present) {
        const Mask q = p ^ (Mask{1} << bit);
        const int edge_index =
            flow.add_edge(left, right_offset + static_cast<int>(q), infinity);
        transport_edges.push_back(TransportEdge{p, q, 1, edge_index});
      }
      if (options.radius == 2) {
        for (std::size_t first = 0; first < present.size(); ++first) {
          for (std::size_t second = first + 1; second < present.size();
               ++second) {
            const Mask q =
                p ^ (Mask{1} << present[first]) ^
                (Mask{1} << present[second]);
            const int edge_index = flow.add_edge(
                left, right_offset + static_cast<int>(q), infinity);
            transport_edges.push_back(
                TransportEdge{p, q, 2, edge_index});
          }
        }
      }
    }

    const auto graph_stop = std::chrono::steady_clock::now();
    const Count maximum = flow.max_flow(source, sink);
    const auto flow_stop = std::chrono::steady_clock::now();

    std::vector<Count> distance_flow(
        static_cast<std::size_t>(options.radius + 1), 0);
    std::vector<std::size_t> distance_edges(
        static_cast<std::size_t>(options.radius + 1), 0);
    std::vector<std::size_t> source_degree(parameter_count, 0);
    std::vector<std::size_t> destination_degree(parameter_count, 0);
    std::vector<Count> cross_out(parameter_count, 0);
    std::vector<Count> cross_in(parameter_count, 0);
    std::vector<Count> deleted_coordinate(
        static_cast<std::size_t>(2 * options.m + 1), 0);
    std::vector<int> longest_support_path(parameter_count, 0);
    Count largest_edge_flow = 0;
    for (const TransportEdge& transport : transport_edges) {
      const int left = left_offset + static_cast<int>(transport.source);
      const Count used =
          flow.reverse_edge(left, transport.graph_index).capacity;
      if (used == 0) {
        continue;
      }
      distance_flow[static_cast<std::size_t>(transport.distance)] += used;
      ++distance_edges[static_cast<std::size_t>(transport.distance)];
      ++source_degree[static_cast<std::size_t>(transport.source)];
      ++destination_degree[static_cast<std::size_t>(transport.destination)];
      largest_edge_flow = std::max(largest_edge_flow, used);
      if (transport.distance != 0) {
        cross_out[static_cast<std::size_t>(transport.source)] += used;
        cross_in[static_cast<std::size_t>(transport.destination)] += used;
      }
      if (transport.distance == 1) {
        const Mask difference = transport.source ^ transport.destination;
        const int parameter = __builtin_ctzll(difference) + 2;
        deleted_coordinate[static_cast<std::size_t>(parameter)] += used;
        longest_support_path[static_cast<std::size_t>(transport.source)] =
            std::max(
                longest_support_path[
                    static_cast<std::size_t>(transport.source)],
                1 + longest_support_path[
                        static_cast<std::size_t>(transport.destination)]);
      }
    }
    const std::size_t max_source_degree =
        *std::max_element(source_degree.begin(), source_degree.end());
    const std::size_t max_destination_degree =
        *std::max_element(destination_degree.begin(),
                          destination_degree.end());
    const int max_support_path =
        *std::max_element(longest_support_path.begin(),
                          longest_support_path.end());

    const double count_seconds =
        std::chrono::duration<double>(count_stop - start).count();
    const double graph_seconds =
        std::chrono::duration<double>(graph_stop - count_stop).count();
    const double flow_seconds =
        std::chrono::duration<double>(flow_stop - graph_stop).count();

    std::cout << "m=" << options.m << " radius=" << options.radius
              << " mode=" << (options.net ? "net" : "raw")
              << " threads=" << options.threads
              << " parameters=" << parameter_count << '\n';
    std::cout << "safe=" << totals.safe
              << " safe_images=" << totals.safe_images
              << " deficit=" << totals.deficit()
              << " boundary0=" << totals.boundary0
              << " boundary1=" << totals.boundary1
              << " capacity=" << totals.capacity() << '\n';
    std::cout << "e0=" << totals.e0() << " e1=" << totals.e1()
              << " g=" << totals.g() << '\n';
    std::cout << "transport_supply=" << transport_supply
              << " transport_capacity=" << transport_capacity << '\n';
    std::cout << "transport_edges=" << transport_edges.size()
              << " maximum_flow=" << maximum
              << " unmatched=" << (transport_supply - maximum)
              << " status="
              << (maximum == transport_supply ? "FULL" : "HALL_FAILURE")
              << '\n';
    std::cout << "used_flow_by_distance=";
    for (int distance = 0; distance <= options.radius; ++distance) {
      if (distance != 0) {
        std::cout << ',';
      }
      std::cout << distance << ':'
                << distance_flow[static_cast<std::size_t>(distance)];
    }
    std::cout << '\n';
    std::cout << "used_edges_by_distance=";
    for (int distance = 0; distance <= options.radius; ++distance) {
      if (distance != 0) {
        std::cout << ',';
      }
      std::cout << distance << ':'
                << distance_edges[static_cast<std::size_t>(distance)];
    }
    std::cout << '\n';
    std::cout << "largest_edge_flow=" << largest_edge_flow
              << " max_source_support=" << max_source_degree
              << " max_destination_support=" << max_destination_degree
              << " max_cross_support_path=" << max_support_path
              << '\n';
    std::cout << "flow_phases=" << flow.phases().size();
    for (std::size_t index = 0; index < flow.phases().size(); ++index) {
      const FlowPhase& phase = flow.phases()[index];
      std::cout << " [" << (index + 1) << ":level=" << phase.sink_level
                << ",flow=" << phase.flow
                << ",pushes=" << phase.pushes << ']';
    }
    std::cout << '\n';
    if (options.radius >= 1) {
      std::cout << "deleted_coordinate_flow=";
      for (int parameter = 2; parameter <= 2 * options.m; ++parameter) {
        if (parameter != 2) {
          std::cout << ',';
        }
        std::cout
            << parameter << ':'
            << deleted_coordinate[static_cast<std::size_t>(parameter)];
      }
      std::cout << '\n';
    }

    if (options.details) {
      std::vector<Mask> cross_sources;
      for (Mask p = 0; p < parameter_count; ++p) {
        if (cross_out[static_cast<std::size_t>(p)] != 0) {
          cross_sources.push_back(p);
        }
      }
      std::sort(cross_sources.begin(), cross_sources.end(),
                [&](const Mask left, const Mask right) {
                  const Count left_flow =
                      cross_out[static_cast<std::size_t>(left)];
                  const Count right_flow =
                      cross_out[static_cast<std::size_t>(right)];
                  if (left_flow != right_flow) {
                    return left_flow > right_flow;
                  }
                  return left < right;
                });
      const std::size_t detail_limit =
          std::min<std::size_t>(25, cross_sources.size());
      std::cout << "TOP_CROSS_SOURCES_BEGIN\n";
      for (std::size_t source_index = 0; source_index < detail_limit;
           ++source_index) {
        const Mask p = cross_sources[source_index];
        const ParameterCounts& profile =
            counts[static_cast<std::size_t>(p)];
        std::cout << p << ' ' << decode_optional(options.m, p)
                  << " d=" << profile.deficit()
                  << " b=" << profile.capacity()
                  << " g=" << profile.g()
                  << " cross_out="
                  << cross_out[static_cast<std::size_t>(p)]
                  << " routes=";
        bool first_route = true;
        for (const TransportEdge& transport : transport_edges) {
          if (transport.source != p || transport.distance == 0) {
            continue;
          }
          const int left =
              left_offset + static_cast<int>(transport.source);
          const Count used =
              flow.reverse_edge(left, transport.graph_index).capacity;
          if (used == 0) {
            continue;
          }
          if (!first_route) {
            std::cout << ';';
          }
          std::cout << decode_optional(options.m, transport.destination)
                    << ':' << used;
          first_route = false;
        }
        std::cout << '\n';
      }
      std::cout << "TOP_CROSS_SOURCES_END\n";
      if (options.radius == 2) {
        std::cout << "DISTANCE_TWO_ROUTES_BEGIN\n";
        for (const TransportEdge& transport : transport_edges) {
          if (transport.distance != 2) {
            continue;
          }
          const int left =
              left_offset + static_cast<int>(transport.source);
          const Count used =
              flow.reverse_edge(left, transport.graph_index).capacity;
          if (used == 0) {
            continue;
          }
          const Mask difference =
              transport.source ^ transport.destination;
          const int first = __builtin_ctzll(difference) + 2;
          const int second =
              __builtin_ctzll(difference & (difference - 1)) + 2;
          std::cout << decode_optional(options.m, transport.source)
                    << " -> "
                    << decode_optional(options.m, transport.destination)
                    << " delete={" << first << ',' << second
                    << "} flow=" << used << '\n';
        }
        std::cout << "DISTANCE_TWO_ROUTES_END\n";
      }
    }

    if (maximum != transport_supply) {
      const std::vector<bool> reached = flow.residual_reachable(source);
      std::vector<Mask> left_witness;
      std::vector<Mask> right_neighborhood;
      Count witness_supply = 0;
      Count neighborhood_capacity = 0;
      for (Mask p = 0; p < parameter_count; ++p) {
        if (reached[static_cast<std::size_t>(
                left_offset + static_cast<int>(p))]) {
          left_witness.push_back(p);
          witness_supply += supplies[static_cast<std::size_t>(p)];
        }
        if (reached[static_cast<std::size_t>(
                right_offset + static_cast<int>(p))]) {
          right_neighborhood.push_back(p);
          neighborhood_capacity +=
              capacities[static_cast<std::size_t>(p)];
        }
      }
      std::cout << "hall_left_count=" << left_witness.size()
                << " hall_left_supply=" << witness_supply
                << " hall_neighbor_count=" << right_neighborhood.size()
                << " hall_neighbor_capacity=" << neighborhood_capacity
                << " hall_deficiency="
                << (witness_supply - neighborhood_capacity) << '\n';
      std::cout << std::hex << std::setfill('0')
                << "hall_left_hash=0x" << std::setw(16)
                << hash_masks(left_witness)
                << " hall_neighbor_hash=0x" << std::setw(16)
                << hash_masks(right_neighborhood) << std::dec
                << std::setfill(' ') << '\n';
      print_rank_histogram("hall_left", left_witness, optional_bits);
      print_rank_histogram("hall_neighbor", right_neighborhood,
                           optional_bits);
      if (options.print_witness) {
        std::cout << "HALL_LEFT_BEGIN\n";
        for (const Mask p : left_witness) {
          std::cout << p << ' ' << decode_optional(options.m, p)
                    << " d="
                    << counts[static_cast<std::size_t>(p)].deficit()
                    << " b="
                    << counts[static_cast<std::size_t>(p)].capacity()
                    << '\n';
        }
        std::cout << "HALL_LEFT_END\nHALL_NEIGHBOR_BEGIN\n";
        for (const Mask p : right_neighborhood) {
          std::cout << p << ' ' << decode_optional(options.m, p)
                    << " d="
                    << counts[static_cast<std::size_t>(p)].deficit()
                    << " b="
                    << counts[static_cast<std::size_t>(p)].capacity()
                    << '\n';
        }
        std::cout << "HALL_NEIGHBOR_END\n";
      }
    }

    std::cout << std::fixed << std::setprecision(6)
              << "count_seconds=" << count_seconds
              << " graph_seconds=" << graph_seconds
              << " flow_seconds=" << flow_seconds
              << " total_seconds="
              << std::chrono::duration<double>(flow_stop - start).count()
              << '\n';
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
