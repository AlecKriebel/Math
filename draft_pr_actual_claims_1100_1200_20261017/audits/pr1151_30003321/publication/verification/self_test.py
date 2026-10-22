#!/usr/bin/env python3
"""Adversarial packaging regression checks in small synthetic local fixtures.

No actual paper/PDF/metadata or existing package output is changed. Synthetic
PDF bytes test packaging mechanics only and are not a PDF rendering test.
"""
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
_script = Path(os.path.abspath(__file__))
_helper = _script.parent / 'package_common.py'
for _input in (_script, _helper):
    for _component in reversed([_input, *_input.parents]):
        if _component.is_symlink():
            raise ValueError('symlink ancestor/member: ' + str(_component))
sys.path.insert(0, str(_helper.parent))
from package_common import (HERE, KIT, PDF, PREFIX, PUBLICATION_MEMBERS, SOURCE,
                            audit_root, byte_pin, encoded, need, read, safe)


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def save(path, value):
    put(path, encoded(value))


def invoke(script, optimized=False):
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(script)]
    return subprocess.run(command, capture_output=True, timeout=300)


def fixture(root):
    root.mkdir()
    audit = root / PREFIX
    audit.mkdir(parents=True)
    scripts = ['build_package.py'] + [name for name in PUBLICATION_MEMBERS
                                    if name.startswith('verification/')
                                    and name != 'verification/AUDIT_MEMBERS.json'
                                    and name != 'verification/REPLAY_RECEIPT.json']
    for name in scripts:
        put(root / name, read(HERE / name))
    put(audit / 'verify_finite_signs.py', read(audit_root() / 'verify_finite_signs.py'))
    put(audit / 'authored-note.md', b'Synthetic authored fixture; no mathematical claim.\n')
    put(root / 'main.tex', b'% Synthetic fixture source; not the released paper.\n')
    put(root / 'README.md', b'Synthetic package fixture.\n')
    put(root / 'LICENSE.txt', b'Synthetic fixture.\n')
    put(root / 'output/pdf' / PDF, b'%PDF-1.4\nSynthetic format-only packaging fixture.\n')
    save(audit / 'ROOT_PDF_QA.json', {'source': byte_pin((root / 'main.tex').read_bytes()),
         'pdf': byte_pin((root / 'output/pdf' / PDF).read_bytes()), 'pages': 1,
         'fixture_only': True})
    save(root / 'verification/AUDIT_MEMBERS.json',
         {name: byte_pin((audit / name).read_bytes())
          for name in ['verify_finite_signs.py', 'ROOT_PDF_QA.json', 'authored-note.md']})
    metadata = {'title': 'Synthetic package fixture; not a deposit', 'upload_type': 'publication'}
    save(root / 'zenodo-metadata.json', metadata)
    save(root / 'zenodo-deposit.json', {'metadata': metadata,
         'files': [{'path': 'output/pdf/' + PDF}, {'path': 'output/' + SOURCE}]})
    result = invoke(root / 'verification/verify_all.py')
    need(result.returncode == 0 and result.stderr == b'', 'fixture setup verification failed: ' + result.stderr.decode())
    put(root / 'verification/REPLAY_RECEIPT.json', result.stdout)
    return root


def snapshot(root):
    result = {}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = ('symlink', os.readlink(path))
        elif path.is_file():
            result[relative] = ('file', byte_pin(path.read_bytes()))
        elif path.is_dir():
            result[relative] = ('directory',)
        else:
            result[relative] = ('other',)
    return result


def main():
    need(len(sys.argv) == 1, 'self-test accepts no command-line arguments')
    checks = []
    scratch_parent = safe(audit_root() / 'families/package_tooling_01/private')
    scratch_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.package-self-test-', dir=scratch_parent) as temporary:
        scratch = Path(temporary)
        good = fixture(scratch / 'good')
        for name in ('build_package.py', 'verification/package_common.py',
                     'verification/verify_all.py', 'verification/self_test.py'):
            need(not any(isinstance(node, ast.Assert)
                         for node in ast.walk(ast.parse((good / name).read_text()))),
                 'assert in package verification: ' + name)
        need(not any(isinstance(node, ast.Assert) for node in ast.walk(
             ast.parse((good / PREFIX / 'verify_finite_signs.py').read_text()))),
             'assert in substantive finite diagnostic')
        checks.append('explicit_checks_survive_optimization')
        before = snapshot(good)
        result = subprocess.run([sys.executable, str(good / 'verification/verify_all.py')],
                                capture_output=True, timeout=300)
        need(result.returncode == 0 and result.stderr == b'' and snapshot(good) == before,
             'verifier wrote files when invoked without -B')
        checks.append('read_only_verifier_without_bytecode_flag')
        first = invoke(good / 'build_package.py')
        need(first.returncode == 0 and first.stderr == b'', 'normal fixture build failed: ' + first.stderr.decode())
        frozen = {name: (good / 'output' / name).read_bytes() for name in (SOURCE, KIT)}
        second = invoke(good / 'build_package.py', True)
        need(second.returncode == 0 and second.stderr == b'' and first.stdout == second.stdout,
             'optimized build/receipt differ')
        need(all((good / 'output' / name).read_bytes() == data for name, data in frozen.items()),
             'repeated source/kit bytes differ')
        checks.append('normal_optimized_builds_byte_identical')
        with zipfile.ZipFile(good / 'output' / KIT) as archive:
            need(set(archive.namelist()) == {PDF, SOURCE, 'README.md', 'zenodo-metadata.json', 'zenodo-deposit.json'},
                 'nonflat/wrong kit inventory')
            need(archive.read(PDF) == (good / 'output/pdf' / PDF).read_bytes()
                 and archive.read(SOURCE) == frozen[SOURCE]
                 and archive.read('zenodo-metadata.json') == (good / 'zenodo-metadata.json').read_bytes(),
                 'kit payload/metadata bytes differ')
            portable = json.loads(archive.read('zenodo-deposit.json'))
            original = json.loads((good / 'zenodo-deposit.json').read_bytes())
            need(portable['metadata'] == original['metadata']
                 and portable['files'] == [{'path': PDF}, {'path': SOURCE}], 'portable deposit differs')
        checks.append('flat_kit_exact_payloads_and_portable_deposit')
        extracted = scratch / 'arbitrary extraction with spaces'
        with zipfile.ZipFile(good / 'output' / SOURCE) as archive:
            archive.extractall(extracted)
        original_replay = (good / 'verification/REPLAY_RECEIPT.json').read_bytes()
        for optimized in (False, True):
            result = invoke(extracted / 'verification/verify_all.py', optimized)
            need(result.returncode == 0 and result.stderr == b'' and result.stdout == original_replay,
                 'portable extracted replay failed')
        result = invoke(extracted / 'build_package.py')
        need(result.returncode == 0 and result.stderr == b'', 'portable extracted rebuild failed: ' + result.stderr.decode())
        need(all((extracted / 'output' / name).read_bytes() == data for name, data in frozen.items()),
             'portable rebuilt archives differ')
        checks.append('arbitrary_root_source_extract_verify_and_rebuild')

        # The following controls each use a fresh small copy, never actual outputs.
        counter = 0

        def negative(label, mutate, expected, verification=False):
            nonlocal counter
            counter += 1
            case = scratch / ('case-' + str(counter))
            # Initial-layout fixture has no SOURCE_MANIFEST, permitting isolated
            # runner controls without an earlier manifest mismatch masking them.
            shutil.copytree(good, case)
            for name in (SOURCE, KIT):
                put(case / 'output' / name, ('sentinel-' + name).encode())
            put(case / 'PACKAGE_RECEIPT.json', b'sentinel-receipt')
            script = mutate(case) or (case / ('verification/verify_all.py' if verification else 'build_package.py'))
            before = snapshot(scratch)
            for optimized in (False, True):
                result = invoke(script, optimized)
                need(result.returncode != 0 and expected in result.stderr.decode('utf-8', errors='replace'),
                     'negative control failed: ' + label + '/' + str(optimized) + '\n' + result.stderr.decode('utf-8', errors='replace'))
                need(snapshot(scratch) == before, 'negative invocation wrote files: ' + label)
            checks.append(label + '_normal_and_optimized_no_writes')
            shutil.rmtree(case)

        def allow_extra(case, name):
            path = case / 'verification/AUDIT_MEMBERS.json'
            allowed = json.loads(path.read_bytes())
            allowed[name] = byte_pin(b'not read')
            save(path, allowed)

        negative('parent_allowlist', lambda p: allow_extra(p, '../escape'), 'absolute/parent member')
        negative('absolute_allowlist', lambda p: allow_extra(p, '/escape'), 'absolute/parent member')
        negative('noncanonical_allowlist', lambda p: allow_extra(p, 'a//b'), 'noncanonical/nonportable')
        negative('private_allowlist', lambda p: allow_extra(p, 'private/x.json'), 'excluded audit member')
        negative('log_allowlist', lambda p: allow_extra(p, 'RESEARCH_LOG.md'), 'log/gate audit member')
        negative('final_review_allowlist', lambda p: allow_extra(p, 'families/final_review/REPORT.md'), 'final review is outside')

        def tamper_audit(case):
            put(case / PREFIX / 'authored-note.md', b'changed authored byte')
        negative('authored_byte_tamper', tamper_audit, 'authored member pin mismatch', True)

        def wrong_positive(case):
            path = case / 'verification/EXPECTED_FINITE_SIGNS.stdout.json'
            wrong = json.loads(path.read_bytes())
            wrong['counts']['nodes'] += 1
            # Maintain PASS and a self-consistent baseline pin to isolate the
            # whole-output comparison against the actual computation.
            put(path, (json.dumps(wrong, sort_keys=True) + '\n').encode())
            control_path = case / 'verification/CONTROL_PLAN.json'
            plan = json.loads(control_path.read_bytes())
            plan['expected_stdout'] = byte_pin(path.read_bytes())
            save(control_path, plan)
        negative('wrong_count_with_pass_and_updated_pin', wrong_positive, 'complete positive output mismatch', True)

        def mask_mutation(case):
            path = case / PREFIX / 'verify_finite_signs.py'
            data = path.read_bytes().replace(b'opt = ap.parse_args()', b'opt = ap.parse_args()\n    opt.mutation = None')
            put(path, data)
            allowed_path = case / 'verification/AUDIT_MEMBERS.json'
            allowed = json.loads(allowed_path.read_bytes())
            allowed['verify_finite_signs.py'] = byte_pin(data)
            save(allowed_path, allowed)
            control_path = case / 'verification/CONTROL_PLAN.json'
            plan = json.loads(control_path.read_bytes())
            plan['diagnostic_source'] = byte_pin(data)
            save(control_path, plan)
        negative('masked_actual_mutation', mask_mutation, 'actual mathematical mutation did not fail', True)

        def symlink_diagnostic(case):
            path = case / PREFIX / 'verify_finite_signs.py'
            target = case / 'kept-source.py'
            path.rename(target)
            path.symlink_to(target)
        negative('symlink_input_member', symlink_diagnostic, 'symlink ancestor/member')

        def symlink_audit(case):
            audit = case / PREFIX
            target = case / 'kept-audit'
            audit.rename(target)
            audit.symlink_to(target, target_is_directory=True)
        negative('symlink_input_ancestor', symlink_audit, 'symlink ancestor/member')

        def symlink_helper(case):
            path = case / 'verification/package_common.py'
            target = case / 'kept-helper.py'
            path.rename(target)
            path.symlink_to(target)
        negative('symlink_helper_before_import', symlink_helper, 'symlink ancestor/member')

        def symlink_helper_directory(case):
            path = case / 'verification'
            target = case / 'kept-verification'
            path.rename(target)
            path.symlink_to(target, target_is_directory=True)
        negative('symlink_helper_ancestor_before_import', symlink_helper_directory, 'symlink ancestor/member')

        def symlink_output(case, relative):
            path = case / relative
            path.unlink()
            # The linked input is an actual source, testing no-clobber behavior.
            path.symlink_to(case / 'main.tex')
        for relative in ('output/' + SOURCE, 'output/' + KIT, 'PACKAGE_RECEIPT.json'):
            negative('symlink_output_' + Path(relative).name,
                     lambda p, rel=relative: symlink_output(p, rel), 'symlink ancestor/member')

        def directory_output(case, relative):
            path = case / relative
            path.unlink()
            path.mkdir()
        for relative in ('output/' + SOURCE, 'output/' + KIT, 'PACKAGE_RECEIPT.json'):
            negative('directory_output_' + Path(relative).name,
                     lambda p, rel=relative: directory_output(p, rel), 'output destination is not a regular file')

        def symlink_output_ancestor(case):
            path = case / 'output'
            target = case / 'kept-output'
            path.rename(target)
            path.symlink_to(target, target_is_directory=True)
        negative('symlink_output_ancestor', symlink_output_ancestor, 'symlink ancestor/member')

        def nondirectory_output_ancestor(case):
            (case / 'output').rename(case / 'kept-output')
            put(case / 'output', b'not a directory')
        negative('nondirectory_output_ancestor', nondirectory_output_ancestor, 'ancestor is not a directory')

        def outer_symlink(case):
            link = case / 'alias-parent'
            link.symlink_to(case, target_is_directory=True)
            return link / 'build_package.py'
        negative('symlink_above_distribution_root', outer_symlink, 'symlink ancestor/member')

        for relative in ('main.tex', PREFIX + '/authored-note.md'):
            path = extracted / relative
            saved = path.read_bytes()
            put(path, saved + b'\nTAMPER\n')
            for optimized in (False, True):
                result = invoke(extracted / 'verification/verify_all.py', optimized)
                need(result.returncode != 0 and b'mismatch' in result.stderr, 'extracted manifest tamper not rejected')
            put(path, saved)
        checks.append('extracted_publication_and_audit_tamper_normal_and_optimized')
    sys.stdout.buffer.write(encoded({'status': 'PASS', 'checks': checks,
        'check_count': len(checks), 'synthetic_fixtures_only': True,
        'actual_release_outputs_modified': False}))


if __name__ == '__main__':
    main()
