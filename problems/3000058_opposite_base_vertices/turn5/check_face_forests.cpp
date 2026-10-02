#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <vector>
using namespace std;
vector<int> partition(const vector<int>&b,const vector<int>&sum,int sign,int n){
 int N=1<<n,cur=0;vector<int>parts;
 while(cur!=N-1){int best=-1;
  for(int s=0;s<N;s++)if(s!=cur && (s&cur)==cur && b[s]==sign*sum[s])if(best<0||__builtin_popcount((unsigned)s)<__builtin_popcount((unsigned)best))best=s;
  assert(best>=0);parts.push_back(best^cur);cur=best;
 }
 return parts;
}
int main(){long long tables=0,maxpoints=0,forestchecks=0,badmax=0;int exampleN=0,exampleMask=0,exampleCode=0;array<long long,6>zeroHist{};
 for(int n=1;n<=5;n++){
  int N=1<<n,full=N-1;vector<int>b(N),freeS;
  for(int s=1;s<full;s++){b[s]=1;int k=__builtin_popcount((unsigned)s);if(min(k,n-k)==2)freeS.push_back(s);}
  vector<array<int,4>>ineq;for(int s=0;s<N;s++)for(int i=0;i<n;i++)if(!(s>>i&1))for(int j=i+1;j<n;j++)if(!(s>>j&1))ineq.push_back({s|(1<<i),s|(1<<j),s,s|(1<<i)|(1<<j)});
  struct P{int code,support;vector<int>x,sum;};vector<P>pts;int T=1;for(int i=0;i<n;i++)T*=3;
  for(int code=0;code<T;code++){P p;p.code=code;p.support=0;p.x.resize(n);int z=code,total=0;for(int i=0;i<n;i++){p.x[i]=z%3-1;z/=3;total+=p.x[i];p.support+=p.x[i]!=0;}if(total)continue;p.sum.resize(N);for(int s=1;s<N;s++){int i=__builtin_ctz((unsigned)s);p.sum[s]=p.sum[s^(1<<i)]+p.x[i];}pts.push_back(p);}
  for(int mask=0;mask<(1<<(int)freeS.size());mask++){
   for(int j=0;j<(int)freeS.size();j++)b[freeS[j]]=1+((mask>>j)&1);
   bool ok=true;for(auto q:ineq)if(b[q[0]]+b[q[1]]<b[q[2]]+b[q[3]]){ok=false;break;}if(!ok)continue;tables++;
   int ms=-1;vector<int>allowed;
   for(int j=0;j<(int)pts.size();j++){auto&p=pts[j];ok=true;for(int s=0;s<N;s++)if(abs(p.sum[s])>b[s]){ok=false;break;}if(!ok)continue;if(p.support>ms){ms=p.support;allowed.clear();}if(p.support==ms)allowed.push_back(j);}
   for(int j:allowed){auto&p=pts[j];maxpoints++;zeroHist[n-p.support]++;auto A=partition(b,p.sum,1,n),B=partition(b,p.sum,-1,n);int k=A.size(),l=B.size();vector<int>dsu(k+l);for(int i=0;i<k+l;i++)dsu[i]=i;
    auto root=[&](int x){while(dsu[x]!=x)x=dsu[x];return x;};
    for(int i=0;i<n;i++){int a=0,c=0;while(!(A[a]>>i&1))a++;while(!(B[c]>>i&1))c++;int u=root(a),v=root(k+c);assert(u!=v);dsu[u]=v;forestchecks++;
     if(p.x[i])assert(__builtin_popcount((unsigned)A[a])==1&&__builtin_popcount((unsigned)B[c])==1);
    }
    bool both=(k==n&&l==n);if(!both){badmax++;if(!exampleN){exampleN=n;exampleMask=mask;exampleCode=p.code;}}
    if(n-p.support<=1)assert(both);
   }
  }
 }
 cout<<"{\n  \"accepted_tables\": "<<tables<<",\n  \"maximum_support_points\": "<<maxpoints<<",\n  \"acyclic_edge_checks\": "<<forestchecks<<",\n  \"maximum_support_points_not_both_original_vertices\": "<<badmax<<",\n  \"first_such_example\": ["<<exampleN<<", "<<exampleMask<<", "<<exampleCode<<"],\n  \"zero_coordinate_histogram\": [";
 for(int i=0;i<6;i++){if(i)cout<<", ";cout<<zeroHist[i];}cout<<"],\n  \"status\": \"PASS; finite exact forest and face-dimension controls only\"\n}\n";
}
