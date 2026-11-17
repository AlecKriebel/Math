"""One documented unmodified native finite-check route in a new isolated copy."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'papers/23204212/reviews/scope-continuation-20261117'
SOURCE=P/'papers/23204212/sources/archives/01-thompson-cstar-verification.zip.extracted/upstream_finite_checks.py'
RUN=OWN/'native-run'
assert not RUN.exists() and not (OWN/'NATIVE_RUN.json').exists()
raw=SOURCE.read_bytes()
before=dict(source_path=str(SOURCE),bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),mode=oct(SOURCE.stat().st_mode&0o7777))
RUN.mkdir()
with (RUN/'upstream_finite_checks.py').open('xb') as f:f.write(raw)
os.chmod(RUN/'upstream_finite_checks.py',SOURCE.stat().st_mode&0o7777)
assert (RUN/'upstream_finite_checks.py').read_bytes()==raw
with (OWN/'NATIVE_INPUT_BEFORE.json').open('x') as f:json.dump(dict(original=before,copy_path=str(RUN/'upstream_finite_checks.py'),copy_SHA256=hashlib.sha256((RUN/'upstream_finite_checks.py').read_bytes()).hexdigest(),fresh_copy=True),f,indent=2);f.write('\n')
argv=[sys.executable,'upstream_finite_checks.py']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (OWN/'NATIVE.stdout.txt').open('xb') as out,(OWN/'NATIVE.stderr.txt').open('xb') as err:r=subprocess.run(argv,cwd=RUN,env=env,stdout=out,stderr=err,check=False)
after=dict(source_path=str(SOURCE),bytes=SOURCE.stat().st_size,SHA256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),mode=oct(SOURCE.stat().st_mode&0o7777))
copy_after=hashlib.sha256((RUN/'upstream_finite_checks.py').read_bytes()).hexdigest()
with (OWN/'NATIVE_INPUT_AFTER.json').open('x') as f:json.dump(dict(original=after,copy_path=str(RUN/'upstream_finite_checks.py'),copy_SHA256=copy_after,original_unchanged=before==after,copy_unchanged=copy_after==before['SHA256']),f,indent=2);f.write('\n')
record=dict(schema='one-current-unmodified-native-finite-route-v1',argv=argv,cwd=str(RUN),documented_route='python3 upstream_finite_checks.py',started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=r.returncode,stdout_bytes=(OWN/'NATIVE.stdout.txt').stat().st_size,stderr_bytes=(OWN/'NATIVE.stderr.txt').stat().st_size,source=before,full_entrypoint_and_all_project_called_bodies_personally_read=True,project_transitive_local_imports=[],standard_library_imports=['fractions.Fraction','functools.lru_cache','json','random'],runtime=sys.version,environment_change={'PYTHONDONTWRITEBYTECODE':'1'},attempt=1,unmodified=True,no_install_or_interpreter_switch_or_repair_or_retry=True,scope='Bounded exact dyadic finite checks; neither analytic displacement nor nonamenability or C*-simplicity nor a Lean kernel certificate',original_and_copy_unchanged=before==after and copy_after==before['SHA256'])
with (OWN/'NATIVE_RUN.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record))
assert before==after and copy_after==before['SHA256']
raise SystemExit(r.returncode)
