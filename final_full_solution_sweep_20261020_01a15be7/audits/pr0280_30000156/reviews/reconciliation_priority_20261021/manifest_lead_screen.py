#!/usr/bin/env python3
"""Narrow read-only screen of local preparation/manifests for PR280 aliases."""
from pathlib import Path
import subprocess,re,json,hashlib,datetime
r=Path('/Users/alec/Documents/Math');o=r/'final_full_solution_sweep_20261020_01a15be7/audits/pr0280_30000156/reviews/reconciliation_priority_20261021'
args=['rg','--files','--hidden','-g','!.git/**','-g','!.zenodo-state/**','-g','*manifest*.json','-g','*MANIFEST*.json','-g','*publication*.json','-g','*METADATA*.json','-g','!**/private/**','-g','!**/raw/**']
p=subprocess.run(args,cwd=r,text=True,capture_output=True,check=True)
pat=re.compile(r'30000156|OWR[-_ ]768[-_ ]006|Maps over finite fields:\s*integrability and reversibility|short[- ]cycle.{0,60}birational|birational.{0,60}short[- ]cycle',re.I|re.S)
files=p.stdout.splitlines(); hits=[]
for name in files:
 f=r/name
 try:t=f.read_text()
 except (UnicodeError,OSError):continue
 if pat.search(t):
  hits.append({'path':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'classification':'audit_or_frozen_submission_metadata_not_prepared_preprint' if ('pr280' in name.lower() or 'pr0280' in name.lower()) else 'aggregate_metadata_snapshot_not_prepared_target_preprint'})
res={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'patterns':pat.pattern,'files_screened':len(files),'hits':hits,'exact_target_prepared_publication_manifest_found':False,'scope':'Repository-visible authored JSON manifest/publication/metadata filenames; known private/raw bodies excluded. A target identifier inside an aggregate PR snapshot is not a prepared target publication. Existing .zenodo-state separately screened.','limitation':'This filename/content screen is bounded; it does not assert absence from every file type or from deleted/unavailable files.'}
(o/'PREPARED_MANIFEST_SCREEN.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'files_screened':len(files),'hit_count':len(hits),'exact_target_prepared_publication_manifest_found':False},indent=2))
