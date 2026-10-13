#!/usr/bin/env python3
"""Freeze the four intended first-party Zenodo payloads; no network actions."""
from pathlib import Path
import hashlib,json,shutil,zipfile
from datetime import datetime,timezone

PROJECT=Path(__file__).resolve().parents[1]
KIT=PROJECT/'publication/zenodo-upload-kit'
SOURCE=[
    'README.md','LICENSES.md','manuscript/main.tex','manuscript/height-repair.tex',
    'reproducibility/README.md','sources/PINNED_INPUT.json',
    'sources/PINNED_COMPANIONS.json','sources/Poonen2009.metadata.json',
]
VERIFY=[
    'LICENSES.md','VERIFIED_CORRECTIONS.md','THEOREM_LEDGER.md',
    'DEPENDENCY_LEDGER.md','APPROACH_TABLE.md','verification/README.md',
    'verification/check_two_converse_programs.py','reproducibility/build_package.py',
    'reproducibility/package_payload.py','reproducibility/arithmetic_checks.py',
    'reproducibility/arithmetic_checks.expected.json','agent_notes/parity_matrix_check.py',
    'receipts/candidate_build.json','receipts/candidate_visual_qa.json','receipts/source_build.json',
    'reviews/dependency_integration.md',
]
VERIFY+=sorted(str(p.relative_to(PROJECT)) for p in (PROJECT/'agent_notes').glob('*.md'))
VERIFY+=sorted(str(p.relative_to(PROJECT)) for p in (PROJECT/'sources/priority_remote').glob('*.json'))


def sha(data): return hashlib.sha256(data).hexdigest()


def archive(name,paths):
    members=[]
    with zipfile.ZipFile(KIT/name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in sorted(set(paths)):
            data=(PROJECT/path).read_bytes()
            info=zipfile.ZipInfo(path,date_time=(2026,10,6,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,data)
            if (PROJECT/path).read_bytes()!=data:
                raise RuntimeError('Source changed while packaging: '+path)
            members.append({'path':path,'bytes':len(data),'sha256':sha(data)})
    with zipfile.ZipFile(KIT/name) as z:
        if z.testzip() is not None: raise RuntimeError('Corrupt ZIP: '+name)
        for m in members:
            if sha(z.read(m['path']))!=m['sha256']:
                raise RuntimeError('ZIP member changed: '+m['path'])
    return members


def main():
    build=json.loads((PROJECT/'receipts/candidate_build.json').read_text())
    if not build['clean_build_passed']: raise RuntimeError('Clean build did not pass')
    for name,digest in build['input_sha256'].items():
        if sha((PROJECT/name).read_bytes())!=digest:
            raise RuntimeError('Build input changed: '+name)
    KIT.mkdir(parents=True,exist_ok=True)
    for doc in build['documents']:
        data=(PROJECT/doc['output']).read_bytes()
        if sha(data)!=doc['pdf_sha256']: raise RuntimeError('PDF differs from clean build')
        target='paper.pdf' if doc['source']=='manuscript/main.tex' else 'height-repair.pdf'
        (KIT/target).write_bytes(data)
    members={'source.zip':archive('source.zip',SOURCE),
             'verification.zip':archive('verification.zip',VERIFY)}
    manifest=json.loads((PROJECT/'zenodo-deposit.json').read_text())
    files=[]
    for item in manifest['files']:
        data=(PROJECT/item['path']).read_bytes()
        files.append({'path':item['path'],'bytes':len(data),'sha256':sha(data),
                      'md5':hashlib.md5(data).hexdigest()})
    inventory={'created_utc':datetime.now(timezone.utc).isoformat(),
               'manifest_sha256':sha((PROJECT/'zenodo-deposit.json').read_bytes()),
               'files':files,'archive_members':members,
               'third_party_manuscript_bodies_included':False,
               'network_or_publication_actions_performed':False}
    (PROJECT/'publication/CANDIDATE_INVENTORY.json').write_text(
        json.dumps(inventory,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'files':files,'members':{n:len(v) for n,v in members.items()}}))


if __name__=='__main__': main()
