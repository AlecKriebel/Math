"""Editorial/custody checks only; never runs deposited mathematics or mutates sources."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
SOURCES = BASE / 'sources'
PACKAGE = SOURCES / 'published-source/dfc_stability_verification/dfc_stability_verification'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

receipt = json.loads((SOURCES / 'receipt.json').read_text())
integrity = json.loads((SOURCES / 'extraction-integrity.json').read_text())
record = json.loads((SOURCES / 'record.json').read_text())
public = receipt['files']
by_name = {f['name']: f for f in public}
assert len(public) == len(by_name) == 2
assert record['metadata']['version'] == '1.0'
assert record['metadata']['publication_date'] == '2026-10-20'
for f in public:
    path = SOURCES / f['name']
    assert path.stat().st_size == f['bytes'] and sha(path) == f['sha256']
    assert hashlib.md5(path.read_bytes()).hexdigest() == f['md5']
assert sha(SOURCES / 'record.json') == receipt['record_sha256']
for f in integrity['members']:
    path = SOURCES / f['path']
    assert path.stat().st_size == f['bytes'] and sha(path) == f['sha256']
assert len(integrity['members']) == 92
assert sha(PACKAGE / 'paper.pdf') == by_name['dfc_stability.pdf']['sha256']
manifest = json.loads((PACKAGE / 'MANIFEST.json').read_text())
manifest_paths = [r['path'] for r in manifest['files']]
assert len(manifest_paths) == len(set(manifest_paths))
assert set(manifest_paths) | {'MANIFEST.json'} == {
    p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()
}
for f in manifest['files']:
    path = PACKAGE / f['path']
    assert path.stat().st_size == f['bytes'] and sha(path) == f['sha256']
with zipfile.ZipFile(SOURCES / 'dfc_stability_verification.zip') as z:
    assert z.testzip() is None
    for f in integrity['members']:
        assert hashlib.sha256(z.read(f['member'])).hexdigest() == f['sha256']
save('custody-final.json', {
    'utc': NOW, 'status': 'PASS_INTEGRITY_ONLY', 'public_assets_checked': 2,
    'extracted_regular_files_checked': 92, 'manifest_entries_checked': len(manifest_paths),
    'archive_crc_and_member_bytes_rechecked': True, 'source_files_mutated': False,
    'reader_pdf_pages': 6, 'duplicate_reader_byte_identity': True,
    'mathematical_programs_executed': False,
})

source = (PACKAGE / 'main.tex').read_text()
abstract_tex = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1).strip()
(HERE / 'abstract.tex.txt').write_text(abstract_tex + '\n')
abstract = re.sub(r'\s+', ' ', abstract_tex.replace('--', '–')).strip()
binding = {
    'record_id': '23524971', 'pdf_sha256': by_name['dfc_stability.pdf']['sha256'],
    'receipt': 'sources/receipt.json', 'receipt_sha256': sha(SOURCES / 'receipt.json'),
    'metadata_sha256': sha(SOURCES / 'record.json'),
    'all_public_assets': [{'filename': r['name'], 'sha256': r['sha256'], 'bytes': r['bytes']} for r in public],
    'embedded_assets': [],
}
content = {
    'title': 'All-load stability of a deterministic-first-chunk file-sharing chain',
    'slug': 'deterministic-first-chunk-stability',
    'description': 'Positive recurrence at every fixed positive arrival rate for the exact two-chunk file-sharing model of Norros, Reittu and Eirola.',
    'abstract': abstract,
    'plain_language': [
        'Imagine a file split into two pieces. Each new participant chooses at random which piece to fetch first, keeps that choice, and leaves as soon as both pieces are obtained. One permanent seed always has both pieces. The paper studies a precise mathematical version of this process.',
        'The result is that this particular random system is stable at every fixed positive arrival rate. Here stability means that it repeatedly returns in finite expected time and has a unique stationary probability distribution. It does not mean that the population never becomes large or that the average population has been bounded.',
        'The question is interesting because the associated large-system differential equations have trajectories that grow without bound. For this model, that deterministic behavior does not force instability of the original random chain. The paper extends the easy small-arrival-rate argument to every positive load.',
    ],
    'result': [
        'For every fixed real λ>0 and every finite initial state (a,b,x,y)∈N₀⁴, Theorem 1 asserts that the six-rate continuous-time chain is nonexplosive, irreducible and positive recurrent. It therefore has a unique stationary probability distribution.',
        'The rates are λ/2 for each of the two arrival types, a(x+1)/D and b(y+1)/D for first downloads, and x(y+1)/D and y(x+1)/D for departures, where D=x+y+1. The empty waiting-room populations a and b do not enter this denominator. These exact rates and the permanent seed are part of the result.',
    ],
    'why_it_works': [
        'The proof combines the amount of unfinished downloading with a smoothed measure of imbalance between the two participant groups. Two bounded corrections handle states in which one piece is scarce.',
        'The corrections are activated by monotone cutoffs. The first-download transitions change those cutoffs in a favorable direction; the remaining changes are bounded explicitly. One global function then has negative expected drift outside a finite set.',
        'The argument uses localized stopping times and a finite-mean return cycle to obtain recurrence. It does not assume in advance that a stationary distribution or a stationary population moment exists.',
    ],
    'limitations': [
        'This is the specified two-chunk model with one permanent seed, independently uniform fixed first choices, immediate departure after completion, and invisible empty waiting rooms. It is not a theorem for arbitrary file-sharing software or other chunk-selection protocols.',
        'There is no separate bound on the seed’s aggregate upload capacity beyond the displayed rates. In particular, many empty participants can contact the seed at once in this idealized model.',
        'The arrival rate is fixed and strictly positive; constants may depend on it. The theorem does not provide a bound uniform in λ, a stationary population moment, a completion-time estimate, a convergence rate, or geometric ergodicity. At λ=0 the zero state is absorbing, so the irreducibility statement does not apply.',
        'The target is the historical stability conjecture in the 2010 Oberwolfach report and the retained 2011 author proof. The 2009 preprint stated the opposite conjecture. The paper does not certify worldwide priority or that every later publication has been excluded.',
    ],
    'background': [
        {'title': 'Norros — On the stability of population processes', 'url': 'https://doi.org/10.4171/OWR/2010/48', 'note': 'Printed pages 2782–2783 state the deterministic-first-chunk stability conjecture despite instability of the large-system differential equations.'},
        {'title': 'Norros, Reittu and Eirola — On the stability of two-chunk file-sharing systems', 'url': 'https://hal.science/hal-00781341', 'note': 'Section 3.2, Figure 2 and Conjecture 3.6 of the retained January 5, 2011 author proof specify the model, including invisible empty waiting rooms, and conjecture stability.'},
        {'title': 'Norros, Reittu and Eirola — 2009 preprint', 'url': 'https://arxiv.org/abs/0910.5577v1', 'note': 'Figure 2 supplies the same transition rates, but this earlier version conjectures high-load instability. It must be distinguished from the later source.'},
        {'title': 'Meyn and Tweedie — Stability of Markovian processes III', 'url': 'https://doi.org/10.2307/1427522', 'note': 'Classical continuous-time Foster–Lyapunov criteria and localized Dynkin arguments provide the background stability method.'},
        {'title': 'Oguz, Anantharam and Norros — Stable, distributed P2P protocols based on random peer sampling', 'url': 'https://doi.org/10.1109/Allerton.2012.6483316', 'note': 'The Common Chunk protocol is a different all-load stable scheme: it samples the entire population and protects rare chunks before departure. Its theorem is not the DFC result.'},
    ],
    'collaboration': 'I welcome substantive collaboration from researchers in stochastic processes, queueing theory and distributed systems, especially on checking the recurrence argument, placing it precisely in the file-sharing literature, and developing a journal-ready treatment. Any coauthorship would reflect a substantive contribution to the research.',
    'follow_up': None,
    'followup_rationale': 'No follow-up is proposed: this scope review has not established a sufficiently strong, independently justified paper-worthy question or conjecture.',
    'publication_date': '2026-10-20', 'version': '1.0',
    'doi': '10.5281/zenodo.23524971', 'author': 'Alec Kriebel',
    'pdf_filename': 'dfc_stability.pdf', 'supplement_filename': None,
    'additional_assets': [{'filename': 'dfc_stability_verification.zip', 'label': 'Source and verification package (ZIP)'}],
    'status': 'Unrefereed preprint',
    'ai_disclosure': 'AI tools were used extensively in research, proof development, literature comparison, computation, manuscript preparation and adversarial auditing. Internal AI review does not constitute formal independent human peer review or proof-assistant certification.',
    'source_binding': binding, 'related_resources': [], 'candidate_only': True,
    'candidate_gate': 'Scope and attribution candidate only. Separate mathematical reviews and root publication approval are required; this content is not a mathematical PASS.',
}
save('content.json', content)
assert json.loads((HERE / 'content.json').read_text())['abstract'] == abstract
save('abstract-check.json', {
    'utc': NOW, 'status': 'PASS_SOURCE_FIDELITY_ONLY',
    'source': str((PACKAGE / 'main.tex').relative_to(BASE)), 'source_sha256': sha(PACKAGE / 'main.tex'),
    'normalizations': ['TeX line wrapping collapsed to spaces', 'TeX birth--death rendered as birth–death'],
    'complete_original_abstract': True, 'paragraphs': 1, 'candidate_sha256': sha(HERE / 'content.json'),
})
save('independence.json', {
    'role': 'scope', 'mathematical_verdict': None, 'strictly_blind': False,
    'current_sibling_opinions_read': False,
    'dedicated_historical_reviewer_bodies_read': False,
    'incidental_exposure': [
        {'utc': '2026-10-25T02:40:00Z', 'source': 'original/RESULT_ACCEPTED.md', 'timing': 'Approximate; while locating original proof, after full current PDF reading and before TURN_4.md reading.', 'content': 'Historical acceptance/PASS summary and old finite-check counts; not used as evidence; disclosed to root.'},
        {'source': 'record metadata, main.tex, reproduce.py, original/TURN_4.md, original/checks/turn4_checks.py', 'content': 'Author historical status/priority claims, expected-output constants and status-producing code text necessarily encountered; excluded as fresh validation evidence.'},
    ],
    'retained_primary_policy': 'Only two raw primary PDFs copied from an older private_sources folder; no adjacent assessment bodies or old source-reading judgments opened.',
    'no_submitted_math_execution': True,
})

primary_dir = HERE / 'cache/primary-sources'
primary_rows = []
for receipt_path in sorted(primary_dir.glob('receipt-*.json')):
    for r in json.loads(receipt_path.read_text()):
        row = dict(r); row['receipt_file'] = receipt_path.name
        if row.get('filename') and (primary_dir / row['filename']).exists():
            row['local_sha256_rechecked'] = sha(primary_dir / row['filename'])
        primary_rows.append(row)
save('primary-references.json', {'utc': NOW, 'retrievals': primary_rows})
interfaces = [
    {'source': 'nre-0910.5577v1.pdf', 'read': 'Section3.2/Figure2/Proposition3.3/Conjecture3.4, printed7–9', 'role': 'Original six rates; earlier opposite conjecture; not an imported DFC stability theorem.', 'access': 'Fresh arXiv v1 PDF'},
    {'source': 'owr-2010-48.pdf', 'read': 'Complete Norros contribution, printed2782–2783/PDF38–39', 'role': 'Historical stochastic stability conjecture, despite divergent deterministic large-system dynamics.', 'access': 'Fresh publisher PDF; remaining workshop contributions not claimed read'},
    {'source': 'nre-2011-retained-authorproof.pdf', 'read': 'Cover/header and introductory model; Section2 stability definition; complete Section3.2 printed10–12/PDF11–13', 'role': 'Invisible-waiting-room six-rate model and Conjecture3.6; stable means irreducible positive recurrence.', 'access': 'Retained raw authorproof, not freshly authenticated final publisher PDF'},
    {'source': 'meyn-tweedie-III.pdf', 'read': 'Sections1.2–1.3, comparison/Dynkin interface, Section4.1 and Theorems4.1–4.3/proofs, printed520–523,528–531', 'role': 'Nonexplosive right process, truncated-generator CD2, closed petite finite set and bounded V there; f=1 gives positive recurrence but no population-moment bound.', 'access': 'Fresh author-hosted published scan'},
    {'source': 'oguz-allerton-2012-retained.pdf', 'read': 'Entire5pages/printed915–919 including operative protocol and proof', 'role': 'Different entire-population three-sample Common Chunk model; theorem and final rare-chunk conjecture not DFC.', 'access': 'Retained raw conference PDF; fresh mirror attempts failed'},
    {'source': 'oguz-technical-report-2012.pdf', 'read': 'Title/front matter only', 'role': 'Different longer technical report; not substituted for conference article or used to establish theorem transfer.', 'access': 'Fresh Berkeley repository PDF'},
]
for row in interfaces:
    row['sha256'] = sha(primary_dir / row['source'])
save('primary-interfaces.json', {'utc': NOW, 'interfaces': interfaces, 'limits': ['No final2011 publisher body or final2015 journal extension acquired/read.', 'No worldwide novelty or present-day openness certification.', 'Full current proof mapped; correctness remains with independent mathematical reviews.']})
inspected = {'main.tex': 'complete current mathematical source', 'paper.pdf': 'all6pages duplicate current manuscript', 'original/TURN_4.md': 'complete original all-state proof', 'original/checks/turn4_checks.py': 'full exact-rational selected-load control implementation, not executed', 'reproduce.py': 'full reproduction entrypoint, not executed', 'original/RESULT_ACCEPTED.md': 'incidental historical status summary; excluded as evidence', 'MANIFEST.json': 'integrity entries only'}
support = []
for row in integrity['members']:
    rel = Path(row['path']).relative_to(Path('published-source/dfc_stability_verification/dfc_stability_verification')).as_posix()
    if rel in inspected:
        use = inspected[rel]
    elif rel.endswith('.py'):
        use = 'mapped mathematical/support program; body not read in scope role and not executed'
    else:
        use = 'mapped/hash-checked only; body kept opaque or unnecessary to current proof scope'
    support.append({'path': row['path'], 'sha256': row['sha256'], 'scope_use': use})
save('support-map.json', {'utc': NOW, 'all_members': support, 'math_execution_claim': False})

with (HERE / 'research-log.md').open('a') as f:
    f.write('\n## ' + NOW + ' — 100% of acquisition/scope assignment\nComplete six-page manuscript, source and original full proof mapped; exact original conjecture/version and classical stability interfaces read. Conditional full-abstract content prepared. Both public assets, all92 extracted files and package manifest rechecked unchanged. No mathematical program execution or mathematical PASS claimed. Historical status exposure disclosed; retained-primary versus fresh-acquisition distinctions preserved. Mathematical correctness and publication remain separate gates.\n')

artifact_rows = []
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name not in {'artifact-manifest.json', 'verdict.json'}:
        artifact_rows.append({'path': p.relative_to(HERE).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)})
save('artifact-manifest.json', {'utc': NOW, 'files': artifact_rows})
save('verdict.json', {
    'schema_version': 1, 'record_id': '23524971', 'doi': '10.5281/zenodo.23524971',
    'role': 'scope', 'status': 'SCOPE_COMPLETE', 'mathematical_verdict': None,
    'publication_clearance': False, 'completed_utc': NOW, 'completion_percent': 100,
    'source_binding': {
        'pdf_filename': 'dfc_stability.pdf', 'pdf_sha256': by_name['dfc_stability.pdf']['sha256'],
        'source_zip_filename': 'dfc_stability_verification.zip', 'source_zip_sha256': by_name['dfc_stability_verification.zip']['sha256'],
        'record_sha256': sha(SOURCES / 'record.json'), 'receipt_sha256': sha(SOURCES / 'receipt.json'),
        'extraction_integrity_sha256': sha(SOURCES / 'extraction-integrity.json'), 'reader_map_sha256': sha(SOURCES / 'reader-pdf-map.json'),
        'public_assets': public,
    },
    'coverage': {'current_manuscript_pages': 6, 'all_current_pages_read': True, 'distinct_reader_pdfs': 1, 'embedded_reader_is_duplicate': True, 'original_full_proof_read': True, 'current_reproduction_entrypoint_inspected': True, 'mathematical_programs_executed': False, 'historical_status_summary_incidentally_read': True, 'dedicated_historical_reviewer_bodies_read': False, 'sibling_findings_read': False},
    'strongest_scope_result': 'All public bytes authenticated; exact current model, all-fixed-positive-load claim, original question, proof/support and primary stability interfaces mapped; full original abstract and conditional content prepared.',
    'remaining_gate': 'Independent mathematical reviews and root assessment; no theorem-correctness or publication approval is supplied by this scope result.',
    'exact_scope': 'N0^4 six-rate continuous-time DFC chain, fixed finite real lambda>0, any finite state, uniform fixed first choice, permanent seed, invisible empty waiting rooms, immediate completion departure; no separately capped aggregate seed capacity.',
    'excluded_claims': ['lambda=0 irreducibility', 'uniform-in-lambda estimates', 'stationary population moments', 'geometric ergodicity or performance bounds', 'many chunks or other protocols', 'infinite initial state', 'worldwide novelty/current-openness certification'],
    'primary_body_access_limits': ['NRE2011 authorproof and Allerton2012 conference body read from retained raw PDFs, not newly authenticated publisher downloads.', 'Final2011 publisher and final2015 journal bodies not acquired/read.', 'Berkeley2012 technical report only front matter read; not substituted for the conference paper.'],
    'independence_file': 'independence.json',
    'candidate': {'file': 'content.json', 'sha256': sha(HERE / 'content.json'), 'candidate_only': True, 'full_abstract_fidelity': 'PASS_SOURCE_FIDELITY_ONLY', 'follow_up': None},
    'unchanged_originals': {'public_assets': 2, 'extracted_regular_files': 92},
    'artifacts': {'report': 'REVIEW.md', 'report_sha256': sha(HERE / 'REVIEW.md'), 'manifest': 'artifact-manifest.json', 'manifest_sha256': sha(HERE / 'artifact-manifest.json'), 'primary_interfaces': 'primary-interfaces.json', 'primary_interfaces_sha256': sha(HERE / 'primary-interfaces.json')},
})
print(json.dumps({'status': 'SCOPE_COMPLETE', 'math_verdict': None, 'report_sha256': sha(HERE / 'REVIEW.md'), 'content_sha256': sha(HERE / 'content.json'), 'verdict_sha256': sha(HERE / 'verdict.json'), 'artifact_count': len(artifact_rows)}, indent=2))
