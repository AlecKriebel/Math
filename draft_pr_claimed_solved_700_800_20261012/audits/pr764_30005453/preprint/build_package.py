"""Build scoped source/support material and matching Zenodo upload kit.

Portable rebuild: use --output-dir OUTSIDE the extracted source archive and
--pdf ORIGINAL_PDF. This leaves every closed input byte unchanged.
"""
from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / 'audit' if (ROOT / 'audit').is_dir() else ROOT.parent
TITLE = 'A vertex maximum principle for subcritical reinforcement'
PREFIX = 'unsolved_math_prioritization/attempts/30005453/'
PIN = '2603a5ef378dbc3e83a3a2862aa5517d63b0a0f0d90dcf7b2ffc4433b7c7b25f'
REVIEW_PINS = {
    'review_deterministic_family': '51f60e1946a252cb1191636469d790cf8bfcf9af6e4f01b8f5a64bb686153a8c',
    'review_stochastic_family': '83d5f8bd9af8ce445b31d3f079ddd262a88895c4d69e4c5fce1ad0321a4528ee',
    'priority_audit': 'c28066bda4655ad4688cf1e680e0ec63618e496028d42c7c810fcc22adfdf775',
    'priority_adversary01': 'a6426b805a4493d39a28a77e5df7390c8ab4879bfb5fe78b459dc195dbd3e064',
}
ROOT_AUDITS = (
    'SNAPSHOT.json', 'ROOT_MATH_AUDIT.md', 'MATH_GATE.json',
    'ROOT_SOURCE_IDENTITY.json', 'ROOT_PRIMARY_RETRIEVAL.json',
    'ROOT_REPRODUCTION_OWN_SCRATCH.json', 'ROOT_MUTATION_CONTROLS.json',
    'ROOT_REPLAY_SPACE_FAILURE.json', 'ROOT_REPRODUCTION.json',
    'ROOT_DETERMINISTIC_REVIEW_GATE.json', 'PRIORITY_GATE.json',
    'PRIORITY_ELIGIBILITY_GATE.json', 'ROOT_PRIORITY_REVIEW01_GATE.json',
    'ROOT_QIN_COMPARISON.json', 'ROOT_QIN_RETRIEVAL.json',
    'ROOT_DIRECT_REGISTRY_SEARCH.json', 'ROOT_DIRECT_REGISTRY_BROAD_SEARCH.json',
    'ROOT_INDEXED_PRIORITY_SEARCH.json', 'ROOT_PUBLIC_CHRONOLOGY_PRELIMINARY.json',
    'ROOT_UPDATED_CHAPTER_SCOPE.json',
)
METADATA = {
    'title': TITLE, 'upload_type': 'publication', 'publication_type': 'preprint',
    'publication_date': '2026-10-13', 'version': '1.0', 'language': 'eng',
    'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                  'orcid': '0009-0001-9320-500X'}],
    'description': (
        '<p>A self-contained alternative proof of unique strictly positive equilibrium '
        'and simultaneous almost-sure coordinatewise homogenization for subcritical '
        'graph-based reinforcement. The graph is countable, undirected and simple, '
        'with bounded degree; vertex firing rates are positive and bounded above, '
        'but their infimum may be zero. The exponent satisfies 0 &lt;= alpha &lt; 1. '
        'Initial edge counts are arbitrary finite deterministic positive integers. '
        'The proof uses finite-volume vertex minimization, an exact compensated jump '
        'transform, and a maximum principle for bounded positive complete vertex '
        'trajectories. Unrestricted nonnegative-equilibrium uniqueness is false; '
        'the positive statement is an explicitly corrected formulation.</p>'
        '<p>Shuo Qin, arXiv:2610.11780v1, Theorem 1.1 (submitted 8 October 2026), '
        'supplies the full positive theorem and broader real initialization. It is '
        'prominently credited, together with the matching example in Remark 1.3, '
        'the older finite-WARM matching mechanism, and the 2018/2021 partial results '
        'of Couzinie and Hirsch. The vertex proof here is different, while the '
        'power/incidence and complete-limit strategy are shared structural ideas. '
        'Angel-Hermon-Yao work reported by Qin was not available as a verified full '
        'manuscript with a public date. Repository PR764 has a server creation date '
        'of 5 October 2026, but this does not certify the first public availability '
        'of current proof bytes. No first, sole, new-theorem or currently-open claim '
        'is made. The final publisher MATRIX chapter body was not obtained; question '
        'wording was checked against the official hosted pre-publication version.</p>'
        '<p>The companion archive preserves all 63 frozen candidate files, distinct '
        'mathematical and priority reviews, bibliographic receipts, and reproducible '
        'integrity and finite diagnostic controls. Computation does not certify the '
        'infinite theorem or exhaustive priority. AI tools were used extensively in '
        'development, writing, reproduction, verification and adversarial review. '
        'This is an unrefereed preprint without external human peer review or formal '
        'proof-assistant certification. The note and companion materials are CC BY 4.0.</p>'),
    'access_right': 'open', 'license': 'cc-by-4.0',
    'keywords': ['subcritical reinforcement', 'Polya urns', 'countable graphs',
                 'positive equilibrium', 'homogenization', 'vertex maximum principle',
                 'martingale compensator', 'OWR-12697708-006'],
    'related_identifiers': [
        {'identifier': 'https://arxiv.org/abs/2610.11780v1', 'relation': 'references', 'scheme': 'url'},
        {'identifier': '10.1214/21-ECP404', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://arxiv.org/abs/2010.03347v2', 'relation': 'references', 'scheme': 'url'},
        {'identifier': 'https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf',
         'relation': 'references', 'scheme': 'url'},
        {'identifier': '10.4171/OWR/2023/12', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': '10.1007/978-3-031-76738-8_29', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://www.matrix-inst.org.au/wp_Matrix2016/wp-content/uploads/2023/Aletti.pdf',
         'relation': 'references', 'scheme': 'url'},
        {'identifier': 'https://arxiv.org/abs/1406.0449v1', 'relation': 'references', 'scheme': 'url'},
        {'identifier': 'https://github.com/AlecKriebel/Math/pull/764',
         'relation': 'isDocumentedBy', 'scheme': 'url'},
        {'identifier': 'https://github.com/AlecKriebel/Math/tree/main/'
         'draft_pr_claimed_solved_700_800_20261012/audits/pr764_30005453',
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
    require(isinstance(name, str) and not PurePosixPath(name).is_absolute() and
            '\\' not in name and all(p not in ('', '.', '..') for p in name.split('/')) and
            str(PurePosixPath(name)) == name, 'Unsafe path: ' + str(name))
    return name


def regular(path):
    require(not path.is_symlink() and path.is_file() and
            stat.S_ISREG(path.stat().st_mode), 'Nonregular source: ' + str(path))
    return path.read_bytes()


def review_entries(manifest):
    data = manifest['authored_files']
    if isinstance(data, dict):
        return [{'path': path, **entry} for path, entry in data.items()]
    require(isinstance(data, list), 'Invalid review entries')
    return data


def materials():
    gate = json.loads(regular(AUDIT / 'PRIORITY_GATE.json'))
    require(gate['result'] == 'PASS_FOR_CREDITED_ALTERNATIVE_PROOF_PREPARATION' and
            not gate['first_sole_new_theorem_claim_allowed'] and
            gate['known_equivalent_results'][0]['covers_candidate'], 'Wrong priority scope')
    files = {name: regular(ROOT / name) for name in
             ('paper.tex', 'build_package.py', 'verify_bundle.py')}
    readme = ROOT / 'README-verification.md'
    files['README.md'] = regular(readme if readme.is_file() else ROOT / 'README.md')
    files['zenodo-metadata.json'] = json_bytes({'metadata': METADATA})
    snapshot = json.loads(regular(AUDIT / 'SNAPSHOT.json'))
    require(len(snapshot['files']) == 63, 'Wrong original inventory size')
    candidate = ROOT / 'historical_candidate'
    if not candidate.is_dir():
        candidate = AUDIT / 'original' / PREFIX
    require(identity(regular(candidate / 'PUBLICATION_MANIFEST.json'))['sha256'] == PIN,
            'Original publication pin changed')
    expected = set()
    for entry in snapshot['files']:
        require(entry['path'].startswith(PREFIX), 'Wrong problem in snapshot')
        name = safe_name(entry['path'][len(PREFIX):])
        require(name not in expected, 'Repeated snapshot path')
        expected.add(name)
        raw = regular(candidate / name)
        require(identity(raw) == {k: entry[k] for k in ('bytes', 'sha256')},
                'Frozen original changed: ' + name)
        files['historical_candidate/' + name] = raw
    actual = {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}
    require(actual == expected, 'Original file inventory changed')
    for family, pin in REVIEW_PINS.items():
        source = AUDIT / family
        raw = regular(source / 'MANIFEST.json')
        require(identity(raw)['sha256'] == pin, 'Review manifest changed: ' + family)
        manifest = json.loads(raw)
        entries = review_entries(manifest)
        listed = set()
        for entry in entries:
            name = safe_name(entry['path'])
            require(name not in listed and name != 'MANIFEST.json', 'Duplicate/self review path')
            listed.add(name)
            value = regular(source / name)
            require(identity(value) == {k: entry[k] for k in ('bytes', 'sha256')},
                    'Review changed: ' + family + '/' + name)
            require(Path(name).suffix in ('.md', '.json', '.py') or name == '.gitignore',
                    'Unexpected review payload')
            files['audit/' + family + '/' + name] = value
        for path in source.rglob('*'):
            require(not path.is_symlink(), 'Review symlink')
        actual = {p.relative_to(source).as_posix() for p in source.rglob('*') if p.is_file()}
        require(actual == listed | {'MANIFEST.json'}, 'Review inventory not closed: ' + family)
        files['audit/' + family + '/MANIFEST.json'] = raw
    for name in ROOT_AUDITS:
        files['audit/' + name] = regular(AUDIT / name)
    manifest = {
        'schema': 'sha256-exact-file-inventory-v1',
        'scope': 'Closed authored source, dated reviews, provenance and finite diagnostics; '
                 'not formal infinite-theorem or historical-priority certification.',
        'files': [{'path': name, **identity(raw)} for name, raw in sorted(files.items())],
    }
    files['MANIFEST.json'] = json_bytes(manifest)
    return files


def archive(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(safe_name(name), date_time=(2026, 10, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path)
    ap.add_argument('--pdf', type=Path)
    args = ap.parse_args()
    out = args.output_dir.resolve() if args.output_dir else ROOT
    if (ROOT / 'MANIFEST.json').is_file():
        require(args.output_dir is not None and out != ROOT and ROOT not in out.parents,
                'Portable rebuild output must be outside closed input archive')
    files = materials()
    pdf = regular(args.pdf.resolve() if args.pdf else ROOT / 'output/pdf/paper.pdf')
    require(pdf.startswith(b'%PDF-'), 'Missing PDF signature')
    out.mkdir(parents=True, exist_ok=True)
    pdf_out = out / 'output/pdf/paper.pdf'
    pdf_out.parent.mkdir(parents=True, exist_ok=True)
    if not pdf_out.is_file() or pdf_out.read_bytes() != pdf:
        pdf_out.write_bytes(pdf)
    support = out / 'support'
    if support.exists():
        existing = {p.relative_to(support).as_posix() for p in support.rglob('*') if p.is_file()}
        require(existing <= set(files), 'Unexpected support file; refusing replacement')
        require(not any(p.is_symlink() for p in support.rglob('*')), 'Support symlink')
    support.mkdir(exist_ok=True)
    for name, raw in sorted(files.items()):
        dest = support / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
    archive(out / 'source-and-verification.zip', files)
    deposit = {'metadata': METADATA, 'files': [
        {'path': 'output/pdf/paper.pdf', 'name': 'paper.pdf'},
        {'path': 'source-and-verification.zip', 'name': 'source-and-verification.zip'}]}
    (out / 'zenodo-deposit.json').write_bytes(json_bytes(deposit))
    (out / 'zenodo-metadata.json').write_bytes(json_bytes({'metadata': METADATA}))
    flat = {'metadata': METADATA, 'files': [{'path': 'paper.pdf'},
                                         {'path': 'source-and-verification.zip'}]}
    archive(out / 'zenodo-upload-kit.zip', {
        'paper.pdf': pdf,
        'source-and-verification.zip': (out / 'source-and-verification.zip').read_bytes(),
        'zenodo-deposit.json': json_bytes(flat),
        'zenodo-metadata.json': json_bytes({'metadata': METADATA}),
        'README.md': b'Upload paper.pdf and source-and-verification.zip separately '
                     b'with the exact enclosed metadata. The outer ZIP is a convenience '
                     b'kit, not an extra deposit file. See the source archive README '
                     b'for scope, credits, disclosure and verification instructions.\n'})
    names = ['paper.tex', 'output/pdf/paper.pdf', 'source-and-verification.zip',
             'zenodo-deposit.json', 'zenodo-metadata.json', 'zenodo-upload-kit.zip']
    if out != ROOT:
        (out / 'paper.tex').write_bytes(files['paper.tex'])
    inventory = {
        'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'title': TITLE, 'version': '1.0', 'support_files': len(files),
        'files': [{'path': name, **identity(regular(out / name))} for name in names]}
    (out / 'PACKAGE_INVENTORY.json').write_bytes(json_bytes(inventory))
    print(json.dumps({'support_files': len(files), 'outputs': names}, indent=2))


if __name__ == '__main__':
    main()
