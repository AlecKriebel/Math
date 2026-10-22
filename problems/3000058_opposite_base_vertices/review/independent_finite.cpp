#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>
using namespace std;
using Vec=vector<int>;
long long assertions=0;
void check(bool v){assert(v);++assertions;}
int inv(int a){for(int i=1;i<101;i++)if(a*i%101==1)return i;assert(false);return 0;}
int rank_rows(vector<Vec> a,int n){int r=0;for(int j=0;j<n;j++){int p=r;while(p<(int)a.size()&&!a[p][j])p++;if(p==(int)a.size())continue;swap(a[p],a[r]);int z=inv(a[r][j]);for(int &v:a[r])v=v*z%101;for(int i=0;i<(int)a.size();i++)if(i!=r){int c=a[i][j];for(int k=0;k<n;k++)a[i][k]=(a[i][k]-c*a[r][k]%101+101)%101;}r++;if(r==n)break;}return r;}
Vec indicator(int S,int n){Vec r(n);for(int i=0;i<n;i++)r[i]=S>>i&1;return r;}
int sumset(const Vec&v,int S){int z=0;for(int i=0;i<(int)v.size();i++)if(S>>i&1)z+=v[i];return z;}
vector<Vec> ternary(int n){vector<Vec> out;int N=1;for(int i=0;i<n;i++)N*=3;for(int a=0;a<N;a++){Vec v(n);int t=a,z=0;for(int&i:v){i=t%3-1;t/=3;z+=i;}if(!z)out.push_back(v);}return out;}
Vec minusv(Vec v){for(int&i:v)i=-i;return v;}
bool feasible(const Vec&v,const Vec&b){for(int S=0;S<(int)b.size();S++)if(sumset(v,S)>b[S])return false;return true;}
vector<Vec> active(const Vec&v,const Vec&b){vector<Vec>a;for(int S=1;S<(int)b.size();S++)if(sumset(v,S)==b[S])a.push_back(indicator(S,v.size()));return a;}
int support(const Vec&v){return count_if(v.begin(),v.end(),[](int x){return x!=0;});}
Vec labels(const Vec&v,const Vec&b){int n=v.size();vector<uint64_t>sig(n);for(int S=1;S<(int)b.size();S++)if(sumset(v,S)==b[S])for(int i=0;i<n;i++)if(S>>i&1)sig[i]|=1ULL<<S;map<uint64_t,int>M;Vec lab;for(auto x:sig){if(!M.count(x)){int m=M.size();M[x]=m;}lab.push_back(M[x]);}return lab;}
int main(){
 long long accepted=0,maxpoints=0,failboth=0;vector<int>validcounts,maxvertices;
 // Rank over F101 equals rational rank for these 0/1 matrices: every minor
 // has absolute determinant <=5^(5/2)<101 by Hadamard.
 for(int n=1;n<=5;n++){
  int all=(1<<n)-1;Vec free,b(1<<n,0);for(int S=1;S<all;S++){b[S]=1;if(min(__builtin_popcount((unsigned)S),n-__builtin_popcount((unsigned)S))==2)free.push_back(S);}
  auto pts=ternary(n);int valid=0,mv=0;
  for(int code=0;code<(1<<(int)free.size());code++){
   for(int i=0;i<(int)free.size();i++)b[free[i]]=1+(code>>i&1);
   bool sub=true;for(int A=0;A<=all&&sub;A++)for(int B=0;B<=all;B++)if(b[A]+b[B]<b[A&B]+b[A|B]){sub=false;break;}
   if(!sub)continue;valid++;accepted++;
   set<Vec> verts;vector<Vec>sym;int maxsupp=-1;
   for(auto v:pts)if(feasible(v,b)){
    if(rank_rows(active(v,b),n)==n)verts.insert(v);
    if(feasible(minusv(v),b)){sym.push_back(v);maxsupp=max(maxsupp,support(v));}
   }
   bool opposite=false;for(auto v:verts)if(verts.count(minusv(v))){opposite=true;break;}
   check(opposite);mv=max(mv,(int)verts.size());
   for(auto v:sym)if(support(v)==maxsupp){
    maxpoints++;auto a=labels(v,b),c=labels(minusv(v),b);int ka=*max_element(a.begin(),a.end())+1,kc=*max_element(c.begin(),c.end())+1;Vec parent(ka+kc);iota(parent.begin(),parent.end(),0);
    function<int(int)>root=[&](int x){return parent[x]==x?x:parent[x]=root(parent[x]);};bool forest=true;
    for(int i=0;i<n;i++){int r=root(a[i]),s=root(ka+c[i]);if(r==s)forest=false;else parent[r]=s;}
    check(forest);auto both=active(v,b),other=active(minusv(v),b);both.insert(both.end(),other.begin(),other.end());check(rank_rows(both,n)==n);
    bool endpoint=verts.count(v)&&verts.count(minusv(v));if(!endpoint)failboth++;
    if(n-support(v)<=1)check(endpoint);
   }
  }
  validcounts.push_back(valid);maxvertices.push_back(mv);
 }
 check(validcounts==Vec({1,1,1,64,4209}));check(maxvertices==Vec({1,2,6,14,31}));check(maxpoints==44879);check(failboth==912);
 // Exhaust all laminar upper families on four coordinates, with bounds 0/1.
 int n=4,all=15;auto points=ternary(n);long long lamcases=0;vector<pair<int,int>> disallowed;
 for(int A=1;A<all;A++)for(int B=A+1;B<all;B++)if((A&B)!=0&&(A&B)!=A&&(A&B)!=B)disallowed.push_back({A-1,B-1});
 for(int mask=0;mask<(1<<14);mask++){
  bool lam=true;for(auto [i,j]:disallowed)if((mask>>i&1)&&(mask>>j&1)){lam=false;break;}if(!lam)continue;
  Vec sets;for(int i=0;i<14;i++)if(mask>>i&1)sets.push_back(i+1);
  for(int zero=0;zero<(1<<(int)sets.size());zero++){
   bool found=false;
   for(auto v:points){
    bool feas=true;for(int j=0;j<(int)sets.size();j++){int k=(zero>>j&1)?0:1;if(abs(sumset(v,sets[j]))>k){feas=false;break;}}if(!feas)continue;
    bool vertices=true;for(int sign:{1,-1}){vector<Vec>rows{Vec(n,1)};for(int i=0;i<n;i++)if(v[i]){Vec e(n);e[i]=1;rows.push_back(e);}for(int j=0;j<(int)sets.size();j++){int k=(zero>>j&1)?0:1;if(sign*sumset(v,sets[j])==k)rows.push_back(indicator(sets[j],n));}if(rank_rows(rows,n)!=n)vertices=false;}
    if(vertices){found=true;break;}
   }
   check(found);lamcases++;
  }
 }
 // All small coordinate-simplex multisets with at most four summands on n=4.
 Vec sets;for(int S=1;S<=15;S++)if(__builtin_popcount((unsigned)S)>=2)sets.push_back(S);
 long long hypercases=0,graphicalcases=0;
 function<void(Vec,int)>walk=[&](Vec chosen,int lo){
  Vec degree(4);for(int H:chosen)for(int i=0;i<4;i++)if(H>>i&1)degree[i]++;if(*max_element(degree.begin(),degree.end())>2)return;
  if(!chosen.empty()){
   set<Vec>alloc{Vec(4)};for(int H:chosen){set<Vec>next;for(auto v:alloc)for(int i=0;i<4;i++)if(H>>i&1){auto w=v;w[i]++;next.insert(w);}alloc=next;}
   set<Vec>verts;Vec perm{0,1,2,3};do{Vec v(4);for(int H:chosen)for(int i:perm)if(H>>i&1){v[i]++;break;}verts.insert(v);}while(next_permutation(perm.begin(),perm.end()));
   for(auto a:alloc){bool cube=true;for(int i=0;i<4;i++)if(a[i]>1||degree[i]-a[i]>1)cube=false;if(!cube)continue;bool found=false;for(auto v:verts){Vec w(4);for(int i=0;i<4;i++)w[i]=2*a[i]-v[i];if(verts.count(w)){found=true;break;}}check(found);hypercases++;if(all_of(chosen.begin(),chosen.end(),[](int H){return __builtin_popcount((unsigned)H)==2;}))graphicalcases++;}
  }
  if(chosen.size()==4)return;for(int j=lo;j<(int)sets.size();j++){auto next=chosen;next.push_back(sets[j]);walk(next,j);}
 };
 walk({},0);
 cout<<"{\n  \"status\": \"PASS\",\n  \"independent_assertions\": "<<assertions<<",\n  \"complete_reduced_tables_accepted\": "<<accepted<<",\n  \"maximum_support_points\": "<<maxpoints<<",\n  \"maximum_support_shortcut_failures\": "<<failboth<<",\n  \"laminar_bound_cases_n4\": "<<lamcases<<",\n  \"hypergraphic_translation_cases_n4\": "<<hypercases<<",\n  \"graphical_cases_included\": "<<graphicalcases<<",\n  \"limits\": \"Exact independent finite controls for the bounded interpretation; no general conjecture proof\"\n}\n";
}
