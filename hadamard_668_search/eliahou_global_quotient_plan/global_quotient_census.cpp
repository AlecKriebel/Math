// Production range kernel for the complete case-26 quotient census.
//
// The packed modular join is shared with benchmark_global_quotient.cpp.
// Every modular survivor is reconstructed, evaluated in the exact integer
// quadratic, and independently replayed from four bit-packed physical rows.

#define H668_GQ_NO_MAIN
#include "benchmark_global_quotient.cpp"

#include <cmath>
#include <iomanip>
#include <sstream>

namespace {

class Sha256 {
 public:
  Sha256() { reset(); }

  void update(const void* data, std::size_t length) {
    const auto* bytes = static_cast<const std::uint8_t*>(data);
    total_bytes_ += length;
    while (length) {
      const std::size_t take =
          std::min(length, block_.size() - block_size_);
      std::memcpy(block_.data() + block_size_, bytes, take);
      block_size_ += take;
      bytes += take;
      length -= take;
      if (block_size_ == block_.size()) {
        transform(block_.data());
        block_size_ = 0;
      }
    }
  }

  template <typename T>
  void update_little_endian(T value) {
    static_assert(std::is_integral_v<T>);
    using Unsigned = std::make_unsigned_t<T>;
    Unsigned encoded = static_cast<Unsigned>(value);
    std::array<std::uint8_t, sizeof(T)> bytes{};
    for (std::size_t index = 0; index < bytes.size(); ++index) {
      bytes[index] = static_cast<std::uint8_t>(
          (encoded >> (8 * index)) & 0xff);
    }
    update(bytes.data(), bytes.size());
  }

  std::string hex_digest() {
    const std::uint64_t bit_length = total_bytes_ * 8;
    const std::uint8_t marker = 0x80;
    update(&marker, 1);
    const std::uint8_t zero = 0;
    while (block_size_ != 56) update(&zero, 1);
    std::array<std::uint8_t, 8> length_bytes{};
    for (int index = 0; index < 8; ++index) {
      length_bytes[7 - index] = static_cast<std::uint8_t>(
          (bit_length >> (8 * index)) & 0xff);
    }
    update(length_bytes.data(), length_bytes.size());
    if (block_size_ != 0) {
      throw std::runtime_error("SHA-256 finalization failed");
    }
    std::ostringstream output;
    output << std::hex << std::setfill('0');
    for (std::uint32_t word : state_) {
      output << std::setw(8) << word;
    }
    return output.str();
  }

 private:
  std::array<std::uint32_t, 8> state_{};
  std::array<std::uint8_t, 64> block_{};
  std::size_t block_size_ = 0;
  std::uint64_t total_bytes_ = 0;

  static std::uint32_t rotate_right(
      std::uint32_t value, int amount) {
    return (value >> amount) | (value << (32 - amount));
  }

  void reset() {
    state_ = {
        0x6a09e667U, 0xbb67ae85U, 0x3c6ef372U, 0xa54ff53aU,
        0x510e527fU, 0x9b05688cU, 0x1f83d9abU, 0x5be0cd19U};
    block_size_ = 0;
    total_bytes_ = 0;
  }

  void transform(const std::uint8_t* block) {
    static constexpr std::array<std::uint32_t, 64> constants = {
        0x428a2f98U, 0x71374491U, 0xb5c0fbcfU, 0xe9b5dba5U,
        0x3956c25bU, 0x59f111f1U, 0x923f82a4U, 0xab1c5ed5U,
        0xd807aa98U, 0x12835b01U, 0x243185beU, 0x550c7dc3U,
        0x72be5d74U, 0x80deb1feU, 0x9bdc06a7U, 0xc19bf174U,
        0xe49b69c1U, 0xefbe4786U, 0x0fc19dc6U, 0x240ca1ccU,
        0x2de92c6fU, 0x4a7484aaU, 0x5cb0a9dcU, 0x76f988daU,
        0x983e5152U, 0xa831c66dU, 0xb00327c8U, 0xbf597fc7U,
        0xc6e00bf3U, 0xd5a79147U, 0x06ca6351U, 0x14292967U,
        0x27b70a85U, 0x2e1b2138U, 0x4d2c6dfcU, 0x53380d13U,
        0x650a7354U, 0x766a0abbU, 0x81c2c92eU, 0x92722c85U,
        0xa2bfe8a1U, 0xa81a664bU, 0xc24b8b70U, 0xc76c51a3U,
        0xd192e819U, 0xd6990624U, 0xf40e3585U, 0x106aa070U,
        0x19a4c116U, 0x1e376c08U, 0x2748774cU, 0x34b0bcb5U,
        0x391c0cb3U, 0x4ed8aa4aU, 0x5b9cca4fU, 0x682e6ff3U,
        0x748f82eeU, 0x78a5636fU, 0x84c87814U, 0x8cc70208U,
        0x90befffaU, 0xa4506cebU, 0xbef9a3f7U, 0xc67178f2U};
    std::array<std::uint32_t, 64> words{};
    for (int index = 0; index < 16; ++index) {
      words[index] =
          (std::uint32_t(block[4 * index]) << 24) |
          (std::uint32_t(block[4 * index + 1]) << 16) |
          (std::uint32_t(block[4 * index + 2]) << 8) |
          std::uint32_t(block[4 * index + 3]);
    }
    for (int index = 16; index < 64; ++index) {
      const std::uint32_t small_zero =
          rotate_right(words[index - 15], 7) ^
          rotate_right(words[index - 15], 18) ^
          (words[index - 15] >> 3);
      const std::uint32_t small_one =
          rotate_right(words[index - 2], 17) ^
          rotate_right(words[index - 2], 19) ^
          (words[index - 2] >> 10);
      words[index] = words[index - 16] + small_zero +
                     words[index - 7] + small_one;
    }
    std::uint32_t a = state_[0];
    std::uint32_t b = state_[1];
    std::uint32_t c = state_[2];
    std::uint32_t d = state_[3];
    std::uint32_t e = state_[4];
    std::uint32_t f = state_[5];
    std::uint32_t g = state_[6];
    std::uint32_t h = state_[7];
    for (int index = 0; index < 64; ++index) {
      const std::uint32_t big_one =
          rotate_right(e, 6) ^ rotate_right(e, 11) ^
          rotate_right(e, 25);
      const std::uint32_t choice = (e & f) ^ (~e & g);
      const std::uint32_t first =
          h + big_one + choice + constants[index] + words[index];
      const std::uint32_t big_zero =
          rotate_right(a, 2) ^ rotate_right(a, 13) ^
          rotate_right(a, 22);
      const std::uint32_t majority =
          (a & b) ^ (a & c) ^ (b & c);
      const std::uint32_t second = big_zero + majority;
      h = g;
      g = f;
      f = e;
      e = d + first;
      d = c;
      c = b;
      b = a;
      a = first + second;
    }
    state_[0] += a;
    state_[1] += b;
    state_[2] += c;
    state_[3] += d;
    state_[4] += e;
    state_[5] += f;
    state_[6] += g;
    state_[7] += h;
  }
};

struct RowBits {
  std::uint64_t nonzero = 0;
  std::uint64_t negative = 0;
  std::uint64_t magnitude_one = 0;
};

struct DetailedRecord {
  std::uint32_t quotient_index = 0;
  std::uint8_t central_value = 0;
  std::uint64_t pair_state = 0;
  std::array<std::int32_t, EQUATIONS> residual{};
  int nonzero_lags = 0;
  int l1 = 0;
  int linf = 0;

  bool score_less(const DetailedRecord& other) const {
    return std::tie(
               nonzero_lags, l1, linf, quotient_index,
               central_value, pair_state) <
           std::tie(
               other.nonzero_lags, other.l1, other.linf,
               other.quotient_index, other.central_value,
               other.pair_state);
  }
};

class ExactReplay {
 public:
  explicit ExactReplay(const Model& model) : model_(model) {
    for (int row = 0; row < 4; ++row) {
      for (int cell = 0; cell < 42; ++cell) {
        const int value = model_.physical_rows[row * 42 + cell];
        if (value == 0) continue;
        base_rows_[row].nonzero |= 1ULL << cell;
        if (value < 0) base_rows_[row].negative |= 1ULL << cell;
        if (std::abs(value) == 1) {
          base_rows_[row].magnitude_one |= 1ULL << cell;
        } else if (std::abs(value) != 2) {
          throw std::runtime_error(
              "physical row has an unsupported magnitude");
        }
      }
    }
  }

  DetailedRecord evaluate(
      std::uint32_t quotient_index,
      const std::array<std::uint8_t, PAIRS>& parity,
      const SurvivorState& survivor) const {
    std::array<std::uint8_t, VARIABLES> support{};
    for (int pair = 0; pair < PAIRS; ++pair) {
      const int y = (survivor.pair_state >> pair) & 1ULL;
      const int left = model_.pairs[2 * pair];
      const int right = model_.pairs[2 * pair + 1];
      if (parity[pair]) {
        support[left] = static_cast<std::uint8_t>(1 - y);
        support[right] = static_cast<std::uint8_t>(y);
      } else {
        support[left] = static_cast<std::uint8_t>(y);
        support[right] = static_cast<std::uint8_t>(y);
      }
    }
    if (std::count(support.begin(), support.end(), 1) != 39) {
      throw std::runtime_error(
          "reconstructed support has the wrong weight");
    }

    std::array<std::int32_t, EQUATIONS> polynomial{};
    for (int equation = 0; equation < EQUATIONS; ++equation) {
      polynomial[equation] = model_.constant[equation];
      for (int variable = 0; variable < VARIABLES; ++variable) {
        if (support[variable]) {
          polynomial[equation] +=
              model_.linear[equation * VARIABLES + variable];
        }
      }
      for (int left = 0; left < VARIABLES; ++left) {
        if (!support[left]) continue;
        for (int right = left + 1; right < VARIABLES; ++right) {
          if (!support[right]) continue;
          const auto offset =
              (equation * VARIABLES + left) * VARIABLES + right;
          polynomial[equation] += model_.quadratic[offset];
        }
      }
    }

    auto rows = base_rows_;
    for (int variable = 0; variable < VARIABLES; ++variable) {
      if (!support[variable]) continue;
      const int first_row =
          model_.variable_blocks[variable] == 0 ? 0 : 2;
      const std::uint64_t keep =
          ~(1ULL << model_.variable_cells[variable]);
      for (int row : {first_row, first_row + 1}) {
        rows[row].nonzero &= keep;
        rows[row].negative &= keep;
        rows[row].magnitude_one &= keep;
      }
    }

    int energy = 0;
    for (const RowBits& row : rows) {
      const int ones = std::popcount(row.magnitude_one);
      const int twos =
          std::popcount(row.nonzero) - ones;
      energy += ones + 4 * twos;
    }
    if (energy != 334) {
      throw std::runtime_error("physical replay has wrong energy");
    }

    std::array<std::int32_t, EQUATIONS> physical{};
    for (int lag = 1; lag <= EQUATIONS; ++lag) {
      int correlation = 0;
      for (const RowBits& row : rows) {
        correlation += shifted_dot(row, lag);
      }
      if (correlation % 4 != 0) {
        throw std::runtime_error(
            "physical residual lost integer content four");
      }
      physical[lag - 1] = correlation / 4;
    }
    if (physical != polynomial) {
      throw std::runtime_error(
          "integer polynomial and bit-packed replay disagree");
    }

    DetailedRecord record;
    record.quotient_index = quotient_index;
    record.central_value = survivor.central_value;
    record.pair_state = survivor.pair_state;
    record.residual = physical;
    for (int value : physical) {
      if (value % 6 != 0) {
        throw std::runtime_error(
            "join emitted a non-mod-6 physical support");
      }
      record.nonzero_lags += value != 0;
      record.l1 += std::abs(value);
      record.linf = std::max(record.linf, std::abs(value));
    }
    return record;
  }

 private:
  const Model& model_;
  std::array<RowBits, 4> base_rows_{};

  static int signed_weight(
      std::uint64_t mask, std::uint64_t negative) {
    return std::popcount(mask) -
           2 * std::popcount(mask & negative);
  }

  static int aligned_dot(
      std::uint64_t left_nonzero,
      std::uint64_t left_negative,
      std::uint64_t left_one,
      std::uint64_t right_nonzero,
      std::uint64_t right_negative,
      std::uint64_t right_one,
      std::uint64_t mask) {
    const std::uint64_t valid =
        left_nonzero & right_nonzero & mask;
    const std::uint64_t negative =
        (left_negative ^ right_negative) & valid;
    const std::uint64_t both_one =
        valid & left_one & right_one;
    const std::uint64_t one_one =
        valid & (left_one ^ right_one);
    const std::uint64_t both_two =
        valid & ~(both_one | one_one);
    return signed_weight(both_one, negative) +
           2 * signed_weight(one_one, negative) +
           4 * signed_weight(both_two, negative);
  }

  static int shifted_dot(const RowBits& row, int lag) {
    const int straight_width = 42 - lag;
    const std::uint64_t straight_mask =
        (1ULL << straight_width) - 1;
    const int straight = aligned_dot(
        row.nonzero >> lag,
        row.negative >> lag,
        row.magnitude_one >> lag,
        row.nonzero,
        row.negative,
        row.magnitude_one,
        straight_mask);
    const std::uint64_t wrap_mask = (1ULL << lag) - 1;
    const int wrap = aligned_dot(
        row.nonzero,
        row.negative,
        row.magnitude_one,
        row.nonzero >> straight_width,
        row.negative >> straight_width,
        row.magnitude_one >> straight_width,
        wrap_mask);
    return straight - wrap;
  }
};

void digest_record(Sha256& digest, const DetailedRecord& record) {
  digest.update_little_endian(record.quotient_index);
  digest.update_little_endian(record.central_value);
  digest.update_little_endian(record.pair_state);
  for (int value : record.residual) {
    if (
        value < std::numeric_limits<std::int16_t>::min() ||
        value > std::numeric_limits<std::int16_t>::max()) {
      throw std::runtime_error(
          "normalized residual does not fit int16");
    }
    digest.update_little_endian(
        static_cast<std::int16_t>(value));
  }
}

std::string residual_json(
    const std::array<std::int32_t, EQUATIONS>& values) {
  std::ostringstream output;
  output << "[";
  for (int index = 0; index < EQUATIONS; ++index) {
    if (index) output << ",";
    output << values[index];
  }
  output << "]";
  return output.str();
}

std::string record_json(const DetailedRecord& record) {
  std::ostringstream output;
  output << "{"
         << "\"quotient_index\":" << record.quotient_index << ","
         << "\"central_value\":"
         << static_cast<int>(record.central_value) << ","
         << "\"pair_state\":" << record.pair_state << ","
         << "\"normalized_residuals\":"
         << residual_json(record.residual) << ","
         << "\"nonzero_lags\":" << record.nonzero_lags << ","
         << "\"l1\":" << record.l1 << ","
         << "\"linf\":" << record.linf
         << "}";
  return output.str();
}

bool valid_hash(const std::string& value) {
  if (value.size() != 64) return false;
  return std::all_of(
      value.begin(), value.end(), [](unsigned char character) {
        return (character >= '0' && character <= '9') ||
               (character >= 'a' && character <= 'f');
      });
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 12) {
      std::cerr
          << "usage: " << argv[0]
          << " MODEL --start I --states N --source-sha HEX"
             " --model-sha HEX --mode gauged|ungauged\n";
      return 2;
    }
    const std::string model_path = argv[1];
    std::uint32_t start = 0;
    std::uint32_t states = 0;
    std::string source_sha;
    std::string model_sha;
    std::string mode;
    for (int argument = 2; argument < argc; argument += 2) {
      const std::string option = argv[argument];
      if (option == "--start") {
        start = static_cast<std::uint32_t>(
            std::stoul(argv[argument + 1]));
      } else if (option == "--states") {
        states = static_cast<std::uint32_t>(
            std::stoul(argv[argument + 1]));
      } else if (option == "--source-sha") {
        source_sha = argv[argument + 1];
      } else if (option == "--model-sha") {
        model_sha = argv[argument + 1];
      } else if (option == "--mode") {
        mode = argv[argument + 1];
      } else {
        throw std::runtime_error("invalid command-line option");
      }
    }
    if (
        states == 0 || start >= (1U << QUOTIENT_DIMENSION) ||
        states > (1U << QUOTIENT_DIMENSION) - start) {
      throw std::runtime_error("requested quotient range is invalid");
    }
    if (!valid_hash(source_sha) || !valid_hash(model_sha)) {
      throw std::runtime_error("source/model hash is malformed");
    }
    if (mode != "gauged" && mode != "ungauged") {
      throw std::runtime_error(
          "mode must be gauged or ungauged");
    }
    const bool reflection_gauge = mode == "gauged";

    {
      Sha256 self_test;
      const std::string abc = "abc";
      self_test.update(abc.data(), abc.size());
      if (
          self_test.hex_digest() !=
          "ba7816bf8f01cfea414140de5dae2223"
          "b00361a396177a9cb410ff61f20015ad") {
        throw std::runtime_error("SHA-256 self-test failed");
      }
    }

    Model model = read_model(model_path);
    Kernel kernel(model);
    ExactReplay replay(model);
    Sha256 survivor_digest;
    std::uint64_t survivor_count = 0;
    std::uint64_t representative_count = 0;
    std::uint64_t exact_count = 0;
    std::vector<DetailedRecord> exact_records;
    DetailedRecord best;
    bool have_best = false;

    const auto started = std::chrono::steady_clock::now();
    for (std::uint32_t offset = 0; offset < states; ++offset) {
      const std::uint32_t quotient_index = start + offset;
      const auto parity = quotient_point(model, quotient_index);
      int gauge_pair = -1;
      if (reflection_gauge) {
        for (int pair = 0; pair < PAIRS; ++pair) {
          if (
              pair != static_cast<int>(model.central) &&
              model.pair_blocks[pair] == 0 && parity[pair] == 1) {
            gauge_pair = pair;
            break;
          }
        }
        if (gauge_pair < 0) {
          throw std::runtime_error(
              "quotient has no odd noncentral L gauge pair");
        }
      }
      std::vector<SurvivorState> representatives;
      const std::uint64_t joined =
          kernel.census_one(parity, &representatives, gauge_pair);
      if (joined != representatives.size()) {
        throw std::runtime_error(
            "survivor reconstruction changed the join count");
      }
      representative_count += representatives.size();
      std::vector<SurvivorState> survivors;
      if (reflection_gauge) {
        std::uint64_t reflection_mask = 0;
        for (int pair = 0; pair < PAIRS; ++pair) {
          if (
              pair != static_cast<int>(model.central) &&
              parity[pair]) {
            reflection_mask |= 1ULL << pair;
          }
        }
        survivors.reserve(2 * representatives.size());
        for (const SurvivorState& representative : representatives) {
          if ((representative.pair_state >> gauge_pair) & 1ULL) {
            throw std::runtime_error(
                "gauge representative violates y_g=0");
          }
          survivors.push_back(representative);
          survivors.push_back(
              SurvivorState{
                  representative.central_value,
                  representative.pair_state ^ reflection_mask});
        }
      } else {
        survivors = std::move(representatives);
      }
      std::sort(survivors.begin(), survivors.end());
      if (
          std::adjacent_find(survivors.begin(), survivors.end(),
                             [](const SurvivorState& left,
                                const SurvivorState& right) {
                               return left.central_value ==
                                          right.central_value &&
                                      left.pair_state ==
                                          right.pair_state;
                             }) != survivors.end()) {
        throw std::runtime_error(
            "the join emitted a duplicate support");
      }
      for (const SurvivorState& survivor : survivors) {
        DetailedRecord record =
            replay.evaluate(quotient_index, parity, survivor);
        digest_record(survivor_digest, record);
        ++survivor_count;
        if (record.nonzero_lags == 0) {
          ++exact_count;
          exact_records.push_back(record);
        }
        if (!have_best || record.score_less(best)) {
          best = record;
          have_best = true;
        }
      }
    }
    const double seconds =
        std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started)
            .count();
    const std::uint64_t join_rows =
        std::uint64_t(states) *
        ((reflection_gauge ? (1U << 19) : (1U << 20)) +
         (1U << 18)) *
        2;

    std::cout
        << "{\n"
        << "  \"schema\": "
           "\"h668-case26-global-quotient-range-v1\",\n"
        << "  \"status\": \"complete\",\n"
        << "  \"case\": 26,\n"
        << "  \"block\": \"S\",\n"
        << "  \"q_index\": 12,\n"
        << "  \"start\": " << start << ",\n"
        << "  \"states\": " << states << ",\n"
        << "  \"stop\": " << (start + states) << ",\n"
        << "  \"central_values_per_state\": 2,\n"
        << "  \"reflection_gauge\": "
        << (reflection_gauge ? "true" : "false") << ",\n"
        << "  \"reflection_gauge_rule\": "
           "\"lowest-index odd noncentral L pair has y=0\",\n"
        << "  \"joined_representatives\": "
        << representative_count << ",\n"
        << "  \"reconstructed_reflection_mates\": "
        << (reflection_gauge ? representative_count : 0) << ",\n"
        << "  \"join_rows\": " << join_rows << ",\n"
        << "  \"joint_mod6_supports\": " << survivor_count << ",\n"
        << "  \"exact_integer_supports\": " << exact_count << ",\n"
        << "  \"integer_polynomial_checks\": "
        << survivor_count << ",\n"
        << "  \"bitpacked_physical_replays\": "
        << survivor_count << ",\n"
        << "  \"survivor_stream_sha256\": \""
        << survivor_digest.hex_digest() << "\",\n"
        << "  \"producer_sources_sha256\": \""
        << source_sha << "\",\n"
        << "  \"model_sha256\": \"" << model_sha << "\",\n"
        << "  \"kernel_seconds\": " << std::setprecision(12)
        << seconds << ",\n"
        << "  \"join_rows_per_second\": "
        << (join_rows / seconds) << ",\n"
        << "  \"best_witness\": "
        << (have_best ? record_json(best) : "null") << ",\n"
        << "  \"exact_candidates\": [";
    for (std::size_t index = 0; index < exact_records.size(); ++index) {
      if (index) std::cout << ",";
      std::cout << record_json(exact_records[index]);
    }
    std::cout << "]\n}\n";
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
  return 0;
}
