"""Physical negative controls for the publication verifier; own disposable copies."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'tmp/portable-input'
FIXTURE = ROOT / 'tmp/attack-fixture'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def manifest_repair(root):
    path = root / 'MANIFEST.json'
    m = json.loads(path.read_bytes())
    for row in m['files']:
        row.update(identity((root / row['path']).read_bytes()))
    path.write_text(json.dumps(m))


def edit_json(root, name, action, repair=False):
    p = root / name
    v = json.loads(p.read_bytes())
    action(v)
    p.write_text(json.dumps(v))
    if repair:
        manifest_repair(root)


def append(root, name, repair=False):
    p = root / name
    p.write_bytes(p.read_bytes() + b'\nchanged')
    if repair:
        manifest_repair(root)


def run_case(name, mutate, reject=True, build=False, pdf=None, inside=False):
    if FIXTURE.exists():
        shutil.rmtree(FIXTURE)
    shutil.copytree(SOURCE, FIXTURE)
    mutate(FIXTURE)
    command = [sys.executable, '-O', '-B', str(FIXTURE /
               ('build_package.py' if build else 'verify_bundle.py'))]
    if build:
        command += ['--output-dir', str(FIXTURE / 'new-output' if inside
                    else ROOT / 'tmp/attack-output'),
                    '--pdf', str(pdf or ROOT / 'output/pdf/paper.pdf')]
    else:
        command += ['--integrity-only', '--pdf', str(pdf or ROOT / 'output/pdf/paper.pdf')]
    env = os.environ.copy()
    env['PYTHONOPTIMIZE'] = '2'
    r = subprocess.run(command, capture_output=True, text=True, cwd='/', env=env, timeout=60)
    require((r.returncode != 0) == reject, 'Unexpected attack disposition: ' + name)
    return {'case': name, 'expected_rejection': reject, 'rejected': r.returncode != 0,
            'exit': r.returncode, 'diagnostic': r.stderr.splitlines()[-1] if r.stderr else None}


def main():
    before = {p.relative_to(SOURCE).as_posix(): p.read_bytes()
              for p in SOURCE.rglob('*') if p.is_file()}
    rows = []
    def case(*a, **kw):
        rows.append(run_case(*a, **kw))
    case('unmodified_physical_baseline', lambda r: None, reject=False)
    case('duplicate_manifest', lambda r: edit_json(r, 'MANIFEST.json',
         lambda m: m['files'].append(m['files'][0])))
    case('unsafe_parent_path', lambda r: edit_json(r, 'MANIFEST.json',
         lambda m: m['files'][0].update(path='../escape')))
    case('unsafe_absolute_path', lambda r: edit_json(r, 'MANIFEST.json',
         lambda m: m['files'][0].update(path='/escape')))
    case('self_manifest_row', lambda r: edit_json(r, 'MANIFEST.json',
         lambda m: m['files'][0].update(path='MANIFEST.json')))
    case('changed_paper', lambda r: append(r, 'paper.tex'))
    case('extra_file', lambda r: (r / 'extra').write_text('extra'))
    case('missing_file', lambda r: (r / 'paper.tex').unlink())
    case('symlink', lambda r: (r / 'extra-link').symlink_to('paper.tex'))
    case('fifo', lambda r: os.mkfifo(r / 'extra-fifo'))
    case('empty_directory', lambda r: (r / 'extra-directory').mkdir())
    case('metadata_changed_outer_manifest_repaired', lambda r:
         edit_json(r, 'zenodo-metadata.json',
                   lambda m: m['metadata'].update(title='wrong title'), True))
    case('original_changed_outer_manifest_repaired', lambda r:
         append(r, 'historical_candidate/author/PROOF.md', True))
    case('review_changed_outer_manifest_repaired', lambda r:
         append(r, 'audit/review_spectral_family/REPORT.md', True))
    case('review_manifest_changed_outer_manifest_repaired', lambda r:
         edit_json(r, 'audit/review_spectral_family/MANIFEST.json',
                   lambda m: m.update(changed=True), True))
    case('priority_overclaim_outer_manifest_repaired', lambda r:
         edit_json(r, 'audit/PRIORITY_GATE.json',
                   lambda m: m.update(historical_first_priority_certified=True), True))
    wrong_pdf = ROOT / 'tmp/wrong.pdf'
    wrong_pdf.write_bytes(b'%PDF-1.5\nwrong PDF\n')
    case('wrong_downloaded_pdf', lambda r: None, pdf=wrong_pdf)
    case('rebuild_wrong_pdf', lambda r: None, build=True, pdf=wrong_pdf)
    case('rebuild_internal_output', lambda r: None, build=True, inside=True)
    case('rebuild_changed_closed_paper', lambda r: append(r, 'paper.tex'), build=True)
    require(before == {p.relative_to(SOURCE).as_posix(): p.read_bytes()
                       for p in SOURCE.rglob('*') if p.is_file()}, 'Source mutated')
    shutil.rmtree(FIXTURE)
    wrong_pdf.unlink()
    receipt = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'status': 'PASS', 'physical_baselines': 1, 'negative_controls': len(rows)-1,
               'outer_flags': ['-O', '-B'], 'environment_PYTHONOPTIMIZE': '2',
               'source_zip': identity((ROOT / 'source-and-verification.zip').read_bytes()),
               'all_closed_inputs_unchanged': True, 'cases': rows,
               'scope': 'Physical integrity guards, not a mathematical proof certificate.'}
    print(json.dumps(receipt, indent=2), flush=True)
    (ROOT / 'ROOT_GUARD_ATTACKS.json').write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
