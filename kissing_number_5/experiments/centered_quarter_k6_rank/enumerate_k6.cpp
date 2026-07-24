// Enumerate fixed-support rank-at-most-five quarter-grid K6 orbit types.
//
// Input is the 4,080 labeled K5 support rows emitted by prepare_support.py.
// A sixth vertex is adjoined with every one of the 7^5 possible edge rows.
// All six K5 faces must remain in the input support.  Because those faces are
// PSD, the complete K6 matrix is PSD exactly when its remaining principal
// determinant is nonnegative.  Rank <= 5 requires that determinant to be
// zero, so the combined condition is simply det(K6)=0.

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using Edges5 = std::array<int, 10>;
using Edges6 = std::array<int, 15>;

static constexpr std::array<std::pair<int, int>, 10> PAIRS5 = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {1, 2},
    {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4},
}};
static constexpr std::array<std::pair<int, int>, 15> PAIRS6 = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5},
    {1, 2}, {1, 3}, {1, 4}, {1, 5}, {2, 3},
    {2, 4}, {2, 5}, {3, 4}, {3, 5}, {4, 5},
}};
static constexpr std::array<int, 7> VALUES = {{-4, -3, -2, -1, 0, 1, 2}};
static constexpr std::array<std::array<int, 10>, 6> FACE_INDICES = {{
    {{5, 6, 7, 8, 9, 10, 11, 12, 13, 14}},
    {{1, 2, 3, 4, 9, 10, 11, 12, 13, 14}},
    {{0, 2, 3, 4, 6, 7, 8, 12, 13, 14}},
    {{0, 1, 3, 4, 5, 7, 8, 10, 11, 14}},
    {{0, 1, 2, 4, 5, 6, 8, 9, 11, 13}},
    {{0, 1, 2, 3, 5, 6, 7, 9, 10, 12}},
}};
static constexpr std::array<std::array<int, 6>, 6> PAIR_INDEX = {{
    {{-1, 0, 1, 2, 3, 4}},
    {{0, -1, 5, 6, 7, 8}},
    {{1, 5, -1, 9, 10, 11}},
    {{2, 6, 9, -1, 12, 13}},
    {{3, 7, 10, 12, -1, 14}},
    {{4, 8, 11, 13, 14, -1}},
}};

std::uint64_t encode5(const Edges5& edges) {
    std::uint64_t value = 0;
    for (int color : edges) value = 7 * value + color;
    return value;
}

std::uint64_t encode6(const Edges6& edges) {
    std::uint64_t value = 0;
    for (int color : edges) value = 7 * value + color;
    return value;
}

int pair_index6(int a, int b) {
    return PAIR_INDEX[a][b];
}

Edges5 face_edges(const Edges6& edges, int deleted) {
    Edges5 face{};
    for (int index = 0; index < 10; ++index)
        face[index] = edges[FACE_INDICES[deleted][index]];
    return face;
}

std::uint64_t encode_face(const Edges6& edges, int deleted) {
    std::uint64_t value = 0;
    for (int index : FACE_INDICES[deleted]) value = 7 * value + edges[index];
    return value;
}

std::int64_t determinant6(const Edges6& edges) {
    std::array<std::array<std::int64_t, 6>, 6> matrix{};
    for (int i = 0; i < 6; ++i) matrix[i][i] = 4;
    for (int index = 0; index < 15; ++index) {
        const auto [i, j] = PAIRS6[index];
        matrix[i][j] = VALUES[edges[index]];
        matrix[j][i] = VALUES[edges[index]];
    }
    // Fraction-free Bareiss elimination with symmetric row pivoting.
    std::int64_t sign = 1;
    std::int64_t previous = 1;
    for (int pivot = 0; pivot < 5; ++pivot) {
        int row = pivot;
        while (row < 6 && matrix[row][pivot] == 0) ++row;
        if (row == 6) return 0;
        if (row != pivot) {
            std::swap(matrix[row], matrix[pivot]);
            sign = -sign;
        }
        const std::int64_t value = matrix[pivot][pivot];
        for (int i = pivot + 1; i < 6; ++i) {
            for (int j = pivot + 1; j < 6; ++j) {
                const std::int64_t numerator =
                    matrix[i][j] * value
                    - matrix[i][pivot] * matrix[pivot][j];
                if (pivot > 0 && numerator % previous != 0) std::abort();
                matrix[i][j] = (pivot == 0) ? numerator : numerator / previous;
            }
        }
        previous = value;
    }
    return sign * matrix[5][5];
}

Edges6 canonical(const Edges6& edges) {
    std::array<int, 6> permutation = {{0, 1, 2, 3, 4, 5}};
    Edges6 best{};
    best.fill(7);
    do {
        Edges6 image{};
        for (int index = 0; index < 15; ++index) {
            const auto [i, j] = PAIRS6[index];
            image[index] = edges[pair_index6(permutation[i], permutation[j])];
        }
        if (image < best) best = image;
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return best;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: enumerate_k6 LABELED_SUPPORT.csv OUTPUT.csv\n";
        return 2;
    }
    std::ifstream input(argv[1]);
    if (!input) return 3;
    std::unordered_map<std::uint64_t, int> support;
    std::vector<Edges5> labeled;
    std::string line;
    std::getline(input, line);
    while (std::getline(input, line)) {
        std::replace(line.begin(), line.end(), ',', ' ');
        std::istringstream fields(line);
        int orbit;
        Edges5 edges{};
        fields >> orbit;
        for (int& color : edges) fields >> color;
        if (!fields || orbit < 0 || orbit >= 51) return 4;
        const auto code = encode5(edges);
        if (!support.emplace(code, orbit).second) return 5;
        labeled.push_back(edges);
    }
    if (labeled.empty()) return 6;

    std::unordered_set<std::uint64_t> seen_orbits;
    std::vector<std::pair<Edges6, std::array<int, 51>>> results;
    std::uint64_t rows_tested = 0;
    std::uint64_t support_compatible = 0;
    std::uint64_t determinant_zero_labeled = 0;

    for (const auto& base : labeled) {
        Edges6 edges{};
        // Map base K5 positions into the K6 order.
        for (int index = 0; index < 10; ++index) {
            const auto [i, j] = PAIRS5[index];
            edges[pair_index6(i, j)] = base[index];
        }
        for (int code = 0; code < 16807; ++code) {
            int remainder = code;
            for (int vertex = 4; vertex >= 0; --vertex) {
                edges[pair_index6(vertex, 5)] = remainder % 7;
                remainder /= 7;
            }
            ++rows_tested;
            std::array<int, 6> face_orbits{};
            bool allowed = true;
            for (int deleted = 0; deleted < 6; ++deleted) {
                const auto found = support.find(encode_face(edges, deleted));
                if (found == support.end()) {
                    allowed = false;
                    break;
                }
                face_orbits[deleted] = found->second;
            }
            if (!allowed) continue;
            ++support_compatible;
            if (determinant6(edges) != 0) continue;
            ++determinant_zero_labeled;
            const Edges6 representative = canonical(edges);
            const auto orbit_code = encode6(representative);
            if (!seen_orbits.insert(orbit_code).second) continue;
            std::array<int, 51> counts{};
            for (int deleted = 0; deleted < 6; ++deleted) {
                const auto found = support.find(
                    encode_face(representative, deleted)
                );
                if (found == support.end()) return 7;
                ++counts[found->second];
            }
            results.push_back({representative, counts});
        }
        if (rows_tested % (30 * 16807ULL) == 0) {
            std::cerr << "rows=" << rows_tested
                      << " compatible=" << support_compatible
                      << " rank5=" << determinant_zero_labeled
                      << " orbits=" << results.size() << "\n";
        }
    }

    std::sort(results.begin(), results.end(), [](const auto& left, const auto& right) {
        return left.first < right.first;
    });
    std::ofstream output(argv[2]);
    if (!output) return 8;
    output << "# labeled_support=" << labeled.size()
           << " rows_tested=" << rows_tested
           << " support_compatible=" << support_compatible
           << " determinant_zero_labeled=" << determinant_zero_labeled
           << " k6_orbits=" << results.size() << "\n";
    for (const auto& [edges, counts] : results) {
        bool first = true;
        for (int color : edges) {
            if (!first) output << ',';
            output << color;
            first = false;
        }
        for (int count : counts) output << ',' << count;
        output << '\n';
    }
    std::cerr << "done rows=" << rows_tested
              << " compatible=" << support_compatible
              << " rank5=" << determinant_zero_labeled
              << " orbits=" << results.size() << "\n";
    return 0;
}
