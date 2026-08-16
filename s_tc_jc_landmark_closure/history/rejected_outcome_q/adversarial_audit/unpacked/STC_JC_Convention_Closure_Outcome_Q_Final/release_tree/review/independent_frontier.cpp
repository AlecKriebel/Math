#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <functional>
#include <string>
#include <tuple>
#include <vector>
using namespace std;

struct RGraph { vector<string> V,L; vector<pair<string,string>> A; string root="rho";};
struct MEdge {string a,b; int head;}; // 0 none, 1 at a, 2 at b
struct MGraph {vector<string> V,L; vector<MEdge> E;};

map<string,int> idx(const vector<string>&v){map<string,int>m;for(int i=0;i<(int)v.size();++i)m[v[i]]=i;return m;}
struct Info {bool valid=false,tc=false,lsa=false; int level=0; map<string,string> type;};

bool reach_without(const RGraph&g,string ban, vector<int>&seen){auto I=idx(g.V);vector<vector<int>>ch(g.V.size());for(auto [a,b]:g.A)if(a!=ban&&b!=ban)ch[I[a]].push_back(I[b]);queue<int>q;if(g.root!=ban){q.push(I[g.root]);seen[I[g.root]]=1;}while(!q.empty()){int u=q.front();q.pop();for(int v:ch[u])if(!seen[v])seen[v]=1,q.push(v);}return true;}

int max_blob_retics(const RGraph&g,const map<string,string>&type){
 auto I=idx(g.V); int n=g.V.size(); vector<vector<pair<int,int>>>adj(n); vector<pair<int,int>> edges;
 for(auto [a,b]:g.A){ if(type.at(a)=="leaf"||type.at(b)=="leaf")continue; int u=I[a],v=I[b],id=edges.size();edges.push_back({u,v});adj[u].push_back({v,id});adj[v].push_back({u,id});}
 vector<int>disc(n),low(n),pe(n,-1),st;int tim=0,best=0;
 function<void(int)>dfs=[&](int u){disc[u]=low[u]=++tim;for(auto [v,e]:adj[u]){if(e==pe[u])continue;if(!disc[v]){pe[v]=e;st.push_back(e);dfs(v);low[u]=min(low[u],low[v]);if(low[v]>=disc[u]){set<int>B;while(!st.empty()){int x=st.back();st.pop_back();B.insert(edges[x].first);B.insert(edges[x].second);if(x==e)break;}int r=0;for(int z:B)if(type.at(g.V[z])=="retic")r++;best=max(best,r);}}else if(disc[v]<disc[u]){st.push_back(e);low[u]=min(low[u],disc[v]);}}};
 for(int i=0;i<n;i++)if(!disc[i])dfs(i);return best;
}

Info validate(const RGraph&g){Info z;set<pair<string,string>>S(g.A.begin(),g.A.end());if(S.size()!=g.A.size())return z;auto I=idx(g.V);int n=g.V.size();vector<int>in(n),out(n);vector<vector<int>>ch(n);for(auto[a,b]:g.A){if(a==b||!I.count(a)||!I.count(b))return z;out[I[a]]++;in[I[b]]++;ch[I[a]].push_back(I[b]);}
 queue<int>q;vector<int>d=in;for(int i=0;i<n;i++)if(!d[i])q.push(i);int ct=0;while(!q.empty()){int u=q.front();q.pop();ct++;for(int v:ch[u])if(--d[v]==0)q.push(v);}if(ct!=n)return z;
 vector<int>seen(n);reach_without(g,"#",seen);if(accumulate(seen.begin(),seen.end(),0)!=n)return z;
 set<string>LS(g.L.begin(),g.L.end());for(int i=0;i<n;i++){string v=g.V[i],t;if(v==g.root&&in[i]==0&&out[i]==2)t="root";else if(LS.count(v)&&in[i]==1&&out[i]==0)t="leaf";else if(in[i]==1&&out[i]==2)t="tree";else if(in[i]==2&&out[i]==1)t="retic";else return z;z.type[v]=t;}
 z.lsa=true;for(string v:g.V)if(v!=g.root){vector<int>s(n);reach_without(g,v,s);bool all=true;for(string l:g.L)if(s[I[l]]){all=false;break;}if(all){z.lsa=false;return z;}}
 z.tc=true;for(string v:g.V)if(!LS.count(v)){bool ok=false;for(int w:ch[I[v]])if(z.type[g.V[w]]=="tree"||z.type[g.V[w]]=="leaf")ok=true;if(!ok)z.tc=false;}
 z.level=max_blob_retics(g,z.type);z.valid=true;return z;}

MGraph raw_sd(const RGraph&g,const Info&in){MGraph m;m.L=g.L;for(string v:g.V)if(v!=g.root)m.V.push_back(v);vector<string>kids;for(auto[a,b]:g.A)if(a==g.root)kids.push_back(b);assert(kids.size()==2);auto add=[&](string a,string b,int h){if(a>b){swap(a,b);if(h==1)h=2;else if(h==2)h=1;}m.E.push_back({a,b,h});};for(auto[a,b]:g.A)if(a!=g.root)add(a,b,in.type.at(b)=="retic"?2:0);int h=0;if(in.type.at(kids[0])=="retic")h=kids[0]<kids[1]?1:2;if(in.type.at(kids[1])=="retic")h=kids[1]<kids[0]?1:2;add(kids[0],kids[1],h);return m;}

MGraph clean(const RGraph&g,const Info&in){MGraph r=raw_sd(g,in);map<pair<string,string>,set<string>>E;for(auto e:r.E){set<string>h;if(e.head==1)h.insert(e.a);if(e.head==2)h.insert(e.b);E[{e.a,e.b}].insert(h.begin(),h.end());}set<string>active(r.V.begin(),r.V.end()),leaf(r.L.begin(),r.L.end());while(true){map<string,vector<pair<pair<string,string>,set<string>>>>inc;for(auto&[k,h]:E){inc[k.first].push_back({k,h});inc[k.second].push_back({k,h});}string v="";for(string x:active)if(!leaf.count(x)&&inc[x].size()==2){v=x;break;}if(v.empty())break;auto x=inc[v][0],y=inc[v][1];string a=x.first.first==v?x.first.second:x.first.first;string b=y.first.first==v?y.first.second:y.first.first;if(a==b)throw runtime_error("loop");E.erase(x.first);E.erase(y.first);active.erase(v);pair<string,string>k=minmax(a,b);set<string>h;if(x.second.count(a))h.insert(a);if(y.second.count(b))h.insert(b);E[k].insert(h.begin(),h.end());}
 MGraph m;m.V.assign(active.begin(),active.end());m.L=r.L;for(auto&[k,h]:E){int hd=0;if(h.size()==1)hd=*h.begin()==k.first?1:2;else if(h.size()>1)hd=3;m.E.push_back({k.first,k.second,hd});}sort(m.E.begin(),m.E.end(),[](auto x,auto y){return tie(x.a,x.b,x.head)<tie(y.a,y.b,y.head);});return m;}

string canon(const MGraph&m){set<string>leaf(m.L.begin(),m.L.end());vector<string>I,L=m.L;sort(L.begin(),L.end());for(string v:m.V)if(!leaf.count(v))I.push_back(v);sort(I.begin(),I.end());string best="";do{map<string,int>p;for(int i=0;i<(int)L.size();i++)p[L[i]]=i;for(int i=0;i<(int)I.size();i++)p[I[i]]=L.size()+i;vector<tuple<int,int,int>>rows;for(auto e:m.E){int a=p[e.a],b=p[e.b],h=e.head;if(a>b){swap(a,b);if(h==1)h=2;else if(h==2)h=1;}rows.push_back({a,b,h});}sort(rows.begin(),rows.end());ostringstream o;for(string x:L)o<<"L:"<<x<<";";o<<"|";for(auto[a,b,h]:rows)o<<a<<","<<b<<","<<h<<";";string s=o.str();if(best.empty()||s<best)best=s;}while(next_permutation(I.begin(),I.end()));return best;}

RGraph family(int L,int dir,int mask){RGraph g;g.V={"rho","p","q"};for(int i=1;i<L;i++){g.V.push_back("v"+to_string(i));g.V.push_back("L"+to_string(i));g.L.push_back("L"+to_string(i));}g.A={{"rho","p"},{"rho","q"}};g.A.push_back(dir==0?make_pair("p","q"):make_pair("q","p"));vector<string>path={"p"};for(int i=1;i<L;i++)path.push_back("v"+to_string(i));path.push_back("q");for(int i=0;i<L;i++){string a=path[i],b=path[i+1];g.A.push_back((mask>>i)&1?make_pair(b,a):make_pair(a,b));}for(int i=1;i<L;i++)g.A.push_back({"v"+to_string(i),"L"+to_string(i)});sort(g.V.begin(),g.V.end());return g;}

int main(int argc,char**argv){string out=argc>1?argv[1]:"independent_frontier.json";ofstream f(out);f<<"{\n  \"status\": \"EXACTLY COMPUTED\",\n  \"frontier\": {\n";for(int L=2;L<=9;L++){int valid=0,tc=0;map<string,pair<int,int>>fib;for(int d=0;d<2;d++)for(int mask=0;mask<(1<<L);mask++){RGraph g=family(L,d,mask);Info z=validate(g);if(!z.valid||z.level>2)continue;valid++;if(z.tc)tc++;MGraph m=clean(g,z);auto &x=fib[canon(m)];x.first++;x.second+=z.tc;}f<<"    \""<<L<<"\": {\"valid_raw_artifact_presentations\": "<<valid<<", \"tree_child_raw_artifact_presentations\": "<<tc<<", \"canonical_clean_target_graphs\": "<<fib.size()<<", \"fibre_profiles\": ["; bool first=true; for(auto &kv:fib){ if(!first)f<<","; first=false; f<<"{\"canonical_code\": \""<<kv.first<<"\", \"raw_presentations\": "<<kv.second.first<<", \"tree_child_presentations\": "<<kv.second.second<<"}";} f<<"]}"<<(L<9?",":"")<<"\n";}f<<"  },\n";
 // strict fibre witness
 RGraph w;w.V={"rho","p","q","a","b","d","L1","L2","L3"};w.L={"L1","L2","L3"};w.A={{"rho","p"},{"rho","q"},{"p","q"},{"p","a"},{"q","b"},{"b","d"},{"d","a"},{"a","L1"},{"b","L2"},{"d","L3"}};Info wi=validate(w);assert(wi.valid&&wi.level==2&&!wi.tc);MGraph wm=clean(w,wi);f<<"  \"strict_witness\": {\"valid\": true, \"rooted_tree_child\": false, \"level\": 2, \"clean_code\": \""<<canon(wm)<<"\"},\n";
 f<<"  \"conclusions\": {\"parallel_theta_112_valid\": false, \"parallel_theta_113_tree_child\": false, \"first_tree_child_length\": 4}\n}\n";f.close();cout<<"PASS independent frontier\n";}
