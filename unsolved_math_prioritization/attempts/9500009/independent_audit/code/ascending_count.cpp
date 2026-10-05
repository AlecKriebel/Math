#include <cstdint>
#include <iostream>
#include <vector>
#include <cstdlib>
using Count = std::uint64_t;

// Independent implementation: assign the SMALLEST unused label next.
// Its vertex is a final local maximum iff ALL neighbors have been assigned.
std::vector<unsigned> grid(int n) {
    std::vector<unsigned> a(n*n);
    for (int u=0; u<n*n; ++u) for(int v=0; v<n*n; ++v)
        if (std::abs(u/n-v/n)+std::abs(u%n-v%n)==1) a[u]|=1u<<v;
    return a;
}
Count exact_set(const std::vector<unsigned>& a, unsigned roots) {
    const unsigned limit=1u<<a.size();
    std::vector<Count> f(limit); f[0]=1;
    // Backward equation on S: choose the vertex assigned the largest label
    // among S. Neighbors outside S will be larger, so this is a peak exactly
    // when its full neighborhood lies inside S.
    for (unsigned s=1; s<limit; ++s) {
        for (unsigned t=s;t;t&=t-1) {
            unsigned bit=t&-t; int v=__builtin_ctz(bit);
            bool is_peak=(a[v]&~s)==0;
            if(is_peak==bool(roots&bit)) f[s]+=f[s^bit];
        }
    }
    return f.back();
}
std::vector<Count> histogram(const std::vector<unsigned>& a) {
    const unsigned limit=1u<<a.size(); const int N=a.size();
    std::vector<std::vector<Count>> f(limit,std::vector<Count>(N+1)); f[0][0]=1;
    for (unsigned s=1;s<limit;++s) for(unsigned t=s;t;t&=t-1) {
        unsigned bit=t&-t; int v=__builtin_ctz(bit),p=(a[v]&~s)==0;
        for(int k=p;k<=N;++k) f[s][k]+=f[s^bit][k-p];
    }
    return f.back();
}
int main() {
    std::cout<<"{\"method\":\"ascending-label predecessor recurrence\",\"squares\":[";
    for(int n=2;n<=4;++n) {
        auto a=grid(n); const int N=n*n;
        if(n>2)std::cout<<",";
        std::cout<<"{\"n\":"<<n<<",\"peak_histogram\":[";
        auto h=histogram(a);
        for(int k=0;k<=N;++k) {if(k)std::cout<<",";std::cout<<h[k];}
        std::cout<<"],\"single_peak_counts\":[";
        for(int v=0;v<N;++v) {if(v)std::cout<<",";std::cout<<exact_set(a,1u<<v);}
        std::cout<<"],\"pair_counts\":[";
        bool first=true;
        for(int u=0;u<N;++u)for(int v=u+1;v<N;++v) {
            if(!first)std::cout<<",";
            first=false;
            std::cout<<"["<<u<<","<<v<<","<<exact_set(a,(1u<<u)|(1u<<v))<<"]";
        }
        std::cout<<"]}";
    }
    std::cout<<"]}\n";
}
