#!/usr/bin/env python3
"""Read-only native source/PDF/ZIP/initial-seal custody check; no code execution."""
from pathlib import Path,PurePosixPath
from io import BytesIO
import hashlib,json,stat,sys,zipfile
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];SRC=ROOT/'sources'
def need(t,s):
 if not t:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 need(len(sys.argv)==1,'No overrides accepted')
 need(sha(SRC/'SOURCE_READY.json')=='aeb11ade749cbe2c6147374642fc3fed6c5d88d323dbae59340b3fb8dfbe4535','source ready pin')
 seal=json.loads((SRC/'SOURCE_READY_SEAL.json').read_text());mf=SRC/'SOURCE_READY_MANIFEST.json'
 need(sha(mf)==seal['manifest_sha256'] and sha(SRC/'SOURCE_READY.json')==seal['source_ready_sha256'],'native ready seal')
 rows=json.loads(mf.read_text())['files'];expected=set()
 for row in rows:
  name=row['path'];q=PurePosixPath(name);p=SRC/name
  need(str(q)==name and not q.is_absolute() and '..' not in q.parts and name not in expected,'safe unique source path');expected.add(name)
  need(not p.is_symlink() and p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'all native source payload bytes '+name)
 need({p.relative_to(SRC).as_posix() for p in SRC.rglob('*') if p.is_file()}==expected|{'SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'},'exact complete native source file set')
 ready=json.loads((SRC/'SOURCE_READY.json').read_text());api=json.loads((SRC/'record.raw.json').read_text())
 need(api['id']==23320818 and api['status']=='published' and api['metadata']['version']=='1.0' and api['metadata']['publication_date']=='2026-10-12','actual published edition')
 assets=ready['all_assets_in_original_order'];need([x['original_api_file_object'] for x in assets]==api['files'],'whole native ordered API file objects')
 need([x['original_api_file_object']['key'] for x in assets]==['regular_zas_bianchi_defect.pdf','regular_zas_bianchi_verification_v1.zip'],'original PDF then ZIP order')
 for item in assets:
  obj=item['original_api_file_object'];p=Path(item['path']);data=p.read_bytes()
  need(p==SRC/obj['key'] and len(data)==item['bytes']==obj['size'] and hashlib.md5(data).hexdigest()==item['md5'] and obj['checksum']=='md5:'+item['md5'] and sha(p)==item['sha256'],'original complete asset identity')
 archive=SRC/'regular_zas_bianchi_verification_v1.zip'
 with zipfile.ZipFile(BytesIO(archive.read_bytes())) as z:
  entries=z.infolist();need(len(entries)==181,'all181 original ZIP payloads')
  seen=set()
  for e in entries:
   name=e.filename;q=PurePosixPath(name);mode=e.external_attr>>16
   need(str(q)==name and not q.is_absolute() and '..' not in q.parts and name not in seen and not e.is_dir() and stat.S_IFMT(mode) in (0,stat.S_IFREG) and not e.flag_bits&1,'safe regular original ZIP entry');seen.add(name)
   data=z.read(e);need((SRC/'published-source'/name).read_bytes()==data and len(data)==e.file_size,'all181 native extracted original bytes')
 initial=json.loads((HERE/'INITIAL_SEAL.json').read_text());im=HERE/'INITIAL_MANIFEST.json'
 need(sha(HERE/'INITIAL_SEAL.json')=='0ad8cffdbed41581b6575ea2247a36b1cecb544f15f49768915cd21a78960aab' and sha(im)==initial['manifest_sha256'],'independent initial seal')
 old=json.loads(im.read_text())['files']
 for row in old:
  p=HERE/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'preserved initial owned bytes '+row['path'])
 print(json.dumps({'assessment':'NATIVE_SOURCE_AND_INDEPENDENT_INITIAL_CUSTODY_SUPPORTED','native_payload_bindings':len(rows),'native_total_files':len(rows)+2,'original_ZIP_payloads_compared':len(seen),'preserved_initial_owned_files':len(old),'original_reader_sha256':sha(SRC/'regular_zas_bianchi_defect.pdf'),'controlling_TeX_sha256':sha(SRC/'published-source/manuscript.tex'),'source_ready_sha256':sha(SRC/'SOURCE_READY.json'),'initial_seal_sha256':sha(HERE/'INITIAL_SEAL.json'),'source_mutations':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
