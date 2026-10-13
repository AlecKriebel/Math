"""Close mathematical review only, after complete fresh evidence readback."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
def req(c,label):
    if not c:raise RuntimeError(label)
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Shared tracked writes paused')
req(not (A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').exists(),'Already accepted')
inputs=load(A/'ROOT_INITIAL_INPUT_BINDINGS.json')
req(inputs['all_original_API_Git_disk_bytes_modes_equal'] and inputs['total_author_assertions']==564189,'Initial authentication missing')
original=load(A/'snapshot_manifest.json');H=original['head']
for j in original['files']:
    q=A/'snapshot'/j['path'];req(pin(q)==dict(bytes=j['bytes'],sha256=j['sha256']),'Original snapshot changed')
families={}
for name,receipt_name in [('markov_closure','ROOT_MARKOV_FINAL_ARTIFACT_AUTHENTICATION.json'),('lattice_factorization','ROOT_LATTICE_FINAL_ARTIFACT_AUTHENTICATION.json')]:
    auth=load(A/receipt_name);req(auth['family_math_percent']==100 and auth['early_independence_pins_unchanged'],'Incomplete fresh family')
    for n,h in auth['final_pins'].items():req(sha((A/name/n).read_bytes())==h,'Fresh final changed')
    families[name]=dict(authentication=pin(A/receipt_name),final_pins=auth['final_pins'])
req(sha((A/'ROOT_PROOF_AUDIT.md').read_bytes())=='cf28e53d9ddbb82d39c1568ec4c8db4281bc158f7b6041057713802b749a82ee','Root proof record changed')
D=A/'mathematical_acceptance_private';D.mkdir(exist_ok=False)
args=['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']
spec=dict(argv=args,cwd=str(A),started_utc=utc(),operator=pin(Path(__file__)))
(D/'live_pr_preexecution.json').write_text(json.dumps(spec,indent=2)+'\n')
r=subprocess.run(args,cwd=A,capture_output=True)
(D/'live_pr.stdout').write_bytes(r.stdout);(D/'live_pr.stderr').write_bytes(r.stderr)
spec.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr))
(D/'live_pr_execution.json').write_text(json.dumps(spec,indent=2)+'\n')
req(r.returncode==0,'Live PR read failed');pr=json.loads(r.stdout)
req(pr['state']=='open' and pr['draft'] and pr['head']['sha']==H,'Live submitted PR changed')
stamp=utc()
rec=dict(utc=stamp,status='PASS_BOTH_EXACT_SOURCE_MATHEMATICAL_ANSWERS_ACCEPTED',original_head=H,
    original_author_turns='2/5',original_file_count=30,conjecture_1='affirmative pointwise closure for all finite binary graphs',
    conjecture_2='negative by exact globally Markov MTP2 C4 law outside clique factorization and its closure',
    conjecture_3='same law also refutes stronger lattice-support factorization statement',
    separate_gaussian_conjecture_4_not_in_scope=True,root_proof_audit=pin(A/'ROOT_PROOF_AUDIT.md'),families=families,
    original_native_reproduction=pin(A/'ROOT_INITIAL_INPUT_BINDINGS.json'),fresh_control_reproduction=pin(A/'ROOT_INDEPENDENT_CONTROL_REPLAYS.json'),
    actual_live_PR_query=spec,root_full_proofs_code_manifests_streams_and_original_source_read=True,
    lattice_late_summary_exposure_disclosed_not_used=True,mathematical_percent=100,workflow_percent=35,
    priority_percent=0,priority_clearance=False,publication_ready=False,merge=False,paper=False,zenodo=False,tracker=False,goal_complete=False)
(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').write_text(json.dumps(rec,indent=2)+'\n')
(A/'ROOT_MATHEMATICAL_ACCEPTANCE.md').write_text('''# Accepted mathematics; priority pending

Both exact finite binary source answers pass full root and two fresh staged independent reviews. The submitted C4 law is globally Markov and MTP2 but violates a classical clique-factor parity invariant, giving a complete negative answer to Conjecture2 (and the stronger Conjecture3). The support/aggregate-attraction/max-flow residual normalization proof gives the affirmative answer to Conjecture1, including zero probabilities, signed finite factor conventions, isolates and empty cases. The fresh lattice family also supplied a distinct complete closure proof through Markov lattice-support reconstruction and a closed restricted log-design space. Root has read and checked that derivation; it preserves the essential approximating-sequence hypothesis and does not assert the false stronger factorization claim.

The exact original source was visually read; all30 source snapshot objects and10/18/28/7 manifest entries were authenticated. All564189 author and89324 inherited assertions, and all three fresh independent controls, reproduced exactly under the root's native runs. Fresh complete reviewer proofs/code/actual streams and final sealed artifacts were read and authenticated. The lattice family's later extra publication-summary exposure is disclosed and excluded from evidence; its earlier independent mathematical verdict and controls preceded that read. New publication reviewers are still required.

'''+f'Accepted at {stamp}. Original author2/5 and all submitted artifacts remain unchanged. Mathematics100%, workflow35%, priority0%. This accepts mathematical correctness only: historical priority and novel resolution remain hypotheses to audit next. No merge, preprint, Zenodo record, DOI, tracker row or release has been performed for PR311. The persistent goal remains active.\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=utc(),descending_311_mathematical_verification_percent=100,
    descending_311_mathematical_verification_complete=True,descending_311_workflow_percent=35,
    descending_311_priority_complete=False,descending_311_priority_percent=0,descending_311_preprint_ready=False)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
entry=stamp+' — PR311 mathematics100% accepted after complete root proof/source/code read and both fresh final family evidence authentication. Exact source C1 affirmative, C2/C3 negative; distinct source-first support/design closure proof also verified. Author2/5 unchanged. Workflow35%, priority0%; next independent priority audits, no promotion/paper/merge/upload/tracker. Goal active.\n'
for q in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with q.open('a') as f:f.write('\n'+entry)
print(json.dumps({k:v for k,v in rec.items() if k not in ['families','actual_live_PR_query']},indent=2))
