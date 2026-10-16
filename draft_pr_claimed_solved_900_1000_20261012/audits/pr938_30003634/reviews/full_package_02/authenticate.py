import hashlib,json,subprocess,zipfile,stat,sys,datetime
from pathlib import Path
R=Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr938_30003634'; D=A/'publication'; O=A/'reviews/full_package_02'
H='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'; prefix='unsolved_math_prioritization/attempts/30003634/'
def digest(b):return hashlib.sha256(b).hexdigest()
def get(*args):return subprocess.check_output(['git',*args],cwd=R)
def require(v,m):
 if not v:raise RuntimeError(m)
fraw=(D/'PREPUBLICATION_FREEZE.json').read_bytes();require(digest(fraw)=='75180bee0473fa3eaed6a8fdcf72695fea6646b49341979e753ccd4425ba5147','freeze external');f=json.loads(fraw)
checks={}
for name,item in f['files'].items():
 b=(D/name).read_bytes();require({'bytes':len(b),'sha256':digest(b)}==item,name);require((D/'reviewed_candidates/candidate02'/name).read_bytes()==b,'snapshot '+name)
for name,item in f['future_helpers'].items():
 b=(P/name).read_bytes();require({'bytes':len(b),'sha256':digest(b)}==item,name);require((D/'reviewed_candidates/candidate02/future_helpers'/name).read_bytes()==b,'helper snapshot '+name)
snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_bytes())
with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
 mraw=z.read('PACKAGE_MANIFEST.json');require(digest(mraw)==f['package_manifest_sha256'],'archive external manifest');m=json.loads(mraw);require(len(m['files'])==203 and len(z.infolist())==204,'count');require(len({i.filename for i in z.infolist()})==204,'duplicates')
 for name,item in m['files'].items():
  b=z.read(name);require({'bytes':len(b),'sha256':digest(b)}==item,'archive '+name)
 tree=get('ls-tree','-r','-z',H,'--',prefix).split(b'\0');rows=[x for x in tree if x];require(len(rows)==44 and len(snap['files'])==44,'original count')
 for row in rows:
  meta,path=row.split(b'\t');mode,kind,blob=meta.decode().split();name=path.decode();b=get('cat-file','blob',blob);disk=A/'original'/name;aname='original_packet/'+name[len(prefix):]
  require(kind=='blob' and mode=='100644' and stat.S_ISREG(disk.lstat().st_mode),'actual original mode '+name)
  require(stat.S_IMODE(disk.stat().st_mode)==0o644 and z.getinfo(aname).external_attr>>16==0o100644,'disk/archive exact mode '+name)
  require(disk.read_bytes()==b and z.read(aname)==b and digest(b)==snap['files'][name],'actual git mismatch '+name)
  checks[name]={'git_mode':mode,'disk_mode':'0644','archive_mode':'100644','git_blob':blob,'bytes':len(b),'sha256':digest(b),'disk_and_archive_match':True}
 branch=get('branch','--show-current').decode().strip();require(branch=='main','main')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'branch_observed':branch,'original_pr_head':H,'freeze_sha256':digest(fraw),'manifest_sha256':digest(mraw),'pdf_sha256':digest((D/'output/pdf/note.pdf').read_bytes()),'frozen_files':len(f['files']),'future_helpers':f['future_helpers'],'payloads':len(m['files']),'archive_members':204,'all_actual_git_blob_mode_disk_archive_checks':checks,'status':'PASS'}
(O/sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='all_actual_git_blob_mode_disk_archive_checks'},indent=2))
