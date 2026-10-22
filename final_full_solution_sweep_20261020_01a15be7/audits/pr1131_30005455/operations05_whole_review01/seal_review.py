"""Closed recursive seal of this review, including all private/nested evidence."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, stat

ROOT=Path(__file__).resolve().parent
SEAL=ROOT/'MANIFEST.json'
LIMIT=150*1024*1024
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()

def inventory():
    rs=ROOT.stat()
    files={};directories={};cache={};seen={(rs.st_dev,rs.st_ino)};allocated=rs.st_blocks*512
    for parent,dirs,names in os.walk(ROOT,followlinks=False):
        for name in dirs+names:
            p=Path(parent)/name;rel=p.relative_to(ROOT).as_posix();s=p.lstat()
            need(not stat.S_ISLNK(s.st_mode),'Symlink in closed review')
            inode=s.st_dev,s.st_ino
            if inode not in seen:allocated+=s.st_blocks*512;seen.add(inode)
            if stat.S_ISDIR(s.st_mode):
                directories[rel]={'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
                continue
            need(stat.S_ISREG(s.st_mode),'Nonregular review evidence')
            if p==SEAL:continue
            key=s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns
            if key not in cache:cache[key]=sha(p.read_bytes())
            after=p.stat()
            need((after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)==key,'Evidence changed while sealing')
            files[rel]={'bytes':s.st_size,'sha256':cache[key],
                        'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
    need(allocated<=LIMIT,'Review exceeds allocated150MiB cap')
    return dict(sorted(files.items())),dict(sorted(directories.items())),allocated

def verify(expected=None):
    raw=SEAL.read_bytes()
    if expected is not None:need(sha(raw)==expected,'External review seal anchor mismatch')
    report=json.loads(raw)
    need(report['excluded_files']==['MANIFEST.json']
         and report['excluded_directories']==[],'Unexpected review exclusion')
    files,dirs,size=inventory()
    need(files==report['files'] and dirs==report['directories'],'Complete review closure/bytes/metadata mismatch')
    need(report['file_count']==len(files) and report['directory_count']==len(dirs),'Review counts mismatch')
    need(report['allocated_bytes_after_seal']==size<=LIMIT,'Review allocated size mismatch')
    return {'status':'PASS','manifest_bytes':len(raw),'manifest_sha256':sha(raw),
            'files':len(files),'directories':len(dirs),'allocated_bytes':size,
            'cap_bytes':LIMIT,'all_nested_manifests_and_private_evidence_included':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true')
    p.add_argument('--expected-sha256');a=p.parse_args()
    if not a.verify_only:
        need(not SEAL.exists(),'Existing complete review seal must not be overwritten')
        files,dirs,size=inventory()
        out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'schema':'complete_recursive_review_custody_v1','excluded_files':['MANIFEST.json'],
             'excluded_directories':[],'file_count':len(files),'directory_count':len(dirs),
             'files':files,'directories':dirs,'allocated_bytes_after_seal':size,
             'allocated_cap_bytes':LIMIT,'service_mutations':0,
             'scope':'All own reviewed source copies, reports, nested manifests, logs, code, raw private captures and generated model evidence. Only this exact self seal is excluded.'}
        with SEAL.open('xb') as f:
            f.write((json.dumps(out,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
        for _ in range(8):
            _,_,actual=inventory()
            if out['allocated_bytes_after_seal']==actual:break
            out['allocated_bytes_after_seal']=actual
            with SEAL.open('wb') as f:
                f.write((json.dumps(out,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
        else:raise RuntimeError('Seal allocated-size fixed point failed')
        fd=os.open(ROOT,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    print(json.dumps(verify(a.expected_sha256),indent=2))
if __name__=='__main__':main()
