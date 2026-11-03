// Exact arithmetic in F_3[z]/(z^7+z^2+2). No external libraries.
#include <array>
#include <vector>
#include <iostream>
#include <stdexcept>
using namespace std;
const int Q=2187,N=7; int pw[8]; vector<array<int,7>> dig(Q); vector<unsigned short> addt(Q*Q),mult(Q*Q); int fr[Q];
int add(int a,int b){return addt[a*Q+b];} int mul(int a,int b){return mult[a*Q+b];}
int power(int a,int b){int v=1;while(b){if(b&1)v=mul(v,a);a=mul(a,a);b>>=1;}return v;}
int rk(array<int,7> cols){int base[7]={},r=0;for(int v:cols){for(int j=0;j<7&&v;j++){int c=dig[v][j];if(!c)continue;if(base[j])v=add(v,mul(3-c,base[j]));else{base[j]=mul(c,v);++r;break;}}}return r;}
int main(){pw[0]=1;for(int i=1;i<=7;i++)pw[i]=3*pw[i-1];for(int a=0;a<Q;a++)for(int j=0;j<7;j++)dig[a][j]=a/pw[j]%3;
for(int a=0;a<Q;a++)for(int b=0;b<Q;b++){int s=0,t[13]={};for(int j=0;j<7;j++){s+=((dig[a][j]+dig[b][j])%3)*pw[j];for(int k=0;k<7;k++)t[j+k]+=dig[a][j]*dig[b][k];}addt[a*Q+b]=s;for(int j=12;j>=7;j--){int c=t[j]%3;t[j-7]+=c; t[j-5]+=2*c;}s=0;for(int j=0;j<7;j++)s+=(t[j]%3)*pw[j];mult[a*Q+b]=s;}
// Exhaustive nonzero inverses certify this quotient is a field, not merely a ring.
for(int a=1;a<Q;a++)if(mul(a,power(a,Q-2))!=1)throw runtime_error("nonfield");
for(int a=0;a<Q;a++)fr[a]=power(a,3);
cout<<"{\n  \"field\": \"F_3[z]/(z^7+z^2+2)\",\n  \"nonzero_inverse_checks\": 2186,\n  \"codes\": [\n";
for(int type=0;type<2;type++){array<array<int,7>,3> g;for(int j=0;j<7;j++){int x=pw[j];if(type==0){g[0][j]=x;g[1][j]=power(x,3);g[2][j]=power(x,27);}else{g[0][j]=add(x,power(x,27));g[1][j]=power(x,3);g[2][j]=power(x,9);}}
long long hist[8]={};for(int lead=0;lead<3;lead++){int lim1=lead<1?Q:1,lim2=lead<2?Q:1;for(int a=0;a<lim1;a++)for(int b=0;b<lim2;b++){int coeff[3]={};coeff[lead]=1;if(lead==0){coeff[1]=a;coeff[2]=b;}if(lead==1)coeff[2]=b;array<int,7> c{};for(int j=0;j<7;j++)for(int i=0;i<3;i++)c[j]=add(c[j],mul(coeff[i],g[i][j]));hist[rk(c)]++;}}
long long total=0;for(int j=0;j<8;j++)total+=hist[j];if(total!=1LL*Q*Q+Q+1||hist[5]==0)throw runtime_error("enumeration/minimum failure");
cout<<"    {\"name\": \""<<(type==0?"monomial_013":"twisted_eta1")<<"\", \"projective_rank_histogram\": [";for(int j=0;j<8;j++)cout<<(j?", ":"")<<hist[j];cout<<"]}"<<(type==0?",\n":"\n");if(hist[0]+hist[1]+hist[2]+hist[3]+hist[4])throw runtime_error("not MRD");}
cout<<"  ]\n}\n";
}
