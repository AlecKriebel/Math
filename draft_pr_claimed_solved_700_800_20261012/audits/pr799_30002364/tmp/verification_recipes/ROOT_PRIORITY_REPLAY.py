from pathlib import Path
import datetime, hashlib, json, os, shutil, stat, subprocess, sys, tempfile
T=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364/tmp')
M=T/'root-receipts'
specs=[
 ('priority_history/packet','MANIFEST.json','verify_packet.py','7b59615fe1dc81b9f16546d4de09696b42328ba781d68bce2b726788f1d482ef','75504827573f7e260000a6875a35c000a4a54bb55f2081e290549911ac2a8703',15),
 ('priority_structural/packet','MANIFEST.json','verify_packet.py','1da9d6190f408e8e207ab811c0967345900aaf58a183745bc04d403645d5eb45','53041380038011e7b97cf607c47d37a391465edfd07df5591f5455fd610f7868',14),
 ('prior_agugliaro_adversary','MANIFEST.json','verify_seal.py','ccba4c1f85310a42e78af87eebcb196dbc20ef9a2ade9897cc6dd1fd4a686b38','fc991f55895ecfba607e98db2575e44bb93cf7d0a767594ad082e10c69e4b625',8),
 ('prior_threefold_adversary','artifact_manifest.json','check.py','07787ba37bae3af4279a7d6706561a1a58c3f7ca2f6ff3d431d60ae0ad7a85cb','3b51b1b8b1d975c98e413f1a04d883a8ab9e22cab4e0616fb3b8fefd79e42006',9)]
def need(ok,msg):
 if not ok: raise ValueError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  need(k not in d,'duplicate key');d[k]=v
 return d
def checked(folder,spec,closed):
 rel,mf,checker,mp,cp,count=spec
 for p in [folder,*folder.parents]: need(not p.is_symlink(),'symlink ancestor')
 need(sha(folder/mf)==mp and sha(folder/checker)==cp,'external pin')
 doc=json.loads((folder/mf).read_text(),object_pairs_hook=unique)
 entries=doc.get('authored_files',doc.get('files'))
 if isinstance(entries,dict):
  rows=[{'path':k,**({'sha256':v} if isinstance(v,str) else v)} for k,v in entries.items()]
 else: rows=[{'path':r.get('path',r.get('name')),**r} for r in entries]
 names={mf}
 for r in rows:
  name=r['path'];need(isinstance(name,str) and Path(name).name==name and name not in ('.','..'),'unsafe name')
  need(name not in names,'duplicate inventory');names.add(name)
  p=folder/name;need(stat.S_ISREG(p.lstat().st_mode) and p.stat().st_nlink==1,'regular single-link member')
  need(sha(p)==r['sha256'],'member digest')
  if 'bytes' in r: need(p.stat().st_size==r['bytes'],'member bytes')
 if rel=='prior_agugliaro_adversary':
  names.add('MANIFEST.sha256');need((folder/'MANIFEST.sha256').read_text().split()[0]==mp,'detached digest')
 need(checker in names and len(names)==count,'complete inventory')
 if closed: need({p.name for p in folder.iterdir()}==names,'extra member')
 return names
def run(cmd):
 r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=240,
                  env=dict(os.environ,TMPDIR=str(T/'owned-runtime-tmp')))
 need(r.returncode==0 and not r.stderr,'execution failed: '+r.stdout+r.stderr)
 return {'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stdout':r.stdout}
records=[]
for i,spec in enumerate(specs):
 rel,mf,checker,mp,cp,count=spec;source=T/rel
 names=checked(source,spec,False)
 before={n:sha(source/n) for n in names}
 copy=T/('root-priority-replay-'+str(i));need(not copy.exists(),'never overwrite existing root replay')
 copy.mkdir()
 for n in names: shutil.copyfile(source/n,copy/n)
 checked(copy,spec,True)
 runs=[]
 for py in [sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
  # The Agugliaro adversary intentionally uses assert-based diagnostics; execute
  # them normally, not under -O. Root's explicit byte checks precede execution.
  for opt in ([False] if i==2 else [False,True]):
   flags=[py,'-I','-S','-B']+(['-O'] if opt else [])
   if i in (0,1):
    cmd=flags+[str(copy/checker),str(copy),mp,cp]+(['--execute'] if i==0 else [])
    out=run(cmd)
   elif i==2:
    seal=run(flags+[str(copy/checker),'--self-test'])
    out=run(flags+[str(copy/'check_claim.py'),'--compare',str(copy/'check_results.json')])
    need('PASS: all exact controls' in out['stdout'],'arithmetic PASS')
    out['seal_stdout_sha256']=seal['stdout_sha256']
   else:
    out=run(flags+[str(copy/checker),'--manifest-sha256',mp]);need('AUDIT_OK' in out['stdout'],'GP result')
   runs.append({'python':py,'optimized':opt,**out})
 controls=[]
 if i in (0,1):
  out=run([sys.executable,'-I','-S','-B',str(copy/'test_packet.py'),str(copy),mp,cp])
  c=json.loads(out['stdout']);need(c['count']==(17 if i==0 else 16),'control count')
  controls=c['controls'];(M/('ROOT_PRIORITY_'+str(i)+'_CONTROLS.json')).write_text(out['stdout'])
 else:
  for label in ['wrong_pin','report_tamper','code_tamper','missing_member','extra_member','member_symlink']:
   with tempfile.TemporaryDirectory(prefix='root prior negative ',dir=T/'owned-runtime-tmp') as td:
    q=Path(td)/'packet';shutil.copytree(copy,q)
    report='REPORT.md' if i==2 else 'report.md'
    other='check_claim.py' if i==2 else 'arithmetic.gp'
    target=q/report
    if label=='wrong_pin': (q/mf).write_bytes((q/mf).read_bytes()+b' ')
    elif label=='report_tamper': target.write_bytes(target.read_bytes()+b'changed')
    elif label=='code_tamper': (q/other).write_bytes((q/other).read_bytes()+b'changed')
    elif label=='missing_member': target.unlink()
    elif label=='extra_member': (q/'unexpected').write_text('x')
    else: target.unlink();target.symlink_to(copy/report)
    try: checked(q,spec,True)
    except (ValueError,FileNotFoundError): controls.append({'control':label,'rejected_before_child_execution':True})
    else: raise ValueError('negative fixture accepted: '+label)
  (M/('ROOT_PRIORITY_'+str(i)+'_CONTROLS.json')).write_text(json.dumps(controls,indent=2)+'\n')
 need(before=={n:sha(source/n) for n in names},'source bundle changed')
 need(before=={n:sha(copy/n) for n in names},'root copy changed')
 records.append({'family':rel,'manifest':mf,'manifest_sha256':mp,'checker':checker,
                 'checker_sha256':cp,'closed_files':count,'root_copy':copy.relative_to(T).as_posix(),
                 'runs':runs,'controls_count':len(controls),'result':'PASS','original_unchanged':True})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS',
 'independent_discovery_families':2,'fresh_priority_adversaries':2,'records':records,
 'primary_geometry_and_all_powers_proofs_reviewed_separately':True,
 'byte_authentication_is_not_formal_mathematical_verification':True,
 'assert_based_adversary_diagnostics_run_only_without_optimization':True}
(M/'ROOT_PRIORITY_REPLAYS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'result':'PASS','families':4,'baseline_executions':sum(len(r['runs']) for r in records),
                  'controls':[r['controls_count'] for r in records]}))
