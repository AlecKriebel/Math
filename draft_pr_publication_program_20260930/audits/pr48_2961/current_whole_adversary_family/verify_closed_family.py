"""Read-only verification after ROOT's genuine separately captured closing child."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,sys
F=Path(__file__).absolute().parent
assert __debug__ and not sys.flags.optimize
p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
b=(F/'MANIFEST.json').read_bytes();assert sha(b)==a.expected_manifest_sha256
m=json.loads(b);assert m['schema']=='pr48-whole-current-independent-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==len(m['files'])
fs=set();ds=set()
for p in F.rglob('*'):
 assert not p.is_symlink()
 n=p.relative_to(F).as_posix()
 if stat.S_ISREG(p.stat().st_mode):fs.add(n)
 else:assert stat.S_ISDIR(p.stat().st_mode);ds.add(n)
names=set()
for row in m['files']:
 assert set(row)=={'path','bytes','sha256','full_mode'} and type(row['bytes']) is int and row['bytes']>=0 and row['full_mode']=='0444'
 n=row['path'];assert n not in names;names.add(n)
 p=F/n;b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert fs==names|{'MANIFEST.json'} and ds==set(m['directories'])=={q.as_posix() for n in fs for q in PurePosixPath(n).parents if q.as_posix()!='.'}
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444 and m['future_acceptance_approved'] is False and m['mandatory_corrections']==[]
print(json.dumps({'status':'PASS_COMPLETE_CLOSED_WHOLE_CURRENT_READBACK','actual_verifier_pid':os.getpid(),'payload_files':len(names),
 'directories':len(ds),'manifest_sha256':a.expected_manifest_sha256,'actual_closing_pid':m['actual_closing_pid'],'future_acceptance_approved':False},indent=2))
