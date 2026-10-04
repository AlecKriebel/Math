#!/usr/bin/env python3
"""Strict portable release inventory, integrity and assertion-enabled replay."""
import argparse, hashlib, json, pathlib, subprocess, sys, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
EXPECTED={'safe/tests/verify_packet.py', 'safe/TEST_RESULTS.json', 'revision-v2/independent-audit/AUDITED_INPUTS.json', 'rank658-30000576-independent-audit.zip', 'safe/TARGET.json', 'README.md', 'independent-audit/AUDIT.md', 'independent-audit/TEST_RESULTS.json', 'revision-v2/independent-audit/SOURCE_CHECKS.json', 'revision-v2/independent-audit/AUDIT_BINDING.json', 'safe/LIMITATIONS.md', 'revision-v2/independent-audit/AUDIT.md', 'revision-v2/safe/APPROACH_LOG.md', 'revision-v2/independent-audit/AUDIT_RESULT.json', 'revision-v2/safe/tests/verify_bridge.py', 'safe/README.md', 'revision-v2/safe/TARGET.json', 'revision-v2/safe/DATASET_VERIFICATION.json', 'revision-v2/safe/EXACT_TEST_RESULTS.json', 'revision-v2/independent-audit/verify_audit.py', 'verify_release.py', 'safe/RESEARCH_LOG.md', 'independent-audit/AUDIT_RESULT.json', 'revision-v2/safe/PRIOR_ATTEMPT_CHECK.json', 'safe/VERIFICATION.md', 'revision-v2/safe/FREEZE_MANIFEST.json', 'revision-v2/safe/tests/verify_packet.py', 'RELEASE_VERIFICATION.json', 'revision-v2/safe/HISTORY_BINDING.json', 'revision-v2/safe/PROOF.md', 'RELEASE_MANIFEST.json', 'revision-v2/safe/PACKET_TEST_RESULTS.json', 'safe/SOURCE_MANIFEST.json', 'revision-v2/safe/SOURCE_MANIFEST.json', 'revision-v2/safe/LIMITATIONS.md', 'revision-v2/independent-audit/TEST_RESULTS.json', 'independent-audit/AUDITED_INPUTS.json', 'independent-audit/SOURCE_CHECKS.json', 'safe/DATASET_VERIFICATION.json', 'independent-audit/AUDIT_BINDING.json', 'revision-v2/safe/README.md', 'revision-v2/rank658-30000576-v2-independent-audit.zip', 'safe/FREEZE_MANIFEST.json', 'independent-audit/verify_audit.py', 'safe/PRIOR_ATTEMPT_CHECK.json'}
DIRECTORIES={'revision-v2/safe/tests', 'safe', 'revision-v2', 'revision-v2/safe', 'independent-audit', 'revision-v2/independent-audit', 'safe/tests'}
ANCHORS={'safe/FREEZE_MANIFEST.json': '23236036135d52baef409a058a8df2cea2792c6faefd5004b669c14abdfa454d', 'independent-audit/AUDIT_BINDING.json': '6579b52abf9493eed085a9c2ae8ad9eea9ab52da2fafa3417d1678127559e85d', 'revision-v2/safe/FREEZE_MANIFEST.json': '0f77ea2dc8653f7680a5709778158b5a4df71811ae9d7a30d5adaefeeb8b2c80', 'revision-v2/independent-audit/AUDIT_BINDING.json': '8d9d81b420e38cdd048fb6f8e458b4cd05d1155a945880c78a74ca593de3663a', 'rank658-30000576-independent-audit.zip': '9f01db767bf67b663c85e373f0f4019b87ee156796ff21693d930382a6983f4d', 'revision-v2/rank658-30000576-v2-independent-audit.zip': '6c62fda923da86e421a7a0b439d3ebcbffaa3708538d4f54702dcf817d365de1'}
def require(value,message):
    if not value:raise SystemExit('Integrity failure: '+message)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--replay',action='store_true');a=p.parse_args()
    files=set();dirs=set()
    for f in ROOT.rglob('*'):
        rel=f.relative_to(ROOT).as_posix()
        require(not f.is_symlink(),'symlink: '+rel)
        if f.is_dir():dirs.add(rel)
        else:
            require(f.is_file(),'nonregular file: '+rel);files.add(rel)
    require(files==EXPECTED,'file inventory');require(dirs==DIRECTORIES,'directory inventory')
    m=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    require(set(m['files'])==EXPECTED-{'RELEASE_MANIFEST.json'},'manifest inventory')
    for rel,meta in m['files'].items():
        b=(ROOT/rel).read_bytes()
        require(len(b)==meta['bytes'] and sha(b)==meta['sha256'],'bytes: '+rel)
    for rel,anchor in ANCHORS.items():require(sha((ROOT/rel).read_bytes())==anchor,'anchor: '+rel)
    for archive,folder in [('rank658-30000576-independent-audit.zip','independent-audit'),('revision-v2/rank658-30000576-v2-independent-audit.zip','revision-v2/independent-audit')]:
        with zipfile.ZipFile(ROOT/archive) as z:
            names=z.namelist()
            require(len(names)==len(set(names))==7,'archive count')
            prefix='' if archive.startswith('revision-v2/') else 'independent-audit/'
            require(set(names)=={prefix+f.name for f in (ROOT/folder).iterdir()},'archive inventory')
            for name in names:require(z.read(name)==(ROOT/folder/pathlib.Path(name).name).read_bytes(),'archive bytes: '+name)
    verified=[]
    if a.replay:
        expected=json.loads((ROOT/'RELEASE_VERIFICATION.json').read_text())['replays']
        for name,rel in [('historical','independent-audit/verify_audit.py'),('revision_2','revision-v2/independent-audit/verify_audit.py')]:
            r=subprocess.run([sys.executable,'-I','-B',str(ROOT/rel)],capture_output=True,text=True)
            require(r.returncode==0,'replay execution: '+rel+' '+r.stderr)
            require(json.loads(r.stdout)==expected[name],'replay result: '+rel)
            verified.append(name)
    print(json.dumps({'status':'pass','release_files':len(files),'safe_archives_verified':2,'replays':verified},sort_keys=True))
if __name__=='__main__':main()
