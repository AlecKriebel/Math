import sys
if not sys.flags.safe_path: raise SystemExit('safe startup required')
import os,json,pathlib,hashlib,zipfile,stat,subprocess,datetime
R=pathlib.Path('/Users/alec/Documents/Math'); A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001'; D=A/'preprint'; W=A/'reviews/full_package_01'
HEAD='7d3adb0e500b0414a49a449e7981d34ade329427'
PINS={'freeze':'715717bdbb17b9c20ded279496e7b5b4ceb439e7d86e20eb238a067efd308920','ops':'95cc6ec6c6d824b9e678b77f9f405ba0ece03aef506821e8ff4c98da385009c8','manifest':'52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec','pdf':'5672873695bd71ff852fc8631e5ba980adffc4025b42ecb38d2617a8673ebb63','zip':'a5a7e176162a67aaaca22650ea0564e8b926ead42206881b45f109f4b4fa3c97','outer':'c4f9be04d187ce46f55535d7f6050b21da084730e906274c293f3ec9fa5d1b56','verifier':'1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d'}
def require(b,msg):
 if not b: raise ValueError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
 require(not p.is_symlink() and p.is_file(),str(p));return p.read_bytes()
def fp(b):return {'bytes':len(b),'sha256':sha(b)}
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
fraw=read(D/'FREEZE.json');require(sha(fraw)==PINS['freeze'],'freeze external pin');f=json.loads(fraw)
opsraw=read(A/'OPERATIONS_INVENTORY.json');require(sha(opsraw)==PINS['ops'],'operations external pin');ops=json.loads(opsraw)
require(len(ops['files'])==7,'operations count')
checked_ops={}
for name,v in ops['files'].items():
 b=read(R/name);require(fp(b)==v,'operation '+name);checked_ops[name]=v
for name,v in f['future_helpers'].items():require(ops['files']['draft_pr_claimed_solved_900_1000_20261012/'+name]==v,'future helper '+name)
for name,v in f['files'].items():require(fp(read(D/name))==v,'frozen '+name)
for name,v in f['evidence_files'].items():require(fp(read(R/name))==v,'evidence '+name)
require(sha(read(D/'global_hessian_verification.zip'))==PINS['zip'],'zip pin');require(sha(read(D/'package/PACKAGE_MANIFEST.json'))==PINS['manifest'],'inner pin');require(sha(read(D/'research_note.pdf'))==PINS['pdf'],'pdf pin');require(sha(read(D/'package/verify_package.py'))==PINS['verifier'],'verifier pin')
original=json.loads(read(A/'ORIGINAL_SNAPSHOT.json'));require(original['head']==HEAD,'head');require(len(original['files'])==33,'33 original files')
with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
 infos=z.infolist();names=[i.filename for i in infos];require(len(names)==len(set(names))==220,'unique220')
 for i in infos:
  p=pathlib.PurePosixPath(i.filename);mode=i.external_attr>>16
  require(not p.is_absolute() and '..' not in p.parts and str(p)==i.filename and all(q not in ('','.','..') for q in p.parts),'unsafe archive name')
  require(stat.S_ISREG(mode) and not i.is_dir(),'nonregular archive '+i.filename)
  require(not any(str(p).startswith(n+'/') for n in names if n!=str(p)),'ancestor file')
 outerraw=z.read('ARCHIVE_MANIFEST.json');require(sha(outerraw)==PINS['outer'],'outer pin');outer=json.loads(outerraw)
 require(set(outer['files'])==set(names)-{'ARCHIVE_MANIFEST.json'},'closed outer inventory')
 for name,v in outer['files'].items():require(fp(z.read(name))==v,'outer '+name)
 require(z.read('research_note.pdf')==read(D/'research_note.pdf'),'identical pdf')
 originals={}
 for name,v in original['files'].items():
  tree=git('ls-tree',HEAD,'--',name).decode().strip().split();require(len(tree)==4,'tree '+name);mode,typ,blob,actual=tree;require(mode=='100644' and typ=='blob' and actual==name,'Git mode')
  gb=git('cat-file','blob',blob);b=read(A/'original'/name);require(sha(gb)==v and b==gb,'Git disk original '+name)
  arc='package/original/'+name;ab=z.read(arc);amode=z.getinfo(arc).external_attr>>16
  require(ab==gb and amode==0o100644 and stat.S_IMODE((A/'original'/name).stat().st_mode)==0o644,'archive/disk mode '+name)
  originals[name]={'bytes':len(gb),'sha256':v,'git_blob':blob,'git_mode':'100644','disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
# Read only target row from immutable complete queue blob.
q=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode();rows=[x for x in q.splitlines() if '| 6000001 / AMR-059-0001 |' in x];require(len(rows)==1,'exact target queue row');require('claimed_solved' in rows[0] and '4/5' in rows[0],'declared4/5')
require(git('branch','--show-current').decode().strip()=='main','main')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_pr_head':HEAD,'freeze_sha256':PINS['freeze'],'package_manifest_sha256':PINS['manifest'],'future_helpers':f['future_helpers'],'candidate_files':f['files'],'payloads':219,'archive_members':220,'originals':originals,'operations_inventory_sha256':PINS['ops'],'operations_files':checked_ops,'evidence_files':f['evidence_files'],'archive_sha256':PINS['zip'],'archive_manifest_sha256':PINS['outer'],'original_queue_row':rows[0],'branch':'main','trusted_bootstrap':'Python -I, interpreter and standard library, git executable; no artifact code executed'}
name=sys.argv[1];require(name in ['AUTHENTICATION_START.json','AUTHENTICATION_END.json'],'output name');(W/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','utc':result['utc'],'originals':len(originals),'frozen_files':len(f['files']),'operations':len(checked_ops),'queue':rows[0]}))
