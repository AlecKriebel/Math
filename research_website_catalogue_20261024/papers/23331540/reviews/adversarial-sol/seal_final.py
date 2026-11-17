"""Data-only final closure; never executes/imports source or scientific programs."""
from pathlib import Path
import hashlib, json, stat, datetime

R = Path(__file__).resolve().parent
S = R.parents[1] / 'sources'

def pin(p, root):
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError('not regular: ' + str(p))
    data = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), bytes=len(data),
                SHA256=hashlib.sha256(data).hexdigest(), mode=stat.S_IMODE(st.st_mode))

def inventory(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        st = p.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(pin(p, root))
        elif stat.S_ISDIR(st.st_mode):
            dirs.append(dict(path=p.relative_to(root).as_posix(), mode=stat.S_IMODE(st.st_mode)))
        else:
            raise RuntimeError('nonregular topology: ' + str(p))
    return files, dirs

def create(name, value):
    with (R / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

for name in ('CLOSING_GUARDS.json', 'MANIFEST.json', 'FINAL.json'):
    if (R / name).exists():
        raise RuntimeError('already sealed: ' + name)
custody = json.loads((R / 'SOURCE_CUSTODY.json').read_text())
sf, sd = inventory(S)
if sf != custody['files'] or sd != custody['directories']:
    raise RuntimeError('source drift')
if stat.S_IMODE(S.lstat().st_mode) != custody['root_mode']:
    raise RuntimeError('source root mode drift')
for name, digest in (
    ('INITIAL_SEAL.json', '8c33f3a20d610cb228a57705778e6035d6578e716e9834115ebc7b939a15e090'),
    ('INITIAL_MANIFEST.json', '7871fd7da61692e874f1cc6e0d30791f1ef004311a44eece622bfe5843b82ca6')):
    if pin(R / name, R)['SHA256'] != digest:
        raise RuntimeError('INITIAL control drift: ' + name)
im = json.loads((R / 'INITIAL_MANIFEST.json').read_text())
for q in im['payload_files']:
    if pin(R / q['path'], R) != q:
        raise RuntimeError('INITIAL payload drift: ' + q['path'])
for d in im['directories']:
    st = (R / d['path']).lstat()
    if not stat.S_ISDIR(st.st_mode) or stat.S_IMODE(st.st_mode) != d['mode']:
        raise RuntimeError('INITIAL directory mode drift')
if stat.S_IMODE(R.lstat().st_mode) != im['root_mode']:
    raise RuntimeError('owned root mode drift')
for name in ('SOURCE_AUTH.stderr.txt', 'PDFINFO.stderr.txt', 'PDFTEXT.stderr.txt',
             'RASTER.stdout.txt', 'RASTER.stderr.txt', 'native-check.stderr.txt'):
    if (R / name).read_bytes() != b'':
        raise RuntimeError('nonempty literal error stream: ' + name)
base = S / 'published-source/container-001/tree/full_stress_stratifications_v1'
if (R / 'native-check.stdout.json').read_bytes() != (base / 'expected/independent_exact_check.json').read_bytes():
    raise RuntimeError('native output differs from supplied reference')
native = json.loads((R / 'native-check.stdout.json').read_text())
if native['verdict'] != 'PASS' or native['total_graphs'] != 1099 or native['total_missing_edge_witnesses'] != 5325:
    raise RuntimeError('unexpected native finite result')
run = json.loads((R / 'NATIVE_RUN.json').read_text())
if run['exit_code'] != 0 or run['native_check_invocations'] != 1 or run['optimization'] != 0:
    raise RuntimeError('inconsistent literal execution receipt')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
create('CLOSING_GUARDS.json', dict(UTC=now, status='PASS_DATA_CUSTODY_AND_LITERAL_STREAMS_ONLY',
    source_regular_files=len(sf), source_child_directories=len(sd),
    all_source_bytes_modes_topology_unchanged=True, all_INITIAL20files1dir_unchanged=True,
    initial_seal=pin(R / 'INITIAL_SEAL.json', R), source_final=pin(S / 'SOURCE_FINAL.json', S),
    source_manifest=pin(S / 'SOURCE_MANIFEST.json', S),
    native_stdout=pin(R / 'native-check.stdout.json', R), native_stderr=pin(R / 'native-check.stderr.txt', R),
    exact_supplied_reference_match=True,
    source_code_readset=[pin(base / name, S) for name in (
        'run_checks.py', 'checks/independent_exact_check.py', 'checks/independent_kernel_check.py',
        'checks/check_collision_witness.py', 'expected/independent_exact_check.json', 'README.md', 'SUPPLEMENT.md')],
    empty_tool_streams=[pin(R / name, R) for name in (
        'SOURCE_AUTH.stderr.txt', 'PDFINFO.stderr.txt', 'PDFTEXT.stderr.txt', 'RASTER.stdout.txt',
        'RASTER.stderr.txt', 'native-check.stderr.txt')],
    native_ordinary_invocations=1, no_rerun_optimized_or_mutation_runner=True,
    own_sealer_full_body_read_before_execution=True))
files, dirs = inventory(R)
if len(files) != 28 or len(dirs) != 1:
    raise RuntimeError('unexpected final owned extent')
create('MANIFEST.json', dict(schema='whole-finite-independent-adversarial-manifest-v1', UTC=now,
    root_mode=stat.S_IMODE(R.lstat().st_mode), payload_files=files, directories=dirs,
    exact_terminal_exclusions=['MANIFEST.json', 'FINAL.json'],
    includes_all_ignored_empty_bytes_and_modes=True))
create('FINAL.json', dict(schema='independent-adversarial-full-original-final-v1', UTC=now,
    row=183, record='23331540', model_preference='GPT-6.1 Sol Ultra',
    status='FROZEN_PASS_FULL_ORIGINAL_AS_EXPLICITLY_STATED',
    exact_disposition='RECONSTRUCTION_COROLLARY_AMBIENT_BOUNDARY_AND_EXPLICIT_LITERAL_PRIMARY_INTERFACE_VERIFIED',
    substantive_defect_found=False, central_remaining_gap=None, source_repair_or_narrowed_promotion=False,
    report=pin(R / 'REPORT.md', R), manifest=pin(R / 'MANIFEST.json', R),
    initial_seal=pin(R / 'INITIAL_SEAL.json', R), initial_hand_results=pin(R / 'INITIAL_HAND_RESULTS.md', R),
    primary_access=pin(R / 'PRIMARY_ACCESS.json', R), native_run=pin(R / 'NATIVE_RUN.json', R),
    closing_guards=pin(R / 'CLOSING_GUARDS.json', R), post_initial_log=pin(R / 'POST_INITIAL_LOG.md', R),
    source_final=pin(S / 'SOURCE_FINAL.json', S), source133files14dirs_and_INITIAL20files1dir_unchanged=True,
    current_root_peer_and_archived_evidence_report_bodies_opened=False,
    native_overview_prior_assertions_seen_postseal_not_adopted_as_authority=True,
    native_scientific_invocations=1, ordinary_optimization0=True, execution_exit=0, stderr_bytes=0,
    literal_access_limits_retained=True,
    limits=['Exact explicit literal fixed-label/full-space convention, not unwritten author intent',
        'Final DKS/Panina journal bodies/numbering not newly verified; actual cited author interfaces read',
        'No raw primary download/byte equivalence or whole DKS/Panina paper reading claim',
        'No exhaustive novelty, formal proof-assistant or human-peer-review certificate',
        'Finite native checks support formulas; written proof establishes universal connectedness'],
    follow_up=None, completion_percent=100,
    all_writes_confined_to_owned_folder=True, publication_or_source_W_Git_Sheet_Zenodo_deploy_authority=False,
    external_contact_or_prepared_outreach=False,
    extent=dict(regular_files=len(files)+2, child_directories=len(dirs),
        all_paths=sorted([q['path'] for q in files]+['MANIFEST.json', 'FINAL.json']), directories=dirs),
    all_handles_terminal=True, quiescent_after_seal=True, terminal_self_hash_excluded=True))
af, ad = inventory(R)
if len(af) != len(files)+2 or ad != dirs:
    raise RuntimeError('finite extent drift while sealing')
for q in files:
    if pin(R / q['path'], R) != q:
        raise RuntimeError('payload drift while sealing: ' + q['path'])
print(json.dumps(dict(FINAL=pin(R / 'FINAL.json', R), MANIFEST=pin(R / 'MANIFEST.json', R),
    REPORT=pin(R / 'REPORT.md', R), regular_files=len(af), child_directories=len(ad), quiescent=True), indent=2))
