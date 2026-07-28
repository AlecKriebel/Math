// Discovery-only exact Gaussian-integer endpoint search.
//
// It searches spans of C1=u1 v1^T and C2=u2 v2^T.  The Hermitian Gram
// matrix R_rs=2^n<C_r,L(C_s)> is computed exactly in Z[i].  A negative span
// exists iff |R12|^2>R11 R22; in that event
//     C = R22 C1 - conjugate(R12) C2
// is an explicit Gaussian-integer witness.
//
// Build/run:
//   c++ -O3 -std=c++17 agent_witness_sparse_complex.cpp -o awsc
//   ./awsc <d=3> <n> <trials> <max_support> <seed>

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <random>
#include <utility>
#include <vector>

struct GI {
  int64_t r = 0, i = 0;
};
static GI add(GI a, GI b) { return {a.r+b.r,a.i+b.i}; }
static GI neg(GI a) { return {-a.r,-a.i}; }
static GI conjg(GI a) { return {a.r,-a.i}; }
static GI mul(GI a, GI b) {
  return {a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r};
}
static GI scale(GI a, int64_t z) { return {a.r*z,a.i*z}; }
static bool zero(GI a) { return a.r==0 && a.i==0; }

struct SV { std::vector<std::pair<int,GI>> x; };
struct SM {
  struct E { int a,b; GI z; };
  std::vector<E> x;
};

static int ipow(int a,int n) { int z=1; while(n--) z*=a; return z; }

static GI random_gi(std::mt19937_64& rng) {
  static const GI z[] = {
    {1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}
  };
  return z[rng()%8];
}

static SV random_sv(int D,int k,std::mt19937_64& rng) {
  std::vector<int> s(D);
  for(int j=0;j<D;++j) s[j]=j;
  std::shuffle(s.begin(),s.end(),rng);
  SV u;
  for(int j=0;j<k;++j) u.x.push_back({s[j],random_gi(rng)});
  return u;
}

static SV mutate(const SV& u,int D,int maxs,std::mt19937_64& rng) {
  std::map<int,GI> z;
  for(auto p:u.x) z[p.first]=p.second;
  for(int k=0;k<1+int(rng()%3);++k) {
    int action=rng()%3;
    if(action==0 && !z.empty()) {
      auto it=z.begin(); std::advance(it,rng()%z.size()); z.erase(it);
    } else if(action==1 && int(z.size())<maxs) {
      z[rng()%D]=random_gi(rng);
    } else if(!z.empty()) {
      auto it=z.begin(); std::advance(it,rng()%z.size());
      it->second=random_gi(rng);
    }
  }
  if(z.empty()) z[rng()%D]={1,0};
  SV v; for(auto p:z) v.x.push_back(p); return v;
}

static bool proportional(const SV& u,const SV& v) {
  std::map<int,GI> a,b;
  for(auto p:u.x) a[p.first]=p.second;
  for(auto p:v.x) b[p.first]=p.second;
  if(a.size()!=b.size() || a.empty()) return false;
  auto ia=a.begin(),ib=b.begin();
  GI x0=ia->second,y0=ib->second;
  for(;ia!=a.end();++ia,++ib)
    if(ia->first!=ib->first ||
       !zero(add(mul(ia->second,y0),neg(mul(ib->second,x0)))))
      return false;
  return true;
}

static SM outer(const SV& u,const SV& v) {
  SM C;
  for(auto [a,x]:u.x) for(auto [b,y]:v.x)
    C.x.push_back({a,b,mul(x,y)});
  return C;
}

static int kernel(int a,int b,int c,int e,int d,int n) {
  int z=1;
  for(int site=0;site<n;++site) {
    int ai=a%d,bi=b%d,ci=c%d,ei=e%d;
    z*=2*(ai==ci && bi==ei)-(ai==bi && ci==ei);
    if(!z) return 0;
    a/=d;b/=d;c/=d;e/=d;
  }
  return z;
}

static GI form(const SM& C,const SM& D,int d,int n) {
  GI s;
  for(const auto& p:C.x) for(const auto& q:D.x)
    s=add(s,scale(mul(conjg(p.z),q.z),
                  kernel(p.a,p.b,q.a,q.b,d,n)));
  return s;
}

static bool full_at(const SV& u,const SV& v,int site,int d) {
  if(d!=3) return false;
  int stride=ipow(d,site);
  std::map<std::pair<int,int>,std::vector<GI>> fs;
  for(int which=0;which<2;++which) {
    const SV& w=which? v:u;
    for(auto [index,z]:w.x) {
      int digit=(index/stride)%d;
      int rest=index%stride+stride*(index/(stride*d));
      auto& f=fs[{which,rest}];
      if(f.empty()) f.assign(3,{0,0});
      f[digit]=z;
    }
  }
  std::vector<std::vector<GI>> f;
  for(auto& p:fs) f.push_back(p.second);
  for(size_t x=0;x<f.size();++x)
    for(size_t y=x+1;y<f.size();++y)
      for(size_t z=y+1;z<f.size();++z) {
        // det[f[x],f[y],f[z]]
        GI t0=mul(f[x][0],add(mul(f[y][1],f[z][2]),
                              neg(mul(f[y][2],f[z][1]))));
        GI t1=mul(f[x][1],add(mul(f[y][0],f[z][2]),
                              neg(mul(f[y][2],f[z][0]))));
        GI t2=mul(f[x][2],add(mul(f[y][0],f[z][1]),
                              neg(mul(f[y][1],f[z][0]))));
        GI det=add(add(t0,neg(t1)),t2);
        if(!zero(det)) return true;
      }
  return false;
}

static bool common_full(const SV& u1,const SV& u2,
                        const SV& v1,const SV& v2,int d,int n) {
  for(int site=0;site<n;++site)
    if(full_at(u1,u2,site,d) && full_at(v1,v2,site,d)) return true;
  return false;
}

static void print_sv(const char* name,const SV& u) {
  std::cout<<name<<" =";
  for(auto [j,z]:u.x) std::cout<<" ("<<j<<","<<z.r<<","<<z.i<<")";
  std::cout<<"\n";
}

int main(int argc,char** argv) {
  if(argc!=6) {
    std::cerr<<"usage: "<<argv[0]<<" d n trials max_support seed\n";
    return 2;
  }
  int d=std::atoi(argv[1]),n=std::atoi(argv[2]);
  int trials=std::atoi(argv[3]),D=ipow(d,n);
  int maxs=std::min(std::atoi(argv[4]),D);
  uint64_t seed=std::strtoull(argv[5],nullptr,10);
  std::mt19937_64 rng(seed);
  long double best=0;
  GI best12; int64_t best11=0,best22=0;
  SV bu1,bu2,bv1,bv2;
  int accepted=0;
  while(accepted<trials) {
    SV u1=random_sv(D,1+rng()%maxs,rng);
    SV v1=random_sv(D,1+rng()%maxs,rng);
    SV u2,v2;
    if(rng()&1) {
      u2=random_sv(D,1+rng()%maxs,rng);
      v2=random_sv(D,1+rng()%maxs,rng);
    } else {
      u2=mutate(u1,D,maxs,rng); v2=mutate(v1,D,maxs,rng);
    }
    if(proportional(u1,u2) && proportional(v1,v2)) continue;
    if(!common_full(u1,u2,v1,v2,d,n)) continue;
    ++accepted;
    SM C1=outer(u1,v1),C2=outer(u2,v2);
    GI z11=form(C1,C1,d,n),z12=form(C1,C2,d,n),z22=form(C2,C2,d,n);
    if(z11.i || z22.i) { std::cerr<<"diagonal lost reality\n"; return 3; }
    __int128 cross=(__int128)z12.r*z12.r+(__int128)z12.i*z12.i;
    __int128 diag=(__int128)z11.r*z22.r;
    if(z11.r<0 || z22.r<0 || cross>diag) {
      std::cout<<"NEGATIVE COMPLEX SPAN accepted trial "<<accepted<<"\n";
      std::cout<<"R11 "<<z11.r<<" R12 "<<z12.r<<"+"<<z12.i
               <<"i R22 "<<z22.r<<"\n";
      std::cout<<"Witness is C=R22*C1-conj(R12)*C2\n";
      print_sv("u1",u1);print_sv("v1",v1);
      print_sv("u2",u2);print_sv("v2",v2);
      return 0;
    }
    if(z11.r>0 && z22.r>0) {
      long double ratio=((long double)z12.r*z12.r+
                         (long double)z12.i*z12.i)/
                        ((long double)z11.r*z22.r);
      if(ratio>best) {
        best=ratio;best11=z11.r;best12=z12;best22=z22.r;
        bu1=u1;bv1=v1;bu2=u2;bv2=v2;
      }
    }
  }
  std::cout.precision(18);
  std::cout<<"no negative complex span; best ratio "<<best<<"\n";
  std::cout<<"R11 "<<best11<<" R12 "<<best12.r<<"+"<<best12.i
           <<"i R22 "<<best22<<"\n";
  print_sv("u1",bu1);print_sv("v1",bv1);
  print_sv("u2",bu2);print_sv("v2",bv2);
}
