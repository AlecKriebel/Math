#!/usr/bin/env python3
"""Build an explicit curated PR919 archive; no remote actions or source bodies."""
import hashlib,json,shutil,stat,zipfile
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;A=P.parent
PREFIX='unsolved_math_prioritization/attempts/30002555/'
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
PIN='a7f24f30d76ca7e53da932dfc1f19deac67f13a675742175274e30ca767832f8'
FAMILIES={
 'topology_family':'869fce20586448e9f76c55f092196b710a8cc42be28c85fed768fded89d7b177',
 'conformal_family':'b068ffd8e017702253fd2a4cac77260b8f95fd515f96e88e01a3dd1dc2fb0c49',
 'source_model_family':'7828f898c26248a828a0b5aaf37f60b8f0ce2255c43eb6768a53df29b8dd0b92',
 'computation_family':'ad4496ec2cb54771156a6ced57eec95667ecb3718c0add575489c0e6dce7188b',
 'priority_veech_family':'04ee8a2e568c335e4ec635e779492de30de3e02318ce478b9aa0e267c539a1b9',
 'priority_conformal_topology_family':'364657a3d5df6a5fa93e3873bbe62480c87621342212766c59de653946fbd8dc'}
ROOT_PUBLIC=['ORIGINAL_SNAPSHOT.json','PR_DESCRIPTION_ANCHOR.md','ROOT_INITIAL_DERIVATION.md','ROOT_ARITHMETIC_CROSSCHECK.md','ROOT_PACKET_AUTHENTICATION.json','ROOT_ORIGINAL_REPRODUCTION.json','ROOT_SOURCE_RETRIEVAL.json','ROOT_PSV_SOURCE_CHECK.json','ROOT_CURRENT_PUBLICATION_CHECK.json','ROOT_PRIORITY_RETRIEVAL.json','ROOT_PRIORITY_QUERY_LOG.json','ROOT_APV2020_RETRIEVAL.json','ROOT_PRIOR_COROLLARY_BRIDGE.md','ROOT_PRIORITY_VEECH_REVIEW_CHECK.json','ROOT_PRIORITY_CONFORMAL_REVIEW_CHECK.json','MATH_AUDIT_SYNTHESIS.json','PRIORITY_AUDIT_SYNTHESIS.json','PRIORITY_AUDIT_SYNTHESIS.md','PUBLICATION_DISPOSITION.json','EXPOSITION_CLARIFICATIONS.md','PUBLICATION_FRAMING.md','PR_DESCRIPTION_CORRECTED.md','PR_DESCRIPTION_REPAIR.json','PR_DESCRIPTION_REPAIR_REVISION01.json','WHOLE_PACKAGE_REVIEW01_ROOT_CHECK.json','GLOBAL_REPAIRS_REVIEW01.json','DISPOSITION_REGRESSION_AFTER.json','RECEIPT_LINKAGE_REGRESSION.json']
def require(ok,label):
 if not ok:raise RuntimeError(label)
def fp(path):
 b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def records(m):
 f=m.get('files',m.get('public_files',m.get('public_allowlist')))
 if type(f) is list:return {x['path']:{'bytes':x.get('bytes',x.get('size')),'sha256':x['sha256']} for x in f}
 require(type(f) is dict and bool(f),'No curated public map')
 if type(m.get('public_allowlist')) is list:require(set(m['public_allowlist'])==set(f),'Curated map mismatch')
 return f

def main():
 bundle=P/'tmp/bundle';require(not bundle.is_symlink(),'Disposable bundle symlink')
 if bundle.exists():shutil.rmtree(bundle)
 bundle.mkdir(parents=True);mapping={}
 def add(source,name,expected=None):
  q=PurePosixPath(name)
  require(not q.is_absolute() and q.as_posix()==name and all(x not in ('','.','..') for x in name.split('/')),'Unsafe archive path')
  require(not any(x in ('private','private_sources','raw_sources','tmp','__pycache__') for x in q.parts),'Private payload forbidden')
  require(name not in mapping and stat.S_ISREG(source.lstat().st_mode),'Duplicate/nonregular payload')
  item=fp(source)
  if expected is not None:
   if type(expected) is str:require(item['sha256']==expected,'Sealed digest changed '+name)
   else:require(item=={'bytes':expected['bytes'],'sha256':expected['sha256']},'Sealed fingerprint changed '+name)
  target=bundle/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);mapping[name]=item
 snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text());require(snap['head']==HEAD and len(snap['files'])==27,'Original identity changed')
 for name,digest in snap['files'].items():
  require(name.startswith(PREFIX),'Original target changed');add(A/'original'/name,'original_packet/'+name[len(PREFIX):],digest)
 require(fp(bundle/'original_packet/PUBLICATION_MANIFEST.json')['sha256']==PIN,'Original manifest pin')
 for family,pin in FAMILIES.items():
  folder=A/'reviews'/family;require(fp(folder/'MANIFEST.json')['sha256']==pin,'Family seal changed '+family)
  m=json.loads((folder/'MANIFEST.json').read_text())
  for name,r in records(m).items():add(folder/name,'reviews/'+family+'/'+name,r)
  add(folder/'MANIFEST.json','reviews/'+family+'/MANIFEST.json',pin)
 for name in ['note.tex','README.md','requirements.txt','verify_package.py','run_checked.py']:add(P/name,name)
 add(P/'output/pdf/note.pdf','note.pdf')
 for name in ROOT_PUBLIC:add(A/name,name)
 manifest={'schema_version':1,'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'original_packet_manifest_sha256':PIN,'scope':'Explicit attributed application note; unchanged original27; six independent public mathematical/priority audit families and curated provenance; raw third-party bodies excluded.','files':dict(sorted(mapping.items()))}
 (bundle/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 archive=P/'rotational-veech-source-verification-v1.0.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted([*mapping,'PACKAGE_MANIFEST.json']):
   info=zipfile.ZipInfo(name,date_time=(2026,10,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,(bundle/name).read_bytes())
 result={'manifest_sha256':fp(bundle/'PACKAGE_MANIFEST.json')['sha256'],'archive_sha256':fp(archive)['sha256'],'archive_bytes':archive.stat().st_size,'payload_files':len(mapping),'zip_members':len(mapping)+1,'original_files_unchanged':27,'authored_pdf_inside_archive_matches_separate_pdf':True,'raw_third_party_sources_distributed':False}
 (P/'BUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
