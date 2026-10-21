"""Separate ROOT readonly closure verification; no imports of other sources."""
import argparse,hashlib,json,math,os,re,stat
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;R=F.parents[3];SELF='SELF_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(rr):
        o={}
        for k,v in rr:need(k not in o,'Duplicate key');o[k]=v
        return o
    def fl(x):v=float(x);need(math.isfinite(v),'Nonfinite');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def raw(p):need(p.is_file() and not p.is_symlink() and all(not x.is_symlink() for x in p.parents),'Regular nonsymlink file');return p.read_bytes()
def check(base,z,mode):
    n=z['path'];p=PurePosixPath(n);need(type(n) is str and n and not p.is_absolute() and p.as_posix()==n and not {'..','.git','__pycache__'}.intersection(p.parts),'Canonical root-relative path');b=raw(base/n)
    need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole bound body');need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Full mode')
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();b=raw(F/SELF);need(sha(b)==a.expected_manifest_sha256,'Explicit actual closure pin');m=parse(b)
    need(set(m)=={'schema','status','utc','self_excluded','files_count','files','production_imported_compiled_executed','future_acceptance_approved'} and m['schema']=='pr48-fresh-V3-SOURCE-adversary-self-closure/v1' and m['status']=='CLOSED_SOURCE_ONLY' and m['self_excluded']==[SELF] and m['production_imported_compiled_executed'] is False and m['future_acceptance_approved'] is False,'Exact scoped SOURCE self closure')
    rr=m['files'];need(type(rr) is list and type(m['files_count']) is int and m['files_count']==len(rr),'Typed complete payload');names={SELF}
    for z in rr:need(type(z) is dict and set(z)=={'path','bytes','sha256'} and z['path'] not in names,'Unique exact member');check(F,z,0o444);names.add(z['path'])
    files=set();dirs=set()
    for p in F.rglob('*'):need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special/symlink');(files if p.is_file() else dirs).add(p.relative_to(F).as_posix())
    expected={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(files==names and dirs==expected and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Exact payload topology and self444')
    o=parse(raw(F/'INPUT_BINDINGS.json'));ee=o['normalized_complete_external_input_bindings'];need(type(ee) is list and len({z['path'] for z in ee})==len(ee),'Entire unique input domain')
    for z in ee:need(set(z)=={'path','bytes','sha256','full_mode'},'Exact external row');check(R,z,z['full_mode'])
    v=parse(raw(F/'VERDICT.json'));need(v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['mandatory_corrections']==[] and v['preparation_manifest_sha256']==o['preparation_manifest_sha256'],'Exact reviewed SOURCE identity')
    print(json.dumps({'status':'PASS_CLOSED_SOURCE_ONLY_READBACK','actual_readback_pid':os.getpid(),'payload_files':len(rr),'directories':len(dirs),'normalized_unique_fixed_inputs':len(ee),'manifest_sha256':sha(b),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
