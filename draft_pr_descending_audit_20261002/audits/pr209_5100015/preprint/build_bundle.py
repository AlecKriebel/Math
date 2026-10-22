"""Seal the local prepublication package; no external calls or release authorization."""
from pathlib import Path
import hashlib,json,zipfile
B=Path(__file__).resolve().parent
FORBIDDEN={'__pycache__','node_modules','reproduction_environment'}
def pin(p,base):
 assert p.is_file() and not p.is_symlink();raw=p.read_bytes()
 return dict(path=p.relative_to(base).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def save(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def files(folder):
 rows=[]
 for p in sorted(folder.rglob('*')):
  rel=p.relative_to(folder)
  assert not p.is_symlink() and not any(t.startswith('private') or t in FORBIDDEN for t in rel.parts),'Unsafe selected path'
  if p.is_file():rows.append(p)
 return rows
def main():
 n=B/'pr_update/5100015';v=B/'verification'
 top=[pin(p,n) for p in sorted(n.iterdir()) if p.is_file() and p.name not in {'MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}]
 save(n/'MANIFEST.json',dict(scope='Dated current top-level presentation; all23 original author bindings remain verbatim under history/original_submission_20261016/',files=top))
 save(n/'CURRENT_PACKET_MANIFEST.json',dict(schema='pr209-current-packet-v1',source_head='fd09a95b479f376234835a4494693bb1316c85ec',self_excluded=True,files=[pin(p,n) for p in files(n) if p.name!='CURRENT_PACKET_MANIFEST.json']))
 save(v/'MANIFEST.json',dict(schema='pr209-verification-sha256-v1',self_excluded=True,files=[pin(p,v) for p in files(v) if p!=v/'MANIFEST.json']))
 names=['manuscript.tex','manuscript.pdf','metadata.json','README.md','build_bundle.py','prepare_package.py','NATIVE_RELEASE_PLAN.json','RENDER_QA.json','ARTIFACT_OPERATION_STARTED.json','PREPARATION_RECEIPT.json','PREPARATION_ENOSPC_RECOVERY.json']
 selected=[B/name for name in names]
 selected+=files(v)+files(n);selected=sorted(set(selected));assert all(p.is_file() for p in selected)
 save(B/'SOURCE_MANIFEST.json',dict(schema='pr209-source-sha256-v1',self_excluded=True,scope='Dated prepublication proof, metadata, native presentation and offline verification; third-party full papers/private transport excluded. Fresh sequential whole-package reviews, final clearance and actual release receipts are separate case records outside this ZIP to avoid circular approval.',files=[pin(p,B) for p in selected]))
 selected.append(B/'SOURCE_MANIFEST.json');archive=B/'k303b-source-verification.zip';prefix='k303b_outer_center_pedal_product/'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(selected):
   info=zipfile.ZipInfo(prefix+p.relative_to(B).as_posix(),date_time=(2026,10,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert len(z.namelist())==len(selected)==len(set(z.namelist())) and z.testzip() is None
  for p in selected:assert z.read(prefix+p.relative_to(B).as_posix())==p.read_bytes()
 save(B/'PACKAGE_MANIFEST.json',dict(schema='pr209-submission-bundle-v1',submission_files=[pin(B/'manuscript.pdf',B),pin(archive,B)],source_manifest=pin(B/'SOURCE_MANIFEST.json',B),manuscript_source=pin(B/'manuscript.tex',B),metadata=pin(B/'metadata.json',B),source_archive_entries=len(selected),clearance_role='Byte binding only. No whole-package approval, publication or merge is self-certified. Actual final clearance and later release receipts are external to this dated ZIP.'))
 save(B/'deposit.json',dict(metadata=json.loads((B/'metadata.json').read_text()),files=[dict(path='manuscript.pdf',name='k303b-outer-center-pedal-areas.pdf'),dict(path=archive.name,name=archive.name)]))
 print(json.dumps(json.loads((B/'PACKAGE_MANIFEST.json').read_text()),indent=2))
if __name__=='__main__':main()
