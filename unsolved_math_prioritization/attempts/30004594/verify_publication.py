#!/usr/bin/env python3
"""Portable read-only integrity and finite replay; not a proof checker."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
SPECS = [
    ('contact_process_30004594_authored.zip','author',24142,
     'a945c97336f27b6cb4fc750e5eb7aa4819e3e459778422dd0a427cc78ac318b5',
     'AUTHOR_MANIFEST.json','b7cec3611fed2152a42b7e7b4c2daa7ca18d899b3f03603898df838ab9819fd6'),
    ('CONTACT_PROCESS_30004594_INDEPENDENT_AUDIT.zip','audit',38872,
     'acb698b64b8437966a8c60a24e24a3f4a6e60b21779c596bfacda624bbad6cc0',
     'AUDIT_MANIFEST.json','1a7fc25bfb1b4419e718a8ee31a795a1b967a72b88b2f54ac2b73ecd6038fe13')]

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def meta(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def integrity(root):
    require(__debug__ and sys.flags.optimize == 0, 'Assertions must be enabled; do not use -O or PYTHONOPTIMIZE.')
    require(not root.is_symlink(), 'Packet root must not be a symlink')
    manifest = json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
    entries = manifest['files']
    require(len({r['path'] for r in entries}) == len(entries), 'Duplicate manifest paths')
    expected = {r['path'] for r in entries} | {'PUBLICATION_MANIFEST.json'}
    for name in expected:
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name, 'Unsafe path')
    files,dirs = set(),set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink forbidden')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.add(name)
        else:
            require(path.is_file(), 'Nonregular file forbidden')
            files.add(name)
    require(files == expected, 'Recursive file inventory mismatch')
    expected_dirs = {str(p) for name in expected for p in Path(name).parents if str(p) != '.'}
    require(dirs == expected_dirs, 'Recursive directory inventory mismatch')
    for row in entries:
        require(meta((root/row['path']).read_bytes()) == {k:row[k] for k in ('bytes','sha256')}, 'Publication file changed: '+row['path'])
    for name,folder,size,digest,mname,mhash in SPECS:
        encoded = (root/'frozen_archives'/(name+'.b64')).read_bytes()
        data = base64.b64decode(encoded.strip(),validate=True)
        require(base64.b64encode(data)+b'\n' == encoded, 'Noncanonical archive encoding')
        require(meta(data) == {'bytes':size,'sha256':digest}, 'Frozen ZIP changed')
        mdata = (root/folder/mname).read_bytes()
        require(hashlib.sha256(mdata).hexdigest() == mhash, 'Frozen manifest changed')
        frozen = json.loads(mdata)
        expected_members = {r['path'] for r in frozen['files']} | {mname}
        require(len(frozen['files'])+1 == len(expected_members), 'Duplicate frozen manifest entry')
        require({p.name for p in (root/folder).iterdir()} == expected_members, 'Frozen directory inventory')
        for row in frozen['files']:
            require(meta((root/folder/row['path']).read_bytes()) == {k:row[k] for k in ('bytes','sha256')}, 'Frozen member bytes')
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            members = z.infolist()
            require(len(members) == len(expected_members) and {x.filename for x in members} == expected_members, 'ZIP member allowlist')
            require(z.testzip() is None, 'ZIP CRC failed')
            for member in members:
                require(not member.is_dir() and not stat.S_ISLNK(member.external_attr >> 16), 'Unsafe ZIP member')
                require(not member.flag_bits & 1, 'Encrypted ZIP member')
                require(z.read(member) == (root/folder/member.filename).read_bytes(), 'ZIP/directory mismatch')
    return len(expected)

def run(script, *args):
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.check_output([sys.executable,'-B',str(script),*map(str,args)],env=env,text=True)

def verify(root=ROOT):
    count = integrity(root)
    run(root/'author/verify_manifest.py')
    run(root/'audit/verify_audit_manifest.py')
    with tempfile.TemporaryDirectory(prefix='contact-process-replay-') as tmp:
        tmp = Path(tmp)
        run(root/'author/verify.py','--output',tmp/'author.json')
        author_bytes = (tmp/'author.json').read_bytes()
        require(author_bytes == (root/'author/verification_results.json').read_bytes(), 'Author replay differs')
        require(author_bytes == (root/'audit/author_replay.json').read_bytes(), 'Frozen audit author replay differs')
        run(root/'audit/audit_math.py','--output',tmp/'audit.json','--author-results',tmp/'author.json')
        audit_bytes = (tmp/'audit.json').read_bytes()
        require(audit_bytes == (root/'audit/independent_math_results.json').read_bytes(), 'Independent replay differs')
        author,audit = json.loads(author_bytes),json.loads(audit_bytes)
    status = json.loads((root/'audit/AUDIT_STATUS.json').read_bytes())
    require(status['original_problem_solved'] is False and status['substantive_approaches_used'] == 5, 'Disposition')
    require(status['mandatory_mathematical_corrections'] == [], 'Unaddressed correction')
    require(author['total_checks'] == 72940 and audit['total_checks'] == 875433, 'Assertion counts')
    require(status['includes_bareiss_exact_division_assertions'] == 343400, 'Divisibility count')
    require(author['original_problem_solved'] is False and audit['original_problem_solved'] is False, 'No solution claim')
    require(integrity(root) == count, 'Replay mutated packet')
    return {'status':'PASS','problem_id':30004594,'packet_files':count,'assertions_enabled':True,
            'author_exact_controls':72940,'independent_exact_controls':875433,
            'includes_bareiss_division_assertions':343400,'both_replays_byte_identical':True,
            'both_freezes_verified':True,'original_problem_solved':False,'approaches_used':'5/5',
            'optional_external_provenance_replay':'NOT_RUN_EXTERNAL_INPUTS_REQUIRED',
            'analytic_proof_certified_by_code':False,'hosted_ci_pass_claimed':False}

if __name__ == '__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
