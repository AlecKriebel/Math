"""Build a closed source archive and two-file Zenodo deposit without changing inputs.

From the extracted ZIP, supply --output-dir OUTSIDE the input tree and --pdf
pointing to the published PDF. Recompilation is a separate check.
"""
from pathlib import Path, PurePosixPath
import argparse
import datetime
import io
import json
import hashlib
import os
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / 'audit' if (ROOT / 'audit').is_dir() else ROOT.parent
TITLE = 'Pure point Dirichlet spectrum on quasi-conical domains'
PREFIX = 'unsolved_math_prioritization/attempts/30005613/'
PIN = '83421d45b2e580c393507194f2b390b8b863fa5b11353d18f73b3170a83f678f'
REVIEW_PINS = {
    'review_spectral_family': '4ecbce1a7321c0f6ccb6f9103c9a0af9bbb9a8827cc41b3906f0348585cef0ad',
    'review_geometry_family': '32e10ca2dd15b4c733fd45c1c0d904ccdc157e6e93f6e31925dc984d0001a3a7',
    'review_spectral_family_addendum': 'e531e3ed21a27f593df4bf945d833eb0c124fe479e0d5a22d7f368f384f2f55c',
    'priority_audit': 'db4985fc0a260a7d0f212d8f8d12e96d00e898c5ce5fb402d5a43629dcc8921e',
    'priority_adversary01': 'c6c7f2f1ed4abcb3b2f80203cfb75b3fec3a64a7983f3f1882f1b4db1d581cd9',
}
ROOT_AUDITS = (
    'ELIGIBILITY_GATE.json', 'SNAPSHOT.json', 'ROOT_INITIAL_POSITION.md',
    'ROOT_MATH_AUDIT.md', 'ROOT_PRIMARY_SCOPE.json', 'ROOT_SOURCE_IDENTITY.json',
    'ROOT_SOURCE_RENDER_CORRECTION.json', 'MATH_GATE.json',
    'ROOT_PRIORITY_POSITION.md', 'ROOT_PRIORITY_QUERIES.json',
    'ROOT_PRIORITY_FOLLOWUP.json', 'ROOT_PRIMARY_BODY_FOLLOWUP.md',
    'ROOT_ZENODO_SEARCH.json', 'ROOT_ZENODO_FOLLOWUP.json',
    'ROOT_ZENODO_METADATA_SCREEN.json', 'PRIORITY_ELIGIBILITY_GATE.json',
    'PRIORITY_GATE.json', 'root_reproduction/RESULT.json',
    'root_reproduction/BUNDLED_PYTHON_REPLAY.json',
    'root_reproduction/GUARD_RESULTS.json',
    'root_reproduction/SPECTRAL_CLOSURE.json',
    'root_reproduction/GEOMETRY_CLOSURE.json',
    'root_reproduction/PRIORITY_CLOSURE.json',
    'root_reproduction/PRIORITY_ADVERSARY_CLOSURE.json',
)
METADATA = {
    'title': TITLE, 'upload_type': 'publication', 'publication_type': 'preprint',
    'publication_date': '2026-10-15', 'version': '1.0', 'language': 'eng',
    'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                  'orcid': '0009-0001-9320-500X'}],
    'description': (
        '<p>For every integer dimension at least two, this note constructs some '
        'connected open quasi-conical tower whose form-defined Dirichlet Laplacian '
        'has a complete orthonormal eigenbasis, spectrum and essential spectrum '
        'equal to the nonnegative half-line, dense positive eigenvalues, no zero '
        'eigenfunction, and no absolutely or singular continuous spectral subspace. '
        'Both expanding cube widths and positive shrinking windows are chosen '
        'inductively. The windows are openings in zero-thickness interface screens. '
        'No arbitrary preassigned-width, smooth-boundary, Neumann, positive-length '
        'passage or effective numerical aperture theorem is asserted.</p>'
        '<p>The result answers the precise existential spectral-type question in '
        'Krejcirik and Lotoreichik, Bulletin of the London Mathematical Society '
        '56 (2024), Sections 2.2, 3 and 5, and the corresponding Oberwolfach '
        'contribution (OWR-14297736-021). Their geometry, freedom of future cube '
        'sizes and finite-window convergence are substantive antecedents. Whole '
        'spectral families and multiplicity control are credited to Hempel, Seco '
        'and Simon (1991), Proposition 1.4, and the warning in KL Remark 3.1. '
        'The additional construction exhaustively transports complete finite '
        'spectral clusters with summable norm errors. Repeated dense probes prove '
        'basis completeness. No new abstract finite-rank diagonalization principle '
        'is claimed. Bounded primary-source, author/citation and direct Zenodo '
        'searches located no full matching predecessor; historical first priority '
        'and current worldwide openness are not certified. Some older full bodies, '
        'a restricted finite-dimensional gap-note body, and unindexed or nonpublic '
        'work remain outside the comparison.</p>'
        '<p>The companion source archive preserves all 39 frozen candidate files, '
        'distinct geometric and spectral audits, an explicitly superseding '
        'source-reading correction, priority searches and a fresh priority '
        'challenge. Offline checks reproduce integrity and finite diagnostics; '
        'they do not formally certify the PDE theorem or exhaustive priority. '
        'AI tools were used extensively in development, writing, reproduction, '
        'verification and adversarial review. This is an unrefereed preprint '
        'without external human peer review or proof-assistant certification. '
        'The note and authored companion material are CC BY 4.0.</p>'),
    'access_right': 'open', 'license': 'cc-by-4.0',
    'keywords': ['quasi-conical domains', 'Dirichlet Laplacian', 'pure point spectrum',
                 'complete eigenbasis', 'singular continuous spectrum',
                 'shrinking windows', 'spectral clusters', 'OWR-14297736-021'],
    'related_identifiers': [
        {'identifier': '10.1112/blms.13113', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://arxiv.org/abs/2205.08172v2',
         'relation': 'references', 'scheme': 'url'},
        {'identifier': '10.4171/OWR/2023/36', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://arxiv.org/abs/2609.28602v1',
         'relation': 'references', 'scheme': 'url'},
        {'identifier': '10.1016/0022-1236(91)90130-W',
         'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://github.com/AlecKriebel/Math/pull/765',
         'relation': 'isDocumentedBy', 'scheme': 'url'},
        {'identifier': 'https://github.com/AlecKriebel/Math/tree/main/'
         'draft_pr_claimed_solved_700_800_20261012/audits/pr765_30005613',
         'relation': 'isSupplementedBy', 'scheme': 'url'}],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def safe_name(name):
    require(isinstance(name, str) and name and not PurePosixPath(name).is_absolute()
            and '\\' not in name and all(p not in ('', '.', '..') for p in name.split('/'))
            and str(PurePosixPath(name)) == name, 'Unsafe path: ' + str(name))
    return name


def regular(path):
    require(not path.is_symlink() and path.is_file() and
            stat.S_ISREG(path.stat().st_mode), 'Nonregular source: ' + str(path))
    return path.read_bytes()


def inventory(root):
    result = {}
    dirs = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink in source: ' + str(p))
        name = safe_name(p.relative_to(root).as_posix())
        if p.is_dir():
            dirs.add(name)
        else:
            result[name] = regular(p)
    expected_dirs = {p.as_posix() for name in result for p in Path(name).parents
                     if p.as_posix() != '.'}
    require(dirs == expected_dirs, 'Unexpected empty directory: ' + str(root))
    return result


def review_entries(manifest):
    entries = manifest.get('authored_files', manifest.get('files'))
    if isinstance(entries, dict):
        entries = [{'path': path, **entry} for path, entry in entries.items()]
    require(isinstance(entries, list), 'Invalid review manifest')
    return entries


def priority_scope(gate):
    require(gate['result'] == 'PASS_FOR_CREDITED_COMPLETE_EXISTENTIAL_CONSTRUCTION'
            and not gate['historical_first_priority_certified']
            and not gate['current_worldwide_open_status_certified']
            and not gate['abstract_method_novelty_claim_allowed']
            and gate['known_equivalent_results'] == []
            and gate['remaining_mathematical_issues'] == []
            and gate['blocking_priority_or_credit_issues'] == [], 'Wrong priority scope')


def materials(pdf):
    priority_scope(json.loads(regular(AUDIT / 'PRIORITY_GATE.json')))
    files = {name: regular(ROOT / name) for name in
             ('paper.tex', 'build_package.py', 'verify_bundle.py', 'guard_controls.py')}
    readme = ROOT / 'README-verification.md'
    files['README.md'] = regular(readme if readme.is_file() else ROOT / 'README.md')
    files['zenodo-metadata.json'] = json_bytes({'metadata': METADATA})
    files['PREPRINT_BINDINGS.json'] = json_bytes({
        'paper.tex': identity(files['paper.tex']), 'paper.pdf': identity(pdf),
        'original_proof_sha256':
        '5d1bab0b62ac5f78c69b0d82babd0b79fa4944097470fa760fdb3c485e362a20',
        'scope': 'Exact external PDF byte binding; compilation is separately verified.'})
    snapshot = json.loads(regular(AUDIT / 'SNAPSHOT.json'))
    require(len(snapshot['files']) == 39, 'Wrong original inventory size')
    candidate = ROOT / 'historical_candidate'
    if not candidate.is_dir():
        candidate = AUDIT / 'original' / PREFIX
    payload = inventory(candidate)
    require(identity(payload['PUBLICATION_MANIFEST.json'])['sha256'] == PIN,
            'Original publication pin changed')
    expected = set()
    for row in snapshot['files']:
        require(row['path'].startswith(PREFIX), 'Wrong source problem')
        name = safe_name(row['path'][len(PREFIX):])
        require(name not in expected, 'Repeated original path')
        expected.add(name)
        require(identity(payload[name]) == {k: row[k] for k in ('bytes', 'sha256')},
                'Frozen original changed: ' + name)
        files['historical_candidate/' + name] = payload[name]
    require(set(payload) == expected, 'Original inventory changed')
    for family, pin in REVIEW_PINS.items():
        payload = inventory(AUDIT / family)
        raw = payload['MANIFEST.json']
        require(identity(raw)['sha256'] == pin, 'Review manifest changed: ' + family)
        names = set()
        for row in review_entries(json.loads(raw)):
            name = safe_name(row['path'])
            require(name not in names and name != 'MANIFEST.json', 'Duplicate/self review path')
            names.add(name)
            require(identity(payload[name]) == {k: row[k] for k in ('bytes', 'sha256')},
                    'Review changed: ' + family + '/' + name)
        require(set(payload) == names | {'MANIFEST.json'}, 'Review inventory not closed')
        for name, raw in payload.items():
            files['audit/' + family + '/' + name] = raw
    for name in ROOT_AUDITS:
        files['audit/' + name] = regular(AUDIT / name)
    files['MANIFEST.json'] = json_bytes({
        'schema': 'sha256-exact-file-inventory-v1',
        'scope': 'Closed source and dated finite diagnostics; not formal PDE or priority certification.',
        'files': [{'path': name, **identity(raw)} for name, raw in sorted(files.items())]})
    return files


def archive(files):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(safe_name(name), date_time=(2026, 10, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw, compresslevel=9)
    return out.getvalue()


def validate_outputs(output, names, closed_root=None, protected_pdf=None):
    """Read-only batch preflight, including aliases and the inventory receipt."""
    lexical = output.absolute()
    targets = [lexical / safe_name(name) for name in names]
    directories = {lexical}
    for target in targets:
        directories.update(target.parents)
    # Inspect lexical ancestors before resolving; resolution alone hides links.
    for directory in sorted(directories, key=lambda p: (len(p.parts), str(p))):
        require(not directory.is_symlink(), 'Output ancestor symlink: ' + str(directory))
        require(not directory.exists() or directory.is_dir(),
                'Output parent is not a directory: ' + str(directory))
    canonical = lexical.resolve()
    closed = closed_root.resolve() if closed_root else None
    protected_inodes = set()
    if closed:
        require(canonical != closed and closed not in canonical.parents,
                'Output root lies inside closed input')
        for path in closed.rglob('*'):
            if path.is_file():
                s = path.stat()
                protected_inodes.add((s.st_dev, s.st_ino))
    if protected_pdf:
        s = protected_pdf.stat()
        protected_inodes.add((s.st_dev, s.st_ino))
    for target in targets:
        require(not target.is_symlink(), 'Output destination symlink: ' + str(target))
        resolved = target.resolve()
        require(canonical in resolved.parents, 'Output escaped intended tree')
        if closed:
            require(resolved != closed and closed not in resolved.parents,
                    'Output target lies inside closed input')
        if target.exists():
            s = target.stat()
            require(stat.S_ISREG(s.st_mode), 'Output destination is not regular')
            require(s.st_nlink == 1, 'Output destination has multiple hardlinks')
            require((s.st_dev, s.st_ino) not in protected_inodes,
                    'Output aliases a protected input file')
    return canonical


def atomic_write(destination, raw):
    """Replace a pathname using a fresh inode; never truncate an existing one."""
    fd, temporary = tempfile.mkstemp(prefix='.preprint-build-', dir=destination.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
        os.chmod(temporary, 0o644)
        os.replace(temporary, destination)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path)
    ap.add_argument('--pdf', type=Path)
    args = ap.parse_args()
    output_arg = args.output_dir.absolute() if args.output_dir else ROOT
    out = output_arg.resolve()
    portable = (ROOT / 'MANIFEST.json').is_file()
    closed_before = None
    if portable:
        require(args.output_dir is not None and out != ROOT and ROOT not in out.parents,
                'Portable rebuild output must be outside closed input tree')
    pdf_path = args.pdf.resolve() if args.pdf else ROOT / 'output/pdf/paper.pdf'
    pdf = regular(pdf_path)
    require(pdf.startswith(b'%PDF-'), 'Missing PDF signature')
    if portable:
        payload = inventory(ROOT)
        closed_before = payload
        rows = json.loads(payload['MANIFEST.json'])['files']
        names = set()
        for row in rows:
            name = safe_name(row['path'])
            require(name not in names and name != 'MANIFEST.json', 'Duplicate/self input path')
            names.add(name)
            require(identity(payload[name]) == {k: row[k] for k in ('bytes', 'sha256')},
                    'Closed rebuild input changed: ' + name)
        require(set(payload) == names | {'MANIFEST.json'}, 'Closed rebuild inventory differs')
        require(identity(pdf) == json.loads(payload['PREPRINT_BINDINGS.json'])['paper.pdf'],
                'Rebuild PDF differs from original binding')
    files = materials(pdf)
    source = archive(files)
    deposit = {'metadata': METADATA, 'files': [
        {'path': 'output/pdf/paper.pdf', 'name': 'paper.pdf'},
        {'path': 'source-and-verification.zip', 'name': 'source-and-verification.zip'}]}
    flat = {'metadata': METADATA, 'files': [
        {'path': 'paper.pdf'}, {'path': 'source-and-verification.zip'}]}
    outputs = {
        'paper.tex': files['paper.tex'], 'output/pdf/paper.pdf': pdf,
        'source-and-verification.zip': source, 'zenodo-deposit.json': json_bytes(deposit),
        'zenodo-metadata.json': json_bytes({'metadata': METADATA}),
        'zenodo-upload-kit.zip': archive({
            'paper.pdf': pdf, 'source-and-verification.zip': source,
            'zenodo-deposit.json': json_bytes(flat),
            'zenodo-metadata.json': json_bytes({'metadata': METADATA}),
            'README.md': b'Upload only paper.pdf and source-and-verification.zip with the '
                         b'exact enclosed metadata. This outer ZIP is a convenience kit. '
                         b'See the source README for scope, credits, review limits and verification.\n'})}
    result = {
        'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'title': TITLE, 'version': '1.0', 'support_files': len(files),
        'files': [{'path': name, **identity(raw)} for name, raw in outputs.items()]}
    outputs['PACKAGE_INVENTORY.json'] = json_bytes(result)
    # Explicit PDF/output arguments are protected inputs in all modes. The
    # argument-free authoring mode retains its already compiled PDF in place.
    protect_pdf = pdf_path if portable or args.pdf or args.output_dir else None
    out = validate_outputs(output_arg, outputs,
                           ROOT if portable else None, protect_pdf)
    out.mkdir(parents=True, exist_ok=True)
    for name, raw in outputs.items():
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.is_file() or regular(dest) != raw:
            atomic_write(dest, raw)
    if portable:
        require(inventory(ROOT) == closed_before, 'Rebuild changed closed input')
    require(regular(pdf_path) == pdf, 'Rebuild changed supplied PDF input')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
