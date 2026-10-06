#!/usr/bin/env python3
"""Pure independent PR108 source/configuration challenges. Never calls prepare/execute/resources.
Only writes its own result JSON. The source/helper/input paths are explicit argv.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,copy,datetime,hashlib,importlib.util,json,os,re
D=Path(sys.argv[1]).absolute(); F=Path(sys.argv[2]).absolute(); J=Path(sys.argv[3]).absolute(); O=Path(__file__).absolute().parent
sys.path.insert(0,str(D))
import v3_guards as g
spec=importlib.util.spec_from_file_location('joint_review_prepare_pure',D/'prepare_review_bundle.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
checks=[]
def ck(name,v):
 if not v:raise RuntimeError(name)
 checks.append(name)
def rej(name,f):
 try:f()
 except (ValueError,KeyError,TypeError):checks.append(name);return
 raise RuntimeError('Expected reject: '+name)
def ok(name,f):f();checks.append(name)
x=g.loads(F.read_bytes());cfg=x['effective'];data=F.read_bytes();g.validate_execution_manifest(x,data)
ck('clean startup flags',sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode)
g.validate_environment_policy(cfg['environment_policy'])
# F10 oracle uses independently enumerated expected physical clauses.
for end in ['\n','\r','\r\n']:
 for pad in ['', ' ', '\t', ' \t']:
  for value in ['', ' ', '\t', ' # default', '""', "''", '"" # default']:
   body=pad+'http_unix_socket:'+value+end+'# intervening'+end+pad+'editor: nano'+end+'aliases:'+end+'  co: pr checkout'+end
   ok('F10 empty socket '+repr((end,pad,value)),lambda b=body:g.validate_gh_configuration_lines(b))
 for value in ['/tmp/socket','"/tmp/socket"',"'/tmp/socket'",'|','>','!evil','null','[]']:
  rej('F10 nonempty socket '+repr((end,value)),lambda v=value,e=end:g.validate_gh_configuration_lines('http_unix_socket: '+v+e+'editor: nano'))
 for body in ['aliases:'+end+'  pr: !echo injected','aliases:'+end+'  pr: "!echo injected"','aliases:'+end+"  pr: '!echo injected'",'aliases:'+end+'  pr:'+end+'    !echo injected','http_unix_socket:'+end+'  /tmp/socket']:
  rej('F10 inline or continuation executable/socket '+repr(body),lambda b=body:g.validate_gh_configuration_lines(b))
ok('F10 whole comments ignored',lambda:g.validate_gh_configuration_lines('# http_unix_socket: /tmp/socket\n# pr: !evil\n'))
# F09 derive against the exact authenticated native manifest from inert read custody.
j=g.loads(J.read_bytes());m=[r for r in j['records'] if r['argv'][1:]==['show',cfg['main_parent']+':unsolved_math_prioritization/manifest.json']]
ck('native manifest one complete bounded prior read',len(m)==1 and m[0]['stdout_bytes']==486)
mb=bytes.fromhex(m[0]['stdout_prefix_hex']);ck('native manifest complete custody SHA',len(mb)==486 and g.sha(mb)==m[0]['stdout_sha256'])
out=D/('candidate_'+g.sha(data)[:16]);control=g.derive_worker_control(x,data,out,mb)
ck('independent control policy exact',control['worker_policy']==cfg['worker_policy'])
ck('independent control queue execution exact',control['queue_py_sha256']==cfg['queue_py_sha256'] and control['execution_inputs_sha256']==g.sha(data))
ck('independent control manifest/source provenance',control['record_count']==15458 and control['dataset_revision']=='37e53eabe540fb458758e198be61634bd02ee008')
caps={Path(v['path']).name:v['bytes']+(524288 if Path(v['path']).name in {'catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'} else 0) for v in cfg['native_baseline_pins']};caps['assessment.json']=131072
ck('independent13 backend cap formula',control['backend_file_caps']==caps)
ok('correct whole control',lambda:g.validate_worker_control(control,x,data,out,mb))
c=copy.deepcopy(control);c['worker_policy']['cpu_seconds']=2
rej('valid numeric CPU2 differs from frozen CPU90',lambda:g.validate_worker_control(c,x,data,out,mb))
def leaves(v,prefix=()):
 for k,z in v.items():
  if isinstance(z,dict):yield from leaves(z,prefix+(k,))
  else:yield prefix+(k,),z
def altered(v,path,value,remove=False):
 c=copy.deepcopy(v);q=c
 for k in path[:-1]:q=q[k]
 if remove:del q[path[-1]]
 else:q[path[-1]]=value
 return c
for path,v in leaves(control):
 for value in [True,1.0,'changed']:
  if g.canonical(value)==g.canonical(v):continue
  c=altered(control,path,value)
  rej('control changed '+str(path)+' '+repr(value),lambda c=c:g.validate_worker_control(c,x,data,out,mb))
 c=altered(control,path,None,True);rej('control omitted '+str(path),lambda c=c:g.validate_worker_control(c,x,data,out,mb))
for path in [(),('worker_policy',),('backend_file_caps',)]:
 c=copy.deepcopy(control);q=c
 for z in path:q=q[z]
 q['extra']=1;rej('control extra '+str(path),lambda c=c:g.validate_worker_control(c,x,data,out,mb))
proc={'exit_code':0,'termination_reason':None,'child_reaped':True,'deadline_seconds':cfg['worker_policy']['deadline_seconds'],'PID':987654}
policy=cfg['worker_policy'];result={'schema':'pr108-native-assess-worker-receipt/v3','fixture':False,'outcome':'success','native_assess_returned_without_exception':True,'actual_operator_PID':987654,'execution_inputs_sha256':g.sha(data),'validated_worker_control':control,'worker_control_binding_sha256':g.sha(g.canonical(control)),'requested_resource_policy':copy.deepcopy(policy),'ROOT':control['ROOT'],'queue_py_sha256':control['queue_py_sha256'],'native_function':'queue.py:assess','SQL_connection':'mode=ro&immutable=1','native_status_command_called':False,'applied_limits':{n:[policy[k],policy[k]] for n,k in [('RLIMIT_CPU','cpu_seconds'),('RLIMIT_FSIZE','file_size_bytes'),('RLIMIT_NOFILE','open_files')]},'hard_memory_limit_claimed':False,'memory_policy':{'hard_memory_limit_claimed':False,'platform':sys.platform,'requested_advisory_bytes':policy['address_space_bytes'],'RLIMIT_RSS_used':False,'RLIMIT_AS_enforcement_certified':False,'RLIMIT_AS_requested':False}}
ok('exact synthetic parent result shape only',lambda:g.validate_worker_result(result,control,proc))
for path,v in leaves(result):
 for value in [True,1.5,'changed']:
  if g.canonical(value)==g.canonical(v):continue
  c=altered(result,path,value);rej('result changed '+str(path)+' '+repr(value),lambda c=c:g.validate_worker_result(c,control,proc))
for k,v in [('exit_code',1),('termination_reason','deadline_exceeded'),('child_reaped',False),('deadline_seconds',119),('PID',987655)]:
 pr={**proc,k:v};rej('process altered '+k,lambda pr=pr:g.validate_worker_result(result,control,pr))
# AST order independently prevents fixture evidence from claiming actual native execution.
w=ast.parse((D/'native_assess_worker.py').read_text()); fn=next(z for z in w.body if isinstance(z,ast.FunctionDef) and z.name=='execute')
find=lambda name:min(z.lineno for z in ast.walk(fn) if isinstance(z,ast.Call) and isinstance(z.func,ast.Attribute) and z.func.attr==name)
ck('worker control validates before resource or module load',find('validate_worker_control')<min(z.lineno for z in ast.walk(fn) if isinstance(z,ast.Call) and ((isinstance(z.func,ast.Name) and z.func.id=='apply_resource_policy') or (isinstance(z.func,ast.Attribute) and z.func.attr=='exec_module'))))
source=(D/'prepare_review_bundle.py').read_text()
ck('parent immutable control bytes verified before result acceptance',source.index("(output/'WORKER_CONTROL.json').read_bytes()==encode(expected_control)")<source.index('g.validate_worker_result'))
# Scope/environment rejection and CSV byte preservation, without external programs.
for role in ['python','initial_launcher','git','gh']:
 e=copy.deepcopy(cfg['environment_policy']);e[role]['environment']['PYTHONPATH']='/tmp/untrusted';rej('ambient policy '+role,lambda e=e:g.validate_environment_policy(e))
for cp in [dict(cfg['capacity_policy'],future_commit_overhead_bytes=1),dict(cfg['capacity_policy'],headroom_bytes=1),dict(cfg['capacity_policy'],runtime_overhead_bytes=1)]:
 rej('invalid reserve '+str(cp),lambda cp=cp:g.capacity_inventory(cfg['native_baseline_pins'],[],{r:{'bytes':65536} for r in g.GATE_ROLES},{},cp,cfg['process_policy']))
for sep in ['\v','\f','\x1c','\x1d','\x1e','\x85','\u2028','\u2029']:
 for end in ['\n','\r','\r\n','']:
  b=('id,local_status,turns_used,holds,reasons,note\r\nother,queued,0,,,"untouched'+sep+'text"\r\n30003996,queued,0,,,old'+end).encode()
  t={'id':'30003996','local_status':'claimed_solved','turns_used':2,'holds':[],'reasons':[],'note':'new\r\nvalue'}
  o=g.csv_overlay(b,t);_,pre=g.csv_records(b);_,post=g.csv_records(o)
  ck('CSV unrelated exact '+repr((sep,end)),pre[0]['bytes']==post[0]['bytes'] and pre[1]['bytes']==post[1]['bytes'] and len(pre)==len(post)==3)
# Exact target row envelope compatibility and complete consumer closure.
C=O.parents[3];A=O.parent;reader=g.ReviewedInputs(x,C,A)
package_path=C/cfg['package']['manifest']['path'];package_bytes=reader.read(cfg['package']['manifest'])[1];package=g.loads(package_bytes);files={}
for item in package['files']:
 pin={'path':cfg['package']['root']+'/'+item['relative_path'],'bytes':item['bytes'],'sha256':item['sha256']};files[item['relative_path']]=reader.read(pin)[1]
pub,doi=p.publication_check(cfg,files,package_bytes,reader.read)
sheet=g.loads(reader.read(cfg['google_sheet']['receipt'])[1]);expected={'DOI':doi,**{k:cfg['google_sheet'][k] for k in ['row_index','values','existing_chat_authorized']}}
g.validate_sheet(sheet,expected,pub['UTC_end'],reader.read);checks.append('actual sealed v2 receipt directly compatible with blankB')
ck('exact blankB and expected row31',cfg['google_sheet']['values'][1]=='' and cfg['google_sheet']['existing_chat_authorized'] is False and cfg['google_sheet']['row_index']==31)
for pin in cfg['original_authentication_pins'].values():
 for v in (pin if isinstance(pin,list) else [pin]):reader.read(v)
for pin in cfg['effective_diagnostics_pins']:reader.read(pin)
gate_usage=g.loads((J.parent/'PROPOSED_GATE_CHECKED_ARTIFACT_USAGE.json').read_bytes())
for pins in gate_usage.values():
 for pin in pins:reader.read(pin)
reader.finish();ck('all exact180 input consumers consumed',len(reader.used)==len(x['input_files'])==180)
r={'schema':'pr108-joint-V5-independent-pure-tests/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'optimized':bool(sys.flags.optimize),'checks_passed':len(checks),'check_names':checks,'execution_inputs_sha256':g.sha(data),'program_sha256':{name:g.sha((D/name).read_bytes()) for name in g.PROGRAMS},'synthetic_results_authorize_actual_native_execution':False,'actual_native_or_services_called':False}
(O/('OPTIMIZED_RESULTS.json' if sys.flags.optimize else 'NORMAL_RESULTS.json')).write_bytes(g.canonical(r));print(json.dumps({'checks_passed':len(checks),'PID':os.getpid(),'optimized':bool(sys.flags.optimize)}))
