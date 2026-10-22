#!/usr/bin/env python3
"""Offline closed-payload custody checker, run only in a new copied review."""
from pathlib import Path
import hashlib,json,sys,subprocess,zipfile
H=Path(__file__).resolve().parent
CONTROLS={'MANIFEST.json','MANIFEST.sha256','REPLAY_RESULTS.json','FINAL_SEAL.json'}
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def files():return {str(p.relative_to(H)):p for p in H.rglob('*') if p.is_file() and not p.is_relative_to(H/'runtime') and str(p.relative_to(H)) not in CONTROLS}
def main():
 need(len(sys.argv)==2,'expected external manifest SHA256 argument')
 mb=(H/'MANIFEST.json').read_bytes();need(sha(mb)==sys.argv[1],'external manifest seal')
 manifest=json.loads(mb);actual=files();need(set(actual)==set(manifest['payloads']),'closed payload membership')
 for name,p in actual.items():
  need(not p.is_symlink() and not any(x.is_symlink() for x in p.parents if x.is_relative_to(H)),'symlink')
  b=p.read_bytes();pin=manifest['payloads'][name];need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'payload:'+name)
 checks=load(H/'CHECKS.json');final=load(H/'FINAL_RECHECK.json');need(len(checks['prs'])==9 and len(final['prs'])==9 and len(checks['records'])==4,'bounded coverage')
 need(final['whole_ledger_start_end_equal'] and final['shared_branch_head_index_unchanged'],'final preservation')
 need(checks['ledger']['rows']==181 and checks['ledger']['all_primary_doi_unique_for_targets'],'ledger')
 old=load(H/'private/HISTORICAL_APPEND_CHECK.json');need(old['all180rows_preserved'] and old['fresh_full_sheet_matches_after'],'historicalappend')
 for n in range(1132,1141):
  d=H/'private'/f'pr{n}';capture=load(d/'CAPTURE.json');need(capture['all_metadata_bound'] and capture['live_equals_pinned_files'] and not capture['queue_files'],'sourcebinding')
  for f in capture['files']:
   b=(d/'head'/f['path']).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(oid==f['blob']==f['api_blob'],'headblob')
 for rec in checks['records']:
  d=H/'private'/f'record{rec["record"]}'
  for f in rec['files']:
   b=(d/f['name']).read_bytes();need(len(b)==f['bytes'] and sha(b)==f['sha256'] and 'md5:'+hashlib.md5(b).hexdigest()==f['md5'],'providerpayload')
 for package in checks['packages']:
  d=H/'private'/f'record{package["record"]}';z=zipfile.ZipFile(next(d.glob('*.zip')));payload={f.filename for f in z.infolist() if not f.is_dir()};m=json.loads(z.read('SOURCE_MANIFEST.json'));need(set(m)==payload-{'SOURCE_MANIFEST.json'},'internalmanifestclosure')
  for name,pin in m.items():
   b=z.read(name);need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'internalpayload')
 flags=[] if sys.flags.optimize==0 else ['-O'] if sys.flags.optimize==1 else ['-OO']
 result=subprocess.run([sys.executable,*flags,str(H/'math_controls.py')],capture_output=True,text=True)
 need(result.returncode==0,'new exact mathematical controls');math=json.loads(result.stdout)
 print(json.dumps({'status':'PASS','manifest_sha256':sha(mb),'closed_payloads':len(actual),'prs':9,'head_files':sum(x['file_count'] for x in checks['prs']),'provider_files':sum(len(x['files']) for x in checks['records']),'ledger_rows':181,'exact_controls':math,'scope':'Bounded captured identity, byte custody and exact finite controls; no live transaction/global priority/full foundational proof certificate'},sort_keys=True))
if __name__=='__main__':main()
