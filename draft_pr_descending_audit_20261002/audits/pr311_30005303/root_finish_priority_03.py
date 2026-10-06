"""Record bounded priority adjudication after root's complete final-report read."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,stat
A=Path(__file__).resolve().parent;V=A/'closure_priority_adversary';sha=lambda b:hashlib.sha256(b).hexdigest()
expected={'public/FINAL_PRIORITY_REPORT.md':'2253f36227468bfdc59b85d4d9c2f14563b2b1d8427bc5a384c9a643509dd71f',
 'public/SEALED_MANIFEST.json':'816aea4b853ecf63fc34920423ee24032b787519d5cac10f3494418c4db95420',
 'public/SEAL_VERIFICATION.json':'30f01a3a7c27ddfd0a24dedca2073f093e524d7fc3f3419a8aa723ab18505a16'}
def measure(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(p.stat().st_mode)))
for name,h in expected.items():
 m=measure(V/name);assert m['sha256']==h and m['mode']=='0o444'
manifest=json.loads((V/'public/SEALED_MANIFEST.json').read_bytes())
for row in manifest['files']:
 m=measure(V/row['path']);assert m=={k:row[k] for k in ['bytes','sha256','mode']}
for row in manifest['released_inputs_reverified']:
 m=measure(Path(row['path']));assert m=={k:row[k] for k in ['bytes','sha256','mode']}
stamp=datetime.now(timezone.utc).isoformat()
j=dict(actual_utc=stamp,status='PASS_BOUNDED_PRIORITY_AUDIT_QUALIFIED_RESEARCH_NOTE_PREPARATION',
 mathematical_acceptance='C1 closure and stronger F2=closure(attractive original-edge laws) valid; C2/C3 negative answers valid.',
 C2_C3_priority='Exact witness previously published in Gandolfi–Lenarda Lemma5.2, publication13April2017; require full attribution. C6 is an attributed lift, not a newly resolving counterexample.',
 C1_priority='KS2024 proves natural-support limit-factorization; complete all-support original-edge extension needs connected ties/edge-design or facial-lattice bridge. Inspected prior bodies do not state the full source theorem or stronger zero-support attractive-approximation characterization.',
 contribution_judgment='A concise explicitly attributed research note is warranted by the general characterization and exact resolution of source Conjecture1. Do not represent the problem as untouched by KS2024, claim new counterexamples, or assert historical first discovery. Elementary deductions from prior theorems do not by themselves establish already-published priority.',
 scope_decision='Retain originally claimed_solved eligibility: no equivalent earlier full theorem was established; complete mathematical resolution remains valid. Publication framing repaired before any promotion.',
 limitation='Bounded primary-source comparison cannot prove universal historical absence. No historical novelty certificate or first-resolution claim is granted.',
 root_read='All three final priority reports and independent complete support bridges fully read; code/native scientific reproductions and immutable artifact pins authenticated. Primary body scope is separately recorded.',
 adversary_sealed_files_authenticated=len(manifest['files']),candidate_inputs_unchanged=True,
 remaining_gates=['prepare complete manuscript and verification package','two sequential fresh full-package adversarial reviews, with global repairs and additional fresh reviews until clean','actual final package and live PR acceptance checks','Zenodo publication and exact-once Google Workspace row'],
 math_percent=100,bounded_priority_audit_percent=100,workflow_percent=45,preprint_ready=False,immutable_publication_clearance=False,goal_complete=False)
out=A/'ROOT_PRIORITY_DECISION_03.json';assert not out.exists();out.write_text(json.dumps(j,indent=2)+'\n')
for p in [A/'RESEARCH_LOG.md',A.parent.parent/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+stamp+' — PR311 bounded priority adjudication complete: third fresh candidate-blind approach frozen then named-gated,110 sealed artifacts/five inputs unchanged; full final report and independent facial bridge root-read. Original C4 exactly GL2017; closure is an attributed all-support extension of KS2024, stronger original-edge attractive approximation separately proved and absent from inspected statements. Accept concise qualified note preparation, with no first-discovery or novelty certificate. Keep eligibleclaimed_solved mathematical resolution; no earlier equivalent full theorem established. Math100%, boundedpriority100%, workflow45%. Preprint reviews/publication/merge still pending.\n')
print(json.dumps(j,indent=2))
