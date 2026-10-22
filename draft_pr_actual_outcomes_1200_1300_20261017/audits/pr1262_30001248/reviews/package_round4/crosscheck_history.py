#!/usr/bin/env python3
"""Explicit current freeze coverage and immutable historical review-seal checks."""
import hashlib,json,pathlib,zipfile
H=pathlib.Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';PROGRAM=A.parents[1];REPO=PROGRAM.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,m):
    if not v:raise ValueError(m)
def binding(p):return dict(bytes=p.stat().st_size,sha256=sha(p))
freeze=json.loads((H/'INPUT_FREEZE.json').read_text());bound={}
for e in freeze['files']+freeze['external_readonly_inputs']:
    p=pathlib.Path(e['path']);p=p if p.is_absolute() else A/p
    need(str(p) not in bound,'duplicate input');bound[str(p)]=e
c=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text())
helpers=['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']
required={str(P/n) for n in helpers}
required|={str(P/n) for n in ['Triangle_Modular_Threshold_Note_v1.0.pdf','Triangle_Modular_Threshold_Verification_v1.0.zip','zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json']}
required|={str(A/n) for n in ['CURRENT_PR1262_CONTEXT.json','MATH_GATE.json','PRIORITY_ADJUDICATION.json','SUBMITTED_SNAPSHOT.json','DRAFT_REPAIR_BASELINE.json']}
required|={str(PROGRAM/'publication_coordinators'/n) for n in ['pr1262.py','repair_pr1262_draft.py','verify_pr1262_merge.py']}
required.add(str(REPO/'zenodo_deposit_tool/zenodo.py'))
required|={str(p) for folder in ['submitted','current_edition'] for p in (A/folder).iterdir()}
required|={str(A/e['path']) for e in c['portable_files']}
required|={str(p) for p in (P/'verification').rglob('*') if p.is_file()}
history=[]
for n in [1,2,3]:
    folder=A/'reviews'/('package_round'+str(n));auth=json.loads((A/('ROOT_PACKAGE_ROUND'+str(n)+'_AUTHENTICATION.json')).read_text())
    for key,name in [('report','REPORT.md'),('verdict','VERDICT.json'),('manifest','MANIFEST.json'),('input_freeze','INPUT_FREEZE.json')]:
        q=folder/name;need(sha(q)==auth[key+'_sha256'],'outside historical review anchor '+str(n)+' '+key);required.add(str(q))
    manifest=json.loads((folder/'MANIFEST.json').read_text())
    for e in manifest['authored_files']:
        need(not pathlib.PurePosixPath(e['path']).is_absolute() and '..' not in pathlib.PurePosixPath(e['path']).parts,'relative prior manifest')
        need(binding(folder/e['path'])=={k:e[k] for k in ['bytes','sha256']},'historical authored seal')
    v=json.loads((folder/'VERDICT.json').read_text());need(v['status']=='CLEAN' and v['actual_review'] is True,'prior literal verdict')
    history.append(dict(round=n,authored_members=len(manifest['authored_files']),report_sha256=sha(folder/'REPORT.md'),verdict_sha256=sha(folder/'VERDICT.json'),manifest_sha256=sha(folder/'MANIFEST.json'),input_freeze_sha256=sha(folder/'INPUT_FREEZE.json'),reviewed_context=v['current_context_sha256']))
need(required<=set(bound),'current freeze missing '+repr(required-set(bound)))
query_a=json.loads((A/'reviews/priority_triangle/QUERY_LEDGER.json').read_text());query_b=json.loads((A/'reviews/priority_modular/QUERY_LEDGER.json').read_text());query_root=json.loads((A/'ROOT_PRIORITY_QUERY_LEDGER.json').read_text())
counts=[sum(len(x['literal_queries']) for x in query_a['batches']),len(query_b['queries']),len(query_root['queries'])];need(counts==[56,52,12],'query counts')
pin=json.loads((A/'reviews/priority_modular_cross_triangle/AUTHENTICATION.json').read_text());need(len(pin['source_pins'])==16,'16 pins')
z=P/'Triangle_Modular_Threshold_Verification_v1.0.zip'
with zipfile.ZipFile(z) as archive:
    need(archive.testzip() is None,'CRC');need(all((i.external_attr>>16)&0o170000!=0o120000 for i in archive.infolist()),'zip symlink')
old=json.loads((A/'release_history/pre_html_escape_20261017/CURRENT_PR1262_CONTEXT.json').read_text())
delta={k:dict(before=old[k],after=c[k]) for k in c if old[k]!=c[k]}
summary=dict(status='PASS',required_current_lexical_paths=len(required),all_required_paths_present_exactly=True,previous_review_seals=history,prior_context_is_historical=True,query_ledger_recount=counts,literal_queries_total=sum(counts),source_pin_count=16,archive_CRC_and_no_symlink=True,context_changed_top_level_keys=list(delta),current_registry_count=len(c['authored_freezes']),prior_registry_count=len(old['authored_freezes']),new_helper_and_baseline_explicitly_frozen=True)
(H/'HISTORY_CROSSCHECK.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
