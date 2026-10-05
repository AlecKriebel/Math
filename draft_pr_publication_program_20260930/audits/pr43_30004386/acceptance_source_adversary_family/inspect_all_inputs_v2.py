"""Independent full-body manifest/source review; no candidate imports or execution."""
from pathlib import Path, PurePosixPath
import ast
import datetime as dt
import hashlib
import json
import math
import os
import stat
import subprocess

H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];S=A/'acceptance_preparation_family';C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
PIN='4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9'
HIST='c61dc0cb572de281b871264819c8b80d647d0373'
historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
reads=[];checks=0;git_records=[]
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def demand(v,m):
    global checks
    checks+=1
    if not v:raise AssertionError(m)
def typed(x,y):return type(x) is type(y) and (set(x)==set(y) and all(typed(x[k],y[k]) for k in x) if type(x) is dict else len(x)==len(y) and all(typed(a,b) for a,b in zip(x,y)) if type(x) is list else x==y)
def parse(raw):
    def pairs(z):
        d={}
        for k,v in z:demand(k not in d,'duplicate JSON key');d[k]=v
        return d
    def floating(v):
        f=float(v);demand(math.isfinite(f),'finite floating point');return f
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def canonical(n):
    demand(type(n) is str and n and '\\' not in n and '\0' not in n,'relative literal string')
    p=PurePosixPath(n);demand(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'canonical relative')
    return n
def regular(p):
    demand(p.is_file() and not p.is_symlink(),'real regular file '+str(p))
    for q in p.parents:demand(not q.is_symlink(),'no symlink ancestor')
    return p
def read(p,role):
    raw=regular(p).read_bytes();reads.append({'path':str(p),'role':role,'bytes':len(raw),'sha256':sha(raw),'full_worktree_mode':stat.S_IMODE(p.stat().st_mode)})
    if p.suffix=='.json':parse(raw)
    if p.suffix=='.jsonl':
        demand(not raw or raw.endswith(b'\n'),'whole JSONL complete')
        for line in raw.splitlines():parse(line)
    return raw
def rows(values):
    if type(values) is dict:values=[{'path':k,**v} for k,v in values.items()]
    demand(type(values) is list,'list rows');out=[]
    for z in values:
        canonical(z['path']);n=z.get('bytes',z.get('size'))
        demand(type(n) is int and n>=0,'typed byte count')
        demand(type(z['sha256']) is str and len(z['sha256'])==64 and all(c in '0123456789abcdef' for c in z['sha256']),'hex hash')
        if 'bytes'in z and 'size'in z:demand(typed(z['bytes'],z['size']),'no conflicting size aliases')
        out.append({**z,'bytes':n})
    demand(len({z['path'] for z in out})==len(out),'unique rows');return out
def full(base,z,role,mode=None):
    raw=read(base/z['path'],role);demand(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'complete hash/size '+z['path'])
    if mode is not None:demand(stat.S_IMODE((base/z['path']).stat().st_mode)==mode,'exact mode '+z['path'])
    return raw
def exact(base,names):
    names=set(names);files=set();dirs=set()
    for p in base.rglob('*'):
        demand(not p.is_symlink() and (p.is_file() or p.is_dir()),'ordinary topology')
        (files if p.is_file() else dirs).add(p.relative_to(base).as_posix())
    expected={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
    demand(files==names and dirs==expected,'exact files plus dirs topology')
def manifest(base,name,pin,count):
    raw=read(base/name,'manifest');demand(sha(raw)==pin,'exact manifest pin');m=parse(raw)
    rr=rows(m['files']);demand(len(rr)==count and m.get('files_count',m.get('member_count',count))==count,'member count')
    demand(m.get('self_excluded',m.get('excluded'))==[name],'literal self exclusion')
    for z in rr:full(base,z,'full closure member',0o444)
    demand(stat.S_IMODE((base/name).stat().st_mode)==0o444,'manifest full mode');exact(base,{z['path'] for z in rr}|{name});return m
def git(*args):
    n='v2_git_'+str(len(git_records)+1);d=H/n;d.mkdir();argv=['git',*args]
    rec={'argv':argv,'cwd':str(R),'started_utc':now()}
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err=p.communicate();rec.update(actual_execution=True,pid=p.pid,completed=True,exit_code=p.returncode,finished_utc=now())
    for ch,raw in [('stdout',out),('stderr',err)]:
        (d/(ch+'.bin')).write_bytes(raw);rec[ch]={'path':ch+'.bin','bytes':len(raw),'sha256':sha(raw)}
    (d/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n');git_records.append(rec);demand(p.returncode==0,'read-only Git success');return out
def foreign_path(literal):
    demand(type(literal) is str and literal.startswith(str(R)+'/') and '\\'not in literal and '\0'not in literal,'absolute repo literal')
    q=R;parts=literal[len(str(R))+1:].split('/')
    for i,part in enumerate(parts):
        demand(part and part not in ('.git','__pycache__'),'foreign component')
        demand(q.is_dir() and not q.is_symlink(),'real prefix')
        if part=='.':continue
        if part=='..':demand(q!=R,'no escape prefix');q=q.parent
        else:q=q/part
        demand(q.exists() and not q.is_symlink(),'existing no-symlink component')
        demand(q==R or q.is_relative_to(R),'all prefix containment')
        if i<len(parts)-1:demand(q.is_dir(),'intermediate directory')
    regular(q);demand(q.resolve(strict=True)==q and q!=R,'strict canonical foreign file');return q
def main():
    started=now();head_before=git('rev-parse','HEAD').decode().strip()
    prep=manifest(S,'PREPARATION_MANIFEST.json',PIN,108)
    demand(prep['source_only'] is True and prep['proposed_helpers_imported_compiled_executed'] is False,'source only')
    candidate=manifest(C,'MANIFEST.json','4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14',347)
    deps=parse(read(C/'CURRENT_DEPENDENCIES.json','dependencies'));demand(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())=='4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e','dep hash')
    dr=rows(deps['files']);demand(len(dr)==274,'274 dependencies')
    for z in dr:full(A,z,'individual dependency')
    inputs=parse(read(S/'INPUT_BINDINGS.json','source inputs'))
    for ref in inputs['pins'].values():full(R,ref,'source binding')
    for key in ('closed_PR42_V2_source_context','closed_root_whole_inspection','closed_whole_manifest','closed_whole_report','closed_whole_result','root_capture_operator'):full(R,inputs[key],'closed named input')
    whole=manifest(W,'SELF_MANIFEST.json','af80fc4d9ce1bb3b282b193f8dbe3dfdd873184f7ffb1143c6b027419f6a0c2d',30)
    fm=whole['external_individually_excluded_inputs'];demand(len(fm)==756 and len({z['path'] for z in fm})==756,'756 literal foreign rows')
    frozen=parse(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json','dated freeze native13'));fn={z['path']:z for z in frozen['files']};historic=[]
    for z in fm:
        p=foreign_path(z['path']);n=p.relative_to(R).as_posix()
        if n in historical:
            ent=git('ls-tree','-z',HIST,'--',n).decode().split('\0');demand(len(ent)==2 and ent[-1]=='','one historical entry')
            fields,literal=ent[0].split('\t');mode,kind,blob=fields.split();demand(mode=='100644' and kind=='blob' and literal==n,'historical regular blob')
            raw=git('show',HIST+':'+n);demand(fn[n]['bytes']==z['bytes'] and fn[n]['sha256']==z['sha256'],'same historical freeze pin');historic.append(n)
            reads.append({'path':z['path'],'role':'dated historical complete immutable Git body, not current authority','bytes':len(raw),'sha256':sha(raw),'git_head':HIST})
        else:raw=read(p,'individual foreign whole body')
        demand(type(z['bytes'])is int and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'entire foreign hash')
    demand(set(historic)==historical and len(historic)==4,'exact four historical bodies')
    snap=parse(read(A/'snapshot_manifest.json','original snapshot'));sr=rows(snap['files']);demand(len(sr)==16 and len(snap['changed_paths'])==17,'original16/17')
    for z in sr:
        original=full(A/'source_snapshot',z,'original16')
        demand(original==read(C/'original_archive'/z['path'],'candidate original archive'),'original archive exact')
    demand((A/'source_snapshot'/'turns.jsonl').read_bytes()==b'','empty0 original ledger')
    demand(typed(parse((A/'pinned_prior_report.json').read_bytes()),{}),'saved{} fallback')
    root=parse((A/'ROOT_WHOLE_CURRENT_REVIEW.json').read_bytes());v=parse((W/'VERDICT.json').read_bytes())
    demand(typed(root['complete_VERDICT_object'],v),'whole root entire verdict')
    demand(v['justified_status']=='already_solved' and v['full_problem_solved_by_project'] is False and v['prior_publication_doi']=='10.4064/sm210413-16-9','credited scope')
    draft=parse((S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json').read_bytes());demand(draft['created_utc']is None and draft['root_acceptance_source_review_completed']is False and draft['root_actual_PR42_predecessor_read_completed']is False,'false draft flags')
    demand(all(draft[x]is None for x in ('whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post')),'draft null refs')
    demand(all(x is None for x in inputs['required_future_PR42_predecessor'].values()),'no invented future predecessor')
    ast_records=[]
    for z in prep['files']:
        if z['path'].endswith('.py'):
            raw=(S/z['path']).read_bytes()
            try:tree=ast.parse(raw,filename=z['path'])
            except SyntaxError as error:
                demand(z['path'].startswith('preserved_') and z['path'].endswith('/integrate_reviewed_partial.py'),'Only explicitly archived invalid drafting literals may fail AST parsing')
                ast_records.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'archived_invalid_drafting_literal':True,'syntax_error':str(error),'no_bytecode_or_execution':True})
            else:ast_records.append({'path':z['path'],'bytes':len(raw),'sha256':sha(raw),'parse_only_no_code_object':True,'functions':[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]})
    captures=[]
    for z in prep['files']:
        if z['path'].endswith('/CAPTURE.json'):
            p=S/z['path'];cap=parse(p.read_bytes())
            demand(type(cap.get('pid'))is int and cap['pid']>0 and cap.get('actual_execution')is True,'actual source operation PID')
            for channel in ('stdout','stderr'):
                q=cap[channel];raw=read(p.parent/q['path'],'source actual stream');demand(len(raw)==q['bytes'] and sha(raw)==q['sha256'],'actual stream whole hash')
            captures.append({'path':z['path'],'pid':cap['pid'],'exit_code':cap['exit_code'],'started_utc':cap['started_utc'],'finished_utc':cap['finished_utc'],'stderr_full_when_failed':(p.parent/cap['stderr']['path']).read_bytes().decode(errors='replace')if cap['exit_code'] else None})
    head_after=git('rev-parse','HEAD').decode().strip()
    result={'schema':'PR43_NEW_ACCEPTANCE_SOURCE_ADVERSARY_FULL_INPUT_READING_v1','started_utc':started,'finished_utc':now(),'actual_pid':os.getpid(),'source_only':True,'proposed_sources_imported_compiled_executed':False,'checks':checks,'full_reads':reads,'full_read_count':len(reads),'whole_read_bytes':sum(z['bytes']for z in reads),'preparation_manifest_sha256':PIN,'preparation_members':108,'candidate_members':347,'dependencies':274,'whole_members':30,'foreign_identities':756,'historical_git_body_count':4,'original_files':16,'ast_parse_only_records':ast_records,'source_actual_captures':captures,'read_only_git_queries':git_records,'main_head_before':head_before,'main_head_after':head_after,'heads_unchanged_during_this_reading':head_before==head_after,'historical_native_is_not_current_authority':True,'future_execution_approved':False}
    (H/'FULL_INPUT_READING.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('full_reads','ast_parse_only_records','read_only_git_queries','source_actual_captures')},indent=2))
if __name__=='__main__':main()
