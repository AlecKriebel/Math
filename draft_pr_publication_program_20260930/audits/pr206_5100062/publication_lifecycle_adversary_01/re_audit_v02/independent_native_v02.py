"""Synthetic native-tree/commit/changed-scope controls and bounded expansion probe."""
from pathlib import Path
import copy, hashlib, json, sys, types
HERE=Path(__file__).absolute().parent
path=HERE/'sealed_source'/'support206.py';raw=path.read_bytes()
S=types.ModuleType('native_boundary_support');S.__file__=str(path);exec(compile(raw,str(path),'exec'),S.__dict__)
R=[]
def run(name,fn,reject=False,predicate=None):
    try:
        value=fn();ok=not reject and (predicate is None or bool(predicate(value)));error=None;observed='accepted'
    except Exception as e:ok=reject;error=type(e).__name__+': '+str(e);observed='rejected'
    R.append({'case':name,'expected':'reject' if reject else 'accept','observed':observed,'pass':ok,'error':error})
def tree(rows):
    items=[]
    for row in rows:
        key=row['path'].encode()+(b'/' if row['type']=='tree' else b'')
        payload=row['mode'].lstrip('0').encode()+b' '+row['path'].encode()+b'\0'+bytes.fromhex(row['sha'])
        items.append((key,payload))
    raw=b''.join(payload for key,payload in sorted(items))
    return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
class H:
    def __init__(self,rows,objects=None):
        self.rows=copy.deepcopy(rows);self.root=tree(rows);self.objects=objects or {};self.calls=0
    def lookup(self,oid,prefix):return ('040000','tree',self.root)
    def api(self,endpoint):
        self.calls+=1
        if self.calls>200:raise RuntimeError('Independent hard API-call bound')
        oid=endpoint.split('/')[-1];rows=self.rows if oid==self.root else self.objects[oid]
        return {'sha':oid,'truncated':False,'tree':copy.deepcopy(rows)}
rows=[{'path':f'proof{i}.md','mode':'100644','type':'blob','sha':S.bpin(f'synthetic{i}'.encode())['git_blob']} for i in range(31)]
h=H(rows)
run('native_tree_exact31',lambda:S.native_leaves(h,'a'*40,S.NATIVE),predicate=lambda v:len(v)==31)
for name,mutate in (
    ('symlink',lambda r:r[0].update(mode='120000')),
    ('executable_mode',lambda r:r[0].update(mode='100755')),
    ('unsafe_name',lambda r:r[0].update(path='../escape')),
    ('duplicate_entry',lambda r:r.append(copy.deepcopy(r[0]))),
):
    bad=copy.deepcopy(rows);mutate(bad);h=H(bad)
    run('native_tree_'+name,lambda h=h:S.native_leaves(h,'a'*40,S.NATIVE),True)
h=H(rows);h.rows[0]['sha']='f'*40
run('native_tree_bad_object_hash',lambda:S.native_leaves(h,'a'*40,S.NATIVE),True)
h=H(rows);original_api=h.api
def truncated(endpoint):r=original_api(endpoint);r['truncated']=True;return r
h.api=truncated
run('native_tree_truncated',lambda:S.native_leaves(h,'a'*40,S.NATIVE),True)

# Exact candidate scope and true two-parent merge, separate from accepted counters.
expected={S.CASE+'synthetic.txt':S.bpin(b'SYNTHETIC')};out={S.CASE+'synthetic.txt':b'SYNTHETIC'}
changes=set(out)
def candidate(phase):
    parent='a'*40;parents=[parent,S.HEAD] if phase=='merge' else [parent]
    prep={'schema':'pr206-lifecycle-preparation-v1','phase':phase,'PR':206,'case_percent':S.PHASES[phase][1],
          'original_head':S.HEAD,'selected_files':copy.deepcopy(expected),'selected_map_sha256':S.digest(expected),
          'overlay_paths':sorted(out),'commit':'b'*40,'tree':'c'*40,'parent_tree':'d'*40,'changed_paths':sorted(changes)}
    commit={'sha':'b'*40,'parents':[{'sha':p} for p in parents],'tree':{'sha':'c'*40},'message':S.message(phase,S.digest(expected))}
    return prep,commit,parents
for phase in S.PHASES:
    p,c,parents=candidate(phase)
    def check(p=p,c=c,parents=parents,phase=phase,actual=changes):
        return S.check_candidate(phase,p,c,'d'*40,expected,out,changes,actual,parents)
    run('candidate_exact_'+phase,check)
    bad=copy.deepcopy(c);bad['parents']=list(reversed(bad['parents'])) if phase=='merge' else bad['parents']+[{'sha':S.HEAD}]
    run('candidate_wrong_parents_'+phase,lambda bad=bad,p=p,parents=parents,phase=phase:S.check_candidate(phase,p,bad,'d'*40,expected,out,changes,changes,parents),True)
    run('candidate_foreign_changed_'+phase,lambda p=p,c=c,parents=parents,phase=phase:S.check_candidate(phase,p,c,'d'*40,expected,out,changes,changes|{S.ALL_NATIVE+'999/FOREIGN.md'},parents),True)
    bad=copy.deepcopy(p);bad['selected_files']={}
    run('candidate_truncated_map_'+phase,lambda bad=bad,c=c,parents=parents,phase=phase:S.check_candidate(phase,bad,c,'d'*40,expected,out,changes,changes,parents),True)

# Valid content-addressed DAG with 61 copies of a500-leaf subtree. Trace only
# result sizes at the source's bound check. No output map or actual tree is saved.
subrows=[{'path':f'leaf{i:03d}','mode':'100644','type':'blob','sha':S.bpin(b'SYNTHETIC')['git_blob']} for i in range(500)]
subtree=tree(subrows)
toprows=[{'path':f'dir{i:03d}','mode':'040000','type':'tree','sha':subtree} for i in range(61)]
h=H(toprows,{subtree:subrows});peak=[0]
def trace(frame,event,arg):
    if event=='line' and frame.f_code.co_filename==str(path) and frame.f_code.co_name=='descend' and frame.f_lineno in (613,628,630,631):
        peak[0]=max(peak[0],len(frame.f_locals['result']))
    return trace
sys.settrace(trace)
try:
    try:S.native_leaves(h,'a'*40,S.NATIVE);expansion_error=None
    except Exception as e:expansion_error=type(e).__name__+': '+str(e)
finally:sys.settrace(None)
expansion={'unique_tree_objects':2,'root_children':61,'subtree_leaves':500,'theoretical_leaves':30500,
           'largest_materialized_map_before_bound_check':peak[0],'declared_MAX_CHANGED':S.MAX_CHANGED,
           'native_GET_calls':h.calls,'exception':expansion_error,
           'interpretation':'Repaired source must stop before allocation exceeds its aggregate budget.'}
outcome={'schema':'pr206-independent-native-boundaries-v1','optimized':bool(sys.flags.optimize),
         'source':S.pin(raw),'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'only_synthetic_native_objects':True,'tests':len(R),'passed':sum(x['pass'] for x in R),
         'failed':sum(not x['pass'] for x in R),'outcomes':R,'bounded_expansion_probe':expansion}
print(json.dumps(outcome,indent=2))
raise SystemExit(bool(outcome['failed']))
