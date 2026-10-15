"""Independent read-only candidate integrity and AST audit; write only local receipts."""
import ast
import hashlib
import io
import json
import pathlib
import re
import subprocess
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PUB = ROOT / 'publication'
REPO = ROOT.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def demand(ok, label):
    if not ok:
        raise RuntimeError(label)


def main():
    manifest = json.loads((PUB / 'PACKAGE_MANIFEST.json').read_text())
    records = manifest['files']
    wanted = [r['path'] for r in records]
    demand(len(wanted) == len(set(wanted)) == 126, 'unique126 inventory')
    demand(wanted == sorted(wanted), 'sorted inventory')
    for row in records:
        body = (PUB / row['path']).read_bytes()
        demand(len(body) == row['bytes'] and digest(body) == row['sha256'], row['path'])
    selected = [PUB / name for name in ('research_note.tex', 'research_note.pdf',
                'README.md', 'SUPPLEMENT.md', 'run_checks.py', 'metadata.json')]
    for directory in ('checks', 'expected', 'evidence'):
        selected.extend(p for p in (PUB / directory).rglob('*') if p.is_file())
    demand(sorted(p.relative_to(PUB).as_posix() for p in selected) == wanted,
           'recipe selection equals inventory')
    rebuilt_manifest = json.dumps({k: v for k, v in manifest.items() if k != 'files'} |
                                  {'files': records}, indent=2) + '\n'
    demand(rebuilt_manifest.encode() == (PUB / 'PACKAGE_MANIFEST.json').read_bytes(),
           'manifest deterministic serialization')
    archive = PUB / 'local_deformation_devissage_source_verification_v1.zip'
    selected.append(PUB / 'PACKAGE_MANIFEST.json')
    prefix = 'local_deformation_devissage_v1/'
    with zipfile.ZipFile(archive) as z:
        expected_names = [prefix + p.relative_to(PUB).as_posix()
                          for p in sorted(selected, key=lambda p: p.relative_to(PUB).as_posix())]
        demand(z.namelist() == expected_names, 'exact127 sorted archive names')
        demand(z.testzip() is None, 'all CRCs')
        for info in z.infolist():
            demand(info.date_time == (2026, 10, 12, 0, 0, 0), 'fixed time')
            demand(info.create_system == 3 and info.external_attr == 0o100644 << 16,
                   'fixed Unix regular file permissions')
            demand(info.compress_type == zipfile.ZIP_DEFLATED, 'compression')
            demand(info.extra == b'' and info.comment == b'', 'no hidden fields')
            demand(z.read(info) == (PUB / info.filename[len(prefix):]).read_bytes(),
                   'exact archived bytes')
            demand('/raw/' not in info.filename and not info.filename.endswith('.png'),
                   'no third-party bodies or renders')
        demand(z.comment == b'', 'no archive comment')
    rebuilt = io.BytesIO()
    with zipfile.ZipFile(rebuilt, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(selected, key=lambda p: p.relative_to(PUB).as_posix()):
            info = zipfile.ZipInfo(prefix + path.relative_to(PUB).as_posix(),
                                   date_time=(2026, 10, 12, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, path.read_bytes())
    demand(rebuilt.getvalue() == archive.read_bytes(), 'entire deterministic ZIP bytes')
    (HERE / 'receipts/independently_rebuilt.zip').write_bytes(rebuilt.getvalue())

    pins = json.loads((PUB / 'evidence/SUBMITTED_PINS.json').read_text())
    demand(len(pins['files']) == 27, '27 original files')
    original_rows = []
    for row in pins['files']:
        result = subprocess.run(['git', 'show', pins['head_commit'] + ':' + row['repository_path']],
                                cwd=REPO, capture_output=True, check=True)
        data = result.stdout
        demand(len(data) == row['size'] and digest(data) == row['sha256'], 'git original pin')
        demand(data == (ROOT / 'submitted' / row['relative']).read_bytes() ==
                    (PUB / 'evidence/submitted' / row['relative']).read_bytes(), 'both snapshot copies')
        original_rows.append({'path': row['relative'], 'sha256': digest(data), 'git_bytes_match': True})
    oldmanifest = json.loads((PUB / 'evidence/submitted/PUBLICATION_MANIFEST.json').read_text())
    for row in oldmanifest['files']:
        data = (PUB / 'evidence/submitted' / row['path']).read_bytes()
        demand(len(data) == row['bytes'] and digest(data) == row['sha256'], 'historical seal hash')

    copy_receipt = json.loads((PUB / 'evidence/PACKAGE_REVIEW_01_COPY.json').read_text())
    for row in copy_receipt['files']:
        data = (PUB / row['path']).read_bytes()
        relative = row['path'].removeprefix('evidence/package_review_01/')
        demand(data == (ROOT / 'reviews/package_01' / relative).read_bytes(), 'review unchanged copy')
        demand(len(data) == row['bytes'] and digest(data) == row['sha256'], 'copy receipt pin')

    original = ast.parse((PUB / 'evidence/functor_review_01/verify_functor_identities.py').read_text())
    adapted = ast.parse((PUB / 'checks/verify_functor_identities_explicit_guards.py').read_text())
    guards = json.loads((PUB / 'evidence/GUARD_ADAPTATION.json').read_text())
    assertions = [n for n in ast.walk(original) if isinstance(n, ast.Assert)]
    demands = [n for n in ast.walk(adapted) if isinstance(n, ast.Call) and
               isinstance(n.func, ast.Name) and n.func.id == 'require']
    demand(len(assertions) == len(demands) == len(guards['guards']) == 11, 'all11 guards')
    for assertion, call, record in zip(assertions, demands, guards['guards']):
        demand(ast.dump(assertion.test) == ast.dump(call.args[0]) == record['test_ast'],
               'predicate exact AST')
        demand(isinstance(call.args[1], ast.Constant) and call.args[1].value ==
               'original assertion at line ' + str(assertion.lineno), 'guard message')
    helper = [n for n in adapted.body if isinstance(n, ast.FunctionDef) and n.name == 'require']
    demand(len(helper) == 1, 'one helper')
    expected_helper = ast.parse('def require(test, message):\n if not test:\n  raise RuntimeError(message)\n').body[0]
    demand(ast.dump(helper[0]) == ast.dump(expected_helper), 'helper semantics')
    adapted.body.remove(helper[0])

    class Undo(ast.NodeTransformer):
        def visit_Expr(self, node):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'require':
                return ast.Assert(test=node.value.args[0], msg=None)
            return self.generic_visit(node)

    restored = Undo().visit(adapted)
    demand(ast.dump(restored) == ast.dump(original), 'ENTIRE module AST restored exactly')
    for path, sha in [('original', guards['original_sha256']), ('adapted', guards['adapted_sha256'])]:
        target = PUB / 'evidence' / guards[path]
        demand(digest(target.read_bytes()) == sha, 'guard source pin')
    for name in ('check_conjugacy.py', 'verify_exact.py'):
        demand((PUB / 'checks/current' / name).read_bytes() ==
               (PUB / 'evidence/submitted/current' / name).read_bytes(), 'unchanged math source')
    demand((PUB / 'checks/check_corrected_case.py').read_bytes() ==
           (PUB / 'evidence/submitted/check_corrected_case.py').read_bytes(), 'unchanged adapter')
    demand((PUB / 'expected/FINITE_CONTRACT.json').read_bytes() ==
           (PUB / 'evidence/submitted/FINITE_CONTRACT.json').read_bytes(), 'unchanged contract')

    metadata = json.loads((PUB / 'metadata.json').read_text())
    deposit = json.loads((PUB / 'zenodo-deposit.json').read_text())
    demand(deposit['metadata'] == metadata, 'deposit metadata exact')
    demand(metadata['title'] == 'A characteristic-two counterexample to dévissage for local deformation functors', 'title')
    demand(metadata['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                                   'orcid': '0009-0001-9320-500X'}], 'author ORCID')
    demand(metadata['publication_date'] == '2026-10-12' and metadata['version'] == '1.0', 'date/version')
    demand(metadata['license'] == 'cc-by-4.0' and manifest['license'] == 'CC-BY-4.0', 'same license')
    demand(metadata['publication_type'] == 'preprint' and metadata['access_right'] == 'open', 'status/access')
    missing_links = []
    for name in ('README.md', 'SUPPLEMENT.md', 'evidence/INDEX.md'):
        path = PUB / name
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if link.startswith(('http:', 'https:', '#')):
                continue
            if not (path.parent / link.split('#')[0]).is_file():
                missing_links.append((name, link))
    demand(not missing_links, 'all portable navigation files exist')
    query = json.loads((PUB / 'evidence/priority_review_01/QUERY_LEDGER.json').read_text())
    querycount = sum(len(b['queries']) for b in query['batches'])
    demand(querycount == query['query_count'] == 65, 'bounded65 count')
    source = json.loads((PUB / 'evidence/priority_review_01/SOURCE_INSPECTION_MANIFEST.json').read_text())
    demand(len(source['sources']) == source['source_count'] == 11, '11 source/version count')
    result = {'status': 'PASS', 'archive_entries': 127, 'inventory_files': 126,
              'archive_sha256': digest(archive.read_bytes()), 'deterministic_entire_bytes_match': True,
              'original_git_pins_checked': original_rows,
              'historical_manifest_entries_checked': len(oldmanifest['files']),
              'review01_unchanged_copies_checked': len(copy_receipt['files']),
              'all_11_guards_and_entire_AST_checked': True, 'exact_metadata_checked': True,
              'navigation_links_missing': missing_links, 'bounded_queries': querycount,
              'bounded_source_version_records': len(source['sources']),
              'earlier_verdicts_used_for_mathematical_acceptance': False}
    (HERE / 'receipts/INTEGRITY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'original_git_pins_checked'}, indent=2))


if __name__ == '__main__':
    main()
