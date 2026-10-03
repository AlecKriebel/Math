#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
#include <cstdlib>
// Independent control: covers are enumerated directly; packing is obtained by
// subset-max transform seeded ONLY at feasible edge subsets.
int main(int argc,char**argv){
 if(argc!=3)return 2;
 const int n=std::atoi(argv[1]),r=std::atoi(argv[2]);
 std::vector<uint32_t> e; for(uint32_t x=1;x<(1u<<n);++x)if(__builtin_popcount(x)==r)e.push_back(x);
 int m=e.size(); uint32_t N=1u<<m;
 std::vector<uint32_t> inc(n,0); for(int j=0;j<m;++j)for(int v=0;v<n;++v)if(e[j]&(1u<<v))inc[v]|=1u<<j;
 std::vector<uint8_t> nu(N,0),delta(N,0);
 for(uint32_t h=0;h<N;++h){int d=0;for(auto mask:inc)d=std::max(d,__builtin_popcount(h&mask));delta[h]=d;if(d<=r)nu[h]=__builtin_popcount(h);}
 for(int j=0;j<m;++j)for(uint32_t h=0;h<N;++h)if(h&(1u<<j))nu[h]=std::max(nu[h],nu[h^(1u<<j)]);
 std::vector<std::pair<int,uint32_t>> covers;
 for(uint32_t vs=0;vs<(1u<<n);++vs){uint32_t missed=0;for(int j=0;j<m;++j)if(!(e[j]&vs))missed|=1u<<j;covers.push_back({__builtin_popcount(vs),missed});}
 std::sort(covers.begin(),covers.end());
 uint64_t proper=0,eq=0,bad=0;
 std::vector<uint64_t> histogram((n+1)*(m+1),0);
 for(uint32_t h=0;h<N;++h){int tau=n;for(auto [size,missed]:covers)if(!(h&missed)){tau=size;break;}histogram[tau*(m+1)+nu[h]]++;
 if(delta[h]>r){proper++;eq+=(tau+r-1==nu[h]);bad+=(tau+r-1>nu[h]);}}
 std::cout<<"{\"n\":"<<n<<",\"r\":"<<r<<",\"complete_edges\":"<<m<<",\"families\":"<<N<<",\"delta_gt_r\":"<<proper<<",\"equalities\":"<<eq<<",\"violations\":"<<bad<<",\"histogram\":[";
 bool first=true;for(int t=0;t<=n;++t)for(int k=0;k<=m;++k)if(histogram[t*(m+1)+k]){if(!first)std::cout<<',';first=false;std::cout<<'['<<t<<','<<k<<','<<histogram[t*(m+1)+k]<<']';}std::cout<<"]}\n";
 return bad?1:0;
}
