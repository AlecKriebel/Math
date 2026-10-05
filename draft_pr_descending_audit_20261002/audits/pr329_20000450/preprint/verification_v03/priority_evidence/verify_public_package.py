"""Read-only portable verifier for the exact allowlisted public subset."""
from pathlib import Path
import hashlib,json,os,subprocess,sys

if sys.flags.optimize:
    raise RuntimeError('Run without -O: verification requires assertions enabled.')
S=Path(__file__).resolve().parent
names={
 'PRIORITY_REPORT.md','MORTON_PRIOR_COMPARISON.md','VERDURE_PRIOR_COMPARISON.md',
 'GAPS_AND_LIMITS.md','VERSION_CHRONOLOGY.md','SOURCE_INVENTORY.json',
 'SEARCH_INVENTORY.json','READING_LEDGER.json','README_PUBLIC.md',
 'verify_prior_parameter_comparison.py','verify_public_package.py'}
m=json.loads((S/'PUBLIC_MANIFEST.json').read_text())
assert m['schema']=='pr329-public-priority-manifest-v1'
assert m['publication_authorization'] is False and m['self_seal'] is False
assert len(m['payloads'])==len(names)
assert {r['path'] for r in m['payloads']}==names
for r in m['payloads']:
 p=S/r['path'];assert p.parent==S and not p.is_symlink(),r['path']
 b=p.read_bytes()
 assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
 assert p.stat().st_mode&0o777==r['mode_decimal'],r['path']
 # Public bodies contain no user-specific filesystem references.
 assert (b'/'+b'Users/') not in b and (b'private_'+b'evidence/') not in b,r['path']
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
p=subprocess.run([sys.executable,'-B',str(S/'verify_prior_parameter_comparison.py')],cwd=S,env=env,capture_output=True)
assert p.returncode==0 and p.stderr==b'',p.stderr.decode(errors='replace')
x=json.loads(p.stdout);assert x['result']=='PASS' and x['exact_comparisons']==25
assert hashlib.sha256(p.stdout).hexdigest()=='81fdcb06f6c4ebafc32224aff64eb6a2c105b59151e6761b4aba11a288fb0249'
print(json.dumps({'result':'PASS','public_payloads':len(names),'exact_comparisons':25,
 'checker_stdout_bytes':len(p.stdout),'checker_stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),
 'scope':'public bodies/modes and formula conventions only; no private source dependency, firstness or publication authorization'},indent=2))
