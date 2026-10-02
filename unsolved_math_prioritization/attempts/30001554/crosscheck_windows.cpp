// C++17, independent literal-border recursion. stdout is the complete canonical
// terminal stream; stderr is a JSON summary. No cap or random search.
#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
using namespace std;
int t,n;vector<int>w,th;vector<bool>paired;vector<unsigned long long>nodes,nonperiodic;unsigned long long leaves=0;
bool has_small_period(){
 for(int p=1;p<=t;p++){
  bool ok=true;for(int j=p;j<(int)w.size();j++)if(w[j]!=th[w[j-p]]){ok=false;break;}
  if(ok)return true;
 }return false;
}
bool valid_suffixes(){
 int m=w.size();for(int length=t+1;length<=m;length++){
  int start=m-length;bool bordered=false;
  for(int k=1;k<length&&!bordered;k++){
   bool equal=true;for(int j=0;j<k;j++)if(w[m-k+j]!=th[w[start+j]]){equal=false;break;}
   bordered=equal;
  }
  if(!bordered)return false;
 }return true;
}
void visit();
void extend(int a){w.push_back(a);if(valid_suffixes())visit();w.pop_back();}
void visit(){
 int m=w.size();nodes[m]++;
 if(m>=t&&!has_small_period())nonperiodic[m]++;
 if(m==n){
  if(!has_small_period())throw runtime_error("threshold counterexample");
  leaves++;cout<<"[[";for(size_t i=0;i<paired.size();i++){if(i)cout<<',';cout<<(paired[i]?"true":"false");}cout<<"],[";
  for(size_t i=0;i<w.size();i++){if(i)cout<<',';cout<<w[i];}cout<<"]]\n";return;
 }
 size_t old=paired.size();for(size_t j=0;j<old;j++){extend(2*j);if(paired[j])extend(2*j+1);}
 if(m<t){
  int a=2*old;paired.push_back(false);th.push_back(a);th.push_back(a+1);extend(a);
  paired.back()=true;th[a]=a+1;th[a+1]=a;extend(a);th.pop_back();th.pop_back();paired.pop_back();
 }
}
void array_json(const vector<unsigned long long>&v){cerr<<'[';for(size_t i=0;i<v.size();i++){if(i)cerr<<',';cerr<<v[i];}cerr<<']';}
int main(int argc,char**argv){
 ios::sync_with_stdio(false);if(argc!=2)return 2;t=stoi(argv[1]);if(t<1||t>20)return 2;n=3*t;nodes.assign(n+1,0);nonperiodic.assign(n+1,0);visit();
 cerr<<"{\"t\":"<<t<<",\"length\":"<<n<<",\"leaves\":"<<leaves<<",\"nodes\":";array_json(nodes);cerr<<",\"nonperiodic_by_length\":";array_json(nonperiodic);cerr<<"}\n";
}
