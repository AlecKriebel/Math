#include <iostream>
#include <vector>
#include <array>
using namespace std;
long long tested; int p; array<int,7> a; bool found;
void rec(int depth,int start){
 if(depth==7){
  ++tested; array<int,64> r{};
  for(int i=0;i<7;i++)for(int j=i;j<7;j++)++r[(a[i]+a[j])%p];
  for(int s=0;s<p;s++)if(r[s]==1)return;
  found=true; cout<<"WITNESS ";for(auto x:a)cout<<x<<' ';cout<<'\n';return;
 }
 for(int x=start;x<=p-(7-depth);x++){a[depth]=x;rec(depth+1,x+1);}
}
int main(){for(int q:{17,19,23,29,31,37,41,43,47,53,59,61}){
 p=q;tested=0;found=false;a[0]=0;a[1]=1;rec(2,2);
 cout<<p<<" "<<tested<<" "<<(found?"FOUND":"NONE")<<endl;
}}
