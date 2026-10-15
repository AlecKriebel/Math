"""ROOT alone executes this SOURCE adversary closure; no production imported."""
import argparse,datetime as dt,hashlib,json,math,os,re,stat
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;R=F.parents[3];SELF='SELF_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(rr):
        d={}
        for k,v in rr:need(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def fl(x):y=float(x);need(math.isfinite(y),'Nonfinite');return y
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def raw(p):need(p.is_file() and not p.is_symlink() and not any(x.is_symlink() for x in p.parents),'Regular nonsymlink file');return p.read_bytes()
def checked(base,z,mode):
    n=z['path'];p=PurePosixPath(n);need(type(n) is str and n and p.as_posix()==n and not p.is_absolute() and not {'..','.git','__pycache__'}.intersection(p.parts),'Canonical member');b=raw(base/n)
    need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire bound body')
    if mode is not None:need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Complete fullmode')
def external():
    o=parse(raw(F/'INPUT_BINDINGS.json'));rr=o['normalized_complete_external_input_bindings'];need(type(rr) is list and len({z['path'] for z in rr})==len(rr),'Normalized unique fixed inputs')
    for z in rr:need(set(z)=={'path','bytes','sha256','full_mode'},'Exact normalized row');checked(R,z,z['full_mode'])
    return o
def files():
    ff={};dd=set()
    for p in F.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No symlink or special topology');n=p.relative_to(F).as_posix()
        if p.is_file():ff[n]=p
        else:dd.add(n)
    expected={p.as_posix() for n in ff for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(dd==expected,'Exact recursive directories; no empty/unbound dirs');return ff,dd
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args()
    need(not (F/SELF).exists() and not (F/SELF).is_symlink(),'Absent-only literal root self');need(sha(raw(F/'REPORT.md'))==a.expected_report_sha256,'ROOT exact report pin')
    v=parse(raw(F/'VERDICT.json'));o=external();need(v['schema']=='pr48-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['mandatory_corrections']==[] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False and v['preparation_manifest_sha256']==o['preparation_manifest_sha256'],'Complete scoped clean verdict')
    ff,dd=files();need(SELF not in ff,'Literal self excluded');rr=[{'path':n,'bytes':len(raw(q)),'sha256':sha(raw(q))} for n,q in sorted(ff.items())]
    for z in rr:checked(F,z,None)
    for q in ff.values():q.chmod(0o444)
    for z in rr:checked(F,z,0o444)
    body=(json.dumps({'schema':'pr48-fresh-V3-SOURCE-adversary-self-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded':[SELF],'files_count':len(rr),'files':rr,'production_imported_compiled_executed':False,'future_acceptance_approved':False},indent=2,sort_keys=True)+'\n').encode()
    staged=F/'.SELF_MANIFEST.stage'
    with staged.open('xb') as h:h.write(body);h.flush();os.fsync(h.fileno())
    staged.chmod(0o444);os.link(staged,F/SELF,follow_symlinks=False);staged.unlink();descriptor=os.open(F,os.O_RDONLY)
    try:os.fsync(descriptor)
    finally:os.close(descriptor)
    external();actual,dirs=files();need(set(actual)==set(ff)|{SELF} and dirs==dd and stat.S_IMODE((F/SELF).stat().st_mode)==0o444,'Exact self-only closure and self444')
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closing_pid':os.getpid(),'files_count':len(rr),'directories':len(dd),'manifest_sha256':sha(raw(F/SELF)),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
