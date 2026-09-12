#!/usr/bin/env python3
"""Read-only checks against recorded evidence; does not refresh expected hashes."""
from pathlib import Path
import hashlib,json,tarfile
PROGRAM=Path(__file__).resolve().parents[2]
REFEREE=PROGRAM/'referee_2026-09-11'
RESPONSE=PROGRAM/'referee_response_20260911'
LEAN=PROGRAM/'bell_lean'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((RESPONSE/'evidence/verification.json').read_text())
assert all(sha(PROGRAM/k)==v for k,v in r['current_artifact_sha256'].items())
assert all(sha(RESPONSE/'evidence'/k)==v for k,v in r['response_log_sha256'].items())
for receipt in [REFEREE/'evidence/kernel_report.json',LEAN/'reports/runs/20260911T022153Z-2ea5f99b/kernel_report.json']:
 k=json.loads(receipt.read_text())
 assert k['status']=='passed'
 assert all(sha(LEAN/f)==v for f,v in k['source_snapshot'].items())
k=json.loads((LEAN/'reports/runs/20260911T022153Z-2ea5f99b/kernel_report.json').read_text())
assert all(sha(LEAN/c['log'])==c['log_sha256'] for c in k['commands'])
for line in (REFEREE/'SHA256SUMS.txt').read_text().splitlines():
 expected,name=line.split('  ',1)
 assert sha(REFEREE/name)==expected,name
found=set()
with tarfile.open(PROGRAM/'submission/arxiv_source.tar.gz','r:gz') as archive:
 for member in archive.getmembers():
  name=Path(member.name).name
  if member.isfile() and name in ['main.tex','appendices.tex']:
   assert archive.extractfile(member).read()==(PROGRAM/'paper'/name).read_bytes()
   found.add(name)
assert found=={'main.tex','appendices.tex'}
assert (RESPONSE/'received_report.md').read_bytes()==(REFEREE/'REFEREE_REPORT.md').read_bytes()
print('PASS: saved artifact/log hashes, both full-run input snapshots, original command logs, preserved referee package, and corrected archive sources.')
