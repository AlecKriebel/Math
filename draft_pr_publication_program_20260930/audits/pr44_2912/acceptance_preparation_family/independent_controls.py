"""Handwritten private controls. Production is read/tokenized as text, never imported/compiled/run."""
from pathlib import Path, PurePosixPath
import copy
import datetime as dt
import hashlib
import io
import json
import math
import os
import re
import stat
import subprocess
import tokenize

H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3];C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def demand(ok,message):
    if not ok:raise ValueError(message)
def equal(a,b):
    return type(a) is type(b) and (a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def parse(raw):
    def pairs(rows):
        o={}
        for k,v in rows:demand(k not in o,'Duplicate JSON');o[k]=v
        return o
    def floating(s):
        v=float(s);demand(math.isfinite(v),'Nonfinite decoded float');return v
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite constant')))
def load(p):return parse(p.read_bytes())
def canonical(n):
    demand(type(n) is str and n and '\\' not in n and '\0' not in n,'Unsafe name')
    p=PurePosixPath(n);demand(not p.is_absolute() and p.as_posix()==n and not set(p.parts).intersection({'.','..','.git','__pycache__'}),'Escaping/noncanonical path');return n
def regular(base,n):
    canonical(n);p=base/n;demand(base.is_dir() and not base.is_symlink() and p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(base.resolve()),'Regular bound file')
    for q in p.parents:
        if q==base:break
        demand(not q.is_symlink(),'Symlink ancestor')
    return p
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def bound(base,z):
    canonical(z['path']);demand(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed row')
    raw=regular(base,z['path']).read_bytes();demand(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire bound body');return raw
def closure(base,name,expectedsha,count):
    p=regular(base,name);raw=p.read_bytes();demand(sha(raw)==expectedsha,'Actual closed manifest');o=parse(raw)
    demand(o['self_excluded']==[name] and type(o['files_count']) is int and o['files_count']==count and len(o['files'])==count,'Literal self/count')
    names=set()
    for z in o['files']:
        demand(z['path'] not in names and z['path']!=name,'Duplicate/self row');names.add(z['path']);bound(base,z)
    expected=names|{name};actual=set();dirs=set()
    for p in base.rglob('*'):
        n=p.relative_to(base).as_posix();canonical(n);demand(not p.is_symlink() and (p.is_file() or p.is_dir()),'Special topology')
        if p.is_file():actual.add(n);demand(stat.S_IMODE(p.stat().st_mode)==0o444,'Full0444 mode')
        else:dirs.add(n)
    expected_dirs={q.as_posix() for n in expected for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    demand(actual==expected and dirs==expected_dirs,'Entire recursive topology')
    return o
def capture_read(folder):
    o=load(folder/'CAPTURE.json');demand(o['actual_execution'] is True and o['completed'] is True and type(o['pid']) is int and o['pid']>0,'Actual PID')
    demand(type(o['exit_code']) is int and o['exit_code']==0 and o['status']=='PASS','Actual completed capture')
    for k in ['stdout','stderr']:bound(folder,o[k])
    pre=load(folder/'PRELAUNCH.json');demand(equal(pre,o['prelaunch']),'Whole prelaunch copy')
    demand(sha((folder/'PRELAUNCH_SOURCE.py').read_bytes())==pre['source_sha256'] and sha((folder/'PRELAUNCH_OPERATOR.py').read_bytes())==pre['operator_sha256'],'Exact prelaunch fullsources')
    demand(o['source_unchanged'] is True and o['operator_unchanged'] is True and pre['production_operations_authorized'] is False,'Own operation source scope')
    return o
def native():
    return [pin(R/z['path']) for z in load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files']]

def main():
    checks=0;negative=[];queries=[];before=native()
    gitdir=H/'OWN_READONLY_GIT';gitdir.mkdir(exist_ok=False)
    def git(*tail):
        idx=len(queries);argv=['git',*tail];start=utc();proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=proc.communicate();finish=utc()
        op=gitdir/str(idx);op.mkdir()
        (op/'stdout.bin').write_bytes(out);(op/'stderr.bin').write_bytes(err)
        rec={'schema':'pr44-source-private-actual-readonly-Git/v1','operator_pid':os.getpid(),'pid':proc.pid,'argv':argv,'cwd':str(R),'started_utc':start,'finished_utc':finish,'stdin_supplied':False,'actual_execution':True,'completed':True,'exit_code':proc.returncode,'stdout':pin(op/'stdout.bin'),'stderr':pin(op/'stderr.bin')}
        (op/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n');queries.append(rec);demand(proc.returncode==0 and not err,'Read-only Git query failed');return out
    demand(git('branch','--show-current')==b'main\n','Stay main');head=git('rev-parse','HEAD')
    current=closure(C,'MANIFEST.json','169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0',430);checks+=431
    whole=closure(W,'SELF_MANIFEST.json','ea6416b54945bf80d0a706cf878c8de707464ddcdaea66ae0e812868ff547c9f',96);checks+=97
    dep=load(C/'CURRENT_DEPENDENCIES.json');demand(len(dep['files'])==369 and sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())=='2c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18','Complete actual dependencies')
    for z in dep['files']:bound(A,z);checks+=1
    inputs=load(H/'INPUT_BINDINGS.json')
    for z in inputs['pins'].values():bound(R,z);checks+=1
    for k in ['closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection','previous_mirror','previous_post','previous_root_post']:bound(R,inputs[k]);checks+=1
    frozen=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');demand(frozen['current_head']=='2b9d0234b1396fa84c4b34055b5e8e14c873588b','Frozen epoch')
    dated={z['path']:z for z in frozen['files']};historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    foreign=load(W/'INDIVIDUAL_INPUTS.json')['files'];demand(len(foreign)==964 and len({z['path'] for z in foreign})==964,'Complete964 identities')
    demand(not historical.intersection(z['path'] for z in foreign),'Dated four excluded from liveforeign964')
    for z in foreign:demand(z['excluded_from_family_authorship'] is True,'Individual exclusion');bound(R,z);checks+=1
    for n in sorted(historical):
        entries=git('ls-tree','-z',frozen['current_head'],'--',n).decode().split('\0');demand(len(entries)==2 and entries[-1]=='','One immutable Git row');fields,literal=entries[0].split('\t');mode,kind,blob=fields.split();demand(mode=='100644' and kind=='blob' and literal==n,'Exact immutable Git mode')
        raw=git('show',frozen['current_head']+':'+n);demand(len(raw)==dated[n]['bytes'] and sha(raw)==dated[n]['sha256'],'Entire immutable frozen native4');checks+=2
    actual43=R/inputs['previous_root_post']['path'];root43=load(actual43);post43=load(R/inputs['previous_post']['path']);mirror43=load(R/inputs['previous_mirror']['path'])
    demand(equal(root43['entire_post'],post43) and root43['schema']=='pr43-root-complete-actual-post-inspection/v1','Whole genuine actual43 ROOT schema')
    demand(post43['targets']==34 and type(post43['targets']) is int and post43['consumed_substantive_turns']==41 and post43['primary_acceptances']==33 and post43['merge_commit']=='c60255489a342fae02c0acf3d1026255b47be3d1' and post43['merge_tree']=='fdc2bb213905051a430d24e13afb20e54fa9106a','Actual43 predecessor counts/head/tree')
    demand(len(mirror43['entries'])==33 and len(mirror43['duplicate_mirrors'])==1 and mirror43['required_completed_prs']==sorted(z['pr'] for z in mirror43['entries']),'Entire actual43 mirror accounting')
    c43=load(actual43.parent/'root_pr43_complete_actual_post_inspection_capture/CAPTURE.json');demand(c43['pid']==77832 and c43['exit_code']==0 and c43['actual_execution'] is True and c43['completed'] is True,'Actual43 genuine child77832')
    for k in ['stdout','stderr']:bound(actual43.parent/'root_pr43_complete_actual_post_inspection_capture',c43[k])
    out43=parse((actual43.parent/'root_pr43_complete_actual_post_inspection_capture/stdout.bin').read_bytes());demand(out43['inspection']==inputs['previous_root_post'] and out43['status']=='PASS_COMPLETE_ACTUAL_ROOT_POST_INSPECTION','Entire actual43 output binding');checks+=8
    root44=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');demand(equal(root44,load(H/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and equal(root44['complete_VERDICT_object'],load(W/'VERDICT.json')),'Whole exact actual44 ROOT read')
    expected=[]
    for n in sorted(historical):expected.extend([['git','ls-tree',frozen['current_head'],'--',n],['git','show',frozen['current_head']+':'+n]])
    demand([z['argv'] for z in root44['complete_dated_git_captures']]==expected and root44['direct_four_independent_ROOT_Git_checks_completed'] is True,'Eight exact ROOT directcapture commands')
    for z in root44['complete_dated_git_captures']:
        demand(z['actual_execution'] is True and z['completed'] is True and z['exit_code']==0 and type(z['pid']) is int and z['pid']>0 and z['operator_pid']==1084,'Genuine entire ROOT query metadata')
        for k in ['stdout','stderr']:bound(R,z[k]);checks+=1
    for folder in ['AUTHORING_ACTUAL_CAPTURE','SOURCE_REPAIR_ACTUAL_CAPTURE']:capture_read(H/folder);checks+=1
    # Lexing only: this creates no executable code object and invokes no production
    # import, compile, AST compiler, helper or application command.
    production=['pr44_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','capture_root_final_operation.py']
    lexical=[]
    for n in production:
        tokens=list(tokenize.tokenize(io.BytesIO((H/n).read_bytes()).readline))
        demand(not [t for t in tokens if t.type==tokenize.ERRORTOKEN and t.string.strip()],'Production source lexical error')
        stack=[]
        for t in tokens:
            if t.type==tokenize.OP and t.string in '([{':stack.append(t.string)
            elif t.type==tokenize.OP and t.string in ')]}':demand(stack and {'(':')','[':']','{':'}'}[stack.pop()]==t.string,'Unbalanced delimiter')
        demand(not stack,'Unclosed delimiter');lexical.append({'source':n,'tokens':len(tokens),'lexical_only':True});checks+=1
    g=(H/'pr44_guards.py').read_text();i=(H/'integrate_reviewed_partial.py').read_text();m=(H/'state_mirror_reconciliation.py').read_text();p=(H/'verify_post_acceptance.py').read_text()
    scope="Incremental present accepted primary PR44 standard partial; original2/5, no new proof turn or historical reconstruction."
    demand('scope='+repr(scope) in g and 'scope='+repr(scope) in m,'M2 literal complete scope identical')
    demand("snapshot_manifest_v2.json" in i and "snapshot_manifest.json" not in i and "snapshot_manifest_v2.json" in g,'M1 exact original manifest filename')
    demand('10.4064' not in p and "'full_target_resolved_in_prior_published_literature':False" in p and "'prior_publication_doi':None" in p,'No inherited43 scientific resolution/DOI')
    for term in ['specified abstract group-pair','degree-one','equal-full-triple','UNSOLVED']:demand(term in i,'Present full gap/scope qualification')
    draft=load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');plan=load(H/'DRAFT_FINAL_PLAN.json');scientific=load(H/'SCIENTIFIC_SCOPE.json')
    refs=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    demand(draft['created_utc'] is None and all(draft[k] is None for k in refs),'No fake typed ROOT reference/time')
    flags=['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','root_actual_PR43_predecessor_read_completed','independent_whole_current_pass']
    demand(all(draft[k] is False and plan[k] is False for k in flags) and plan['partial_valid'] is None and plan['immutable_evidence_references']==[],'All future completed fields remain unset')
    demand(scientific['original_substantive_attempts']==2 and type(scientific['original_substantive_attempts']) is int and scientific['new_substantive_attempts']==0 and scientific['full_problem_solved'] is False and len(scientific['exact_remaining_gaps'])==2,'Exact scoped original2,new0 two gaps')
    ledger=regular(C,'turns.jsonl').read_bytes();entries=[parse(line) for line in ledger.splitlines()];demand(len(entries)==2 and [x['turn'] for x in entries]==[1,2] and all(x['outcome']=='stalled' for x in entries),'Actual original two-turn ledger')
    def ledger_guard(raw,used,limit):demand(type(used) is int and type(limit) is int and used==2 and limit==5 and type(raw) is bytes and raw==ledger,'Exact full ledger guard')
    ledger_guard(ledger,2,5);checks+=1
    mutants=[('empty',b'',2,5),('whitespace_only',b'\n',2,5),('invented_JSONL',b'{"turn":1}\n',2,5),('bool_used',ledger,True,5),('wrong_used',ledger,1,5),('wrong_limit',ledger,2,4)]
    for label,raw,used,limit in mutants:
        try:ledger_guard(raw,used,limit)
        except ValueError:negative.append(label)
        else:raise ValueError('Handwritten control accepted mutant')
    for raw in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:
        try:parse(raw)
        except ValueError:negative.append('strict_JSON_'+raw.decode())
        else:raise ValueError('Strict JSON control accepted mutant')
    for bad in ['../escape','/absolute','x/../y','x//y','x/./y','x\\y','.git/config','__pycache__/x']:
        try:canonical(bad)
        except ValueError:negative.append('path_'+bad)
        else:raise ValueError('Path control accepted mutant')
    demand(not equal(1,True) and not equal(1,1.0) and not equal({'x':1},{'x':True}) and not equal({'x':None},{'x':False}),'Recursive exact types')
    probes=H/'OWN_PRIVATE_MODE_PROBES';probes.mkdir(exist_ok=False);observations=[]
    for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o777]:
        probe=probes/('mode_'+oct(mode));probe.write_bytes(b'Own private full-permission probe.\n');probe.chmod(mode);actual=stat.S_IMODE(probe.stat().st_mode);demand(actual==mode,'Actual full mode observation');observations.append({'path':probe.relative_to(H).as_posix(),'actual_mode_before_closure':actual,'accepted_by_literal0444_predicate':actual==0o444})
    for mode in range(0o10000):demand((mode==0o444)==(stat.S_IMODE(mode)==0o444),'All4096 complete mode controls');checks+=1
    queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();lines=queue.decode().splitlines(keepends=True);matched=[x for x in lines if len(x.split('|'))==14 and x.split('|')[2].strip()=='2912 / KP-4.36'];demand(len(matched)==1,'Unique current queue primary');oldrow=matched[0];cells=oldrow.split('|');demand(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Fresh current row before acceptance')
    oldcells=copy.deepcopy(cells);cells[8]=' unsolved ';cells[9]=' 2/5 ';cells[11]=' Standard meridional duality kernel, sufficient degree-one pair-map criterion and conditional integral kernel for the specified abstract group-pair; unmarked full2type pair-map and actual equal-full-triple exterior realization gaps remain. [Accepted scoped UNSOLVED partial](attempts/2912/ACCEPTANCE.md). Original2/5,new0,audit0; no novelty/paper/new DOI/tracker. '
    newrow='|'.join(cells);demand([i for i,(x,y) in enumerate(zip(oldcells,cells)) if x!=y]==[8,9,11] and oldcells[10]==cells[10] and oldcells[12]==cells[12],'Exact Status/Turns/Findings only; ChatDOI retained');prospective=queue.replace(oldrow.encode(),newrow.encode(),1);demand(prospective.replace(newrow.encode(),oldrow.encode(),1)==queue,'Entire queue inverse preservation');checks+=1
    inventory=load(R/'draft_pr_publication_program_20260930/inventory.json');state=load(R/'unsolved_math_prioritization/state.json');demand(len(state)==34 and '2912' not in state and sum(v['turns_used'] for v in state.values())==41,'Actual before34/41');demand(len(inventory['items'])==180 and inventory['completed_count']==33 and inventory['current_pr']==44,'Actual full before inventory')
    proposed=copy.deepcopy(inventory);chosen=next(x for x in proposed['items'] if x['number']==44);demand(chosen['headRefOid']=='c772dc5b851ec91da9d46d534577609e5d3ca389','Actual inventory original head')
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',original_attempts='2/5',cumulative_attempts='2/5',new_substantive_attempts=0,paper_or_new_doi_or_tracker=False);proposed.update(completed_count=34,current_pr=45,program_completion_estimate_percent=34/180*100,completion_estimate_percent=34/180*100)
    demand(all(equal(x,y) for x,y in zip(inventory['items'],proposed['items']) if x['number']!=44),'Entire179 unrelated inventory entries unchanged')
    (H/'PROSPECTIVE_QUEUE_CONTROL.json').write_text(json.dumps({'source_only':True,'executed_native_write':False,'allowed_named_changes':['Status','Turns','Findings'],'row_before':oldrow,'row_prospective':newrow,'whole_before_sha256':sha(queue),'whole_prospective_sha256':sha(prospective),'all_other_bytes_and_Chat_DOI_preserved':True},indent=2)+'\n')
    demand(native()==before and git('rev-parse','HEAD')==head,'Whole native13/HEAD unchanged by own controls')
    result={'schema':'pr44-independent-handwritten-source-controls/v1','status':'PASS_PRIVATE_CONTROLS_ONLY','actual_control_pid':os.getpid(),'utc':utc(),'checks':checks,'rejected_hostile_cases':negative,'actual_permission_observations':observations,'lexical_source_checks':lexical,'production_imported_compiled_executed':False,'production_runtime_success_claimed':False,'native13_unchanged':True,'main_HEAD_unchanged':True,'complete_readonly_Git_queries':queries,'actual43_complete_post_capture_pid':77832,'actual44_direct_four_operator_pid':1084,'closure_counts':{'candidate':430,'dependencies':369,'whole':96,'foreign':964},'source_preparation_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0}
    (H/'OWN_CONTROL_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'actual_control_pid':os.getpid(),'checks':checks,'hostile_rejections':len(negative),'production_executed':False,'readonly_Git_queries':len(queries),'native13_unchanged':True},sort_keys=True))
if __name__=='__main__':main()
