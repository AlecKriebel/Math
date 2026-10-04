#!/usr/bin/python3
"""ROOT only after reviewer exits; self-only close, no production import/call."""
import argparse,datetime,hashlib,json,math,os,pathlib,re,stat
F=pathlib.Path(__file__).absolute().parent;H=F.parent/'acceptance_preparation_family_v2';SELF='SELF_MANIFEST.json';MF='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40'
EXPECTED={'fixed_corpus':1,'fixed_corpus_v2':1,'fixed_corpus_v3':0,'ownership_phase':0,'final_capture':0}
def need(v,n):
    if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file');return p.read_bytes()
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate JSON');d[k]=v
        return d
    def floating(s):
        v=float(s);need(math.isfinite(v),'Finite JSON');return v
    def constant(s):raise ValueError('Nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=constant)
def clock(s):
    t=datetime.datetime.fromisoformat(s);need(t.utcoffset()==datetime.timedelta(0),'Aware UTC');return t
def tree():
    need(F==pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr46_30004438/acceptance_source_adversary_family_v2') and not F.is_symlink(),'Exact own family')
    files={};dirs={'.':stat.S_IMODE(F.stat().st_mode)};folded=set()
    for p in F.rglob('*'):
        n=p.relative_to(F).as_posix();need(not p.is_symlink() and n.casefold() not in folded,'No symlink/alias');folded.add(n.casefold())
        if stat.S_ISREG(p.stat().st_mode):files[n]=p
        else:need(stat.S_ISDIR(p.stat().st_mode),'No special member');dirs[n]=stat.S_IMODE(p.stat().st_mode)
    implied={'.'}|{str(q) for n in files for q in pathlib.PurePosixPath(n).parents if str(q)!='.'};need(set(dirs)==implied,'Exact nonempty directory topology');return files,dirs
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);p.add_argument('--expected-verdict-sha256',required=True);a=p.parse_args();need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Checks enabled')
    for value in [a.expected_report_sha256,a.expected_verdict_sha256]:need(re.fullmatch('[0-9a-f]{64}',value) is not None,'Explicit exact SHA')
    need(sha(read(F/'REPORT.md'))==a.expected_report_sha256 and sha(read(F/'VERDICT.json'))==a.expected_verdict_sha256 and not (F/SELF).exists(),'Exact report/verdict and never overwrite closure')
    need(sha(read(H/'PREPARATION_MANIFEST.json'))==MF and stat.S_IMODE((H/'PREPARATION_MANIFEST.json').stat().st_mode)==292,'Actual immutable V2 source pin')
    v=parse(read(F/'VERDICT.json'));need(v['schema']=='pr46-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['preparation_manifest_sha256']==MF and v['mandatory_corrections']==[] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False,'Actual scoped verdict, no future approval')
    captures=[]
    for name,exitcode in sorted(EXPECTED.items()):
        d=F/'captures'/name;c=parse(read(d/'CAPTURE.json'));pre=parse(read(d/'PRELAUNCH.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==exitcode and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False and 'operator_failure' not in c,'Actual retained completed child')
        need(c['status']==('PASS_PRIVATE_SOURCE_ONLY' if exitcode==0 else 'FAILED_PRIVATE_SOURCE_CONTROL_PRESERVED') and c['production_imported_compiled_executed'] is False,'Retained successes and failures')
        need(all(c[k]==pre[k] for k in pre if k!='schema') and sha(read(d/'PRELAUNCH_SOURCE.py'))==pre['source_sha256'] and sha(read(d/'PRELAUNCH_OPERATOR.py'))==pre['operator_sha256'] and sha(read(pathlib.Path(pre['argv'][2])))==pre['source_sha256'],'Complete actual prelaunch values and sources')
        need(clock(pre['created_utc'])<=clock(c['started_utc'])<=clock(c['finished_utc'])<datetime.datetime.now(datetime.timezone.utc),'Actual child/operator containment')
        for k in ['stdout','stderr']:
            b=read(d/c[k]['path']);need(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'Complete streams')
        captures.append({'directory':'captures/'+name,'actual_pid':c['pid'],'exit_code':exitcode,'capture_sha256':sha(read(d/'CAPTURE.json')),'finished_utc':c['finished_utc']})
    need({p.name for p in (F/'captures').iterdir()}==set(EXPECTED),'Exactly five retained actual controls')
    fixed=parse(read(F/'FIXED_CORPUS_RESULT_V3.json'));owned=parse(read(F/'OWNERSHIP_PHASE_RESULT.json'));final=parse(read(F/'FINAL_CAPTURE_RESULT.json'));need(fixed['assertions_passed']==77649 and owned['assertions_passed']==12406 and final['assertions_passed']==45 and all(z['production_imported_compiled_executed'] is False and z['future_acceptance_approved'] is False for z in [fixed,owned,final]),'Complete successful controls, no approval')
    for name,digest in fixed['six_source_sha256'].items():need(sha(read(H/name))==digest and stat.S_IMODE((H/name).stat().st_mode)==292,'Fixed reviewed production source unchanged')
    files,dirs=tree();need(SELF not in files,'Sole self-exclusion not yet present')
    for q in files.values():q.chmod(292)
    rows=[]
    for n,q in sorted(files.items()):
        b=read(q);need(stat.S_IMODE(q.stat().st_mode)==292,'Complete own full0444');rows.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':292})
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat();need(all(clock(c['finished_utc'])<clock(utc) for c in captures),'Closure after every actual child exit')
    m={'schema':'pr46-acceptance-source-adversary-self-only/v1','created_utc':utc,'actual_closing_pid':os.getpid(),'files_count':len(rows),'files':rows,'self_excluded':[SELF],'manifest_full_mode':292,'directories':[{'path':n,'full_mode':mode} for n,mode in sorted(dirs.items())],'preparation_manifest_sha256':MF,'retained_actual_controls':captures,'source_only':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    data=(json.dumps(m,indent=2,allow_nan=False)+'\n').encode()
    with (F/SELF).open('xb') as h:h.write(data);h.flush();os.fsync(h.fileno())
    (F/SELF).chmod(292);nowfiles,nowdirs=tree();need(set(nowfiles)==set(files)|{SELF} and nowdirs==dirs,'Complete self-only final topology')
    for r in rows:b=read(F/r['path']);need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((F/r['path']).stat().st_mode)==292,'All final body/full-mode hashes')
    need(read(F/SELF)==data and stat.S_IMODE((F/SELF).stat().st_mode)==292,'Self manifest full0444')
    print(json.dumps({'status':'PASS_ROOT_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE','actual_closing_pid':os.getpid(),'manifest_sha256':sha(data),'files_count':len(rows),'directories_including_root':len(dirs),'preparation_manifest_sha256':MF,'source_verdict':'PASS_SOURCE_ONLY_SCOPED','production_imported_compiled_executed':False,'future_acceptance_approved':False}))
if __name__=='__main__':main()
