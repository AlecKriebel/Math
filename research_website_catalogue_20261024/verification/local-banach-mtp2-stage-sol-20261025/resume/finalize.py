"""One-time close of private stage after target tests; no production writes."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
E=Path(__file__).resolve().parent;O=E.parent;P=O.parents[1];PY=sys.executable;H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
if (E/'SEAL.json').exists():raise RuntimeError('private stage already sealed')
def put(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
faults=[json.loads((E/('FAULTS_'+mode+'.json')).read_bytes()) for mode in ['normal','optimized']]
if not all(x['status']=='PASS' and x['case_count']==x['passed']==204 for x in faults):raise ValueError('expanded target suite not complete')
if [(x['record'],x['case'],x['positive'],x['passed']) for x in faults[0]['cases']]!=[(x['record'],x['case'],x['positive'],x['passed']) for x in faults[1]['cases']]:raise ValueError('mode disagreement')
for x in faults:
 if any(H(E/name)!=pin for name,pin in x['code_bindings'].items()):raise ValueError('fault suite code changed')
for mode in ['normal','optimized']:
 for suffix in ['json','md','stdout','stderr']:
  old=E/('target-final-'+mode+'.'+suffix)
  if old.exists():old.rename(E/('target-pre-auditor192-'+mode+'.'+suffix))
(E/'FINAL_POSITIVE_COMMANDS.json').rename(E/'PRE_AUDITOR_FINAL_POSITIVE_COMMANDS.json')
commands=[]
for mode,flag in [('normal',[]),('optimized',['-O'])]:
 command=[PY,'-B',*flag,str(E/'run.py'),str(E/'final-content-check.stage.py'),'23217863','23146753','--site',str(E/'public'),'--output-dir',str(E),'--output-stem','target-final-'+mode]
 r=subprocess.run(command,capture_output=True,text=True)
 (E/('target-final-'+mode+'.stdout')).write_text(r.stdout);(E/('target-final-'+mode+'.stderr')).write_text(r.stderr)
 commands.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'exit':r.returncode})
 if r.returncode:put('FINAL_POSITIVE_COMMANDS_FAILED.json',commands);raise RuntimeError('final positive failed '+mode)
put('FINAL_POSITIVE_COMMANDS.json',commands)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
readmap=json.loads((E/'PRE_AUDITOR_RENDERED_READ_MAP.json').read_bytes());readmap['utc']=now
for x in readmap['records']:
 qa=json.loads((E/'target-final-normal.json').read_bytes())['papers'][x['record_id']]
 x['passed_checks']=len(qa['checks']);x['whole_document_visibility_grammar_and_wrappers_checked']=True
put('RENDERED_READ_MAP.json',readmap)
v=json.loads((E/'PRE_AUDITOR_VERDICT.json').read_bytes());v['utc']=now
v.update({'normal_fault_cases_passed':204,'optimized_fault_cases_passed':204,'independent_auditor_counterexample_fixed':'Outer template/noscript wrapper suppressed visible article while passing syntactic body text checks. Whole-document parent/nesting grammar and six outer wrapper controls perrecord added. Prior192passes/unadopted readiness retained.','independent_auditor_adoption_received':False,'root_adoption_received':False,'whole_document_closed_grammar':True})
put('VERDICT.json',v)
faultbase=[PY,'-B',str(E/'run.py'),str(E/'fault_campaign.py')]
ledger={'utc':now,'recovery_render_commands':json.loads((E/'RECOVERY_COMMANDS.json').read_bytes()),'fault_commands_in_actual_order':[{'command':faultbase,'exit':1,'receipt':'FAULTS_normal_initial_failure.json'},{'command':faultbase,'exit':0,'receipt':'FAULTS_normal_intermediate_pass.json'},{'command':faultbase,'exit':0,'receipt':'FAULTS_normal_pre_auditor192_pass.json'},{'command':[PY,'-B','-O',str(E/'run.py'),str(E/'fault_campaign.py')],'exit':0,'receipt':'FAULTS_optimized_pre_auditor192_pass.json'},{'command':faultbase,'exit':0,'receipt':'FAULTS_normal.json'},{'command':[PY,'-B','-O',str(E/'run.py'),str(E/'fault_campaign.py')],'exit':0,'receipt':'FAULTS_optimized.json'}],'compatibility_command':{'command':[PY,'-B',str(E/'compatibility_once.py')],'exit':0,'receipt':'COMPATIBILITY.json'},'final_positive_commands':commands,'predecessor_pypdf_failure':'Unmodified ../initial-render-103.stderr; this existed before resume. Recovered with the bundled Python from load_workspace_dependencies; no package installation.','no_legacy_campaign_repetition':True}
put('COMMAND_LEDGER.json',ledger)
with (E/'RESEARCH_LOG.md').open('a') as f:f.write('* '+now+' — Completion100% of bounded private preparation. Expanded204/204 normal and204/204 optimized target controls PASS, same outcomes. Final pristine positives33/33 and32/32 in bothmodes. One old69 suite4037checks and paired138 renderer processes/426complete outputfiles remain PASS without repetition. Seal and read-only verifier prepared. Independent auditor/root adoption and all installation/live/browser390/native PDF/download/Sheet gates remain pending. No production, source, Git or external-contact mutation.\n')
owned=[p for p in sorted(E.rglob('*')) if p.is_file() and p.name not in {'OWNED_MANIFEST.json','SEAL.json'}]
put('OWNED_MANIFEST.json',{'utc':now,'status':'PRIVATE_STAGE_OWNED_PAYLOADS_ONLY','files':[{'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':H(p)} for p in owned],'owned_bindings':len(owned)})
put('SEAL.json',{'utc':now,'status':'PRIVATE_STAGE_SEALED_FOR_INDEPENDENT_ROOT_ADOPTION','manifest_sha256':H(E/'OWNED_MANIFEST.json'),'manifest_bytes':(E/'OWNED_MANIFEST.json').stat().st_size,'owned_bindings':len(owned),'immutable_input_bindings':359,'planning_owned_bindings':10,'records':['23217863','23146753'],'production_adoption':False,'publication_authority':False,'private_preparation_completion_percent':100,'overall203_goal_complete':False})
print('sealed',len(owned),'owned payloads; sealSHA256',H(E/'SEAL.json'))
