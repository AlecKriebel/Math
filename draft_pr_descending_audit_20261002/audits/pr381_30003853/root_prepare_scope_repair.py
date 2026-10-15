"""Qualify the current gap without overwriting immutable historical evidence."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
A=Path(__file__).resolve().parent;S=A/'repaired_snapshot/problems/30003853_thompson_subgroup_abelianization';D=A/'tmp/scope_repaired_packet'
shutil.copytree(S,D,dirs_exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
t=datetime.datetime.now(datetime.timezone.utc).isoformat()
text='''# Current diagram-group scope correction

This note is the authoritative current interpretation of the exact remaining gap in historical FINAL_RESULT.md. It supersedes the unsupported diagram-group portion of “An arbitrary finitely presented subgroup of F need not be ... a diagram group”. The packet supplies no finitely presented subgroup of F proved not to be a diagram group, so that wording is not promoted as a theorem or counterexample. Historical author and reviewer files stay unchanged as evidence of what was previously written.

**Correct remaining gap:** finite presentation alone has not been shown **in this packet** to put an arbitrary subgroup of Thompson's F in a proved positive class. In particular, the packet establishes neither universal diagram-group status for finitely presented F subgroups nor an example refuting that status. It gives no universal bridge to its restricted wreath, solvable, simple-derived subdirect, closed/diagram or normal-subgroup classes, and no finitely presented embedded subgroup with torsion in abelianization.

The credited diagram-group homology theorem and the closed-subgroup positive class retain their hypotheses. They do not establish a reduction for every finitely presented subgroup merely because F itself is a diagram group. This note asserts no general theorem about closure of diagram groups under arbitrary subgroups and no worldwide literature-completeness claim. The actual source Question111 still asks whether every finitely presented subgroup of F has torsion-free abelianization; the verified abstract nilpotent proxy countermodels are proved nonembeddable and are not counterexamples to that question.

All five substantive author turns remain valid scoped partial findings, and the original question remains unresolved by this package, **unsolved,5/5**. No sixth search turn or mathematical novelty claim is introduced. Keep exact finite presentation versus FP2, ordinary finite generation of normal closures versus finite normal generation, coefficient/source-version assumptions and the actual PL embedding requirement.

All original author/historical-review bytes and their pinned manifests remain unchanged. Current REVIEWED_STATUS.md, PUBLICATION_MANIFEST.json and verify_publication.py now incorporate this authoritative qualification. Historical “no correction required” verdicts are historical scoped evidence, not a clean current-head certification. Fresh corrected-head adversarial review and root verification remain required before acceptance.

AI tools were used extensively for research, drafting, verification and review. This is unrefereed and is not external human peer review. No paper, Zenodo deposit, DOI, tracker row or release is created for this unresolved result.
'''
(D/'CURRENT_SCOPE_CORRECTION.md').write_text(text)
cm={'utc':t,'target_id':30003853,'original_frozen_head':'5b7bd8db9f34294d10862fed0f723055da864df6','queue_only_head':'89d5f156c4a2846d6ef0b840cd24c854677d07ca','current_authoritative_scope':'No diagram-group membership reduction or fp non-diagram subgroup counterexample established by this packet','original_status':'unsolved','turns':'5/5','historical_files_preserved':True,'files':[{'path':'CURRENT_SCOPE_CORRECTION.md','bytes':len((D/'CURRENT_SCOPE_CORRECTION.md').read_bytes()),'sha256':sha((D/'CURRENT_SCOPE_CORRECTION.md').read_bytes())}]}
(D/'CURRENT_SCOPE_MANIFEST.json').write_text(json.dumps(cm,indent=2)+'\n')
status=(D/'REVIEWED_STATUS.md').read_text();status=status.replace('This additive wrapper supersedes the historical review-pending status without changing frozen author or reviewer files.','This current wrapper retains the historical author/reviewer evidence. Read CURRENT_SCOPE_CORRECTION.md first: the diagram-group portion of the historical exact-gap sentence is unsupported and is superseded by an explicit statement that this packet proves no universal membership reduction and supplies no finitely presented non-diagram subgroup example. Corrected-head acceptance review remains pending.')
status=status.replace('No merge or release is part of this publication.','No release or solved-paper publication is part of this unresolved package. Acceptance requires the corrected-head final gate.')
(D/'REVIEWED_STATUS.md').write_text(status)
code=(D/'verify_publication.py').read_text();addition=f"\n# Additional authoritative scope; immutable historical manifests remain pinned.\nassert hashlib.sha256((P/'CURRENT_SCOPE_MANIFEST.json').read_bytes()).hexdigest()=={sha((D/'CURRENT_SCOPE_MANIFEST.json').read_bytes())!r}\nfor e in json.loads((P/'CURRENT_SCOPE_MANIFEST.json').read_text())['files']:\n b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']\n"
code=code.replace("actual=json.loads(subprocess.check_output",addition+"\nactual=json.loads(subprocess.check_output")
code=code.replace('raw source replay omitted (0/20 local-only bindings)','current diagram-group gap qualification bound; raw source replay omitted (0/20 local-only bindings)')
(D/'verify_publication.py').write_text(code)
pm=json.loads((D/'PUBLICATION_MANIFEST.json').read_text());pm['current_authoritative_scope_correction']='CURRENT_SCOPE_CORRECTION.md';pm['historical_author_and_review_bindings_preserved']=True
def entry(path):
 b=(D/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
pm['files']=[entry(e['path']) for e in pm['files']]+[entry(p) for p in ['CURRENT_SCOPE_CORRECTION.md','CURRENT_SCOPE_MANIFEST.json']];pm['files'].sort(key=lambda e:e['path']);(D/'PUBLICATION_MANIFEST.json').write_text(json.dumps(pm,indent=2)+'\n')
changed=[str(f.relative_to(S)) for f in S.rglob('*') if f.is_file() and f.read_bytes()!=(D/f.relative_to(S)).read_bytes()]
assert set(changed)=={'REVIEWED_STATUS.md','PUBLICATION_MANIFEST.json','verify_publication.py'},changed
r=subprocess.run([sys.executable,'-B',str((D/'verify_publication.py').absolute())],capture_output=True,cwd=D)
(A/'root_scope_repaired_publication.stdout').write_bytes(r.stdout);(A/'root_scope_repaired_publication.stderr').write_bytes(r.stderr);assert r.returncode==0 and not r.stderr,r.stderr.decode()
(A/'CURRENT_CORRECTED_SCOPE.md').write_bytes((D/'CURRENT_SCOPE_CORRECTION.md').read_bytes())
receipt={'utc':t,'original_frozen_head':cm['original_frozen_head'],'queue_only_head':cm['queue_only_head'],'private_packet':str(D.absolute()),'original_files_preserved_except_current_wrappers':changed,'new_files':['CURRENT_SCOPE_CORRECTION.md','CURRENT_SCOPE_MANIFEST.json'],'all_historical_author_and_review_bytes_unchanged':True,'current_all_target_files':46,'full_current_publication_replay_exit':0,'complete_stdout_sha256':sha(r.stdout),'scope_repair':'Unsupported fp subgroup non-diagram claim replaced by packet-local no-membership-reduction gap','status':'unsolved','turns':'5/5','workflow_percent':90,'branch_repair_pending':True,'new_adversary_after_global_current_updates_required':True}
(A/'scope_repair_preparation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
