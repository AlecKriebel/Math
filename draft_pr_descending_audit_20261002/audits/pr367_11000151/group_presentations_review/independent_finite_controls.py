"""Independent reversed-order frontier and explicit backward coaccessibility audit."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json, hashlib, datetime, subprocess
D=Path(__file__).resolve().parent; P=D/'private_streams'; P.mkdir(exist_ok=True); (D/'private_tmp').mkdir(exist_ok=True)
def inverse(word): return tuple(-a for a in reversed(word))
def reduced(word):
 result=[]
 for a in word:
  if result and a==-result[-1]: result.pop()
  else: result.append(a)
 return tuple(result)
def substitute(word,table):
 output=[]
 for a in word: output.extend(table[a-1] if a>0 else inverse(table[-a-1]))
 return reduced(output)
def compose_right(images,table): return tuple(substitute(word,table) for word in images)
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),((1,),(2,),(3,),(3,-2,1,4))]
B=[((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),((1,),(2,),(3,),(-1,2,-3,4))]
I=tuple((i,) for i in range(1,5)); c=(1,2,3,4)*5; h=(5,4,3,2,1,1,2,3,4,5)
def action(word,tables=A):
 result=I
 for a in word:result=compose_right(result,tables[a-1])
 return result
assert all(compose_right(A[i],B[i])==I==compose_right(B[i],A[i]) for i in range(5))
relations=[((i,j,i),(j,i,j)) if j==i+1 else ((i,j),(j,i)) for i,j in combinations(range(1,6),2)]
assert all(action(x)==action(y) for x,y in relations);assert action(c)==action(h)
mutant=list(A);mutant[4]=((1,),(2,),(3,),(2,-2,1,4)); mutation_failures=sum(action(x,mutant)!=action(y,mutant) for x,y in relations)+int(action(c,mutant)!=action(h,mutant));assert mutation_failures>0
# Carry images in a reversed-direction iterative frontier; retain every complete candidate.
survivors=set(); census=[]; total=0; stream=[]; target=action(c+c)
for center in range(6):
 frontier=[(center,(0,)*5,(),I)]
 for depth in range(20):
  nxt=[]
  for pos,counts,word,images in frontier:
   for dest in (pos+1,pos-1):
    if dest<0 or dest>5:continue
    edge=min(pos,dest)
    if counts[edge]==4:continue
    nc=list(counts);nc[edge]+=1
    nxt.append((dest,tuple(nc),word+(edge+1,),compose_right(images,A[edge])))
  frontier=nxt
 cases=[r for r in frontier if r[0]==center]; census.append(len(cases));total+=len(cases)
 for pos,counts,word,images in cases:
  assert counts==(4,)*5
  yes=images==target
  if yes:survivors.add(word)
  stream.append({'center':center+1,'word':word,'images':images,'survives':yes})
assert total==810 and census==[81,162,162,162,162,81]
assert survivors=={(h+h)[j:]+(h+h)[:j] for j in range(20)}
(P/'all_810_F4_actions.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in stream))
# Construct reachability with descending generator order, and backward reachability with
# explicit predecessor transitions from the full state. No complement rule is used to choose S.
rank_results=[]
for strands in range(1,7):
 pairs=list(combinations(range(strands),2)); index={pair:i for i,pair in enumerate(pairs)}; weights=[3**i for i in range(len(pairs))]; full=3**len(pairs)-1
 identity=tuple(range(strands)); parents={0:(identity,None,None)}; queue=[0]; forward_edges=0
 for code in queue:
  permutation=parents[code][0]
  for generator in range(strands-2,-1,-1):
   pair=tuple(sorted(permutation[generator:generator+2])); step=weights[index[pair]]
   if code//step%3>=2:continue
   forward_edges+=1; nc=code+step; np=list(permutation);np[generator],np[generator+1]=np[generator+1],np[generator];np=tuple(np)
   if nc in parents:assert parents[nc][0]==np
   else:parents[nc]=(np,code,generator+1);queue.append(nc)
 backwards={full:identity}; backqueue=[full]; backward_edges=0
 for code in backqueue:
  permutation=backwards[code]
  for generator in range(strands-1):
   pair=tuple(sorted(permutation[generator:generator+2]));step=weights[index[pair]]
   if code//step%3==0:continue
   backward_edges+=1;nc=code-step;np=list(permutation);np[generator],np[generator+1]=np[generator+1],np[generator];np=tuple(np)
   if nc in backwards:assert backwards[nc]==np
   else:backwards[nc]=np;backqueue.append(nc)
 co=parents.keys() & backwards.keys(); assert co=={code for code in parents if full-code in parents}
 tables=[]
 for g in range(1,strands):
  t=[(j,) for j in range(1,strands+1)];t[g-1]=(g,g+1,-g);t[g]=(g,);tables.append(t)
 images={0:tuple((j,) for j in range(1,strands+1))}
 for code in queue:
  if code and code in co:
   permutation,parent,g=parents[code];assert parent in co
   images[code]=compose_right(images[parent],tables[g-1])
 comparisons=0;sha=hashlib.sha256();path_count={0:1}
 for code in queue:
  if code not in co:continue
  permutation=parents[code][0]
  for gen in range(strands-1):
   pair=tuple(sorted(permutation[gen:gen+2]));step=weights[index[pair]]
   if code//step%3==2:continue
   nc=code+step
   if nc not in co:continue
   assert compose_right(images[code],tables[gen])==images[nc];comparisons+=1
   path_count[nc]=path_count.get(nc,0)+path_count[code]
 standard=images[0]
 for repeat in range(strands):
  for table in tables:standard=compose_right(standard,table)
 assert images[full]==standard
 stream_path=P/f'rank{strands}_all_coaccessible_actions.txt'
 with stream_path.open('wb') as output:
  for code in sorted(co):
   permutation=parents[code][0];packed=sum(a<<(3*i) for i,a in enumerate(permutation))
   line=('S|'+str(code)+'|'+str(packed)+'|'+'|'.join(','.join(map(str,word)) for word in images[code])+'\n').encode();sha.update(line);output.write(line)
 result={'strands':strands,'reachable_states':len(parents),'outgoing_edges':forward_edges,'backward_states':len(backwards),'backward_edges':backward_edges,'coaccessible_states':len(co),'coaccessible_edges':comparisons,'complete_positive_words':path_count[full],'canonical_action_stream_sha256':sha.hexdigest()}
 rank_results.append(result); print(json.dumps(result),flush=True)
 if strands==6:
  assert len(parents)==234368 and forward_edges==711342 and len(co)==90921 and comparisons==261810
  assert sha.hexdigest()=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf'
# Complete C++ raw stream retention and byte-level comparison, not digest-only comparison.
snapshot=D.parent/'snapshot/problems/11000151_artin_a5_quotient';exe=D/'private_tmp/check_turn_4_cpp';cppstream=P/'candidate_cpp_full_stream.stdout'
subprocess.run(['g++','-O3','-std=c++17',str(snapshot/'check_turn_4.cpp'),'-o',str(exe)],check=True)
process=subprocess.Popen([str(exe),'--stream'],stdout=subprocess.PIPE)
stream_bytes=0;stream_records=0
with (P/'rank6_all_coaccessible_actions.txt').open('rb') as expected:
 for actual in process.stdout:
  stream_bytes+=len(actual)
  if actual.startswith(b'S|'):
   assert actual==expected.readline();stream_records+=1
  else:
   cpp_receipt=json.loads(actual)
 assert expected.read()==b''
assert process.wait()==0 and stream_records==90921
b_bytes=stream_bytes
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','F4_inverse_pairs':10,'F4_artin_relations':10,'F4_extra_relation':True,'mutant_failed_relations':mutation_failures,'twenty_candidates':total,'twenty_survivors':len(survivors),'all_810_images_retained':True,'ranks':rank_results,'candidate_Cpp_full_stream_bytes':b_bytes,'candidate_Cpp_records_exact_match':True,'scope':'Complete rank1..6 controls; rank6 is the stated theorem. Independent backwards graph and descending-generator canonical paths. No rank7 inference.'}
(D/'receipts/INDEPENDENT_FINITE_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
