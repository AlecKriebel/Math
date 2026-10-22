#!/usr/bin/env python3
"""Rebuild the source archive and portable five-file upload kit. Does not publish.
Uses the frozen PDF. To revise it, deliberately compile/render/review the TeX first.
"""
import hashlib, json, pathlib, stat, subprocess, sys, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
ZIP='output/finite-warm-thresholds-source-and-verification.zip'
KIT='output/zenodo-upload-kit.zip'
FIXED=['main.tex','README.md','LICENSE.txt','PROVENANCE.json','zenodo-metadata.json','zenodo-deposit.json','build_package.py','output/pdf/finite-warm-thresholds.pdf']

def need(c,s):
    if not c:raise ValueError(s)

def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def archive(path,members):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n,b in sorted(members.items()):
            info=zipfile.ZipInfo(n,(2026,10,21,0,0,0));info.create_system=3;info.external_attr=(stat.S_IFREG|0o644)<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,b,compresslevel=9)
    with zipfile.ZipFile(path) as z:
        need(z.testzip() is None and set(z.namelist())==set(members) and len(z.namelist())==len(members),'rebuilt archive closure')
        for n,b in members.items():need(z.read(n)==b,'rebuilt bytes')


def main():
    names=FIXED+[str(p.relative_to(ROOT)) for folder in ['original','audit','verification'] for p in sorted((ROOT/folder).rglob('*')) if p.is_file()]
    need(len(names)==len(set(names)),'duplicate names')
    members={}
    for n in names:
        p=ROOT/n;need(p.is_file() and not p.is_symlink() and '..' not in pathlib.PurePosixPath(n).parts,'unsafe/missing source '+n);members[n]=p.read_bytes()
    meta=json.loads(members['zenodo-metadata.json']);native=json.loads(members['zenodo-deposit.json']);need(native['metadata']==meta,'native metadata differs')
    manifest={n:pin(b) for n,b in sorted(members.items())};mb=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(ROOT/'SOURCE_MANIFEST.json').write_bytes(mb);members['SOURCE_MANIFEST.json']=mb
    z=subprocess.run([sys.executable,'-B',str(ROOT/'verification/run_checks.py'),'--manifest-sha256',hashlib.sha256(mb).hexdigest()],capture_output=True,text=True,cwd=ROOT)
    need(z.returncode==0,'verification failed: '+z.stderr[-2000:]);result=json.loads(z.stdout)
    archive(ROOT/ZIP,members)
    flat={'metadata':meta,'files':[{'path':pathlib.PurePosixPath(e['path']).name} for e in native['files']]}
    kit={'README.md':members['README.md'],'zenodo-metadata.json':members['zenodo-metadata.json'],'zenodo-deposit.json':(json.dumps(flat,indent=2,ensure_ascii=False)+'\n').encode(),'finite-warm-thresholds.pdf':members['output/pdf/finite-warm-thresholds.pdf'],'finite-warm-thresholds-source-and-verification.zip':(ROOT/ZIP).read_bytes()}
    archive(ROOT/KIT,kit)
    print(json.dumps({'status':'PASS','source_members':len(members),'kit_members':len(kit),'source_zip':pin((ROOT/ZIP).read_bytes()),'kit':pin((ROOT/KIT).read_bytes()),'finite_control_runs':len(result['runs']),'source_manifest_sha256':hashlib.sha256(mb).hexdigest(),'publication_performed':False},sort_keys=True))

if __name__=='__main__':main()
