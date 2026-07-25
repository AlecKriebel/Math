// Exact representation-aware Hall verifier for the Boolean down-set program.
//
// This file is intentionally independent of hall_transport.cpp.  The latter
// tests a count-only transportation graph, while this program requires every
// edge to have a generator-representation certificate.
//
// Fix x=-m.  For a parameter set P containing 1, write
//
//   A_P = { C in F_m(P) : x notin C },
//   H_P = { C\{x} : C in F_m(P), x in C },
//   U_P = V(P),                 pi_P(C) = C\U_P.
//
// A left unit is a non-top member A of a pi_P-fibre in A_P.  (Every such
// fibre is union closed and hence has a unique top.)  The two typed right
// units are
//
//   R^0_P = { (P,0,T) : T in pi_P(H_P)\K_P },
//   R^1_P = { (P,1,T) : T in (pi_P(A_P) union pi_P(H_P))\K_P },
//   K_P   = { T : T union U_P is in H_P }.
//
// The same trace T in types 0 and 1 is two distinct capacity-one vertices.
// In fact their underlying trace sets are always equal when 1 is in P.
// Indeed G_P(-m)={-m,m}, and m is in U_P.  Thus every safe A produces
// h=A union {m} in H_P, whence A union U_P=h union U_P lies in H_P join U_P.
// Therefore A_P join U_P is contained in H_P join U_P and the two original
// boundary sets B_0 and B_1 coincide setwise.  The verifier checks this for
// every profile.  Keeping the colors explicit records that each trace still
// has capacity two (equivalently, an untyped 2-congestion target).
//
// An edge (P,A) -> (Q,t,T) is present exactly when all of the following hold:
//
//   (i)  Q is P or is obtained from P by deleting one element other than 1;
//   (ii) B,B' are subsets of the ORIGINAL 2m labelled generator rows
//        J_m={-m,...,-1,1,...,m}; duplicate row signatures are not merged;
//   (iii) Phi_P(B)=A; and
//   (iv) Phi_Q(B') yields the typed right trace:
//          x absent  => only type 1, T=pi_Q(Phi_Q(B'));
//          x present => types 0 and/or 1,
//                       T=pi_Q(Phi_Q(B')\{x}),
//        subject in either case to that typed vertex actually existing.
//
// The row-edit condition has two deliberately separate stages.
//
//   stage A ("one local edit"):
//       |B\B'| <= 1 and |B'\B| <= 1.
//       Thus it permits no edit, one add, one remove, or one genuine exchange.
//
//   stage B (the sole enlargement):
//       |B triangle B'| <= 2.
//       It adds exactly the two same-direction cases (two adds or two
//       removals).  No larger row radius and no parameter radius two is used.
//
// Consequently the often-used shorthand "|B triangle B'|<=2 is one row
// exchange" is false for subsets: it also contains two additions and two
// removals.  Reporting stages A and B separately prevents that ambiguity.
//
// A saturated matching is a simultaneous injection for all P.  Since every
// edge points from P down to Q, it restricts to each principal parameter
// ideal and proves its exact deficit/capacity inequality.
//
// Implementation notes:
//   * m is hard-limited to 7.
//   * All Phi_P(B) values are cached as uint16_t (at m=7 there are 15 value
//     coordinates), about 256 MiB.
//   * A left signature stores only its representation list.  Its shared
//     row-neighbourhood is generated once per stage and reused for every
//     allowed child Q.
//   * Edges are deduplicated at the typed right vertex while retaining a
//     canonical exact certificate (deleted parameter, B, B').
//   * Hopcroft--Karp records exact augmenting-depth histograms and compressed
//     alternating certificate templates.  On failure, residual reachability
//     emits an exact maximum-deficiency Hall set.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

using Signature = std::uint16_t;
using Selection = std::uint16_t;
using Parameter = std::uint16_t;
using Vertex = std::uint32_t;
using Certificate = std::uint64_t;

constexpr Vertex kNoVertex = std::numeric_limits<Vertex>::max();
constexpr int kInfinity = std::numeric_limits<int>::max() / 4;

enum class Stage : int {
  kOneLocalEdit = 1,
  kHammingRadiusTwo = 2,
};

// The first two rules are used only to reproduce the earlier m<=5 prototype
// numbers.  They are subgraphs, not additional discovery stages.
enum class ReachRule : int {
  kSameRepresentative = 0,
  kHammingRadiusOne = 1,
  kOneLocalEdit = 2,
  kHammingRadiusTwo = 3,
};

enum class MoveType : std::uint8_t {
  kNone = 0,
  kAdd = 1,
  kRemove = 2,
  kExchange = 3,
  kDoubleAdd = 4,
  kDoubleRemove = 5,
};

struct Options {
  int m = 0;
  unsigned threads = 2;
  bool run_both = false;
  bool stage_a_only = false;
  bool quiet_progress = false;
};

struct LeftDescriptor {
  Vertex id = kNoVertex;
  Signature signature = 0;
  std::vector<Selection> representations;
};

struct RightTrace {
  Signature trace = 0;
  Vertex type0 = kNoVertex;
  Vertex type1 = kNoVertex;
};

struct Profile {
  Signature u = 0;
  std::uint32_t family_size = 0;
  std::uint32_t safe_size = 0;
  std::uint32_t safe_images = 0;
  std::uint32_t boundary0 = 0;
  std::uint32_t boundary1 = 0;
  std::vector<LeftDescriptor> left;
  std::vector<RightTrace> right;
};

struct Edge {
  Vertex right = kNoVertex;
  Certificate certificate = 0;
};

struct ReachChoice {
  Selection target = 0;
  Selection representative = 0;
};

struct AlternatingSegment {
  Certificate forward = 0;
  Certificate backward = 0;
  bool has_backward = false;
  bool forward_is_new = false;
  bool backward_is_new = false;
};

struct MatchStats {
  std::uint64_t matching = 0;
  std::map<int, std::uint64_t> depth_histogram;
  std::map<int, std::uint64_t> phase_augmentations;
  std::map<std::string, std::uint64_t> path_templates;
  std::map<std::string, std::uint64_t> forward_templates;
  std::map<std::string, std::uint64_t> new_forward_templates;
  std::map<std::string, std::uint64_t> new_backward_templates;
  std::map<std::string, std::uint64_t> alternating_transitions;
  int max_depth = 0;
  int phases = 0;
  std::uint64_t augmentations = 0;
  std::uint64_t paths_using_new_edges = 0;
  std::uint64_t new_forward_edges = 0;
  std::uint64_t new_backward_edges = 0;
};

struct GraphStats {
  std::uint64_t edges = 0;
  std::uint64_t isolated_left = 0;
  std::size_t min_degree = 0;
  std::size_t max_degree = 0;
  long double mean_degree = 0.0L;
  std::map<std::string, std::uint64_t> edge_templates;
};

struct HallWitness {
  std::uint64_t left_size = 0;
  std::uint64_t neighbor_size = 0;
  std::uint64_t excess = 0;
  std::uint64_t profiles_touched = 0;
  std::vector<Vertex> unmatched_left;
};

std::string stage_name(const Stage stage) {
  return stage == Stage::kOneLocalEdit ? "A_one_local_edit"
                                       : "B_hamming_radius_two";
}

std::string move_name(const MoveType move) {
  switch (move) {
    case MoveType::kNone:
      return "none";
    case MoveType::kAdd:
      return "add";
    case MoveType::kRemove:
      return "remove";
    case MoveType::kExchange:
      return "exchange";
    case MoveType::kDoubleAdd:
      return "double_add";
    case MoveType::kDoubleRemove:
      return "double_remove";
  }
  throw std::logic_error("unknown move type");
}

Signature value_bit(const int m, const int value) {
  return static_cast<Signature>(Signature{1} << (value + m));
}

Parameter full_parameter_mask(const Parameter optional) {
  return static_cast<Parameter>((optional << 1) | Parameter{1});
}

Signature generator_mask(const int m,
                         const Parameter full_parameter,
                         const int row) {
  Signature result =
      static_cast<Signature>(value_bit(m, row) | value_bit(m, -row));
  Parameter remaining = full_parameter;
  while (remaining != 0) {
    const int index = __builtin_ctz(static_cast<unsigned>(remaining));
    const int p = index + 1;
    const int value = row - p;
    if (-m <= value && value <= m) {
      result = static_cast<Signature>(result | value_bit(m, value));
    }
    remaining = static_cast<Parameter>(remaining & (remaining - 1));
  }
  return result;
}

Signature u_mask(const int m, const Parameter full_parameter) {
  Signature result = 0;
  Parameter remaining = full_parameter;
  while (remaining != 0) {
    const int index = __builtin_ctz(static_cast<unsigned>(remaining));
    const int p = index + 1;
    result =
        static_cast<Signature>(result | value_bit(m, m + 1 - p));
    remaining = static_cast<Parameter>(remaining & (remaining - 1));
  }
  return result;
}

std::vector<int> row_labels(const int m) {
  std::vector<int> rows;
  rows.reserve(static_cast<std::size_t>(2 * m));
  for (int row = -m; row <= m; ++row) {
    if (row != 0) {
      rows.push_back(row);
    }
  }
  return rows;
}

std::string decode_parameter(const int m, const Parameter optional) {
  const Parameter full = full_parameter_mask(optional);
  std::ostringstream output;
  output << '{';
  bool first = true;
  for (int p = 1; p <= 2 * m; ++p) {
    if ((full & (Parameter{1} << (p - 1))) == 0) {
      continue;
    }
    if (!first) {
      output << ',';
    }
    output << p;
    first = false;
  }
  output << '}';
  return output.str();
}

std::string decode_signature(const int m, const Signature signature) {
  std::ostringstream output;
  output << '{';
  bool first = true;
  for (int value = -m; value <= m; ++value) {
    if ((signature & value_bit(m, value)) == 0) {
      continue;
    }
    if (!first) {
      output << ',';
    }
    output << value;
    first = false;
  }
  output << '}';
  return output.str();
}

MoveType classify_move(const Selection from, const Selection to) {
  const Selection removed = static_cast<Selection>(from & ~to);
  const Selection added = static_cast<Selection>(to & ~from);
  const int remove_count =
      __builtin_popcount(static_cast<unsigned>(removed));
  const int add_count = __builtin_popcount(static_cast<unsigned>(added));
  if (remove_count == 0 && add_count == 0) {
    return MoveType::kNone;
  }
  if (remove_count == 0 && add_count == 1) {
    return MoveType::kAdd;
  }
  if (remove_count == 1 && add_count == 0) {
    return MoveType::kRemove;
  }
  if (remove_count == 1 && add_count == 1) {
    return MoveType::kExchange;
  }
  if (remove_count == 0 && add_count == 2) {
    return MoveType::kDoubleAdd;
  }
  if (remove_count == 2 && add_count == 0) {
    return MoveType::kDoubleRemove;
  }
  throw std::logic_error("move outside the frozen stages");
}

// Certificate ordering is deterministic: local Q before a deletion, then
// deleted coordinate, move type, representative B, and target B'.
Certificate pack_certificate(const int deleted_parameter,
                             const Selection representative,
                             const Selection target) {
  const MoveType move = classify_move(representative, target);
  return (static_cast<Certificate>(deleted_parameter) << 40) |
         (static_cast<Certificate>(move) << 36) |
         (static_cast<Certificate>(representative) << 18) |
         static_cast<Certificate>(target);
}

int certificate_deleted_parameter(const Certificate certificate) {
  return static_cast<int>((certificate >> 40) & 0x1f);
}

MoveType certificate_move(const Certificate certificate) {
  return static_cast<MoveType>((certificate >> 36) & 0x0f);
}

Selection certificate_from(const Certificate certificate) {
  return static_cast<Selection>((certificate >> 18) & 0xffff);
}

Selection certificate_to(const Certificate certificate) {
  return static_cast<Selection>(certificate & 0x3ffff);
}

std::string coarse_certificate(const Certificate certificate) {
  std::ostringstream output;
  const int deleted = certificate_deleted_parameter(certificate);
  output << (deleted == 0 ? "q0:" : "q1:") << move_name(
      certificate_move(certificate));
  return output.str();
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
    } else if (argument == "--threads") {
      const int value = next_integer(argument);
      if (value < 1 || value > 8) {
        throw std::invalid_argument("--threads must lie in [1,8]");
      }
      options.threads = static_cast<unsigned>(value);
    } else if (argument == "--run-both") {
      options.run_both = true;
    } else if (argument == "--stage-a-only") {
      options.stage_a_only = true;
    } else if (argument == "--quiet-progress") {
      options.quiet_progress = true;
    } else if (argument == "--help" || argument == "-h") {
      std::cout
          << "Usage: representation_hall --m M [--threads T] [--run-both] "
             "[--stage-a-only] [--quiet-progress]\n"
          << "  M must lie in [3,7].  By default stage B runs only if stage A "
             "fails.\n";
      std::exit(EXIT_SUCCESS);
    } else {
      throw std::invalid_argument("unknown argument: " + argument);
    }
  }
  if (options.m < 3 || options.m > 7) {
    throw std::invalid_argument("--m must lie in [3,7]");
  }
  if (options.run_both && options.stage_a_only) {
    throw std::invalid_argument(
        "--run-both and --stage-a-only are incompatible");
  }
  return options;
}

class RepresentationExperiment {
 public:
  explicit RepresentationExperiment(const Options options)
      : options_(options),
        m_(options.m),
        row_count_(2 * m_),
        selection_count_(std::size_t{1} << row_count_),
        signature_count_(std::size_t{1} << (2 * m_ + 1)),
        profile_count_(std::size_t{1} << (2 * m_ - 1)),
        rows_(row_labels(m_)),
        signatures_(checked_signature_table_size()),
        profiles_(profile_count_) {}

  void run() {
    const auto start = std::chrono::steady_clock::now();
    build_signature_table();
    build_profiles();
    validate_profile_totals();
    print_enumeration_summary(start);
    if (m_ <= 5) {
      run_small_regressions();
    }

    const bool stage_a_saturated = run_stage(Stage::kOneLocalEdit);
    if (options_.run_both ||
        (!options_.stage_a_only && !stage_a_saturated)) {
      run_stage(Stage::kHammingRadiusTwo);
      if (!stage_a_saturated) {
        run_incremental_repair();
      }
    }
  }

 private:
  std::size_t checked_signature_table_size() const {
    const std::uint64_t entries =
        static_cast<std::uint64_t>(selection_count_) * profile_count_;
    const std::uint64_t bytes = entries * sizeof(Signature);
    constexpr std::uint64_t kCeiling = UINT64_C(512) * 1024 * 1024;
    if (bytes > kCeiling) {
      throw std::runtime_error(
          "signature cache would exceed the 512 MiB safety ceiling");
    }
    return static_cast<std::size_t>(entries);
  }

  Signature* signature_row(const Parameter parameter) {
    return signatures_.data() +
           static_cast<std::size_t>(parameter) * selection_count_;
  }

  const Signature* signature_row(const Parameter parameter) const {
    return signatures_.data() +
           static_cast<std::size_t>(parameter) * selection_count_;
  }

  void build_signature_worker(const unsigned worker,
                              const unsigned worker_count) {
    std::vector<Signature> generators(static_cast<std::size_t>(row_count_));
    for (std::size_t parameter = worker; parameter < profile_count_;
         parameter += worker_count) {
      const Parameter full =
          full_parameter_mask(static_cast<Parameter>(parameter));
      for (int row_index = 0; row_index < row_count_; ++row_index) {
        generators[static_cast<std::size_t>(row_index)] =
            generator_mask(m_, full,
                           rows_[static_cast<std::size_t>(row_index)]);
      }
      Signature* values = signature_row(static_cast<Parameter>(parameter));
      values[0] = 0;
      for (std::size_t selection = 1; selection < selection_count_;
           ++selection) {
        const int bit = __builtin_ctz(static_cast<unsigned>(selection));
        const std::size_t previous = selection & (selection - 1);
        values[selection] = static_cast<Signature>(
            values[previous] | generators[static_cast<std::size_t>(bit)]);
      }
    }
  }

  void build_signature_table() {
    const auto start = std::chrono::steady_clock::now();
    const unsigned worker_count =
        std::min<unsigned>(options_.threads,
                           static_cast<unsigned>(profile_count_));
    std::vector<std::thread> workers;
    workers.reserve(worker_count);
    for (unsigned worker = 0; worker < worker_count; ++worker) {
      workers.emplace_back(&RepresentationExperiment::build_signature_worker,
                           this, worker, worker_count);
    }
    for (std::thread& worker : workers) {
      worker.join();
    }
    const double seconds =
        std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                     start)
            .count();
    std::cout << "signature_cache entries=" << signatures_.size()
              << " bytes=" << signatures_.size() * sizeof(Signature)
              << " seconds=" << std::fixed << std::setprecision(3) << seconds
              << '\n';
  }

  void build_profiles() {
    const Signature bottom = value_bit(m_, -m_);
    const Signature without_bottom =
        static_cast<Signature>(
            static_cast<Signature>(signature_count_ - 1) ^ bottom);

    std::vector<std::uint8_t> family(signature_count_, 0);
    std::vector<std::uint8_t> h_family(signature_count_, 0);
    std::vector<std::uint8_t> pi_a(signature_count_, 0);
    std::vector<std::uint8_t> pi_h(signature_count_, 0);
    std::vector<std::uint8_t> fibre_seen(signature_count_, 0);
    std::vector<Signature> fibre_top(signature_count_, 0);
    std::vector<int> local_left(signature_count_, -1);
    std::vector<Signature> family_list;
    family_list.reserve(selection_count_);

    for (std::size_t parameter_index = 0; parameter_index < profile_count_;
         ++parameter_index) {
      std::fill(family.begin(), family.end(), 0);
      std::fill(h_family.begin(), h_family.end(), 0);
      std::fill(pi_a.begin(), pi_a.end(), 0);
      std::fill(pi_h.begin(), pi_h.end(), 0);
      std::fill(fibre_seen.begin(), fibre_seen.end(), 0);
      std::fill(fibre_top.begin(), fibre_top.end(), 0);
      std::fill(local_left.begin(), local_left.end(), -1);
      family_list.clear();

      const Parameter parameter =
          static_cast<Parameter>(parameter_index);
      const Parameter full = full_parameter_mask(parameter);
      Profile& profile = profiles_[parameter_index];
      profile.u = u_mask(m_, full);
      const Signature outside_u = static_cast<Signature>(
          static_cast<Signature>(signature_count_ - 1) ^ profile.u);
      const Signature* values = signature_row(parameter);

      for (std::size_t selection = 0; selection < selection_count_;
           ++selection) {
        const Signature signature = values[selection];
        if (family[signature] == 0) {
          family[signature] = 1;
          family_list.push_back(signature);
        }
      }
      std::sort(family_list.begin(), family_list.end());
      profile.family_size =
          static_cast<std::uint32_t>(family_list.size());

      for (const Signature signature : family_list) {
        if ((signature & bottom) == 0) {
          ++profile.safe_size;
          const Signature trace =
              static_cast<Signature>(signature & outside_u);
          pi_a[trace] = 1;
          if (fibre_seen[trace] == 0) {
            fibre_seen[trace] = 1;
            fibre_top[trace] = signature;
          } else {
            fibre_top[trace] =
                static_cast<Signature>(fibre_top[trace] | signature);
          }
        } else {
          const Signature h =
              static_cast<Signature>(signature & without_bottom);
          h_family[h] = 1;
          pi_h[static_cast<Signature>(h & outside_u)] = 1;
        }
      }

      for (std::size_t trace = 0; trace < signature_count_; ++trace) {
        if (pi_a[trace] != 0) {
          ++profile.safe_images;
          const Signature top = fibre_top[trace];
          if (family[top] == 0 || (top & bottom) != 0) {
            throw std::logic_error("pi_A fibre top is not safe family");
          }
        }
      }

      std::vector<Signature> left_signatures;
      for (const Signature signature : family_list) {
        if ((signature & bottom) != 0) {
          continue;
        }
        const Signature trace =
            static_cast<Signature>(signature & outside_u);
        if (signature != fibre_top[trace]) {
          left_signatures.push_back(signature);
        }
      }
      profile.left.reserve(left_signatures.size());
      for (const Signature signature : left_signatures) {
        const int local = static_cast<int>(profile.left.size());
        local_left[signature] = local;
        LeftDescriptor descriptor;
        descriptor.id = left_count_++;
        descriptor.signature = signature;
        profile.left.push_back(std::move(descriptor));
      }
      for (std::size_t selection = 0; selection < selection_count_;
           ++selection) {
        const int local = local_left[values[selection]];
        if (local >= 0) {
          profile.left[static_cast<std::size_t>(local)]
              .representations.push_back(
                  static_cast<Selection>(selection));
        }
      }

      for (std::size_t trace = 0; trace < signature_count_; ++trace) {
        if (pi_a[trace] == 0 && pi_h[trace] == 0) {
          continue;
        }
        const Signature lifted =
            static_cast<Signature>(trace | profile.u);
        const bool in_k = h_family[lifted] != 0;
        RightTrace right;
        right.trace = static_cast<Signature>(trace);
        if (pi_h[trace] != 0 && !in_k) {
          right.type0 = right_count_++;
          ++profile.boundary0;
        }
        if ((pi_a[trace] != 0 || pi_h[trace] != 0) && !in_k) {
          right.type1 = right_count_++;
          ++profile.boundary1;
        }
        if (right.type0 != kNoVertex || right.type1 != kNoVertex) {
          if (right.type0 == kNoVertex ||
              right.type1 == kNoVertex) {
            throw std::logic_error(
                "B0=B1 trace identity failed at P=" +
                decode_parameter(m_, parameter));
          }
          profile.right.push_back(right);
        }
      }
      if (profile.boundary0 != profile.boundary1) {
        throw std::logic_error("B0=B1 count identity failed");
      }

      // Independent direct checks against the original join-U boundary
      // formulas.  These are intentionally separate from the trace formulas
      // used to instantiate right vertices.
      std::vector<std::uint8_t> safe_join(signature_count_, 0);
      std::vector<std::uint8_t> h_join(signature_count_, 0);
      std::uint32_t direct_safe_images = 0;
      std::uint32_t direct_boundary0 = 0;
      std::uint32_t direct_boundary1 = 0;
      for (const Signature signature : family_list) {
        if ((signature & bottom) == 0) {
          const Signature joined =
              static_cast<Signature>(signature | profile.u);
          if (safe_join[joined] == 0) {
            safe_join[joined] = 1;
            ++direct_safe_images;
          }
        } else {
          const Signature h =
              static_cast<Signature>(signature & without_bottom);
          h_join[static_cast<Signature>(h | profile.u)] = 1;
        }
      }
      for (std::size_t signature = 0; signature < signature_count_;
           ++signature) {
        if (h_join[signature] != 0 && h_family[signature] == 0) {
          ++direct_boundary0;
        }
        if ((safe_join[signature] != 0 || h_join[signature] != 0) &&
            h_family[signature] == 0) {
          ++direct_boundary1;
        }
      }
      if (direct_safe_images != profile.safe_images ||
          direct_boundary0 != profile.boundary0 ||
          direct_boundary1 != profile.boundary1 ||
          profile.left.size() !=
              profile.safe_size - profile.safe_images) {
        throw std::logic_error("decomposition identity failed at P=" +
                               decode_parameter(m_, parameter));
      }

      if (!options_.quiet_progress && m_ >= 6 &&
          (parameter_index + 1) % 1024 == 0) {
        std::cerr << "profiles " << (parameter_index + 1) << '/'
                  << profile_count_ << '\n';
      }
    }
  }

  void validate_profile_totals() const {
    static const std::map<int, std::uint64_t> known_deficits = {
        {3, 7}, {4, 129}, {5, 1298}, {6, 11155}, {7, 101623}};
    const auto found = known_deficits.find(m_);
    if (found != known_deficits.end() && left_count_ != found->second) {
      throw std::logic_error(
          "left deficit total disagrees with the independent baseline");
    }
    if (m_ == 6 || m_ == 7) {
      const std::uint64_t expected_safe = m_ == 6 ? 35594 : 254496;
      const std::uint64_t expected_images = m_ == 6 ? 24439 : 152873;
      std::uint64_t safe = 0;
      std::uint64_t images = 0;
      for (const Profile& profile : profiles_) {
        safe += profile.safe_size;
        images += profile.safe_images;
      }
      if (safe != expected_safe || images != expected_images) {
        throw std::logic_error(
            "safe/image totals disagree with independent baseline");
      }
    }
  }

  void print_enumeration_summary(
      const std::chrono::steady_clock::time_point start) const {
    std::uint64_t family = 0;
    std::uint64_t safe = 0;
    std::uint64_t images = 0;
    std::uint64_t boundary0 = 0;
    std::uint64_t boundary1 = 0;
    std::uint64_t representation_mass = 0;
    std::size_t max_representations = 0;
    for (const Profile& profile : profiles_) {
      family += profile.family_size;
      safe += profile.safe_size;
      images += profile.safe_images;
      boundary0 += profile.boundary0;
      boundary1 += profile.boundary1;
      for (const LeftDescriptor& left : profile.left) {
        representation_mass += left.representations.size();
        max_representations =
            std::max(max_representations, left.representations.size());
      }
    }
    const double seconds =
        std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                     start)
            .count();
    std::cout << "enumeration m=" << m_
              << " profiles=" << profile_count_
              << " row_selections=" << selection_count_
              << " family_distinct_total=" << family
              << " safe=" << safe
              << " pi_safe=" << images
              << " left=" << left_count_
              << " right0=" << boundary0
              << " right1=" << boundary1
              << " right_total=" << right_count_
              << " left_representation_mass=" << representation_mass
              << " max_representations_per_left=" << max_representations
              << " seconds=" << std::fixed << std::setprecision(3)
              << seconds << '\n';
  }

  std::vector<ReachChoice> build_reach(
      const LeftDescriptor& left,
      const ReachRule rule,
      std::vector<std::uint32_t>& stamps,
      std::vector<Selection>& best_representative,
      std::uint32_t& stamp) const {
    ++stamp;
    if (stamp == 0) {
      std::fill(stamps.begin(), stamps.end(), 0);
      ++stamp;
    }
    std::vector<ReachChoice> result;
    result.reserve(std::min<std::size_t>(
        selection_count_,
        left.representations.size() *
            static_cast<std::size_t>(1 + row_count_ +
                                     row_count_ * (row_count_ - 1) / 2)));

    const auto add = [&](const Selection target,
                         const Selection representative) {
      const std::size_t index = static_cast<std::size_t>(target);
      if (stamps[index] == stamp) {
        const Selection old = best_representative[index];
        if (pack_certificate(0, representative, target) <
            pack_certificate(0, old, target)) {
          best_representative[index] = representative;
        }
        return;
      }
      stamps[index] = stamp;
      best_representative[index] = representative;
      result.push_back(ReachChoice{target, representative});
    };

    for (const Selection representation : left.representations) {
      add(representation, representation);
      if (rule == ReachRule::kSameRepresentative) {
        continue;
      }
      for (int first = 0; first < row_count_; ++first) {
        add(static_cast<Selection>(representation ^
                                   (Selection{1} << first)),
            representation);
      }
      if (rule == ReachRule::kHammingRadiusOne) {
        continue;
      }
      for (int first = 0; first < row_count_; ++first) {
        const bool first_selected =
            (representation & (Selection{1} << first)) != 0;
        for (int second = first + 1; second < row_count_; ++second) {
          const bool second_selected =
              (representation & (Selection{1} << second)) != 0;
          if (rule == ReachRule::kOneLocalEdit &&
              first_selected == second_selected) {
            continue;
          }
          add(static_cast<Selection>(
                  representation ^ (Selection{1} << first) ^
                  (Selection{1} << second)),
              representation);
        }
      }
      if (result.size() == selection_count_) {
        break;
      }
    }
    for (ReachChoice& choice : result) {
      choice.representative =
          best_representative[static_cast<std::size_t>(choice.target)];
    }
    std::sort(result.begin(), result.end(),
              [](const ReachChoice& left_choice,
                 const ReachChoice& right_choice) {
                return left_choice.target < right_choice.target;
              });
    return result;
  }

  int deleted_parameter(const Parameter parent,
                        const Parameter child) const {
    if (parent == child) {
      return 0;
    }
    const Parameter difference =
        static_cast<Parameter>(parent & ~child);
    if (__builtin_popcount(static_cast<unsigned>(difference)) != 1) {
      throw std::logic_error("parameter edge is not one deletion");
    }
    // Optional bit 0 represents parameter p=2.
    return __builtin_ctz(static_cast<unsigned>(difference)) + 2;
  }

  std::uint64_t build_regression_graph(
      const ReachRule rule,
      const int parameter_radius,
      std::vector<std::vector<Edge>>& adjacency) const {
    adjacency.assign(static_cast<std::size_t>(left_count_), {});
    std::vector<Vertex> right0(signature_count_, kNoVertex);
    std::vector<Vertex> right1(signature_count_, kNoVertex);
    std::vector<std::uint32_t> reach_stamps(selection_count_, 0);
    std::vector<Selection> best_representative(selection_count_, 0);
    std::uint32_t reach_stamp = 0;
    std::vector<std::uint32_t> right_seen(
        static_cast<std::size_t>(right_count_), 0);
    const Signature bottom = value_bit(m_, -m_);
    const Signature without_bottom =
        static_cast<Signature>(
            static_cast<Signature>(signature_count_ - 1) ^ bottom);

    for (std::size_t parent_index = 0; parent_index < profile_count_;
         ++parent_index) {
      const Parameter parent = static_cast<Parameter>(parent_index);
      const Profile& parent_profile = profiles_[parent_index];
      std::vector<std::vector<ReachChoice>> reaches;
      reaches.reserve(parent_profile.left.size());
      for (const LeftDescriptor& left : parent_profile.left) {
        reaches.push_back(build_reach(
            left, rule, reach_stamps, best_representative, reach_stamp));
      }

      std::vector<Parameter> children;
      Parameter deletion = parent;
      while (true) {
        if (__builtin_popcount(static_cast<unsigned>(deletion)) <=
            parameter_radius) {
          children.push_back(
              static_cast<Parameter>(parent & ~deletion));
        }
        if (deletion == 0) {
          break;
        }
        deletion =
            static_cast<Parameter>((deletion - 1) & parent);
      }

      std::vector<std::vector<Vertex>> collected(
          parent_profile.left.size());
      for (const Parameter child : children) {
        const Profile& child_profile =
            profiles_[static_cast<std::size_t>(child)];
        for (const RightTrace& right : child_profile.right) {
          right0[right.trace] = right.type0;
          right1[right.trace] = right.type1;
        }
        const Signature* child_signatures = signature_row(child);
        const Signature outside_u = static_cast<Signature>(
            static_cast<Signature>(signature_count_ - 1) ^
            child_profile.u);
        for (std::size_t local = 0; local < parent_profile.left.size();
             ++local) {
          const Vertex left_id = parent_profile.left[local].id;
          const std::uint32_t left_stamp = left_id + 1;
          const auto add_right = [&](const Vertex right) {
            if (right == kNoVertex ||
                right_seen[static_cast<std::size_t>(right)] ==
                    left_stamp) {
              return;
            }
            right_seen[static_cast<std::size_t>(right)] = left_stamp;
            collected[local].push_back(right);
          };
          for (const ReachChoice& choice : reaches[local]) {
            const Signature signature =
                child_signatures[choice.target];
            const Signature trace = static_cast<Signature>(
                (signature & without_bottom) & outside_u);
            if ((signature & bottom) == 0) {
              add_right(right1[trace]);
            } else {
              add_right(right0[trace]);
              add_right(right1[trace]);
            }
          }
        }
        for (const RightTrace& right : child_profile.right) {
          right0[right.trace] = kNoVertex;
          right1[right.trace] = kNoVertex;
        }
      }
      for (std::size_t local = 0; local < parent_profile.left.size();
           ++local) {
        std::vector<Vertex>& rights = collected[local];
        std::sort(rights.begin(), rights.end());
        std::vector<Edge>& edges =
            adjacency[parent_profile.left[local].id];
        edges.reserve(rights.size());
        for (const Vertex right : rights) {
          // Regression matching needs cardinality only; certificate zero is
          // not presented as a discovery-edge witness.
          edges.push_back(Edge{right, 0});
        }
      }
    }
    return std::accumulate(
        adjacency.begin(), adjacency.end(), std::uint64_t{0},
        [](const std::uint64_t total, const std::vector<Edge>& edges) {
          return total + edges.size();
        });
  }

  void run_regression_case(const std::string& label,
                           const ReachRule rule,
                           const int parameter_radius,
                           const std::uint64_t expected_matching,
                           const std::uint64_t expected_edges = 0) const {
    std::vector<std::vector<Edge>> adjacency;
    const std::uint64_t edges =
        build_regression_graph(rule, parameter_radius, adjacency);
    std::vector<Vertex> pair_left;
    std::vector<Vertex> pair_right;
    std::vector<Certificate> matched_certificate;
    const MatchStats stats =
        maximum_matching(adjacency, pair_left, pair_right,
                         matched_certificate);
    if (stats.matching != expected_matching ||
        (expected_edges != 0 && edges != expected_edges)) {
      throw std::logic_error("small-m regression failed: " + label);
    }
    std::cout << "regression m=" << m_
              << " label=" << label
              << " parameter_radius=" << parameter_radius
              << " edges=" << edges
              << " matching=" << stats.matching
              << " left=" << left_count_
              << " expected_matching=" << expected_matching;
    if (expected_edges != 0) {
      std::cout << " expected_edges=" << expected_edges;
    }
    std::cout << " validated=yes\n";
  }

  void run_small_regressions() const {
    if (m_ == 3) {
      run_regression_case("same_rows", ReachRule::kSameRepresentative,
                          0, 0);
      run_regression_case("hamming_le_1",
                          ReachRule::kHammingRadiusOne, 0, 4);
      run_regression_case("same_rows", ReachRule::kSameRepresentative,
                          1, 2);
      run_regression_case("hamming_le_1",
                          ReachRule::kHammingRadiusOne, 1, 7);
    } else if (m_ == 4) {
      run_regression_case("same_rows", ReachRule::kSameRepresentative,
                          1, 50);
      run_regression_case("hamming_le_1",
                          ReachRule::kHammingRadiusOne, 1, 114);
      run_regression_case("hamming_le_1",
                          ReachRule::kHammingRadiusOne, 2, 114);
      run_regression_case("hamming_le_2",
                          ReachRule::kHammingRadiusTwo, 1, 129);
    } else if (m_ == 5) {
      run_regression_case("hamming_le_2",
                          ReachRule::kHammingRadiusTwo, 1, 1298, 56669);
    }
  }

  GraphStats build_graph(const Stage stage,
                         std::vector<std::vector<Edge>>& adjacency) const {
    const auto start = std::chrono::steady_clock::now();
    adjacency.assign(static_cast<std::size_t>(left_count_), {});
    std::vector<Vertex> right0(signature_count_, kNoVertex);
    std::vector<Vertex> right1(signature_count_, kNoVertex);
    std::vector<std::uint32_t> reach_stamps(selection_count_, 0);
    std::vector<Selection> best_representative(selection_count_, 0);
    std::uint32_t reach_stamp = 0;
    std::vector<std::uint32_t> right_seen(
        static_cast<std::size_t>(right_count_), 0);
    std::vector<Certificate> best_certificate(
        static_cast<std::size_t>(right_count_), 0);
    const Signature bottom = value_bit(m_, -m_);
    const Signature without_bottom =
        static_cast<Signature>(
            static_cast<Signature>(signature_count_ - 1) ^ bottom);

    std::uint64_t reach_total = 0;
    std::size_t max_reach = 0;

    for (std::size_t parent_index = 0; parent_index < profile_count_;
         ++parent_index) {
      const Parameter parent = static_cast<Parameter>(parent_index);
      const Profile& parent_profile = profiles_[parent_index];
      std::vector<std::vector<ReachChoice>> reaches;
      reaches.reserve(parent_profile.left.size());
      const ReachRule reach_rule =
          stage == Stage::kOneLocalEdit
              ? ReachRule::kOneLocalEdit
              : ReachRule::kHammingRadiusTwo;
      for (const LeftDescriptor& left : parent_profile.left) {
        reaches.push_back(build_reach(left, reach_rule, reach_stamps,
                                      best_representative, reach_stamp));
        reach_total += reaches.back().size();
        max_reach = std::max(max_reach, reaches.back().size());
      }

      std::vector<Parameter> children;
      children.push_back(parent);
      Parameter remaining = parent;
      while (remaining != 0) {
        const int optional_bit =
            __builtin_ctz(static_cast<unsigned>(remaining));
        children.push_back(static_cast<Parameter>(
            parent & ~(Parameter{1} << optional_bit)));
        remaining =
            static_cast<Parameter>(remaining & (remaining - 1));
      }

      // Finish one left vertex before moving to the next.  best_certificate
      // is indexed only by right ID, so interleaving different left stamps
      // would overwrite another left's canonical witness before emission.
      for (std::size_t local = 0; local < parent_profile.left.size();
           ++local) {
        const LeftDescriptor& left = parent_profile.left[local];
        const std::uint32_t left_stamp = left.id + 1;
        std::vector<Vertex> rights;
        for (const Parameter child : children) {
          const Profile& child_profile =
              profiles_[static_cast<std::size_t>(child)];
          for (const RightTrace& right : child_profile.right) {
            right0[right.trace] = right.type0;
            right1[right.trace] = right.type1;
          }
          const Signature* child_signatures = signature_row(child);
          const Signature outside_u = static_cast<Signature>(
              static_cast<Signature>(signature_count_ - 1) ^
              child_profile.u);
          const int deleted = deleted_parameter(parent, child);
          for (const ReachChoice& choice : reaches[local]) {
            const Signature signature =
                child_signatures[choice.target];
            const Signature trace = static_cast<Signature>(
                (signature & without_bottom) & outside_u);
            const Certificate certificate = pack_certificate(
                deleted, choice.representative, choice.target);

            const auto add_right = [&](const Vertex right) {
              if (right == kNoVertex) {
                return;
              }
              const std::size_t index = static_cast<std::size_t>(right);
              if (right_seen[index] != left_stamp) {
                right_seen[index] = left_stamp;
                best_certificate[index] = certificate;
                rights.push_back(right);
              } else if (certificate < best_certificate[index]) {
                best_certificate[index] = certificate;
              }
            };

            if ((signature & bottom) == 0) {
              add_right(right1[trace]);
            } else {
              add_right(right0[trace]);
              add_right(right1[trace]);
            }
          }
          for (const RightTrace& right : child_profile.right) {
            right0[right.trace] = kNoVertex;
            right1[right.trace] = kNoVertex;
          }
        }
        std::sort(rights.begin(), rights.end(),
                  [&](const Vertex first, const Vertex second) {
                    const Certificate first_certificate =
                        best_certificate[first];
                    const Certificate second_certificate =
                        best_certificate[second];
                    if (first_certificate != second_certificate) {
                      return first_certificate < second_certificate;
                    }
                    return first < second;
                  });
        std::vector<Edge>& edges =
            adjacency[static_cast<std::size_t>(left.id)];
        edges.reserve(rights.size());
        for (const Vertex right : rights) {
          edges.push_back(Edge{right, best_certificate[right]});
        }
      }

      if (!options_.quiet_progress && m_ >= 6 &&
          (parent_index + 1) % 512 == 0) {
        std::cerr << "graph " << stage_name(stage) << ' '
                  << (parent_index + 1) << '/' << profile_count_ << '\n';
      }
    }

    GraphStats stats;
    stats.min_degree = adjacency.empty()
                           ? 0
                           : std::numeric_limits<std::size_t>::max();
    long double degree_sum = 0.0L;
    for (const std::vector<Edge>& edges : adjacency) {
      stats.edges += edges.size();
      degree_sum += static_cast<long double>(edges.size());
      stats.min_degree = std::min(stats.min_degree, edges.size());
      stats.max_degree = std::max(stats.max_degree, edges.size());
      if (edges.empty()) {
        ++stats.isolated_left;
      }
      for (const Edge& edge : edges) {
        ++stats.edge_templates[coarse_certificate(edge.certificate)];
      }
    }
    stats.mean_degree =
        adjacency.empty() ? 0.0L
                          : degree_sum /
                                static_cast<long double>(adjacency.size());
    const double seconds =
        std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                     start)
            .count();
    std::cout << "graph stage=" << stage_name(stage)
              << " left=" << left_count_
              << " right=" << right_count_
              << " edges=" << stats.edges
              << " isolated_left=" << stats.isolated_left
              << " min_degree=" << stats.min_degree
              << " max_degree=" << stats.max_degree
              << " mean_degree=" << std::fixed << std::setprecision(6)
              << static_cast<double>(stats.mean_degree)
              << " reachable_selection_total=" << reach_total
              << " max_reachable_per_left=" << max_reach
              << " seconds=" << std::setprecision(3) << seconds << '\n';
    print_string_histogram("edge_certificate_templates",
                           stats.edge_templates, 20);
    return stats;
  }

  static void print_integer_histogram(
      const std::string& label,
      const std::map<int, std::uint64_t>& histogram) {
    std::cout << label;
    for (const auto& [key, count] : histogram) {
      std::cout << ' ' << key << ':' << count;
    }
    std::cout << '\n';
  }

  static void print_string_histogram(
      const std::string& label,
      const std::map<std::string, std::uint64_t>& histogram,
      const std::size_t limit) {
    std::vector<std::pair<std::string, std::uint64_t>> entries(
        histogram.begin(), histogram.end());
    std::sort(entries.begin(), entries.end(),
              [](const auto& left, const auto& right) {
                if (left.second != right.second) {
                  return left.second > right.second;
                }
                return left.first < right.first;
              });
    std::cout << label << " distinct=" << entries.size();
    const std::size_t shown = std::min(limit, entries.size());
    for (std::size_t index = 0; index < shown; ++index) {
      std::cout << " [" << entries[index].first << "]="
                << entries[index].second;
    }
    std::cout << '\n';
  }

  std::string alternating_path_template(
      const std::vector<AlternatingSegment>& path) const {
    std::ostringstream output;
    const std::size_t show = 6;
    const auto append = [&](const AlternatingSegment& segment,
                            const bool prepend_separator) {
      if (prepend_separator) {
        output << '>';
      }
      output << (segment.forward_is_new ? "+F" : "F")
             << coarse_certificate(segment.forward);
      if (segment.has_backward) {
        output << (segment.backward_is_new ? "<+B" : "<B")
               << coarse_certificate(segment.backward);
      }
    };
    if (path.size() <= 2 * show) {
      for (std::size_t index = 0; index < path.size(); ++index) {
        append(path[index], index != 0);
      }
    } else {
      for (std::size_t index = 0; index < show; ++index) {
        append(path[index], index != 0);
      }
      output << ">...depth" << path.size() << "...";
      for (std::size_t index = path.size() - show; index < path.size();
           ++index) {
        append(path[index], true);
      }
    }
    return output.str();
  }

  void record_path(const std::vector<AlternatingSegment>& path,
                   MatchStats& stats) const {
    const int depth = static_cast<int>(path.size());
    ++stats.depth_histogram[depth];
    stats.max_depth = std::max(stats.max_depth, depth);
    ++stats.path_templates[alternating_path_template(path)];
    bool uses_new = false;
    for (std::size_t index = 0; index < path.size(); ++index) {
      ++stats.forward_templates[
          coarse_certificate(path[index].forward)];
      if (path[index].forward_is_new) {
        uses_new = true;
        ++stats.new_forward_edges;
        ++stats.new_forward_templates[
            coarse_certificate(path[index].forward)];
      }
      if (path[index].backward_is_new) {
        uses_new = true;
        ++stats.new_backward_edges;
        ++stats.new_backward_templates[
            coarse_certificate(path[index].backward)];
      }
      if (path[index].has_backward && index + 1 < path.size()) {
        const std::string transition =
            coarse_certificate(path[index].backward) + " -> " +
            coarse_certificate(path[index + 1].forward);
        ++stats.alternating_transitions[transition];
      }
    }
    if (uses_new) {
      ++stats.paths_using_new_edges;
    }
  }

  bool bfs_layers(const std::vector<std::vector<Edge>>& adjacency,
                  const std::vector<Vertex>& pair_left,
                  const std::vector<Vertex>& pair_right,
                  std::vector<int>& distance,
                  int& terminal_distance) const {
    std::queue<Vertex> queue;
    terminal_distance = kInfinity;
    for (Vertex left = 0; left < left_count_; ++left) {
      if (pair_left[left] == kNoVertex) {
        distance[left] = 0;
        queue.push(left);
      } else {
        distance[left] = kInfinity;
      }
    }
    while (!queue.empty()) {
      const Vertex left = queue.front();
      queue.pop();
      if (distance[left] >= terminal_distance) {
        continue;
      }
      for (const Edge& edge : adjacency[left]) {
        const Vertex next_left = pair_right[edge.right];
        if (next_left == kNoVertex) {
          terminal_distance = distance[left] + 1;
        } else if (distance[next_left] == kInfinity) {
          distance[next_left] = distance[left] + 1;
          queue.push(next_left);
        }
      }
    }
    return terminal_distance != kInfinity;
  }

  bool dfs_augment(const Vertex left,
                   const int terminal_distance,
                   const std::vector<std::vector<Edge>>& adjacency,
                   const std::vector<std::vector<Vertex>>* old_rights,
                   std::vector<Vertex>& pair_left,
                   std::vector<Vertex>& pair_right,
                   std::vector<Certificate>& matched_certificate,
                   std::vector<int>& distance,
                   std::vector<std::size_t>& next_edge,
                   std::vector<AlternatingSegment>& path) const {
    const auto is_new_edge = [&](const Vertex edge_left,
                                 const Vertex edge_right) {
      if (old_rights == nullptr) {
        return false;
      }
      const std::vector<Vertex>& old =
          (*old_rights)[static_cast<std::size_t>(edge_left)];
      return !std::binary_search(old.begin(), old.end(), edge_right);
    };
    for (std::size_t& edge_index = next_edge[left];
         edge_index < adjacency[left].size(); ++edge_index) {
      const Edge edge = adjacency[left][edge_index];
      const Vertex next_left = pair_right[edge.right];
      if (next_left == kNoVertex) {
        if (distance[left] + 1 != terminal_distance) {
          continue;
        }
        path.push_back(
            AlternatingSegment{edge.certificate, 0, false,
                               is_new_edge(left, edge.right), false});
        pair_left[left] = edge.right;
        pair_right[edge.right] = left;
        matched_certificate[left] = edge.certificate;
        return true;
      }
      if (distance[next_left] != distance[left] + 1) {
        continue;
      }
      const Certificate backward = matched_certificate[next_left];
      path.push_back(
          AlternatingSegment{edge.certificate, backward, true,
                             is_new_edge(left, edge.right),
                             is_new_edge(next_left, edge.right)});
      if (dfs_augment(next_left, terminal_distance, adjacency, old_rights,
                      pair_left, pair_right, matched_certificate, distance,
                      next_edge, path)) {
        pair_left[left] = edge.right;
        pair_right[edge.right] = left;
        matched_certificate[left] = edge.certificate;
        return true;
      }
      path.pop_back();
    }
    distance[left] = kInfinity;
    return false;
  }

  MatchStats augment_matching(
      const std::vector<std::vector<Edge>>& adjacency,
      std::vector<Vertex>& pair_left,
      std::vector<Vertex>& pair_right,
      std::vector<Certificate>& matched_certificate,
      const std::vector<std::vector<Vertex>>* old_rights = nullptr) const {
    if (pair_left.size() != left_count_ ||
        pair_right.size() != right_count_ ||
        matched_certificate.size() != left_count_) {
      throw std::logic_error("initial matching arrays have wrong sizes");
    }
    std::vector<int> distance(static_cast<std::size_t>(left_count_),
                              kInfinity);
    std::vector<std::size_t> next_edge(
        static_cast<std::size_t>(left_count_), 0);
    MatchStats stats;
    stats.matching = static_cast<std::uint64_t>(
        std::count_if(pair_left.begin(), pair_left.end(),
                      [](const Vertex right) {
                        return right != kNoVertex;
                      }));
    int terminal_distance = kInfinity;
    while (bfs_layers(adjacency, pair_left, pair_right, distance,
                      terminal_distance)) {
      ++stats.phases;
      std::fill(next_edge.begin(), next_edge.end(), 0);
      std::uint64_t phase_count = 0;
      for (Vertex left = 0; left < left_count_; ++left) {
        if (pair_left[left] != kNoVertex || distance[left] != 0) {
          continue;
        }
        std::vector<AlternatingSegment> path;
        path.reserve(static_cast<std::size_t>(terminal_distance));
        if (dfs_augment(left, terminal_distance, adjacency, old_rights,
                        pair_left, pair_right, matched_certificate, distance,
                        next_edge, path)) {
          ++stats.matching;
          ++stats.augmentations;
          ++phase_count;
          record_path(path, stats);
        }
      }
      stats.phase_augmentations[terminal_distance] += phase_count;
    }
    return stats;
  }

  MatchStats maximum_matching(
      const std::vector<std::vector<Edge>>& adjacency,
      std::vector<Vertex>& pair_left,
      std::vector<Vertex>& pair_right,
      std::vector<Certificate>& matched_certificate) const {
    pair_left.assign(static_cast<std::size_t>(left_count_), kNoVertex);
    pair_right.assign(static_cast<std::size_t>(right_count_), kNoVertex);
    matched_certificate.assign(static_cast<std::size_t>(left_count_), 0);
    return augment_matching(adjacency, pair_left, pair_right,
                            matched_certificate);
  }

  HallWitness hall_witness(
      const std::vector<std::vector<Edge>>& adjacency,
      const std::vector<Vertex>& pair_left,
      const std::vector<Vertex>& pair_right) const {
    std::vector<std::uint8_t> reached_left(
        static_cast<std::size_t>(left_count_), 0);
    std::vector<std::uint8_t> reached_right(
        static_cast<std::size_t>(right_count_), 0);
    std::queue<Vertex> queue;
    HallWitness witness;
    for (Vertex left = 0; left < left_count_; ++left) {
      if (pair_left[left] == kNoVertex) {
        reached_left[left] = 1;
        queue.push(left);
        if (witness.unmatched_left.size() < 12) {
          witness.unmatched_left.push_back(left);
        }
      }
    }
    while (!queue.empty()) {
      const Vertex left = queue.front();
      queue.pop();
      for (const Edge& edge : adjacency[left]) {
        // Residual L->R arcs are precisely unmatched graph edges.
        if (pair_left[left] == edge.right ||
            reached_right[edge.right] != 0) {
          continue;
        }
        reached_right[edge.right] = 1;
        const Vertex next_left = pair_right[edge.right];
        if (next_left != kNoVertex && reached_left[next_left] == 0) {
          reached_left[next_left] = 1;
          queue.push(next_left);
        }
      }
    }
    witness.left_size =
        std::accumulate(reached_left.begin(), reached_left.end(),
                        std::uint64_t{0});
    witness.neighbor_size =
        std::accumulate(reached_right.begin(), reached_right.end(),
                        std::uint64_t{0});
    witness.excess = witness.left_size - witness.neighbor_size;

    std::vector<std::uint8_t> profile_touched(profile_count_, 0);
    for (std::size_t parameter = 0; parameter < profile_count_;
         ++parameter) {
      for (const LeftDescriptor& left : profiles_[parameter].left) {
        if (reached_left[left.id] != 0) {
          profile_touched[parameter] = 1;
          break;
        }
      }
    }
    witness.profiles_touched =
        std::accumulate(profile_touched.begin(), profile_touched.end(),
                        std::uint64_t{0});
    return witness;
  }

  void verify_graph_certificates(
      const Stage stage,
      const std::vector<std::vector<Edge>>& adjacency) const {
    std::vector<Parameter> right_parameter(
        static_cast<std::size_t>(right_count_), 0);
    std::vector<Signature> right_trace(
        static_cast<std::size_t>(right_count_), 0);
    std::vector<std::uint8_t> right_type(
        static_cast<std::size_t>(right_count_), 0xff);
    for (std::size_t parameter = 0; parameter < profile_count_;
         ++parameter) {
      for (const RightTrace& right : profiles_[parameter].right) {
        if (right.type0 != kNoVertex) {
          right_parameter[right.type0] =
              static_cast<Parameter>(parameter);
          right_trace[right.type0] = right.trace;
          right_type[right.type0] = 0;
        }
        if (right.type1 != kNoVertex) {
          right_parameter[right.type1] =
              static_cast<Parameter>(parameter);
          right_trace[right.type1] = right.trace;
          right_type[right.type1] = 1;
        }
      }
    }

    const Signature bottom = value_bit(m_, -m_);
    const Signature without_bottom =
        static_cast<Signature>(
            static_cast<Signature>(signature_count_ - 1) ^ bottom);
    std::uint64_t checked = 0;
    for (std::size_t parameter = 0; parameter < profile_count_;
         ++parameter) {
      const Parameter parent = static_cast<Parameter>(parameter);
      for (const LeftDescriptor& left : profiles_[parameter].left) {
        if (adjacency[left.id].empty()) {
          continue;
        }
        for (const Edge& edge : adjacency[left.id]) {
          if (edge.right >= right_count_ ||
              right_type[edge.right] == 0xff) {
            throw std::logic_error(
                "edge points to a nonexistent typed right");
          }
          const Certificate certificate = edge.certificate;
          const Selection from = certificate_from(certificate);
          const Selection to = certificate_to(certificate);
          if (from >= selection_count_ || to >= selection_count_ ||
              signature_row(parent)[from] != left.signature) {
            throw std::logic_error(
                "edge certificate has an invalid left representation");
          }
          const int deleted =
              certificate_deleted_parameter(certificate);
          Parameter child = parent;
          if (deleted != 0) {
            if (deleted < 2 || deleted > 2 * m_) {
              throw std::logic_error(
                  "edge certificate deletes an invalid parameter");
            }
            const Parameter optional_bit =
                static_cast<Parameter>(Parameter{1} << (deleted - 2));
            if ((parent & optional_bit) == 0) {
              throw std::logic_error(
                  "edge certificate deletes a parameter absent from P");
            }
            child = static_cast<Parameter>(parent & ~optional_bit);
          }
          if (right_parameter[edge.right] != child) {
            throw std::logic_error(
                "edge certificate child does not equal right profile");
          }
          const int removed = __builtin_popcount(
              static_cast<unsigned>(from & ~to));
          const int added = __builtin_popcount(
              static_cast<unsigned>(to & ~from));
          if ((stage == Stage::kOneLocalEdit &&
               (removed > 1 || added > 1)) ||
              (stage == Stage::kHammingRadiusTwo &&
               __builtin_popcount(
                   static_cast<unsigned>(from ^ to)) > 2)) {
            throw std::logic_error(
                "edge certificate violates the stage row rule");
          }
          if (classify_move(from, to) !=
              certificate_move(certificate)) {
            throw std::logic_error(
                "edge certificate move label is inconsistent");
          }
          const Signature target_signature = signature_row(child)[to];
          const Signature outside_u = static_cast<Signature>(
              static_cast<Signature>(signature_count_ - 1) ^
              profiles_[static_cast<std::size_t>(child)].u);
          const Signature trace = static_cast<Signature>(
              (target_signature & without_bottom) & outside_u);
          if (trace != right_trace[edge.right]) {
            throw std::logic_error(
                "edge certificate yields the wrong right trace");
          }
          if ((target_signature & bottom) == 0 &&
              right_type[edge.right] != 1) {
            throw std::logic_error(
                "a safe target was connected to right type 0");
          }
          ++checked;
        }
      }
    }
    const std::uint64_t expected = std::accumulate(
        adjacency.begin(), adjacency.end(), std::uint64_t{0},
        [](const std::uint64_t total, const std::vector<Edge>& edges) {
          return total + edges.size();
        });
    if (checked != expected) {
      throw std::logic_error("not every graph edge was audited");
    }
    std::cout << "certificate_audit stage=" << stage_name(stage)
              << " checked_edges=" << checked
              << " result=valid\n";
  }

  void verify_matching(
      const Stage stage,
      const std::vector<std::vector<Edge>>& adjacency,
      const std::vector<Vertex>& pair_left,
      const std::vector<Vertex>& pair_right,
      const std::vector<Certificate>& matched_certificate,
      const std::uint64_t matching) const {
    std::uint64_t counted = 0;
    for (Vertex left = 0; left < left_count_; ++left) {
      const Vertex right = pair_left[left];
      if (right == kNoVertex) {
        continue;
      }
      ++counted;
      if (right >= right_count_ || pair_right[right] != left) {
        throw std::logic_error("matching inverse is inconsistent");
      }
      const auto found =
          std::find_if(adjacency[left].begin(), adjacency[left].end(),
                       [&](const Edge& edge) {
                         return edge.right == right &&
                                edge.certificate ==
                                    matched_certificate[left];
                       });
      if (found == adjacency[left].end()) {
        throw std::logic_error("matched edge has no exact certificate");
      }
      const Selection from =
          certificate_from(matched_certificate[left]);
      const Selection to = certificate_to(matched_certificate[left]);
      const int removed = __builtin_popcount(
          static_cast<unsigned>(from & ~to));
      const int added = __builtin_popcount(
          static_cast<unsigned>(to & ~from));
      if (stage == Stage::kOneLocalEdit) {
        if (removed > 1 || added > 1) {
          throw std::logic_error("stage A matching used a forbidden edit");
        }
      } else if (__builtin_popcount(
                     static_cast<unsigned>(from ^ to)) > 2) {
        throw std::logic_error("stage B matching used a forbidden edit");
      }
    }
    if (counted != matching) {
      throw std::logic_error("matching cardinality check failed");
    }
  }

  void print_matching_templates(
      const std::vector<Vertex>& pair_left,
      const std::vector<Certificate>& matched_certificate) const {
    std::map<std::string, std::uint64_t> templates;
    std::map<int, std::uint64_t> deleted_coordinates;
    for (Vertex left = 0; left < left_count_; ++left) {
      if (pair_left[left] == kNoVertex) {
        continue;
      }
      const Certificate certificate = matched_certificate[left];
      ++templates[coarse_certificate(certificate)];
      ++deleted_coordinates[
          certificate_deleted_parameter(certificate)];
    }
    print_string_histogram("final_matching_templates", templates, 20);
    print_integer_histogram("final_matching_deleted_parameter",
                            deleted_coordinates);
  }

  bool run_stage(const Stage stage) const {
    std::cout << "stage_begin m=" << m_
              << " stage=" << stage_name(stage) << '\n';
    std::vector<std::vector<Edge>> adjacency;
    const GraphStats graph = build_graph(stage, adjacency);
    verify_graph_certificates(stage, adjacency);

    // The previous independent prototype's stage-B edge count is a useful
    // regression test of all typed-edge and representation semantics.
    if (stage == Stage::kHammingRadiusTwo && m_ == 5 &&
        graph.edges != 56669) {
      throw std::logic_error(
          "m=5 stage-B edge count disagrees with independent prototype");
    }

    const auto match_start = std::chrono::steady_clock::now();
    std::vector<Vertex> pair_left;
    std::vector<Vertex> pair_right;
    std::vector<Certificate> matched_certificate;
    const MatchStats stats =
        maximum_matching(adjacency, pair_left, pair_right,
                         matched_certificate);
    verify_matching(stage, adjacency, pair_left, pair_right,
                    matched_certificate, stats.matching);
    const double match_seconds =
        std::chrono::duration<double>(
            std::chrono::steady_clock::now() - match_start)
            .count();
    const std::uint64_t shortfall = left_count_ - stats.matching;
    std::cout << "matching m=" << m_
              << " stage=" << stage_name(stage)
              << " cardinality=" << stats.matching
              << " left=" << left_count_
              << " shortfall=" << shortfall
              << " phases=" << stats.phases
              << " max_augmenting_depth=" << stats.max_depth
              << " max_augmenting_edge_length="
              << (stats.max_depth == 0 ? 0 : 2 * stats.max_depth - 1)
              << " seconds=" << std::fixed << std::setprecision(3)
              << match_seconds << '\n';
    print_integer_histogram("augmenting_depth_histogram",
                            stats.depth_histogram);
    print_integer_histogram("hopcroft_karp_phase_depths",
                            stats.phase_augmentations);
    print_string_histogram("augmenting_forward_templates",
                           stats.forward_templates, 20);
    print_string_histogram("alternating_transitions",
                           stats.alternating_transitions, 20);
    print_string_histogram("alternating_path_templates",
                           stats.path_templates, 20);
    print_matching_templates(pair_left, matched_certificate);

    if (shortfall != 0) {
      const HallWitness witness =
          hall_witness(adjacency, pair_left, pair_right);
      if (witness.excess != shortfall) {
        throw std::logic_error(
            "residual Hall excess does not equal matching shortfall");
      }
      std::cout << "hall_mincut left_set=" << witness.left_size
                << " neighbor_set=" << witness.neighbor_size
                << " excess=" << witness.excess
                << " profiles_touched=" << witness.profiles_touched
                << " unmatched_samples=";
      for (std::size_t index = 0;
           index < witness.unmatched_left.size(); ++index) {
        if (index != 0) {
          std::cout << ',';
        }
        std::cout << witness.unmatched_left[index];
      }
      std::cout << '\n';
      print_unmatched_samples(pair_left, 12);
    }
    std::cout << "stage_end m=" << m_
              << " stage=" << stage_name(stage)
              << " saturated=" << (shortfall == 0 ? "yes" : "no")
              << '\n';
    return shortfall == 0;
  }

  void run_incremental_repair() const {
    std::cout << "incremental_repair_begin m=" << m_
              << " preserve_stage_A=yes\n";
    std::vector<std::vector<Edge>> stage_a_adjacency;
    std::vector<std::vector<Edge>> stage_b_adjacency;
    build_graph(Stage::kOneLocalEdit, stage_a_adjacency);

    std::vector<Vertex> pair_left;
    std::vector<Vertex> pair_right;
    std::vector<Certificate> matched_certificate;
    const MatchStats initial =
        maximum_matching(stage_a_adjacency, pair_left, pair_right,
                         matched_certificate);
    verify_matching(Stage::kOneLocalEdit, stage_a_adjacency, pair_left,
                    pair_right, matched_certificate, initial.matching);

    build_graph(Stage::kHammingRadiusTwo, stage_b_adjacency);
    std::vector<std::vector<Vertex>> old_rights(
        static_cast<std::size_t>(left_count_));
    std::uint64_t old_edges = 0;
    std::uint64_t new_edges = 0;
    std::map<std::string, std::uint64_t> new_edge_templates;
    for (Vertex left = 0; left < left_count_; ++left) {
      std::vector<Vertex>& old = old_rights[left];
      old.reserve(stage_a_adjacency[left].size());
      for (const Edge& edge : stage_a_adjacency[left]) {
        old.push_back(edge.right);
      }
      std::sort(old.begin(), old.end());
      if (std::adjacent_find(old.begin(), old.end()) != old.end()) {
        throw std::logic_error("stage A contains a duplicate right");
      }
      old_edges += old.size();
      for (const Edge& edge : stage_b_adjacency[left]) {
        if (std::binary_search(old.begin(), old.end(), edge.right)) {
          continue;
        }
        ++new_edges;
        const MoveType move = certificate_move(edge.certificate);
        if (move != MoveType::kDoubleAdd &&
            move != MoveType::kDoubleRemove) {
          throw std::logic_error(
              "stage-B difference has a non-double edit certificate");
        }
        ++new_edge_templates[coarse_certificate(edge.certificate)];
      }
      for (const Vertex right : old) {
        const auto found = std::find_if(
            stage_b_adjacency[left].begin(),
            stage_b_adjacency[left].end(),
            [&](const Edge& edge) { return edge.right == right; });
        if (found == stage_b_adjacency[left].end()) {
          throw std::logic_error("stage A is not a subgraph of stage B");
        }
      }
    }
    if (old_edges + new_edges !=
        std::accumulate(
            stage_b_adjacency.begin(), stage_b_adjacency.end(),
            std::uint64_t{0},
            [](const std::uint64_t total,
               const std::vector<Edge>& edges) {
              return total + edges.size();
            })) {
      throw std::logic_error("incremental edge accounting failed");
    }

    // The pair itself is preserved.  Replace its stage-A certificate by the
    // canonical certificate stored on the same edge in the enlarged graph.
    for (Vertex left = 0; left < left_count_; ++left) {
      if (pair_left[left] == kNoVertex) {
        continue;
      }
      const auto found = std::find_if(
          stage_b_adjacency[left].begin(),
          stage_b_adjacency[left].end(),
          [&](const Edge& edge) {
            return edge.right == pair_left[left];
          });
      if (found == stage_b_adjacency[left].end()) {
        throw std::logic_error("preserved stage-A pair disappeared");
      }
      matched_certificate[left] = found->certificate;
    }

    const MatchStats repair =
        augment_matching(stage_b_adjacency, pair_left, pair_right,
                         matched_certificate, &old_rights);
    verify_matching(Stage::kHammingRadiusTwo, stage_b_adjacency, pair_left,
                    pair_right, matched_certificate, repair.matching);
    if (repair.matching != left_count_ ||
        repair.augmentations != left_count_ - initial.matching) {
      throw std::logic_error(
          "incremental repair did not exactly close the stage-A shortfall");
    }

    std::uint64_t final_new_edges = 0;
    std::map<std::string, std::uint64_t> final_new_templates;
    for (Vertex left = 0; left < left_count_; ++left) {
      if (pair_left[left] == kNoVertex ||
          std::binary_search(old_rights[left].begin(),
                             old_rights[left].end(),
                             pair_left[left])) {
        continue;
      }
      ++final_new_edges;
      ++final_new_templates[
          coarse_certificate(matched_certificate[left])];
    }

    std::cout << "incremental_edge_difference old_edges=" << old_edges
              << " added_edges=" << new_edges
              << " enlarged_edges=" << (old_edges + new_edges) << '\n';
    print_string_histogram("incremental_added_edge_templates",
                           new_edge_templates, 20);
    std::cout << "incremental_repair initial_matching="
              << initial.matching
              << " initial_shortfall=" << (left_count_ - initial.matching)
              << " augmentations=" << repair.augmentations
              << " final_matching=" << repair.matching
              << " phases=" << repair.phases
              << " max_augmenting_depth=" << repair.max_depth
              << " max_augmenting_edge_length="
              << (repair.max_depth == 0 ? 0
                                        : 2 * repair.max_depth - 1)
              << " paths_using_new_edges="
              << repair.paths_using_new_edges
              << " new_forward_edge_uses=" << repair.new_forward_edges
              << " new_backward_edge_uses=" << repair.new_backward_edges
              << " final_new_matched_edges=" << final_new_edges << '\n';
    print_integer_histogram("incremental_augmenting_depth_histogram",
                            repair.depth_histogram);
    print_integer_histogram("incremental_phase_depths",
                            repair.phase_augmentations);
    print_string_histogram("incremental_new_forward_templates",
                           repair.new_forward_templates, 20);
    print_string_histogram("incremental_new_backward_templates",
                           repair.new_backward_templates, 20);
    print_string_histogram("incremental_alternating_transitions",
                           repair.alternating_transitions, 20);
    print_string_histogram("incremental_path_templates",
                           repair.path_templates, 30);
    print_string_histogram("incremental_final_new_templates",
                           final_new_templates, 20);
    std::cout << "incremental_repair_end m=" << m_
              << " saturated=yes\n";
  }

  void print_unmatched_samples(const std::vector<Vertex>& pair_left,
                               const std::size_t limit) const {
    std::size_t shown = 0;
    for (std::size_t parameter = 0;
         parameter < profile_count_ && shown < limit; ++parameter) {
      for (const LeftDescriptor& left : profiles_[parameter].left) {
        if (pair_left[left.id] != kNoVertex) {
          continue;
        }
        std::cout << "unmatched left=" << left.id
                  << " P="
                  << decode_parameter(m_,
                                      static_cast<Parameter>(parameter))
                  << " A=" << decode_signature(m_, left.signature)
                  << " representations="
                  << left.representations.size() << '\n';
        if (++shown == limit) {
          break;
        }
      }
    }
  }

  Options options_;
  int m_;
  int row_count_;
  std::size_t selection_count_;
  std::size_t signature_count_;
  std::size_t profile_count_;
  std::vector<int> rows_;
  std::vector<Signature> signatures_;
  std::vector<Profile> profiles_;
  Vertex left_count_ = 0;
  Vertex right_count_ = 0;
};

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = parse_options(argc, argv);
    RepresentationExperiment experiment(options);
    experiment.run();
    return EXIT_SUCCESS;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return EXIT_FAILURE;
  }
}
