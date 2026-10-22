#!/usr/bin/env python3
"""Isolated portable author-artifact tests. Hash roots are pinned, not inferred."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_ARCHIVE_SHA256='abaee91d08a6173ca929bde0aa28578486e5d4412bca3a8ce23230a970502612'
AUTHOR_ARCHIVE_BYTES=16824
AUTHOR_MANIFEST_SHA256='ae9be91cf28ef9d77dc2560068f1ce9089b1776bfd330e14fd9bf9fcd91226f7'

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(b):return hashlib.sha256(b).hexdigest()

def check_external(root,manifest):
    actual={p.name for p in root.iterdir()}
    require(actual==set(manifest['files']),'external inventory mismatch')
    for name,meta in manifest['files'].items():
        p=root/name
        require(p.is_file() and not p.is_symlink(),'external nonregular member')
        b=p.read_bytes()
        require(len(b)==meta['bytes'] and sha(b)==meta['sha256'],'external member mismatch: '+name)

def authenticated_extract(packet,temporary):
    archive=packet/'AUTHOR_SAFE_FREEZE.zip';b=archive.read_bytes()
    require(len(b)==AUTHOR_ARCHIVE_BYTES and sha(b)==AUTHOR_ARCHIVE_SHA256,'author archive trust-root mismatch')
    b=(packet/'AUTHOR_EXTERNAL_MANIFEST.json').read_bytes()
    require(sha(b)==AUTHOR_MANIFEST_SHA256,'author external manifest trust-root mismatch')
    manifest=json.loads(b)
    require(manifest['archive']['sha256']==AUTHOR_ARCHIVE_SHA256,'author archive metadata mismatch')
    with zipfile.ZipFile(archive) as z:
        members=z.infolist()
        require(len(members)==len(manifest['files']),'duplicate or missing ZIP members')
        require({m.filename for m in members}==set(manifest['files']),'ZIP inventory mismatch')
        for m in members:
            require(m.filename==Path(m.filename).name and not m.is_dir(),'unsafe ZIP member')
            mode=m.external_attr>>16
            require((mode & 0o170000)!=0o120000,'ZIP symlink rejected')
            b=z.read(m)
            meta=manifest['files'][m.filename]
            require(len(b)==meta['bytes'] and sha(b)==meta['sha256'],'ZIP member integrity mismatch')
            (temporary/m.filename).write_bytes(b)
    check_external(temporary,manifest)
    return manifest

def tests(packet):
    rows=[]
    with tempfile.TemporaryDirectory(prefix='reciprocal-independent-') as name:
        work=Path(name);original=work/'original';original.mkdir()
        manifest=authenticated_extract(packet,original)
        cases=[('original',None,True),('relocated with spaces',None,True),
               ('report_append','report_append',False),('report_same_size','report_same_size',False),
               ('expected_append','expected_append',False),('expected_same_size','expected_same_size',False),
               ('code_append','code_append',False),('missing_source','missing_source',False),
               ('unexpected_file','unexpected_file',False),('source_symlink','source_symlink',False),
               ('manifest_wrong_hash','manifest_wrong_hash',False)]
        for label,mutation,expected in cases:
            directory=work/(label+' case');shutil.copytree(original,directory)
            if mutation in ['report_append','expected_append','code_append']:
                f={'report_append':'REPORT.md','expected_append':'EXPECTED_DIAGNOSTICS.json','code_append':'exact_diagnostics.py'}[mutation]
                with (directory/f).open('ab') as s:s.write(b'\n')
            elif mutation=='report_same_size':
                p=directory/'REPORT.md';b=p.read_bytes();p.write_bytes(b.replace(b'bounded',b'founded',1))
            elif mutation=='expected_same_size':
                p=directory/'EXPECTED_DIAGNOSTICS.json';b=p.read_bytes();p.write_bytes(b.replace(b'10204',b'10205',1))
            elif mutation=='missing_source':(directory/'SOURCES.md').unlink()
            elif mutation=='unexpected_file':(directory/'UNDECLARED.txt').write_text('not in the packet\n')
            elif mutation=='source_symlink':
                p=directory/'SOURCES.md';p.unlink();p.symlink_to(original/'SOURCES.md')
            elif mutation=='manifest_wrong_hash':
                p=directory/'MANIFEST.json';j=json.loads(p.read_text());j['files']['REPORT.md']['sha256']='0'*64;p.write_text(json.dumps(j))
            for optimized in [False,True]:
                command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(directory/'verify_packet.py')]
                run=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=30)
                require((run.returncode==0)==expected,'unexpected author test outcome: '+label)
                if expected:
                    value=json.loads(run.stdout)
                    require(value['verified'] and not value['full_problem_resolved'],'incorrect success semantics')
                    d=value['diagnostics']['m4_square_hole_complete_grid_search']
                    require(d['states']==75 and d['candidate_trials']==10204 and not d['feasible'],'author replay counter mismatch')
                rows.append({'case':label,'isolated':True,'optimized':optimized,'expected_success':expected,
                             'exit_code':run.returncode,'stdout_sha256':sha(run.stdout.encode()),'stderr':run.stderr.strip()})
        # Demonstrate the authentication boundary: a self-consistent replacement
        # manifest is not an independent trust root. The external pins must reject it.
        directory=work/'coordinated';shutil.copytree(original,directory)
        p=directory/'REPORT.md';p.write_bytes(p.read_bytes()+b'\n')
        p=directory/'MANIFEST.json';j=json.loads(p.read_text());b=(directory/'REPORT.md').read_bytes()
        j['files']['REPORT.md']={'bytes':len(b),'sha256':sha(b)};p.write_text(json.dumps(j))
        rejected=False
        try:check_external(directory,manifest)
        except ValueError:rejected=True
        require(rejected,'external pins accepted coordinated content and manifest changes')
        rows.append({'case':'coordinated_report_and_inner_manifest','external_pins_rejected':True})
    return {'schema':'independent-author-artifact-tests-v1','all_expected_outcomes':True,
            'subprocess_test_count':22,'external_coordinated_tamper_test_count':1,'tests':rows}

if __name__=='__main__':
    print(json.dumps(tests(Path(__file__).resolve().parent),sort_keys=True,indent=2))
