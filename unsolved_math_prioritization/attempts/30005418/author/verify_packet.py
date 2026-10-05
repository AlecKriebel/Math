#!/usr/bin/env python3
"""Strict safe inventory and deterministic arithmetic replay.
An externally supplied manifest hash is optional for independent binding.
"""
import hashlib,json,pathlib,subprocess,sys,tempfile
if not __debug__:raise SystemExit('Assertions must remain enabled.')
PAYLOAD={'README.md','PROOF.md','RESEARCH_LOG.md','SOURCES.json','PRIOR_ATTEMPT_CHECK.json','verify_math.py','MATH_RESULTS.json','verify_sources.py','SOURCE_REHASH_RESULTS.json','verify_packet.py'}
def meta(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    root=pathlib.Path(__file__).resolve().parent;manifest=root/'AUTHOR_MANIFEST.json';mb=manifest.read_bytes();mh=hashlib.sha256(mb).hexdigest()
    if len(sys.argv)==3 and sys.argv[1]=='--expected-manifest':assert mh==sys.argv[2],'external manifest hash mismatch'
    elif len(sys.argv)!=1:raise SystemExit('Usage: verify_packet.py [--expected-manifest SHA256]')
    paths=list(root.iterdir());assert all(p.is_file() and not p.is_symlink() for p in paths),'unexpected directory or symlink'
    assert {p.name for p in paths}==PAYLOAD|{'AUTHOR_MANIFEST.json'},'inventory mismatch'
    m=json.loads(mb);assert m['problem_id']==30005418 and m['outcome']=='unsolved' and m['approach_families_used']==5
    assert len(m['files'])==len(PAYLOAD) and {e['path'] for e in m['files']}==PAYLOAD
    for e in m['files']:assert meta((root/e['path']).read_bytes())=={k:e[k] for k in ('bytes','sha256')},e['path']
    with tempfile.TemporaryDirectory(prefix='kahler-replay-') as d:
        output=pathlib.Path(d)/'math.json';subprocess.run([sys.executable,str(root/'verify_math.py'),'--output',str(output)],cwd=d,check=True,stdout=subprocess.DEVNULL)
        assert output.read_bytes()==(root/'MATH_RESULTS.json').read_bytes(),'nonidentical arithmetic replay'
    print(json.dumps({'status':'PASS','payload_files_verified':len(PAYLOAD),'manifest_sha256':mh,'math_replay':'byte-identical','source_scope':'Source hashes recorded; source-byte verification is a separate optional invocation.'},indent=2))
if __name__=='__main__':main()
