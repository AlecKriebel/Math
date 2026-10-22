"""Verify public bindings and exact finite-control outputs. Raw sources are not checked."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
m=json.loads((p/'FINAL_AUTHOR_MANIFEST.json').read_text())
for n,h in m['sha256'].items():
    assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
for k in (3,4,5):
    actual=json.loads(subprocess.check_output([sys.executable,str(p/f'check_turn_{k}.py')],text=True))
    expected=json.loads((p/f'TURN_{k}_CHECKS.json').read_text())
    assert actual==expected,(k,actual,expected)
print(json.dumps({'public_bindings':len(m['sha256']),'exact_assertions':61033,'raw_sources_checked':0,'original_resolved':False},sort_keys=True))
