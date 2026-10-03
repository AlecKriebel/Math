"""Genuine ROOT fresh source-review and current-freeze prerequisites; no acceptance."""
from pathlib import Path, PurePosixPath
import ast, datetime as dt, hashlib, json, os, stat, subprocess, sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).absolute().parent
S=A/'current_preparation_family';F=A/'current_source_adversary_family';B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def encode(o):return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:assert k not in d;d[k]=v
        return d
    def bad(v):raise ValueError(v)
    return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=bad)
def ref(p,mode=False):
    b=raw(p);r=dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
    if mode:r['full_mode']=stat.S_IMODE(p.stat().st_mode)
    return r
def write(p,o):
    b=o if type(o) is bytes else encode(o)
    with p.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
    return ref(p)
prep=load(S/'PREPARATION_MANIFEST.json')
assert sha(raw(S/'PREPARATION_MANIFEST.json'))=='ee165341f8980110f1362a19c27f697db6df2e68eac01cc110a31c8d08ee9640'
assert sha(raw(S/'prepare_current_packet.py'))=='f815ea1867d0c38ce101e45d7eff48ee2979c6b113a7a5f76d8b3e44daa152f2'
assert sha(raw(S/'capture_root_builder_operation.py'))=='a1e7b1e4d0cb3a5bdd0ed8967352b0861650b5a5f9ba25b175421b14d411e9ef'
m=load(F/'MANIFEST.json')
assert sha(raw(F/'MANIFEST.json'))=='5c106f49f414b9695bbb3edd5969fcec9c63c94e6e5623380556beac60730440'
assert m['schema']=='pr48-independent-current-source-adversary-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and m['files_count']==len(m['files'])==86
members=[];owned=[]
for r in m['files']:
    assert set(r)=={'path','bytes','sha256','full_mode'} and type(r['bytes']) is int and r['full_mode']==0o444
    n=r['path'];assert PurePosixPath(n).as_posix()==n and not {'.','..'}.intersection(PurePosixPath(n).parts)
    q=ref(F/n,True);assert q['bytes']==r['bytes'] and q['sha256']==r['sha256'] and q['full_mode']==0o444
    owned.append(q);members.append({k:q[k] for k in ['path','bytes','sha256']})
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in m['files']}|{'MANIFEST.json'}
assert {'.'}|{p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}=={r['path'] for r in m['directories']}
for r in m['directories']:assert stat.S_IMODE((F/r['path']).stat().st_mode)==r['full_mode']
v=load(F/'VERDICT.json');assert v['mandatory_source_corrections']==v['mandatory_mathematical_corrections']==[] and v['future_acceptance_approved'] is False
assert sha(raw(F/'REPORT.md'))=='f2d8b4319f82f02dfec2f0a5630c6a1a488f050fc6f79cd9626d06692d36a98b'
assert sha(raw(F/'VERDICT.json'))=='4f2f150891313345bbe8b90829354b217995e49f3d9cdcafdd4b4376474ba546'
bindings=load(F/'AUDIT_BINDINGS.json');external=[]
for r in bindings['whole_external_read_rows']:
    p=R/r['path'];q=ref(p,True)
    assert q==r
    external.append(q)
assert len(external)==1698
captures=[]
for name,pid in [('root_pr48_current_source_closure_actual_capture',50088),('root_pr48_current_source_closed_readback_actual_capture',50493),('root_pr48_current_source_adversary_closure_actual_capture',86310),('root_pr48_current_source_adversary_closed_readback_actual_capture',86540)]:
    d=B/name;c=load(d/'CAPTURE.json')
    assert set(p.name for p in d.iterdir())=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    assert c['schema']=='root-explicit-command-capture/v1' and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==0 and c['actual_execution'] is True and c['completed'] is True and c['operator_unchanged'] is True
    assert sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']
    for k in ['stdout','stderr']:
        b=raw(d/c[k]['path']);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
    assert not raw(d/'stderr.bin')
    captures.append(dict(complete_capture=c,complete_members=[ref(p,True) for p in sorted(d.iterdir())],complete_stdout_object=load(d/'stdout.bin')))
assert dt.datetime.fromisoformat(captures[0]['complete_capture']['finished_utc'])<dt.datetime.fromisoformat(captures[1]['complete_capture']['started_utc'])
assert dt.datetime.fromisoformat(captures[2]['complete_capture']['started_utc'])<dt.datetime.fromisoformat(m['utc'])<dt.datetime.fromisoformat(captures[2]['complete_capture']['finished_utc'])<dt.datetime.fromisoformat(captures[3]['complete_capture']['started_utc'])
record=dict(schema='pr48-root-new-source-adversary-record/v1',approved_by_root=True,complete_report_personally_read=True,new_different_source_adversary=True,closed_clean=True,mandatory_corrections=[],created_utc=stamp(),
    preparation_manifest_sha256=sha(raw(S/'PREPARATION_MANIFEST.json')),builder_sha256=sha(raw(S/'prepare_current_packet.py')),operator_sha256=sha(raw(S/'capture_root_builder_operation.py')),
    manifest=ref(F/'MANIFEST.json'),report=ref(F/'REPORT.md'),members=members,complete_VERDICT_object=v,normalized_complete_owned_body_mode_rows=owned,individual_complete_external_bindings=external,complete_actual_SOURCE_and_adversary_closure_readback_captures=captures,
    all86_closed_members_full_bytes_modes_read=True,all1698_external_complete_bytes_modes_read=True,actual_postexit_capture_chronology_checked=True,production_import_compile_execution=False,new_whole_current_gate='PENDING',future_acceptance_approved=False,
    independence_qualification='Different PR48 SOURCE reviewer prepared unrelated PR47 V2; inherited context and review order are disclosed. ROOT personally read entire report, verdict, closer and verifier. Four failed private audit scripts and expected negative are retained; no old PASS is promoted to current WHOLE approval. This bounded source review grants no mathematical target resolution or future acceptance.')
record_ref=write(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json',record)
scope='''# ROOT PR48 exact unresolved partial acceptance

ROOT_SCOPE_ACCEPTED_EXACT_UNSOLVED_PARTIAL_ONLY

Original head: e2e5c8c3e5ad218f867fa753c465bb96b3687bda
GitHub base: c6975ca76f9f667f1250ba403d0e6da2aafe14d0
Actual merge base: 60292bed09f59236aa192cb17aa138f7b4750e1a
Status: unsolved
Original shared turns: 2/5; new: 0; audit: 0
Full target resolved: false
Novelty: false
Duplicate: 30004403 / OWR-17471-009
NEW whole-current review: PENDING
Paper/new DOI/tracker: false

The exact target is a closed orientable smooth four-manifold whose full smooth identity component has unbounded ordinary commutator length. Stabilization gives at most four commutators only on the included subgroup and vanishing homogeneous ambient quasimorphisms there. The suffix compression argument, cutoff plateau factorization, signed pushforward term and blocked retraction/invariant-measure routes are verified partial conclusions. Known smooth perfectness, portability, surface unboundedness and handle theorems are imported and credited. A Borel algebraic toy is not a smooth four-manifold construction. No arbitrary ambient sequence or theorem excluding all examples is supplied.

Both exact source IDs share one historical two-turn budget. Both upstream report keys are ABSENT, the SQLite fallback is literal {}, and no original prior-report file exists. Literal historical6570 receipts bind the old note; the final-input replay changes only its mathematical-note hash, and duplicate author replay is not independent. All original scientific text is preserved; old model/runtime/deadline/PASS/pending assertions are dated and globally qualified. ROOT's fresh primary reads concern cited text/formulas, with no fresh PDF/pixel authentication claim. Extensive AI use; unrefereed and no human peer review.

This certificate approves the exact unresolved mathematics for preparation only. A new whole-current adversary must review the actual postexit frozen packet. Subsequent acceptance needs another fresh13/main/foreign-work check and an independently reviewed acceptance source. No merge or native mirror is authorized by this record alone.
'''.encode()
scope_ref=write(A/'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md',scope)
common=dict(approved_by_root=True,operative_preparation_directory='current_preparation_family',created_utc=stamp(),preparation_manifest_sha256=sha(raw(S/'PREPARATION_MANIFEST.json')),source_qualification_sha256=sha(raw(S/'SOURCE_PRECISION_QUALIFICATIONS.md')))
evidence=dict(common,schema='pr48-root-evidence-bindings/v1',manifest=ref(A/'root_original_actual_reproduction_v2/MANIFEST.json'),summary=ref(A/'root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),proof_notes=ref(A/'ROOT_MATHEMATICAL_REVIEW.md'),raw_audit=ref(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'),source_adversary=record_ref,future_acceptance_approved=False)
evidence_ref=write(A/'ROOT_EVIDENCE_BINDINGS.json',evidence)
tree=ast.parse(raw(S/'prepare_current_packet.py'));flags=None
for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FLAGS' for t in n.targets):flags=ast.literal_eval(n.value)
assert type(flags) is list and len(flags)==8 and len(set(flags))==8
reading=dict(common,schema='pr48-root-primary-read-ledger/v1',reading_completed=True,root_flags={f:True for f in flags},scope_certificate_sha256=scope_ref['sha256'],evidence_bindings_sha256=evidence_ref['sha256'],future_acceptance_approved=False,
    reading_notes='ROOT personally read all original17 science files and complete18-path diff, full helper/results/metadata and original two-entry ledger, both closed independent mathematical reports/proofs, complete original ROOT38 Git/four helper and raw15458 derived audit, full builder/operator/global qualifications. The complete newly closed SOURCE review, all86 member bodies and1698 external bindings, entire verdict and four actual closure/readback captures were reconciled here after actual exit. Primary-source text/formula checks support credited imported hypotheses. Four-commutator stabilization concerns the included subgroup only; no arbitrary ambient lower bound or full solution. Historical receipt hashes are differentiated from final-input replay; duplicated author copy is not independent.')
write(A/'ROOT_PRIMARY_READ_LEDGER.json',reading)
science=dict(common,schema='pr48-root-science-card/v1',scope_certificate_sha256=scope_ref['sha256'],evidence_bindings_sha256=evidence_ref['sha256'],status='unsolved',full_problem_solved=False,project_solved=False,novelty_claimed=False,duplicate_id=30004403,duplicate_shared_budget=True,original_substantive_attempts=2,turn_limit=5,new_substantive_attempts=0,audit_turns=0,paper_created=False,new_DOI_created=False,tracker_row_created=False,current_model=None,current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None,new_whole_current_gate='PENDING',future_acceptance_approved=False,
    exact_remaining_gap='Construct an unbounded ordinary commutator-length sequence in the full smooth identity component of some closed orientable four-manifold, or rule out every such manifold by a sufficient theorem.',strongest_verified_result='Stabilized included subgroup uniformly bounded by four; quasimorphisms vanish there. Candidate retraction/invariant-measure/cutoff routes blocked under their stated assumptions.',imported_theorem_scope='Classical smooth perfectness and credited compression/portability, surface unboundedness and specific no-middle-handle theorem; conservative bound not claimed optimal.')
write(A/'ROOT_SCIENCE_CARD.json',science)
G=A/'root_current_prerequisite_Git_actual_captures';G.mkdir(exist_ok=False);commands=[]
def git(argv):
    assert argv[:1]==['git'] and argv[1] in {'branch','rev-parse','show'}
    if argv[1]=='branch':assert argv==['git','branch','--show-current']
    d=G/str(len(commands));d.mkdir();pre=dict(schema='pr48-root-prerequisite-readonly-git-prelaunch/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),created_utc=stamp(),source=None)
    write(d/'PRELAUNCH.json',pre)
    c=dict(schema='pr48-root-prerequisite-readonly-git-actual/v1',argv=argv,cwd=str(R),operator_pid=os.getpid(),started_utc=stamp(),actual_execution=False,completed=False,pid=None,exit_code=None,source=None,source_unchanged=None,stdin_supplied=False)
    with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
        p=subprocess.Popen(argv,cwd=str(R),stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));c.update(actual_execution=True,pid=p.pid)
        try:c['exit_code']=p.wait(timeout=60);c['completed']=True
        except BaseException:p.kill();c['exit_code']=p.wait();raise
    c['finished_utc']=stamp()
    for k in ['stdout','stderr']:b=raw(d/(k+'.bin'));c[k]=dict(path=k+'.bin',bytes=len(b),sha256=sha(b))
    write(d/'CAPTURE.json',c);commands.append(c)
    assert c['completed'] is True and c['exit_code']==0 and not raw(d/'stderr.bin')
    return raw(d/'stdout.bin')
assert git(['git','branch','--show-current'])==b'main\n';head=git(['git','rev-parse','HEAD']).decode().strip()
native={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}
native.add('draft_pr_publication_program_20260930/inventory.json');files=[ref(R/n,True) for n in sorted(native)]
for n in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json']:assert git(['git','show',head+':'+n])==raw(R/n)
for r in files:assert ref(R/r['path'],True)==r
assert git(['git','branch','--show-current'])==b'main\n' and git(['git','rev-parse','HEAD']).decode().strip()==head
write(A/'ROOT_CURRENT_INPUT_PREIMAGES.json',dict(schema='pr48-root-fresh13-input-preimages/v1',approved_by_root=True,created_utc=stamp(),reason='ROOT read all13 complete live bodies and full modes in place, verified native4 against the actual committed main, rechecked everybody/mode and actual main after the reads. Dated current-freeze authority only; future acceptance requires fresh new checks.',current_head=head,files=files,operative_preparation_directory='current_preparation_family'))
print(json.dumps(dict(status='PASS_GENUINE_ROOT_CURRENT_FREEZE_PREREQUISITES_ONLY',actual_pid=os.getpid(),current_head=head,source_members=86,source_external_bindings=1698,complete_source_record=ref(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),five_actual_prerequisites=[ref(A/n) for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']],actual_readonly_Git_children=len(commands),new_whole_current_gate='PENDING',future_acceptance_approved=False),indent=2))
