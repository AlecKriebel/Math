#!/usr/bin/env python3
"""Build the explicitly curated PR938 archive. No network or remote mutation."""
import hashlib,json,shutil,stat,zipfile
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent; A=P.parent
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
PREFIX='unsolved_math_prioritization/attempts/30003634/'
PIN='149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'
FAMILIES={
 'topology_family':('MANIFEST.json','3a1d63dd809ffd527b193e323220ca7eb34d3acc93a3efc010820a0039e5694c'),
 'goeritz_family':('PUBLIC_MANIFEST.json','4ad69f501889239782b6120a66fff9c4830fb683692eeebab5fdf59d5a899dda'),
 'meyer_algebra_family':('PUBLIC_MAP.json','44e854b09304f2d5d444460f53dacf574289b3dd2bc765703a1b62604d024517'),
 'source_model_family':('PUBLIC_MANIFEST.json','fe9ea4cc0bfc0c5ac4c017b9315a49f2c9cc5d2c6d9758795611c81740b1866a'),
 'reproducibility_family':('PUBLIC_MANIFEST.json','342c41da878c06e5ad7d8967d128228a55b3ccb7d834ed55d626fc00b46fcd24'),
 'classical_priority':('PUBLIC_MANIFEST.json','2dfbfb2d7ebd0cf035f90184548a8080f860bd80f072b88f9d54c7520c8f31a9'),
 'recent_priority':('CURATED_MANIFEST.json','6b14495b8be285af6e8d30084fa36593038a9174b57c5a4e19796ad5ddbe2498'),
 'quasimorphism_falsifier':('CURATED_MANIFEST.json','b8d8b8ab173ecb4c58252fb0c0c3bfb8f9c29fe6af0ef4e29957bc9fb11a8784')}
ROOT_PUBLIC=['ORIGINAL_SNAPSHOT.json','RESEARCH_CHARTER.md','RESEARCH_LOG.md',
 'PRIORITY_CHARTER.md','ROOT_INDEPENDENT_RECONSTRUCTION.md','ROOT_STATIC_AND_SOURCE_RECEIPT.json',
 'ROOT_PACKET_AUTHENTICATION.json','ROOT_PUBLICATION_REPLAY.json','ROOT_REPLAY_RECEIPT.json',
 'ROOT_REPRODUCIBILITY_FAMILY_VERIFICATION.json','ROOT_THREE_FAMILY_VERIFICATION.json',
 'ROOT_FINAL_MATH_REVIEW_VERIFICATION.json','ROOT_ADDITIONAL_PRIMARY_INSPECTION.json',
 'ROOT_PRIORITY_PLAN.md','ROOT_PRIORITY_FAMILY_VERIFICATION.json','ROOT_FINAL_PRIORITY_INSPECTION.json',
 'NEW_PRIORITY_MECHANISM_LEDGER.json','REVIEW_FAMILY_TRACKER.json','SYNTHESIS_REQUIREMENTS.md',
 'PUBLICATION_DISPOSITION.json','PR_DESCRIPTION_CORRECTED.md','PR_DESCRIPTION_REPAIR.json','WHOLE_PACKAGE_REVIEW01_ROOT_CHECK.json','GLOBAL_REPAIRS_REVIEW01.json','REVIEW01_REPAIR_REGRESSION.json','WHOLE_PACKAGE_REVIEW02_ROOT_CHECK.json','GLOBAL_REPAIRS_REVIEW02.json','REVIEW02_REPAIR_REGRESSION.json']
def require(ok,label):
 if not ok: raise RuntimeError(label)
def fp(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def records(m):
 f=m.get('files',m.get('public_files',m.get('records')))
 if type(f) is list: f={r['path']:{'bytes':r.get('bytes',r.get('size')),'sha256':r['sha256']} for r in f}
 require(type(f) is dict and bool(f),'Invalid curated map');return f
def main():
 bundle=P/'tmp/bundle'; require(not bundle.is_symlink(),'Bundle symlink')
 if bundle.exists(): shutil.rmtree(bundle)
 bundle.mkdir(parents=True); mapping={}
 def add(source,name,expected=None):
  q=PurePosixPath(name)
  require(not q.is_absolute() and q.as_posix()==name and all(x not in ('','.','..') for x in name.split('/')),'Unsafe archive path')
  require(not any(x in ('private','private_sources','raw_sources','tmp','__pycache__') for x in q.parts),'Private payload forbidden')
  require(name not in mapping and stat.S_ISREG(source.lstat().st_mode),'Duplicate/nonregular payload')
  item=fp(source)
  if type(expected) is str: require(item['sha256']==expected,'Digest changed: '+name)
  elif expected is not None: require(item=={'bytes':expected.get('bytes',expected.get('size')),'sha256':expected['sha256']},'Fingerprint changed: '+name)
  target=bundle/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,target); mapping[name]=item
 snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text()); require(snap['head']==HEAD and len(snap['files'])==44,'Wrong original target')
 for name,pin in snap['files'].items():
  require(name.startswith(PREFIX),'Wrong source prefix');add(A/'original'/name,'original_packet/'+name[len(PREFIX):],pin)
 require(fp(bundle/'original_packet/PUBLICATION_MANIFEST.json')['sha256']==PIN,'Original manifest changed')
 for family,(mapname,pin) in FAMILIES.items():
  folder=A/'reviews'/family;require(fp(folder/mapname)['sha256']==pin,'Family seal changed: '+family)
  for name,r in records(json.loads((folder/mapname).read_text())).items():add(folder/name,'reviews/'+family+'/'+name,r)
  add(folder/mapname,'reviews/'+family+'/'+mapname,pin)
 for name in ['note.tex','README.md','requirements.txt','verify_package.py','run_checked.py']:add(P/name,name)
 add(P/'output/pdf/note.pdf','note.pdf')
 for name in ROOT_PUBLIC:add(A/name,name)
 S=A/'strengthening/unsolved_math_prioritization/attempts/30003634'
 for name in ['PROOF.md','READINESS.json','ATTEMPT_LEDGER.json','NATIVE_HISTORY.jsonl','NATIVE_TURN_RECEIPT.json','NATIVE_ACCOUNTING_NOTE.md']:add(S/name,'strengthening/'+name)
 manifest={'schema_version':1,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,
  'original_packet_manifest_sha256':PIN,'scope':'Every finite positive derived depth outside integral smooth F1 for m>=3, hence every n>=1 source containment fails; all44 immutable originals with explicitn1 witness, eight curated independent families and new2/5 accounting. No firstness or current-openness certification. Raw third-party bodies excluded.',
  'files':dict(sorted(mapping.items()))}
 (bundle/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 archive=P/'deep-derived-pure-braids-source-verification-v1.0.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted([*mapping,'PACKAGE_MANIFEST.json']):
   info=zipfile.ZipInfo(name,date_time=(2026,10,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,(bundle/name).read_bytes())
 result={'manifest_sha256':fp(bundle/'PACKAGE_MANIFEST.json')['sha256'],'archive_sha256':fp(archive)['sha256'],
 'archive_bytes':archive.stat().st_size,'payload_files':len(mapping),'zip_members':len(mapping)+1,
 'original_files_unchanged':44,'authored_pdf_inside_archive_matches_separate_pdf':True,'raw_third_party_sources_distributed':False}
 (P/'BUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
