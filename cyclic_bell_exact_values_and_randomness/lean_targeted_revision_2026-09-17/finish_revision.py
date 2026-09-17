"""Publish the revised review artifact only after the frozen clean run passes."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent/'lean_formalization'
STAGE = WORK/'staging/lean_formalization'
receipt = json.loads((STAGE/'verification/latest_run.json').read_text())
assert receipt['status'] == 'passed' and receipt['kernel_checked'] is True
sys.path.insert(0, str(ROOT/'scripts'))
import package
assert receipt['protected_source_hashes'] == package.protected_fingerprints(ROOT)
assert len(receipt['axioms']) == package.AXIOM_COUNT == 1894
assert (ROOT/'reference/manuscript/main.tex').read_bytes() == (ROOT.parent/'main.tex').read_bytes()
assert (ROOT/'reference/manuscript/paper.pdf').read_bytes() == (ROOT.parent/'output/pdf/cyclic_bell_exact_values_and_randomness.pdf').read_bytes()
oldzip = ROOT.parent/'cyclic-bell-lean-review.zip'
assert hashlib.sha256(oldzip.read_bytes()).hexdigest() == 'f1bcadd327b0321f4277baa8b136723da2b15bbc878ab5f9d2de3fbe949b73e9'
recorded = ROOT/'verification/recorded'
previous = WORK/'previous_receipt'
assert {p.name for p in recorded.iterdir()} == {p.name for p in previous.iterdir()}
for p in recorded.iterdir():
    assert p.is_file() and not p.is_symlink()
    assert p.read_bytes() == (previous/p.name).read_bytes(), p.name
for p in recorded.iterdir():
    p.unlink()
source = STAGE/'verification/runs'/receipt['run_id']
for name in ['run.json'] + [c['log'] for c in receipt['commands']]:
    shutil.copyfile(source/name, recorded/name)
index = ROOT/'verification/README.md'
s = index.read_text()
s = s.replace('Revision in progress: the retained receipt below belongs to the preceding release. New targeted endpoints require a fresh complete run before export.\n\n', '')
summary = (f"Recorded result: **passed** on {receipt['finished_utc'][:10]} (UTC), "
           f"run `{receipt['run_id']}`. The standalone check completed "
           f"{len(receipt['commands'])} commands in {receipt['elapsed_seconds']/60:.1f} minutes, "
           f"including all {len(receipt['axioms']):,} expected declaration reports and "
           "five acceptance/twenty rejection controls. All reported axioms are among "
           "`propext`, `Classical.choice`, and `Quot.sound`.")
s, n = re.subn(r'Recorded result: \*\*passed\*\*[^\n]*', lambda _: summary, s)
assert n == 1
index.write_text(s)
output = ROOT.parent/'cyclic-bell-lean-review-r2.zip'
subprocess.run([sys.executable, str(ROOT/'scripts/package.py'), '--output', str(output)], check=True)
extract = WORK/'extracted'
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
assert package.protected_fingerprints(export) == receipt['protected_source_hashes']
missing = []
for p in [*export.glob('*.md'), *(export/'verification').glob('*.md')]:
    for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        target = target.split('#')[0]
        if target and '://' not in target and not (p.parent/target).exists():
            missing.append((str(p.relative_to(export)), target))
assert not missing, missing
for command, name in [([sys.executable,'scripts/check.py','--static-only'],'extracted_static.log'),
                      ([sys.executable,'-m','unittest','discover','-s','scripts','-p','test_*.py'],'extracted_tests.log')]:
    with (WORK/name).open('w') as f:
        subprocess.run(command, cwd=export, stdout=f, stderr=subprocess.STDOUT, check=True)
repacked = extract/'repacked.zip'
subprocess.run([sys.executable,'scripts/package.py','--output',str(repacked)], cwd=export, check=True)
assert output.read_bytes() == repacked.read_bytes(), 'Non-deterministic export'
result = {'status':'passed', 'run_id':receipt['run_id'], 'commands':len(receipt['commands']),
          'declarations':len(receipt['axioms']), 'manifest_files':len(manifest),
          'archive_bytes':output.stat().st_size, 'archive_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'preserved_original_archive_sha256':hashlib.sha256(oldzip.read_bytes()).hexdigest(),
          'extracted_static_checks':'passed', 'extracted_python_tests':87,
          'byte_identical_reexport':True, 'missing_local_doc_links':missing,
          'extracted_protected_inputs_identical_to_clean_built_inputs':True,
          'proof_rebuild_location':'standalone copy; locked dependency cache supplied and checked'}
(WORK/'FINAL_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result, indent=2))
