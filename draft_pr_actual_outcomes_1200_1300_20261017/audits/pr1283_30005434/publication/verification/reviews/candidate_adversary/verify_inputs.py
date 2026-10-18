#!/usr/bin/env python3
"""Check captured bytes and public-side ledger consistency, never historical originals."""
import hashlib
import json
from pathlib import Path
import sys

class InputError(Exception):
    pass

def require(ok,msg):
    if not ok:
        raise InputError(msg)

def h(b):
    return hashlib.sha256(b).hexdigest()

def main():
    here=Path(__file__).resolve().parent
    receipts=json.loads((here/'INPUT_RECEIPTS.json').read_text())
    for row in receipts['files']:
        data=Path(row['absolute_path']).read_bytes()
        require(len(data)==row['bytes'] and h(data)==row['sha256'],'input receipt mismatch '+row['absolute_path'])
        if 'git_blob_sha1' in row:
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(blob==row['git_blob_sha1'],'git blob mismatch')
    A=here.parent.parent
    snapshot=(A/'SUBMITTED_SNAPSHOT.json').read_bytes()
    require(h(snapshot)==receipts['snapshot_sha256'],'snapshot pin mismatch')
    s=json.loads(snapshot)
    require(s['head']==receipts['original_head'] and s['parents']==receipts['parents'],'snapshot identity mismatch')
    for row in s['files']:
        data=(A/row['local_path']).read_bytes()
        require(len(data)==row['bytes'] and h(data)==row['sha256'],'snapshot file mismatch')
    submitted=A/'submitted'
    manifest=json.loads((submitted/'MANIFEST.json').read_text())
    require(sorted(manifest['allowlist'])==sorted(p.name for p in submitted.iterdir() if p.is_file()),'submitted allowlist mismatch')
    for row in manifest['files']:
        data=(submitted/row['file']).read_bytes()
        require(len(data)==row['bytes'] and h(data)==row['sha256'],'submitted manifest mismatch')
    require(len(manifest['files'])==manifest['covered_file_count'],'manifest count')
    require(sum(row['bytes'] for row in manifest['files'])==manifest['covered_bytes'],'manifest byte count')
    ledger=json.loads((submitted/'BYTE_PRESERVATION.json').read_text())
    segments=0
    for row in ledger['files']:
        data=(submitted/row['file']).read_bytes()
        require(len(data)==row['public']['bytes'] and h(data)==row['public']['sha256'],'ledger public whole-file mismatch')
        ranges={key:[] for key in ['original','public']}
        for unchanged in row['unchanged_regions']:
            a,b=unchanged['public_range']
            require(b-a==unchanged['bytes'] and h(data[a:b])==unchanged['sha256'],'unchanged public region mismatch')
            require(unchanged['original_range'][1]-unchanged['original_range'][0]==unchanged['bytes'],'unchanged original length inconsistency')
            for key in ranges:
                ranges[key].append(unchanged[key+'_range'])
            segments+=1
        for edit in row['editorial_changes']:
            a,b=edit['public_range']
            require(b-a==edit['replacement_bytes'] and h(data[a:b])==edit['replacement_sha256'],'replacement public region mismatch')
            require(edit['original_range'][1]-edit['original_range'][0]==edit['original_bytes'],'edit original length inconsistency')
            for key in ranges:
                ranges[key].append(edit[key+'_range'])
            segments+=1
        for key,rs in ranges.items():
            position=0
            for a,b in sorted(rs):
                require(a==position and b>=a,'ledger range gap or overlap '+key)
                position=b
            require(position==row[key]['bytes'],'ledger range total mismatch')
    for row in ledger['named_unchanged_regions']:
        data=(submitted/row['file']).read_bytes();a,b=row['public_range']
        require(b-a==row['bytes'] and h(data[a:b])==row['sha256'],'named public region mismatch')
        require(row['original_range'][1]-row['original_range'][0]==row['bytes'],'named original region length')
    print(json.dumps({'status':'PASS','snapshot':'authenticated','captured_submitted_files':len(s['files']),'captured_submitted_bytes':sum(r['bytes'] for r in s['files']),'receipted_inputs':len(receipts['files']),'public_ledger_segments_checked':segments,'named_public_regions_checked':len(ledger['named_unchanged_regions']),'historical_originals':'NOT VERIFIED: earlier original bytes and finite-check scripts absent from captured packet','source_chronology_and_priority':'NOT ASSESSED'},sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:
        main()
    except (InputError,OSError,ValueError,KeyError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},sort_keys=True,separators=(',',':')))
        sys.exit(2)
