// Exhaustive exact endpoint search for n=2,d=3 when all four within-side
// factors are vectorizations of signed 3-by-3 permutation matrices.
// These factors have full support on both copies and evade the local-support
// obstruction.  The search is finite and exact, but covers only this ansatz.

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

struct V { int x[9] = {}; };
struct E { int a,b,z; };
using C = std::vector<E>;

static std::vector<V> signed_permutations() {
  std::vector<V> out;
  int p[3]={0,1,2};
  do {
    for(int signs=0;signs<8;++signs) {
      V v;
      for(int row=0;row<3;++row)
        v.x[3*row+p[row]]=(signs&(1<<row)) ? -1:1;
      out.push_back(v);
    }
  } while(std::next_permutation(p,p+3));
  return out;
}

static C outer(const V& u,const V& v) {
  C z;
  for(int a=0;a<9;++a) if(u.x[a])
    for(int b=0;b<9;++b) if(v.x[b])
      z.push_back({a,b,u.x[a]*v.x[b]});
  return z;
}

static int kernel(int a,int b,int c,int e) {
  int z=1;
  for(int site=0;site<2;++site) {
    int ai=a%3,bi=b%3,ci=c%3,ei=e%3;
    z*=2*(ai==ci && bi==ei)-(ai==bi && ci==ei);
    a/=3;b/=3;c/=3;e/=3;
  }
  return z;
}

static int64_t form(const C& A,const C& B) {
  int64_t z=0;
  for(auto p:A) for(auto q:B)
    z+=int64_t(p.z)*q.z*kernel(p.a,p.b,q.a,q.b);
  return z;
}

static void print_v(const char* name,const V& v) {
  std::cout<<name<<"\n";
  for(int i=0;i<3;++i) {
    for(int j=0;j<3;++j) std::cout<<v.x[3*i+j]<<" ";
    std::cout<<"\n";
  }
}

int main() {
  std::vector<V> p=signed_permutations();
  const int N=p.size(),M=N*N;
  std::vector<C> terms;
  terms.reserve(M);
  for(int u=0;u<N;++u) for(int v=0;v<N;++v)
    terms.push_back(outer(p[u],p[v]));
  long double best=0;
  int bt=-1,bs=-1;
  int64_t b11=0,b12=0,b22=0;
  uint64_t tested=0;
  for(int t=0;t<M;++t) {
    int u1=t/N,v1=t%N;
    int64_t r11=form(terms[t],terms[t]);
    for(int s=t+1;s<M;++s) {
      int u2=s/N,v2=s%N;
      // Exclude proportional column or row pairs, which only reproduce a
      // rank-one coefficient matrix after combining terms.
      bool up=true,vp=true,um=true,vm=true;
      for(int j=0;j<9;++j) {
        up &= p[u1].x[j]==p[u2].x[j];
        um &= p[u1].x[j]==-p[u2].x[j];
        vp &= p[v1].x[j]==p[v2].x[j];
        vm &= p[v1].x[j]==-p[v2].x[j];
      }
      if(up||um||vp||vm) continue;
      ++tested;
      int64_t r12=form(terms[t],terms[s]);
      int64_t r22=form(terms[s],terms[s]);
      if((__int128)r12*r12>(__int128)r11*r22) {
        std::cout<<"NEGATIVE signed-permutation span\n";
        std::cout<<"R11 "<<r11<<" R12 "<<r12<<" R22 "<<r22<<"\n";
        std::cout<<"witness = R22*C1-R12*C2\n";
        print_v("u1",p[u1]);print_v("v1",p[v1]);
        print_v("u2",p[u2]);print_v("v2",p[v2]);
        return 0;
      }
      long double ratio=(long double)r12*r12/
                        ((long double)r11*r22);
      if(ratio>best) {
        best=ratio;bt=t;bs=s;b11=r11;b12=r12;b22=r22;
      }
    }
  }
  std::cout.precision(18);
  std::cout<<"no negative span among "<<tested
           <<" nondegenerate pairs; best ratio "<<best<<"\n";
  std::cout<<"R11 "<<b11<<" R12 "<<b12<<" R22 "<<b22<<"\n";
  print_v("u1",p[bt/N]);print_v("v1",p[bt%N]);
  print_v("u2",p[bs/N]);print_v("v2",p[bs%N]);
}
