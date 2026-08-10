#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <vector>

using V = std::array<int,3>;
static const std::array<std::string,10> N={"0","A","B","C","2A","2B","2C","AB","AC","BC"};
static const std::array<V,10> Y={V{0,0,0},V{1,0,0},V{0,1,0},V{0,0,1},V{2,0,0},V{0,2,0},V{0,0,2},V{1,1,0},V{1,0,1},V{0,1,1}};
static const std::array<V,4> H={V{1,1,0},V{2,3,0},V{1,2,0},V{1,3,0}};

long long det3(const V&a,const V&b,const V&c){
 return 1LL*a[0]*(1LL*b[1]*c[2]-1LL*b[2]*c[1])-1LL*a[1]*(1LL*b[0]*c[2]-1LL*b[2]*c[0])+1LL*a[2]*(1LL*b[0]*c[1]-1LL*b[1]*c[0]);
}
V cross(const V&a,const V&b){return V{a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]};}
bool nonzero(const V&a){return a[0]||a[1]||a[2];}
bool parallel(const V&a,const V&b){return !nonzero(cross(a,b));}
int dot(const V&a,const V&b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
std::vector<V> rows(uint16_t mask){
 int root=-1;for(int i=0;i<10;i++)if(mask>>i&1){root=i;break;}
 std::vector<V> out;
 for(int i=root+1;i<10;i++)if(mask>>i&1)out.push_back(V{Y[i][0]-Y[root][0],Y[i][1]-Y[root][1],Y[i][2]-Y[root][2]});
 return out;
}
int rank_rows(const std::vector<V>&r){
 V a{0,0,0},b{0,0,0};bool ha=false,hb=false;
 for(auto x:r){
  if(!nonzero(x))continue;
  if(!ha){a=x;ha=true;continue;}
  if(!hb && !parallel(a,x)){b=x;hb=true;continue;}
  if(hb && det3(a,b,x)!=0)return 3;
 }
 return hb?2:(ha?1:0);
}
std::vector<V> all_rows(uint16_t a,uint16_t b){auto r=rows(a),s=rows(b);r.insert(r.end(),s.begin(),s.end());return r;}
bool common_invariant(uint16_t m1,uint16_t m2){
 auto r=all_rows(m1,m2);int rk=rank_rows(r);
 if(rk==3)return false;
 if(rk==0)return true;
 V a{0,0,0},b{0,0,0};bool ha=false,hb=false;
 for(auto x:r)if(nonzero(x)){
  if(!ha){a=x;ha=true;}
  else if(!hb&&!parallel(a,x)){b=x;hb=true;break;}
 }
 if(rk==1){
  if(a[2]!=0)return true; // qA=qB=1, solve qC.
  if(a[0]==0&&a[1]==0)return true;
  return 1LL*a[0]*a[1]<0;
 }
 V n=cross(a,b);
 return n[0]!=0&&n[1]!=0&&1LL*n[0]*n[1]>0;
}
int deficiency(uint16_t a,uint16_t b){return __builtin_popcount(a)+__builtin_popcount(b)-2-rank_rows(all_rows(a,b));}

enum Kind {AVAILABLE,SHIELDED};
Kind classify(uint16_t mask,const V&h){
 int mx=-1;std::vector<int> ys,top;
 for(int i=0;i<10;i++)if(mask>>i&1){ys.push_back(i);mx=std::max(mx,dot(h,Y[i]));}
 for(int i:ys)if(dot(h,Y[i])==mx)top.push_back(i);
 if(top.size()==ys.size())return SHIELDED;
 for(int i:top)if(Y[i][0]+Y[i][1]>=2)return AVAILABLE;
 std::set<int>K;
 for(int i:top){if(Y[i][0])K.insert(0);if(Y[i][1])K.insert(1);}
 bool allq=true;
 for(int i:ys){int q=0;for(int j:K)q+=Y[i][j];if(q!=1){allq=false;break;}}
 if(allq)return SHIELDED;
 for(int i:top)if(Y[i][0]+Y[i][1]+Y[i][2]==1)return AVAILABLE;
 bool service=false;for(int i:top)if(Y[i][2])service=true;
 if(service){
  for(int i:ys)if(dot(h,Y[i])<mx&&Y[i][2])return AVAILABLE;
 }
 return SHIELDED;
}
int pindex(int idx,const std::array<int,3>&p){V z{0,0,0};for(int i=0;i<3;i++)z[p[i]]=Y[idx][i];for(int j=0;j<10;j++)if(Y[j]==z)return j;return -1;}
uint16_t pmask(uint16_t m,const std::array<int,3>&p){uint16_t q=0;for(int i=0;i<10;i++)if(m>>i&1)q|=uint16_t(1u<<pindex(i,p));return q;}
bool service_template(uint16_t a,uint16_t b){
 const uint16_t s1a=(1u<<3)|(1u<<6); // C,2C
 const uint16_t s1b=(1u<<0)|(1u<<1)|(1u<<4)|(1u<<9); //0,A,2A,BC
 const uint16_t s2a=(1u<<0)|(1u<<3)|(1u<<6);
 const uint16_t s2b=(1u<<1)|(1u<<4)|(1u<<9);
 std::array<int,3> p{0,1,2};
 do{
  auto x=pmask(a,p),y=pmask(b,p);
  if((x==s1a&&y==s1b)||(y==s1a&&x==s1b)||(x==s2a&&y==s2b)||(y==s2a&&x==s2b))return true;
 }while(std::next_permutation(p.begin(),p.end()));
 return false;
}

int main(){
 long long assignments=0,shielded=0,common=0,dz=0,service=0,fail=0;
 std::map<int,long long> bydef;
 const int total=59049; //3^10
 for(auto h:H){
  for(int code=0;code<total;code++){
   int z=code;uint16_t m1=0,m2=0;
   for(int i=0;i<10;i++){int d=z%3;z/=3;if(d==1)m1|=1u<<i;else if(d==2)m2|=1u<<i;}
   if(__builtin_popcount(m1)<2||__builtin_popcount(m2)<2)continue;
   assignments++;
   if(classify(m1,h)!=SHIELDED||classify(m2,h)!=SHIELDED)continue;
   shielded++;
   if(common_invariant(m1,m2)){common++;continue;}
   int d=deficiency(m1,m2);bydef[d]++;
   if(d==0){dz++;continue;}
   if(d==1&&service_template(m1,m2)){service++;continue;}
   fail++;
   if(fail<10){std::cerr<<"FAIL d="<<d<<" h="<<h[0]<<","<<h[1]<<" masks="<<m1<<","<<m2<<"\n";}
  }
 }
 std::cout<<"{\"status\":\""<<(fail?"fail":"pass")<<"\",\"workload_assignments_checked\":"<<assignments
          <<",\"shielded_assignments\":"<<shielded<<",\"common_invariant_assignments\":"<<common
          <<",\"deficiency_zero_assignments\":"<<dz<<",\"service_assignments\":"<<service
          <<",\"unclassified_assignments\":"<<fail<<",\"noninvariant_deficiency_counts\":{\"0\":"<<bydef[0]<<",\"1\":"<<bydef[1]<<"}}\n";
 return fail?1:0;
}
