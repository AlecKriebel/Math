// Exact exhaustive proof for d<=6. No floating-point arithmetic or assert checks.
#include <cstdint>
#include <vector>
#include <iostream>
#include <stdexcept>
using U=uint64_t;
int pc(U x){return __builtin_popcountll(x);}
std::vector<U> upsets(int d){
 if(d==0)return {0,1};
 auto prev=upsets(d-1); std::vector<U> out;int shift=1<<(d-1);
 for(U a:prev)for(U b:prev)if((a&~b)==0)out.push_back(a|(b<<shift));
 return out;
}
U unions(U a,U b,int q){U out=0;for(int x=0;x<q;x++)if(a>>x&1)for(int y=0;y<q;y++)if((b>>y&1)&&!(x&y))out|=U(1)<<(x|y);return out;}
int main(){
 for(int d=1;d<=6;d++){
  auto small=upsets(d-1);int q=1<<(d-1),M=small.size();
  std::vector<U> D(M);std::vector<std::vector<U>> cross(q,std::vector<U>(M));
  for(int j=0;j<M;j++){
   D[j]=unions(small[j],small[j],q);
   for(int x=0;x<q;x++)cross[x][j]=unions(U(1)<<x,small[j],q);
  }
  uint64_t count=0;int best=-1;U witness=0;
  for(int i=0;i<M;i++)for(int j=0;j<M;j++)if(!(small[i]&~small[j])){
   count++;U f=small[i]|(small[j]<<q);
   // Proper admissible F excludes empty and includes the full set.
   if((f&1)||!(f>>(2*q-1)&1))continue;
   U D1=0;for(int x=0;x<q;x++)if(small[i]>>x&1)D1|=cross[x][j];
   int score=pc(small[i])+pc(small[j])-pc(D[i])-pc(D1);
   if(score>best){best=score;witness=f;}
  }
  U fullD=unions(witness,witness,2*q);
  if(pc(witness)-pc(fullD)!=best)throw std::runtime_error("Witness mismatch");
  std::cout<<"d="<<d<<" upsets="<<count<<" maximum_deficiency="<<best<<" witness="<<witness<<"\n";
 }
}
