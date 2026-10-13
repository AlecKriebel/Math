#!/usr/bin/env python3
"""Independent read-only ZIP and provenance audit; explicit guards under -O."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile

OUT = Path(__file__).resolve().parent
AUDIT = OUT.parent.parent
REPO = AUDIT.parents[2]
PKG = AUDIT / 'package'
FREEZE_SHA = '6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352'
checks = 0

def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(label)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(p):
    return json.loads(p.read_bytes())

def safe(name):
    p = PurePosixPath(name)
    forbidden = {'private_sources', 'private_cases', 'mutation_fixtures', 'venv', '.venv', '__pycache__', '.secrets', '.zenodo-state'}
    need(isinstance(name,str) and name == p.as_posix() and not p.is_absolute() and '..' not in p.parts, 'noncanonical path')
    need(not set(p.parts) & forbidden and not name.endswith(('.pyc','.pdf','.png','.jpg')), 'forbidden archive component')
    return p

def run():
    freeze_path = AUDIT / 'PACKAGE_REVIEW_INPUT_2.json'
    need(sha(freeze_path.read_bytes()) == FREEZE_SHA, 'frozen review input changed')
    freeze = load(freeze_path)
    need(freeze['pr'] == 464 and freeze['problem'] == '30004807' and freeze['original_head'] == '97b2ed225574ca61bd03cb8db021a533e04938dc', 'candidate identity')
    need(len(freeze['files']) == 8, 'top inventory count')
    for name, rec in freeze['files'].items():
        p = PKG/name
        need(not p.is_symlink(), 'symlink top file')
        data=p.read_bytes()
        need(len(data)==rec['bytes'] and sha(data)==rec['sha256'], 'top hash/size '+name)
    for name,key in [('SOURCE_RECEIPT.json','source_receipt_sha256'),('MATHEMATICAL_ACCEPTANCE_GATE.json','mathematical_acceptance_gate_sha256'),('BRANCH_INSTALL_PLAN.json','branch_install_plan_sha256')]:
        need(sha((AUDIT/name).read_bytes())==freeze[key], 'internal binding '+name)
    manifest=load(PKG/'SHA256SUMS.json')
    inventory=manifest['files']
    need(len(inventory)==180, 'payload count')
    with zipfile.ZipFile(PKG/'regular_zas_bianchi_verification_v1.zip') as z:
        infos=z.infolist()
        names=[i.filename for i in infos]
        need(len(names)==181 and len(set(names))==181, 'ZIP entry uniqueness')
        need(set(names)==set(inventory)|{'SHA256SUMS.json'}, 'ZIP exact positive inventory')
        need(z.testzip() is None, 'ZIP CRC')
        for i in infos:
            safe(i.filename)
            need(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16), 'ZIP directory/symlink')
            data=z.read(i.filename)
            need(data==(PKG/i.filename).read_bytes(), 'ZIP/local bytes '+i.filename)
            if i.filename in inventory:
                rec=inventory[i.filename]
                need(len(data)==rec['bytes'] and sha(data)==rec['sha256'], 'ZIP SHA/size '+i.filename)
    selections=load(PKG/'REVIEW_EVIDENCE_SELECTION.json')['entries']
    need(len(selections)==138 and len({i['path'] for i in selections})==138, 'evidence selection count')
    for item in selections:
        safe(item['path']); safe(item['origin'])
        original=REPO/item['origin']
        need(original.is_file() and not original.is_symlink(), 'evidence original exists')
        data=(PKG/item['path']).read_bytes()
        need(data==original.read_bytes(), 'evidence origin bytes')
        need(len(data)==item['bytes'] and sha(data)==item['sha256'], 'evidence origin SHA/size')
    binding=load(PKG/'verification/SOURCE_BINDINGS.json')
    receipt=load(AUDIT/'SOURCE_RECEIPT.json')
    by_original={i['path']:i for i in receipt['files']}
    need(len(by_original)==13 and len(binding['files'])==13, 'source original count')
    for item in binding['files']:
        orig=item['original_repository_path']; rec=by_original[orig]
        local=PKG/'verification'/item['package_path']
        need(local.read_bytes()==(AUDIT/'source_snapshot'/orig).read_bytes(), '13 original source bytes')
        need(sha(local.read_bytes())==rec['sha256'] and local.stat().st_size==rec['bytes'], '13 original source SHA/size')
    hist=PKG/'verification/frozen_history'
    author=load(hist/'audit/FROZEN_INPUTS.json')
    old=load(hist/'audit/AUDIT_MANIFEST.json')
    refs=[(hist/'release'/i['path'],i) for i in author['files']]
    refs += [(hist/'audit'/p,r) for p,r in old['portable_files'].items()]
    need(len(refs)==11, 'extant refs count')
    for p,r in refs:
        need(p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256'], '11 extant ref')
    need(binding['unattested_reference']['status']=='UNATTESTED' and binding['unattested_reference']['sha256']==author['author_manifest_sha256'], 'unattested digest distinction')
    metadata=load(PKG/'metadata.json'); deposit=load(PKG/'deposit.json')
    need(metadata==deposit['metadata'], 'exact metadata')
    need(deposit['files']==[{'path':'manuscript.pdf','name':'regular_zas_bianchi_defect.pdf'},{'path':'regular_zas_bianchi_verification_v1.zip'}], 'exact two uploads')
    need(metadata['title']=='A regular zero-area singularity with a nonzero weak Bianchi defect' and metadata['publication_type']=='preprint', 'title/type')
    need(metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}], 'author metadata')
    return {'verdict':'PASS','explicit_checks':checks,'freeze_sha256':FREEZE_SHA,'top_files':freeze['files'],'zip_entries':181,'payload_files':180,'origin_selections':138,'original_source_files':13,'extant_historical_references':11,'standalone_digest':'UNATTESTED','metadata_exact':True,'network_or_service_writes':False}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
