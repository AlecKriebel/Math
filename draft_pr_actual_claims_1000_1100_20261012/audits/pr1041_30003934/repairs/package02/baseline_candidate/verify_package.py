#!/usr/bin/env python3
"""Exact integrity/provenance check; not a mathematical theorem verifier."""
import sys
sys.dont_write_bytecode=True
import gzip,hashlib,json,re,struct,tarfile,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def require(test,message):
    if not test:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def record_ok(path,record):
    data=path.read_bytes()
    require(len(data)==record['bytes'] and sha(data)==record['sha256'],'Hash/size mismatch: '+str(path))

def main():
    manifest=json.loads((ROOT/'CURRENT_INTEGRITY.json').read_text())
    current={r['path']:r for r in manifest['files']}
    from build_archive import content_paths,EXCLUDE_DIRS
    require(set(current)==set(content_paths()),'Current manifest/content membership mismatch')
    for name,record in current.items():record_ok(ROOT/name,record)
    # No privately retained sources, extracts, renders, or raw response bodies in
    # the declared distributed content, including files outside raw directories.
    copies=json.loads((ROOT/'EVIDENCE_COPY_MANIFEST.json').read_text())
    authored_streams={r['package_path'] for r in copies['files'] if r['group']=='frozen_package_01' and r['package_path'].endswith(('_stdout.txt','_stderr.txt'))}
    for name in current:
        path=Path(name)
        require(not any(p in EXCLUDE_DIRS for p in path.parts),'Private/intermediate component: '+name)
        require(path.suffix.lower() not in {'.png','.jpg','.jpeg','.gif','.webp','.pyc'},'Private/intermediate suffix: '+name)
        require(path.suffix.lower()!='.txt' or name in authored_streams,'Unapproved text stream/source extract: '+name)
        require(path.name.lower()!='fullsource.txt','Source extract outside raw: '+name)
        require(path.suffix.lower()!='.pdf' or name=='output/pdf/paper.pdf','Third-party PDF: '+name)
        require('CITATION_DISCOVERY' not in name,'Raw discovery response dump: '+name)
    for record in copies['files']:record_ok(ROOT/record['package_path'],record)
    require(sum(r['group']=='frozen_original_11' for r in copies['files'])==11,'Original eleven-file count')
    pins=json.loads((ROOT/'evidence/root/SUBMITTED_PINS.json').read_text())
    for r in pins['files']:record_ok(ROOT/'evidence/original'/r['snapshot_path'],r)
    require(len(pins['files'])==11,'Original submitted pin count')
    checked_historic=0;excluded_historic=[]
    for family in ['game_certificate_01','flow_source_01','priority_01','package_01']:
        base=ROOT/'evidence/reviews'/family
        pins=json.loads((base/'OUTPUT_PINS.json').read_text())
        for r in pins.get('files',pins.get('entries',[])):
            name=r.get('path',r.get('file'));path=base/name
            if path.is_file():record_ok(path,r);checked_historic+=1
            else:excluded_historic.append(family+'/'+name)
    for name in excluded_historic:
        parts=Path(name).parts
        allowed=any(p in {'raw','rawprivate','__pycache__','render','cache','caches'} for p in parts) or name=='priority_01/sources/CITATION_DISCOVERY.json'
        require(allowed,'Unexpected historic output pin absent: '+name)
    receipt=json.loads((ROOT/'BUILD_RECEIPT.json').read_text())
    require(receipt['current_integrity_sha256']==sha((ROOT/'CURRENT_INTEGRITY.json').read_bytes()),'Integrity receipt mismatch')
    require(receipt['content_files']==len(current),'Content count mismatch')
    archive=ROOT/receipt['archive_name'];archive_checked=False;members=0
    if archive.exists():
        sidecar=json.loads((ROOT/'ARCHIVE_SHA256.json').read_text());record_ok(archive,sidecar)
        require(sidecar['current_integrity_sha256']==sha((ROOT/'CURRENT_INTEGRITY.json').read_bytes()),'Archive integrity sidecar')
        require(sidecar['build_receipt_sha256']==sha((ROOT/'BUILD_RECEIPT.json').read_bytes()),'Build receipt sidecar')
        expected=set(current)|{'CURRENT_INTEGRITY.json','BUILD_RECEIPT.json'}
        raw=archive.read_bytes()
        require(raw[:3]==b'\x1f\x8b\x08' and raw[3]==0 and raw[4:8]==b'\x00'*4,'Gzip header/mtime/optional fields')
        expanded=gzip.decompress(raw)
        crc,isize=struct.unpack('<II',raw[-8:])
        require(crc==zlib.crc32(expanded)&0xffffffff and isize==len(expanded)&0xffffffff,'Gzip CRC/isize')
        with tarfile.open(archive,'r:gz') as tar:
            allmembers=tar.getmembers();names=[]
            for member in allmembers:
                require(member.isfile(),'Non-file archive member')
                require(member.name.startswith(receipt['archive_prefix']),'Archive prefix')
                name=member.name[len(receipt['archive_prefix']):];names.append(name)
                require(re.fullmatch(r'[A-Za-z0-9_.\-/]+',name) is not None and not name.startswith('/') and all(p not in {'','..','.'} for p in name.split('/')),'Unsafe archive path: '+name)
                require(name in expected,'Unexpected archive member: '+name)
                require(tar.extractfile(member).read()==(ROOT/name).read_bytes(),'Archive/local mismatch: '+name)
                require(member.mtime==receipt['epoch'] and member.uid==member.gid==0 and member.mode==0o644 and member.uname==member.gname=='','Archive metadata mismatch')
            require(set(names)==expected and len(names)==len(expected),'Archive membership mismatch')
            require(names==sorted(names) and len({n.casefold() for n in names})==len(names),'Archive order/casefold uniqueness')
            members=len(names)
        archive_checked=True
    status=json.loads((ROOT/'STATUS.json').read_text())
    require(isinstance(status['publication_ready'],bool) and isinstance(status['all_issues_resolved'],bool),'Invalid current status flags')
    if status['new_whole_package_review'].startswith('PENDING_'):
        require(status['publication_ready'] is False and status['all_issues_resolved'] is False,'Pending review improperly promoted')
    require(receipt['status']=='PREPARED_CANDIDATE_'+status['new_whole_package_review'] and receipt['publication_ready']==status['publication_ready'] and receipt['all_issues_resolved']==status['all_issues_resolved'],'Build/state mismatch')
    wrapper=json.loads((ROOT/'zenodo-deposit.json').read_text())
    metadata=json.loads((ROOT/'publication/zenodo.json').read_text())
    require(wrapper['metadata']==metadata,'External wrapper metadata mismatch')
    require(wrapper['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'supportkit-v1.0.tar.gz','name':'supportkit-v1.0.tar.gz'}],'External wrapper file binding mismatch')
    require('zenodo-deposit.json' not in current,'Archive wrapper self-reference')
    for entry in wrapper['files']:
        require((ROOT/entry['path']).is_file(),'Missing local upload attachment')
    result=dict(status='PASS_INTEGRITY_PROVENANCE_AND_EXCLUSIONS',content_files=len(current),copied_authored_records=len(copies['files']),original_files_verified=11,historic_output_pin_members_verified=checked_historic,intentionally_excluded_historic_pin_members=excluded_historic,archive_checked=archive_checked,archive_members=members,gzip_crc_isize_verified=True,safe_sorted_casefold_unique_paths=True,external_wrapper_metadata_and_files_verified=True,mathematical_proof_formally_verified=False,new_whole_package_review=status['new_whole_package_review'],publication_ready=status['publication_ready'],all_issues_resolved=status['all_issues_resolved'])
    (ROOT/'VERIFICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
