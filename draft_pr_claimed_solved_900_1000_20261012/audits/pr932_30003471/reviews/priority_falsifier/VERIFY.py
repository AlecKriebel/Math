"""Read-only package/original authentication plus deterministic diagnostic replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]; AUDIT=HERE.parents[1]
manifest=json.loads((HERE/'MANIFEST.json').read_text())
assert manifest['self_excluded'] is True
assert manifest['file_count']==len(manifest['files'])
for e in manifest['files']:
 p=HERE/e['path'];assert p.is_file(),e['path'];b=p.read_bytes()
 assert len(b)==e['bytes'],e['path']
 assert hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
 assert not any(s in p.relative_to(HERE).parts for s in ('private','tmp','renders')),e['path']
head='c09ef9df8b1f4642be0396ba6343344be8fa25b0'; prefix='unsolved_math_prioritization/attempts/30003471/'
run=lambda *a:subprocess.check_output(a,cwd=ROOT)
paths=run('git','ls-tree','-r','--name-only',head,'--',prefix).decode().splitlines();assert len(paths)==29
for f in paths:assert run('git','show',head+':'+f)==(AUDIT/'original'/f).read_bytes(),f
proof=AUDIT/'original'/prefix/'public/PROOF.md'
assert hashlib.sha256(proof.read_bytes()).hexdigest()=='6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415'
subprocess.run([sys.executable,str(HERE/'CONTROLS.py')],check=True,stdout=subprocess.DEVNULL)
assert json.loads((HERE/'CONTROL_RESULTS.json').read_text())['all_passed']
# Replay output is deterministic and must still match its seal.
for e in manifest['files']:
 assert hashlib.sha256((HERE/e['path']).read_bytes()).hexdigest()==e['sha256']
print(json.dumps({'verified':True,'public_file_count':manifest['file_count'],'original_file_count':29,'all_original_disk_equal_actual_git':True,'controls_replayed':True,'manifest_sha256':hashlib.sha256((HERE/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))
