"""Read-only source closure verification; only after the real closing child exits."""
import argparse, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected-manifest-sha256',required=True);args=parser.parse_args();p=F/'PREPARATION_MANIFEST.json';b=p.read_bytes();assert __debug__ and sha(b)==args.expected_manifest_sha256 and not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444;m=json.loads(b)
    assert m['schema']=='pr48-current-source-only-closure/v1' and m['self_excluded']==[p.name] and type(m['files_count']) is int and m['files_count']==len(m['files']) and m['production_builder_imported_compiled_or_executed'] is False and m['future_acceptance_approved'] is False
    actualfiles=set();actualdirs={'.'}
    for q in F.rglob('*'):
        assert not q.is_symlink();n=q.relative_to(F).as_posix()
        if stat.S_ISREG(q.stat().st_mode):actualfiles.add(n)
        else:assert stat.S_ISDIR(q.stat().st_mode);actualdirs.add(n)
    assert actualfiles=={r['path'] for r in m['files']}|{p.name} and actualdirs=={r['path'] for r in m['directories']}
    for r in m['files']:
        q=F/r['path'];body=q.read_bytes();assert len(body)==r['bytes'] and sha(body)==r['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
    for r in m['directories']:assert type(r['full_mode']) is int and stat.S_IMODE((F/r['path']).stat().st_mode)==r['full_mode']
    print(json.dumps({'status':'PASS_READONLY_SOURCE_CLOSURE_AFTER_REAL_CHILD_EXIT','actual_readback_pid':os.getpid(),'files_count':m['files_count'],'directories_including_root':len(actualdirs),'manifest_sha256':sha(b),'future_acceptance_approved':False},indent=2))
if __name__=='__main__':main()
