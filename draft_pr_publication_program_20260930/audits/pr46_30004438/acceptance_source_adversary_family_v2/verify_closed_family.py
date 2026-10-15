#!/usr/bin/python3
"""ROOT separate postexit readonly own closure verifier; no production import/call."""
import argparse,datetime,hashlib,json,os,pathlib,re,stat
F=pathlib.Path(__file__).absolute().parent;SELF='SELF_MANIFEST.json'
def need(v,n):
    if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode) and stat.S_IMODE(p.stat().st_mode)==292,'Regular full0444');return p.read_bytes()
def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args();need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Checks enabled');b=read(F/SELF);need(re.fullmatch('[0-9a-f]{64}',a.manifest_sha256) is not None and sha(b)==a.manifest_sha256,'Actual ROOT closure hash');m=json.loads(b)
    need(m['schema']=='pr46-acceptance-source-adversary-self-only/v1' and m['self_excluded']==[SELF] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['production_imported_compiled_executed'] is False and m['future_acceptance_approved'] is False,'Source-only self closure')
    need(type(m['actual_closing_pid']) is int and m['actual_closing_pid']>0 and m['actual_closing_pid']!=os.getpid(),'Separate real child');closed=datetime.datetime.fromisoformat(m['created_utc']);need(closed.utcoffset()==datetime.timedelta(0) and closed<datetime.datetime.now(datetime.timezone.utc),'Actual prior closing clock')
    names=set()
    for r in m['files']:
        need(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['bytes']) is int and r['bytes']>=0 and type(r['full_mode']) is int and r['full_mode']==292 and r['path'] not in names,'Typed unique full rows');n=pathlib.PurePosixPath(r['path']);need(not n.is_absolute() and str(n)==r['path'] and not {'.','..','.git','__pycache__'}&set(n.parts) and '\\' not in r['path'],'Canonical member');names.add(r['path']);raw=read(F/r['path']);need(len(raw)==r['bytes'] and sha(raw)==r['sha256'],'Every complete body')
    files=set();dirs={'.':stat.S_IMODE(F.stat().st_mode)}
    for p in F.rglob('*'):
        need(not p.is_symlink(),'No symlink');n=p.relative_to(F).as_posix()
        if p.is_dir():dirs[n]=stat.S_IMODE(p.stat().st_mode)
        else:read(p);files.add(n)
    implied={'.'}|{str(q) for n in names for q in pathlib.PurePosixPath(n).parents if str(q)!='.'};need(files==names|{SELF} and set(dirs)==implied and len(m['directories'])==len(dirs) and {d['path'] for d in m['directories']}==set(dirs) and all(type(d['full_mode']) is int and dirs[d['path']]==d['full_mode'] for d in m['directories']),'Complete exact topology/modes')
    v=json.loads(read(F/'VERDICT.json'));need(v['schema']=='pr46-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['mandatory_corrections']==[] and v['preparation_manifest_sha256']==m['preparation_manifest_sha256'] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False,'Exact source scoped verdict')
    print(json.dumps({'status':'PASS_SEPARATE_ROOT_SOURCE_ADVERSARY_READONLY_READBACK','actual_readback_pid':os.getpid(),'actual_closing_pid':m['actual_closing_pid'],'manifest_sha256':sha(b),'files_count':len(names),'directories_including_root':len(dirs),'source_verdict':'PASS_SOURCE_ONLY_SCOPED','future_acceptance_approved':False,'readback_writes':0}))
if __name__=='__main__':main()
