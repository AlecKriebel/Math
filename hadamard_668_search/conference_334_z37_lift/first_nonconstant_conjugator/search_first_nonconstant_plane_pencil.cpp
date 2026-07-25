#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <unordered_map>
#include <utility>
#include <vector>

// Exact census for the first nonconstant two-plane conjugator.
//
// Work in F_37[y]/(y^37), put z=log(1+y), and consider
//
//   K = z A + z^2 B
//
// on a common nondegenerate two-dimensional support.  After removing the
// scalar part of A on the support, the active 2 by 2 part satisfies
//
//   K_0^2 = (alpha*z^2 + beta*z^4) I.
//
// The scalar gap t between the support and its complement contributes
// x^t, x=(1+y), to the exponential entries.  Decimation normalizes every
// t != 0 to t=1, leaving exactly 37*36 pairs (alpha,beta), beta != 0.
//
// For each pair this program builds the deliberately generous diagonal
// function over-code
//
//   W = span{ entry(E_-)*entry(E_+),
//             z^18*entry(E_-)*entry(E_+) },
//
// where E_+ is spanned by 1 and x*(c,z*s,z^2*s), E_- analogously uses
// x^-1, and exp(K_0)=c I+s K_0.  It then intersects W exactly with
//
//   {0} x {18,19}^36
//
// using a meet-in-the-middle binary search.  Since W forgets the actual
// N0 and J coefficients, emptiness (or weight restrictions) are safe
// obstructions.  This is a formal over-code, not a binary lift search.

namespace {

constexpr int p = 37;
using Poly = std::array<int, p>;
using Row = std::array<int, p>;

int mod(int value) {
  value %= p;
  return value < 0 ? value + p : value;
}

int inverse(int value) {
  value = mod(value);
  assert(value != 0);
  for (int candidate = 1; candidate < p; ++candidate) {
    if (value * candidate % p == 1) return candidate;
  }
  assert(false);
  return 0;
}

Poly zero_poly() {
  Poly result{};
  result.fill(0);
  return result;
}

Poly one_poly() {
  Poly result = zero_poly();
  result[0] = 1;
  return result;
}

Poly add(const Poly& left, const Poly& right) {
  Poly result{};
  for (int i = 0; i < p; ++i) result[i] = mod(left[i] + right[i]);
  return result;
}

Poly subtract(const Poly& left, const Poly& right) {
  Poly result{};
  for (int i = 0; i < p; ++i) result[i] = mod(left[i] - right[i]);
  return result;
}

Poly scale(const Poly& value, int scalar) {
  Poly result{};
  for (int i = 0; i < p; ++i) result[i] = mod(value[i] * scalar);
  return result;
}

Poly multiply(const Poly& left, const Poly& right) {
  Poly result = zero_poly();
  for (int i = 0; i < p; ++i) {
    if (left[i] == 0) continue;
    for (int j = 0; i + j < p; ++j) {
      if (right[j] == 0) continue;
      result[i + j] =
          mod(result[i + j] + left[i] * right[j]);
    }
  }
  return result;
}

Poly power(Poly base, int exponent) {
  Poly result = one_poly();
  while (exponent != 0) {
    if (exponent & 1) result = multiply(result, base);
    base = multiply(base, base);
    exponent >>= 1;
  }
  return result;
}

Poly logarithm() {
  Poly result = zero_poly();
  for (int degree = 1; degree < p; ++degree) {
    const int sign = degree % 2 ? 1 : -1;
    result[degree] = mod(sign * inverse(degree));
  }
  return result;
}

std::array<std::array<int, p>, p> binomial_table() {
  std::array<std::array<int, p>, p> result{};
  for (auto& row : result) row.fill(0);
  result[0][0] = 1;
  for (int n = 1; n < p; ++n) {
    result[n][0] = result[n][n] = 1;
    for (int k = 1; k < n; ++k) {
      result[n][k] = mod(result[n - 1][k - 1] + result[n - 1][k]);
    }
  }
  return result;
}

const auto binom = binomial_table();

Row y_to_x(const Poly& value) {
  // value(y)=sum_t result[t]*(1+y)^t.
  Row result{};
  result.fill(0);
  for (int degree = p - 1; degree >= 0; --degree) {
    int coefficient = value[degree];
    for (int index = degree + 1; index < p; ++index) {
      coefficient -= result[index] * binom[index][degree];
    }
    result[degree] = mod(coefficient);
  }
  return result;
}

struct Basis {
  std::vector<Row> rows;
  std::vector<int> pivots;
};

Basis reduced_row_basis(const std::vector<Row>& generators) {
  Basis result;
  for (Row work : generators) {
    for (std::size_t i = 0; i < result.rows.size(); ++i) {
      const int pivot = result.pivots[i];
      if (work[pivot] == 0) continue;
      const int factor = work[pivot];
      for (int column = 0; column < p; ++column) {
        work[column] =
            mod(work[column] - factor * result.rows[i][column]);
      }
    }
    int pivot = -1;
    for (int column = 0; column < p; ++column) {
      if (work[column] != 0) {
        pivot = column;
        break;
      }
    }
    if (pivot < 0) continue;
    const int inv = inverse(work[pivot]);
    for (int column = 0; column < p; ++column) {
      work[column] = work[column] * inv % p;
    }
    for (Row& old : result.rows) {
      if (old[pivot] == 0) continue;
      const int factor = old[pivot];
      for (int column = 0; column < p; ++column) {
        old[column] = mod(old[column] - factor * work[column]);
      }
    }
    std::size_t position = 0;
    while (position < result.pivots.size() &&
           result.pivots[position] < pivot) {
      ++position;
    }
    result.rows.insert(result.rows.begin() + position, work);
    result.pivots.insert(result.pivots.begin() + position, pivot);
  }
  for (std::size_t i = 0; i < result.rows.size(); ++i) {
    for (std::size_t j = 0; j < result.rows.size(); ++j) {
      assert(result.rows[i][result.pivots[j]] == (i == j ? 1 : 0));
    }
  }
  return result;
}

struct HyperbolicFunctions {
  Poly c;
  Poly s;
};

HyperbolicFunctions hyperbolic_functions(
    int alpha, int beta, const Poly& z2, const Poly& z4) {
  const Poly delta = add(scale(z2, alpha), scale(z4, beta));
  Poly c = zero_poly();
  Poly s = zero_poly();
  Poly delta_power = one_poly();
  int even_factorial = 1;
  for (int n = 0; n <= 18; ++n) {
    if (n != 0) {
      even_factorial =
          even_factorial * (2 * n - 1) % p * (2 * n) % p;
    }
    c = add(c, scale(delta_power, inverse(even_factorial)));
    if (2 * n + 1 < p) {
      const int odd_factorial =
          even_factorial * (2 * n + 1) % p;
      s = add(s, scale(delta_power, inverse(odd_factorial)));
    }
    delta_power = multiply(delta_power, delta);
  }
  // exp(K)exp(-K)=1 when K^2=delta*I.
  assert(add(multiply(c, c), scale(multiply(delta, multiply(s, s)), -1))
         == one_poly());
  return {c, s};
}

Basis diagonal_overcode(
    int scalar_gap, int alpha, int beta,
    const Poly& z, const Poly& z2, const Poly& z4,
    const Poly& half_power) {
  const HyperbolicFunctions functions =
      hyperbolic_functions(alpha, beta, z2, z4);

  Poly x = one_poly();
  x[1] = 1;
  const Poly positive_scalar = power(x, mod(scalar_gap));
  const Poly negative_scalar = power(x, mod(-scalar_gap));

  const std::array<Poly, 3> core = {
      functions.c,
      multiply(z, functions.s),
      multiply(z2, functions.s),
  };
  std::vector<Poly> positive = {one_poly()};
  std::vector<Poly> negative = {one_poly()};
  for (const Poly& value : core) {
    positive.push_back(multiply(positive_scalar, value));
    negative.push_back(multiply(negative_scalar, value));
  }

  std::vector<Row> generators;
  for (const Poly& left : negative) {
    for (const Poly& right : positive) {
      const Poly product = multiply(left, right);
      generators.push_back(y_to_x(product));
      generators.push_back(y_to_x(multiply(half_power, product)));
    }
  }
  return reduced_row_basis(generators);
}

Basis symmetric_diagonal_overcode(
    int scalar_gap, int alpha, int beta,
    const Poly& z, const Poly& z2, const Poly& z4,
    const Poly& half_power) {
  // Restore only the fact that the conjugated matrices N0 and J are
  // symmetric.  Write
  //
  //   E_+ = I+aP+bS+cB,  E_- = I+a'P+b'S+c'B,
  //
  // with P,S symmetric and B skew.  Reversal of a product preserves its
  // diagonal.  The ten displayed coefficient functions therefore contain
  // every diagonal entry of E_- M E_+ for every symmetric M.  Their span
  // and its z^18 multiple remain an over-code because all matrix
  // coefficients are allowed to vary independently.
  const HyperbolicFunctions functions =
      hyperbolic_functions(alpha, beta, z2, z4);
  Poly x = one_poly();
  x[1] = 1;
  const Poly positive_scalar = power(x, mod(scalar_gap));
  const Poly negative_scalar = power(x, mod(-scalar_gap));
  const Poly zs = multiply(z, functions.s);
  const Poly z2s = multiply(z2, functions.s);

  const Poly a = subtract(
      multiply(positive_scalar, functions.c), one_poly());
  const Poly a_prime = subtract(
      multiply(negative_scalar, functions.c), one_poly());
  const Poly b = multiply(positive_scalar, zs);
  const Poly b_prime = scale(multiply(negative_scalar, zs), -1);
  const Poly c = multiply(positive_scalar, z2s);
  const Poly c_prime = scale(multiply(negative_scalar, z2s), -1);

  const std::array<Poly, 10> functions_by_matrix_coefficient = {
      one_poly(),
      add(a, a_prime),
      add(b, b_prime),
      subtract(c_prime, c),
      multiply(a_prime, a),
      add(multiply(a_prime, b), multiply(b_prime, a)),
      subtract(multiply(c_prime, a), multiply(a_prime, c)),
      multiply(b_prime, b),
      subtract(multiply(c_prime, b), multiply(b_prime, c)),
      multiply(c_prime, c),
  };
  std::vector<Row> generators;
  for (const Poly& value : functions_by_matrix_coefficient) {
    generators.push_back(y_to_x(value));
    generators.push_back(y_to_x(multiply(half_power, value)));
  }
  return reduced_row_basis(generators);
}

std::uint64_t packed_key(
    const std::array<int, p>& values, int count) {
  std::uint64_t result = 0;
  for (int i = 0; i < count; ++i) {
    result = result * p + values[i];
  }
  return result;
}

struct WordCensus {
  std::uint64_t count = 0;
  std::map<int, std::uint64_t> weights;
  std::vector<Row> words;
};

WordCensus compatible_binary_words(const Basis& basis) {
  assert(basis.rows.size() >= 2);
  assert(basis.pivots.front() == 0);

  std::array<bool, p> is_pivot{};
  is_pivot.fill(false);
  for (int pivot : basis.pivots) is_pivot[pivot] = true;
  std::array<int, p> checks{};
  int check_count = 0;
  for (int coordinate = 0; coordinate < p; ++coordinate) {
    if (!is_pivot[coordinate]) checks[check_count++] = coordinate;
  }
  assert(check_count == p - static_cast<int>(basis.rows.size()));

  // The coefficient of the pivot-zero row is forced to zero.  Every
  // remaining information coordinate is 18+bit.
  std::vector<Row> bit_rows(
      basis.rows.begin() + 1, basis.rows.end());
  const int information_bits = static_cast<int>(bit_rows.size());
  assert(information_bits <= 23);
  std::array<int, p> base{};
  base.fill(0);
  for (const Row& row : bit_rows) {
    for (int j = 0; j < check_count; ++j) {
      base[j] = mod(base[j] + 18 * row[checks[j]]);
    }
  }

  const int left_bits = information_bits / 2;
  const int right_bits = information_bits - left_bits;
  const int keyed_coordinates = std::min(6, check_count);

  auto subset_sums = [&](int begin, int count) {
    std::vector<std::array<int, p>> sums(1u << count);
    for (auto& value : sums) value.fill(0);
    for (std::uint32_t mask = 1; mask < (1u << count); ++mask) {
      const std::uint32_t bit = mask & (~mask + 1);
      const int offset = __builtin_ctz(bit);
      const std::uint32_t previous = mask ^ bit;
      sums[mask] = sums[previous];
      const Row& row = bit_rows[begin + offset];
      for (int j = 0; j < check_count; ++j) {
        sums[mask][j] =
            mod(sums[mask][j] + row[checks[j]]);
      }
    }
    return sums;
  };

  const auto left_sums = subset_sums(0, left_bits);
  const auto right_sums = subset_sums(left_bits, right_bits);
  std::unordered_map<std::uint64_t, std::vector<std::uint32_t>>
      right_buckets;
  right_buckets.reserve(right_sums.size() * 2);
  for (std::uint32_t mask = 0; mask < right_sums.size(); ++mask) {
    right_buckets[packed_key(right_sums[mask], keyed_coordinates)]
        .push_back(mask);
  }

  WordCensus census;
  for (std::uint32_t left_mask = 0;
       left_mask < left_sums.size(); ++left_mask) {
    const auto& left = left_sums[left_mask];
    for (int target_mask = 0;
         target_mask < (1 << keyed_coordinates); ++target_mask) {
      std::array<int, p> needed{};
      needed.fill(0);
      for (int j = 0; j < keyed_coordinates; ++j) {
        const int target = 18 + ((target_mask >> j) & 1);
        needed[j] = mod(target - base[j] - left[j]);
      }
      const auto found =
          right_buckets.find(packed_key(needed, keyed_coordinates));
      if (found == right_buckets.end()) continue;
      for (std::uint32_t right_mask : found->second) {
        const auto& right = right_sums[right_mask];
        bool compatible = true;
        for (int j = keyed_coordinates; j < check_count; ++j) {
          const int value = mod(base[j] + left[j] + right[j]);
          if (value != 18 && value != 19) {
            compatible = false;
            break;
          }
        }
        if (!compatible) continue;

        Row word{};
        word.fill(0);
        for (std::size_t row_index = 0;
             row_index < bit_rows.size(); ++row_index) {
          const bool bit =
              static_cast<int>(row_index) < left_bits
                  ? ((left_mask >> row_index) & 1)
                  : ((right_mask >> (row_index - left_bits)) & 1);
          const int coefficient = 18 + static_cast<int>(bit);
          for (int coordinate = 0; coordinate < p; ++coordinate) {
            word[coordinate] =
                mod(word[coordinate]
                    + coefficient * bit_rows[row_index][coordinate]);
          }
        }
        assert(word[0] == 0);
        int weight = 0;
        for (int coordinate = 1; coordinate < p; ++coordinate) {
          assert(word[coordinate] == 18 || word[coordinate] == 19);
          weight += word[coordinate] - 18;
        }
        ++census.count;
        ++census.weights[weight];
        census.words.push_back(word);
      }
    }
  }
  return census;
}

}  // namespace

int main() {
  const Poly z = logarithm();
  const Poly z2 = multiply(z, z);
  const Poly z4 = multiply(z2, z2);
  const Poly half_power = power(z, 18);
  Poly expected_socle = zero_poly();
  expected_socle[36] = 1;
  assert(multiply(half_power, half_power) == expected_socle);

  std::map<std::uint64_t, int> trace_zero_word_count_distribution;
  std::map<int, std::uint64_t> trace_zero_weight_distribution;
  std::map<int, int> trace_zero_symmetric_dimension_distribution;
  std::map<std::uint64_t, int>
      trace_zero_symmetric_word_count_distribution;
  std::map<int, std::uint64_t>
      trace_zero_symmetric_weight_distribution;
  int trace_zero_orbits = 0;
  std::array<std::array<bool, p>, p> seen{};
  for (auto& row : seen) row.fill(false);
  for (int alpha = 0; alpha < p; ++alpha) {
    for (int beta = 1; beta < p; ++beta) {
      if (seen[alpha][beta]) continue;
      ++trace_zero_orbits;
      for (int multiplier = 1; multiplier < p; ++multiplier) {
        const int transformed_alpha =
            multiplier * multiplier % p * alpha % p;
        const int square = multiplier * multiplier % p;
        const int fourth = square * square % p;
        const int transformed_beta = fourth * beta % p;
        seen[transformed_alpha][transformed_beta] = true;
      }
      const Basis basis = diagonal_overcode(
          0, alpha, beta, z, z2, z4, half_power);
      assert(basis.rows.size() == 18);
      const WordCensus census = compatible_binary_words(basis);
      ++trace_zero_word_count_distribution[census.count];
      for (const auto& [weight, count] : census.weights) {
        trace_zero_weight_distribution[weight] += count;
      }
      const Basis symmetric_basis = symmetric_diagonal_overcode(
          0, alpha, beta, z, z2, z4, half_power);
      ++trace_zero_symmetric_dimension_distribution[
          static_cast<int>(symmetric_basis.rows.size())];
      const WordCensus symmetric_census =
          compatible_binary_words(symmetric_basis);
      ++trace_zero_symmetric_word_count_distribution[
          symmetric_census.count];
      for (const auto& [weight, count] : symmetric_census.weights) {
        trace_zero_symmetric_weight_distribution[weight] += count;
      }
    }
  }
  assert(trace_zero_orbits == 76);

  std::map<std::uint64_t, int> nonzero_word_count_distribution;
  std::map<int, std::uint64_t> nonzero_weight_distribution;
  std::map<int, int> nonzero_symmetric_dimension_distribution;
  std::map<std::uint64_t, int>
      nonzero_symmetric_word_count_distribution;
  std::map<int, std::uint64_t> nonzero_symmetric_weight_distribution;
  struct ExceptionalRecord {
    int alpha;
    int beta;
    WordCensus census;
  };
  std::vector<ExceptionalRecord> exceptional_records;
  int parameter_pairs = 0;
  for (int alpha = 0; alpha < p; ++alpha) {
    for (int beta = 1; beta < p; ++beta) {
      const Basis basis = diagonal_overcode(
          1, alpha, beta, z, z2, z4, half_power);
      assert(basis.rows.size() == 24);
      const WordCensus census = compatible_binary_words(basis);
      ++nonzero_word_count_distribution[census.count];
      if (census.count != 2) {
        exceptional_records.push_back({alpha, beta, census});
      }
      for (const auto& [weight, count] : census.weights) {
        nonzero_weight_distribution[weight] += count;
      }
      const Basis symmetric_basis = symmetric_diagonal_overcode(
          1, alpha, beta, z, z2, z4, half_power);
      ++nonzero_symmetric_dimension_distribution[
          static_cast<int>(symmetric_basis.rows.size())];
      const WordCensus symmetric_census =
          compatible_binary_words(symmetric_basis);
      ++nonzero_symmetric_word_count_distribution[
          symmetric_census.count];
      for (const auto& [weight, count] : symmetric_census.weights) {
        nonzero_symmetric_weight_distribution[weight] += count;
      }
      ++parameter_pairs;
    }
  }
  assert(parameter_pairs == 37 * 36);
  assert((trace_zero_symmetric_dimension_distribution
          == std::map<int, int>{{12, 76}}));
  assert((trace_zero_symmetric_word_count_distribution
          == std::map<std::uint64_t, int>{{2, 76}}));
  assert((trace_zero_symmetric_weight_distribution
          == std::map<int, std::uint64_t>{{18, 152}}));
  assert((nonzero_symmetric_dimension_distribution
          == std::map<int, int>{{14, 1332}}));
  assert((nonzero_symmetric_word_count_distribution
          == std::map<std::uint64_t, int>{{2, 1330}, {4, 2}}));
  assert((nonzero_symmetric_weight_distribution
          == std::map<int, std::uint64_t>{
              {12, 1}, {14, 1}, {18, 2664}, {22, 1}, {24, 1}}));

  std::cout << "trace_zero_decimation_orbits="
            << trace_zero_orbits << "\n";
  std::cout << "trace_zero_overcode_dimension=18\n";
  std::cout << "trace_zero_word_count_distribution";
  for (const auto& [count, classes] :
       trace_zero_word_count_distribution) {
    std::cout << " " << count << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "trace_zero_aggregate_weight_distribution";
  for (const auto& [weight, count] : trace_zero_weight_distribution) {
    std::cout << " " << weight << ":" << count;
  }
  std::cout << "\n";
  std::cout << "trace_zero_symmetric_dimension_distribution";
  for (const auto& [dimension, classes] :
       trace_zero_symmetric_dimension_distribution) {
    std::cout << " " << dimension << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "trace_zero_symmetric_word_count_distribution";
  for (const auto& [count, classes] :
       trace_zero_symmetric_word_count_distribution) {
    std::cout << " " << count << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "trace_zero_symmetric_weight_distribution";
  for (const auto& [weight, count] :
       trace_zero_symmetric_weight_distribution) {
    std::cout << " " << weight << ":" << count;
  }
  std::cout << "\n";
  std::cout << "normalized_nonzero_scalar_gap=1\n";
  std::cout << "nonzero_trace_parameter_pairs=" << parameter_pairs << "\n";
  std::cout << "overcode_dimension=24\n";
  std::cout << "binary_information_bits=23\n";
  std::cout << "nonzero_trace_word_count_distribution";
  for (const auto& [count, classes] :
       nonzero_word_count_distribution) {
    std::cout << " " << count << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "nonzero_trace_aggregate_weight_distribution";
  for (const auto& [weight, count] : nonzero_weight_distribution) {
    std::cout << " " << weight << ":" << count;
  }
  std::cout << "\n";
  std::cout << "nonzero_trace_symmetric_dimension_distribution";
  for (const auto& [dimension, classes] :
       nonzero_symmetric_dimension_distribution) {
    std::cout << " " << dimension << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "nonzero_trace_symmetric_word_count_distribution";
  for (const auto& [count, classes] :
       nonzero_symmetric_word_count_distribution) {
    std::cout << " " << count << ":" << classes;
  }
  std::cout << "\n";
  std::cout << "nonzero_trace_symmetric_weight_distribution";
  for (const auto& [weight, count] :
       nonzero_symmetric_weight_distribution) {
    std::cout << " " << weight << ":" << count;
  }
  std::cout << "\n";
  std::cout << "exceptional_parameter_count="
            << exceptional_records.size() << "\n";
  for (const ExceptionalRecord& record : exceptional_records) {
    std::cout << "exception alpha=" << record.alpha
              << " beta=" << record.beta
              << " word_count=" << record.census.count
              << " weights";
    for (const auto& [weight, count] : record.census.weights) {
      std::cout << " " << weight << ":" << count;
    }
    std::cout << "\n";
    for (const Row& word : record.census.words) {
      std::cout << "exception_word weight=";
      int weight = 0;
      for (int coordinate = 1; coordinate < p; ++coordinate) {
        weight += word[coordinate] - 18;
      }
      std::cout << weight << " bits=";
      for (int coordinate = 1; coordinate < p; ++coordinate) {
        std::cout << word[coordinate] - 18;
      }
      std::cout << "\n";
    }
  }
  std::cout << "certificate=PASS\n";
}
