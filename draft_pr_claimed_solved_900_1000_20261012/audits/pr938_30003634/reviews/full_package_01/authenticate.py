"""Read-only, actual Git/disk/archive authentication for PR938 review."""
import datetime, hashlib, json, pathlib, stat, subprocess, zipfile

R=pathlib.Path('/Users/alec/Documents/Math')
A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr938_30003634'
D=A/'publication'
C=D/'reviewed_candidates/candidate01'
O=A/'reviews/full_package_01'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
PREFIX='unsolved_math_prioritization/attempts/30003634/'
FREEZE='a7fae8c5b9364251b80d470859f8b34339be679fa52f853e032e2db03713c536'
MANIFEST='7aa302b1ad5242fe03c576b68bf19af825e135f9aa1b296056cd4587c54ae51e'
def sha(b): return hashlib.sha256(b).hexdigest()
def require(c,s):
    if not c: raise RuntimeError(s)
def regular(p):
    require(stat.S_ISREG(p.lstat().st_mode),'nonregular '+str(p))
    return p.read_bytes()
def main(label,output=None):
    raw=regular(C/'PREPUBLICATION_FREEZE.json'); require(sha(raw)==FREEZE,'freeze pin')
    f=json.loads(raw); snapshots=json.loads(regular(A/'ORIGINAL_SNAPSHOT.json'))
    out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,
         'freeze_sha256':sha(raw),'original_pr_head':HEAD,'originals':{},'candidate_files':{},'future_helpers':{}}
    require(regular(D/'PREPUBLICATION_FREEZE.json')==raw,'current freeze drift')
    for n,meta in f['files'].items():
        b=regular(C/n); require({'bytes':len(b),'sha256':sha(b)}==meta,n)
        require(regular(D/n)==b,'current candidate drift '+n)
        out['candidate_files'][n]=meta
    for n,meta in f['future_helpers'].items():
        b=regular(C/'future_helpers'/n); require({'bytes':len(b),'sha256':sha(b)}==meta,n)
        require(regular(A.parent.parent/n)==b,'current helper drift '+n)
        out['future_helpers'][n]=meta
    z=zipfile.ZipFile(C/'deep-derived-pure-braids-source-verification-v1.0.zip')
    names=z.namelist(); require(len(names)==len(set(names)),'duplicate archive member')
    require(len(names)==201,'archive count')
    require(all(stat.S_ISREG(i.external_attr>>16) for i in z.infolist()),'Nonregular archive member')
    rawmanifest=z.read('PACKAGE_MANIFEST.json'); require(sha(rawmanifest)==MANIFEST,'manifest pin')
    manifest=json.loads(rawmanifest); require(len(manifest['files'])==200,'payload count')
    require(set(names)==set(manifest['files'])|{'PACKAGE_MANIFEST.json'},'closed archive inventory')
    for n,meta in manifest['files'].items():
        p=pathlib.PurePosixPath(n)
        require(not p.is_absolute() and all(t not in ('.','..') for t in p.parts),'unsafe archive member')
        b=z.read(n); require({'bytes':len(b),'sha256':sha(b)}==meta,'archive fingerprint '+n)
        require(stat.S_ISREG(z.getinfo(n).external_attr>>16),'archive nonregular '+n)
    tree=subprocess.check_output(['git','ls-tree','-rz',HEAD,'--',PREFIX],cwd=R).split(b'\0')
    for rec in tree:
        if not rec: continue
        left,path=rec.split(b'\t',1); mode,kind,oid=left.decode().split(); path=path.decode()
        require(mode=='100644' and kind=='blob','unexpected original mode')
        b=subprocess.check_output(['git','cat-file','blob',oid],cwd=R)
        require(sha(b)==snapshots['files'][path],'inventory mismatch '+path)
        disk=A/'original'/path; require(regular(disk)==b,'disk original mismatch '+path)
        require((disk.stat().st_mode & 0o111)==0,'disk original executable mode')
        require(stat.S_IMODE(disk.stat().st_mode)==0o644,'disk original permission mode')
        archived='original_packet/'+path[len(PREFIX):]
        require(z.read(archived)==b,'archive original mismatch '+path)
        require((z.getinfo(archived).external_attr>>16)&0o777==0o644,'archive original mode')
        out['originals'][path]={'git_blob':oid,'git_mode':mode,'disk_mode':'0644','archive_mode':'100644','bytes':len(b),'sha256':sha(b),'disk_and_archive_match':True}
    require(len(out['originals'])==44 and set(out['originals'])==set(snapshots['files']),'original count')
    out['archive_members']=len(names); out['payloads']=len(manifest['files']);out['package_manifest_sha256']=MANIFEST
    out['status']='PASS'
    rendered=json.dumps(out,indent=2)+'\n'
    if output: pathlib.Path(output).write_text(rendered)
    print(rendered,end='')
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('label');ap.add_argument('--output');args=ap.parse_args()
    main(args.label,args.output)
