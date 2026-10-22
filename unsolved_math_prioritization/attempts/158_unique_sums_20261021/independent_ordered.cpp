#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
using namespace std;
int p,n; uint64_t seen; vector<int>A, witness;
bool search(int next){
 if((int)A.size()==n){
  ++seen; int r[32]={0};
  for(int x:A)for(int y:A)++r[(x+y)%p];
  for(int s=0;s<p;++s)if(r[s]==1||r[s]==2)return false;
  witness=A; return true;
 }
 for(int x=next;x<=p-(n-(int)A.size());++x){A.push_back(x);if(search(x+1))return true;A.pop_back();}
 return false;
}
int main(){for(int prime:{3,5,7,11,13,17,19,23,29,31}){p=prime;
 // Every singleton fails: its one diagonal sum has ordered count one.
 cout<<"p="<<p<<" n=1 candidates=1 found=0\n";
 for(n=2;n<=p;++n){A={0,1};seen=0;bool yes=search(2);cout<<"p="<<p<<" n="<<n<<" candidates="<<seen<<" found="<<yes;if(yes){cout<<" witness=";for(int x:witness)cout<<x<<",";}cout<<"\n";if(yes)break;}
}}
