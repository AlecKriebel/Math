"""Independent physical package checks; writes only beneath this review folder.

Run with Python >=3.11, no third-party modules. Diagnostic output is evidence
of finite computations and byte preservation only, never proof of the PDE.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT.parent / 'preprint'
SCRATCH = ROOT / 'tmp'
SOURCE = SCRATCH / 'source'
PY312 = Path('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
SIX = ['paper.tex', 'output/pdf/paper.pdf', 'source-and-verification.zip',
       'zenodo-deposit.json', 'zenodo-metadata.json', 'zenodo-upload-kit.zip']


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def ident(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def tree(root):
    return {p.relative_to(root).as_posix(): ident(p.read_bytes())
            for p in root.rglob('*') if p.is_file() and not p.is_symlink()}


def execute(cmd, env=None):
    result = subprocess.run(list(map(str, cmd)), cwd='/', env=env,
                            capture_output=True, text=True, timeout=300)
    return {'cmd': list(map(str, cmd)), 'returncode': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def main():
    SCRATCH.mkdir(exist_ok=True)
    if not SOURCE.exists():
        with zipfile.ZipFile(PACKAGE / 'source-and-verification.zip') as archive:
            for name in archive.namelist():
                part = Path(name)
                need(not part.is_absolute() and '..' not in part.parts, 'unsafe source entry')
            archive.extractall(SOURCE)
    frozen = {n: ident((PACKAGE / n).read_bytes()) for n in SIX}
    baseline = tree(SOURCE)
    rows = json.loads((SOURCE / 'MANIFEST.json').read_text())['files']
    expected = {r['path']: {k: r[k] for k in ['bytes', 'sha256']} for r in rows}
    need(len(expected) == len(rows) == 119, 'source manifest count')
    need(set(baseline) == set(expected) | {'MANIFEST.json'}, 'closed inventory')
    need(all(baseline[n] == v for n, v in expected.items()), 'source manifest identities')
    original = json.loads((SOURCE / 'audit/SNAPSHOT.json').read_text())['files']
    original_root = ROOT.parent / 'original'
    need(len(original) == 39, 'original count')
    original_comparison = []
    for row in original:
        part = row['path'].split('unsolved_math_prioritization/attempts/30005613/', 1)[1]
        raw = (SOURCE / 'historical_candidate' / part).read_bytes()
        need(ident(raw) == {k: row[k] for k in ['bytes', 'sha256']}, 'original hash: '+part)
        need(raw == (original_root / row['path']).read_bytes(), 'actual original bytes: '+part)
        original_comparison.append({'path': part, **ident(raw)})
    archives = []
    verdict = json.loads((SOURCE / 'historical_candidate/VERDICT.json').read_text())
    for row in verdict['archives']:
        p = SOURCE / 'historical_candidate' / row['path']
        z = zipfile.ZipFile(p)
        target = SOURCE / 'historical_candidate' / row['extracted_directory']
        names = z.namelist()
        need(len(names) == len(set(names)) == row['members'], 'original ZIP names')
        need(z.testzip() is None, 'original ZIP CRC')
        need(set(names) == set(tree(target)), 'original ZIP closure')
        need(all(z.read(n) == (target / n).read_bytes() for n in names), 'original ZIP bytes')
        archives.append({'path': row['path'], 'members': len(names), **ident(p.read_bytes())})
    modes = [('normal', sys.executable, [], None),
             ('outer_O', sys.executable, ['-O'], None),
             ('env_PYTHONOPTIMIZE2', sys.executable, [], '2'),
             ('bundled312', PY312, [], None)]
    replays = []
    for label, executable, flags, opt in modes:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        if opt:
            env['PYTHONOPTIMIZE'] = opt
        run = execute([executable, *flags, '-B', SOURCE / 'verify_bundle.py',
                       '--pdf', PACKAGE / 'output/pdf/paper.pdf'], env)
        need(run['returncode'] == 0, label + ': ' + run['stderr'])
        data = json.loads(run['stdout'])
        need(data['status'] == 'PASS' and data['inventory_files'] == 120
             and data['original_files'] == 39, label+' counts')
        h = data['historical_replay']
        need([h[k] for k in ['author_assertions', 'first_portable_assertions',
              'first_with_author_archive_assertions', 'second_exact_tail_checks']]
             == [4187, 2911, 2923, 2304], label+' diagnostics')
        need(tree(SOURCE) == baseline, label+' changed source tree')
        replays.append({'mode': label, **run, 'json': data,
                        'closed_tree_unchanged': True})
    write('REPLAY_RECEIPT.json', {'status': 'PASS', 'runs': replays,
          'scope': 'Finite controls and closure; no analytic certification.'})
    rebuilds = []
    for label, exe, flags in [('normal', sys.executable, []), ('outer_O', sys.executable, ['-O']),
                              ('bundled312', PY312, [])]:
        dest = SCRATCH / ('rebuild_'+label)
        run = execute([exe, *flags, '-B', SOURCE/'build_package.py',
                       '--pdf', PACKAGE/'output/pdf/paper.pdf', '--output-dir', dest])
        need(run['returncode'] == 0, 'rebuild '+label+': '+run['stderr'])
        matches = {n: (dest/n).read_bytes() == (PACKAGE/n).read_bytes() for n in SIX}
        need(all(matches.values()), 'rebuild bytes '+label)
        need(tree(SOURCE) == baseline, 'rebuild input mutated')
        rebuilds.append({'mode': label, **run, 'six_byte_matches': matches})
        shutil.rmtree(dest)
    meta = json.loads((PACKAGE/'zenodo-metadata.json').read_text())['metadata']
    deposit = json.loads((PACKAGE/'zenodo-deposit.json').read_text())
    need(deposit['metadata'] == meta and len(deposit['files']) == 2, 'two-file metadata')
    kit = zipfile.ZipFile(PACKAGE/'zenodo-upload-kit.zip')
    need(set(kit.namelist()) == {'paper.pdf','source-and-verification.zip','zenodo-deposit.json',
                                'zenodo-metadata.json','README.md'}, 'kit inventory')
    need(kit.read('paper.pdf') == (PACKAGE/'output/pdf/paper.pdf').read_bytes(), 'kit PDF')
    need(kit.read('source-and-verification.zip') == (PACKAGE/'source-and-verification.zip').read_bytes(), 'kit source')
    need(kit.read('zenodo-metadata.json') == (PACKAGE/'zenodo-metadata.json').read_bytes(), 'kit metadata')
    flat = json.loads(kit.read('zenodo-deposit.json'))
    need(flat['metadata'] == meta and flat['files'] == [{'path':'paper.pdf'},
                             {'path':'source-and-verification.zip'}], 'kit flat two files')
    write('REBUILD_RECEIPT.json', {'status':'PASS', 'runs':rebuilds,
             'metadata_copies_match':True,'kit_exact_files':kit.namelist(),
             'deposit_files':deposit['files'], 'source_unchanged':True})

    # Each case uses actual physical paths. Only this review's scratch is mutated.
    attack = SCRATCH/'attack'
    if attack.exists():
        shutil.rmtree(attack)
    controls = []
    def case(label, mutation, mode='verify', optimization='O'):
        shutil.copytree(SOURCE, attack)
        mutation(attack)
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE',None)
        flags=['-O'] if optimization == 'O' else []
        if optimization == 'env2': env['PYTHONOPTIMIZE']='2'
        cmd=[sys.executable,*flags,'-B',attack/('verify_bundle.py' if mode=='verify' else 'build_package.py')]
        if mode=='verify': cmd += ['--integrity-only','--pdf',PACKAGE/'output/pdf/paper.pdf']
        elif mode=='internal': cmd += ['--pdf',PACKAGE/'output/pdf/paper.pdf','--output-dir',attack/'out']
        elif mode=='wrongpdf': cmd += ['--pdf',SCRATCH/'wrong.pdf','--output-dir',SCRATCH/'rejected-output']
        else: cmd += ['--pdf',PACKAGE/'output/pdf/paper.pdf','--output-dir',SCRATCH/'rejected-output']
        run=execute(cmd,env)
        need(run['returncode'] != 0, 'accepted corruption '+label)
        controls.append({'case':label,'optimization':optimization,'rejected':True,**run})
        shutil.rmtree(attack)
        need(not (SCRATCH/'rejected-output').exists(), 'rejected build wrote output')
    def change_manifest(p, change):
        m=json.loads((p/'MANIFEST.json').read_text());change(m)
        (p/'MANIFEST.json').write_text(json.dumps(m))
    def altered(p,name):
        f=p/name;f.write_bytes(f.read_bytes()+b'\nreview corruption\n')
    def repin(p,name):
        change_manifest(p,lambda m: [row.update(ident((p/name).read_bytes()))
                         for row in m['files'] if row['path']==name])
    def pin_attack(p,name):
        altered(p,name);repin(p,name)
    attacks = [
      ('changed_tex',lambda p:altered(p,'paper.tex')),
      ('changed_metadata',lambda p:altered(p,'zenodo-metadata.json')),
      ('changed_original',lambda p:altered(p,'historical_candidate/author/PROOF.md')),
      ('changed_original_zip',lambda p:altered(p,'historical_candidate/archives/QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip')),
      ('missing_file',lambda p:(p/'paper.tex').unlink()),
      ('extra_hidden_file',lambda p:(p/'.extra').write_bytes(b'x')),
      ('extra_empty_dir',lambda p:(p/'empty').mkdir()),
      ('physical_symlink',lambda p:(p/'symlink').symlink_to(p/'paper.tex')),
      ('physical_fifo',lambda p:os.mkfifo(p/'fifo')),
      ('duplicate_manifest',lambda p:change_manifest(p,lambda m:m['files'].append(m['files'][0]))),
      ('unsafe_parent_path',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='../escape'))),
      ('unsafe_absolute_path',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='/escape'))),
      ('unsafe_backslash',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='x\\y'))),
      ('manifest_self_reference',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='MANIFEST.json'))),
      ('repinned_original_publication_manifest',lambda p:pin_attack(p,'historical_candidate/PUBLICATION_MANIFEST.json')),
      ('repinned_review_manifest',lambda p:pin_attack(p,'audit/review_spectral_family/MANIFEST.json')),
    ]
    for opt in ['O','env2']:
        for label,mutation in attacks:case(label,mutation,optimization=opt)
        case('internal_output',lambda p:None,'internal',opt)
        (SCRATCH/'wrong.pdf').write_bytes(b'%PDF-1.7\nNot the published PDF\n')
        case('wrong_PDF',lambda p:None,'wrongpdf',opt)
        case('changed_build_input',lambda p:altered(p,'paper.tex'),'build',opt)
    write('PHYSICAL_NEGATIVE_CONTROLS.json',{'status':'PASS','cases':controls,
          'negative_count':len(controls),'scope':'Actual physical manifest/rebuild guards; neither security audit nor PDE proof.'})
    write('PRESERVATION_RECEIPT.json',{'status':'PASS','original_files':original_comparison,
          'original_zip_payloads':archives,'source_archive_members':len(baseline),
          'all_six_unchanged':frozen=={n:ident((PACKAGE/n).read_bytes()) for n in SIX},
          'closed_source_after_all_checks_unchanged':tree(SOURCE)==baseline,
          'checked_at_utc':datetime.now(timezone.utc).isoformat()})
    print(json.dumps({'status':'PASS','replays':len(replays),'rebuilds':len(rebuilds),
                      'physical_negative_controls':len(controls),'original_files':39},indent=2))


if __name__ == '__main__':
    main()
