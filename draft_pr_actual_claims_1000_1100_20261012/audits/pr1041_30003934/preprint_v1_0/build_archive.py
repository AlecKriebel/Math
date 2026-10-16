#!/usr/bin/env python3
"""Deterministic local supportkit build; no publication or service operations."""
import sys
sys.dont_write_bytecode=True
import gzip, hashlib, io, json, re, tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ARCHIVE='supportkit-v1.0.tar.gz'
PREFIX='rank_one_uniqueness_v1_0/'
EXCLUDE_NAMES={'CURRENT_INTEGRITY.json','BUILD_RECEIPT.json','ARCHIVE_SHA256.json','VERIFICATION_RECEIPT.json','zenodo-deposit.json',ARCHIVE}
EXCLUDE_DIRS={'tmp','raw','rawprivate','private','replay','render','rendered','extract','extracted','cache','caches','__pycache__','.git'}
EXCLUDE_SUFFIX={'.txt','.png','.jpg','.jpeg','.gif','.webp','.aux','.log','.out','.toc','.pyc'}
EPOCH=1791849600 # 2026-10-13 00:00:00 UTC

def digest(data):return hashlib.sha256(data).hexdigest()
def require(test,message):
    if not test:raise RuntimeError(message)
def unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON key: '+key)
        result[key]=value
    return result
def read_json(path):return json.loads(path.read_text(),object_pairs_hook=unique_object)
OUTPUT_PIN_HASHES={
    'package_01':'9dd709031e353bd253171a50c988fbce1c67a935e8438a4f52b8ff87f53a9449',
    'package_02':'e775864222e9787782f5e743d216a1a29d4da6778e482859918a63f85d254dd3',
    'package_03':'2f0672d67a1d5fb69cb590ae905ec24d9ab92ffbffe520347ea857c06cf4e7bd',
}
def authored_stream_paths(copies):
    """Allow only exact copied OUTPUT_PINS text members of the three reviews."""
    streams=set()
    for family,expected in OUTPUT_PIN_HASHES.items():
        base=ROOT/'evidence/reviews'/family;pinpath=base/'OUTPUT_PINS.json'
        require(digest(pinpath.read_bytes())==expected,'Historic output-pin identity: '+family)
        pins={r['path']:r for r in read_json(pinpath)['files']}
        for record in copies['files']:
            if record['group']!='frozen_'+family or Path(record['package_path']).suffix.lower()!='.txt':continue
            name=Path(record['package_path']).name
            require(record['package_path']=='evidence/reviews/'+family+'/'+name and record['source_path']=='reviews/'+family+'/'+name,'Authored stream locator: '+name)
            require(name in pins and all(record[k]==pins[name][k] for k in ['bytes','sha256']),'Unpinned authored stream: '+name)
            streams.add(record['package_path'])
    return streams
def terminal_gate():
    """Readiness is bound to the exact accepted whole03 candidate and verdict."""
    status=read_json(ROOT/'STATUS.json')
    require(type(status['publication_ready']) is bool and type(status['all_issues_resolved']) is bool,'Invalid current status flags')
    if status['new_whole_package_review'].startswith('PENDING_'):
        require(status['publication_ready'] is False and status['all_issues_resolved'] is False,'Pending review improperly promoted')
        return status
    require(status['new_whole_package_review']=='FINAL_ZERO_ACTIONABLE_NEW_WHOLE_03_ROOT_ACCEPTED','Unrecognized terminal review status')
    require(status['publication_ready'] is True and status['all_issues_resolved'] is True,'Terminal readiness flags')
    require(status.get('published') is False and type(status.get('ascending_services_held_at')) is int and status['ascending_services_held_at']==1032,'Unpublished held-service state')
    require(type(status.get('fresh_whole_package_reviews')) is int and status['fresh_whole_package_reviews']==3 and type(status.get('minimum_fresh_whole_package_reviews')) is int and status['minimum_fresh_whole_package_reviews']==2,'Fresh whole-review count')
    def zero(counts,label):
        require(type(counts) is dict and set(counts)=={'P0','P1','P2','P3'} and all(type(v) is int and v==0 for v in counts.values()),'Terminal zero severity counts: '+label)
    zero(status.get('terminal_severity_counts'),'status')
    protected={
        'paper.tex':'0ccac52f998823d98c020608c34ec2ad2cbd1d1f54db1815f0a00f898c5258c0',
        'output/pdf/paper.pdf':'3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449',
        'publication/zenodo.json':'fae257794f77515a4e24eacc98cd62b6a767c6f532de5a06b4f2435c74537874',
        'HISTORIC_EXCLUSIONS.json':'0211f0bca2713ff176baa16d28802da5c5fdee9b17e030bd1fa5b7bc6962f889',
        'REVIEW_HISTORY.json':'f8dce9a54186c94ad275a734697ab4b46796cd7f425be115268f9ee0afb2f8d8',
        'evidence/reviews/package_03/REPORT.md':'e6cfc2a4781244afd169c2ed6306bfb2b15f4195a0cdf670d7affaeab63ce57f',
        'evidence/reviews/package_03/VERDICT.json':'5ec3865a3806197f5e05c6c34969dacaf403ea9d86d7fdedb19048298518890e',
        'evidence/reviews/package_03/OUTPUT_PINS.json':OUTPUT_PIN_HASHES['package_03'],
        'evidence/reviews/package_03/SEAL.json':'68474a531debd23f9aca0c3da91acbad188866f88d4ec2995720a3d6aadd3554',
        'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json':'59151cb84aa8a9a15b2d4dfede66b689cff7697f4165562da657efd0f866e803',
    }
    for name,expected in protected.items():
        path=ROOT/name
        require(path.is_file() and not path.is_symlink() and digest(path.read_bytes())==expected,'Terminal accepted/protected identity: '+name)
    verdict=read_json(ROOT/'evidence/reviews/package_03/VERDICT.json')
    root=read_json(ROOT/'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json')
    seal=read_json(ROOT/'evidence/reviews/package_03/SEAL.json')
    zero(verdict['severity_counts'],'verdict');zero(root['severity_counts'],'root adoption')
    require(verdict['review']=='NEW_WHOLE_03' and verdict['status']=='PASS_COMPLETE_CURRENT_MANUSCRIPT_AND_PACKAGE' and verdict['findings']==[] and verdict['required_repairs']==[] and verdict['remaining_mathematical_gap'] is None,'Terminal full-review verdict')
    require(root['status']=='ADOPT_ZERO_ACTIONABLE_WHOLE03_PENDING_TERMINAL_ADMIN_SEAL' and root['root_entire_report_and_verdict_read'] is True and root['outputs_rehashed']==304 and root['fresh_whole_package_reviews']==3,'Terminal root adoption')
    for field,path in [('report_sha256','evidence/reviews/package_03/REPORT.md'),('verdict_sha256','evidence/reviews/package_03/VERDICT.json'),('output_pins_sha256','evidence/reviews/package_03/OUTPUT_PINS.json')]:
        require(root[field]==protected[path] and seal[field]==protected[path],'Terminal root/seal binding: '+field)
    require(seal['terminal'] is True and seal['authored_output_records']==304 and len(read_json(ROOT/'evidence/reviews/package_03/OUTPUT_PINS.json')['files'])==304,'Terminal sealed output count')
    third=status['third_whole_package_review'];zero(third['severity_counts'],'third review status')
    require(third['review']=='NEW_WHOLE_03' and third['verdict']==verdict['status'] and third['verdict_path']=='evidence/reviews/package_03/VERDICT.json' and third['root_adoption_path']=='evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json' and third['terminal_outputs']==304,'Terminal status/adoption binding')
    history=read_json(ROOT/'REVIEW_HISTORY.json');last=history['events'][-1]
    zero(last['severity_counts'],'dated third-review history')
    require(last['stage']=='NEW_WHOLE_03' and last['status']==verdict['status'] and last['root_adoption_sha256']==protected['evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_03.json'],'Terminal dated review binding')
    require(history['events'][2]['stage']=='NEW_WHOLE_02' and history['events'][2]['severity_counts']=={'P0':0,'P1':0,'P2':1,'P3':0},'Historical sole-P2 disposition')
    return status
def content_paths():
    result=[]
    copies=json.loads((ROOT/'EVIDENCE_COPY_MANIFEST.json').read_text())
    authored_streams=authored_stream_paths(copies)
    for path in ROOT.rglob('*'):
        if not path.is_file():continue
        rel=path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):continue
        if rel.as_posix() in EXCLUDE_NAMES:continue
        if path.name.lower()=='fullsource.txt' or 'CITATION_DISCOVERY' in path.name:continue
        if path.suffix.lower() in EXCLUDE_SUFFIX and rel.as_posix() not in authored_streams:continue
        if path.suffix.lower()=='.pdf' and rel.as_posix()!='output/pdf/paper.pdf':continue
        if path.is_symlink():raise RuntimeError('No symlinks in package content: '+str(rel))
        require(re.fullmatch(r'[A-Za-z0-9_.\-/]+',rel.as_posix()) is not None and all(p not in {'','..','.'} for p in rel.parts),'Unsafe content path: '+str(rel))
        if rel.as_posix()!='output/pdf/paper.pdf':path.read_bytes().decode('utf-8')
        result.append(rel.as_posix())
    require(len({p.casefold() for p in result})==len(result),'Casefold content-path collision')
    return sorted(result)

def main():
    status=terminal_gate()
    paths=content_paths()
    entries=[]
    for name in paths:
        data=(ROOT/name).read_bytes();entries.append(dict(path=name,bytes=len(data),sha256=digest(data)))
    integrity=dict(hash_algorithm='SHA-256',self_reference_policy='Current distributed content only. This manifest and deterministic build/verification/archive-hash receipts have separate roles.',archive_exclusions=dict(directories=sorted(EXCLUDE_DIRS),suffixes=sorted(EXCLUDE_SUFFIX),other_pdfs=True,external_sidecar='ARCHIVE_SHA256.json'),files=entries)
    blob=(json.dumps(integrity,indent=2)+'\n').encode();(ROOT/'CURRENT_INTEGRITY.json').write_bytes(blob)
    receipt=dict(status='PREPARED_CANDIDATE_'+status['new_whole_package_review'],publication_ready=status['publication_ready'],all_issues_resolved=status.get('all_issues_resolved',False),archive_name=ARCHIVE,archive_prefix=PREFIX,content_files=len(entries),current_integrity_sha256=digest(blob),timestamp_policy='2026-10-13 00:00:00 UTC for every tar member; gzip mtime=0',epoch=EPOCH,ordering='sorted relative POSIX paths',owner_group='0/0, empty names',mode='0644',private_source_bodies_included=False,receipt_policy='BUILD_RECEIPT.json is included outside current-integrity self-reference domain; archive binary hash is in external ARCHIVE_SHA256.json. External zenodo-deposit.json names the archive and is excluded to avoid self-reference; the default verifier checks packaged content and validates this wrapper strictly when present; --require-deposit additionally requires it and both verified local attachments.')
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
    sidecar=dict(archive=ARCHIVE,bytes=len(data),sha256=digest(data),current_integrity_sha256=digest(blob),build_receipt_sha256=digest((ROOT/'BUILD_RECEIPT.json').read_bytes()),archive_members=len(archived),publication_ready=status['publication_ready'],all_issues_resolved=status.get('all_issues_resolved',False))
    (ROOT/'ARCHIVE_SHA256.json').write_text(json.dumps(sidecar,indent=2)+'\n')
    print(json.dumps(sidecar))
if __name__=='__main__':main()
