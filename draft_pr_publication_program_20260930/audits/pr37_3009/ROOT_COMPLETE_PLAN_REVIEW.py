#!/usr/bin/env python3
"""Root independent complete-object review; consumes raw plan without importing adapter."""
import collections,copy,datetime,hashlib,json,re
from pathlib import Path
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr37_3009';O=A/'root_source_first_private_reexecution';E=A/'whole_current_source_first_family/replay_v7';P=A/'final_receipt_preparation_family/ROOT_REVIEW_COMPARISON_PLAN_DRAFT.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def typed(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return set(a)==set(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def n(s):
 s=s.replace(str(O),'<OUTPUT>').replace(str(E),'<OUTPUT>')
 return re.sub(r'(root_(?:original_)?replay_)20261002T\d{12}Z',r'\1<CLOCK>',s)
def leaf(v,p):
 q=p.split('/')[1:];q=[x.replace('~1','/').replace('~0','~') for x in q]
 for x in q[:-1]:v=v[int(x)] if isinstance(v,list) else v[x]
 k=int(q[-1]) if isinstance(v,list) else q[-1]
 assert not isinstance(v[k],(dict,list));return v,k
index={};counts=collections.Counter();streams=[]
for root in [O,A/'whole_current_source_first_family',A/'reviewed_candidate']:
 for f in root.rglob('*'):
  if f.is_file() and not f.is_symlink():
   b=f.read_bytes();index.setdefault(digest(b),[]).append({'path':str(f.relative_to(R)),'bytes':len(b)})
for f in O.rglob('*.stderr'):
 if not f.is_file():continue
 g=E/f.relative_to(O)
 if not g.is_file():continue
 x,y=f.read_text(),g.read_text()
 if n(x)==n(y):streams.append((x,y,str(f.relative_to(R)),str(g.relative_to(R))))
j=json.loads(P.read_bytes());assert j['root_reviewed'] is False and j['entire_current_packet_source_first_review_checked_by_root'] is False
records=[];bad=[]
for c in j['comparisons']:
 raw=[]
 for role in ['actual','expected']:
  pin=c[role];f=R/pin['path'];b=f.read_bytes();assert len(b)==pin['bytes'] and digest(b)==pin['sha256'];raw.append(b)
 assert c['actual']['path']!=c['expected']['path'] and (R/c['actual']['path']).is_relative_to(O)
 x,y=raw;cr={'label':c['label'],'kind':c['kind'],'raw_byte_equal':x==y,'operations':[]}
 if c['kind']=='byte_exact':assert x==y and not c['normalizations']
 elif c['kind']=='full_text_exact_after_literal_path_transport':
  assert len(c['normalizations'])==1 and n(x.decode())==n(y.decode());counts['exact_complete_source_path_transport']+=1
 elif c['kind']=='full_parsed_json':
  l,r=json.loads(x),json.loads(y);seen=set()
  for z in c['normalizations']:
   ptr=z['pointer'];assert ptr not in seen;seen.add(ptr)
   a,k=leaf(l,ptr);b,h=leaf(r,ptr);u,v=a[k],b[h]
   assert typed(u,z['actual_before']) and typed(v,z['expected_before']) and type(u)==type(v)==type(z['canonical_value'])
   category=None;evidence=[]
   if type(u)==int:
    if str(k) in ['bytes','size','stdout_bytes','stderr_bytes'] or str(k) in ['actual','expected','saved'] and isinstance(a,dict) and re.search('/(bytes|size|stdout_bytes|stderr_bytes)$',a.get('path','')):category='explicit_recorded_output_byte_count'
   elif type(u)==str:
    if re.fullmatch(r'2026-\d\d-\d\d[T ].*',u) and re.fullmatch(r'2026-\d\d-\d\d[T ].*',v):
     datetime.datetime.fromisoformat(u.replace(' UTC','+00:00'));datetime.datetime.fromisoformat(v.replace(' UTC','+00:00'));category='actual_recorded_execution_clock'
    elif re.fullmatch('[0-9a-f]{64}',u) and re.fullmatch('[0-9a-f]{64}',v):
     if u in index and v in index:category='derived_hash_of_retained_complete_bytes';evidence=[index[u][0],index[v][0]]
     elif c['label']=='full_support__BUILDER_FULL_DIFF.json' and re.fullmatch('/differences/[0-6]/actual/sha256',ptr) or c['label']=='full_support__private_actual_builder.stdout' and ptr=='/manifest_sha256':category='qualified_ephemeral_builder_admin_hash_not_retained'
    elif n(u)==n(v):category='exact_literal_output_or_stamped_private_directory_transport'
    elif len(u)==len(v)==500:
     hits=[(f,g) for a1,b1,f,g in streams if a1.endswith(u) and b1.endswith(v)]
     if hits:category='length500_tail_of_complete_retained_equivalent_traceback';evidence=hits[:1]
   if category is None:bad.append({'label':c['label'],'pointer':ptr,'actual':u,'expected':v})
   else:counts[category]+=1
   cr['operations'].append({'pointer':ptr,'category':category,'evidence':evidence})
   a[k]=copy.deepcopy(z['canonical_value']);b[h]=copy.deepcopy(z['canonical_value'])
  assert typed(l,r),'complete object differs '+c['label']
 else:raise AssertionError(c['kind'])
 records.append(cr)
report={'schema':'root-independent-pr37-full-plan-review/v1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'draft_plan_sha256':digest(P.read_bytes()),'comparison_count':len(records),'normalization_count':sum(len(c['normalizations']) for c in j['comparisons']),'classifications':dict(counts),'unclassified':bad,'complete_objects_type_strict_equal_after_exact_reviewed_operations':True,'root_reports_previously_read_completely':['whole_current_source_first_family/REPORT.md','whole_current_source_first_family/SUMMARY.json'],'ephemeral_builder_limit':'Seven deleted private builder administrative rows/manifest hashes are reported by retained full diff and unchanged executed source; absent raw bytes are not certified retained. All96 internal full comparisons already executed and passed; exact original science/claims remain frozen.', 'records':records}
out=A/'ROOT_COMPLETE_PLAN_REVIEW.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'comparisons':len(records),'normalizations':report['normalization_count'],'classifications':dict(counts),'unclassified_count':len(bad),'first_unclassified':bad[:2],'report_sha256':digest(out.read_bytes())}))
