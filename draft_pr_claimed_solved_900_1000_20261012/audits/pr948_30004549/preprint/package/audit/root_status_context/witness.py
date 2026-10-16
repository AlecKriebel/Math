"""Historical exact-code synthetic status-selection witness; no service calls."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012')
A=P/'audits/pr948_30004549'
S=A/'preprint/reviewed_candidates/candidate01/operations'/P.name/'accept_pr948.py'
raw=S.read_bytes();source_pin=hashlib.sha256(raw).hexdigest()
if source_pin!='1f538840a9e3d0ec26270d977960699cfd6155e8706ffa7de3c82854042be563':
    raise ValueError('Externally known historical core pin')
N={'__file__':str(P/'accept_pr948.py'),'__name__':'_historical_scope_witness_'}
exec(compile(raw,str(S),'exec',dont_inherit=True,optimize=0),N)

# An explicit valid commit DAG. The head H never changes. Main D later merges
# the head's ancestor C2. The merge base advances from O to C2.
dag={
    'O':{'parents':[],'tree':{'A':0,'B':0,'misc':0}},
    'D':{'parents':['O'],'tree':{'A':0,'B':0,'misc':1}},
    'C1':{'parents':['O'],'tree':{'A':1,'B':0,'misc':0}},
    'C2':{'parents':['C1'],'tree':{'A':1,'B':1,'misc':0}},
    'H':{'parents':['C2'],'tree':{'A':1,'B':0,'misc':0}},
    'M':{'parents':['D','C2'],'tree':{'A':1,'B':1,'misc':1}},
}
def ancestors(node):
    return {node}.union(*(ancestors(x) for x in dag[node]['parents']))
def mergebase(a,b):
    common=ancestors(a)&ancestors(b)
    maximal=[x for x in common if not any(x!=y and x in ancestors(y) for y in common)]
    if len(maximal)!=1:raise ValueError('Unique merge base required')
    return maximal[0]
def difference(a,b):return sorted(k for k in dag[a]['tree'] if dag[a]['tree'][k]!=dag[b]['tree'][k])
old_base=mergebase('D','H');new_base=mergebase('M','H')
if (old_base,new_base,difference(old_base,'H'),difference(new_base,'H'))!=('O','C2',['A'],['B']):
    raise ValueError('DAG witness')
ids={'A':'1000001','B':'1000002'}
paths={k:'unsolved_math_prioritization/attempts/'+v+'/proof.md' for k,v in ids.items()}
def row(key,status):return '| 1 | '+key+' / SYNTHETIC | Title | 0 | 0 | 0 | 2020 | '+status+' | 4/5 | | | |'
queue=(row(ids['A'],'claimed_solved')+'\n'+row(ids['B'],'unsolved')+'\n').encode()
metadata={'number':952,'state':'OPEN','isDraft':True,'headRefOid':'e'*40,'headRefName':'synthetic-head','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952'}
hidden={'base':'D'};oids={'D':'d'*40,'M':'f'*40};calls=[]
def fake_run(args,*a,**kw):
    if args[:3]==['gh','pr','view']:
        fields=args[args.index('--json')+1].split(',')
        full={**metadata,'baseRefOid':oids[hidden['base']]}
        calls.append({'request':'PR metadata','baseRefOid_requested':'baseRefOid' in fields,'actual_base':hidden['base']})
        return json.dumps({k:full[k] for k in fields})
    if args[:3]!=['gh','api','graphql']:raise AssertionError('Unexpected actual operation')
    query=next(v[6:] for v in args if v.startswith('query='))
    if 'files(first:100' in query:
        calls.append({'request':'changed filenames','baseRefOid_requested':'baseRefOid' in query,'actual_base':'D'})
        node={**metadata,'changedFiles':1,'files':{'nodes':[{'path':paths['A']}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}
        if 'baseRefOid' in query:node['baseRefOid']=oids['D']
        return json.dumps({'data':{'repository':{'pullRequest':node}}})
    if 'object(expression:$expr)' in query:
        calls.append({'request':'immutable QUEUE status only','proof_source_read':False})
        hidden['base']='M' # concurrent main advance after the complete file read
        return json.dumps({'data':{'repository':{'object':{'text':queue.decode(),'isBinary':False,'byteSize':len(queue),'oid':hashlib.sha1(b'blob '+str(len(queue)).encode()+b'\0'+queue).hexdigest()}}}})
    raise AssertionError('Unknown query')
N['run']=fake_run
inventory=[{'number':952,'headRefOid':'c'*40,'entries':[{'id':ids['A']}]}]
skipped,selected=N['gate_next'](inventory)
if skipped or selected['problem_id']!=ids['A'] or selected['status']!='claimed_solved' or hidden['base']!='M':
    raise ValueError('Historical-code result differs')
out={'utc':datetime.now(timezone.utc).isoformat(),'finding_id':'R948-WORKFLOW-ROOT-02','amendment':'BASE_REF_OID_BINDING_AFTER_FULL01','classification':'required','source_core_sha256':source_pin,'synthetic_only':True,'actual_remote_mutations':0,'actual_mathematics_or_other_problem_source_reads':0,'dag':dag,'old_merge_base':old_base,'new_merge_base':new_base,'old_changed_files':[paths['A']],'new_changed_files':[paths['B']],'same_PR_head_and_name_and_file_count':True,'immutable_head_queue_statuses':{ids['A']:'claimed_solved',ids['B']:'unsolved'},'actual_historical_gate_selected':selected,'current_comparison_problem_id':ids['B'],'current_comparison_status':'unsolved','calls':calls,'conclusion':'With a changed initial head, the selector can accept a claimed target from an earlier complete filename comparison even though the unchanged PR head now compares only an unsolved target. Name/head/draft/state/count binding omits the changed base commit. No real retarget or processed excluded PR is alleged.','required_correction':'Bind well-formed baseRefOid in before/after metadata and every changed-file page, in addition to head/name/draft/state and full filename count. Apply the same boundary to the final status-only resweep. Preserve all existing static identity/status exclusions.','primary_documentation':['https://docs.github.com/en/pull-requests/reference/branches','https://docs.github.com/en/graphql/reference/pulls'],'source_inference':'GitHub documents the three-dot merge-base/head comparison and exposes baseRefOid; the finite DAG and actual inert-code witness supply this specific race, rather than claiming a documented real occurrence.'}
target=Path(__file__).with_name('WITNESS.json')
with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'utc':out['utc'],'finding_id':out['finding_id'],'amendment':out['amendment'],'old_unique_target':ids['A'],'current_unique_target':ids['B'],'old_actual_gate_selected':selected['problem_id'],'actual_service_calls':0}))
