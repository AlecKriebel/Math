"""Unexecuted ROOT-only closer of this bounded self-only family; no approvals."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os,stat,sys
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');SELF='MANIFEST.json'
def need(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink()and all(not q.is_symlink()for q in p.parents)and stat.S_ISREG(p.stat().st_mode),'regular');return p.read_bytes()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
        return d
    def bad(s):raise ValueError(s)
    return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=bad)
def utc(s):
    t=dt.datetime.fromisoformat(s);need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'aware UTC');return t
def tree():
    need(F==R/'draft_pr_publication_program_20260930/audits/pr50_10600042/classical_markov_adversary_family'and F.is_dir()and not F.is_symlink(),'own exact root')
    files={};dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for p in F.rglob('*'):
        need(not p.is_symlink(),'no symlink');n=p.relative_to(F).as_posix();q=PurePosixPath(n);need(str(q)==n and not set(q.parts)&{'.','..','.git','__pycache__'},'safe path');mode=p.stat().st_mode
        if stat.S_ISREG(mode):files[n]=p
        else:need(stat.S_ISDIR(mode),'no special member');dirs[n]=stat.S_IMODE(mode)
    need(set(dirs)=={'.'}|{str(p)for n in files for p in PurePosixPath(n).parents if str(p)!='.'},'exact ancestor topology');return files,dirs
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();need(not sys.flags.optimize,'guards enabled');need(sha(raw(F/'REPORT.md'))==a.expected_report_sha256,'ROOT exact report read pin');need(not(F/SELF).exists()and not(F/SELF).is_symlink(),'never overwrite self closure')
    v=load(F/'VERDICT.json');need(v['verdict']=='PASS_CLASSICAL_EVEN_STRAND_REFORMULATION'and v['mandatory_mathematical_corrections']==[]and v['future_acceptance_approved']is False and v['virtual_theorem_certified']is False,'bounded mathematical scope')
    bindings=load(F/'SELECTED_INPUT_BINDINGS.json')
    for r in bindings['selected_files']:
        q=R/r['path'];b=raw(q);need(len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE(q.stat().st_mode)==r['full_mode']==292,'selected original evidence stable')
    captures=[]
    for name,pid in [('INDEPENDENT_CONTROLS_ACTUAL_CAPTURE',54290),('LITERAL_AUTHOR_REPLAY_ACTUAL_CAPTURE',54848),('COMPLETE_PRIVATE_READ_ACTUAL_CAPTURE',56201)]:
        d=F/name;need({q.name for q in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','prelaunch_operator.py','prelaunch_target.py','stdout.bin','stderr.bin'},'complete capture6')
        c=load(d/'CAPTURE.json');pre=load(d/'PRELAUNCH.json');need(c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']==pid and type(c['exit_code'])is int and c['exit_code']==0 and c['source_unchanged']is True and c['operator_unchanged']is True and c['stdin_supplied']is False,'actual child')
        need(utc(c['started_utc'])<utc(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'actual times');source=c['source'];need(c['argv']==['/usr/bin/python3','-B',str(R/source['path'])]and raw(d/'prelaunch_target.py')==raw(R/source['path'])and sha(raw(d/'prelaunch_target.py'))==source['sha256'],'actual prelaunch source/argv')
        need(sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256']==sha(raw(F/'capture_private.py')),'captured operator')
        need(pre['actual_execution']is False and pre['completed']is False and pre['pid']is None,'prelaunch honest')
        for k in ['stdout','stderr']:
            r=c[k];b=raw(d/r['path']);need(type(r['bytes'])is int and r['path']==k+'.bin'and len(b)==r['bytes']and sha(b)==r['sha256'],'full streams')
        need(c['stderr']['bytes']==0,'successful stderr');captures.append(dict(directory=name,actual_pid=pid,capture_sha256=sha(raw(d/'CAPTURE.json')),finished_utc=c['finished_utc']))
    need(load(F/'CONTROL_RESULT.json')['assertions']==6155 and load(F/'PRIVATE_EVIDENCE_VALIDATION.json')['literal_replay_byte_and_recursive_type_exact']is True,'bounded results')
    files,dirs=tree()
    for q in files.values():q.chmod(0o444)
    members=[]
    for n,q in sorted(files.items()):b=raw(q);need(stat.S_IMODE(q.stat().st_mode)==292,'full0444');members.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode=292))
    created=dt.datetime.now(dt.timezone.utc).isoformat();need(all(utc(c['finished_utc'])<utc(created)for c in captures),'close after actual operations')
    m=dict(schema='pr50-classical-markov-adversary-self-only-closure/v1',created_utc=created,actual_closing_pid=os.getpid(),files_count=len(members),files=members,self_excluded=[SELF],directories=[dict(path=n,full_mode=m)for n,m in sorted(dirs.items())],manifest_full_mode=292,report_sha256=a.expected_report_sha256,verdict=v['verdict'],mandatory_mathematical_corrections=[],captured_actual_children=captures,retained_failed_children=0,virtual_theorem_certified=False,priority_certified=False,ROOT_approval_created=False,future_acceptance_approved=False)
    data=(json.dumps(m,indent=2,allow_nan=False)+'\n').encode()
    with(F/SELF).open('xb')as h:h.write(data);h.flush();os.fsync(h.fileno())
    (F/SELF).chmod(0o444);now,ndirs=tree();need(set(now)==set(files)|{SELF}and ndirs==dirs,'self-only final topology')
    for r in members:q=F/r['path'];need(len(raw(q))==r['bytes']and sha(raw(q))==r['sha256']and stat.S_IMODE(q.stat().st_mode)==292,'final bodies/modes')
    print(json.dumps(dict(status='PASS_ROOT_CLASSICAL_FAMILY_SELF_ONLY_CLOSURE',actual_closing_pid=os.getpid(),manifest_sha256=sha(data),files_count=len(members),directories_count=len(dirs),future_acceptance_approved=False)))
if __name__=='__main__':main()
