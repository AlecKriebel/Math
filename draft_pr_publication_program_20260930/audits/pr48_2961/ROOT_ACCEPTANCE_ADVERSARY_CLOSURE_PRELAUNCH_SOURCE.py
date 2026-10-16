"""UNEXECUTED proposed ROOT closer for this correction-bearing review, self only."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, math, os, re, stat
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
def rel(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Relative path'); p=PurePosixPath(n)
    need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path'); return n
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Real nonsymlink regular input'); return p.read_bytes()
def check(base,z,mode=None):
    need(type(z) is dict and set(z) in [{'path','bytes','sha256'},{'path','bytes','sha256','full_mode'}],'Typed exact row')
    n=rel(z['path']); b=raw(base/n); need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Full bound body')
    if mode is not None: need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Full permission mode')
def tree():
    need(F.is_dir() and not F.is_symlink(),'Owned root'); ff={}; dd=set()
    for p in F.rglob('*'):
        n=rel(p.relative_to(F).as_posix()); need(not p.is_symlink() and (p.is_file() or p.is_dir()),'Regular topology only')
        if p.is_file(): ff[n]=p
        else: dd.add(n)
    parent={str(p) for n in ff for p in PurePosixPath(n).parents if str(p)!='.'}; need(dd==parent,'Exact ancestor topology'); return ff,dd
def inputs():
    z=parse(raw(F/'INPUT_READ_BINDINGS.json')); rr=z['rows']; need(z['foreign_bodies_copied'] is False and type(rr) is list and len(rr)==4354==len({x['path'] for x in rr}),'Complete metadata bindings')
    for x in rr: check(R,x,x['full_mode'])
    return len(rr)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--expected-report-sha256',required=True); a=p.parse_args()
    need(not (F/SELF).exists() and not (F/SELF).is_symlink(),'Absent literal self'); need(sha(raw(F/'REPORT.md'))==a.expected_report_sha256,'ROOT supplied exact REPORT hash')
    v=parse(raw(F/'VERDICT.json')); need(v['schema']=='pr48-acceptance-source-adversary-verdict/v1' and v['verdict']=='NEEDS_SOURCE_CORRECTION_SCOPED' and type(v['mandatory_corrections']) is list and len(v['mandatory_corrections'])==1 and v['future_acceptance_approved'] is False and v['production_imported_compiled_executed'] is False and v['report_sha256']==a.expected_report_sha256,'Honest correction-bearing scoped verdict')
    need(sha(raw(F.parent/'acceptance_preparation_family/PREPARATION_MANIFEST.json'))==v['preparation_manifest_sha256']=='2f5e572078066a5a895ac813e813106b140f4cc3beabd38f488b7633d07b9c86','Exact reviewed source manifest')
    external_count=inputs(); ff,dd=tree(); need(SELF not in ff,'Self-only payload'); rr=[]
    for n,p in sorted(ff.items()): b=raw(p); rr.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    for z in rr: check(F,z)
    later,dirs=tree(); need(set(later)==set(ff) and dirs==dd,'Stable topology before close')
    body=(json.dumps({'schema':'pr48-acceptance-source-adversary-self-only-closure/v1','status':'CLOSED_CORRECTION_BEARING_SOURCE_REVIEW','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[SELF],'files_count':len(rr),'files':rr,'directories_count':len(dd),'foreign_excluded_prefixes':[],'source_only':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'verdict':'NEEDS_SOURCE_CORRECTION_SCOPED'},sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    for p in ff.values(): p.chmod(0o444)
    for z in rr: check(F,z,0o444)
    stage=F/'.SELF_MANIFEST.staging'
    with stage.open('xb') as h: h.write(body); h.flush(); os.fsync(h.fileno())
    stage.chmod(0o444); os.link(stage,F/SELF,follow_symlinks=False); stage.unlink(); fd=os.open(F,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    closed,dirs=tree(); need(set(closed)==set(ff)|{SELF} and dirs==dd and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Exact self-only full0444 closure'); inputs()
    print(json.dumps({'status':'CLOSED_CORRECTION_BEARING_SOURCE_REVIEW','actual_closing_pid':os.getpid(),'manifest_sha256':sha(raw(F/SELF)),'payload_files':len(rr),'directories':len(dd),'complete_metadata_input_bindings':external_count,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__': main()
