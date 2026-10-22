#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
struct G {int n; vector<pair<int,int>> edges; uint32_t mask;};
bool colorable(int n, const vector<pair<int,int>>& es, uint32_t mask, int deleted=-1) {
 vector<int> col(n,-1); vector<vector<int>> a(n); for(int e=0;e<(int)es.size();e++)if(mask>>e&1){auto [x,y]=es[e];a[x].push_back(y);a[y].push_back(x);}
 vector<int> order;for(int v=0;v<n;v++)if(v!=deleted)order.push_back(v);sort(order.begin(),order.end(),[&](int x,int y){return a[x].size()>a[y].size();});
 auto dfs=[&](auto&& self,int k)->bool{if(k==(int)order.size())return true; int v=order[k];for(int c=0;c<3;c++){bool ok=true;for(int u:a[v])if(col[u]==c)ok=false;if(ok){col[v]=c;if(self(self,k+1))return true;col[v]=-1;}}return false;};return dfs(dfs,0);
}
bool property(int n,const vector<pair<int,int>>& es,uint32_t mask) {
 vector<vector<bool>> a(n,vector<bool>(n));for(int e=0;e<(int)es.size();e++)if(mask>>e&1){auto [x,y]=es[e];a[x][y]=a[y][x]=1;}
 for(int a0=0;a0<n;a0++)for(int b=a0+1;b<n;b++)for(int c=b+1;c<n;c++)for(int d=c+1;d<n;d++)if(a[a0][b]&&a[a0][c]&&a[a0][d]&&a[b][c]&&a[b][d]&&a[c][d])return false;
 if(colorable(n,es,mask))return true;for(int v=0;v<n;v++)if(colorable(n,es,mask,v))return true;return false;
}
vector<int> hamming_distance(vector<int> v,int m) {for(int bit=0;bit<m;bit++)for(int s=0;s<(int)v.size();s++)v[s]=min(v[s],1+v[s^(1<<bit)]);return v;}
int main(){uint64_t graphs=0,states=0,steps=0,hered=0,monotone=0;int positive=0;vector<int> graph_counts;
 for(int n=1;n<=6;n++) {vector<pair<int,int>> es;for(int x=0;x<n;x++)for(int y=x+1;y<n;y++)es.push_back({x,y});int m=es.size(),lim=1<<m;vector<int>d3(lim,1000),dp(lim,1000);vector<bool>p(lim),c3(lim);
  for(int s=0;s<lim;s++){c3[s]=colorable(n,es,s);p[s]=property(n,es,s);assert(!c3[s]||p[s]);if(c3[s])d3[s]=0;if(p[s])dp[s]=0;}
  d3=hamming_distance(d3,m);dp=hamming_distance(dp,m);for(int s=0;s<lim;s++){graphs++;assert(d3[s]>=dp[s]);if(d3[s])positive++;for(int e=0;e<m;e++)if(s>>e&1){assert(!p[s]||p[s^(1<<e)]);monotone++;}
   if(p[s])for(int v=0;v<n;v++){vector<pair<int,int>> sub;uint32_t sm=0;for(int e=0;e<m;e++){auto[x,y]=es[e];if(x==v||y==v)continue;if(s>>e&1)sm|=1u<<sub.size();sub.push_back({x-(x>v),y-(y>v)});}assert(property(n-1,sub,sm));hered++;}
   // Independent exact 3-color edit optimum: every assignment's monochromatic edges.
   if(n<=5){int count=1;for(int i=0;i<n;i++)count*=3;int exact=m;for(int z=0;z<count;z++){int q=z;vector<int>cs(n);for(int i=0;i<n;i++){cs[i]=q%3;q/=3;}int bad=0;for(int e=0;e<m;e++)if((s>>e&1)&&cs[es[e].first]==cs[es[e].second])bad++;exact=min(exact,bad);}assert(exact==d3[s]);}
   if(n>5||!d3[s])continue;vector<vector<bool>>a(n,vector<bool>(n));for(int e=0;e<m;e++)if(s>>e&1){auto[x,y]=es[e];a[x][y]=a[y][x]=1;}
   int cnt=1;for(int i=0;i<n;i++)cnt*=4;for(int z=0;z<cnt;z++){int q=z;vector<int>cs(n);for(int i=0;i<n;i++){cs[i]=q%4;q/=4;}bool proper=true;for(int e=0;e<m;e++)if((s>>e&1)&&cs[es[e].first]&&cs[es[e].first]==cs[es[e].second])proper=false;if(!proper)continue;
    states++;vector<int>ls(n),delta(n);int u=0,phi=0;for(int v=0;v<n;v++)if(!cs[v]){ls[v]=7;for(int w=0;w<n;w++)if(a[v][w]&&cs[w])ls[v]&=~(1<<(cs[w]-1));phi+=__builtin_popcount((unsigned)ls[v]);if(!ls[v])u++;}
    int sum=0,wcnt=0;for(int v=0;v<n;v++)if(!cs[v]&&ls[v]){delta[v]=n;for(int col=0;col<3;col++)if(ls[v]>>col&1){int d=0;for(int w=0;w<n;w++)if(!cs[w]&&ls[w]&&a[v][w]&&(ls[w]>>col&1))d++;delta[v]=min(delta[v],d);}sum+=delta[v];if(2*n*delta[v]>=d3[s])wcnt++;}
    assert(d3[s]<=n*u+sum);assert(2*n*(u+wcnt)>=d3[s]);
    for(int v=0;v<n;v++)if(!cs[v]&&ls[v]&&2*n*delta[v]>=d3[s])for(int col=0;col<3;col++)if(ls[v]>>col&1){int after=0;for(int w=0;w<n;w++)if(w!=v&&!cs[w]){int l=ls[w];if(a[v][w])l&=~(1<<col);after+=__builtin_popcount((unsigned)l);}assert(phi-after>=delta[v]);assert(2*n*(phi-after)>=d3[s]);steps++;}
   }
  }graph_counts.push_back(lim);
 }
 cout<<"all simple labelled graphs n=1..6: "<<graphs<<"\npositive C3 edit distance graphs: "<<positive<<"\nproper partial colorings checked on positive-distance n<=5: "<<states<<"\nall feasible W color steps checked: "<<steps<<"\nP inherited induced vertex deletions checked: "<<hered<<"\nedge deletion implications checked: "<<monotone<<"\n";
 // Mutations are independently checked with full adjacency and exact 3-colorability.
 auto evaluate=[&](int n,vector<pair<int,int>>es){uint32_t mask=(1u<<es.size())-1;return pair<bool,bool>{colorable(n,es,mask),property(n,es,mask)};};
 vector<pair<int,int>>wheel;for(int i=1;i<=5;i++){wheel.push_back({0,i});wheel.push_back({i,1+i%5});}
 auto w=evaluate(6,wheel);assert(!w.first&&w.second);vector<pair<int,int>> overlap=wheel;for(auto[x,y]:wheel)overlap.push_back({x?x+5:0,y?y+5:0});auto o=evaluate(11,overlap);assert(!o.first&&o.second);
 vector<pair<int,int>>twice=wheel;for(auto[x,y]:wheel)twice.push_back({x+6,y+6});auto t=evaluate(12,twice);assert(!t.first&&!t.second);
 vector<int>labels={0,0,1,2,3,4,5};vector<pair<int,int>>expanded;for(int i=0;i<7;i++)for(int j=i+1;j<7;j++)for(auto[x,y]:wheel)if((labels[i]==x&&labels[j]==y)||(labels[i]==y&&labels[j]==x))expanded.push_back({i,j});auto e=evaluate(7,expanded);assert(!e.first&&!e.second);
 cout<<"wheel: C3=false P=true\nshared-center two-wheel witnesses: C3=false P=true\ndisjoint two-wheel witnesses: C3=false P=false\nduplicate-center expanded occurrence graph: C3=false P=false (correct distinct-label graph P=true)\nPASS\n";
}
