"""Separate ROOT readonly verifier. Never imports closer, proposed sources or controls, never writes."""
import argparse,hashlib,json,math,os,re,stat
from pathlib import Path,PurePosixPath
H=Path(__file__).absolute().parent;R=H.parents[3];NAME='PREPARATION_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v:need(k not in d,'Duplicate key');d[k]=x
        return d
    def fl(s):v=float(s);need(math.isfinite(v),'Nonfinite float');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def check(base,z,mode=None):
    n=z['path'];need(type(n) is str and n and '\\' not in n and '\0' not in n,'Path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and n!='.' and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path');b=raw(base/n);need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole bound bytes')
    if mode is not None:need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Exact fullmode')
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();b=raw(H/NAME);need(sha(b)==a.expected_manifest_sha256,'Explicit actual closure SHA');m=parse(b);need(set(m)=={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'} and m['schema']=='pr48-acceptance-source-closure/v1' and m['status']=='CLOSED_SOURCE_ONLY' and m['self_excluded']==[NAME] and m['source_only'] is True and m['proposed_helpers_imported_compiled_executed'] is False and m['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact source-only self closure');rr=m['files'];need(type(rr) is list and type(m['files_count']) is int and m['files_count']==len(rr),'Typed complete rows');names=set()
    for z in rr:need(type(z) is dict and set(z)=={'path','bytes','sha256'} and z['path'] not in names and z['path']!=NAME,'Unique exact payload');check(H,z,0o444);names.add(z['path'])
    names.add(NAME);files=set();dirs=set()
    for p in H.rglob('*'):need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special topology');(files if p.is_file() else dirs).add(p.relative_to(H).as_posix())
    expected={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(files==names and dirs==expected and stat.S_IMODE((H/NAME).stat().st_mode)==0o444,'Exact topology and self444');inputs=parse(raw(H/'INPUT_BINDINGS.json'))
    for z in list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]:check(R,z,z['full_mode'])
    need(len(inputs['external_input_rows'])==3912 and inputs['actual_predecessor_PR47_completed'] is False and inputs['previous_root_post'] is None,'Fixed3912 and no invented actual predecessor');print(json.dumps({'status':'PASS_CLOSED_SOURCE_ONLY_READBACK','actual_readback_pid':os.getpid(),'payload_files':len(rr),'directories':len(dirs),'manifest_sha256':sha(b),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
