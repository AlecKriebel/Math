#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Word = std::uint64_t;

constexpr int P = 37;
constexpr int N = 9;
constexpr int RANK = 4;
constexpr int CORANK = N - RANK;
constexpr int FIELD_BITS = P - 1;
constexpr int PARAMETER_COUNT = RANK * CORANK * FIELD_BITS;
constexpr int EQUATION_BITS = N * N * P;
constexpr int MARGIN_BITS = N * (N + 1) / 2;
constexpr int TRACE_BITS = P;
constexpr int CONSTRAINT_BITS =
    EQUATION_BITS + MARGIN_BITS + TRACE_BITS;
constexpr int SYNDROME_WORDS = (CONSTRAINT_BITS + 63) / 64;
constexpr Word MASK = (Word{1} << P) - 1;

using FieldMatrix9 = std::array<std::array<Word, N>, N>;
using FieldMatrix4 = std::array<std::array<Word, RANK>, RANK>;
using Chart = std::array<std::array<Word, RANK>, CORANK>;
using BlockWords = std::array<std::array<Word, N>, N>;
using BinaryMatrix9 = std::array<std::array<int, N>, N>;
using Syndrome = std::array<Word, SYNDROME_WORDS>;

Word rotate37(Word value, int amount) {
  amount %= P;
  if (amount == 0) return value & MASK;
  return ((value << amount) | (value >> (P - amount))) & MASK;
}

Word cyclic_multiply(Word left, Word right) {
  Word result = 0;
  while (left) {
    const int exponent = std::countr_zero(left);
    result ^= rotate37(right, exponent);
    left &= left - 1;
  }
  return result & MASK;
}

// F_(2^36) is represented as F_2[x]/Phi_37.  In the cyclic-word
// representation, quotienting by Phi_37 identifies a word with its
// complement.  We choose the unique representative with coefficient zero
// at x^0.
Word canonical_field(Word value) {
  value &= MASK;
  return (value & 1) ? (value ^ MASK) : value;
}

Word field_multiply(Word left, Word right) {
  return canonical_field(cyclic_multiply(left, right));
}

Word cyclic_star(Word value) {
  Word result = value & 1;
  for (int exponent = 1; exponent < P; ++exponent) {
    if ((value >> exponent) & 1)
      result |= Word{1} << (P - exponent);
  }
  return result & MASK;
}

Word field_star(Word value) {
  return canonical_field(cyclic_star(value));
}

Word field_power(Word base, std::uint64_t exponent) {
  const Word one = MASK ^ 1;
  Word result = one;
  while (exponent) {
    if (exponent & 1) result = field_multiply(result, base);
    base = field_multiply(base, base);
    exponent >>= 1;
  }
  return result;
}

Word field_inverse(Word value) {
  if (value == 0) throw std::runtime_error("division by zero");
  return field_power(value, (Word{1} << FIELD_BITS) - 2);
}

bool invert_matrix4(const FieldMatrix4& input, FieldMatrix4& inverse) {
  const Word one = MASK ^ 1;
  std::array<std::array<Word, 2 * RANK>, RANK> augmented{};
  for (int row = 0; row < RANK; ++row) {
    for (int column = 0; column < RANK; ++column)
      augmented[row][column] = input[row][column];
    augmented[row][RANK + row] = one;
  }
  for (int column = 0; column < RANK; ++column) {
    int pivot = column;
    while (pivot < RANK && augmented[pivot][column] == 0) ++pivot;
    if (pivot == RANK) return false;
    std::swap(augmented[pivot], augmented[column]);
    const Word scale = field_inverse(augmented[column][column]);
    for (int j = 0; j < 2 * RANK; ++j)
      augmented[column][j] =
          field_multiply(augmented[column][j], scale);
    for (int row = 0; row < RANK; ++row) {
      if (row == column || augmented[row][column] == 0) continue;
      const Word factor = augmented[row][column];
      for (int j = 0; j < 2 * RANK; ++j)
        augmented[row][j] ^=
            field_multiply(factor, augmented[column][j]);
    }
  }
  for (int row = 0; row < RANK; ++row)
    for (int column = 0; column < RANK; ++column)
      inverse[row][column] = augmented[row][RANK + column];
  return true;
}

FieldMatrix9 multiply9(const FieldMatrix9& left,
                       const FieldMatrix9& right) {
  FieldMatrix9 result{};
  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j)
      for (int k = 0; k < N; ++k)
        result[i][j] ^=
            field_multiply(left[i][k], right[k][j]);
  return result;
}

bool build_projection(const Chart& chart, FieldMatrix9& projection) {
  const Word one = MASK ^ 1;
  FieldMatrix4 gram{};
  for (int i = 0; i < RANK; ++i) {
    gram[i][i] = one;
    for (int j = 0; j < RANK; ++j)
      for (int row = 0; row < CORANK; ++row)
        gram[i][j] ^=
            field_multiply(field_star(chart[row][i]),
                           chart[row][j]);
  }
  FieldMatrix4 gram_inverse{};
  if (!invert_matrix4(gram, gram_inverse)) return false;

  std::array<std::array<Word, RANK>, N> frame{};
  for (int i = 0; i < RANK; ++i) frame[i][i] = one;
  for (int row = 0; row < CORANK; ++row)
    for (int column = 0; column < RANK; ++column)
      frame[RANK + row][column] = chart[row][column];

  projection = {};
  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j)
      for (int a = 0; a < RANK; ++a)
        for (int b = 0; b < RANK; ++b)
          projection[i][j] ^=
              field_multiply(
                  field_multiply(frame[i][a], gram_inverse[a][b]),
                  field_star(frame[j][b]));

  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j)
      if (projection[i][j] != field_star(projection[j][i]))
        throw std::runtime_error("projection is not Hermitian");
  if (multiply9(projection, projection) != projection)
    throw std::runtime_error("projection is not idempotent");
  return true;
}

Word find_omega() {
  const Word one = MASK ^ 1;
  const std::uint64_t exponent =
      ((Word{1} << FIELD_BITS) - 1) / 3;
  for (Word trial = 2; trial < 100000; ++trial) {
    Word candidate = canonical_field(trial);
    if (candidate == 0) continue;
    Word omega = field_power(candidate, exponent);
    if (omega != one && omega != 0 &&
        (field_multiply(omega, omega) ^ omega ^ one) == 0 &&
        field_star(omega) == omega)
      return omega;
  }
  throw std::runtime_error("failed to locate F4");
}

FieldMatrix9 projection_to_d(const FieldMatrix9& projection,
                             Word omega_squared) {
  const Word one = MASK ^ 1;
  FieldMatrix9 d = projection;
  for (int i = 0; i < N; ++i) d[i][i] ^= omega_squared;
  FieldMatrix9 equation = multiply9(d, d);
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) equation[i][j] ^= d[i][j];
    equation[i][i] ^= one;
  }
  for (const auto& row : equation)
    for (Word entry : row)
      if (entry != 0)
        throw std::runtime_error("D^2+D=I failed in field factor");
  return d;
}

BinaryMatrix9 parity_type(int type) {
  BinaryMatrix9 result{};
  const std::array<std::array<int, 2>, 18> type_two_edges{{
      {{0, 7}}, {{0, 8}}, {{1, 4}}, {{1, 5}}, {{1, 6}}, {{1, 8}},
      {{2, 3}}, {{2, 5}}, {{2, 6}}, {{2, 8}}, {{3, 4}}, {{3, 6}},
      {{3, 8}}, {{4, 6}}, {{4, 8}}, {{5, 6}}, {{5, 8}}, {{6, 7}},
  }};
  if (type == 1) {
    const std::array<std::array<int, 2>, 14> edges{{
        {{0, 7}}, {{0, 8}}, {{1, 6}}, {{1, 8}}, {{2, 5}},
        {{2, 8}}, {{3, 4}}, {{3, 8}}, {{4, 5}}, {{4, 6}},
        {{4, 7}}, {{5, 6}}, {{5, 7}}, {{6, 7}},
    }};
    for (auto edge : edges)
      result[edge[0]][edge[1]] = result[edge[1]][edge[0]] = 1;
  } else if (type == 2) {
    for (auto edge : type_two_edges)
      result[edge[0]][edge[1]] = result[edge[1]][edge[0]] = 1;
  } else {
    throw std::runtime_error("unknown parity type");
  }
  return result;
}

BinaryMatrix9 quotient_target(int type) {
  if (type == 1) {
    return {{
        {{16, 18, 18, 18, 22, 22, 22, 13, 17}},
        {{18, 16, 18, 18, 22, 22, 13, 22, 17}},
        {{18, 18, 16, 18, 22, 13, 22, 22, 17}},
        {{18, 18, 18, 16, 13, 22, 22, 22, 17}},
        {{22, 22, 22, 13, 18, 17, 17, 17, 18}},
        {{22, 22, 13, 22, 17, 18, 17, 17, 18}},
        {{22, 13, 22, 22, 17, 17, 18, 17, 18}},
        {{13, 22, 22, 22, 17, 17, 17, 18, 18}},
        {{17, 17, 17, 17, 18, 18, 18, 18, 26}},
    }};
  }
  if (type == 2) {
    return {{
        {{24, 20, 20, 20, 18, 18, 16, 15, 15}},
        {{20, 22, 14, 14, 19, 19, 17, 22, 19}},
        {{20, 14, 18, 17, 24, 15, 19, 18, 21}},
        {{20, 14, 17, 18, 15, 24, 19, 18, 21}},
        {{18, 19, 24, 15, 14, 16, 21, 20, 19}},
        {{18, 19, 15, 24, 16, 14, 21, 20, 19}},
        {{16, 17, 19, 19, 21, 21, 20, 21, 12}},
        {{15, 22, 18, 18, 20, 20, 21, 12, 20}},
        {{15, 19, 21, 21, 19, 19, 12, 20, 20}},
    }};
  }
  throw std::runtime_error("unknown quotient target");
}

void verify_quotient_target(const BinaryMatrix9& quotient,
                            const BinaryMatrix9& parity) {
  for (int i = 0; i < N; ++i) {
    int row_sum = 0;
    for (int j = 0; j < N; ++j) {
      if (quotient[i][j] != quotient[j][i])
        throw std::runtime_error("quotient is not symmetric");
      if ((quotient[i][j] & 1) != parity[i][j])
        throw std::runtime_error("quotient parity mismatch");
      row_sum += quotient[i][j];
      int square = 0;
      for (int k = 0; k < N; ++k)
        square += quotient[i][k] * quotient[k][j];
      const int target = 83 * (i == j) + 83 * P;
      if (square + quotient[i][j] != target)
        throw std::runtime_error("integral quotient equation failed");
    }
    if (row_sum != 166)
      throw std::runtime_error("integral quotient row sum failed");
  }
}

void verify_parity_equation(const BinaryMatrix9& parity) {
  for (int i = 0; i < N; ++i) {
    if (parity[i][i])
      throw std::runtime_error("parity quotient has a loop");
    for (int j = 0; j < N; ++j) {
      int value = parity[i][j];
      for (int k = 0; k < N; ++k)
        value ^= parity[i][k] & parity[k][j];
      const int target = (i != j);
      if (value != target)
        throw std::runtime_error("parity quotient equation failed");
    }
  }
}

BlockWords reconstruct_words(const FieldMatrix9& d,
                             const BinaryMatrix9& parity) {
  BlockWords words{};
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      Word word = canonical_field(d[i][j]);
      if ((std::popcount(word) & 1) != parity[i][j]) word ^= MASK;
      words[i][j] = word;
    }
  }
  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j)
      if (words[i][j] != cyclic_star(words[j][i]))
        throw std::runtime_error("CRT reconstruction lost block symmetry");
  for (int i = 0; i < N; ++i)
    if (words[i][i] & 1)
      throw std::runtime_error(
          "Hermitian even-augmentation diagonal acquired a loop");
  return words;
}

void verify_full_mod2_equation(const BlockWords& words) {
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      Word value = words[i][j];
      for (int k = 0; k < N; ++k)
        value ^= cyclic_multiply(words[i][k], words[k][j]);
      Word target = MASK;
      if (i == j) target ^= 1;
      if (value != target)
        throw std::runtime_error("full group-ring mod-2 equation failed");
    }
  }
}

Syndrome mod4_carry_syndrome(const BlockWords& words) {
  Syndrome syndrome{};
  int bit_index = 0;
  for (int i = 0; i < N; ++i) {
    for (int j = 0; j < N; ++j) {
      for (int lag = 0; lag < P; ++lag, ++bit_index) {
        int value = static_cast<int>((words[i][j] >> lag) & 1);
        for (int k = 0; k < N; ++k) {
          Word left = words[i][k];
          while (left) {
            const int source = std::countr_zero(left);
            const int other = (lag - source + P) % P;
            value += static_cast<int>(
                (words[k][j] >> other) & 1);
            left &= left - 1;
          }
        }
        const int target =
            83 * (1 + ((i == j && lag == 0) ? 1 : 0));
        int residue = (value - target) % 4;
        if (residue < 0) residue += 4;
        if (residue & 1)
          throw std::runtime_error("mod-2 equation did not make carry");
        if (residue == 2)
          syndrome[bit_index / 64] |=
              Word{1} << (bit_index % 64);
      }
    }
  }
  return syndrome;
}

Syndrome targeted_mod4_syndrome(
    const BlockWords& words, const BinaryMatrix9& quotient) {
  Syndrome syndrome = mod4_carry_syndrome(words);
  int bit_index = EQUATION_BITS;
  for (int i = 0; i < N; ++i) {
    for (int j = i; j < N; ++j, ++bit_index) {
      const int weight = std::popcount(words[i][j]);
      const int difference = weight - quotient[i][j];
      if (difference & 1)
        throw std::runtime_error("quotient parity mismatch");
      if ((difference / 2) & 1)
        syndrome[bit_index / 64] |=
            Word{1} << (bit_index % 64);
    }
  }
  Word trace_parity = 0;
  for (int i = 0; i < N; ++i) trace_parity ^= words[i][i];
  for (int lag = 0; lag < P; ++lag, ++bit_index) {
    int incidence = 0;
    for (int i = 0; i < N; ++i)
      incidence += (words[i][i] >> lag) & 1;
    const int target =
        lag == 0 ? 0 : (((trace_parity >> lag) & 1) ? 3 : 6);
    const int difference = incidence - target;
    if (difference & 1)
      throw std::runtime_error("trace-law parity mismatch");
    if ((difference / 2) & 1)
      syndrome[bit_index / 64] |=
          Word{1} << (bit_index % 64);
  }
  if (bit_index != CONSTRAINT_BITS)
    throw std::runtime_error("targeted syndrome shape mismatch");
  return syndrome;
}

int syndrome_weight(const Syndrome& syndrome) {
  int result = 0;
  for (Word word : syndrome) result += std::popcount(word);
  return result;
}

Syndrome syndrome_xor(Syndrome left, const Syndrome& right) {
  for (int i = 0; i < SYNDROME_WORDS; ++i) left[i] ^= right[i];
  return left;
}

int highest_bit(const Syndrome& syndrome) {
  for (int word = SYNDROME_WORDS - 1; word >= 0; --word) {
    if (syndrome[word])
      return word * 64 + 63 - std::countl_zero(syndrome[word]);
  }
  return -1;
}

class BinarySpan {
 public:
  bool insert(Syndrome value) {
    while (true) {
      const int pivot = highest_bit(value);
      if (pivot < 0) return false;
      if (!occupied_[pivot]) {
        basis_[pivot] = value;
        occupied_[pivot] = true;
        ++rank_;
        return true;
      }
      value = syndrome_xor(value, basis_[pivot]);
    }
  }

  int rank() const { return rank_; }

 private:
  std::array<Syndrome, CONSTRAINT_BITS> basis_{};
  std::array<bool, CONSTRAINT_BITS> occupied_{};
  int rank_ = 0;
};

std::uint64_t next_random(std::uint64_t& state) {
  state ^= state << 13;
  state ^= state >> 7;
  state ^= state << 17;
  return state;
}

Chart random_chart(std::uint64_t& state) {
  Chart result{};
  for (auto& row : result)
    for (Word& entry : row)
      entry = canonical_field(next_random(state) & MASK);
  return result;
}

struct Evaluation {
  Syndrome carry{};
  Syndrome targeted{};
  int loops = 0;
  int total_weight = 0;
};

Evaluation evaluate(const Chart& chart, const BinaryMatrix9& parity,
                    const BinaryMatrix9& quotient, Word omega_squared) {
  FieldMatrix9 projection{};
  if (!build_projection(chart, projection))
    throw std::runtime_error("singular chart Gram matrix");
  const FieldMatrix9 d = projection_to_d(projection, omega_squared);
  const BlockWords words = reconstruct_words(d, parity);
  verify_full_mod2_equation(words);
  Word trace_word = 0;
  for (int i = 0; i < N; ++i) trace_word ^= words[i][i];
  Word expected_trace = canonical_field(omega_squared);
  if ((std::popcount(expected_trace) & 1) != 0) expected_trace ^= MASK;
  if (trace_word != expected_trace ||
      (trace_word & 1) != 0 ||
      std::popcount(trace_word) != 18 ||
      cyclic_star(trace_word) != trace_word)
    throw std::runtime_error("rank-four trace word changed");
  Evaluation result;
  result.carry = mod4_carry_syndrome(words);
  result.targeted = targeted_mod4_syndrome(words, quotient);
  for (int i = 0; i < N; ++i)
    result.loops += words[i][i] & 1;
  for (int i = 0; i < N; ++i)
    for (int j = i; j < N; ++j)
      result.total_weight += std::popcount(words[i][j]);
  return result;
}

void audit_chart(int parity_index, int sample_index, Chart chart,
                 const BinaryMatrix9& parity,
                 const BinaryMatrix9& quotient, Word omega_squared) {
  const Evaluation base =
      evaluate(chart, parity, quotient, omega_squared);
  BinarySpan derivatives;
  int singular_toggles = 0;
  for (int parameter = 0; parameter < PARAMETER_COUNT; ++parameter) {
    const int field_coordinate = parameter % FIELD_BITS + 1;
    const int matrix_coordinate = parameter / FIELD_BITS;
    const int row = matrix_coordinate / RANK;
    const int column = matrix_coordinate % RANK;
    chart[row][column] ^= Word{1} << field_coordinate;
    try {
      const Evaluation neighbor =
          evaluate(chart, parity, quotient, omega_squared);
      derivatives.insert(
          syndrome_xor(base.targeted, neighbor.targeted));
    } catch (const std::runtime_error& error) {
      if (std::string(error.what()) != "singular chart Gram matrix")
        throw;
      ++singular_toggles;
    }
    chart[row][column] ^= Word{1} << field_coordinate;
  }
  const int derivative_rank = derivatives.rank();
  const bool base_in_derivative_span =
      !derivatives.insert(base.targeted);
  std::cout << "parity_type=" << parity_index
            << " sample=" << sample_index
            << " carry_weight=" << syndrome_weight(base.carry)
            << " physical_loops=" << base.loops
            << " upper_block_weight_sum=" << base.total_weight
            << " targeted_boolean_derivative_rank=" << derivative_rank
            << " augmented_rank=" << derivatives.rank()
            << " base_in_derivative_span="
            << (base_in_derivative_span ? "yes" : "no")
            << " singular_toggles=" << singular_toggles << "\n";
}

void audit_affine_hull(int parity_index, int sample_count,
                       const BinaryMatrix9& parity,
                       const BinaryMatrix9& quotient, Word omega_squared,
                       std::uint64_t& state) {
  Syndrome origin{};
  bool have_origin = false;
  BinarySpan differences;
  int accepted = 0;
  int singular = 0;
  while (accepted < sample_count) {
    Chart chart = random_chart(state);
    FieldMatrix9 projection{};
    if (!build_projection(chart, projection)) {
      ++singular;
      continue;
    }
    const Evaluation evaluation =
        evaluate(chart, parity, quotient, omega_squared);
    if (!have_origin) {
      origin = evaluation.targeted;
      have_origin = true;
    } else {
      differences.insert(
          syndrome_xor(origin, evaluation.targeted));
    }
    ++accepted;
  }
  const int difference_rank = differences.rank();
  const bool zero_in_sampled_affine_hull =
      !differences.insert(origin);
  std::cout << "parity_type=" << parity_index
            << " affine_samples=" << accepted
            << " sampled_difference_rank=" << difference_rank
            << " augmented_rank=" << differences.rank()
            << " zero_in_sampled_affine_hull="
            << (zero_in_sampled_affine_hull ? "yes" : "no")
            << " singular_charts=" << singular << "\n";
}

}  // namespace

int main(int argc, char** argv) {
  int samples = 2;
  bool affine_mode = false;
  if (argc >= 2 && std::string(argv[1]) == "--affine") {
    affine_mode = true;
    if (argc != 3)
      throw std::runtime_error("usage: --affine SAMPLE_COUNT");
    samples = std::stoi(argv[2]);
  } else if (argc == 2) {
    samples = std::stoi(argv[1]);
  } else if (argc > 2) {
    throw std::runtime_error("usage: [SAMPLES] or --affine SAMPLE_COUNT");
  }
  if (samples <= 0)
    throw std::runtime_error("samples must be positive");

  const Word one = MASK ^ 1;
  if (field_multiply(one, one) != one)
    throw std::runtime_error("field identity failed");
  Word x = Word{1} << 1;
  if (field_power(x, P) != one)
    throw std::runtime_error("37th root representation failed");
  if (field_power(x, 1) == one)
    throw std::runtime_error("37th root collapsed");
  const Word omega = find_omega();
  const Word omega_squared = field_multiply(omega, omega);
  if ((omega ^ omega_squared) != one)
    throw std::runtime_error("F4 relation failed");

  std::cout << "field=F_2^36 chart_bits=" << PARAMETER_COUNT
            << " carry_equation_bits=" << EQUATION_BITS
            << " targeted_constraint_bits=" << CONSTRAINT_BITS
            << " omega=0x" << std::hex << omega
            << " omega_squared=0x" << omega_squared << std::dec << "\n";

  std::uint64_t state = 0x66833437d00dULL;
  for (int parity_index = 1; parity_index <= 2; ++parity_index) {
    const BinaryMatrix9 parity = parity_type(parity_index);
    const BinaryMatrix9 quotient = quotient_target(parity_index);
    verify_parity_equation(parity);
    verify_quotient_target(quotient, parity);
    if (affine_mode) {
      audit_affine_hull(parity_index, samples, parity, quotient,
                        omega_squared, state);
      continue;
    }
    for (int sample = 0; sample < samples; ++sample) {
      while (true) {
        Chart chart = random_chart(state);
        FieldMatrix9 projection{};
        if (!build_projection(chart, projection)) continue;
        audit_chart(parity_index, sample, chart, parity, quotient,
                    omega_squared);
        break;
      }
    }
  }
  return 0;
}
