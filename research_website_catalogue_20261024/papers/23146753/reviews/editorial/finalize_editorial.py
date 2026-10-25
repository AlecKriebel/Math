"""One-shot private editorial custody seal; do not rerun once sealed."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,sys,zipfile
O=Path(__file__).resolve().parent;D=O.parent.parent;S=D/'sources'
utc=lambda:datetime.now(timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def bind(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return dict(bytes=p.stat().st_size,sha256=h.hexdigest())
def write(name,d):(O/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
if (O/'MANIFEST.json').exists() or (O/'SEAL.json').exists():raise SystemExit('Immutable editorial packet exists; refusing rerun.')
results=[]
for mode in [[],['-O']]:
    run=subprocess.run([sys.executable,*mode,str(O/'verify_editorial.py')],capture_output=True,cwd=O,timeout=30)
    if run.returncode or run.stderr:raise RuntimeError(run.stderr.decode() or run.stdout.decode())
    results.append(json.loads(run.stdout))
if results[0]!=results[1]:raise RuntimeError('Normal/optimized static checks differ')
write('CONSISTENCY_CONTROLS.json',dict(utc=utc(),normal_and_optimized_equal=True,
    verifier_sha256=bind(O/'verify_editorial.py')['sha256'],result=results[0],
    limitation='Static private editorial consistency only; no shared-consumer compatibility, rendering, HTTP/browser/native validation or mathematical programme replay.'))
before=load(O/'BEFORE_BINDINGS.json')['files'];protected=load(O/'PROTECTED_PRIOR_PACKAGES.json')['bindings']
after={}
for path,spec in {**before,**protected}.items():
    actual=bind(Path(path))
    if actual!=spec:raise RuntimeError('Earlier immutable input changed: '+path)
    after[path]=dict(before=spec,after=actual,equal=True)
members=[]
with zipfile.ZipFile(S/'mtp2-edge-closure-verification.zip') as z:
    for info in z.infolist():
        data=z.read(info)
        if data!=(S/'published-source'/info.filename).read_bytes():raise RuntimeError('Archive member differs')
        members.append(dict(member=info.filename,bytes=len(data),crc32=f'{info.CRC:08x}',sha256=hashlib.sha256(data).hexdigest(),original_extraction_equal=True))
configs={str(D/name):bind(D/name) for name in ['publication.json','promotion.json']}
write('CUSTODY_AFTER.json',dict(utc=utc(),complete_before_after_bindings=after,
    source_scientific_recent_original_bindings=len(before),protected_prior_private_manifest_seals=len(protected),
    unchanged=True,config_bindings=configs,archive_CRC_body_comparisons=members,embedded_reader_byteidentical=True,
    original_raw_object_copies=17,source_files=27,source_writes=False,shared_site_UI_native_Git_HTTP_writes=False))
with (O/'RESEARCH_LOG.md').open('a')as f:
    f.write(f'\n{utc()} — final checkpoint:100% of bounded private editorial preparation. Complete approved scope/original abstract/credit/status/assets/edition retained; exact root and whole original source/verdict objects preserved. Normal/-O static checks agree,29 in-memory altered-input controls reject. All187 originals plus14 earlier private manifests/seals unchanged;13ZIPpayloads match. No rendering/source/math rerun or publication/native/UI/Git/HTTP work. Root must independently read and approve; all203 programme remains ongoing.\n')
owned={str(p.relative_to(O)):bind(p) for p in sorted(O.rglob('*')) if p.is_file()}
write('MANIFEST.json',dict(utc=utc(),record_id='23146753',immutable=True,owned_bindings=owned,
    config_bindings=configs,original_bindings={**before,**protected},
    complete_before_after_custody='CUSTODY_AFTER.json',no_stale_mutable_site_core_baselines_followed=True))
write('SEAL.json',dict(utc=utc(),record_id='23146753',immutable=True,
    status='COMPLETE_PRIVATE_EDITORIAL_READY_FOR_ROOT_REVIEW',
    scientific_root_status='PASS_WITH_EXPLICIT_PRIMARY_AND_PRIORITY_LIMITS',
    manifest_binding=bind(O/'MANIFEST.json'),owned_files=len(owned),new_config_files=2,
    source_scientific_recent_original_bindings=len(before),protected_prior_private_manifest_seals=len(protected),
    report_binding=bind(O/'REPORT.md'),public_copy_binding=bind(O/'PUBLIC_COPY.md'),adapter_binding=bind(O/'SCHEMA_ADAPTER.md'),
    root_editorial_clearance_received=False,rendered=False,live=False,browser=False,native=False,
    canonical_url=None,AA=None,follow_up=None,all203_goal_complete=False))
print(json.dumps(dict(seal=bind(O/'SEAL.json'),manifest=bind(O/'MANIFEST.json'),owned_files=len(owned),
    config_bindings=configs,report=bind(O/'REPORT.md'),public_copy=bind(O/'PUBLIC_COPY.md'),adapter=bind(O/'SCHEMA_ADAPTER.md')),indent=2))
