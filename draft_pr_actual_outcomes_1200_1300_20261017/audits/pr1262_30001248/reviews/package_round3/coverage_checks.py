from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';REPO=A.parents[2]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,msg):
 if not x:raise RuntimeError(msg)
C=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text());F=json.loads((R/'INPUT_FREEZE.json').read_text());frozen={str((Path(e['path']) if Path(e['path']).is_absolute() else A/e['path']).absolute()):e for e in F['files']+F['external_readonly_inputs']}
workflow={'prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py'}
required={str((P/n).absolute()) for n in workflow}|{str((P/n).absolute()) for n in ['Triangle_Modular_Threshold_Note_v1.0.pdf','Triangle_Modular_Threshold_Verification_v1.0.zip','zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json']}
required|={str((A/n).absolute()) for n in ['CURRENT_PR1262_CONTEXT.json','MATH_GATE.json','PRIORITY_ADJUDICATION.json','SUBMITTED_SNAPSHOT.json']}
required|={str((REPO/'zenodo_deposit_tool/zenodo.py').absolute()),str((REPO/'draft_pr_actual_outcomes_1200_1300_20261017/publication_coordinators/pr1262.py').absolute())}
names={'ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json'}
required|={str((A/folder/n).absolute()) for folder in ['submitted','current_edition'] for n in names}
required|={str((A/e['path']).absolute()) for e in C['portable_files']}
required|={str(p.absolute()) for p in (P/'verification').rglob('*') if p.is_file()}
prior=[]
for label in ['package_round1','package_round2']:
 family=A/'reviews'/label;M=json.loads((family/'MANIFEST.json').read_text())
 for e in M['authored_files']:
  need(not Path(e['path']).is_absolute() and '..' not in Path(e['path']).parts,'review manifest unsafe');p=family/e['path'];need(p.stat().st_size==e['bytes'] and h(p)==e['sha256'],'review authored seal mismatch')
 old=json.loads((family/'INPUT_FREEZE.json').read_text());common=0;changed=[];renames=[]
 for e in old['files']+old['external_readonly_inputs']:
  raw=e['path'];p=Path(raw) if Path(raw).is_absolute() else A/raw;key=str(p.absolute())
  if key not in frozen and raw=='reviews/reconstruction_adversary/manifest.json':
   key=str((A/'reviews/reconstruction_adversary/MANIFEST.json').absolute());renames.append({'old':raw,'new':'reviews/reconstruction_adversary/MANIFEST.json'})
  if key in frozen:
   common+=1
   if (e['bytes'],e['sha256'])!=(frozen[key]['bytes'],frozen[key]['sha256']):changed.append(raw)
 need(not changed,'prior common byte drift')
 for n in ['REPORT.md','VERDICT.json','MANIFEST.json','INPUT_FREEZE.json']:required.add(str((family/n).absolute()))
 prior.append({'family':label,'authored_members_authenticated':len(M['authored_files']),'shared_inputs_same_bytes':common,'historical_lexical_rename':renames,'changed_common_bytes':changed,'status':json.loads((family/'VERDICT.json').read_text())['status']})
missing=sorted(required-set(frozen));need(not missing,'omitted operative lexical paths '+repr(missing));need(len(required)==403,'required count changed')
# Exact historical wrapping, unchanged AUDIT and sole explicit PROOF insertion.
for n in ['ACCEPTANCE.json','SOURCES.json','VERIFICATION.json']:
 cur=json.loads((A/'current_edition'/n).read_text());old=json.loads((A/'submitted'/n).read_text());need(cur['historical_submitted_record_20261011']==old,'historical wrapper changed')
old=(A/'submitted/AUDIT.md').read_text();cur=(A/'current_edition/AUDIT.md').read_text();need(cur.endswith(old),'historical AUDIT changed')
old=(A/'submitted/PROOF.md').read_text();cur=(A/'current_edition/PROOF.md').read_text();insert='Current clarification: this nondegenerate ordinary 2K2 conditional reconstruction is for n>=4; triangle normalization elsewhere starts at n>=3.\n\n';need(cur.replace(insert,'').endswith(old),'PROOF hidden body change')
# Recount query ledgers and detached source-pin clerical correction.
a=json.loads((A/'reviews/priority_triangle/QUERY_LEDGER.json').read_text());b=json.loads((A/'reviews/priority_modular/QUERY_LEDGER.json').read_text());root=json.loads((A/'ROOT_PRIORITY_QUERY_LEDGER.json').read_text());counta=sum(len(x['literal_queries']) for x in a['batches']);need(counta==56 and len(b['queries'])==52 and len(root['queries'])==12,'query recount')
pins=json.loads((A/'reviews/priority_modular_cross_triangle/AUTHENTICATION.json').read_text())['source_pins'];need(len(pins)==16,'detached count')
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','required_operative_artifact_registry_prior_review_paths':len(required),'all403_exact_lexical_paths_covered':True,'required_paths':sorted(required),'prior_reviews':prior,'v3_historical_wrappers_exact':True,'historical_AUDIT_unchanged':True,'historical_PROOF_only_explicit_n4_insertion':True,'literal_query_counts':{'A':counta,'B':len(b['queries']),'root':len(root['queries']),'sum':120,'A_separate_Crossref_queries':len(a['other_searches'])},'detached_source_pin_count':16,'limits':'Recounts and immutable evidence cross-checks, not a new search, a reconstruction of transport requests or a priority certificate. Earlier clean review payloads retained; earlier lexical freeze omissions corrected only by new current freeze.'}
(R/'COVERAGE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='required_paths'}))
