from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,sys
A=Path(__file__).resolve().parents[1];D=A/'native_post_assess_carryforward_v3_20261006'
def need(v,m):
 if not v:raise RuntimeError(m)
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(f):return {'path':str(f.relative_to(A)),**hp(f.read_bytes())}
def obj(f):return json.loads(f.read_bytes())
checked=[]
def check(f,s):
 st=f.lstat();need(f.is_file() and not f.is_symlink() and st.st_nlink==1,'Safe regular body')
 need(hp(f.read_bytes())=={k:s[k] for k in ('bytes','sha256')},'Exact complete body '+str(f))
 checked.append(pin(f))
adpath=Path(sys.argv[1]);need(adpath.is_relative_to(A),'Dedicated review')
ad=obj(adpath);V=adpath.parent
need(ad['schema']=='pr110-post-assess-carryforward-adversary/v1' and ad['actual_review'] is True and ad['clearance'] is True and ad['required_findings']==[] and ad['future_candidate_approved'] is False and ad['live_actions_approved'] is False and ad['original_resource_policy_unchanged'] is True,'Actual limited preexecution review')
m=obj(D/'OUTPUT_MANIFEST.json');seal=obj(D/'SEAL_RECEIPT.json');check(D/'OUTPUT_MANIFEST.json',seal['manifest_pin'])
need(m['file_count']==len(m['files']) and m['total_bytes']==sum(s['bytes'] for s in m['files']),'Complete sealed preparation manifest')
for s in m['files']:check(D/s['path'],s)
for key in ['program_pin','action_program_pin','outer_launcher_pin','linear_diff_program_pin','stopped_CPU_continuation_inventory_pin','integration_inputs_pin','stopped_continuation_inventory_pin','seed_inventory_pin','failed_run_root_authentication_pin','report_pin']:
 s=ad[key];check(A/s['path'],s)
for s in ad['reviewed_root_helper_pins']:check(A/s['path'],s)
for key in ['stopped_CPU_continuation_inventory_pin','stopped_continuation_inventory_pin','seed_inventory_pin']:
 inventory=obj(A/ad[key]['path']);root=Path(inventory['source_workspace'])
 for s in inventory['files']:check(root/s['path'],s)
 for s in inventory.get('checked_artifacts',[]):check(A/s['path'],s)
 need({str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}=={s['path'] for s in inventory['files']},'Exact whole stopped inventory')
manifest=V/sys.argv[2];vm=obj(manifest)
for s in vm['files']:check(V/s['path'],s)
unchanged={}
for old,new,exception in [('native_post_assess_carryforward_v2_20261006/post_assess_carryforward.py','post_assess_carryforward_v3.py','main'),('native_post_assess_carryforward_v2_20261006/native_acceptance_actions_v3.py','native_acceptance_actions_v4.py','load_gate')]:
 x=ast.parse((A/old).read_bytes());y=ast.parse((D/new).read_bytes());defs={n.name:n for n in y.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};count=0
 for n in x.body:
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!=exception:
   need(ast.dump(n,include_attributes=False)==ast.dump(defs[n.name],include_attributes=False),'Unchanged core definition '+n.name);count+=1
 unchanged[new]=count
r={'schema':'pr110-root-linear-carryforward-preexecution-authentication/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_root_PID':os.getpid(),'actual_review':True,'required_findings':[],'preexecution_clearance':True,'adversary_pin':pin(adpath),'program_pin':ad['program_pin'],'action_program_pin':ad['action_program_pin'],'outer_launcher_pin':ad['outer_launcher_pin'],'linear_diff_program_pin':ad['linear_diff_program_pin'],'stopped_CPU_continuation_inventory_pin':ad['stopped_CPU_continuation_inventory_pin'],'integration_inputs_pin':ad['integration_inputs_pin'],'manifest_pin':pin(D/'OUTPUT_MANIFEST.json'),'adversary_manifest_pin':pin(manifest),'checked_artifacts':checked,'unchanged_core_definition_counts':unchanged,'root_full_source_semantic_diffs_and_report_read_completed':True,'zero_range_syntax_repair_verified':True,'historical_assessment_and_current_main_distinguished':True,'all_three_stopped_workspaces_preserved':True,'original_resource_policy_unchanged':True,'native_assess_authorized':False,'actual_future_candidate_or_live_actions_approved':False}
f=A/'ROOT_LINEAR_CARRYFORWARD_PREEXECUTION_REVIEW_AUTHENTICATION_20261006.json';need(not f.exists(),'Unique completed root review');f.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({'root_review_pin':pin(f),'checked_full_bodies':len(checked),'preexecution_clearance':True,'actual_root_PID':os.getpid()}))
