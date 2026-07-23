// Structured local constructor for the 45-phase quartic LP(333) quotient.
//
// This is not a search over 666 independent signs.  Every state satisfies
// the fixed compression and all four nontrivial row-axis equations exactly:
//
//   * z is one of the 972 normalized QPSK encodings of LP(9);
//   * four target-sum length-9 sequences have real PAF signatures summing 0.
//
// The objective contains only the two pure-column and sixteen mixed
// cyclotomic equations from NOVEL_LP333_THEORY.md.  A zero is expanded and
// checked against all 332 oriented nonzero correlations before acceptance.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

constexpr int kCodeCount = 1 << 18;  // 4^9

constexpr std::array<int, 4> kRootReal{1, 0, -1, 0};
constexpr std::array<int, 4> kRootImag{0, 1, 0, -1};

// M_s(k,l) = #{c in P_k : c+b in P_l}, b in C_s.
constexpr int kTransition[4][5][5] = {
    {{0, 1, 0, 0, 0},
     {0, 2, 1, 2, 4},
     {0, 2, 2, 4, 1},
     {1, 2, 2, 2, 2},
     {0, 2, 4, 1, 2}},
    {{0, 0, 1, 0, 0},
     {0, 2, 2, 4, 1},
     {0, 4, 2, 1, 2},
     {0, 1, 2, 2, 4},
     {1, 2, 2, 2, 2}},
    {{0, 0, 0, 1, 0},
     {1, 2, 2, 2, 2},
     {0, 1, 2, 2, 4},
     {0, 2, 4, 2, 1},
     {0, 4, 1, 2, 2}},
    {{0, 0, 0, 0, 1},
     {0, 2, 4, 1, 2},
     {1, 2, 2, 2, 2},
     {0, 4, 1, 2, 2},
     {0, 1, 2, 4, 2}}};

struct Signature {
  std::array<int, 4> value{};

  friend bool operator<(const Signature& left, const Signature& right) {
    return left.value < right.value;
  }
};

Signature operator+(const Signature& left, const Signature& right) {
  Signature result;
  for (int index = 0; index < 4; ++index) {
    result.value[index] = left.value[index] + right.value[index];
  }
  return result;
}

Signature operator-(const Signature& input) {
  Signature result;
  for (int index = 0; index < 4; ++index) {
    result.value[index] = -input.value[index];
  }
  return result;
}

struct State {
  int z_code = 0;
  std::array<int, 4> w_code{};
};

struct Catalog {
  std::vector<int> z;
  std::vector<int> w;
  std::array<Signature, kCodeCount> signature_by_code{};
  std::map<Signature, std::vector<int>> w_by_signature;
};

std::array<int, 9> Decode(int code) {
  std::array<int, 9> result{};
  for (int index = 0; index < 9; ++index) {
    result[index] = code & 3;
    code >>= 2;
  }
  return result;
}

int Encode(const std::array<int, 9>& phases) {
  int result = 0;
  for (int index = 8; index >= 0; --index) {
    result = (result << 2) | phases[index];
  }
  return result;
}

int RealProduct(int left, int right) {
  const int difference = (left - right) & 3;
  return kRootReal[difference];
}

Signature RealSignature(const std::array<int, 9>& phases) {
  Signature result;
  for (int lag = 1; lag <= 4; ++lag) {
    int value = 0;
    for (int row = 0; row < 9; ++row) {
      value += RealProduct(phases[row], phases[(row + lag) % 9]);
    }
    result.value[lag - 1] = value;
  }
  return result;
}

std::pair<int, int> PhaseSum(const std::array<int, 9>& phases) {
  int real = 0;
  int imag = 0;
  for (const int phase : phases) {
    real += kRootReal[phase];
    imag += kRootImag[phase];
  }
  return {real, imag};
}

Catalog BuildCatalog() {
  Catalog catalog;
  for (int code = 0; code < kCodeCount; ++code) {
    const auto phases = Decode(code);
    const auto sum = PhaseSum(phases);
    const Signature signature = RealSignature(phases);
    catalog.signature_by_code[code] = signature;
    if (sum == std::pair<int, int>{1, 0} &&
        signature.value == std::array<int, 4>{-1, -1, -1, -1}) {
      catalog.z.push_back(code);
    }
    if (sum == std::pair<int, int>{0, -3}) {
      catalog.w.push_back(code);
      catalog.w_by_signature[signature].push_back(code);
    }
  }
  if (catalog.z.size() != 972 || catalog.w.size() != 7056 ||
      catalog.w_by_signature.size() != 28) {
    throw std::runtime_error("short-sequence catalog fingerprint failed");
  }
  return catalog;
}

std::array<std::array<int, 9>, 5> ExpandState(const State& state) {
  std::array<std::array<int, 9>, 5> result{};
  result[0] = Decode(state.z_code);
  for (int index = 0; index < 4; ++index) {
    result[index + 1] = Decode(state.w_code[index]);
    // C_1 and C_3 need sum +3i.  Negation preserves every PAF.
    if (index == 1 || index == 3) {
      for (int& phase : result[index + 1]) {
        phase = (phase + 2) & 3;
      }
    }
  }
  return result;
}

int QuotientCorrelation(
    const std::array<std::array<int, 9>, 5>& phases, int row_lag,
    int class_lag) {
  int total = 0;
  for (int row = 0; row < 9; ++row) {
    const int next_row = (row + row_lag) % 9;
    for (int left = 0; left < 5; ++left) {
      for (int right = 0; right < 5; ++right) {
        total += kTransition[class_lag][left][right] *
                 RealProduct(phases[left][row], phases[right][next_row]);
      }
    }
  }
  return total;
}

int RowAxisCorrelation(
    const std::array<std::array<int, 9>, 5>& phases, int row_lag) {
  int total = 0;
  for (int row = 0; row < 9; ++row) {
    const int next_row = (row + row_lag) % 9;
    total += RealProduct(phases[0][row], phases[0][next_row]);
    for (int part = 1; part < 5; ++part) {
      total +=
          9 * RealProduct(phases[part][row], phases[part][next_row]);
    }
  }
  return total;
}

int Energy(const State& state) {
  const auto phases = ExpandState(state);
  int energy = 0;

  // At row lag zero, signs identify C_0 with C_2 and C_1 with C_3.
  for (int class_lag = 0; class_lag < 2; ++class_lag) {
    const int residual = QuotientCorrelation(phases, 0, class_lag) + 1;
    energy += residual * residual;
  }
  for (int row_lag = 1; row_lag <= 4; ++row_lag) {
    if (RowAxisCorrelation(phases, row_lag) != -1) {
      throw std::runtime_error("constructor left the exact row-axis fiber");
    }
    for (int class_lag = 0; class_lag < 4; ++class_lag) {
      const int residual =
          QuotientCorrelation(phases, row_lag, class_lag) + 1;
      energy += residual * residual;
    }
  }
  return energy;
}

struct DefectStats {
  int pure_column_bad = 0;
  int mixed_bad = 0;
  int energy = 0;
  int max_absolute_residual = 0;
};

DefectStats MeasureDefects(const State& state) {
  const auto phases = ExpandState(state);
  DefectStats result;
  for (int class_lag = 0; class_lag < 2; ++class_lag) {
    const int residual = QuotientCorrelation(phases, 0, class_lag) + 1;
    result.pure_column_bad += residual != 0;
    result.energy += residual * residual;
    result.max_absolute_residual =
        std::max(result.max_absolute_residual, std::abs(residual));
  }
  for (int row_lag = 1; row_lag <= 4; ++row_lag) {
    for (int class_lag = 0; class_lag < 4; ++class_lag) {
      const int residual =
          QuotientCorrelation(phases, row_lag, class_lag) + 1;
      result.mixed_bad += residual != 0;
      result.energy += residual * residual;
      result.max_absolute_residual =
          std::max(result.max_absolute_residual, std::abs(residual));
    }
  }
  return result;
}

template <class Generator>
int RandomElement(const std::vector<int>& values, Generator& generator) {
  std::uniform_int_distribution<std::size_t> distribution(0,
                                                           values.size() - 1);
  return values[distribution(generator)];
}

template <class Generator>
State RandomState(const Catalog& catalog, Generator& generator) {
  State result;
  result.z_code = RandomElement(catalog.z, generator);
  for (;;) {
    Signature partial;
    for (int index = 0; index < 3; ++index) {
      result.w_code[index] = RandomElement(catalog.w, generator);
      partial =
          partial + catalog.signature_by_code[result.w_code[index]];
    }
    const auto found = catalog.w_by_signature.find(-partial);
    if (found != catalog.w_by_signature.end()) {
      result.w_code[3] = RandomElement(found->second, generator);
      return result;
    }
  }
}

template <class Generator>
bool Propose(const Catalog& catalog, const State& current, State* proposal,
             Generator& generator) {
  *proposal = current;
  std::uniform_int_distribution<int> kind_distribution(0, 4);
  const int kind = kind_distribution(generator);
  if (kind == 0) {
    proposal->z_code = RandomElement(catalog.z, generator);
    return proposal->z_code != current.z_code;
  }

  std::uniform_int_distribution<int> position_distribution(0, 3);
  if (kind <= 2) {
    const int position = position_distribution(generator);
    const Signature signature =
        catalog.signature_by_code[current.w_code[position]];
    const auto& bucket = catalog.w_by_signature.at(signature);
    proposal->w_code[position] = RandomElement(bucket, generator);
    return proposal->w_code[position] != current.w_code[position];
  }

  // Replace two W sequences while keeping the sum of all four real PAF
  // signatures exactly zero.
  int left = position_distribution(generator);
  int right = position_distribution(generator);
  while (right == left) {
    right = position_distribution(generator);
  }
  Signature fixed;
  for (int index = 0; index < 4; ++index) {
    if (index != left && index != right) {
      fixed = fixed + catalog.signature_by_code[current.w_code[index]];
    }
  }
  for (int attempt = 0; attempt < 24; ++attempt) {
    const int new_left = RandomElement(catalog.w, generator);
    const Signature required =
        -(fixed + catalog.signature_by_code[new_left]);
    const auto found = catalog.w_by_signature.find(required);
    if (found == catalog.w_by_signature.end()) {
      continue;
    }
    proposal->w_code[left] = new_left;
    proposal->w_code[right] = RandomElement(found->second, generator);
    return proposal->w_code != current.w_code;
  }
  return false;
}

State EncodePhaseTable(const int table[9][5]) {
  State result;
  std::array<int, 9> column{};
  for (int row = 0; row < 9; ++row) {
    column[row] = table[row][0];
  }
  result.z_code = Encode(column);
  for (int part = 1; part < 5; ++part) {
    for (int row = 0; row < 9; ++row) {
      column[row] = table[row][part];
      if (part == 2 || part == 4) {
        column[row] = (column[row] + 2) & 3;
      }
    }
    result.w_code[part - 1] = Encode(column);
  }
  return result;
}

State AxisWitness() {
  // Columns are (zero,C0,C1,C2,C3), transposed from the table in the notes.
  constexpr int table[9][5] = {
      {3, 3, 1, 3, 1}, {0, 0, 2, 3, 1}, {2, 0, 1, 3, 2},
      {2, 2, 0, 2, 0}, {0, 0, 3, 1, 2}, {1, 2, 0, 3, 1},
      {0, 3, 1, 2, 1}, {1, 3, 1, 0, 3}, {3, 2, 2, 0, 0}};
  return EncodePhaseTable(table);
}

State PilotBest() {
  // Retained from the bounded 60-second seed-1668 pilot.
  constexpr int table[9][5] = {
      {3, 0, 2, 1, 3}, {3, 3, 0, 1, 2}, {0, 1, 2, 3, 0},
      {1, 3, 2, 3, 1}, {0, 3, 1, 3, 1}, {1, 0, 1, 3, 2},
      {3, 3, 1, 0, 1}, {2, 2, 0, 2, 0}, {1, 2, 0, 3, 1}};
  return EncodePhaseTable(table);
}

void VerifyStrict(const State& state) {
  const auto phases = ExpandState(state);
  int a[9][37]{};
  int b[9][37]{};

  std::array<int, 37> class_of{};
  class_of.fill(-1);
  int value = 1;
  for (int exponent = 0; exponent < 36; ++exponent) {
    class_of[value] = exponent & 3;
    value = value * 2 % 37;
  }
  for (int row = 0; row < 9; ++row) {
    for (int column = 0; column < 37; ++column) {
      const int part = column == 0 ? 0 : class_of[column] + 1;
      const int phase = phases[part][row];
      // Invert u=(A+iB)/(1+i).
      a[row][column] = (phase == 0 || phase == 3) ? 1 : -1;
      b[row][column] = (phase == 0 || phase == 1) ? 1 : -1;
    }
  }

  for (int column = 0; column < 37; ++column) {
    int sum_a = 0;
    int sum_b = 0;
    for (int row = 0; row < 9; ++row) {
      sum_a += a[row][column];
      sum_b += b[row][column];
    }
    const int chi = column == 0 ? 0 : (class_of[column] % 2 == 0 ? 1 : -1);
    const int expected_a = column == 0 ? 1 : 3 * chi;
    const int expected_b = column == 0 ? 1 : -3 * chi;
    if (sum_a != expected_a || sum_b != expected_b) {
      throw std::runtime_error("strict fixed-compression verification failed");
    }
  }

  for (int row_lag = 0; row_lag < 9; ++row_lag) {
    for (int column_lag = 0; column_lag < 37; ++column_lag) {
      int correlation = 0;
      for (int row = 0; row < 9; ++row) {
        for (int column = 0; column < 37; ++column) {
          correlation +=
              a[row][column] *
                  a[(row + row_lag) % 9][(column + column_lag) % 37] +
              b[row][column] *
                  b[(row + row_lag) % 9][(column + column_lag) % 37];
        }
      }
      const int expected =
          row_lag == 0 && column_lag == 0 ? 666 : -2;
      if (correlation != expected) {
        throw std::runtime_error("strict full-correlation verification failed");
      }
    }
  }
}

void PrintState(const State& state) {
  const auto phases = ExpandState(state);
  std::cout << "phase table (0,C0,C1,C2,C3):\n";
  for (int row = 0; row < 9; ++row) {
    std::cout << '(';
    for (int part = 0; part < 5; ++part) {
      if (part != 0) {
        std::cout << ',';
      }
      std::cout << phases[part][row];
    }
    std::cout << ")\n";
  }
}

void PrintResiduals(const State& state) {
  const auto phases = ExpandState(state);
  std::cout << "pure-column residuals:";
  for (int class_lag = 0; class_lag < 2; ++class_lag) {
    std::cout << ' ' << QuotientCorrelation(phases, 0, class_lag) + 1;
  }
  std::cout << "\nmixed residuals by row lag:\n";
  for (int row_lag = 1; row_lag <= 4; ++row_lag) {
    std::cout << row_lag << ':';
    for (int class_lag = 0; class_lag < 4; ++class_lag) {
      std::cout << ' '
                << QuotientCorrelation(phases, row_lag, class_lag) + 1;
    }
    std::cout << '\n';
  }
}

struct Options {
  double seconds = 60.0;
  std::uint64_t seed = 668;
  int epoch = 100000;
  double temperature_start = 256.0;
  double temperature_end = 0.5;
};

Options ParseOptions(int argc, char** argv) {
  Options options;
  for (int index = 1; index < argc; ++index) {
    const std::string argument = argv[index];
    auto require_value = [&]() -> std::string {
      if (++index >= argc) {
        throw std::invalid_argument("missing value after " + argument);
      }
      return argv[index];
    };
    if (argument == "--seconds") {
      options.seconds = std::stod(require_value());
    } else if (argument == "--seed") {
      options.seed = std::stoull(require_value());
    } else if (argument == "--epoch") {
      options.epoch = std::stoi(require_value());
    } else if (argument == "--temperature-start") {
      options.temperature_start = std::stod(require_value());
    } else if (argument == "--temperature-end") {
      options.temperature_end = std::stod(require_value());
    } else {
      throw std::invalid_argument("unknown argument: " + argument);
    }
  }
  if (!(options.seconds > 0.0) || options.epoch <= 0 ||
      !(options.temperature_start > 0.0) ||
      !(options.temperature_end > 0.0)) {
    throw std::invalid_argument("all search parameters must be positive");
  }
  return options;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Options options = ParseOptions(argc, argv);
    const Catalog catalog = BuildCatalog();
    const State axis = AxisWitness();
    if (Energy(axis) != 1536) {
      throw std::runtime_error("axis-witness quotient fingerprint failed");
    }
    const State pilot = PilotBest();
    if (Energy(pilot) != 112) {
      throw std::runtime_error("pilot-best quotient fingerprint failed");
    }

    std::mt19937_64 generator(options.seed);
    std::uniform_real_distribution<double> unit(0.0, 1.0);
    State best = pilot;
    int best_energy = Energy(best);
    std::uint64_t proposals = 0;
    std::uint64_t accepted = 0;
    std::uint64_t restarts = 0;

    const auto start = std::chrono::steady_clock::now();
    const auto deadline =
        start + std::chrono::duration<double>(options.seconds);
    while (std::chrono::steady_clock::now() < deadline && best_energy != 0) {
      State current = restarts == 0 ? pilot : RandomState(catalog, generator);
      int current_energy = Energy(current);
      for (int step = 0; step < options.epoch; ++step) {
        if ((step & 1023) == 0 &&
            std::chrono::steady_clock::now() >= deadline) {
          break;
        }
        State proposal;
        if (!Propose(catalog, current, &proposal, generator)) {
          continue;
        }
        ++proposals;
        const int proposal_energy = Energy(proposal);
        const double fraction =
            static_cast<double>(step) / std::max(1, options.epoch - 1);
        const double temperature =
            options.temperature_start *
            std::pow(options.temperature_end / options.temperature_start,
                     fraction);
        const int delta = proposal_energy - current_energy;
        if (delta <= 0 ||
            unit(generator) < std::exp(-static_cast<double>(delta) /
                                      temperature)) {
          current = proposal;
          current_energy = proposal_energy;
          ++accepted;
        }
        if (current_energy < best_energy) {
          best = current;
          best_energy = current_energy;
          std::cout << "best_energy=" << best_energy
                    << " proposals=" << proposals
                    << " restarts=" << restarts << '\n';
          std::cout.flush();
        }
        if (best_energy == 0) {
          break;
        }
      }
      ++restarts;
    }

    const double elapsed =
        std::chrono::duration<double>(std::chrono::steady_clock::now() - start)
            .count();
    const DefectStats defects = MeasureDefects(best);
    if (defects.energy != best_energy) {
      throw std::runtime_error("final quotient-energy replay failed");
    }
    const int quotient_bad = defects.pure_column_bad + defects.mixed_bad;
    std::cout << std::fixed << std::setprecision(3)
              << "RESULT energy=" << best_energy
              << " full_orbit_energy=" << 9 * best_energy
              << " quotient_bad=" << quotient_bad << "/18"
              << " remaining_independent_bad=" << 9 * quotient_bad << "/162"
              << " full_independent_bad=" << 9 * quotient_bad << "/166"
              << " pure_column_bad=" << defects.pure_column_bad << "/2"
              << " mixed_bad=" << defects.mixed_bad << "/16"
              << " max_abs_residual=" << defects.max_absolute_residual
              << " proposals=" << proposals << " accepted=" << accepted
              << " restarts=" << restarts << " seconds=" << elapsed << '\n';
    PrintState(best);
    PrintResiduals(best);
    if (best_energy == 0) {
      VerifyStrict(best);
      std::cout << "EXACT LP(333): all 332 oriented correlations verified\n";
      return 0;
    }
    std::cout << "NON-CANDIDATE: zero quotient energy was not reached\n";
    return 2;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
