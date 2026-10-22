#include <bits/stdc++.h>
using namespace std;
int M=8,K=6,D=2;vector<int> lists;vector<int> farb;using S=array<uint16_t,12>;
struct H {size_t operator()(S const&a)const{size_t h=0;for(auto x:a)h=h*1000003+x;return h;}};
S step(S const&a,int L){S b={};for(int c=0;c<M;c++)if(L>>c&1)for(int x=0;x<M;x++)if((farb[c]>>x&1)&&(a[x]&farb[c]))b[c]|=1<<x;return b;}
int robust(S const&a){int ct=0;for(int i=0;i<M;i++)if(a[i]){int low=__builtin_ctz(a[i]),hi=31-__builtin_clz((unsigned)a[i]);if(hi-low>=2*D-1)ct++;}return ct;}
int main(int argc,char**argv){if(argc>1)M=atoi(argv[1]);for(int L=0;L<(1<<M);L++)if(__builtin_popcount((unsigned)L)==K)lists.push_back(L);for(int a=0;a<M;a++){int m=0;for(int b=0;b<M;b++)if(abs(a-b)>=D)m|=1<<b;farb.push_back(m);}
 unordered_set<S,H>seen;vector<S>q;for(int A:lists)for(int B:lists){S t={};for(int b=0;b<M;b++)if(B>>b&1)t[b]=A&farb[b];if(seen.insert(t).second)q.push_back(t);}
 size_t start=0;int minrob=99;long long transitions=0;
 while(start<q.size()){
  S a=q[start++];int r=robust(a);if(r<minrob){minrob=r;cout<<"minrob="<<r<<" processed="<<start<<" states="<<q.size()<<"\n";for(int i=0;i<M;i++)if(a[i])cout<<i<<":"<<a[i]<<" ";cout<<endl;}
  for(int L:lists){S t=step(a,L);transitions++;if(all_of(t.begin(),t.end(),[](int x){return x==0;})){cout<<"EMPTY FOUND"<<endl;return 0;}if(seen.insert(t).second)q.push_back(t);}
  if(start%100000==0)cout<<"progress="<<start<<" states="<<q.size()<<endl;
  if(q.size()>2000000){cout<<"CAP states="<<q.size()<<endl;return 0;}
 }
 cout<<"CLOSED M="<<M<<" states="<<q.size()<<" transitions="<<transitions<<" minrob="<<minrob<<endl;
}
