"""Finite source-first seal only; data hashing, no science/code imports or external actions."""
from pathlib import Path
import datetime, hashlib, json, stat

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

def create(name, obj):
    with (R / name).open('x') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

for name in ('INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'):
    if (R / name).exists():
        raise RuntimeError('already sealed: ' + name)
custody = json.loads((R / 'SOURCE_CUSTODY.json').read_text())
sf, sd = inventory(S)
if sf != custody['files'] or sd != custody['directories']:
    raise RuntimeError('source drift before initial seal')
if stat.S_IMODE(S.lstat().st_mode) != custody['root_mode']:
    raise RuntimeError('source root mode drift')
for name in ('SOURCE_AUTH.stderr.txt', 'PDFINFO.stderr.txt', 'PDFTEXT.stderr.txt',
             'RASTER.stdout.txt', 'RASTER.stderr.txt'):
    if (R / name).read_bytes() != b'':
        raise RuntimeError('unexpected source tool stream: ' + name)
fs, ds = inventory(R)
if len(fs) != 18 or len(ds) != 1:
    raise RuntimeError('unexpected owned finite extent')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
create('INITIAL_MANIFEST.json', dict(schema='source-first-adversarial-initial-manifest-v1', UTC=now,
    root_mode=stat.S_IMODE(R.lstat().st_mode), payload_files=fs, directories=ds,
    exact_terminal_exclusions=['INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'],
    includes_all_ignored_and_empty_file_bytes_modes=True))
create('INITIAL_SEAL.json', dict(schema='source-first-adversarial-initial-seal-v1', UTC=now,
    row=183, record='23331540', status='FROZEN_SOURCE_FIRST_HAND_RESULTS_AWAIT_CHECKPOINT_RESUME',
    model_preference='GPT-6.1 Sol Ultra',
    manifest=pin(R / 'INITIAL_MANIFEST.json', R), initial=pin(R / 'INITIAL.md', R),
    hand_results=pin(R / 'INITIAL_HAND_RESULTS.md', R), readset=pin(R / 'INITIAL_READSET.json', R),
    log=pin(R / 'RESEARCH_LOG.md', R), custody=pin(R / 'SOURCE_CUSTODY.json', R),
    source_final=pin(S / 'SOURCE_FINAL.json', S), source_manifest=pin(S / 'SOURCE_MANIFEST.json', S),
    source_extent=dict(regular_files=len(sf), child_directories=len(sd)),
    all_source_bytes_modes_topology_unchanged=True,
    actual_full180line_TeX_and_all3PDFtext_and_fresh_pixels_read=True,
    supporting_program_result_archived_review_foreign_body_current_peer_root_bodies_opened=False,
    native_scientific_or_old_helper_executions=0,
    data_authentication_pdfinfo_pdftotext_pdftoppm_exits=[0, 0, 0, 0],
    prior_related_project_exposure_disclosed=True,
    whole_original_disposition='PENDING_PRIMARY_AND_SUPPORT_REVIEW', follow_up=None,
    source_first_completion_percent=100, full_review_estimate_percent=35,
    source_W_Git_Sheet_Zenodo_deploy_or_old_packet_writes=False,
    action_or_publication_authority=False, external_contact_or_prepared_outreach=False,
    owned_extent=dict(regular_files=len(fs)+2, child_directories=len(ds),
        all_paths=sorted([q['path'] for q in fs]+['INITIAL_MANIFEST.json', 'INITIAL_SEAL.json']),
        directories=ds),
    all_handles_terminal=True, quiescent_until_explicit_root_resume=True,
    terminal_self_hash_excluded=True))
af, ad = inventory(R)
if len(af) != len(fs)+2 or ad != ds:
    raise RuntimeError('owned extent drift while sealing')
for q in fs:
    if pin(R / q['path'], R) != q:
        raise RuntimeError('payload drift while sealing: ' + q['path'])
print(json.dumps(dict(INITIAL_SEAL=pin(R / 'INITIAL_SEAL.json', R),
    INITIAL_MANIFEST=pin(R / 'INITIAL_MANIFEST.json', R),
    regular_files=len(af), child_directories=len(ad), source_files=len(sf), source_dirs=len(sd),
    quiescent=True), indent=2))
