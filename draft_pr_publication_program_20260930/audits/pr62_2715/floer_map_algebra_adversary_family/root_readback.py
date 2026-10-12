#!/usr/bin/env python3
"""Separate ROOT read-only readback. Not executed by this family."""
import datetime,hashlib,json,os,pathlib,stat,sys
ROOT=pathlib.Path(__file__).resolve().parent
def descriptor(path):
 p=ROOT/path;s=p.lstat()
 assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 return {'path':path,'bytes':s.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(stat.S_IMODE(s.st_mode))}
def prepared(with_manifest):
 index=json.loads((ROOT/'INDEX.json').read_bytes());ready=json.loads((ROOT/'READY.json').read_bytes())
 assert index['role']=='SOURCE' and ready['role']=='SOURCE'
 assert index['excluded_fixed_metadata']==['INDEX.json','READY.json'] and index['only_future_body']=='MANIFEST.json'
 assert all(mode=='0o755' for mode in index['directories'].values())
 entries=index['files'];paths=[v['path'] for v in entries]
 assert len(paths)==len(set(paths))
 for path in paths:
  p=pathlib.PurePosixPath(path)
  assert not p.is_absolute() and '..' not in p.parts and path not in ('INDEX.json','READY.json','MANIFEST.json')
 expected=set(paths)|{'INDEX.json','READY.json'}
 if with_manifest:expected.add('MANIFEST.json')
 actual_files=set();actual_dirs={'.'}
 for directory,dirs,files in os.walk(ROOT,followlinks=False):
  for name in dirs+files:
   p=pathlib.Path(directory)/name;s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
   rel=p.relative_to(ROOT).as_posix()
   if stat.S_ISDIR(s.st_mode):actual_dirs.add(rel)
   else:assert stat.S_ISREG(s.st_mode);actual_files.add(rel)
 assert actual_files==expected and actual_dirs==set(index['directories'])
 for path in actual_dirs:
  assert stat.S_IMODE((ROOT/path).lstat().st_mode)==0o755
 for entry in entries:
  assert descriptor(entry['path'])==entry and entry['mode']=='0o444'
 for name in ('INDEX.json','READY.json'):
  assert descriptor(name)['mode']=='0o444'
 for key,name in (('index','INDEX.json'),('report','REPORT.md'),('verdict','VERDICT.json')):
  assert ready[key]=={k:v for k,v in descriptor(name).items() if k in ('bytes','sha256')}
 assert ready['ROOT_manifest_absent_at_preparation'] is True and ready['ROOT_mathematical_approval_inferred'] is False
 assert ready['ROOT_helpers_executed_by_family'] is False
 return index,ready,entries+[descriptor('INDEX.json'),descriptor('READY.json')]
if __name__=='__main__':
 index,ready,entries=prepared(True)
 manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
 assert descriptor('MANIFEST.json')['mode']=='0o444'
 assert manifest['files']==entries and manifest['directories']==index['directories']
 assert manifest['literal_self_exclusion']=='MANIFEST.json'
 assert manifest['role']=='SOURCE' and manifest['operator']=='ROOT'
 assert isinstance(manifest['actual_pid'],int) and manifest['actual_pid']>0
 assert manifest['mathematical_approval_inferred'] is False
 print(json.dumps({'operation':'ROOT read-only SOURCE readback','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prepared_regular_bodies':len(entries),'manifest_self_excluded':True,'manifest_sha256':descriptor('MANIFEST.json')['sha256'],'mathematical_approval_inferred':False}))
