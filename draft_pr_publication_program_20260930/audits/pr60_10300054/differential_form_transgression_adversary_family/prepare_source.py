#!/usr/bin/env python3
"""One-use own SOURCE preparation; never executes the ROOT helpers."""
import datetime,hashlib,json,os,pathlib,stat,sys
root=pathlib.Path(__file__).resolve().parent
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not any((root/name).exists() for name in ('INDEX.json','READY.json','MANIFEST.json'))
for name in ('root_close.py','root_readback.py'):
 compile((root/name).read_text(),str(root/name),'exec')
record={'operation':'own SOURCE preparation, before fixed index construction','operator':'PR60 differential-form subagent /root/algebra_reproduction_audit','actual_pid':os.getpid(),'utc':utc,'argv':sys.orig_argv,'executable':sys.executable,'python':sys.version,'environment':dict(os.environ),'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'ROOT_helpers_executed':False,'ROOT_manifest_absent':True,'mathematical_approval_inferred':False}
body=json.dumps(record,indent=2)+'\n'
(root/'SOURCE_PREPARATION.start.json').write_text(body)
sys.stdout.write(body);sys.stdout.flush()
(root/'SOURCE_PREPARATION.stdout').write_text(body)
(root/'SOURCE_PREPARATION.stderr').write_bytes(b'')
with (root/'research_log.md').open('a') as stream:
 stream.write('\n'+utc+': independent verification complete100%; discovery credit0. Universal smooth proof and78 independent coordinate assertions agree with original61 exact replay. Fixed SOURCE index/READY preparation follows; ROOT helpers only syntax-compiled, never executed; ROOT manifest remains absent. Original unsolved1/5 unchanged.\n')
files=[];directories={'.':oct(0o755)}
for directory,dirs,names in os.walk(root,followlinks=False):
 for name in dirs:
  p=pathlib.Path(directory)/name;assert not p.is_symlink();p.chmod(0o755);directories[p.relative_to(root).as_posix()]=oct(0o755)
 for name in names:
  p=pathlib.Path(directory)/name;s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
  p.chmod(0o444);b=p.read_bytes()
  files.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(0o444)})
root.chmod(0o755);files.sort(key=lambda v:v['path'])
index={'schema':'pr60-form-fixed-index/v1','role':'SOURCE','directories':dict(sorted(directories.items())),'files':files,'excluded_fixed_metadata':['INDEX.json','READY.json'],'only_future_body':'MANIFEST.json'}
index_body=(json.dumps(index,indent=2)+'\n').encode();(root/'INDEX.json').write_bytes(index_body);(root/'INDEX.json').chmod(0o444)
pin=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
ready={'schema':'pr60-form-READY/v1','role':'SOURCE','index':pin(index_body),'report':pin((root/'REPORT.md').read_bytes()),'verdict':pin((root/'VERDICT.json').read_bytes()),'ROOT_manifest_absent_at_preparation':True,'ROOT_helpers_executed_by_family':False,'ROOT_mathematical_approval_inferred':False}
(root/'READY.json').write_text(json.dumps(ready,indent=2)+'\n');(root/'READY.json').chmod(0o444)
assert not (root/'MANIFEST.json').exists()
assert set(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())==set(v['path'] for v in files)|{'INDEX.json','READY.json'}
for entry in files:
 p=root/entry['path'];assert stat.S_IMODE(p.lstat().st_mode)==0o444 and p.stat().st_nlink==1
 assert len(p.read_bytes())==entry['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
for name in ('INDEX.json','READY.json'):
 assert stat.S_IMODE((root/name).lstat().st_mode)==0o444
