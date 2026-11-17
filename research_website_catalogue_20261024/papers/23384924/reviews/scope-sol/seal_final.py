"""Read-only evidence comparisons and exclusive finite seal; no scientific/project imports."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
R=Path(__file__).resolve().parent; S=R.parents[1]/'sources'
def pin(p,root=None):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular: '+str(p))
    b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p),bytes=len(b),
        SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
def inv(root):
    fs=[];ds=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode):fs.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode):ds.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
        else:raise RuntimeError('unexpected object: '+str(p))
    return fs,ds
def create(name,value):
    with (R/name).open('x') as f:f.write(json.dumps(value,indent=2)+'\n')
for n in ('DATA_CHECKS.json','MANIFEST.json','FINAL.json'):
    if (R/n).exists():raise RuntimeError('already sealed: '+n)
custody=json.loads((R/'SOURCE_CUSTODY.json').read_text());sf,sd=inv(S)
if sf!=custody['files'] or sd!=custody['directories']:raise RuntimeError('source drift')
if oct(stat.S_IMODE(S.lstat().st_mode))!=custody['root_mode']:raise RuntimeError('source root-mode drift')
for name,expected in {
    'INITIAL_MANIFEST.json':'2114c6f9c2963e4080ec6ac9790fba6f7af7ea7bb40c1d3858be01991843148d',
    'INITIAL_SEAL.json':'a6011dfb3d656050816e267ddb27c5a6e037376289772d700f1056655fa6d2db',
    'CHECKPOINT_MANIFEST.json':'685e54c2d232aa3b9b6f18aa1c0fd639be088cb0f953e91343a0d336c8c820c2',
    'CHECKPOINT.json':'471ae7f3d2849cc3e6a99999205ac187fb0b5cd7bfd605b65b988308b90820fb'
}.items():
    if pin(R/name,R)['SHA256']!=expected:raise RuntimeError('frozen control drift: '+name)
for name in ('INITIAL_MANIFEST.json','CHECKPOINT_MANIFEST.json'):
    m=json.loads((R/name).read_text())
    for p in m['payload_files']:
        if pin(R/p['path'],R)!=p:raise RuntimeError('frozen payload drift: '+p['path'])
    for d in m['directories']:
        p=R/d['path'];st=p.lstat()
        if not stat.S_ISDIR(st.st_mode) or oct(stat.S_IMODE(st.st_mode))!=d['mode']:raise RuntimeError('frozen directory drift')
native=S/'published-source/container-002/tree/exact_controls.py'
if native.read_bytes()!=(R/'native-run/exact_controls.py').read_bytes():raise RuntimeError('native copy mismatch')
if pin(R/'native-run/exact_controls.py',R)['SHA256']!='d2c096251103e0cd7b95ffecf6ef451bcef19083faf0e6e6ca0517862ab3e531':raise RuntimeError('executed code pin mismatch')
if (R/'native-run/stderr.txt').read_bytes()!=b'':raise RuntimeError('native stderr nonempty')
result=json.loads((R/'native-run/stdout.txt').read_text())
if result['status']!='PASS' or result['checks']!=3558 or sum(result['by_family'].values())!=3558:raise RuntimeError('native result mismatch')
receipt=json.loads((R/'EXECUTION_RECEIPT.json').read_text())
if receipt['output']['by_family']!=result['by_family']:raise RuntimeError('execution receipt family mismatch')
if (R/'primaries/aleksandrov-popova.response.body').exists():raise RuntimeError('unexpected claimed-uncreated body')
if (R/'primaries/aleksandrov-popova.stderr.txt').read_text()!='curl: (56) The requested URL returned error: 403\n':raise RuntimeError('literal access-error mismatch')
for name in ('hayman-lingham-v2.pdf','koepf1986.pdf'):
    if not (R/'primaries'/name).read_bytes().startswith(b'%PDF'):raise RuntimeError('not an actual primary PDF')
base=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/audits/pr662_2306086/reviews')
external=[]
for rel,digest in [
 ('priority_literature_01/tmp/jenkins1962_recheck.pdf','f5e81479d158b49f557bcce334f8c4992ef4543b2b81eba3db92e8842808650d'),
 ('historical_source_access_01/tmp/rodemich1979_ams_wayback.pdf','04df2b98e61313f7afb1da73329dc536237ce6d8c0f7431a9409991f693a64a0'),
 ('historical_source_access_01/tmp/rodemich1979_A68.png','e34277d4568410e77050da1ad2291be073cb37638eccc7a3d8c4bcb685c08a68')]:
    p=pin(base/rel)
    if p['SHA256']!=digest:raise RuntimeError('cached primary drift')
    external.append(p)
now=datetime.now(timezone.utc).isoformat()
checks=dict(UTC=now,status='SOURCE_INITIAL_CHECKPOINT_AND_LITERAL_OUTPUT_DATA_AUTHENTICATED',
    source_regular_files=len(sf),source_child_directories=len(sd),all163source_bytes_modes_exact=True,
    original_INITIAL21files1dir_unchanged=True,original_CHECKPOINT38files3dirs_unchanged=True,
    native_code_copy=pin(R/'native-run/exact_controls.py',R),native_scientific_invocations=1,native_actual_exit=0,native_stderr_empty=True,
    complete_native_stdout_JSON_read_as_data=result,external_primary_reference_pins=external,
    cached_primary_live_equivalence_asserted=False,
    source_final=pin(S/'SOURCE_FINAL.json',S),source_manifest=pin(S/'SOURCE_MANIFEST.json',S),
    own_data_comparator_whole_body_read_before_execution=True,
    mathematical_or_project_code_imported_or_executed_by_this_utility=False)
create('DATA_CHECKS.json',checks)
files,dirs=inv(R)
manifest=dict(schema='whole-owned-scientific-scope-manifest-v1',UTC=now,payload_files=files,directories=dirs,
    root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),exact_excluded_terminal_controls=['MANIFEST.json','FINAL.json'],
    includes_all_ignored_empty_files_and_modes=True,no_future_carveouts=True)
create('MANIFEST.json',manifest)
final=dict(schema='source-first-scientific-scope-final-v1',UTC=now,record='23384924',row=176,
    family='scope-primary-literature-sol',model_preference='GPT-6.1 Sol Ultra',
    status='FROZEN_COMPLETE_FINDINGS_CLOSED_PENDING_ROOT_SOURCE_FIRST_GATE',
    disposition='FULL_STATED_QUALITATIVE_THEOREM_AND_REDUCTION_BOUNDARY_PROPOSITION_SUPPORTED',
    substantive_mathematical_gap_found=None,repair_or_narrowed_promotion=False,
    exact_unresolved_limits=['Full Jenkins1960 derivative-bound overlap unverified',
        'Full Aleksandrov–Popova1973 solved-case overlap unverified',
        'No novelty/firstness/current-openness or exhaustive literature certification',
        'No sharp radius/general extremizer/explicit upper-gap formula claimed',
        'Finite exact controls are not a formal universal proof certificate'],
    report=pin(R/'REPORT.md',R),manifest=pin(R/'MANIFEST.json',R),data_checks=pin(R/'DATA_CHECKS.json',R),
    source_final=pin(S/'SOURCE_FINAL.json',S),initial_seal=pin(R/'INITIAL_SEAL.json',R),checkpoint=pin(R/'CHECKPOINT.json',R),
    full_actual293line_TeX_all5PDFtext_pages_and5fresh_source_pixels_personally_read=True,
    source163files21dirs_initial21files1dir_checkpoint38files3dirs_byte_modes_unchanged=True,
    source_first_hand_results_preceded_support_code_primaries_and_archived_opinions=True,
    informed_prior_related_exposure_disclosed=True,
    archived_source_binding_and_Rodemich_addendum_exposure_after_INITIAL_disclosed=True,
    current176root_peer_or_other_family_findings_read=False,
    native_scientific_invocations=1,native_actual_exit=0,native_stderr_empty=True,
    native_retry_install_optimized_or_exploration_campaign=False,
    primary_readset=pin(R/'PRIMARY_READSET.json',R),execution_receipt=pin(R/'EXECUTION_RECEIPT.json',R),access_limits=pin(R/'ACCESS_LIMITS.json',R),
    external_primary_reference_pins=external,
    follow_up=None,completion_percent_assigned_family=100,
    finite_extent=dict(regular_files=len(files)+2,child_directories=len(dirs),payload_regular_files=len(files),
        all_paths=sorted([p['path'] for p in files]+['MANIFEST.json','FINAL.json']),directories=dirs),
    all_writes_confined_to_owned_scope_folder=True,publication_or_W_Git_Sheet_deploy_Zenodo_authority=False,
    parent_handoff_readiness_pins_extent_only=True,quiescent_after_seal=True,self_hash_excluded=True)
create('FINAL.json',final)
af,ad=inv(R)
if len(af)!=len(files)+2 or ad!=dirs:raise RuntimeError('finite terminal extent mismatch')
for p in files:
    if pin(R/p['path'],R)!=p:raise RuntimeError('payload changed during seal')
print(json.dumps(dict(FINAL=pin(R/'FINAL.json',R),MANIFEST=pin(R/'MANIFEST.json',R),regular_files=len(af),child_directories=len(ad)),indent=2))
