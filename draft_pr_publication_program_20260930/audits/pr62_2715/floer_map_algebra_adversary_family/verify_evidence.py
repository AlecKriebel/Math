import datetime,hashlib,json,os,pathlib,sqlite3,stat
root=pathlib.Path(__file__).resolve().parent
original=root.parent/'original_preparation_family'
N=pathlib.Path('/Users/alec/Documents/Math')
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
auth=json.loads((original/'ORIGINAL_AUTHENTICATION.json').read_bytes())
ck(auth['head']=='98cc2821e9376507caf2d2c57414f7c7e7719c1b')
ck(len(auth['scientific_files'])==17)
for row in auth['scientific_files']:
 p=original/'original'/row['relative_path']
 ck(pin(p)=={k:row[k] for k in ('bytes','sha256')})
 ck(stat.S_IMODE(p.lstat().st_mode)==0o444 and p.lstat().st_nlink==1)
for name in ('OBSTRUCTION.md','verify.py'):
 ck((root/'original_replay'/name).read_bytes()==(original/'original'/name).read_bytes())
for label in ('algebra_controls','original_verify'):
 prefix=root/'captures'/label
 pre=json.loads(prefix.with_suffix('.prelaunch.json').read_bytes())
 post=json.loads(prefix.with_suffix('.post.json').read_bytes())
 ck(post['returncode']==0 and post['child_pid']>0 and post['capture_pid']==pre['capture_pid'])
 ck(post['prelaunch_sha256']==pin(prefix.with_suffix('.prelaunch.json'))['sha256'])
 for source in pre['sources']:
  ck(pin(pathlib.Path(source['path']))=={k:source[k] for k in ('bytes','sha256')})
 for suffix in ('stdout','stderr'):
  ck(post[suffix]==pin(prefix.with_suffix('.'+suffix)))
 ck(post['stderr']['bytes']==0)
a=json.loads((root/'captures/algebra_controls.stdout').read_bytes())
v=json.loads((root/'captures/original_verify.stdout').read_bytes())
ck(a['assertions_passed']==15026 and a['all_F2_matrices']==5058)
ck(v['assertions']==564 and v['status']=='PASS')
ck((root/'captures/original_verify.stdout').read_bytes()==(original/'original/verification.json').read_bytes())
cache=N/'unsolved_math_prioritization/cache'
manifest=json.loads((N/'unsolved_math_prioritization/manifest.json').read_bytes())
corpus={}
for name in ('problems.json','research_results.json'):
 p=cache/name;desc=pin(p);corpus[name]={'path':str(p),**desc,'not_copied':True}
 ck(desc=={k:manifest['files'][name][k] for k in ('bytes','sha256')})
 data=json.loads(p.read_bytes())
 if name=='problems.json':
  rows=[r for r in data if r['id']==2715]
  ck(len(rows)==1);problem=rows[0]
 else:
  ck('KP-1.56' not in data);raw=data.get('KP-1.56')
sql=sqlite3.connect((cache/'catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
payload,report,kind=sql.execute('SELECT payload,report,typeof(report) FROM records WHERE key=?',('2715',)).fetchone();sql.close()
ck(json.loads(payload)==problem==json.loads((original/'original/source_record.json').read_bytes()))
ck(raw is None and kind=='text' and report=='{}' and json.loads(report)!=raw)
ck(json.loads((original/'SELECTED_RAW_PRIOR.json').read_bytes()) is None)
ck((original/'RAW_PRIOR_SQL_TEXT.txt').read_bytes()==b'{}')
turn=json.loads((original/'original/turns.json').read_bytes())
ck(turn['substantive_proof_attempts']==1 and turn['budget']==5 and len(turn['turns'])==1 and turn['turns'][0]['outcome']=='unsolved')
result={'status':'PASS_SOURCE_CAPTURE_TYPED_ACCOUNTING_ONLY','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':checks,'corpus':corpus,'raw_prior':{'KP-1.56_key_present':False,'selected_raw_value':None,'SQL_typeof_report':kind,'SQL_literal':report,'SQL_decoded_equals_raw':False},'original_budget':'unsolved1/5','new_substantive_attempts':0,'audit_increment':0,'no_Git_or_source_mutation':True,'historical_bodies_hashed_not_interpreted':True,'original_source_pin':pin(original/'original/source_record.json'),'original_turns_pin':pin(original/'original/turns.json')}
print(json.dumps(result,indent=2,sort_keys=True))
