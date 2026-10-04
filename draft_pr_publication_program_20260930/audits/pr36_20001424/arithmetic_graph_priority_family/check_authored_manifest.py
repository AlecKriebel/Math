"""Strict, self-excluding authored closure. Foreign source downloads live in ignored tmp/."""
from pathlib import Path,PurePosixPath
import json,hashlib,sys,datetime,shutil
D=Path(__file__).resolve().parent
M='AUTHORED_MANIFEST.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def authored(root):
 out=[]
 for p in root.rglob('*'):
  rel=p.relative_to(root).as_posix()
  if rel=='tmp' or rel.startswith('tmp/'):continue
  if p.is_symlink():raise ValueError('symlink in authored closure: '+rel)
  if p.is_file() and rel!=M:out.append(rel)
 return sorted(out)
def make(root):
 result={'schema':'strict-self-excluding-authored-closure-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'self_excluded':[M],'excluded_roots':['tmp/'],'foreign_source_rule':'Downloaded foreign sources and derivatives stay only in ignored tmp/foreign_sources. Their retrieval hashes are in authored receipts; foreign bytes are never packaged as authored outputs.','files':[{'path':f,'bytes':(root/f).stat().st_size,'sha256':sha(root/f)} for f in authored(root)]}
 (root/M).write_text(json.dumps(result,indent=2)+'\n');return result

def verify(root):
 m=json.loads((root/M).read_text())
 if m.get('schema')!='strict-self-excluding-authored-closure-v1' or m.get('self_excluded')!=[M] or m.get('excluded_roots')!=['tmp/']:raise ValueError('Invalid closure schema/exclusions')
 paths=[]
 for item in m['files']:
  rel=item['path'];p=PurePosixPath(rel)
  if p.is_absolute() or '..' in p.parts or rel!=p.as_posix() or rel==M or rel.startswith('tmp/') or rel in paths:raise ValueError('Unsafe/duplicate/excluded path: '+rel)
  paths.append(rel)
  f=root/rel
  if f.is_symlink() or not f.is_file():raise ValueError('Missing/unsafe file: '+rel)
  if f.stat().st_size!=item['bytes'] or sha(f)!=item['sha256']:raise ValueError('Size/hash mismatch: '+rel)
 if sorted(paths)!=authored(root):raise ValueError('Authored inventory mismatch')
 return {'status':'PASS','authored_file_count':len(paths),'self_excluded_manifest_only':True,'foreign_root_excluded':True,'sha256_of_manifest':sha(root/M)}

def controls():
 base=D/'tmp/manifest_controls';base.mkdir(parents=True,exist_ok=True)
 files=authored(D)+[M]
 results=[]
 for name in ['unchanged','hash_corruption','file_omitted','extra_authored','path_traversal','foreign_inclusion','ignored_foreign_positive']:
  dst=base/name
  if dst.exists():shutil.rmtree(dst)
  dst.mkdir()
  for f in files:
   (dst/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/f,dst/f)
  if name=='hash_corruption':
   with (dst/'REPORT.md').open('a') as out:out.write('\nCORRUPTED\n')
  elif name=='file_omitted':(dst/'REPORT.md').unlink()
  elif name=='extra_authored':(dst/'UNACCOUNTED.md').write_text('unexpected authored file\n')
  elif name=='path_traversal':
   m=json.loads((dst/M).read_text());m['files'][0]['path']='../REPORT.md';(dst/M).write_text(json.dumps(m))
  elif name=='foreign_inclusion':
   m=json.loads((dst/M).read_text());m['files'].append({'path':'tmp/foreign_sources/silverman1995.pdf','bytes':0,'sha256':'0'*64});(dst/M).write_text(json.dumps(m))
  elif name=='ignored_foreign_positive':
   (dst/'tmp/foreign_sources').mkdir(parents=True);(dst/'tmp/foreign_sources/test.pdf').write_bytes(b'Foreign data ignored')
  expected=name in ['unchanged','ignored_foreign_positive']
  try:r=verify(dst);passed=True;reason=r
  except Exception as e:passed=False;reason=str(e)
  if passed!=expected:raise AssertionError((name,passed,expected,reason))
  results.append({'case':name,'expected_accept':expected,'actual_accept':passed,'correct_result':True,'observed':reason})
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_controls':results,'all_seven_controls_correct':True}
 (D/'AUTHORED_MANIFEST_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 if '--make' in sys.argv:print(json.dumps({'manifest_created':True,'files':len(make(D)['files'])}))
 elif '--controls' in sys.argv:print(json.dumps(controls(),indent=2))
 else:print(json.dumps(verify(D),indent=2))
