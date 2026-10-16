#!/usr/bin/env python3
"""Assemble only the explicitly selected PR948 release inputs; no publication.

Run with Python -I -S -B. This repository-side builder needs the authenticated
audit working tree. Reproduction of the distributed finite checks does not.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Invoke with Python -I -S -B')
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import stat
import zipfile

D = Path(__file__).resolve().parent
A = D.parent
HEAD = 'be4313efafa1af5962394e07d8a4debff2e94d92'
ROOT = D / 'package'
FAMILIES = {
    'global_topology': 'db92a2810dfeb5e88b9b36f7465cfa8895fe3bfa25a51c97d90389564ba3adc1',
    'local_geometry': '58d2701b6d33179f76d2b49ae4f70f2fbf2f5a9be367e3218daa6d674a2bc93a',
    'source_scope': 'b630e035dcd9a4e91ade2e444ac47193b5be7a661c298442c792132453bd4cea',
    'computation_family': '9227bad3bd362f073c7f3ee49858768d9f2b7100e4fb9f1bc69bbb4309c551f2',
    'mathematical_falsifier': '01c2c3a813bb060150c8bc9ccf2b3d2921fa13b80cc23b99f5cdd88a87ca93e9',
    'classical_priority': '41ff65fc95d0ed4a99287fe3eee1c40acbec13c7b7cef497703f23f3c87ec3da',
    'mechanism_priority': '2354407ea8ff379658f9115bf1b524f6582badfe817d6e4b2130d461fb150cb9',
    'recent_priority': '3b58a26df8b2f81b856569c5a6600aee4b99dc004457a170c415986302f6e659',
    'priority_falsifier_01': '5bdbced0027b72e38bd1d13d1e4be8f1783268e88be7c07c40768a823b5725d4',
}
PROFILE = A / 'publication/profile'
DRIVER_SHA = '252b38c10858eab3fd2ea2e7314e1d2aeee7a257bb5fb6360bac3e9526949046'
ALLOWLIST_SHA = 'eb9e551bed22ea2939c33523e4a713ad099bddc7e885901b53a1d16e500eeca8'
HISTORICAL_FULL_REVIEWS = {
    'full_package_01': '348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66',
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(path, pin=None):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'not regular/single-link: '+str(path))
    need(st.st_size <= 8*1024**2, 'input too large')
    data = path.read_bytes()
    need(len(data) == st.st_size, 'input size changed')
    if pin is not None:
        need(digest(data) == pin, 'input hash mismatch: '+str(path))
    return data

def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True)+'\n').encode()

def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    for parent in (path.parent, *path.parents):
        need(not parent.is_symlink(), 'symlink parent')
    if path.exists() or path.is_symlink():
        need(stat.S_ISREG(path.lstat().st_mode) and path.lstat().st_nlink == 1, 'unsafe destination')
        if path.read_bytes() == data and stat.S_IMODE(path.stat().st_mode) == 0o644:
            return
    temp = path.with_name(path.name+'.root_build_tmp')
    with temp.open('xb') as f:
        f.write(data)
    temp.chmod(0o644)
    os.replace(temp, path)

def pin(data):
    return {'bytes': len(data), 'sha256': digest(data)}

def main():
    # Authenticate the executable before importing or following its declarations.
    read(PROFILE/'verify_package.py', DRIVER_SHA)
    spec = importlib.util.spec_from_file_location('pr948_trusted_profile', PROFILE/'verify_package.py')
    profile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile)
    selected, provenance = {}, {}
    def add(name, source, expected=None):
        profile.canonical_path(name)
        need(name not in selected, 'duplicate selection '+name)
        data = read(source, expected)
        selected[name] = data
        provenance[name] = {'source_relative_to_audit': os.path.relpath(source,A), **pin(data)}
    originals = json.loads(read(A/'ORIGINAL_FILE_RECORDS.json'))
    need(originals['head'] == HEAD and len(originals['files']) == 24, 'original map identity')
    for name, record in originals['files'].items():
        need(record['git_mode'] == '100644', 'original mode')
        data = read(A/'original'/name, record['sha256'])
        need(len(data) == record['bytes'], 'original length')
        need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == record['git_blob'], 'original Git blob')
        add('original/'+name,A/'original'/name,record['sha256'])
    for family, expected in FAMILIES.items():
        base = A/'reviews'/family
        manifest_data = read(base/'MANIFEST.json',expected)
        manifest = json.loads(manifest_data)
        entries = manifest.get('payloads',manifest.get('files'))
        need(isinstance(entries,(list,dict)), 'family manifest entries')
        if isinstance(entries,dict):
            entries = [{'path':name,**record} for name,record in entries.items()]
        for record in entries:
            name = record.get('path',record.get('file'))
            need(isinstance(name,str), 'family payload name')
            data = read(base/name,record['sha256'])
            need(len(data) == record['bytes'], 'family size')
            add('audit/'+family+'/'+name,base/name,record['sha256'])
        for name in ('MANIFEST.json','MANIFEST.sha256','EXTERNAL_SEAL.json'):
            if (base/name).exists():
                add('audit/'+family+'/'+name,base/name,expected if name=='MANIFEST.json' else None)
    allow = json.loads(read(PROFILE/'PUBLIC_ALLOWLIST.json',ALLOWLIST_SHA))
    need(len(allow['public_files']) == 36, 'profile inventory')
    old = json.loads(read(PROFILE/'history/pre_root01/SNAPSHOT_MANIFEST.json',
                         'a948328d3edf37568b48eb9b2cdac6efae89f5c74b3aee2758570a0fe1e885dd'))
    oldfiles = old.get('files',old.get('payloads'))
    need(isinstance(oldfiles,(dict,list)), 'profile history shape')
    if isinstance(oldfiles,dict):
        oldfiles=[{'path':name,**record} for name,record in oldfiles.items()]
    for record in oldfiles:
        name=record.get('path',record.get('file'))
        need(len(read(PROFILE/'history/pre_root01'/name,record['sha256']))==record['bytes'],'profile old size')
    for name in allow['public_files']:
        add('profile/'+name,PROFILE/name,DRIVER_SHA if name=='verify_package.py' else None)
    # Previous complete adverse reviews are historical evidence. Reviews of this
    # new candidate stay outside its closed tree, avoiding recursive approval.
    for family, expected in HISTORICAL_FULL_REVIEWS.items():
        base = A/'reviews'/family
        manifest_data = read(base/'MANIFEST.json',expected)
        manifest = json.loads(manifest_data)
        entries = manifest['files']
        allowed = manifest['explicit_public_allowlist']
        need(isinstance(entries,dict) and isinstance(allowed,list)
             and len(allowed)==len(set(allowed)) and set(entries)==set(allowed)
             and 'MANIFEST.json' not in entries,'historical whole-review allowlist')
        for name, record in entries.items():
            data = read(base/name,record['sha256'])
            need(len(data)==record['bytes'],'historical whole-review payload size')
            add('audit/'+family+'/'+name,base/name,record['sha256'])
        add('audit/'+family+'/MANIFEST.json',base/'MANIFEST.json',expected)
    for name in ('README.md','AUTHORSHIP_PROVENANCE.md','AUDIT_LIMITS.md',
                 'FINDING_DISPOSITIONS.json','FULL_PACKAGE_REVIEW_DISPOSITIONS.json'):
        add(name,D/name)
    add('paper/note.tex',D/'note.tex')
    add('paper/note.pdf',D/'output/pdf/note.pdf')
    rootfiles = [
        'ORIGINAL_FILE_RECORDS.json','ORIGINAL_SNAPSHOT.json','GATED_QUEUE_ROW.md',
        'TARGET_IDENTITY_PREFLIGHT.json','RESEARCH_CHARTER.md',
        'ROOT_ORIGINAL_AUTHENTICATION_AND_BUDGET.json',
        'ROOT_INDEPENDENT_MATHEMATICAL_RECONSTRUCTION.md',
        'ROOT_LOCAL_FAMILY_ACTUAL_REPLAY.json','MATHEMATICAL_GATE.json','PRIORITY_GATE.json',
        'ROOT_PRIORITY_FALSIFIER_01_AUTHENTICATION.json',
        'ROOT_PRE_PACKAGE_SOURCE_CONTINUITY_06.json',
        'ROOT_PROFILE_ROOT01_AUTHENTICATION.json','ROOT_PROFILE_ROOT01_REPLAY.json',
        'PUBLICATION_FINDINGS_REGISTER.md','ROOT_WORKFLOW_PRE_FREEZE_FINDINGS.json',
        'ROOT_FULL01_REPORT_AUTHENTICATION.json',
        'ROOT_CANDIDATE1_ARCHIVE_AUTHENTICATION.json',
    ]
    for name in rootfiles:
        add('audit/root/'+name,A/name)
    for name in ('witness.py','WITNESS.json','witness_unchanged_head.py',
                 'WITNESS_UNCHANGED_HEAD.json','WITNESS_UNCHANGED_HEAD_REPLAY.json'):
        add('audit/root_status_context/'+name,A/'publication/root_status_context'/name)
    for name in ('LIVE_BASE_OBSERVATION.json','STORED_BASE_WITNESS.json',
                 'witness_stored_base.py'):
        add('audit/root_live_base_context/'+name,A/'publication/root_live_base_context'/name)
    for name in ('PRE_REVIEW_SYNTHESIS.md','QUERY_LEDGER.json','ROOT_RETRIEVALS_01.json',
                 'ROOT_RENDER_INPUTS_01.json','SUPPLEMENTARY_PRIMARY_READING.json',
                 'BIBLIOGRAPHIC_ACCESS_FOLLOWUP.json','RESEARCH_LOG.md'):
        add('audit/root_priority/'+name,A/'reviews/root_priority'/name)
    for name in ('ARTIFACT_OPERATION.json','INITIAL_AUTHORING_CORRECTIONS.json',
                 'COMPILE_ATTEMPT_01.json','COMPILE_ATTEMPT_02.json','RENDER_INPUTS_01.json'):
        add('audit/paper_build/'+name,D/name)
    profile.validate_namespace(selected)
    need(len(selected)+1<=profile.MAX_FILES,'package file cap')
    manifest={'schema':profile.SCHEMA,'version':1,'problem_id':30004549,
              'original_head':HEAD,'files':{name:{**pin(data),'mode':'100644'}
                                           for name,data in sorted(selected.items())}}
    manifest_data=encoded(manifest)
    need(len(manifest_data)<=profile.MAX_MANIFEST_BYTES,'manifest cap')
    selected[profile.MANIFEST]=manifest_data
    if ROOT.exists():
        _, files, _ = profile.scan_tree(str(ROOT))
        need(not(set(files)-set(selected)),'unexpected prior package entry; do not delete automatically')
    for name,data in sorted(selected.items()):
        put(ROOT/name,data)
    anchor=digest(manifest_data)
    result,_=profile.verify(str(ROOT),anchor)
    pdfname='anti-invariant-four-manifold-v1.0.pdf'
    zipname='anti-invariant-four-manifold-verification-v1.0.zip'
    put(D/pdfname,selected['paper/note.pdf'])
    archive_temp=D/(zipname+'.root_build_tmp')
    with archive_temp.open('xb') as stream:
        with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,data in sorted(selected.items()):
                item=zipfile.ZipInfo(name,date_time=(2026,10,16,0,0,0))
                item.create_system=3
                item.external_attr=0o100644<<16
                item.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(item,data,compresslevel=6)
    archive_temp.chmod(0o644)
    archive_data=read(archive_temp)
    archive_expected={name:{**pin(data),'mode':'100644'} for name,data in selected.items()}
    archive_result=profile.inspect_archive(archive_data,archive_expected)
    os.replace(archive_temp,D/zipname)
    receipt={'schema':'pr948-package-build-v1',
             'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'original_head':HEAD,'result':'PASS_FINITE_BUILD_NOT_PUBLICATION_ACCEPTANCE',
             'package_manifest_sha256':anchor,'package_files_including_manifest':len(selected),
             'package_pdf':'paper/note.pdf','pdf_upload':{'name':pdfname,**pin(selected['paper/note.pdf'])},
             'zip_upload':{'name':zipname,**pin(archive_data)},
             'tree_verification':result,'archive_members_verified':len(archive_result),
             'source_selection':provenance,'family_manifest_pins':FAMILIES,
             'builder_sha256':digest(read(Path(__file__))),
             'limitations':'No mathematical, novelty, publication or whole-package approval follows. External review/freeze and operational authentication remain required. No recursive manifest self-hash.'}
    print(json.dumps({key:value for key,value in receipt.items() if key!='source_selection'},indent=2))
    put(D/'BUILD_RECEIPT.json',encoded(receipt))

if __name__=='__main__':
    main()
