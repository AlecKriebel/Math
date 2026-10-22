// Independent descending-subset enumeration. No comparable-pair recurrence.
#include <cstdint>
#include <iostream>
#include <stdexcept>
using U=uint64_t;
int d,q,best; uint64_t count; U witness;
void visit(int x,U family,U unions){
 if(x<0){++count;if((family&1)==0 && ((family>>(q-1))&1)){int score=__builtin_popcountll(family)-__builtin_popcountll(unions);if(score>best){best=score;witness=family;}}return;}
 visit(x-1,family,unions);
 for(int i=0;i<d;++i)if(!(x>>i&1) && !(family>>(x|(1<<i))&1))return;
 U next=unions;
 for(int y=x+1;y<q;++y)if((family>>y&1) && !(x&y))next|=U(1)<<(x|y);
 if(x==0)next|=1; // repeated empty summands
 visit(x-1,family|(U(1)<<x),next);
}
int main(){for(d=1;d<=6;++d){q=1<<d;best=-1;count=0;visit(q-1,0,0);std::cout<<d<<" "<<count<<" "<<best<<" "<<witness<<"\n";}}
