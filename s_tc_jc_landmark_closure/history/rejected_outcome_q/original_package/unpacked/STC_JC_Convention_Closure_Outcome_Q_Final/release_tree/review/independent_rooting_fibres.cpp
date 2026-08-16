#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <vector>
using namespace std;

struct MEdge { string a,b; int head; }; // 0 U, 1 head=a, 2 head=b
struct MGraph { vector<string> V,L; vector<MEdge> E; };
struct RInfo { bool valid=false, tree_child=false, lsa=false; };

static map<string,int> index_of(const vector<string>& V){ map<string,int> I; for(int i=0;i<(int)V.size();++i) I[V[i]]=i; return I; }

static RInfo validate_rooted(const vector<string>& V,const vector<string>& L,const vector<pair<string,string>>& A,const string& root){
 RInfo z; auto I=index_of(V); int n=V.size(); set<pair<string,string>> uniq(A.begin(),A.end()); if(uniq.size()!=A.size()) return z;
 vector<int> in(n),out(n),d(n); vector<vector<int>> ch(n);
 for(auto [a,b]:A){ if(!I.count(a)||!I.count(b)||a==b) return z; out[I[a]]++; in[I[b]]++; ch[I[a]].push_back(I[b]); }
 queue<int> q; d=in; for(int i=0;i<n;i++) if(!d[i]) q.push(i); int seen=0; while(!q.empty()){int u=q.front();q.pop();seen++;for(int v:ch[u])if(--d[v]==0)q.push(v);} if(seen!=n)return z;
 set<string> leaf(L.begin(),L.end()); map<string,string> type;
 for(string v:V){int i=I[v]; if(v==root){if(in[i]!=0||out[i]!=2)return z;type[v]="root";} else if(leaf.count(v)){if(in[i]!=1||out[i]!=0)return z;type[v]="leaf";} else if(in[i]==1&&out[i]==2)type[v]="tree"; else if(in[i]==2&&out[i]==1)type[v]="retic"; else return z;}
 // Reachability.
 vector<int> reach(n); queue<int> r; reach[I[root]]=1;r.push(I[root]);while(!r.empty()){int u=r.front();r.pop();for(int v:ch[u])if(!reach[v]){reach[v]=1;r.push(v);}} if(accumulate(reach.begin(),reach.end(),0)!=n)return z;
 // Root is LSA: no proper vertex separates root from all labelled leaves.
 for(string ban:V) if(ban!=root){vector<int> vis(n);queue<int> qq;vis[I[root]]=1;qq.push(I[root]);while(!qq.empty()){int u=qq.front();qq.pop();for(int v:ch[u])if(V[v]!=ban&&!vis[v]){vis[v]=1;qq.push(v);}} bool all_lost=true;for(string l:L)if(vis[I[l]]){all_lost=false;break;}if(all_lost)return z;}
 bool tc=true; for(string v:V) if(!leaf.count(v)){bool ok=false;for(int w:ch[I[v]])if(type[V[w]]=="tree"||type[V[w]]=="leaf")ok=true;if(!ok)tc=false;}
 z.valid=true;z.tree_child=tc;z.lsa=true;return z;
}

static vector<pair<vector<pair<string,string>>,RInfo>> rootings(const MGraph& G){
 vector<pair<vector<pair<string,string>>,RInfo>> result; auto I=index_of(G.V); set<string> leaf(G.L.begin(),G.L.end());
 map<string,int> incoming; for(auto e:G.E){if(e.head==1)incoming[e.a]++;if(e.head==2)incoming[e.b]++;}
 for(int re=0;re<(int)G.E.size();++re){
  auto root_edge=G.E[re]; if(root_edge.head==3)continue;
  vector<pair<string,string>> fixed={{"ROOT",root_edge.a},{"ROOT",root_edge.b}}; vector<pair<string,string>> free_edges;
  for(int i=0;i<(int)G.E.size();++i) if(i!=re){auto e=G.E[i];if(e.head==0)free_edges.push_back({e.a,e.b}); else if(e.head==1)fixed.push_back({e.b,e.a}); else if(e.head==2)fixed.push_back({e.a,e.b}); else goto next_root_edge;}
  {
   int m=free_edges.size();
   for(int mask=0;mask<(1<<m);++mask){vector<pair<string,string>> A=fixed;for(int j=0;j<m;++j){auto [a,b]=free_edges[j];A.push_back((mask>>j)&1?make_pair(b,a):make_pair(a,b));}
    vector<string> V=G.V;V.push_back("ROOT");auto z=validate_rooted(V,G.L,A,"ROOT");if(z.valid)result.push_back({A,z});}
  }
  next_root_edge: ;
 }
 // exact arc-set deduplication
 map<vector<pair<string,string>>,RInfo> uniq;for(auto rec:result){auto A=rec.first;sort(A.begin(),A.end());uniq[A]=rec.second;}result.clear();for(auto &kv:uniq)result.push_back(kv);return result;
}

static MGraph strict_target(){
 // Cleaned three-sunlet from the non-tree-child root zipper witness.
 MGraph g;g.V={"a","b","d","L1","L2","L3"};g.L={"L1","L2","L3"};
 g.E={{"a","b",1},{"a","d",1},{"b","d",0},{"L1","a",0},{"L2","b",0},{"L3","d",0}};
 return g;
}

static MGraph theta_source(bool target){
 // Directly encode the two standard reductions; source has L1 at B, target at E.
 MGraph g;g.V={"A","B","C","D","E","F","L1","L2","L3","L4"};g.L={"L1","L2","L3","L4"};
 g.E={{"A","B",0},{"A","C",2},{"B","C",2},{"C","D",0},{"D","E",0},{"A","F",2},{"E","F",2}};
 if(!target){g.E.push_back({"B","L1",0});g.E.push_back({"D","L2",0});g.E.push_back({"F","L3",0});g.E.push_back({"E","L4",0});}
 else {g.E.push_back({"E","L1",0});g.E.push_back({"D","L2",0});g.E.push_back({"F","L3",0});g.E.push_back({"B","L4",0});}
 return g;
}

static string json_bool(bool x){return x?"true":"false";}
int main(int argc,char**argv){string out=argc>1?argv[1]:"independent_rooting_fibres.json";
 auto s=rootings(strict_target()); auto a=rootings(theta_source(false)); auto b=rootings(theta_source(true));
 assert(s.size()==5 && all_of(s.begin(),s.end(),[](auto&r){return r.second.tree_child;}));
 assert(a.size()==5 && count_if(a.begin(),a.end(),[](auto&r){return r.second.tree_child;})==2);
 assert(b.size()==5 && count_if(b.begin(),b.end(),[](auto&r){return r.second.tree_child;})==2);
 ofstream f(out);f<<"{\n  \"status\": \"EXACTLY COMPUTED\",\n";
 f<<"  \"strict_target_sd0_rootings\": {\"valid\": 5, \"tree_child\": 5, \"strong\": true},\n";
 f<<"  \"theta_source\": {\"valid\": 5, \"tree_child\": 2, \"strong\": false},\n";
 f<<"  \"theta_target\": {\"valid\": 5, \"tree_child\": 2, \"strong\": false},\n";
 f<<"  \"independence_note\": \"Brute-force all orientations after each possible root-edge insertion; no Python canonicalizer or rooting routine is imported.\"\n}\n";
 cout<<"PASS independent rooting fibres: strict 5/5; theta 5/2 and 5/2\n";
}
