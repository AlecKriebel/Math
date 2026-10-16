"""ROOT actual active148 request: small immutable posts and read-only observations."""
from pathlib import Path
import hashlib,json,os,types
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
P=C/'draft_pr_publication_program_20260930';A=P/'audits/pr148_5100002';D=A/'active_checkpoint_operator_preparation_20261008'
SRC=D/'active_checkpoint_operator_v3.py';body=SRC.read_bytes()
if len(body)!=44473 or hashlib.sha256(body).hexdigest()!='106f92eb866ee0517b33e7d8abb743283f1b1264f00f6b106f83df73611cbcbe':raise RuntimeError('sealed v3 source changed')
op=types.ModuleType('exact_active148_operator');op.__file__=str(SRC);exec(compile(body,str(SRC),'exec'),op.__dict__);m=op.m
D.joinpath('private').mkdir(exist_ok=True);run=D/'private/ROOT_ACTUAL_REQUEST_02';run.mkdir(exist_ok=False)
j={'schema':'pr148-root-active-request-preparation/v1','actual_ROOT_PID':os.getpid(),'UTC_start':m.utc(),'children':[],'child_custody_root':str(run/'raw'),'provider_mutation_performed':False,'local_program_installation_performed':False}
m.dump(run/'RECEIPT.json',j)
def full(p):return {'path':str(p),**m.pin(p)}
def inventory(p):
    p=m.safe(p);files=[];dirs=[]
    for current,ds,fs in os.walk(p):
        current=Path(current)
        for name in sorted(ds):
            item=current/name;m.require(not item.is_symlink(),'directory symlink');dirs.append(item.relative_to(p).as_posix())
        for name in sorted(fs):files.append({'relative':(current/name).relative_to(p).as_posix(),**m.pin(current/name)})
    return {'path':str(p),'files':sorted(files,key=lambda x:x['relative']),'directories':sorted(dirs)}
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
    try:
        view=memoryview(b)
        while view:
            n=os.write(fd,view);m.require(n>0,'write progress');view=view[n:]
        os.fchmod(fd,420);os.fsync(fd)
    finally:os.close(fd)
    m.require(p.read_bytes()==b,'whole created body')
try:
    gate=full(op.BASELINE_GATE);native=op.baseline_acceptance(gate)
    accepted_plan=m.native_json(m.read_pinned(native['final_evidence_pins']['plan']))
    base=m.remote(j)
    m.require(base==op.FINAL_COMMIT,'fresh direct main exactly completed147 final checkpoint')
    # Read-only object access must still occur through a fresh owned workspace.
    # The sealed source initializes its own bare store and a read-only alternate;
    # no old workspace/control is modified, and there is no history-fetch route.
    op.workspace({'native':native,'base_commit':base},j,run)
    j['own_private_git_workspace_initialization_performed']=True
    for root,expected in ((R,accepted_plan['R_HEAD']),(C,accepted_plan['C_HEAD'])):
        m.require(m.git(['rev-parse','HEAD','refs/heads/main'],j,root=root).decode().splitlines()==[expected,expected],'real HEAD/main guards')
    render_path=A/'active_checkpoint_data_preparation_20261008/ROOT_POSTIMAGES_01/RENDER_RESULT.json'
    render=m.native_json(render_path.read_bytes());m.require(m.digest(render_path.read_bytes())=='f717be0ec53b4c5415b5c1c58f82a07849f717f4917a4cf6e75604eab02a3f20','genuine conditional render')
    m.full_pin(render['source']);m.full_pin(render['goal_record']);m.require(render['publication_installation_or_final_acceptance_performed'] is False and render['baseline_gate']==gate and render['mathematical_gate']==op.mathematical_gate_source(),'render stage/gates')
    proposed={}
    for name,spec in render['postimages'].items():
        m.full_pin(spec);rel='draft_pr_publication_program_20260930/'+name
        m.require(render['before'][name]==full(C/rel),'accepted current C program before');proposed[rel]=m.read_pinned(spec)
    own=[
      'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json','ROOT_INITIAL_REVIEW_READBACK_20261008.json','ROOT_MATHEMATICAL_GATE_20261008.json','ROOT_GUARDED_SUPPORT_DIAGNOSTIC_20261008.json','ROOT_GOAL_TOOL_OBSERVATION_20261008.json','ROOT_PRELIMINARY_DERIVATION_20261008.md','ROOT_PRELIMINARY_EXACT_ARITHMETIC_20261008.json','RESEARCH_LOG.md',
      'math_operations_20261008/authenticate_initial_reviews.py','math_operations_20261008/build_guarded_support.py','math_operations_20261008/run_guarded_support.py','math_operations_20261008/accept_mathematics.py',
      'active_checkpoint_data_preparation_20261008/render_active_program.py','active_checkpoint_data_preparation_20261008/prepare_actual_request.py',
      'geometry_falsification_20261008/GEOMETRY_AUDIT.md','geometry_falsification_20261008/STATUS.json','geometry_falsification_20261008/SOURCE_PINS.json','geometry_falsification_20261008/independent_geometry_results.json','geometry_falsification_20261008/ARTIFACT_MANIFEST.json',
      'analytic_family_adversary_20261008/ANALYTIC_AUDIT.md','analytic_family_adversary_20261008/exact_check_output.json',
      'verification_code_adversary_20261008/AUDIT_REPORT.md','verification_code_adversary_20261008/AUDIT_SUMMARY.json','verification_code_adversary_20261008/candidate_repair_manifest.json',
      'verification_code_adversary_20261008/support_checker_hardening_20261008/SUPPORT_FINAL_REPORT.md','verification_code_adversary_20261008/support_checker_hardening_20261008/SUPPORT_FINAL_SUMMARY.json','verification_code_adversary_20261008/support_checker_hardening_20261008/SUPPORT_INTEGRITY_CHECK.json','verification_code_adversary_20261008/support_checker_hardening_20261008/SUPPORT_SOURCE_MANIFEST_BEFORE.json',
      'active_checkpoint_operator_preparation_20261008/active_checkpoint_operator_v3.py','active_checkpoint_operator_preparation_20261008/REQUEST_CONTRACT_v3.json','active_checkpoint_operator_preparation_20261008/REPORT_v3.md','active_checkpoint_operator_preparation_20261008/SOURCE_PREPARATION_RESULT_v3.json','active_checkpoint_operator_preparation_20261008/FINAL_MANIFEST_v3.json','active_checkpoint_operator_preparation_20261008/FINAL_READBACK_v3.json']
    own += ['guarded_support_v1/'+p for p in ['SOURCE_MANIFEST.json','author/verify.py','author/COUNTEREXAMPLE.md','author/expected_verification.json','inherited/independent_checks.py','inherited/author_replay/COUNTEREXAMPLE.md','inherited/expected_independent_results.json','analytic/check_analytic_family.py','geometry/independent_geometry.py']]
    for name in own:proposed[A.relative_to(C).as_posix()+'/'+name]=m.safe(A/name).read_bytes()
    for rel in sorted(op.FINAL_COMPACT):proposed[rel]=m.safe(C/rel).read_bytes()
    for name in sorted(op.INTAKE_NAMES):
        p=C/(op.INTAKE+name)
        if p.exists():proposed[op.INTAKE+name]=m.safe(p).read_bytes()
    posts=D/'private/ROOT_IMMUTABLE_POSTIMAGES_02';posts.mkdir(exist_ok=False)
    postimages={};preimages={};artifacts=[];omitted=[]
    for rel,data in sorted(proposed.items()):
        raw=m.git(['ls-tree','-z',base,'--',rel],j);pre=None
        if raw:
            m.require(raw.endswith(b'\0') and raw.count(b'\0')==1,'single current selected entry')
            header,sep,name=raw[:-1].partition(b'\t');fields=header.split(b' ')
            m.require(sep and len(fields)==3 and fields[0]==b'100644' and fields[1]==b'blob' and name.decode()==rel,'current selected mode/path')
            old=m.git(['cat-file','blob',fields[2].decode()],j);pre={'bytes':len(old),'mode':420,'sha256':m.digest(old),'Git_blob':fields[2].decode()}
            if old==data:m.require(rel not in op.PROGRAM,'program must change');omitted.append(rel);continue
        create(posts/rel,data);postimages[rel]=full(posts/rel);preimages[rel]=pre
        if rel not in op.PROGRAM:artifacts.append(rel)
    protected=accepted_plan['protected']
    for spec in protected:m.full_pin(spec)
    absences=accepted_plan['protected_absences']
    for p in absences:m.require(not m.local_case_guard(p).exists(),'current protected absence')
    dirs=list(accepted_plan['protected_directories'])
    for d in dirs:m.closed_directory(d)
    dirs += [native['original148_directory'],inventory(posts)]
    request={'schema':'pr148-active-checkpoint-request/v1','baseline_acceptance':gate,'fresh_base_commit':base,'R_HEAD':accepted_plan['R_HEAD'],'C_HEAD':accepted_plan['C_HEAD'],'git_executable':accepted_plan['git_executable'],'gh_executable':accepted_plan['gh_executable'],'postimage_root':str(posts),'artifact_paths':artifacts,'postimages':postimages,'remote_preimages':preimages,'program_preimages':{rel:{k:render['before'][Path(rel).name][k] for k in ('bytes','mode','sha256')} for rel in op.PROGRAM},'protected':protected,'protected_absences':absences,'protected_directories':dirs,'commit_message':'Audit PR148 literal k108 counterexample and begin priority review\n\nPreserve completed PR147 final acceptance and26 completed cases/14 publications. Record independent physical-family proofs, exact unequal six-period values and optimization-safe fresh verification support. Original1/5 and immutable original20 retained; no new central proof-search turns. Priority/publication/native disposition remain pending; persistent goal active.'}
    create(run/'REQUEST.json',m.canonical(request));op.proposal(full(run/'REQUEST.json'))
    m.require(m.remote(j)==base,'direct main unchanged after preparation')
    j.update(status='ACTUAL_ACTIVE148_REQUEST_READY_REVIEW_REQUIRED',request=full(run/'REQUEST.json'),source=full(SRC),render=full(render_path),mathematical_gate=op.mathematical_gate_source(),postimage_root=str(posts),selected_path_count=len(postimages),artifact_path_count=len(artifacts),omitted_unchanged_artifacts=omitted,program_preimages_unchanged=True,current_native147_32_unchanged=True,protected_file_count=len(protected),closed_directory_count=len(dirs),overall_goal_complete=False)
except BaseException as error:j.update(error_type=type(error).__name__,error=str(error));raise
finally:
    j.update(UTC_end=m.utc(),all_obtained_children_complete=m.children_custody_complete(j));m.dump(run/'RECEIPT.json',j)
m.require(j['all_obtained_children_complete'],'all obtained request children closed')
for child in j['children']:m.authenticate_child_custody(child)
print(json.dumps({'status':j['status'],'request':j['request'],'paths':j['selected_path_count'],'closed_children':len(j['children'])}))
