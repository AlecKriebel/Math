// Independent, deterministic C++17 reconstruction and certificate verifier.
// No NumPy/SymPy arrays or precomputed bracket tables are read.
// Only the pivot plan (a proposed certificate, independently checked) is read.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using i64=std::int64_t; using u64=std::uint64_t;
using i128=__int128_t; using u128=__uint128_t;
constexpr int d=31, p=1009, nr=d*d*(d-1)/2, nc=d*d;
using Vec=std::array<i64,d>;
using Table=std::array<i64,d*d*d>;
static int ix(int i,int j,int k){return (i*d+j)*d+k;}
static void require(bool q,const char* why){if(!q)throw std::runtime_error(why);}
static i64 fall(int n,int k){if(k<0||n<k)return 0;i64 z=1;for(int j=0;j<k;++j)z*=n-j;return z;}
static i64 binom(int n,int k){return fall(n,k)/fall(k,k);}
static i64 trans(int m,int n,int r,int i,int j){
    if(i+j<r||i+j-r>m+n-2*r)return 0;
    i64 z=0;for(int k=0;k<=r;++k)
        z+=(k%2?-1:1)*binom(r,k)*fall(m-i,r-k)*fall(i,k)*fall(n-j,k)*fall(j,r-k);
    return z;
}
static Table build(){
    Table C{};auto put=[&](int i,int j,int k,i64 a){
        require(i!=j||a==0,"nonalternating bracket");
        require(C[ix(i,j,k)]==0||C[ix(i,j,k)]==a,"inconsistent bracket coefficient");
        C[ix(i,j,k)]=a;C[ix(j,i,k)]=-a;
    };
    put(0,1,1,2);put(0,2,2,-2);put(1,2,0,1);
    const int deg[]={6,4,6,2,4,0}, st[]={3,10,15,22,25,30};
    for(int a=0;a<6;++a)for(int i=0;i<=deg[a];++i){
        put(0,st[a]+i,st[a]+i,deg[a]-2*i);
        if(i)put(1,st[a]+i,st[a]+i-1,i);
        if(i<deg[a])put(2,st[a]+i,st[a]+i+1,deg[a]-i);
    }
    const int products[][4]={{0,0,2,3},{0,1,3,4},{0,2,3,5},{0,4,3,4},
                              {1,1,3,3},{1,4,5,4},{4,4,3,3}};
    for(auto &z:products){int a=z[0],b=z[1],c=z[2],r=z[3];
        for(int i=0;i<=deg[a];++i)for(int j=0;j<=deg[b];++j){
            if(a==b&&i>=j)continue;
            i64 q=trans(deg[a],deg[b],r,i,j);
            if(q)put(st[a]+i,st[b]+j,st[c]+i+j-r,q);
        }
    }
    return C;
}
static int jacobi(const Table &C){
    int checks=0;
    for(int i=0;i<d;++i)for(int j=i+1;j<d;++j)for(int k=j+1;k<d;++k){
        for(int b=0;b<d;++b){i128 v=0;
            for(int a=0;a<d;++a)v+=(i128)C[ix(j,k,a)]*C[ix(i,a,b)]
                    +(i128)C[ix(k,i,a)]*C[ix(j,a,b)]+(i128)C[ix(i,j,a)]*C[ix(k,a,b)];
            require(v==0,"integer Jacobi identity failed");
        }++checks;
    }
    for(int i=0;i<d;++i)for(int j=0;j<d;++j)for(int k=0;k<d;++k)
        require(C[ix(i,j,k)]==-C[ix(j,i,k)],"skew symmetry failed");
    return checks;
}
static Table adapted(const Table &C){
    std::array<Vec,d> b{};b[0][0]=1;
    for(int a:{1,2,4,10,27})b[1][a]=1;
    b[2][3]=1;int t=3;
    for(int a=0;a<d;++a)if(a!=0&&a!=1&&a!=3)b[t++][a]=1;
    Table R{};
    for(int i=0;i<d;++i)for(int j=0;j<d;++j){
        Vec z{};
        for(int a=0;a<d;++a)if(b[i][a])for(int c=0;c<d;++c)if(b[j][c])
            for(int k=0;k<d;++k)z[k]+=b[i][a]*b[j][c]*C[ix(a,c,k)];
        R[ix(i,j,0)]=z[0];R[ix(i,j,1)]=z[1];R[ix(i,j,2)]=z[3]; t=3;
        for(int a=0;a<d;++a)if(a!=0&&a!=1&&a!=3){
            bool coupled=a==2||a==4||a==10||a==27;
            R[ix(i,j,t++)]=z[a]-(coupled?z[1]:0);
        }
    }
    return R;
}
static int modp(i64 a){int z=a%p;return z<0?z+p:z;}
static int inversep(int a){int z=1,b=a,e=p-2;while(e){if(e&1)z=z*b%p;b=b*b%p;e>>=1;}return z;}
static int rankp(std::vector<std::vector<int>> a){
    if(a.empty())return 0;
    int n=a.size(),m=a[0].size(),r=0;
    for(int c=0;c<m&&r<n;++c){int s=r;while(s<n&&!a[s][c])++s;if(s==n)continue;
        std::swap(a[s],a[r]);int inv=inversep(a[r][c]);
        for(int j=c;j<m;++j)a[r][j]=a[r][j]*inv%p;
        for(int i=r+1;i<n;++i)if(a[i][c]){int f=a[i][c];
            for(int j=c;j<m;++j)a[i][j]=modp(a[i][j]-f*a[r][j]);
        }
        ++r;
    }return r;
}
static int inner_rank(const Table &C){
    std::vector<std::vector<int>> M(d*d,std::vector<int>(d));
    for(int j=0;j<d;++j)for(int k=0;k<d;++k)for(int a=0;a<d;++a)
        M[j*d+k][a]=modp(C[ix(a,j,k)]);
    return rankp(M);
}
static int perfect_rank(const Table &C){
    std::vector<std::vector<int>> M;
    for(int i=0;i<d;++i)for(int j=i+1;j<d;++j){std::vector<int> z(d);
        for(int k=0;k<d;++k)z[k]=modp(C[ix(i,j,k)]);
        M.push_back(z);
    }
    return rankp(M);
}
static int flag_rank(const Table &C,bool weaker){
    std::vector<std::vector<int>> M;
    for(int j=0;j<2;++j)for(int k=(weaker?3:2);k<d;++k){std::vector<int> z(d);
        for(int a=0;a<d;++a)z[a]=modp(C[ix(a,j,k)]);
        M.push_back(z);
    }
    if(!weaker)for(int k=3;k<d;++k){std::vector<int> z(d);
        for(int a=0;a<d;++a)z[a]=modp(C[ix(a,2,k)]);
        M.push_back(z);
    }
    return rankp(M);
}
static int generated_rank(const Table &C){
    std::vector<std::vector<int>> v;std::vector<int> piv;
    auto insert=[&](std::vector<int> z){
        for(size_t t=0;t<v.size();++t)if(z[piv[t]]){int f=z[piv[t]];
            for(int k=0;k<d;++k)z[k]=modp(z[k]-f*v[t][k]);
        }
        int c=0;while(c<d&&!z[c])++c;if(c==d)return;
        int f=inversep(z[c]);for(int &a:z)a=a*f%p;v.push_back(z);piv.push_back(c);
    };
    std::vector<int> x(d),y(d);x[0]=1;y[1]=1;insert(x);insert(y);
    for(size_t i=0;i<v.size()&&v.size()<d;++i)for(size_t j=0;j<i&&v.size()<d;++j){
        std::vector<int> z(d);
        for(int a=0;a<d;++a)if(v[i][a])for(int b=0;b<d;++b)if(v[j][b])
            for(int k=0;k<d;++k)if(C[ix(a,b,k)])
                z[k]=modp(z[k]+(i64)v[i][a]*v[j][b]%p*modp(C[ix(a,b,k)]));
        insert(z);
    }
    return v.size();
}
static void h1checks(const Table &C){
    for(auto ms:std::vector<std::pair<int,int>>{{0,30},{2,22},{4,10},{6,3}}){
        int m=ms.first,s=ms.second,z=m+1;
        std::vector<std::vector<int>> M(3*z,std::vector<int>(3*z));int pair=0;
        for(int a=0;a<3;++a)for(int b=a+1;b<3;++b){
            for(int k=0;k<z;++k){int row=pair*z+k;
                for(int c=0;c<3;++c)M[row][c*z+k]=modp(M[row][c*z+k]+C[ix(a,b,c)]);
                for(int t=0;t<z;++t){
                    M[row][b*z+t]=modp(M[row][b*z+t]-C[ix(a,s+t,s+k)]);
                    M[row][a*z+t]=modp(M[row][a*z+t]+C[ix(b,s+t,s+k)]);
                }
            }++pair;
        }
        std::vector<std::vector<int>> cob(3*z,std::vector<int>(z));
        for(int a=0;a<3;++a)for(int k=0;k<z;++k)for(int t=0;t<z;++t)
            cob[a*z+k][t]=modp(C[ix(a,s+t,s+k)]);
        int ker=3*z-rankp(M),im=rankp(cob);require(ker==im,"H1 nonzero");
        std::cout<<"H1 highest_weight="<<m<<" cocycle_dimension="<<ker
                 <<" coboundary_dimension="<<im<<" H1_dimension=0\n";
    }
}

static int derivation_rank_mod_p(const Table &C){
    // Independent streamed Gaussian elimination of the entire unscaled matrix.
    std::array<std::vector<std::pair<int,int>>,nc> pivots;
    int rank=0;
    for(int i=0;i<d;++i)for(int j=i+1;j<d;++j)for(int k=0;k<d;++k){
        std::array<int,nc> row{};
        for(int a=0;a<d;++a){
            row[k*d+a]=modp(row[k*d+a]+C[ix(i,j,a)]);
            row[a*d+i]=modp(row[a*d+i]-C[ix(a,j,k)]);
            row[a*d+j]=modp(row[a*d+j]-C[ix(i,a,k)]);
        }
        for(int c=0;c<nc;++c)if(row[c]){
            if(pivots[c].empty()){
                int inv=inversep(row[c]);
                for(int b=c;b<nc;++b)if(row[b])pivots[c].push_back({b,row[b]*inv%p});
                ++rank;break;
            }
            int factor=row[c];
            for(auto z:pivots[c])row[z.first]=modp(row[z.first]-factor*z.second);
        }
    }
    return rank;
}

static u64 modulus;
static u64 norm(i128 a){a%=(i128)modulus;if(a<0)a+=modulus;return (u64)a;}
static u64 mul(u64 a,u64 b){return (u128)a*b%modulus;}
static u64 sub(u64 a,u64 b){return a>=b?a-b:modulus-(b-a);}
static u64 invunit(u64 a){
    i128 t=0,tt=1,r=modulus,rr=a;
    while(rr){i128 q=r/rr, z=t-q*tt;t=tt;tt=z;z=r-q*rr;r=rr;rr=z;}
    require(r==1,"nonunit inversion attempted");return norm(t);
}
static int val(u64 a,int precision){if(!a)return precision;int v=0;while(a%p==0){a/=p;++v;}return v;}
int main(int argc,char**argv){try{
    if(argc!=2)throw std::runtime_error("usage: independent_verify data/smith_pivot_plan.txt");
    auto start=std::chrono::steady_clock::now();
    for(int k=2;k*k<=p;++k)require(p%k!=0,"p is not prime");
    Table C=build();std::cout<<"original_integer_jacobi_checks="<<jacobi(C)<<"\n";
    Table Ca=adapted(C);std::cout<<"adapted_integer_jacobi_checks="<<jacobi(Ca)<<"\n";
    int ir=inner_rank(C),pr=perfect_rank(C),fr=flag_rank(Ca,false),wr=flag_rank(Ca,true),gr=generated_rank(Ca);
    require(ir==30&&pr==31&&fr==30&&wr==30&&gr==31,"small rank certificate failed");
    std::cout<<"inner_rank="<<ir<<" centre_dimension="<<d-ir<<" perfect_rank="<<pr
             <<" infinitesimal_flag_stabilizer_dimension="<<ir-fr
             <<" first_congruence_stabilizer_dimension="<<ir-wr<<" generated_dimension="<<gr<<"\n";
    h1checks(C);
    int dr=derivation_rank_mod_p(C);require(dr==931,"derivation rank modulo p mismatch");
    std::cout<<"unscaled_derivation_rank_mod_p="<<dr<<" derivation_dimension="<<nc-dr<<"\n";
    const int precision=6;modulus=1;for(int k=0;k<precision;++k)modulus*=p;
    std::array<u64,7> powers{};powers[0]=1;for(int k=1;k<=6;++k)powers[k]=powers[k-1]*p;
    int weights[d];for(int k=0;k<d;++k)weights[k]=k<2?0:k==2?1:2;
    std::array<u64,d*d*d> L{};
    for(int i=0;i<d;++i)for(int j=0;j<d;++j)for(int k=0;k<d;++k){
        int e=2+weights[i]+weights[j]-weights[k];require(e>=0&&e<=6,"nonintegral L bracket");
        L[ix(i,j,k)]=norm((i128)Ca[ix(i,j,k)]*powers[e]);
    }
    std::vector<u64> M((size_t)nr*nc,0);
    int row=0;
    for(int i=0;i<d;++i)for(int j=i+1;j<d;++j)for(int k=0;k<d;++k,++row){
        auto add=[&](int col,u64 a){u64 &x=M[(size_t)row*nc+col];x=norm((i128)x+a);};
        for(int a=0;a<d;++a){
            add(k*d+a,L[ix(i,j,a)]);
            add(a*d+i,sub(0,L[ix(a,j,k)]));
            add(a*d+j,sub(0,L[ix(i,a,k)]));
        }
    }
    require(row==nr,"wrong matrix shape");
    std::ifstream plan(argv[1]);require((bool)plan,"cannot open plan");int count;plan>>count;require(count==931,"wrong pivot count");
    std::vector<bool> active_r(nr,true),active_c(nc,true);std::array<int,7> histogram{};
    int previous=-1;
    for(int step=0;step<count;++step){
        int r,c,v;plan>>r>>c>>v;require((bool)plan,"truncated pivot plan");
        require(r>=0&&r<nr&&c>=0&&c<nc&&active_r[r]&&active_c[c],"bad pivot index");
        u64 *pivot=&M[(size_t)r*nc];require(val(pivot[c],precision)==v,"pivot valuation mismatch");
        require(v>=previous&&v<precision,"invalid valuation order");
        if(v!=previous){
            for(int a=0;a<nr;++a){
                if(!active_r[a])continue;
                for(int b=0;b<nc;++b){
                    if(active_c[b])require(M[(size_t)a*nc+b]%powers[v]==0,"pivot not globally minimal");
                }
            }
            previous=v;
        }
        u64 inverse=invunit(pivot[c]/powers[v]);std::vector<int> support;
        for(int b=0;b<nc;++b)if(active_c[b]&&pivot[b]){
            pivot[b]=mul(pivot[b],inverse);require(pivot[b]%powers[v]==0,"pivot row not divisible");support.push_back(b);
        }
        require(pivot[c]==powers[v],"pivot normalization failed");
        for(int a=0;a<nr;++a)if(active_r[a]&&a!=r){u64 *target=&M[(size_t)a*nc];
            if(!target[c])continue;
            require(target[c]%powers[v]==0,"nonexact pivot division");
            u64 factor=target[c]/powers[v];for(int b:support)target[b]=sub(target[b],mul(factor,pivot[b]));
            require(target[c]==0,"pivot column not cleared");
        }
        // Elementary column operations clear the pivot row and leave every
        // other active row unchanged because its pivot-column entry is zero.
        active_r[r]=false;active_c[c]=false;++histogram[v];
        if((step+1)%100==0)std::cout<<"verified_pivots="<<step+1<<" valuation="<<v<<"\n";
    }
    std::string extra;require(!(plan>>extra),"unexpected trailing certificate data");
    for(int a=0;a<nr;++a)if(active_r[a])for(int b=0;b<nc;++b)if(active_c[b])
        require(M[(size_t)a*nc+b]==0,"nonzero residual Smith block");
    // Integer Jacobi plus 30 independent inner derivations gives rank <=931
    // over Q. The 931 nonzero local pivots give the reverse inequality. Hence
    // no unobserved larger-valuation nonzero invariants are possible.
    const std::array<int,7> expected={87,55,758,6,25,0,0};require(histogram==expected,"unexpected Smith multiplicities");
    int sum=0;for(int v=0;v<7;++v){sum+=v*histogram[v];if(histogram[v])
        std::cout<<"smith_valuation="<<v<<" multiplicity="<<histogram[v]<<"\n";}
    require(sum==1689,"wrong Smith sum");
    std::cout<<"prime="<<p<<" precision="<<precision<<" modulus="<<modulus
             <<" derivation_rank=931 nullity=30 sum_smith_valuations="<<sum<<"\n";
    std::cout<<"candidate_quotient_depth="<<sum<<" candidate_group_order_exponent="<<d*sum
             <<" predicted_aut_order_exponent="<<30*sum+sum<<"\n";
    std::cout<<"elapsed_seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()
             <<"\nALL_CHECKS_PASSED\n";
    return 0;
}catch(const std::exception&e){std::cerr<<"VERIFICATION_FAILED: "<<e.what()<<"\n";return 1;}}
