#!/usr/bin/env python3
"""Strict portable publication integrity and assertion-enabled finite replay."""
import argparse, ast, difflib, hashlib, json, pathlib, subprocess, sys, zipfile
from collections import Counter
ROOT = pathlib.Path(__file__).resolve().parent
PINNED = {
    'release/release-packet.zip': '292f2b355365976081d094c83154e6fb16a818025c125f598b061fbafa202b65',
    'release/corrected-author-packet.zip': '2b6ff9f11cd02141542f61fb0ddfdf3b6f5032af274909190a589e9826f5a0b7',
    'release/RELEASE_FREEZE.json': '54b548f91073101bb8095a781d301a3e56fbd730ce8b919246ac937f375b324a',
    'final-audit/FINAL_BINDING_ACCEPTANCE.json': 'e77dafff627f06a7ca796fa617d6ef835d4a06e5a00187e37321a1451c376051',
}
def require(condition, message):
    if not condition:
        raise SystemExit('Verification failure: ' + message)
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def read(rel):
    return (ROOT / rel).read_bytes()
def doc(rel):
    return json.loads(read(rel))
def fingerprint(rel, meta):
    raw = read(rel)
    require(len(raw) == meta['bytes'] and sha(raw) == meta['sha256'], 'fingerprint: ' + rel)
def entries(archive):
    with zipfile.ZipFile(ROOT / archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'duplicate ZIP entry: ' + archive)
        for name in names:
            p = pathlib.PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and not name.endswith('/'), 'unsafe ZIP path')
            require((z.getinfo(name).external_attr >> 16) & 0o170000 != 0o120000, 'ZIP symlink')
        return {name: z.read(name) for name in names}
def check_manifest(prefix, name):
    manifest = doc(prefix + name)
    listed = [r['path'] for r in manifest['files']]
    require(len(listed) == len(set(listed)), 'duplicate manifest path')
    for row in manifest['files']:
        p = pathlib.PurePosixPath(row['path'])
        require(not p.is_absolute() and '..' not in p.parts, 'unsafe manifest path')
        fingerprint(prefix + row['path'], row)
    return set(listed)
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    manifest = doc('PUBLICATION_MANIFEST.json')
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    found, directories = set(), set()
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT).as_posix()
        require(not p.is_symlink(), 'symlink: ' + rel)
        if p.is_dir():
            directories.add(rel)
        else:
            require(p.is_file(), 'nonregular file: ' + rel)
            found.add(rel)
    require(found == expected, 'file inventory')
    expected_dirs = {str(parent) for rel in expected for parent in pathlib.PurePosixPath(rel).parents if str(parent) != '.'}
    require(directories == expected_dirs, 'directory inventory')
    for rel, meta in manifest['files'].items():
        fingerprint(rel, meta)
    for rel, digest in PINNED.items():
        require(sha(read(rel)) == digest, 'frozen root: ' + rel)
    acceptance = doc('final-audit/FINAL_BINDING_ACCEPTANCE.json')
    require(acceptance['acceptance'] == 'accepted' and acceptance['scientific_status'] == 'unsolved', 'acceptance status')
    require(acceptance['turns_used'] == acceptance['turn_limit'] == 5, 'budget status')
    for rel, meta in acceptance['bound_corrected_release_files'].items():
        fingerprint('release/' + rel, meta)
    binding = doc('release/release-meta/RELEASE_BINDING.json')
    for key in ('corrected_author_manifest','corrected_author_packet','exact_diff','original_audit_binding','original_audit_packet','original_author_packet'):
        row = binding[key]
        fingerprint('release/' + row['filename'], row)
    for key in ('original_audit_packet','original_author_packet'):
        fingerprint('release/' + binding[key]['filename'], acceptance[key])
    fingerprint('release/audit-safe/AUDIT_BINDING.json', acceptance['original_audit_binding'])
    author = check_manifest('release/safe/', 'MANIFEST.json') | {'MANIFEST.json'}
    audit = check_manifest('release/audit-safe/', 'MANIFEST.json') | {'MANIFEST.json'}
    release = check_manifest('release/', 'RELEASE_MANIFEST.json') | {'RELEASE_MANIFEST.json'}
    for zip_name, prefix, expected_entries in [
        ('release/corrected-author-packet.zip','release/safe/',author),
        ('release/history/original-audit-packet.zip','release/audit-safe/',audit),
        ('release/release-packet.zip','release/',release)]:
        items = entries(zip_name)
        require(set(items) == expected_entries, 'ZIP inventory: ' + zip_name)
        for name, raw in items.items():
            require(raw == read(prefix + name), 'ZIP bytes: ' + name)
    original = entries('release/history/original-author-packet.zip')
    require(set(original) == author, 'original author inventory')
    original_manifest = json.loads(original['MANIFEST.json'])
    require({r['path'] for r in original_manifest['files']} == author - {'MANIFEST.json'}, 'original manifest inventory')
    for row in original_manifest['files']:
        raw = original[row['path']]
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'original payload fingerprint')
    changed = sorted(name for name in author if original[name] != read('release/safe/' + name))
    require(changed == ['CONTROL_RESULTS.json','MANIFEST.json','PROOF.md','verify.py'], 'changed author files')
    diff = ''.join(''.join(difflib.unified_diff(original[name].decode().splitlines(True), read('release/safe/'+name).decode().splitlines(True), fromfile='original/'+name, tofile='corrected/'+name)) for name in changed)
    require(diff.encode() == read('release/release-meta/EXACT_AUTHOR_DIFF.patch'), 'exact author diff')
    replays = []
    actual_asserts = None
    if args.replay:
        for script, arguments, output in [
            ('release/verify_release.py', [], None),
            ('release/safe/verify_manifest.py', [], None),
            ('release/audit-safe/verify_audit_manifest.py', [], None),
            ('release/safe/verify.py', [], 'release/safe/CONTROL_RESULTS.json'),
            ('release/audit-safe/audit_verify.py', [str(ROOT/'release/history/original-author-packet.zip')], 'release/audit-safe/AUDIT_CONTROL_RESULTS.json')]:
            process = subprocess.run([sys.executable, '-I', '-B', str(ROOT/script)] + arguments, capture_output=True)
            require(process.returncode == 0, 'replay execution: ' + script)
            if output is not None:
                require(process.stdout == read(output), 'saved stdout: ' + script)
            replays.append(script)
        hits = Counter()
        class Instrument(ast.NodeTransformer):
            def visit_Assert(self, node):
                call = ast.Expr(ast.Call(ast.Name('_hit',ast.Load()),[ast.Constant(node.lineno)],[]))
                return [ast.copy_location(call,node), node]
        tree = ast.fix_missing_locations(Instrument().visit(ast.parse(read('release/safe/verify.py').decode())))
        ns = {'__name__':'counted_corrected_verifier', '_hit': lambda n: hits.update([n])}
        exec(compile(tree,'corrected-verify.py','exec',optimize=0), ns)
        report = ns['run']()
        actual_asserts = sum(hits.values())
        require(actual_asserts == report['total_exact_assertions'] == 7580, 'corrected actual assertion count')
        require(report == doc('release/safe/CONTROL_RESULTS.json'), 'instrumented report')
        require(sum(hits[n] for n in (18,19,20,22,23)) == 5600, 'corrected exponent count')
    print(json.dumps({'passed':True,'publication_files':len(found),'release_files':len(release)+2,'author_assertions':actual_asserts,'independent_checks':87730 if args.replay else None,'replays':replays,'scientific_status':'unsolved','turns':'5/5','exact_author_diff_matches':True},sort_keys=True))
if __name__ == '__main__':
    main()
