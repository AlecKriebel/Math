#!/usr/bin/env python3
"""Exercise the acceptance gate locally with synthetic review03 and terminal-write sentinel."""
import argparse,contextlib,copy,hashlib,importlib.util,io,json,pathlib,shutil,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1];P=R.parents[3];ROOT=P.parent
class TerminalGateObserved(Exception):pass
def need(x,s):
 if not x:raise RuntimeError(s)
def fp(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def perform():
 spec=importlib.util.spec_from_file_location('review03_acceptance_gate',R/'reviewed_helpers/accept_pr919.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 work=R/'private/acceptance_gate_controls';work.mkdir(exist_ok=True);rows=[]
 with tempfile.TemporaryDirectory(dir=work,prefix='SYNTHETIC_') as td:
  synthetic=pathlib.Path(td);effort=synthetic/'program';audit=effort/'audits/pr919_30002555';d=audit/'publication';d.mkdir(parents=True)
  for n in ['ORIGINAL_SNAPSHOT.json','PUBLICATION_DISPOSITION.json','PREMERGE_QUEUE_SCOPE_CHECK.json','TARGET_IDENTITY_PREFLIGHT.json','FUTURE_HELPERS_PREPARATION.json']:shutil.copy2(A/n,audit/n)
  snap=json.loads((audit/'ORIGINAL_SNAPSHOT.json').read_text())
  for n in snap['files']:
   q=audit/'original'/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(A/'original'/n,q)
  freeze=json.loads((A/'publication/PREPUBLICATION_FREEZE.json').read_text())
  for n in [*freeze['files'],'PREPUBLICATION_FREEZE.json']:
   q=d/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(A/'publication'/n,q)
  for n in m.HELPERS:shutil.copy2(R/'reviewed_helpers'/n,effort/n)
  for number in (1,2):
   old=A/'reviews'/f'full_package_{number:02}';dest=audit/'reviews'/old.name;dest.mkdir(parents=True)
   manifest=json.loads((old/'MANIFEST.json').read_text())
   for n in [*manifest['files'],'MANIFEST.json']:
    q=dest/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old/n,q)
  latest=audit/'reviews/full_package_03';latest.mkdir();(latest/'REPRODUCTION_RECEIPT.json').write_text(json.dumps({'status':'PASS','synthetic_fixture':True}))
  baseline={'pr':919,'problem_id':'30002555','original_pr_head':m.HEAD,'required_issues':[],'optional_issues':[],'clean_for_preprint':True,'mathematical_remaining_gap_for_stated_theorem':None,'candidate_pins':{'freeze':m.FREEZE,'manifest':m.PACKAGE,'pdf':freeze['files']['output/pdf/note.pdf']['sha256']},'started_utc':'2026-10-15T06:47:08+00:00','completed_utc':'2026-10-15T07:00:00+00:00','prior_issue_resolution':{k:{'verified':True} for k in ['R1','R2','O1','O2','O3']},'executed_validations':{'full_reproducer_completed':True,'final_endpoint_authentication_after_seal_verifier_and_full_reproducer':True},'inspected_helper_hashes':{n:fp(effort/n) for n in m.HELPERS},'inspected_acceptance_gate':fp(R/'reviewed_helpers/accept_pr919.py'),'strongest_verified_theorem':'SYNTHETIC THEOREM FIELD; NOT AN ACCEPTANCE'}
  live=json.loads((R/'START_AUTHENTICATION.json').read_text())['live_pr'];source=json.loads((audit/'TARGET_IDENTITY_PREFLIGHT.json').read_text());scope=json.loads((audit/'PREMERGE_QUEUE_SCOPE_CHECK.json').read_text());calls=[]
  def fake_run(args,binary=False):
   calls.append(args[:3])
   if args[:3]==['gh','pr','view']:return json.dumps({**live,'url':'https://github.com/AlecKriebel/Math/pull/919'})
   if args[:2]==['gh','api']:return '\n'.join([*snap['files'],m.QUEUE])
   if args[:2]==['git','ls-remote']:return '19c1c3a32d560bba70488efb929126b15a0a88ef\trefs/heads/main\n'
   if args[:2]==['git','fetch']:return ''
   if args[:2]==['git','show']:
    if args[2].endswith(':unsolved_math_prioritization/catalog.json'):return json.dumps([{'id':30002555,'present':True,'holds':[],'statement_hash':source['statement_hash'],'review_hash':source['review_hash']}])
    raw=subprocess.check_output(args,cwd=ROOT);return raw if binary else raw.decode()
   raise RuntimeError('Unexpected external command blocked: '+str(args))
  m.P=effort;m.A=audit;m.D=d;m.ROOT=synthetic;m.run=fake_run
  def stop_before_any_final_write(*args):raise TerminalGateObserved('all gates passed; first write blocked')
  m.save=stop_before_any_final_write
  def reseal(result):
   (latest/'RESULT.json').write_text(json.dumps(result));names=['RESULT.json','REPRODUCTION_RECEIPT.json'];manifest={'files':{n:fp(latest/n) for n in names},'explicit_public_allowlist':names};(latest/'MANIFEST.json').write_text(json.dumps(manifest));return fp(latest/'MANIFEST.json')['sha256']
  cases=[('clean_positive_terminal_sentinel',None,None,True),('remaining_required',['required_issues'],[{'id':'X'}],False),('remaining_optional',['optional_issues'],[{'id':'X'}],False),('unclean',['clean_for_preprint'],False,False),('math_gap',['mathematical_remaining_gap_for_stated_theorem'],'gap',False),('wrong_candidate',['candidate_pins','freeze'],'0'*64,False),('unreproduced',['executed_validations','full_reproducer_completed'],False,False),('no_final_endpoint',['executed_validations','final_endpoint_authentication_after_seal_verifier_and_full_reproducer'],False,False),('nonsequential_start',['started_utc'],'2026-10-15T06:20:00+00:00',False),('O3_unresolved',['prior_issue_resolution','O3','verified'],False,False),('helper_different',['inspected_helper_hashes','run_pr919_zenodo.py','sha256'],'0'*64,False),('gate_different',['inspected_acceptance_gate','sha256'],'0'*64,False)]
  for label,path,value,positive in cases:
   r=copy.deepcopy(baseline)
   if path:
    x=r
    for k in path[:-1]:x=x[k]
    x[path[-1]]=value
   seal=reseal(r);old=sys.argv;sys.argv=['synthetic_acceptance','--review03-manifest',seal];reached=False;error=None
   try:
    with contextlib.redirect_stdout(io.StringIO()):m.main()
   except TerminalGateObserved:reached=True
   except RuntimeError as e:error=str(e)
   finally:sys.argv=old
   need(reached==positive,label);need(not (audit/'ACCEPTANCE.json').exists() and not (audit/'FINAL_ACCEPTANCE_GATE.json').exists(),'receipt accidentally written');rows.append({'case':label,'terminal_write_sentinel_reached':reached,'rejected':not reached,'guard':error,'passed':True})
 return {'status':'PASS','positive_all_gates_terminal_sentinel':1,'negative_rejections':len(cases)-1,'rows':rows,'synthetic_review03_not_real_acceptance':True,'actual_service_actions':0,'real_acceptance_receipts_written':0,'gate':fp(R/'reviewed_helpers/accept_pr919.py')}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path);a=p.parse_args();r=perform()
 if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
