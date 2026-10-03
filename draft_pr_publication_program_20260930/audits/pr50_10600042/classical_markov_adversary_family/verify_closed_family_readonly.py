"""Unexecuted separate ROOT postexit readback. Read only, no approvals/imports."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,os,stat,sys
F=Path(__file__).absolute().parent;SELF='MANIFEST.json'
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
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();need(not sys.flags.optimize,'checks enabled');data=raw(F/SELF);need(sha(data)==a.expected_manifest_sha256,'actual manifest pin');m=load(F/SELF)
    need(m['schema']=='pr50-classical-markov-adversary-self-only-closure/v1'and m['self_excluded']==[SELF]and type(m['files_count'])is int and m['files_count']==len(m['files'])and m['manifest_full_mode']==292 and m['mandatory_mathematical_corrections']==[]and m['future_acceptance_approved']is False and m['virtual_theorem_certified']is False and m['priority_certified']is False,'exact bounded self closure')
    need(type(m['actual_closing_pid'])is int and m['actual_closing_pid']>0 and m['actual_closing_pid']!=os.getpid(),'distinct readback child');t=dt.datetime.fromisoformat(m['created_utc']);need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0)and t<dt.datetime.now(dt.timezone.utc),'past actual awareUTC closure')
    names=set()
    for r in m['files']:
        need(type(r)is dict and set(r)=={'path','bytes','sha256','full_mode'}and type(r['bytes'])is int and r['bytes']>=0 and type(r['full_mode'])is int and r['full_mode']==292,'exact typed rows');n=r['path'];q=PurePosixPath(n);need(type(n)is str and n not in names and n!='.'and '\\'not in n and not q.is_absolute()and str(q)==n and not set(q.parts)&{'.','..','.git','__pycache__'},'unique safe relative');names.add(n);b=raw(F/n);need(len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE((F/n).stat().st_mode)==292,'complete member bytes/modes')
    files=set();dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for q in F.rglob('*'):
        need(not q.is_symlink(),'no symlinks');n=q.relative_to(F).as_posix();mode=q.stat().st_mode
        if stat.S_ISREG(mode):files.add(n)
        else:need(stat.S_ISDIR(mode),'no special');dirs[n]=stat.S_IMODE(mode)
    need(files==names|{SELF}and stat.S_IMODE((F/SELF).stat().st_mode)==292,'self-only complete files')
    need(dirs=={r['path']:r['full_mode']for r in m['directories']}and len(dirs)==len(m['directories'])and set(dirs)=={'.'}|{str(q)for n in names for q in PurePosixPath(n).parents if str(q)!='.'},'all directory modes/topology')
    need(sha(raw(F/'REPORT.md'))==m['report_sha256'],'entire report unchanged')
    for r in m['captured_actual_children']:
        c=load(F/r['directory']/'CAPTURE.json');need(sha(raw(F/r['directory']/'CAPTURE.json'))==r['capture_sha256']and type(c['pid'])is int and c['pid']==r['actual_pid']and type(c['exit_code'])is int and c['exit_code']==0 and dt.datetime.fromisoformat(c['finished_utc'])<t,'retained actual children predate closure')
    print(json.dumps(dict(status='PASS_SEPARATE_ROOT_CLASSICAL_FAMILY_READONLY_READBACK',actual_readback_pid=os.getpid(),actual_closing_pid=m['actual_closing_pid'],manifest_sha256=sha(data),files_count=len(names),directories_count=len(dirs),readback_writes=0,future_acceptance_approved=False)))
if __name__=='__main__':main()
