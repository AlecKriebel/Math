"""One-time finalization of this own source/scope packet only.
Does not edit any original or early file, execute paper code, or mutate Git.
"""
from pathlib import Path
import json,hashlib,datetime,subprocess,os
E=Path(__file__).resolve().parent;R=E.parents[1];S=R/'sources';G=R.parents[2]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def binding(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
assert not (E/'FINAL_SEAL.json').exists() and not (S/'SOURCE_FINAL_SEAL.json').exists()
ready_manifest=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())
for r in ready_manifest['files']:
 b=(S/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
source_files=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(S.rglob('*')) if p.is_file()]
assert len(source_files)==153
save(S/'SOURCE_FINAL_MANIFEST.json',{'utc':now(),'status':'COMPLETE_ORIGINAL_SOURCE_CUSTODY','files':source_files,'original_SOURCE_READY_manifest_sha256':sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'no_original_mutation':True})
m=S/'SOURCE_FINAL_MANIFEST.json'
save(S/'SOURCE_FINAL_SEAL.json',{'utc':now(),'status':'IMMUTABLE_COMPLETE_ORIGINAL_SOURCE_CUSTODY','manifest':{'path':'SOURCE_FINAL_MANIFEST.json','bytes':m.stat().st_size,'sha256':sha(m.read_bytes())},'original_bindings':len(source_files),'source_ready_sha256':sha((S/'SOURCE_READY.json').read_bytes()),'preserve_immutable':True})
save(E/'SOURCE_BINDING_RECEIPT.json',{'utc':now(),'complete_source_files':[binding(p) for p in sorted(S.rglob('*')) if p.is_file()],'source_ready_original_bindings':151,'source_final_original_bindings':153,'whole_original_API_objects':'sources/record.raw.json; latest.raw.json; versions.raw.json; original list order and complete objects retained in SOURCE_READY','original_API_asset_order':['weighted-yamabe-heat-trace-note.pdf','weighted-yamabe-heat-trace-verification.zip'],'no_aliases_or_repacked_originals':True})
baseline=json.loads((E/'PRESERVATION_BEFORE.json').read_text());changed=[]
for r in baseline['files']:
 p=Path(r['path'])
 if not p.exists() or p.stat().st_size!=r['bytes'] or sha(p.read_bytes())!=r['sha256']:changed.append(r['path'])
refs={ref:subprocess.run(['git','rev-parse',ref],cwd=G,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True).stdout.decode().strip() for ref in baseline['resolved_Git_refs']}
assert not changed and refs==baseline['resolved_Git_refs']
save(E/'PRESERVATION_AFTER.json',{'utc':now(),'prior_bindings':len(baseline['files']),'changed_originals':changed,'resolved_Git_refs':refs,'local_HEAD_main_index_unchanged':True,'source_ready_originals_unchanged':151,'early_seal_sha256':sha((E/'EARLY_SEAL.json').read_bytes()),'previous_sealed_packets_unchanged':True})
verdict={'utc':now(),'record_id':23383952,'native_row':108,'status':'FINITE_WEIGHTED_YAMABE_COUNTEREXAMPLE_SURVIVES_INDEPENDENT_SOURCE_SCOPE_REVIEW','strongest_verified_claim':'Complete original finite normalized smooth positive S3 weight with explicit positive time t*=4a, scaled trace strictly above1106714561/1700054750>13/20, round all-time maximum below321/500, and both maxima attained.','verified_lower_fraction':'1106714561/1700054750','verified_lower_margin_above_13_over_20':'3357947/3400109500','verified_round_uniform_enclosure':'641202/1000000 <321/500','mathematical_defect_identified':None,'substantive_remaining_proof_gap':None,'original_question_operator_normalization_dimension_verified':True,'inherited_mechanism':'Classical Pinocchio/cylindrical conformal geometry, conformal covariance and Dirichlet form min–max estimates. No newly invented geometric method claimed.','novelty_status':'Bounded primary/source search only; worldwide firstness and continued openness until2026 remain unestablished.','source_version_limits':['AJ2008 exact author body and AJ arXivv1 inspected, not asserted to be the final23-page2011 chapter.','Morpurgo author-web transformed-trace interfaces inspected; complete authenticated final2002 journal PDF not obtained or read.'],'not_addressed':['Comparison restricted to n>=4','Separate n>=4 monotonicity conjecture'],'execution_scope':'Three positive runs and five expected-failure controls. Independent exact recurrence/isqrt/Machin certificates support the separate written analytic proof; no finite grid is a universal bound.','source_version':'1.0.0','declared_date':'2026-10-13','actual_created_UTC':'2026-10-15T04:00:37.039113+00:00','publication_authority':False,'follow_up':None,'source_repair_or_narrow_replacement':False,'all203_programme_complete':False,'completion_percent_this_source_scope_subtask':100}
save(E/'verdict.json',verdict)
with (E/'RESEARCH_LOG.md').open('a') as f:f.write('* '+now()+' — Final whole-theorem/source-scope report and custom verdict completed. Actual primary interfaces and source-version/access limits, ten attack families, eight run receipts, original source bindings and preservation evidence are complete. No source repair or public authority supplied. Source100%; scope100%; no follow-up proposed; all203 ongoing.\n')
cache=[]
for root in [E/'cache',E/'tmp']:
 for p in sorted(root.rglob('*')):
  if p.is_file():cache.append({'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save(E/'CACHE_MANIFEST.json',{'utc':now(),'files':cache,'ignored_before_writing':True,'foreign_primary_bodies_and_full_text_kept_only_in_ignored_cache':True})
payload=[]
for p in sorted(E.rglob('*')):
 if p.is_file() and not any(x in ['cache','tmp'] for x in p.relative_to(E).parts):payload.append({'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save(E/'FINAL_MANIFEST.json',{'utc':now(),'status':'IMMUTABLE_SOURCE_SCOPE_EVIDENCE','files':payload,'source_binding_receipt':'SOURCE_BINDING_RECEIPT.json','cache_manifest':'CACHE_MANIFEST.json','preserve_immutable':True})
save(E/'FINAL_SEAL.json',{'utc':now(),'manifest_sha256':sha((E/'FINAL_MANIFEST.json').read_bytes()),'report_sha256':sha((E/'REPORT.md').read_bytes()),'verdict_sha256':sha((E/'verdict.json').read_bytes()),'owned_payload_files':len(payload),'source_final_manifest_sha256':sha((S/'SOURCE_FINAL_MANIFEST.json').read_bytes()),'source_final_seal_sha256':sha((S/'SOURCE_FINAL_SEAL.json').read_bytes()),'preserve_immutable':True,'publication_authority':False})
print(json.dumps({'report':binding(E/'REPORT.md'),'verdict':binding(E/'verdict.json'),'manifest':binding(E/'FINAL_MANIFEST.json'),'seal':binding(E/'FINAL_SEAL.json'),'source_manifest':binding(S/'SOURCE_FINAL_MANIFEST.json'),'source_seal':binding(S/'SOURCE_FINAL_SEAL.json'),'protected_prior_bindings':len(baseline['files']),'owned_payload_files':len(payload),'cache_files':len(cache)},indent=2))
