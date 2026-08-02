// Fast numerical discovery search for the Bd+dB cross-sum at r=3/2.
//
// This is not a proof component.  It builds the two effective subset chains
// directly from the update definitions, solves them by dense pivoted
// elimination, and samples complete or sparse symmetric weight matrices over
// separated logarithmic scales.  Any apparent violation must be rationalized
// and checked by the exact verifier.

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Matrix = std::vector<std::vector<double>>;

double baseline(int n, bool bd) {
  constexpr double r = 1.5;
  if (bd) return (1.0 - 1.0 / r) / (1.0 - std::pow(r, -n));
  return (n - 1.0) / n * (1.0 - 1.0 / r) /
         (1.0 - std::pow(r, -(n - 1)));
}

std::vector<double> solve(Matrix a, std::vector<double> b) {
  const int n = static_cast<int>(b.size());
  for (int k = 0; k < n; ++k) {
    int pivot = k;
    for (int i = k + 1; i < n; ++i)
      if (std::abs(a[i][k]) > std::abs(a[pivot][k])) pivot = i;
    if (std::abs(a[pivot][k]) < 1e-14)
      throw std::runtime_error("singular absorbing system");
    std::swap(a[k], a[pivot]);
    std::swap(b[k], b[pivot]);
    for (int i = k + 1; i < n; ++i) {
      const double factor = a[i][k] / a[k][k];
      if (factor == 0.0) continue;
      a[i][k] = 0.0;
      for (int j = k + 1; j < n; ++j) a[i][j] -= factor * a[k][j];
      b[i] -= factor * b[k];
    }
  }
  std::vector<double> x(n);
  for (int i = n - 1; i >= 0; --i) {
    double value = b[i];
    for (int j = i + 1; j < n; ++j) value -= a[i][j] * x[j];
    x[i] = value / a[i][i];
  }
  return x;
}

double fixation(const Matrix& w, bool bd) {
  constexpr double r = 1.5;
  const int n = static_cast<int>(w.size());
  const int full = (1 << n) - 1;
  const int m = full - 1;
  std::vector<double> degree(n, 0.0);
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < n; ++j) degree[i] += w[i][j];
  Matrix matrix(m, std::vector<double>(m, 0.0));
  std::vector<double> rhs(m, 0.0);
  for (int state = 1; state < full; ++state) {
    const int row = state - 1;
    matrix[row][row] = 1.0;
    std::vector<std::pair<int, double>> flips;
    double mass = 0.0;
    for (int target = 0; target < n; ++target) {
      const bool target_mutant = state & (1 << target);
      double mutant_weight = 0.0;
      if (bd) {
        // Incoming reproductive mass from parents, normalized by each
        // parent's weighted degree.  The common total-fitness denominator
        // cancels after deleting self-loops.
        for (int parent = 0; parent < n; ++parent)
          if (state & (1 << parent))
            mutant_weight += w[parent][target] / degree[parent];
        double resident_weight = 0.0;
        for (int parent = 0; parent < n; ++parent)
          if (!(state & (1 << parent)))
            resident_weight += w[parent][target] / degree[parent];
        const double value = target_mutant ? resident_weight : r * mutant_weight;
        if (value > 0.0) {
          flips.emplace_back(state ^ (1 << target), value);
          mass += value;
        }
      } else {
        // At a target death, mutant and resident incident weights compete
        // with relative fitness r.  The common target-selection factor 1/n
        // cancels after deleting self-loops.
        for (int parent = 0; parent < n; ++parent)
          if (state & (1 << parent)) mutant_weight += w[parent][target];
        const double resident_weight = degree[target] - mutant_weight;
        const double denominator = r * mutant_weight + resident_weight;
        const double value = target_mutant
                                 ? resident_weight / denominator
                                 : r * mutant_weight / denominator;
        if (value > 0.0) {
          flips.emplace_back(state ^ (1 << target), value);
          mass += value;
        }
      }
    }
    if (!(mass > 0.0)) throw std::runtime_error("disconnected graph");
    for (const auto& transition : flips) {
      const int next = transition.first;
      const double probability = transition.second / mass;
      if (next == full)
        rhs[row] += probability;
      else if (next != 0)
        matrix[row][next - 1] -= probability;
    }
  }
  const auto values = solve(std::move(matrix), std::move(rhs));
  double result = 0.0;
  for (int i = 0; i < n; ++i) result += values[(1 << i) - 1];
  return result / n;
}

bool connected(const Matrix& w) {
  const int n = static_cast<int>(w.size());
  std::vector<int> seen(n, 0), stack{0};
  seen[0] = 1;
  while (!stack.empty()) {
    const int i = stack.back();
    stack.pop_back();
    for (int j = 0; j < n; ++j)
      if (w[i][j] > 0.0 && !seen[j]) {
        seen[j] = 1;
        stack.push_back(j);
      }
  }
  return std::all_of(seen.begin(), seen.end(), [](int x) { return x; });
}

void print_matrix(const Matrix& w) {
  std::cout << "[";
  for (std::size_t i = 0; i < w.size(); ++i) {
    if (i) std::cout << ",";
    std::cout << "[";
    for (std::size_t j = 0; j < w.size(); ++j) {
      if (j) std::cout << ",";
      std::cout << std::setprecision(17) << w[i][j];
    }
    std::cout << "]";
  }
  std::cout << "]\n";
}

Matrix random_regular(int n, std::mt19937_64& rng, int steps) {
  // Hit-and-run in {symmetric zero-diagonal W: W 1 = 1, W >= floor}.
  // Projection onto the nullspace of the unsigned vertex-edge incidence B
  // uses BB^T=(n-2)I+J.
  constexpr double floor = 1e-10;
  std::normal_distribution<double> normal(0.0, 1.0);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  Matrix w(n, std::vector<double>(n, 0.0));
  for (int i = 0; i < n; ++i)
    for (int j = i + 1; j < n; ++j) w[i][j] = w[j][i] = 1.0 / (n - 1);
  for (int step = 0; step < steps; ++step) {
    Matrix z(n, std::vector<double>(n, 0.0));
    std::vector<double> sums(n, 0.0);
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        z[i][j] = z[j][i] = normal(rng);
        sums[i] += z[i][j];
        sums[j] += z[i][j];
      }
    const double sum_s = std::accumulate(sums.begin(), sums.end(), 0.0);
    std::vector<double> lambda(n);
    for (int i = 0; i < n; ++i)
      lambda[i] = sums[i] / (n - 2.0) -
                  sum_s / ((n - 2.0) * (2.0 * n - 2.0));
    double norm = 0.0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        z[i][j] = z[j][i] = z[i][j] - lambda[i] - lambda[j];
        norm += z[i][j] * z[i][j];
      }
    norm = std::sqrt(norm);
    if (norm < 1e-14) continue;
    double lower = -std::numeric_limits<double>::infinity();
    double upper = std::numeric_limits<double>::infinity();
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j) {
        z[i][j] /= norm;
        z[j][i] = z[i][j];
        if (z[i][j] > 1e-15)
          lower = std::max(lower, (floor - w[i][j]) / z[i][j]);
        else if (z[i][j] < -1e-15)
          upper = std::min(upper, (floor - w[i][j]) / z[i][j]);
      }
    const double amount = lower + uniform(rng) * (upper - lower);
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j)
        w[i][j] = w[j][i] = w[i][j] + amount * z[i][j];
  }
  return w;
}

#ifndef CROSS_SUM_NO_MAIN
int main(int argc, char** argv) {
  if (argc < 5) {
    std::cerr << "usage: search_fast N SAMPLES SEED LOG_SPAN [SPARSE]\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  const long samples = std::stol(argv[2]);
  const std::uint64_t seed = std::stoull(argv[3]);
  const double span = std::stod(argv[4]);
  const int mode = argc >= 6 ? std::stoi(argv[5]) : 0;
  const int objective_type = mode / 4;  // 0=sum, 1=product, 2=tangent
  const int search_mode = mode % 4;
  const bool allow_sparse = search_mode == 1;
  std::mt19937_64 rng(seed);
  std::uniform_real_distribution<double> uniform(0.0, 1.0);
  std::uniform_real_distribution<double> log_weight(-span, span);
  const double base_bd = baseline(n, true);
  const double base_db = baseline(n, false);
  const double target = objective_type == 0
                            ? base_bd + base_db
                            : (objective_type == 1 ? base_bd * base_db
                                                   : 2 * base_bd * base_db);
  auto objective_value = [&](double bd, double db) {
    if (objective_type == 0) return bd + db;
    if (objective_type == 1) return bd * db;
    return base_db * bd + base_bd * db;
  };
  if (search_mode == 3) {
    // Multistart simulated annealing on complete-support log weights.  This
    // explores remote local maxima that direct random sampling can miss.
    const bool fixed_support = argc >= 7;
    const std::uint64_t support_mask =
        fixed_support ? std::stoull(argv[6]) : std::numeric_limits<std::uint64_t>::max();
    std::vector<std::pair<int, int>> active_edges;
    int complete_edge = 0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j, ++complete_edge)
        if (!fixed_support || (support_mask & (std::uint64_t(1) << complete_edge)))
          active_edges.emplace_back(i, j);
    const int edge_count = static_cast<int>(active_edges.size());
    const int restarts = std::max(1L, std::min(40L, samples / 1000));
    const long steps = std::max(1000L, samples / restarts);
    std::normal_distribution<double> normal(0.0, 1.0);
    auto build = [&](const std::vector<double>& logs) {
      Matrix w(n, std::vector<double>(n, 0.0));
      const double mean = std::accumulate(logs.begin(), logs.end(), 0.0) /
                          static_cast<double>(logs.size());
      for (int edge = 0; edge < edge_count; ++edge) {
        const auto [i, j] = active_edges[edge];
        w[i][j] = w[j][i] = std::exp(logs[edge] - mean);
      }
      return w;
    };
    double global = -std::numeric_limits<double>::infinity();
    Matrix global_w;
    double global_bd = 0.0, global_db = 0.0;
    for (int restart = 0; restart < restarts; ++restart) {
      std::vector<double> logs(edge_count);
      for (double& value : logs) value = (2 * uniform(rng) - 1) * span;
      Matrix w = build(logs);
      double bd, db, value;
      try {
        bd = fixation(w, true);
        db = fixation(w, false);
        value = objective_value(bd, db);
      } catch (const std::exception&) {
        continue;
      }
      for (long step = 0; step < steps; ++step) {
        const double progress = static_cast<double>(step) / steps;
        const double scale = 1.2 * std::pow(0.02, progress);
        const double temperature = 2e-4 * std::pow(1e-3, progress);
        const int edge = static_cast<int>(rng() % edge_count);
        const double old = logs[edge];
        logs[edge] = std::max(-span, std::min(span, old + scale * normal(rng)));
        Matrix proposal = build(logs);
        try {
          const double pbd = fixation(proposal, true);
          const double pdb = fixation(proposal, false);
          const double proposed = objective_value(pbd, pdb);
          if (proposed >= value ||
              uniform(rng) < std::exp((proposed - value) / temperature)) {
            w = std::move(proposal);
            bd = pbd;
            db = pdb;
            value = proposed;
          } else {
            logs[edge] = old;
          }
        } catch (const std::exception&) {
          logs[edge] = old;
        }
      }
      if (value > global) {
        global = value;
        global_w = w;
        global_bd = bd;
        global_db = db;
      }
      if (value - target > 1e-8) {
        std::cout << "APPARENT_VIOLATION anneal " << restart << " excess "
                  << std::setprecision(17) << value - target << " Bd " << bd
                  << " dB " << db << "\n";
        print_matrix(w);
        return 1;
      }
    }
    std::cout << "NO_VIOLATION anneal n " << n << " best_excess "
              << std::setprecision(17) << global - target << " Bd " << global_bd
              << " dB " << global_db << "\n";
    print_matrix(global_w);
    return 0;
  }
  double best_excess = -std::numeric_limits<double>::infinity();
  double best_bd = 0.0, best_db = 0.0;
  Matrix best;
  long valid = 0;
  for (long sample = 0; sample < samples; ++sample) {
    Matrix w = search_mode == 2 ? random_regular(n, rng, 8 * n)
                         : Matrix(n, std::vector<double>(n, 0.0));
    if (search_mode != 2) {
      const double edge_probability = allow_sparse ? 0.18 + 0.80 * uniform(rng) : 1.0;
      for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j) {
          if (uniform(rng) > edge_probability) continue;
          const double value = std::exp(log_weight(rng));
          w[i][j] = w[j][i] = value;
        }
    }
    if (!connected(w)) continue;
    try {
      const double bd = fixation(w, true);
      const double db = fixation(w, false);
      const double excess = objective_value(bd, db) - target;
      ++valid;
      if (excess > best_excess) {
        best_excess = excess;
        best_bd = bd;
        best_db = db;
        best = w;
      }
      if (excess > 1e-8) {
        std::cout << "APPARENT_VIOLATION sample " << sample << " excess "
                  << std::setprecision(17) << excess << " Bd " << bd << " dB "
                  << db << "\n";
        print_matrix(w);
        return 1;
      }
    } catch (const std::exception&) {
      continue;
    }
  }
  std::cout << "NO_VIOLATION n " << n << " valid " << valid << " best_excess "
            << std::setprecision(17) << best_excess << " Bd " << best_bd
            << " dB " << best_db << "\n";
  print_matrix(best);
  return 0;
}
#endif
