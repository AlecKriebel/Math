#!/usr/bin/env python3
"""Replay the frozen packet in disposable copies; attack optimization/trust.

Run with Python and SymPy 1.14.0. Writes only this review's results directory.
Never imports scripts from, nor executes scripts in, the frozen original.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent.parent
ARCHIVE_ROOT=HERE.parent.parent
ARCHIVED_PACKET=ARCHIVE_ROOT/'original_packet'
WORKSPACE_PACKET=ARCHIVE_ROOT/'original/unsolved_math_prioritization/attempts/30000717'
ROOT=ARCHIVED_PACKET if ARCHIVED_PACKET.is_dir() else WORKSPACE_PACKET
PIN='1492167c7a7cfeb168976aa4d91b32c0be56c3b58de4090c417785a9d324a765'
PROOF_PIN='a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1'
PYTHON=sys.executable
def require(ok,label):
    if not ok: raise RuntimeError(label)
def digest(b):return hashlib.sha256(b).hexdigest()
def inventory(root):
    return {f.relative_to(root).as_posix():{'sha256':digest(f.read_bytes()),'bytes':f.stat().st_size} for f in sorted(root.rglob('*')) if f.is_file()}
def run(script, args=(), optimized=False, environment=None):
    cmd=[PYTHON]+([] if environment else ['-I'])+['-B']+(['-O'] if optimized else [])+[str(script),*args]
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    if environment:env.update(environment)
    p=subprocess.run(cmd,cwd=script.parent,env=env,capture_output=True,timeout=120)
    return {'returncode':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace'),'stdout_sha256':digest(p.stdout),'optimized':optimized,'environment_override':environment or {}}
def mutation_manifest(root):
    m=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
    m['files']=inventory(root)
    m['files'].pop('PUBLIC_MANIFEST.json')
    (root/'PUBLIC_MANIFEST.json').write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
    return digest((root/'PUBLIC_MANIFEST.json').read_bytes())
def update_nested(root, folder, filename, listkey, changed):
    f=root/folder/filename;m=json.loads(f.read_text())
    for record in m[listkey]:
        p=root/folder/record['path']
        if record['path'] in changed:
            record.update(bytes=p.stat().st_size,sha256=digest(p.read_bytes()))
    f.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
def main():
    global PYTHON
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python',type=Path,help='Pinned SymPy1.14.0 child interpreter; default is the running interpreter')
    parser.add_argument('--result-name',default='replay_and_attack.json',help='Results basename; use a new name to preserve historical output')
    args=parser.parse_args()
    if args.python is not None:PYTHON=str(args.python.expanduser().absolute())
    require(Path(args.result_name).name==args.result_name and args.result_name.endswith('.json'),'Unsafe result basename')
    probe=subprocess.run([PYTHON,'-I','-B','-c','import json,sys,sympy; print(json.dumps({"python":sys.version,"sympy":sympy.__version__}))'],capture_output=True,text=True,timeout=30)
    require(probe.returncode==0,'Cannot import pinned SymPy in selected child interpreter: '+probe.stderr)
    version=json.loads(probe.stdout)
    require(version['sympy']=='1.14.0','Pinned SymPy required')
    require(ROOT.is_dir(),'Frozen packet missing: expected archive original_packet or workspace original/unsolved_math_prioritization/attempts/30000717')
    before=inventory(ROOT)
    require(digest((ROOT/'PUBLIC_MANIFEST.json').read_bytes())==PIN,'Snapshot anchor mismatch')
    require(digest((ROOT/'author/PROOF.md').read_bytes())==PROOF_PIN,'Frozen proof anchor mismatch')
    result={'started_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
            'child_python':version['python'],'child_interpreter':PYTHON,
            'sympy_version':version['sympy'],'anchor':PIN,'proof_anchor':PROOF_PIN,
            'packet_layout':'archive original_packet' if ROOT==ARCHIVED_PACKET else 'historical workspace original',
            'anchor_provenance':'Frozen snapshot and independently confirmed live PR description; see PR_DESCRIPTION_ANCHOR.json',
            'ordinary_replays':{},'optimization_replays':{},'attacks':{}}
    with tempfile.TemporaryDirectory(prefix='packet-replay-',dir=HERE) as td:
        td=Path(td);r=td/'packet';shutil.copytree(ROOT,r)
        expected=['author/checks.json','audit_a/results/independent_exact_checks.json','audit_b/checks/independent_results.json']
        scripts=['author/verify.py','audit_a/checks/verify_robinson_obstruction_independent.py','audit_b/checks/independent_verify.py']
        for script,saved in zip(scripts,expected):
            p=run(r/script);require(p['returncode']==0,'Replay failed '+script)
            if script.startswith('audit_a'):
                same=(r/saved).read_bytes()==(ROOT/saved).read_bytes()
            else:same=p['stdout'].encode()==(ROOT/saved).read_bytes()
            require(same,'Saved output mismatch '+script)
            p['saved_output_byte_identical']=same
            result['ordinary_replays'][script]=p
        for name in ('verify_publication.py','mutation_tests.py'):
            for opt in (False,True):
                p=run(r/name,['--expected-manifest',PIN],optimized=opt)
                require(p['returncode']==0,'Packet replay failed '+name+str(opt))
                result['optimization_replays'][name+(':-O' if opt else ':normal')]=p
        p=run(r/'verify_publication.py',['--expected-manifest',PIN],environment={'PYTHONOPTIMIZE':'2'})
        require(p['returncode']==0,'Publication inherited optimization replay failed')
        result['optimization_replays']['verify_publication.py:PYTHONOPTIMIZE=2']=p
        for name in scripts:
            p=run(r/name,optimized=True)
            require(p['returncode']==0,'Original -O supporting replay failed')
            result['optimization_replays'][name+':-O']=p

        # Standalone false-positive fixtures: adding 1 to R destroys its
        # zero-line hypothesis while leaving derivatives/determinants alone.
        changes={
          'author/verify.py':('+3*x**2*y**2*z**2','+3*x**2*y**2*z**2+1'),
          'audit_a/checks/verify_robinson_obstruction_independent.py':('+3*x*x*y*y*z*z','+3*x*x*y*y*z*z+1'),
          'audit_b/checks/independent_verify.py':('+3*x**2*y**2*z**2','+3*x**2*y**2*z**2+1')}
        for name,(old,new) in changes.items():
            rr=td/('fixture-'+name.split('/')[0]);shutil.copytree(ROOT,rr)
            f=rr/name;s=f.read_text();require(s.count(old)==1,'Fixture replacement ambiguous '+name)
            f.write_text(s.replace(old,new))
            normal=run(f);optimized=run(f,optimized=True)
            require(normal['returncode']!=0,'Normal guard failed to reject fixture '+name)
            require(optimized['returncode']==0,'Expected removed-assert fixture did not PASS '+name)
            record={'mutation':'R replaced by R+1, destroying exact zero-line identities', 'normal':normal,'optimized':optimized,
                    'risk_scope':'Standalone supporting scripts only; not an accepted modified release'}
            if not name.startswith('audit_a'):
                saved=ROOT/('author/checks.json' if name.startswith('author') else 'audit_b/checks/independent_results.json')
                record['optimized_stdout_still_byte_identical_to_saved_pass']=optimized['stdout'].encode()==saved.read_bytes()
                require(record['optimized_stdout_still_byte_identical_to_saved_pass'],'Fixture expected identical false-positive output')
            for opt in (False,True):
                block=run(rr/'verify_publication.py',['--expected-manifest',PIN],optimized=opt)
                require(block['returncode']!=0,'Publication accepted changed supporting script')
                record['publication_optimized' if opt else 'publication_normal']=block
            result['attacks']['standalone_assert_fixture:'+name]=record

        # A false fixture applied to this review's code must reject even -O.
        f=td/'own_false_fixture.py';s=(HERE/'checks/exact_controls.py').read_text()
        old='scale(mul(mul(power(X[0],2),power(X[1],2)),power(X[2],2)),3)'
        require(s.count(old)==1,'Independent fixture replacement ambiguous')
        f.write_text(s.replace(old,old[:-2]+'4)'))
        own=[run(f),run(f,optimized=True)]
        require(all(p['returncode']!=0 for p in own),'Own explicit guard admitted false fixture')
        result['attacks']['own_false_fixture_rejects_normal_and_optimized']=own

        # Malicious trivial verifier plus rehashed manifests: hard-coded frozen
        # author/MANIFEST anchor must reject even when self-supplied hash changes.
        rr=td/'vacuous-author';shutil.copytree(ROOT,rr)
        saved=(ROOT/'author/checks.json').read_text()
        (rr/'author/verify.py').write_text('print('+repr(saved)+', end="")\n')
        update_nested(rr,'author','MANIFEST.json','files',{'verify.py'})
        rehashed=mutation_manifest(rr)
        p=run(rr/'verify_publication.py',['--expected-manifest',rehashed])
        require(p['returncode']!=0 and 'Frozen acceptance mismatch' in p['stderr'],'Vacuous author rewrite was not blocked by frozen anchor')
        result['attacks']['vacuous_author_rehashed_packet']=p

        # Changing README and using self-computed hash demonstrates the external
        # anchor's necessity; an integrity verifier cannot authenticate that hash.
        rr=td/'untrusted-rehash';shutil.copytree(ROOT,rr)
        (rr/'README.md').write_text('ARBITRARY MATHEMATICAL CLAIM: zero equals one.\n')
        rehashed=mutation_manifest(rr)
        trusted=run(rr/'verify_publication.py',['--expected-manifest',PIN])
        untrusted=run(rr/'verify_publication.py',['--expected-manifest',rehashed])
        require(trusted['returncode']!=0 and untrusted['returncode']==0,'Anchor-boundary fixture behaved unexpectedly')
        result['attacks']['untrusted_self_rehash']={'trusted_anchor_rejects':trusted,'self_computed_anchor_passes':untrusted,
          'interpretation':'Expected trust boundary, not defect: PASS is integrity/exact-controls scope, not mathematical certification; trusted external digest is essential.'}

        # Import validator from disposable copy. Add independent adversarial
        # classes absent from its bundled mutation sweep.
        sys.dont_write_bytecode=True
        spec=importlib.util.spec_from_file_location('packet_validator',r/'verify_publication.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        attacks=[]
        def reject(label, mutate):
            rr=td/('integrity-'+str(len(attacks)));shutil.copytree(ROOT,rr);mutate(rr)
            try:module.validate(rr,PIN)
            except Exception as e:attacks.append({'test':label,'rejected':True,'exception':type(e).__name__,'reason':str(e)})
            else:raise RuntimeError('Independent mutation accepted '+label)
        reject('symlinked listed file',lambda rr: ((rr/'author/PROOF.md').unlink(),(rr/'author/PROOF.md').symlink_to(ROOT/'author/PROOF.md')))
        reject('symlinked unlisted directory',lambda rr:(rr/'source-link').symlink_to(ROOT,target_is_directory=True))
        reject('wrong external digest',lambda rr:(rr/'PUBLIC_MANIFEST.json').write_bytes((rr/'PUBLIC_MANIFEST.json').read_bytes()+b' '))
        reject('hidden unlisted file',lambda rr:(rr/'.hidden').write_text('source leak'))
        reject('zero-byte unlisted file',lambda rr:(rr/'zero').write_bytes(b''))
        result['attacks']['independent_integrity_mutations']=attacks

        # Ordinary file manifest intentionally ignores non-regular filesystem
        # objects. Such objects cannot be Git blob entries in this PR.
        if hasattr(os,'mkfifo'):
            rr=td/'fifo';shutil.copytree(ROOT,rr);os.mkfifo(rr/'unlisted_fifo')
            module.validate(rr,PIN)
            result['attacks']['unlisted_fifo']={'accepted_by_validate':True,'interpretation':'Low-impact filesystem hardening gap: file-set scan includes only is_file(); FIFO is not a Git-trackable blob and contains no source bytes.'}

    after=inventory(ROOT)
    require(before==after,'Frozen originals changed')
    result['original_file_set_and_bytes_unchanged']=True
    result['original_inventory']=before
    result['source_free_inventory']={'files':len(before),'extensions':sorted(set(Path(n).suffix for n in before)),
       'all_utf8_text':all((ROOT/n).read_bytes().decode('utf-8') is not None for n in before),
       'no_pdf_render_dataset_or_catalogue_record_file':all(Path(n).suffix in ('.md','.py','.json','.txt') for n in before),
       'limitation':'Checks current packet bytes and absence of redistributed source assets; does not authenticate historical source retrievals or prove priority.'}
    result['completed_utc']=datetime.now(timezone.utc).isoformat()
    result['verdict']='PASS_REPLAY_AND_PACKAGING_WITH_STANDALONE_OPTIMIZATION_AND_FILESYSTEM_BOUNDARIES_DOCUMENTED'
    out=HERE/'results'/args.result_name;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'verdict':result['verdict'],'output':str(out),'original_unchanged':True},indent=2))
if __name__=='__main__':main()
