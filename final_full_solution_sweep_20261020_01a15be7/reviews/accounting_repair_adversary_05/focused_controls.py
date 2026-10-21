from pathlib import Path
import copy,datetime as dt,hashlib,importlib.util,json,os,shutil,subprocess,sys
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent;F=Q/'fixtures/focused';ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def change(rel,fn):
 p=F/rel;d=json.loads(p.read_text());fn(d);save(p,d)
def ledger(pr):return f'audits/pr{pr:04d}_{ {292:"30001608",397:"9700002",399:"30001179",280:"30000156"}[pr]}/LEDGER_PUBLICATION_VERIFICATION.json'
def proof(pr):return f'PR{pr:04d}_'+('REOPENED_' if pr==280 else '')+'PUBLICATION_VERIFICATION.json'
def link(pr,prefix,suffix):
 old='https://github.com/AlecKriebel/Math/pull/'+str(pr);change(ledger(pr),lambda d:d['values'].__setitem__(3,d['values'][3].replace(old,prefix+old+suffix)))
def symlink(rel):
 p=F/rel;t=Q/'external/focused'/rel;t.parent.mkdir(parents=True,exist_ok=True)
 if p.is_dir():
  if not t.exists():shutil.copytree(p,t)
  shutil.rmtree(p)
 else:t.write_bytes(p.read_bytes());p.unlink()
 p.symlink_to(t)
cases=[('baseline',lambda:None,False),('reverse_completed',lambda:change('STATE.json',lambda d:d['completed_publications'].reverse()),False)]
for pr in [292,397,399,280]:
 for label,prefix,suffix in [('space','reference ',' '),('markdown','[PR](',')'),('autolink','<','>'),('quote','"','"'),('sentence','(',').')]:
  cases.append((f'positive_{label}_{pr}',lambda pr=pr,prefix=prefix,suffix=suffix:link(pr,prefix,suffix),False))
 for label,prefix,suffix in [('invalid_word','invalid',''),('unicode_word','é',''),('relative_path','../',''),('external_url','https://evil.invalid/',''),('query_suffix','','?x=1'),('longer_number','','0')]:
  cases.append((f'negative_{label}_{pr}',lambda pr=pr,prefix=prefix,suffix=suffix:link(pr,prefix,suffix),True))
for pr in [9,100,280,292,397,399,614]:cases.append((f'symlink_saved_{pr}',lambda pr=pr:symlink(f'PR{pr:04d}_DISPOSITION.json'),True))
for rel in [proof(292),proof(397),ledger(399),'audits/pr0397_9700002']:
 cases.append(('symlink_'+rel.replace('/','_'),lambda rel=rel:symlink(rel),True))
# Direct function controls challenge both positive normalization and independently malformed evidence.
spec=importlib.util.spec_from_file_location('captured_coverage',Q/'inputs/current/coverage_snapshot.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
direct=[]
url='https://github.com/AlecKriebel/Math/pull/397'
for prefix in ['', ' ', '\n', '(', '[reference](', '<', '"', "'", 'See: ', '— ']:
 suffix=')' if prefix.endswith('(') else ('>' if prefix=='<' else ('"' if prefix=='"' else ("'" if prefix=="'" else '.')))
 accepted=url in mod.ledger_urls([prefix+url+suffix]);assert accepted;direct.append(dict(family='url_positive',prefix=prefix,suffix=suffix,accepted=accepted,pass_=True))
for prefix in ['word','é','_', '+','/','../','https://evil.invalid/','ftp://evil.invalid/','x@','x:']:
 accepted=url in mod.ledger_urls([prefix+url]);assert not accepted;direct.append(dict(family='url_negative',prefix=prefix,accepted=accepted,pass_=True))
for pr in [397,399,280]:
 data=json.loads((Q/'inputs/current'/proof(pr)).read_text());baseline=mod.public_files(data);assert baseline
 for what in ['legacy_schema','negative_http','negative_download','no_manifest','manifest_count','missing_zip','unsafe_filename','duplicate_name']:
  d=copy.deepcopy(data);z=next(f for f in d['files'] if f['name'].endswith('.zip'))
  if what=='legacy_schema':
   z['size']=z.pop('bytes');z['checksum']='md5:'+z.pop('md5');z.update(download_verified=True,zip_crc_ok=True,members=['a','b'])
   for k in ['downloaded_and_matches_reviewed','http_status','zip_crc_safe_unique_pass','all_manifest_payloads_verified']:z.pop(k,None)
  elif what=='negative_http':z['http_status']=404
  elif what=='negative_download':z['downloaded_and_matches_reviewed']=False
  elif what=='no_manifest':z.pop('all_manifest_payloads_verified')
  elif what=='manifest_count':z['all_manifest_payloads_verified']-=1
  elif what=='missing_zip':d['files']=[f for f in d['files'] if not f['name'].endswith('.zip')]
  elif what=='unsafe_filename':z['name']='../'+z['name']
  elif what=='duplicate_name':d['files'].append(copy.deepcopy(d['files'][0]))
  try:mod.public_files(d);rejected=False
  except (RuntimeError,ValueError,TypeError):rejected=True
  assert rejected,(pr,what);direct.append(dict(family='file_evidence',pr=pr,mutation=what,rejected=True,pass_=True))
save(Q/'DIRECT_FUNCTION_CONTROLS.json',dict(at=now(),checks=direct,check_count=len(direct),scope='Direct function cases, not separate report executions.'))
rows=[]
for name,fn,reject in cases:
 if F.exists():shutil.rmtree(F)
 shutil.copytree(Q/'inputs/current',F);before={str(p.relative_to(F)):p.read_bytes() for p in F.rglob('*') if p.is_file()};fn();c=Q/'focused_cases'/name;mut=[]
 for p in F.rglob('*'):
  if p.is_symlink():mut.append(dict(path=str(p.relative_to(F)),symlink=os.readlink(p)))
  elif p.is_file():
   rel=str(p.relative_to(F));b=p.read_bytes()
   if b!=before.get(rel):mut.append(dict(path=rel,before_sha256=sha(before[rel]) if rel in before else None,after_sha256=sha(b),after_text=b.decode()))
 save(c/'MUTATIONS.json',mut)
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  x=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],cwd=Q,env=ENV,capture_output=True);(c/(mode+'.stdout')).write_bytes(x.stdout);(c/(mode+'.stderr')).write_bytes(x.stderr);a=dict(name=name,mode=mode,expected_reject=reject,accepted=x.returncode==0,returncode=x.returncode,control_pass=(x.returncode==0)!=reject,stdout_sha256=sha(x.stdout),stderr_sha256=sha(x.stderr));rows.append(a)
 if not all(x['control_pass'] for x in rows[-2:]):raise RuntimeError('Focused control failed '+name)
save(Q/'FOCUSED_CONTROL_RESULTS.json',dict(at=now(),cases_per_mode=len(cases),executions=len(rows),results=rows));print(json.dumps(dict(cases=len(cases),executions=len(rows),direct_checks=len(direct),all_pass=True)))
