// Heuristic search for the fixed-q special Golay system at length 167.
//
// This is deliberately dependency-free.  Every state satisfies the forced
// endpoint, ordinary-sum, and alternating-sum invariants, so a move is just a
// sign swap within one of four parity classes.  Correlations and objective
// changes are maintained with exact integer arithmetic.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <filesystem>
#include <iomanip>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

namespace {

constexpr int NX = 83;
constexpr int NY = 81;
constexpr int MAX_LAG = 81;

using Clock = std::chrono::steady_clock;

struct Options {
  double seconds = 60.0;
  uint64_t iterations = 0;  // Per thread; zero means use the wall clock.
  int threads = 1;
  uint64_t seed = 668;
  int epoch = 250000;
  int polish_steps = 80;
  int objective = -1;  // -1 diversifies workers; 0=L2, 1=L1, 2/3 hybrids.
  std::string mode = "auto";
  double temperature_start = 0.0;  // Zero uses a worker-diversified default.
  double temperature_end = 0.0;
  std::string output = "output/special_local_best.json";
  bool quiet = false;
};

struct State {
  std::array<int8_t, NX> x{};
  std::array<int8_t, NY> y{};
  std::array<int16_t, MAX_LAG + 1> r{};  // r[0] is unused.
  int energy = 0;
};

struct Metrics {
  int energy = 0;
  int nonzero = 0;
  int max_abs = 0;
  int l1 = 0;

  auto key() const { return std::tie(energy, nonzero, max_abs, l1); }
};

struct WorkerResult {
  State best;
  Metrics metrics;
  uint64_t moves = 0;
  uint64_t accepted = 0;
  uint64_t restarts = 0;
  uint64_t worker_seed = 0;
  bool initialized = false;
};

struct FlipSet {
  // Global coordinates 0..82 are X and 83..163 are Y.
  std::array<int, 4> p{};
  int size = 0;
};

std::array<std::vector<int>, 4> make_groups() {
  std::array<std::vector<int>, 4> g;
  // X-even excludes the two fixed endpoints x[0]=+1, x[82]=-1.
  for (int i = 2; i <= 80; i += 2) g[0].push_back(i);
  for (int i = 1; i <= 81; i += 2) g[1].push_back(i);
  // No endpoint of Y is fixed after safely normalizing sum(Y)=+9.
  for (int i = 0; i <= 80; i += 2) g[2].push_back(NX + i);
  for (int i = 1; i <= 79; i += 2) g[3].push_back(NX + i);
  return g;
}

const std::array<std::vector<int>, 4> GROUPS = make_groups();
const std::array<int, 4> GROUP_PLUS = {20, 25, 25, 20};

int8_t &at(State &s, int p) { return p < NX ? s.x[p] : s.y[p - NX]; }
int8_t at(const State &s, int p) {
  return p < NX ? s.x[p] : s.y[p - NX];
}

Metrics metrics(const State &s) {
  Metrics m;
  for (int k = 1; k <= MAX_LAG; ++k) {
    const int v = s.r[k];
    m.energy += v * v;
    m.nonzero += (v != 0);
    m.max_abs = std::max(m.max_abs, std::abs(v));
    m.l1 += std::abs(v);
  }
  return m;
}

// Several exact objectives share the same unique zero set but have quite
// different local minima.  Parallel workers deliberately diversify over
// them; candidates are always ranked for output by the unweighted L2 energy.
int search_cost(const State &s, int kind) {
  const Metrics m = metrics(s);
  switch (kind & 3) {
    case 0: return m.energy;
    case 1: return 4 * m.l1;
    case 2: return m.energy + 8 * m.nonzero;
    default: return m.energy + 4 * m.l1;
  }
}

int search_cost_after(const State &s,
                      const std::array<int16_t, MAX_LAG + 1> &d, int kind) {
  int energy = 0, nonzero = 0, l1 = 0;
  for (int k = 1; k <= MAX_LAG; ++k) {
    const int v = s.r[k] + d[k];
    energy += v * v;
    nonzero += (v != 0);
    l1 += std::abs(v);
  }
  switch (kind & 3) {
    case 0: return energy;
    case 1: return 4 * l1;
    case 2: return energy + 8 * nonzero;
    default: return energy + 4 * l1;
  }
}

bool better(const State &a, const State &b) {
  const auto ma = metrics(a);
  const auto mb = metrics(b);
  if (ma.key() != mb.key()) return ma.key() < mb.key();
  if (a.x != b.x) return a.x < b.x;
  return a.y < b.y;
}

void recompute(State &s) {
  s.r.fill(0);
  for (int k = 1; k <= MAX_LAG; ++k) {
    int v = 0;
    for (int i = 0; i + k < NX; ++i) v += s.x[i] * s.x[i + k];
    if (k < NY) {
      for (int i = 0; i + k < NY; ++i) v += s.y[i] * s.y[i + k];
    }
    s.r[k] = static_cast<int16_t>(v);
  }
  s.energy = metrics(s).energy;
}

template <size_t N>
int sign_sum(const std::array<int8_t, N> &a) {
  return std::accumulate(a.begin(), a.end(), 0);
}

template <size_t N>
int alternating_sum(const std::array<int8_t, N> &a) {
  int v = 0;
  for (size_t i = 0; i < N; ++i) v += (i & 1) ? -a[i] : a[i];
  return v;
}

void validate(const State &s) {
  if (s.x[0] != 1 || s.x[82] != -1 || sign_sum(s.x) != 9 ||
      alternating_sum(s.x) != -9 || sign_sum(s.y) != 9 ||
      alternating_sum(s.y) != 9) {
    throw std::runtime_error("state invariant failure");
  }
  State copy = s;
  recompute(copy);
  if (copy.r != s.r || copy.energy != s.energy) {
    throw std::runtime_error("incremental correlation failure");
  }
}

template <typename Rng>
void choose_exact_pluses(State &s, int group, Rng &rng) {
  auto positions = GROUPS[group];
  std::shuffle(positions.begin(), positions.end(), rng);
  for (int p : positions) at(s, p) = -1;
  for (int j = 0; j < GROUP_PLUS[group]; ++j) at(s, positions[j]) = 1;
}

template <typename Rng>
State random_state(Rng &rng) {
  State s;
  s.x.fill(-1);
  s.y.fill(-1);
  s.x[0] = 1;
  s.x[82] = -1;
  for (int g = 0; g < 4; ++g) choose_exact_pluses(s, g, rng);
  recompute(s);
  return s;
}

// Published modular seed, split into the active X(83),Y(81) blocks.
constexpr const char *SEED_X =
    "++++----++++----++++--+-++-+--+-++-+--+-+-----++++----++++----++-+--+-++-+--+-++-+-";
constexpr const char *SEED_Y =
    "-++++----++++----+++-++-+--+-++-+--+-++-+++----++++----++++---+--+-++-+--+-++-+--";

template <typename Rng>
void project_group(State &s, int group, const std::vector<int8_t> &target,
                   Rng &rng) {
  std::vector<int> preferred, other;
  for (int p : GROUPS[group]) {
    const int local = p < NX ? p : p - NX;
    (target[local] == 1 ? preferred : other).push_back(p);
  }
  std::shuffle(preferred.begin(), preferred.end(), rng);
  std::shuffle(other.begin(), other.end(), rng);
  for (int p : GROUPS[group]) at(s, p) = -1;
  int need = GROUP_PLUS[group];
  for (int p : preferred) {
    if (!need) break;
    at(s, p) = 1;
    --need;
  }
  for (int p : other) {
    if (!need) break;
    at(s, p) = 1;
    --need;
  }
}

std::vector<int8_t> signs_from_string(const char *text, int n) {
  std::vector<int8_t> a;
  for (int i = 0; text[i] && static_cast<int>(a.size()) < n; ++i) {
    if (text[i] == '+') a.push_back(1);
    if (text[i] == '-') a.push_back(-1);
  }
  if (static_cast<int>(a.size()) != n) throw std::runtime_error("bad seed string");
  return a;
}

template <typename Rng>
State projected_seed_state(Rng &rng, int variant) {
  auto tx = signs_from_string(SEED_X, NX);
  auto ty = signs_from_string(SEED_Y, NY);
  if (variant & 1) std::reverse(tx.begin(), tx.end());
  if (variant & 2) std::reverse(ty.begin(), ty.end());
  if (variant & 4) for (auto &v : tx) v = -v;
  if (variant & 8) for (auto &v : ty) v = -v;

  State s;
  s.x.fill(-1);
  s.y.fill(-1);
  s.x[0] = 1;
  s.x[82] = -1;
  project_group(s, 0, tx, rng);
  project_group(s, 1, tx, rng);
  project_group(s, 2, ty, rng);
  project_group(s, 3, ty, rng);
  recompute(s);
  return s;
}

template <typename Rng>
int random_with_sign(const State &s, int group, int wanted, Rng &rng) {
  const auto &positions = GROUPS[group];
  // Every group always contains both signs.  Rejection sampling takes two
  // probes on average and avoids rebuilding positive/negative lists.
  for (;;) {
    const int p = positions[rng() % positions.size()];
    if (at(s, p) == wanted) return p;
  }
}

template <typename Rng>
FlipSet propose(const State &s, Rng &rng, bool compound) {
  FlipSet f;
  const int g1 = static_cast<int>(rng() % 4);
  f.p[f.size++] = random_with_sign(s, g1, 1, rng);
  f.p[f.size++] = random_with_sign(s, g1, -1, rng);
  if (compound) {
    int g2;
    do g2 = static_cast<int>(rng() % 4); while (g2 == g1);
    f.p[f.size++] = random_with_sign(s, g2, 1, rng);
    f.p[f.size++] = random_with_sign(s, g2, -1, rng);
  }
  return f;
}

bool contains_local(const std::array<int, 4> &p, int count, int value) {
  for (int i = 0; i < count; ++i) if (p[i] == value) return true;
  return false;
}

void correlation_delta(const State &s, const FlipSet &f,
                       std::array<int16_t, MAX_LAG + 1> &d) {
  d.fill(0);
  std::array<int, 4> local{};
  for (int which = 0; which < 2; ++which) {
    const bool want_x = (which == 0);
    int count = 0;
    for (int j = 0; j < f.size; ++j) {
      if ((f.p[j] < NX) == want_x)
        local[count++] = want_x ? f.p[j] : f.p[j] - NX;
    }
    const int n = want_x ? NX : NY;
    for (int j = 0; j < count; ++j) {
      const int p = local[j];
      const int sp = want_x ? s.x[p] : s.y[p];
      for (int q = 0; q < n; ++q) {
        if (contains_local(local, count, q)) continue;
        const int k = std::abs(p - q);
        if (!k || k > MAX_LAG) continue;
        const int sq = want_x ? s.x[q] : s.y[q];
        d[k] -= static_cast<int16_t>(2 * sp * sq);
      }
    }
  }
}

int energy_delta(const State &s,
                 const std::array<int16_t, MAX_LAG + 1> &d) {
  int de = 0;
  for (int k = 1; k <= MAX_LAG; ++k)
    de += 2 * s.r[k] * d[k] + d[k] * d[k];
  return de;
}

void apply(State &s, const FlipSet &f,
           const std::array<int16_t, MAX_LAG + 1> &d, int de) {
  for (int j = 0; j < f.size; ++j) at(s, f.p[j]) = -at(s, f.p[j]);
  for (int k = 1; k <= MAX_LAG; ++k) s.r[k] += d[k];
  s.energy += de;
}

struct SwapChoice {
  FlipSet flips;
  std::array<int16_t, MAX_LAG + 1> delta{};
  int de = 0;
  bool found = false;
};

// Exact best-improvement descent over all currently valid invariant-preserving
// two-flip swaps.  Used sparingly after each stochastic epoch.
SwapChoice best_improving_swap(const State &s) {
  SwapChoice best;
  best.de = 0;
  std::array<int16_t, MAX_LAG + 1> d{};
  for (int g = 0; g < 4; ++g) {
    const auto &positions = GROUPS[g];
    for (int a : positions) {
      if (at(s, a) != 1) continue;
      for (int b : positions) {
        if (at(s, b) != -1) continue;
        FlipSet f;
        f.p[0] = a;
        f.p[1] = b;
        f.size = 2;
        correlation_delta(s, f, d);
        const int de = energy_delta(s, d);
        if (de < best.de) {
          best.flips = f;
          best.delta = d;
          best.de = de;
          best.found = true;
        }
      }
    }
  }
  return best;
}

void polish(State &s, int max_steps, uint64_t &moves, uint64_t &accepted) {
  for (int step = 0; step < max_steps; ++step) {
    const auto best = best_improving_swap(s);
    // Count candidate-equivalent work approximately for throughput reporting.
    moves += 1600;
    if (!best.found) break;
    apply(s, best.flips, best.delta, best.de);
    ++accepted;
  }
}

uint64_t splitmix64(uint64_t x) {
  x += 0x9e3779b97f4a7c15ULL;
  x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
  x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
  return x ^ (x >> 31);
}

void update_best(WorkerResult &result, const State &candidate) {
  if (!result.initialized || better(candidate, result.best)) {
    result.best = candidate;
    result.metrics = metrics(candidate);
    result.initialized = true;
  }
}

WorkerResult run_worker(const Options &opt, int worker, Clock::time_point deadline,
                        std::atomic<bool> &solved) {
  WorkerResult result;
  result.worker_seed = splitmix64(opt.seed + static_cast<uint64_t>(worker));
  std::mt19937_64 rng(result.worker_seed);
  std::uniform_real_distribution<double> unit(0.0, 1.0);

  const double t0_table[] = {220.0, 360.0, 600.0, 900.0};
  const double t0 = opt.temperature_start > 0 ? opt.temperature_start
                                               : t0_table[worker % 4];
  const double tend = opt.temperature_end > 0 ? opt.temperature_end
                                               : ((worker & 1) ? 1.0 : 4.0);
  const int objective_kind = opt.objective < 0 ? (worker & 3) : opt.objective;
  const int epoch = opt.epoch + (worker % 3) * (opt.epoch / 5);
  const bool use_tabu = opt.mode == "tabu" ||
                        (opt.mode == "auto" && (worker % 3) == 2);

  while (!solved.load(std::memory_order_relaxed)) {
    if (opt.iterations && result.moves >= opt.iterations) break;
    if (!opt.iterations && Clock::now() >= deadline) break;

    State current;
    if ((result.restarts % 5) == 0)
      current = projected_seed_state(rng, static_cast<int>(rng() & 15));
    else
      current = random_state(rng);
    State epoch_best = current;
    int current_cost = search_cost(current, objective_kind);
    update_best(result, current);
    ++result.restarts;

    if (!use_tabu) {
      for (int step = 0; step < epoch; ++step) {
        if ((step & 4095) == 0) {
          if (solved.load(std::memory_order_relaxed)) break;
          if (opt.iterations && result.moves >= opt.iterations) break;
          if (!opt.iterations && Clock::now() >= deadline) break;
        }
        const double phase = static_cast<double>(step) / std::max(1, epoch - 1);
        const double temperature = t0 * std::pow(tend / t0, phase);
        // Compound swaps become more useful late in the cooling schedule, when
        // all single swaps may be uphill.
        const bool compound = (rng() % 1000) < static_cast<uint64_t>(80 + 170 * phase);
        const FlipSet f = propose(current, rng, compound);
        std::array<int16_t, MAX_LAG + 1> d{};
        correlation_delta(current, f, d);
        const int de = energy_delta(current, d);
        const int new_cost = search_cost_after(current, d, objective_kind);
        const int dc = new_cost - current_cost;
        ++result.moves;
        if (dc <= 0 || unit(rng) < std::exp(-static_cast<double>(dc) / temperature)) {
          apply(current, f, d, de);
          current_cost = new_cost;
          ++result.accepted;
          if (better(current, epoch_best)) epoch_best = current;
          update_best(result, current);
          if (current.energy == 0) {
            solved.store(true, std::memory_order_relaxed);
            break;
          }
        }
      }
    } else {
      // Sampled tabu steepest descent.  It accepts the best admissible move
      // even uphill and forbids immediate reversal of recently flipped signs.
      std::array<uint64_t, NX + NY> tabu_until{};
      uint64_t tabu_step = 0;
      int basin_best_cost = current_cost;
      constexpr int samples = 96;
      for (int budget = 0; budget < epoch; budget += samples, ++tabu_step) {
        if ((tabu_step & 63) == 0) {
          if (solved.load(std::memory_order_relaxed)) break;
          if (opt.iterations && result.moves >= opt.iterations) break;
          if (!opt.iterations && Clock::now() >= deadline) break;
        }
        SwapChoice choice;
        int choice_cost = std::numeric_limits<int>::max();
        int choice_energy = std::numeric_limits<int>::max();
        for (int sample = 0; sample < samples; ++sample) {
          const bool compound = (rng() % 1000) < 120;
          const FlipSet f = propose(current, rng, compound);
          bool is_tabu = false;
          for (int j = 0; j < f.size; ++j)
            is_tabu |= tabu_until[f.p[j]] > tabu_step;
          std::array<int16_t, MAX_LAG + 1> d{};
          correlation_delta(current, f, d);
          const int de = energy_delta(current, d);
          const int new_cost = search_cost_after(current, d, objective_kind);
          // Aspiration allows a tabu move when it improves the best search
          // objective seen in this basin.
          if (is_tabu && new_cost >= basin_best_cost) continue;
          const int new_energy = current.energy + de;
          if (std::tie(new_cost, new_energy) <
              std::tie(choice_cost, choice_energy)) {
            choice.flips = f;
            choice.delta = d;
            choice.de = de;
            choice.found = true;
            choice_cost = new_cost;
            choice_energy = new_energy;
          }
        }
        result.moves += samples;
        if (!choice.found) {
          tabu_until.fill(0);
          continue;
        }
        apply(current, choice.flips, choice.delta, choice.de);
        current_cost = choice_cost;
        basin_best_cost = std::min(basin_best_cost, current_cost);
        ++result.accepted;
        const uint64_t tenure = 5 + (rng() % 9);
        for (int j = 0; j < choice.flips.size; ++j)
          tabu_until[choice.flips.p[j]] = tabu_step + tenure;
        if (better(current, epoch_best)) epoch_best = current;
        update_best(result, current);
        if (current.energy == 0) {
          solved.store(true, std::memory_order_relaxed);
          break;
        }
      }
    }

    current = epoch_best;
    polish(current, opt.polish_steps, result.moves, result.accepted);
    update_best(result, current);
    if (current.energy == 0) {
      solved.store(true, std::memory_order_relaxed);
      break;
    }
  }
  validate(result.best);
  return result;
}

std::string json_array(const int8_t *values, int n) {
  std::ostringstream out;
  out << '[';
  for (int i = 0; i < n; ++i) {
    if (i) out << ',';
    out << static_cast<int>(values[i]);
  }
  out << ']';
  return out.str();
}

void write_result(const Options &opt, const WorkerResult &best,
                  const std::vector<WorkerResult> &workers, double elapsed) {
  const auto slash = opt.output.find_last_of('/');
  if (slash != std::string::npos) {
    const std::string dir = opt.output.substr(0, slash);
    if (!dir.empty()) std::filesystem::create_directories(dir);
  }
  const std::string temporary = opt.output + ".tmp";
  std::ofstream out(temporary);
  if (!out) throw std::runtime_error("cannot open output file");
  out << "{\n";
  out << "  \"kind\": \"fixed-q-special-local-search-candidate\",\n";
  out << "  \"exact\": " << (best.metrics.energy == 0 ? "true" : "false") << ",\n";
  out << "  \"base_seed\": " << opt.seed << ",\n";
  out << "  \"worker_seed\": " << best.worker_seed << ",\n";
  out << "  \"threads\": " << opt.threads << ",\n";
  out << "  \"seconds\": " << std::fixed << std::setprecision(6) << elapsed << ",\n";
  out << "  \"energy\": " << best.metrics.energy << ",\n";
  out << "  \"nonzero_lags\": " << best.metrics.nonzero << ",\n";
  out << "  \"max_abs_residual\": " << best.metrics.max_abs << ",\n";
  out << "  \"l1_residual\": " << best.metrics.l1 << ",\n";
  out << "  \"normalization\": {\"sum_x\":9,\"alt_x\":-9,\"x0\":1,\"x82\":-1,\"sum_y\":9,\"alt_y\":9},\n";
  out << "  \"x\": " << json_array(best.best.x.data(), NX) << ",\n";
  out << "  \"y\": " << json_array(best.best.y.data(), NY) << ",\n";
  out << "  \"residuals_lag_1_through_81\": [";
  for (int k = 1; k <= MAX_LAG; ++k) {
    if (k > 1) out << ',';
    out << best.best.r[k];
  }
  out << "],\n";
  uint64_t moves = 0, accepted = 0, restarts = 0;
  for (const auto &w : workers) {
    moves += w.moves;
    accepted += w.accepted;
    restarts += w.restarts;
  }
  out << "  \"search\": {\"moves\":" << moves << ",\"accepted\":" << accepted
      << ",\"restarts\":" << restarts << ",\"epoch\":" << opt.epoch
      << ",\"polish_steps\":" << opt.polish_steps
      << ",\"objective\":" << opt.objective << ",\"mode\":\"" << opt.mode
      << "\",\"temperature_start\":" << opt.temperature_start
      << ",\"temperature_end\":" << opt.temperature_end << "}\n";
  out << "}\n";
  out.close();
  if (std::rename(temporary.c_str(), opt.output.c_str()) != 0)
    throw std::runtime_error("cannot rename output file");
}

void usage(const char *argv0) {
  std::cerr << "Usage: " << argv0
            << " [--seconds N] [--iterations N] [--threads N] [--seed N]\n"
               "       [--epoch N] [--polish-steps N] [--objective -1..3]\n"
               "       [--mode auto|anneal|tabu] [--temperature-start N]\n"
               "       [--temperature-end N] [--output PATH] [--quiet]\n";
}

Options parse_args(int argc, char **argv) {
  Options o;
  o.threads = std::max(1u, std::thread::hardware_concurrency());
  for (int i = 1; i < argc; ++i) {
    const std::string a = argv[i];
    auto value = [&]() -> std::string {
      if (++i >= argc) throw std::runtime_error("missing value after " + a);
      return argv[i];
    };
    if (a == "--seconds") o.seconds = std::stod(value());
    else if (a == "--iterations") o.iterations = std::stoull(value());
    else if (a == "--threads") o.threads = std::stoi(value());
    else if (a == "--seed") o.seed = std::stoull(value());
    else if (a == "--epoch") o.epoch = std::stoi(value());
    else if (a == "--polish-steps") o.polish_steps = std::stoi(value());
    else if (a == "--objective") o.objective = std::stoi(value());
    else if (a == "--mode") o.mode = value();
    else if (a == "--temperature-start") o.temperature_start = std::stod(value());
    else if (a == "--temperature-end") o.temperature_end = std::stod(value());
    else if (a == "--output") o.output = value();
    else if (a == "--quiet") o.quiet = true;
    else if (a == "--help" || a == "-h") { usage(argv[0]); std::exit(0); }
    else throw std::runtime_error("unknown argument: " + a);
  }
  if (o.seconds <= 0 || o.threads <= 0 || o.epoch <= 0 || o.polish_steps < 0)
    throw std::runtime_error("numeric options must be positive");
  if (o.objective < -1 || o.objective > 3)
    throw std::runtime_error("objective must be -1, 0, 1, 2, or 3");
  if (o.mode != "auto" && o.mode != "anneal" && o.mode != "tabu")
    throw std::runtime_error("mode must be auto, anneal, or tabu");
  return o;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    const Options opt = parse_args(argc, argv);
    const auto start = Clock::now();
    const auto deadline = start + std::chrono::duration_cast<Clock::duration>(
                                      std::chrono::duration<double>(opt.seconds));
    std::atomic<bool> solved{false};
    std::vector<WorkerResult> results(opt.threads);
    std::vector<std::thread> threads;
    threads.reserve(opt.threads);
    for (int w = 0; w < opt.threads; ++w) {
      threads.emplace_back([&, w] { results[w] = run_worker(opt, w, deadline, solved); });
    }
    for (auto &thread : threads) thread.join();
    const double elapsed = std::chrono::duration<double>(Clock::now() - start).count();

    int winner = 0;
    for (int w = 1; w < opt.threads; ++w)
      if (better(results[w].best, results[winner].best)) winner = w;
    const auto &best = results[winner];
    write_result(opt, best, results, elapsed);

    uint64_t moves = 0, accepted = 0, restarts = 0;
    for (const auto &w : results) {
      moves += w.moves;
      accepted += w.accepted;
      restarts += w.restarts;
    }
    if (!opt.quiet) {
      std::cout << "energy=" << best.metrics.energy
                << " nonzero=" << best.metrics.nonzero
                << " max_abs=" << best.metrics.max_abs
                << " l1=" << best.metrics.l1 << '\n';
      std::cout << "elapsed=" << std::fixed << std::setprecision(3) << elapsed
                << " moves=" << moves << " accepted=" << accepted
                << " restarts=" << restarts << " winner=" << winner << '\n';
      std::cout << "output=" << opt.output << '\n';
      for (int w = 0; w < opt.threads; ++w) {
        const bool is_tabu = opt.mode == "tabu" ||
                             (opt.mode == "auto" && (w % 3) == 2);
        const int objective = opt.objective < 0 ? (w & 3) : opt.objective;
        std::cout << "worker=" << w << " mode=" << (is_tabu ? "tabu" : "anneal")
                  << " objective=" << objective
                  << " energy=" << results[w].metrics.energy
                  << " nonzero=" << results[w].metrics.nonzero
                  << " max_abs=" << results[w].metrics.max_abs << '\n';
      }
    }
    return best.metrics.energy == 0 ? 0 : 2;
  } catch (const std::exception &e) {
    std::cerr << "error: " << e.what() << '\n';
    return 1;
  }
}
