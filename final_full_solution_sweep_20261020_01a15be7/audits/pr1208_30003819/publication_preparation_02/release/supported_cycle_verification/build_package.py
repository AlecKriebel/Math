#!/usr/bin/env python3
"""Rebuild the frozen-PDF source ZIP and five-member upload kit locally."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile


def archive(path, members):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(members):
            info = zipfile.ZipInfo(name, date_time=(2026,10,22,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)


def main():
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable,'-B',str(root/'reproduce.py')],check=True,capture_output=True)
    output = root.parent/'output'
    (output/'pdf').mkdir(parents=True,exist_ok=True)
    pdf = (root/'paper.pdf').read_bytes()
    (output/'pdf'/'supported-cycle-bound.pdf').write_bytes(pdf)
    zip_path = output/'supported-cycle-source-and-verification.zip'
    archive(zip_path,[(root.name+'/'+p.relative_to(root).as_posix(),p.read_bytes()) for p in root.rglob('*') if p.is_file()])
    metadata = (root/'zenodo-metadata.json').read_bytes()
    manifest = {'metadata':json.loads(metadata),'files':[{'path':'supported-cycle-bound.pdf','name':'supported-cycle-bound.pdf'},{'path':zip_path.name,'name':zip_path.name}]}
    deposit = (json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode()
    instructions = b'LOCAL UPLOAD KIT. No publication has been performed by this builder.\nThe two scientific files are the PDF and source/verification ZIP.\nMetadata and a portable Zenodo manifest accompany them.\nFresh whole-package review and human-authorized release operations remain separate.\nUse the repository Zenodo tool only after those gates; no DOI is reserved here.\n'
    kit = output/'supported-cycle-zenodo-upload-kit.zip'
    archive(kit,[('supported-cycle-bound.pdf',pdf),(zip_path.name,zip_path.read_bytes()),('zenodo-metadata.json',metadata),('zenodo-deposit.json',deposit),('README.txt',instructions)])
    print(json.dumps({'status':'PASS','frozen_pdf_recompiled':False,'publication_performed':False,'files':[{'name':p.relative_to(output).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [output/'pdf'/'supported-cycle-bound.pdf',zip_path,kit]]},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
