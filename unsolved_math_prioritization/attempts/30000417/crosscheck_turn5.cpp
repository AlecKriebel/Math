#include <bits/stdc++.h>
using namespace std; using U=__uint128_t;
struct Hash {size_t operator()(U x)const{uint64_t a=x,b=x>>64;a^=b+0x9e3779b97f4a7c15ULL+(a<<6)+(a>>2);a^=a>>30;a*=0xbf58476d1ce4e5b9ULL;a^=a>>27;a*=0x94d049bb133111ebULL;return a^(a>>31);}};
int main(int argc,char**argv){int M=argc>1?atoi(argv[1]):9,K=argc>2?atoi(argv[2]):6,D=argc>3?atoi(argv[3]):2;size_t cap=argc>4?stoull(argv[4]):8000000;
 if(M>11||M<1||K>M)return 2;
 vector<unsigned> lists,far(M);vector<U>masks;
 for(unsigned L=0;L<(1u<<M);L++)if(__builtin_popcount(L)==K){lists.push_back(L);U mask=0;for(int c=0;c<M;c++)if(L>>c&1)mask|=U((1u<<M)-1)<<(M*c);masks.push_back(mask);}
 for(int a=0;a<M;a++)for(int b=0;b<M;b++)if(abs(a-b)>=D)far[a]|=1u<<b;
 vector<U> q;vector<uint32_t>parent;vector<uint16_t>incoming,first,depth;unordered_set<U,Hash>seen;
 for(unsigned ai=0;ai<lists.size();ai++)for(unsigned bi=0;bi<lists.size();bi++){
  U s=0;for(int b=0;b<M;b++)if(lists[bi]>>b&1)s|=U(lists[ai]&far[b])<<(M*b);
  if(!s){cout<<"EMPTY_INITIAL\n";return 0;}
  if(seen.insert(s).second){q.push_back(s);parent.push_back(UINT32_MAX);incoming.push_back(bi);first.push_back(ai);depth.push_back(2);}}
 size_t initial=q.size(),head=0;uint64_t transitions=0;unsigned maxdepth=2;
 while(head<q.size()){
  U s=q[head],full=0;unsigned rows[11];for(int b=0;b<M;b++)rows[b]=(s>>(M*b))&((1u<<M)-1);
  for(int c=0;c<M;c++){unsigned out=0;for(int b=0;b<M;b++)if((far[c]>>b&1)&&(rows[b]&far[c]))out|=1u<<b;full|=U(out)<<(M*c);}
  for(unsigned li=0;li<lists.size();li++){
   U nxt=full&masks[li];transitions++;
   if(!nxt){vector<unsigned>wit{lists[li]};size_t cur=head;while(parent[cur]!=UINT32_MAX){wit.push_back(lists[incoming[cur]]);cur=parent[cur];}wit.push_back(lists[incoming[cur]]);wit.push_back(lists[first[cur]]);reverse(wit.begin(),wit.end());cout<<"EMPTY length="<<wit.size()<<" M="<<M<<" K="<<K<<" D="<<D<<"\n";for(unsigned L:wit){for(int c=0;c<M;c++)if(L>>c&1)cout<<c+1<<",";cout<<"\n";}return 0;}
   if(seen.insert(nxt).second){q.push_back(nxt);parent.push_back(head);incoming.push_back(li);first.push_back(0);depth.push_back(depth[head]+1);maxdepth=max(maxdepth,unsigned(depth.back()));}
  }
  head++;
  if(head%500000==0)cout<<"PROGRESS head="<<head<<" states="<<q.size()<<" depth="<<depth[head-1]<<endl;
  if(q.size()>cap){cout<<"CAPPED states="<<q.size()<<" processed="<<head<<" depth="<<maxdepth<<endl;return 0;}
 }
 cout<<"CLOSED M="<<M<<" K="<<K<<" D="<<D<<" inputs="<<lists.size()<<" initial="<<initial<<" states="<<q.size()<<" transitions="<<transitions<<" max_shortest_length="<<maxdepth<<endl;
 if(argc>5){sort(q.begin(),q.end());ofstream f(argv[5],ios::binary);int width=(M*M+7)/8;for(U s:q)for(int j=0;j<width;j++){char c=(s>>(8*j))&255;f.write(&c,1);}f.close();cout<<"STATE_BYTES "<<q.size()*width<<endl;}
}
