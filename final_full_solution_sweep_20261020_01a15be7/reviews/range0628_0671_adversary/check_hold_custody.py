from pathlib import Path
import datetime as dt,hashlib,json,os,re,shutil,subprocess,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
manifest=json.loads((Q/'INPUT_MANIFEST.json').read_text());captured={e['source'] for e in manifest['files']}
def capture(src):
 rel=Path('private/inputs')/src.relative_to(R);dest=Q/rel;b=src.read_bytes();dest.parent.mkdir(parents=True,exist_ok=True)
 if str(src) in captured:require(dest.read_bytes()==b,'existing capture differs')
 else:dest.write_bytes(b);manifest['files'].append(dict(source=str(src),path=str(rel),bytes=len(b),sha256=sha(b),captured_at=now(),source_mtime_ns=src.stat().st_mtime_ns));captured.add(str(src))
 return b
reviews=[(628,'pr0628_30000403','homogeneous_geometry_recheck01','OUTPUT_MANIFEST.json','outputs'),(628,'pr0628_30000403','primary_priority_recheck01','FINAL_SEAL.json','files'),(630,'pr0630_30000700','primary_scope_priority_recheck01','SEAL.json','files')]
seals=[]
for n,folder,review,name,key in reviews:
 root=R/'audits'/folder/'reviews'/review;raw=capture(root/name);seal=json.loads(raw);entries=seal[key]
 for v in entries:
  rel=v.get('path',v.get('relative_path'));b=capture(root/rel);require(len(b)==v['bytes'] and sha(b)==v['sha256'],'bad sealed entry '+str(root/rel))
 if name=='OUTPUT_MANIFEST.json':
  final=json.loads(capture(root/'FINAL_SEAL.json'));require(final['output_manifest_sha256']==sha(raw),'geometry final manifest hash differs')
 if n==630:
  capture(root/'SEAL.sha256');checkpoint=json.loads((root/'SOURCE_FIRST_CHECKPOINT_SEAL.json').read_text())
  for rel,digest in checkpoint['files'].items():require(sha((root/rel).read_bytes())==digest,'source-first checkpoint invalid')
 seals.append(dict(pr=n,review=review,seal_path=str(Path('private/inputs')/(root/name).relative_to(R)),seal_sha256=sha(raw),entries_verified=len(entries)))
for folder in ['pr0628_30000403','pr0630_30000700']:
 root=R/'audits'/folder
 for src in root.iterdir():
  if src.is_file():capture(src)
 for rel in ['private/account_complete.json','private/account_matches.json','private/final_live_pr.json','private/release_replay.stdout','private/release_replay.stderr']:
  if (root/rel).is_file():capture(root/rel)
 for dr in ['private/custody_replay_incident','private/root_review_replay01']:
  if (root/dr).is_dir():
   for src in sorted((root/dr).rglob('*')):
    if src.is_file() and not src.is_symlink():capture(src)
 accept=json.loads((root/'ROOT_FINAL_RECHECK_ACCEPTANCE.json').read_text());n=628 if '0628' in folder else 630
 expected=[x for x in seals if x['pr']==n]
 if n==628:
  geometry=sha((root/'reviews/homogeneous_geometry_recheck01/FINAL_SEAL.json').read_bytes());require(accept['geometry_review']['seal_sha256']==geometry,'geometry acceptance seal differs');require(accept['primary_review']['seal_sha256']==expected[1]['seal_sha256'],'628 primary seal acceptance differs')
 else:require(accept['seal_sha256']==expected[0]['seal_sha256'] and accept['sealed_files_verified']==71,'630 seal acceptance differs')
 blobentries=[x for x in json.loads((Q/'GIT_BLOB_INPUT_MANIFEST.json').read_text())['files'] if x['pr']==n and '/attempts/' in x['path']]
 original=json.loads((root/'ROOT_ORIGINAL_REPLAY.json').read_text());require(len(original['science_files'])==len(blobentries)==(36 if n==628 else 28),'original science count differs');lookup={x['path']:x for x in blobentries}
 for x in original['science_files']:require(x['bytes']==lookup[x['path']]['bytes'] and x['sha256']==lookup[x['path']]['sha256'],'original immutable digest differs')
 account=json.loads((root/'private/account_complete.json').read_text());require(len(account['records'])==account['total']==197 and len({str(x['id']) for x in account['records']})==197,'account total/unique inconsistency')
 require(any(str(x['id'])=='23174283' for x in account['records']),'account positive control absent')
 accountreceipt=json.loads((root/'DUPLICATE_ACCOUNT_CHECK.json').read_text());require(accountreceipt['account_complete_sha256']==sha((root/'private/account_complete.json').read_bytes()),'account capture SHA mismatch')
 # Direct identity search over the captured complete account, not just the old match subset.
 pid='30000403' if n==628 else '30000700';alias='1188-004' if n==628 else '1460-004';ident=[]
 for record in account['records']:
  text=json.dumps(record.get('metadata',{}),ensure_ascii=False)
  if re.search(r'(?<!\d)'+pid+r'(?!\d)',text) or alias in text or f'/pull/{n}' in text:ident.append(record['id'])
 require(not ident,'candidate record identity found')
 # Independently reread the exact existing closure; no issue/comment mutations.
 cid='6183889457' if n==628 else '6184155421';wire=subprocess.run(['gh','api','--hostname','github.com',f'repos/AlecKriebel/Math/issues/comments/{cid}'],cwd=REPO,capture_output=True,check=True).stdout;save(f'private/live_closure_{n}.json',json.loads(wire))
incident=json.loads((R/'audits/pr0628_30000403/ROOT_CUSTODY_REPLAY_INCIDENT.json').read_text());certroot=R/'audits/pr0628_30000403/reviews/primary_priority_recheck01';cert=(certroot/'SHARPNESS_CERTIFICATE.json').read_bytes();require(sha(cert)==incident['recovery_preimage_sha256']=='40ed144ed4b1cbf1d65f316bdad876df848eaedef0ee1f34fd89aa50512c4f79','restored certificate mismatch');require(incident['preservation_limits'].find('mtimechanged')>=0,'mtime disclosure absent')
replays=[]
for n,source,expected in [(628,certroot/'verify_sharpness_exact.py',certroot/'SHARPNESS_CERTIFICATE.json'),(630,R/'audits/pr0630_30000700/reviews/primary_scope_priority_recheck01/certificates/exact_priority_controls.py',R/'audits/pr0630_30000700/private/root_review_replay01/normal.stdout.json')]:
 # Never execute code in canonical, sealed or captured-input directories.
 dest=Q/f'private/new_replay_pr{n}';require(not dest.exists(),'private replay must be new');dest.mkdir(parents=True);script=dest/source.name;script.write_bytes(source.read_bytes());results=[]
 for mode in ['normal','optimized'] if n==630 else ['normal']:
  args=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(script)];res=subprocess.run(args,cwd=dest,capture_output=True);(dest/f'{mode}.stdout').write_bytes(res.stdout);(dest/f'{mode}.stderr').write_bytes(res.stderr);require(res.returncode==0,'private independent replay failed')
  if n==628:
   actual=json.loads((dest/'SHARPNESS_CERTIFICATE.json').read_text());wanted=json.loads(expected.read_text());require(actual.pop('utc') is not None and wanted.pop('utc') is not None and actual==wanted,'full 628 replay certificate differs')
  else:require(res.stdout==expected.read_bytes(),'630 root private replay differs')
  results.append(dict(mode=mode,exit_code=res.returncode,stdout_sha256=sha(res.stdout),stderr_sha256=sha(res.stderr)))
 replays.append(dict(pr=n,new_private_copy=True,script_sha256=sha(script.read_bytes()),results=results,full_certificate_equal_except_execution_UTC=n==628,root_and_sealed_output_equal=n==630))
for entry in manifest['files']:
 require(sha((Q/entry['path']).read_bytes())==entry['sha256'],'captured input altered')
save('INPUT_MANIFEST.json',manifest);save('hold_custody_checks.json',dict(at=now(),seals=seals,replays=replays,restored_628_certificate_sha256=sha(cert),original_inputs_verified={628:36,630:28},account_receipt_identity_checks_passed=True,account_scope='Captured root authenticated account with 197 unique records; not a new independent authenticated account fetch. Fresh ledger and public DOI fetched separately.',conclusion='Disposition evidence is consistent, bound and reproducible; no fresh firstness/proof certification.'))
log=json.loads((Q/'RESEARCH_LOG.json').read_text());log.append(dict(at=now(),completion_estimate_percent=65,event='Verified 13+47+71 sealed review payloads, 36+28 immutable originals, custody recovery and independent private replays. Both closed priority dispositions remain supported.'));save('RESEARCH_LOG.json',log)
print(json.dumps(dict(sealed_entries=sum(x['entries_verified'] for x in seals),originals=64,replay_prs=2,captures=len(manifest['files']))))
