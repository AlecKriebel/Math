#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <vector>
using U = uint64_t;

// Row-major vertices; open boundaries, not a torus. Each permutation is a
// decreasing-label placement order. A new peak has no earlier neighbor.
std::vector<unsigned> square(int n) {
    std::vector<unsigned> adj(n*n, 0);
    for (int x=0;x<n;x++) for (int y=0;y<n;y++) {
        int v=x*n+y;
        for (auto d: std::vector<std::array<int,2>>{{1,0},{-1,0},{0,1},{0,-1}}) {
            int a=x+d[0],b=y+d[1];
            if (0<=a && a<n && 0<=b && b<n) adj[v] |= 1u<<(a*n+b);
        }
    }
    return adj;
}

// Counts placements with every peak in allowed. Subtract the two singleton
// counts to get precisely a given two-element peak set. No sampling.
U permitted(const std::vector<unsigned>& adj, unsigned allowed) {
    const unsigned end=1u<<adj.size();
    std::vector<U> dp(end,0); dp[0]=1;
    for (unsigned s=0;s<end;s++) if (dp[s]) {
        unsigned todo=(end-1)^s;
        while (todo) {
            int v=__builtin_ctz(todo); todo &= todo-1;
            if ((allowed & (1u<<v)) || (s&adj[v])) dp[s|(1u<<v)]+=dp[s];
        }
    }
    return dp.back();
}

// Direct exact-root recurrence: root status must equal the birth indicator.
// This does not use subtraction of allowed-root counts.
U exact_roots(const std::vector<unsigned>& adj, unsigned roots) {
    const unsigned end=1u<<adj.size();
    std::vector<U> dp(end,0); dp[0]=1;
    for (unsigned s=0;s<end;s++) if(dp[s]) {
        unsigned todo=(end-1)^s;
        while(todo) {
            int v=__builtin_ctz(todo); todo&=todo-1;
            bool birth=!(s&adj[v]), root=bool(roots&(1u<<v));
            if(birth==root)dp[s|(1u<<v)]+=dp[s];
        }
    }
    return dp.back();
}

// A separate DP counts all birth-counts without specifying any peak locations.
std::vector<U> birth_histogram(const std::vector<unsigned>& adj) {
    const unsigned end=1u<<adj.size(); const int N=adj.size();
    std::vector<U> dp(size_t(end)*(N+1),0); dp[0]=1;
    for (unsigned s=0;s<end;s++) {
        unsigned todo=(end-1)^s;
        while (todo) {
            int v=__builtin_ctz(todo); todo &= todo-1;
            int birth=!(s&adj[v]);
            for (int k=0;k+birth<=N;k++)
                dp[size_t(s|(1u<<v))*(N+1)+k+birth]+=dp[size_t(s)*(N+1)+k];
        }
    }
    return std::vector<U>(dp.end()-(N+1),dp.end());
}

int main() {
    std::cout<<"{\"graph\":\"P_n Cartesian-product P_n\",\"integer_type\":\"uint64_t; 16! fits\",\"squares\":[";
    for (int n=2;n<=4;n++) {
        auto adj=square(n); int N=n*n;
        std::vector<U> singles(N),pairs(N*N,0),dist(2*n-1,0);
        for (int a=0;a<N;a++) singles[a]=permitted(adj,1u<<a);
        for (int a=0;a<N;a++) for (int b=a+1;b<N;b++) {
            U allowed=permitted(adj,(1u<<a)|(1u<<b));
            assert(allowed>=singles[a]+singles[b]);
            pairs[a*N+b]=allowed-singles[a]-singles[b];
            assert(pairs[a*N+b]==exact_roots(adj,(1u<<a)|(1u<<b)));
            int d=abs(a/n-b/n)+abs(a%n-b%n);
            dist[d]+=pairs[a*N+b];
            assert((pairs[a*N+b]>0)==!(adj[a]&(1u<<b)));
        }
        auto hist=birth_histogram(adj); U factorial=1;
        for (int k=2;k<=N;k++) factorial*=k;
        assert(std::accumulate(hist.begin(),hist.end(),U(0))==factorial);
        assert(std::accumulate(singles.begin(),singles.end(),U(0))==hist[1]);
        assert(std::accumulate(dist.begin(),dist.end(),U(0))==hist[2]);
        bool brute=false;
        if (n<=3) {
            std::vector<int> labels(N); std::iota(labels.begin(),labels.end(),1);
            std::vector<U> h(N+1,0),p(N*N,0),one(N,0);
            do {
                std::vector<int> peaks;
                for (int v=0;v<N;v++) {
                    unsigned nbr=adj[v]; bool peak=true;
                    while(nbr) {int w=__builtin_ctz(nbr);nbr&=nbr-1;if(labels[v]<labels[w])peak=false;}
                    if(peak)peaks.push_back(v);
                }
                h[peaks.size()]++;
                if(peaks.size()==1)one[peaks[0]]++;
                if(peaks.size()==2)p[peaks[0]*N+peaks[1]]++;
            } while(std::next_permutation(labels.begin(),labels.end()));
            assert(h==hist && p==pairs && one==singles); brute=true;
        }
        if(n>2)std::cout<<",";
        std::cout<<"{\"n\":"<<n<<",\"factorial\":"<<factorial<<",\"peak_histogram\":[";
        for(int k=0;k<=N;k++){if(k)std::cout<<",";std::cout<<hist[k];}
        std::cout<<"],\"single_peak_counts\":[";
        for(int k=0;k<N;k++){if(k)std::cout<<",";std::cout<<singles[k];}
        std::cout<<"],\"two_peak_distance_counts\":[";
        for(int k=0;k<int(dist.size());k++){if(k)std::cout<<",";std::cout<<dist[k];}
        std::cout<<"],\"pair_counts\":[";
        bool first=true;
        for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){
            if(!first)std::cout<<",";
            first=false;
            std::cout<<"["<<a<<","<<b<<","<<pairs[a*N+b]<<"]";
        }
        std::cout<<"],\"brute_force_verified\":"<<(brute?"true":"false")<<",\"birth_histogram_crosscheck\":true,\"direct_root_crosscheck\":true}";
    }
    std::cout<<"]}\n";
}
