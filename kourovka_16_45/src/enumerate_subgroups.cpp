// Exhaustive subgroup enumeration from a multiplication table (identity = 0).
// Every extension <H,g> is considered, with one representative per left coset Hg.
// Completeness: each subgroup is reached by successively adjoining its generators.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct Sub { vector<int> elems, gens; string bits; };
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: enumerate_subgroups table.txt subgroups.json\n";return 1;}
 ifstream in(argv[1]); int n; in>>n;
 if(!in||n<1){cerr<<"invalid table\n";return 1;}
 vector<int> tab(n*n); for(int&x:tab){in>>x;if(!in||x<0||x>=n)return 2;}
 auto key=[&](const vector<int>& e){string s((n+7)/8,0);for(int x:e)s[x/8]|=(1<<(x%8));return s;};
 vector<Sub> subs; subs.push_back({{0},{},key({0})});
 unordered_map<string,int> known;known[subs[0].bits]=0;
 vector<int> seen(n),mark(n);int stamp=0;
 for(size_t hi=0;hi<subs.size();hi++){
   // Copy because vector may reallocate when a new subgroup is appended.
   auto he=subs[hi].elems;auto hg=subs[hi].gens;
   fill(seen.begin(),seen.end(),0);for(int x:he)seen[x]=1;
   for(int g=1;g<n;g++)if(!seen[g]){
     for(int h:he)seen[tab[h*n+g]]=1;
     ++stamp;vector<int> e=he,gens=hg;gens.push_back(g);
     for(int x:e)mark[x]=stamp;
     for(size_t i=0;i<e.size();i++)for(int a:gens){int x=tab[e[i]*n+a];if(mark[x]!=stamp){mark[x]=stamp;e.push_back(x);}}
     sort(e.begin(),e.end());string k=key(e);
     if(known.find(k)==known.end()){known[k]=subs.size();subs.push_back({move(e),move(gens),move(k)});}
   }
 }
 ofstream out(argv[2]);out<<"{\"order\":"<<n<<",\"subgroups\":[\n";
 for(size_t i=0;i<subs.size();i++){
   if(i)out<<",\n";out<<"{\"elements\":[";
   for(size_t j=0;j<subs[i].elems.size();j++){if(j)out<<",";out<<subs[i].elems[j];}
   out<<"],\"generators\":[";
   for(size_t j=0;j<subs[i].gens.size();j++){if(j)out<<",";out<<subs[i].gens[j];}out<<"]}";
 }
 out<<"\n]}\n";cerr<<n<<" elements; "<<subs.size()<<" subgroups\n";
}
