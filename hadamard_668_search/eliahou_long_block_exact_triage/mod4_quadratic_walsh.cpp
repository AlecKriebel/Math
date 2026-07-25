// Exact Walsh census for twenty quadratic Boolean forms on 57 variables.
//
// The binary model is emitted by run_mod4_walsh_census.py.  A full run
// visits the 2^20 linear combinations of the forms.  For each combination,
// symplectic elimination returns the polar rank and signed Walsh sum without
// enumerating the 2^57 affine points.

#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kVariables = 57;
constexpr int kForms = 20;
constexpr char kMagic[8] = {'H', '6', '6', '8', 'M', '4', 'Q', '1'};

struct Form {
  std::uint64_t constant = 0;
  std::uint64_t linear = 0;
  std::array<std::uint64_t, kVariables> adjacency{};
};

struct WalshResult {
  std::int64_t value;
  int polar_rank;
};

struct Model {
  std::array<Form, kForms> forms;
};

template <typename T>
T Read(std::ifstream* input) {
  T value{};
  input->read(reinterpret_cast<char*>(&value), sizeof(value));
  if (!*input) throw std::runtime_error("truncated model");
  return value;
}

Model ReadModel(const std::string& path) {
  std::ifstream input(path, std::ios::binary);
  if (!input) throw std::runtime_error("cannot open model");
  char magic[8]{};
  input.read(magic, sizeof(magic));
  if (!input || std::memcmp(magic, kMagic, sizeof(magic)) != 0) {
    throw std::runtime_error("bad model magic");
  }
  const auto variables = Read<std::uint32_t>(&input);
  const auto forms = Read<std::uint32_t>(&input);
  if (variables != kVariables || forms != kForms) {
    throw std::runtime_error("bad model dimensions");
  }
  Model model;
  for (auto& form : model.forms) {
    form.constant = Read<std::uint64_t>(&input);
    form.linear = Read<std::uint64_t>(&input);
    for (auto& row : form.adjacency) {
      row = Read<std::uint64_t>(&input);
    }
  }
  char trailing = 0;
  if (input.read(&trailing, 1)) {
    throw std::runtime_error("trailing model payload");
  }
  return model;
}

WalshResult Evaluate(Form form) {
  std::uint64_t active = (std::uint64_t{1} << kVariables) - 1;
  int pairs = 0;
  while (true) {
    int left = -1;
    std::uint64_t neighbors = 0;
    for (int variable = 0; variable < kVariables; ++variable) {
      if (((active >> variable) & 1) == 0) continue;
      neighbors = form.adjacency[variable] & active;
      if (neighbors) {
        left = variable;
        break;
      }
    }
    if (left < 0) break;
    const int right = std::countr_zero(neighbors);
    const std::uint64_t keep =
        active & ~(std::uint64_t{1} << left) &
        ~(std::uint64_t{1} << right);
    const std::uint64_t alpha = form.adjacency[left] & keep;
    const std::uint64_t beta = form.adjacency[right] & keep;
    const bool left_linear = (form.linear >> left) & 1;
    const bool right_linear = (form.linear >> right) & 1;
    if (left_linear && right_linear) form.constant ^= 1;
    form.linear ^=
        (left_linear ? beta : 0) ^
        (right_linear ? alpha : 0) ^
        (alpha & beta);

    std::uint64_t scan = alpha;
    while (scan) {
      const int variable = std::countr_zero(scan);
      form.adjacency[variable] ^= beta;
      scan &= scan - 1;
    }
    scan = beta;
    while (scan) {
      const int variable = std::countr_zero(scan);
      form.adjacency[variable] ^= alpha;
      scan &= scan - 1;
    }
    active = keep;
    ++pairs;
  }

  const int rank = 2 * pairs;
  if (form.linear & active) return {0, rank};
  const int remaining = std::popcount(active);
  const int exponent = pairs + remaining;
  if (exponent >= 63) {
    throw std::runtime_error("Walsh amplitude overflow");
  }
  const std::int64_t amplitude = std::int64_t{1} << exponent;
  return {
      (form.constant & 1) ? -amplitude : amplitude,
      rank,
  };
}

std::int64_t BruteWalsh(const Form& form, int variables) {
  std::int64_t result = 0;
  for (std::uint64_t state = 0;
       state < (std::uint64_t{1} << variables); ++state) {
    int value = std::popcount(state & form.linear) & 1;
    value ^= form.constant & 1;
    for (int left = 0; left < variables; ++left) {
      if ((state >> left) & 1) {
        value ^= std::popcount(
                     state & form.adjacency[left] &
                     ~((std::uint64_t{1} << (left + 1)) - 1)) &
                 1;
      }
    }
    result += value ? -1 : 1;
  }
  return result;
}

void SelfTest() {
  std::uint64_t state = 668'404'207;
  auto next = [&]() {
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state;
  };
  for (int trial = 0; trial < 256; ++trial) {
    constexpr int variables = 8;
    Form form;
    form.constant = next() & 1;
    form.linear = next() & ((std::uint64_t{1} << variables) - 1);
    for (int left = 0; left < variables; ++left) {
      for (int right = left + 1; right < variables; ++right) {
        if (next() & 1) {
          form.adjacency[left] |= std::uint64_t{1} << right;
          form.adjacency[right] |= std::uint64_t{1} << left;
        }
      }
    }
    // Variables 8,...,56 are fixed absent from the small brute-force form.
    // Evaluate would otherwise include them as free radical variables.
    Form padded = form;
    for (int variable = variables; variable < kVariables; ++variable) {
      padded.linear |= std::uint64_t{1} << variable;
    }
    // Sum over a newly linear free variable is zero.  Test nonzero small
    // sums by coupling each padding variable to variable zero instead.
    if (BruteWalsh(form, variables) != 0) {
      padded = form;
      for (int variable = variables; variable < kVariables; ++variable) {
        padded.adjacency[0] |= std::uint64_t{1} << variable;
        padded.adjacency[variable] |= std::uint64_t{1};
      }
      // This padding changes the sum, so use the 57-variable evaluator only
      // for structural invariants below and test the exact algorithm on an
      // embedded 8-variable implementation by adding 49 isolated variables:
      // each isolated variable multiplies the Walsh sum by two.
      padded = form;
      const auto exact = Evaluate(padded).value;
      const auto wanted =
          BruteWalsh(form, variables) *
          (std::int64_t{1} << (kVariables - variables));
      if (exact != wanted) {
        throw std::runtime_error("quadratic Walsh self-test failed");
      }
    } else if (Evaluate(form).value != 0) {
      throw std::runtime_error("zero Walsh self-test failed");
    }
  }
}

std::string Decimal(__int128 value) {
  if (value == 0) return "0";
  bool negative = value < 0;
  if (negative) value = -value;
  std::string result;
  while (value) {
    result.push_back(static_cast<char>('0' + value % 10));
    value /= 10;
  }
  if (negative) result.push_back('-');
  std::reverse(result.begin(), result.end());
  return result;
}

std::uint64_t Parse(const char* text) {
  std::size_t used = 0;
  const std::string value(text);
  const auto result = std::stoull(value, &used);
  if (used != value.size()) throw std::runtime_error("bad integer argument");
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 4) {
      throw std::runtime_error(
          "usage: mod4_quadratic_walsh MODEL START STOP");
    }
    SelfTest();
    const Model model = ReadModel(argv[1]);
    const std::uint64_t start = Parse(argv[2]);
    const std::uint64_t stop = Parse(argv[3]);
    if (start > stop || stop > (std::uint64_t{1} << kForms)) {
      throw std::runtime_error("invalid Walsh range");
    }

    Form combined;
    const std::uint64_t first_gray = start ^ (start >> 1);
    for (int form_index = 0; form_index < kForms; ++form_index) {
      if (((first_gray >> form_index) & 1) == 0) continue;
      const auto& source = model.forms[form_index];
      combined.constant ^= source.constant;
      combined.linear ^= source.linear;
      for (int row = 0; row < kVariables; ++row) {
        combined.adjacency[row] ^= source.adjacency[row];
      }
    }

    std::array<std::uint64_t, kVariables + 1> rank_histogram{};
    std::uint64_t zero_walsh = 0;
    int minimum_nonzero_pencil_rank = kVariables + 1;
    __int128 signed_sum = 0;
    std::uint64_t previous_gray = first_gray;
    const auto began = std::chrono::steady_clock::now();
    for (std::uint64_t index = start; index < stop; ++index) {
      if (index != start) {
        const std::uint64_t gray = index ^ (index >> 1);
        const std::uint64_t changed = gray ^ previous_gray;
        const int form_index = std::countr_zero(changed);
        const auto& source = model.forms[form_index];
        combined.constant ^= source.constant;
        combined.linear ^= source.linear;
        for (int row = 0; row < kVariables; ++row) {
          combined.adjacency[row] ^= source.adjacency[row];
        }
        previous_gray = gray;
      }
      const WalshResult result = Evaluate(combined);
      ++rank_histogram[result.polar_rank];
      if (result.value == 0) ++zero_walsh;
      signed_sum += result.value;
      if (index != 0) {
        minimum_nonzero_pencil_rank =
            std::min(minimum_nonzero_pencil_rank, result.polar_rank);
      }
    }
    const double seconds = std::chrono::duration<double>(
                               std::chrono::steady_clock::now() - began)
                               .count();
    const std::uint64_t combinations = stop - start;
    std::cout << "{\n";
    std::cout << "  \"schema\": \"h668-mod4-quadratic-walsh-range-v1\",\n";
    std::cout << "  \"start\": " << start << ",\n";
    std::cout << "  \"stop\": " << stop << ",\n";
    std::cout << "  \"combinations\": " << combinations << ",\n";
    std::cout << "  \"zero_walsh_count\": " << zero_walsh << ",\n";
    std::cout << "  \"minimum_nonzero_pencil_polar_rank\": "
              << minimum_nonzero_pencil_rank << ",\n";
    std::cout << "  \"rank_histogram\": {";
    bool first = true;
    for (int rank = 0; rank <= kVariables; ++rank) {
      if (!rank_histogram[rank]) continue;
      if (!first) std::cout << ", ";
      first = false;
      std::cout << '\"' << rank << "\": " << rank_histogram[rank];
    }
    std::cout << "},\n";
    std::cout << "  \"signed_walsh_sum\": \""
              << Decimal(signed_sum) << "\",\n";
    if (start == 0 && stop == (std::uint64_t{1} << kForms)) {
      if (signed_sum % (std::uint64_t{1} << kForms) != 0) {
        throw std::runtime_error("common-zero character sum not integral");
      }
      std::cout << "  \"common_zeros\": \""
                << Decimal(signed_sum >> kForms) << "\",\n";
    } else {
      std::cout << "  \"common_zeros\": null,\n";
    }
    std::cout << "  \"seconds\": " << seconds << ",\n";
    std::cout << "  \"combinations_per_second\": "
              << (seconds ? combinations / seconds : 0) << "\n";
    std::cout << "}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
