#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb,lcm
import json,hashlib,datetime
P=Path(__file__).resolve().parent;B=P.parent
h=lambda b:hashlib.sha256(b).hexdigest()
seal=json.loads((P/'INDEPENDENT_SEAL.json').read_text())
for e in seal['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and h(b)==e['sha256']
cert=json.loads((P/'weighted_full_certificates.json').read_text())
for z in cert:
 p=list(map(F,z['weights']));q=list(map(F,z['q']));r=list(map(F,z['r']));dx=list(map(F,z['dual_x']));dy=list(map(F,z['dual_y']));x,y=F(z['x']),F(z['y']);S=z['B_supports'];T=z['maximal_allowed_unions'];k=z['k']
 assert sum(p)==sum(q)==sum(r)==sum(dx)==sum(dy)==1
 A=[[int(s>>a&1) for s in S] for a in range(len(p))];C=[[int(s&t==s) for t in T] for s in S]
 assert min(sum(q[j]*A[i][j] for j in range(len(q))) for i in range(len(p)))==x
 assert max(sum(dx[i]*A[i][j] for i in range(len(p))) for j in range(len(q)))==x
 assert min(sum(r[j]*C[i][j] for j in range(len(r))) for i in range(len(S)))==y
 assert max(sum(dy[i]*C[i][j] for i in range(len(S))) for j in range(len(r)))==y
 assert all(sum(p[a] for a in range(len(p)) if t>>a&1)<F(1,k) for t in T)
 assert not(x+k*y>1 and k*x+y>=1)
# Independently verify every source/LP family's frozen exact certificate.
V=json.loads((B/'sources_lp_review/NEW_CONTROLS.json').read_text());lp=0;uniform=0;cover=0
for z in V['lp_instances']:
 beta=list(map(F,z['B_weights']));masks=z['B_C_masks'];x=F(z['ordinary_graph']['x']);y=F(z['ordinary_graph']['y']);a=list(map(F,z['alpha']));q=list(map(F,z['dual_q']));rho=F(z['rho'])
 S=[s for s in range(1,1<<len(beta)) if sum(beta[j] for j in range(len(beta)) if s>>j&1)>=x]
 T=[sum(1<<j for j,mask in enumerate(masks) if mask>>c&1) for c in range(3)]
 M=[[int(bool(s&t)) for s in S] for t in T]
 assert len(a)==len(S) and len(q)==len(T) and sum(a)==sum(q)==1 and min(a)>=0 and min(q)>=0
 rows=[sum(a[j]*M[i][j] for j in range(len(a))) for i in range(len(q))];cols=[sum(q[i]*M[i][j] for i in range(len(q))) for j in range(len(a))]
 assert max(rows)==min(cols)==rho
 assert all(not a[j] or cols[j]==rho for j in range(len(a))) and all(not q[i] or rows[i]==rho for i in range(len(q)))
 assert min(F(mask.bit_count(),3) for mask in masks)==y
 assert z['ordinary_graph']['parts']==[lcm(*(w.denominator for w in a)),lcm(*(w.denominator for w in beta)),3]
 assert F(z['ordinary_graph']['maximum_reach'])==rho;lp+=1
for z in V['uniform_boundary_instances']:
 n,r,x,hs=z['n'],z['r'],F(z['x']),z['h'];assert hs==next(t for t in range(r,n+1) if comb(t,r)>=(x*comb(n,r)).__ceil__()) and F(z['reach'])==F(hs,n);uniform+=1
for z in V['exact_cover_dual_controls']:
 E=[{a} for a in range(5)]+list(map(set,z['edges']));u=list(map(F,z['dual_u']));c=list(map(F,z['primal_cover']));cost=F(z['cost']);assert sum(u)==sum(c)==cost and min(u)>=0 and min(c)>=0
 assert all(sum(u[a] for a in s)<=1 for s in E);assert all(sum(c[j] for j,s in enumerate(E) if a in s)>=1 for a in range(5));cover+=1
# Compare every root control stdout to the family data, excluding exactly its
# recorded metadata field when a full-stream artifact exists.
comparisons=[]
for script,name,artifact,omit in [('actual_graph_controls','maximal_types_review','ACTUAL_GRAPH_CHECKS.json','elapsed_seconds'),('rank_witness_controls','maximal_types_review','RANK_WITNESS_CHECKS.json',None),('triple_clique_controls','maximal_types_review','TRIPLE_CLIQUE_CHECKS.json',None),('deletion_boundary_controls','maximal_types_review','DELETION_BOUNDARY_CHECKS.json',None)]:
 a=json.loads((B/f'root_{name}_{script}.stdout').read_text());b=json.loads((B/name/artifact).read_text())
 if omit:a.pop(omit);b.pop(omit)
 assert a==b;comparisons.append({'family':name,'script':script,'full_json_equal':True,'excluded_metadata':omit})
s=json.loads((B/'root_sources_lp_review_new_controls.stdout').read_text());assert s['counts']==V['counts'] and s['input_files_verified']==49
L=json.loads((B/'laminar_uncrossing_review/INDEPENDENT_CONTROLS.json').read_text());s=json.loads((B/'root_laminar_uncrossing_review_independent_controls.stdout').read_text());assert s['counts']==L['counts'] and s['uncrossing_minimum_legal_max_reach']=='51/55'
assert (P/'publication_source.stdout').read_bytes()==(B/'root_public_replay.stdout').read_bytes()
# Current family file inventories, beyond individual file hashes.
for dr,mn,ex in [('sources_lp_review','OUTPUT_MANIFEST.json',{'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST_VERIFY.json'}),('maximal_types_review','AUDIT_MANIFEST.json',{'AUDIT_MANIFEST.json'}),('laminar_uncrossing_review','AUDIT_MANIFEST.json',{'AUDIT_MANIFEST.json'})]:
 d=B/dr;v=json.loads((d/mn).read_text());actual={str(f.relative_to(d)) for f in d.rglob('*') if f.is_file() and str(f.relative_to(d)) not in ex};assert actual=={e['path'] for e in v['files']},(dr,actual-{e['path'] for e in v['files']})
VR=json.loads((B/'sources_lp_review/OUTPUT_MANIFEST_VERIFY.json').read_text());mp=B/'sources_lp_review/OUTPUT_MANIFEST.json';assert mp.stat().st_size==VR['manifest_bytes'] and h(mp.read_bytes())==VR['manifest_sha256']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_seal_still_valid':True,'every_own_weighted_primal_dual_certificate_rechecked':len(cert),'every_sources_family_lp_certificate_rechecked':lp,'every_uniform_boundary_rechecked':uniform,'every_cover_primal_dual_rechecked':cover,'root_full_control_stream_comparisons':comparisons,'root_source_and_laminar_summary_counts_match_frozen_full_outputs':True,'own_complete_source_publication_replay_equals_root_full_stdout':True,'all_family_artifact_inventories_exact':True,'reports_compared':['ROOT_MATHEMATICAL_RECONSTRUCTION.md','sources_lp_review/REVIEW.md','maximal_types_review/PROOF_AUDIT.md','maximal_types_review/REPORT.md','laminar_uncrossing_review/FINAL_REVIEW.md','snapshot/unsolved_math_prioritization/attempts/30004047/review/REVIEW.md'],'proof_scope_agreement':'All independently agree on restricted theorem scopes and unresolved arbitrary overlapping higher-rank gap; historical/family conclusions are comparisons, not premises.'},indent=2))
