"""Own adverse evidence only. Never loads proposed production code."""
from pathlib import Path, PurePosixPath
import hashlib, json, re, stat
R=Path('/Users/alec/Documents/Math')
F=Path(__file__).absolute().parent
def need(v,m):
    if not v:raise ValueError(m)
def safe(n):
    need(type(n) is str and n and '\\' not in n and '\0' not in n,'Literal member')
    p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical member');return n
def raw(p):
    need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular nonsymlink body');return p.read_bytes()
def pairs(items):
    d={}
    for k,v in items:need(k not in d,'No duplicate JSON key');d[k]=v
    return d
def load(p):return json.loads(raw(p),object_pairs_hook=pairs,parse_constant=lambda n:(_ for _ in ()).throw(ValueError(n)))
def triple(p,n):
    b=raw(p);return dict(path=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def row(base,z,mode=None):
    keys={'path','bytes','sha256'}|({'full_mode'} if mode is None else set())
    need(type(z) is dict and set(z)==keys and type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed binding')
    p=base/safe(z['path']);b=raw(p);need(len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'],'Complete referenced body')
    expected=z['full_mode'] if mode is None else mode;need(type(expected) is int and 0<=expected<=0o7777 and stat.S_IMODE(p.stat().st_mode)==expected,'Exact full07777 file mode')
def topology(base,names,dirs,mode):
    need(type(names) is list and names==sorted(set(names)) and all(safe(n)==n for n in names),'Distinct exact file names')
    need(type(dirs) is list and dirs==sorted(set(dirs)) and '.' in dirs and all(d=='.' or safe(d)==d for d in dirs),'Distinct exact directory names')
    actual_files=[];actual_dirs=['.']
    need(base.is_dir() and not base.is_symlink() and all(not q.is_symlink() for q in base.parents),'Own directory')
    for q in base.rglob('*'):
        need(not q.is_symlink(),'No symlink');s=q.lstat();n=q.relative_to(base).as_posix()
        if stat.S_ISREG(s.st_mode):actual_files.append(n);need(stat.S_IMODE(s.st_mode)==mode,'All own full file modes')
        elif stat.S_ISDIR(s.st_mode):actual_dirs.append(n);need(stat.S_IMODE(s.st_mode)==0o755,'All own full directory modes')
        else:raise ValueError('No FIFO/device/socket')
    need(sorted(actual_files)==names and sorted(actual_dirs)==dirs and stat.S_IMODE(base.stat().st_mode)==0o755,'Exact complete topology/root mode')
    required={'.'}|{p.as_posix() for n in names for p in PurePosixPath(n).parents}
    need(set(dirs)==required,'No extra empty directories')
def fixed_inputs():
    v=load(F/'FIXED_INPUT_BINDINGS.json');rows=v['fixed_rows'];need(type(v['fixed_rows_count']) is int and v['fixed_rows_count']==len(rows)==229,'Bounded full custody rows')
    need([z['path'] for z in rows]==sorted(set(z['path'] for z in rows)),'Unique fixed domain')
    for z in rows:row(R,z)
    for z in v['exact_preserved_families']:
        topology(R/safe(z['path']),z['payload_names'],sorted(z['directory_names']),z['full_file_mode'])
    z=v['additional_genuine_outer_directory'];need(type(z['full_mode']) is int and z['full_mode']==0o700,'Typed genuine outer700');p=R/safe(z['path']);need(p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==0o700,'Unchanged genuine outer full mode')
    for z in v['additional_genuine_outer_directories']:
        p=R/safe(z['path']);need(type(z['full_mode']) is int and z['full_mode']==0o700 and p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==0o700,'Each genuine M3 outer full700')
    verdict=load(F/'VERDICT.json');need(verdict['schema']=='pr48-post-push-epoch-independent-SOURCE-verdict/v1' and verdict['status']=='REPAIR_REQUIRED_SOURCE' and verdict['source_ready_sha256']=='4a2ca334cfea92fb44dfebb874de8d4b0827292b0ab3fb7e82a57de3b8746771' and verdict['production_executed'] is False and verdict['future_acceptance_approved'] is False and [z['id'] for z in verdict['mandatory_findings']]==['M4'],'Operative adverse verdict only')
def own_ready(expected,mode):
    need(__debug__ and F.name=='corrective_source_adversary_v4','Exact own family and no optimized Python');b=raw(F/'READY.json');need(hashlib.sha256(b).hexdigest()==expected,'Actual own READY pin');v=load(F/'READY.json')
    need(v['schema']=='pr48-corrective-v4-adverse-readiness/v1' and v['source_only'] is True and v['production_executed'] is False and v['future_acceptance_approved'] is False,'Source-only readiness')
    names=v['closure_payload_files'];need('READY.json' in names and 'SELF_MANIFEST.json' not in names,'Self excluded');need([z['path'] for z in v['fixed_own_files']]==[n for n in names if n!='READY.json'],'Entire own pre-READY domain')
    for z in v['fixed_own_files']:row(F,z,mode)
    return v
