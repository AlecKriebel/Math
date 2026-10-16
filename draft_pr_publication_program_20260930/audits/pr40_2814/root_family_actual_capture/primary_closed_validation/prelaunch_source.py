#!/usr/bin/env python3
"""Strict full family closure; only two explicit ROOT directories and ROOT self are excluded."""
import argparse,datetime,hashlib,json,pathlib,re,shutil,subprocess,sys
SELF='FIRST_PARTY_MANIFEST.json'
EXCLUDED={'foreign_cache','ignored_tmp'}
def sha(b):return hashlib.sha256(b).hexdigest()
def inventory(root):
 rows=[]
 def visit(d):
  for p in sorted(d.iterdir()):
   rel=p.relative_to(root)
   if p.is_symlink():raise ValueError('symlink '+str(rel))
   if d==root and p.is_dir() and p.name in EXCLUDED:continue
   if p.is_dir():visit(p)
   elif p.is_file():
    if str(rel)==SELF:continue
    b=p.read_bytes();rows.append({'path':rel.as_posix(),'size':len(b),'sha256':sha(b)})
   else:raise ValueError('nonregular '+str(rel))
 visit(root);return sorted(rows,key=lambda r:r['path'])
def verify(root):
 m=json.loads((root/SELF).read_bytes())
 if m.get('schema')!='pr40-primary-first-party/v1' or m.get('status')!='CLOSED' or m.get('excluded_root_directories')!=sorted(EXCLUDED) or not isinstance(m.get('files'),list):raise ValueError('manifest header')
 seen=set()
 for r in m['files']:
  if set(r)!={'path','size','sha256'} or type(r['size']) is not int or r['size']<0 or not isinstance(r['path'],str) or not isinstance(r['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',r['sha256']):raise ValueError('manifest row')
  q=pathlib.PurePosixPath(r['path'])
  if q.is_absolute() or q.as_posix()!=r['path'] or any(x in {'.','..'} for x in q.parts) or q.parts[0] in EXCLUDED or r['path']==SELF or r['path'] in seen:raise ValueError('unsafe/duplicate manifest path')
  seen.add(r['path'])
 actual=inventory(root)
 if actual!=m['files']:raise ValueError('full first-party byte or membership mismatch')
 return {'status':'PASS','files':len(actual),'manifest_sha256':sha((root/SELF).read_bytes()),'strict_root_only_exclusions':True}
def tests(out):
 out.mkdir(exist_ok=False); source=pathlib.Path(__file__).resolve();results=[];payload=b'Actual closed-file provenance test input.\n'
 for label in ['baseline','extra_regular','nested_self_name','changed_bytes','missing_payload','symlink_payload','boolean_size']:
  d=out/label;d.mkdir();(d/'payload.txt').write_bytes(payload);m={'schema':'pr40-primary-first-party/v1','status':'CLOSED','excluded_root_directories':sorted(EXCLUDED),'files':[{'path':'payload.txt','size':len(payload),'sha256':sha(payload)}]}
  if label=='extra_regular':(d/'extra.txt').write_text('unexpected')
  if label=='nested_self_name':(d/'nested').mkdir();(d/'nested'/SELF).write_text('{}\n')
  if label=='changed_bytes':(d/'payload.txt').write_bytes(payload+b'changed')
  if label=='missing_payload':(d/'payload.txt').unlink()
  if label=='symlink_payload':(d/'payload.txt').unlink();(d/'target.txt').write_bytes(payload);(d/'payload.txt').symlink_to('target.txt')
  if label=='boolean_size':m['files'][0]['size']=True
  (d/SELF).write_text(json.dumps(m,indent=2)+'\n');argv=['/usr/bin/python3',str(source),'--family-root',str(d)];r=subprocess.run(argv,capture_output=True,timeout=15);expected=0 if label=='baseline' else 1
  (d/'ACTUAL_STDOUT.bin').write_bytes(r.stdout);(d/'ACTUAL_STDERR.bin').write_bytes(r.stderr)
  row={'label':label,'argv':argv,'returncode':r.returncode,'expected_returncode':expected,'matched_expected':r.returncode==expected,'stdout':{'size':len(r.stdout),'sha256':sha(r.stdout)},'stderr':{'size':len(r.stderr),'sha256':sha(r.stderr)},'fixture_manifest_sha256':sha((d/SELF).read_bytes()),'fixture_manifest_full':m,'fixture_payload_full_hex':(payload+b'changed').hex() if label=='changed_bytes' else (None if label in {'missing_payload','symlink_payload'} else payload.hex()),'fixture_symlink_target':'target.txt' if label=='symlink_payload' else None,'fixture_extra_payload':'unexpected' if label=='extra_regular' else None,'fixture_nested_self_payload':(d/'nested'/SELF).read_text() if label=='nested_self_name' else None,'qualification':'Full fixture inputs/stdio retained. Capture stream files were written after verifier execution and are not in the intentionally minimal test manifest.'};results.append(row)
  if r.returncode!=expected:raise AssertionError(label)
 (out/'RESULT.json').write_text(json.dumps({'schema':'pr40-family-closure-controls/v1','status':'PASS','actual_program_sha256':sha(source.read_bytes()),'controls':results},indent=2)+'\n');print(json.dumps({'status':'PASS','baseline_passes':1,'actual_rejected_controls':6}))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--family-root',type=pathlib.Path);a.add_argument('--self-tests-output',type=pathlib.Path);x=a.parse_args()
 try:
  if bool(x.family_root)==bool(x.self_tests_output):raise ValueError('choose exactly one operation')
  if x.family_root:print(json.dumps(verify(x.family_root.resolve()),sort_keys=True))
  else:tests(x.self_tests_output.resolve())
 except Exception as e:
  print(json.dumps({'status':'REJECTED','error_type':type(e).__name__,'error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
