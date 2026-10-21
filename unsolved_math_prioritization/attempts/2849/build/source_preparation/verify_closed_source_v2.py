"""Separately launch only after the SOURCE V2 closing child exits; read-only."""
import argparse, hashlib, json, math, os, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink member'); return p.read_bytes()
def load(b):
    def pairs(items):
        out={}
        for k,v in items: need(k not in out,'Duplicate JSON key');out[k]=v
        return out
    def constant(x): raise ValueError('Nonfinite JSON constant '+x)
    def floating(x):
        n=float(x);need(math.isfinite(n),'Nonfinite JSON float');return n
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--expected-manifest-sha256',required=True);a=parser.parse_args();need(__debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Unoptimized readback')
    b=raw(F/'PREPARATION_MANIFEST.json');need(sha(b)==a.expected_manifest_sha256 and stat.S_IMODE((F/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'Exact completed SOURCE self/full0444');m=load(b)
    need(m['schema']=='PR47_CURRENT_SOURCE_ONLY_CLOSURE_v2' and m['operative_preparation_directory']==F.name and m['self_excluded']==['PREPARATION_MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['production_import_compile_or_execution'] is False and m['ROOT_reading_or_approval'] is None and m['future_acceptance_approved'] is False,'Genuine completed self-only SOURCE V2')
    fs=set();ds=set()
    for p in F.rglob('*'):
        need(not p.is_symlink(),'No symlinks');n=p.relative_to(F).as_posix()
        if stat.S_ISREG(p.stat().st_mode):fs.add(n)
        else:need(stat.S_ISDIR(p.stat().st_mode),'No special members');ds.add(n)
    names=set();readbytes=0
    for rr in m['files']:
        need(type(rr) is dict and set(rr)=={'path','bytes','sha256'} and type(rr['path']) is str and rr['path'] not in names and not PurePosixPath(rr['path']).is_absolute() and str(PurePosixPath(rr['path']))==rr['path'] and not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(rr['path']).parts) and type(rr['bytes']) is int and rr['bytes']>=0,'Exact unique typed safe member')
        names.add(rr['path']);p=F/rr['path'];rb=raw(p);need(len(rb)==rr['bytes'] and sha(rb)==rr['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Every entire closed member and full0444');readbytes+=len(rb)
    need(fs==names|{'PREPARATION_MANIFEST.json'} and ds==set(m['directories']) and ds=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'Exact whole SOURCE topology, no extras/empty dirs')
    print(json.dumps({'status':'PASS_READONLY_FULL_CLOSED_SOURCE_V2_READBACK','actual_readonly_pid':os.getpid(),'manifest_sha256':sha(b),'files_count':len(names),'directories':len(ds),'complete_member_bytes_read':readbytes,'production_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
