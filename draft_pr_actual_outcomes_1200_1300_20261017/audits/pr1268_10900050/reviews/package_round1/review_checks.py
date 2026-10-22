#!/usr/bin/env python3
"""R1 detached checks. Writes are confined to this family's ignored scratch.

This script checks actual frozen bytes; mocked workflow probes remain tooling
evidence only and do not represent a real publication or actual final gate.
"""
from pathlib import Path
import copy, datetime, hashlib, importlib.util, json, os, shutil, subprocess, sys, zipfile

R = Path(__file__).resolve().parent
A = R.parents[1]
S = R / 'scratch' / 'detached_checks'
S.mkdir(parents=True, exist_ok=True)
TMP = S / 'tmp'
TMP.mkdir(exist_ok=True)
ENV = dict(os.environ, TMPDIR=str(TMP), PYTHONDONTWRITEBYTECODE='1')
ENV.pop('PYTHONOPTIMIZE', None)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    spec = importlib.util.spec_from_file_location('r1_' + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run(program, flags=(), args=()):
    p = subprocess.run([sys.executable, '-B', *flags, str(program), *args],
                       cwd=S, env=ENV, capture_output=True, text=True, timeout=180)
    return {'flags': list(flags), 'returncode': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

def need(value, message):
    if not value:
        raise RuntimeError(message)

def authenticate():
    freeze = json.loads((R/'INPUT_FREEZE.json').read_text())
    bad=[]
    for entry in freeze['files']+freeze['external_readonly_inputs']:
        p=Path(entry['path']); p=p if p.is_absolute() else A/p
        if p.stat().st_size!=entry['bytes'] or sha(p)!=entry['sha256']:
            bad.append(entry['path'])
    return {'relative_files':len(freeze['files']),
            'external_readonly_inputs':len(freeze['external_readonly_inputs']),
            'freeze_sha256':sha(R/'INPUT_FREEZE.json'), 'mismatches':bad}

def archive_checks():
    dest=S/'actual_archive'
    if dest.exists():shutil.rmtree(dest)
    dest.mkdir()
    with zipfile.ZipFile(A/'publication/Prime_Difference_Counterexample_Verification_v1.0.zip') as z:
        names=z.namelist()
        need(len(names)==len(set(names))==167, 'Actual archive member count')
        need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names), 'Unsafe ZIP member')
        need(all((i.external_attr>>16)&0o170000 != 0o120000 for i in z.infolist()), 'ZIP symlink')
        z.extractall(dest)
    need(all((dest/n).read_bytes()==(A/'publication/verification'/n).read_bytes() for n in names), 'ZIP/local divergence')
    build=json.loads((A/'publication/BUILD_RECEIPT.json').read_text())
    anchors=build['verification_anchors']
    args=[s for k,v in anchors.items() for s in ['--expected-'+k+'-sha256',v]]
    baseline=[run(dest/'verify.py',f,args) for f in [[],['-O'],['-OO']]]
    need(all(p['returncode']==0 for p in baseline), 'Actual archive baseline failed')
    negative=[]
    def check(label, mutate, restore, passed_args=args):
        mutate()
        try:
            for flags in [[],['-O'],['-OO']]:
                p=run(dest/'verify.py',flags,passed_args)
                need(p['returncode']!=0,'Corruption accepted '+label)
                negative.append({'label':label,'flags':flags,'returncode':p['returncode'],
                                 'exception_tail':p['stderr'].splitlines()[-1]})
        finally:restore()
    member=dest/'current_edition/PROOF.md';body=member.read_bytes()
    check('changed_actual_current_proof', lambda:member.write_bytes(body+b'\nTAMPER'), lambda:member.write_bytes(body))
    check('missing_actual_current_proof', member.unlink, lambda:member.write_bytes(body))
    extra=dest/'UNLISTED.txt'
    check('unlisted_member', lambda:extra.write_text('unlisted'), extra.unlink)
    man=dest/'MANIFEST.json';old=man.read_bytes()
    check('root_manifest_changed', lambda:man.write_bytes(old+b'\n'),lambda:man.write_bytes(old))
    for key in ['manifest','context','snapshot']:
        changed=[s for k,v in anchors.items() for s in ['--expected-'+k+'-sha256','0'*64 if k==key else v]]
        check('wrong_outside_'+key+'_anchor',lambda:None,lambda:None,changed)
    # Coupled outer repair does not repair the independently bound nested member.
    payload=dest/'reviews/source_question_family/SOURCE_ONLY_RECONSTRUCTION.md'
    old_payload=payload.read_bytes()
    def coupled():
        payload.write_bytes(old_payload+b'\nTAMPER')
        obj=json.loads(old)
        for e in obj['files']:
            if e['path']==payload.relative_to(dest).as_posix():
                e.update(bytes=payload.stat().st_size,sha256=sha(payload))
        man.write_text(json.dumps(obj,indent=2)+'\n')
    coupled()
    changed=[s for k,v in anchors.items() for s in ['--expected-'+k+'-sha256',sha(man) if k=='manifest' else v]]
    try:
        for flags in [[],['-O'],['-OO']]:
            p=run(dest/'verify.py',flags,changed)
            need(p['returncode']!=0,'Coupled outer tampering accepted')
            negative.append({'label':'coupled_outer_repair_nested_payload','flags':flags,
                             'returncode':p['returncode'],'exception_tail':p['stderr'].splitlines()[-1]})
    finally:payload.write_bytes(old_payload);man.write_bytes(old)
    return {'members':167,'all_members_equal_actual_local_tree':True,
            'baseline':baseline,'actual_archive_negative_controls':negative,
            'three_outside_anchors':anchors,'temporary_directory':str(TMP)}

def finite_checks():
    root=S/'math_replays';root.mkdir(exist_ok=True)
    shutil.copyfile(A/'reconstruction_replay.py',root/'reconstruction_replay.py')
    target=root/'reviews/reconstruction_adversary/audit_checks.py'
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(A/'reviews/reconstruction_adversary/audit_checks.py',target)
    replay=run(root/'reconstruction_replay.py',(),['--source',str(A/'reviews/source_question_family'),
                       '--scratch',str(root/'source_reconstruction'),
                       '--output',str(root/'source_reconstruction/result.json')])
    need(replay['returncode']==0,'Reconstruction replay failed')
    outcome=json.loads((root/'source_reconstruction/result.json').read_text())
    return {'detached_reconstruction_replay':outcome,
            'scope':'Finite diagnostics and 18 rejected mutations supplement the separately checked universal proof.'}

def main():
    result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'before':authenticate(),'archive':archive_checks(),'finite':finite_checks()}
    result['after']=authenticate()
    need(result['before']['mismatches']==result['after']['mismatches']==[], 'Frozen input drift')
    (R/'DETACHED_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','archive_members':167,'archive_baseline_modes':3,
                      'archive_negative_runs':len(result['archive']['actual_archive_negative_controls']),
                      'finite_negative_runs':len(result['finite']['detached_reconstruction_replay']['negative_controls']),
                      'input_authentication':'all 419 entries match before and after'}))

if __name__=='__main__':main()
