#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>

// Exact finite incidence-pattern search for a rank-three (6,4) counterexample.
// No external solver or floating-point arithmetic. See TURN5.md. Aborted outputs are not impossibility certificates.
using Bits = std::array<uint64_t,194>;
struct Candidate { unsigned support; Bits covers{}; };
struct ProofNode { unsigned target=0; std::vector<unsigned> supports; std::vector<int> children; };
struct Search {
  int m, d;
  bool aborted=false;
  uint64_t node_limit=25000;
  unsigned full;
  std::vector<unsigned> targets;
  std::vector<Candidate> candidates;
  std::vector<int> chosen;
  std::array<int,17> degree{};
  std::array<unsigned,17> row_signature{};
  uint64_t nodes=0, dead_targets=0, capacity_prunes=0, pair_prunes=0, duplicate_prunes=0;
  std::vector<ProofNode> proof;

  Search(int edge_count,int maximum_degree):m(edge_count),d(maximum_degree),full((1u<<m)-1){
    for(unsigned x=1;x<=full;++x)if(__builtin_popcount(x)==6)targets.push_back(x);
    for(unsigned x=1;x<=full;++x){
      int size=__builtin_popcount(x);
      if(size<4 || size>d)continue;
      Candidate c;c.support=x;
      for(size_t j=0;j<targets.size();++j)
        if(__builtin_popcount(x&targets[j])>=4)c.covers[j/64]|=uint64_t(1)<<(j%64);
      candidates.push_back(c);
    }
  }

  bool feasible(int index){
    unsigned support=candidates[index].support;
    for(int v=0;v<m;++v)if((support>>v&1u)&&degree[v]>=3){++capacity_prunes;return false;}
    for(int selected:chosen)if(__builtin_popcount(support|candidates[selected].support)>m-2){++pair_prunes;return false;}
    for(size_t a=0;a<chosen.size();++a)
      for(size_t b=0;b<a;++b)
        if((support|candidates[chosen[a]].support|candidates[chosen[b]].support)==full){++pair_prunes;return false;}
    unsigned tag=1u<<chosen.size();
    for(int i=0;i<m;++i){
      int di=degree[i]+int(support>>i&1u);
      if(di!=3)continue;
      unsigned si=row_signature[i]|((support>>i&1u)?tag:0);
      for(int j=0;j<i;++j){
        int dj=degree[j]+int(support>>j&1u);
        unsigned sj=row_signature[j]|((support>>j&1u)?tag:0);
        if(dj==3 && si==sj){++duplicate_prunes;return false;}
      }
    }
    return true;
  }

  void add(int index){
    unsigned support=candidates[index].support, tag=1u<<chosen.size();
    for(int v=0;v<m;++v)if(support>>v&1u){++degree[v];row_signature[v]|=tag;}
    chosen.push_back(index);
  }
  void remove(){
    int index=chosen.back();chosen.pop_back();
    unsigned support=candidates[index].support, tag=1u<<chosen.size();
    for(int v=0;v<m;++v)if(support>>v&1u){--degree[v];row_signature[v]&=~tag;}
  }

  bool dfs(std::vector<int> allowed,Bits covered){
    if(++nodes>node_limit){aborted=true;return false;}
    int node_id=proof.size();proof.emplace_back();
    std::vector<int> valid;
    for(int index:allowed)if(feasible(index))valid.push_back(index);
    int best=-1;
    std::vector<int> branches;
    for(size_t j=0;j<targets.size();++j){
      if(covered[j/64]>>(j%64)&1u)continue;
      std::vector<int> options;
      for(int index:valid)if(candidates[index].covers[j/64]>>(j%64)&1u)options.push_back(index);
      if(options.empty()){++dead_targets;proof[node_id].target=targets[j];return false;}
      if(best<0 || options.size()<branches.size()){best=j;branches=std::move(options);}
    }
    if(best<0)return true;
    proof[node_id].target=targets[best];
    for(int index:branches){
      valid.erase(std::remove(valid.begin(),valid.end(),index),valid.end());
      Bits next=covered;
      for(int k=0;k<194;++k)next[k]|=candidates[index].covers[k];
      add(index);
      proof[node_id].supports.push_back(candidates[index].support);
      proof[node_id].children.push_back(proof.size());
      if(dfs(valid,next))return true;
      if(aborted)return false;
      remove();
      // Subsequent branches exclude this candidate: they exhaust solutions
      // according to the first chosen cover of the selected uncovered target.
    }
    return false;
  }

  bool run(){
    // Relabel a maximum-degree vertex's support to {0,...,d-1}.
    unsigned first=(1u<<d)-1;
    int fixed=-1;std::vector<int> allowed;
    for(int i=0;i<int(candidates.size());++i)
      if(candidates[i].support==first)fixed=i;else allowed.push_back(i);
    if(fixed<0)std::abort();
    add(fixed);
    return dfs(allowed,candidates[fixed].covers);
  }

  void write_proof(const char* path){
    std::ofstream out(path);
    if(!out)std::abort();
    out<<"{\"edges\":"<<m<<",\"maximum_degree\":"<<d<<",\"root\":0,\"nodes\":[";
    for(size_t i=0;i<proof.size();++i){
      if(i)out<<',';
      out<<"["<<proof[i].target<<",[";
      for(size_t j=0;j<proof[i].supports.size();++j){
        if(j)out<<',';
        out<<'['<<proof[i].supports[j]<<','<<proof[i].children[j]<<']';
      }
      out<<"]]";
    }
    out<<"]}\n";
    if(!out)std::abort();
  }
};

int main(int argc,char**argv){
  if(argc<3 || argc>5)return 2;
  int m=std::atoi(argv[1]),d=std::atoi(argv[2]);
  if(m<7 || m>17 || d<4 || d>7 || d>m-3)return 2;
  Search search(m,d);
  if(argc==5)search.node_limit=std::strtoull(argv[4],nullptr,10);
  bool sat=search.run();
  if(!sat && !search.aborted && argc>=4)search.write_proof(argv[3]);
  std::cout<<"{\"edges\":"<<m<<",\"maximum_degree\":"<<d
           <<",\"aborted\":"<<(search.aborted?"true":"false")<<",\"satisfiable\":"<<(sat?"true":"false")<<",\"nodes\":"<<search.nodes
           <<",\"dead_targets\":"<<search.dead_targets
           <<",\"capacity_prunes\":"<<search.capacity_prunes
           <<",\"pair_prunes\":"<<search.pair_prunes
           <<",\"duplicate_prunes\":"<<search.duplicate_prunes;
  if(sat){
    std::cout<<",\"supports\":[";
    for(size_t i=0;i<search.chosen.size();++i){
      if(i)std::cout<<',';
      std::cout<<search.candidates[search.chosen[i]].support;
    }
    std::cout<<']';
  }
  std::cout<<"}\n";
  return search.aborted?3:(sat?1:0);
}
