from pathlib import Path
import shutil,subprocess,sys,json,hashlib,datetime,time,runpy,io,contextlib
R=Path(__file__).resolve().parent;S=R.parent/'repaired_snapshot/unsolved_math_prioritization/attempts/6600013';P=R/'tmp'/'packet';P.mkdir(parents=True,exist_ok=True)
for f in S.rglob('*'):
 if f.is_file():
  t=P/f.relative_to(S);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,t)
assert all((P/f.relative_to(S)).read_bytes()==f.read_bytes() for f in S.rglob('*') if f.is_file())
real=subprocess.check_output;captures=[]
def record(*args,**kw):
 v=real(*args,**kw);cmd=args[0]
 if len(cmd)>1 and Path(cmd[1]).name.startswith('verify_turn'):
  name=Path(cmd[1]).stem;(R/(name+'.stdout')).write_bytes(v)
  turn=int(name.replace('verify_turn',''));frozen=(S/f'TURN_{turn}_CHECKS.json').read_bytes();assert v==frozen
  captures.append({'turn':turn,'stdout_bytes':len(v),'sha256':hashlib.sha256(v).hexdigest(),'complete_expected_bytes_equal':True,'assertions':json.loads(v)['assertions']})
 return v
subprocess.check_output=record
sys.argv=[str(P/'REPLAY_ALL.py')];buffer=io.StringIO();start=time.monotonic()
with contextlib.redirect_stdout(buffer):runpy.run_path(str(P/'REPLAY_ALL.py'),run_name='__main__')
auth=buffer.getvalue().encode();(R/'author_replay.stdout').write_bytes(auth);(R/'author_replay.stderr').write_bytes(b'');assert len(captures)==5
subprocess.check_output=real
hist=subprocess.run([sys.executable,str(P/'final_review/independent_checks.py')],capture_output=True,cwd=P)
(R/'historical_replay.stdout').write_bytes(hist.stdout);(R/'historical_replay.stderr').write_bytes(hist.stderr)
assert hist.returncode==0 and hist.stdout==(S/'final_review/INDEPENDENT_CHECKS.json').read_bytes() and not hist.stderr
# Revalidate all nested manifests/blobs independently of the packet validator.
manifest_results=[];blobs=[]
for f in S.rglob('*MANIFEST.json'):
 j=json.loads(f.read_text())
 if 'files' not in j:continue
 for e in j['files']:
  loc=(f.parent/e['path']) if f.parent.name=='final_review' else S/e['path']
  bb=loc.read_bytes();assert len(bb)==e['bytes'] and hashlib.sha256(bb).hexdigest()==e['sha256'];manifest_results.append({'manifest':str(f.relative_to(S)),'path':e['path'],'bytes':len(bb),'sha256':e['sha256']})
for e in json.loads((S/'final_review/REMOTE_BINDING.json').read_text())['files']:
 bb=(S/e['path']).read_bytes();gitsha=hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest();assert len(bb)==e['size'] and gitsha==e['sha'];blobs.append({'path':e['path'],'blob':gitsha})
receipt={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'private_copy_byte_exact':True,'author_complete_stdout':json.loads(auth),'turn_complete_outputs':captures,'historical_complete_stdout':json.loads(hist.stdout),'historical_expected_bytes_equal':True,'source_free_count':0,'historical_git_blob_bindings':blobs,'all_nested_manifest_entries':manifest_results,'no_frozen_file_mutations':all((P/f.relative_to(S)).read_bytes()==f.read_bytes() for f in S.rglob('*') if f.is_file())}
(R/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['all_nested_manifest_entries','historical_git_blob_bindings']},indent=2))
