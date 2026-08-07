#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

using u64 = std::uint64_t;

static std::vector<unsigned char> read_all(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("cannot open " + path);
    return std::vector<unsigned char>((std::istreambuf_iterator<char>(in)), {});
}

static long long popcount_words(const std::vector<u64>& words) {
    long long n=0; for (u64 x: words) n += __builtin_popcountll(x); return n;
}

int main(int argc, char** argv) {
    if (argc != 6) {
        std::cerr << "usage: regenerate_directed_pair_universe STRONG.bin WEAK.bin BYTES_PER_RECORD K OUT.tsv\n";
        return 2;
    }
    const std::string strong_path=argv[1], weak_path=argv[2], out_path=argv[5];
    const std::size_t width=std::stoull(argv[3]);
    const int k=std::stoi(argv[4]);
    auto strong=read_all(strong_path), weak=read_all(weak_path);
    if (width==0 || strong.size()%width || weak.size()%width) throw std::runtime_error("bad record width");
    const std::size_t ns=strong.size()/width, nt=weak.size()/width;
    const std::size_t feature_count=width*7;
    const std::size_t words=(nt+63)/64;
    std::vector<std::vector<u64>> index(feature_count, std::vector<u64>(words));
    std::vector<std::size_t> freq(feature_count,0);
    for (std::size_t j=0;j<nt;++j) {
        const auto* rec=&weak[j*width];
        for (std::size_t p=0;p<width;++p) {
            unsigned char v=rec[p];
            for (int b=0;b<7;++b) if (v&(1u<<b)) {
                std::size_t f=p*7+b; index[f][j/64] |= u64(1)<<(j%64); ++freq[f];
            }
        }
    }
    std::ofstream out(out_path);
    if (!out) throw std::runtime_error("cannot write output");
    out << "source_index\ttarget_index\trelation\n";
    long long total=0,equal=0,strict=0;
    std::vector<u64> candidates(words), all(words,~u64(0));
    if (nt%64) all.back()=(u64(1)<<(nt%64))-1;
    for (std::size_t i=0;i<ns;++i) {
        const auto* s=&strong[i*width];
        std::vector<std::size_t> required;
        for (std::size_t p=0;p<width;++p) for (int b=0;b<7;++b)
            if (s[p]&(1u<<b)) required.push_back(p*7+b);
        std::sort(required.begin(), required.end(), [&](auto a, auto b){return freq[a]<freq[b];});
        candidates=all;
        for (auto f: required) {
            for (std::size_t w=0;w<words;++w) candidates[w]&=index[f][w];
            const auto remaining=popcount_words(candidates);
            if (!remaining || remaining<=128) break;
        }
        for (std::size_t w=0;w<words;++w) {
            u64 bits=candidates[w];
            while(bits) {
                unsigned bit=__builtin_ctzll(bits); bits&=bits-1;
                std::size_t j=w*64+bit; if (j>=nt) continue;
                const auto* t=&weak[j*width];
                bool ok=true, eq=true;
                for (std::size_t p=0;p<width;++p) {
                    if (s[p] & static_cast<unsigned char>(~t[p])) {ok=false;break;}
                    if (s[p]!=t[p]) eq=false;
                }
                if (!ok) continue;
                out << i << '\t' << j << '\t' << (eq?"equal":"strict") << '\n';
                ++total; if(eq)++equal; else ++strict;
            }
        }
    }
    const long long expected_total = k==5?27000:32940;
    const long long expected_equal = k==5?8520:10980;
    const long long expected_strict = k==5?18480:21960;
    if (total!=expected_total || equal!=expected_equal || strict!=expected_strict)
        throw std::runtime_error("unexpected directed-pair counts");
    std::cout << "{\n"
              << "  \"status\": \"EXACTLY COMPUTED FROM REGENERATED SIGNATURES\",\n"
              << "  \"outgoing_count\": " << k << ",\n"
              << "  \"source_signatures\": " << ns << ",\n"
              << "  \"target_signatures\": " << nt << ",\n"
              << "  \"directed_pairs\": " << total << ",\n"
              << "  \"equal_pairs\": " << equal << ",\n"
              << "  \"strict_pairs\": " << strict << ",\n"
              << "  \"duplicates\": 0\n"
              << "}\nALL DIRECTED PAIR UNIVERSE CHECKS PASSED\n";
}
