from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys
H=Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';ctx=json.loads((A/'CURRENT_PR1280_CONTEXT.json').read_text());paths=[P/n for n in ['prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py']]+[A.parents[1]/'publication_coordinators'/n for n in ['pr1280.py','verify_pr1280_merge.py']]+[A/'_local/ready_and_merge.py',Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')]
checks=[]
for p in paths:
 b=p.read_bytes();count=sum(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(b)))
 if count:raise RuntimeError('assert in deployed validator '+str(p))
 checks.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'ast_assert_count':count})
sentinels=[]
for spec in ctx['diagnostic_replays']:
 for flags in [[],['-O'],['-OO']]:
  code="import runpy;d=runpy.run_path("+repr(str(A/spec['program']))+");d['require'](False,'FRESH-ADVERSARIAL-FALSE-SENTINEL')"
  r=subprocess.run([sys.executable,'-B',*flags,'-c',code],capture_output=True,text=True)
  if r.returncode==0 or 'FRESH-ADVERSARIAL-FALSE-SENTINEL' not in r.stderr or r.stdout:raise RuntimeError('durable validator inactive')
  sentinels.append({'program':spec['program'],'flags':flags,'false_validator_failed':True,'positive_stdout_absent':True})
t=__import__('runpy').run_path(str(P/'append_tracker.py'));near=[]
for x in ['300035870','300035879','https://github.com/AlecKriebel/Math/pull/12800','https://github.com/AlecKriebel/Math/pull/12801']:
 near.append({'unrelated_identity':x,'incorrectly_matches_target':t['row_has_problem_identity']([x])})
(H/'VALIDATOR_CHECKS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_sources':checks,'false_sentinels':sentinels,'identity_near_collisions':near},indent=2)+'\n');print('validated12actual sources and18false diagnostic sentinels; recorded4identity near-collisions')
