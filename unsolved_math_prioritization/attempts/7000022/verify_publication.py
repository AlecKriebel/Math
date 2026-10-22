#!/usr/bin/env python3
"""Portable byte and finite-control verification; not a general conjecture proof."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = (
    ('geometry_7000022', 'GEOMETRY_7000022_AUTHOR_SAFE_FREEZE.zip', 34700,
     '5bd080b117c98900da18f44084511654b2161f9fbffc9acc9129657cff40996f', 'AUTHOR_MANIFEST.json'),
    ('geometry_7000022_independent_audit', 'GEOMETRY_7000022_INDEPENDENT_AUDIT_SAFE_FREEZE.zip', 19920,
     '3295c4809afc9e1b30b7223280b833960345f9c1743cfe88b467afba81e3f19c', 'AUDIT_MANIFEST.json'),
)
MUTATIONS = (
    ('single_planar_area_instead_of_double', 'square_surface=2*square_planar', 'square_surface=square_planar'),
    ('wrong_mean_width_coefficient', 'mean=scale(pi,F(1,16))', 'mean=scale(pi,F(1,8))'),
    ('missing_pole_edge_length', 'le=add(scalar(2*h),', 'le=add(scalar(0),'),
    ('half_intrinsic_pole_distance', 'd=scale(root(h*h+F(1,2)),2)', 'd=scale(root(h*h+F(1,2)),1)'),
    ('wrong_support_gradient_sign', 'energy=average_z(padd(pmul(hp,hp),pscale(grad2,F(-1,2))))',
     'energy=average_z(padd(pmul(hp,hp),pscale(grad2,F(1,2))))'),
    ('wrong_tree_length', 'assert tree_length==scalar(6)', 'assert tree_length==scalar(3)'),
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def unique(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(blob):
    return json.loads(blob, object_pairs_hook=unique)


def read(path):
    return decode(path.read_bytes())


def safe(value):
    need(isinstance(value, str) and value and '\\' not in value, 'unsafe path')
    p = PurePosixPath(value)
    need(str(p) == value and not p.is_absolute() and '..' not in p.parts, 'unsafe path')
    return value


def matches(blob, item):
    return len(blob) == item['bytes'] and hashlib.sha256(blob).hexdigest() == item['sha256']


def integrity():
    manifest = read(ROOT / 'PUBLICATION_MANIFEST.json')
    entries = manifest['files']
    names = [safe(x['path']) for x in entries]
    need(len(names) == len(set(names)), 'duplicate manifest path')
    nodes = list(ROOT.rglob('*'))
    need(not any(p.is_symlink() for p in nodes), 'symlink in publication')
    actual = {p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()}
    need(actual == set(names) | {'PUBLICATION_MANIFEST.json'}, 'strict inventory mismatch')
    for item in entries:
        need(matches((ROOT / item['path']).read_bytes(), item), 'publication content mismatch: ' + item['path'])
    for folder, name, size, digest, manifest_name in ARCHIVES:
        raw = (ROOT / 'freeze' / name).read_bytes()
        need(matches(raw, {'bytes': size, 'sha256': digest}), 'archive pin mismatch')
        with zipfile.ZipFile(ROOT / 'freeze' / name) as archive:
            archive_names = archive.namelist()
            need(len(archive_names) == len(set(archive_names)) == 9, 'archive inventory count mismatch')
            for n in archive_names:
                safe(n)
                need(n.startswith(folder + '/'), 'unexpected archive prefix')
                need(archive.read(n) == (ROOT / n).read_bytes(), 'frozen member mismatch: ' + n)
            frozen = decode(archive.read(folder + '/' + manifest_name))
            frozen_paths = [safe(x['path']) for x in frozen['files']]
            need(len(frozen_paths) == len(set(frozen_paths)) == 8, 'frozen manifest inventory mismatch')
            need(set(archive_names) == {folder + '/' + p for p in frozen_paths + [manifest_name]}, 'archive manifest mismatch')
            need({p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*') if p.is_file()} == set(archive_names), 'expanded inventory mismatch')
            for item in frozen['files']:
                need(matches(archive.read(folder + '/' + item['path']), item), 'frozen manifest content mismatch')
    status = read(ROOT / 'CURRENT_STATUS.json')
    need(status['problem_id'] == 7000022 and status['rank'] == 749, 'identity mismatch')
    need(status['status'] == 'unsolved' and status['turns'] == '5/5', 'disposition mismatch')
    need(status['full_target_resolved'] is False and status['novelty_claimed'] is False, 'scope inflation')
    frozen_input = read(ROOT / 'geometry_7000022_independent_audit/FROZEN_INPUT_MANIFEST.json')
    need(frozen_input['file_count'] == 9, 'audit input count mismatch')
    for item in frozen_input['files']:
        need(matches((ROOT / 'geometry_7000022' / safe(item['path'])).read_bytes(), item), 'audit input mismatch')
    return {'status': 'PASS', 'publication_files': len(actual), 'unchanged_archives': 2, 'unchanged_expanded_files': 18}


def run(script, args=()):
    # -I ignores PYTHONOPTIMIZE and other caller environment settings. We never
    # inherit -O/-OO from this wrapper; assertions are required in frozen scripts.
    result = subprocess.run([sys.executable, '-I', '-B', str(script)] + list(map(str, args)),
                            cwd=script.parent, capture_output=True, text=True)
    need(result.returncode == 0, 'replay failed: ' + script.name + '\n' + result.stderr)
    need(not result.stderr, 'unexpected replay stderr: ' + script.name)
    return decode(result.stdout)


def replay():
    with tempfile.TemporaryDirectory(prefix='curve-area-replay-') as directory:
        temp = Path(directory)
        author = temp / 'author'
        audit = temp / 'audit'
        shutil.copytree(ROOT / 'geometry_7000022', author)
        shutil.copytree(ROOT / 'geometry_7000022_independent_audit', audit)
        author_summary = run(author / 'verify.py')
        need(author_summary['status'] == 'all_exact_controls_passed', 'author did not pass')
        need((author / 'CHECK_RESULTS.json').read_bytes() == (ROOT / 'geometry_7000022/CHECK_RESULTS.json').read_bytes(), 'author replay bytes differ')
        standalone = run(audit / 'independent_verify.py')
        need(standalone['audit_control_status'] == 'PASS', 'standalone audit did not pass')
        need((audit / 'INDEPENDENT_CHECK_RESULTS.json').read_bytes() == (ROOT / 'geometry_7000022_independent_audit/INDEPENDENT_CHECK_RESULTS.json').read_bytes(), 'standalone replay bytes differ')
        crosscheck = run(audit / 'independent_verify.py', ('--author', author))
        need(crosscheck['audit_control_status'] == 'PASS' and crosscheck['full_target_resolved'] is False, 'audit scope mismatch')
        need(len(crosscheck['author_saved_certificate_crosschecks']) == 12, 'missing author certificate crosschecks')
        need((audit / 'INDEPENDENT_CHECK_RESULTS.json').read_bytes() == (ROOT / 'geometry_7000022_independent_audit/INDEPENDENT_CHECK_RESULTS.json').read_bytes(), 'crosschecked replay bytes differ')
        saved = read(audit / 'INDEPENDENT_CHECK_RESULTS.json')
        negative = saved['negative_controls_rejected']
        need(len(negative) == 8 and all(value is True for value in negative.values()), 'false surrogate controls failed')
        source = (audit / 'independent_verify.py').read_text()
        mutations = []
        for label, old, new in MUTATIONS:
            need(source.count(old) == 1, 'mutation target ambiguous: ' + label)
            script = temp / (label + '.py')
            script.write_text(source.replace(old, new))
            result = subprocess.run([sys.executable, '-I', '-B', str(script)], cwd=temp, capture_output=True, text=True)
            need(result.returncode != 0 and 'AssertionError' in result.stderr, 'mutation not rejected: ' + label)
            mutations.append({'mutation': label, 'rejected': True, 'exit_code': result.returncode})
        return {'status': 'PASS', 'assertions_enabled_in_children': True,
                'author_replay_byte_identical': True, 'independent_standalone_byte_identical': True,
                'independent_crosschecked_byte_identical': True, 'author_certificate_crosschecks': 12,
                'false_surrogate_controls_rejected': 8, 'implementation_mutations': mutations,
                'author': author_summary, 'audit': crosscheck}


def main():
    before = integrity()
    controls = replay()
    need(integrity() == before, 'publication changed during replay')
    return {'publication_verification': 'PASS', 'problem_id': 7000022,
            'full_target_resolved': False, 'status': 'unsolved', 'turns': '5/5',
            'wrapper_optimization': sys.flags.optimize, 'integrity': before, 'finite_controls': controls,
            'limitations': 'Finite checks and byte consistency only; no formal analytic proof or novelty certification.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
