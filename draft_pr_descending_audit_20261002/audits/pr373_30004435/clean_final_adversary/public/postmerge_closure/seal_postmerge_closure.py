#!/usr/bin/env python3
"""Immutable-object postmerge verification; never reruns an open-PR gate."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
P=Path(__file__).resolve().parent.parent;A=P.parent;ROOT=Path('/Users/alec/Documents/Math')
O=P/'public/postmerge_closure';assert not O.exists();O.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_bytes())
def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT)
root_receipt=A/'ACTUAL_MERGE_VERIFICATION.json';rootcmp=A/'root_clean_live_comparison_receipt.json'
r=read(root_receipt);c=read(rootcmp);v=read(P/'live_acceptance_v2_run1/VERDICT.json')
merge='c9aac76208a57069d2c66f6a05583195a34eba86';base='ef789480d00794adeb841310218b2979bac57caa';head='07f83847edc7b91201c3a71fa8ca694b5172bd6d';tree='1278c533cb2e68aec138db0ef328162025edf7eb'
assert r['actual_merge']==merge and r['reviewed_head']==head and r['actual_parents']==[base,head]
assert git('show','-s','--format=%P',merge).decode().strip().split()==[base,head]
assert git('rev-parse',merge+'^{tree}').decode().strip()==git('rev-parse',head+'^{tree}').decode().strip()==tree
S=A/'repaired_snapshot';paths=sorted(str(f.relative_to(S)) for f in S.rglob('*') if f.is_file())
assert len(paths)==53 and git('diff','--name-only',base,merge).decode().splitlines()==paths
bindings=[]
for f in paths:
 b=git('show',merge+':'+f);assert b==(S/f).read_bytes();bindings.append({'path':f,'bytes':len(b),'sha256':sha(b)})
q='unsolved_math_prioritization/QUEUE.md';bq=git('show',base+':'+q);mq=git('show',merge+':'+q)
old=r['base_row'].encode();new=r['accepted_row'].encode();assert bq.count(old)==1 and mq==bq.replace(old,new)
assert sha(bq)==r['base_queue_sha256'] and sha(mq)==r['accepted_queue_sha256']
assert mq.decode().splitlines()[408]==new.decode().rstrip('\n')
def tm(ref):return {p.split('\t',1)[1]:p.split('\t',1)[0] for p in git('ls-tree','-r',ref).decode().splitlines()}
allowed=set(paths);bt=tm(base);mt=tm(merge)
assert {k:x for k,x in bt.items() if k not in allowed}=={k:x for k,x in mt.items() if k not in allowed}
# Root's whole-stream comparison receipt is checked against our exact complete generated streams.
assert c['agent_fullverdict_sha256']==sha((P/'live_acceptance_v2_run1/VERDICT.json').read_bytes())
assert c['whole_verdict_matches_except_only_at_utc_and_finished_at_utc'] is True
assert len(c['complete_program_streams'])==8 and c['all_1225_material_checks_pass'] is True
stream_metadata=[]
for row in c['complete_program_streams']:
 label=row['label'];b=(P/'live_acceptance_v2_run1/streams'/(label+'.stdout')).read_bytes();err=(P/'live_acceptance_v2_run1/private'/(label+'.stderr')).read_bytes()
 assert len(b)==row['stdout_bytes'] and sha(b)==row['stdout_sha256'] and row['complete_stdout_stderr_exact'] is True and err==b''
 stream_metadata.append({'label':label,'stdout_bytes':len(b),'stdout_sha256':sha(b),'stderr_bytes':len(err),'stderr_sha256':sha(err),'root_complete_stdout_stderr_match_recorded':True})
# Read the actual immutable remote merge object, keeping its raw API body private.
private=P/'postmerge_private';private.mkdir()
api=subprocess.check_output(['gh','api','repos/AlecKriebel/Math/git/commits/'+merge],cwd=ROOT);(private/'actual_merge_commit_api.json').write_bytes(api);j=json.loads(api)
assert j['sha']==merge and j['tree']['sha']==tree and [x['sha'] for x in j['parents']]==[base,head]
preserve=read(P/'GATE_V2_SEAL.json')['original_preservation']
for f,h in preserve.items():assert sha((P/f).read_bytes())==h
prior_files=['public/ADDITIVE_GATE_V2_ALLOWLIST_MANIFEST.json','public/live_acceptance_v2/ADDITIVE_FINAL_ALLOWLIST_MANIFEST.json','public/live_acceptance_v2/FINAL_LIVE_SEAL.json','public/live_acceptance_v2/FINAL_LIVE_REVIEW.md','code/read_only_acceptance_gate_v2.py']
prior={f:sha((P/f).read_bytes()) for f in prior_files};at=datetime.now(timezone.utc).isoformat()
evidence={'at_utc':at,'status':'PASS_ACTUAL_MERGE_OF_SCOPED_UNSOLVED_5_OF_5','actual_merge':merge,'root_recorded_merged_at':r['merged_at'],'actual_parents':[base,head],'actual_complete_root_tree':tree,'actual_remote_immutable_commit_verified':True,'actual_remote_commit_api_sha256':sha(api),'root_actual_merge_receipt_sha256':sha(root_receipt.read_bytes()),'root_complete_stream_comparison_receipt_sha256':sha(rootcmp.read_bytes()),'premerge_observed_from_utc':v['at_utc'],'premerge_observed_through_utc':v['finished_at_utc'],'premerge_check_count':len(v['checks']),'premerge_verdict_sha256':sha((P/'live_acceptance_v2_run1/VERDICT.json').read_bytes()),'complete_53_actual_merge_file_bindings':bindings,'all_52_original_target_files_preserved':True,'literal_whole_queue_own_line409_cells8_9_only':True,'all_other_actual_tree_path_mode_type_blob_preserved':True,'complete_generated_stream_comparison':stream_metadata,'open_pr_gate_rerun_after_merge':False,'review_completion_percent':100,'unrestricted_discovery_percent':0,'original_source_math_publicmanifest_negative_gate_preserved':preserve,'prior_additive_certificates_preserved':prior,'scope':'Actual immutable merge/tree verified; original probability-only method request remains unresolved. No novelty/external peer review/formal proof/full-resolution claim. Raw assets/API/Git bodies remain private.'}
(O/'POSTMERGE_VERIFICATION.json').write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
report=f'''# Postmerge closure for the independently reviewed PR373 partial packet\n\n**PASS: actual merge `{merge}` matches the exact premerge-reviewed packet.** The accepted research disposition remains **unsolved5/5** for the unrestricted probability-only method request.\n\nThe immutable premerge live gate ran from {v['at_utc']} to {v['finished_at_utc']} with1225 checks passing. Its whole nested verdict matched the root's independently reproduced verdict except only the declared `at_utc` and `finished_at_utc` observations; all eight complete program stdout/stderr comparisons were recorded and their stdout lengths/hashes independently checked. The exact live body has no scope concern: subclass premises, classical credit, proof/control distinction and unresolved unrestricted gap are explicit.\n\nThe root's actual merge receipt records completion at {r['merged_at']}. Independently read local and remote immutable commit objects confirm merge parents `{base}` and `{head}`, and complete tree `{tree}`, equal to the accepted head's complete tree. Every53 changed path matches the reviewed repaired snapshot; all52 original mathematical/review/publication file bytes are preserved. The complete queue changes only the target's line409 cells8/9, queued/0/5 to unsolved/5/5. Every other queue byte and every other path/mode/type/blob is unchanged relative to the current-main parent.\n\nRoot actual receipt SHA256: `{evidence['root_actual_merge_receipt_sha256']}`. Root complete-stream comparison receipt SHA256: `{evidence['root_complete_stream_comparison_receipt_sha256']}`. Full independently computed actual merge bindings are retained in POSTMERGE_VERIFICATION.json.\n\nThe original source/math seals, historical negative gate, initial public manifest, v2 additive manifest and premerge final certificate remain unchanged. No open-PR gate was rerun after merge. This separate additive closure publishes only own report/code/metadata. Raw API/Git bodies, source PDFs/extracts/renders and authorpacket copies remain private.\n\nReview-goal completion100%; unrestricted-discovery completion0%. Strongest verified result: the stated scoped probability-only partials and their reproducible actual merged package. Exact remaining mathematical gap: the entropy-free proof for all stationary finite-alphabet processes remains absent. No novelty, external human peer review, formal proof-assistant certification, preprint, Zenodo, DOI, tracker row or release is claimed.\n'''
(O/'FINAL_POSTMERGE_REVIEW.md').write_text(report)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+at+' — Checkpoint6: actual merge c9aac762 independently verified by immutable local/remote commit/tree and every53path/fullqueue/allotherpath. Premerge certificate preserved; no postmerge openPRgate rerun. Review completion100%, unrestricted discovery0%. Exact unresolved mathematical gap unchanged.\n')
shutil.copyfile(P/'RESEARCH_LOG.md',O/'POSTMERGE_RESEARCH_LOG.md');shutil.copyfile(Path(__file__),O/'seal_postmerge_closure.py')
files=[{'path':str(f.relative_to(O)),'bytes':len(f.read_bytes()),'sha256':sha(f.read_bytes())} for f in sorted(O.rglob('*')) if f.is_file()]
seal={'at_utc':at,'status':evidence['status'],'files':files,'premerge_immutable_certificate_and_initial_public_manifest_unchanged':True,'actual_merge':merge,'source_math_negative_preservation':preserve,'prior_additive_preservation':prior}
(O/'POSTMERGE_SEAL.json').write_text(json.dumps(seal,indent=2,sort_keys=True)+'\n');files.append({'path':'POSTMERGE_SEAL.json','bytes':len((O/'POSTMERGE_SEAL.json').read_bytes()),'sha256':sha((O/'POSTMERGE_SEAL.json').read_bytes())})
allow={'at_utc':at,'status':evidence['status'],'policy':'Separate explicit additive postmerge allowlist. Publish only these five own report/code/metadata files and this manifest, alongside the separately sealed prior public manifests.','files':files,'exclude':'Raw Git/API bodies, primary PDFs/extracts/renders, authorpacket, private clones, unlisted files.','prior_manifests_unchanged':True}
(O/'ADDITIVE_POSTMERGE_ALLOWLIST_MANIFEST.json').write_text(json.dumps(allow,indent=2,sort_keys=True)+'\n')
for f,h in preserve.items():assert sha((P/f).read_bytes())==h
for f,h in prior.items():assert sha((P/f).read_bytes())==h
for row in files:assert sha((O/row['path']).read_bytes())==row['sha256']
print(json.dumps({'status':evidence['status'],'at_utc':at,'actual_merge':merge,'report':str(O/'FINAL_POSTMERGE_REVIEW.md'),'manifest':str(O/'ADDITIVE_POSTMERGE_ALLOWLIST_MANIFEST.json'),'listed_files':len(files),'premerge_final_manifest_sha256':prior['public/live_acceptance_v2/ADDITIVE_FINAL_ALLOWLIST_MANIFEST.json'],'postmerge_manifest_sha256':sha((O/'ADDITIVE_POSTMERGE_ALLOWLIST_MANIFEST.json').read_bytes()),'root_actual_merge_receipt_sha256':evidence['root_actual_merge_receipt_sha256'],'open_pr_gate_rerun_after_merge':False},indent=2))
