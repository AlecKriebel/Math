"""UNEXECUTED separate read-only ROOT verifier, never imports closer or reviewed code."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, math, os, re, stat
F=Path(__file__).absolute().parent; R=F.parents[3]; SELF='SELF_MANIFEST.json'
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v: need(k not in d,'Duplicate key'); d[k]=x
        return d
    def fl(s): x=float(s); need(math.isfinite(x),'Nonfinite'); return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Real regular nonsymlink'); return p.read_bytes()
def check(base,z,mode):
    need(type(z) is dict and set(z) in [{'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}],'Exact reference keys'); n=z['path']; need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Literal relative path'); p=PurePosixPath(n); need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path')
    b=raw(base/n); need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete reference bytes'); need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Full mode')
def main():
    p=argparse.ArgumentParser(); p.add_argument('--expected-manifest-sha256',required=True); a=p.parse_args(); b=raw(F/SELF); need(sha(b)==a.expected_manifest_sha256,'Exact actual closing manifest pin'); m=parse(b)
    need(set(m)=={'schema','status','utc','self_excluded','files_count','files','directories_count','foreign_excluded_prefixes','source_only','production_imported_compiled_executed','future_acceptance_approved','verdict'} and m['schema']=='pr48-acceptance-source-adversary-self-only-closure/v1' and m['self_excluded']==[SELF] and m['foreign_excluded_prefixes']==[] and m['source_only'] is True and m['production_imported_compiled_executed'] is False and m['future_acceptance_approved'] is False and m['verdict']=='NEEDS_SOURCE_CORRECTION_SCOPED','Exact correction-bearing SOURCE scope')
    rr=m['files']; need(type(rr) is list and type(m['files_count']) is int and m['files_count']==len(rr),'Typed full payload count'); names=set()
    for z in rr: need(z['path'] not in names and z['path']!=SELF,'Unique self-only payload'); check(F,z,0o444); names.add(z['path'])
    names.add(SELF); ff=set(); dd=set()
    for p in F.rglob('*'): need(not p.is_symlink() and (p.is_file() or p.is_dir()),'Regular topology'); (ff if p.is_file() else dd).add(p.relative_to(F).as_posix())
    parents={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}; need(ff==names and dd==parents and type(m['directories_count']) is int and m['directories_count']==len(dd) and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Exact whole self-only topology and full0444')
    v=parse(raw(F/'VERDICT.json')); need(v['verdict']=='NEEDS_SOURCE_CORRECTION_SCOPED' and len(v['mandatory_corrections'])==1 and v['future_acceptance_approved'] is False and sha(raw(F/'REPORT.md'))==v['report_sha256'],'Correction not promoted to PASS'); z=parse(raw(F/'INPUT_READ_BINDINGS.json')); need(len(z['rows'])==4354==len({x['path'] for x in z['rows']}),'All unique individual inputs')
    for x in z['rows']: check(R,x,x['full_mode'])
    print(json.dumps({'status':'PASS_CLOSED_CORRECTION_BEARING_REVIEW_READBACK','actual_readback_pid':os.getpid(),'manifest_sha256':sha(b),'payload_files':len(rr),'directories':len(dd),'complete_metadata_input_bindings':4354,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__': main()
