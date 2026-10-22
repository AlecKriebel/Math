"""Deliberately seal only authored public audit material; manifest self-excluded."""
from pathlib import Path
import datetime,hashlib,json,stat

HERE=Path(__file__).resolve().parent.parent
PUBLIC=[
 'AUDIT_REPORT.md',
 'MATHEMATICAL_RECONSTRUCTION.md',
 'RESEARCH_LOG.md',
 'SEAL_NOTICE.md',
 'SOURCE_REVIEW.md',
 'receipts/actual_reproduction.json',
 'receipts/archive_OO_launch.json',
 'receipts/archive_O_launch.json',
 'receipts/archive_initial_inspection.json',
 'receipts/archive_normal_launch.json',
 'receipts/authenticate_after_launch.json',
 'receipts/execution_adversary_launch.json',
 'receipts/finite_OO_launch.json',
 'receipts/finite_O_launch.json',
 'receipts/finite_normal_launch.json',
 'receipts/new_execution_adversary.json',
 'receipts/new_execution_commands.jsonl',
 'receipts/original_after.json',
 'receipts/original_before.json',
 'receipts/outer_boundaries_launch.json',
 'receipts/outer_cli_boundaries.json',
 'receipts/receipt_validation.json',
 'receipts/receipt_validation_launch.json',
 'sources/archive_and_binding_adversary.py',
 'sources/authenticate.py',
 'sources/execution_adversary.py',
 'sources/new_finite_checks.py',
 'sources/outer_boundary_processes.py',
 'sources/run_logged.py',
 'sources/run_reproduction.py',
 'sources/seal.py',
 'sources/validate_receipts.py',
]

def require(ok,msg):
 if not ok:raise RuntimeError(msg)

def main():
 require(not (HERE/'MANIFEST.json').exists(),'already sealed; do not reseal silently')
 require(len(PUBLIC)==len(set(PUBLIC)) and PUBLIC==sorted(PUBLIC),'public list must be equal, unique and sorted')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (HERE/'RESEARCH_LOG.md').open('a') as f:
  f.write('- '+now+' — Independent proof reconstruction and all scoped execution/packaging adversaries complete. Original26-file before/after authentication and receipt consistency checks passed. Optional nested-JSON traceback retained; historical runtime/original-write claims NOT_REPRODUCED, fresh source/corpus NOT_RUN. Deliberate public allowlist sealed for root authentication before substantive intake. Completion estimate:100% of assigned computational-adversary review; no parent acceptance/publication implied.\n')
 notice=('# Deliberate public audit seal\n\nSealed UTC: '+now+'\n\n'
         'The explicit public allowlist is deliberately enumerated in sources/seal.py and MANIFEST.json. '
         'The manifest maps exactly those unique names to byte counts and SHA-256 digests, and excludes itself. '
         'Only authored reasoning, authored test/authentication/seal source, original-file hash/mode metadata and actual command receipts are public. '
         'private/, fixtures/ and tmp/ are excluded in their entirety, including copied candidate code/fixtures, mutation copies, hostile modules, caches and transient files. '
         'No downloaded primary body, extract or image, private source record or corpus content is included. '
         'The seal is an internally delivered checkable audit closure, not an external publication or acceptance decision. '
         'Authenticate the manifest against its externally delivered digest and verify every allowed byte before substantive intake. '
         'All malformed-input failures and the inaccurate unsampled progress-time label remain documented; no historical environment was simulated.\n')
 (HERE/'SEAL_NOTICE.md').write_text(notice)
 actual_sources={str(p.relative_to(HERE)) for p in (HERE/'sources').iterdir()}
 actual_receipts={str(p.relative_to(HERE)) for p in (HERE/'receipts').iterdir()}
 require(actual_sources|actual_receipts=={p for p in PUBLIC if '/' in p},'public source/receipt inventory differs')
 records={}
 for name in PUBLIC:
  p=HERE/name
  require(stat.S_ISREG(p.lstat().st_mode),'nonregular public file')
  b=p.read_bytes();records[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 manifest=dict(schema_version=1,purpose='Independent computational adversary audit, public authored closure',
               explicit_public_allowlist=PUBLIC,files=records)
 raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
 (HERE/'MANIFEST.json').write_bytes(raw)
 # Read back every sealed public byte immediately. Nothing is changed afterward.
 require((HERE/'MANIFEST.json').read_bytes()==raw,'manifest readback')
 for name,row in records.items():
  b=(HERE/name).read_bytes()
  require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'public readback mismatch')
 print(json.dumps(dict(manifest_sha256=hashlib.sha256(raw).hexdigest(),manifest_bytes=len(raw),
                      public_files=len(records),public_bytes=sum(v['bytes'] for v in records.values()),
                      seal_utc=now,self_excluded=True,all_public_bytes_readback_verified=True),indent=2))

if __name__=='__main__':main()
