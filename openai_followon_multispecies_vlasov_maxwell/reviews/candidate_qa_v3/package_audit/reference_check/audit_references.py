#!/usr/bin/env python3
"""Read-only package-v3 reference audit. Writes only beside this audit script.

No candidate programs, package builder, network, or Git commands are executed.
Reference classification is packaging/provenance classification, not proof QA.
"""
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PACKET = ROOT / 'reviews/package_v3'
SOURCE = PACKET / 'source-and-verification'
START = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def snapshot():
    return {str(p.relative_to(PACKET)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
            for p in sorted(PACKET.rglob('*')) if p.is_file()}

before = snapshot()
archive = json.loads((SOURCE / 'ARCHIVE_MAP.json').read_text())
mapping = archive['original_project_paths']
pin = json.loads((SOURCE / 'PINNED_SOURCE.json').read_text())
builder = ROOT / 'checks/build_publication_package.py'
builder_snapshot = OUT / 'initial_builder_snapshot.py'
if not builder_snapshot.exists():
    builder_snapshot.write_bytes(builder.read_bytes())
builder_tree = ast.parse(builder_snapshot.read_text())
builder_mapping = next(ast.literal_eval(n.value) for n in builder_tree.body
                       if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'files' for t in n.targets))

NOTE = '> Archive provenance note: original project paths below identify historical evidence. The provided formal inventory, scan and failed-build receipt use FORMAL_ filenames. The project-local reproduction script and Lean checkout are intentionally excluded; obtain the pinned upstream sources and follow their documented build instructions. No formal build succeeded. See ARCHIVE_MAP.json.\n\n'

def expected_copy(name, data):
    if not name.endswith('.md'):
        return data
    s = data.decode()
    for old, new in {'PAIR_IDENTITY.md': 'SUPPLEMENT_PAIR_IDENTITY.md',
                     'LOCAL_THEORY.md': 'SUPPLEMENT_LOCAL_THEORY.md',
                     'UNIFORM_LEMMA_CHAIN.md': 'SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md'}.items():
        if name != new:
            s = s.replace('`' + old + '`', '`' + new + '`')
    if name == 'SUPPLEMENT_UNIFORM_LEMMA_CHAIN.md':
        s = s.replace('`AUDIT.md`', '`SUPPLEMENT_OCCUPATION_AUDIT.md`')
    if name == 'FORMAL_SCOPE_AUDIT.md':
        s = NOTE + s
        for old, new in {'checks/formal_scope/source_inventory.json': 'FORMAL_SOURCE_INVENTORY.json',
                         'static_scan.json': 'FORMAL_STATIC_SCAN.json',
                         'build_receipt.json': 'FORMAL_BUILD_LIMITATIONS.json'}.items():
            s = s.replace('`' + old + '`', '`' + new + '`')
    return s.encode()

correspondences = []
for name, original in mapping.items():
    p, q = SOURCE / name, ROOT / original
    raw, supplied = q.read_bytes(), p.read_bytes()
    correspondences.append({'archive_file': name, 'original_project_path': original,
                            'original_sha256': sha(raw), 'archive_sha256': sha(supplied),
                            'byte_identical': raw == supplied,
                            'documented_normalization_matches': expected_copy(name, raw) == supplied})

# Preserve the initial binding. Later root input/builder drift is an advisory
# distinct from a frozen package-byte mutation. This file is never overwritten.
initial_path = OUT / 'INITIAL_INPUT_STATE.json'
if not initial_path.exists():
    initial_path.write_text(json.dumps({'captured_utc': START,
        'builder_snapshot_sha256': sha(builder_snapshot.read_bytes()),
        'candidate_packet_hashes': before,
        'mapped_original_inputs': correspondences}, indent=2) + '\n')
initial = json.loads(initial_path.read_text())
initial_correspondences = {r['archive_file']: r for r in initial['mapped_original_inputs']}
original_drift = [{'archive_file': r['archive_file'], 'original_project_path': r['original_project_path'],
                   'initial_sha256': initial_correspondences[r['archive_file']]['original_sha256'],
                   'current_sha256': r['original_sha256']}
                  for r in correspondences if r['original_sha256'] != initial_correspondences[r['archive_file']]['original_sha256']]
builder_drift = sha(builder.read_bytes()) != initial['builder_snapshot_sha256']

zip_path = PACKET / 'upload-kit/source-and-verification.zip'
with zipfile.ZipFile(zip_path) as z:
    zip_names = z.namelist()
    expected_names = ['source-and-verification/' + p.name for p in sorted(SOURCE.iterdir()) if p.is_file()]
    zip_equal = set(zip_names) == set(expected_names) and len(zip_names) == len(set(zip_names))
    zip_byte_mismatches = [name for name in expected_names if name not in zip_names or z.read(name) != (PACKET / name).read_bytes()]
    zip_unsafe = [name for name in zip_names if name.startswith('/') or '..' in Path(name).parts]

inverse = {v: k for k, v in mapping.items()}
pin_paths = set(pin['sha256'])
upstream_tex = {Path(p).name: p for p in pin_paths if '/build/sections/' in p and p.endswith('.tex')}
upstream_lean = {p.removeprefix('lean/'): p for p in pin_paths if p.startswith('lean/')}
priority_logs = {'retrieval_log.json', 'retrieval_log_extra.json', 'preprints_tree_retrieval.json',
                 'primary_pdf_response_hashes.json', 'cached_primary_hash_check.json',
                 'candidate_reviewed_hashes.json', 'upstream_reviewed_hashes.json'}
formal_local = {'lakefile.upstream.lean', 'lake-manifest.upstream.json', 'model_initial_check.log',
                'model_direct_check.log', 'Audit.lean', 'checks/formal_scope/reproduce.sh',
                'checks/formal_scope/lean', '/Users/alec/Desktop/math'}

def classify(token, doc):
    # Historical final-priority audit denotes v1 files/hashes. Its leading scope
    # statement is explicit; it must never be read as a v3 identity receipt.
    if token in priority_logs or token.startswith('sources/priority_final/') and Path(token).name in priority_logs:
        return 'omitted_project_priority_receipt', None, 'Historical project evidence; no supplied counterpart and no project repository URL in packet.'
    if token == 'SEARCH_LOG.json' and doc.name == 'PRIORITY_AUDIT.md':
        return 'mapped_contextual', 'PRIORITY_SEARCH_LOG.json', 'Paragraph identifies sources/priority_final; ARCHIVE_MAP provides its SEARCH_LOG counterpart.'
    if token in formal_local or token.startswith('/Users/'):
        return 'omitted_formal_or_historical_local', None, 'Leading archive note excludes local reproduction script and Lean checkout; this historical pathname is not portable.'
    if token in inverse:
        return 'mapped_exact', inverse[token], 'Exact original project path in ARCHIVE_MAP.'
    if token in mapping or (SOURCE / token).is_file():
        return 'supplied_direct', token, 'File exists in source archive.'
    if token in {'paper.pdf', 'source-and-verification.zip'}:
        return 'supplied_upload_kit', 'upload-kit/' + token, 'README describes enclosing upload kit; these files are outside the ZIP.'
    if (PACKET / token).is_file():
        return 'supplied_packet', token, 'File exists at review packet root-relative pathname.'
    if token in upstream_tex:
        return 'omitted_upstream_pinned', upstream_tex[token], 'Source section is identified/hash-pinned in PINNED_SOURCE and deliberately fetched separately.'
    if token == 'build/sections/continuation.tex':
        return 'omitted_upstream_pinned', upstream_tex['continuation.tex'], 'Pinned family manuscript section; not a supplied supplement.'
    if token in {'build/sections', 'lean/docs/362.md', '362.md', 'AGENTS.md'}:
        return 'omitted_upstream_historical', 'lean/docs/362.md' if token == '362.md' else token, 'Report explicitly describes upstream material actually read; not promised in archive.'
    if token in upstream_lean:
        return 'omitted_upstream_pinned', upstream_lean[token], 'PINNED_SOURCE provides the external Lean path/hash.'
    if token.endswith('.lean'):
        norm = token.replace('OAI.Analysis.', 'OAI/Analysis/').replace('VlasovMaxwell.Main.lean', 'VlasovMaxwell/Main.lean')
        candidates = [p for p in upstream_lean if p == norm or p.endswith('/' + norm)]
        if len(candidates) == 1:
            return 'omitted_upstream_pinned', upstream_lean[candidates[0]], 'Formal shorthand resolves uniquely in pinned source manifest.'
    if token.startswith('preprints/'):
        return 'omitted_upstream_pinned', token, 'Upstream family directory at the stated exact pin.'
    if token == 'reviews/package_v1':
        return 'historical_candidate_scope', token, 'The included priority report states it audited v1, not v3.'
    return 'needs_manual_review', None, 'No direct or mapped supplied target automatically identified.'

filename_re = re.compile(r'(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_./-]*\.(?:md|json|py|tex|lean|pdf|bib|txt|zip|sh|log))(?![A-Za-z0-9_])')
url_re = re.compile(r'https?://[^\s<>]+')
refs, urls = [], []
docs = sorted(SOURCE.glob('*.md')) + [SOURCE / 'main.tex', PACKET / 'upload-kit/README.md']
for doc in docs:
    for line_no, line in enumerate(doc.read_text().splitlines(), 1):
        for url in url_re.findall(line):
            urls.append({'document': str(doc.relative_to(PACKET)), 'line': line_no, 'url': url.rstrip(').,]')})
        local_line = url_re.sub('', line)
        tokens = filename_re.findall(local_line)
        for inline in re.findall(r'`([^`\n]+)`', local_line):
            if inline in {'build/sections', 'checks/formal_scope/lean', '/Users/alec/Desktop/math', 'reviews/package_v1'} or inline.startswith('preprints/'):
                tokens.append(inline)
        for token in sorted(set(tokens)):
            status, target, reason = classify(token, doc)
            refs.append({'document': str(doc.relative_to(PACKET)), 'line': line_no, 'reference': token,
                         'classification': status, 'target': target, 'reason': reason})

main = (SOURCE / 'main.tex').read_text()
dependency_commands = re.findall(r'\\(?:input|include|includegraphics|bibliography|addbibresource)\s*(?:\[[^\]]*\])?\{([^}]+)\}', main)
labels = re.findall(r'\\label\{([^}]+)\}', main)
label_refs = re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}', main)
missing_labels = sorted(set(label_refs) - set(labels))
duplicate_labels = [x for x, n in collections.Counter(labels).items() if n > 1]

formal_inv = json.loads((SOURCE / 'FORMAL_SOURCE_INVENTORY.json').read_text())
formal_modules = [r for r in formal_inv['copied_file_inventory'] if r['path'].startswith('OAI/')]
formal_pin_mismatches = [r['path'] for r in formal_modules if pin['sha256'].get('lean/' + r['path']) != r['sha256']]
attribution = json.loads((SOURCE / 'ORIGINAL_CONTINUATION_ATTRIBUTION.json').read_text())
attribution_scope = attribution.get('scope_actually_inspected', '')
attribution_check = (attribution.get('doi') == '10.1007/BF00250732'
    and attribution.get('authors') == ['Robert T. Glassey', 'Walter A. Strauss']
    and attribution.get('year') == 1986 and attribution.get('volume') == 92
    and attribution.get('pages') == '59–90'
    and attribution.get('primary_url') == 'https://link.springer.com/article/10.1007/BF00250732'
    and 'publisher bibliographic record and abstract' in attribution_scope
    and 'original full theorem/proof not revalidated here' in attribution_scope
    and 'without adding a new analytic dependency' in attribution_scope
    and '\\cite{GlasseyStrauss1986}' in main
    and '10.1007/BF00250732' in main
    and 'in the precise formulation of\nLuk--Strain' in main)
after = snapshot()
generated_exceptions = sorted({p.name for p in SOURCE.iterdir()} - set(mapping))
manual = [r for r in refs if r['classification'] == 'needs_manual_review']
checks = {
    'archive_map_matches_read_only_builder_allowlist': mapping == builder_mapping,
    'all_25_initial_source_correspondences_match_documented_transform': len(mapping) == 25 and all(r['documented_normalization_matches'] for r in initial['mapped_original_inputs']),
    'map_targets_are_unique': len(mapping.values()) == len(set(mapping.values())),
    'mapped_files_and_explicit_omitted_input_prefixes_do_not_overlap': not any(v.startswith(k.rstrip('/')) for v in mapping.values() for k in archive['omitted_inputs'] if k.endswith('/')),
    'only_generated_map_and_digest_manifest_lack_original_paths': generated_exceptions == ['ARCHIVE_MAP.json', 'SHA256SUMS.json'],
    'zip_names_are_exact_portable_source_inventory': zip_equal and not zip_unsafe,
    'source27_zip27_packet32_expected_counts': len(expected_names) == 27 and len(zip_names) == 27 and len(before) == 32,
    'zip_bytes_match_supplied_source_tree': not zip_byte_mismatches,
    'frozen_v3_expected_pdf_zip_sha256_match': sha((PACKET / 'upload-kit/paper.pdf').read_bytes()) == '20581b8b253c470d9fd775f88931002fc99729b7d7db21da5e6274482c5b990a' and sha(zip_path.read_bytes()) == 'b14fa882d987ef6b168b9b821c86b1685f4e6abcd7540837e9f3afa9c0cff527',
    'all_markdown_tex_file_tokens_classified': not manual,
    'main_tex_has_no_local_file_dependency_commands': not dependency_commands,
    'main_tex_internal_labels_resolve_without_duplicates': not missing_labels and not duplicate_labels,
    'formal_207_module_paths_and_hashes_match_pinned_manifest': len(formal_modules) == 207 and not formal_pin_mismatches,
    'original_1986_attribution_explicitly_limits_inspection_to_publisher_record_abstract': attribution_check,
    'candidate_packet_matches_preserved_initial_hash_binding': before == initial['candidate_packet_hashes'],
    'candidate_packet_hashes_unchanged_during_audit': before == after,
}
findings = [
    {'id': 'R-A1', 'severity': 'advisory', 'locations': ['FORMAL_SCOPE_AUDIT.md:1', 'FORMAL_SCOPE_AUDIT.md:69', 'FORMAL_SCOPE_AUDIT.md:73', 'FORMAL_SCOPE_AUDIT.md:79'],
     'issue': 'Historical formal report says local configurations/logs are retained and reproduce.sh is supplied. These files are absent from ZIP; the leading archive note explicitly excludes the reproduction script and Lean checkout, so this is qualified historical wording rather than a current supplied-file promise.',
     'exact_omitted_references': sorted(formal_local - {'/Users/alec/Desktop/math'}),
     'recommendation': 'Optionally add these local artifacts to omitted_inputs and label the historical Reproduction paragraph as project-only. Fetching upstream does not recreate the altered minimal configuration or Audit.lean byte-for-byte.'},
    {'id': 'R-A2', 'severity': 'advisory', 'locations': ['PRIORITY_AUDIT.md:17', 'PRIORITY_AUDIT.md:117', 'README.md:17', 'ARCHIVE_MAP.json:28'],
     'issue': 'Seven project-owned priority retrieval/hash receipts are cited but neither supplied nor individually listed as omitted. README locates review receipts in the public project repository, but gives no project repository URL. Supplied PRIORITY_SEARCH_LOG.json does resolve the historical SEARCH_LOG.json context.',
     'exact_omitted_references': ['sources/priority_final/' + p for p in sorted(priority_logs)],
     'recommendation': 'Optionally record these seven omitted project receipts and provide a stable project repository URL; preserve the report\'s explicit v1 scope rather than presenting its v1 hashes as v3 identities.'},
    {'id': 'R-A3', 'severity': 'advisory', 'locations': ['ARCHIVE_MAP.json:31', 'PRELIMINARY_PRIORITY_AUDIT.md:78', 'PRIORITY_AUDIT.md:51', 'PRIMARY_REFERENCE_PROVENANCE.md:5'],
     'issue': 'omitted_inputs says PDF source URLs/hashes are in priority/provenance records. The supplied provenance table contains hashes for Glassey 1996, Bouchut-Golse-Pallard, and Luk-Strain; no exact Glassey-Schaeffer 1988 PDF digest or preliminary GitHub API response digest is in the supplied records, although historical reports describe hash checks/source-manifest hashes.',
     'recommendation': 'Optionally narrow the hash-availability wording or include the permitted project-owned digest/retrieval records; the third-party PDFs themselves remain intentionally omitted.'},
]
if original_drift or builder_drift:
    findings.append({'id': 'R-A4', 'severity': 'advisory', 'locations': ['Current project builder/mapped original inputs'],
        'issue': 'Project originals or builder changed after the initial audit snapshot. Frozen archive integrity is evaluated against initial bindings and expected v3 PDF/ZIP hashes, separately from this root drift.',
        'original_input_drift': original_drift, 'builder_drift': builder_drift,
        'recommendation': 'Keep future root edits separate from immutable package-v3 and this initial snapshot.'})
result = {
    'scope': 'Read-only package-v3 archive/reference portability; no mathematics, priority, source build, external URL availability, or publication approval.',
    'started_utc': START,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'completion_estimate_percent': 100,
    'verdict': 'PASS_WITH_ADVISORIES' if all(checks.values()) else 'REVIEW_REQUIRED',
    'blockers': [] if all(checks.values()) else [k for k,v in checks.items() if not v],
    'checks': checks,
    'check_count': len(checks), 'passed_checks': sum(checks.values()),
    'findings': findings,
    'archive_map': {'mapped_source_files': len(mapping), 'generated_without_original_path': generated_exceptions,
                    'omitted_inputs_as_supplied': archive['omitted_inputs'], 'correspondences': correspondences},
    'reference_occurrences': refs,
    'reference_classification_counts': dict(collections.Counter(r['classification'] for r in refs)),
    'external_url_occurrences_recorded_without_fetch': urls,
    'formal_upstream_inventory': {'module_count': len(formal_modules), 'pin_mismatches': formal_pin_mismatches},
    'standalone_tex': {'local_dependency_commands': dependency_commands, 'missing_labels': missing_labels, 'duplicate_labels': duplicate_labels},
    'zip': {'sha256': sha(zip_path.read_bytes()), 'file_count': len(zip_names), 'names': zip_names, 'byte_mismatches': zip_byte_mismatches, 'unsafe_names': zip_unsafe},
    'builder_read_only_sha256': sha(builder.read_bytes()),
    'initial_builder_snapshot_sha256': initial['builder_snapshot_sha256'],
    'initial_mapped_original_input_hashes': initial['mapped_original_inputs'],
    'current_root_drift': {'original_inputs': original_drift, 'builder_changed': builder_drift},
    'original_continuation_attribution': attribution,
    'candidate_packet_hashes': before,
    'unclassified_references': manual,
    'candidate_unchanged': before == after,
}
(OUT / 'reference_receipt.json').write_text(json.dumps(result, indent=2) + '\n')
lines = [
    '# Package v3 reference portability receipt', '',
    f'Finished: {result["finished_utc"]}. Completion estimate: 100% of this packaging-reference audit.', '',
    f'**{result["verdict"]}: {result["passed_checks"]}/{len(checks)} checks passed; no broken current supplied-file promises identified.**', '',
    'The audit read the immutable package tree/ZIP, every supplied Markdown document and standalone TeX file, the map, source/provenance/priority receipts, and the current builder without executing it. Candidate bytes remained unchanged. No Git, network, publication, or external communication occurred.', '',
    f'All {len(mapping)} original-project mappings identify existing supplied files and match the initial original bytes after the builder\'s documented Markdown normalization. ARCHIVE_MAP.json and SHA256SUMS.json are generated archive metadata, with no original project counterpart. ZIP contains the same 27 flat files with identical bytes; packet contains 32 files including REVIEW_INVENTORY.json. All 207 formal module hashes correspond to the pinned external manifest; those external modules are intentionally absent.', '',
    f'{len(refs)} Markdown/TeX file-reference occurrences were classified; all current supplied references resolve directly, by precise map entry, or by enclosing upload-kit scope. Upstream manuscript/Lean references denote excluded pinned inputs. main.tex has no local input/include/graphics/bibliography dependency and its internal labels resolve.', '',
    'The new ORIGINAL_CONTINUATION_ATTRIBUTION.json maps exactly to its project receipt and limits inspected scope to the 1986 publisher bibliographic record and abstract. It expressly says the original full theorem/proof was not revalidated and adds no analytic dependency; the manuscript credits the original while identifying Luk–Strain\'s precise relied-on formulation. No publisher endpoint or original proof was independently checked by this packaging audit.', '',
    f'Initial builder SHA256: {initial["builder_snapshot_sha256"]}. Initial mapped-original hashes and packet hashes are preserved in INITIAL_INPUT_STATE.json. Later root drift is classified separately: {len(original_drift)} mapped inputs changed; builder changed={builder_drift}. Expected v3 PDF/ZIP hashes were checked.', '',
    '## Exact remaining concerns (advisories)', '',
]
for f in findings:
    lines += [f'**{f["id"]}** ({", ".join(f["locations"])}): {f["issue"]}', '', f'Recommendation: {f["recommendation"]}', '']
lines += ['The historical priority audit expressly covers package v1 and retains its v1 hashes; this audit does not promote it to approval of v3. External URLs were recorded but not fetched. The receipt establishes packaging reference integrity, not mathematical correctness, novelty/priority, formal certification, or readiness to publish.', '',
          'The JSON receipt contains exact per-reference classifications, all mapping comparisons and candidate SHA256 hashes. The accompanying script is rerunnable and writes only in this reference_check folder.', '']
(OUT / 'reference_receipt.md').write_text('\n'.join(lines))
artifact_hashes = {p.name: sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'REFERENCE_ARTIFACT_SHA256.json'}
(OUT / 'REFERENCE_ARTIFACT_SHA256.json').write_text(json.dumps(artifact_hashes, indent=2) + '\n')
print(json.dumps({'verdict': result['verdict'], 'checks': checks, 'reference_counts': result['reference_classification_counts'], 'unclassified': manual, 'changed_candidate_files': [k for k in before if before[k] != after[k]]}, indent=2))
