#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>
using u64=std::uint64_t;
static std::vector<unsigned char> readall(const std::string&p){std::ifstream f(p,std::ios::binary);if(!f)throw std::runtime_error("open "+p);return{(std::istreambuf_iterator<char>(f)),{}};}
static long long pc(const std::vector<u64>&x){long long n=0;for(auto z:x)n+=__builtin_popcountll(z);return n;}
int main(int argc,char**argv){
 if(argc!=10){std::cerr<<"usage source target width label out expected_total expected_equal expected_strict summary.json\n";return 2;}
 auto S=readall(argv[1]),T=readall(argv[2]);std::size_t w=std::stoull(argv[3]);std::string label=argv[4],outpath=argv[5],summary=argv[9];long long et=std::stoll(argv[6]),ee=std::stoll(argv[7]),es=std::stoll(argv[8]);
 if(!w||S.size()%w||T.size()%w)throw std::runtime_error("width");std::size_t ns=S.size()/w,nt=T.size()/w,Q=(nt+63)/64;
 std::vector<std::vector<u64>> idx(w*7,std::vector<u64>(Q));std::vector<std::size_t> freq(w*7);
 for(std::size_t j=0;j<nt;++j)for(std::size_t p=0;p<w;++p){unsigned v=T[j*w+p];for(int b=0;b<7;++b)if(v>>b&1){idx[p*7+b][j/64]|=u64(1)<<(j%64);++freq[p*7+b];}}
 std::vector<u64> all(Q,~u64(0)),cand;if(nt%64)all.back()=(u64(1)<<(nt%64))-1;std::ofstream out(outpath);out<<"source_index\ttarget_index\trelation\n";long long total=0,equal=0;
 for(std::size_t i=0;i<ns;++i){const auto*s=&S[i*w];std::vector<std::size_t>req;for(std::size_t p=0;p<w;++p)for(int b=0;b<7;++b)if(s[p]>>b&1)req.push_back(p*7+b);std::sort(req.begin(),req.end(),[&](auto a,auto b){return std::tie(freq[a],a)<std::tie(freq[b],b);});cand=all;for(auto f:req){for(std::size_t q=0;q<Q;++q)cand[q]&=idx[f][q];auto n=pc(cand);if(!n||n<=128)break;}for(std::size_t q=0;q<Q;++q){u64 z=cand[q];while(z){int bit=__builtin_ctzll(z);z&=z-1;std::size_t j=q*64+bit;if(j>=nt)continue;const auto*t=&T[j*w];bool ok=true,eq=true;for(std::size_t p=0;p<w;++p){if(s[p]&static_cast<unsigned char>(~t[p])){ok=false;break;}if(s[p]!=t[p])eq=false;}if(!ok)continue;out<<i<<'\t'<<j<<'\t'<<(eq?"equal":"strict")<<'\n';++total;equal+=eq;}}}
 if(total!=et||equal!=ee||total-equal!=es)throw std::runtime_error("unexpected relation counts");std::ofstream js(summary);js<<"{\n  \"status\": \"EXACTLY COMPUTED FROM REGENERATED SIGNATURES\",\n  \"relation\": \""<<label<<"\",\n  \"source_signatures\": "<<ns<<",\n  \"target_signatures\": "<<nt<<",\n  \"directed_pairs\": "<<total<<",\n  \"equal_pairs\": "<<equal<<",\n  \"strict_pairs\": "<<(total-equal)<<",\n  \"duplicates\": 0\n}\n";std::cout<<"PASS "<<label<<" pairs="<<total<<" equal="<<equal<<" strict="<<(total-equal)<<"\n";
}
