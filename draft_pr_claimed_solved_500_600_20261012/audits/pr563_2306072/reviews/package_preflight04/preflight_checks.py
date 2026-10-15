#!/usr/bin/env python3
"""Independent frozen-package audit. Writes only this assigned review folder.

Finite controls and package rejection tests do not formalize imported analytic
theorems, authenticate historical authorship, or certify literature completeness.
Run with unoptimized Python 3.10+. Internet is used only for the documented fresh
dependency installation; no optional raw-PDF/account custody helper is run.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parents[1]
PUB = AUDIT / 'publication'
SCRATCH = ROOT / 'scratch'
FIXED = {
    'support_slit.pdf': '134c3e24a4a2d1db58a2f9744477491e05b0bc14297b3e23621138c00a22ecbc',
    'verification_package.zip': 'af42a0b08550da3f42165316d874f85c4c230d3c6ba44f341519064e5fdeb5a5',
    'make_package.py': '5e6a400191a77597e5a1858f26270c7e7960d9738fd651d76c4408012134519a',
}
BASELINE_SHA = 'eaf22e2617d2dbbe240b4adc7661801cff2cfa3751ba834379002789c4e7eb83'
OLD_SHA = '1115899b96895d6e3a06eee1d42fd621450518b5e282f3d6898fdf76cac80be3'
checks, receipts = [], []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def check(name, condition, details=None):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'pass': True, 'details': details})


def execute(name, command, cwd=None, env=None, success=True, contains=None):
    start = now()
    p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    result = {'name': name, 'started_utc': start, 'finished_utc': now(),
              'command': [str(s) for s in command], 'returncode': p.returncode,
              'stdout': p.stdout, 'stderr': p.stderr}
    receipts.append(result)
    check(name, (p.returncode == 0) == success, {'returncode': p.returncode})
    if contains:
        check(name + ' expected diagnostic', contains in p.stdout + p.stderr)
    return p


def record_for(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def install_fixture(name):
    folder = SCRATCH / 'controls' / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    for key, data in payloads.items():
        p = folder / key
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return folder


def outer_reseal(folder, names):
    m = json.loads((folder / 'MANIFEST.json').read_bytes())
    for name in names:
        m['files'][name] = record_for((folder / name).read_bytes())
    (folder / 'MANIFEST.json').write_text(json.dumps(m, indent=2) + '\n')


def json_change(folder, name, modify):
    obj = json.loads((folder / name).read_bytes())
    modify(obj)
    (folder / name).write_text(json.dumps(obj, indent=2) + '\n')
    outer_reseal(folder, [name])


def run_fixture(name, success=False, contains=None, modify=None, flags=(), env=None, python=None):
    folder = install_fixture(name)
    if modify:
        modify(folder)
    return execute(name, [python or PYTHON, *flags, folder / 'run_all.py'],
                   success=success, contains=contains,
                   env=env or dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))


if __name__ == '__main__':
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise RuntimeError('Run this adversarial suite without optimization')
    SCRATCH.mkdir(exist_ok=True)
    check('main branch', subprocess.check_output(
        ['git', 'branch', '--show-current'], cwd=AUDIT, text=True).strip() == 'main')
    for name, wanted in FIXED.items():
        check('exact frozen hash ' + name, sha((PUB / name).read_bytes()) == wanted)
    with zipfile.ZipFile(PUB / 'verification_package.zip') as z:
        names = z.namelist()
        check('221 unique outer ZIP members', len(names) == len(set(names)) == 221)
        check('ZIP member confinement and no symlinks', all(
            n.startswith('support_slit_verification/') and '..' not in Path(n).parts
            and not n.endswith('/') and (i.external_attr >> 16) & 0o170000 == 0o100000
            for n, i in zip(names, z.infolist())))
        payloads = {n.removeprefix('support_slit_verification/'): z.read(n) for n in names}
    manifest = json.loads(payloads['MANIFEST.json'])
    check('220 outer payload inventory', set(payloads) == set(manifest['files']) | {'MANIFEST.json'}
          and len(manifest['files']) == 220)
    for name, rec in manifest['files'].items():
        check('outer payload ' + name, record_for(payloads[name]) == rec)
    check('all payloads authored text/code; no raw PDF/account binary',
          all(Path(n).suffix in ('.md', '.json', '.jsonl', '.py', '.tex', '.txt')
              or Path(n).name == '.gitignore' for n in payloads))

    base = install_fixture('clean_base')
    spec = importlib.util.spec_from_file_location('preflight04_integrity', base / 'integrity.py')
    integrity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(integrity)
    registry = json.loads(payloads['SEALS.json'])
    check('14 registered seals', len(registry) == 14 and registry == manifest['nested_seals'])
    check('140 registered inner entries', integrity.verify_nested(payloads, registry) == 140)
    inner = {}
    for name in registry:
        data = json.loads(payloads[name])
        schema = next(k for k in ('files', 'authored_files', 'authored_outputs') if k in data)
        entries = integrity.seal_entries(data)
        inner[name] = {'schema': schema, 'count': len(entries),
                       'paths': [(Path(name).parent / x['path']).as_posix() for x in entries]}
    check('new authored_outputs schema present',
          inner['reviews/priority06_zemyan2003/MANIFEST.json']['schema'] == 'authored_outputs')
    check('hidden gitignores included in new source seals', all(
        any(Path(p).name == '.gitignore' for p in inner[seal]['paths'])
        for seal in registry if any(f'priority{n:02d}' in seal for n in range(6, 11))))

    fresh = SCRATCH / 'fresh_readme_environment'
    if fresh.exists():
        shutil.rmtree(fresh)
    execute('fresh README virtual environment', [sys.executable, '-m', 'venv', fresh])
    PYTHON = str(fresh / 'bin/python')
    execute('fresh README pinned dependency installation',
            [PYTHON, '-m', 'pip', 'install', '--no-cache-dir', '-r', base / 'requirements.txt'])
    execute('fresh dependency version', [PYTHON, '-c',
            'import mpmath,sys; print(sys.version); print(mpmath.__version__); assert mpmath.__version__=="1.4.1"'])
    for k in (1, 2):
        folder = install_fixture('complete_replay_' + str(k))
        before = {n: (folder / n).read_bytes() for n in payloads}
        p = execute('immutable complete replay ' + str(k), [PYTHON, folder / 'run_all.py'],
                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        result = json.loads(p.stdout.strip().splitlines()[-1])
        check('complete counts ' + str(k), result['outer_payloads_verified'] == 220
              and result['nested_entries_verified'] == 140 and result['replayed_jobs'] == 15
              and result['frozen_payloads_unchanged'])
        check('independent byte immutability ' + str(k), all((folder / n).read_bytes() == d
                                                          for n, d in before.items()))

    # Reseal only outer records so each inner seal itself is actually exercised.
    for i, (seal, info) in enumerate(inner.items()):
        chosen = next((p for p in info['paths'] if Path(p).name == '.gitignore'), info['paths'][0])
        def mutate(folder, chosen=chosen):
            (folder / chosen).write_bytes((folder / chosen).read_bytes() + b'\n')
            outer_reseal(folder, [chosen])
        run_fixture('inner_seal_' + str(i + 1), contains='Nested', modify=mutate)
    run_fixture('missing_hidden_gitignore', contains='Inventory mismatch', modify=lambda folder:
                (folder / 'reviews/priority06_zemyan2003/.gitignore').unlink())
    run_fixture('extra_payload', contains='Inventory mismatch', modify=lambda folder:
                (folder / 'unexpected.txt').write_text('extra'))
    run_fixture('omitted_payload', contains='Inventory mismatch', modify=lambda folder:
                (folder / 'support_slit.tex').unlink())
    run_fixture('unexpected_symlink', contains='Unexpected symlink', modify=lambda folder:
                (folder / 'unexpected_link').symlink_to('support_slit.tex'))
    for bad in ('../x', '/x', 'x\\y', 'x:y', './x'):
        try:
            integrity.safe_path(bad)
        except RuntimeError:
            check('unsafe relative path rejected ' + bad, True)
        else:
            raise AssertionError('unsafe path accepted')

    # Change full expected math records while retaining every family/check count.
    wrapper_record = 'root_reproduction/supplied_primary_controls.json'
    controls = [
        ('wrong_interval_same_sample_count', lambda d: d['priority06_zemyan2003']['interval_controls']['samples'][0].__setitem__('theta_prime', '[1, 2]')),
        ('missing_interval_block_same_family_count', lambda d: d['priority06_zemyan2003'].pop('interval_controls')),
        ('wrong_exact_same_family_count', lambda d: d['priority06_zemyan2003']['exact_controls'].__setitem__('candidate_q1', '0')),
        ('wrong07_detail_same_check_count', lambda d: d['priority07_zemyan_bounds']['checks'][0].__setitem__('detail', 'altered')),
        ('wrong08_q_same_check_count', lambda d: d['priority08_radial_extrema'].__setitem__('q_at_1', '0')),
        ('wrong09_evidence_same_check_count', lambda d: d['priority09_commentary_citations']['checks'][0].__setitem__('evidence', 'altered')),
        ('wrong10_detail_same_check_count', lambda d: d['priority10_adversary']['checks'][0].__setitem__('details', 'altered')),
    ]
    for name, modifier in controls:
        run_fixture(name, contains='Replay mismatch', modify=lambda folder, modifier=modifier:
                    json_change(folder, wrapper_record, modifier))
    run_fixture('misassigned_timestamp_normalization', contains='Timestamp normalization assigned to wrong job',
                modify=lambda folder: json_change(folder, 'JOBS.json', lambda j:
                    j[0].__setitem__('ignored_dynamic_fields', ['checked_at_utc'])))
    run_fixture('unknown_normalization_field', contains='Unsupported replay normalization',
                modify=lambda folder: json_change(folder, 'JOBS.json', lambda j:
                    j[0].__setitem__('ignored_dynamic_fields', ['all_checks_passed'])))
    run_fixture('optimized_interpreter', flags=('-O',), contains='Run without Python optimization')
    run_fixture('optimization_environment', env=dict(os.environ, PYTHONOPTIMIZE='1'),
                contains='Run without Python optimization')
    nodeps = SCRATCH / 'no_dependency_environment'
    if nodeps.exists():
        shutil.rmtree(nodeps)
    execute('fresh missing-dependency environment', [sys.executable, '-m', 'venv', nodeps])
    run_fixture('missing_mpmath_rejected', python=str(nodeps / 'bin/python'), contains='mpmath')
    fake = SCRATCH / 'wrong_version'
    fake.mkdir(exist_ok=True)
    (fake / 'sitecustomize.py').write_text('import mpmath\nmpmath.__version__="0.0.0"\n')
    run_fixture('wrong_dependency_version_rejected', env=dict(os.environ, PYTHONPATH=str(fake)),
                contains='Replay mismatch')

    # Recreate producer input layout from frozen payloads, never canonical files.
    builder = SCRATCH / 'producer_rebuild'
    if builder.exists():
        shutil.rmtree(builder)
    buildpub = builder / 'publication'
    buildpub.mkdir(parents=True)
    publication_names = ('support_slit.tex', 'README.md', 'CORRECTIONS.md', 'BUILD.json',
                         'PDF_QA.json', 'requirements.txt', 'integrity.py', 'run_all.py',
                         'JOBS.json', 'SEALS.json')
    for name, data in payloads.items():
        if name == 'MANIFEST.json':
            continue
        dest = (buildpub / name) if name in publication_names else (builder / name)
        if name == 'metadata.json':
            dest = buildpub / 'zenodo-deposit.json'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    for name in ('make_package.py', 'support_slit.pdf'):
        (buildpub / name).write_bytes((PUB / name).read_bytes())
    execute('deterministic producer replay from reconstructed frozen inputs',
            [sys.executable, buildpub / 'make_package.py'], env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    check('reconstructed producer ZIP byte exact',
          sha((buildpub / 'verification_package.zip').read_bytes()) == FIXED['verification_package.zip'])
    prior = AUDIT / 'reviews/package_preflight03/.cache/producer_rebuild/publication/verification_package.zip'
    check('prior metadata-repair freeze exact', sha(prior.read_bytes()) == OLD_SHA)
    with zipfile.ZipFile(prior) as z:
        old = {n.removeprefix('support_slit_verification/'): z.read(n) for n in z.namelist()}
    check('old/new same inventory', set(old) == set(payloads))
    changed = [n for n in sorted(payloads) if payloads[n] != old[n]]
    check('metadata repair changes exactly metadata and MANIFEST', changed == ['MANIFEST.json', 'metadata.json'], changed)
    check('current actual config equals frozen metadata',
          (PUB / 'zenodo-deposit.json').read_bytes() == payloads['metadata.json'])
    metadata = json.loads(payloads['metadata.json'])['metadata']
    description = metadata['description']
    check('all three named material gaps explicit in deposit description',
          all(s in description for s in ('Duren commentary (2013 online/2014 print)',
                                        "Goh's 1992 coefficient-functional journal article", 'Hibschweiler (1995)')))
    check('deposit acceptance and publication explicitly withheld preparation',
          'preparation draft' in description and 'acceptance and publication clearance remain withheld' in description)
    check('metadata AI/unrefereed/no-human/license/ORCID',
          'AI tools were used extensively' in description and 'unrefereed' in description
          and 'has not received human peer review' in description
          and metadata['license'] == 'cc-by-4.0'
          and metadata['creators'][0]['orcid'] == '0009-0001-9320-500X')

    baseline = payloads['root_reproduction/PRIMARY_AUDIT_BASELINE.tex']
    check('historical manuscript baseline exact', sha(baseline) == BASELINE_SHA)
    split = b'\\section{Attribution, scope and verification}'
    check('current mathematical proof prefix byte exact to historical baseline',
          payloads['support_slit.tex'].split(split)[0] == baseline.split(split)[0])
    mappings = {}
    for n in range(6, 11):
        family = next(p.split('/')[1] for p in payloads if p.startswith(f'reviews/priority{n:02d}'))
        witnesses = [p for p, d in payloads.items() if p.startswith('reviews/' + family + '/')
                     and p.endswith('.json') and BASELINE_SHA.encode() in d]
        check('historical baseline mapped source family ' + family, bool(witnesses), witnesses)
        mappings[family] = witnesses
    snapshot = json.loads((AUDIT / 'ORIGINAL_SNAPSHOT.json').read_bytes())
    check('original source head equals archived manifest provenance', snapshot['head'] == manifest['head'])
    for rec in snapshot['files']:
        blob = subprocess.check_output(['git', 'show', snapshot['head'] + ':' + rec['path']], cwd=AUDIT)
        archived = payloads['original/' + rec['path']]
        check('original Git blob ' + rec['path'], blob == archived
              and sha(blob) == rec['sha256'] and len(blob) == rec['size'])

    eps, eta, T, r = F(1, 10**24), F(1, 10**12), F(7, 4), F(2, 3)
    q = lambda t: t*t-F(2, 5)*t**4
    exact = {
        'area_H_tail': str(r**4/(3*(1-r*r))),
        'area_Hprime_tail': str((1-r*r)**-2-1),
        'q1': str(q(F(1))), 'qT': str(q(T)),
        'tip_gap': str(F(25, 81)-F(3, 10)),
        'reciprocal_square_f_error_over_eta': str(F(14, 5)*r),
        'derivative_numerator_error_over_eta': str(5+2*r*10),
        'V_remainder_over_eps_eta': str(486+18315*eta),
        'Vprime_remainder_over_eps_eta': str(161+45621*eta),
        'Z_remainder_over_eps_eta': str(1541+4662*eta),
        'q_short_endpoint_7over5': str(q(F(7, 5))),
    }
    check('epsilon exact positive eta squared', eps == eta*eta > 0)
    check('weighted tail constants strict', r**4/(3*(1-r*r)) < F(1, 4)
          and (1-r*r)**-2-1 < F(9, 4))
    check('uniform H/Hprime coarse margins', 4*r+2 < 5 and 4+4*F(3, 2) == 10)
    check('reciprocal-square and numerator derivative margins',
          F(14, 5)*r < 2 and 5+2*r*10 < 19 and F(19)/(F(3, 2)**3) < 6)
    check('reciprocal-cube derivative margin', F(1, 3)*5*11/F(125, 8) < 2)
    check('tip/trajectory strict quantitative separation',
          F(7, 25)+7*eta < F(3, 10) < F(25, 81)
          and F(25, 81)-F(3, 10) == F(7, 810) and T+333*eps < F(9, 5))
    check('analytic remainder absorptions', 486+18315*eta < 487
          and 161+45621*eta < 162 and 1541+4662*eta < 2000
          and F(111**2, 2)*eta < 1)
    check('orientation independent from sign expansion', 222*eps/(1-111*eps) < 223*eps < 1)
    check('target signs robust with exact margins', q(F(1))-2000*eta > F(1, 2)
          and q(T)+2000*eta < F(-1, 2))
    check('shortened-segment negative witness control', q(F(7, 5)) > 0)
    check('epsilon zero boundary removes strict signed witnesses', 0*q(F(1)) == 0*q(T) == 0)
    result = {'timestamp_utc': now(), 'status': 'PASS', 'checks': checks, 'count': len(checks),
              'inner_seals': inner, 'historical_baseline_mappings': mappings,
              'exact_math_controls': exact, 'frozen_hashes': FIXED,
              'new_actionable_technical_findings': [],
              'math_component': 'PASS within stated classical premises',
              'portable_package_component': 'PASS',
              'overall_submission_publication_acceptance': 'HOLD',
              'hold_gaps': ['Duren2014 commentary (2013 online)', 'Goh1992 journal', 'Hibschweiler1995'],
              'limits': 'No formal proof or human peer review. Integrity is not authenticity, novelty, or source-gap closure.'}
    (ROOT / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'REPLAY_RECEIPTS.json').write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'count': len(checks), 'execution_receipts': len(receipts),
                      'new_actionable_technical_findings': 0, 'overall': 'HOLD'}))
