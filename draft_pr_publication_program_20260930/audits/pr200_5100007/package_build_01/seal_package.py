"""Deterministically seal the authored PR200 payload and exact three-file upload."""
from pathlib import Path
import datetime,hashlib,json,zipfile,sys
A=Path(__file__).resolve().parent.parent;P=A/(sys.argv[1] if len(sys.argv)>1 else 'publication_package_v1');M=P/'materials'
assert P.parent==A and P.name.startswith('publication_package_v')
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(o):return (json.dumps(o,indent=2)+'\n').encode()
receipt=A/'package_build_01/portable_replay_01/ROOT_REPLAY_RECEIPT.json'
r=json.loads(receipt.read_bytes());assert len(r['checks'])==4 and all(x['all_result_fields_equal_to_retained_expected'] and x['exit']==0 and x['deliberate_false_guard_exit']!=0 for x in r['checks'])
(M/'verification/ROOT_PORTABLE_REPLAY_RECEIPT.json').write_bytes(receipt.read_bytes())
assert (M/'outer_focal_period.tex').read_bytes()==(P/'outer_focal_period.tex').read_bytes()
meta=json.loads((M/'metadata.json').read_bytes());deposit=json.loads((P/'zenodo-deposit.json').read_bytes());assert deposit['metadata']==meta
payload={str(f.relative_to(M)):f.read_bytes() for f in sorted(M.rglob('*')) if f.is_file() and f.name!='MANIFEST.json'}
assert not any('private' in rel.lower() or 'runtime_packages' in rel for rel in payload)
manifest={'schema':1,'purpose':'Explicit authored ZIP payload only; self-excluded manifest, no third-party fulltexts/dependencies.','files':{rel:pin(b) for rel,b in payload.items()}}
(M/'MANIFEST.json').write_bytes(enc(manifest));payload['MANIFEST.json']=(M/'MANIFEST.json').read_bytes()
with zipfile.ZipFile(P/'verification-package.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for rel,b in sorted(payload.items()):
  info=zipfile.ZipInfo(rel,date_time=(2026,10,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
with zipfile.ZipFile(P/'verification-package.zip') as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(payload) and set(z.namelist())==set(payload)
 for rel,b in payload.items():assert z.read(rel)==b
upload={x['path']:pin((P/x['path']).read_bytes()) for x in deposit['files']};assert set(upload)=={'outer_focal_period.pdf','outer_focal_period.tex','verification-package.zip'}
files={str(f.relative_to(P)):pin(f.read_bytes()) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='PACKAGE_SEAL.json'}
seal={'schema':1,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'title':meta['title'],'PR':200,'original_head':'379a959609958f1e28f68f1ab6e42970ca9d1641','upload_files':upload,'package_safe_files':files,'zip_entries':{rel:pin(b) for rel,b in sorted(payload.items())},'metadata_exact':meta,'metadata_file':'materials/metadata.json','historical_firstness_independence_certified':False,'no_thirdparty_fulltexts_or_dependency_software_in_payload':True,'whole_package_reviews_not_self_certified':True}
(P/'PACKAGE_SEAL.json').write_bytes(enc(seal))
print(json.dumps({'upload_files':upload,'package_file_count_without_seal':len(files),'ZIP_entries':len(payload),'seal':pin((P/'PACKAGE_SEAL.json').read_bytes())}))
