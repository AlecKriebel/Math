#!/usr/bin/env python3
"""Fetch the publication-tag TeX, without treating it as the DOI archive.

Fails if the bytes do not match the observed Git blob. Existing frozen files
are never silently replaced. DOI-version identity is a separate obligation.
"""
import hashlib, json, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SHA='b575b59086c1f9756c4c65991f6aa8905a73304e'
BLOB='841503aca7ff13677f868ce77b7f3972efeb5556'
URL=f'https://raw.githubusercontent.com/AlecKriebel/Math/{SHA}/kourovka_16_63/report/kourovka_16_63.tex'
DEST=ROOT/'reference/publication_tag_v1.1.0.tex'

def main():
    try:
        if DEST.exists(): data=DEST.read_bytes()
        else:
            with urllib.request.urlopen(URL,timeout=20) as response: data=response.read()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!=BLOB: raise RuntimeError(f'Git blob mismatch: expected {BLOB}, obtained {blob}')
        if not DEST.exists(): DEST.write_bytes(data)
        result={'status':'tagged_source_bytes_verified','url':URL,'git_blob':blob,
                'sha256':hashlib.sha256(data).hexdigest(),'doi_identity_verified':False}
        rc=0
    except Exception as ex:
        result={'status':'source_acquisition_failed','url':URL,'error':str(ex),
                'doi_identity_verified':False}; rc=1
    (ROOT/'logs/source_acquisition.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return rc

if __name__=='__main__': raise SystemExit(main())
