"""Bounded dependency/witness check. No submitted module is imported or run.

Reads one retained finite-ledger row and reconstructs its tiny literal graphs;
this is not an atlas/classifier or rank-certificate replay.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import permutations
import ast, gzip, hashlib, json, signal, zipfile

O=Path(__file__).resolve().parent
P=O.parents[3]
T=P/'papers/22395326/sources/published-source/Symmetry-Stratified_Level2_Journal_TeX.zip/Symmetry-Stratified_Level2_Journal_TeX'
OLD=P/'papers/22168797'
K=OLD/'sources/published-source/K2P_SAME_Reproducibility_Package_v1.0.5-r1/k2p_same_reproducibility_v1.0.5-r1'
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError()))
signal.alarm(55)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def need(c,label):
 if not c:raise RuntimeError(label)
article=OLD/'sources/K2P_SAME_Principal_Domain_Article.pdf'
archive=OLD/'sources/K2P_SAME_Reproducibility_Package_v1.0.5-r1.zip'
need(sha(article)=='e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4','Wrong companion article')
need(sha(archive)=='477c160057f7a729215dfd37960063d283ddbedcf95396a8239a9fd22e94ac62','Wrong companion archive')
atlas=K/'package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py'
need(sha(atlas)=='afafe6c4289870a02226516e2b7ff207c57b844f4c45fc6864cedf826e9ec742','Wrong exact semantic helper')
ledger=K/'work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz'
need(sha(ledger)=='7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6','Wrong frozen finite ledger')
archive_matches=[]
with zipfile.ZipFile(archive) as z:
 for path in [atlas,ledger]:
  matches=[x for x in z.namelist() if x.endswith(str(path.relative_to(K)))]
  need(len(matches)==1,'Ambiguous/missing full-archive member')
  data=z.read(matches[0])
  need(hashlib.sha256(data).hexdigest()==sha(path),'Extracted evidence does not equal bound archive')
  archive_matches.append(dict(member=matches[0],sha256=sha(path),bytes=len(data),exact=True))
root=json.loads((OLD/'root-defect-check.json').read_text())
row=None
with gzip.open(ledger,'rt') as f:
 for line_index,line in enumerate(f,1):
  r=json.loads(line)
  if r.get('raw_id')==137124:
   row=r;break
need(row==root['published_row'],'Literal row differs from original falsification data')
need((row['source_index'],row['target_index'],row['permutation_index'],row['port_permutation'])==(2,85,12,[2,0,1,3]),'Wrong raw case')
need(row['corrected_category']=='exact_rank_exclusion' and row['evidence_binding']['source_exact_rank']==14 and row['evidence_binding']['target_exact_rank']==13,'Wrong certificate claim')

# Parse only the immutable literal core table; do not import the atlas module.
tree=ast.parse(atlas.read_text())
cores=[ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and
       any(isinstance(t,ast.Name) and t.id=='CORES' for t in n.targets)]
need(len(cores)==1,'Core literal not unique');cores=cores[0]
def wc(total,bins):
 if bins==1:
  yield (total,);return
 for first in range(total+1):
  for rest in wc(total-first,bins-1):yield (first,)+rest
sources=[(name,ri,repair) for name in ['theta0','theta1','theta3'] for ri,repair in enumerate(cores[name]['repairs'])]
need(sources[2]==('theta1',0,(2,3)),'Source2 does not have printed template')
# Reconstruct only target descriptors through85, stopping before the remainder.
index=0;desc=None
for name,spec in cores.items():
 if desc is not None:break
 for mask in range(1<<len(spec['sinks'])):
  if desc is not None:break
  ordinary=3-mask.bit_count()
  for counts in wc(ordinary,len(spec['arcs'])):
   if desc is not None:break
   repairs=[(None,())] if name=='cycle' else list(enumerate(spec['repairs']))
   for ri,repair in repairs:
    if index==85:
     desc=dict(core=name,mask=mask,counts=list(counts),repair_index=ri,repair=list(repair));break
    index+=1
need(desc==dict(core='theta0',mask=1,counts=[0,0,1,1,0],repair_index=0,repair=[2,3]),'Target85 template differs')
need(list(permutations(range(4)))[12]==(2,0,1,3),'Permutation index convention differs')

def graph(core):
 spec=cores[core];arcs=[]
 for i,(u,v) in enumerate(spec['arcs']):
  if i in (2,3):
   mid='P'+str(i);arcs += [(u,mid),(mid,v),(mid,'L'+str(i-1))]
  else:arcs.append((u,v))
 arcs += [('r','S'),('r','L0'),('X','L3')]
 return arcs,set(spec['retics'])
def mixed(arcs,retics,permutation):
 rename=lambda x:'L'+str(permutation[int(x[1:])]) if x.startswith('L') else x
 result=[];children=[]
 for u,v in arcs:
  if u=='r':children.append(rename(v));continue
  result.append((rename(u),rename(v),rename(v) if v in retics else ''))
 need(len(children)==2,'Root degree')
 result.append((children[0],children[1],''))
 return result
source_arcs,retics=graph('theta1');target_arcs,_=graph('theta0')
source=mixed(source_arcs,retics,range(4));target=mixed(target_arcs,retics,[2,0,1,3])
iso={'S':'P3','U':'U','V':'V','X':'X','P2':'S','P3':'P2',**{f'L{i}':f'L{i}' for i in range(4)}}
can=lambda u,v,h:(*sorted((u,v)),h)
mapped=[can(iso[u],iso[v],iso[h] if h else '') for u,v,h in target]
need(len(iso)==len(set(iso.values()))==10,'Not a bijection')
need({can(*x) for x in source}==set(mapped),'Not the same labelled/headed mixed graph')
need(len(source)==len(target)==11,'Edge count')
checks=[]
for label,arcs,M in [('source',source_arcs,source),('target',target_arcs,target)]:
 vertices={v for e in arcs for v in e};indeg={v:sum(w==v for _,w in arcs) for v in vertices};queue=[v for v in vertices if indeg[v]==0];seen=[]
 while queue:
  v=queue.pop();seen.append(v)
  for u,w in arcs:
   if u==v:
    indeg[w]-=1
    if indeg[w]==0:queue.append(w)
 need(len(seen)==len(vertices),'Not an acyclic rooting')
 for v in vertices:
  deg=(sum(w==v for _,w in arcs),sum(u==v for u,_ in arcs))
  need(deg==((0,2) if v=='r' else (1,0) if v.startswith('L') else (2,1) if v in retics else (1,2)),'Binary degree')
  if not v.startswith('L'):
   need(any(w.startswith('L') or w not in retics for u,w in arcs if u==v),'Not tree-child')
 for u,v,h in M:
  if h:
   tail=v if h==u else u
   need(sum(not head and tail in (a,b) for a,b,head in M)==2,'No-omnian local strong criterion fails')
 checks.append(dict(graph=label,acyclic_binary_rooting=True,tree_child=True,all_reticulation_tails_two_ordinary_incidences=True))
wrong=mixed(target_arcs,retics,[2,1,0,3])
need({can(*x) for x in source}!={can(iso[u],iso[v],iso[h] if h else '') for u,v,h in wrong},'Wrong-label control undetected')
wronghead=list(target);u,v,h=wronghead[1];wronghead[1]=(u,v,'' if h else v)
need({can(*x) for x in source}!={can(iso[u],iso[v],iso[h] if h else '') for u,v,h in wronghead},'Wrong-head control undetected')

supp=(T/'supplement.tex').read_text();main=(T/'sections/03_main_theorems.tex').read_text();transfer=(T/'sections/04_transfer_principle.tex').read_text()
need(sha(article) in supp and sha(archive) in supp and sha(atlas) in supp,'Synthesis no longer binds exact defective release')
need('Necessity is taken from the full-factor finite proof of Theorem~6.3' in supp,'A6 dependency differs')
need('In\nK2P, the A2--A6 local, restoration, and probe chain gives necessity' in main,'Main theorem dependency differs')
need('For K2P, the finite\nproof of Theorem~6.3 compares the full selected complete-factor graphs' in transfer,'Sitewise crosswalk dependency differs')
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='SAME_DEFECTIVE_FINITE_IMPORT_STILL_REQUIRED_NO_BYPASS_FOUND',
 exact_bound_article=sha(article),exact_bound_archive=sha(archive),exact_bound_semantic_helper=sha(atlas),
 exact_archive_payload_comparisons=archive_matches,raw_row_line=line_index,published_row=row,
 source_descriptor=dict(index=2,core='theta1',repair=[2,3],incoming_label=0),
 target_descriptor=dict(index=85,**desc,incoming_label_after_permutation=2),source_mixed_edges=source,target_mixed_edges_after_port_permutation=target,
 target_to_source_label_and_head_preserving_map=iso,all_eleven_edges_and_heads_match=True,graph_checks=checks,
 negative_controls=dict(wrong_label_rejected=True,wrong_head_rejected=True),
 rank_interpretation='The retained14vs13 numbers are arm-fixed ranks. They are not an obstruction to the same mixed graph with independently chosen incoming boundaries and incidence/physical transport. No fresh rank-certificate replay claimed.',
 dependency_interpretation='The synthesis explicitly imports the full-factor finite proof for A6/T3 necessity; its semantic helper identifies allowed terminals but does not soundly reclassify every earlier rank exclusion or quotient incoming boundary gauges.',
 conclusion_limits='Invalid imported finite proof object; missing complete K2P local-rigidity proof at declared interface. Not a counterexample to the structural theorem, not a K3P-rooting conclusion, and no repair performed.',
 full_atlas_rerun=False,submitted_modules_imported=False,original_writes=False)
(O/'RECONCILIATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'archive_payloads':len(archive_matches),'raw_id':137124,'edges':11,'negative_controls':2},indent=2))
