#!/usr/bin/env python3
"""Build the PR909 explicit source/verification archive; no remote actions."""
import hashlib,json,shutil,stat,zipfile
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent
A=P.parent
PREFIX='unsolved_math_prioritization/attempts/30001345/'
HEAD='d186dea31791cd3e8acf6829e0b65d01849623b8'
PIN='a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02'
FAMILIES=['construction_family','invariant_family','computation_family','source_model_family','priority_arrangement_family','priority_singularity_family','priority_disposition_adversary']
def require(ok,label):
 if not ok:raise RuntimeError(label)
def fp(path):
 b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def records(m):
 f=m.get('files',m.get('intentional_public_files'))
 require(type(f) is dict and bool(f),'No explicit public digest map')
 allow=set(m['explicit_public_allowlist'])
 require(allow==set(f) or allow==set(f)|{'MANIFEST.json'},'Map/allowlist disagreement')
 return f

def main():
 bundle=P/'tmp/bundle';require(not bundle.is_symlink(),'Disposable bundle symlink')
 if bundle.exists():shutil.rmtree(bundle)
 bundle.mkdir(parents=True);mapping={}
 def add(source,name,expected=None):
  q=PurePosixPath(name)
  require(not q.is_absolute() and q.as_posix()==name and all(x not in ('','.','..') for x in name.split('/')),'Unsafe archive path')
  require(not any(x in ('private_sources','raw_sources','tmp','__pycache__') for x in q.parts),'Private payload forbidden')
  require(name not in mapping and stat.S_ISREG(source.lstat().st_mode),'Duplicate/nonregular payload')
  item=fp(source)
  if expected is not None:
   if type(expected) is str:require(item['sha256']==expected,'Sealed digest changed')
   else:
    require(item['sha256']==expected['sha256'],'Sealed digest changed')
    if 'bytes' in expected:require(item['bytes']==expected['bytes'],'Sealed size changed')
  target=bundle/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);mapping[name]=item
 snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
 require(snap['head']==HEAD and len(snap['files'])==28,'Original identity changed')
 for name,digest in snap['files'].items():
  require(name.startswith(PREFIX),'Original target changed')
  add(A/'original'/name,'original_packet/'+name[len(PREFIX):],digest)
 require(fp(bundle/'original_packet/PACKAGE_MANIFEST.json')['sha256']==PIN,'Original manifest pin')
 for family in FAMILIES:
  folder=A/'reviews'/family;m=json.loads((folder/'MANIFEST.json').read_text())
  for name,pin in records(m).items():add(folder/name,'reviews/'+family+'/'+name,pin)
  add(folder/'MANIFEST.json','reviews/'+family+'/MANIFEST.json')
 for name in ['note.tex','README.md','requirements.txt','verify_package.py','run_checked.py']:add(P/name,name)
 add(P/'output/pdf/note.pdf','note.pdf')
 for name in ['ORIGINAL_SNAPSHOT.json','PR_DESCRIPTION_ANCHOR.md','ROOT_INITIAL_DERIVATION.md','ROOT_SOURCE_ACCESS_RECEIPT.json','ROOT_PRIORITY_SOURCE_RECEIPT.json','ROOT_PRIORITY_MECHANISM_CHECK.md','MATH_AUDIT_SYNTHESIS.json','PRIORITY_AUDIT_SYNTHESIS.json','PUBLICATION_FRAMING.md','PR_DESCRIPTION_CORRECTED.md','PR_DESCRIPTION_REPAIR.json']:
  add(A/name,name)
 manifest={'schema_version':1,'pr':909,'problem_id':'30001345','original_pr_head':HEAD,'original_packet_manifest_sha256':PIN,'scope':'Authored explicit classical-corollary note, unchanged original28-file packet, independent public audits and curated provenance; raw third-party sources excluded.','files':dict(sorted(mapping.items()))}
 (bundle/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 archive=P/'rough-m-arrangements-source-verification-v1.0.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted([*mapping,'PACKAGE_MANIFEST.json']):
   info=zipfile.ZipInfo(name,date_time=(2026,10,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,(bundle/name).read_bytes())
 result={'manifest_sha256':fp(bundle/'PACKAGE_MANIFEST.json')['sha256'],'archive_sha256':fp(archive)['sha256'],'archive_bytes':archive.stat().st_size,'payload_files':len(mapping),'zip_members':len(mapping)+1,'original_files_unchanged':28,'authored_pdf_inside_archive_matches_separate_pdf':True,'raw_third_party_sources_distributed':False}
 (P/'BUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
