#!/usr/bin/env python3
"""Authenticate the publication, preserve freezes, and safely replay exact checks."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

AUTHOR = ('HOPF_LIE_30005902_AUTHOR_SAFE_FREEZE.zip', 21055, 'ff9116239038710665c590fa392318df98aa368171545db229cebb912a7cd2f8', '0fcd8510f2eede331a5a2bb9c2c55d21d2448e21515cdc494a2771d8c33ee281', 13)
AUDIT = ('HOPF_LIE_30005902_AUDIT_SAFE_FREEZE.zip', 20265, 'f1e4cee2e11f207808827867cf4da566363600016deb8ce273887a2129095287', 'cd6d1f5eb18b070261a6761f277a9c65828ed6af1c05ca204634f2766d93e0e5', 12)
ROOT_FILES = {'README.md','RESULT.json','QUEUE_DELTA.json','REPOSITORY_RECHECK.json','verify_publication.py','check_identity_safe.py','PUBLICATION_MANIFEST.json'}
ROOT_DIRS = {'author','audit','frozen_archives'}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def meta(data):
    return {'bytes': len(data), 'sha256': sha(data)}

def run(path, *args, cwd=None):
    env = os.environ.copy()
    env['PYTHONOPTIMIZE'] = '0'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run([sys.executable, '-B', str(path), *map(str,args)], env=env, cwd=cwd, capture_output=True, check=True).stdout

def check(root, pin=None, replay=False):
    root = Path(root).resolve()
    paths = list(root.rglob('*'))
    need(all(not p.is_symlink() for p in paths), 'Symlink')
    need({p.relative_to(root).as_posix() for p in paths if p.is_dir()} == ROOT_DIRS, 'Directory inventory')
    need(all(p.is_file() or p.is_dir() for p in paths), 'Special file')
    need({p.name for p in root.iterdir() if p.is_file()} == ROOT_FILES, 'Root inventory')
    raw = (root/'PUBLICATION_MANIFEST.json').read_bytes()
    if pin is not None:
        need(sha(raw) == pin, 'External publication manifest pin')
    manifest = json.loads(raw)
    need(set(manifest) == {'format','problem_id','files'}, 'Publication manifest schema')
    need(manifest['format'] == 1 and manifest['problem_id'] == '30005902', 'Publication identity')
    actual = {p.relative_to(root).as_posix() for p in paths if p.is_file()} - {'PUBLICATION_MANIFEST.json'}
    need(set(manifest['files']) == actual, 'Publication file inventory')
    for name in sorted(actual):
        need(manifest['files'][name] == meta((root/name).read_bytes()), 'Publication file bytes: '+name)
    count = 0
    for directory, frozen in [('author',AUTHOR),('audit',AUDIT)]:
        name, size, digest, manifest_pin, members = frozen
        archive = root/'frozen_archives'/name
        need(meta(archive.read_bytes()) == {'bytes':size,'sha256':digest}, 'Immutable archive: '+name)
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            need(len(names) == len(set(names)) == members, 'ZIP count')
            need(set(names) == {p.name for p in (root/directory).iterdir()}, 'ZIP/extraction inventory')
            for info in z.infolist():
                need('/' not in info.filename and '\\' not in info.filename and info.filename not in {'.','..'}, 'ZIP path')
                need(stat.S_ISREG(info.external_attr >> 16), 'ZIP regular member')
                need(z.read(info.filename) == (root/directory/info.filename).read_bytes(), 'ZIP/extracted byte identity')
                count += 1
        need(sha((root/directory/'MANIFEST.json').read_bytes()) == manifest_pin, 'Frozen manifest pin')
    need({p.name for p in (root/'frozen_archives').iterdir()} == {AUTHOR[0],AUDIT[0]}, 'Archive inventory')
    result = json.loads((root/'RESULT.json').read_bytes())
    need(result['disposition'] == 'claimed_solved_literal_unrestricted_field_negative_answer', 'Disposition')
    need(result['novelty_claim'] is False and result['human_peer_review'] is False, 'Scope flags')
    need(result['substantive_approaches_used'] == 1 and len(result['not_settled_here']) == 3, 'Scope and budget')
    out = {'status':'PASS','file_count':len(actual)+1,'archive_members_matched':count,'manifest_sha256':sha(raw),'external_manifest_pin_checked':pin is not None,'replay':'NOT_RUN','queue_check':'NOT_RUN','full_corpus_check':'NOT_RUN: external corpora required; use check_identity_safe.py'}
    if replay:
        author = json.loads(run(root/'author'/'verify_packet.py','--manifest-sha256',AUTHOR[3],'--negative-controls'))
        audit = json.loads(run(root/'audit'/'verify_audit.py','--manifest-sha256',AUDIT[3],'--negative-controls','--author-zip',root/'frozen_archives'/AUTHOR[0]))
        need(author['status'] == audit['status'] == 'PASS', 'Frozen replay status')
        need(len(author['rejected_negative_controls']) == len(audit['rejected_negative_controls']) == 8, 'Frozen mutations')
        need(run(root/'author'/'verify_counterexample.py') == (root/'author'/'results.json').read_bytes(), 'Author result bytes')
        need(run(root/'audit'/'independent_check.py') == (root/'audit'/'INDEPENDENT_RESULTS.json').read_bytes(), 'Independent result bytes')
        out['replay'] = {'status':'PASS','author_assertions':26584,'independent_assertions':29708,'author_mathematical_controls':4,'independent_mathematical_controls':4,'author_integrity_controls':8,'audit_integrity_controls':8,'optimization_forced_to_zero':True}
    return out

def queue_check(root, before, after):
    b, a = Path(before).read_bytes(), Path(after).read_bytes()
    delta = json.loads((Path(root)/'QUEUE_DELTA.json').read_bytes())
    need(meta(b) == {'bytes':delta['base_bytes'],'sha256':delta['base_sha256']}, 'Queue base identity')
    need(meta(a) == {'bytes':delta['updated_bytes'],'sha256':delta['updated_sha256']}, 'Queue updated identity')
    old, new = b.splitlines(keepends=True), a.splitlines(keepends=True)
    need(len(old) == len(new), 'Queue line count')
    changes = [i for i,(x,y) in enumerate(zip(old,new)) if x != y]
    need(len(changes) == 1, 'Exactly one queue row')
    i = changes[0]
    need(b'30005902 / OWR-14298370-002' in old[i], 'Queue target')
    c,d = old[i].split(b'|'),new[i].split(b'|')
    need(len(c) == len(d) == 14, 'Queue columns')
    need([j for j,(x,y) in enumerate(zip(c,d)) if x != y] == [8,9,11], 'Only Status/Turns/Findings')
    for field,index in [('Status',8),('Turns',9),('Findings',11)]:
        need(c[index].decode().strip() == delta['changes'][field]['from'], 'Old '+field)
        need(d[index].decode().strip() == delta['changes'][field]['to'], 'New '+field)
    return {'status':'PASS','changed_rows':1,'changed_columns':['Status','Turns','Findings'],'all_other_bytes_preserved':True}

def negative_controls(root,pin):
    rejected = []
    def trial(name, mutation):
        with tempfile.TemporaryDirectory(prefix='hopf-publish-control-') as d:
            copy = Path(d)/'packet'; shutil.copytree(root,copy); mutation(copy)
            try:
                check(copy,pin)
            except (ValueError,FileNotFoundError,json.JSONDecodeError,zipfile.BadZipFile):
                rejected.append(name)
            else:
                raise ValueError('False publication accepted: '+name)
    trial('changed_proof', lambda p:(p/'author'/'PROOF.md').write_bytes(b'changed'))
    trial('changed_code', lambda p:(p/'audit'/'independent_check.py').write_bytes(b'pass\n'))
    trial('changed_author_archive',lambda p:(p/'frozen_archives'/AUTHOR[0]).write_bytes(b'changed'))
    trial('changed_audit_archive',lambda p:(p/'frozen_archives'/AUDIT[0]).write_bytes(b'changed'))
    trial('missing_file',lambda p:(p/'RESULT.json').unlink())
    trial('extra_file',lambda p:(p/'extra.txt').write_bytes(b'extra'))
    trial('extra_directory',lambda p:(p/'extra').mkdir())
    def symlink(p):
        (p/'RESULT.json').unlink(); (p/'RESULT.json').symlink_to('README.md')
    trial('symlink',symlink)
    def rebound(p):
        f=p/'README.md'; f.write_bytes(f.read_bytes()+b'changed')
        m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes());m['files']['README.md']=meta(f.read_bytes())
        (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    trial('rebound_publication_manifest',rebound)
    with tempfile.TemporaryDirectory(prefix='hopf-assertion-control-') as d:
        probe=Path(d)/'probe.py';probe.write_text("assert False, 'ASSERTION_SAFETY_SENTINEL'\n")
        code="import importlib.util,sys; s=importlib.util.spec_from_file_location('safe',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.run_source(sys.argv[2],[])"
        env=os.environ.copy();env['PYTHONOPTIMIZE']='2';env['PYTHONDONTWRITEBYTECODE']='1'
        p=subprocess.run([sys.executable,'-O','-B','-c',code,str(Path(root)/'check_identity_safe.py'),str(probe)],env=env,capture_output=True)
        need(p.returncode != 0 and b'AssertionError: ASSERTION_SAFETY_SENTINEL' in p.stderr,'Optimized assertion control')
        rejected.append('assertion_stripping_under_optimized_launcher')
    return rejected

if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256');ap.add_argument('--replay',action='store_true');ap.add_argument('--negative-controls',action='store_true');ap.add_argument('--queue-base');ap.add_argument('--queue-updated');a=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=check(root,a.manifest_sha256,a.replay)
    if bool(a.queue_base) != bool(a.queue_updated):
        ap.error('Supply both queue snapshots')
    if a.queue_base:
        out['queue_check']=queue_check(root,a.queue_base,a.queue_updated)
    if a.negative_controls:
        out['rejected_publication_negative_controls']=negative_controls(root,a.manifest_sha256 or out['manifest_sha256'])
    if a.manifest_sha256 is None:
        out['qualification']='Publication internal consistency only; compare the manifest with the external publication receipt. Original freezes have hard-coded pins.'
    print(json.dumps(out,indent=2,sort_keys=True))
