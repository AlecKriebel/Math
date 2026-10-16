"""Seal only this explicit review selection after checking actual receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,re
R=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise RuntimeError(s)
def read(n):return json.loads((R/n).read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
spec=importlib.util.spec_from_file_location('base',R/'base_review_checks.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
before=read('AUTHENTICATION.json')['snapshot']
need(before==b.authenticate(R.parent/'replay/revision_r1'),'final197 unchanged')
for n in ('CURRENT_normal.validated.json','CURRENT_optimized.validated.json','BUILD_optimized.validated.json'):
    v=read(n);need(v['status']=='PASS' and v['all197_unchanged'],'actual run receipt '+n)
need(read('ADDITIONAL_FINITE.json')['counts']['with_individual_net_difference']==9316,'finite distinction')
need(read('ADDITIONAL_CONTROLS.json')['all_controls_zero_archival_Popen_measured'],'CLI zero child')
need(len(read('PDF_RENDER_RECEIPT.json')['pages'])==6 and all(r['matches_existing_final'] for r in read('PDF_RENDER_RECEIPT.json')['pages']),'six actual PDF renders')
now=datetime.now(timezone.utc).isoformat()
decision={'timestamp_utc':now,'verdict':'CLEAR','scope':'Second new whole-package review on unchanged exact sealed core; no publication authorization.','current_manifest_sha256':b.MANIFEST_PIN,'portable_index_sha256':b.INDEX_PIN,'all197_and_core13_authenticated':True,'complete_original_target_supported':True,'fresh_source_origin':'local pinned Git subtree30/modes/blob, no fresh remote status','actual_current_normal':'PASS','actual_current_optimized':'PASS','actual_optimized_fresh_outside_build':'PASS','earlier_optimized_build_failure_cause':'UNESTABLISHED; preserved','authoritative_analytic_freeze':'Pre-exposure full message to parent after sampled04:53:41UTC; later capture is labeled; compact file draft05:01 is erroneous.','new_candidate_issues':[],'completion_estimate_percent':100,'original_effort':'5/5 unchanged'}
(R/'DECISION.json').write_text(json.dumps(decision,indent=2,sort_keys=True)+'\n')
with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Review100%, CLEAR on unchanged197/13core. Final independent authentication matches original snapshot. All actual run receipts and six render matches checked before sealing. Explicit safe selection below excludes scratch/primary bodies/corpora/renders/credentials and itself. No publication action authorized or taken.\n')
names=['SOURCE_FIRST_FREEZE.md','ANALYTIC_FREEZE.md','ANALYTIC_CAPTURE.md','RESEARCH_LOG.md','REPORT.md','DECISION.json','base_review_checks.py','supplemental.py','seal_review.py','AUTHENTICATION.json','RAW_CENTRAL.json','SOURCE_ORIGIN.json','PRIMARY_PINS.json','SOURCE_ONLY.stdout.json','SOURCE_ONLY.receipt.json','CURRENT_normal.stdout.json','CURRENT_normal.stderr.txt','CURRENT_normal.receipt.json','CURRENT_normal.validated.json','CURRENT_optimized.stdout.json','CURRENT_optimized.stderr.txt','CURRENT_optimized.receipt.json','CURRENT_optimized.validated.json','BUILD_optimized.stdout.json','BUILD_optimized.stderr.txt','BUILD_optimized.receipt.json','BUILD_optimized.validated.json','FINITE_CHECKS.json','ADDITIONAL_FINITE.json','ADDITIONAL_CONTROLS.json','PDF_RENDER_RECEIPT.json','SOURCE_VISUAL_RECEIPT.json','PRIOR_REVIEW_AUTHENTICATION.json']
rows=[]
for n in names:
    p=R/n;need(p.is_file() and not p.is_symlink(),'safe ordinary file')
    raw=p.read_bytes();text=raw.decode()
    patterns=(r'/(?:Users|home|private)/[A-Za-z0-9]',r'Bearer [A-Za-z0-9_.=-]{10,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9]{12,}')
    need(not any(re.search(s,text) for s in patterns),'safe contextual privacy scan '+n)
    rows.append({'path':n,**pin(raw)})
manifest={'schema':'pr885-whole-package-review02-safe-files-v1','verdict':'CLEAR','current_manifest_sha256':b.MANIFEST_PIN,'scope':'Explicit selection only; no recursive authority; hashes authenticate bytes, not proof.','files':rows,'excluded':['SAFE_FILES_MANIFEST.json itself','private_tmp in full','raw primary and corpus bodies','source extractions and rendered images','fresh outside ZIP scratch','unlisted files/credentials']}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(R/'SAFE_FILES_MANIFEST.json').write_bytes(raw)
print(json.dumps({'status':'PASS','safe_payload_count':len(rows),'safe_manifest':pin(raw),'report':pin((R/'REPORT.md').read_bytes()),'decision':pin((R/'DECISION.json').read_bytes())},sort_keys=True))
