#!/usr/bin/env python3
"""Replay the pinned author packet with isolated Python and adversarial controls.
This verifies bytes and finite sanity checks, never the infinite theorem.
Run: python3 -I -B verify_author_freeze.py AUTHOR.zip AUTHOR_EXTERNAL_MANIFEST.json
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_SHA = '2c62215d1fb82098c2c3777d67f90545b9fa10cf83d4a0d5c91313f84a5a33c5'
ARCHIVE_BYTES = 13928
MANIFEST_SHA = '227a90bcc9104cf0a9ce5ea45146aee4624b91a0b3e2f3198b5c43d8a5f99297'
MEMBERS = {'author/'+n for n in ('APPROACH_LOG.md','LITERATURE.md','MANIFEST.json','PROOF.md','README.md','STATUS.json','VERIFICATION_METADATA.json','verification_results.json','verify.py')}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def regular_member(info):
    p = PurePosixPath(info.filename)
    mode = info.external_attr >> 16
    return not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename and not info.is_dir() and stat.S_IFMT(mode) in (0,stat.S_IFREG)

def inspect_archive(archive, manifest):
    raw = Path(archive).read_bytes()
    mb = Path(manifest).read_bytes()
    require(len(raw)==ARCHIVE_BYTES and digest(raw)==ARCHIVE_SHA, 'Author archive pin mismatch')
    require(digest(mb)==MANIFEST_SHA, 'Author external manifest pin mismatch')
    m = json.loads(mb)
    require(m['archive']['bytes']==ARCHIVE_BYTES and m['archive']['sha256']==ARCHIVE_SHA, 'Archive declaration mismatch')
    expected = {i['path']:i for i in m['members']}
    require(len(expected)==len(m['members']) and set(expected)==MEMBERS, 'External member inventory mismatch')
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist()
        require(len(infos)==len(MEMBERS) and {i.filename for i in infos}==MEMBERS, 'ZIP member inventory mismatch')
        payload={}
        for i in infos:
            require(regular_member(i), 'Unsafe/nonregular ZIP member')
            b=z.read(i)
            require(len(b)==expected[i.filename]['bytes'] and digest(b)==expected[i.filename]['sha256'], 'ZIP member pin mismatch: '+i.filename)
            payload[i.filename]=b
    return payload, expected

def inspect_tree(root, expected):
    actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    require(set(actual)==set(expected), 'Extracted tree inventory mismatch')
    for n,p in actual.items():
        require(stat.S_ISREG(p.lstat().st_mode), 'Extracted member is not a regular file: '+n)
        b=p.read_bytes()
        require(len(b)==expected[n]['bytes'] and digest(b)==expected[n]['sha256'], 'Extracted member pin mismatch: '+n)

def run(script,cwd,flags=(),args=(),env=None):
    p=subprocess.run([sys.executable,'-I','-B',*flags,str(script),*args],cwd=cwd,env=env,text=True,capture_output=True,timeout=30)
    return {'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}

def reject_tree(root,expected):
    try: inspect_tree(root,expected)
    except RuntimeError as e: return str(e)
    raise RuntimeError('Corrupted tree was accepted')

def main():
    require(len(sys.argv)==3, 'Usage: verify_author_freeze.py AUTHOR.zip AUTHOR_EXTERNAL_MANIFEST.json')
    payload,expected=inspect_archive(*sys.argv[1:])
    result={'scope':'Pinned bytes, isolated execution, finite sanity checks, adversarial integrity controls; not a formal mathematical proof','author_archive_sha256':ARCHIVE_SHA,'author_external_manifest_sha256':MANIFEST_SHA,'members_verified':len(payload),'checks':[]}
    with tempfile.TemporaryDirectory(prefix='positive_hankel_audit_') as td:
        root=Path(td); pristine=root/'relocated_packet'; unrelated=root/'unrelated'; unrelated.mkdir()
        for name, which in (('author_archive_corruption',0),('external_manifest_corruption',1)):
            changed=root/(name+'.bin')
            changed.write_bytes(Path(sys.argv[1+which]).read_bytes()+b'X')
            arguments=list(sys.argv[1:]);arguments[which]=str(changed)
            try: inspect_archive(*arguments)
            except RuntimeError as e:
                result['checks'].append({'name':name,'outcome':'EXPECTED_REJECTION','detail':str(e),'author_code_executed':False})
            else: raise RuntimeError('Pinned corrupt envelope accepted: '+name)
        for n,b in payload.items():
            p=pristine/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        inspect_tree(pristine,expected)
        script=pristine/'author/verify.py'
        normal=run(script,unrelated)
        require(normal['returncode']==0, 'Normal isolated replay failed')
        parsed=json.loads(normal['stdout'])
        require(parsed['counts']['total_exact_checks']==1948 and parsed['integrity']=='PASS_EXACT_INVENTORY_AND_ALL_SHA256', 'Replay did not report expected checks')
        result['exact_sanity_check_counts']=parsed['counts']
        result['checks'].append({'name':'relocated_isolated_normal_replay','outcome':'PASS','detail':normal})
        math=run(script,unrelated,args=('--math-only',))
        require(math['returncode']==0 and json.loads(math['stdout'])['counts']['total_exact_checks']==1948, 'Math-only replay failed')
        result['checks'].append({'name':'isolated_math_only','outcome':'PASS'})
        for flag in ('-O','-OO'):
            for args in ((),('--math-only',)):
                r=run(script,unrelated,flags=(flag,),args=args)
                require(r['returncode']!=0 and 'Optimized execution is refused' in r['stderr'], 'Optimized run was not explicitly rejected')
                result['checks'].append({'name':'optimized_'+flag+'_'.join(args),'outcome':'EXPECTED_REJECTION','detail':r})
        mutations={
            'same_size_proof_corruption':lambda a:(a/'PROOF.md').write_bytes(b'X'+(a/'PROOF.md').read_bytes()[1:]),
            'missing_member':lambda a:(a/'README.md').unlink(),
            'unexpected_member':lambda a:(a/'unexpected.txt').write_text('extra'),
            'manifest_corruption':lambda a:(a/'MANIFEST.json').write_text('{}'),
            'verification_results_corruption':lambda a:(a/'verification_results.json').write_text('{}'),
            'unexpected_bytecode_cache':lambda a:((a/'__pycache__').mkdir(),(a/'__pycache__/verify.cpython-311.pyc').write_bytes(b'not a bytecode file')),
        }
        for name, mutate in mutations.items():
            target=root/name;shutil.copytree(pristine,target);mutate(target/'author')
            why=reject_tree(target,expected)
            r=run(target/'author/verify.py',unrelated)
            require(r['returncode']!=0, 'Author self-check failed to reject '+name)
            result['checks'].append({'name':name,'outcome':'EXPECTED_REJECTION','external_reason':why,'detail':r})
        target=root/'forged_checker';shutil.copytree(pristine,target)
        (target/'author/verify.py').write_text('print("PASS")\n')
        why=reject_tree(target,expected)
        result['checks'].append({'name':'forged_checker_pre_execution','outcome':'EXPECTED_REJECTION','external_reason':why,'forged_code_executed':False})
        target=root/'symlink_member';shutil.copytree(pristine,target)
        proof=target/'author/PROOF.md';proof.unlink();proof.symlink_to(pristine/'author/PROOF.md')
        result['checks'].append({'name':'symlink_substitution_pre_execution','outcome':'EXPECTED_REJECTION','external_reason':reject_tree(target,expected)})
        shadow=root/'shadow';shadow.mkdir()
        for name in ('fractions','json','hashlib','pathlib','sitecustomize'):
            (shadow/(name+'.py')).write_text('raise RuntimeError("AUDIT_SHADOW_IMPORTED")\n')
        environment=dict(os.environ);environment['PYTHONPATH']=str(shadow);environment['PYTHONPYCACHEPREFIX']=str(shadow/'cache')
        r=run(script,shadow,env=environment)
        require(r['returncode']==0 and 'AUDIT_SHADOW_IMPORTED' not in r['stderr'], 'Isolated execution imported shadow module')
        require(not list(pristine.rglob('__pycache__')) and not (shadow/'cache').exists(), 'Replay produced unexpected bytecode cache')
        inspect_tree(pristine,expected)
        result['checks'].append({'name':'hostile_cwd_and_pythonpath_shadow','outcome':'PASS_ISOLATION','detail':'Five raising shadow modules were ignored under -I; -B produced no bytecode cache; packet rehashed unchanged.'})
    result['result']='PASS_PINNED_AUTHOR_REPLAY_AND_EXPECTED_NEGATIVE_CONTROLS'
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
