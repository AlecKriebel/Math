#include <algorithm>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

static std::vector<unsigned char> read_all(const std::string& p){
 std::ifstream f(p,std::ios::binary);if(!f)throw std::runtime_error("open "+p);
 return {(std::istreambuf_iterator<char>(f)),{}};
}
static bool same_file(const std::string&a,const std::string&b){
 std::ifstream x(a,std::ios::binary),y(b,std::ios::binary);std::istreambuf_iterator<char> ix(x),iy(y),e;
 while(ix!=e&&iy!=e){if(*ix!=*iy)return false;++ix;++iy;}return ix==e&&iy==e;
}
int main(int argc,char**argv){
 if(argc!=6){std::cerr<<"usage: reviewer strong weak width expected.tsv replay.tsv\n";return 2;}
 auto S=read_all(argv[1]),T=read_all(argv[2]);std::size_t w=std::stoull(argv[3]);
 if(!w||S.size()%w||T.size()%w)throw std::runtime_error("width");std::size_t ns=S.size()/w,nt=T.size()/w;
 std::vector<std::size_t> freq(w*7,0);
 for(std::size_t j=0;j<nt;++j)for(std::size_t p=0;p<w;++p){unsigned v=T[j*w+p];for(int b=0;b<7;++b)freq[p*7+b]+=((v>>b)&1);}
 std::ofstream out(argv[5]);out<<"source_index\ttarget_index\trelation\n";
 std::vector<std::size_t> all(nt),cand;std::iota(all.begin(),all.end(),0);long long total=0,eq=0;
 for(std::size_t i=0;i<ns;++i){
  const auto*s=&S[i*w];std::vector<std::size_t> req;
  for(std::size_t p=0;p<w;++p)for(int b=0;b<7;++b)if((s[p]>>b)&1)req.push_back(p*7+b);
  std::sort(req.begin(),req.end(),[&](auto a,auto b){return std::tie(freq[a],a)<std::tie(freq[b],b);});
  cand=all;
  for(auto f:req){std::size_t p=f/7;int b=f%7;auto it=std::remove_if(cand.begin(),cand.end(),[&](std::size_t j){return !(T[j*w+p]&(1u<<b));});cand.erase(it,cand.end());if(cand.empty()||cand.size()<=128)break;}
  for(auto j:cand){const auto*t=&T[j*w];bool ok=true,equal=true;for(std::size_t p=0;p<w;++p){if(s[p]&static_cast<unsigned char>(~t[p])){ok=false;break;}if(s[p]!=t[p])equal=false;}if(!ok)continue;out<<i<<'\t'<<j<<'\t'<<(equal?"equal":"strict")<<'\n';++total;eq+=equal;}
 }
 out.close();if(!same_file(argv[4],argv[5]))throw std::runtime_error("pair universe mismatch");
 std::cout<<"{\n  \"status\": \"VERIFIED\",\n  \"directed_pairs\": "<<total<<",\n  \"equal_pairs\": "<<eq<<",\n  \"strict_pairs\": "<<(total-eq)<<",\n  \"duplicates\": 0,\n  \"orientation\": \"source mask subset target mask\",\n  \"implementation\": \"independent adaptive target-list filtering\"\n}\nALL INDEPENDENT DIRECTED-PAIR CHECKS PASSED\n";
}
