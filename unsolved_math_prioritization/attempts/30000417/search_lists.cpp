#include <bits/stdc++.h>
using namespace std;
uint64_t farbits[64]; int N,D,K,M;
int score(const vector<uint64_t>& L){
 uint64_t a[64]={},b[64]={};
 uint64_t cur=L[1];while(cur){int j=__builtin_ctzll(cur);cur&=cur-1;a[j]=L[0]&farbits[j];}
 for(int i=2;i<N;i++){
  memset(b,0,sizeof(b));uint64_t next=L[i];
  while(next){int j=__builtin_ctzll(next);next&=next-1;
   uint64_t prior=L[i-1]&farbits[j];
   while(prior){int h=__builtin_ctzll(prior);prior&=prior-1;if(a[h]&farbits[j])b[j]|=1ULL<<h;}}
  memcpy(a,b,sizeof(a));
 }
 int s=0;for(int j=0;j<M;j++)s+=__builtin_popcountll(a[j]);return s;
}
int main(){mt19937_64 rng(20261002);long long total=0;
 vector<pair<int,int>> cases={{4,2},{5,2},{6,2},{7,2},{4,3},{5,3},{6,3},{8,3},{9,3},{4,4},{5,4},{4,6},{4,8},{5,6}};
 for(auto [n,d]:cases){N=n;D=d;K=(3*d*(n-1))/n+1;int best=100000;vector<uint64_t>bestL;
  for(int restart=0;restart<80;restart++){
   M=K+2+(restart%(min(3*d,62-K)-1));uint64_t all=(1ULL<<M)-1;
   for(int c=0;c<M;c++){farbits[c]=0;for(int e=0;e<M;e++)if(abs(c-e)>=D)farbits[c]|=1ULL<<e;}
   vector<uint64_t>L(N);
   for(auto &x:L){x=0;while(__builtin_popcountll(x)<K)x|=1ULL<<(rng()%M);}
   int old=score(L);
   for(int st=0;st<2500;st++){
    int v=rng()%N;uint64_t before=L[v];int j=rng()%K;uint64_t t=before;while(j--)t&=t-1;int rem=__builtin_ctzll(t);uint64_t missing=all^before;j=rng()%__builtin_popcountll(missing);while(j--)missing&=missing-1;int add=__builtin_ctzll(missing);
    L[v]^=(1ULL<<rem)|(1ULL<<add);int now=score(L);total++;
    if(now<best){best=now;bestL=L;}
    if(now==0){cout<<"FOUND "<<N<<" "<<D<<" "<<K<<" "<<M<<"\n";for(auto x:L){for(int j=0;j<M;j++)if(x>>j&1)cout<<j+1<<",";cout<<"\n";}return 0;}
    double temp=0.25+3.0*(1.0-(st%500)/500.0);
    if(now<=old||generate_canonical<double,53>(rng)<exp((old-now)/temp))old=now;else L[v]=before;
   }
  }
  cout<<"NO_WITNESS n="<<N<<" d="<<D<<" k="<<K<<" best_terminal_pairs="<<best<<" trials="<<200000<<" total="<<total<<endl;
 }
}
