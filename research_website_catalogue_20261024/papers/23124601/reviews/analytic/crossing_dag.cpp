// Independently reconstructed finite6-strand certificate. No shipped code/records read.
#include <array>
#include <vector>
#include <unordered_map>
#include <queue>
#include <iostream>
#include <stdexcept>
#include <string>
#include <algorithm>
#include <cstdint>
using Word=std::vector<int8_t>;
using Images=std::array<Word,6>;
struct Node {uint32_t q,perm,parent; uint8_t letter,depth; std::array<int32_t,5> next;};
void need(bool x,const std::string&s){if(!x)throw std::runtime_error(s);}
void append(Word&w,int x){if(!w.empty()&&w.back()==-x)w.pop_back();else w.push_back(static_cast<int8_t>(x));}
Word stepword(const Word&w,int generator){
 int i=std::abs(generator); Word out;out.reserve(w.size()*2+4);
 for(int x:w){int a=std::abs(x);int b[3];int n=1;
  if(generator>0){if(a==i){b[0]=i;b[1]=i+1;b[2]=-i;n=3;}else if(a==i+1)b[0]=i;else b[0]=a;}
  else{if(a==i)b[0]=i+1;else if(a==i+1){b[0]=-(i+1);b[1]=i;b[2]=i+1;n=3;}else b[0]=a;}
  if(x>0){for(int k=0;k<n;k++)append(out,b[k]);}
  else{for(int k=n-1;k>=0;k--)append(out,-b[k]);}
 }
 return out;
}
Images step(const Images&a,int gen){Images b;for(int j=0;j<6;j++)b[j]=stepword(a[j],gen);return b;}
Images identity(){Images a;for(int j=0;j<6;j++)a[j].push_back(j+1);return a;}
Images action(const std::vector<int>&w){Images a=identity();for(int g:w)a=step(a,g);return a;}
std::vector<int> repeated(std::vector<int>w,int n){std::vector<int> v;for(int i=0;i<n;i++)v.insert(v.end(),w.begin(),w.end());return v;}
uint32_t swapped(uint32_t p,int i){uint32_t a=(p>>(3*i))&7,b=(p>>(3*(i+1)))&7;return p^((a^b)<<(3*i))^((a^b)<<(3*(i+1)));}
int main(int argc,char**argv){try{
 std::string fault=argc>1?argv[1]:"";std::array<uint32_t,16> pow3;pow3[0]=1;for(int i=1;i<16;i++)pow3[i]=3*pow3[i-1];
 int index[6][6];int k=0;for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)index[i][j]=index[j][i]=k++;
 uint32_t initialperm=0;for(int i=0;i<6;i++)initialperm|=i<<(3*i);
 std::vector<Node> nodes;nodes.reserve(250000);std::unordered_map<uint32_t,uint32_t> ids;ids.reserve(300000);
 Node zero{0,initialperm,0,0,0,{-1,-1,-1,-1,-1}};nodes.push_back(zero);ids[0]=0;uint64_t redges=0;
 for(uint32_t u=0;u<nodes.size();u++){
  Node current=nodes[u];
  for(int i=0;i<5;i++){
   int a=(current.perm>>(3*i))&7,b=(current.perm>>(3*(i+1)))&7;uint32_t power=pow3[index[a][b]];
   if((current.q/power)%3==2)continue;
   uint32_t q=current.q+power,p=swapped(current.perm,i),v;auto it=ids.find(q);
   if(it==ids.end()){v=nodes.size();Node child{q,p,u,static_cast<uint8_t>(i+1),static_cast<uint8_t>(current.depth+1),{-1,-1,-1,-1,-1}};nodes.push_back(child);ids[q]=v;}
   else{v=it->second;need(nodes[v].perm==p,"count_parity_permutation_merge");need(nodes[v].depth==current.depth+1,"DAG_depth");}
   nodes[u].next[i]=v;redges++;
  }
 }
 uint32_t full=pow3[15]-1;need(ids.count(full),"full_count_vector_reachable");uint32_t fid=ids.at(full);need(nodes[fid].perm==initialperm&&nodes[fid].depth==30,"terminal_purity_and_depth");
 std::vector<std::vector<uint32_t>> incoming(nodes.size());for(uint32_t u=0;u<nodes.size();u++)for(int32_t v:nodes[u].next)if(v>=0)incoming[v].push_back(u);
 std::vector<uint8_t> good(nodes.size(),0);std::queue<uint32_t> back;good[fid]=1;back.push(fid);while(!back.empty()){uint32_t v=back.front();back.pop();for(uint32_t u:incoming[v])if(!good[u]){good[u]=1;back.push(u);}}
 uint64_t snodes=0,sedges=0;for(uint32_t u=0;u<nodes.size();u++){bool complement=ids.count(full-nodes[u].q);need(bool(good[u])==complement,"independent_backward_vs_complement_coaccessibility");if(good[u]){snodes++;for(int32_t v:nodes[u].next)if(v>=0&&good[v])sedges++;}}
 need(good[0],"initial_coaccessible");
 std::vector<Images> U(nodes.size());U[0]=identity();for(uint32_t u=1;u<nodes.size();u++)if(good[u]){need(good[nodes[u].parent],"parent_closed_coaccessibility");U[u]=step(U[nodes[u].parent],nodes[u].letter);}
 if(fault=="potential")for(uint32_t u=1;u<nodes.size();u++)if(good[u]&&nodes[u].depth==6){append(U[u][0],U[u][0].empty()||U[u][0].back()!=-1?1:2);break;}
 uint64_t comparisons=0;bool skipped=false;for(uint32_t u=0;u<nodes.size();u++)if(good[u])for(int i=0;i<5;i++){int32_t v=nodes[u].next[i];if(v<0||!good[v])continue;if(fault=="skip-edge"&&!skipped){skipped=true;continue;}need(step(U[u],i+1)==U[v],"literal_edge_action_mismatch_q="+std::to_string(nodes[u].q)+"_generator="+std::to_string(i+1));comparisons++;}
 need(comparisons==sedges,"every_coaccessible_edge_compared");
 std::vector<int> d={1,2,3,4,5},c=repeated({1,2,3,4},5),h={5,4,3,2,1,1,2,3,4,5},z=repeated(d,6),ch=c,hc=h;ch.insert(ch.end(),h.begin(),h.end());hc.insert(hc.end(),c.begin(),c.end());
 Images az=action(z);need(U[fid]==az,"final_action_is_displayed_full_twist");need(action(ch)==az&&action(hc)==az,"B6_full_twist_decomposition_both_orders");
 for(int g=1;g<=5;g++){auto zg=z;zg.push_back(g);std::vector<int> gz={g};gz.insert(gz.end(),z.begin(),z.end());need(action(zg)==action(gz),"full_twist_central_action");}
 auto state=[&](std::vector<int>w){uint32_t u=0;for(int g:w){int32_t v=nodes[u].next[g-1];need(v>=0,"negative_control_path_reachable");u=v;}return u;};
 uint32_t left=state({1,1,2,2}),right=state({2,2,1,1});need(left==right&&!good[left]&&action({1,1,2,2})!=action({2,2,1,1}),"equal_counts_do_not_determine_arbitrary_prefix_action");
 std::vector<int> ddinv;for(auto it=d.rbegin();it!=d.rend();++it)ddinv.push_back(-*it);for(int g=1;g<=4;g++){auto w=d;w.push_back(g);w.insert(w.end(),ddinv.begin(),ddinv.end());need(action(w)==action({g+1}),"explicit_shift_conjugation");}
 uint64_t letters=0,maxword=0;for(uint32_t u=0;u<nodes.size();u++)if(good[u])for(auto&w:U[u]){letters+=w.size();maxword=std::max(maxword,uint64_t(w.size()));}
 need(nodes.size()==234368&&redges==711342&&snodes==90921&&sedges==261810,"independently_reconstructed_exact_state_edge_counts");
 std::cout<<"{\"status\":\"PASS\",\"forward_states\":"<<nodes.size()<<",\"forward_edges\":"<<redges<<",\"backward_and_complement_coaccessible_states\":"<<snodes<<",\"coaccessible_edges\":"<<sedges<<",\"literal_six_word_edge_comparisons\":"<<comparisons<<",\"total_stored_reduced_word_letters\":"<<letters<<",\"maximum_single_free_word_length\":"<<maxword<<",\"final_full_twist_action_equal\":true,\"full_twist_decomposition_both_orders\":true,\"five_central_and_four_shift_identities\":true,\"equal_counts_different_prefix_actions_negative_control\":true,\"source_stream_or_code_read\":false}\n";
 return 0;
 }catch(const std::exception&e){std::cout<<"{\"status\":\"REJECTED\",\"error\":\""<<e.what()<<"\"}\n";return 1;}}
