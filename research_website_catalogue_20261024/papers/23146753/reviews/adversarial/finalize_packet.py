"""One-shot seal creation. Do not rerun or modify a sealed packet."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys

HERE = Path(__file__).resolve().parent
stamp = lambda: datetime.now(timezone.utc).isoformat()
def bind(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
if (HERE/'FINAL_MANIFEST.json').exists() or (HERE/'FINAL_SEAL.json').exists():
    raise SystemExit('Immutable final packet already exists; refusing rerun.')
run = subprocess.run([sys.executable,str(HERE/'verify_packet.py')],cwd=HERE,capture_output=True,timeout=30)
if run.returncode or run.stderr:
    raise RuntimeError(run.stderr.decode() or run.stdout.decode())
write('VERIFICATION.json',dict(utc=stamp(), phase='preseal', exit_code=run.returncode,
    result=json.loads(run.stdout), read_only_verifier_sha256=bind(HERE/'verify_packet.py')['sha256']))
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n{stamp()} — final checkpoint:100% of this independent adversarial lane. Full original theorem reviewed without repair or narrowing; derivations, actual primary interfaces, independent exact attacks and bounded source replay complete. All47 original bindings /25 before-source files /13 ZIP members and earlier protected seals verify unchanged. Publication and root adoption remain separate and false/null. Estimated remaining lane work:0 minutes; root final reading remains outside this lane.\n')
owned = {str(p.relative_to(HERE)):bind(p) for p in sorted(HERE.rglob('*')) if p.is_file()}
custody=json.loads((HERE/'CUSTODY.json').read_text())
write('FINAL_MANIFEST.json',dict(utc=stamp(), immutable=True, record_id='23146753',
    owned_bindings=owned, owned_count=len(owned),
    original_bindings=custody['original_bindings'],
    private_cache_included_for_custody_but_ignored=True,
    no_publication_authority=True))
write('FINAL_SEAL.json',dict(utc=stamp(), immutable=True, status='COMPLETE_INDEPENDENT_ADVERSARIAL_PACKET',
    record_id='23146753', manifest_binding=bind(HERE/'FINAL_MANIFEST.json'), owned_files=len(owned),
    original_bindings=len(custody['original_bindings']), report_binding=bind(HERE/'REPORT.md'),
    verdict_binding=bind(HERE/'VERDICT.json'), early_seal_binding=bind(HERE/'INITIAL_SEAL.json'),
    publication_authority=False, root_adoption=None, followup=None,
    limitations='Mathematical review and exact finite diagnostics; not human peer review, formal certification, or historical first-priority certification.'))
print(json.dumps(dict(seal=bind(HERE/'FINAL_SEAL.json'),manifest=bind(HERE/'FINAL_MANIFEST.json'),owned_files=len(owned)),indent=2))
