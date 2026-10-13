#!/usr/bin/env python3
"""Parent regression replay; NOT a new independent operations review.

The sealed round-2 attack definitions remain unchanged. Only their private
work/output directory is redirected. Added complete-build controls generate
and remove synthetic private fixtures, never actual candidate files.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent
ATTACKS = ROOT / 'reviews/operations_adversary2/independent_controls.py'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def snapshot(root):
    result = {}
    for p in root.rglob('*'):
        info = p.lstat()
        name = p.relative_to(root).as_posix()
        if stat.S_ISLNK(info.st_mode):
            result[name] = ('link', os.readlink(p))
        elif stat.S_ISREG(info.st_mode):
            result[name] = ('file', p.read_bytes())
        else:
            result[name] = ('type', stat.S_IFMT(info.st_mode))
    return result


def setup(m, f):
    (f.package / 'CURRENT_PUBLICATION_NOTES.md').write_bytes(b'Valid synthetic offline note.\n')
    m.write_json(f.package / 'verification/PUBLIC_OUTPUT_WHITELIST.json',
                 {'positive_whitelist_only': True, 'public_files': []})
    m.write_json(f.package / 'REVIEW_EVIDENCE_SELECTION.json',
                 {'positive_explicit_selection': True, 'entries': []})


def run_builder(m, f, arguments, root=None, package=None):
    with patch.multiple(m.builder, ROOT=root or f.audit, PACKAGE=package or f.package), \
         patch.object(sys, 'argv', ['builder', *arguments]), contextlib.redirect_stdout(io.StringIO()):
        m.builder.main()


def reject_unchanged(m, f, arguments, diagnostic, root=None, package=None):
    before = snapshot(f.repo)
    m.rejection(lambda: run_builder(m, f, arguments, root, package), diagnostic)
    require(snapshot(f.repo) == before, 'Rejected build changed private fixture bytes or paths')


def unsafe_output(m, f, name, kind):
    setup(m, f)
    output = f.audit / name if name == 'BRANCH_INSTALL_PLAN.json' else f.package / name
    output.unlink(missing_ok=True)
    target = f.audit / 'unrelated_sentinel.txt'
    target.write_bytes(b'Preserve unrelated private sentinel.\n')
    if kind == 'symlink':
        output.symlink_to(target)
    elif kind == 'dangling':
        output.symlink_to(f.audit / 'nonexistent_target.txt')
    elif kind == 'directory':
        output.mkdir()
    elif kind == 'fifo':
        os.mkfifo(output)
    elif kind == 'hardlink':
        os.link(target, output)
    else:
        raise RuntimeError('Unknown control kind')
    message = 'Symlink in generated' if kind in {'symlink', 'dangling'} else 'Unsafe existing output'
    reject_unchanged(m, f, [], message)


def freeze_output(m, f, kind):
    setup(m, f)
    output = f.audit / 'PACKAGE_REVIEW_INPUT_3.json'
    target = f.audit / 'unrelated_sentinel.txt'
    target.write_bytes(b'Preserve private frozen-output sentinel.\n')
    if kind == 'symlink':
        output.symlink_to(target)
    elif kind == 'dangling':
        output.symlink_to(f.audit / 'nonexistent_target.txt')
    elif kind == 'regular':
        output.write_bytes(b'Existing immutable private freeze.\n')
    else:
        output.mkdir()
    message = 'Symlink in generated' if kind in {'symlink', 'dangling'} else 'Never overwrite a frozen'
    reject_unchanged(m, f, ['--freeze', '3'], message)


def unsafe_root(m, f, kind):
    setup(m, f)
    if kind == 'package_symlink':
        alias = f.audit / 'package_alias'
        alias.symlink_to(f.package, target_is_directory=True)
        reject_unchanged(m, f, [], 'Unsafe output root', package=alias)
    elif kind == 'root_symlink':
        alias = f.repo / 'audit_alias'
        alias.symlink_to(f.audit, target_is_directory=True)
        reject_unchanged(m, f, [], 'Unsafe output root', root=alias)
    else:
        alias = f.repo / 'ancestor_alias'
        alias.symlink_to(f.audit.parent, target_is_directory=True)
        reject_unchanged(m, f, [], 'Unsafe output root', root=alias / f.audit.name)


def successful_build(m, f):
    setup(m, f)
    earlier = (f.audit / f.manifest_name).read_bytes()
    run_builder(m, f, ['--freeze', '3'])
    require((f.audit / f.manifest_name).read_bytes() == earlier, 'Successful build edited earlier freeze')
    freeze = json.loads((f.audit / 'PACKAGE_REVIEW_INPUT_3.json').read_bytes())
    for name, spec in freeze['files'].items():
        data = (f.package / name).read_bytes()
        require(len(data) == spec['bytes'] and m.c.sha(data) == spec['sha256'], 'New freeze byte mismatch')
    manifest = json.loads((f.package / 'SHA256SUMS.json').read_bytes())
    with zipfile.ZipFile(f.package / m.c.ZIP_NAME) as archive:
        require(archive.testzip() is None, 'Successful ZIP CRC failure')
        require(len(archive.namelist()) == len(set(archive.namelist()))
                and set(archive.namelist()) == set(manifest['files']) | {'SHA256SUMS.json'}, 'ZIP entry set differs')
        for name, spec in manifest['files'].items():
            data = archive.read(name)
            require(data == (f.package / name).read_bytes() and len(data) == spec['bytes']
                    and m.c.sha(data) == spec['sha256'], 'ZIP payload byte mismatch')
    plan = json.loads((f.audit / 'BRANCH_INSTALL_PLAN.json').read_bytes())
    selected = set(manifest['files']) | set(freeze['files'])
    require(len(plan['entries']) == len(selected), 'Install entry count differs')
    for item in plan['entries']:
        data = (f.repo / item['local_program_path']).read_bytes()
        require(len(data) == item['bytes'] and m.c.sha(data) == item['sha256'], 'Install byte mismatch')
        require(item['repository_destination'] == m.c.PREPRINT
                + (f.repo / item['local_program_path']).relative_to(f.package).as_posix(), 'Install destination differs')
    for name in ('source_receipt_sha256', 'mathematical_acceptance_gate_sha256', 'branch_install_plan_sha256'):
        source = {'source_receipt_sha256': 'SOURCE_RECEIPT.json',
                  'mathematical_acceptance_gate_sha256': 'MATHEMATICAL_ACCEPTANCE_GATE.json',
                  'branch_install_plan_sha256': 'BRANCH_INSTALL_PLAN.json'}[name]
        require(freeze[name] == m.c.sha((f.audit / source).read_bytes()), 'New freeze cross-binding differs')
    require(not [p for p in f.audit.rglob('.*') if p.is_file()], 'Temporary output file remains')


def main():
    before = hashlib.sha256(ATTACKS.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location('sealed_ops2_attack_replay', ATTACKS)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    private = ROOT / 'private_sources'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='output_repair_controls_', dir=private) as tmp:
        m.HERE = Path(tmp).resolve()
        for name in ['SHA256SUMS.json', m.c.ZIP_NAME, 'ARCHIVE_RECEIPT.json', 'deposit.json', 'BRANCH_INSTALL_PLAN.json']:
            for kind in ['symlink', 'dangling', 'directory', 'fifo', 'hardlink']:
                m.case('parent_output_' + name + '_' + kind, lambda f, name=name, kind=kind: unsafe_output(m, f, name, kind))
        for kind in ['symlink', 'dangling', 'regular', 'directory']:
            m.case('parent_freeze_' + kind, lambda f, kind=kind: freeze_output(m, f, kind))
        for number in ['0', '-1']:
            def invalid(f, number=number):
                setup(m, f)
                reject_unchanged(m, f, ['--freeze', number], 'Invalid review round')
            m.case('parent_invalid_freeze_' + number, invalid)
        for kind in ['package_symlink', 'root_symlink', 'ancestor_symlink']:
            m.case('parent_unsafe_root_' + kind, lambda f, kind=kind: unsafe_root(m, f, kind))
        m.case('parent_successful_complete_build_and_new_freeze', lambda f: successful_build(m, f))
        m.main()  # exact original 160 independent expectations, unmodified
        suffix = 'OPTIMIZED' if not __debug__ else 'NORMAL'
        result = json.loads((m.HERE / ('INDEPENDENT_CONTROLS_' + suffix + '.json')).read_bytes())
        require(result['case_count'] == 195 and result['passed_count'] == 195
                and result['all_passed'] is True and result['real_external_calls'] == 0, 'Repair controls failed')
        result['replay_by'] = 'Parent regression replay, not a new independent review'
        result['sealed_attack_source_sha256'] = before
        result['current_builder_sha256'] = hashlib.sha256((ROOT / 'build_preprint_package.py').read_bytes()).hexdigest()
        require(hashlib.sha256(ATTACKS.read_bytes()).hexdigest() == before, 'Historical attack source changed')
        (ROOT / ('ARCHIVE_OUTPUT_REPAIR_CONTROLS_' + suffix + '.json')).write_bytes(m.c.json_bytes(result))


if __name__ == '__main__':
    main()
