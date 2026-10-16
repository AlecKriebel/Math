from pathlib import Path
import datetime,hashlib,json,subprocess,zipfile
A=Path(__file__).resolve().parent;P=A/'publication_package_v1';D=A/'root_packet_reproduction_01';D.mkdir(exist_ok=False)
def sha(b):return hashlib.sha256(b).hexdigest()
packet=json.loads((P/'REVIEW_PACKET_MANIFEST.json').read_text())
for x in packet['files']:
 b=(P/x['path']).read_bytes()
 if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError(x['path'])
with zipfile.ZipFile(P/'verification-package.zip') as z:
 names=z.namelist()
 if len(names)!=len(set(names)) or z.testzip() is not None:raise RuntimeError('ZIP corrupt')
 for n in names:
  q=Path(n)
  if q.is_absolute() or '..' in q.parts or any('private' in k.lower() for k in q.parts):raise RuntimeError(n)
 manifest=json.loads(z.read('SHA256SUMS.json'))
 if set(names)!={x['path'] for x in manifest['files']}|{'SHA256SUMS.json'}:raise RuntimeError('ZIP extra/missing')
 for x in manifest['files']:
  b=z.read(x['path'])
  if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError('ZIP manifest '+x['path'])
  if x['path'].startswith('controls/'):
   p=D/x['path'];p.parent.mkdir(exist_ok=True);p.write_bytes(b)
standard='/opt/homebrew/opt/python@3.14/bin/python3.14'
symbolic=A/'gv_algebra_reproduction_adversary/private/control_env/bin/python'
records=[]
for name in ['verify_forms.py','independent_integrable_controls.py','finite_sampling_counterexample.py','independent_symbolic_checks.py']:
 for optimized in [False,True]:
  args=[str(symbolic) if name.startswith('independent_symbolic') else standard,'-E','-B','-P']+(['-O'] if optimized else [])+[str(D/'controls'/name)]
  start=datetime.datetime.now(datetime.UTC).isoformat();r=subprocess.run(args,cwd=D,capture_output=True,timeout=120);end=datetime.datetime.now(datetime.UTC).isoformat()
  tag=name.removesuffix('.py')+('_optimized' if optimized else '_ordinary')
  (D/(tag+'.stdout.json')).write_bytes(r.stdout);(D/(tag+'.stderr.txt')).write_bytes(r.stderr)
  if r.returncode:raise RuntimeError(tag+' failed')
  obj=json.loads(r.stdout)
  records.append({'name':name,'optimized':optimized,'utc_start':start,'utc_end':end,'exit':r.returncode,'source_sha256':sha((D/'controls'/name).read_bytes()),'stdout_sha256':sha(r.stdout),'result':obj})
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'packet_manifest_sha256':sha((P/'REVIEW_PACKET_MANIFEST.json').read_bytes()),'all_outer_and_zip_manifest_bytes_accepted':True,'zip_members':len(names),'actual_replays':records,'global_mathematical_certificate':False,'priority_certificate':False,'status':'PACKAGED_BYTES_AND_EIGHT_FRESH_REPRODUCTIONS_ACCEPTED'}
(D/'ROOT_PACKET_ACCEPTANCE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'runs':len(records),'members':len(names)}))
