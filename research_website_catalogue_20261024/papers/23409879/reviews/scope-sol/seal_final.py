"""Data-only finite closure: no project/native imports, network, or scientific execution."""
from pathlib import Path
import hashlib
import json
import stat
from datetime import datetime, timezone

R = Path(__file__).resolve().parent
S = R.parents[1] / 'sources'

def pin(p, root):
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError('not a regular file: ' + str(p))
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), bytes=len(b),
                SHA256=hashlib.sha256(b).hexdigest(), mode=oct(stat.S_IMODE(st.st_mode)))

def inventory(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        st = p.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(pin(p, root))
        elif stat.S_ISDIR(st.st_mode):
            dirs.append(dict(path=p.relative_to(root).as_posix(), mode=oct(stat.S_IMODE(st.st_mode))))
        else:
            raise RuntimeError('unexpected object: ' + str(p))
    return files, dirs

def create(name, data):
    with (R / name).open('x') as f:
        f.write(json.dumps(data, indent=2) + '\n')

if (R / 'FINAL.json').exists() or (R / 'MANIFEST.json').exists():
    raise RuntimeError('already sealed')
custody = json.loads((R / 'SOURCE_CUSTODY.json').read_text())
sf, sd = inventory(S)
if sf != custody['files'] or sd != custody['directories']:
    raise RuntimeError('source drift')
initial = json.loads((R / 'INITIAL_MANIFEST.json').read_text())
for expected in initial['payload_files']:
    if pin(R / expected['path'], R) != expected:
        raise RuntimeError('initial payload drift')
for name, digest in {
    'INITIAL_MANIFEST.json':'040ca9503d696d1360130388457a5a4ca18640cff8967ccfc2278fbba70e2a70',
    'INITIAL_SEAL.json':'833bc2dc68db3cb011a51ef1c9e59c45396825a79fde8871fc3efc416148b3b2'
}.items():
    if pin(R / name, R)['SHA256'] != digest:
        raise RuntimeError('initial control drift')
for d in initial['directories']:
    if oct(stat.S_IMODE((R / d['path']).lstat().st_mode)) != d['mode']:
        raise RuntimeError('initial directory drift')
if oct(stat.S_IMODE(S.lstat().st_mode)) != custody['root_mode']:
    raise RuntimeError('source root mode drift')
checks = json.loads((R / 'DATA_CHECKS.json').read_text())
if checks['status'] != 'DATA_GUARDS_AND_ALL_OUTPUT_RECORDS_INSPECTED':
    raise RuntimeError('missing data inspection')
files, dirs = inventory(R)
now = datetime.now(timezone.utc).isoformat()
manifest = dict(schema='whole-owned-scope-final-manifest-v1', UTC=now,
    root_mode=oct(stat.S_IMODE(R.lstat().st_mode)), payload_files=files, directories=dirs,
    exact_excluded_terminal_controls=['MANIFEST.json','FINAL.json'],
    includes_ignored_and_empty_files=True, no_future_carveouts=True)
create('MANIFEST.json', manifest)
final = dict(schema='source-first-scientific-scope-final-v1', UTC=now,
    record='23409879', row=174, family='scope-import-sol', model_preference='GPT-6.1 Sol Ultra',
    status='FROZEN_COMPLETE_SCOPE_FAMILY_FINDINGS_CLOSED_PENDING_ROOT_GATE',
    scientific_disposition='FULL_ORIGINAL_LEAST_PERIOD_THEOREM_SUPPORTED_WITHIN_STATED_DOMAIN',
    substantive_mathematical_gap_found=None, repair_or_narrowed_promotion=False,
    report=pin(R/'REPORT.md',R), manifest=pin(R/'MANIFEST.json',R),
    initial_seal=pin(R/'INITIAL_SEAL.json',R), initial_manifest=pin(R/'INITIAL_MANIFEST.json',R),
    source_final=pin(S/'SOURCE_FINAL.json',S), source_manifest=pin(S/'SOURCE_MANIFEST.json',S),
    all77source_files10dirs_bytes_modes_unchanged=True,
    original25_initial_files1dir_unchanged=True,
    personally_read_entire393_line_manuscript_6PDF_text_pages_and6_fresh_pixels=True,
    informed_prior_related_exposure_disclosed=True,
    independent_source_first_hand_results_frozen_before_support_and_foreign_bodies=True,
    current174root_peer_other_family_findings_accessed=False,
    actual_primary_readset=pin(R/'PRIMARY_READSET.json',R),
    execution_receipt=pin(R/'EXECUTION_RECEIPT.json',R),
    access_and_literal_error_limits=pin(R/'ACCESS_LIMITS.json',R),
    native_scientific_invocations=1, native_actual_exit=0, native_stderr_empty=True,
    native_retry_install_optimized_or_campaign=False,
    archived_expected_opinion_result_bodies_read=False,
    standard_history_firstness_or_human_review_certified=False,
    exact_remaining_limits=['No direct journal-numbering body authentication',
        'No historical novelty/priority certification', 'No exhaustive literature review',
        'Finite numerical diagnostics are not interval-certified proof',
        'No proof-assistant verification or replay of every archived verifier'],
    follow_up=None, percent_completion_assigned_family=100,
    finite_extent=dict(regular_files=len(files)+2, child_directories=len(dirs),
        payload_regular_files=len(files), terminal_controls=['MANIFEST.json','FINAL.json'],
        all_paths=sorted([x['path'] for x in files]+['MANIFEST.json','FINAL.json']),
        directories=dirs),
    publication_or_W_Git_Sheet_deploy_Zenodo_action_authority=False,
    all_writes_confined_to_owned_scope_folder=True,
    parent_handoff_readiness_pins_extent_status_only=True,
    quiescent_after_seal=True, self_hash_excluded=True)
create('FINAL.json', final)
actual_files, actual_dirs = inventory(R)
if len(actual_files) != len(files)+2 or actual_dirs != dirs:
    raise RuntimeError('terminal finite extent mismatch')
for p in files:
    if pin(R / p['path'], R) != p:
        raise RuntimeError('payload changed during seal')
print(json.dumps(dict(FINAL=pin(R/'FINAL.json',R), MANIFEST=pin(R/'MANIFEST.json',R),
    regular_files=len(actual_files), child_directories=len(actual_dirs)), indent=2))
