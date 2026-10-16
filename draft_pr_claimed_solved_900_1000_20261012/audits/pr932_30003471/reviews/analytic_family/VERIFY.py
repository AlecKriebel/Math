"""Verify this audit against an externally supplied MANIFEST.json SHA256 pin.

Usage: python3 VERIFY.py --manifest-sha256 <digest>
The manifest deliberately excludes itself. Private primary bodies/renderings are
not public-map members and are not required to verify the curated audit files.
"""
from pathlib import Path
import argparse,hashlib,json,re,stat
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
if not re.fullmatch('[0-9a-f]{64}',a.manifest_sha256):raise SystemExit('invalid external digest')
r=Path(__file__).resolve().parent
m=r/'MANIFEST.json';raw=m.read_bytes();got=hashlib.sha256(raw).hexdigest()
if got!=a.manifest_sha256:raise SystemExit('external manifest digest mismatch')
d=json.loads(raw)
expected={'AUDIT.md','RESULT.json','INITIAL_RECONSTRUCTION.md','RESEARCH_LOG.md','AUTH_START.json','AUTH_END.json','analytic_checks.py','CHECK_RESULTS.json','SOURCE_PINS.json','VERIFY.py'}
if set(d['curated_public_allowlist'])!=expected or set(d['files'])!=expected:raise SystemExit('allowlist mismatch')
if 'MANIFEST.json' in d['files']:raise SystemExit('manifest must be self-excluded')
for rel,e in d['files'].items():
 if Path(rel).is_absolute() or '..' in Path(rel).parts or rel.startswith('private/'):raise SystemExit('unsafe/public private path')
 f=r/rel
 if not stat.S_ISREG(f.lstat().st_mode):raise SystemExit('nonregular member '+rel)
 b=f.read_bytes()
 if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise SystemExit('member digest mismatch '+rel)
extra={f.name for f in r.iterdir() if f.is_file()}-expected-{'MANIFEST.json'}
if extra:raise SystemExit('unmapped top-level files '+repr(extra))
for n in ['AUTH_START.json','AUTH_END.json']:
 if not json.loads((r/n).read_text())['all_ok']:raise SystemExit('original authentication failed')
if not json.loads((r/'CHECK_RESULTS.json').read_text())['all_expected_checks_pass']:raise SystemExit('finite check failed')
res=json.loads((r/'RESULT.json').read_text())
if res['required_issues'] or res['exact_mathematical_remaining_gap'] is not None:raise SystemExit('claimed pass has unresolved required issue')
print(json.dumps({'verified':True,'external_manifest_sha256':got,'public_members':len(expected),'self_excluded':True,'private_bodies_and_renders_excluded':True},indent=2))
