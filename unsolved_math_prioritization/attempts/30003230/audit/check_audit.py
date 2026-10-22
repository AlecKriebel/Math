#!/usr/bin/env python3
"""Validate safe audit bytes, source-correction preconditions, and exact replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def require(value,message):
    if not value:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=3:raise SystemExit('Usage: check_audit.py AUTHOR_RELEASE AUTHOR_ZIP')
    original=Path(sys.argv[1]).resolve();archive=Path(sys.argv[2]).resolve()
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    require({p.name for p in ROOT.iterdir()}==set(manifest['files'])|{'MANIFEST.json'},'Audit file set differs')
    for name,m in manifest['files'].items():
        p=ROOT/name
        require(p.name==name and p.is_file(),'Unsafe audit member')
        require(len(p.read_bytes())==m['bytes'] and digest(p)==m['sha256'],'Audit member mismatch: '+name)
    correction=json.loads((ROOT/'SOURCE_METADATA_CORRECTION.json').read_text())
    bound=correction['bound_original']
    require(digest(original/'SOURCE_AUDIT.json')==bound['source_audit_sha256'],'Correction does not bind this source record')
    require(digest(original/'MANIFEST.json')==bound['manifest_sha256'],'Correction does not bind this author manifest')
    require(digest(archive)==bound['archive_sha256'] and len(archive.read_bytes())==bound['archive_bytes'],'Correction does not bind this archive')
    source=json.loads((original/'SOURCE_AUDIT.json').read_text())['sources'][0]
    for key,value in correction['superseded_fields'].items():require(source[key]==value,'Overlay precondition mismatch: '+key)
    new=correction['corrected_fields'];old=correction['superseded_fields']
    require(new['pdf_bytes']==old['pdf_bytes'] and new['pdf_sha256']==old['pdf_sha256'],'Correction must not change stored PDF identity')
    records=json.loads((ROOT/'INDEPENDENT_SOURCE_AUDIT.json').read_text())['sources']
    ems=next(r for r in records if r['key']=='OWR_EMS');mfo=next(r for r in records if r['key']=='OWR_MFO')
    require(new['url']==ems['url'] and new['pdf_bytes']==ems['bytes'] and new['pdf_sha256']==ems['sha256'],'Corrected record does not match fresh EMS retrieval')
    require(old['url']==mfo['url'] and mfo['sha256']!=ems['sha256'] and mfo['bytes']!=ems['bytes'],'MFO and EMS must remain separately identified')
    require(correction['general_status']=='unresolved' and correction['mathematical_revision_required'] is False,'Correction scope changed')
    verdict=json.loads((ROOT/'VERDICT.json').read_text())
    require(verdict['authored_frozen_packet_verdict']=='REVISE_REQUIRED' and verdict['corrected_composite_verdict']=='PASS','Source scope verdict lost')
    expected=(ROOT/'INDEPENDENT_RESULTS.json').read_bytes()
    for flags in ([],['-O']):
        p=subprocess.run([sys.executable,*flags,str(ROOT/'independent_verify.py'),str(original),str(archive)],capture_output=True)
        require(p.returncode==0 and not p.stderr and p.stdout==expected,'Independent replay mismatch')
    print(json.dumps({'audit_verified':True,'original_packet_verdict':'REVISE_REQUIRED','corrected_composite_verdict':'PASS','correction':'C1','general_status':'unresolved','independent_checks':json.loads(expected)['total_independent_checks'],'replay_modes':['ordinary','optimized'],'file_count_including_manifest':len(manifest['files'])+1},sort_keys=True,indent=2))

if __name__=='__main__':main()
