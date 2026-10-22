// Independent audit of KOU-21.100. No author checker or Walsh transform used.
// Points encoded as 8*(x + 4*y) + z, unlike the packet's x+4*y+16*z.
// Uses literal 128-bit supports, dot products, and weighted orbit representatives.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using Word=unsigned __int128;
int weight(Word x) {return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
Word shift(Word f, int t) {Word out=0; for(int v=0;v<128;++v) if((f>>v)&1) out|=Word(1)<<(v^t); return out;}
// Companion matrices for r^2+r+1 and s^3+s+1, applied coordinatewise.
int r(int x) {int a=x&1,b=(x>>1)&1;return b+2*(a^b);}
int s(int z) {int a=z&1,b=(z>>1)&1,c=(z>>2)&1;return c+2*(a^c)+4*b;}
int T(int v) {int u=v>>3;return 8*(r(u&3)+4*r(u>>2))+s(v&7);}
void printmap(std::map<int,int> m) {std::cout<<"{";bool first=true;for(auto [a,b]:m){if(!first)std::cout<<", ";first=false;std::cout<<"\""<<a<<"\": "<<b;}std::cout<<"}";}
int main() {
 // Construct the spread directly, independently of operator orbit traversal.
 std::array<std::array<int,3>,5> lines={{{1,2,3},{4,8,12},{5,10,15},{6,11,13},{7,9,14}}};
 std::vector<std::vector<int>> orbs(12);orbs[0]={0};
 for(int i=0;i<5;++i){for(int u:lines[i])orbs[1+i].push_back(8*u);}
 for(int w=1;w<8;++w)orbs[6].push_back(w);
 for(int i=0;i<5;++i)for(int u:lines[i])for(int w=1;w<8;++w)orbs[7+i].push_back(8*u+w);
 std::set<int> all;
 std::array<int,128> orbitIndex{};
 std::array<Word,12> block{};
 for(int j=0;j<12;++j){
   std::set<int> actual;int t=orbs[j][0];do{actual.insert(t);t=T(t);}while(t!=orbs[j][0]);
   assert(actual==std::set<int>(orbs[j].begin(),orbs[j].end()));
   for(int v:orbs[j]){assert(all.insert(v).second);orbitIndex[v]=j;block[j]|=Word(1)<<v;}
 }
 assert(all.size()==128);
 int fixed=0;
 for(int v=0;v<128;++v){fixed+=T(v)==v;for(int w=0;w<128;++w)assert(T(v^w)==(T(v)^T(w)));}
 assert(fixed==1);
 for(int power=1;power<=21;++power){bool isIdentity=true;for(int v=0;v<128;++v){int tv=v;for(int k=0;k<power;++k)tv=T(tv);if(tv!=v)isIdentity=false;}assert(isIdentity==(power==21));}
 std::array<Word,4096> masks{};
 for(int u=0;u<4096;++u)for(int j=0;j<12;++j)if((u>>j)&1)masks[u]|=block[j];
 std::map<int,int> zeroHist,degreeHist,nowhereDegree,stabilizerHist,criterionHist;
 std::array<long long,257> valueHist{};
 long long zeros=0,pairs=0;int nowhere=0,balanced=0;
 for(Word c:masks)balanced+=weight(c)==64;
 for(int u=0;u<4096;++u){
   std::array<Word,128> translated;
   int stab=0;
   for(int t=0;t<128;++t){translated[t]=shift(masks[u],t);stab+=translated[t]==masks[u];}
   assert(stab>0 && (128%stab)==0);
   // For every translation, verify equivalence of its pairing functional on B^A
   // to the representative for the same operator orbit, independently of c.
   for(int t=0;t<128;++t)for(int j=0;j<12;++j)
     assert((weight(translated[t]&block[j])&1)==(weight(translated[orbs[orbitIndex[t]][0]]&block[j])&1));
   ++stabilizerHist[stab];++degreeHist[128/stab];int rowZeros=0;
   for(int c=0;c<4096;++c){
     int value=0;
     for(int j=0;j<12;++j){int p=weight(translated[orbs[j][0]]&masks[c])&1;value+=(p?-1:1)*int(orbs[j].size());}
     assert(value%stab==0);value/=stab;
     assert(value>=-128 && value<=128);++valueHist[128+value];
     rowZeros+=value==0;++pairs;
   }
   // Independently compare every direct row with the source's optional analytic
   // zero criterion, after the direct values have already been computed.
   int X=u&63,Y=u>>6,P=X^Y;
   int p0=P&1, p=P>>1, y=Y>>1, rr=p^(p0?31:0);
   bool firstCriterion=(__builtin_popcount((unsigned)P)&1)!=0;
   bool secondCriterion=!firstCriterion && __builtin_popcount((unsigned)rr)==2
      && (__builtin_popcount((unsigned)Y)&1)==1
      && (__builtin_popcount((unsigned)(rr&y))&1)==(1^p0);
   assert((rowZeros>0)==(firstCriterion||secondCriterion));
   ++criterionHist[firstCriterion?1:(secondCriterion?2:0)];
   ++zeroHist[rowZeros];zeros+=rowZeros;
   if(rowZeros==0){++nowhere;++nowhereDegree[128/stab];}
 }
 // One completely concrete support and direct degree-128 representation trace.
 Word witness=block[0]|block[7]|block[8]|block[9];
 int trace=0;for(int t=0;t<128;++t)trace+=((witness>>t)&1)?-1:1;
 assert(weight(witness)==64 && trace==0);
 std::cout<<"{\n  \"method\": \"literal 128-bit supports and direct weighted dot products; no Walsh transform\",\n"
 <<"  \"operator_order\": 21,\n  \"operator_fixed_vectors\": 1,\n  \"orbit_sizes\": [1,3,3,3,3,3,7,21,21,21,21,21],\n"
 <<"  \"balanced_invariant_subsets\": "<<balanced<<",\n  \"invariant_characters\": 4096,\n  \"character_element_pairs\": "<<pairs<<",\n"
 <<"  \"nowhere_zero_characters\": "<<nowhere<<",\n  \"zero_pairs\": "<<zeros<<",\n  \"degree_histogram\": ";printmap(degreeHist);
 std::cout<<",\n  \"nowhere_zero_degree_histogram\": ";printmap(nowhereDegree);
 std::cout<<",\n  \"zero_count_histogram\": ";printmap(zeroHist);
 std::cout<<",\n  \"stabilizer_size_histogram\": ";printmap(stabilizerHist);
 std::cout<<",\n  \"analytic_criterion_histogram\": ";printmap(criterionHist);
 std::cout<<",\n  \"witness_support\": [";bool first=true;for(int v=0;v<128;++v)if((witness>>v)&1){if(!first)std::cout<<", ";first=false;std::cout<<v;}
 std::cout<<"],\n  \"witness_support_size\": "<<weight(witness)<<",\n  \"witness_trace\": "<<trace<<"\n}\n";
}
