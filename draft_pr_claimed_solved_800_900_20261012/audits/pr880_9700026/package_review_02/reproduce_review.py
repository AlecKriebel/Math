#!/usr/bin/env python3
"""Independent PR880 review replay; writes only this review directory. No publication."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction as F
import ast, hashlib, io, json, os, stat, subprocess, sys, tempfile, zipfile
R=Path(__file__).resolve().parent
A=R.parent
P=A/'preprint'
O=A/'replay/revision_r1'
V=A/'replay/portable_r1_polished'
ROOT=A.parents[2]
T=R/'private'/'execution'
T.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(T)
tempfile.tempdir=str(T)
SHAS={'seal':'d747f3188be029b1e7b6806effc707f059913679a1734cd5c0a59109ade668dd','outer':'11258d48f5ba2c0c0d5bd1893c1aaba8ac2fe3c2c4cd042181ba22f25f8decc2','index':'7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d','wrapper':'b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7','verifier':'73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a','checker':'e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f','builder':'a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca','assembler':'939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055','zip':'944e5d99825a3ef6689cff551f28bc9bb7aee04a1f58dbbceb6fd55bace4af2f'}
def ck(c,m):
 if not c: raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,value):(R/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def pins():
 for path,key in [(A/'PACKAGE_SEAL_R1.json','seal'),(O/'PUBLICATION_MANIFEST.json','outer'),(V/'package_index.json','index'),(O/'verify_current_publication.py','wrapper'),(V/'verify_package.py','verifier'),(V/'check_originals.py','checker'),(V/'build_verification.py','builder'),(A/'local_tools/pr880_assemble.py','assembler'),(P/'verification.zip','zip')]:ck(sha(path.read_bytes())==SHAS[key],'startup '+key)
def inventory():
 results={}
 for root,index_name,count in [(O,'PUBLICATION_MANIFEST.json',215),(V,'package_index.json',161)]:
  raw=(root/index_name).read_bytes();idx=json.loads(raw);files=idx['files'];names={r['path'] for r in files}|{index_name}
  actual={p.relative_to(root).as_posix() for p in root.rglob('*') if not p.is_dir()}
  ck(names==actual and len(names)==count and len(files)==count-1,'closed inventory')
  for p in root.rglob('*'):ck(stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode),'nonregular candidate')
  for row in files:
   data=(root/row['path']).read_bytes();ck(len(data)==row['bytes'] and sha(data)==row['sha256'],'row pin')
  results[root.name]={'files':count,'indexed_files':len(files),'index_sha256':sha(raw),'verified_independently':True}
 seal=json.loads((A/'PACKAGE_SEAL_R1.json').read_bytes())
 for row in seal['core_files']:
  data=(P/row['path']).read_bytes();ck((len(data),sha(data))==(row['bytes'],row['sha256']),'core pin')
 # Independently compare every portable ZIP member with actual portable files.
 zr=P/'verification.zip'
 with zipfile.ZipFile(zr) as z:
  ck(z.namelist()==sorted(names:={p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file()}),'ZIP names')
  for info in z.infolist():
   ck(z.read(info)==(V/info.filename).read_bytes(),'ZIP payload')
   ck(info.date_time==(2026,10,15,0,0,0) and info.external_attr==(stat.S_IFREG|0o644)<<16,'ZIP metadata')
  ck(z.testzip() is None,'CRC')
 results['core_count']=len(seal['core_files']);results['zip_members_compared']=len(names)
 # Read-only local Git object comparison; does not update refs or index.
 prefix='unsolved_math_prioritization/attempts/9700026/'
 preview='b0a238c2704c1d5d2a444058d095563cec30e501'
 tree=subprocess.run(['git','ls-tree','-r',preview,'--',prefix],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
 entries={line.split('\t')[1][len(prefix):]:line.split()[2] for line in tree}
 actual={p.relative_to(O).as_posix():p for p in O.rglob('*') if p.is_file()}
 ck(set(entries)==set(actual),'preview tree names')
 for n,p in actual.items():
  b=p.read_bytes();ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entries[n],'preview blob '+n)
 results['preview']={'commit':preview,'files':len(entries),'all_git_blob_identities_match':True}
 frozen=json.loads((A/'SOURCE_MANIFEST.json').read_bytes())
 old=subprocess.run(['git','ls-tree','-r','fba74a301786f9648e48722e76f440097b0746c2','--',prefix],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
 oldmap={line.split('\t')[1][len(prefix):]:line.split()[2] for line in old}
 ck(set(oldmap)=={r['path'] for r in frozen['files']} and all(oldmap[r['path']]==r['git_blob'] for r in frozen['files']),'frozen real Git tree')
 results['frozen_original_commit']={'commit':'fba74a301786f9648e48722e76f440097b0746c2','all_40_manifest_git_blobs_match_real_local_tree':True}
 dump('INDEPENDENT_INVENTORY.json',results)
 return results

def execute(cmd,name):
 proc=subprocess.run(cmd,cwd=R,env=os.environ,capture_output=True,timeout=800)
 
 if proc.returncode or proc.stderr:
  dump('FAILED_'+name,{'returncode':proc.returncode,'stdout':proc.stdout.decode(errors='replace'),'stderr':proc.stderr.decode(errors='replace'),'free_bytes':__import__('shutil').disk_usage(R).free})
 ck(proc.returncode==0 and not proc.stderr,'execution '+name+' '+str(proc.returncode)+' '+proc.stderr.decode(errors='replace')+' '+proc.stdout.decode(errors='replace')[:400])
 result=json.loads(proc.stdout);ck(result['status']=='PASS','status '+name);(R/name).write_bytes(proc.stdout);return result

def replay_and_build():
 out=[]
 for opt in (False,True):
  label='OPTIMIZED' if opt else 'NORMAL';base=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])
  result=execute(base+[str(O/'verify_current_publication.py'),SHAS['outer'],'--root',str(O),'--full'],'OUTER_FULL_'+label+'.json')
  replay=result['inner_verifier_result']['full_replay'];ck(len(replay['receipts'])==8 and replay['source_replay']=='NOT_RUN','source-free truth')
  with tempfile.TemporaryDirectory(prefix='fresh build with spaces ') as td:
   built=execute(base+[str(P/'build_verification.py'),str(V),SHAS['index'],SHAS['verifier'],str(Path(td)/'new archive output')],'FRESH_BUILD_'+label+'.json')
   ck(built['sha256']==SHAS['zip'] and built['bytes']==568282 and Path(built['archive']).read_bytes()==(P/'verification.zip').read_bytes(),'fresh archive byte equality')
  out.append({'mode':label,'outer_receipts':len(replay['receipts']),'source_replay':replay['source_replay'],'fresh_build_byte_identical':True})
 # Optional complete source path, real files only, no copies and no shortened pair.
 sources=['--catalog',str(ROOT/'unsolved_math_prioritization/catalog.json'),'--problems',str(ROOT/'unsolved_math_prioritization/cache/problems.json'),'--reports',str(ROOT/'unsolved_math_prioritization/cache/research_results.json'),'--pdf-dir',str(A/'private_sources'),'--pdf-2012',str(A/'private_sources/1209.5120v1.pdf')]
 before=[]
 for p in [Path(sources[i+1]) for i in (0,2,4,8)]+[A/'private_sources/cities-notes.pdf']:
  s=p.stat();before.append((p,s.st_size,s.st_mtime_ns,s.st_mode,s.st_ino,s.st_nlink))
 result=execute([sys.executable,'-I','-S','-B',str(O/'verify_current_publication.py'),SHAS['outer'],'--root',str(O),'--full',*sources],'OUTER_COMPLETE_INPUTS.json')
 replay=result['inner_verifier_result']['full_replay'];ck(len(replay['receipts'])==10 and replay['source_replay']=='PASS','complete source replay')
 for p,size,mtime,mode,ino,links in before:
  s=p.stat();ck((s.st_size,s.st_mtime_ns,s.st_mode,s.st_ino,s.st_nlink)==(size,mtime,mode,ino,links),'source inode changed')
 out.append({'mode':'COMPLETE_INPUTS','outer_receipts':10,'source_replay':'PASS','original_input_stat_and_link_counts_unchanged':True})
 dump('REPRODUCTION_SUMMARY.json',out)

def privacy():
 import re
 rows=[];forbidden=[];credential=[]
 def visit(data,label,depth=0):
  ck(depth<=5,'nested depth')
  if data.startswith(b'PK\x03\x04'):
   with zipfile.ZipFile(io.BytesIO(data)) as z:
    for i in z.infolist():
     ck(not i.is_dir() and i.file_size<5_000_000,'unexpected archive member')
     d=z.read(i);rows.append({'archive_path':label+'!'+i.filename,'bytes':len(d),'sha256':sha(d)})
     parts=Path(i.filename).parts
     if any(t.lower() in ('private','private_sources','rendered','__pycache__') for t in parts) or i.filename.endswith(('.png','.jpg','.jpeg','.pyc')):forbidden.append(label+'!'+i.filename)
     if d.startswith(b'%PDF') and i.filename!='note.pdf':forbidden.append(label+'!'+i.filename)
     # Literal high-confidence secret formats only; no raw matches emitted.
     if re.search(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{32,}',d):credential.append(label+'!'+i.filename)
     visit(d,label+'!'+i.filename,depth+1)
 visit((P/'verification.zip').read_bytes(),'verification.zip')
 ck(not forbidden and not credential,'privacy match requires inspection')
 rawpair=(R/'private/complete_target_pair.json').read_bytes() if (R/'private/complete_target_pair.json').exists() else None
 primary=[p.read_bytes() for p in [A/'private_sources/cities-notes.pdf',A/'private_sources/1209.5120v1.pdf',A/'priority_direct_audit_01/private_sources/eulersolve_0023_v1.pdf',A/'priority_structural_audit_01/private/aurenhammer1984.pdf']]
 private_payload_hits=[]
 regular_count=0
 for p in V.rglob('*'):
  if p.is_file():
   data=p.read_bytes();regular_count+=1
   if (rawpair is not None and rawpair in data) or any(q in data for q in primary):private_payload_hits.append(p.relative_to(V).as_posix())
 ck(not private_payload_hits,'exact private payload leaked')
 result={'status':'PASS','archive_member_occurrences_recursively_scanned':len(rows),'archives_depth_limit':5,'forbidden_name_or_primary_PDF_hits':forbidden,'high_confidence_credential_pattern_hits':credential,'limitations':'Names, magic bytes and bounded signature scan plus reviewed inventories; not a universal DLP guarantee. References and input hashes are permitted; all review source extracts/renders/fixtures stay private.','members':rows,'exact_complete_target_pair_or_full_primary_PDF_byte_substring_hits':private_payload_hits,'regular_files_checked_for_exact_private_payloads':regular_count,'exact_pair_substring_check': 'PASS' if rawpair is not None else 'NOT_RUN'}
 dump('ARCHIVE_PRIVACY.json',result)

if __name__=='__main__':
 ck(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'use -I -S -B')
 pins();inventory();replay_and_build();privacy();print('PASS independent inventories, fresh replay/builds, complete-source hardlinks, recursive privacy')
