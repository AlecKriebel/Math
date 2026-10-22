"""Deterministic local packaging from the frozen reviewed source and PDF.

No network, credentials, DOI allocation or service operations. This copies
paper.pdf; it does not independently typeset main.tex or establish a theorem.
"""
from pathlib import Path
import hashlib
import json
import shutil
import stat
import sys
import zipfile

SOURCE_PREFIX = 'free_chain_nash_intersections_source'
STEM = 'free-chain-nash-intersections'
STAMP = (2026, 10, 22, 0, 0, 0)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'source must be an actual directory')
    rows = {}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'source symlink forbidden')
        if p.is_file():
            require(stat.S_ISREG(p.stat().st_mode), 'nonregular source')
            n = p.relative_to(root).as_posix()
            if n == 'PUBLIC_MANIFEST.json':
                continue
            b = p.read_bytes()
            rows[n] = {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    return rows


def validate(root):
    expected = json.loads((root/'PUBLIC_MANIFEST.json').read_text())
    require(expected['schema']=='free-chain-nash-public-files-v1', 'wrong manifest schema')
    require(set(expected)=={'schema','files','scope'}, 'unknown manifest field')
    actual = inventory(root)
    require(actual==expected['files'], 'source bytes or complete membership differ')
    return actual


def zip_bytes(path, members):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.create_system = 3
            info.external_attr = (stat.S_IFREG|0o644)<<16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)


def build(root, out):
    root = root.resolve(); out = out.resolve()
    require(out!=root and root not in out.parents,'output cannot be inside source')
    members = validate(root)
    out.mkdir(parents=True,exist_ok=True)
    require(not list(out.iterdir()),'output must be empty to protect existing work')
    source_members = {SOURCE_PREFIX+'/'+name:(root/name).read_bytes() for name in [*members,'PUBLIC_MANIFEST.json']}
    for origin, target in [('paper.pdf',STEM+'.pdf'),('zenodo-metadata.json','zenodo-metadata.json'),('zenodo-deposit.json','zenodo-deposit.json'),('UPLOAD_README.txt','UPLOAD_README.txt')]:
        shutil.copyfile(root/origin,out/target)
    source_zip = STEM+'-source-and-verification.zip'
    zip_bytes(out/source_zip,source_members)
    kit_names=[STEM+'.pdf',source_zip,'zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt']
    zip_bytes(out/(STEM+'-upload-kit.zip'),{name:(out/name).read_bytes()for name in kit_names})
    return [{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(out.iterdir())]


if __name__=='__main__':
    require(len(sys.argv)==2,'usage: python3 build_package.py EMPTY_OUTPUT_DIRECTORY')
    print(json.dumps({'status':'PASS','frozen_pdf_copied_not_typeset':True,'files':build(Path(__file__).resolve().parent,Path(sys.argv[1]))},sort_keys=True,indent=2))
