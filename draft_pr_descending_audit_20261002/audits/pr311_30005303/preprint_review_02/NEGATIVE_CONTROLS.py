"""Run native rejection controls on fresh copies, preserving complete streams."""
import argparse, datetime, hashlib, json, pathlib, shutil, subprocess, sys
def pin(p):
 p=pathlib.Path(p).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
p=argparse.ArgumentParser();p.add_argument('--private-dir',type=pathlib.Path,required=True);a=p.parse_args();D=a.private_dir.resolve();base=D/'negative_cases';base.mkdir();records=[]
for name in ['optimization','existing_output','boundary_count','priority_weight','missing_expected','wrong_unary_sign','negative_coupling','nonlattice_law','independent_bad_expected']:
 folder=base/name;shutil.copytree(D/'different_location'/'portable_package',folder);argv=[sys.executable,str(folder/'REPRODUCE.py'),'--out-dir',str(folder/'results')]
 if name=='optimization':argv.insert(1,'-O')
 if name=='existing_output':(folder/'results').mkdir()
 if name=='boundary_count':
  f=folder/'expected'/'boundary.json';j=json.loads(f.read_text());j['networks']+=1;f.write_text(json.dumps(j,indent=2)+'\n')
 if name in ['priority_weight','independent_bad_expected']:
  f=folder/'expected'/'priority_laws.json';j=json.loads(f.read_text());j['laws']['gandolfi_lenarda_lemma5_2']['integer_weights']['1111']=3;f.write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
 if name=='missing_expected':(folder/'expected'/'priority_laws.json').unlink()
 if name=='wrong_unary_sign':
  f=folder/'verify_boundary.py';s=f.read_text();assert s.count('b[u] -= interaction')==1;f.write_text(s.replace('b[u] -= interaction','b[u] += interaction'))
 if name=='negative_coupling':argv=[sys.executable,'-c','import verify_boundary as v; v.gauge(2, [(0,1)], [0,0], [-1])']
 if name=='nonlattice_law':argv=[sys.executable,'-c','import verify_priority_examples as v; w={x:((0 if x==(1,1,1,1) else 1) if x[2]==x[3] else 0) for x in v.product((0,1),repeat=4)}; r=v.verify_law(4,((0,1),(1,2),(2,3),(0,3)),w,v.bits("0000","0111","1011","1100"),v.bits("0011","0100","1000","1111")); assert r["mtp2_failure_count"]==0']
 if name=='independent_bad_expected':argv=[sys.executable,str(D.parent/'INDEPENDENT_CHECKS.py'),'--expected',str(folder/'expected'),'--output',str(folder/'independent_result.json')]
 inputpins=[pin(f) for f in sorted(folder.rglob('*')) if f.is_file()]
 record={'name':name,'argv':argv,'cwd':str(folder),'start_utc':utc(),'executable_pin':pin(sys.executable),'inputs':inputpins}
 r=subprocess.run(argv,cwd=folder,capture_output=True,check=False)
 out=folder/'native.stdout';err=folder/'native.stderr';out.write_bytes(r.stdout);err.write_bytes(r.stderr)
 record.update(end_utc=utc(),exit_code=r.returncode,stdout=pin(out),stderr=pin(err),expected='nonzero rejection',passed=r.returncode!=0)
 (folder/'native_execution.json').write_text(json.dumps(record,indent=2)+'\n');assert record['passed'];records.append(record)
# A separate authenticated-manifest check rejects a malformed pin. The runner
# advertises result reproduction, so no manifest-verification claim is assigned to it.
manifest=json.loads((D/'different_location'/'portable_package'/'MANIFEST.json').read_text());manifest['README.md']['sha256']='0'*64
bad=D/'negative_cases'/'malformed_manifest.json';bad.write_text(json.dumps(manifest,indent=2)+'\n')
actual=pin(D/'different_location'/'portable_package'/'README.md')['sha256'];assert actual!=manifest['README.md']['sha256']
result={'status':'PASS_NEGATIVE_CONTROLS','native_cases':[{'name':r['name'],'exit_code':r['exit_code'],'passed':r['passed'],'execution_record':str(base/r['name']/'native_execution.json')} for r in records],'malformed_pin_independently_rejected':True,'limits':'Rejection cases validate specific checks only; manifest authentication is separate from the published runner.'}
(D.parent/'NEGATIVE_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
