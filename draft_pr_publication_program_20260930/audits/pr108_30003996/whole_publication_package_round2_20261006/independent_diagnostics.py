#!/usr/bin/env python3
"""Fresh first-party R2 checks; does not call package tree or cost evaluators."""
from pathlib import Path, PurePosixPath
from itertools import product, combinations
from collections import Counter
import datetime,hashlib,importlib.util,json,os,stat,sys,zipfile
O=Path(__file__).resolve().parent; A=O.parent; D=A/'publication_ready_package_v2';checks=Counter()
def ck(value,key):
 if not value:raise RuntimeError(key)
 checks[key]+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validpath(s):
 p=PurePosixPath(s)
 return not p.is_absolute() and bool(p.parts) and '..' not in p.parts and '\\' not in s and str(p)==s
# Independent byte inventory; no trust in self-reported inventory success.
pins=json.loads((O/'INPUT_PINS.json').read_text())['files']
ck(len(pins)==48,'48_pinned_files')
for row in pins:
 p=D/row['path'];ck(p.is_file() and not p.is_symlink(),'regular_pinned_file');ck(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'input_pin_stable')
manifest=json.loads((D/'PACKAGE_MANIFEST.json').read_text()); rows=manifest['files']
ck(len(rows)==46,'46_logical_payload_rows');names=[r['relative_path'] for r in rows]
ck(len(names)==len(set(names)),'manifest_no_duplicates');ck(all(validpath(x) for x in names),'manifest_safe_paths')
ck(set(names)=={r['path'] for r in pins}-{'PACKAGE_MANIFEST.json','root_dependent_spanning_trees_support.zip'},'manifest_exact_global_coverage')
for r in rows:ck((D/r['relative_path']).stat().st_size==r['bytes'] and sha(D/r['relative_path'])==r['sha256'],'outer_manifest_row_bytes')
for folder,filename,exclude in [(D,'PACKAGE_MANIFEST.json',{'PACKAGE_MANIFEST.json','SHA256SUMS','root_dependent_spanning_trees_support.zip'}),(D/'source_preparation','SOURCE_PREPARATION_MANIFEST.json',{'SHA256SUMS','SEAL.json'})]:
 lines=(folder/'SHA256SUMS').read_text().splitlines();pairs=[l.split('  ',1) for l in lines]
 ck(len(pairs)==len({p[1] for p in pairs}),'checksum_no_duplicates')
 for digest,name in pairs:ck(validpath(name) and sha(folder/name)==digest,'checksum_correct_safe')
 if folder==D:ck({p[1] for p in pairs}==set(names)-{'SHA256SUMS'},'outer_checksum_exact_coverage')
 else:
  sm=json.loads((folder/filename).read_text());ck(len(sm['files'])==36 and sum(r['bytes'] for r in sm['files'])==sm['payload_total_bytes']==186557,'source_manifest_totals')
  for r in sm['files']:ck(sha(folder/r['relative_path'])==r['sha256'] and (folder/r['relative_path']).stat().st_size==r['bytes'],'source_manifest_rows')
  ck({p[1] for p in pairs}=={r['relative_path'] for r in sm['files']}|{filename},'source_checksum_exact_coverage')
with zipfile.ZipFile(D/'root_dependent_spanning_trees_support.zip') as z:
 members=z.infolist();znames=[p.filename for p in members]
 ck(len(members)==47 and len(znames)==len(set(znames)),'zip_47_unique_members')
 ck(set(znames)==set(names)|{'PACKAGE_MANIFEST.json'},'zip_exact_members')
 ck(z.testzip() is None,'zip_crc')
 for p in members:
  ck(validpath(p.filename) and not p.is_dir() and not stat.S_ISLNK(p.external_attr>>16),'zip_no_traversal_or_symlink')
  ck(z.read(p.filename)==(D/p.filename).read_bytes(),'zip_exact_member_bytes')
metas=[json.loads((D/p).read_text())['metadata'] for p in ['intended_zenodo_metadata.json','zenodo-deposit.json','source_preparation/intended_zenodo_metadata.json','source_preparation/zenodo-deposit.json']]
ck(all(m==metas[0] for m in metas),'four_metadata_objects_identical')
ck((D/'intended_zenodo_metadata.json').read_bytes()==(D/'source_preparation/intended_zenodo_metadata.json').read_bytes(),'metadata_copies_byte_identical')
ck((D/'zenodo-deposit.json').read_bytes()==(D/'source_preparation/zenodo-deposit.json').read_bytes(),'deposit_copies_byte_identical')
ck(json.loads((D/'zenodo-deposit.json').read_text())['files']==[{'path':'root_dependent_spanning_trees.pdf'},{'path':'root_dependent_spanning_trees_support.zip'}],'two_planned_uploads')
ck('prereserve_doi' not in json.dumps(metas[0]) and 'placeholder' not in json.dumps(metas[0]),'no_DOI_placeholder')
qa=json.loads((A/'ROOT_PDF_BUILD_V1_QA_20261006.json').read_text())
for r in qa['page_image_pins']:ck(sha(A/r['path_relative_to_pr108_audit'])==r['sha256'],'actual_viewed_image_binding')
ck(sha(D/'root_dependent_spanning_trees.pdf')==qa['PDF']['sha256'],'actual_PDF_image_provenance_binding')
ck(sha(D/'source_preparation/root_dependent_spanning_trees.tex')==qa['source_after_export']['sha256'],'actual_TeX_PDF_continuity')
# Fresh combinatorial construction and evaluator: tree directions are selected by
# distances to each root, calculated with Floyd-Warshall, not package BFS/cuts.
def make(cs,B=2,shift=0):
 symbols=sorted({abs(l) for c in cs for l in c}); n=len(symbols);ren={s:i+2 for i,s in enumerate(symbols)};m=len(cs);N=n+m+2
 edges={(0,1)}|{tuple(sorted((h,v))) for h in (0,1) for v in ren.values()}
 edges|={(ren[abs(l)],n+2+j) for j,c in enumerate(cs) for l in c};edges=tuple(sorted(edges));arcs=tuple(a for u,v in edges for a in ((u,v),(v,u)))
 costs={(r,u,v):shift for r in range(N) for u,v in arcs}
 for u,v in edges:
  val=0 if (u,v)==(0,1) else B if v>=n+2 else 1
  costs[0,u,v]+=val;costs[0,v,u]+=val
 for j,c in enumerate(cs):
  for l in c:costs[n+2+j,ren[abs(l)],1 if l>0 else 0]+=1
 return dict(N=N,edges=edges,costs=costs,K=B*m+n+shift*N*(N-1),n=n,m=m,cs=cs,ren=ren,arcs=arcs)
def distances(N,tree):
 d=[[0 if i==j else N+1 for j in range(N)] for i in range(N)]
 for u,v in tree:d[u][v]=d[v][u]=1
 for k in range(N):
  for i in range(N):
   for j in range(N):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
 return d
def trees(N,edges):
 for es in combinations(edges,N-1):
  d=distances(N,es)
  if all(d[0][i]<N for i in range(N)):yield es,d
# Connectivity plus N-1 edges suffices for simple undirected trees.
def value(inst,es,d,inward=False,transpose=False):
 vals=[]
 for r in range(inst['N']):
  val=0
  for u,v in es:
   a,b=(u,v) if d[r][u]<d[r][v] else (v,u)
   if inward:a,b=b,a
   if transpose:a,b=b,a
   val+=inst['costs'][r,a,b]
  vals.append(val)
 return vals
def test(cs,B):
 I=make(cs,B);N,n,m,K=I['N'],I['n'],I['m'],I['K'];sats=[]
 for ass in product((False,True),repeat=n):
  if all(any(ass[abs(l)-1]==(l>0) for l in c) for c in cs):sats.append(ass)
 feasible=[];totals=[];nonstructured=0
 for es,d in trees(N,I['edges']):
  vals=value(I,es,d);F=sum(vals);q=sum(v>=n+2 for u,v in es);h=int((0,1) in es);p=N-1-q-h
  ck(vals[0]==p+B*q==K+1-h+(B-1)*(q-m),'fresh_all_tree_base_identity');ck(q>=m and F>=vals[0],'fresh_nonnegative_domination')
  ck(value(I,es,d,True,True)==vals,'fresh_transpose_all_roots')
  shifted=make(cs,B,1);ck(value(shifted,es,d)==[v+N-1 for v in vals],'fresh_shift_all_roots')
  if h==1 and q==m:
   ass=tuple((0,i+2) in es for i in range(n));pen=0
   for j,c in enumerate(cs):
    v=next(u for u,w in es if w==n+2+j);l=next(l for l in c if abs(l)+1==v);false=int(ass[abs(l)-1]!=(l>0))
    ck(vals[n+2+j]==false,'fresh_individual_clause_orientation');pen+=false
   ck(F==K+pen,'fresh_structured_identity')
  else:ck(F>K,'fresh_unstructured_exclusion');nonstructured+=1
  if F<=K:feasible.append(es)
  totals.append(F)
 ck(bool(feasible)==bool(sats),'fresh_SAT_equivalence')
 return dict(N=N,B=B,clauses=cs,trees=len(totals),unstructured_trees=nonstructured,minimum=min(totals),K=K,histogram=dict(sorted(Counter(totals).items())))
fixture=json.loads((D/'source_preparation/example_full_cost_instance.json').read_text());f=fixture['instance'];cs=((1,2),(1,-2),(-1,2),(-1,-2));I=make(cs)
ck(f['N']==I['N'] and tuple(map(tuple,f['edges']))==I['edges'] and f['K']==I['K'],'fresh_fixture_graph_threshold')
ck(f['costs']==[[I['costs'][r,u,v] for u,v in I['arcs']] for r in range(I['N'])],'fresh_all208_costs')
ck(sum(map(len,f['costs']))==208,'208_full_entries')
fixture_result=test(cs,2);ck(fixture_result['trees']==384 and fixture_result['minimum']==11 and fixture_result['K']==10,'fresh_384_tree_exact_fixture')
# Independent matrix-tree census with exact fraction elimination.
from fractions import Fraction
M=[[Fraction(0) for _ in range(7)] for _ in range(7)]
for u,v in I['edges']:
 if u<7:M[u][u]+=1
 if v<7:M[v][v]+=1
 if u<7 and v<7:M[u][v]-=1;M[v][u]-=1
det=Fraction(1)
for k in range(7):
 pivot=next(j for j in range(k,7) if M[j][k]);
 if pivot!=k:M[k],M[pivot]=M[pivot],M[k];det=-det
 p=M[k][k];det*=p
 for j in range(k+1,7):
  factor=M[j][k]/p
  for l in range(k,7):M[j][l]-=factor*M[k][l]
ck(det==384,'fresh_matrix_tree_384')
formula_results=[fixture_result]
for cs in [((1,),),((1,),(-1,)),((1,2),(-1,2)),((1,2,3),(-1,-2,-3)),((1,),(-2,),(2,3))]:
 for B in sorted({2,len({abs(l) for c in cs for l in c})+1}):formula_results.append(test(cs,B))
# Test public normalization entrypoints without using their cost/tree evaluator.
spec=importlib.util.spec_from_file_location('copied_exact',O/'scratch/source/verify_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
malformed_results=[]
for entry in (mod.normalize,mod.construct):
 for bad,guard in [([0],'literal_labels_are_nonzero_integers'),([True],'literal_labels_are_nonzero_integers'),([1,2,3,4],'at_most_three_input_literals'),(['1'],'literal_labels_are_nonzero_integers'),([1.0],'literal_labels_are_nonzero_integers')]:
  for raw in [[bad],[[],bad],[bad,[]]]:
   try:entry(raw)
   except AssertionError as e:ck(str(e)==guard,'fresh_intended_entrypoint_malformed_guard');malformed_results.append(dict(entry=entry.__name__,raw=raw,guard=str(e)))
   else:ck(False,'malformed_accepted')
for raw,kind in [([], 'yes'),([[]],'no'),([(9,-9)],'yes'),([(9,9)],'ordinary'),([(9,-9),()],'no')]:ck(mod.normalize(raw)['kind']==kind,'fresh_normalization_boundary')
ck(mod.normalize([(10**100,10**100),(-41,),(41,10**100)])=={'kind':'ordinary','clauses':[(2,),(-1,),(1,2)],'symbols':[41,10**100]},'fresh_arbitrarily_sparse_binary_labels')
ck(mod.normalize(iter((iter((9,-9)),iter((41,41)))))=={'kind':'ordinary','clauses':[(1,)],'symbols':[41]},'fresh_single_use_iterators')
# Meaningful independent failure controls; neither guard disappears with -O.
for label,fn in [('false_guard',lambda:ck(False,'intentional_fresh_guard')),('cost_corruption',lambda:ck(f['costs'][0][0]+1==I['costs'][0,0,1],'intentional_fixture_cost_corruption'))]:
 try:fn()
 except RuntimeError as e:ck(str(e).startswith('intentional_'),'fresh_control_intended_failure')
 else:ck(False,'fresh_control_failed_to_reject')
result=dict(schema='pr108-fresh-r2-independent-diagnostics/v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_PID=os.getpid(),optimization=sys.flags.optimize,checks=dict(checks),total_checks=sum(checks.values()),all_pass=True,fixture=fixture_result,formula_results=formula_results,malformed_results=malformed_results,matrix_tree_count=int(det),source_import_scope='Only normalization and construction malformed entrypoints; no package tree/cost evaluators imported or called',finite_scope='Selected boundary/formula cases independently constructed and evaluated; does not replace all-size proof')
(O/f'INDEPENDENT_DIAGNOSTICS_{sys.flags.optimize}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
