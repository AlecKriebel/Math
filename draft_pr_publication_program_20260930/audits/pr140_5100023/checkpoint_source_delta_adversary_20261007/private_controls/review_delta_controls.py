"""Small in-memory SOURCE-ONLY controls; never call candidate main/publish/install."""
from pathlib import Path
import ast, copy, datetime, hashlib, json, os, sys

ROOT=Path(__file__).resolve().parents[2]
NEW=ROOT/'scoped_active_checkpoint_20261007/scoped_checkpoint_publish_v1.py'
OLD=ROOT.parent/'pr134_2306064/scoped_completion_transaction_20261007/scoped_publish_v6.py'
NEW_SHA='c7d2ac2cd330233efe96e69e6f6f47a1e3fc8cd7f3af868aad656182fc3aca32'
OLD_SHA='5ed00128d4c7b34d629807d2e80d2f68d8306bfd7e8a8f91683bd9fa18e2754a'
def sha(b):return hashlib.sha256(b).hexdigest()
def demand(ok,msg):
    if not ok:raise RuntimeError(msg)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
new,old=NEW.read_bytes(),OLD.read_bytes()
demand(sha(new)==NEW_SHA and sha(old)==OLD_SHA,'immutable source pins')
ns={'__name__':'source_review_only','__file__':str(NEW)}
exec(compile(new,str(NEW),'exec'),ns)
demand(ns['NATIVE']==set() and ns['ATTEMPT']==set(),'native mutation enabled')
demand(ns['PROGRAM']=={'draft_pr_publication_program_20260930/'+f for f in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']},'program install set')
old_defs={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(old).body if isinstance(n,ast.FunctionDef)}
new_defs={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(new).body if isinstance(n,ast.FunctionDef)}
demand(set(old_defs)==set(new_defs),'function inventory changed')
changed={k for k in old_defs if old_defs[k]!=new_defs[k]}
demand(changed=={'guard','load_inputs','install','main'},'unexpected changed function')
# Confirm the only function-level changes are the documented guard/schema/temp delta.
old_text=old.decode();new_text=new.decode()
def function_text(body,name):
    tree=ast.parse(body);n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    return '\n'.join(body.splitlines()[n.lineno-1:n.end_lineno])
for name in changed:
    before=function_text(old_text,name)
    if name=='guard':
        before=before.replace("plan['original_PR_head']","plan['previous_PR134_original_head']")
        before+='\n    current_pr=json.loads(run([GH,\'api\',\'repos/AlecKriebel/Math/pulls/140\'],journal))\n    require(current_pr[\'state\']==\'open\' and current_pr[\'merged_at\'] is None and current_pr[\'draft\'] is True and current_pr[\'head\'][\'sha\']==plan[\'current_PR140_original_head\'],\'PR140 intake head/state changed\')'
    elif name=='load_inputs':before=before.replace('pr134-scoped-overlay/v1','pr140-active-checkpoint-overlay/v1')
    elif name=='install':before=before.replace('.pr134-','.pr140-')
    else:before=before.replace('pr134-scoped-operation-receipt/v1','pr140-active-checkpoint-operation-receipt/v1')
    demand(before==function_text(new_text,name),'function delta: '+name)

files={str(NEW):new};checks=[];cases=[]
class MemPath:
    def __init__(self,p):self.key=str(p)
    def read_bytes(self):return files[self.key]
    def __str__(self):return self.key
ns['Path']=MemPath
ns['safe']=lambda p:MemPath(p)
ns['check']=lambda p,e:checks.append(str(p))
pin={'bytes':1,'mode':420,'sha256':sha(b'x')}
def load_case(name,members,accept,schema='pr140-active-checkpoint-overlay/v1'):
    plan={'schema':schema,'source_sha256':NEW_SHA,'git_executable':pin,'gh_executable':pin,'members':members}
    pb=json.dumps(plan,sort_keys=True).encode();ph=sha(pb)
    rb=json.dumps({'verdict':'PASS','plan_sha256':ph,'source_sha256':NEW_SHA}).encode()
    files['mem_plan']=pb;files['mem_review']=rb
    try:ns['load_inputs']('mem_plan',ph,'mem_review',sha(rb));actual=True;error=None
    except RuntimeError as exc:actual=False;error=str(exc)
    demand(actual==accept,'unexpected allowlist outcome '+name)
    cases.append({'name':name,'accepted':actual,'expected':accept,'rejection':error})
def member(path,install=False,mode=420):return {'path':path,'source':'mem_source','post':dict(pin,mode=mode),'install':install}
for path in sorted(ns['PROGRAM']):load_case('program install '+path,[member(path,True)],True)
for prefix in ns['AUDIT']:
    load_case('audit publication '+prefix,[member(prefix+'REPORT.md')],True)
    load_case('audit installation forbidden '+prefix,[member(prefix+'REPORT.md',True)],False)
for path in ['unsolved_math_prioritization/state.json','unsolved_math_prioritization/attempts/2306064/README.md','draft_pr_publication_program_20260930/audits/pr140_51000230/REPORT.md','draft_pr_publication_program_20260930/ordered_intake_20261007/after_PR1340/REPORT.md','draft_pr_publication_program_20260930/audits/pr140_5100023/../outside.md','/absolute.md','draft_pr_publication_program_20260930/audits/pr140_5100023//REPORT.md']:
    load_case('outside or noncanonical '+path,[member(path)],False)
program=sorted(ns['PROGRAM'])[0]
load_case('duplicate path',[member(program),member(program)],False)
load_case('unsupported file mode',[member(program,True,493)],False)
load_case('old plan schema',[member(program)],False,'pr134-scoped-overlay/v1')

plan={'protected':[],'protected_absences':[],'R_HEAD':'a'*40,'C_HEAD':'b'*40,'previous_PR134_original_head':'c'*40,'current_PR140_original_head':'d'*40,'closing_comment_body_sha256':sha(b'closed explanation')}
records={'repos/AlecKriebel/Math/pulls/134':{'state':'closed','merged_at':None,'draft':True,'head':{'sha':'c'*40}},'repos/AlecKriebel/Math/issues/comments/6028564660':{'body':'closed explanation'},'repos/AlecKriebel/Math/pulls/140':{'state':'open','merged_at':None,'draft':True,'head':{'sha':'d'*40}}}
ns['git']=lambda args,journal:((plan['R_HEAD'] if args[1]==str(ns['R']) else plan['C_HEAD'])+'\n') .encode()*2
requests=[]
def fake_run(argv,journal,*args,**kw):
    requests.append(argv[2]);return json.dumps(active_records[argv[2]]).encode()
ns['run']=fake_run
def guard_case(name,mutate,accept):
    global active_records
    active_records=copy.deepcopy(records);mutate(active_records)
    try:ns['guard'](plan,{'children':[]});actual=True;error=None
    except RuntimeError as exc:actual=False;error=str(exc)
    demand(actual==accept,'unexpected PR guard outcome '+name)
    cases.append({'name':name,'accepted':actual,'expected':accept,'rejection':error})
guard_case('current original draft and prior closed disposition',lambda r:None,True)
for field,value in [('state','closed'),('draft',False),('merged_at','2026-10-07'),('head',{'sha':'e'*40})]:
    guard_case('PR140 changed '+field,lambda r,f=field,v=value:r['repos/AlecKriebel/Math/pulls/140'].__setitem__(f,v),False)
for field,value in [('state','open'),('draft',False),('merged_at','2026-10-07'),('head',{'sha':'e'*40})]:
    guard_case('PR134 changed '+field,lambda r,f=field,v=value:r['repos/AlecKriebel/Math/pulls/134'].__setitem__(f,v),False)
guard_case('prior closing comment changed',lambda r:r['repos/AlecKriebel/Math/issues/comments/6028564660'].__setitem__('body','different'),False)
guard_case('PR140 truthy nonboolean draft',lambda r:r['repos/AlecKriebel/Math/pulls/140'].__setitem__('draft',1),False)
guard_case('PR140 null state',lambda r:r['repos/AlecKriebel/Math/pulls/140'].__setitem__('state',None),False)
demand(set(requests)==set(records),'guard request scope')
demand(NEW.read_bytes()==new and OLD.read_bytes()==old,'source changed during review')
result={'schema':'pr140-checkpoint-source-delta-controls/v1','verdict':'PASS','source_sha256':NEW_SHA,'predecessor_sha256':OLD_SHA,'actual_PID':os.getpid(),'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'optimized':not __debug__,'changed_functions':sorted(changed),'inherited_identical_functions':sorted(set(new_defs)-changed),'cases':cases,'case_count':len(cases),'candidate_main_publish_install_called':False,'candidate_subprocess_called':False,'fake_records_only':True,'publication_executed':False,'plan_or_postimage_clearance':False}
out=Path(sys.argv[1]);demand(out.parent==Path(__file__).resolve().parent,'owned result path');demand(not out.exists(),'result exists')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');out.chmod(0o644)
print(json.dumps({'verdict':result['verdict'],'case_count':len(cases),'actual_PID':os.getpid(),'optimized':result['optimized'],'output':str(out)}))
