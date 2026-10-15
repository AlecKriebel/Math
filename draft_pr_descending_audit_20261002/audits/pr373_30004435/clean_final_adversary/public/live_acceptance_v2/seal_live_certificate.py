#!/usr/bin/env python3
"""Seal exact observed PR373 live PASS without modifying repo/API/old evidence."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,subprocess,sys,os
P=Path(__file__).resolve().parent.parent;A=P.parent;R=P/'live_acceptance_v2_run1';O=P/'public/live_acceptance_v2'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
assert not O.exists();O.mkdir()
v=read(R/'VERDICT.json');root=read(A/'root_clean_live_full_verdict.json');receipt=read(A/'root_clean_live_reproduction_receipt.json')
ex=['at_utc','finished_at_utc'];assert set(v)==set(root)
assert {k:x for k,x in v.items() if k not in ex}=={k:x for k,x in root.items() if k not in ex}
assert v['status']=='PASS_LIVE_SCOPED_UNSOLVED_5_OF_5' and len(v['checks'])==1225
assert sha((P/'code/read_only_acceptance_gate_v2.py').read_bytes())==v['gate_code_sha256']=='73eaa51a1a95c7f78a09f98099657cbf531fddae596536f6954fa7a4f9adab52'
assert receipt['complete_full_verdict_sha256']==sha((A/'root_clean_live_full_verdict.json').read_bytes())
assert receipt['exact_head']==v['expected_head']=='07f83847edc7b91201c3a71fa8ca694b5172bd6d'
assert receipt['exact_main']==v['expected_main']=='ef789480d00794adeb841310218b2979bac57caa'
assert receipt['body_sha256']==v['prepared_body_sha256'] and receipt['all_checks']==1225
# Preserve all prior evidence exactly and prove the target/metadata input inventory anew.
preserve=read(P/'GATE_V2_SEAL.json')['original_preservation']
for f,h in preserve.items():assert sha((P/f).read_bytes())==h
prior=['public/ADDITIVE_GATE_V2_ALLOWLIST_MANIFEST.json','GATE_V2_SEAL.json','code/read_only_acceptance_gate_v2.py']
prior_binding={f:sha((P/f).read_bytes()) for f in prior}
S=A/'repaired_snapshot';manifest=read(A/'repaired_snapshot_manifest.json');paths=sorted(str(f.relative_to(S)) for f in S.rglob('*') if f.is_file())
assert sorted(r['path'] for r in manifest['files'])==paths and len(paths)==53
for row in manifest['files']:
 b=(S/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
assert sha((A/'accepted_pr_body.txt').read_bytes())==v['prepared_body_sha256']
for f in paths:
 if f.startswith('unsolved_math_prioritization/attempts/30004435/'):
  assert (S/f).read_bytes()==(A/'snapshot'/f).read_bytes()
# The gate already reread actual Git/API before and after all checks. The immutable API commits are preserved privately.
start=read(R/'private/pr_start.json');end=read(R/'private/pr_end.json');tm=read(R/'private/test_merge.json');tme=read(R/'private/test_merge_end.json')
assert start['draft'] is False and end['draft'] is False and start['mergeable'] is True and end['mergeable'] is True
assert start['mergeable_state']==end['mergeable_state']=='clean'
assert start['merge_commit_sha']==end['merge_commit_sha']==tm['sha']==tme['sha']=='d907806d69fcafbfc4af4aaf74aae557e5be7648'
assert tm['tree']['sha']==tme['tree']['sha']=='1278c533cb2e68aec138db0ef328162025edf7eb'
at=datetime.now(timezone.utc).isoformat()
comparison={'at_utc':at,'status':'PASS_COMPLETE_NESTED_VERDICT_COMPARISON','our_verdict_sha256':sha((R/'VERDICT.json').read_bytes()),'root_verdict_sha256':sha((A/'root_clean_live_full_verdict.json').read_bytes()),'root_reproduction_receipt_sha256':sha((A/'root_clean_live_reproduction_receipt.json').read_bytes()),'only_excluded_observational_fields':ex,'all_other_nested_fields_exactly_equal':True,'our_at_utc':v['at_utc'],'our_finished_at_utc':v['finished_at_utc'],'root_at_utc':root['at_utc'],'root_finished_at_utc':root['finished_at_utc'],'check_count':1225,'scope':'No output/count/source/binding/check normalization; exact equality apart from the two declared UTC observations.'}
(O/'FULL_VERDICT_COMPARISON.json').write_text(json.dumps(comparison,indent=2,sort_keys=True)+'\n')
inputs={'at_utc':at,'head':v['expected_head'],'current_main':v['expected_main'],'testmerge':tm['sha'],'complete_testmerge_head_root_tree':tm['tree']['sha'],'body_sha256':v['prepared_body_sha256'],'repaired_snapshot_manifest_sha256':sha((A/'repaired_snapshot_manifest.json').read_bytes()),'queue_repair_receipt_sha256':sha((A/'queue_repair_receipt.json').read_bytes()),'all_53_snapshot_entries_revalidated':True,'all_52_original_targetfiles_byte_identical':True,'full_queue_candidate_sha256':sha((S/'unsolved_math_prioritization/QUEUE.md').read_bytes()),'public_raw_source_count':0,'source_and_math_independence_preserved':True,'preserved_original_bindings':preserve,'preserved_additive_v2_bindings':prior_binding}
(O/'ACTUAL_INPUT_BINDINGS.json').write_text(json.dumps(inputs,indent=2,sort_keys=True)+'\n')
shutil.copyfile(R/'VERDICT.json',O/'COMPLETE_LIVE_GATE_VERDICT.json')
streams=O/'streams';streams.mkdir()
for f in sorted((R/'streams').glob('*.stdout')):shutil.copyfile(f,streams/f.name)
assert len(list(streams.glob('*.stdout')))==8
# Reproduce the two independently written mathematical control streams wholly, with no author imports.
for name in ['original_controls','original_wordspan_adversary']:
 r=subprocess.run([sys.executable,str(P/'code'/(name+'.py'))],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 assert r.returncode==0 and not r.stderr and r.stdout==(P/'replays'/(name+'.json')).read_bytes()
 (streams/(name+'.stdout')).write_bytes(r.stdout)
report=f'''# Final exact live review certificate for PR373\n\n**PASS for live acceptance of the scoped unsolved5/5 packet. No review blocker remains for the exact observed objects.** The unrestricted probability-only method request remains unresolved. This certificate does not claim a new general identity, novelty, external human peer review, formal proof-assistant verification, or a completed merge.\n\nThe source-first baseline was sealed before candidate mathematics, and the five-turn mathematical verdict before author code/receipts/prior review/metadata. Both seals are unchanged. The quantified Markov, hidden Markov, uniform-coupling, locally decisive finite-mean coding and conditional-law mixture results pass with their assumptions and exact general gap preserved. The exact prepared live body was read in full and keeps those boundaries explicit.\n\nThe immutable gatev2 ({v['gate_code_sha256']}) ran from {v['at_utc']} to {v['finished_at_utc']} against actual head `{v['expected_head']}`, current main `{v['expected_main']}`, and body SHA256 `{v['prepared_body_sha256']}`. All1225 checks passed. The PR was ready/draftfalse, open/unmerged, mergeabletrue and CLEAN initially and late. Actual testmerge `{tm['sha']}` retained parents currentmain/head and complete root tree `{tm['tree']['sha']}`, exactly the expectedhead root tree. Head/base/main/body/mergeability/testmergeidentity stayed stable throughout the gate.\n\nThe complete actual diff and API inventory contain53 paths:52 original target files and QUEUE. Every original target byte is unchanged. The entire queue equals currentmain's entire queue with only target line409 cells8/9 changing queued/0/5 to unsolved/5/5; every other queue byte and every other complete-tree path/mode/type/blob is preserved. All original42author+7review frozen files,166 historical/final author bindings,51 publication bindings,6 review-manifest bindings and42 author Gitblob bindings pass. The supplied repaired snapshot manifest was independently revalidated against all53 actual files.\n\nAll five complete generated author streams reproduce byte for byte with per-turn counts5527,25404,25455,123026,31562, totaling210974. The complete old independent review stream reproduces9334 controls, and both wrappers' complete outputs agree exactly. Four primary sources were fetched anew separately and their exact lengths/hashes verified. The two own original mathematical control programs were rerun and both whole streams agree with their independently sealed outputs. Finite checks supplement the written infinite-probability arguments.\n\nThe root independently ran the same sealed gate on its private copied inputs. The complete nested verdicts agree exactly after excluding only `at_utc` and `finished_at_utc`, the two explicitly declared observational UTC fields. No assertion count, source count, manifest entry, tree binding, body, output, status or other field was normalized. Our complete verdict SHA256 is `{comparison['our_verdict_sha256']}`; root complete verdict SHA256 is `{comparison['root_verdict_sha256']}`.\n\nThe original negative stale-base run, original gate, initial publication allowlist, additivev2 allowlist and source/math seals remain intact. This final additive allowlist exports only own report/code/complete generated mathematical streams/metadata. Raw source PDFs/extracts/renders, raw Git/API responses, private clones, and copied author packets remain private.\n\nReview-goal completion estimate100%; unrestricted-discovery completion estimate0% for this packet. Exact strongest result: the stated scoped probability-only results and their complete live reproducibility/binding certificate. Exact remaining mathematical gap: prove the known completed left/right tail identity for every stationary finite-alphabet process without entropy or unsupported subclass reduction. Actual merge and any subsequent state reconciliation remain the root operator's work.\n'''
(O/'FINAL_LIVE_REVIEW.md').write_text(report)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+at+' — Checkpoint5: actual immutablev2 live PASS1225checks; complete root verdict comparison exact apart from at_utc/finished_at_utc only. Review completion estimate100%; unrestricted discovery estimate0%. Exact head07f83847/currentmain ef789480/body ae06ab90/testmerge d907806d/root tree1278c533 bound. No review blocker; actual merge not claimed. Original seals/negative/initialpublicMF remain unchanged.\n')
shutil.copyfile(P/'RESEARCH_LOG.md',O/'FINAL_RESEARCH_LOG.md')
shutil.copyfile(Path(__file__),O/'seal_live_certificate.py')
files=[]
for f in sorted(O.rglob('*')):
 if f.is_file():files.append({'path':str(f.relative_to(O)),'bytes':len(f.read_bytes()),'sha256':sha(f.read_bytes())})
seal={'at_utc':at,'status':'PASS_LIVE_SCOPED_UNSOLVED_5_OF_5','review_completion_percent':100,'unrestricted_discovery_percent':0,'files':files,'original_preservation':preserve,'additive_v2_preservation':prior_binding,'source_math_seals_unchanged':True,'actual_merge_claimed':False,'remaining_gap':'Unrestricted probability-only theorem method unresolved; actual merge remains operator work.'}
(O/'FINAL_LIVE_SEAL.json').write_text(json.dumps(seal,indent=2,sort_keys=True)+'\n')
files.append({'path':'FINAL_LIVE_SEAL.json','bytes':len((O/'FINAL_LIVE_SEAL.json').read_bytes()),'sha256':sha((O/'FINAL_LIVE_SEAL.json').read_bytes())})
allow={'at_utc':at,'status':seal['status'],'policy':'Separate additive immutable final allowlist. Publish only the listed own report/code/full generated mathematical streams/metadata and this manifest. Initial PUBLIC_ALLOWLIST_MANIFEST.json and ADDITIVE_GATE_V2_ALLOWLIST_MANIFEST.json remain unchanged.','exclude':'private raw source PDFs/extracts/renders/Git/API, private clones, authorpacket, arbitrary unlisted files and raw root reports','files':files,'actual_merge_claimed':False}
(O/'ADDITIVE_FINAL_ALLOWLIST_MANIFEST.json').write_text(json.dumps(allow,indent=2,sort_keys=True)+'\n')
for row in files:assert len((O/row['path']).read_bytes())==row['bytes'] and sha((O/row['path']).read_bytes())==row['sha256']
for f,h in preserve.items():assert sha((P/f).read_bytes())==h
for f,h in prior_binding.items():assert sha((P/f).read_bytes())==h
print(json.dumps({'status':seal['status'],'seal_at_utc':at,'full_gate_checks':1225,'complete_verdict_sha256':comparison['our_verdict_sha256'],'root_complete_verdict_sha256':comparison['root_verdict_sha256'],'only_excluded_fields':ex,'all_other_nested_fields_equal':True,'published_allowlisted_file_count':len(files),'full_generated_streams':10,'final_report':str(O/'FINAL_LIVE_REVIEW.md'),'final_manifest':str(O/'ADDITIVE_FINAL_ALLOWLIST_MANIFEST.json')},indent=2))
