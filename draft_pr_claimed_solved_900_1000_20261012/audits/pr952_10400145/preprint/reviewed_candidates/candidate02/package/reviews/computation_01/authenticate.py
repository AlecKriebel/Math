from pathlib import Path
import json,hashlib,stat,subprocess,datetime,platform,sys
A=Path(__file__).resolve().parents[2]
W=Path(__file__).resolve().parent
root=Path('/Users/alec/Documents/Math')
r=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_text()); s=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':r['head'],'host':platform.platform(),'python':sys.version,'records_sha256':hashlib.sha256((A/'ORIGINAL_FILE_RECORDS.json').read_bytes()).hexdigest(),'snapshot_sha256':hashlib.sha256((A/'ORIGINAL_SNAPSHOT.json').read_bytes()).hexdigest(),'files':{}}
for name,expect in r['files'].items():
 p=A/'original'/name; b=p.read_bytes(); sha=hashlib.sha256(b).hexdigest(); mode=f'{stat.S_IMODE(p.lstat().st_mode):04o}'
 blob=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
 gitb=subprocess.run(['git','cat-file','blob',r['head']+':'+name],cwd=root,capture_output=True,check=True).stdout
 tree=subprocess.run(['git','ls-tree',r['head'],'--',name],cwd=root,capture_output=True,text=True,check=True).stdout.split()
 checks={'regular':stat.S_ISREG(p.lstat().st_mode),'bytes':len(b)==expect['bytes'],'sha256':sha==expect['sha256']==s['files'][name],'disk_mode':mode==expect['disk_mode'],'git_blob':blob==expect['git_blob']==tree[2],'git_mode':tree[0]==expect['git_mode'],'immutable_git_bytes':gitb==b}
 out['files'][name]={'bytes':len(b),'sha256':sha,'disk_mode':mode,'git_blob':blob,'git_mode':tree[0],'checks':checks}
out['count']=len(out['files']); out['pass']=out['count']==33 and all(all(f['checks'].values()) for f in out['files'].values())
dest=W/(sys.argv[1] if len(sys.argv)>1 else 'START.json'); dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'receipt':dest.name,'count':out['count'],'pass':out['pass'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
if not out['pass']: raise SystemExit(1)
