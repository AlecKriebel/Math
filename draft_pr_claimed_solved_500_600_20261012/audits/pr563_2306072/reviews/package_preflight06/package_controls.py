#!/usr/bin/env python3
import base64,datetime,hashlib,importlib.util,json,os,shutil,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent; PUB=AUDIT/'publication'; ROOT=HERE/'extract/support_slit_verification'
sha=lambda b:hashlib.sha256(b).hexdigest()
def inv(root):return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and '.venv' not in p.parts}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def command(args,cwd,stem,env=None):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
 (HERE/(stem+'.stdout.txt')).write_text(p.stdout);(HERE/(stem+'.stderr.txt')).write_text(p.stderr)
 return {'args':args,'cwd':str(cwd),'exit_code':p.returncode,'stdout_sha256':sha(p.stdout.encode()),'stderr_sha256':sha(p.stderr.encode())}
mode=sys.argv[1]
if mode=='integrity':
 z=zipfile.ZipFile(PUB/'verification_package.zip'); names=z.namelist();assert len(names)==len(set(names))==255
 assert all(n.startswith('support_slit_verification/') and '..' not in PurePosixPath(n).parts for n in names)
 m=json.loads((ROOT/'MANIFEST.json').read_text()); actual=inv(ROOT)
 assert set(actual)==set(m['files'])|{'MANIFEST.json'}
 assert all(actual[k]==v for k,v in m['files'].items())
 nested=0
 for seal in m['nested_seals']:
  rec=json.loads((ROOT/seal).read_text());items=rec.get('files',rec.get('authored_files',rec.get('authored_outputs')))
  if isinstance(items,dict):items=[dict(path=k,sha256=v) if isinstance(v,str) else dict(path=k,**v) for k,v in items.items()]
  seen=set()
  for x in items:
   p=PurePosixPath(seal).parent/PurePosixPath(x['path']);assert '..' not in p.parts and not p.is_absolute()
   assert str(p) not in seen;seen.add(str(p)); b=(ROOT/str(p)).read_bytes();assert sha(b)==x['sha256']
   size=x.get('bytes',x.get('size_bytes',x.get('size')));assert size is None or size==len(b);nested+=1
 assert nested==164 and len(m['nested_seals'])==16
 originals={k:v for k,v in actual.items() if k.startswith('original/')};assert len(originals)==17
 for k in originals:assert (ROOT/k).read_bytes()==(AUDIT/k).read_bytes()
 forbidden=[k for k in actual if k.endswith(('.pdf','.png','.jpg','.jpeg','.whl')) or (k.endswith('.txt') and k!='requirements.txt') or '.private' in k or '__pycache__' in k]
 assert not forbidden
 write('INTEGRITY_CHECK.json',{'status':'PASS','archive_members':len(names),'outer_payloads':len(m['files']),'nested_seals':len(m['nested_seals']),'nested_entries':nested,'original_files':len(originals),'original_canonical_bytes_match':True,'pinned_head':m['head'],'independent_manifest_implementation':True,'third_party_binary_payloads':forbidden,'originals':originals})
elif mode=='offline':
 guard=HERE/'offline_guard';guard.mkdir(exist_ok=True)
 (guard/'sitecustomize.py').write_text('import socket\ndef forbidden(*a,**k):\n raise RuntimeError("network forbidden by package06 offline test")\nsocket.socket=forbidden\nsocket.create_connection=forbidden\nsocket.getaddrinfo=forbidden\n')
 env=dict(os.environ,PYTHONPATH=str(guard),PYTHONDONTWRITEBYTECODE='1',PIP_NO_INDEX='1');before=inv(ROOT)
 cmd=command([str(HERE/'venv/bin/python'),'run_all.py'],ROOT,'OFFLINE_REPLAY',env)
 assert cmd['exit_code']==0
 lines=[json.loads(x) for x in (HERE/'OFFLINE_REPLAY.stdout.txt').read_text().splitlines()];assert len(lines)==18 and lines[-1]['replayed_jobs']==17
 assert before==inv(ROOT)
 p=subprocess.run([str(HERE/'venv/bin/python'),'-c','import mpmath;print(mpmath.__version__)'],capture_output=True,text=True);assert p.stdout.strip()=='1.4.1'
 write('OFFLINE_REPLAY.json',dict(cmd,status='PASS',summary=lines[-1],mpmath='1.4.1',fresh_venv=True,network_denied_via_inherited_socket_guard=True,wheel_sha256=sha((HERE/'mpmath-1.4.1-py3-none-any.whl').read_bytes())))
elif mode=='producer':
 build=HERE/'producer/audit';dest=build/'publication';dest.mkdir(parents=True)
 for p in ROOT.iterdir():
  if p.is_dir():shutil.copytree(p,build/p.name)
  else:shutil.copy2(p,build/p.name)
 for n in ['support_slit.tex','README.md','CORRECTIONS.md','BUILD.json','PDF_QA.json','requirements.txt','integrity.py','run_all.py','JOBS.json','SEALS.json','make_package.py','zenodo-deposit.json','support_slit.pdf']:shutil.copy2(PUB/n,dest/n)
 before=inv(build)
 cmd=command([sys.executable,'make_package.py'],dest,'PRODUCER_REBUILD');assert cmd['exit_code']==0
 for n in ['verification_package.zip','PACKAGE_MANIFEST.json','PACKAGE_BUILD.json']:assert (dest/n).read_bytes()==(PUB/n).read_bytes(),n
 write('PRODUCER_REBUILD.json',dict(cmd,status='PASS',byte_identical=['verification_package.zip','PACKAGE_MANIFEST.json','PACKAGE_BUILD.json'],zip_sha256=sha((dest/'verification_package.zip').read_bytes()),independent_scratch_layout=True))
elif mode=='pdf':
 dest=HERE/'pdf_rebuild';dest.mkdir()
 env=dict(os.environ,SOURCE_DATE_EPOCH='1791892800')
 cmd=command(['/opt/homebrew/bin/tectonic','--outdir',str(dest),str(PUB/'support_slit.tex')],HERE,'PDF_REBUILD',env)
 assert cmd['exit_code']==0
 b=(dest/'support_slit.pdf').read_bytes();assert b==(PUB/'support_slit.pdf').read_bytes()
 write('PDF_REBUILD.json',dict(cmd,status='PASS',byte_identical=True,sha256=sha(b),bytes=len(b)))
elif mode=='negative':
 results=[];base=HERE/'negative_controls';base.mkdir()
 def neg(name,mutate,opt=False,producer=False):
  source=HERE/'producer/audit' if producer else ROOT;d=base/name;shutil.copytree(source,d,ignore=shutil.ignore_patterns('__pycache__'))
  mutate(d)
  immutable_before=inv(d)
  p=subprocess.run([str(HERE/'venv/bin/python')]+(['-O'] if opt else [])+[str(d/('publication/make_package.py' if producer else 'run_all.py'))],cwd=d,capture_output=True,text=True)
  assert p.returncode!=0,name
  assert immutable_before==inv(d),name+' changed payloads after rejecting input'
  results.append({'name':name,'exit_code':p.returncode,'immutable_after_rejection':True,'stderr_last_line':p.stderr.strip().splitlines()[-1]})
 neg('tamper_payload',lambda d:(d/'support_slit.tex').write_bytes((d/'support_slit.tex').read_bytes()+b'\n'))
 neg('extra_payload',lambda d:(d/'unlisted.json').write_text('{}'))
 neg('missing_payload',lambda d:(d/'README.md').unlink())
 neg('optimized_python',lambda d:None,True)
 neg('symlink_payload',lambda d:(d/'unexpected_link').symlink_to(d/'README.md'))
 def nested_tamper(d):
  name='reviews/analytic01/CHECKS.json';p=d/name;p.write_bytes(p.read_bytes()+b'\n');m=json.loads((d/'MANIFEST.json').read_text());m['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())};(d/'MANIFEST.json').write_text(json.dumps(m))
 neg('stale_nested_after_outer_reseal',nested_tamper)
 def replay_tamper(d):
  name='root_reproduction/manifest_rerun.json';p=d/name;v=json.loads(p.read_text());v['package06_injected']=True;p.write_text(json.dumps(v));m=json.loads((d/'MANIFEST.json').read_text());m['files'][name]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())};(d/'MANIFEST.json').write_text(json.dumps(m))
 neg('replay_full_json_mismatch',replay_tamper)
 neg('producer_stale_nested',lambda d:(d/'reviews/analytic01/CHECKS.json').write_text('{}'),producer=True)
 neg('producer_symlink_input',lambda d:((d/'publication/README.md').unlink(),(d/'publication/README.md').symlink_to(d/'README.md')),producer=True)
 # Direct pathological registry controls, with same integrity module.
 spec=importlib.util.spec_from_file_location('int06',ROOT/'integrity.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 for name in ['../escape','/absolute','a\\b','a:b','a/./b','']:
  try:mod.safe_path(name)
  except RuntimeError:results.append({'name':'safe_path_'+repr(name),'rejected':True})
  else:raise AssertionError(name)
 write('NEGATIVE_CONTROLS.json',{'status':'PASS','expected_rejections':len(results),'results':results,'scope':'Deliberate corruptions on independent copies only; consistency rather than authenticity.'})
elif mode=='provenance':
 names=['root_reproduction/PRIMARY_AUDIT_BASELINE.tex','root_reproduction/PRE_GOH_MANUSCRIPT.tex','support_slit.tex'];recs=[]
 for n in names:
  b=(ROOT/n).read_bytes();body=b[b.index(b'\\section{The question and precise statement}'):b.index(b'\\section{Attribution, scope and verification}')];assert len(body)==10407
  recs.append({'path':n,'sha256':sha(b),'math_body_bytes':len(body),'math_body_sha256':sha(body)})
 assert len({x['math_body_sha256'] for x in recs})==1
 assert sha((ROOT/'support_slit.tex').read_bytes())=='c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3'
 meta=json.loads((ROOT/'metadata.json').read_text());assert meta==json.loads((PUB/'zenodo-deposit.json').read_text())
 assert meta['metadata']['version']=='1.0' and meta['metadata']['publication_date']=='2026-10-14'
 write('PROVENANCE_CHECK.json',{'status':'PASS','historical_manuscripts':recs,'metadata_canonical_exact':True,'metadata_version':'1.0','publication_date':'2026-10-14','proof_body_identity':True,'limits':'Original 17 files hash-matched against preserved canonical audit; pinned Git commit identity is inherited from fixed provenance and seals. No Git accessed or canonical changes made.'})
