#!/usr/bin/env python3
"""Read-only by default; --write-receipt intentionally reseals the local audit receipt."""
from pathlib import Path
import argparse, datetime, hashlib, json
E=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()

def check(p,b):return p.is_file() and p.stat().st_size==b['bytes'] and sha(p)==b['sha256']

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write-receipt',action='store_true');args=parser.parse_args();problems=[]
 baseline=json.loads((E/'preservation-before.json').read_text())
 for row in baseline['files']:
  if not check(Path(row['path']),row):problems.append({'kind':'preservation','path':row['path']})
 sm=json.loads((E/'screenshot-manifest.json').read_text())
 for row in sm['captures']:
  if not check(E/row['file'],row):problems.append({'kind':'screenshot','path':row['file']})
 dl=json.loads((E/'actual-download-verification.json').read_text())
 for row in dl['files']:
  binding={'bytes':row['expected_bytes'],'sha256':row['expected_sha256']}
  for name in [row['path'],row['site_path'],*row['matching_primary_sources']]:
   if not check(Path(name),binding):problems.append({'kind':'download_binding','path':name})
  if not row['matching_primary_sources']:problems.append({'kind':'no_primary_source_match','file':row['filename']})
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_pass':not problems,'preservation_paths':len(baseline['files']),'screenshots':len(sm['captures']),'downloads':len(dl['files']),'distinct_download_tab_count':len({r['tab_id'] for r in dl['files']}),'problems':problems,'inherited_cleanup_pending':json.loads((E/'browser-cleanup.json').read_text())['remaining_authorized_inherited_ids'],'full_native_URL_gate_PASS_claimed':False}
 if args.write_receipt:(E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2));return bool(problems)
if __name__=='__main__':raise SystemExit(main())
