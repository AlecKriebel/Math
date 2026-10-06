"""Independent, read-only acceptance replay of the pinned 30001913 author freeze.
Usage: python -I -S replay_audit.py AUTHOR.zip EXTERNAL_MANIFEST.json RECEIPT.json
It executes only already reviewed, hash-pinned author code in isolated child processes.
Mutations and marker payloads exist only in temporary trees. No network access is used.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import py_compile
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'archive': ('3ac226f14b1e8b9912358006e11fd0130f688d5de20eccb1dea58a8da4f6fb36', 17107),
    'manifest': ('b2679cde75abcc86b8f4f19302d284d5c36c367d403abdc2ef5ca9f557573bea', 1145),
    'receipt': ('5e0914ffdcc290e037e08e4aff75470677635be2297d4cde72f9138a6516f690', 6214),
}
BOOTSTRAP_SHA = 'beb54b54f1ed72b242b184cf8d880849295d27f5fccf9e64f768c5f2dca366be'
ALLOWED = {'README.md','RESULTS.md','APPROACHES.md','SOURCES.json','STATUS.json','verify.py','bootstrap.py','EXPECTED.json'}
EXPECTED = {
    'F4_initial_period': [1,0,8,0,120,0,2240,0,47320,0],
    'base_change_defects_m_1_to_12': [0,0,2,2,4,4,6,6,8,8,10,10],
    'complete_solution_claimed': False, 'family_hodge_tate_parameters': [-4,0,4],
    'finite_checks': 1932, 'geometric_proofs_formalized': False,
    'problem_id': 30001913, 'status': 'unsolved', 'substantive_approaches': 5,
}
LOG = []

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    require(sys.flags.isolated and sys.flags.no_site, 'audit requires -I -S')
    require(len(sys.argv)==4, 'expected archive, external manifest, receipt')
    inputs = {k: Path(v).resolve() for k,v in zip(PINS,sys.argv[1:])}
    original = {k:p.read_bytes() for k,p in inputs.items()}
    for k,raw in original.items():
        require((digest(raw),len(raw))==PINS[k], 'input anchor mismatch: '+k)
    manifest=json.loads(original['manifest'])
    receipt=json.loads(original['receipt'])
    launcher=receipt['bootstrap_launcher']
    require(set(manifest['files'])==ALLOWED, 'author manifest inventory')
    with tempfile.TemporaryDirectory(prefix='hodge-independent-audit-') as tmp:
        work=Path(tmp); pristine=work/'pristine'; pristine.mkdir()
        with zipfile.ZipFile(inputs['archive']) as z:
            seen=set()
            for info in z.infolist():
                p=PurePosixPath(info.filename)
                require(not p.is_absolute() and '..' not in p.parts and len(p.parts)==2 and p.parts[0]=='hodge_extremality_30001913', 'archive path')
                require(p.name in ALLOWED and p.name not in seen and stat.S_ISREG(info.external_attr>>16), 'archive item')
                seen.add(p.name); data=z.read(info); expected=manifest['files'][p.name]
                require(len(data)==expected['bytes'] and digest(data)==expected['sha256'], 'archive member hash: '+p.name)
                (pristine/p.name).write_bytes(data)
            require(seen==ALLOWED, 'archive inventory')
        saved={p.name:p.read_bytes() for p in pristine.iterdir()}
        def run(case,root,optimized=False,diag=None,cwd=None,env=None,m=None,msha=None,flags=None,markers=()):
            options=['-I','-S'] if flags is None else flags
            command=[sys.executable]+options+(['-O'] if optimized else [])+['-c',launcher,str(root),str(m or inputs['manifest']),msha or PINS['manifest'][0],BOOTSTRAP_SHA]
            p=subprocess.run(command,capture_output=True,text=True,cwd=cwd or work,env=env,timeout=120)
            if diag is None:
                require(p.returncode==0 and not p.stderr, case+': clean success expected: '+p.stderr)
                require(json.loads(p.stdout)==EXPECTED, case+': independent expected output mismatch')
                result='passed_exact_independent_expected_output'
            else:
                require(p.returncode!=0 and diag in p.stderr and not p.stdout,case+': wrong rejection diagnostic: '+p.stderr)
                result='rejected_with_expected_diagnostic'
            require(not any(x.exists() for x in markers), case+': marker payload executed')
            LOG.append({'case':case,'optimized':optimized,'outcome':result,'diagnostic':diag})
        for opt in (False,True):
            run('pristine archive replay',pristine,opt)
            relocated=work/('relocated O'+str(int(opt))); shutil.copytree(pristine,relocated)
            run('relocated path with spaces',relocated,opt)
            hostile=work/('hostile O'+str(int(opt)));hostile.mkdir(); marker=hostile/'executed'
            payload='from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nraise RuntimeError("untrusted module executed")\n'
            for name in ('hashlib','pathlib','json','fractions','math','stat','sitecustomize','usercustomize'):
                (hostile/(name+'.py')).write_text(payload)
            env=os.environ.copy();env['PYTHONPATH']=str(hostile);env['PYTHONHOME']=str(hostile);env['PYTHONSTARTUP']=str(hostile/'sitecustomize.py')
            run('hostile cwd and Python environment',pristine,opt,cwd=hostile,env=env,markers=(marker,))
            cases={
                'proof byte tampering':'REJECT: byte mismatch: RESULTS.md',
                'expected output tampering':'REJECT: byte mismatch: EXPECTED.json',
                'status byte tampering':'REJECT: byte mismatch: STATUS.json',
                'extra file':'REJECT: tree inventory mismatch',
                'empty directory':'REJECT: nonregular item: empty',
                'nested manifest':'REJECT: nonregular item: nested',
                'missing proof':'REJECT: tree inventory mismatch',
                'expected-file symlink':'REJECT: nonregular item: RESULTS.md',
                'extra symlink':'REJECT: nonregular item: extra_link',
                'FIFO instead of proof':'REJECT: nonregular item: RESULTS.md',
                'root symlink':'REJECT: root is not a real directory',
                'payload entrypoint tampering':'REJECT: byte mismatch: verify.py',
                'bootstrap entrypoint tampering':'REJECT: bootstrap anchor',
                'bootstrap symlink':'REJECT: bootstrap type',
                'package json shadow':'REJECT: tree inventory mismatch',
                'package sitecustomize shadow':'REJECT: tree inventory mismatch',
                'payload legacy bytecode':'REJECT: tree inventory mismatch',
                'payload cache directory':'REJECT: nonregular item: __pycache__',
                'bootstrap cache directory':'REJECT: nonregular item: __pycache__',
                'external manifest byte tampering':'REJECT: external manifest anchor',
                'self-consistent solved status with changed manifest':'REJECT: external manifest anchor',
            }
            for index,(case,diag) in enumerate(cases.items()):
                trial=work/('trial-'+str(int(opt))+'-'+str(index));trial.mkdir();root=trial/'tree';shutil.copytree(pristine,root)
                m=trial/'manifest.json';m.write_bytes(original['manifest']);marker=trial/'executed'
                payload='from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n'
                if case=='proof byte tampering':(root/'RESULTS.md').write_bytes(saved['RESULTS.md']+b'\nmodified')
                elif case=='expected output tampering':(root/'EXPECTED.json').write_text('{}')
                elif case=='status byte tampering':(root/'STATUS.json').write_text('{}')
                elif case=='extra file':(root/'extra').write_text('extra')
                elif case=='empty directory':(root/'empty').mkdir()
                elif case=='nested manifest':(root/'nested').mkdir();(root/'nested/MANIFEST.json').write_text('{}')
                elif case=='missing proof':(root/'RESULTS.md').unlink()
                elif case=='expected-file symlink':(root/'RESULTS.md').unlink();(root/'RESULTS.md').symlink_to(pristine/'RESULTS.md')
                elif case=='extra symlink':(root/'extra_link').symlink_to(pristine/'RESULTS.md')
                elif case=='FIFO instead of proof':(root/'RESULTS.md').unlink();os.mkfifo(root/'RESULTS.md')
                elif case=='root symlink':link=trial/'root-link';link.symlink_to(root,target_is_directory=True);root=link
                elif case=='payload entrypoint tampering':(root/'verify.py').write_text(payload)
                elif case=='bootstrap entrypoint tampering':(root/'bootstrap.py').write_text(payload)
                elif case=='bootstrap symlink':(root/'bootstrap.py').unlink();(root/'bootstrap.py').symlink_to(pristine/'bootstrap.py')
                elif case=='package json shadow':(root/'json.py').write_text(payload)
                elif case=='package sitecustomize shadow':(root/'sitecustomize.py').write_text(payload)
                elif case in ('payload legacy bytecode','payload cache directory','bootstrap cache directory'):
                    source=trial/'marker.py';source.write_text(payload)
                    if case=='payload legacy bytecode':target=root/'verify.pyc'
                    else:
                        (root/'__pycache__').mkdir();name='bootstrap' if case.startswith('bootstrap') else 'verify'
                        target=root/'__pycache__'/(name+'.'+sys.implementation.cache_tag+'.pyc')
                    py_compile.compile(str(source),cfile=str(target),doraise=True)
                elif case=='external manifest byte tampering':m.write_text('{}')
                elif case=='self-consistent solved status with changed manifest':
                    st=json.loads(saved['STATUS.json']);st['status']='solved';st['complete_proof']=True;raw=json.dumps(st).encode();(root/'STATUS.json').write_bytes(raw)
                    changed=json.loads(original['manifest']);changed['files']['STATUS.json']={'bytes':len(raw),'sha256':digest(raw)};m.write_text(json.dumps(changed))
                run(case,root,opt,diag=diag,m=m,markers=(marker,))
            # A deliberately replaced trust anchor is a separate diagnostic, not acceptance of a replacement freeze.
            replacement=work/('replacement-'+str(int(opt)));shutil.copytree(pristine,replacement)
            st=json.loads(saved['STATUS.json']);st['status']='solved';st['complete_proof']=True;raw=json.dumps(st).encode();(replacement/'STATUS.json').write_bytes(raw)
            changed=json.loads(original['manifest']);changed['files']['STATUS.json']={'bytes':len(raw),'sha256':digest(raw)}
            m=work/('replacement-manifest-'+str(int(opt))+'.json');m.write_text(json.dumps(changed))
            run('explicit replacement anchor still rejects solved status',replacement,opt,diag='status contract changed: status',m=m,msha=digest(m.read_bytes()))
            run('missing isolation flag rejected in clean cwd',pristine,opt,diag='REJECT: Python -I -S is required',flags=['-S'])
            run('missing no-site flag rejected in clean cwd',pristine,opt,diag='REJECT: Python -I -S is required',flags=['-I'])
        require({p.name:p.read_bytes() for p in pristine.iterdir()}==saved,'pristine tree was changed')
    for k,p in inputs.items():
        require(p.read_bytes()==original[k],'original input changed: '+k)
    print(json.dumps({'schema':'hodge-extremality-independent-replay-v1','problem_id':30001913,'input_pins_verified':True,'input_bytes_unchanged':True,'tests':len(LOG),'normal_tests':sum(not x['optimized'] for x in LOG),'optimized_tests':sum(x['optimized'] for x in LOG),'finite_controls_per_successful_author_run':1932,'cases':LOG,'limitations':['The system Python installation and explicit trust anchors are trusted.','No simultaneous adversarial filesystem writer is modeled.','Finite arithmetic and replay integrity do not formally verify the geometric proofs.']},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
