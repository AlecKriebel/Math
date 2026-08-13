#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using Edge=std::pair<int,int>;
// 0=u,1=v,2=a,3=b, 4=root, leaves >=5.
const std::array<Edge,5> CORE={Edge{0,1},Edge{0,2},Edge{2,1},Edge{0,3},Edge{3,1}};

bool dag_reachable(int n,const std::vector<Edge>& arcs,int root=4){
  std::vector<int> indeg(n,0); std::vector<std::vector<int>> ch(n);
  for(auto [x,y]:arcs){++indeg[y];ch[x].push_back(y);} 
  std::queue<int> q; for(int i=0;i<n;++i) if(indeg[i]==0) q.push(i);
  int count=0; auto work=indeg;
  while(!q.empty()){int x=q.front();q.pop();++count;for(int y:ch[x]) if(--work[y]==0)q.push(y);} 
  if(count!=n)return false;
  std::vector<int> seen(n,0);seen[root]=1;q.push(root);int reach=0;
  while(!q.empty()){int x=q.front();q.pop();++reach;for(int y:ch[x])if(!seen[y]){seen[y]=1;q.push(y);}}
  return reach==n;
}

bool tree_child(const std::vector<int>& kind,const std::vector<Edge>& arcs){
  // kind: 0 leaf, 1 root/tree, 2 reticulation.
  std::vector<std::vector<int>> ch(kind.size());
  for(auto [x,y]:arcs)ch[x].push_back(y);
  for(size_t x=0;x<kind.size();++x){
    if(kind[x]==1){bool good=false;for(int y:ch[x])if(kind[y]!=2)good=true;if(!good)return false;}
    if(kind[x]==2){if(ch[x].size()!=1 || kind[ch[x][0]]==2)return false;}
  }
  return true;
}

int failure_kind(const std::vector<int>& kind,const std::vector<Edge>& arcs){
  std::vector<std::vector<int>> ch(kind.size());for(auto [x,y]:arcs)ch[x].push_back(y);
  for(size_t x=0;x<kind.size();++x)if(kind[x]==2 && ch[x].size()==1 && kind[ch[x][0]]==2)return 1;
  for(size_t x=0;x<kind.size();++x)if(kind[x]==1 && !ch[x].empty()){
    bool allR=true;for(int y:ch[x])allR &= kind[y]==2;if(allR)return 2;
  }
  return 0;
}

bool degree_ok(const std::vector<int>& kind,const std::vector<Edge>& arcs){
  std::vector<int> in(kind.size(),0),out(kind.size(),0);for(auto [x,y]:arcs){++out[x];++in[y];}
  for(size_t x=0;x<kind.size();++x){
    if(kind[x]==0 && std::pair<int,int>{in[x],out[x]}!=std::pair<int,int>{1,0})return false;
    if(kind[x]==1){
      if(x==4){if(std::pair<int,int>{in[x],out[x]}!=std::pair<int,int>{0,2})return false;}
      else if(std::pair<int,int>{in[x],out[x]}!=std::pair<int,int>{1,2})return false;
    }
    if(kind[x]==2 && std::pair<int,int>{in[x],out[x]}!=std::pair<int,int>{2,1})return false;
  }
  return true;
}

int main(){
  // Arithmetic core checks.
  assert(CORE.size()-4+1==2); // cyclomatic number of K4 minus one edge.
  std::set<std::set<int>> edgeSet;for(auto [x,y]:CORE)edgeSet.insert({x,y});
  int triangles=0;for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)for(int k=j+1;k<4;++k)
    if(edgeSet.count({i,j})&&edgeSet.count({i,k})&&edgeSet.count({j,k}))++triangles;
  assert(triangles==2);
  int lengthSolutions=0;std::array<int,3> only{};
  for(int a=1;a<=20;++a)for(int b=a;b<=20;++b)for(int c=b;c<=20;++c){
    if((a==1)+(b==1)+(c==1)>1)continue;
    int t=(a+b==3)+(a+c==3)+(b+c==3);
    if(t>=2){++lengthSolutions;only={a,b,c};}
  }
  const std::array<int,3> expectedLengths={1,2,2};
  assert(lengthSolutions==1 && only==expectedLengths);

  int attemptsExternal=0, attemptsInternal=0, validExternal=0, validInternal=0, tc=0;
  int failReticChild=0, failAllRetic=0;
  // Root outside through port a or b. Nodes core 0..3, root4, outgroup5, downstream6.
  for(int entry: {2,3}){
    int exitv= entry==2?3:2;
    for(int r1=0;r1<4;++r1)for(int r2=r1+1;r2<4;++r2){
      for(int mask=0;mask<32;++mask){
        ++attemptsExternal;
        std::vector<Edge> arcs={{4,entry},{4,5},{exitv,6}};
        for(int e=0;e<5;++e){auto [x,y]=CORE[e];if(mask&(1<<e))std::swap(x,y);arcs.push_back({x,y});}
        std::vector<int> kind(7,1);kind[5]=kind[6]=0;kind[r1]=kind[r2]=2;
        if(!degree_ok(kind,arcs)||!dag_reachable(7,arcs))continue;
        ++validExternal;bool ok=tree_child(kind,arcs);tc+=ok;
        if(!ok){int f=failure_kind(kind,arcs);assert(f);if(f==1)++failReticChild;else ++failAllRetic;}
      }
    }
  }
  // Root inside one core edge. Leaves5,6 attach to a,b.
  for(int rootEdge=0;rootEdge<5;++rootEdge){
    for(int r1=0;r1<4;++r1)for(int r2=r1+1;r2<4;++r2){
      for(int mask=0;mask<16;++mask){
        ++attemptsInternal;auto [p,q]=CORE[rootEdge];
        std::vector<Edge> arcs={{4,p},{4,q},{2,5},{3,6}};int bit=0;
        for(int e=0;e<5;++e)if(e!=rootEdge){auto [x,y]=CORE[e];if(mask&(1<<bit))std::swap(x,y);++bit;arcs.push_back({x,y});}
        std::vector<int> kind(7,1);kind[5]=kind[6]=0;kind[r1]=kind[r2]=2;
        if(!degree_ok(kind,arcs)||!dag_reachable(7,arcs))continue;
        ++validInternal;bool ok=tree_child(kind,arcs);tc+=ok;
        if(!ok){int f=failure_kind(kind,arcs);assert(f);if(f==1)++failReticChild;else ++failAllRetic;}
      }
    }
  }
  assert(attemptsExternal==384 && attemptsInternal==480);
  assert(validExternal==4 && validInternal==21);
  assert(tc==0);
  assert(failReticChild==20 && failAllRetic==5);
  std::cout << "path_lengths=1,2,2\n";
  std::cout << "valid_external_rootings=" << validExternal << "\n";
  std::cout << "valid_internal_rootings=" << validInternal << "\n";
  std::cout << "tree_child_rootings=" << tc << "\n";
  std::cout << "INDEPENDENT MULTI-TRIANGLE REVIEW PASSED\n";
}
