// Independently written exact correlation enumeration for Hou's 128-point example.
// Compile: c++ -O2 -std=c++17 verify_exact_count.cpp -o /tmp/verify_exact_count
// No source-paper code, floating point, or nonstandard library is used.
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <vector>

int times_x(int a, int modulus, int degree) {
    a <<= 1;
    if (a & (1 << degree)) a ^= modulus;
    return a;
}
int T(int v) {
    return times_x(v & 3, 7, 2) | (times_x((v >> 2) & 3, 7, 2) << 2)
           | (times_x(v >> 4, 11, 3) << 4);
}
int parity(int x) {
    int p=0;
    while(x) { p ^= 1; x &= x-1; }
    return p;
}

void print_map(const std::map<int, int>& m) {
    std::cout << "{";
    bool first = true;
    for (auto [k,v] : m) {
        if (!first) std::cout << ", ";
        first = false;
        std::cout << "\"" << k << "\": " << v;
    }
    std::cout << "}";
}

int main() {
    std::array<int,128> orbit;
    orbit.fill(-1);
    int k=0;
    std::vector<int> sizes;
    for (int v=0; v<128; ++v) {
        if (orbit[v]>=0) continue;
        int w=v, n=0;
        do { assert(orbit[w]<0); orbit[w]=k; w=T(w); ++n; } while(w!=v);
        sizes.push_back(n); ++k;
    }
    assert(k==12);
    // For fixed t and output orbit j, this mask records the parity of the
    // number of x in orbit j with x+t in each input orbit.
    std::array<std::array<int,12>,128> masks{};
    for(int t=0;t<128;++t)
        for(int x=0;x<128;++x) masks[t][orbit[x]] ^= 1<<orbit[x^t];
    std::map<int,int> zero_histogram, degree_histogram, nowhere_degree_histogram;
    long long pair_count=0, zero_pairs=0;
    int nowhere=0;
    for(int u=0;u<4096;++u) {
        std::array<int,4096> values{};
        int stabilizer=0;
        for(int t=0;t<128;++t) {
            int signature=0;
            for(int j=0;j<12;++j) signature |= parity(u & masks[t][j])<<j;
            ++values[signature];
            bool fixed=true;
            for(int x=0;x<128;++x)
                if (((u>>orbit[x])&1) != ((u>>orbit[x^t])&1)) {fixed=false;break;}
            stabilizer += fixed;
        }
        assert(stabilizer>0 && 128%stabilizer==0);
        for(int half=1;half<4096;half*=2)
            for(int block=0;block<4096;block+=2*half)
                for(int j=0;j<half;++j) {
                    int a=values[block+j], b=values[block+j+half];
                    values[block+j]=a+b; values[block+j+half]=a-b;
                }
        assert(values[0]==128);
        int zeros=0;
        for(int c=0;c<4096;++c) {
            assert(values[c]%stabilizer==0);
            zeros += values[c]==0;
            ++pair_count;
        }
        // A separate direct character sum checks selected rows, including the witness u=1.
        if(u==0 || u==1 || u==4095 || u==1365 || u==2730) {
            for(int c=0;c<4096;++c) {
                int direct=0;
                for(int t=0;t<128;++t) {
                    int e=0;
                    for(int x=0;x<128;++x)
                        e ^= ((u>>orbit[x^t])&1) & ((c>>orbit[x])&1);
                    direct += e ? -1 : 1;
                }
                assert(direct==values[c]);
            }
        }
        ++degree_histogram[128/stabilizer];
        ++zero_histogram[zeros];
        zero_pairs += zeros;
        if(zeros==0) {++nowhere; ++nowhere_degree_histogram[128/stabilizer];}
    }
    assert(nowhere==1728);
    std::cout << "{\n  \"status\": \"PASS\",\n  \"invariant_characters\": 4096,\n"
              << "  \"nowhere_zero_characters\": " << nowhere << ",\n"
              << "  \"characters_with_a_zero\": " << 4096-nowhere << ",\n"
              << "  \"character_element_pairs\": " << pair_count << ",\n"
              << "  \"zero_pairs\": " << zero_pairs << ",\n"
              << "  \"direct_sum_crosschecked_rows\": 5,\n  \"degree_histogram\": ";
    print_map(degree_histogram);
    std::cout << ",\n  \"nowhere_zero_degree_histogram\": "; print_map(nowhere_degree_histogram);
    std::cout << ",\n  \"zero_count_histogram\": "; print_map(zero_histogram);
    std::cout << "\n}\n";
}
