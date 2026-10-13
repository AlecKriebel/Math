// Exact finite Artin-action certificate. C++17; no state/depth cap.
#include <array>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <stdexcept>
using Word = std::vector<int>;
using Aut = std::array<Word, 6>;
static void append_reduced(Word& w, int x) {
    if (!w.empty() && w.back() == -x) w.pop_back();
    else w.push_back(x);
}
static Aut act_generator(const Aut& input, int g) {
    Aut output;
    for (int k = 0; k < 6; ++k) {
        for (int x : input[k]) {
            const int v = x > 0 ? x : -x;
            if (v == g) {
                append_reduced(output[k], g);
                append_reduced(output[k], x > 0 ? g + 1 : -g - 1);
                append_reduced(output[k], -g);
            } else if (v == g + 1) {
                append_reduced(output[k], x > 0 ? g : -g);
            } else append_reduced(output[k], x);
        }
    }
    return output;
}
static void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
int main(int argc, char** argv) {
    const bool stream = argc == 2 && std::string(argv[1]) == "--stream";
    require(argc == 1 || stream, "Only --stream is supported");
    int pair_index[6][6], pair_count = 0;
    for (int i = 0; i < 6; ++i)
        for (int j = i + 1; j < 6; ++j)
            pair_index[i][j] = pair_index[j][i] = pair_count++;
    std::vector<int> power(16, 1);
    for (int i = 1; i <= 15; ++i) power[i] = 3 * power[i - 1];
    const int count = power[15], full = count - 1;
    // -2 means unreached; the empty-state parent is -1.
    std::vector<int> parent(count, -2), permutation(count);
    std::vector<unsigned char> last_generator(count);
    std::vector<int> queue;
    parent[0] = -1;
    for (int i = 0; i < 6; ++i) permutation[0] |= i << (3 * i);
    queue.push_back(0);
    long long edges = 0;
    for (std::size_t head = 0; head < queue.size(); ++head) {
        const int code = queue[head], perm = permutation[code];
        for (int i = 0; i < 5; ++i) {
            const int a = (perm >> (3 * i)) & 7;
            const int b = (perm >> (3 * (i + 1))) & 7;
            const int step = power[pair_index[a][b]];
            if (code / step % 3 == 2) continue;
            ++edges;
            const int next = code + step;
            const int np = perm ^ ((a ^ b) << (3 * i)) ^ ((a ^ b) << (3 * (i + 1)));
            if (parent[next] == -2) {
                parent[next] = code;
                permutation[next] = np;
                last_generator[next] = i + 1;
                queue.push_back(next);
            } else require(permutation[next] == np, "Parity/permutation inconsistency");
        }
    }
    auto good = [&](int code) { return parent[code] != -2 && parent[full - code] != -2; };
    Aut identity;
    for (int i = 0; i < 6; ++i) identity[i] = {i + 1};
    std::unordered_map<int, Aut> images;
    images.reserve(100000);
    images.emplace(0, identity);
    for (int code : queue) {
        if (!code || !good(code)) continue;
        auto it = images.find(parent[code]);
        require(it != images.end(), "Canonical parent is not coaccessible");
        images.emplace(code, act_generator(it->second, last_generator[code]));
    }
    long long comparisons = 0;
    for (int code : queue) {
        if (!good(code)) continue;
        const int perm = permutation[code];
        for (int i = 0; i < 5; ++i) {
            const int a = (perm >> (3 * i)) & 7;
            const int b = (perm >> (3 * (i + 1))) & 7;
            const int step = power[pair_index[a][b]];
            if (code / step % 3 == 2) continue;
            const int next = code + step;
            if (!good(next)) continue;
            require(act_generator(images.at(code), i + 1) == images.at(next),
                    "Different free-group actions on paths to one state");
            ++comparisons;
        }
    }
    Aut standard = identity;
    for (int repetition = 0; repetition < 6; ++repetition)
        for (int g = 1; g <= 5; ++g) standard = act_generator(standard, g);
    require(images.at(full) == standard, "Terminal action is not full twist");
    require(queue.size() == 234368 && edges == 711342, "Reachable census mismatch");
    require(images.size() == 90921 && comparisons == 261810, "Coaccessible census mismatch");
    if (stream) {
        for (int code = 0; code < count; ++code) {
            if (!good(code)) continue;
            std::cout << "S|" << code << '|' << permutation[code];
            for (const auto& word : images.at(code)) {
                std::cout << '|';
                bool first = true;
                for (int x : word) {
                    if (!first) std::cout << ',';
                    first = false;
                    std::cout << x;
                }
            }
            std::cout << '\n';
        }
    }
    std::cout << "{\"status\":\"PASS\",\"reachable_states\":" << queue.size()
              << ",\"outgoing_edges\":" << edges
              << ",\"coaccessible_states\":" << images.size()
              << ",\"coaccessible_edges\":" << comparisons << "}\n";
}
