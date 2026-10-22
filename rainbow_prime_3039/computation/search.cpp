// Exact exhaustive search, no external dependencies. C++17.
#include <bits/stdc++.h>
using namespace std;
int p,lo,hi; vector<array<int,4>> edges; uint64_t nodes; double seconds; chrono::steady_clock::time_point start; bool timedout; vector<int> solution;
int bits(int x){return __builtin_popcount((unsigned)x);}
bool propagate(vector<int>&dom){
 bool changed=true;
 while(changed){changed=false;
  for(int x:dom) if(!x)return false;
  for(int c=0;c<4;c++){
   int b=1<<c, fixed=0, possible=0;
   for(int x:dom){fixed+=x==b;possible+=(x&b)!=0;}
   if(fixed>hi || possible<lo)return false;
   if(fixed==hi)for(int &x:dom)if(x!=b && (x&b)){x^=b;changed=true;if(!x)return false;}
   if(possible==lo)for(int &x:dom)if((x&b) && x!=b){x=b;changed=true;}
  }
  for(auto e:edges){
   // A forbidden all-different edge with three fixed distinct colors.
   for(int omitted=0;omitted<4;omitted++){
    int used=0;bool distinct=true;
    for(int j=0;j<4;j++)if(j!=omitted){int x=dom[e[j]];if(bits(x)!=1 || (used&x)){distinct=false;break;} used|=x;}
    if(distinct){int &x=dom[e[omitted]],bad=15^used;if(x&bad){x^=bad;changed=true;if(!x)return false;}}
   }
  }
 }
 return true;
}
bool dfs(vector<int> dom){
 nodes++;if(nodes%1024==0 && chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds){timedout=true;return false;}
 if(!propagate(dom))return false;
 int v=-1,best=5;for(int i=0;i<p;i++)if(bits(dom[i])>1&&bits(dom[i])<best){v=i;best=bits(dom[i]);}
 if(v<0){solution=dom;return true;}
 for(int c=0;c<4;c++)if(dom[v]&(1<<c)){auto next=dom;next[v]=1<<c;if(dfs(next))return true;if(timedout)return false;}
 return false;
}
int main(int argc,char**argv){
 p=argc>1?atoi(argv[1]):13;seconds=argc>2?atof(argv[2]):30;lo=p/4;hi=(p+3)/4;
 if(argc>3){lo=atoi(argv[3]);hi=p-3*lo;}
 if(p<5){cerr<<"Use primes >=5\n";return 2;}
 for(int d=2;d*d<=p;d++)if(p%d==0){cerr<<"Prime required\n";return 2;}
 set<array<int,4>> unique;
 for(int a=0;a<p;a++)for(int d=1;d<p;d++){array<int,4>e;for(int j=0;j<4;j++)e[j]=(a+j*d)%p;sort(e.begin(),e.end());unique.insert(e);}
 edges.assign(unique.begin(),unique.end());vector<int>dom(p,15);dom[0]=1;dom[1]=2;
 // Every balanced coloring has two distinct-colored points u,v. The invertible
 // affine substitution x -> u+(v-u)x moves these to 0,1. Relabel their colors.
 // No size ordering or extra spatial symmetry is assumed.
 nodes=0;start=chrono::steady_clock::now();bool sat=dfs(dom);
 cout<<"{\"p\":"<<p<<",\"min_size\":"<<lo<<",\"max_size\":"<<hi<<",\"edges\":"<<edges.size()<<",\"nodes\":"<<nodes<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"status\":\""<<(sat?"SAT":timedout?"UNKNOWN_TIMEOUT":"UNSAT_EXHAUSTIVE")<<"\"";
 if(sat){cout<<",\"coloring\":[";for(int i=0;i<p;i++)cout<<(i?",":"")<<__builtin_ctz((unsigned)solution[i]);cout<<"]";}
 cout<<"}\n";
}
