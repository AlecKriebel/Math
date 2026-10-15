#!/usr/bin/env python3
"""Create/read back the exact compact support ZIP; Python 3.9+, standard library.
Refuses overwrite; validates each member before building.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
import hashlib
import json
import zipfile

MEMBERS=("LICENSE-CODE.txt","LICENSE-TEXT.md","README.md","SHA256SUMS",
         "SOURCE_QUALIFICATIONS.md","VERIFICATION_PROVENANCE.json","VERIFICATION_RECORD.json",
         "build_verification_zip.py","integer_endpoint_discontinuity.tex","expected_results.json","verify_integer_endpoint.py")
BASE=Path(__file__).absolute().parent
DEST=BASE/'integer-endpoint-discontinuity-verification-v1.zip'


def main():
    if DEST.exists() or DEST.is_symlink():raise ValueError('Refusing overwrite of existing archive')
    expected={}
    for row in (BASE/'SHA256SUMS').read_text(encoding='ascii').splitlines():
        digest,name=row.split('  ',1)
        if name in expected or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('Invalid checksum row')
        expected[name]=digest
    if set(expected)!=set(MEMBERS)-{'SHA256SUMS'}:raise ValueError('Exact checksum member domain')
    bodies={}
    for name in MEMBERS:
        q=BASE/name
        if q.is_symlink() or not q.is_file():raise ValueError('Regular member required: '+name)
        b=q.read_bytes()
        if name!='SHA256SUMS' and hashlib.sha256(b).hexdigest()!=expected[name]:raise ValueError('Exact member hash: '+name)
        bodies[name]=b
    with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in MEMBERS:
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,bodies[name],compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(DEST,'r') as archive:
        if archive.namelist()!=list(MEMBERS) or archive.testzip() is not None:raise ValueError('Exact archive topology/CRC')
        for name in MEMBERS:
            if archive.read(name)!=bodies[name]:raise ValueError('Exact member readback')
    b=DEST.read_bytes()
    print(json.dumps({'status':'PASS_ARCHIVE_BUILD_AND_EXACT_MEMBER_READBACK','name':DEST.name,'members':len(MEMBERS),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},indent=2,sort_keys=True))


if __name__=='__main__':main()
