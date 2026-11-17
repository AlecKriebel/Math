"""One fresh v2 transformer invocation; literal streams, no retry or repair."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time

L = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/thompson-cstar-editorial-corrected-v2-sol-20261117')
assert not (L / 'TRANSFORM_RUN.json').exists()
assert not (L / 'TRANSFORM.stdout').exists() and not (L / 'TRANSFORM.stderr').exists()
argv = [sys.executable, str(L / 'copy_transformer.py')]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
r = subprocess.run(argv, cwd=L, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
elapsed = time.monotonic() - t0
(L / 'TRANSFORM.stdout').write_bytes(r.stdout)
(L / 'TRANSFORM.stderr').write_bytes(r.stderr)
receipt = {'argv': argv, 'cwd': str(L), 'UTC_started': started, 'UTC_finished': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': elapsed, 'exit': r.returncode, 'attempt_count_in_this_authorized_lane': 1, 'repair_or_retry_count': 0, 'transformer_sha256': hashlib.sha256((L / 'copy_transformer.py').read_bytes()).hexdigest(), 'stdout_bytes': len(r.stdout), 'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(), 'stderr_bytes': len(r.stderr), 'stderr_sha256': hashlib.sha256(r.stderr).hexdigest(), 'original_builder_execution': False, 'scientific_source_execution': False, 'private_only': True, 'separate_prior_failure_is_preserved': True}
(L / 'TRANSFORM_RUN.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
sys.exit(r.returncode)
