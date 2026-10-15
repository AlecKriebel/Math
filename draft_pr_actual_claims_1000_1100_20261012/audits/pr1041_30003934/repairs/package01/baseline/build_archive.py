#!/usr/bin/env python3
"""Deterministic local supportkit build; no publication or service operations."""
import sys
sys.dont_write_bytecode=True
import gzip, hashlib, io, json, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ARCHIVE='supportkit-v1.0.tar.gz'
PREFIX='rank_one_uniqueness_v1_0/'
EXCLUDE_NAMES={'CURRENT_INTEGRITY.json','BUILD_RECEIPT.json','ARCHIVE_SHA256.json','VERIFICATION_RECEIPT.json',ARCHIVE}
EXCLUDE_DIRS={'tmp','raw','rawprivate','render','cache','caches','__pycache__','.git'}
EXCLUDE_SUFFIX={'.txt','.png','.jpg','.jpeg','.gif','.webp','.aux','.log','.out','.toc','.pyc'}
EPOCH=1791849600 # 2026-10-13 00:00:00 UTC

def digest(data):return hashlib.sha256(data).hexdigest()
def content_paths():
    result=[]
    for path in ROOT.rglob('*'):
        if not path.is_file():continue
        rel=path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):continue
        if rel.as_posix() in EXCLUDE_NAMES or path.suffix.lower() in EXCLUDE_SUFFIX:continue
        if path.suffix.lower()=='.pdf' and rel.as_posix()!='output/pdf/paper.pdf':continue
        if path.is_symlink():raise RuntimeError('No symlinks in package content: '+str(rel))
        result.append(rel.as_posix())
    return sorted(result)

def main():
    paths=content_paths()
    entries=[]
    for name in paths:
        data=(ROOT/name).read_bytes();entries.append(dict(path=name,bytes=len(data),sha256=digest(data)))
    integrity=dict(hash_algorithm='SHA-256',self_reference_policy='Current distributed content only. This manifest and deterministic build/verification/archive-hash receipts have separate roles.',archive_exclusions=dict(directories=sorted(EXCLUDE_DIRS),suffixes=sorted(EXCLUDE_SUFFIX),other_pdfs=True,external_sidecar='ARCHIVE_SHA256.json'),files=entries)
    blob=(json.dumps(integrity,indent=2)+'\n').encode();(ROOT/'CURRENT_INTEGRITY.json').write_bytes(blob)
    receipt=dict(status='PREPARED_CANDIDATE_PENDING_NEW_WHOLE_01',publication_ready=False,archive_name=ARCHIVE,archive_prefix=PREFIX,content_files=len(entries),current_integrity_sha256=digest(blob),timestamp_policy='2026-10-13 00:00:00 UTC for every tar member; gzip mtime=0',epoch=EPOCH,ordering='sorted relative POSIX paths',owner_group='0/0, empty names',mode='0644',private_source_bodies_included=False,receipt_policy='BUILD_RECEIPT.json is included outside current-integrity self-reference domain; archive binary hash is in external ARCHIVE_SHA256.json.')
    (ROOT/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    archived=paths+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json']
    out=io.BytesIO()
    with gzip.GzipFile(fileobj=out,mode='wb',mtime=0,filename='') as compressed:
        with tarfile.open(fileobj=compressed,mode='w',format=tarfile.PAX_FORMAT) as archive:
            for name in sorted(archived):
                data=(ROOT/name).read_bytes();info=tarfile.TarInfo(PREFIX+name)
                info.size=len(data);info.mtime=EPOCH;info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644
                archive.addfile(info,io.BytesIO(data))
    data=out.getvalue();(ROOT/ARCHIVE).write_bytes(data)
    sidecar=dict(archive=ARCHIVE,bytes=len(data),sha256=digest(data),current_integrity_sha256=digest(blob),build_receipt_sha256=digest((ROOT/'BUILD_RECEIPT.json').read_bytes()),archive_members=len(archived),publication_ready=False)
    (ROOT/'ARCHIVE_SHA256.json').write_text(json.dumps(sidecar,indent=2)+'\n')
    print(json.dumps(sidecar))
if __name__=='__main__':main()
