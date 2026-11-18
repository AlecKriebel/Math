// Audit-only regeneration: insert the MINIMUM, test literal cuts directly.
// No derived basis, E/S criterion, or production module is used.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using P=std::array<int,13>;
bool literal(const P&p,int n){
 for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c){
  if(!(p[a]<p[c]&&p[c]<p[b]))continue;
  for(int d=c+1;d<n;++d)if(p[b]<p[d])return false;
 }
 for(int cut=0;cut<=n;++cut){
  bool left=true,right=true;
  for(int a=0;a<cut&&left;++a)for(int b=a+1;b<cut&&left;++b)for(int c=b+1;c<cut;++c)
   if(p[a]<p[c]&&p[c]<p[b]){left=false;break;}
  if(!left)continue;
  for(int a=cut;a<n&&right;++a)for(int b=a+1;b<n&&right;++b)for(int c=b+1;c<n;++c)
   if(p[c]<p[a]&&p[a]<p[b]){right=false;break;}
  if(right)return true;
 }
 return false;
}
int inversions(const P&p,int n){int r=0;for(int i=0;i<n;++i)for(int j=i+1;j<n;++j)r+=p[i]>p[j];return r;}
int main(){
 std::vector<P> a(1),b;std::cout<<"[\n";
 for(int n=0;n<=11;++n){
  std::vector<uint64_t> count(n*(n-1)/2+1);uint64_t both=0,tchecks=0;
  for(const P&p:a){
   int k=inversions(p,n);++count[k];
   P lo{},hi{};lo[0]=1;for(int i=0;i<n;++i){lo[i+1]=p[i]+1;hi[i]=p[i];}hi[n]=n+1;
   both+=!literal(lo,n+1)&&!literal(hi,n+1);
   int mx=0,cut=0;for(int i=0;i<n-1;++i){mx=std::max(mx,p[i]);if(mx==i+1){cut=i+1;break;}}
   if(cut){
    P t{};for(int i=0;i<cut;++i)t[i]=p[i];t[cut]=cut+1;for(int i=cut;i<n;++i)t[i+1]=p[i]+1;
    if(!literal(t,n+1)||inversions(t,n+1)!=k){std::cerr<<"T failure";return 2;}++tchecks;
   }
  }
  if(n)std::cout<<",\n";
  std::cout<<"{\"n\":"<<n<<",\"total\":"<<a.size()<<",\"both_end_extensions_fail\":"<<both<<",\"T_checks\":"<<tchecks<<",\"counts\":[";
  for(size_t i=0;i<count.size();++i){if(i)std::cout<<",";std::cout<<count[i];}std::cout<<"]}"<<std::flush;
  if(n==11)break;
  b.clear();b.reserve(a.size()*6);
  for(const P&p:a)for(int pos=0;pos<=n;++pos){
   P q{};for(int i=0;i<pos;++i)q[i]=p[i]+1;q[pos]=1;for(int i=pos;i<n;++i)q[i+1]=p[i]+1;
   if(literal(q,n+1))b.push_back(q);
  }
  a.swap(b);
 }
 std::cout<<"\n]\n";
}
