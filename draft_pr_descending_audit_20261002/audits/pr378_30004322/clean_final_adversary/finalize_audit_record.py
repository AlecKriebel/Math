"""One-time own-evidence finalization, preserving the pending-stage record.

No candidate, index, Git/ref, remote or service mutations are performed.
"""
from pathlib import Path
import hashlib,json,datetime,subprocess
D=Path(__file__).resolve().parent
R=Path('/Users/alec/Documents/Math')
def sha(b):return hashlib.sha256(b).hexdigest()
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
oldraw=(D/'FINAL_AUDIT_MANIFEST.json').read_bytes();old=json.loads(oldraw)
assert sha(oldraw)=='7ae10a1c01e46b7c0326430bd561b2d81ddcfa7243197aae96d1b5f2fbe4456c'
assert len(old['files'])==46
for e in old['files']:
    b=(D/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
gate=json.loads((D/'final_repaired_package_gate.json').read_text())
inc=json.loads((D/'incidence_label_reproducibility.json').read_text())
assert gate['status']=='PASS_SCOPED_FINAL_REPAIRED_PACKAGE' and inc['status']=='PASS'
assert subprocess.check_output(['git','rev-parse','main'],cwd=R).decode().strip()==gate['actual_main']
assert not (D/'pending_head_record').exists()
(D/'pending_head_record').mkdir()
mutable=['audit_report.md','post_seal_corrections.md','post_seal_research_log.md']
for p in mutable:
    (D/'pending_head_record'/p).write_bytes((D/p).read_bytes())
(D/'pending_head_record/FINAL_AUDIT_MANIFEST.json').write_bytes(oldraw)
preserve={'utc':utc,'pending_manifest_sha256':sha(oldraw),'pending_file_count':46,
          'qualification':'Historical pending-stage manifest is preserved byte-exact. Its three subsequently updated files are resolved via preserved_path_map; all remaining paths retain their historical bytes in the current dedicated folder.',
          'preserved_path_map':{p:'pending_head_record/'+p for p in mutable}}
for e in old['files']:
    target=D/preserve['preserved_path_map'].get(e['path'],e['path'])
    assert len(target.read_bytes())==e['bytes'] and sha(target.read_bytes())==e['sha256']
(D/'pending_head_evidence_preservation.json').write_text(json.dumps(preserve,sort_keys=True,indent=2)+'\n')

seals=[];ignored=[]
for line in (D/'initial_seal_sha256.txt').read_text().splitlines():
    digest,p=line.split('  ',1)
    b=(D/p).read_bytes();assert sha(b)==digest
    seals.append({'path':p,'bytes':len(b),'sha256':digest})
    if p.startswith('primary/'):
        rel=str((D/p).relative_to(R))
        result=subprocess.run(['git','check-ignore','--',rel],cwd=R,capture_output=True)
        assert result.returncode==0 and result.stdout.decode().strip()==rel
        ignored.append(p)
assert len(seals)==11
(D/'final_initial_seal_readback.json').write_text(json.dumps({'utc':utc,'status':'PASS','initial_seal_instances':11,'all_initial_instances_unchanged':True,'files':seals,'raw_primary_instances_confirmed_git_ignored':ignored,'no_raw_sources_in_candidate_packet':True},sort_keys=True,indent=2)+'\n')

with (D/'post_seal_corrections.md').open('a') as f:
    f.write('\n## Final reporting qualification ('+utc+')\n\nThe interim compact chat summary labeled 214,070 and 93,918 as stream byte lengths. They are assertion counts. The five exact author JSON stdout streams total 1,855 bytes; the old independent JSON stdout is 2,348 bytes. All full streams remain preserved and byte-exact to the recorded receipts. The detailed new incidence JSON files are reproducible up to the unique permutation of the three unordered coordinate vertices, rather than byte-exact across Python hash seeds; their summary stdout is byte-exact. No sealed initial derivation, control code or original detailed incidence file was rewritten.\n')
with (D/'post_seal_research_log.md').open('a') as f:
    f.write('\n- '+utc+': Final exact head/base/ancestry/whole-queue and live read-only GitHub metadata gate PASS; audit completion 100%, original problem remains unsolved 5/5 and resolution estimate 0%. Repaired head `'+gate['repaired_head']+'` has exact original/main parents and tree, all 46 mathematical files unchanged, all 47 repaired freeze entries matching Git, all prior mathematical receipts/manifests bound directly to repaired head, and no extra packet/raw-source files. Queue physical line 413, displayed rank 402: only raw pipe cells 8/9 changed queued/0/5 to unsolved/5/5; every other queue byte and prior outcome preserved. Actual PR379 merge is an ancestor of fixed main `'+gate['actual_main']+'`. All eleven initial-seal instances rechecked unchanged; raw primary inputs remain Git-ignored.\n')
    f.write('- '+utc+': Independently read and reconciled all 51/921/17,775 detailed q1/q2/q4 support/class/dual-load records and every representative pair. Full JSON equivalence is under the unique three-vertex relabeling; summary stdout is byte-exact. My first reconciliation script used the opposite mapping convention from the root receipt; its failed script/stdout/stderr are preserved, then the convention was explicitly inverted. All underlying full records had already matched. This was an evidence-harness assumption, not a candidate defect. Original control code and original incidence data remain untouched. The interim chat assertion-count/byte-count label is corrected additively. Read-only Git status exposed unrelated pathnames after the initial seal; no unrelated contents were read. No candidate/index/Git/remote/service/paper/DOI mutation or external-individual communication occurred.\n')

report=(D/'audit_report.md').read_text()
before='Provisional mathematical verdict: **PASS scoped, original unresolved 5/5** at frozen original head `5da73632ab7a621de7b62edb5f70dfb8017e4a50`. No mandatory mathematical repair found. The repaired-head and actual-main queue acceptance gate is pending; this report is not yet a final merge approval. Overall audit completion: 90%.'
after='Final whole-package verdict: **PASS scoped, original unresolved 5/5** at repaired head `'+gate['repaired_head']+'`, against actual main `'+gate['actual_main']+'`. All mathematical and exact repaired-head/queue audit gates pass; no mandatory repair found. This is acceptance of the partial research packet within its stated assumptions, with no claim that the original conjecture is solved. Overall audit completion: 100%; original-problem resolution estimate: 0%.'
assert before in report;report=report.replace(before,after,1)
report=report.replace('Full incidence records are retained. It deliberately rejects', 'Full incidence records are retained. Their reproduction across Python hash seeds is exact after the unique permutation of the three unordered coordinate vertices; summary stdout remains byte-exact. Every support/class/dual-load record and every representative pair was independently reconciled against the root actual outputs in `incidence_label_reproducibility.json`. It deliberately rejects',1)
section='''## Final repaired-head and whole-queue gate

`final_repaired_package_gate.json` independently verifies the exact repaired commit, tree `c810b51c5d552bc0ce745ccfeddcf4e64074b85b`, parents original `5da73632ab7a621de7b62edb5f70dfb8017e4a50` and actual main `e491808c3544ff44e8526d9b24857b5c9ca64208`, and ancestry of actual PR379 merge `3ef0b0f3fa8cdaf3561c0a38408bb29719ecac6d`. The main ref was reread before and after the gate. All 47 repaired snapshot paths match their exact Git objects and repaired freeze hashes; all 46 mathematical paths also match the original freeze and original Git objects byte-for-byte. The entire problem subtree has exactly those 46 files, with no additional raw source or sixth-turn file. The PR three-dot diff against this actual main has precisely those 46 additions and the queue modification.

Every historical mathematical receipt (7/13/19/25 entries), the 36-entry author freeze, all 62 author manifest entries with prior-manifest chains, and the seven old-review manifest entries are rebound directly to the repaired tree and historical Git objects. Current STATE_T5 and PUBLICATION_SCOPE still explicitly record original unresolved/unsolved, five turns, stopped author search, preserved author/review files, no novelty certification and no raw-source inclusion. Fresh read-only GitHub API metadata advertises the same repaired head and actual base, 47 changed paths and an open draft titled original unsolved (5/5). The API's prospective merge_commit_sha is not treated as a completed PR merge.

Complete actual-main and repaired-head queue bytes are retained under `streams/repaired_queue_main.txt` and `streams/repaired_queue_head.txt`. The target is physical line **413**, displayed rank **402**. Exactly raw pipe cells **8 and 9** change `queued / 0/5` to `unsolved / 5/5`; all other target cells and every other queue byte match. This directly preserves all prior queue outcomes rather than relying on a subset of rows. Queue hashes are `a1210bbc36ebd6cd4ced6480edb0fe5e01d28bac59ebd2cf4910312853e396be` (main) and `78ed3d11ae95cf6b72550ce1df5dc6143ad2bc6b21a9d817cdc149314e3d3513` (head).

All eleven initial-seal instances remain unchanged; raw source files and renders remain locally Git-ignored and outside the bounded public evidence manifest. The prior pending report, manifest, log and correction bytes are preserved in `pending_head_record/`, with their explicit resolution map in `pending_head_evidence_preservation.json`. The first vertex-mapping comparison assumed the same convention as the root receipt; its inverse-convention failure is preserved and corrected without changing scientific code/data. The interim chat label of 214,070/93,918 as byte lengths is corrected: those are assertion counts; actual stdout sizes are 1,855 combined author bytes and 2,348 independent bytes.

'''
needle='## Strongest verified result and exact remaining gap\n'
assert needle in report;report=report.replace(needle,section+needle,1)
report=report.replace('subject to final artifact bindings.','with final artifact bindings verified.',1)
report=report.replace("The operational gap is the repaired head's 46-file invariance and QUEUE.md preservation against actual main after prior PR merges.", 'All operational audit gates are closed for the exact head/base named above. A later change to either mathematical packet or preservation baseline requires rebinding; no candidate merge or service disposition was performed by this reviewer.',1)
(D/'audit_report.md').write_text(report)

# Bound an explicit public evidence set: previous 46 plus the exact final gate
# artifacts. Exclude all raw PDFs/renders/runtime/private copies and caches.
extras=['verify_final_repaired_package.py','verify_incidence_label_reproducibility.py',
 'verify_incidence_label_reproducibility_first_attempt.py','finalize_audit_record.py',
 'final_repaired_package_gate.json','repaired_head_gate.json','incidence_label_reproducibility.json',
 'final_initial_seal_readback.json','pending_head_evidence_preservation.json',
 'pending_head_record/FINAL_AUDIT_MANIFEST.json',
 *['pending_head_record/'+p for p in mutable],
 'streams/repaired_queue_main.txt','streams/repaired_queue_head.txt',
 'streams/repaired_head_gate.stderr.txt','streams/final_repaired_package_gate.stderr.txt',
 'streams/incidence_label_reproducibility.stderr.txt',
 'streams/incidence_label_reproducibility_first_attempt.stderr.txt',
 'streams/incidence_label_reproducibility_first_attempt.stdout.txt',
 *['streams/'+label+'.'+kind+'.txt' for label in ('final_repaired_commit','final_pr_diff','final_github_pr_metadata') for kind in ('stdout','stderr')]]
paths=sorted({e['path'] for e in old['files']}|set(extras))
assert len(paths)==len(old['files'])+len(extras)
files=[]
for p in paths:
    assert not any(p.startswith(excluded) for excluded in ('primary/','runtime/','private_replay/','__pycache__/'))
    b=(D/p).read_bytes();files.append({'path':p,'bytes':len(b),'sha256':sha(b)})
manifest={k:v for k,v in old.items() if k!='files'}
manifest.update({'files':files,'recorded_utc':utc,'scope_completion_percent':100,
 'status':'PASS_SCOPED_FINAL_REPAIRED_PACKAGE_ORIGINAL_UNSOLVED_5_OF_5',
 'repaired_head':gate['repaired_head'],'actual_main':gate['actual_main'],'actual_379_merge':gate['actual_379_merge'],
 'repaired_snapshot_manifest_sha256':gate['repaired_snapshot_manifest_sha256'],
 'original_problem_status':'unsolved','original_problem_resolution_percent':0,'author_turns':'5/5',
 'final_gate_sha256':sha((D/'final_repaired_package_gate.json').read_bytes()),
 'incidence_reproducibility_sha256':sha((D/'incidence_label_reproducibility.json').read_bytes()),
 'pending_stage_manifest_sha256':sha(oldraw),'initial_seal_instances_unchanged':11,
 'queue_physical_line':413,'queue_displayed_rank':402,'queue_changed_pipe_cells':[8,9],
 'all_other_queue_bytes_and_prior_outcomes_preserved':True,'all_46_mathematical_files_unchanged':True,
 'mandatory_repairs':[],'remaining_audit_gates':[],
 'qualification':'Final scoped audit at exact repaired head and actual main, preserving original unsolved 5/5. Summary stdout byte-exact; detailed new incidence JSON reproducible up to the unique three-coordinate-vertex permutation, with every support/class/load record and representative verified. Wrappers source_files_checked=0; four own PDF matches do not constitute six-file source replay. Raw sources/renders stay local and ignored. No universal solution, novelty/priority certification, candidate merge, paper or DOI.'})
raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
(D/'FINAL_AUDIT_MANIFEST.json').write_bytes(raw)
for e in files:
    b=(D/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
print(json.dumps({'status':'PASS','public_evidence_files':len(files),
 'manifest_sha256':sha(raw),'report_sha256':sha((D/'audit_report.md').read_bytes()),
 'exact_repaired_head':gate['repaired_head'],'exact_actual_main':gate['actual_main'],
 'workflow_completion_percent':100,'original_problem_status':'unsolved','author_turns':'5/5'},sort_keys=True,indent=2))
