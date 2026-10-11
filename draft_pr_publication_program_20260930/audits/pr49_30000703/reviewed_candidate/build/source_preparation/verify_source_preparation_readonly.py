#!/usr/bin/python3
"""ROOT separate postexit readback; no writes and no production import/call."""
import argparse,datetime,hashlib,json,math,os,pathlib,re,stat,sys
F=pathlib.Path(__file__).absolute().parent;SELF='PREPARATION_MANIFEST.json'
def require(v,n):
    if not v:raise ValueError(n)
def digest(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink file');return p.read_bytes()
def load(b):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def number(s):
        v=float(s);require(math.isfinite(v),'Finite JSON');return v
    def const(s):raise ValueError('Nonfinite JSON')
    return json.loads(b,object_pairs_hook=pairs,parse_float=number,parse_constant=const)
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Checks enabled')
    b=raw(F/SELF);require(re.fullmatch('[0-9a-f]{64}',a.expected_manifest_sha256) is not None and digest(b)==a.expected_manifest_sha256,'ROOT actual manifest SHA');m=load(b)
    require(m['schema']=='pr49-current-source-only-closure/v1' and m['self_excluded']==[SELF] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['SOURCE_adversary_verdict'] is None and m['future_acceptance_approved'] is False and m['production_builder_imported_compiled_executed'] is False and m['production_operator_imported_compiled_executed'] is False,'Closed SOURCE only')
    require(type(m['actual_closing_pid']) is int and m['actual_closing_pid']>0 and m['actual_closing_pid']!=os.getpid(),'Distinct real child');closed=datetime.datetime.fromisoformat(m['created_utc']);require(closed.utcoffset()==datetime.timedelta(0) and closed<datetime.datetime.now(datetime.timezone.utc),'Aware prior closure UTC')
    names=set()
    for r in m['files']:
        require(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['path']) is str and r['path'] not in names and type(r['bytes']) is int and r['bytes']>=0 and type(r['full_mode']) is int and r['full_mode']==0o444,'Exact typed row');n=pathlib.PurePosixPath(r['path']);require(not n.is_absolute() and str(n)==r['path'] and not {'.','..','.git','__pycache__'}&set(n.parts) and '\\' not in r['path'],'Canonical member');names.add(r['path']);q=F/r['path'];data=raw(q);require(len(data)==r['bytes'] and digest(data)==r['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444,'Complete closed body/fullmode')
    files=set();dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for q in F.rglob('*'):
        require(not q.is_symlink(),'No symlink');n=q.relative_to(F).as_posix()
        if stat.S_ISREG(q.stat().st_mode):files.add(n)
        else:require(stat.S_ISDIR(q.stat().st_mode),'No special file');dirs[n]=stat.S_IMODE(q.stat().st_mode)
    require(files==names|{SELF} and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Exact self-only files')
    expected={'.'}|{str(q) for n in names for q in pathlib.PurePosixPath(n).parents if str(q)!='.'};require(set(dirs)==expected and len(m['directories'])==len(dirs) and all(type(d['full_mode']) is int and dirs[d['path']]==d['full_mode'] for d in m['directories']) and {d['path'] for d in m['directories']}==set(dirs),'Exact complete directory topology/modes')
    for c in m['retained_actual_nonproduction_captures']:
        cap=load(raw(F/c['directory']/'CAPTURE.json'));require(digest(raw(F/c['directory']/'CAPTURE.json'))==c['capture_sha256'] and cap['pid']==c['actual_pid'] and type(cap['pid']) is int and type(cap['exit_code']) is int and cap['exit_code']==c['exit_code'] and cap['completed'] is True and cap['actual_execution'] is True and datetime.datetime.fromisoformat(cap['finished_utc'])<closed,'Actual retained completion before closure')
    print(json.dumps({'status':'PASS_SEPARATE_ROOT_SOURCE_READONLY_READBACK','actual_readback_pid':os.getpid(),'actual_closing_pid':m['actual_closing_pid'],'manifest_sha256':digest(b),'files_count':len(names),'directories_count':len(dirs),'SOURCE_adversary_verdict':None,'production_execution':False,'readback_writes':0}))
if __name__=='__main__':main()
