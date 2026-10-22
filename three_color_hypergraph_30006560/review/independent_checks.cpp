#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
int pc(unsigned x){return __builtin_popcount(x);}
int success_count(int n,int r,const vector<int>& C){int t=0;for(int s=0;s<(1<<n);++s)if(pc(s)==r){int k=0;for(int e=0;e<(1<<n);++e)if(C[e] && (e&s)==e)k|=1<<C[e];t+=(k==14);}return t;}
int main(){uint64_t total=0,link_checks=0; int maxT=0;for(int n=0;n<=5;++n)for(int r=3;r<=6;++r){vector<int>E;for(int e=0;e<(1<<n);++e)if(pc(e)==r-1)E.push_back(e);uint64_t stop=1ULL<<(2*E.size());for(uint64_t config=0;config<stop;++config){vector<int>C(1<<n);array<int,4>counts{};for(int j=0;j<(int)E.size();++j){int c=(config>>(2*j))&3;C[E[j]]=c;++counts[c];}int t=0,mult=0;uint64_t direct=0;for(int s=0;s<(1<<n);++s)if(pc(s)==r){array<int,4>a{};for(int e:E)if((e&s)==e)++a[C[e]];if(a[1]&&a[2]&&a[3]){++t;direct|=1ULL<<(((1<<n)-1)^s);}mult+=a[1]*a[2]*a[3];}
assert(t<=counts[1]*counts[2] && t<=counts[1]*counts[3] && t<=counts[2]*counts[3]);assert(t*t<=2*counts[1]*counts[2]*counts[3]);
if(n>=r){array<uint64_t,4> shadows{};for(int e:E)if(C[e]){int f=((1<<n)-1)^e;for(int v=0;v<n;++v)if(f&(1<<v))shadows[C[e]]|=1ULL<<(f^(1<<v));}assert((shadows[1]&shadows[2]&shadows[3])==direct);assert(t<=(n-r+1)*min({counts[1],counts[2],counts[3]}));}
int linkmult=0;for(int a=0;a<(1<<n);++a)if(pc(a)==r-3)for(int u=0;u<n;++u)for(int v=u+1;v<n;++v)for(int w=v+1;w<n;++w){int triangle=(1<<u)|(1<<v)|(1<<w);if(a&triangle)continue;int c1=C[a|(1<<u)|(1<<v)],c2=C[a|(1<<u)|(1<<w)],c3=C[a|(1<<v)|(1<<w)];linkmult+=(c1&&c2&&c3&&c1!=c2&&c1!=c3&&c2!=c3);}assert(linkmult==mult);++link_checks;++total;maxT=max(maxT,t);
}}
uint64_t shift_tests=0;for(int r=3;r<=10;++r){int n=r+2;for(int S=0;S<(1<<n);++S)if(pc(S)==r){vector<int>vertices;for(int v=0;v<n;++v)if(S&(1<<v))vertices.push_back(v);for(int a=0;a<r;++a)for(int b=a+1;b<r;++b)for(int c=b+1;c<r;++c){array<int,3>edges={S^(1<<vertices[a]),S^(1<<vertices[b]),S^(1<<vertices[c])};for(int i=0;i<n;++i)for(int j=0;j<n;++j)if(i!=j){array<int,3>out=edges;for(int k=0;k<3;++k){int e=edges[k];if((e&(1<<j))&&!(e&(1<<i))){int f=e^(1<<j)^(1<<i);if(find(edges.begin(),edges.end(),f)==edges.end())out[k]=f;}}assert(out[0]!=out[1]&&out[0]!=out[2]&&out[1]!=out[2]);assert(pc(out[0]|out[1]|out[2])==r);++shift_tests;}}}}
cout<<"{\"exhaustive_colored_hypergraphs_n_le_5_r_3_to_6\":"<<total<<",\"exact_link_identity_checks\":"<<link_checks<<",\"max_T\":"<<maxT<<",\"three_edge_shift_checks_r_3_to_10\":"<<shift_tests<<",\"all_passed\":true}\n";
}
