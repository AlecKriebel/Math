#!/usr/bin/env python3
"""Portable fail-closed audit replay. All optional evidence is caller supplied.
No network and no writes to supplied inputs. Negative tests use temporary copies.
"""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile,zipfile,shutil
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_MANIFEST_SHA='28ec0d19ba6891338c95a37f24d8842de69300cb78984a65367b465596704920'
AUTHOR_ZIP_SHA='6ba3c58803407218391afc5d045939f8c3f0e8d750756e516aa5de0c300a7e01'
def sha(b):return hashlib.sha256(b).hexdigest()
def failif(b,msg):
 if b: raise AssertionError(msg)
def inventory(root):
 failif(any(p.is_symlink() for p in root.rglob('*')),'symlink')
 return {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
def verify_author(d):
 b=(d/'AUTHOR_MANIFEST.json').read_bytes()
 failif(sha(b)!=AUTHOR_MANIFEST_SHA,'author manifest anchor')
 m=json.loads(b); expected={x['path'] for x in m['files']}|{'AUTHOR_MANIFEST.json'}
 failif(inventory(d)!=expected,'author recursive inventory')
 for x in m['files']:
  p=pathlib.PurePosixPath(x['path']);failif(p.is_absolute() or '..' in p.parts,'unsafe path')
  b=(d/x['path']).read_bytes(); failif(len(b)!=x['bytes'] or sha(b)!=x['sha256'],'author file '+x['path'])
 return expected
def run(p):return subprocess.run([sys.executable,'-B',str(p)],capture_output=True,check=True).stdout
def expect_reject(fn):
 try:fn()
 except (AssertionError,FileNotFoundError,json.JSONDecodeError):return True
 raise AssertionError('mutation was not rejected')
def main():
 p=argparse.ArgumentParser();p.add_argument('--author-dir',type=pathlib.Path,required=True)
 p.add_argument('--author-zip',type=pathlib.Path);p.add_argument('--source-dir',type=pathlib.Path)
 p.add_argument('--problems',type=pathlib.Path);p.add_argument('--research-results',type=pathlib.Path)
 p.add_argument('--catalog',type=pathlib.Path);p.add_argument('--queue',type=pathlib.Path)
 a=p.parse_args();result={'status':'PASS'}
 m=json.loads((ROOT/'AUDIT_MANIFEST.json').read_text())
 failif(inventory(ROOT)!={x['path'] for x in m['files']}|{'AUDIT_MANIFEST.json'},'audit inventory')
 for x in m['files']:
  b=(ROOT/x['path']).read_bytes();failif(len(b)!=x['bytes'] or sha(b)!=x['sha256'],'audit hash '+x['path'])
 result['audit_files']=len(m['files'])+1
 expected=verify_author(a.author_dir); result['author_files']=len(expected)
 author=run(a.author_dir/'verify_math.py'); failif(author!=(a.author_dir/'CHECK_RESULTS.json').read_bytes(),'author replay')
 result['author_controls']=json.loads(author)['total_checks'];failif(result['author_controls']!=4455,'author count')
 independent=run(ROOT/'verify_independent.py');failif(independent!=(ROOT/'INDEPENDENT_RESULTS.json').read_bytes(),'independent replay')
 result['independent_controls']=json.loads(independent)['total_checks']
 result['author_zip_checked']=False
 if a.author_zip:
  b=a.author_zip.read_bytes();failif(len(b)!=18835 or sha(b)!=AUTHOR_ZIP_SHA,'archive anchor')
  with zipfile.ZipFile(a.author_zip) as z:
   names=z.namelist();failif(len(names)!=len(set(names)) or set(names)!={'kourovka_2551/'+n for n in expected},'archive inventory')
   failif(any(z.read(n)!=(a.author_dir/pathlib.PurePosixPath(n).name).read_bytes() for n in names),'archive content')
  result['author_zip_checked']=True
 evidence=json.loads((ROOT/'EVIDENCE_METADATA.json').read_text())
 result['scholarly_hashes_checked']=0
 if a.source_dir:
  for s in evidence['fresh_source_retrievals']:
   b=(a.source_dir/s['replay_filename']).read_bytes()
   failif(len(b)!=s['bytes'] or sha(b)!=s['sha256'],'source '+s['title'])
   result['scholarly_hashes_checked']+=1
 result['dataset_inputs_checked']=[]
 for name,path in [('problems.json',a.problems),('research_results.json',a.research_results),('catalog.json',a.catalog),('QUEUE.md',a.queue)]:
  if path is None:continue
  b=path.read_bytes();pin=evidence['data_pins'][name]
  failif(len(b)!=pin['bytes'] or sha(b)!=pin['sha256'],'data pin '+name)
  if 'git_blob_sha1' in pin:failif(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=pin['git_blob_sha1'],'git identity')
  if name=='problems.json':
   data=json.loads(b);selected=[x for x in data if str(x.get('id'))=='2551']
   failif(len(data)!=15458 or len(selected)!=1 or selected[0]['problem_number']!='KOU-21.42','problem identity')
  elif name=='catalog.json':
   selected=[x for x in json.loads(b) if str(x.get('id'))=='2551']
   failif(len(selected)!=1 or selected[0]['rank']!=768 or selected[0]['problem_number']!='KOU-21.42','catalog identity')
  elif name=='research_results.json':
   data=json.loads(b)
   failif(len(data)!=6701 or any(k.startswith('KOU') for k in data),'research key controls')
   failif(any('KOU-21.42' in json.dumps(v) or 'Kourovka Notebook Problem 21.42' in json.dumps(v) for v in data.values()),'research target control')
  else:
   rows=[line for line in b.decode().splitlines() if '| 2551 /' in line]
   failif(len(rows)!=1 or 'KOU-21.42' not in rows[0] or '| queued |' not in rows[0] or '| 0/5 |' not in rows[0],'queue identity')
  result['dataset_inputs_checked'].append(name)
 # Freeze mutations must fail before running any untrusted changed author code.
 mutation={}
 with tempfile.TemporaryDirectory(prefix='kourovka-audit-') as t:
  root=pathlib.Path(t)
  for kind in ['changed_bytes','missing_file','extra_file','nested_file','manifest_changed']:
   dest=root/kind;shutil.copytree(a.author_dir,dest)
   if kind=='changed_bytes':(dest/'RESULT.md').write_bytes((dest/'RESULT.md').read_bytes()+b'\n')
   if kind=='missing_file':(dest/'RESULT.md').unlink()
   if kind=='extra_file':(dest/'EXTRA.txt').write_text('mutation')
   if kind=='nested_file':(dest/'nested').mkdir();(dest/'nested'/'EXTRA.txt').write_text('mutation')
   if kind=='manifest_changed':(dest/'AUTHOR_MANIFEST.json').write_bytes((dest/'AUTHOR_MANIFEST.json').read_bytes()+b' ')
   mutation[kind]=expect_reject(lambda:verify_author(dest))
 result['freeze_mutations_rejected']=mutation
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
