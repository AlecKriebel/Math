#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>

namespace {

constexpr int COLORS = 7;
constexpr std::array<int, COLORS> VALUES = {-4, -3, -2, -1, 0, 1, 2};

long long determinant(const std::vector<std::vector<int>>& matrix) {
  const int n = static_cast<int>(matrix.size());
  std::vector<int> permutation(n);
  for (int i = 0; i < n; ++i) permutation[i] = i;
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

std::array<int, 6> decode6(int code) {
  std::array<int, 6> answer{};
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
  // Edge order 01,02,03,04,12,13,14,23,24,34.
  return {
      {4, VALUES[e[0]], VALUES[e[1]], VALUES[e[2]], VALUES[e[3]]},
      {VALUES[e[0]], 4, VALUES[e[4]], VALUES[e[5]], VALUES[e[6]]},
      {VALUES[e[1]], VALUES[e[4]], 4, VALUES[e[7]], VALUES[e[8]]},
      {VALUES[e[2]], VALUES[e[5]], VALUES[e[7]], 4, VALUES[e[9]]},
      {VALUES[e[3]], VALUES[e[6]], VALUES[e[8]], VALUES[e[9]], 4},
  };
}

std::array<int, 3> sorted3(int a, int b, int c) {
  std::array<int, 3> answer = {a, b, c};
  std::sort(answer.begin(), answer.end());
  return answer;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: enumerate_k5 OUTPUT.csv\n";
    return 2;
  }

  std::array<int, COLORS * COLORS * COLORS> triple_index{};
  triple_index.fill(-1);
  int triple_count = 0;
  for (int a = 0; a < COLORS; ++a) {
    for (int b = a; b < COLORS; ++b) {
      for (int c = b; c < COLORS; ++c) {
        std::vector<std::vector<int>> gram = {
            {4, VALUES[a], VALUES[b]},
            {VALUES[a], 4, VALUES[c]},
            {VALUES[b], VALUES[c], 4},
        };
        if (determinant(gram) >= 0) {
          triple_index[a + COLORS * b + COLORS * COLORS * c] = triple_count++;
        }
      }
    }
  }
  if (triple_count != 51) {
    std::cerr << "unexpected triple count " << triple_count << "\n";
    return 3;
  }

  constexpr int K4_COUNT = COLORS * COLORS * COLORS * COLORS * COLORS * COLORS;
  std::vector<unsigned char> feasible4(K4_COUNT, 0);
  std::vector<std::array<int, 6>> feasible4_edges;
  feasible4_edges.reserve(30000);
  for (int code = 0; code < K4_COUNT; ++code) {
    auto edges = decode6(code);
    auto f0 = sorted3(edges[0], edges[1], edges[3]);
    auto f1 = sorted3(edges[0], edges[2], edges[4]);
    auto f2 = sorted3(edges[1], edges[2], edges[5]);
    auto f3 = sorted3(edges[3], edges[4], edges[5]);
    auto index = [&](const std::array<int, 3>& f) {
      return triple_index[f[0] + COLORS * f[1] + COLORS * COLORS * f[2]];
    };
    if (index(f0) < 0 || index(f1) < 0 || index(f2) < 0 || index(f3) < 0) {
      continue;
    }
    if (determinant(gram4(edges)) < 0) continue;
    feasible4[code] = 1;
    feasible4_edges.push_back(edges);
  }

  std::unordered_map<std::uint64_t, std::array<unsigned char, 10>> features;
  features.reserve(1000000);
  std::uint64_t feasible5_count = 0;

  auto face_code = [](const std::array<int, 10>& e, int omitted) {
    // Edge order in e: 01,02,03,04,12,13,14,23,24,34.
    switch (omitted) {
      case 0: return encode6({e[4], e[5], e[6], e[7], e[8], e[9]});
      case 1: return encode6({e[1], e[2], e[3], e[7], e[8], e[9]});
      case 2: return encode6({e[0], e[2], e[3], e[5], e[6], e[9]});
      case 3: return encode6({e[0], e[1], e[3], e[4], e[6], e[8]});
      default: return encode6({e[0], e[1], e[2], e[4], e[5], e[7]});
    }
  };

  auto triangle_ids = [&](const std::array<int, 10>& e) {
    std::array<int, 10> ids = {
        triple_index[sorted3(e[0], e[1], e[4])[0] +
                     COLORS * sorted3(e[0], e[1], e[4])[1] +
                     COLORS * COLORS * sorted3(e[0], e[1], e[4])[2]],
        triple_index[sorted3(e[0], e[2], e[5])[0] +
                     COLORS * sorted3(e[0], e[2], e[5])[1] +
                     COLORS * COLORS * sorted3(e[0], e[2], e[5])[2]],
        triple_index[sorted3(e[0], e[3], e[6])[0] +
                     COLORS * sorted3(e[0], e[3], e[6])[1] +
                     COLORS * COLORS * sorted3(e[0], e[3], e[6])[2]],
        triple_index[sorted3(e[1], e[2], e[7])[0] +
                     COLORS * sorted3(e[1], e[2], e[7])[1] +
                     COLORS * COLORS * sorted3(e[1], e[2], e[7])[2]],
        triple_index[sorted3(e[1], e[3], e[8])[0] +
                     COLORS * sorted3(e[1], e[3], e[8])[1] +
                     COLORS * COLORS * sorted3(e[1], e[3], e[8])[2]],
        triple_index[sorted3(e[2], e[3], e[9])[0] +
                     COLORS * sorted3(e[2], e[3], e[9])[1] +
                     COLORS * COLORS * sorted3(e[2], e[3], e[9])[2]],
        triple_index[sorted3(e[4], e[5], e[7])[0] +
                     COLORS * sorted3(e[4], e[5], e[7])[1] +
                     COLORS * COLORS * sorted3(e[4], e[5], e[7])[2]],
        triple_index[sorted3(e[4], e[6], e[8])[0] +
                     COLORS * sorted3(e[4], e[6], e[8])[1] +
                     COLORS * COLORS * sorted3(e[4], e[6], e[8])[2]],
        triple_index[sorted3(e[5], e[6], e[9])[0] +
                     COLORS * sorted3(e[5], e[6], e[9])[1] +
                     COLORS * COLORS * sorted3(e[5], e[6], e[9])[2]],
        triple_index[sorted3(e[7], e[8], e[9])[0] +
                     COLORS * sorted3(e[7], e[8], e[9])[1] +
                     COLORS * COLORS * sorted3(e[7], e[8], e[9])[2]],
    };
    std::sort(ids.begin(), ids.end());
    return ids;
  };

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
            ++feasible5_count;
            auto ids = triangle_ids(e);
            std::uint64_t key = 0;
            for (int id : ids) key = (key << 6) | static_cast<unsigned>(id);
            if (features.find(key) == features.end()) {
              std::array<unsigned char, 10> compact{};
              for (int i = 0; i < 10; ++i) compact[i] = e[i];
              features.emplace(key, compact);
            }
          }
  }

  std::ofstream output(argv[1]);
  output << "# feasible_labeled_k5=" << feasible5_count
         << " distinct_triangle_count_vectors=" << features.size() << "\n";
  std::vector<std::pair<std::uint64_t, std::array<unsigned char, 10>>>
      sorted_features(features.begin(), features.end());
  std::sort(
      sorted_features.begin(), sorted_features.end(),
      [](const auto& left, const auto& right) {
        return left.first < right.first;
      });
  for (const auto& [key, edges] : sorted_features) {
    output << key;
    for (unsigned char edge : edges) output << ',' << static_cast<int>(edge);
    output << '\n';
  }
  std::cout << "feasible labeled K4: " << feasible4_edges.size() << "\n"
            << "feasible labeled K5: " << feasible5_count << "\n"
            << "distinct triangle-count vectors: " << features.size() << "\n";
}
