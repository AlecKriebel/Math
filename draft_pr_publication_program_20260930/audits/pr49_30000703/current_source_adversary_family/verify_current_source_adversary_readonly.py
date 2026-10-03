"""ROOT separate postexit readback. Read only; never import/call production/helpers."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat, sys
F=Path(__file__).absolute().parent;SELF='MANIFEST.json'
def need(x,n):
    if not x:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'regular nonsymlink');return p.read_bytes()
def load(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
        return d
    def number(s):
        x=float(s);need(math.isfinite(x),'finite JSON');return x
    def const(s):raise ValueError('nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=number,parse_constant=const)
def utc(s):
    need(type(s) is str,'UTC string');x=dt.datetime.fromisoformat(s);need(x.utcoffset()==dt.timedelta(0),'aware UTC');return x
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'checks enabled');b=raw(F/SELF);need(re.fullmatch('[0-9a-f]{64}',a.expected_manifest_sha256) and sha(b)==a.expected_manifest_sha256,'actual ROOT manifest pin');m=load(b)
    need(m['schema']=='pr49-current-source-adversary-self-only-closure/v1' and m['self_excluded']==[SELF] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['manifest_full_mode']==292 and m['mandatory_corrections']==[] and m['future_acceptance_approved'] is False and m['production_imported_compiled_executed'] is False and m['helpers_executed'] is False and m['new_whole_current_review_gate']=='PENDING','exact bounded SOURCE closure');need(type(m['actual_closing_pid']) is int and m['actual_closing_pid']>0 and m['actual_closing_pid']!=os.getpid(),'distinct real readonly child');closed=utc(m['created_utc']);need(closed<dt.datetime.now(dt.timezone.utc),'prior actual closure')
    names=set()
    for r in m['files']:
        need(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['path']) is str and r['path'] not in names and type(r['bytes']) is int and r['bytes']>=0 and type(r['full_mode']) is int and r['full_mode']==292 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']),'exact typed member');n=PurePosixPath(r['path']);need(not n.is_absolute() and str(n)==r['path'] and r['path']!='.' and '\\' not in r['path'] and not set(n.parts)&{'.','..','.git','__pycache__'},'canonical self member');names.add(r['path']);q=F/r['path'];data=raw(q);need(len(data)==r['bytes'] and sha(data)==r['sha256'] and stat.S_IMODE(q.stat().st_mode)==292,'complete own closed body/mode')
    files=set();dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for q in F.rglob('*'):
        need(not q.is_symlink(),'no symlink');n=q.relative_to(F).as_posix();mode=q.stat().st_mode
        if stat.S_ISREG(mode):files.add(n)
        else:need(stat.S_ISDIR(mode),'no special');dirs[n]=stat.S_IMODE(mode)
    need(files==names|{SELF} and stat.S_IMODE((F/SELF).stat().st_mode)==292,'exact self-only file set');need(dirs=={r['path']:r['full_mode'] for r in m['directories']} and len(m['directories'])==len(dirs),'all directory full modes');need(set(dirs)=={'.'}|{str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'},'no empty/extra directories')
    need(sha(raw(F/'REPORT.md'))==m['report_sha256'],'full report pin');v=load(raw(F/'VERDICT.json'));need(v['mandatory_corrections']==[] and v['future_acceptance_approved'] is False and v['new_whole_current_review_gate']=='PENDING','own bounded verdict')
    for entry in m['retained_actual_captures']:
        c=load(raw(F/entry['directory']/'CAPTURE.json'));need(sha(raw(F/entry['directory']/'CAPTURE.json'))==entry['capture_sha256'] and c['pid']==entry['actual_pid'] and type(c['pid']) is int and type(c['exit_code']) is int and c['exit_code']==entry['exit_code'] and c['actual_execution'] is True and c['completed'] is True and utc(c['finished_utc'])<closed,'actual retained operation completion')
    print(json.dumps(dict(status='PASS_SEPARATE_ROOT_CURRENT_SOURCE_ADVERSARY_READONLY_READBACK',actual_readback_pid=os.getpid(),actual_closing_pid=m['actual_closing_pid'],manifest_sha256=sha(b),files_count=len(names),directories_count=len(dirs),readback_writes=0,future_acceptance_approved=False,new_whole_current_review_gate='PENDING')))
if __name__=='__main__':main()
