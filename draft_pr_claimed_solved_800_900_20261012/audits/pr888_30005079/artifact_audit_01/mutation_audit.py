"""Bounded negative controls of PR888's original publication integrity checker.
All mutations are confined to this audit's disposable private copies.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys

p=argparse.ArgumentParser(); p.add_argument('--source',type=Path,required=True)
a=p.parse_args(); source=a.source.resolve(); out=Path(__file__).resolve().parent
scratch=out/'private_tmp'/'mutation_runs'; scratch.mkdir(parents=True,exist_ok=True)

def dump(root, obj):
    (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(obj,indent=2)+'\n')

def rebind(root, name):
    p=root/'PUBLICATION_MANIFEST.json'; m=json.loads(p.read_text()); data=(root/name).read_bytes()
    for e in m['files']:
        if e['file']==name:
            e.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    dump(root,m)

def modify(root,name):
    q=root/name; q.write_bytes(q.read_bytes()+b'\nAudit controlled mutation.\n')

cases=[]
def test(name, mutate):
    root=scratch/name; shutil.copytree(source,root,dirs_exist_ok=True); mutate(root)
    r=subprocess.run([sys.executable,'-B',str(root/'verify_publication.py'),'--integrity-only'],cwd=scratch,capture_output=True,text=True,timeout=30)
    cases.append({'control':name,'exit_code':r.returncode,'accepted':r.returncode==0,'stdout':r.stdout,'stderr':r.stderr.replace(str(scratch),'<PRIVATE_TMP>')})
    print(name, r.returncode, flush=True)

test('malformed_json',lambda r:(r/'PUBLICATION_MANIFEST.json').write_text('{broken'))
def duplicate_key(r):
    m=json.loads((r/'PUBLICATION_MANIFEST.json').read_text())
    (r/'PUBLICATION_MANIFEST.json').write_text('{"files": [],'+json.dumps(m)[1:])
test('duplicate_root_files_key_last_wins',duplicate_key)
def extra_nan(r):
    m=json.loads((r/'PUBLICATION_MANIFEST.json').read_text());m['unrecognized']=float('nan');dump(r,m)
test('unrecognized_nan_field',extra_nan)
def entries(r, change):
    m=json.loads((r/'PUBLICATION_MANIFEST.json').read_text()); change(m['files']);dump(r,m)
test('empty_inventory',lambda r:entries(r,lambda es:es.clear()))
test('duplicate_file_entry',lambda r:entries(r,lambda es:es.append(es[0].copy())))
test('malformed_sha256',lambda r:entries(r,lambda es:es[0].update(sha256='x'*64)))
test('negative_byte_count',lambda r:entries(r,lambda es:es[0].update(bytes=-1)))
test('path_traversal',lambda r:entries(r,lambda es:es[0].update(file='../EDITION_HISTORY.json')))
test('absolute_path',lambda r:entries(r,lambda es:es[0].update(file='/EDITION_HISTORY.json')))
test('proof_changed',lambda r:modify(r,'PROOF.md'))
def changed_rebind(r,name):
    modify(r,name);rebind(r,name)
test('proof_changed_outer_rebound',lambda r:changed_rebind(r,'PROOF.md'))
test('author_checker_changed_outer_rebound',lambda r:changed_rebind(r,'checks/verify_construction.py'))
test('independent_checker_changed_outer_rebound',lambda r:changed_rebind(r,'audits/reviewer_b/independent_checks.py'))
test('patch_damaged',lambda r:modify(r,'corrections/CITATION_CORRECTION.patch'))
test('patch_damaged_outer_rebound',lambda r:changed_rebind(r,'corrections/CITATION_CORRECTION.patch'))
test('source_metadata_changed_outer_rebound',lambda r:changed_rebind(r,'SOURCE_MANIFEST.json'))
test('missing_source_metadata',lambda r:(r/'SOURCE_MANIFEST.json').unlink())
test('missing_acceptance_report',lambda r:(r/'audits/INDEPENDENT_ACCEPTANCE_A.md').unlink())
test('extra_file',lambda r:(r/'extra.txt').write_text('extra'))
test('extra_empty_directory',lambda r:(r/'extra').mkdir(exist_ok=True))
def symlink(r):
    p=r/'README.md';p.unlink();p.symlink_to(r/'PROOF.md')
test('symlink',symlink)
def changed_driver(r):
    p=r/'verify_publication.py';p.write_bytes(p.read_bytes()+b'\nprint("AUDIT_DRIVER_MUTATION_EXECUTED")\n');rebind(r,'verify_publication.py')
test('driver_changed_outer_rebound_trust_root',changed_driver)
test('filesystem_mode_changed',lambda r:(r/'PROOF.md').chmod(0o755))

def omitting(r):
    (r/'LITERATURE_AND_SCOPE.md').unlink()
    entries(r,lambda es:es.__setitem__(slice(None),[e for e in es if e['file']!='LITERATURE_AND_SCOPE.md']))
test('omitted_file_and_outer_entry',omitting)

# Probe parser behavior independently of hash protection. These inputs are not
# changes that pass the intact packet's byte-hash gates.
spec=importlib.util.spec_from_file_location('original_packet_driver',source/'verify_publication.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
parser=[]
for name,patch in [
    ('header_only_no_hunks',b'--- old\n+++ new\n'),
    ('inconsistent_new_line_coordinate',b'--- old\n+++ new\n@@ -1 +999 @@\n-a\n+b\n'),
    ('incorrect_count',b'--- old\n+++ new\n@@ -1,2 +1 @@\n-a\n+b\n'),
    ('wrong_context',b'--- old\n+++ new\n@@ -1 +1 @@\n-c\n+b\n'),
]:
    try:
        value=module.apply_unified(b'a\n',patch)
        parser.append({'control':name,'accepted':True,'output_utf8':value.decode()})
    except Exception as e:
        parser.append({'control':name,'accepted':False,'error_type':type(e).__name__,'error':str(e)})

result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'interpreter':sys.version,
        'controls':cases,'direct_patch_parser_probes':parser,
        'scope':'Finite, named controls only. An accepted duplicate JSON key, permissive field or changed trust root is not evidence of altered immutable source passing external authentication.'}
(out/'MUTATION_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
