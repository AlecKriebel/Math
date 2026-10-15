from pathlib import Path
import argparse,json,hashlib,datetime,os
ap=argparse.ArgumentParser();ap.add_argument('spec',type=Path);args=ap.parse_args()
A=Path(__file__).resolve().parent
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rows(x):
 if isinstance(x,dict):
  if 'bytes' in x and 'sha256' in x and any(k in x for k in ['path','file','relative_path','private_relative_path','path_relative_to_pr108_audit']):yield x
  for v in x.values():yield from rows(v)
 elif isinstance(x,list):
  for v in x:yield from rows(v)
def resolve(D,row):
 if 'path_relative_to_pr108_audit' in row:return (A/row['path_relative_to_pr108_audit']).resolve()
 key=next(k for k in ['path','file','relative_path','private_relative_path'] if k in row)
 q=Path(row[key]);return q.resolve() if q.is_absolute() else (D/q).resolve()
spec=json.loads(args.spec.read_text());families=[];public=set()
for f in spec['families']:
 D=A/f['directory'];pins=[]
 report=D/f.get('report','REPORT.md');verdict=D/f.get('verdict','VERDICT.json')
 require(sha(report.read_bytes())==f['root_read_report_sha256'],'root report-reading pin drift')
 require(sha(verdict.read_bytes())==f['root_read_verdict_sha256'],'root verdict-reading pin drift')
 for name in f['manifests']:
  M=D/name;mb=M.read_bytes();x=json.loads(mb)
  binding_base=(D/f.get('manifest_base_overrides',{}).get(name,'.')).resolve()
  for row in rows(x):
   q=resolve(binding_base,row);require(q.is_file() and not q.is_symlink(),'missing/nonregular manifested body '+str(q))
   b=q.read_bytes();prefix='append-only' in row.get('snapshot_semantics','') and 'prefix' in row.get('snapshot_semantics','')
   actual=b[:row['bytes']] if prefix else b
   require(len(actual)==row['bytes'] and sha(actual)==row['sha256'],'body pin drift '+str(q))
   pins.append({'path':str(q),'bound_bytes':row['bytes'],'bound_sha256':row['sha256'],'binding_mode':'explicit_append_only_prefix' if prefix else 'complete_body','current_bytes':len(b),'current_sha256':sha(b)})
  pins.append({'path':str(M),'bound_bytes':len(mb),'bound_sha256':sha(mb),'binding_mode':'complete_body'})
  if not any(p in ['private','_private','private_sources'] for p in Path(name).parts):public.add(str(M.relative_to(A)))
 for name in f['public_manifests']:
  M=D/name
  for row in rows(json.loads(M.read_text())):
   q=resolve(D,row)
   if q.is_relative_to(D) and not any(p in ['private','_private','private_sources'] or p.startswith('private_') for p in q.relative_to(D).parts):
    require(q.suffix.lower() not in ['.pdf','.png','.jpg','.html'],'unapproved public primary payload')
    public.add(str(q.relative_to(A)))
 for name in f.get('extra_public_files',[]):
  q=D/name;require(q.is_file() and not q.is_symlink(),'extra public body missing')
  public.add(str(q.relative_to(A)));b=q.read_bytes();pins.append({'path':str(q),'bound_bytes':len(b),'bound_sha256':sha(b),'binding_mode':'complete_body'})
 families.append({'family':f['directory'],'effective_report':str(report.relative_to(A)),'root_full_report_read':True,'root_full_verdict_read':True,'pin_bindings_verified':len(pins),'pins':pins})
out=A/spec['output'];require(not out.exists(),'output already exists')
out.write_text(json.dumps({'schema':'pr108-root-priority-evidence-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),'families':families,'public_family_paths':sorted(public),'third_party_raw_payload_excluded':True,'byte_pins_all_match':True,'audit_is_not_a_priority_absence_proof':True,'priority_clearance':False,'publication_clearance':False},indent=2)+'\n')
print(json.dumps({'UTC':now(),'operator_PID':os.getpid(),'families':len(families),'pin_bindings_verified':sum(x['pin_bindings_verified'] for x in families),'public_family_paths':len(public),'output':str(out)}))
