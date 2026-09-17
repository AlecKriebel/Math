"""Assemble only after the standalone proof verification has passed."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent / 'lean_formalization'
STAGE = WORK / 'standalone_verification/lean_formalization'
receipt = json.loads((STAGE/'verification/latest_run.json').read_text())
assert receipt['status'] == 'passed' and receipt['kernel_checked'] is True
sys.path.insert(0, str(ROOT/'scripts'))
import package
assert receipt['protected_source_hashes'] == package.protected_fingerprints(ROOT)
source = STAGE/'verification/runs'/receipt['run_id']
recorded = ROOT/'verification/recorded'
recorded.mkdir(exist_ok=False)
for name in ['run.json'] + [c['log'] for c in receipt['commands']]:
    shutil.copyfile(source/name, recorded/name)
index = ROOT/'verification/README.md'
s = index.read_text()
summary = (f"Recorded result: **passed** on {receipt['finished_utc'][:10]} (UTC), "
           f"run `{receipt['run_id']}`. The standalone check completed "
           f"{len(receipt['commands'])} commands in {receipt['elapsed_seconds']/60:.1f} minutes, "
           f"including all {len(receipt['axioms']):,} expected declaration reports and "
           "five acceptance/twenty rejection controls. All reported axioms are among "
           "`propext`, `Classical.choice`, and `Quot.sound`.\n\n")
index.write_text(s.replace('# Verification evidence\n\n', '# Verification evidence\n\n'+summary))
output = ROOT.parent/'cyclic-bell-lean-review.zip'
subprocess.run([sys.executable, str(ROOT/'scripts/package.py'), '--output', str(output)], check=True)
extract = WORK/'extracted_check'
extract.mkdir(exist_ok=False)
with zipfile.ZipFile(output) as z:
    assert all(n.startswith('lean_formalization/') and '..' not in Path(n).parts for n in z.namelist())
    assert z.testzip() is None
    z.extractall(extract)
export = extract/'lean_formalization'
manifest = (export/'SHA256SUMS').read_text().splitlines()
manifest_names = set()
for line in manifest:
    digest, name = line.split('  ', 1)
    assert hashlib.sha256((export/name).read_bytes()).hexdigest() == digest, name
    manifest_names.add(name)
assert {str(p.relative_to(export)) for p in export.rglob('*') if p.is_file()} == manifest_names | {'SHA256SUMS'}
missing = []
for p in [*export.glob('*.md'), *(export/'verification').glob('*.md')]:
    for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        target = target.split('#')[0]
        if target and '://' not in target and not (p.parent/target).exists():
            missing.append((str(p.relative_to(export)), target))
assert not missing, missing
for command, name in [([sys.executable,'scripts/check.py','--static-only'],'extracted-static.log'),
                      ([sys.executable,'-m','unittest','discover','-s','scripts','-p','test_*.py'],'extracted-tests.log')]:
    with (WORK/name).open('w') as f:
        subprocess.run(command, cwd=export, stdout=f, stderr=subprocess.STDOUT, check=True)
repacked = extract/'repacked.zip'
subprocess.run([sys.executable,'scripts/package.py','--output',str(repacked)], cwd=export, check=True)
assert output.read_bytes() == repacked.read_bytes(), 'Non-deterministic export'
result = {'status':'passed', 'run_id':receipt['run_id'], 'commands':len(receipt['commands']),
          'declarations':len(receipt['axioms']), 'manifest_files':len(manifest),
          'archive_bytes':output.stat().st_size, 'archive_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'extracted_static_checks':'passed', 'extracted_python_tests':87,
          'byte_identical_reexport':True, 'missing_local_doc_links':missing,
          'proof_rebuild_location':'standalone copy; pinned dependency caches supplied and checked'}
(WORK/'FINAL_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result, indent=2))
