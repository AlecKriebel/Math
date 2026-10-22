"""Caller-pinned standard-library-only READ ONLY closed-review integrity check."""
import sys
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use nonoptimized -I -S -B')
from pathlib import Path
import hashlib,json,re,stat
D=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise RuntimeError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(xs):
        d={}
        for k,v in xs:need(k not in d,'Duplicate JSON key');d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def pin(path):
    s=path.lstat();need(not path.is_symlink()and stat.S_ISREG(s.st_mode),'Nonregular pinned input')
    b=path.read_bytes();return {'bytes':len(b),'sha256':H(b),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
def check_namespace(root,manifest):
    actual={'.'}|{p.relative_to(root).as_posix()for p in root.rglob('*')if p!=root/'MANIFEST.json'}
    need(actual==set(manifest['entries']),'Closed namespace changed '+root.name)
    groups={}
    for name,wanted in manifest['entries'].items():
        p=root if name=='.'else root/name;s=p.lstat();need(not p.is_symlink(),'Closed symlink')
        need(stat.S_IMODE(s.st_mode)==wanted['mode']and s.st_mtime_ns==wanted['mtime_ns'],'Closed metadata changed '+str(p))
        if 'nlink'in wanted:need(s.st_nlink==wanted['nlink'],'Pinned nlink changed')
        if wanted['kind']=='file':
            need(stat.S_ISREG(s.st_mode),'Expected regular file');b=p.read_bytes();need(len(b)==wanted['bytes']and H(b)==wanted['sha256'],'Closed bytes changed '+str(p))
            groups.setdefault((s.st_dev,s.st_ino),[]).append(name)
        else:need(wanted['kind']=='directory'and stat.S_ISDIR(s.st_mode),'Expected directory')
    if 'hardlink_groups'in manifest:need(sorted(sorted(v)for v in groups.values()if len(v)>1)==sorted(sorted(v)for v in manifest['hardlink_groups']),'Closed hardlink groups changed')
    return sum(p['kind']=='file'for p in manifest['entries'].values())
def main():
    need(len(sys.argv)==3 and sys.argv[1]=='--manifest-sha256'and re.fullmatch('[a-f0-9]{64}',sys.argv[2]),'Exact caller manifest hash required')
    raw=(D/'MANIFEST.json').read_bytes();need(H(raw)==sys.argv[2],'Caller review hash mismatch');m=parse(raw)
    need(m['exclusions']==['MANIFEST.json']and m['publication_ready']is False and m['root_action_accepted']is False and m['verdict']=='HOLD_NONINJECTIVE_PARSED_ORIGINAL_CUSTODY_AND_STALE_HEAD_HANDOFF','Integrity is not authority or clearance')
    files=check_namespace(D,m);external=0
    for name,wanted in m['external_closed_roots'].items():
        p=Path(name)/'MANIFEST.json';b=p.read_bytes();need({'bytes':len(b),'sha256':H(b)}==wanted,'External manifest changed');external+=check_namespace(p.parent,parse(b))
    readback=parse((D/'private/FINAL_INPUT_READBACK.json').read_bytes())
    for name,wanted in readback['inventory'].items():need(pin(Path(name))==wanted,'Historical/scientific input changed '+name)
    for name,wanted in m['extra_input_pins'].items():need(pin(Path(name))==wanted,'Extra bound input changed '+name)
    freeze=parse((D/'source/SOURCE_FREEZE.json').read_bytes());old=D.parent/'operations'
    need({p.name for p in(old/'runtime').iterdir()}==set(freeze['prior_runtime_files']),'Original13runtime namespace changed')
    revoked=old/'runtime/ROOT_OPERATIONAL_CLEARANCE.json'
    need(not revoked.exists()and not revoked.is_symlink(),'Revoked authority revived')
    for number in range(6,18):
        runtime=D.parent/('operations'+str(number).zfill(2))/'runtime'
        need(not runtime.exists()and not runtime.is_symlink(),'Unauthorized production runtime appeared; preactivation review closure cannot be claimed unchanged')
    print(json.dumps({'status':'PASS_INTEGRITY_ONLY_HOLD_REMAINS','files':files,'directories':sum(x['kind']=='directory'for x in m['entries'].values()),'external_closed_files':external,'external_inventory_records':len(readback['inventory']),'caller_manifest_sha256':sys.argv[2],'publication_ready':False,'root_action_authority':False,'project_imports_replays_services_writes':0},sort_keys=True))
if __name__=='__main__':main()
