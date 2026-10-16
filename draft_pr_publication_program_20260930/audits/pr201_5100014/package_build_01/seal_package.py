"""Seal exact authored payload, metadata and upload files without external writes."""
from pathlib import Path
import datetime,hashlib,json,zipfile,sys
A=Path(__file__).resolve().parent.parent
P=A/(sys.argv[1] if len(sys.argv)>1 else 'publication_package_v1');M=P/'materials'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,indent=2)+'\n').encode()
def manifest():
 payload={str(f.relative_to(M)):f.read_bytes() for f in sorted(M.rglob('*')) if f.is_file() and f.name!='MANIFEST.json'}
 if any(f.is_symlink() for f in M.rglob('*')):raise ValueError('symlink')
 if any('runtime_packages' in k or '/private_sources/' in k or '/primary_private/' in k for k in payload):raise ValueError('private payload')
 m={'schema':1,'purpose':'Explicit authored payload only; manifest self-excluded, dependencies/third-party fulltexts/private state excluded.','files':{k:pin(b) for k,b in payload.items()}}
 (M/'MANIFEST.json').write_bytes(enc(m));return {**payload,'MANIFEST.json':(M/'MANIFEST.json').read_bytes()}
if __name__=='__main__':
 payload=manifest()
 if '--manifest-only' in sys.argv:print(json.dumps({'manifest_entries':len(payload)-1}));sys.exit(0)
 r=json.loads((M/'verification/ROOT_PORTABLE_REPLAY_RECEIPT.json').read_text())
 if not r['all_jobs_passed'] or not r['ordinary_optimized_failure_guard_passed']:raise ValueError('portable checks not accepted')
 if (M/'outer_pedal_flag.tex').read_bytes()!=(P/'outer_pedal_flag.tex').read_bytes():raise ValueError('source copies differ')
 d=json.loads((P/'zenodo-deposit.json').read_bytes());meta=json.loads((M/'metadata.json').read_bytes())
 if d['metadata']!=meta:raise ValueError('metadata differs')
 with zipfile.ZipFile(P/'verification-package.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for rel,b in sorted(payload.items()):
   i=zipfile.ZipInfo(rel,date_time=(2026,10,16,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,b)
 with zipfile.ZipFile(P/'verification-package.zip') as z:
  if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=set(payload):raise ValueError('ZIP names differ')
  for k,b in payload.items():
   if z.read(k)!=b:raise ValueError('ZIP bytes differ')
 uploads={x['path']:pin((P/x['path']).read_bytes()) for x in d['files']}
 if set(uploads)!={'outer_pedal_flag.pdf','outer_pedal_flag.tex','verification-package.zip'}:raise ValueError('unexpected upload')
 files={str(f.relative_to(P)):pin(f.read_bytes()) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='PACKAGE_SEAL.json'}
 seal={'schema':1,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'original_head':'90bdb85235979f2ffa7496b9b689036654e55200','title':meta['title'],'upload_files':uploads,'metadata_exact':meta,'metadata_file':'materials/metadata.json','package_safe_files':files,'zip_entries':{k:pin(v) for k,v in sorted(payload.items())},'theorem_novelty_firstness_independence_certified':False,'authored_payload_no_dependencies_or_thirdparty_fulltexts':True,'whole_package_reviews_not_self_certified':True}
 (P/'PACKAGE_SEAL.json').write_bytes(enc(seal))
 print(json.dumps({'upload_files':uploads,'ZIP_entries':len(payload),'seal':pin((P/'PACKAGE_SEAL.json').read_bytes())}))
