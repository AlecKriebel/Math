#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>

namespace {

constexpr int COLORS = 7;
constexpr std::array<int, COLORS> VALUES = {-4, -3, -2, -1, 0, 1, 2};
constexpr std::array<std::pair<int, int>, 10> EDGES = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {1, 2},
    {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4},
}};

long long determinant(const std::vector<std::vector<int>>& matrix) {
  const int n = static_cast<int>(matrix.size());
  std::vector<int> permutation(n);
  std::iota(permutation.begin(), permutation.end(), 0);
  long long answer = 0;
  do {
    int inversions = 0;
    long long product = 1;
    for (int i = 0; i < n; ++i) {
      product *= matrix[i][permutation[i]];
      for (int j = i + 1; j < n; ++j) {
        inversions += permutation[i] > permutation[j];
      }
    }
    answer += inversions % 2 ? -product : product;
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return answer;
}

int encode6(const std::array<int, 6>& edges) {
  int answer = 0;
  int multiplier = 1;
  for (int edge : edges) {
    answer += edge * multiplier;
    multiplier *= COLORS;
  }
  return answer;
}

std::uint32_t encode10(const std::array<int, 10>& edges) {
  std::uint32_t answer = 0;
  std::uint32_t multiplier = 1;
  for (int edge : edges) {
    answer += static_cast<std::uint32_t>(edge) * multiplier;
    multiplier *= COLORS;
  }
  return answer;
}

std::array<int, 6> decode6(int code) {
  std::array<int, 6> answer{};
  for (int& edge : answer) {
    edge = code % COLORS;
    code /= COLORS;
  }
  return answer;
}

std::array<int, 10> decode10(std::uint32_t code) {
  std::array<int, 10> answer{};
  for (int& edge : answer) {
    edge = code % COLORS;
    code /= COLORS;
  }
  return answer;
}

std::vector<std::vector<int>> gram4(const std::array<int, 6>& e) {
  return {
      {4, VALUES[e[0]], VALUES[e[1]], VALUES[e[2]]},
      {VALUES[e[0]], 4, VALUES[e[3]], VALUES[e[4]]},
      {VALUES[e[1]], VALUES[e[3]], 4, VALUES[e[5]]},
      {VALUES[e[2]], VALUES[e[4]], VALUES[e[5]], 4},
  };
}

std::vector<std::vector<int>> gram5(const std::array<int, 10>& e) {
  return {
      {4, VALUES[e[0]], VALUES[e[1]], VALUES[e[2]], VALUES[e[3]]},
      {VALUES[e[0]], 4, VALUES[e[4]], VALUES[e[5]], VALUES[e[6]]},
      {VALUES[e[1]], VALUES[e[4]], 4, VALUES[e[7]], VALUES[e[8]]},
      {VALUES[e[2]], VALUES[e[5]], VALUES[e[7]], 4, VALUES[e[9]]},
      {VALUES[e[3]], VALUES[e[6]], VALUES[e[8]], VALUES[e[9]], 4},
  };
}

int edge_index(int first, int second) {
  if (first > second) std::swap(first, second);
  for (int index = 0; index < 10; ++index) {
    if (EDGES[index].first == first && EDGES[index].second == second) {
      return index;
    }
  }
  return -1;
}

std::vector<std::array<int, 5>> permutations5() {
  std::array<int, 5> permutation = {0, 1, 2, 3, 4};
  std::vector<std::array<int, 5>> answer;
  do {
    answer.push_back(permutation);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return answer;
}

std::uint32_t transform_code(
    const std::array<int, 10>& edges,
    const std::array<int, 5>& permutation) {
  std::array<int, 10> transformed{};
  for (int position = 0; position < 10; ++position) {
    const auto [first, second] = EDGES[position];
    transformed[position] =
        edges[edge_index(permutation[first], permutation[second])];
  }
  return encode10(transformed);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: enumerate_k5_orbits OUTPUT.csv\n";
    return 2;
  }

  constexpr int K4_COUNT = 117649;       // 7^6
  constexpr std::uint32_t K5_COUNT = 282475249;  // 7^10
  std::vector<unsigned char> feasible4(K4_COUNT, 0);
  std::vector<std::array<int, 6>> feasible4_edges;
  for (int code = 0; code < K4_COUNT; ++code) {
    auto edges = decode6(code);
    bool triples_ok = true;
    const std::array<std::array<int, 3>, 4> faces = {{
        {edges[0], edges[1], edges[3]},
        {edges[0], edges[2], edges[4]},
        {edges[1], edges[2], edges[5]},
        {edges[3], edges[4], edges[5]},
    }};
    for (const auto& face : faces) {
      std::vector<std::vector<int>> gram = {
          {4, VALUES[face[0]], VALUES[face[1]]},
          {VALUES[face[0]], 4, VALUES[face[2]]},
          {VALUES[face[1]], VALUES[face[2]], 4},
      };
      if (determinant(gram) < 0) {
        triples_ok = false;
        break;
      }
    }
    if (!triples_ok || determinant(gram4(edges)) < 0) continue;
    feasible4[code] = 1;
    feasible4_edges.push_back(edges);
  }

  auto face_code = [](const std::array<int, 10>& e, int omitted) {
    switch (omitted) {
      case 0: return encode6({e[4], e[5], e[6], e[7], e[8], e[9]});
      case 1: return encode6({e[1], e[2], e[3], e[7], e[8], e[9]});
      case 2: return encode6({e[0], e[2], e[3], e[5], e[6], e[9]});
      case 3: return encode6({e[0], e[1], e[3], e[4], e[6], e[8]});
      default: return encode6({e[0], e[1], e[2], e[4], e[5], e[7]});
    }
  };

  std::vector<std::uint64_t> feasible_bits((K5_COUNT + 63) / 64, 0);
  std::uint64_t feasible_count = 0;
  for (const auto& base : feasible4_edges) {
    for (int a = 0; a < COLORS; ++a)
      for (int b = 0; b < COLORS; ++b)
        for (int c = 0; c < COLORS; ++c)
          for (int d = 0; d < COLORS; ++d) {
            std::array<int, 10> e = {
                base[0], base[1], base[2], a, base[3],
                base[4], b,       base[5], c, d,
            };
            bool faces_ok = true;
            for (int omitted = 0; omitted < 4; ++omitted) {
              if (!feasible4[face_code(e, omitted)]) {
                faces_ok = false;
                break;
              }
            }
            if (!faces_ok || determinant(gram5(e)) < 0) continue;
            const auto code = encode10(e);
            feasible_bits[code >> 6] |= std::uint64_t{1} << (code & 63);
            ++feasible_count;
          }
  }

  const auto permutations = permutations5();
  std::ofstream output(argv[1]);
  output << "# feasible_labeled_k5=" << feasible_count
         << " full_orbits=PENDING\n";
  std::uint64_t orbit_count = 0;
  std::uint64_t orbit_size_sum = 0;
  for (std::uint32_t code = 0; code < K5_COUNT; ++code) {
    const std::uint64_t mask = std::uint64_t{1} << (code & 63);
    if (!(feasible_bits[code >> 6] & mask)) continue;
    const auto edges = decode10(code);
    int automorphisms = 0;
    for (const auto& permutation : permutations) {
      const auto image = transform_code(edges, permutation);
      feasible_bits[image >> 6] &=
          ~(std::uint64_t{1} << (image & 63));
      if (image == code) ++automorphisms;
    }
    const int orbit_size = 120 / automorphisms;
    orbit_size_sum += orbit_size;
    ++orbit_count;
    output << code;
    for (int color : edges) output << ',' << color;
    output << ',' << automorphisms << '\n';
  }
  output.close();

  // Replace the provisional header deterministically.
  std::ifstream input(argv[1]);
  std::string ignored;
  std::getline(input, ignored);
  const std::string temporary = std::string(argv[1]) + ".tmp";
  std::ofstream corrected(temporary);
  corrected << "# feasible_labeled_k5=" << feasible_count
            << " full_orbits=" << orbit_count
            << " orbit_size_sum=" << orbit_size_sum << '\n';
  corrected << input.rdbuf();
  corrected.close();
  input.close();
  std::remove(argv[1]);
  std::rename(temporary.c_str(), argv[1]);

  std::cout << "feasible labeled K4: " << feasible4_edges.size() << '\n'
            << "feasible labeled K5: " << feasible_count << '\n'
            << "full K5 orbits: " << orbit_count << '\n'
            << "orbit-size sum: " << orbit_size_sum << '\n';
  return orbit_size_sum == feasible_count ? 0 : 3;
}
