"""One-shot addendum seal. Never rerun after finalization."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent
def bind(p):return dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(O/n).write_text(json.dumps(d,indent=2)+'\n')
utc=lambda:datetime.now(timezone.utc).isoformat()
if (O/'FINAL_SEAL.json').exists() or (O/'FINAL_MANIFEST.json').exists():raise SystemExit('Immutable packet exists')
r=subprocess.run([sys.executable,str(O/'verify_reconciliation.py')],capture_output=True,timeout=30)
if r.returncode or r.stderr:raise RuntimeError(r.stderr.decode())
write('VERIFICATION.json',dict(utc=utc(),phase='preseal',result=json.loads(r.stdout)))
with(O/'RESEARCH_LOG.md').open('a')as f:f.write(f'\n{utc()} — finalcheckpoint100% of bounded dependencyreconciliation. Central importedfiniteproofgap preciselydocumented; no structuralcounterexample/repair/narrowedsubstitute. All449 earlierbindingsunchanged. Rootdispositionandall203programmecontinue separately. Remainingboundedlanework0minutes.\n')
owned={str(p.relative_to(O)):bind(p) for p in sorted(O.rglob('*')) if p.is_file()}
write('FINAL_MANIFEST.json',dict(utc=utc(),immutable=True,record_id='22395326',owned_bindings=owned,
 original_bindings=json.loads((O/'BEFORE_BINDINGS.json').read_text())['files'],
 private_cache_ignored=True,all_three_current_scientific_families_preserved=True))
write('FINAL_SEAL.json',dict(utc=utc(),immutable=True,status='COMPLETE_BOUNDED_DEPENDENCY_RECONCILIATION',
 manifest_binding=bind(O/'FINAL_MANIFEST.json'),owned_files=len(owned),original_bindings=449,
 report_binding=bind(O/'REPORT.md'),verdict_binding=bind(O/'VERDICT.json'),
 source_repair=False,full_atlas_rerun=False,publication_authority=False,root_adoption=None,followup=None))
print(json.dumps(dict(seal=bind(O/'FINAL_SEAL.json'),manifest=bind(O/'FINAL_MANIFEST.json'),
 report=bind(O/'REPORT.md'),verdict=bind(O/'VERDICT.json'),owned=len(owned)),indent=2))
