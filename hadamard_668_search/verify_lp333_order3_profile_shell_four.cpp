// Deterministic exhaustive verifier for the LP(333) order-three profile shell
// (n_9,n_3,n_0)=(4,6,14).
//
// The six norm-three letters are first enumerated in legal opposite-pair
// quartets.  Every norm-nine coefficient is divisible by three, so all
// high-high correlation products vanish modulo nine.  After division by
// three, the remaining modulo-three correlation is affine in the four high
// letters.  Its two Eisenstein coordinates at each of the six reversal-
// independent lags have a useful flag/phase split:
//
//   * the coordinate sum depends only on the high support in that quartet;
//   * high/medium cross terms have coordinate sum zero; and
//   * if a quartet contains a high letter, its three phases span the
//     remaining one-dimensional coordinate.
//
// Thus high supports are joined by a six-layer weight-four DP and phases
// are solved independently inside occupied quartets.  Every modulo-nine
// survivor is replayed using all 37 exact physical correlations.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr int P = 37;
constexpr int CLASS_COUNT = 12;
constexpr int POSITION_COUNT = 24;
constexpr int ZERO_ID = 5;
constexpr std::array<int, 6> MEDIUM_IDS = {1, 2, 4, 6, 7, 8};
constexpr std::array<int, 3> HIGH_IDS = {0, 3, 9};
constexpr std::array<std::array<int, 3>, 10> PROFILES = {{
    {{0, 0, 3}},
    {{0, 1, 2}},
    {{0, 2, 1}},
    {{0, 3, 0}},
    {{1, 0, 2}},
    {{1, 1, 1}},
    {{1, 2, 0}},
    {{2, 0, 1}},
    {{2, 1, 0}},
    {{3, 0, 0}},
}};

using Target = std::array<int, 4>;

constexpr std::array<Target, 22> TARGETS = {{
    {{-3, -3, -4, -2}},
    {{-3, -3, -2, 2}},
    {{-3, 0, -3, -3}},
    {{-3, 0, 0, 3}},
    {{-1, -2, -5, -1}},
    {{-1, -2, -4, 1}},
    {{0, 3, -4, -2}},
    {{0, 3, -2, 2}},
    {{1, -1, 2, -2}},
    {{1, -1, 4, 2}},
    {{1, 2, -5, -1}},
    {{1, 2, -4, 1}},
    {{2, -2, -4, -2}},
    {{2, -2, -2, 2}},
    {{2, 1, 2, -2}},
    {{2, 1, 4, 2}},
    {{3, 0, 0, -3}},
    {{3, 0, 3, 3}},
    {{4, -1, 0, 0}},
    {{4, 2, -4, -2}},
    {{4, 2, -2, 2}},
    {{5, 1, 0, 0}},
}};

struct E {
  int a = 0;
  int b = 0;
};

E operator+(E x, E y) { return {x.a + y.a, x.b + y.b}; }
E operator-(E x, E y) { return {x.a - y.a, x.b - y.b}; }
E operator*(int n, E x) { return {n * x.a, n * x.b}; }
bool operator==(E x, E y) { return x.a == y.a && x.b == y.b; }
bool operator!=(E x, E y) { return !(x == y); }

E conjugate(E x) { return {x.a - x.b, -x.b}; }

E multiply(E x, E y) {
  return {x.a * y.a - x.b * y.b,
          x.a * y.b + x.b * y.a - x.b * y.b};
}

int mod3(int x) {
  x %= 3;
  return x < 0 ? x + 3 : x;
}

E raw_profile(int id) {
  const auto &p = PROFILES.at(static_cast<std::size_t>(id));
  return {p[0] - p[2], p[1] - p[2]};
}

int profile_norm(int id) {
  E z = raw_profile(id);
  return z.a * z.a - z.a * z.b + z.b * z.b;
}

E coefficient(int position, int id) {
  int channel = position / CLASS_COUNT;
  int class_index = position % CLASS_COUNT;
  int epsilon = class_index % 2 == 0 ? 1 : -1;
  int factor = channel == 0 ? -epsilon : epsilon;
  return factor * raw_profile(id);
}

E pair_signature(int left_id, int right_id) {
  E value = conjugate(raw_profile(left_id)) + raw_profile(right_id);
  return {mod3(value.a), mod3(value.b)};
}

int position(int quartet, int slot) {
  switch (slot) {
    case 0:
      return quartet;
    case 1:
      return quartet + 6;
    case 2:
      return 12 + quartet;
    case 3:
      return 12 + quartet + 6;
    default:
      throw std::runtime_error("bad local slot");
  }
}

std::array<std::array<int, 3>, CLASS_COUNT> classes;
std::array<int, P> class_of;

void initialize_classes() {
  int power = 1;
  constexpr std::array<int, 3> subgroup = {1, 26, 10};
  class_of.fill(-1);
  for (int index = 0; index < CLASS_COUNT; ++index) {
    for (int k = 0; k < 3; ++k) {
      int value = power * subgroup[k] % P;
      classes[index][k] = value;
      if (class_of[value] != -1) {
        throw std::runtime_error("cyclotomic classes overlap");
      }
      class_of[value] = index;
    }
    power = power * 2 % P;
  }
  for (int value = 1; value < P; ++value) {
    if (class_of[value] < 0) {
      throw std::runtime_error("cyclotomic classes do not cover F_37^*");
    }
  }
}

using Assignment = std::array<std::uint8_t, POSITION_COUNT>;
using Six = std::array<E, 6>;

Six direct_six(const Assignment &assignment) {
  std::array<std::array<E, P>, 2> words{};
  words[0][0] = {-1, 0};
  words[1][0] = {2, 0};
  for (int channel = 0; channel < 2; ++channel) {
    for (int column = 1; column < P; ++column) {
      int cls = class_of[column];
      words[channel][column] =
          coefficient(channel * CLASS_COUNT + cls,
                      assignment[channel * CLASS_COUNT + cls]);
    }
  }
  Six result{};
  for (int part = 0; part < 6; ++part) {
    int lag = classes[part][0];
    E value{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int column = 0; column < P; ++column) {
        value = value +
                multiply(words[channel][(column + lag) % P],
                         conjugate(words[channel][column]));
      }
    }
    result[part] = value;
  }
  return result;
}

std::array<E, P> direct_physical(const Assignment &assignment) {
  std::array<std::array<E, P>, 2> words{};
  words[0][0] = {-1, 0};
  words[1][0] = {2, 0};
  for (int channel = 0; channel < 2; ++channel) {
    for (int column = 1; column < P; ++column) {
      int cls = class_of[column];
      words[channel][column] =
          coefficient(channel * CLASS_COUNT + cls,
                      assignment[channel * CLASS_COUNT + cls]);
    }
  }
  std::array<E, P> result{};
  for (int lag = 0; lag < P; ++lag) {
    E value{};
    for (int channel = 0; channel < 2; ++channel) {
      for (int column = 0; column < P; ++column) {
        value = value +
                multiply(words[channel][(column + lag) % P],
                         conjugate(words[channel][column]));
      }
    }
    if (lag == 0) {
      value.a -= 167;
    }
    result[lag] = value;
  }
  return result;
}

Assignment zero_assignment() {
  Assignment result{};
  result.fill(ZERO_ID);
  return result;
}

constexpr std::array<int, 7> POW3 = {1, 3, 9, 27, 81, 243, 729};

struct Sig {
  std::uint16_t a = 0;
  std::uint16_t b = 0;
};

std::array<std::array<std::uint8_t, 6>, 729> trits;
std::vector<std::uint16_t> add_code;
std::array<std::uint16_t, 729> negate_code;

void initialize_signature_arithmetic() {
  for (int code = 0; code < 729; ++code) {
    int value = code;
    for (int index = 0; index < 6; ++index) {
      trits[code][index] = static_cast<std::uint8_t>(value % 3);
      value /= 3;
    }
    int negative = 0;
    for (int index = 0; index < 6; ++index) {
      negative += mod3(-trits[code][index]) * POW3[index];
    }
    negate_code[code] = static_cast<std::uint16_t>(negative);
  }
  add_code.resize(729 * 729);
  for (int left = 0; left < 729; ++left) {
    for (int right = 0; right < 729; ++right) {
      int value = 0;
      for (int index = 0; index < 6; ++index) {
        value +=
            ((trits[left][index] + trits[right][index]) % 3) * POW3[index];
      }
      add_code[left * 729 + right] = static_cast<std::uint16_t>(value);
    }
  }
}

Sig sig_add(Sig x, Sig y) {
  return {add_code[x.a * 729 + y.a], add_code[x.b * 729 + y.b]};
}

Sig sig_negate(Sig x) { return {negate_code[x.a], negate_code[x.b]}; }

Sig sig_subtract(Sig x, Sig y) { return sig_add(x, sig_negate(y)); }

std::pair<int, int> sig_part(Sig x, int part) {
  return {trits[x.a][part], trits[x.b][part]};
}

Sig divided_signature(const Six &values, const std::string &label) {
  int a_code = 0;
  int b_code = 0;
  for (int index = 0; index < 6; ++index) {
    if (values[index].a % 3 || values[index].b % 3) {
      throw std::runtime_error(label + " is not coefficientwise divisible by 3");
    }
    a_code += mod3(values[index].a / 3) * POW3[index];
    b_code += mod3(values[index].b / 3) * POW3[index];
  }
  return {static_cast<std::uint16_t>(a_code),
          static_cast<std::uint16_t>(b_code)};
}

Six six_subtract(Six x, const Six &y) {
  for (int index = 0; index < 6; ++index) {
    x[index] = x[index] - y[index];
  }
  return x;
}

int medium_index(int id) {
  for (int index = 0; index < 6; ++index) {
    if (MEDIUM_IDS[index] == id) {
      return index;
    }
  }
  throw std::runtime_error("not a medium profile ID");
}

std::array<std::array<Six, 6>, POSITION_COUNT> single_medium_exact;
std::array<std::array<Sig, 3>, POSITION_COUNT> single_high_sig;
std::array<std::array<std::array<std::array<Sig, 6>, POSITION_COUNT>, 6>,
           POSITION_COUNT>
    cross_mm;
std::array<std::array<std::array<Sig, 6>, POSITION_COUNT>, POSITION_COUNT>
    cross_hm;
std::array<std::array<Sig, 3>, POSITION_COUNT> high_phase_delta;
std::array<int, POSITION_COUNT> high_flag;

void initialize_variable_tables() {
  for (int pos = 0; pos < POSITION_COUNT; ++pos) {
    for (int mi = 0; mi < 6; ++mi) {
      Assignment assignment = zero_assignment();
      assignment[pos] = MEDIUM_IDS[mi];
      single_medium_exact[pos][mi] = direct_six(assignment);
    }
    for (int hi = 0; hi < 3; ++hi) {
      Assignment assignment = zero_assignment();
      assignment[pos] = HIGH_IDS[hi];
      single_high_sig[pos][hi] =
          divided_signature(direct_six(assignment), "one-high table");
    }
    high_phase_delta[pos][0] =
        sig_subtract(single_high_sig[pos][0], single_high_sig[pos][2]);
    high_phase_delta[pos][1] =
        sig_subtract(single_high_sig[pos][1], single_high_sig[pos][2]);
    high_phase_delta[pos][2] = {};

    int lag = pos % 6;
    auto canonical = sig_part(single_high_sig[pos][2], lag);
    high_flag[pos] = (canonical.first + canonical.second) % 3;
    if (high_flag[pos] == 0) {
      throw std::runtime_error("a high support has zero flag");
    }
    for (int part = 0; part < 6; ++part) {
      for (int hi = 0; hi < 3; ++hi) {
        auto value = sig_part(single_high_sig[pos][hi], part);
        if (part != lag && value != std::pair<int, int>{0, 0}) {
          throw std::runtime_error("a high phase affected a remote lag");
        }
        if (part == lag &&
            (value.first + value.second) % 3 != high_flag[pos]) {
          throw std::runtime_error("the high flag depends on phase");
        }
        auto delta = sig_part(high_phase_delta[pos][hi], part);
        if ((delta.first + delta.second) % 3 != 0) {
          throw std::runtime_error("a high phase changed the support flag");
        }
      }
    }
  }

  for (int left = 0; left < POSITION_COUNT; ++left) {
    for (int li = 0; li < 6; ++li) {
      for (int right = 0; right < POSITION_COUNT; ++right) {
        for (int ri = 0; ri < 6; ++ri) {
          if (left / 12 != right / 12 || left == right) {
            cross_mm[left][li][right][ri] = {};
            continue;
          }
          Assignment assignment = zero_assignment();
          assignment[left] = MEDIUM_IDS[li];
          assignment[right] = MEDIUM_IDS[ri];
          Six cross = six_subtract(
              six_subtract(direct_six(assignment),
                           single_medium_exact[left][li]),
              single_medium_exact[right][ri]);
          cross_mm[left][li][right][ri] =
              divided_signature(cross, "medium-medium cross term");
        }
      }
    }
  }

  for (int high_pos = 0; high_pos < POSITION_COUNT; ++high_pos) {
    for (int medium_pos = 0; medium_pos < POSITION_COUNT; ++medium_pos) {
      for (int mi = 0; mi < 6; ++mi) {
        if (high_pos / 12 != medium_pos / 12 ||
            high_pos == medium_pos) {
          cross_hm[high_pos][medium_pos][mi] = {};
          continue;
        }
        Sig canonical{};
        for (int hi = 0; hi < 3; ++hi) {
          Assignment assignment = zero_assignment();
          assignment[high_pos] = HIGH_IDS[hi];
          assignment[medium_pos] = MEDIUM_IDS[mi];
          Six cross =
              six_subtract(
                  six_subtract(direct_six(assignment),
                               [&]() {
                                 Assignment high_only = zero_assignment();
                                 high_only[high_pos] = HIGH_IDS[hi];
                                 return direct_six(high_only);
                               }()),
                  single_medium_exact[medium_pos][mi]);
          Sig value = divided_signature(cross, "high-medium cross term");
          if (hi == 0) {
            canonical = value;
          } else if (value.a != canonical.a || value.b != canonical.b) {
            throw std::runtime_error(
                "a high-medium cross term depends on high phase modulo 9");
          }
        }
        cross_hm[high_pos][medium_pos][mi] = canonical;
        for (int part = 0; part < 6; ++part) {
          auto value = sig_part(canonical, part);
          if ((value.first + value.second) % 3 != 0) {
            throw std::runtime_error(
                "a high-medium cross term changed a support flag");
          }
        }
      }
    }
  }
}

struct Variable {
  std::uint8_t position = 0;
  std::uint8_t medium_index = 0;
};

struct State {
  std::array<std::uint8_t, 4> ids{};
  std::uint8_t medium_count = 0;
  std::uint8_t medium_mask = 0;
  std::array<Variable, 4> variables{};
  Target aggregate{};
  Sig self{};
  std::array<Sig, POSITION_COUNT> hm{};
};

std::array<std::array<std::vector<State>, 5>, 6> states;

void initialize_states() {
  constexpr std::array<int, 7> alphabet = {ZERO_ID, 1, 2, 4, 6, 7, 8};
  std::array<std::uint64_t, 5> local_counts{};
  for (int quartet = 0; quartet < 6; ++quartet) {
    for (int x0 : alphabet)
      for (int x1 : alphabet)
        for (int x2 : alphabet)
          for (int x3 : alphabet) {
            std::array<int, 4> q = {x0, x1, x2, x3};
            if (pair_signature(q[0], q[1]) !=
                pair_signature(q[2], q[3])) {
              continue;
            }
            State state;
            int variable_count = 0;
            Assignment assignment = zero_assignment();
            for (int slot = 0; slot < 4; ++slot) {
              state.ids[slot] = static_cast<std::uint8_t>(q[slot]);
              if (q[slot] == ZERO_ID) {
                continue;
              }
              int pos = position(quartet, slot);
              int mi = medium_index(q[slot]);
              state.medium_mask |= static_cast<std::uint8_t>(1U << slot);
              state.variables[variable_count++] = {
                  static_cast<std::uint8_t>(pos),
                  static_cast<std::uint8_t>(mi),
              };
              assignment[pos] = static_cast<std::uint8_t>(q[slot]);
              E value = coefficient(pos, q[slot]);
              int channel = pos / 12;
              state.aggregate[2 * channel] += value.a;
              state.aggregate[2 * channel + 1] += value.b;
            }
            state.medium_count = static_cast<std::uint8_t>(variable_count);
            state.self =
                divided_signature(direct_six(assignment), "local medium state");
            for (int high_pos = 0; high_pos < POSITION_COUNT; ++high_pos) {
              Sig value{};
              for (int index = 0; index < variable_count; ++index) {
                const Variable &variable = state.variables[index];
                value = sig_add(
                    value,
                    cross_hm[high_pos][variable.position]
                            [variable.medium_index]);
              }
              state.hm[high_pos] = value;
            }
            states[quartet][variable_count].push_back(state);
            if (quartet == 0) {
              ++local_counts[variable_count];
            }
          }
  }
  if (local_counts !=
      std::array<std::uint64_t, 5>{1, 0, 108, 216, 486}) {
    throw std::runtime_error("the legal medium-only quartet census changed");
  }
  for (int quartet = 0; quartet < 6; ++quartet) {
    for (int count : {0, 2, 3, 4}) {
      if (states[quartet][count].size() != local_counts[count]) {
        throw std::runtime_error("quartet state counts depend on position");
      }
    }
  }
}

struct Counters {
  std::uint64_t medium_frames = 0;
  std::uint64_t support_leaves = 0;
  std::uint64_t support_empty_gate = 0;
  std::uint64_t phase_solutions = 0;
  std::uint64_t modulo_nine_survivors = 0;
  std::array<std::uint64_t, 22> target_survivors{};
  std::map<int, std::uint64_t> bad_class_histogram;
  std::uint64_t exact_profiles = 0;
};

Counters counters;

int target_index(const Target &value) {
  for (int index = 0; index < static_cast<int>(TARGETS.size()); ++index) {
    if (value == TARGETS[index]) {
      return index;
    }
  }
  return -1;
}

struct LocalSupport {
  std::uint8_t mask = 0;
  std::uint8_t count = 0;
};

struct LocalPhase {
  std::array<std::uint8_t, 4> high_indices{};
  Target aggregate{};
};

Sig cross_between_states(const State &left, const State &right) {
  Sig result{};
  for (int i = 0; i < left.medium_count; ++i) {
    for (int j = 0; j < right.medium_count; ++j) {
      const Variable &x = left.variables[i];
      const Variable &y = right.variables[j];
      result =
          sig_add(result,
                  cross_mm[x.position][x.medium_index][y.position]
                          [y.medium_index]);
    }
  }
  return result;
}

struct FrameProcessor {
  std::array<const State *, 3> active{};
  int active_count = 0;
  Sig baseline{};
  Target medium_aggregate{};
  Assignment medium_assignment = zero_assignment();
  std::array<std::uint8_t, 6> medium_masks{};
  std::array<std::vector<LocalSupport>, 6> options;
  std::array<std::uint8_t, 6> chosen_masks{};
  std::array<Sig, POSITION_COUNT> support_increment{};
  std::array<bool, POSITION_COUNT> increment_ready{};

  explicit FrameProcessor(const std::vector<const State *> &input) {
    active_count = static_cast<int>(input.size());
    if (active_count < 2 || active_count > 3) {
      throw std::runtime_error("unexpected number of active medium quartets");
    }
    for (int index = 0; index < active_count; ++index) {
      active[index] = input[index];
      baseline = sig_add(baseline, input[index]->self);
      for (int coordinate = 0; coordinate < 4; ++coordinate) {
        medium_aggregate[coordinate] += input[index]->aggregate[coordinate];
      }
      int quartet = input[index]->variables[0].position % 6;
      medium_masks[quartet] = input[index]->medium_mask;
      for (int v = 0; v < input[index]->medium_count; ++v) {
        const Variable &variable = input[index]->variables[v];
        medium_assignment[variable.position] =
            static_cast<std::uint8_t>(MEDIUM_IDS[variable.medium_index]);
      }
    }
    for (int i = 0; i < active_count; ++i) {
      for (int j = i + 1; j < active_count; ++j) {
        baseline =
            sig_add(baseline, cross_between_states(*active[i], *active[j]));
      }
    }
    for (int quartet = 0; quartet < 6; ++quartet) {
      int available = (~medium_masks[quartet]) & 15;
      auto base = sig_part(baseline, quartet);
      int base_flag = (base.first + base.second) % 3;
      for (int subset = available;; subset = (subset - 1) & available) {
        int flag = base_flag;
        int count = 0;
        for (int slot = 0; slot < 4; ++slot) {
          if (subset >> slot & 1) {
            ++count;
            flag += high_flag[position(quartet, slot)];
          }
        }
        if (flag % 3 == 0 && count <= 4) {
          options[quartet].push_back(
              {static_cast<std::uint8_t>(subset),
               static_cast<std::uint8_t>(count)});
        }
        if (subset == 0) {
          break;
        }
      }
    }
  }

  Sig increment(int high_pos) {
    if (!increment_ready[high_pos]) {
      Sig value = single_high_sig[high_pos][2];
      for (int index = 0; index < active_count; ++index) {
        value = sig_add(value, active[index]->hm[high_pos]);
      }
      support_increment[high_pos] = value;
      increment_ready[high_pos] = true;
    }
    return support_increment[high_pos];
  }

  void replay(const std::array<std::uint8_t, POSITION_COUNT> &high_choice,
              const Target &aggregate) {
    int target = target_index(aggregate);
    if (target < 0) {
      return;
    }
    ++counters.modulo_nine_survivors;
    ++counters.target_survivors[target];
    Assignment assignment = medium_assignment;
    for (int pos = 0; pos < POSITION_COUNT; ++pos) {
      if (high_choice[pos] < 3) {
        assignment[pos] =
            static_cast<std::uint8_t>(HIGH_IDS[high_choice[pos]]);
      }
    }
    auto physical = direct_physical(assignment);
    if (physical[0] != E{0, 0}) {
      throw std::runtime_error("a shell assignment has nonzero origin D");
    }
    int bad_classes = 0;
    for (int part = 0; part < CLASS_COUNT; ++part) {
      E representative = physical[classes[part][0]];
      for (int value : classes[part]) {
        if (physical[value] != representative) {
          throw std::runtime_error("physical replay lost H-invariance");
        }
      }
      E expected =
          part < 6 ? representative
                   : conjugate(physical[classes[part - 6][0]]);
      if (representative != expected) {
        throw std::runtime_error("physical replay lost reversal symmetry");
      }
      if (representative.a % 9 || representative.b % 9) {
        throw std::runtime_error("an affine survivor failed modulo nine");
      }
      bad_classes += representative != E{0, 0};
    }
    ++counters.bad_class_histogram[bad_classes];
    if (bad_classes == 0) {
      ++counters.exact_profiles;
      std::cout << "EXACT";
      for (int value : assignment) {
        std::cout << ' ' << value;
      }
      std::cout << '\n';
    }
  }

  void combine_phases(
      int occupied_index, const std::vector<int> &occupied,
      const std::array<std::vector<LocalPhase>, 6> &phase_options,
      Target aggregate,
      std::array<std::uint8_t, POSITION_COUNT> &high_choice) {
    if (occupied_index == static_cast<int>(occupied.size())) {
      ++counters.phase_solutions;
      replay(high_choice, aggregate);
      return;
    }
    int quartet = occupied[occupied_index];
    for (const LocalPhase &phase : phase_options[quartet]) {
      Target next = aggregate;
      for (int coordinate = 0; coordinate < 4; ++coordinate) {
        next[coordinate] += phase.aggregate[coordinate];
      }
      int cursor = 0;
      for (int slot = 0; slot < 4; ++slot) {
        if (chosen_masks[quartet] >> slot & 1) {
          high_choice[position(quartet, slot)] =
              phase.high_indices[cursor++];
        }
      }
      combine_phases(occupied_index + 1, occupied, phase_options, next,
                     high_choice);
      for (int slot = 0; slot < 4; ++slot) {
        if (chosen_masks[quartet] >> slot & 1) {
          high_choice[position(quartet, slot)] = 3;
        }
      }
    }
  }

  void support_leaf() {
    ++counters.support_leaves;
    Sig value = baseline;
    std::vector<int> occupied;
    for (int quartet = 0; quartet < 6; ++quartet) {
      if (chosen_masks[quartet]) {
        occupied.push_back(quartet);
      }
      for (int slot = 0; slot < 4; ++slot) {
        if (chosen_masks[quartet] >> slot & 1) {
          value = sig_add(value, increment(position(quartet, slot)));
        }
      }
    }
    for (int quartet = 0; quartet < 6; ++quartet) {
      if (!chosen_masks[quartet] &&
          sig_part(value, quartet) != std::pair<int, int>{0, 0}) {
        return;
      }
    }
    ++counters.support_empty_gate;

    std::array<std::vector<LocalPhase>, 6> phase_options;
    for (int quartet : occupied) {
      std::array<int, 4> slots{};
      int count = 0;
      for (int slot = 0; slot < 4; ++slot) {
        if (chosen_masks[quartet] >> slot & 1) {
          slots[count++] = slot;
        }
      }
      int combinations = 1;
      for (int index = 0; index < count; ++index) {
        combinations *= 3;
      }
      for (int code = 0; code < combinations; ++code) {
        int work = code;
        Sig candidate = value;
        LocalPhase phase;
        for (int index = 0; index < count; ++index) {
          int hi = work % 3;
          work /= 3;
          int pos = position(quartet, slots[index]);
          phase.high_indices[index] = static_cast<std::uint8_t>(hi);
          candidate = sig_add(candidate, high_phase_delta[pos][hi]);
          E coefficient_value = coefficient(pos, HIGH_IDS[hi]);
          int channel = pos / 12;
          phase.aggregate[2 * channel] += coefficient_value.a;
          phase.aggregate[2 * channel + 1] += coefficient_value.b;
        }
        if (sig_part(candidate, quartet) ==
            std::pair<int, int>{0, 0}) {
          phase_options[quartet].push_back(phase);
        }
      }
      int expected = 1;
      for (int index = 1; index < count; ++index) {
        expected *= 3;
      }
      if (static_cast<int>(phase_options[quartet].size()) != expected) {
        throw std::runtime_error(
            "an occupied quartet lost the one-dimensional phase solve");
      }
    }
    std::array<std::uint8_t, POSITION_COUNT> high_choice{};
    high_choice.fill(3);
    combine_phases(0, occupied, phase_options, medium_aggregate, high_choice);
  }

  void combine_supports(int quartet, int used) {
    if (quartet == 6) {
      if (used == 4) {
        support_leaf();
      }
      return;
    }
    for (const LocalSupport &option : options[quartet]) {
      int next = used + option.count;
      if (next > 4) {
        continue;
      }
      chosen_masks[quartet] = option.mask;
      combine_supports(quartet + 1, next);
    }
  }

  void run() {
    ++counters.medium_frames;
    combine_supports(0, 0);
  }
};

void process(const std::vector<const State *> &active) {
  FrameProcessor frame(active);
  frame.run();
  if (counters.medium_frames % 1000000 == 0) {
    std::cerr << "frames=" << counters.medium_frames
              << " supports=" << counters.support_leaves
              << " mod9=" << counters.modulo_nine_survivors << '\n';
  }
}

void enumerate_frames() {
  // 2+2+2
  for (int first = 0; first < 6; ++first) {
    for (int second = first + 1; second < 6; ++second) {
      for (int third = second + 1; third < 6; ++third) {
        for (const State &x : states[first][2])
          for (const State &y : states[second][2])
            for (const State &z : states[third][2])
              process({&x, &y, &z});
      }
    }
  }
  // 3+3
  for (int first = 0; first < 6; ++first) {
    for (int second = first + 1; second < 6; ++second) {
      for (const State &x : states[first][3])
        for (const State &y : states[second][3]) process({&x, &y});
    }
  }
  // 4+2, with the roles ordered.
  for (int four = 0; four < 6; ++four) {
    for (int two = 0; two < 6; ++two) {
      if (four == two) {
        continue;
      }
      for (const State &x : states[four][4])
        for (const State &y : states[two][2]) process({&x, &y});
    }
  }
}

void audit_alphabet() {
  std::array<int, 3> counts{};
  for (int id = 0; id < 10; ++id) {
    int norm = profile_norm(id);
    if (norm == 0)
      ++counts[0];
    else if (norm == 3)
      ++counts[1];
    else if (norm == 9)
      ++counts[2];
    else
      throw std::runtime_error("unexpected profile norm");
  }
  if (counts != std::array<int, 3>{1, 6, 3}) {
    throw std::runtime_error("profile norm alphabet changed");
  }
  std::set<Target> target_set(TARGETS.begin(), TARGETS.end());
  if (target_set.size() != TARGETS.size()) {
    throw std::runtime_error("target catalog contains a duplicate");
  }
  for (int left : {ZERO_ID, HIGH_IDS[0], HIGH_IDS[1], HIGH_IDS[2]}) {
    for (int right : {ZERO_ID, HIGH_IDS[0], HIGH_IDS[1], HIGH_IDS[2]}) {
      if (pair_signature(left, right) != E{0, 0}) {
        throw std::runtime_error(
            "zero/high letters are not pair-signature inert");
      }
    }
  }
  for (int left : HIGH_IDS) {
    for (int right : HIGH_IDS) {
      E product = multiply(raw_profile(left), conjugate(raw_profile(right)));
      if (product.a % 9 || product.b % 9) {
        throw std::runtime_error("a high-high product survived modulo 9");
      }
    }
  }
}

}  // namespace

int main() {
  try {
    initialize_classes();
    initialize_signature_arithmetic();
    audit_alphabet();
    initialize_variable_tables();
    initialize_states();
    enumerate_frames();

    if (counters.medium_frames != 27468720ULL) {
      throw std::runtime_error("the global medium-frame census changed");
    }
    if (counters.support_leaves != 115033608ULL ||
        counters.support_empty_gate != 6835368ULL ||
        counters.phase_solutions != 12835512ULL ||
        counters.modulo_nine_survivors != 345984ULL) {
      throw std::runtime_error("the affine shell-four census changed");
    }
    constexpr std::array<std::uint64_t, 22> expected_target_survivors = {
        15162, 15162, 13518, 13518, 14970, 14970, 15162, 15162,
        19818, 19818, 14970, 14970, 15147, 15147, 19818, 19818,
        14358, 14358, 14922, 15147, 15147, 14922,
    };
    if (counters.target_survivors != expected_target_survivors) {
      throw std::runtime_error("the target-resolved shell-four census changed");
    }
    const std::map<int, std::uint64_t> expected_bad_histogram = {
        {4, 204},
        {6, 1860},
        {8, 16884},
        {10, 96192},
        {12, 230844},
    };
    if (counters.bad_class_histogram != expected_bad_histogram) {
      throw std::runtime_error("the exact shell-four failure census changed");
    }
    if (counters.exact_profiles != 0) {
      throw std::runtime_error("the excluded shell gained an exact profile");
    }
    std::cout << "medium_support_masks=4740\n";
    std::cout << "medium_frames=" << counters.medium_frames << '\n';
    std::cout << "support_leaves=" << counters.support_leaves << '\n';
    std::cout << "support_empty_gate=" << counters.support_empty_gate << '\n';
    std::cout << "phase_solutions=" << counters.phase_solutions << '\n';
    std::cout << "modulo_nine_survivors="
              << counters.modulo_nine_survivors << '\n';
    for (int index = 0; index < 22; ++index) {
      std::cout << "target[" << index
                << "]=" << counters.target_survivors[index] << '\n';
    }
    for (const auto &[bad, count] : counters.bad_class_histogram) {
      std::cout << "bad_classes[" << bad << "]=" << count << '\n';
    }
    std::cout << "exact_profiles=" << counters.exact_profiles << '\n';
    std::cout << "memory_model=streaming_constant_state\n";
    std::cout << "PASS: exhaustive shell-four affine sieve and exact replay\n";
    return counters.exact_profiles == 0 ? 0 : 2;
  } catch (const std::exception &error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
