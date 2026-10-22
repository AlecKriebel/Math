from pathlib import Path
import copy,datetime as dt,hashlib,json,os,shutil,subprocess,sys
sys.dont_write_bytecode=True
Q=Path(__file__).resolve().parent
F=Q/'fixtures/current'
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def change(rel,fn):
 p=F/rel;d=json.loads(p.read_text());fn(d);save(p,d)
def ledger(pr,fn):change(f'audits/pr{pr:04d}_{ {292:"30001608",397:"9700002",399:"30001179",280:"30000156"}[pr]}/LEDGER_PUBLICATION_VERIFICATION.json',fn)
def proof(pr,fn):change(f'PR{pr:04d}_'+('REOPENED_' if pr==280 else '')+'PUBLICATION_VERIFICATION.json',fn)
def both(pr,fn):
 proof(pr,fn);change(f'audits/pr{pr:04d}_{ {397:"9700002",399:"30001179",280:"30000156"}[pr]}/ZENODO_PUBLIC_FILE_VERIFICATION.json',fn)
def link(pr,which,suffix='',prefix=''):
 old=('https://github.com/AlecKriebel/Math/pull/'+str(pr)) if which=='pr' else 'https://zenodo.org/records/'+str({292:23524971,397:23527793,399:23539283,280:23539734}[pr])
 ledger(pr,lambda d:d['values'].__setitem__(3,d['values'][3].replace(old,prefix+old+suffix)))
def zipfalse(d):next(f for f in d['files'] if f['name'].endswith('.zip')).update(zip_crc_safe_unique_pass=False)
def symlink(rel):
 p=F/rel;t=Q/'external'/rel;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(p.read_bytes());p.unlink();p.symlink_to(t)
cases=[('baseline',lambda:None,False,'positive'),('own_list_reverse',lambda:change('STATE.json',lambda d:d['completed_publications'].reverse()),False,'positive')]
for pr in [292,397,399,280]:
 for suffix in ['evil','.evil','/other','?x=1','#other','0']:
  cases.append((f'pr_url_suffix_{suffix.replace("/","_")}_{pr}',lambda pr=pr,suffix=suffix:link(pr,'pr',suffix=suffix),True,'pr_link'))
 for prefix in ['https://evil.invalid/','invalid']:
  cases.append((f'pr_url_prefix_{prefix.replace("/","_")}_{pr}',lambda pr=pr,prefix=prefix:link(pr,'pr',prefix=prefix),True,'pr_link_prefix'))
 for suffix in ['evil','/other','?x=1']:
  cases.append((f'record_url_suffix_{suffix.replace("/","_")}_{pr}',lambda pr=pr,suffix=suffix:link(pr,'record',suffix=suffix),True,'record_link'))
 # The real Original Problem field is a canonical catalogue URL in all four receipts.
 for variant in ['evil_suffix','foreign_origin','incidental_id']:
  pid={292:'30001608',397:'9700002',399:'30001179',280:'30000156'}[pr]
  value={'evil_suffix':'https://www.unsolvedmath.com/problems/'+pid+'evil','foreign_origin':'https://unrelated.invalid/problems/'+pid,'incidental_id':'Some unrelated problem; ignore catalogue '+pid}[variant]
  cases.append((f'source_{variant}_{pr}',lambda pr=pr,value=value:ledger(pr,lambda d:d['values'].__setitem__(0,value)),True,'source_semantics'))
 for kind in ['pr','record']:
  cases.append((f'link_markdown_positive_{kind}_{pr}',lambda pr=pr,kind=kind:link(pr,kind,prefix='[reference](',suffix=')'),False,'positive'))
for pr in [397,399,280]:
 cases.extend([(f'zip_negative_{pr}',lambda pr=pr:both(pr,zipfalse),True,'archive'),(f'empty_files_{pr}',lambda pr=pr:both(pr,lambda d:d.update(files=[])),True,'archive'),(f'negative_download_{pr}',lambda pr=pr:both(pr,lambda d:d['files'][0].update(downloaded_and_matches_reviewed=False)),True,'download'),(f'file_list_reverse_{pr}',lambda pr=pr:both(pr,lambda d:d['files'].reverse()),False,'positive')])
for pr in [9,292,397,399,280]:
 cases.append((f'symlink_disposition_{pr}',lambda pr=pr:symlink(f'PR{pr:04d}_DISPOSITION.json'),True,'symlink_saved_disposition'))
for rel in ['STATE.json','rest_inventory.json','dispositions.jsonl']:
 cases.append(('symlink_input_'+rel,lambda rel=rel:symlink(rel),None,'scope_probe'))
# Semantic metadata assertions: report separately rather than impose new all-field validation.
cases.extend([('root_metadata_exact_false_397',lambda:proof(397,lambda d:d.update(all_intended_metadata_exact=False)),None,'scope_probe'),('state_count_float',lambda:change('STATE.json',lambda d:d.update(completed_pr_count=float(d['completed_pr_count']))),None,'scope_probe')])
rows=[]
for name,fn,reject,family in cases:
 if F.exists():shutil.rmtree(F)
 shutil.copytree(Q/'inputs/current',F);before={str(p.relative_to(F)):p.read_bytes() for p in F.rglob('*') if p.is_file()};fn();c=Q/'new_cases'/name;changes=[]
 for p in F.rglob('*'):
  if p.is_file():
   rel=str(p.relative_to(F));b=p.read_bytes()
   if p.is_symlink():changes.append({'path':rel,'symlink':os.readlink(p),'sha256':hashlib.sha256(b).hexdigest()})
   elif before.get(rel)!=b:changes.append({'path':rel,'before_sha256':hashlib.sha256(before[rel]).hexdigest() if rel in before else None,'after_text':b.decode()})
 save(c/'MUTATIONS.json',changes)
 for mode,flags in [('normal',[]),('optimized',['-O'])]:
  x=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],cwd=Q,env=ENV,capture_output=True);(c/(mode+'.stdout')).write_bytes(x.stdout);(c/(mode+'.stderr')).write_bytes(x.stderr);a={'name':name,'mode':mode,'family':family,'expected_reject':reject,'accepted':x.returncode==0,'returncode':x.returncode,'stdout_sha256':hashlib.sha256(x.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(x.stderr).hexdigest()}
  if reject is not None:a['control_pass']=(a['accepted']!=reject)
  rows.append(a)
save(Q/'NEW_CONTROL_RESULTS.json',{'results':rows});summary={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'cases_per_mode':len(cases),'by_mode':{mode:{'executions':len([r for r in rows if r['mode']==mode]),'false_accepts':[r['name'] for r in rows if r['mode']==mode and r.get('control_pass') is False and r['accepted']],'false_rejects':[r['name'] for r in rows if r['mode']==mode and r.get('control_pass') is False and not r['accepted']]} for mode in ['normal','optimized']}};save(Q/'NEW_CONTROL_SUMMARY.json',summary);print(json.dumps(summary,indent=2))
