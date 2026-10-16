#!/usr/bin/env python3
"""Independent read-only freeze/ZIP/original authentication and extraction."""
import hashlib, json, pathlib, stat, subprocess, zipfile
from datetime import datetime, timezone

HERE=pathlib.Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
PUBLICATION=AUDIT/'publication'
EXPECTED_FREEZE='400dd39f443ad2bf42f8e0231bf411002f409e43877f3b1a24f3ca3ca1d06643'
EXPECTED_MANIFEST='ec577f92be60547f1d83d07d3037aeee7b4c1cde4ddd1007076a8ede28928794'
HEAD='a35667b1bb0bafed69916709997a4684223ecc93'
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(data): return hashlib.sha256(data).hexdigest()
def strict(data):
    def pairs(items):
        out={}
        for k,v in items:
            require(k not in out,'duplicate JSON key')
            out[k]=v
        return out
    return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--label',default='start');ap.add_argument('--extract',action='store_true');args=ap.parse_args()
    frozen=(PUBLICATION/'PREPUBLICATION_FREEZE.json').read_bytes()
    require(sha(frozen)==EXPECTED_FREEZE,'freeze bytes changed')
    f=strict(frozen);checked={}
    for name,record in f['files'].items():
        p=PUBLICATION/name;require(stat.S_ISREG(p.lstat().st_mode),'nonregular candidate')
        d=p.read_bytes();require({'bytes':len(d),'sha256':sha(d)}==record,'frozen file changed: '+name);checked[name]=record
    archive=PUBLICATION/'bounded-region-fermions-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();require(len(names)==len(set(names))==107,'ZIP duplicates/count')
        require(all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in names),'unsafe zip path')
        mraw=z.read('PACKAGE_MANIFEST.json');require(sha(mraw)==EXPECTED_MANIFEST,'manifest mismatch')
        m=strict(mraw);require(set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'ZIP closed inventory')
        for n,r in m['files'].items():
            info=z.getinfo(n);require(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'ZIP nonregular')
            d=z.read(n);require({'bytes':len(d),'sha256':sha(d)}==r,'ZIP payload mismatch: '+n)
        require(z.read('note.pdf')==(PUBLICATION/'output/pdf/note.pdf').read_bytes(),'PDF copy mismatch')
        orig={n:r for n,r in m['files'].items() if n.startswith('original_packet/')}
        require(len(orig)==26,'original count mismatch')
        git_checked=0
        for n,r in orig.items():
            rel=n.removeprefix('original_packet/')
            live=AUDIT/'original/unsolved_math_prioritization/attempts/30006191/bounded_region_v2'/rel
            require(live.read_bytes()==z.read(n),'disk original changed: '+n)
            gp='unsolved_math_prioritization/attempts/30006191/bounded_region_v2/'+rel
            proc=subprocess.run(['git','show',HEAD+':'+gp],capture_output=True,check=True)
            require(proc.stdout==z.read(n),'original differs from Git head: '+n);git_checked+=1
        if args.extract:
            out=HERE/'tmp/bundle';out.mkdir(parents=True,exist_ok=True)
            require(not list(out.iterdir()),'bundle destination not empty')
            for n in names:
                dest=out/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(n))
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','freeze_sha256':sha(frozen),'frozen_files_checked':len(checked),'zip_members':len(names),'zip_payloads_checked':len(m['files']),'manifest_sha256':sha(mraw),'original_git_head_files_checked':git_checked,'original_git_head':HEAD,'identical_pdf':True,'files':checked}
    (HERE/('AUTHENTICATION_'+args.label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
if __name__=='__main__': main()
