"""Build the scoped PR778 source archive and exact two-file deposit. No publication is performed."""
from pathlib import Path, PurePosixPath
import argparse, datetime, io, json, hashlib, os, stat, tempfile, zipfile, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "audit" if (ROOT / "audit").is_dir() else ROOT.parent
TITLE = 'A missing multiplicity condition for double-permutation sequences'
PREFIX = "unsolved_math_prioritization/attempts/30001054/"
PIN = "21eb9d5f34f62f6cbabee80bd3d9c638becbb8417421c4849d3715489da9714d"
REVIEW_PINS = {'review_combinatorial_family': 'd41d7aba4a9cc9439f230a55722bb56fbc5c73d8106e1695ca23a0678033b8bd',
 'review_geometric_family': '0419ecf13bee99d10bea3adeeacc4de34ebeb9b2b675da62f1267417180c8afe',
 'priority_audit': '476645870d6613b35c6e5e3b677a38333e51d1c886c16bd1393e52011e019b83',
 'priority_adversary01': 'b8a089ae50e18847cc7aa5dea57729ee1f96578de4597c2c688619f82761a881'}
ROOT_AUDITS = ('ELIGIBILITY_GATE.json', 'SNAPSHOT.json', 'ROOT_INITIAL_POSITION.md', 'ROOT_SOURCE_IDENTITY.json', 'ROOT_PRIMARY_SOURCE_READINGS.json', 'ROOT_MATHEMATICAL_ASSESSMENT.md', 'MATH_GATE.json', 'ROOT_READONLY_REPRODUCTION.json', 'ROOT_PRIORITY_PROGRESS.json', 'ROOT_PRIORITY_ASSESSMENT.md', 'PRIORITY_GATE.json', 'root_reproduction/COMBINATORIAL_CLOSURE.json', 'root_reproduction/GEOMETRIC_CLOSURE.json', 'root_reproduction/PUBLICATION_REPLAY.json', 'root_reproduction/PRIORITY_CLOSURE.json', 'root_reproduction/PRIORITY_ADVERSARY_CLOSURE.json')
METADATA = {'title': 'A missing multiplicity condition for double-permutation sequences',
 'upload_type': 'publication',
 'publication_type': 'preprint',
 'publication_date': '2026-10-16',
 'version': '1.0',
 'language': 'eng',
 'creators': [{'name': 'Kriebel, Alec',
               'affiliation': 'Independent researcher',
               'orcid': '0009-0001-9320-500X'}],
 'description': '<p>The four term-sequence axioms printed in the inspected Goodman-Pollack '
                'manuscript and the official 2008 Oberwolfach problem session do not imply '
                'the proposed connected-set encoding with compatible tangent and separating '
                'pseudolines. The explicit two-body period A,B,A,B,C,B,C,B has least period '
                'eight, respects both endpoint orders, makes one adjacent different-body swap '
                'at each step, and satisfies reverse-toggle half-period symmetry. Every mixed '
                'primed/unprimed switch is absent, whereas the required internal tangents '
                'must produce mixed events. This is a negative answer to the literal '
                'universal realization assertion under those four axioms.</p><p>The note also '
                'proves that an explicitly required fully separated input term forces every '
                'ordered different-body switch exactly once per full period. It does not '
                'construct polygons or refute the normalized-input variant. Older stronger '
                'allowable-interval definitions are credited to Dhandapani, Goodman, Holmsen '
                'and Pollack and to Novick. Habert and Pocchiola already proved the properly '
                'constrained specified-fibration representation theorem; the example is '
                'outside that input class. No new solution of that stronger theorem is '
                'claimed. The source-bound correction concerns the inspected 26 November 2006 '
                'author manuscript and official OWR44/2008 passages. The final '
                'Goodman-Pollack journal body and an older cited 2004 version were not '
                'obtained. Bounded primary-source and citation searches identified no '
                'matching earlier literal-negative result, but firstness, exhaustive priority '
                'and present-day worldwide open status are not certified.</p><p>The companion '
                'source archive preserves all 32 frozen candidate files, distinct '
                'combinatorial and geometric mathematical audits, two independent priority '
                'reviews and exact finite checks. It reproduces the eight-term witness, two '
                'independent exhaustive two-body enumerations, separated-start controls, '
                'corrupted-input rejection and recursive artifact custody. Software does not '
                'formally certify the topological representation theorem, the general proof '
                'or literature completeness. AI tools were used extensively in development, '
                'source investigation, writing, reproduction, verification and adversarial '
                'review. This is an unrefereed preprint without external human peer review or '
                'proof-assistant certification. The note and authored companion material are '
                'CC BY 4.0; no third-party source PDF or full extracted body is '
                'redistributed.</p>',
 'access_right': 'open',
 'license': 'cc-by-4.0',
 'keywords': ['double-permutation sequences',
              'allowable interval sequences',
              'pseudoline arrangements',
              'tangents',
              'realization',
              'counterexample',
              'OWR-2090-003'],
 'related_identifiers': [{'identifier': 'https://math.nyu.edu/inmemoriam/pollack/pubs/dblperm11-26-06.pdf',
                          'relation': 'references',
                          'scheme': 'url'},
                         {'identifier': '10.4171/OWR/2008/44',
                          'relation': 'references',
                          'scheme': 'doi'},
                         {'identifier': 'https://math.nyu.edu/inmemoriam/pollack/pubs/interval.pdf',
                          'relation': 'references',
                          'scheme': 'url'},
                         {'identifier': '10.1007/s00454-012-9457-x',
                          'relation': 'references',
                          'scheme': 'doi'},
                         {'identifier': '10.1007/s00454-013-9532-y',
                          'relation': 'references',
                          'scheme': 'doi'},
                         {'identifier': 'https://github.com/AlecKriebel/Math/pull/778',
                          'relation': 'isDocumentedBy',
                          'scheme': 'url'},
                         {'identifier': 'https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_700_800_20261012/audits/pr778_30001054',
                          'relation': 'isSupplementedBy',
                          'scheme': 'url'}]}

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
    require(gate['result'] == 'PASS_FOR_HISTORICAL_FOUR_AXIOM_NEGATIVE_WITH_BOUNDED_PRIORITY'
            and gate['literal_four_axiom_negative_accepted']
            and not gate['historical_first_priority_certified']
            and not gate['current_worldwide_open_status_certified']
            and not gate['new_resolution_of_proper_fibration_problem']
            and not gate['final_GP_journal_body_inspected']
            and gate['known_full_literal_negative_predecessors'] == []
            and gate['remaining_mathematical_issues'] == []
            and gate['blocking_statement_or_credit_issues'] == [],
            'Wrong mathematical/priority publication scope')

def materials(pdf):
    priority_scope(json.loads(regular(AUDIT / 'PRIORITY_GATE.json')))
    require(all(len(value) == 64 for value in REVIEW_PINS.values()), 'Priority closure pending')
    files = {name: regular(ROOT / name) for name in
             ('paper.tex', 'build_package.py', 'verify_bundle.py', 'guard_controls.py')}
    require(b'\\textbf{Draft status.}' not in files['paper.tex'], 'Paper is still a draft')
    readme = ROOT / 'README-verification.md'
    files['README.md'] = regular(readme if readme.is_file() else ROOT / 'README.md')
    files['zenodo-metadata.json'] = json_bytes({'metadata': METADATA})
    files['PREPRINT_BINDINGS.json'] = json_bytes({
        'paper.tex': identity(files['paper.tex']), 'paper.pdf': identity(pdf),
        'scope_correction_sha256':'f0eeb8d06a27c296583e140e560807f8bfe38784f7fd110f68937f1e9cee2ff6',
        'witness_sha256':'585bddbe34e2a349b131c9a5384970504d585702ed21671cc58cffbb32b360d6',
        'scope':'Exact PDF byte binding; compilation, proof interpretation and priority remain distinct checks.'})
    snapshot = json.loads(regular(AUDIT / 'SNAPSHOT.json'))
    require(len(snapshot['files']) == 32, 'Wrong frozen original count')
    payload = inventory(AUDIT / 'original' / PREFIX)
    require(identity(payload['PUBLICATION_MANIFEST.json'])['sha256'] == PIN, 'Original publication pin changed')
    expected = set()
    for row in snapshot['files']:
        require(row['path'].startswith(PREFIX), 'Wrong source problem')
        name = safe_name(row['path'][len(PREFIX):])
        require(name not in expected, 'Repeated original path')
        expected.add(name)
        require(identity(payload[name]) == {k:row[k] for k in ('bytes','sha256')}, 'Frozen original changed: '+name)
        files['audit/original/' + PREFIX + name] = payload[name]
    require(set(payload) == expected, 'Original closure changed')
    for family,pin in REVIEW_PINS.items():
        payload = inventory(AUDIT / family)
        raw = payload['MANIFEST.json']
        require(identity(raw)['sha256'] == pin, 'Review manifest changed: '+family)
        names = set()
        for row in review_entries(json.loads(raw)):
            name = safe_name(row['path'])
            require(name not in names and name != 'MANIFEST.json', 'Duplicate/self review path')
            names.add(name)
            require(identity(payload[name]) == {k:row[k] for k in ('bytes','sha256')}, 'Review changed: '+family+'/'+name)
        require(set(payload) == names | {'MANIFEST.json'}, 'Review is not closed: '+family)
        for name,raw in payload.items():
            files['audit/' + family + '/' + name] = raw
    record = regular(AUDIT / 'private_sources/selected_record.json')
    require(identity(record)['sha256'] == '7a1d26575554344c3033d03813d55f3b249a09775c667fa38bc06be93d2b85d1', 'Selected source changed')
    selected = json.loads(record)
    require(hashlib.sha256(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode()).hexdigest()
            == '51710cccfe6bcd44ff5a8bd2b663db2387edbf19169806cfc0c1855f24822377', 'Canonical source hash changed')
    files['audit/private_sources/selected_record.json'] = record
    for name in ROOT_AUDITS:
        files['audit/' + name] = regular(AUDIT / name)
    files['MANIFEST.json'] = json_bytes({
        'schema':'sha256-exact-file-inventory-v1',
        'scope':'Closed source and exact finite replication; not formal proof verification or exhaustive priority.',
        'files':[{'path':name,**identity(raw)} for name,raw in sorted(files.items())]})
    return files

def archive(files):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(safe_name(name), date_time=(2026, 10, 16, 0, 0, 0))
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

if __name__ == "__main__":
    main()
