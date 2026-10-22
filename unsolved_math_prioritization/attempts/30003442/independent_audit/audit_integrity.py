#!/usr/bin/env python3
"""Pinned author-package integrity and bounded adversarial corruption tests."""
import argparse,hashlib,json,shutil,tempfile,zipfile
from pathlib import Path
PIN='388e9f7d81f3c5f13dac355b43721a65bd408cfa5b25c0d61b356c96c8a094ff'
MANIFEST_PIN='bbc539d32efaccd64ea3918b44e79270cb586a153062643b50d6e8d8024bdf11'
NAMES={'MANIFEST.json','PROOF.md','README.md','RESEARCH_LOG.md','SOURCE_METADATA.json','audit_checks.json','audit_manifest.py','requirements.txt','selftest.json','verification.json','verify.py'}
class IntegrityFailure(Exception):pass

def require(ok,msg):
    if not ok:raise IntegrityFailure(msg)

def digest(data):return hashlib.sha256(data).hexdigest()

def check(root,archive=None):
    require(root.is_dir() and not root.is_symlink(),'root must be a real directory')
    require({p.name for p in root.iterdir()}==NAMES,'exact flat allowlist')
    for name in NAMES:require((root/name).is_file() and not (root/name).is_symlink(),'regular non-symlink input: '+name)
    manifest=(root/'MANIFEST.json').read_bytes()
    require(digest(manifest)==MANIFEST_PIN,'externally pinned manifest')
    j=json.loads(manifest)
    require(set(j['files'])==NAMES-{'MANIFEST.json'},'manifest entries')
    require(j['problem_id']=='30003442' and j['status']=='partial; unrestricted target unresolved','retained status')
    for name,entry in j['files'].items():
        data=(root/name).read_bytes()
        require(len(data)==entry['bytes'],'byte count: '+name)
        require(digest(data)==entry['sha256'],'digest: '+name)
    if archive is not None:
        require(archive.is_file() and not archive.is_symlink(),'regular archive')
        data=archive.read_bytes();require(len(data)==24172 and digest(data)==PIN,'externally pinned archive')
        with zipfile.ZipFile(archive) as z:
            infos=z.infolist();require(len(infos)==len(NAMES),'no duplicate archive members')
            require({i.filename for i in infos}==NAMES,'archive flat allowlist')
            for info in infos:require(z.read(info)==(root/info.filename).read_bytes(),'archive member equality')
    return {'status':'PASS','safe_files':len(NAMES),'manifest_sha256':MANIFEST_PIN,'archive_sha256':PIN if archive else None}

def adversarial(root):
    out=[]
    def rejects(label,change):
        with tempfile.TemporaryDirectory(prefix='stable-roots-independent-') as temp:
            dst=Path(temp)/'safe';shutil.copytree(root,dst);change(dst)
            try:check(dst)
            except (IntegrityFailure,ValueError,KeyError,FileNotFoundError,json.JSONDecodeError):out.append(label);return
            raise IntegrityFailure('accepted corrupt package: '+label)
    for name in sorted(NAMES):rejects('alter '+name,lambda p,n=name:(p/n).write_bytes((p/n).read_bytes()+b'\n'))
    rejects('delete proof',lambda p:(p/'PROOF.md').unlink())
    rejects('unexpected PDF',lambda p:(p/'source.pdf').write_bytes(b'excluded'))
    rejects('unexpected hidden file',lambda p:(p/'.hidden').write_text('excluded'))
    rejects('unexpected directory',lambda p:(p/'nested').mkdir())
    def link(p,name):
        (p/name).unlink();(p/name).symlink_to(p/'README.md')
    rejects('symlink proof',lambda p:link(p,'PROOF.md'))
    rejects('symlink manifest',lambda p:link(p,'MANIFEST.json'))
    def altered_with_rehashed_manifest(p):
        f=p/'PROOF.md';f.write_bytes(f.read_bytes()+b'\n')
        mf=p/'MANIFEST.json';j=json.loads(mf.read_text());j['files']['PROOF.md']={'bytes':f.stat().st_size,'sha256':digest(f.read_bytes())};mf.write_text(json.dumps(j))
    rejects('self-consistent altered proof and manifest',altered_with_rehashed_manifest)
    def traversal(p):
        f=p/'MANIFEST.json';j=json.loads(f.read_text());j['files']['../escape']={};f.write_text(json.dumps(j))
    rejects('manifest path traversal',traversal)
    return out

def main():
    a=argparse.ArgumentParser();a.add_argument('--author',type=Path,required=True);a.add_argument('--archive',type=Path);a.add_argument('--self-test',action='store_true');a.add_argument('--output',type=Path);q=a.parse_args()
    result=check(q.author,q.archive)
    if q.self_test:result['corruptions_rejected']=adversarial(q.author);result['corruption_count']=len(result['corruptions_rejected'])
    value=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if q.output:q.output.write_text(value)
    else:print(value,end='')
if __name__=='__main__':main()
