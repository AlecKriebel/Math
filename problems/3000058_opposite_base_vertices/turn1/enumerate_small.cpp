#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int main(){
 cout<<"{\n  \"scope\": \"Exhaustive positive proper-subset rank functions, ground sizes 1 through 5; general reduction is in TURN_1.md\",\n  \"cases\": [\n";
 for(int n=1;n<=5;n++){
  int N=1<<n,full=N-1; vector<int> freeS,b(N,0),p(n),pow3(n);int total3=1;
  for(int i=0;i<n;i++){p[i]=i;pow3[i]=total3;total3*=3;}
  for(int s=1;s<full;s++){int k=__builtin_popcount((unsigned)s);b[s]=1;if(min(k,n-k)==2)freeS.push_back(s);}
  vector<array<int,4>>ineq;
  for(int s=0;s<N;s++)for(int i=0;i<n;i++)if(!(s>>i&1))for(int j=i+1;j<n;j++)if(!(s>>j&1))ineq.push_back({s|(1<<i),s|(1<<j),s,s|(1<<i)|(1<<j)});
  vector<vector<int>>perms;do{perms.push_back(p);}while(next_permutation(p.begin(),p.end()));
  uint64_t tried=1ULL<<freeS.size(),valid=0,greedy=0,checks=0,hash=1469598103934665603ULL;int maxverts=0;array<uint64_t,6>hist{};
  for(uint64_t mask=0;mask<tried;mask++){
   for(int j=0;j<(int)freeS.size();j++)b[freeS[j]]=1+((mask>>j)&1);
   bool ok=true;for(auto q:ineq){checks++;if(b[q[0]]+b[q[1]]<b[q[2]]+b[q[3]]){ok=false;break;}}
   if(!ok)continue;valid++;vector<int>verts;
   for(auto perm:perms){int s=0,code=0;for(int i:perm){int ns=s|(1<<i),v=b[ns]-b[s];assert(-1<=v&&v<=1);code+=(v+1)*pow3[i];s=ns;greedy++;}verts.push_back(code);}
   sort(verts.begin(),verts.end());verts.erase(unique(verts.begin(),verts.end()),verts.end());maxverts=max(maxverts,(int)verts.size());int witness=-1,support=-1;
   for(int v:verts)if(binary_search(verts.begin(),verts.end(),total3-1-v)){witness=v;int z=v;support=0;for(int i=0;i<n;i++){support+=(z%3!=1);z/=3;}break;}
   if(witness<0){cerr<<"COUNTEREXAMPLE n="<<n<<" mask="<<mask<<"\n";return 2;}
   hist[support]++;for(uint64_t x:{mask,(uint64_t)witness})for(int j=0;j<8;j++){hash^=(x>>(8*j))&255;hash*=1099511628211ULL;}
  }
  cout<<"    {\"n\": "<<n<<", \"candidate_tables\": "<<tried<<", \"submodular_tables\": "<<valid<<", \"submodular_inequality_checks\": "<<checks<<", \"greedy_coordinate_checks\": "<<greedy<<", \"max_vertices\": "<<maxverts<<", \"witness_stream_fnv64\": \""<<hash<<"\", \"witness_support_histogram\": [";
  for(int i=0;i<=n;i++){if(i)cout<<", ";cout<<hist[i];}cout<<"]}"<<(n<5?",":"")<<"\n";
 }
 cout<<"  ],\n  \"status\": \"PASS; every enumerated admissible table has an opposite greedy-vertex pair\",\n  \"retention\": \"Witness rows are deterministically regenerable; only aggregate counts and rolling checksum are retained.\"\n}\n";
}
