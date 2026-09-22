// Standalone C++17 verifier. No external library, catalogue, or Python data.
// Independently reconstructs the matrix group and all 76 actual subgroups,
// checks the small-group intersection bounds, and enumerates affine witnesses.
#include <algorithm>
#include <array>
#include <bitset>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using M=std::array<int,4>;
using Bits=std::bitset<128>;
using Key=std::array<unsigned long long,2>;
const M I{1,0,0,1}, A{0,28,1,0}, B{2,7,12,28}, Z{28,0,0,28};
void check(bool ok,const char* message){if(!ok)throw std::runtime_error(message);}
M mult(const M&x,const M&y,int p=29){
 return {(x[0]*y[0]+x[1]*y[2])%p,(x[0]*y[1]+x[1]*y[3])%p,
         (x[2]*y[0]+x[3]*y[2])%p,(x[2]*y[1]+x[3]*y[3])%p};
}
M power(M x,int k,int p=29){M a=I;while(k--){a=mult(a,x,p);}return a;}
Key key(const Bits&b){Key k{0,0};for(int i=0;i<120;i++)if(b[i])k[i/64]|=1ULL<<(i%64);return k;}
struct Sub{Bits bits;std::vector<int> generators;};
int main(int argc,char**argv){try{
 std::set<M> found{I};std::vector<M> queue{I};
 for(size_t k=0;k<queue.size();k++)for(M g:{A,B}){M y=mult(g,queue[k]);if(found.insert(y).second)queue.push_back(y);}
 check(found.size()==120,"matrix complement order");
 std::vector<M> H(found.begin(),found.end());std::map<M,int> ix;
 for(int i=0;i<120;i++)ix[H[i]]=i;
 int id=ix[I],z=ix[Z];std::array<std::array<int,120>,120>T{};
 for(int i=0;i<120;i++)for(int j=0;j<120;j++){
   M q=mult(H[i],H[j]);check(ix.count(q),"matrix closure");T[i][j]=ix[q];
 }
 check(power(A,2)==Z&&power(B,3)==Z&&power(mult(A,B),5)==Z,"triangle relations");
 std::array<int,120> inv{};int involutions=0;
 for(int i=0;i<120;i++){
   if(i!=id&&T[i][i]==id)involutions++;
   for(int j=0;j<120;j++)if(T[i][j]==id)inv[i]=j;
 }
 check(involutions==1&&T[z][z]==id,"unique involution");
 // Construct the full isomorphism from SL(2,5), using different element order.
 const M A5{0,4,1,0},B5{0,4,1,1};
 std::map<M,M> iso{{I,I}};std::vector<M> q5{I};
 for(size_t i=0;i<q5.size();i++)for(auto g:std::vector<std::pair<M,M>>{{A5,A},{B5,B}}){
   M n5=mult(g.first,q5[i],5),n29=mult(g.second,iso.at(q5[i]));
   if(!iso.count(n5)){iso[n5]=n29;q5.push_back(n5);}else check(iso.at(n5)==n29,"isomorphism consistency");
 }
 check(iso.size()==120,"SL2(5) map order");std::set<M> images;
 for(auto x:iso){images.insert(x.second);for(auto y:iso)check(iso.at(mult(x.first,y.first,5))==mult(x.second,y.second),"isomorphism product");}
 check(images==found,"SL2(5) bijectivity");
 // Exhaustive subgroup search, adjoining elements. The bitsets use a different
 // indexing from the Python verifier; an optional export permits set comparison.
 auto close=[&](const std::vector<int>&gens){Bits s;s.set(id);std::vector<int>q{id};
   for(size_t i=0;i<q.size();i++)for(int g:gens){int y=T[g][q[i]];if(!s[y]){s.set(y);q.push_back(y);}}
   return s;};
 std::vector<Sub> subs{{close({}),{}}};std::map<Key,int> known{{key(subs[0].bits),0}};
 for(size_t i=0;i<subs.size();i++){
   auto h=subs[i];
   for(int g=0;g<120;g++)if(!h.bits[g]){auto gs=h.generators;gs.push_back(g);Bits s=close(gs);Key k=key(s);
     if(!known.count(k)){known[k]=subs.size();subs.push_back({s,gs});}}
 }
 check(subs.size()==76,"subgroup count");std::set<int> odd_orders;std::vector<int> normal_orders;
 for(auto h:subs){if(h.bits.count()%2)odd_orders.insert(h.bits.count());bool normal=true;
   for(int g=0;g<120;g++)for(int x:h.generators)if(!h.bits[T[T[inv[g]][x]][g]])normal=false;
   if(normal)normal_orders.push_back(h.bits.count());}
 std::sort(normal_orders.begin(),normal_orders.end());
 check(odd_orders==std::set<int>{1,3,5},"odd subgroup orders");
 check(normal_orders==std::vector<int>{1,2,120},"normal subgroup orders");
 std::vector<Bits> proper;for(auto h:subs)if(h.bits.count()<120)proper.push_back(h.bits);
 long long fours=0,threes=0;Bits one;one.set(id);
 for(size_t i=0;i<proper.size();i++)for(size_t j=i+1;j<proper.size();j++)for(size_t k=j+1;k<proper.size();k++){
   Bits a=proper[i],b=proper[j],c=proper[k];threes++;
   check(!((a&b&c)==one&&(a&b)!=one&&(a&c)!=one&&(b&c)!=one),"faithful 3-family in H");
   for(size_t l=k+1;l<proper.size();l++){Bits d=proper[l],m=a&b&c&d;fours++;
     check(!((b&c&d)!=m&&(a&c&d)!=m&&(a&b&d)!=m&&(a&b&c)!=m),"irredundant 4-family in H");}
 }
 check(fours==1215450&&threes==67525,"family coverage counts");
 const std::vector<M> rm{A,M{12,24,0,17},M{25,3,4,4}};
 std::vector<int>ri;for(M r:rm){check(ix.count(r),"independent matrix membership");ri.push_back(ix[r]);}
 std::vector<int> pair_orders;
 for(int i=0;i<3;i++){std::vector<int> gs;for(int j=0;j<3;j++)if(i!=j)gs.push_back(ri[j]);Bits s=close(gs);pair_orders.push_back(s.count());check(!s[ri[i]],"complement independence");}
 check(pair_orders==std::vector<int>{8,12,20}&&close(ri).count()==120,"triple subgroup orders");
 for(int s=0;s<30;s++){
   int x=s==29?0:1,y=s==29?1:s;std::vector<M> stab;
   for(M h:H)if(((h[0]*x+h[1]*y)*y-(h[2]*x+h[3]*y)*x)%29==0)stab.push_back(h);
   check(stab.size()==4,"line stabilizer size");bool order4=false;
   for(M h:stab) {
     if(power(h,2)==Z) order4=true;
   }
   check(order4,"cyclic line stabilizer");
 }
 // Affine elements use integer encoding (29*x+y)*120 + matrix_index.
 auto enc=[](int x,int y,int h){return (29*x+y)*120+h;};
 auto am=[&](int x,int y){int hx=x%120,hy=y%120,v=x/120,w=y/120;
   int a=v/29,b=v%29,c=w/29,d=w%29;M h=H[hx];
   return enc((a+h[0]*c+h[1]*d)%29,(b+h[2]*c+h[3]*d)%29,T[hx][hy]);};
 int eid=enc(0,0,id),ez=enc(0,0,z),tr=enc(1,0,id);
 auto aclose=[&](const std::vector<int>&gs){std::vector<unsigned char>s(100920);s[eid]=1;std::vector<int> q{eid};
   for(size_t i=0;i<q.size();i++) {
     for(int g:gs) {
       int y=am(g,q[i]);
       if(!s[y]) {s[y]=1;q.push_back(y);}
     }
   }
   return s;
 };
 auto count=[](const std::vector<unsigned char>&s){return std::count(s.begin(),s.end(),1);};
 std::vector<int>S{tr,enc(0,0,ri[0]),enc(0,0,ri[1]),enc(0,0,ri[2])};
 check(count(aclose(S))==100920,"affine order");std::vector<std::vector<unsigned char>> omissions;std::vector<int> omission_orders;
 for(int i=0;i<4;i++){auto gs=S;gs.erase(gs.begin()+i);auto s=aclose(gs);check(!s[S[i]],"affine independence");omission_orders.push_back(count(s));omissions.push_back(s);}
 check(omission_orders==std::vector<int>{120,6728,10092,16820},"affine omission orders");
 std::vector<int> inter;for(int i=0;i<100920;i++)if(omissions[0][i]&&omissions[1][i]&&omissions[2][i]&&omissions[3][i])inter.push_back(i);
 check(inter.size()==2&&std::find(inter.begin(),inter.end(),eid)!=inter.end()&&std::find(inter.begin(),inter.end(),ez)!=inter.end(),"affine omission intersection");
 check(am(am(tr,ez),enc(28,0,id))==enc(2,0,z),"nonnormality witness");
 std::vector<std::vector<int>> bg{{enc(1,0,id),ez},{enc(0,1,id),ez},{enc(1,1,id),enc(2,0,z)}};
 std::vector<std::vector<unsigned char>> bs;for(auto gs:bg){bs.push_back(aclose(gs));check(count(bs.back())==58,"base subgroup order");}
 for(int j=0;j<3;j++){int c=0;for(int i=0;i<100920;i++)if(bs[(j+1)%3][i]&&bs[(j+2)%3][i])c++;check(c==2,"base pair intersection");}
 int triple_count=0;for(int i=0;i<100920;i++)if(bs[0][i]&&bs[1][i]&&bs[2][i])triple_count++;
 check(triple_count==1,"faithful base total intersection");
 if(argc>1){std::ofstream out(argv[1]);check(bool(out),"cannot open subgroup export");out<<subs.size()<<"\n";
   for(auto s:subs){bool first=true;for(int i=0;i<120;i++)if(s.bits[i]){if(!first)out<<' ';first=false;M h=H[i];out<<(((h[0]*29+h[1])*29+h[2])*29+h[3]);}out<<'\n';}}
 std::cout<<"PASS: independent C++17 verification\n"
          <<"H: 120 matrices; all 76 subgroups enumerated; SL(2,5) isomorphism checked on all products.\n"
          <<"Normal subgroup orders: 1, 2, 120. Odd subgroup orders: 1, 3, 5. Unique involution.\n"
          <<"All "<<fours<<" proper-subgroup 4-families checked: none irredundant.\n"
          <<"All "<<threes<<" proper-subgroup 3-families checked: none faithful and minimal.\n"
          <<"Thirty line stabilizers: all cyclic of order 4.\n"
          <<"Independent complement triple: omission orders 8, 12, 20; generates 120.\n"
          <<"Independent affine 4-set: generates 100920; omission orders 120, 6728, 10092, 16820.\n"
          <<"Omission intersection: order 2, not normal in the affine group.\n"
          <<"Faithful minimal 3-family: subgroup orders 58,58,58; pair orders 2,2,2; total order 1.\n"
          <<"The all-representations upper bound is the structural proof, not a catalogue cutoff.\n";
 return 0;
 }catch(const std::exception&e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
