// Deterministic outside-in enumeration of normalized odd-n Turyn sequences.
//
// This independently reconstructs the recursive search described by
// Edmondson--Seberry--Anderson (1994): scan the nonperiodic-correlation
// equations from the highest nonautomatic lag downwards, assign exactly the
// variables first occurring in that equation, and reject the branch unless
// the now-complete equation vanishes.
//
// The implementation is intentionally dependency-free, single-threaded, and
// constant-memory apart from the recursion stack and small sequence arrays.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Entry {
  int variable;  // -1 for a constant
  int coefficient;
};

struct Step {
  int lag;
  std::vector<int> variables;
};

struct Options {
  int n = 41;
  std::string prefix;
  std::uint64_t node_limit = std::numeric_limits<std::uint64_t>::max();
  double seconds = 0.0;
  int bounds_depth = 10;
  bool swap_cd = true;
  bool row_sums_41 = true;
  bool describe = false;
  int emit_step_depth = -1;
  bool cubes_only = false;
};

class Enumerator {
 public:
  explicit Enumerator(Options options)
      : options_(std::move(options)),
        n_(options_.n),
        m_((n_ - 1) / 2),
        assignment_(4 * m_ - 2, 0),
        fixed_by_prefix_(4 * m_ - 2, false),
        start_(std::chrono::steady_clock::now()) {
    if (n_ < 3 || n_ % 2 == 0) {
      throw std::runtime_error("n must be odd and at least 3");
    }
    build_sequences();
    build_steps();
    build_search_order();
    apply_prefix();
    nodes_by_depth_.assign(steps_.size() + 1, 0);
  }

  int run() {
    if (options_.describe) {
      describe();
      return 0;
    }
    search(0);
    if (options_.emit_step_depth >= 0 && options_.cubes_only) {
      return stopped_ ? 2 : 0;
    }
    const double elapsed = elapsed_seconds();
    std::cout << "n=" << n_ << "\n";
    std::cout << "primary_variables=" << assignment_.size() << "\n";
    std::cout << "steps=" << steps_.size() << "\n";
    std::cout << "prefix=" << options_.prefix << "\n";
    std::cout << "complete=" << (stopped_ ? "false" : "true") << "\n";
    std::cout << "solutions=" << solutions_ << "\n";
    std::cout << "emitted_prefixes=" << emitted_ << "\n";
    std::cout << "nodes=" << nodes_ << "\n";
    std::cout << "elapsed_seconds=" << elapsed << "\n";
    std::cout << "nodes_by_depth=";
    for (std::size_t index = 0; index < nodes_by_depth_.size(); ++index) {
      if (index) std::cout << ",";
      std::cout << nodes_by_depth_[index];
    }
    std::cout << "\n";
    if (options_.emit_step_depth >= 0) return stopped_ ? 2 : 0;
    return stopped_ ? 2 : (solutions_ ? 10 : 20);
  }

 private:
  Options options_;
  int n_;
  int m_;
  std::array<std::vector<Entry>, 4> sequences_;
  std::vector<std::string> variable_names_;
  std::vector<int> assignment_;
  std::vector<bool> fixed_by_prefix_;
  std::vector<Step> steps_;
  std::vector<int> search_order_;
  std::vector<std::uint64_t> nodes_by_depth_;
  std::chrono::steady_clock::time_point start_;
  std::uint64_t nodes_ = 0;
  std::uint64_t solutions_ = 0;
  std::uint64_t emitted_ = 0;
  bool stopped_ = false;

  int add_variable(const std::string& name) {
    const int result = static_cast<int>(variable_names_.size());
    variable_names_.push_back(name);
    return result;
  }

  static Entry constant(int sign) { return Entry{-1, sign}; }
  static Entry positive(int variable) { return Entry{variable, 1}; }
  static Entry negative(int variable) { return Entry{variable, -1}; }

  void build_sequences() {
    std::vector<int> a, b, c, d;
    for (int index = 2; index <= m_; ++index) {
      a.push_back(add_variable("a" + std::to_string(index)));
    }
    for (int index = 2; index <= m_; ++index) {
      b.push_back(add_variable("b" + std::to_string(index)));
    }
    for (int index = 1; index <= m_; ++index) {
      c.push_back(add_variable("c" + std::to_string(index)));
    }
    for (int index = 1; index <= m_; ++index) {
      d.push_back(add_variable("d" + std::to_string(index)));
    }

    auto& sequence_a = sequences_[0];
    sequence_a.push_back(constant(1));
    sequence_a.push_back(constant(1));
    for (int variable : a) sequence_a.push_back(positive(variable));
    for (auto it = a.rbegin(); it != a.rend(); ++it) {
      sequence_a.push_back(negative(*it));
    }
    sequence_a.push_back(constant(-1));
    sequence_a.push_back(constant(-1));

    auto& sequence_b = sequences_[1];
    sequence_b.push_back(constant(1));
    sequence_b.push_back(constant(1));
    for (int variable : b) sequence_b.push_back(positive(variable));
    for (auto it = b.rbegin(); it != b.rend(); ++it) {
      sequence_b.push_back(negative(*it));
    }
    sequence_b.push_back(constant(-1));
    sequence_b.push_back(constant(1));

    auto build_symmetric = [&](std::vector<Entry>& sequence,
                               const std::vector<int>& variables) {
      sequence.push_back(constant(1));
      for (int variable : variables) sequence.push_back(positive(variable));
      for (auto it = variables.rbegin() + 1; it != variables.rend(); ++it) {
        sequence.push_back(positive(*it));
      }
      sequence.push_back(constant(1));
    };
    build_symmetric(sequences_[2], c);
    build_symmetric(sequences_[3], d);

    const std::array<std::size_t, 4> expected = {
        static_cast<std::size_t>(n_ + 1),
        static_cast<std::size_t>(n_ + 1),
        static_cast<std::size_t>(n_),
        static_cast<std::size_t>(n_)};
    for (std::size_t index = 0; index < sequences_.size(); ++index) {
      if (sequences_[index].size() != expected[index]) {
        throw std::runtime_error("internal sequence-length error");
      }
    }
    if (variable_names_.size() != assignment_.size()) {
      throw std::runtime_error("internal variable-count error");
    }
  }

  void build_steps() {
    std::vector<bool> seen(assignment_.size(), false);
    for (int lag = n_ - 2; lag >= 1; --lag) {
      // Simplify the quadratic sign polynomial first.  For example, b2
      // occurs twice with opposite coefficients at the first lag and must
      // not be treated as a fresh variable until the following equation.
      std::map<std::pair<int, int>, int> polynomial;
      for (const auto& sequence : sequences_) {
        for (int index = 0; index + lag < static_cast<int>(sequence.size());
             ++index) {
          const Entry left = sequence[index];
          const Entry right = sequence[index + lag];
          const int coefficient = left.coefficient * right.coefficient;
          std::pair<int, int> monomial;
          if (left.variable < 0 && right.variable < 0) {
            monomial = {-1, -1};
          } else if (left.variable < 0 || right.variable < 0) {
            monomial = {std::max(left.variable, right.variable), -1};
          } else if (left.variable == right.variable) {
            monomial = {-1, -1};
          } else {
            monomial = std::minmax(left.variable, right.variable);
          }
          polynomial[monomial] += coefficient;
        }
      }
      std::vector<int> fresh;
      for (const auto& [monomial, coefficient] : polynomial) {
        if (!coefficient) continue;
        for (const int variable : {monomial.first, monomial.second}) {
          if (variable >= 0 && !seen[variable]) {
            seen[variable] = true;
            fresh.push_back(variable);
          }
        }
      }
      std::sort(fresh.begin(), fresh.end());
      fresh.erase(std::unique(fresh.begin(), fresh.end()), fresh.end());
      if (!fresh.empty()) steps_.push_back(Step{lag, std::move(fresh)});
    }
    if (std::find(seen.begin(), seen.end(), false) != seen.end()) {
      throw std::runtime_error("some variables never entered an equation");
    }
  }

  void build_search_order() {
    for (const Step& step : steps_) {
      search_order_.insert(search_order_.end(), step.variables.begin(),
                           step.variables.end());
    }
    if (search_order_.size() != assignment_.size()) {
      throw std::runtime_error("search order does not cover every variable");
    }
  }

  void apply_prefix() {
    if (options_.prefix.size() > search_order_.size()) {
      throw std::runtime_error("prefix is longer than the search order");
    }
    for (std::size_t index = 0; index < options_.prefix.size(); ++index) {
      const char bit = options_.prefix[index];
      if (bit != '0' && bit != '1') {
        throw std::runtime_error("prefix must contain only 0 and 1");
      }
      const int variable = search_order_[index];
      assignment_[variable] = bit == '0' ? 1 : -1;
      fixed_by_prefix_[variable] = true;
    }
  }

  int entry_value(const Entry& entry) const {
    if (entry.variable < 0) return entry.coefficient;
    return entry.coefficient * assignment_[entry.variable];
  }

  bool entry_known(const Entry& entry) const {
    return entry.variable < 0 || assignment_[entry.variable] != 0;
  }

  int correlation_sum(int lag) const {
    int result = 0;
    for (const auto& sequence : sequences_) {
      for (int index = 0; index + lag < static_cast<int>(sequence.size());
           ++index) {
        const Entry left = sequence[index];
        const Entry right = sequence[index + lag];
        if (left.variable >= 0 && left.variable == right.variable) {
          // A sign squares to one even before that sign has been assigned.
          result += left.coefficient * right.coefficient;
        } else {
          result += entry_value(left) * entry_value(right);
        }
      }
    }
    return result;
  }

  bool lag_bound_feasible(int lag) const {
    int fixed = 0;
    int unknown = 0;
    for (const auto& sequence : sequences_) {
      for (int index = 0; index + lag < static_cast<int>(sequence.size());
           ++index) {
        const Entry left = sequence[index];
        const Entry right = sequence[index + lag];
        if (left.variable >= 0 && left.variable == right.variable) {
          fixed += left.coefficient * right.coefficient;
        } else if (entry_known(left) && entry_known(right)) {
          fixed += entry_value(left) * entry_value(right);
        } else {
          ++unknown;
        }
      }
    }
    return std::abs(fixed) <= unknown && ((fixed + unknown) & 1) == 0;
  }

  bool all_lower_lag_bounds_feasible(int highest_exclusive) const {
    for (int lag = 1; lag < highest_exclusive; ++lag) {
      if (!lag_bound_feasible(lag)) return false;
    }
    return true;
  }

  bool cd_order_feasible() const {
    if (!options_.swap_cd) return true;
    const int c_start = 2 * (m_ - 1);
    const int d_start = c_start + m_;
    for (int offset = 0; offset < m_; ++offset) {
      const int c_value = assignment_[c_start + offset];
      const int d_value = assignment_[d_start + offset];
      if (!c_value || !d_value) return true;
      if (c_value != d_value) {
        // Lexicographic order with +1 before -1.
        return c_value > d_value;
      }
    }
    return true;
  }

  bool short_row_sum_feasible(int start) const {
    std::uint64_t reachable = 1;
    int assigned_negative_weight = 0;
    for (int offset = 0; offset < m_; ++offset) {
      const int weight = offset + 1 == m_ ? 1 : 2;
      const int value = assignment_[start + offset];
      if (!value) {
        reachable |= reachable << weight;
      } else if (value < 0) {
        assigned_negative_weight += weight;
      }
    }
    for (const int target : {16, 25}) {
      const int remaining = target - assigned_negative_weight;
      if (remaining >= 0 && remaining < 64 &&
          ((reachable >> remaining) & 1U)) {
        return true;
      }
    }
    return false;
  }

  bool row_sums_feasible() const {
    if (!options_.row_sums_41 || n_ != 41) return true;
    const int c_start = 2 * (m_ - 1);
    const int d_start = c_start + m_;
    return short_row_sum_feasible(c_start) &&
           short_row_sum_feasible(d_start);
  }

  bool should_stop() {
    if (nodes_ >= options_.node_limit) {
      stopped_ = true;
      return true;
    }
    if (options_.seconds > 0 && (nodes_ & 0xffffU) == 0 &&
        elapsed_seconds() >= options_.seconds) {
      stopped_ = true;
      return true;
    }
    return false;
  }

  double elapsed_seconds() const {
    return std::chrono::duration<double>(std::chrono::steady_clock::now() -
                                         start_)
        .count();
  }

  void search(std::size_t depth) {
    if (stopped_ || should_stop()) return;
    ++nodes_;
    ++nodes_by_depth_[depth];
    if (static_cast<int>(depth) == options_.emit_step_depth) {
      std::size_t prefix_length = 0;
      for (std::size_t index = 0; index < depth; ++index) {
        prefix_length += steps_[index].variables.size();
      }
      std::cout << "cube=";
      for (std::size_t index = 0; index < prefix_length; ++index) {
        const int value = assignment_[search_order_[index]];
        if (!value) throw std::runtime_error("unassigned emitted prefix");
        std::cout << (value < 0 ? '1' : '0');
      }
      std::cout << "\n";
      ++emitted_;
      return;
    }
    if (depth == steps_.size()) {
      for (int lag = 1; lag <= n_; ++lag) {
        if (correlation_sum(lag) != 0) return;
      }
      ++solutions_;
      return;
    }

    const Step& step = steps_[depth];
    std::vector<int> free;
    for (int variable : step.variables) {
      if (!fixed_by_prefix_[variable]) free.push_back(variable);
    }
    const unsigned combinations = 1U << free.size();
    for (unsigned mask = 0; mask < combinations; ++mask) {
      for (std::size_t index = 0; index < free.size(); ++index) {
        assignment_[free[index]] = (mask >> index) & 1U ? -1 : 1;
      }
      if (correlation_sum(step.lag) == 0 && cd_order_feasible() &&
          row_sums_feasible() &&
          (static_cast<int>(depth) < options_.bounds_depth ||
           all_lower_lag_bounds_feasible(step.lag))) {
        search(depth + 1);
      }
      for (int variable : free) assignment_[variable] = 0;
      if (stopped_) return;
    }
  }

  void describe() const {
    std::cout << "n=" << n_ << "\n";
    std::cout << "primary_variables=" << assignment_.size() << "\n";
    std::cout << "steps=" << steps_.size() << "\n";
    for (std::size_t depth = 0; depth < steps_.size(); ++depth) {
      std::cout << depth << ":lag=" << steps_[depth].lag << ":";
      for (std::size_t index = 0; index < steps_[depth].variables.size();
           ++index) {
        if (index) std::cout << ",";
        std::cout << variable_names_[steps_[depth].variables[index]];
      }
      std::cout << "\n";
    }
    std::cout << "search_order=";
    for (std::size_t index = 0; index < search_order_.size(); ++index) {
      if (index) std::cout << ",";
      std::cout << variable_names_[search_order_[index]];
    }
    std::cout << "\n";
  }
};

Options parse_options(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto require_value = [&](const std::string& flag) -> std::string {
      if (++index >= argc) throw std::runtime_error("missing value for " + flag);
      return argv[index];
    };
    if (argument == "--n") {
      options.n = std::stoi(require_value(argument));
    } else if (argument == "--prefix") {
      options.prefix = require_value(argument);
    } else if (argument == "--node-limit") {
      options.node_limit = std::stoull(require_value(argument));
    } else if (argument == "--seconds") {
      options.seconds = std::stod(require_value(argument));
    } else if (argument == "--bounds-depth") {
      options.bounds_depth = std::stoi(require_value(argument));
    } else if (argument == "--no-swap-cd") {
      options.swap_cd = false;
    } else if (argument == "--no-row-sums") {
      options.row_sums_41 = false;
    } else if (argument == "--describe") {
      options.describe = true;
    } else if (argument == "--emit-step-depth") {
      options.emit_step_depth = std::stoi(require_value(argument));
    } else if (argument == "--cubes-only") {
      options.cubes_only = true;
    } else {
      throw std::runtime_error("unknown option: " + argument);
    }
  }
  return options;
}

int main(int argc, char** argv) {
  try {
    Enumerator enumerator(parse_options(argc, argv));
    return enumerator.run();
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
}
