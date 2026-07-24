// Construct rank-five PSD K6 triangle-count columns from the K5 catalog.
//
// This is a discovery search, not a complete K6 enumeration.  The K5 input
// stores one representative for each attained triangle-count vector, not
// every K5 orbit.  A positive result is a valid local K6 construction; a
// negative result from this subcatalog proves nothing.

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

static constexpr std::array<int, 7> VALUES = {{-4, -3, -2, -1, 0, 1, 2}};
static constexpr std::array<std::pair<int, int>, 10> PAIRS5 = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {1, 2},
    {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4},
}};
static constexpr std::array<std::pair<int, int>, 15> PAIRS6 = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5},
    {1, 2}, {1, 3}, {1, 4}, {1, 5}, {2, 3},
    {2, 4}, {2, 5}, {3, 4}, {3, 5}, {4, 5},
}};
using Edges5 = std::array<int, 10>;
using Edges6 = std::array<int, 15>;
using Matrix5 = std::array<std::array<std::int64_t, 5>, 5>;

std::int64_t determinant(
    const std::vector<std::vector<std::int64_t>>& matrix
) {
    const int size = static_cast<int>(matrix.size());
    std::vector<int> permutation(size);
    for (int i = 0; i < size; ++i) permutation[i] = i;
    std::int64_t total = 0;
    do {
        int inversions = 0;
        std::int64_t product = 1;
        for (int i = 0; i < size; ++i) {
            product *= matrix[i][permutation[i]];
            for (int j = i + 1; j < size; ++j)
                inversions += permutation[i] > permutation[j];
        }
        total += inversions % 2 ? -product : product;
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return total;
}

Matrix5 gram5(const Edges5& edges) {
    Matrix5 matrix{};
    for (int i = 0; i < 5; ++i) matrix[i][i] = 4;
    for (int index = 0; index < 10; ++index) {
        const auto [i, j] = PAIRS5[index];
        matrix[i][j] = VALUES[edges[index]];
        matrix[j][i] = VALUES[edges[index]];
    }
    return matrix;
}

std::int64_t det5(const Matrix5& matrix) {
    std::vector<std::vector<std::int64_t>> dynamic(
        5, std::vector<std::int64_t>(5)
    );
    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < 5; ++j) dynamic[i][j] = matrix[i][j];
    return determinant(dynamic);
}

std::array<std::array<std::int64_t, 5>, 5> adjugate(
    const Matrix5& matrix
) {
    std::array<std::array<std::int64_t, 5>, 5> answer{};
    for (int row = 0; row < 5; ++row) {
        for (int column = 0; column < 5; ++column) {
            std::vector<std::vector<std::int64_t>> minor;
            for (int i = 0; i < 5; ++i) {
                if (i == column) continue;  // transpose cofactor indices
                std::vector<std::int64_t> minor_row;
                for (int j = 0; j < 5; ++j) {
                    if (j != row) minor_row.push_back(matrix[i][j]);
                }
                minor.push_back(std::move(minor_row));
            }
            answer[row][column] =
                ((row + column) % 2 ? -1 : 1) * determinant(minor);
        }
    }
    return answer;
}

int pair_index6(int a, int b) {
    if (a > b) std::swap(a, b);
    for (int index = 0; index < 15; ++index)
        if (PAIRS6[index] == std::pair<int, int>{a, b}) return index;
    std::abort();
}

struct FeatureKey {
    std::uint64_t low;
    std::uint64_t high;
    bool operator==(const FeatureKey&) const = default;
};

struct FeatureHash {
    std::size_t operator()(const FeatureKey& key) const {
        std::uint64_t value =
            key.low ^ (key.high + 0x9e3779b97f4a7c15ULL
                       + (key.low << 6) + (key.low >> 2));
        return static_cast<std::size_t>(value);
    }
};

FeatureKey triangle_feature(
    const Edges6& edges, const std::array<int, 343>& triple_index
) {
    std::array<int, 20> ids{};
    int cursor = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j) {
            for (int k = j + 1; k < 6; ++k) {
                std::array<int, 3> colors = {{
                    edges[pair_index6(i, j)],
                    edges[pair_index6(i, k)],
                    edges[pair_index6(j, k)],
                }};
                std::sort(colors.begin(), colors.end());
                const int code = colors[0] + 7 * colors[1] + 49 * colors[2];
                const int id = triple_index[code];
                if (id < 0) std::abort();
                ids[cursor++] = id;
            }
        }
    }
    std::sort(ids.begin(), ids.end());
    FeatureKey key{0, 0};
    for (int i = 0; i < 10; ++i) key.low = (key.low << 6) | ids[i];
    for (int i = 10; i < 20; ++i) key.high = (key.high << 6) | ids[i];
    return key;
}

std::array<int, 20> decode_feature(const FeatureKey& key) {
    std::array<int, 20> ids{};
    std::uint64_t low = key.low;
    std::uint64_t high = key.high;
    for (int i = 9; i >= 0; --i) {
        ids[i] = low & 63;
        low >>= 6;
    }
    for (int i = 19; i >= 10; --i) {
        ids[i] = high & 63;
        high >>= 6;
    }
    return ids;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "usage: search_direct_k6_triangle K5.csv MAX_BASES OUTPUT.csv\n";
        return 2;
    }
    const int requested = std::stoi(argv[2]);
    std::ifstream input(argv[1]);
    if (!input || requested <= 0) return 3;
    std::string line;
    std::getline(input, line);
    std::vector<Edges5> positive_definite;
    while (std::getline(input, line)) {
        std::replace(line.begin(), line.end(), ',', ' ');
        std::istringstream fields(line);
        std::uint64_t ignored_key;
        Edges5 edges{};
        fields >> ignored_key;
        for (int& color : edges) fields >> color;
        if (!fields) return 4;
        if (det5(gram5(edges)) > 0) positive_definite.push_back(edges);
    }
    if (positive_definite.size() != 101272) return 5;
    const int selected_count =
        std::min(requested, static_cast<int>(positive_definite.size()));

    std::array<int, 343> triple_index{};
    triple_index.fill(-1);
    int triple_count = 0;
    for (int a = 0; a < 7; ++a) {
        for (int b = a; b < 7; ++b) {
            for (int c = b; c < 7; ++c) {
                std::vector<std::vector<std::int64_t>> matrix = {
                    {4, VALUES[a], VALUES[b]},
                    {VALUES[a], 4, VALUES[c]},
                    {VALUES[b], VALUES[c], 4},
                };
                if (determinant(matrix) >= 0)
                    triple_index[a + 7 * b + 49 * c] = triple_count++;
            }
        }
    }
    if (triple_count != 51) return 6;

    std::unordered_map<FeatureKey, Edges6, FeatureHash> features;
    features.reserve(static_cast<std::size_t>(selected_count) * 20);
    std::uint64_t quadratic_rows = 0;
    std::uint64_t rank_five_labeled = 0;
    for (int selected = 0; selected < selected_count; ++selected) {
        const std::size_t base_index =
            (static_cast<std::uint64_t>(selected)
             * positive_definite.size()) / selected_count;
        const Edges5& base = positive_definite[base_index];
        const Matrix5 matrix = gram5(base);
        const std::int64_t base_determinant = det5(matrix);
        const auto adj = adjugate(matrix);
        Edges6 edges{};
        for (int index = 0; index < 10; ++index) {
            const auto [i, j] = PAIRS5[index];
            edges[pair_index6(i, j)] = base[index];
        }
        std::array<std::int64_t, 5> z{};
        for (int c0 = 0; c0 < 7; ++c0) {
            z[0] = VALUES[c0];
            edges[pair_index6(0, 5)] = c0;
            for (int c1 = 0; c1 < 7; ++c1) {
                z[1] = VALUES[c1];
                edges[pair_index6(1, 5)] = c1;
                for (int c2 = 0; c2 < 7; ++c2) {
                    z[2] = VALUES[c2];
                    edges[pair_index6(2, 5)] = c2;
                    for (int c3 = 0; c3 < 7; ++c3) {
                        z[3] = VALUES[c3];
                        edges[pair_index6(3, 5)] = c3;
                        ++quadratic_rows;
                        std::int64_t constant = -4 * base_determinant;
                        for (int i = 0; i < 4; ++i)
                            for (int j = 0; j < 4; ++j)
                                constant += z[i] * adj[i][j] * z[j];
                        std::int64_t linear = 0;
                        for (int i = 0; i < 4; ++i)
                            linear += 2 * z[i] * adj[i][4];
                        const std::int64_t quadratic = adj[4][4];
                        for (int c4 = 0; c4 < 7; ++c4) {
                            const std::int64_t x = VALUES[c4];
                            if (quadratic * x * x + linear * x + constant != 0)
                                continue;
                            ++rank_five_labeled;
                            edges[pair_index6(4, 5)] = c4;
                            features.emplace(
                                triangle_feature(edges, triple_index), edges
                            );
                        }
                    }
                }
            }
        }
        if ((selected + 1) % 1000 == 0) {
            std::cerr << "bases=" << (selected + 1)
                      << " rank5=" << rank_five_labeled
                      << " features=" << features.size() << "\n";
        }
    }

    std::vector<std::pair<FeatureKey, Edges6>> sorted(
        features.begin(), features.end()
    );
    std::sort(sorted.begin(), sorted.end(), [](const auto& left, const auto& right) {
        if (left.first.high != right.first.high)
            return left.first.high < right.first.high;
        return left.first.low < right.first.low;
    });
    std::ofstream output(argv[3]);
    if (!output) return 7;
    output << "# positive_definite_k5_catalog=101272"
           << " selected_bases=" << selected_count
           << " quadratic_rows=" << quadratic_rows
           << " rank_five_labeled=" << rank_five_labeled
           << " distinct_triangle_count_vectors=" << sorted.size() << "\n";
    for (const auto& [key, edges] : sorted) {
        bool first = true;
        for (int color : edges) {
            if (!first) output << ',';
            output << color;
            first = false;
        }
        for (int id : decode_feature(key)) output << ',' << id;
        output << '\n';
    }
    std::cerr << "done bases=" << selected_count
              << " rank5=" << rank_five_labeled
              << " features=" << sorted.size() << "\n";
    return 0;
}
