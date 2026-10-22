"""Fresh known-PR-reference counterexample through unmodified full production main."""
from pathlib import Path
import hashlib,json,sys,datetime
V=Path(__file__).resolve().parent;C=V/'private/packet_copy'
source=(C/'actual_main_controls_v03.py').read_text();marker='# Exhaustive finite known-family matrix; each case invokes actual fullmain.'
prefix=source.split(marker)[0]
if source.count(marker)!=1 or prefix.count("'v03_world_'")!=1:raise RuntimeError('Fixture marker drift')
prefix=prefix.replace("'v03_world_'","'fresh_pr_reference_world_'")
g={'__file__':str(C/'actual_main_controls_v03.py'),'__name__':'_pr_reference_fixture'}
exec(compile(prefix,str(C/'actual_main_controls_v03.py'),'exec'),g)
ParentWorld=g['World']
class KnownPRWorld(ParentWorld):
 def __init__(self,name,issue=None,injected=None):
  super().__init__(name,issue,injected)
  if issue=='known_pr':
   self.rows.append(['Every finite acyclic quiver of wild representation type admits uniform expansion for a suitable slope','','','Earlier solution audited in '+injected+'.'])
g['World']=KnownPRWorld
results=[]
for name,ref in [('short_hash','PR #1007'),('short_no_hash','PR1007'),('expanded_words','pull request 1007'),('url_control','https://github.com/AlecKriebel/Math/pull/1007')]:
 r=g['execute']('known_pr_'+name,'known_pr',injected=ref);r['existing_row_pr_reference']=ref
 g['check'](r['all_publication_logic_executed'],'Not full publication/PR gates')
 if name=='url_control':g['check'](r['write_attempts']==0 and not r['case_exists'] and not r['receipt_exists'] and 'New/unreconciled' in r['error'],'Recognized URL positive control failed')
 else:g['check'](r['write_attempts']==1 and r['case_exists'] and r['receipt_exists'] and r['error'] is None,'Missing-PR lead counterexample changed')
 results.append(r);print(name,r['write_attempts'],r['receipt_exists'],flush=True)
mode='OO' if sys.flags.optimize==2 else 'O' if sys.flags.optimize else 'normal'
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REPRODUCED_KNOWN_PR_REFERENCE_DUPLICATE_GUARD_GAP','optimization':sys.flags.optimize,'source_plan_sha256':g['runner'].PLAN_SHA,'source_runner_sha256':hashlib.sha256((C/'append_reviewed_rows.py').read_bytes()).hexdigest(),'source_core_sha256':g['runner'].CORE_SHA,'own_constructed_existing_row_A':'Every finite acyclic quiver of wild representation type admits uniform expansion for a suitable slope','own_constructed_existing_row_C':'','interpretation':'This is a plausible incomplete row for the exact known PR/result; it requires reconciliation instead of another row. Only external sheet responses differ. No raw private old cells disclosed.','results':results,'real_service_calls':0,'real_service_writes':0}
(V/('PR_REFERENCE_CONTROLS_'+mode+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'mode':mode,'full_main_cases':len(results)}))
