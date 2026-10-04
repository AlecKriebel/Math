#!/usr/bin/env python3
"""Read-only custody of ROOT's fixed package, with independently captured reproductions."""
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import zipfile

if sys.flags.optimize:
    raise RuntimeError('Independent package checker requires nonoptimized execution.')
here=Path(__file__).resolve().parent
shared=here.parent/'preprint_v1'
private=here/'private';private.mkdir(exist_ok=True)
frozen=private/'frozen';frozen.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
expected={
 'paper.tex':'2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6',
 'common_tangent_nullness.pdf':'80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327',
 'common_tangents_null_locus_v1.zip':'1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5',
 'ARCHIVE_MANIFEST.json':'595bf1903377f68b6836f345bdfa252d6e65342c4d5cce0c67f02fc9f2b333b2',
 'ZENODO_UPLOAD_MANIFEST.json':'5d45d5b3ba4137ddfa19efd2b2a8c63055cb308942b8cc9a6c01019d4f0ed119'}
received={}
for name,want in expected.items():
    path=shared/name;body=path.read_bytes();s=path.lstat()
    if sha(body)!=want or not stat.S_ISREG(s.st_mode):raise RuntimeError('Frozen identity mismatch: '+name)
    (frozen/name).write_bytes(body)
    received[name]={'bytes':len(body),'sha256':sha(body),'full_mode':oct(s.st_mode),'nlink':s.st_nlink}
manifest=json.loads((frozen/'ARCHIVE_MANIFEST.json').read_bytes())
archive=frozen/'common_tangents_null_locus_v1.zip'
extract=private/'extracted';extract.mkdir(exist_ok=False)
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    domain=sorted(manifest['payload_domain']+['ARCHIVE_MANIFEST.json'])
    if names!=domain or len(names)!=len(set(names)):raise RuntimeError('ZIP domain/order/duplicates mismatch')
    for entry in z.infolist():
        p=PurePosixPath(entry.filename)
        if p.is_absolute() or '..' in p.parts or '\\' in entry.filename:raise RuntimeError('Unsafe ZIP path')
        if entry.date_time!=(2026,10,3,0,0,0) or entry.external_attr>>16!=0o100644 or entry.compress_type!=zipfile.ZIP_STORED:raise RuntimeError('ZIP modes/timestamps/compression mismatch')
        b=z.read(entry)
        if entry.filename=='ARCHIVE_MANIFEST.json':
            if b!=(frozen/'ARCHIVE_MANIFEST.json').read_bytes():raise RuntimeError('Internal/external manifest differs')
        else:
            row=manifest['entries'][entry.filename]
            if len(b)!=row['bytes'] or sha(b)!=row['sha256'] or b!=(shared/entry.filename).read_bytes():raise RuntimeError('ZIP/source payload mismatch '+entry.filename)
        destination=extract/p
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(b)

metadata=json.loads((extract/'zenodo_metadata.json').read_bytes())
upload=json.loads((frozen/'ZENODO_UPLOAD_MANIFEST.json').read_bytes())
if upload['file_domain']!=['common_tangent_nullness.pdf','common_tangents_null_locus_v1.zip'] or len(upload['files'])!=2:raise RuntimeError('Upload domain differs')
for row in upload['files']:
    if row['sha256']!=received[row['name']]['sha256'] or row['bytes']!=received[row['name']]['bytes']:raise RuntimeError('Upload artifact binding mismatch')
if upload['metadata_sha256']!=sha((extract/'zenodo_metadata.json').read_bytes()) or upload['archive_manifest_sha256']!=expected['ARCHIVE_MANIFEST.json']:raise RuntimeError('Upload metadata/manifest binding mismatch')
if upload['completed_upload'] or upload['assigned_doi'] is not None or metadata['local_preparation']['completed_deposit'] or metadata['local_preparation']['assigned_doi'] is not None:raise RuntimeError('False completed publication flag')
if metadata['metadata']['creators']!=[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}] or metadata['metadata']['publication_type']!='preprint':raise RuntimeError('Author/publication metadata mismatch')
binding=json.loads((extract/'PDF_BINDING.json').read_bytes())
export=(shared/'ROOT_PDF_EXPORT_v2.json').read_bytes()
if binding['paper_sha256']!=expected['paper.tex'] or binding['pdf_sha256']!=expected['common_tangent_nullness.pdf'] or binding['root_export_receipt']['sha256']!=sha(export):raise RuntimeError('PDF/source/export binding mismatch')
(frozen/'ROOT_PDF_EXPORT_v2.json').write_bytes(export)

environment={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','PYTHONHASHSEED':'0','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8'}
results=[]
def capture(name,script,args=(),cwd=None,want=0,guard=None):
    folder=here/'package_actual_captures'/name;folder.mkdir(parents=True,exist_ok=False)
    source=script.read_bytes();(folder/'PRELAUNCH_SOURCE.py').write_bytes(source)
    argv=[sys.executable,'-B']+list(args[:1] if args and args[0] in ('-O','-OO') else [])+[str(script)]+list(args[1:] if args and args[0] in ('-O','-OO') else args)
    record={'name':name,'argv':argv,'cwd':str(cwd or script.parent),'environment':environment,'controller_pid':os.getpid(),'start_utc':utc(),'source_sha256':sha(source),'source_bytes':len(source),'expected_exit':want}
    (folder/'PRELAUNCH.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    p=subprocess.Popen(argv,cwd=cwd or script.parent,env=environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    (folder/'stdout.bin').write_bytes(out);(folder/'stderr.bin').write_bytes(err)
    record.update({'actual_child_pid':p.pid,'end_utc':utc(),'exit_code':p.returncode,'source_unchanged':script.read_bytes()==source,'stdout_bytes':len(out),'stderr_bytes':len(err),'stdout_sha256':sha(out),'stderr_sha256':sha(err),'failure_text_guard':guard,'guard_matched':guard is None or guard.encode() in err})
    (folder/'CAPTURE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    results.append(record)
    if p.returncode!=want or not record['source_unchanged'] or not record['guard_matched']:raise RuntimeError('Unexpected case: '+name)
    print(name+': expected exit '+str(p.returncode)+'; actual child PID '+str(p.pid))
    return out

# Rebuild twice before modifying the timestamped positive receipt.
capture('unchanged_build_1',extract/'build_archive.py',cwd=here)
rebuilt=(extract/'common_tangents_null_locus_v1.zip').read_bytes()
if sha(rebuilt)!=expected['common_tangents_null_locus_v1.zip']:raise RuntimeError('Original-byte rebuild differs')
capture('unchanged_build_2',extract/'build_archive.py',cwd=here)
if (extract/'common_tangents_null_locus_v1.zip').read_bytes()!=rebuilt:raise RuntimeError('Second deterministic rebuild differs')
capture('optimized_builder',extract/'build_archive.py',args=('-O',),want=1,guard='requires nonoptimized execution')
positive=capture('positive_verify',extract/'verify.py',cwd=here)
receipt=json.loads(positive)
if receipt['status']!='PASS_FINITE_CONTROLS' or receipt['manuscript_sha256']!=expected['paper.tex'] or receipt['candidate_sha256']!='8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12':raise RuntimeError('Positive verifier receipt scope mismatch')
capture('negative_verify',extract/'verify.py',args=('--negative-control',),want=1,guard='intentional false control')
capture('optimized_verify',extract/'verify.py',args=('-O',),want=1,guard='nonoptimized execution')
capture('double_optimized_verify',extract/'verify.py',args=('-OO',),want=1,guard='nonoptimized execution')
capture('new_receipt_build_1',extract/'build_archive.py')
newzip=(extract/'common_tangents_null_locus_v1.zip').read_bytes()
capture('new_receipt_build_2',extract/'build_archive.py')
if newzip!=(extract/'common_tangents_null_locus_v1.zip').read_bytes():raise RuntimeError('Build not deterministic after receipt refresh')

for label,target,change,program,guard in [
 ('tampered_candidate','source/CANDIDATE.md',lambda b:b+b'\n', 'verify.py','reviewed_source_binding'),
 ('stale_manuscript_receipt','paper.tex',lambda b:b+b'\n% adversarial local mutation\n','build_archive.py','Verification receipt is stale'),
 ('tampered_pdf','common_tangent_nullness.pdf',lambda b:b+b'\n% adversarial local mutation\n','build_archive.py','Exported PDF binding is stale')]:
    tree=private/label;shutil.copytree(extract,tree)
    path=tree/target;path.write_bytes(change(path.read_bytes()))
    capture(label,tree/program,want=1,guard=guard)

for name,want in expected.items():
    if sha((shared/name).read_bytes())!=want:raise RuntimeError('Shared frozen source changed: '+name)
for name,row in manifest['entries'].items():
    if sha((shared/name).read_bytes())!=row['sha256']:raise RuntimeError('Shared payload changed: '+name)
report={'schema':'independent-pr18-fixed-package-reproduction/v1','start_source':'ROOT exact 2026-10-03 frozen package','completed_utc':utc(),'actual_controller_pid':os.getpid(),'frozen_files':received,'archive_payload_count':len(manifest['payload_domain']),'archive_entry_count':len(domain),'unchanged_payload_rebuild_sha256':sha(rebuilt),'refreshed_receipt_rebuild_sha256':sha(newzip),'finite_positive_check_count':receipt['assertions_passed'],'actual_cases':results,'shared_frozen_payload_unchanged':True,'mathematical_or_priority_or_publication_clearance':False}
(here/'PACKAGE_REPRODUCTION.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('ALL INDEPENDENT PORTABLE PACKAGE CHECKS PASSED; '+str(len(results))+' genuine cases captured.')
